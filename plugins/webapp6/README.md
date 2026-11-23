# webapp6 plugin

One skill, `webapp6`, that tells an agent to apply six web-app principles when it builds,
changes, or reviews a web app, with optional count-up and scroll-animation rules.

- Skill: [`skills/webapp6/SKILL.md`](skills/webapp6/SKILL.md)
- Six principles and the real-app acceptance matrix: [`skills/webapp6/references/webapp-principles.md`](skills/webapp6/references/webapp-principles.md)
- Optional motion rules: [`skills/webapp6/references/motion.md`](skills/webapp6/references/motion.md)

The same folder installs on Antigravity CLI (`plugin.json`), Claude Code (`.claude-plugin/plugin.json`),
and Codex (`.codex-plugin/plugin.json`). Apart from its PNG icon it is text only: no scripts, hooks,
MCP servers, or network calls. MIT licensed.

## Install

Claude Code 2.1.275 or later, in one step inside a session:

```text
/plugin install webapp6 --marketplace Technoetic/webapp6
```

Other hosts and versions:

```sh
claude plugin marketplace add Technoetic/webapp6 && claude plugin install webapp6@technoetic-webapp6
agy plugin install https://github.com/Technoetic/webapp6/tree/main/plugins/webapp6
codex plugin marketplace add Technoetic/webapp6 && codex plugin add webapp6@technoetic-webapp6
```

## Use

- Claude Code: `/webapp6:webapp6 <request>`
- Codex: `$webapp6:webapp6 <request>`
- Antigravity CLI: `/webapp6 <request>` (per the Antigravity docs)

More in the [repository README](https://github.com/Technoetic/webapp6).
