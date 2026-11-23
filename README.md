<h1 align="center">⚡ webapp6</h1>

<p align="center">
  <b>Six web-app principles as one installable skill for Antigravity CLI (<code>agy</code>), Claude Code, and Codex.</b><br>
  Use it when an AI coding agent builds, changes, or reviews a web app. An optional rule set covers
  count-up numbers and scroll animations.
</p>

<div align="center">

<a href="https://github.com/Technoetic/webapp6/releases/tag/v0.1.0"><img src="docs/art/badges/release.svg" alt="Release v0.1.0"></a>
<a href="LICENSE"><img src="docs/art/badges/license.svg" alt="License MIT"></a>
<a href="https://github.com/Technoetic/webapp6/actions/workflows/ci.yml"><img src="https://github.com/Technoetic/webapp6/actions/workflows/ci.yml/badge.svg" alt="CI status"></a>
<br>
<a href="#-install"><img src="docs/art/badges/hosts.svg" alt="Hosts: agy, Claude Code, Codex"></a>
<a href="plugins/webapp6/skills/webapp6/SKILL.md"><img src="docs/art/badges/skill.svg" alt="Skill: 1, webapp6"></a>
<a href="#-the-six-principles"><img src="docs/art/badges/principles.svg" alt="Principles: 6 plus optional motion rules"></a>
<br>
<a href="#-real-app-acceptance-checks"><img src="docs/art/badges/checks.svg" alt="Real-app acceptance checks: 15"></a>
<a href="tests/test_plugin.py"><img src="docs/art/badges/tests.svg" alt="Packaging tests: 9"></a>
<a href="#-what-the-plugin-does-and-does-not-do"><img src="docs/art/badges/ships.svg" alt="Ships text and an icon, no scripts"></a>

</div>

<p align="center">
  <picture>
    <source media="(prefers-reduced-motion: reduce)" srcset="https://raw.githubusercontent.com/Technoetic/webapp6/main/docs/art/hero.png">
    <img src="docs/art/hero.gif" width="880" alt="Header animation: six tiles count up to this repository's counts at v0.1.0, which are 6 principles, 3 hosts, 1 skill, 15 real-app checks, 9 packaging tests, and 2 CI operating systems.">
  </picture>
</p>

<div align="center">

[한국어 README](README.ko.md) · MIT License · v0.1.0

</div>

## 🧭 At a glance

<p align="center">
  <kbd>agy</kbd> <kbd>/webapp6</kbd> &nbsp;·&nbsp; <kbd>Claude Code</kbd> <kbd>/webapp6:webapp6</kbd> &nbsp;·&nbsp; <kbd>Codex</kbd> <kbd>&#36;webapp6:webapp6</kbd><br>
  <sub>The Antigravity CLI form follows the Antigravity docs.</sub>
</p>

One plugin folder carries a manifest for each host and a single skill. All three hosts get the same
`SKILL.md`, which points to the same two reference documents (`motion.md` only when motion is in scope).

```mermaid
%%{init: {'layout': 'dagre', 'theme': 'base', 'themeVariables': {'lineColor': '#8B93A7', 'edgeLabelBackground': '#E8ECF5', 'fontSize': '15px'}}}%%
flowchart LR
    accTitle: One plugin folder, three hosts
    accDescr: plugins/webapp6 holds plugin.json for Antigravity CLI (/webapp6), .claude-plugin/plugin.json for Claude Code (/webapp6:webapp6) and .codex-plugin/plugin.json for Codex ($webapp6:webapp6). All three lead to skills/webapp6/SKILL.md, which points to references/webapp-principles.md and, when motion is in scope, references/motion.md.
    SRC["📁 plugins/webapp6<br/>one folder"]:::src
    SRC --> AGM["plugin.json"]:::cyan --> AG["🪐 Antigravity CLI<br/>/webapp6"]:::cyan
    SRC --> CCM[".claude-plugin/plugin.json"]:::amber --> CC["🤖 Claude Code<br/>/webapp6:webapp6"]:::amber
    SRC --> CXM[".codex-plugin/plugin.json"]:::violet --> CX["🧠 Codex<br/>$webapp6:webapp6"]:::violet
    AG & CC & CX --> SK["📘 skills/webapp6/SKILL.md"]:::lime
    SK --> GUIDE["references/webapp-principles.md<br/>six principles + 15 real-app checks"]:::lime
    SK -. "when motion is in scope" .-> MOTION["references/motion.md<br/>count-up + scroll rules"]:::magenta

    classDef src fill:#131621,stroke:#94A3B8,color:#F8FAFC,stroke-width:2px
    classDef cyan fill:#062F33,stroke:#00F5D4,color:#CCFBF1,stroke-width:2px
    classDef amber fill:#3A2306,stroke:#FF9E00,color:#FEF3C7,stroke-width:2px
    classDef violet fill:#1E1650,stroke:#7B61FF,color:#EDE9FE,stroke-width:2px
    classDef lime fill:#1A2E05,stroke:#C8FF00,color:#ECFCCB,stroke-width:2px
    classDef magenta fill:#4A0D2C,stroke:#FF2E93,color:#FCE7F3,stroke-width:2px
```

> [!NOTE]
> Counts on this page (principles, hosts, files, checks, tests) come from this repository at v0.1.0.
> Illustrative examples are labeled as such.

## 🧱 The six principles

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

## 🚀 Rule 6 in one picture

Rule 6 carries the most real-app checks: 10 of 15 when the checks are grouped by the rule section they
exercise (see below). An open tab notices a new build, and the next clean navigation brings the new build in
as a full document.

```mermaid
%%{init: {'layout': 'dagre', 'theme': 'base', 'themeVariables': {'lineColor': '#8B93A7', 'edgeLabelBackground': '#E8ECF5', 'fontSize': '15px'}}}%%
flowchart TD
    accTitle: Rule 6 decision flow
    accDescr: On navigation, tab return or history/BFCache restore, the tab requests a fresh same-origin version. If the request fails, times out or the response is invalid, the app and drafts stay usable and it checks again later. If the build IDs are equal, it navigates normally. If they differ (a rollback counts), the change is noted without a background reload; on the next navigation, dirty input or a save in flight is protected until saved, cancelled or discarded, otherwise the target URL loads as a full document.
    EV["🧭 Check on navigation,<br/>tab return, or history/BFCache restore"]:::cyan --> VER{"Fresh same-origin<br/>version response?"}:::amber
    VER -- "request fails, times out,<br/>or the response is invalid" --> KEEP["Keep the current app and drafts usable<br/>and check again later"]:::lime
    VER -- "received" --> CMP{"Embedded build ID differs<br/>from the fresh build ID?<br/>(a rollback counts)"}:::amber
    CMP -- "equal" --> SAME["Navigate normally"]:::lime
    CMP -- "different" --> NEXT["Changed build detected<br/>(never a background reload)"]:::violet --> DIRTY{"Next navigation:<br/>dirty input or save in flight?<br/>(recheck right before leaving)"}:::magenta
    DIRTY -- "yes" --> PROTECT["Notify and protect until saved,<br/>cancelled, or explicitly discarded"]:::magenta
    DIRTY -- "no" --> FULL["🚀 Load the target URL<br/>as a full document"]:::violet

    classDef cyan fill:#062F33,stroke:#00F5D4,color:#CCFBF1,stroke-width:2px
    classDef amber fill:#3A2306,stroke:#FF9E00,color:#FEF3C7,stroke-width:2px
    classDef violet fill:#1E1650,stroke:#7B61FF,color:#EDE9FE,stroke-width:2px
    classDef lime fill:#1A2E05,stroke:#C8FF00,color:#ECFCCB,stroke-width:2px
    classDef magenta fill:#4A0D2C,stroke:#FF2E93,color:#FCE7F3,stroke-width:2px
```

The core of the rule as one condition, where `u` is the target URL of the next navigation:

```math
\mathrm{fullLoad}(u) \Leftarrow \mathrm{id}_{\mathrm{loaded}} \neq \mathrm{id}_{\mathrm{fresh}} \;\land\; \lnot\,\mathrm{dirty} \;\land\; \lnot\,\mathrm{saving}
```

`id_loaded` is the build identity embedded in the running page; `id_fresh` comes from a fresh same-origin
version response. Any difference counts, including a rollback. The rule says when a full load must happen;
it does not forbid one otherwise. If the version request fails, times out, or returns an invalid response,
the app keeps running as it is.

> [!WARNING]
> A notice offering a manual reload, an accept-update button, or instructions to press F5 do not satisfy
> rule 6. The next clean navigation loads the target URL as a full document on its own.

> [!CAUTION]
> Never force a background reload. Recheck dirty input and saves in flight immediately before the
> transition, and protect them until they are saved, cancelled, or explicitly discarded.

<p align="center">
  <a href="docs/art/cards/structure-plantuml.png"><img src="docs/art/cards/structure-plantuml.png" width="880" alt="Sequence diagram of rule 6: an open tab running build A meets a deploy of build B; on navigation, tab return or history restore it requests a fresh version; when the IDs differ and the next navigation is clean, the target URL loads as a full document; dirty input or a save in flight is protected; a failed version request leaves the app usable."></a>
</p>

## 🧪 Real-app acceptance checks

The guide lists 15 checks to run in a real app for the behavior you changed, recording each result or marking
it untested.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'xyChart': {'backgroundColor': '#131621', 'titleColor': '#E8ECF5', 'xAxisLabelColor': '#E8ECF5', 'yAxisLabelColor': '#E8ECF5', 'xAxisTitleColor': '#A7B0C4', 'yAxisTitleColor': '#A7B0C4', 'xAxisLineColor': '#8B93A7', 'yAxisLineColor': '#8B93A7', 'xAxisTickColor': '#8B93A7', 'yAxisTickColor': '#8B93A7', 'plotColorPalette': '#3D8BFF'}}}}%%
xychart-beta
    title "15 real-app checks by the rule section they exercise"
    x-axis ["Rules 1-3 structure", "Rule 4 async", "Rule 5 routing", "Rule 6 updates"]
    y-axis "checks" 0 --> 10
    bar [2, 1, 2, 10]
```

<p align="center"><sub>Rules 1–3: 2 · Rule 4: 1 · Rule 5: 2 · Rule 6: 10</sub></p>

<details open>
<summary><b>All 15 checks</b> (names translated from the guide)</summary>

| Rule section | Checks |
|---|---|
| 1–3 structure | JS and CSS sources · project conventions |
| 4 async | async errors and races |
| 5 routing | direct links and refresh · Back/Forward and 404 |
| 6 deployment updates | fresh entry A → B · already-open A tab · startup race · tab return and history restore · dirty input · editing while saving or checking · rollback B → A · version check failure · data-only update · asset and auth cache |

</details>

The grouping by rule section is ours; the guide lists the checks in one table.

## ✨ Optional: count-up and scroll animations

Only for landing, portfolio, and introduction pages, KPI summaries, or when you ask for it. The rules keep
content complete without motion, respect `prefers-reduced-motion`, animate only `transform` and `opacity`,
handle printing and BFCache restoration, never show `0` as a placeholder for API-fed numbers, and add their
own verification steps. See [`references/motion.md`](plugins/webapp6/skills/webapp6/references/motion.md).

> [!IMPORTANT]
> Never add this motion to data-entry screens, tables, or live values. If a motion rule conflicts with the
> six principles, the six principles win.

- 🧾 **Content first** — final numbers and text are in the HTML; the start state comes only from a class that script adds.
- 🐢 **Reduced motion** — with `prefers-reduced-motion: reduce`, the final state shows at once.
- 🎚 **Transform and opacity only** — no layout properties; space is reserved up front so nothing shifts.
- 🖨 **Print** — `@media print` cancels start states, or `beforeprint` settles every count-up.
- 🔁 **BFCache** — no cleanup in `unload`; what `pagehide` disconnects, `pageshow` reconnects when `event.persisted` is true.
- 🔢 **Formatting** — `Intl.NumberFormat`; Korean units such as 건·명·개 stay outside the number, because `style: 'unit'` throws `RangeError` for them.
- 🔈 **Screen readers** — the moving number is `aria-hidden="true"`; the final value lives in visually hidden text.
- 📡 **API numbers** — loading, empty, and error states each show; a count-up starts only from a successful response.
- 📜 **Scroll** — entrance effects and a progress indicator only, no scroll hijacking; the indicator shows only under `@supports (animation-timeline: scroll())`.

**Illustrative Example** — one ease-out curve that fits the rule. The rule itself asks for an ease-out over
1–2 seconds that ends exactly on the target value:

$$
v(t) = V\left(1-\left(1-\frac{t}{T}\right)^{3}\right), \qquad 1\text{ s} \le T \le 2\text{ s}, \qquad v(T) = V
$$

The header animation on this page uses this curve with `T = 1.2 s`: each tile lands exactly on its value, tiles
only fade and rise, the animation plays once, and a reduced-motion PNG shows the final state.

<table>
<tr>
<td width="50%" align="center"><a href="docs/art/cards/data-matplotlib.png"><img src="docs/art/cards/data-matplotlib.png" width="430" alt="The header&#x27;s count-up curve: a cubic ease-out over 1.2 s sampled every 50 ms that lands exactly on the final value, with a dashed linear reference."></a><br><sub>Matplotlib · the curve, sampled every 50 ms</sub></td>
<td width="50%" align="center"><a href="docs/art/cards/structure-wavedrom.png"><img src="docs/art/cards/structure-wavedrom.png" width="430" alt="Timing of this README&#x27;s header animation: six tiles start 100 ms apart, each fades in over 0.4 s and counts up over 1.2 s to 6, 3, 1, 15, 9 and 2; the animation plays once and stops on its last frame."></a><br><sub>WaveDrom · when each tile fades in and counts</sub></td>
</tr>
</table>

## 🔌 Install

### 🪐 Antigravity CLI (`agy`)

```sh
agy plugin install https://github.com/Technoetic/webapp6/tree/main/plugins/webapp6
```

> [!TIP]
> Pin to this release: `https://github.com/Technoetic/webapp6/tree/v0.1.0/plugins/webapp6`

### 🤖 Claude Code

```sh
claude plugin marketplace add Technoetic/webapp6
claude plugin install webapp6@technoetic-webapp6
```

On Claude Code 2.1.275 or later you can also install in one step inside a session:
`/plugin install webapp6 --marketplace Technoetic/webapp6`

### 🧠 Codex

```sh
codex plugin marketplace add Technoetic/webapp6
codex plugin add webapp6@technoetic-webapp6
```

## 🎯 Use

| Host | Invocation |
|---|---|
| Claude Code | `/webapp6:webapp6 review the checkout page` (or let the skill trigger on web-app work) |
| Codex | `$webapp6:webapp6 review the checkout page` |
| Antigravity CLI | `/webapp6 review the checkout page` (per the Antigravity docs; or let it trigger on web-app work) |

With no target, the skill tells the agent to apply the rules to the web-app work in the current conversation; if
there is none, to explain the rules and how to invoke it instead of creating an app.

## 🔒 What the plugin does and does not do

- 📦 Apart from its PNG icon it ships text only: one skill (`SKILL.md`), two reference documents, an agent display
  file (`agents/openai.yaml`), manifests, a README, and a license. No scripts, hooks, MCP servers, or network calls.
- 🙋 The skill tells agents not to install, deploy, or change host settings on their own, and to deploy only where
  and when you say so; your host's permissions and approvals still apply.
- 🧾 The skill tells agents to report what they actually verified separately from what is untested. Whether a host
  selects the skill and whether an agent follows it is not guaranteed: skill discovery proves delivery, not compliance.

## 📁 Repository layout

```text
.                                        ← repository root
├── .claude-plugin/marketplace.json      ← Claude Code marketplace
├── .agents/plugins/marketplace.json     ← Codex marketplace
├── .github/workflows/ci.yml             ← packaging tests on Ubuntu and Windows
├── docs/art/                            ← README art: header GIF and PNG, badges, 25 engine cards
├── plugins/webapp6/                     ← single installable plugin for all three hosts
│   ├── plugin.json                      ← Antigravity manifest
│   ├── .claude-plugin/plugin.json       ← Claude Code manifest
│   ├── .codex-plugin/plugin.json        ← Codex manifest
│   ├── assets/icon.png                  ← plugin icon (1024 x 1024), declared in all three manifests
│   └── skills/webapp6/                  ← the one skill
│       ├── SKILL.md                     ← checklist, how to run, invocation
│       ├── agents/openai.yaml           ← agent display file
│       └── references/
│           ├── webapp-principles.md     ← six principles + acceptance matrix
│           └── motion.md                ← optional count-up and scroll rules
└── tests/test_plugin.py                 ← packaging checks (run in CI)
```

<p align="center">
  <a href="docs/art/cards/structure-d2.png"><img src="docs/art/cards/structure-d2.png" width="880" alt="Nested containers: the repository, plugins/webapp6, skills/webapp6 with SKILL.md, and references with the two documents; each of the three manifests points to its host: Antigravity CLI, Claude Code and Codex."></a>
</p>

## 🎨 Visual tour: 25 engines

> [!NOTE]
> On this page only the Mermaid diagrams and the math render live on GitHub. Every card here is a static PNG
> drawn offline by the named engine from this repository (plugin facts at v0.1.0); the Structurizr card is
> drawn through PlantUML. Cards marked *illustrative* use example input because the repository has no such
> data (music, maps, a sample app).

Four more cards sit next to the text they explain: PlantUML in rule 6, Matplotlib and WaveDrom in the motion
rules, and D2 in the repository layout. Select a card to open it at full size.

<details open>
<summary><b>🎭 Structure and signals</b> · 6 cards</summary>

<table>
<tr><td align="center" valign="top" width="33%"><a href="docs/art/cards/structure-graphviz.png"><img src="docs/art/cards/structure-graphviz.png" width="280" alt="Package graph: the two marketplace files point to plugins/webapp6; each of the three manifests declares assets/icon.png and the Codex manifest declares skills/; SKILL.md links to webapp-principles.md once and to motion.md twice; tests/test_plugin.py checks the plugin folder."></a><br><b>Graphviz</b><br><sub>Package graph</sub></td><td align="center" valign="top" width="33%"><a href="docs/art/cards/structure-structurizr.png"><img src="docs/art/cards/structure-structurizr.png" width="280" alt="System context: a developer asks an AI coding host (Antigravity CLI, Claude Code or Codex) to build, change or review a web app; the host loads the webapp6 plugin and works on the web app against the six principles."></a><br><b>Structurizr</b><br><sub>Who uses webapp6</sub></td><td align="center" valign="top" width="33%"><a href="docs/art/cards/structure-markmap.png"><img src="docs/art/cards/structure-markmap.png" width="280" alt="Mind map of the English headings of webapp-principles.md and motion.md, some shortened: the six principles with rule 6&#x27;s three subsections, the real-app acceptance matrix with 15 checks, verification and handoff, and the optional motion rules with sections of 9, 5, 4 and 5 bullets."></a><br><b>markmap</b><br><sub>The guide as a mind map</sub></td></tr>
<tr><td align="center" valign="top" width="33%"><a href="docs/art/cards/structure-excalidraw.png"><img src="docs/art/cards/structure-excalidraw.png" width="280" alt="Illustrative example: a hand-drawn browser at example.app/orders/42; refresh keeps the same screen, Back and Forward keep URL and screen in step, and a missing /assets/app.js returns a real 404, not HTML 200."></a><br><b>Excalidraw</b> · <i>illustrative</i><br><sub>One page, many screens</sub></td><td align="center" valign="top" width="33%"><a href="docs/art/cards/structure-abcjs.png"><img src="docs/art/cards/structure-abcjs.png" width="280" alt="Illustrative example: the header&#x27;s six tile entrances written as six rising eighth notes, one every 100 ms, and a held note standing for the 1.2-second count-up (in the GIF each count-up starts at its tile&#x27;s entrance)."></a><br><b>abcjs</b> · <i>illustrative</i><br><sub>The header&#x27;s entrance rhythm</sub></td><td align="center" valign="top" width="33%"><a href="docs/art/cards/structure-mermaid.png"><img src="docs/art/cards/structure-mermaid.png" width="280" alt="Still render of this README&#x27;s first Mermaid diagram: one plugin folder, three manifests, three hosts, the shared SKILL.md and its two reference documents."></a><br><b>Mermaid</b><br><sub>One folder, three hosts (static)</sub></td></tr>
</table>

</details>

<details open>
<summary><b>📊 Data, statistics, networks and maps</b> · 11 cards</summary>

<table>
<tr><td align="center" valign="top" width="33%"><a href="docs/art/cards/data-echarts.png"><img src="docs/art/cards/data-echarts.png" width="280" alt="Sankey from plugins/webapp6 through each manifest to its host and invocation (/webapp6, /webapp6:webapp6, $webapp6:webapp6); every flow is 1 because it shows structure, not volume."></a><br><b>Apache ECharts</b><br><sub>One folder, three hosts</sub></td><td align="center" valign="top" width="33%"><a href="docs/art/cards/data-observable-plot.png"><img src="docs/art/cards/data-observable-plot.png" width="280" alt="Bytes per shipped plugin file at v0.1.0, from references/webapp-principles.md at 15,674 bytes down to agents/openai.yaml at 433 bytes; 39,997 bytes in total."></a><br><b>Observable Plot</b><br><sub>What an install receives</sub></td><td align="center" valign="top" width="33%"><a href="docs/art/cards/data-d3.png"><img src="docs/art/cards/data-d3.png" width="280" alt="The six principles on a ring around webapp6, with links from motion.md to the principles its rule sections cite: principles 1, 2, 3 and 5 once each and principle 4 twice; principle 6 is not cited."></a><br><b>D3</b><br><sub>Where the motion rules lean on the six</sub></td></tr>
<tr><td align="center" valign="top" width="33%"><a href="docs/art/cards/data-vega-lite.png"><img src="docs/art/cards/data-vega-lite.png" width="280" alt="Bar chart of the 15 real-app acceptance checks by rule section: rules 1 to 3 have 2, rule 4 has 1, rule 5 has 2 and rule 6 has 10, which is 67 percent."></a><br><b>Vega-Lite</b><br><sub>15 real-app checks by rule section</sub></td><td align="center" valign="top" width="33%"><a href="docs/art/cards/data-seaborn.png"><img src="docs/art/cards/data-seaborn.png" width="280" alt="Heatmap of how often 15 English terms, from rollback and build ID to IntersectionObserver and Intl.NumberFormat, appear in SKILL.md, webapp-principles.md and motion.md; Korean wording in the guide is not counted."></a><br><b>seaborn</b><br><sub>Where each English term appears</sub></td><td align="center" valign="top" width="33%"><a href="docs/art/cards/data-altair.png"><img src="docs/art/cards/data-altair.png" width="280" alt="Bytes per file role in the plugin: references 22,481, icon 6,719, skill 5,573, manifests 2,274, readme 1,450, license 1,067 and agent display 433; 39,997 bytes in total."></a><br><b>Altair</b><br><sub>Payload by file type</sub></td></tr>
<tr><td align="center" valign="top" width="33%"><a href="docs/art/cards/data-ggplot2.png"><img src="docs/art/cards/data-ggplot2.png" width="280" alt="Words per section in SKILL.md, webapp-principles.md and motion.md as box plots with each section as a dot; the longest section in each file is How to run (172 words), Real-app acceptance matrix (489) and Common (301)."></a><br><b>ggplot2</b><br><sub>How long each section runs</sub></td><td align="center" valign="top" width="33%"><a href="docs/art/cards/data-chartjs.png"><img src="docs/art/cards/data-chartjs.png" width="280" alt="Doughnut of the 10 shipped plugin files by kind: 3 manifests, 2 references, and one each of skill, agent display, icon, readme and license."></a><br><b>Chart.js</b><br><sub>Ten files, seven kinds</sub></td><td align="center" valign="top" width="33%"><a href="docs/art/cards/data-plotly.png"><img src="docs/art/cards/data-plotly.png" width="280" alt="Treemap of the 21 tracked files at v0.1.0, sized by bytes and nested by folder; 61,999 bytes in total."></a><br><b>Plotly</b><br><sub>Repository by size</sub></td></tr>
<tr><td align="center" valign="top" width="33%"><a href="docs/art/cards/data-cytoscape.png"><img src="docs/art/cards/data-cytoscape.png" width="280" alt="Graph of the 16 relative Markdown links among 7 repository files, merged into 15 edges; SKILL.md links to motion.md twice."></a><br><b>Cytoscape.js</b><br><sub>Document links</sub></td><td align="center" valign="top" width="33%"><a href="docs/art/cards/data-leaflet.png"><img src="docs/art/cards/data-leaflet.png" width="280" alt="Illustrative example: rule 5 as a route map of an invented single-page app on a flat, non-geographic plane, with screens /, /orders, /orders/42, /settings and /settings/profile, and a missing /assets/app.js that returns a real 404."></a><br><b>Leaflet</b> · <i>illustrative</i><br><sub>Rule 5 as a route map</sub></td><td></td></tr>
</table>

</details>

<details open>
<summary><b>🧮 Code and math</b> · 4 cards</summary>

<table>
<tr><td align="center" valign="top" width="33%"><a href="docs/art/cards/notation-mathjax.png"><img src="docs/art/cards/notation-mathjax.png" width="280" alt="Illustrative example: one ease-out count-up formula, v(t) = V(1 - (1 - t/T)^3) with T between 1 and 2 seconds and v(T) = V, typeset by MathJax."></a><br><b>MathJax</b> · <i>illustrative</i><br><sub>Ease-out count-up</sub></td><td align="center" valign="top" width="33%"><a href="docs/art/cards/notation-shiki.png"><img src="docs/art/cards/notation-shiki.png" width="280" alt="The README&#x27;s install commands for Antigravity CLI, Claude Code and Codex, highlighted by Shiki."></a><br><b>Shiki</b><br><sub>Install on three hosts</sub></td><td align="center" valign="top" width="33%"><a href="docs/art/cards/notation-highlightjs.png"><img src="docs/art/cards/notation-highlightjs.png" width="280" alt="The full Antigravity manifest plugins/webapp6/plugin.json (17 lines), highlighted by highlight.js."></a><br><b>highlight.js</b><br><sub>The Antigravity manifest</sub></td></tr>
<tr><td align="center" valign="top" width="33%"><a href="docs/art/cards/notation-katex.png"><img src="docs/art/cards/notation-katex.png" width="280" alt="Rule 6 as one condition typeset by KaTeX: a full load of the target URL follows when id_loaded differs from id_fresh and nothing is dirty or saving."></a><br><b>KaTeX</b><br><sub>Rule 6 as one condition</sub></td><td></td><td></td></tr>
</table>

</details>

## 🧬 Origin

The six principles are adapted from `docs/webapp-principles.md` in
[Technoetic/agentic-vault](https://github.com/Technoetic/agentic-vault) (MIT) so they can be installed on their own.

## 📜 License

[MIT](LICENSE)
