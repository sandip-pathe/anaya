# Manual Product Checks

These checks are for human judgment, not automated correctness. Run them after a
green test/lint pass when you want to sanity-check the product feel.

## 1. CLI Output Readability

```bash
anaya scan tests\fixtures\python\dirty\security_matrix.py --no-config --format table
anaya test-rule --rule ANAYA-OWASP-007 --file tests\fixtures\python\dirty\security_matrix.py --no-config
```

Check:

- Is the summary easy to understand in under 30 seconds?
- Are the rule names and fix hints actionable?
- Does the volume of findings feel scannable, or too noisy?

## 2. Clean Fixture Confidence

```bash
anaya scan tests\fixtures\python\clean --no-config
anaya scan tests\fixtures\javascript\clean --no-config
```

Check:

- Both scans should pass with `No findings.`
- If anything fires, the rule is probably too noisy for V1.

## 3. Real Or Demo Repo Noise

```bash
anaya scan C:\x\git-app\fintech-demo --no-config --format table
```

Check:

- Which findings feel genuinely useful?
- Which findings look like false positives?
- Are there obvious policy problems in the repo that Anaya misses?

## 4. SARIF Smoke

```bash
anaya scan tests\fixtures\python\dirty\security_matrix.py --no-config --format sarif -o anaya.sarif
```

Check:

- The file should be created.
- Open it briefly and confirm it is JSON with `version` set to `2.1.0`.
