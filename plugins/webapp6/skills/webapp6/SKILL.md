---
name: webapp6
description: "Use when creating, changing, or reviewing a web app: JavaScript/CSS structure, screen and service boundaries, async data loading, routing and deep links, deployment updates for already-open tabs, or cache behavior. Optional rules cover count-up numbers and scroll animations on landing, portfolio, and introduction pages, KPI summary areas, or on request. 웹앱을 만들거나 고치거나 검토할 때 6원칙과 선택 항목(카운트업·스크롤 애니메이션)을 적용한다."
---

# webapp6 — six web-app principles

Apply six rules when building, changing, or reviewing a web app. The current user's
instructions and project policies take priority; follow the workflow and framework already
chosen, and keep an existing structure when it meets the same responsibility. Reading this
skill grants no permission to install, deploy, rewrite a project, change host settings, or
save documents.

**Required reading:** before implementing or reviewing, read the canonical
[six-rule guide and real-app acceptance matrix](references/webapp-principles.md).
When the page calls for count-up numbers or scroll animations, also read the
[optional motion rules](references/motion.md). This checklist does not replace them.

## How to run

1. Read the guide from this skill's folder (and the motion rules when they apply).
   Do not substitute an earlier conversation summary for the files. If
   `references/webapp-principles.md` (or `references/motion.md` when it applies) cannot be
   read, say so and do not claim the rules were applied.
2. Apply it to the request that came with the invocation. A review request is read-only:
   report findings with evidence.
3. This skill alone never starts another workflow, installs packages, or deploys. Deploy
   only to the platform the user names and within the approval the user gives.
4. Report what you actually verified separately from what is untested.

If the invocation names no target, apply the rules to the web-app work in the current
conversation. If there is none, explain the six rules, the optional motion rules, and how
to invoke this skill — do not create an app.

Invocation: Claude Code `/webapp6:webapp6 <request>`, Codex `$webapp6:webapp6 <request>`,
Antigravity CLI `/webapp6 <request>` (per the Antigravity docs). Hosts may also select the
skill on their own for web-app work.

## Scope

Use for app creation, changes, and reviews, including stale code after deployment or
broken deep links. Ordinary documents that mention websites, or explanations of web
concepts, do not start app work.

## Six-rule checklist

| Rule | Required outcome |
|---|---|
| 1. JavaScript | Develop modules by responsibility: entry, screens, services, shared utilities. A bundled single-HTML deliverable remains valid. |
| 2. CSS | Separate tokens, base styles, and components in source; preserve the project's styling system. |
| 3. Screen/service boundaries | Use classes for distinct responsibilities by default; retain project/framework equivalents when its conventions or user instructions differ. |
| 4. Async loading | Use async/await for I/O and dependent rendering; handle loading, HTTP/errors, cancellation, and stale-response races. |
| 5. Single entry | Give screens URLs; support direct deep links, refresh, Back/Forward, and genuine asset/API 404s. |
| 6. Deployment updates | Detect changed app code in already-open tabs; automatically load the intended target as a full document on the next clean navigation, protecting edits and saves. |

## Rule 6 must remain explicit

Compare a build identity embedded in the loaded HTML/build with a fresh same-origin
version response or framework equivalent. Do not initialize the loaded identity from a
startup fetch of the latest server version. Any unequal identity, including rollback,
means changed code.

Check on navigation, tab return, and relevant history/BFCache restoration. After
detecting a change, a clean next navigation automatically loads its target URL as a full
document. A notice offering manual reload, an accept-update button, or instructions to
press F5 do not fulfill this requirement. Recheck both dirty state and saves in flight
immediately before transition. Protect and notify until saved, cancelled, or explicitly
discarded; never force a background reload. Version/network failures keep the current app
and drafts usable.

Use entry-HTML revalidation or appropriate private no-store, build-specific asset
identities, and fresh data requests as separate concerns. A query parameter on HTML alone
does not invalidate imported assets. Do not add a service worker or polling dependency
solely for this rule.

## Optional: count-up and scroll animations

Only for landing, portfolio, and introduction pages, KPI summaries, or when the user asks;
never for data-entry screens, tables, or live values. Content must be complete without
motion, `prefers-reduced-motion` shows the final state at once, only `transform` and
`opacity` move, printing and BFCache restoration must not leave content hidden, and
API-fed numbers never use `0` as a placeholder. The full rules and their extra checks are in
[motion.md](references/motion.md).

## Verify and report

Use the acceptance matrix for affected behavior. Record actual commands and results,
exceptions, and untested cases; distinguish agent-plan evaluations, package delivery, and
application tests. Use the guide's six-field handoff and an independent `verified_by` for
important artifacts. Skill discovery alone proves neither agent adherence nor app behavior.
