# M0 Security Rotation Note

Date: 2026-06-06

## Current Status

- `rbi-compliance-scanner/private-key.pem` was removed from Git tracking in
  commit `d1876b2`.
- Local PEM files are ignored by both the prototype and Anaya repositories.
- `anaya/` contains no real runtime secrets; only placeholder values are present
  in `.env.example`.
- `anaya/` is intended to become the fresh canonical repository.

## Required External Rotation

The following actions require access to external service dashboards and must be
done outside this local workspace:

1. GitHub App private key:
   - Generate a new private key.
   - Revoke/delete the old key.
   - Replace the local ignored PEM with the new key.

2. GitHub webhook secret:
   - Generate a new strong webhook secret.
   - Update GitHub App settings.
   - Update local `.env`.

3. Legacy AI-provider API key from the old prototype, if present:
   - Revoke the old key.
   - Do not add non-OpenAI LLM configuration to Anaya.

4. OpenAI API key:
   - Revoke the old key.
   - Generate a new key.
   - Update local `.env`.

Anaya uses OpenAI for any future optional LLM fallback. Other LLM providers
belong only to archived prototype context and should not be carried into the
product.

## History Decision

Recommended decision: keep `rbi-compliance-scanner` as a private/archive-only
prototype and make `anaya/` the clean product repository.

If the old prototype must remain public, rewrite its history with a tool such as
`git filter-repo` after key rotation. Rotation is still mandatory because the
key may already have been exposed.

## M0 Acceptance Checklist

- [x] No private key is tracked in the prototype working tree.
- [x] PEM/key-style files are ignored.
- [x] `anaya/` has no committed secrets.
- [x] Secret rotation work is documented.
- [x] `anaya/` has an AGPL-3.0-or-later license.
- [ ] External service keys have been rotated.
