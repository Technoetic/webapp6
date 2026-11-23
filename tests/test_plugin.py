"""Packaging, link, anchor, hygiene, art-reproducibility, and release-ZIP tests for webapp6."""
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "webapp6"
SKILL = PLUGIN / "skills" / "webapp6" / "SKILL.md"
INVISIBLE = {chr(c) for c in (
    0xFEFF, 0x00AD, 0x034F, 0x061C, 0x200B, 0x200C, 0x200D, 0x200E, 0x200F,
    0x202A, 0x202B, 0x202C, 0x202D, 0x202E, 0x2060, 0x2066, 0x2067, 0x2068,
    0x2069, 0x3164, 0xFFA0,
)}
TEXT_SUFFIXES = {".md", ".json", ".yml", ".yaml", ".py", ".txt", ".svg"}
TEXT_NAMES = {"LICENSE", ".gitattributes", ".gitignore"}
# Catches local paths, profile folders, and e-mail addresses before a release.
LEAK = re.compile(r"(?<![A-Za-z])[A-Za-z]:[\\/](?![\\/])|[\\/]Users[\\/]|AppData|[\w.+-]+@[\w-]+\.[\w.]+")
# The README promises text only apart from the icon: these are the only files an install receives.
PLUGIN_FILES = {
    "LICENSE",
    "README.md",
    "plugin.json",
    ".claude-plugin/plugin.json",
    "assets/icon.png",
    ".codex-plugin/plugin.json",
    "skills/webapp6/SKILL.md",
    "skills/webapp6/agents/openai.yaml",
    "skills/webapp6/references/webapp-principles.md",
    "skills/webapp6/references/motion.md",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def all_refs(markdown_path: Path):
    """Yield every local Markdown link and HTML src/href/srcset reference (excluding external URLs)."""
    text = markdown_path.read_text(encoding="utf-8")
    patterns = (
        re.findall(r"\]\(([^)\s]+)\)", text),
        re.findall(r'(?:src|href|srcset)="([^"]+)"', text),
    )
    for matches in patterns:
        for ref in matches:
            url = urlsplit(ref)
            if url.scheme or url.netloc or ref.startswith("#"):
                continue
            yield ref, (markdown_path.parent / unquote(url.path)).resolve()


def github_heading_slugs(markdown_text: str) -> set[str]:
    """Compute GitHub-compatible heading anchor slugs for ATX markdown and <h1..h6> HTML headings."""
    slugs: set[str] = set()
    counts: dict[str, int] = {}
    in_fence = False
    for line in markdown_text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        heading = None
        m = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if m:
            heading = m.group(1)
        else:
            mh = re.match(r"^<h[1-6][^>]*>(.+?)</h[1-6]>", line.strip(), re.I)
            if mh:
                heading = re.sub(r"<[^>]+>", "", mh.group(1))
        if heading is None:
            continue
        clean = re.sub(r"`([^`]*)`", r"\1", heading)
        clean = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", clean)
        out = []
        for ch in clean.lower():
            if ch == " " or ch == "-":
                out.append("-")
            elif ch.isalnum() or ch == "_":
                out.append(ch)
        base = "".join(out)
        n = counts.get(base, 0)
        counts[base] = n + 1
        slugs.add(base if n == 0 else f"{base}-{n}")
    return slugs


class PackagingTests(unittest.TestCase):
    def test_catalogs_and_host_manifests_agree(self):
        claude = load(ROOT / ".claude-plugin" / "marketplace.json")
        codex = load(ROOT / ".agents" / "plugins" / "marketplace.json")
        self.assertEqual(claude["name"], codex["name"])
        claude_entry, = claude["plugins"]
        codex_entry, = codex["plugins"]
        self.assertEqual(codex_entry["source"]["source"], "local")
        package = (ROOT / claude_entry["source"]).resolve()
        self.assertEqual(package, (ROOT / codex_entry["source"]["path"]).resolve())
        self.assertEqual(package, PLUGIN.resolve())

        hosts = [
            load(PLUGIN / ".claude-plugin" / "plugin.json"),
            load(PLUGIN / ".codex-plugin" / "plugin.json"),
            load(PLUGIN / "plugin.json"),
        ]
        for host in hosts:
            self.assertEqual(host["name"], "webapp6")
            self.assertEqual(host["name"], claude_entry["name"])
            self.assertEqual(host["name"], codex_entry["name"])
            self.assertEqual(host["version"], claude_entry["version"])
            self.assertEqual(host["description"], claude_entry["description"])
            self.assertEqual(host["license"], "MIT")
            self.assertEqual(host["repository"], "https://github.com/Technoetic/webapp6")
        self.assertEqual((PLUGIN / hosts[1]["skills"]).resolve(), (PLUGIN / "skills").resolve())

        version = claude_entry["version"]
        self.assertRegex(version, r"^\d+\.\d+\.\d+$")
        self.assertIn(f"## {version} ", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"))
        for readme in ("README.md", "README.ko.md"):
            self.assertIn(f"v{version}", (ROOT / readme).read_text(encoding="utf-8"))

    def test_plugin_ships_text_and_icon_only(self):
        shipped = {
            p.relative_to(PLUGIN).as_posix()
            for p in PLUGIN.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts
        }
        self.assertEqual(shipped, PLUGIN_FILES)

    def test_icon_is_a_square_png_declared_by_all_hosts(self):
        icon = PLUGIN / "assets" / "icon.png"
        claude = load(PLUGIN / ".claude-plugin" / "plugin.json")
        codex = load(PLUGIN / ".codex-plugin" / "plugin.json")
        antigravity = load(PLUGIN / "plugin.json")
        for declared in (
            claude["icon"], codex["interface"]["logo"], codex["interface"]["composerIcon"],
            antigravity["logo"],
        ):
            self.assertEqual((PLUGIN / declared).resolve(), icon.resolve())
        # Codex silently drops interface assets and skills paths that do not start with "./".
        for value in (claude["icon"], codex["interface"]["logo"], codex["interface"]["composerIcon"], codex["skills"]):
            self.assertTrue(value.startswith("./"), value)
        data = icon.read_bytes()
        self.assertLess(len(data), 2 * 1024 * 1024)
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        width, height = struct.unpack(">II", data[16:24])
        self.assertEqual(width, height)
        self.assertTrue(512 <= width <= 2048)

    def test_license_is_shipped_with_the_plugin(self):
        root = (ROOT / "LICENSE").read_bytes()
        self.assertEqual(root, (PLUGIN / "LICENSE").read_bytes())
        self.assertTrue(root.startswith(b"MIT License\n\nCopyright (c) 2026 Technoetic\n"))

    def test_single_skill_with_valid_front_matter(self):
        skills = sorted((PLUGIN / "skills").glob("*/SKILL.md"))
        self.assertEqual([p.parent.name for p in skills], ["webapp6"])
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        head = text.split("---", 2)[1]
        self.assertRegex(head, r"(?m)^name: webapp6$")
        description = re.search(r'(?m)^description: "(.+)"$', head)
        self.assertIsNotNone(description)
        self.assertLessEqual(len(description.group(1)), 1024)
        for reference in ("references/webapp-principles.md", "references/motion.md"):
            self.assertIn(f"]({reference})", text)

    def test_openai_yaml_structure_and_english_alignment(self):
        yaml_path = PLUGIN / "skills/webapp6/agents/openai.yaml"
        lines = yaml_path.read_text(encoding="utf-8").splitlines()
        self.assertEqual(lines[0], "interface:")
        parsed = {}
        for line in lines[1:]:
            self.assertFalse("\t" in line, "tabs not allowed in openai.yaml")
            m = re.fullmatch(r'  ([a-z_]+): "([^"]+)"', line)
            self.assertIsNotNone(m, f"invalid YAML line: {line!r}")
            parsed[m.group(1)] = m.group(2)
        self.assertEqual(set(parsed), {"display_name", "short_description", "default_prompt"})
        self.assertTrue(parsed["default_prompt"].startswith("$webapp6:webapp6 "))
        # Must stay English to match .codex-plugin/plugin.json
        for k, v in parsed.items():
            self.assertIsNone(re.search(r"[가-힣]", v), f"openai.yaml {k} should be English")

    def test_canonical_references_are_complete_and_english(self):
        guide = (PLUGIN / "skills/webapp6/references/webapp-principles.md").read_text(encoding="utf-8")
        for number in range(1, 7):
            self.assertRegex(guide, rf"(?m)^## {number}\. ")
        for needle in (
            "### Build identity and HTTP cache",
            "### Already-open tabs and the next navigation",
            "### Data freshness is separate",
            "## Real-app acceptance matrix",
            "## Verification and handoff",
            "`verified_by`",
            "v0.56.0",
        ):
            self.assertIn(needle, guide)
        matrix = guide.split("## Real-app acceptance matrix", 1)[1].split("## Verification and handoff", 1)[0]
        rows = [ln for ln in matrix.splitlines() if ln.startswith("|") and not ln.startswith(("| Check |", "|---"))]
        self.assertEqual(len(rows), 15)
        self.assertIsNone(re.search(r"[가-힣]", guide), "webapp-principles.md canonical guide must be English")

        motion = (PLUGIN / "skills/webapp6/references/motion.md").read_text(encoding="utf-8")
        for needle in (
            "prefers-reduced-motion",
            "@media print",
            "pageshow",
            'aria-hidden="true"',
            "Intl.NumberFormat",
            "animation-timeline",
            "## Verification",
        ):
            self.assertIn(needle, motion)
        # Only the illustrative Korean unit note ('건', '명', '개') may contain Hangul characters.
        hangul_count = len(re.findall(r"[가-힣]", motion))
        self.assertLessEqual(hangul_count, 5, f"motion.md canonical guide should be English (found {hangul_count} Hangul chars)")

    def test_links_inside_the_plugin_stay_inside_the_plugin(self):
        for markdown in PLUGIN.rglob("*.md"):
            for link, target in all_refs(markdown):
                self.assertTrue(target.exists(), f"{markdown.relative_to(ROOT)} -> {link}")
                self.assertIn(PLUGIN.resolve(), [target, *target.parents], f"{link} leaves the plugin folder")

    def test_repository_readme_markdown_and_html_links_resolve(self):
        for readme in ("README.md", "README.ko.md"):
            refs = list(all_refs(ROOT / readme))
            self.assertGreaterEqual(len(refs), 10)
            for link, target in refs:
                self.assertTrue(target.exists(), f"{readme} -> {link}")

    def test_repository_readme_internal_anchors_resolve(self):
        for readme in ("README.md", "README.ko.md"):
            text = (ROOT / readme).read_text(encoding="utf-8")
            slugs = github_heading_slugs(text)
            # Extract both HTML href="#..." and Markdown ](#...)
            html_hashes = re.findall(r'href="#([^"]+)"', text)
            md_hashes = re.findall(r'\]\(#([^)\s]+)\)', text)
            all_hashes = html_hashes + md_hashes
            self.assertGreaterEqual(len(all_hashes), 4, f"{readme} should have internal anchors")
            for h in all_hashes:
                self.assertIn(unquote(h), slugs, f"{readme}: broken internal anchor #{h}")

    def test_text_and_svg_hygiene(self):
        checked = 0
        svg_checked = 0
        for path in sorted(ROOT.rglob("*")):
            if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
                continue
            if path.suffix not in TEXT_SUFFIXES and path.name not in TEXT_NAMES:
                continue
            data = path.read_bytes()
            text = data.decode("utf-8")
            name = path.relative_to(ROOT).as_posix()
            self.assertNotIn(b"\r", data, f"{name}: CR line ending")
            self.assertTrue(text.endswith("\n"), f"{name}: missing final newline")
            self.assertFalse(INVISIBLE & set(text), f"{name}: invisible character")
            if path != Path(__file__).resolve():
                self.assertIsNone(LEAK.search(text), f"{name}: possible private detail")
            if path.suffix == ".svg":
                ET.fromstring(text)
                self.assertIsNone(re.search(r"<script|on[a-z]+\s*=", text, re.I), f"{name}: active script in SVG")
                svg_checked += 1
            checked += 1
        self.assertGreater(checked, 20)
        self.assertGreaterEqual(svg_checked, 9)

    def test_generated_art_is_reproducible_and_in_sync(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "tools/generate_art.py"), "--check"],
            cwd=ROOT, capture_output=True, text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_hero_gif_plays_once_and_matches_png_dimensions(self):
        gif = (ROOT / "docs/art/hero.gif").read_bytes()
        png = (ROOT / "docs/art/hero.png").read_bytes()
        self.assertTrue(gif.startswith(b"GIF89a"))
        self.assertTrue(png.startswith(b"\x89PNG\r\n\x1a\n"))
        gw, gh = struct.unpack("<HH", gif[6:10])
        pw, ph = struct.unpack(">II", png[16:24])
        self.assertEqual((gw, gh), (pw, ph))
        self.assertNotIn(b"NETSCAPE2.0", gif, "hero.gif must play once without infinite loop extension")
        self.assertGreater(gif.count(b"\x21\xf9\x04"), 10, "hero.gif should have smooth count-up frames")

    def test_release_zip_is_deterministic_and_slim(self):
        import hashlib

        with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
            for d in (d1, d2):
                p = subprocess.run(
                    [sys.executable, str(ROOT / "tools/build_release_zip.py"), "--out", d],
                    cwd=ROOT, capture_output=True, text=True,
                )
                self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            zips1 = list(Path(d1).glob("webapp6-plugin-*.zip"))
            zips2 = list(Path(d2).glob("webapp6-plugin-*.zip"))
            self.assertEqual(len(zips1), 1)
            raw = zips1[0].read_bytes()
            self.assertEqual(raw, zips2[0].read_bytes())
            self.assertLess(len(raw), 100 * 1024)
            digest = hashlib.sha256(raw).hexdigest()
            sums = (Path(d1) / "SHA256SUMS.txt").read_text(encoding="utf-8").strip()
            self.assertEqual(sums, f"{digest}  {zips1[0].name}")
            with zipfile.ZipFile(zips1[0]) as zf:
                names = {n.removeprefix("webapp6/") for n in zf.namelist()}
            self.assertEqual(names, PLUGIN_FILES)

    def test_ci_workflow_pins_actions_and_runs_all_checks(self):
        ci = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        uses = re.findall(r"uses:\s*([^\s#]+)", ci)
        self.assertGreaterEqual(len(uses), 2)
        for action in uses:
            self.assertRegex(action, r"@[0-9a-f]{40}$", f"action not pinned to SHA-40: {action}")
        self.assertIn("contents: read", ci)
        self.assertIn("persist-credentials: false", ci)
        self.assertIn("tools/generate_art.py --check", ci)
        self.assertIn("tools/build_release_zip.py --check-temp", ci)

    def test_community_and_security_files_exist(self):
        for rel in (
            "LICENSE",
            "SECURITY.md",
            "CONTRIBUTING.md",
            "CODE_OF_CONDUCT.md",
            ".github/ISSUE_TEMPLATE/bug_report.md",
            ".github/ISSUE_TEMPLATE/rule_proposal.md",
            ".github/pull_request_template.md",
        ):
            self.assertTrue((ROOT / rel).is_file(), f"missing community/security file: {rel}")


if __name__ == "__main__":
    unittest.main()
