# Codebase Learnings

## React Single-File Prototypes
- **Component Nesting:** Ensure all React components are defined at the top-level scope. Defining components inside other components (like `App`) causes them to be recreated on every render, leading to focus loss and state issues. It also makes the code harder to debug and prone to syntax errors during merges.
- **Merge Conflicts:** When merging changes in a single-file application, pay close attention to component boundaries. It is easy to accidentally duplicate component definitions or wrap the entire file in a function, causing the application to fail to render.

## 2026-02-06 - LCP Optimization and Compilation
**Learning:** Single-file React apps embedded in HTML often suffer from performance issues if they rely on in-browser compilation (which was missing here, causing a crash) or mixed content. Pre-compiling JSX to vanilla JS significantly improves reliability and startup performance.
**Action:** Extract JSX, compile with `esbuild`, and inject back into the HTML. Also, optimize Hero images with `srcset`, `sizes`, and `fetchpriority="high"` for significant LCP gains.
