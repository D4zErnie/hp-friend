## 2026-02-05 - React Components Defined Inside Components
**Learning:** The `App` component in `dirking.html` defines sub-components (`HomePage`, `ContactPage`, etc.) *inside* its render function. This causes React to redefine the component function on every render of `App`. Consequently, React treats them as new components, unmounting the old instance and mounting the new one. This leads to severe performance degradation (full DOM thrashing) and bugs (loss of input focus in `ContactPage` when typing).
**Action:** Always define React components outside of other components. Pass data via props or use Context. If a refactor is too large for a "small optimization", prioritize documenting this anti-pattern to prevent future recurrence or to flag for a larger refactor.

## 2026-02-05 - 404 Hero Image & LCP Optimization
**Learning:** The hero image in `dirking.html` pointed to a non-existent URL (404), preventing accurate baseline performance measurements.
**Action:** When optimizing assets, verify their existence first. Replaced the broken asset with a working Unsplash ID (`photo-1472214103451`) and implemented responsive best practices: `srcset` for bandwidth savings and `fetchpriority="high"` to improve Largest Contentful Paint (LCP). Note that replacing broken assets changes visual content, which should be flagged, but is necessary when the original is unrecoverable.
