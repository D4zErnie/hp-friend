# Palette's Journal

## 2024-05-21 - Interactive Elements as Divs
**Learning:** This application frequently uses `div` elements with `onClick` and `cursor-pointer` for interactive buttons (e.g., footer social icons, contact cards), which excludes keyboard users and screen readers.
**Action:** In future enhancements, prioritize refactoring these to semantic `<button>` or `<a>` tags, or at minimum add `role="button"`, `tabIndex="0"`, and keydown handlers.

## 2024-05-22 - Semantic Contact Links
**Learning:** Contact information (phone, email) wrapped in `div` tags with `cursor-pointer` creates a misleading affordance without functionality. Users expect these to initiate actions (call, email).
**Action:** Always use semantic `<a>` tags with `tel:` and `mailto:` schemes for contact details to provide immediate utility and accessibility.
