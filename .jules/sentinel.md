## 2026-02-05 - Supply Chain Security in Static Sites
**Vulnerability:** Usage of "latest" versions for CDN libraries and missing Subresource Integrity (SRI) checks.
**Learning:** In static sites relying on CDNs, using unversioned links (e.g., `unpkg.com/package@latest`) exposes the application to supply chain attacks. If the library is compromised or updated with breaking changes, the site breaks or becomes malicious automatically.
**Prevention:** Always pin specific versions of dependencies and use SRI hashes (`integrity` attribute) to verify that the fetched resource matches the expected content. This creates a "lockfile" equivalent for CDN resources.

## 2026-02-06 - SRI Compatibility with Tailwind CDN
**Vulnerability:** Inability to secure Tailwind CDN resource with SRI.
**Learning:** The Tailwind Play CDN (`cdn.tailwindcss.com`) does not provide `Access-Control-Allow-Origin` headers compatible with `crossorigin="anonymous"`. This prevents the use of Subresource Integrity (SRI) hashes, as the integrity check requires CORS to be enabled.
**Prevention:** For production security requiring SRI, avoid `cdn.tailwindcss.com`. Use the Tailwind CLI to generate static CSS and serve it from the same origin or a CORS-compliant CDN.

## 2026-02-08 - Duplicate Script Tags Defeating SRI
**Vulnerability:** A script library was included twice: once without SRI (top) and once with SRI (bottom). The browser executes the first occurrence, rendering the SRI protection useless.
**Learning:** Simply adding a secured script tag is insufficient if an insecure version remains in the document. Browsers process scripts sequentially.
**Prevention:** Audit HTML for duplicate script inclusions and ensure only the secured, pinned version is present.
