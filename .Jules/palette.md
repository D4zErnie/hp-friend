# Palette's Journal

## 2024-05-21 - Interactive Elements as Divs
**Learning:** This application frequently uses `div` elements with `onClick` and `cursor-pointer` for interactive buttons (e.g., footer social icons, contact cards), which excludes keyboard users and screen readers.
**Action:** In future enhancements, prioritize refactoring these to semantic `<button>` or `<a>` tags, or at minimum add `role="button"`, `tabIndex="0"`, and keydown handlers.

## 2024-05-22 - Single-File React Source Strategy
**Learning:** In a single-file React project, compiling JSX to pure JS ensures performance but destroys maintainability.
**Action:** Use Babel Standalone (`<script type="text/babel">`) to allow writing semantic JSX (like accessible `<button>` tags) while keeping the file runnable and editable.
