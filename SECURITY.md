# Security

## Secret Handling

Do not commit runtime secrets, private keys, webhook secrets, or `.env` files.

Local secret material should live outside the repository or under an ignored
`secrets/` directory. GitHub App private keys should be referenced through
`ANAYA_GITHUB_PRIVATE_KEY_PATH` locally or a raw secret environment variable in
hosted deployments.

## Prototype Key Rotation

The old `rbi-compliance-scanner` prototype previously tracked a GitHub App
private key. The file has been removed from Git tracking and PEM files are now
ignored, but the committed key must still be treated as compromised.

Before pushing, deploying, or using the old GitHub App again:

1. Generate a new GitHub App private key in GitHub App settings.
2. Delete/revoke the old private key in GitHub.
3. Rotate the GitHub webhook secret.
4. Rotate local legacy AI-provider keys from the old prototype if present.
5. Rotate local OpenAI keys that were present in `.env`.
6. Update local `.env` files with the new values.
7. Keep the old prototype repository history private or rewrite/archive it.

Anaya V1 uses OpenAI for any future optional LLM fallback. Other LLM providers
are not part of the Anaya product direction.

## Repository Direction

`anaya/` is the clean canonical product foundation. The older
`rbi-compliance-scanner/` repo should be treated as a reference prototype, not
the production codebase.
