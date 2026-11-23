# webapp6

**Six web-app principles as one installable skill for Antigravity CLI (`agy`), Claude Code, and Codex.**
Use it when an AI coding agent builds, changes, or reviews a web app. An optional rule set covers
count-up numbers and scroll animations.

[한국어 README](README.ko.md) · MIT License · v0.1.0

## The six principles

| # | Principle | Required outcome |
|---|---|---|
| 1 | Responsibility-based JavaScript modules | Entry, screens, services, and shared utilities are separate modules. A bundled single-HTML deliverable is still fine. |
| 2 | Layered CSS | Design tokens, base styles, and component styles are separate in source. An existing styling system that already does this stays. |
| 3 | Screen and service boundaries | New code without other conventions uses classes per responsibility; hooks, composables, and similar project conventions are kept. |
| 4 | Async loading and rendering | `async`/`await` for I/O; loading, empty, success, and error states; request cancellation or request IDs so stale responses never overwrite a newer screen. |
| 5 | Single entry with navigable screens | Every screen has a URL; deep links, refresh, Back/Forward work; missing assets and API calls return real 404s. |
| 6 | Safe deployment updates | Already-open tabs detect a changed build (including a rollback) and automatically load the intended target URL as a full document on the next clean navigation, with no accept-update prompt and without losing drafts or saves. |

The canonical guide with the real-app acceptance matrix is
[`references/webapp-principles.md`](plugins/webapp6/skills/webapp6/references/webapp-principles.md).

## Optional: count-up and scroll animations

Only for landing, portfolio, and introduction pages, KPI summaries, or when you ask for it. The rules keep
content complete without motion, respect `prefers-reduced-motion`, animate only `transform` and `opacity`,
handle printing and BFCache restoration, never show `0` as a placeholder for API-fed numbers, and add their
own verification steps. See [`references/motion.md`](plugins/webapp6/skills/webapp6/references/motion.md).

## Install

### Antigravity CLI (`agy`)

```sh
agy plugin install https://github.com/Technoetic/webapp6/tree/main/plugins/webapp6
```

Pinned to this release: `https://github.com/Technoetic/webapp6/tree/v0.1.0/plugins/webapp6`

### Claude Code

```sh
claude plugin marketplace add Technoetic/webapp6
claude plugin install webapp6@technoetic-webapp6
```

On Claude Code 2.1.275 or later you can also install in one step inside a session:
`/plugin install webapp6 --marketplace Technoetic/webapp6`

### Codex

```sh
codex plugin marketplace add Technoetic/webapp6
codex plugin add webapp6@technoetic-webapp6
```

## Use

| Host | Invocation |
|---|---|
| Claude Code | `/webapp6:webapp6 review the checkout page` (or let the skill trigger on web-app work) |
| Codex | `$webapp6:webapp6 review the checkout page` |
| Antigravity CLI | `/webapp6 review the checkout page` (per the Antigravity docs; or let it trigger on web-app work) |

With no target, the skill tells the agent to apply the rules to the web-app work in the current conversation; if
there is none, to explain the rules and how to invoke it instead of creating an app.

## What the plugin does and does not do

- Apart from its PNG icon it ships text only: one skill (`SKILL.md`), two reference documents, an agent display
  file (`agents/openai.yaml`), manifests, a README, and a license. No scripts, hooks, MCP servers, or network calls.
- The skill tells agents not to install, deploy, or change host settings on their own, and to deploy only where
  and when you say so; your host's permissions and approvals still apply.
- The skill tells agents to report what they actually verified separately from what is untested. Whether a host
  selects the skill and whether an agent follows it is not guaranteed: skill discovery proves delivery, not compliance.

## Repository layout

```text
.
├── .claude-plugin/marketplace.json     Claude Code marketplace
├── .agents/plugins/marketplace.json    Codex marketplace
├── plugins/webapp6/                    single installable plugin for all three hosts
│   ├── plugin.json                     Antigravity manifest
│   ├── .claude-plugin/plugin.json      Claude Code manifest
│   ├── assets/icon.png                 plugin icon (1024 x 1024), declared in all three manifests
│   ├── .codex-plugin/plugin.json       Codex manifest
│   └── skills/webapp6/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       └── references/
│           ├── webapp-principles.md    six principles + acceptance matrix
│           └── motion.md               optional count-up and scroll rules
└── tests/test_plugin.py                packaging checks (run in CI)
```

## Origin

The six principles are adapted from `docs/webapp-principles.md` in
[Technoetic/agentic-vault](https://github.com/Technoetic/agentic-vault) (MIT) so they can be installed on their own.

## License

[MIT](LICENSE)
