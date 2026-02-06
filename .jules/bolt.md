# Codebase Learnings

## React Single-File Prototypes
- **Component Nesting:** Ensure all React components are defined at the top-level scope. Defining components inside other components (like `App`) causes them to be recreated on every render, leading to focus loss and state issues. It also makes the code harder to debug and prone to syntax errors during merges.
- **Merge Conflicts:** When merging changes in a single-file application, pay close attention to component boundaries. It is easy to accidentally duplicate component definitions or wrap the entire file in a function, causing the application to fail to render.

## 2026-02-06 - LCP Optimization and Compilation
**Learning:** Single-file React apps embedded in HTML often suffer from performance issues if they rely on in-browser compilation (which was missing here, causing a crash) or mixed content. Pre-compiling JSX to vanilla JS significantly improves reliability and startup performance.
**Action:** Extract JSX, compile with `esbuild`, and inject back into the HTML. Also, optimize Hero images with `srcset`, `sizes`, and `fetchpriority="high"` for significant LCP gains.

## 2026-02-06 - Single-File Architecture and Babel
**Learning:** For quick prototypes (`dirking.html`) without a build system, introducing a full compilation pipeline (esbuild, package.json) violates the "zero-config" architecture. The correct fix for broken JSX in a script tag is adding `@babel/standalone` and setting `type="text/babel"`, even if client-side compilation has a performance cost.
**Action:** Always prefer minimal fixes that respect the existing architecture. Optimize LCP via standard HTML attributes (`srcset`, `fetchpriority`) rather than refactoring the entire build process.
