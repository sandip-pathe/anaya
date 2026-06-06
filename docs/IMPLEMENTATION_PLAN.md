# Anaya Implementation Plan

Status: Draft v1  
Date: 2026-06-06  
Inputs: `ANAYA_SPEC.py`, `deck.html`, `rbi-compliance-scanner`, `fintech-demo`, current `anaya/` scaffold

## 1. Product Intent

Anaya is a policy-pack-agnostic compliance-as-code engine that turns policy requirements into executable code checks at pull request time.

The V1 product has two surfaces over one shared engine:

- CLI: local developer and CI usage through `anaya scan`. The CLI is OSS, similar in spirit to Semgrep.
- GitHub App: PR-native checks through GitHub Check Runs, inline annotations, and SARIF upload

The product thesis from the deck is: compliance fails in code, not in policy decks. Developers miss regulatory constraints because the signal is trapped in PDFs, circulars, and review processes instead of appearing in the pull request where code changes happen.

V1 must stay narrow:

- No web dashboard
- No billing system
- No Slack/Jira bot
- No runtime monitoring
- Deterministic scanners first; OpenAI-backed LLM fallback only when explicitly enabled

## 2. Business And Packaging Direction

Open core:

- Free/MIT:
  - Engine core
  - CLI
  - GitHub Action or self-hosted workflow
  - Generic rule packs
  - User-authored custom policy packs
  - Community rule packs
  - Limited hosted GitHub App tier later
- Paid/proprietary later:
  - RBI, SEBI, DPDP packs
  - PCI-DSS, SOC2, ISO 27001 packs
  - Auto-updating regulation packs
  - Organization policy controls
  - Audit exports
  - Scan history and trends
  - Custom rule builder

V1 should prove developer value before monetization: install, scan, PR annotation, and trustworthy findings.

## 3. Current State

### Existing Prototype: `rbi-compliance-scanner`

Useful as reference:

- GitHub App JWT and installation-token flow in `github_utils.py`
- Webhook HMAC signature verification in `github_app.py`
- Basic GitHub API patterns for fetching PR files and posting feedback
- RBI demo corpus and generated audit examples

Do not port:

- Agent/orchestrator engine
- AI-first judging model
- Old rule YAML
- Synchronous Flask PR handler
- PR-comment/commit-status output model
- Hardcoded `main.py` scan target behavior

Security cleanup already started:

- `private-key.pem` removed from Git tracking in the prototype repo
- `*.pem` ignored
- Local key file still exists, but the key must be rotated because it was already committed

### New App: `anaya/`

Already implemented:

- Python package scaffold
- CLI with `scan`, `init`, `validate-pack`, `packs list`
- Engine dataclasses
- Rule pack loader with validation
- Repository config discovery from `anaya.yml`
- Pattern scanner
- Inline rule suppression support
- Table, JSON, and SARIF-ish reporters
- Generic packs:
  - `generic/secrets-detection`
  - `generic/owasp-top10`
  - `generic/pii-handling`
  - `generic/tls-encryption`
- `generic/audit-logging`
- 26 deterministic built-in rules
- Python and JavaScript dirty/clean fixture matrix
- `anaya test-rule --rule RULE_ID --file FILE`
- Tests passing and Ruff clean

Known gaps:

- No AST scanner yet
- Audit logging pack is pattern-based; structural missing-audit detection waits for AST scanner
- SARIF has contract tests but still needs full schema validation
- Table output is plain text with metadata, not Rich-polished
- Diff-file scanning exists; changed-line-aware annotations are still future work
- No GitHub App in the new app
- No FastAPI, Celery, Redis, or Docker yet
- No GitHub Check Runs API
- No GitHub Code Scanning SARIF upload
- No LLM fallback module
- No OpenAI integration module yet

## 4. Target Architecture

```text
GitHub PR
  -> Webhook POST /webhook
  -> FastAPI verifies signature
  -> Create Check Run: in_progress
  -> Dispatch Celery task scan_pr(repo, pr, sha, installation)
  -> Worker fetches anaya.yml from default branch
  -> Worker fetches PR diff files
  -> Shared Anaya engine loads packs
  -> Pattern scanner + AST scanner + optional OpenAI judge
  -> Reporters produce Check Run annotations + SARIF + summary
  -> GitHub Check Run completed
  -> Optional SARIF upload to Code Scanning
```

CLI uses the same engine:

```text
anaya scan PATH
  -> discover anaya.yml
  -> resolve packs
  -> collect files or diff files
  -> run shared engine
  -> render table/json/sarif
  -> exit 1 on fail threshold
```

## 5. Engineering Principles

1. YAML is the source of truth for rules.
   Rule behavior belongs in pack YAML except scanner mechanics.

2. Deterministic by default.
   Pattern and AST checks run first. OpenAI checks are opt-in and non-blocking on failure.

3. GitHub-native output.
   V1 should use Check Runs and annotations, not only PR comments.

4. Diff-first scanning.
   PRs scan changed files/lines by default. Full repo scan is explicit.

5. Fast enough for PR flow.
   Target: under 30 seconds for a typical PR with 10 files and roughly 500 changed lines.

6. Trust over cleverness.
   Dedupe findings, avoid noisy duplicates, support suppressions, and explain fixes clearly.

## 6. Milestone Plan

### M0. Security And Repository Hygiene

Goal: make the work safe to continue and publish.

Tasks:

- Rotate the committed GitHub App private key.
- Rotate the GitHub webhook secret.
- Rotate old prototype AI-provider keys and any OpenAI keys that appeared in local `.env`.
- Decide whether to rewrite old repo history or archive the old repo as compromised-prototype history.
- Add `.gitignore` coverage for `.env`, `*.pem`, generated outputs, caches, and local secrets.
- Create a fresh Git repo for `anaya/` or move it into the intended main repo.
- Add `LICENSE` if open-core engine is MIT.

Acceptance:

- No private key is tracked.
- `git status --ignored` shows local PEM ignored.
- New app has no committed secrets.
- Secret rotation documented in a short security note.

### M1. Package And Project Foundation

Goal: make Anaya installable and pleasant for contributors.

Tasks:

- Update `README.md` to reflect current four packs and exact commands.
- Add `LICENSE`.
- Add `CHANGELOG.md`.
- Add `CONTRIBUTING.md`.
- Add `Makefile` or `justfile` equivalents for:
  - `test`
  - `lint`
  - `format`
  - `scan-fixtures`
- Add GitHub Actions CI:
  - install
  - ruff
  - pytest
  - package build
- Add `pytest-cov` and coverage target.
- Decide whether `cli` remains top-level or moves to `anaya/cli`.
- Replace dataclass settings with `pydantic-settings` per spec.

Acceptance:

- `pip install -e .[dev]` works from a clean checkout.
- `anaya --help` works.
- CI runs tests and lint.
- Coverage reports for `anaya/engine`.

### M2. Engine Completion

Goal: make the deterministic engine solid enough to trust.

Tasks:

- Extend rule schema validation:
  - pack metadata required fields
  - SemVer validation
  - unique rule IDs
  - valid severities
  - valid languages
  - valid references
  - invalid regex diagnostics
- Add config validation:
  - unknown packs
  - unknown rules in ignore list
  - invalid thresholds
  - invalid scan mode
- Add language filtering from `anaya.yml`.
- Add file collection improvements:
  - hidden directories
  - symlink behavior
  - binary file skip
  - max file size guard
- Add diff scanning:
  - `--diff REF`
  - changed files only
  - future: changed lines only for annotations
- Add robust dedupe:
  - `(file, line, rule_id, snippet)` as primary key
  - avoid duplicate pattern matches on one line
- Add suppression tests:
  - Python `# noqa: RULE`
  - JavaScript `// noqa: RULE`
  - generic `noqa: anaya`
- Improve `ScanSummary`:
  - include rules checked by pack
  - include skipped file counts and reasons
  - include config path used
  - include pack versions

Acceptance:

- Engine tests cover valid/invalid packs and config.
- External custom policy packs can be loaded and scanned by the OSS CLI.
- No duplicate findings for same file/line/rule.
- Dirty fixtures trigger expected rules.
- Clean fixtures pass.
- `--diff` scans only changed files.

### M3. Rule Packs And Fixture Matrix

Goal: complete V1 generic packs with 20+ tested rules.

Current pack status:

- Secrets: 6 rules
- OWASP: 8 rules
- PII: 5 rules
- TLS: 4 rules
- Audit logging: 3 pattern rules
- Total: 26 rules

Combined M3/M4 pass status:

- Built-in packs load as 5 generic OSS packs.
- Dirty Python and JavaScript matrix fixtures assert exact expected rule IDs.
- Clean Python and JavaScript fixtures pass.
- Suppression edge fixture passes.
- Remaining later upgrade: replace audit logging heuristics with AST-based missing-audit detection in M6.

Tasks:

- Complete `generic/owasp-top10.yml` to 8 rules:
  - SQL injection
  - command injection
  - unsafe eval
  - path traversal
  - weak crypto
  - insecure deserialization
  - SSRF pattern
  - disabled CSRF protection
- Complete `generic/pii-handling.yml` to 5 rules:
  - PII in logs
  - PII in API responses
  - PII in error messages
  - PII in comments/docstrings
  - unmasked PII in string formatting
- Complete `generic/tls-encryption.yml` to 4 rules:
  - TLS verification disabled
  - insecure HTTP URL
  - weak TLS versions
  - database SSL disabled/missing
- Add `generic/audit-logging.yml` with 3 deterministic pattern rules now:
  - audit logging disabled
  - transaction audit bypass
  - authentication audit bypass
- Add Python fixtures:
  - dirty and clean per rule
  - edge cases per rule
  - suppressions
- Add JavaScript/TypeScript fixtures:
  - dirty and clean per supported JS rule
  - suppressions
- Add golden expected rule IDs for fixture directories.
- Run false-positive sanity checks on known clean codebases.

Acceptance:

- At least 5 generic packs load.
- At least 20 total rules.
- Every rule has:
  - one dirty fixture
  - one clean fixture
  - one edge case
- Fixture tests assert exact expected rule IDs.
- False-positive report exists or is tracked through a manual noise-review checklist.

### M4. CLI Productization

Goal: make `anaya scan` good enough for real developer use.

Combined M3/M4 pass status:

- `scan`, `init`, `validate-pack`, `test-rule`, and `packs list` exist.
- Output files create parent directories.
- Table output includes status, counts, pack versions, skipped files, fix hints, and no-finding state.
- JSON and SARIF reporter contracts are tested.
- Exit-code behavior is tested for pass, fail-threshold findings, and invalid config.
- Remaining later polish: Rich visual formatting, overwrite policy, GitHub Action example docs, and full SARIF schema validation.

Tasks:

- Polish Typer command hierarchy:
  - `anaya scan [PATH]`
  - `anaya init`
  - `anaya validate-pack PATH`
  - `anaya test-rule --rule RULE_ID --file FILE`
  - `anaya packs list`
- Add Rich table output:
  - pack status table
  - severity counts
  - grouped findings
  - readable fix hints
  - no-color mode
- Add output file behavior:
  - create parent dirs
  - refuse overwrite unless explicit? decide
  - stdout by default
- Add JSON output contract tests.
- Add SARIF output contract tests.
- Add exit-code tests:
  - 0 pass
  - 1 fail threshold findings
  - 2 invalid config/pack/usage if desired
- Add CLI docs with copy-paste examples.
- Add a self-hosted GitHub Action example:
  - install Anaya
  - run `anaya scan --diff origin/main --format sarif`
  - upload SARIF with GitHub tooling

Acceptance:

- New user can install and scan a sample project.
- CLI output is stable and tested.
- JSON output is useful in CI.
- SARIF output validates.

### M5. Reporter Hardening

Goal: make outputs suitable for GitHub and enterprise workflows.

Tasks:

- SARIF 2.1.0:
  - validate with schema
  - include tool metadata
  - include rule metadata
  - include help URIs
  - include regions with start line/column
  - normalize paths
  - support Windows and POSIX paths
- Check Run reporter:
  - title
  - summary markdown
  - annotation formatting
  - severity to annotation level
  - 50-annotation batching
  - overflow summary when more than 50 annotations
- PR summary comment reporter:
  - optional, not primary
  - concise summary with links to Check Run
- Audit report JSON:
  - scan metadata
  - rules applied
  - violations
  - versions
  - timestamps
  - suitable later for paid exports

Acceptance:

- SARIF uploads cleanly to GitHub Code Scanning.
- Check Run payloads are unit-tested.
- Large result sets batch correctly.

### M6. AST Scanner

Goal: support structural rules that regex cannot express.

Tasks:

- Add tree-sitter dependencies:
  - `tree-sitter`
  - `tree-sitter-python`
  - `tree-sitter-javascript`
- Implement `anaya/engine/scanners/ast_scanner.py`.
- Support AST pattern schema:
  - `node_type`
  - `name_matches`
  - `must_contain`
  - `if_missing: flag`
- Support Python and JavaScript first.
- Route rules by type in orchestrator:
  - pattern rules to PatternScanner
  - ast rules to AstScanner
  - llm rules later
- Implement audit-logging pack.
- Add fixtures:
  - transfer/debit/credit/disburse with audit log
  - transfer/debit/credit/disburse without audit log
  - login without attempt logging
  - delete without deletion audit trail

Acceptance:

- Detects missing audit logging in Python and JavaScript.
- Clean structural fixtures pass.
- AST parse errors are reported as warnings/skips, not crashes.

### M7. GitHub App Foundation

Goal: create the hosted GitHub App surface using the shared engine.

Tasks:

- Add dependencies:
  - FastAPI
  - uvicorn
  - httpx
  - PyJWT[crypto]
  - pydantic-settings
- Implement `anaya/api/app.py`.
- Implement `anaya/api/health.py`.
- Implement `anaya/api/webhooks.py`.
- Port only:
  - webhook HMAC signature verification from old `github_app.py`
  - JWT/token logic from old `github_utils.py`
- Rewrite:
  - GitHub client as async `httpx`
  - Check Runs API
  - file fetching
  - config fetching from default branch
- GitHub permissions:
  - checks: write
  - contents: read
  - pull_requests: read
  - metadata: read
  - code_scanning_alerts/security_events if SARIF upload requires it
- Webhook events:
  - pull_request
  - installation

Webhook flow:

1. Verify signature.
2. Parse event.
3. If PR action is opened/synchronize/reopened:
   - extract repo, PR number, head SHA, installation ID
   - create Check Run in progress
   - dispatch background task
   - return 202 quickly
4. Ignore other events with 200.

Acceptance:

- `/health` returns 200.
- Invalid webhook signatures return 403.
- PR webhook returns 202 in under 1 second.
- Check Run is created immediately.

### M8. Async Worker And GitHub Scan Flow

Goal: make GitHub App scans reliable and non-blocking.

Tasks:

- Add Redis and Celery.
- Add `anaya/worker/tasks.py`.
- Add Docker Compose with Redis.
- Cache installation tokens in Redis:
  - key `anaya:gh_token:{installation_id}`
  - TTL 3300 seconds
- Implement `scan_pr` task:
  - fetch default-branch `anaya.yml`
  - fetch PR changed files
  - filter deleted/renamed/binary files
  - fetch file contents at head SHA
  - run engine
  - update Check Run
  - upload SARIF
- Add retry behavior:
  - GitHub 401 refresh token
  - 429 backoff
  - transient 5xx retry
- Add failure behavior:
  - update Check Run as failure/error with actionable message
  - do not leave infinite in-progress checks

Acceptance:

- Local ngrok/manual test:
  - install GitHub App on test repo
  - open PR
  - Check Run appears as in_progress
  - scan completes
  - annotations appear inline
  - SARIF appears in Code Scanning
- Webhook response time under 1 second.
- Typical scan under 30 seconds.

### M9. Optional OpenAI Judge

Goal: add OpenAI-assisted reasoning only where deterministic rules are insufficient.

Tasks:

- Add optional extra dependency:
  - `openai`
- Add `anaya/llm/judge.py`.
- Add `anaya/llm/prompts.py`.
- Support `type: llm` rules.
- Enforce guards:
  - only runs when `llm.enabled: true`
  - file-scope or function-scope, not line-by-line
  - OpenAI model configured through Anaya settings
  - max tokens capped at 300
  - temperature 0.1
  - 10 second timeout
  - one retry on 429/500
  - on error: skip with warning, never default to violation
- Use structured JSON output:
  - PASS/WARN/FAIL
  - confidence
  - reason
  - optional line number

Acceptance:

- No live OpenAI calls in tests.
- Mocked LLM responses produce deterministic outcomes.
- API failure never blocks or creates false violations.
- LLM rules disabled by default.

### M10. Deployment And Demo Readiness

Goal: make the product usable by a design partner or demo repo.

Tasks:

- Add Dockerfile.
- Add docker-compose with Redis and app.
- Add deployment docs:
  - local dev with ngrok
  - production environment variables
  - GitHub App creation
  - GitHub App permissions
  - secret rotation
- Add sample `anaya.yml`.
- Add demo walkthrough using `fintech-demo`.
- Add screenshot or terminal transcript docs.
- Add troubleshooting docs:
  - missing private key
  - invalid webhook secret
  - GitHub permission error
  - SARIF upload rejected
  - no files scanned

Acceptance:

- A new developer can run the GitHub App locally in under 15 minutes.
- A PR in a test repo produces visible findings.
- Demo script is repeatable.

### M11. Regulatory Pack Path: RBI/SEBI/DPDP

Goal: preserve the paid/regulatory future without blocking V1.

Tasks:

- Keep RBI prototype separate until V1 generic engine is stable.
- Create a private/proprietary pack namespace later:
  - `india/rbi-data-security`
  - `india/dpdp-privacy`
  - `india/sebi-cybersecurity`
- Translate RBI prototype ideas into new schema.
- Avoid AI-first compliance judgment.
- Add references to regulations in YAML.
- Add audit export metadata.
- Add stronger fixture corpus from `fintech-demo`.

Acceptance:

- RBI pack uses same engine and reporters.
- No special-case RBI code in engine.
- Pack can be distributed separately from open-core engine.

## 7. Testing Strategy

Test layers:

- Unit:
  - rule loader
  - config loader
  - file collection
  - scanner behavior
  - reporters
  - GitHub auth
- Integration:
  - CLI scans fixture directories
  - SARIF generation
  - Check Run payloads
  - webhook handler with fake payloads
  - worker task with mocked GitHub client
- Golden fixtures:
  - dirty/clean expected findings
  - exact rule IDs
  - suppressed lines
  - ignored paths
- Manual:
  - ngrok GitHub App test
  - SARIF Code Scanning upload
  - branch protection behavior
- Performance:
  - typical PR: 10 files, 500 changed lines, under 30 seconds
  - large result set annotation batching

Coverage target:

- Over 80% on `anaya/engine`
- Higher bar for `rule_loader`, `repo_config`, and reporters

## 8. Developer Experience Requirements

Time to first value target:

- CLI: under 5 minutes
- GitHub App local dev: under 15 minutes

CLI happy path:

```bash
pip install anaya
anaya init
anaya scan .
```

CI happy path:

```bash
anaya scan --diff origin/main --format sarif -o anaya.sarif
```

Error messages must explain:

- what failed
- why it failed
- how to fix it
- which file/config/pack is involved

Examples:

- Invalid regex in pack: show pack path, rule ID, regex, and parser error.
- Unknown pack: show attempted ID and available pack IDs.
- No files scanned: explain supported extensions and ignores.
- GitHub permission denied: show required permission.

## 9. Security Requirements

Hard requirements:

- Never commit keys or `.env`.
- Support raw PEM through env var for deployed environments.
- Validate webhook signatures with HMAC-SHA256.
- Fetch `anaya.yml` from default branch for PR scans, not from PR branch.
- Avoid executing user code.
- Treat scanned content as untrusted.
- Do not send code to LLM unless `llm.enabled: true`.
- If LLM enabled, document data handling clearly.
- Avoid logging file contents, secrets, or full snippets in hosted logs.
- Rotate old prototype keys before any push/deploy.

## 10. Repository Organization Decision

Preferred path:

- Make `C:\x\git-app\anaya` the new canonical product repo.
- Keep `rbi-compliance-scanner` as archived prototype/reference.
- Keep `fintech-demo` as demo/fixture corpus, eventually move selected cases into `anaya/tests/fixtures`.

Alternative:

- Move `anaya/` into the existing `rbi-compliance-scanner` repo and rename repo.

Recommendation:

- Use a fresh Anaya repo. The prototype history contains a private key and hackathon code that the spec explicitly says not to port.

## 11. Open Decisions

1. Canonical repo location:
   - Fresh Anaya repo recommended.

2. History cleanup:
   - Rotate keys either way.
   - Decide whether old repo history rewrite is worth the disruption.

3. Hosted GitHub App timeline:
   - Build CLI + GitHub Action first, or GitHub App immediately after engine?
   - Recommendation: CLI + SARIF first, then GitHub App.

4. Rule-pack licensing:
   - Confirm generic packs are MIT.
   - Confirm RBI/SEBI/DPDP are private/proprietary.

5. LLM timing:
   - Spec places LLM in Phase 7.
   - Recommendation: keep OpenAI integration late. It is not needed to prove V1.

6. Tree-sitter scope:
   - Python and JavaScript first.
   - TypeScript soon after if dependency ergonomics are smooth.

## 12. Suggested Execution Order

Next 10 concrete tasks:

1. Add full SARIF 2.1.0 schema validation.
2. Add GitHub Action example docs.
3. Add Rich table rendering while preserving `--no-color`.
4. Decide output overwrite policy.
5. Add AST scanner.
6. Upgrade audit logging pack from bypass patterns to missing-audit structural rules.
7. Add TypeScript fixture matrix.
8. Run false-positive review on `fintech-demo` and capture findings.
9. Add FastAPI app and health endpoint.
10. Port webhook signature verification.

After that:

11. Port GitHub App JWT/token logic with `httpx`.
12. Implement Check Runs API.
13. Implement Celery worker and Redis token cache.
14. End-to-end GitHub App test on a demo repo.
15. Add optional OpenAI judge.
16. Prepare deployment/demo docs.

## 13. V1 Definition Of Done

V1 is complete when all are true:

- `anaya scan ./some-project` works locally.
- SARIF output is valid and uploadable to GitHub Code Scanning.
- GitHub App installed on a test repo:
  - PR opened creates Check Run in progress.
  - Scan completes and updates Check Run.
  - Violations appear inline in PR diff.
  - SARIF is uploaded to Code Scanning.
  - Merge can be blocked on critical violations via branch protection.
- 5 generic packs exist with at least 20 total rules.
- Every rule has dirty, clean, and edge-case fixtures.
- No hardcoded rule logic in Python beyond scanner mechanics.
- Typical PR scan finishes in under 30 seconds.
- Webhook response time is under 1 second.
- Engine test coverage is over 80%.

## 14. Product Demo Script

CLI demo:

1. Show `fintech-demo` as an ordinary lending codebase.
2. Run `anaya init`.
3. Run `anaya scan ../fintech-demo --no-config --format table`.
4. Show findings grouped by severity and pack.
5. Run `anaya scan ../fintech-demo --format sarif -o anaya.sarif`.
6. Show JSON/SARIF artifacts.

GitHub demo:

1. Install Anaya GitHub App on demo repo.
2. Open PR with hardcoded secret and PII logging.
3. Show Check Run in progress.
4. Show completed Check Run with annotations.
5. Show Code Scanning SARIF result.
6. Show branch protection blocking merge on CRITICAL.

Narrative:

- The developer does not need to read a 40-page policy PDF.
- The rule appears where the code change happens.
- The output explains the problem and the fix.
- The same engine works locally, in CI, and in GitHub App mode.
