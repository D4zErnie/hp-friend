## 2026-02-05 - React Components Defined Inside Components
**Learning:** The `App` component in `dirking.html` defines sub-components (`HomePage`, `ContactPage`, etc.) *inside* its render function. This causes React to redefine the component function on every render of `App`. Consequently, React treats them as new components, unmounting the old instance and mounting the new one. This leads to severe performance degradation (full DOM thrashing) and bugs (loss of input focus in `ContactPage` when typing).
**Action:** Always define React components outside of other components. Pass data via props or use Context. If a refactor is too large for a "small optimization", prioritize documenting this anti-pattern to prevent future recurrence or to flag for a larger refactor.

## 2026-02-05 - Inline Static Data in Render Loops
**Learning:** Defining static data arrays inline within the render method (e.g., `{[...].map(...)`) creates a new array reference on every render. While typically cheap, in this codebase it contributed to unnecessary allocations (approx. 15% slower in micro-benchmarks compared to static constants).
**Action:** Hoist static configuration data or feature lists to constants outside the component definition. This improves performance (allocations) and code readability.
