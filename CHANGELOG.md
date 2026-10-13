# Changelog

## 1.3.0

- High-performance hybrid STL generation:
  - Instant client-side parametric 3D STL generation directly in the browser (~18ms), eliminating server bottlenecks and network latency.
  - Interactive real-time 3D preview: dynamic updates on slider changes (thickness, borders, alignment, symbols) and live typing without reloading.
  - Optimized backend STL serialization: implemented contiguous structured NumPy arrays and vectorized cross-product calculations in `VtkStlSerializer`.
  - In-memory LRU caching for backend STL service, speeding up repeated requests to <1ms.
  - Fixed 3D preview geometry: corrected face winding order on spherical caps and enabled DoubleSide rendering to prevent backface culling artifacts.

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
