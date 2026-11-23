## Summary

- What changed and why:

## Verification checklist

- [ ] `python -m unittest discover -s tests -v` passes
- [ ] `python tools/generate_art.py --check` passes
- [ ] `python tools/build_release_zip.py --check-temp` passes
- [ ] `README.md` and `README.ko.md` are aligned (if user-facing docs changed)
- [ ] `plugins/webapp6/` remains text + icon only (no scripts, hooks, MCP, or network calls)
