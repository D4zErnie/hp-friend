# Codebase Learnings

## React Single-File Prototypes
- **Component Nesting:** Ensure all React components are defined at the top-level scope. Defining components inside other components (like `App`) causes them to be recreated on every render, leading to focus loss and state issues. It also makes the code harder to debug and prone to syntax errors during merges.
- **Merge Conflicts:** When merging changes in a single-file application, pay close attention to component boundaries. It is easy to accidentally duplicate component definitions or wrap the entire file in a function, causing the application to fail to render.

## 2026-02-07 - [Transpiled Code Contamination]
**Learning:** In single-file React apps using `@babel/standalone`, pasting transpiled `React.createElement` output into the source file not only degrades readability but causes massive performance regressions if the code is pasted inside a component definition (e.g., `App`). This forces the entire component tree to remount on every state update, losing focus and state.
**Action:** When seeing `React.createElement` mixed with JSX, immediately suspect a copy-paste error of build artifacts. Always move component definitions to the top level scope and revert to JSX source.

## 2026-02-10 - [Lucide createIcons Overhead]
**Learning:** Using `lucide.createIcons()` inside a React `useEffect` hook triggers a full DOM scan on every render/update, which is O(N) where N is the number of icons. In a single-file React app, this pattern is often copied from static site examples but kills performance.
**Action:** Always replace `createIcons` with a dedicated `Icon` component that looks up the SVG definition in `lucide.icons` and renders it directly, avoiding the DOM scan entirely.
