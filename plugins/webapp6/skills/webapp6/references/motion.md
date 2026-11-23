# Optional: Count-Up and Scroll Animations

Apply these rules **only** for landing, portfolio, and introduction pages, KPI summary areas, or when the user explicitly requests them. Do **not** add motion to data-entry screens, tables, or live operational values. If any motion rule conflicts with the [six principles](webapp-principles.md), the six principles win.

## Common

- **Content first:** The page must remain complete without animation. Put final numbers and body copy directly in the HTML, and apply initial hidden or zero states (`0`, `opacity: 0`, optional `transform` offset) only via a class added by script. Readers with JavaScript disabled and search engines see the complete final values.
- **Never break accessibility or find-in-page:** Do not hide elements with `visibility: hidden`, `display: none`, or the `hidden` attribute, because those remove content from screen readers, keyboard focus, and in-page search. For above-the-fold elements, either establish the initial state before first paint or skip entrance motion so final values do not flash to `0`.
- **API-fed metrics (Rule 4):** Values loaded from an API cannot be hardcoded in HTML. Render distinct `loading`, `empty`, and `error` states, and never use `0` as a loading placeholder. Start a count-up only from a successful response, and abort if the screen unmounted or a newer request already settled. On subsequent refreshes within the same screen, update directly to the new value instead of counting up from `0` again.
- **Reduced motion:** Under `prefers-reduced-motion: reduce`, skip motion and show the final state immediately.
- **Observe once:** Script-driven reveals start once when entering the viewport (`IntersectionObserver`, calling `unobserve()` once triggered). Do not read layout geometry on every scroll event.
- **Compositor-only properties:** Animate only `transform` and `opacity`. Never animate layout-triggering properties (`top`, `width`, `height`, `margin`), and reserve final space up front to prevent layout shifts.
- **Print safety:** Printing captures the current scripted DOM state, so handle print explicitly: override initial hidden states in `@media print` (`opacity: 1; transform: none; animation: none; transition: none`) so final accessible text displays, or settle all count-ups to their target values on `beforeprint`.
- **Modules, boundaries, and tokens (Rules 1–3):** Keep each motion feature in its own responsibility module. In new code without competing conventions, use a dedicated class per responsibility (for example `CountUp`, `Reveal`); if the project uses function components, hooks, or composables, separate the same responsibilities with those idioms rather than rewriting into classes. Define durations and easing curves as CSS design tokens.
- **Lifecycle and BFCache (Rules 4–5):** When an SPA screen unmounts, cancel any active `requestAnimationFrame` with `cancelAnimationFrame` and call `disconnect()` on observers. Never attach cleanup to `unload`. If `pagehide` disconnects observers or cancels frames, reconnect them in `pageshow` when `event.persisted` is `true` (initialization code does not rerun on BFCache restoration): re-observe untriggered elements and snap interrupted count-ups to their final values. Deep links, refreshes, and Back/Forward restorations landing mid-page (`#anchor` or restored scroll offset) must never leave visible content stuck hidden.

## Count-up

- Animate with `requestAnimationFrame` along an ease-out curve over 1–2 seconds, guaranteeing that the final frame lands on the exact target value.
- Format grouping separators, decimals, percentages, and currencies with `Intl.NumberFormat`. Place non-CLDR units (such as Korean `건`, `명`, `개`) outside the formatted number, because `style: 'unit'` throws `RangeError` for unsupported unit identifiers.
- Apply `font-variant-numeric: tabular-nums` (when supported by the font) so digit widths remain uniform, and reserve width for the longest formatted string (for example `display: inline-block; min-width: 6ch; text-align: end`) so growing digits and commas do not cause horizontal jitter.
- Prevent screen readers from announcing intermediate frames: mark the animated visual node `aria-hidden="true"` (explicit attribute value) and provide the final value in visually hidden accessible text (such as `.sr-only`). Never hide that accessible text with `display: none` or `hidden`, and never attach `aria-live` to rapidly ticking numbers.
- Default to script-driven count-ups. CSS-only approaches (`@property` integer with `counter()`) complicate locale separators and accessible text, so use them only when explicitly requested.

## Scroll animations

- Restrict scroll motion to subtle entrance reveals and scroll-progress indicators. Never hijack scroll speed, inertia, or direction.
- **Entrance effects:** Gate CSS scroll-driven animations (`animation-timeline: view()`) behind `@supports`, falling back to `IntersectionObserver` class toggles elsewhere. Because `view()` animations reverse when scrolling back up, use `IntersectionObserver` even in supporting browsers whenever an element should reveal once and stay visible.
- **Progress indicators:** Render scroll-progress bars only inside `@supports (animation-timeline: scroll())`. Hide them in unsupported browsers and under `prefers-reduced-motion: reduce`; never fake them with `IntersectionObserver` or scroll listeners, and never pin them permanently at `100%`.
- **Reachability:** Choose `rootMargin`, `threshold`, and `animation-range` values so both bottom-of-page elements and elements taller than the viewport still reach their complete state. Avoid negative bottom `rootMargin` values or mid-viewport end ranges (such as `animation-range: 0% 50%`) that trap tall or footer elements unfinished.

## Verification

Append these checks to the real-app acceptance matrix whenever motion rules are in scope, marking any unexecuted item `untested`:

- `prefers-reduced-motion: reduce`, JavaScript disabled, and Print Preview.
- Direct mid-page `#anchor` navigation and Back/Forward scroll restoration (including BFCache restore).
- Scrolling to the very bottom of the page: final elements and elements taller than the viewport reach their complete final state.
- 4x CPU throttling: no frame-drop jank and zero layout shift.
- API-fed metrics: `loading`, `empty`, and `error` states each render cleanly, and refreshed values do not recount from `0`.
