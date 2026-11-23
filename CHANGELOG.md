# Changelog

## 0.2.0 — 2026-11-23

- **English canonical references and aligned Codex metadata:** Rewrote `references/webapp-principles.md`
  and `references/motion.md` as full English canonical guides (preserving all six principles, all 15
  real-app acceptance checks, the six-field handoff, and every motion rule), pinned upstream provenance
  to `Technoetic/agentic-vault` `v0.56.0` (MIT), and aligned `agents/openai.yaml` with the English
  manifests.
- **Slim, 100% reproducible README art:** Replaced the prior `docs/art/` assets (`1.68 MiB`, 95.4% of the
  repository, including 25 external static PNG cards at `1.32 MiB`) with a zero-dependency Python 3
  standard-library generator (`tools/generate_art.py`) that deterministically generates the badges,
  play-once count-up `hero.gif` / reduced-motion `hero.png`, and two purposeful vector diagrams
  (`docs/art/rule6-sequence.svg`, `docs/art/motion-curve.svg`), shrinking `docs/art/` to `~99 KiB`.
- **Synchronized bilingual READMEs:** Streamlined `README.md` (compact Rule 6 flowchart, focused visual
  hierarchy) and synchronized `README.ko.md` with matching live Mermaid diagrams, math, alerts, hero,
  badges, and vector diagrams.
- **Deterministic slim release packaging and expanded checks:** Added `tools/build_release_zip.py`
  (UTC deterministic slim plugin ZIP + `SHA256SUMS.txt`), expanded `tests/test_plugin.py` to check HTML
  image/link targets, internal heading anchors, `.svg`/`.gitattributes` hygiene, `agents/openai.yaml`
  structure, art zero-drift reproducibility, and ZIP determinism, and added `CONTRIBUTING.md`,
  `CODE_OF_CONDUCT.md`, and issue/PR templates.

## 0.1.0 — 2026-11-23

- First release: the `webapp6` skill for Antigravity CLI, Claude Code, and Codex from one plugin folder.
- Six web-app principles and the real-app acceptance matrix, adapted from Technoetic/agentic-vault (MIT).
- Optional count-up and scroll-animation rules with their own verification steps.
- Packaging tests and CI on Ubuntu and Windows.
