# Changelog

## Unreleased

- STL generation now goes through a bounded FIFO queue instead of rejecting requests when busy.

## 1.0.0

- First tagged release, published as a Docker image on GitHub Container Registry.
- Security hardening of the API and the container (see SECURITY.md).
- Dependencies upgraded; all Trivy findings (critical, high and medium) resolved.
