# Security

## What this plugin contains

Apart from its PNG icon (`assets/icon.png`), webapp6 ships text only: one skill (`SKILL.md`), two reference documents, an
agent display file (`agents/openai.yaml`), manifests, a README, and a license. It has no scripts, hooks,
MCP servers, executables, or network calls, and it asks no host for extra permissions.

The skill tells agents not to install packages, deploy, or change host settings on their own. Any such
action still goes through the permissions and approvals of the host you run (Antigravity CLI, Claude Code,
or Codex).

## Reporting a problem

Please report security concerns through GitHub's private vulnerability reporting on this repository
(Security tab, "Report a vulnerability"). Do not include secrets or private data in public issues.
