# Security Policy

## Reporting a vulnerability

Please report vulnerabilities privately through
[GitHub Security Advisories](https://github.com/lucasrguerra/InBraille/security/advisories/new)
instead of opening a public issue. You can expect an answer within a few days.

## Hardening in place

- Strict input validation: size, line count, alphabet, Braille-only characters for STL generation.
- Cost budget for STL generation (filled cells × resolution), per-client rate limits and a bounded FIFO queue (2 running, up to 20 waiting, 3 per client, 60 s max wait; otherwise `503` with `Retry-After`).
- Request body cap, no interactive API docs, generic error messages (details only in server logs).
- Security headers (CSP, `nosniff`, `X-Frame-Options`, ...) and path-confined static file serving.
- Container runs as a non-root user with a read-only filesystem and no capabilities.
- Dependencies pinned, scanned with Trivy on every push and before every release.
