# Codebase Learnings

## React Single-File Prototypes
- **Component Nesting:** Ensure all React components are defined at the top-level scope. Defining components inside other components (like `App`) causes them to be recreated on every render, leading to focus loss and state issues. It also makes the code harder to debug and prone to syntax errors during merges.
- **Merge Conflicts:** When merging changes in a single-file application, pay close attention to component boundaries. It is easy to accidentally duplicate component definitions or wrap the entire file in a function, causing the application to fail to render.
