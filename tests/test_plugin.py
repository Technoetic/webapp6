"""Packaging checks for webapp6: catalogs, host manifests, license, skill, references, links, and text hygiene."""
import json
from pathlib import Path
import re
import struct
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "webapp6"
SKILL = PLUGIN / "skills" / "webapp6" / "SKILL.md"
INVISIBLE = {chr(c) for c in (0xFEFF, 0x200B, 0x200C, 0x200D, 0x200E, 0x200F, 0x00AD, 0x2060,
                              0x202A, 0x202B, 0x202C, 0x202D, 0x202E, 0x2066, 0x2067, 0x2068, 0x2069)}
TEXT_SUFFIXES = {".md", ".json", ".yml", ".yaml", ".py", ".txt"}
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


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def local_links(markdown_path):
    for link in re.findall(r"\]\(([^)\s]+)\)", markdown_path.read_text(encoding="utf-8")):
        url = urlsplit(link)
        if url.scheme or url.netloc or link.startswith("#"):
            continue
        yield link, (markdown_path.parent / unquote(url.path)).resolve()


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

    def test_plugin_ships_text_only(self):
        shipped = {p.relative_to(PLUGIN).as_posix() for p in PLUGIN.rglob("*") if p.is_file()
                   and "__pycache__" not in p.parts}
        self.assertEqual(shipped, PLUGIN_FILES)

    def test_icon_is_a_square_png_declared_by_all_hosts(self):
        icon = PLUGIN / "assets" / "icon.png"
        claude = load(PLUGIN / ".claude-plugin" / "plugin.json")
        codex = load(PLUGIN / ".codex-plugin" / "plugin.json")
        antigravity = load(PLUGIN / "plugin.json")
        for declared in (claude["icon"], codex["interface"]["logo"], codex["interface"]["composerIcon"],
                         antigravity["logo"]):
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
        root = (ROOT / "LICENSE").read_bytes().replace(b"\r\n", b"\n")
        self.assertEqual(root, (PLUGIN / "LICENSE").read_bytes().replace(b"\r\n", b"\n"))
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

    def test_guide_keeps_six_rules_matrix_and_motion_checks(self):
        guide = (PLUGIN / "skills/webapp6/references/webapp-principles.md").read_text(encoding="utf-8")
        for number in range(1, 7):
            self.assertRegex(guide, rf"(?m)^## {number}\. ")
        self.assertIn("## 실제 앱 합격 기준 / Real-app acceptance matrix", guide)
        motion = (PLUGIN / "skills/webapp6/references/motion.md").read_text(encoding="utf-8")
        for needle in ("prefers-reduced-motion", "@media print", "pageshow", "aria-hidden=\"true\"",
                       "animation-timeline", "## 검증 / Verification"):
            self.assertIn(needle, motion)

    def test_links_inside_the_plugin_stay_inside_the_plugin(self):
        for markdown in PLUGIN.rglob("*.md"):
            for link, target in local_links(markdown):
                self.assertTrue(target.exists(), f"{markdown.relative_to(ROOT)} -> {link}")
                self.assertIn(PLUGIN.resolve(), [target, *target.parents], f"{link} leaves the plugin folder")

    def test_repository_readme_links_resolve(self):
        for readme in ("README.md", "README.ko.md"):
            for link, target in local_links(ROOT / readme):
                self.assertTrue(target.exists(), f"{readme} -> {link}")

    def test_text_hygiene(self):
        checked = 0
        for path in sorted(ROOT.rglob("*")):
            if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
                continue
            if path.suffix not in TEXT_SUFFIXES and path.name != "LICENSE":
                continue
            data = path.read_bytes()
            text = data.decode("utf-8")
            name = path.relative_to(ROOT).as_posix()
            self.assertNotIn(b"\r", data, f"{name}: CR line ending")
            self.assertTrue(text.endswith("\n"), f"{name}: missing final newline")
            self.assertFalse(INVISIBLE & set(text), f"{name}: invisible character")
            if path != Path(__file__).resolve():  # this file defines the pattern itself
                self.assertIsNone(LEAK.search(text), f"{name}: possible private detail")
            checked += 1
        self.assertGreater(checked, 10)


if __name__ == "__main__":
    unittest.main()
