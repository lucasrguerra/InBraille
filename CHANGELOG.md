# Changelog

## 1.2.0

- Improved SEO: added robots.txt, sitemap.xml, Schema.org structured data (WebApplication and FAQPage), rich social meta tags, and interactive FAQ section.
- Fixed Braille glyph rendering: bundled and self-hosted Noto Sans Symbols 2 font to render Braille dots as crisp circles instead of square blocks across all platforms.
- Upgraded CI/CD dependencies and pinned GitHub Actions runners to ubuntu-24.04.
- Updated Docker runtime image to Python 3.14.

## 1.1.0

- STL generation now goes through a bounded FIFO queue instead of rejecting requests when busy.

## 1.0.0

- First tagged release, published as a Docker image on GitHub Container Registry.
- Security hardening of the API and the container (see SECURITY.md).
- Dependencies upgraded; all Trivy findings (critical, high and medium) resolved.
