# Palette's Journal

## 2024-05-21 - Interactive Elements as Divs
**Learning:** This application frequently uses `div` elements with `onClick` and `cursor-pointer` for interactive buttons (e.g., footer social icons, contact cards), which excludes keyboard users and screen readers.
**Action:** In future enhancements, prioritize refactoring these to semantic `<button>` or `<a>` tags, or at minimum add `role="button"`, `tabIndex="0"`, and keydown handlers.

## 2024-05-22 - Semantic Contact Links
**Learning:** Replacing `div` containers with `<a>` tags for phone and email not only improves accessibility but also enables native browser features like "Click to Call" and default mail client opening, which is crucial for mobile users.
**Action:** Always wrap contact information (phone, email, social) in semantic `<a>` tags with appropriate `href` schemes (`tel:`, `mailto:`, `https://wa.me`) rather than using `onClick` handlers or static text.

## 2024-05-24 - Semantic Button Refactoring
**Learning:** When refactoring `div` containers to `button` elements for accessibility, `text-align: left` and `width: 100%` must be explicitly set, as user agent styles center text and default to inline-block display.
**Action:** Always include reset classes like `w-full text-left` when converting block-level interactive divs to buttons to preserve visual layout.

## 2024-05-24 - Hit Area Expansion
**Learning:** Using negative margins combined with equal padding (e.g., `p-4 -m-4`) effectively expands the clickable hit area of interactive elements without affecting the surrounding layout flow.
**Action:** Use this technique for small touch targets or lists where maintaining tight visual spacing is desired but larger hit targets are needed for accessibility.

## 2024-05-24 - Accessibility for Icon-Only Buttons
**Learning:** Icon-only buttons (like the mobile menu toggle) are invisible to screen readers without explicit labels.
**Action:** Always add `aria-label` to describe the action (e.g., "Open menu") and `aria-expanded` for toggle states. Also, ensure the internal icon has `aria-hidden="true"` to prevent redundancy or confusion.

## 2024-05-24 - Skip to Content Link
**Learning:** For keyboard users, navigating through repeated header content (navigation, logo) on every page load is tedious.
**Action:** Always implement a "Skip to Content" link as the first focusable element. It should be visually hidden (`sr-only`) until focused, pointing to `<main id="main-content" tabIndex="-1">` to ensure focus moves correctly to the content area.

## 2024-05-24 - Tooltip Visibility on Focus
**Learning:** Icon-only buttons with tooltips relying solely on `group-hover` are inaccessible to keyboard users as hover states don't trigger on focus.
**Action:** Always pair `group-hover:opacity-100` with `group-focus-visible:opacity-100` on tooltip elements to ensure they appear when the parent button receives keyboard focus.

## 2024-05-24 - File Input Accessibility
**Learning:** Invisible file inputs (opacity 0) overlaying custom UI lack native focus indication, making them inaccessible to keyboard users who can't see where they are navigating.
**Action:** Always add focus-within styles (e.g., ring, border change) to the parent container of the invisible file input to provide visual feedback when the input receives focus.
