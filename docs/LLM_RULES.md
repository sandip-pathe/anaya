# Optional OpenAI Judge

Anaya is deterministic by default. LLM-backed rules run only when a repository
config opts in with `llm.enabled: true` and OpenAI settings are available.

Install the optional dependency when you want live OpenAI judging:

```bash
python -m pip install -e .[llm]
```

For local development with tests:

```bash
python -m pip install -e .[dev,llm]
```

## Environment

```bash
ANAYA_OPENAI_API_KEY=your-openai-api-key
ANAYA_OPENAI_MODEL=gpt-4o-mini
ANAYA_OPENAI_MAX_TOKENS=300
ANAYA_OPENAI_TEMPERATURE=0.1
ANAYA_OPENAI_TIMEOUT_SECONDS=10
```

The runtime caps output tokens at 300, temperature at 0.1, and request timeout
at 10 seconds even if larger values are configured.

## Repository Opt-In

```yaml
packs:
  - policies/custom-llm.yml

llm:
  enabled: true
```

Without `llm.enabled: true`, `type: llm` rules are not counted or executed.
When LLM is enabled but `ANAYA_OPENAI_API_KEY` is missing, the scan finishes
with a warning and no LLM findings.

## Rule Schema

```yaml
pack:
  id: custom/ambiguous-audit
  version: 1.0.0

rules:
  - id: CUSTOM-LLM-001
    name: Ambiguous Audit Evidence
    description: Use OpenAI only where deterministic checks are insufficient.
    type: llm
    severity: HIGH
    languages: [python]
    llm:
      scope: file
      prompt: "Decide whether this code clearly records audit evidence for sensitive actions."
    message: "OpenAI judge returned {status}: {reason}"
    fix_hint: "Add explicit audit evidence or replace this with a deterministic rule."
```

Supported scopes:

- `file`: sends the source file as one bounded judgment task.
- `function`: sends each Python function as a bounded judgment task.

Function scope is intentionally not line-by-line. JavaScript/TypeScript
function scoping will land with the later JavaScript AST milestone.

## Failure Behavior

- OpenAI output must be structured JSON with `PASS`, `WARN`, or `FAIL`.
- `PASS` produces no finding.
- `WARN` and `FAIL` produce a finding using the rule severity.
- Invalid JSON, invalid structured output, missing credentials, timeouts, or API
  errors produce scan warnings, not violations.
- GitHub/API scans surface warnings in Check Run summaries.

When enabled, source code for the configured scope is sent to OpenAI. Do not
enable LLM rules for repositories where that data handling is not acceptable.
