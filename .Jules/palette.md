# Palette's Journal

## 2024-05-21 - Interactive Elements as Divs
**Learning:** This application frequently uses `div` elements with `onClick` and `cursor-pointer` for interactive buttons (e.g., footer social icons, contact cards), which excludes keyboard users and screen readers.
**Action:** In future enhancements, prioritize refactoring these to semantic `<button>` or `<a>` tags, or at minimum add `role="button"`, `tabIndex="0"`, and keydown handlers.

## 2024-05-22 - Semantic Contact Links
**Learning:** Replacing `div` containers with `<a>` tags for phone and email not only improves accessibility but also enables native browser features like "Click to Call" and default mail client opening, which is crucial for mobile users.
**Action:** Always wrap contact information (phone, email, social) in semantic `<a>` tags with appropriate `href` schemes (`tel:`, `mailto:`, `https://wa.me`) rather than using `onClick` handlers or static text.
