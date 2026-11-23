# Webapp Development Principles

> Adapted from `docs/webapp-principles.md` in [Technoetic/agentic-vault](https://github.com/Technoetic/agentic-vault) (`v0.56.0`, MIT) for standalone installation across Antigravity CLI, Claude Code, and Codex.

These six principles govern how an AI coding agent builds, modifies, or reviews a web application. The [webapp6 skill](../SKILL.md) points all three hosts to this canonical guide.

Always prioritize the current user's explicit instructions and project policies, and follow the existing workflow and framework already chosen for the repository. Keep an existing structure whenever it fulfills the same responsibility. Reading this guide grants no permission to install packages, deploy, alter host settings, or save documents. Read-only reviews report findings and evidence without modifying files. Do not start web-app work solely because an ordinary document mentions websites or explains web concepts.

## 1. Responsibility-based JavaScript modules

Split JavaScript by responsibility in source: entry points handle initialization and wiring, screen modules handle view state and presentation, services handle API and storage I/O, and shared utilities hold small reusable helpers. Do not accumulate all screens, network calls, and state inside a single monolithic file. Keep input/output contracts and dependency directions explicit between modules.

Source modularity is independent from deployment packaging. Bundling multiple JS modules into a single HTML file for distribution remains valid. Use the bundler or framework module conventions already present in the project, and do not introduce a build tool or runtime dependency solely to satisfy this rule.

## 2. Layered CSS (tokens, base, components)

Separate design tokens (colors, spacing, typography), base element styles, and screen or component styles in development source. Extract repeated values into tokens and scope component rules so they do not leak across screens. If the project already fulfills this separation through CSS modules, utility CSS, or CSS-in-JS, preserve that styling system. Combining or inlining CSS in the built output remains valid.

## 3. Screen and service boundaries

For new code without competing conventions, represent distinct screen and service responsibilities as classes. For example, `OrdersScreen` owns rendering, DOM events, and screen lifecycle, while `OrdersService` owns fetching and persistence. Clean up listeners and in-flight requests when a screen unmounts, and keep services from directly owning DOM nodes or browser navigation.

When user instructions or the chosen framework use function components, hooks, composables, or equivalent idioms, keep the same responsibility boundaries using those conventions instead of rewriting an existing app into classes. During reviews, verify clear ownership of state and side effects, and record any project convention exceptions applied.

## 4. Async loading and rendering (`async`/`await`)

Any render that depends on asynchronous data must await its I/O and distinguish `loading`, `empty`, `success`, and `error` states. Handle HTTP error statuses and malformed payloads explicitly and provide a way for the user to retry. Independent requests may run in parallel, while dependent steps must preserve execution order.

Prevent slow older responses from overwriting a newer screen by using request cancellation (`AbortController`) or monotonic request IDs. Discard stale results if the screen has unmounted or a newer request has already settled. Track in-progress and failed saves explicitly, and never report a failed save as completed. Reuse the framework's built-in async data and cancellation primitives when present.

## 5. Single entry point with navigable screen URLs

Serve the app from one entry point while giving every screen a shareable URL. Parse the URL into app state and synchronize in-app navigation with browser history. Direct deep links, full page refreshes on non-root URLs, and browser Back/Forward navigation must all restore the exact intended screen. Reuse the existing router or framework entry point rather than swapping in a new router.

Apply server-side app-shell fallback only to genuine screen routes. Missing static assets (JS, CSS, images) and missing API endpoints must return genuine `404` responses rather than HTML `200` fallbacks. Define unknown-route handling according to project policy, and never stop verification at the root URL alone.

## 6. Safe deployment updates (no hard refresh required)

Users must receive new app code after a deployment without performing a hard refresh. Configuring HTTP cache headers and replacing an already-running document are both required: changing `Cache-Control: no-store` alone does not replace JavaScript already executing in open browser tabs.

### Build identity and HTTP cache

- **Loaded build identity:** Embed the build ID in the loaded HTML metadata or its matching asset bundle. Never initialize the loaded build ID from a startup fetch of the latest server version: if build B deploys right after build A HTML is served, tab A would misidentify itself as build B.
- **Server deployment version:** Query a fresh same-origin version endpoint (or framework equivalent) with cache settings that guarantee a current response, and validate both HTTP status and response shape. Compare by **equality** (`serverBuild !== loadedBuild`), never by numeric ordering or timestamps: rolling back from B to A is also a changed build.
- **Entry HTML caching:** Use revalidated `Cache-Control: no-cache` with an `ETag`, or `Cache-Control: private, no-store` when appropriate. Never allow authenticated or user-specific HTML/API responses into shared public caches. Verify real browser, proxy, and CDN behavior in the target environment.
- **Static assets:** Differentiate build-specific assets with content-hashed filenames or immutable build paths. Public immutable assets may use long cache lifetimes. Deploy HTML and its referenced asset graph together, and decide how prior-build assets are served during transitions. Never assume that appending `?v=...` to the HTML URL invalidates imported JS or CSS modules.

### Already-open tabs and the next navigation

Tabs already running build A are explicitly in scope. Check for a changed build before internal screen navigation, upon returning to the tab (`focus`/`visibilitychange`), and on relevant history or BFCache restorations (`pageshow`). Use framework navigation and lifecycle hooks where available, and ensure restored documents keep comparing against their own embedded build ID.

After a changed build is detected, **the next clean navigation (no unsaved edits and no save in flight) must automatically load the user's intended target URL as a full document.** Swapping only the SPA view leaves stale runtime code in memory, so a full document load (such as `location.assign(targetURL)`) or an equivalent framework deployment transition is required. Preserve normal history semantics on Back/Forward. Showing a manual reload banner, requiring an "accept update" button click, or telling users to press F5 does **not** satisfy this rule.

Focus return or background checks may mark an update as pending, but must **never force a background reload.** Immediately before committing the transition, **recheck** both dirty input state and saves in flight, because new edits or saves can begin while an asynchronous version check is pending.

If unsaved edits exist **or** a save is in flight, notify the user of the update and preserve their work. Apply the full-document transition on the next navigation only after the save succeeds, editing is cancelled, or the user explicitly discards the draft. Never treat a failed save as clean. Preserve existing unsaved-changes guards so updates neither drop drafts nor trigger duplicate saves.

Handle version-check network failures, timeouts, and invalid responses gracefully so the current app and drafts remain usable. Never create an infinite reload loop or trap users from leaving. Whether navigation continues under the current runtime follows project policy, and version checks resume on the next appropriate trigger after connectivity returns. Do not add a service worker or polling library solely to satisfy this rule; if a service worker already exists, verify its caching, activation, and client-transition behavior as well.

### Data freshness is separate

Application data can change even while the app build stays identical. Never reload the entire document merely because data changed. Fetch fresh data on navigation, user refresh, or other appropriate triggers using matching server cache policies. Request API endpoints via same-origin **absolute paths or absolute URLs** (for example `new URL('/api/orders', location.origin)` with `cache: 'no-store'`, respecting any configured subpath base) so nested screen URLs do not produce broken relative API paths. Maintain auth/permission checks and response validation, and distinguish data-fetch failures from app build updates in the UI.

## Real-app acceptance matrix

Run the rows matching your change scope in a real app environment and record observed results and evidence. Prepare builds A and B with distinct visible markers or build IDs. Mark unexecuted rows `untested` and unsupported environment items `unsupported` with the reason.

| Check | Scenario and action | Expected outcome |
|---|---|---|
| JS and CSS sources | Inspect screen/service/shared JS and token/base/component CSS, then run the existing build | Clear responsibility boundaries and working build output (single-HTML bundle remains valid). |
| Project conventions | Review an app with an existing functional framework or explicit structural instructions | Responsibilities are met within existing conventions without unnecessary class/framework rewrites; exceptions are recorded. |
| Async errors and races | Reproduce a failed request and a slower older request settling after a newer request | Error state and retry work; stale responses never overwrite the newer screen. |
| Direct links and refresh | Open a non-root screen URL in a fresh tab and perform a normal refresh | Intended screen, assets, and data load cleanly. |
| Back/Forward and 404 | Navigate across screens then use Back/Forward; request a missing static asset and API route | URL and screen stay synchronized; missing assets and APIs return real 404s instead of HTML 200. |
| Fresh entry A → B | Visit A, deploy B, and open the app URL in a fresh tab | Build B HTML and matching assets run without a hard refresh. |
| Already-open A tab | Keep A open, deploy B, and navigate to another screen while clean | Target URL loads automatically as a full document with no accept-update prompt and runs build B. |
| Startup race | Serve A HTML, deploy B immediately, then let the initial version fetch finish | Loaded identity stays A so the change to B is detected rather than missed. |
| Tab return and history restore | Leave tab A, deploy B, return to the tab or restore via BFCache, then navigate cleanly | Change is detected without background reload; next clean navigation loads B. |
| Dirty input | Enter unsaved input in A, deploy B, and attempt navigation | Update is announced and the draft is protected; after save, cancel, or explicit discard, next navigation loads B. |
| Editing while saving or checking | Navigate while a save is in flight or after typing during a pending version check | State is rechecked right before transition so edits and saves stay protected; failed saves are never marked clean. |
| Rollback B → A | Keep tab B open, roll server back to A, and navigate cleanly | Inequality check detects the rollback and loads document A. |
| Version check failure | Simulate offline network, timeout, or invalid version payload | Current app and drafts stay usable with no reload loop; checks resume after recovery. |
| Data-only update | Keep the same app build, update API data, and trigger a data refresh | Fresh data loads from the proper same-origin absolute API URL without a full-document reload. |
| Asset and auth cache | Inspect HTML, static asset, and API response headers and live requests in an open tab | HTML revalidates or uses private no-store, assets match the build, and sensitive responses are never cached publicly. |

Headers, screenshots, or documentation keywords alone do not prove open-tab transitions: verify actual document navigation, running build ID, target URL, draft/save state, and live data responses together. Skill discovery and installed-file byte checks prove **instruction delivery**, and synthetic baseline/candidate prompts observe **agent plans**; report both separately from real-app tests, and never claim that a skill is always triggered or automatically obeyed.

## Verification and handoff

For significant work, record exact commands, observed results, and scope using these six fields. Follow the project's existing handoff location and format instead of creating unrequested log files.

| Field | Required content |
|---|---|
| `task_id` | Task identifier |
| `artifact_paths` | Changed or verified file and artifact paths |
| `verification_commands_and_results` | Exact commands/procedures run, environment, observed outcomes, failures, and untested items |
| `assumptions` | Deployment, routing, and cache assumptions plus any user or project exceptions applied |
| `unresolved` | Open issues plus unsupported or untested scope |
| `next_safe_action` | Next step within current authority; deployment and installation require separate approval |

For important code, structural, or aggregate outputs, have a separate session or read-only verifier rerun the verification commands and append `verified_by` (actor, timestamp, scope, result). Distinguish self-checks from independent verification. Never mark an unexecuted check as passed or present an agent's plan as real-app execution.
