# Policy Pack Authoring

Anaya's engine is policy-pack agnostic. Built-in packs are just YAML files, and
external policy packs use the same schema. The OSS CLI must always support
user-authored packs.

## Use A Custom Pack

```bash
anaya scan . --pack path\to\my-policy-pack.yml
anaya validate-pack path\to\my-policy-pack.yml
anaya test-rule --rule ACME-PAY-001 --file tests\fixtures\dirty.py --pack path\to\my-policy-pack.yml
```

`anaya.yml` can also reference custom pack paths:

```yaml
version: "1"

packs:
  - id: generic/secrets-detection
  - ./policies/internal-payments.yml
```

## Pack Shape

```yaml
pack:
  id: "acme/internal-payments"
  version: "1.0.0"
  name: "Internal Payments Policy"
  description: "Checks internal payment-code rules"
  last_updated: "2026-06-06"
  authors: ["Acme Security"]
  sources:
    - url: "https://example.com/policy"
      title: "Internal policy"

rules:
  - id: "ACME-PAY-001"
    name: "No Debug Payment Bypass"
    description: "Payment bypass flags must not be committed."
    type: pattern
    severity: CRITICAL
    languages: [python, javascript, typescript]
    patterns:
      - regex: 'debug_payment_bypass\s*=\s*True'
        description: "Matches enabled payment bypass flags."
        exclude_patterns:
          - "noqa"
    message: "Debug payment bypass is enabled at line {line}."
    fix_hint: "Remove the bypass or guard it behind an approved test-only fixture."
    references:
      - url: "https://example.com/policy#payment-bypass"
        title: "Payment bypass policy"
    tags: ["payments", "internal"]
    enabled: true
```

## Rule Types

Current:

- `pattern`: deterministic regex rules.
- `ast`: structural Python rules for function-level missing-call checks.

Planned:

- `llm`: optional OpenAI-backed fallback rules, disabled by default and never required for OSS use.

AST rules currently support this shape:

```yaml
type: ast
languages: [python]
ast:
  node_type: function
  name_matches: "(transfer|debit|credit)"
  must_contain:
    - "(audit|record_audit|emit_audit)"
  if_missing: flag
```

The rule flags a matching top-level Python function when no call in the function
body matches any `must_contain` pattern.

## Design Rules

- Do not hardcode policy behavior in Python when YAML can express it.
- Prefer deterministic rules before OpenAI-assisted review.
- Every rule should have dirty, clean, and edge-case fixtures.
- Rule IDs must be globally unique within a pack ecosystem.
- Pack authors should include practical `fix_hint` values; developers need a next step, not just a violation.

## Testing A Rule

Use `test-rule` while authoring a pack. It runs one rule against one file using
the same engine path as `scan`, which makes it useful for debugging regexes,
suppression behavior, and expected snippets.

```bash
anaya test-rule --rule ACME-PAY-001 --file tests\fixtures\dirty.py --pack policies\payments.yml
anaya test-rule --rule ACME-PAY-001 --file tests\fixtures\clean.py --pack policies\payments.yml
```
