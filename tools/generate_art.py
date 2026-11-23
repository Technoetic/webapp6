#!/usr/bin/env python3
"""Zero-dependency Python 3 stdlib generator for all webapp6 README art assets.

Generates deterministically under docs/art/:
  - docs/art/badges/*.svg     (7 two-tone WCAG-contrasted SVG badges)
  - docs/art/hero.gif         (play-once 960x440 cubic ease-out count-up GIF89a, no loop ext)
  - docs/art/hero.png         (identical 960x440 final-frame PNG for prefers-reduced-motion)
  - docs/art/rule6-sequence.svg (vector sequence diagram for Rule 6 deployment updates)
  - docs/art/motion-curve.svg   (vector cubic ease-out curve + tile stagger timeline)

Run `python tools/generate_art.py` to regenerate, or `python tools/generate_art.py --check`
to verify zero drift against repository metadata.
"""
from __future__ import annotations

import argparse
import ast
import json
import math
from pathlib import Path
import re
import struct
import sys
import unicodedata
from xml.sax.saxutils import escape
import zlib

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "webapp6"
ART = ROOT / "docs" / "art"

HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
DEFAULT_LABEL_BG = "#1E2436"

# 16-color indexed palette for compact 4-bit GIF89a and indexed PNG
PALETTE_HEX = (
    "#0B0F1A",  # 0: obsidian background
    "#131929",  # 1: tile fill
    "#1E293B",  # 2: dot grid / bar track
    "#2A3550",  # 3: tile border
    "#94A3B8",  # 4: muted label text
    "#F8FAFC",  # 5: bright white title / digits
    "#00F5D4",  # 6: electric cyan
    "#FF2E93",  # 7: hot magenta
    "#C8FF00",  # 8: acid lime
    "#FF9E00",  # 9: solar amber
    "#7B61FF",  # 10: ultraviolet
    "#38BDF8",  # 11: sky blue
    "#CBD5E1",  # 12: subtitle text
    "#0D3B3F",  # 13: cyan dim
    "#471534",  # 14: magenta dim
    "#293548",  # 15: subtle divider
)
PALETTE_RGB = tuple((int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)) for h in PALETTE_HEX)

# Crisp 5x7 bitmap glyphs (rows top-to-bottom, 5 bits MSB-left)
FONT_5X7: dict[str, tuple[str, ...]] = {
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    "-": ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    "/": ("00001", "00010", "00100", "01000", "10000", "00000", "00000"),
    "·": ("00000", "00000", "00000", "00100", "00000", "00000", "00000"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("01110", "10000", "11110", "10001", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01111", "10000", "10000", "10000", "10000", "10000", "01111"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01111", "10000", "10000", "10111", "10001", "10001", "01110"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "10010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
}


def collect_repo_metrics() -> dict[str, object]:
    manifest = json.loads((PLUGIN / "plugin.json").read_text(encoding="utf-8"))
    version = manifest["version"]
    plugin_files = [p for p in PLUGIN.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    plugin_bytes = sum(p.stat().st_size for p in plugin_files)

    guide_text = (PLUGIN / "skills/webapp6/references/webapp-principles.md").read_text(encoding="utf-8")
    matrix_section = guide_text.split("## Real-app acceptance matrix", 1)[1].split("## Verification and handoff", 1)[0]
    matrix_rows = [
        ln for ln in matrix_section.splitlines()
        if ln.startswith("|") and not ln.startswith("| Check |") and not ln.startswith("|---")
    ]

    test_tree = ast.parse((ROOT / "tests/test_plugin.py").read_text(encoding="utf-8"))
    test_count = sum(
        1 for node in ast.walk(test_tree)
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
    )

    ci_text = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    os_match = re.search(r"os:\s*\[([^\]]+)\]", ci_text)
    ci_os_count = len([x.strip() for x in os_match.group(1).split(",") if x.strip()]) if os_match else 2

    return {
        "version": version,
        "principles": 6,
        "hosts": 3,
        "skills": 1,
        "checks": len(matrix_rows),
        "tests": test_count,
        "ci_oses": ci_os_count,
        "plugin_files": len(plugin_files),
        "plugin_bytes": plugin_bytes,
    }


def _text_width(text: str) -> int:
    cells = sum(
        2 if unicodedata.east_asian_width(c) in ("W", "F") else 1
        for c in text if unicodedata.category(c) not in ("Mn", "Me", "Cf")
    )
    return max(8, math.ceil(7.4 * cells))


def _ink_color(bg: str) -> str:
    if not HEX_RE.fullmatch(bg):
        raise ValueError(f"Invalid hex color: {bg!r}")
    channels = [int(bg[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    lum = sum(k * c for k, c in zip((0.2126, 0.7152, 0.0722), linear))
    return "#FFFFFF" if 1.05 / (lum + 0.05) >= (lum + 0.05) / 0.05 else "#0B0F1A"


def badge_svg(label: str, value: str, color: str, label_bg: str = DEFAULT_LABEL_BG) -> bytes:
    lw, vw = _text_width(label), _text_width(value)
    split = lw + 18
    width = split + vw + 18
    li, vi = _ink_color(label_bg), _ink_color(color)
    le, ve = escape(label), escape(value)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="28" viewBox="0 0 {width} 28" '
        f'role="img" aria-labelledby="title">\n'
        f'  <title id="title">{le}: {ve}</title>\n'
        f'  <clipPath id="r"><rect width="{width}" height="28" rx="4" fill="#fff"/></clipPath>\n'
        f'  <g clip-path="url(#r)">\n'
        f'    <rect width="{split}" height="28" fill="{label_bg}"/>\n'
        f'    <rect x="{split}" width="{width - split}" height="28" fill="{color}"/>\n'
        f'  </g>\n'
        f'  <g font-family="Verdana, DejaVu Sans, sans-serif" font-size="11" font-weight="700" '
        f'text-anchor="middle" letter-spacing=".5">\n'
        f'    <text x="{split / 2:g}" y="18" fill="{li}" textLength="{lw}" lengthAdjust="spacingAndGlyphs">{le}</text>\n'
        f'    <text x="{(split + width) / 2:g}" y="18" fill="{vi}" textLength="{vw}" lengthAdjust="spacingAndGlyphs">{ve}</text>\n'
        f'  </g>\n'
        f'</svg>\n'
    )
    return svg.encode("utf-8")


def _fill_rect(buf: bytearray, w: int, h: int, x0: int, y0: int, x1: int, y1: int, c: int) -> None:
    x0, x1 = max(0, min(w, x0)), max(0, min(w, x1))
    y0, y1 = max(0, min(h, y0)), max(0, min(h, y1))
    if x1 <= x0 or y1 <= y0:
        return
    span = bytes([c]) * (x1 - x0)
    for y in range(y0, y1):
        row = y * w
        buf[row + x0 : row + x1] = span


def _stroke_rect(buf: bytearray, w: int, h: int, x0: int, y0: int, x1: int, y1: int, c: int, t: int = 2) -> None:
    _fill_rect(buf, w, h, x0, y0, x1, y0 + t, c)
    _fill_rect(buf, w, h, x0, y1 - t, x1, y1, c)
    _fill_rect(buf, w, h, x0, y0, x0 + t, y1, c)
    _fill_rect(buf, w, h, x1 - t, y0, x1, y1, c)


def _draw_text(buf: bytearray, w: int, h: int, x: int, y: int, text: str, scale: int, c: int, gap: int = 1) -> None:
    cursor = x
    for ch in text.upper():
        glyph = FONT_5X7.get(ch, FONT_5X7[" "])
        for ry, row in enumerate(glyph):
            for rx, bit in enumerate(row):
                if bit == "1":
                    _fill_rect(
                        buf, w, h,
                        cursor + rx * scale, y + ry * scale,
                        cursor + (rx + 1) * scale, y + (ry + 1) * scale,
                        c,
                    )
        cursor += (5 + gap) * scale


def _lzw_encode_gif(pixels: bytes, min_code_size: int = 4) -> bytes:
    clear_code = 1 << min_code_size
    eoi_code = clear_code + 1
    next_code = eoi_code + 1
    code_size = min_code_size + 1
    max_code = 1 << code_size
    out = bytearray()
    bit_buf = 0
    bit_cnt = 0

    def emit(code: int) -> None:
        nonlocal bit_buf, bit_cnt
        bit_buf |= code << bit_cnt
        bit_cnt += code_size
        while bit_cnt >= 8:
            out.append(bit_buf & 0xFF)
            bit_buf >>= 8
            bit_cnt -= 8

    emit(clear_code)
    table: dict[int, int] = {}
    prefix = pixels[0]
    for k in pixels[1:]:
        key = (prefix << 8) | k
        found = table.get(key)
        if found is not None:
            prefix = found
        else:
            emit(prefix)
            if next_code < 4096:
                table[key] = next_code
                next_code += 1
                if next_code > max_code and code_size < 12:
                    code_size += 1
                    max_code = 1 << code_size
            else:
                emit(clear_code)
                table.clear()
                next_code = eoi_code + 1
                code_size = min_code_size + 1
                max_code = 1 << code_size
            prefix = k
    emit(prefix)
    emit(eoi_code)
    if bit_cnt > 0:
        out.append(bit_buf & 0xFF)
    return bytes(out)


def _encode_play_once_gif(frames: list[bytes], width: int, height: int, delay_cs: int = 5) -> bytes:
    """Encode indexed 16-color frames into a compact play-once GIF89a (NO NETSCAPE2.0 loop block)."""
    out = bytearray(b"GIF89a")
    out.extend(struct.pack("<HHBBB", width, height, 0xF3, 0, 0))
    for r, g, b in PALETTE_RGB:
        out.extend((r, g, b))
    prev: bytes | None = None
    for i, pixels in enumerate(frames):
        d = 200 if i == len(frames) - 1 else delay_cs
        if prev is None:
            x0, y0, sw, sh = 0, 0, width, height
            sub = pixels
        else:
            min_x, min_y, max_x, max_y = width, height, -1, -1
            for y in range(height):
                row_off = y * width
                cur_row = pixels[row_off : row_off + width]
                prev_row = prev[row_off : row_off + width]
                if cur_row != prev_row:
                    if y < min_y:
                        min_y = y
                    max_y = y
                    for x in range(width):
                        if cur_row[x] != prev_row[x]:
                            if x < min_x:
                                min_x = x
                            if x > max_x:
                                max_x = x
            if max_x < 0:
                x0, y0, sw, sh = 0, 0, 1, 1
                sub = bytes([pixels[0]])
            else:
                x0, y0 = min_x, min_y
                sw, sh = max_x - min_x + 1, max_y - min_y + 1
                cropped = bytearray(sw * sh)
                for ry in range(sh):
                    src_off = (y0 + ry) * width + x0
                    cropped[ry * sw : (ry + 1) * sw] = pixels[src_off : src_off + sw]
                sub = bytes(cropped)
        out.extend(struct.pack("<BBBBHB", 0x21, 0xF9, 4, 0x04, d, 0))
        out.append(0x00)
        out.extend(struct.pack("<BHHHHB", 0x2C, x0, y0, sw, sh, 0))
        out.append(4)
        compressed = _lzw_encode_gif(sub, min_code_size=4)
        for j in range(0, len(compressed), 255):
            chunk = compressed[j : j + 255]
            out.append(len(chunk))
            out.extend(chunk)
        out.append(0x00)
        prev = pixels
    out.append(0x3B)
    return bytes(out)


def _png_chunk(tag: bytes, payload: bytes) -> bytes:
    crc = zlib.crc32(tag + payload) & 0xFFFFFFFF
    return struct.pack(">I", len(payload)) + tag + payload + struct.pack(">I", crc)


def _encode_indexed_png(pixels: bytes, width: int, height: int) -> bytes:
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 3, 0, 0, 0)
    plte = b"".join(struct.pack("BBB", *rgb) for rgb in PALETTE_RGB)
    rows = bytearray()
    for y in range(height):
        rows.append(0)
        row = y * width
        rows.extend(pixels[row : row + width])
    idat = zlib.compress(bytes(rows), level=9)
    return b"\x89PNG\r\n\x1a\n" + _png_chunk(b"IHDR", ihdr) + _png_chunk(b"PLTE", plte) + _png_chunk(b"IDAT", idat) + _png_chunk(b"IEND", b"")


def render_hero(metrics: dict[str, object]) -> tuple[bytes, bytes]:
    w, h = 960, 440
    tiles = [
        ("PRINCIPLES", int(metrics["principles"]), 6),
        ("HOSTS", int(metrics["hosts"]), 7),
        ("SKILL", int(metrics["skills"]), 8),
        ("REAL-APP CHECKS", int(metrics["checks"]), 9),
        ("PACKAGING TESTS", int(metrics["tests"]), 10),
        ("CI PLATFORMS", int(metrics["ci_oses"]), 11),
    ]
    base = bytearray(w * h)
    # Subtle dot grid
    for gy in range(20, h, 24):
        for gx in range(20, w, 24):
            base[gy * w + gx] = 2
    _stroke_rect(base, w, h, 0, 0, w, h, 3, 2)

    # Header title + rainbow bar + subtitle
    _draw_text(base, w, h, 42, 30, "WEBAPP6", scale=6, c=5, gap=1)
    # Multi-segment neon accent rule under title
    bar_colors = (6, 11, 10, 7, 9, 8)
    for idx, col in enumerate(bar_colors):
        _fill_rect(base, w, h, 42 + idx * 42, 82, 42 + (idx + 1) * 42, 87, col)
    _draw_text(base, w, h, 42, 100, "SIX WEB-APP PRINCIPLES · AGY · CLAUDE CODE · CODEX", scale=2, c=12, gap=1)
    _draw_text(base, w, h, 770, 44, f"V{metrics['version']}", scale=3, c=6, gap=1)

    # Footer caption
    _draw_text(
        base, w, h, 42, 412,
        f"COUNTS AT V{metrics['version']} · CUBIC EASE-OUT OVER 1.2S · PLAYS ONCE",
        scale=2, c=4, gap=1,
    )

    # 50 ms per frame: 24 frames = 1.20 s ease-out, 2-frame (100 ms) stagger across 6 tiles = 1.70 s total
    total_frames = 35
    frames: list[bytes] = []
    for f in range(total_frames):
        buf = bytearray(base)
        for idx, (label, target, accent) in enumerate(tiles):
            col_i = idx % 3
            row_i = idx // 3
            tx = 42 + col_i * 298
            ty = 136 + row_i * 132
            tw, th = 280, 114
            local = max(0.0, min(1.0, (f - idx * 2) / 24.0))
            if f == total_frames - 1:
                local = 1.0
            eased = 1.0 - (1.0 - local) ** 3
            val = target if f == total_frames - 1 else round(target * eased)

            _fill_rect(buf, w, h, tx, ty, tx + tw, ty + th, 1)
            _stroke_rect(buf, w, h, tx, ty, tx + tw, ty + th, 3, 2)
            _fill_rect(buf, w, h, tx, ty, tx + 6, ty + th, accent)
            _draw_text(buf, w, h, tx + 22, ty + 18, label, scale=2, c=4, gap=1)
            _draw_text(buf, w, h, tx + 22, ty + 46, str(val), scale=6, c=5, gap=1)
            # Bottom progress rail
            rail_x0, rail_x1 = tx + 22, tx + tw - 20
            rail_y0, rail_y1 = ty + th - 14, ty + th - 9
            _fill_rect(buf, w, h, rail_x0, rail_y0, rail_x1, rail_y1, 2)
            fill_w = int((rail_x1 - rail_x0) * eased)
            if fill_w > 0:
                _fill_rect(buf, w, h, rail_x0, rail_y0, rail_x0 + fill_w, rail_y1, accent)
        frames.append(bytes(buf))

    gif_bytes = _encode_play_once_gif(frames, w, h, delay_cs=5)
    png_bytes = _encode_indexed_png(frames[-1], w, h)
    return gif_bytes, png_bytes


def render_rule6_sequence_svg(version: str) -> bytes:
    ver = escape(f"webapp6 v{version}")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="480" viewBox="0 0 960 480" role="img" aria-labelledby="title desc">
  <title id="title">Rule 6 sequence diagram: already-open tab meets a new deployment</title>
  <desc id="desc">An open tab running build A checks a fresh same-origin version endpoint after build B deploys. Clean navigation automatically loads the target URL as a full document; dirty edits or saves in flight are protected; network failures keep build A usable.</desc>
  <defs>
    <marker id="arr-cyan" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#00F5D4"/>
    </marker>
    <marker id="arr-slate" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#CBD5E1"/>
    </marker>
    <marker id="arr-amber" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#FF9E00"/>
    </marker>
  </defs>
  <rect width="960" height="480" rx="12" fill="#0B0F1A" stroke="#2A3550" stroke-width="2"/>
  <text x="32" y="40" fill="#F8FAFC" font-family="Segoe UI, Verdana, sans-serif" font-size="20" font-weight="700">Rule 6: Already-Open Tab Meets a New Deployment</text>
  <rect x="32" y="48" width="240" height="3" fill="#00F5D4"/>
  <text x="928" y="40" text-anchor="end" fill="#64748B" font-family="Consolas, monospace" font-size="12">{ver}</text>

  <!-- Lifelines -->
  <g font-family="Segoe UI, Verdana, sans-serif" font-size="13" font-weight="700" text-anchor="middle">
    <rect x="70" y="70" width="140" height="34" rx="6" fill="#1E1650" stroke="#7B61FF" stroke-width="2"/>
    <text x="140" y="92" fill="#EDE9FE">User</text>
    <rect x="370" y="70" width="220" height="34" rx="6" fill="#062F33" stroke="#00F5D4" stroke-width="2"/>
    <text x="480" y="92" fill="#CCFBF1">Open Tab (loadedBuild = A)</text>
    <rect x="750" y="70" width="140" height="34" rx="6" fill="#1E293B" stroke="#94A3B8" stroke-width="2"/>
    <text x="820" y="92" fill="#F8FAFC">Origin Server</text>
  </g>
  <g stroke="#334155" stroke-width="1.5" stroke-dasharray="5 5">
    <line x1="140" y1="104" x2="140" y2="452"/>
    <line x1="480" y1="104" x2="480" y2="452"/>
    <line x1="820" y1="104" x2="820" y2="452"/>
  </g>

  <!-- Step 1: Initial load -->
  <line x1="820" y1="132" x2="488" y2="132" stroke="#CBD5E1" stroke-width="1.8" marker-end="url(#arr-slate)"/>
  <text x="654" y="125" text-anchor="middle" fill="#E2E8F0" font-family="Segoe UI, Verdana, sans-serif" font-size="12">Build A HTML (embedded build ID = A; never from startup fetch)</text>

  <!-- Deploy banner -->
  <line x1="60" y1="164" x2="900" y2="164" stroke="#475569" stroke-width="1.5"/>
  <rect x="240" y="150" width="480" height="26" rx="13" fill="#1E293B" stroke="#7B61FF" stroke-width="1.5"/>
  <text x="480" y="167" text-anchor="middle" fill="#F8FAFC" font-family="Segoe UI, Verdana, sans-serif" font-size="12" font-weight="700">Build B deployed (any serverBuild != A counts, including rollback)</text>

  <!-- Trigger & check -->
  <line x1="140" y1="204" x2="472" y2="204" stroke="#CBD5E1" stroke-width="1.8" marker-end="url(#arr-slate)"/>
  <text x="308" y="197" text-anchor="middle" fill="#E2E8F0" font-family="Segoe UI, Verdana, sans-serif" font-size="12">Navigation, tab return, or BFCache restore</text>
  <line x1="480" y1="204" x2="812" y2="204" stroke="#CBD5E1" stroke-width="1.8" marker-end="url(#arr-slate)"/>
  <text x="650" y="197" text-anchor="middle" fill="#E2E8F0" font-family="Segoe UI, Verdana, sans-serif" font-size="12">Fresh same-origin version request (no-store)</text>

  <!-- Branch 1: Clean -->
  <rect x="52" y="226" width="856" height="92" rx="8" fill="#071E24" stroke="#00F5D4" stroke-width="1.5"/>
  <rect x="52" y="226" width="304" height="22" rx="4" fill="#00F5D4"/>
  <text x="64" y="241" fill="#0B0F1A" font-family="Segoe UI, Verdana, sans-serif" font-size="11" font-weight="700">ALT 1 · IDs differ &amp; next navigation is clean</text>
  <text x="295" y="272" text-anchor="middle" fill="#99F6E4" font-family="Segoe UI, Verdana, sans-serif" font-size="11.5">Recheck !dirty &amp;&amp; !saving right before leaving</text>
  <line x1="480" y1="274" x2="812" y2="274" stroke="#00F5D4" stroke-width="2" marker-end="url(#arr-cyan)"/>
  <text x="650" y="267" text-anchor="middle" fill="#00F5D4" font-family="Segoe UI, Verdana, sans-serif" font-size="12" font-weight="700">Full-document load of target URL (no accept prompt)</text>
  <line x1="820" y1="302" x2="488" y2="302" stroke="#00F5D4" stroke-width="2" stroke-dasharray="5 3" marker-end="url(#arr-cyan)"/>
  <text x="654" y="296" text-anchor="middle" fill="#CCFBF1" font-family="Segoe UI, Verdana, sans-serif" font-size="12">Build B HTML + matching hashed assets run</text>

  <!-- Branch 2: Dirty or saving -->
  <rect x="52" y="330" width="856" height="58" rx="8" fill="#2A1708" stroke="#FF9E00" stroke-width="1.5"/>
  <rect x="52" y="330" width="304" height="22" rx="4" fill="#FF9E00"/>
  <text x="64" y="345" fill="#0B0F1A" font-family="Segoe UI, Verdana, sans-serif" font-size="11" font-weight="700">ALT 2 · Dirty input or save in flight</text>
  <line x1="480" y1="372" x2="148" y2="372" stroke="#FF9E00" stroke-width="2" marker-end="url(#arr-amber)"/>
  <text x="314" y="366" text-anchor="middle" fill="#FEF3C7" font-family="Segoe UI, Verdana, sans-serif" font-size="12" font-weight="700">Notify &amp; protect draft until saved, cancelled, or discarded</text>
  <text x="654" y="372" text-anchor="middle" fill="#FDBA74" font-family="Segoe UI, Verdana, sans-serif" font-size="12">Never force a background reload</text>

  <!-- Branch 3: Failure -->
  <rect x="52" y="400" width="856" height="50" rx="8" fill="#151C2C" stroke="#475569" stroke-width="1.5"/>
  <rect x="52" y="400" width="304" height="22" rx="4" fill="#475569"/>
  <text x="64" y="415" fill="#F8FAFC" font-family="Segoe UI, Verdana, sans-serif" font-size="11" font-weight="700">ALT 3 · Version request fails / times out</text>
  <text x="480" y="438" text-anchor="middle" fill="#CBD5E1" font-family="Segoe UI, Verdana, sans-serif" font-size="12">Keep Build A and drafts usable; retry on a later trigger (no reload loop)</text>
</svg>
'''
    return svg.encode("utf-8")


def render_motion_curve_svg(metrics: dict[str, object]) -> bytes:
    ver = escape(f"webapp6 v{metrics['version']}")
    # Sample cubic ease-out polyline for left chart (x: 74..434, y: 294..94)
    x0, x1, y0, y1 = 74.0, 434.0, 294.0, 94.0
    pts = []
    for i in range(25):
        u = i / 24.0
        eased = 1.0 - (1.0 - u) ** 3
        px = x0 + (x1 - x0) * u
        py = y0 - (y0 - y1) * eased
        pts.append(f"{px:.1f},{py:.1f}")
    curve_points = " ".join(pts)

    # Right panel stagger bars (6 tiles, 0..500 ms start, 1200 ms ease-out duration, total 1700 ms)
    bar_specs = [
        (f"principles ({metrics['principles']})", 0, "#00F5D4"),
        (f"hosts ({metrics['hosts']})", 100, "#FF2E93"),
        (f"skill ({metrics['skills']})", 200, "#C8FF00"),
        (f"checks ({metrics['checks']})", 300, "#FF9E00"),
        (f"tests ({metrics['tests']})", 400, "#7B61FF"),
        (f"CI OS ({metrics['ci_oses']})", 500, "#38BDF8"),
    ]
    bars_svg = []
    bx0, bw = 602.0, 316.0
    for i, (label, start_ms, col) in enumerate(bar_specs):
        by = 104 + i * 33
        sx = bx0 + bw * (start_ms / 1800.0)
        sw = bw * (1200.0 / 1800.0)
        ink = _ink_color(col)
        bars_svg.append(
            f'    <text x="592" y="{by + 14}" text-anchor="end" fill="#CBD5E1" font-family="Segoe UI, Verdana, sans-serif" font-size="11.5">{escape(label)}</text>\n'
            f'    <rect x="{bx0:.0f}" y="{by}" width="{bw:.0f}" height="20" rx="4" fill="#131929" stroke="#26314A"/>\n'
            f'    <rect x="{sx:.1f}" y="{by + 2}" width="{sw:.1f}" height="16" rx="3" fill="{col}" fill-opacity="0.88"/>\n'
            f'    <text x="{sx + sw - 6:.1f}" y="{by + 14}" text-anchor="end" fill="{ink}" font-family="Consolas, monospace" font-size="10.5" font-weight="700">{start_ms}..{start_ms + 1200}ms</text>'
        )
    bars_block = "\n".join(bars_svg)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="360" viewBox="0 0 960 360" role="img" aria-labelledby="title desc">
  <title id="title">Optional motion rule: cubic ease-out curve and staggered play-once timeline</title>
  <desc id="desc">Left panel plots cubic ease-out v(t) = V(1 - (1 - t/T)^3) over T = 1.2 s compared with a dashed linear reference, landing on 100 percent at t = T. Right panel shows six KPI tiles staggered 100 ms apart, each counting up over 1.2 s once.</desc>
  <rect width="960" height="360" rx="12" fill="#0B0F1A" stroke="#2A3550" stroke-width="2"/>
  <text x="32" y="38" fill="#F8FAFC" font-family="Segoe UI, Verdana, sans-serif" font-size="19" font-weight="700">Illustrative Motion Timing: Cubic Ease-Out &amp; Play-Once Stagger</text>
  <rect x="32" y="46" width="260" height="3" fill="#FF2E93"/>
  <text x="928" y="38" text-anchor="end" fill="#64748B" font-family="Consolas, monospace" font-size="12">{ver}</text>

  <!-- Left panel: Ease-out curve -->
  <rect x="28" y="66" width="436" height="270" rx="8" fill="#111726" stroke="#26314A"/>
  <text x="48" y="88" fill="#E2E8F0" font-family="Segoe UI, Verdana, sans-serif" font-size="13" font-weight="700">Cubic ease-out (T = 1.2 s) vs linear</text>
  <g stroke="#26314A" stroke-width="1">
    <line x1="74" y1="94" x2="434" y2="94"/>
    <line x1="74" y1="144" x2="434" y2="144"/>
    <line x1="74" y1="194" x2="434" y2="194"/>
    <line x1="74" y1="244" x2="434" y2="244"/>
    <line x1="74" y1="294" x2="434" y2="294" stroke="#64748B"/>
    <line x1="74" y1="94" x2="74" y2="294" stroke="#64748B"/>
  </g>
  <line x1="74" y1="294" x2="434" y2="94" stroke="#64748B" stroke-width="1.5" stroke-dasharray="6 4"/>
  <polyline fill="none" stroke="#00F5D4" stroke-width="3" points="{curve_points}"/>
  <circle cx="434" cy="94" r="5" fill="#C8FF00"/>
  <g fill="#94A3B8" font-family="Consolas, monospace" font-size="11">
    <text x="66" y="98" text-anchor="end">100%</text>
    <text x="66" y="198" text-anchor="end">50%</text>
    <text x="66" y="298" text-anchor="end">0%</text>
    <text x="74" y="314" text-anchor="middle">0.0s</text>
    <text x="254" y="314" text-anchor="middle">0.6s</text>
    <text x="434" y="314" text-anchor="middle">1.2s</text>
    <text x="348" y="114" fill="#C8FF00" font-weight="700">v(T) = V</text>
    <text x="280" y="220" fill="#94A3B8">linear ref</text>
  </g>

  <!-- Right panel: Stagger timeline -->
  <rect x="484" y="66" width="448" height="270" rx="8" fill="#111726" stroke="#26314A"/>
  <text x="504" y="88" fill="#E2E8F0" font-family="Segoe UI, Verdana, sans-serif" font-size="13" font-weight="700">Header tiles: 100 ms stagger, plays once</text>
  <g>
{bars_block}
  </g>
  <g fill="#94A3B8" font-family="Consolas, monospace" font-size="11">
    <text x="602" y="320" text-anchor="middle">0s</text>
    <text x="707" y="320" text-anchor="middle">0.6s</text>
    <text x="813" y="320" text-anchor="middle">1.2s</text>
    <text x="918" y="320" text-anchor="middle">1.8s</text>
  </g>
</svg>
'''
    return svg.encode("utf-8")


def build_all_assets() -> dict[Path, bytes]:
    m = collect_repo_metrics()
    ver = str(m["version"])
    kb = round(int(m["plugin_bytes"]) / 1024)
    hero_gif, hero_png = render_hero(m)
    return {
        ART / "badges" / "release.svg": badge_svg("RELEASE", f"v{ver}", "#00F5D4"),
        ART / "badges" / "license.svg": badge_svg("LICENSE", "MIT", "#C8FF00"),
        ART / "badges" / "hosts.svg": badge_svg("HOSTS", "agy · Claude · Codex", "#38BDF8"),
        ART / "badges" / "principles.svg": badge_svg("PRINCIPLES", "6 + motion", "#FF2E93"),
        ART / "badges" / "checks.svg": badge_svg("REAL-APP CHECKS", str(m["checks"]), "#FF9E00"),
        ART / "badges" / "tests.svg": badge_svg("TESTS", str(m["tests"]), "#7B61FF"),
        ART / "badges" / "payload.svg": badge_svg("PLUGIN", f"{m['plugin_files']} files · {kb} KiB", "#00F5D4"),
        ART / "hero.gif": hero_gif,
        ART / "hero.png": hero_png,
        ART / "rule6-sequence.svg": render_rule6_sequence_svg(ver),
        ART / "motion-curve.svg": render_motion_curve_svg(m),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify docs/art matches generated output exactly.")
    args = parser.parse_args(argv)

    expected = build_all_assets()
    if args.check:
        actual_files = {p for p in ART.rglob("*") if p.is_file()} if ART.exists() else set()
        expected_files = set(expected)
        drift: list[str] = []
        for extra in sorted(actual_files - expected_files):
            drift.append(f"extra: {extra.relative_to(ROOT).as_posix()}")
        for path in sorted(expected_files):
            if not path.exists():
                drift.append(f"missing: {path.relative_to(ROOT).as_posix()}")
            elif path.read_bytes() != expected[path]:
                drift.append(f"changed: {path.relative_to(ROOT).as_posix()}")
        if drift:
            print("docs/art drift detected:\n  " + "\n  ".join(drift), file=sys.stderr)
            return 1
        print(f"OK: {len(expected)} generated assets in docs/art/ match byte-for-byte.")
        return 0

    for path, content in sorted(expected.items()):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    # Remove any stale files under docs/art not in expected
    for existing in sorted(ART.rglob("*")):
        if existing.is_file() and existing not in expected:
            existing.unlink()
    for folder in sorted(ART.rglob("*"), reverse=True):
        if folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()
    total = sum(len(b) for b in expected.values())
    print(f"Generated {len(expected)} assets ({total:,} bytes) under docs/art/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
