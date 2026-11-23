# Contributing to webapp6

Contributions that sharpen the six principles, tighten the real-app acceptance checks, or improve
three-host plugin packaging are welcome.

## Development workflow

1. Fork the repository and create a topic branch from `main`.
2. Keep `plugins/webapp6/` text-only apart from `assets/icon.png` (no runtime scripts, hooks, MCP
   servers, or network calls).
3. Keep all three host manifests (`plugin.json`, `.claude-plugin/plugin.json`,
   `.codex-plugin/plugin.json`) and `.claude-plugin/marketplace.json` synchronized.
4. When version numbers, checks, or test counts change, regenerate the README assets with Python 3
   (standard library only):

   ```sh
   python tools/generate_art.py
   ```

5. Verify everything before opening a pull request:

   ```sh
   python -m unittest discover -s tests -v
   python tools/generate_art.py --check
   python tools/build_release_zip.py --check-temp
   ```

   If you have Claude Code or Antigravity CLI installed, also verify:

   ```sh
   claude plugin validate --profile directory plugins/webapp6
   agy plugin validate --strict plugins/webapp6
   ```

## Style and hygiene

- Use UTF-8 with LF line endings and a trailing newline on all text files (enforced by tests).
- Never include local machine paths, credentials, or personal contact details.
- Keep `README.md` (English) and `README.ko.md` (Korean) aligned in structure and facts.
- Follow the [Code of Conduct](CODE_OF_CONDUCT.md).
