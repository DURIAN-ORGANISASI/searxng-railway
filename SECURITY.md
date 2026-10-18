# Security Policy

## Intended deployment model

This template is intended for a private SearXNG service consumed by n8n through Railway private networking. The sample configuration disables SearXNG's limiter and does not add API authentication. Do not expose it publicly as-is.

SEARXNG_SECRET is an internal SearXNG configuration secret. It is not an API key or access-control layer for the HTTP Search API.

## Reporting a vulnerability

Do not publish credentials, tokens, private search terms, or exploitable details in a public issue. Use GitHub's Report a vulnerability feature in the repository Security tab when available. If private reporting is unavailable, contact the maintainers privately before disclosing details publicly.

## Secret handling

- Generate a random value for SEARXNG_SECRET and store it in Railway Variables or a password manager.
- Never commit secrets, .env files, or unredacted deployment logs.
- Rotate a secret immediately if it may have been exposed.
- Remove internal hostnames, private queries, and credential values before sharing logs.
- Before enabling any public access, independently add and test authentication, access controls, rate limiting, monitoring, and abuse protections.
