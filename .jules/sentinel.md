## 2026-02-05 - Supply Chain Security in Static Sites
**Vulnerability:** Usage of "latest" versions for CDN libraries and missing Subresource Integrity (SRI) checks.
**Learning:** In static sites relying on CDNs, using unversioned links (e.g., `unpkg.com/package@latest`) exposes the application to supply chain attacks. If the library is compromised or updated with breaking changes, the site breaks or becomes malicious automatically.
**Prevention:** Always pin specific versions of dependencies and use SRI hashes (`integrity` attribute) to verify that the fetched resource matches the expected content. This creates a "lockfile" equivalent for CDN resources.
