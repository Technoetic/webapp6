#!/usr/bin/env python3
"""Build a deterministic UTC slim plugin ZIP and SHA256SUMS.txt using Python stdlib only."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "webapp6"
DEFAULT_EPOCH = 1795392000  # 2026-11-23T00:00:00Z


def _zip_datetime() -> tuple[int, int, int, int, int, int]:
    epoch = int(os.environ.get("SOURCE_DATE_EPOCH", str(DEFAULT_EPOCH)))
    t = dt.datetime.fromtimestamp(epoch, tz=dt.timezone.utc)
    return (t.year, t.month, t.day, t.hour, t.minute, t.second)


def build_zip(out_dir: Path) -> tuple[Path, Path, str]:
    manifest = json.loads((PLUGIN / "plugin.json").read_text(encoding="utf-8"))
    version = manifest["version"]
    out_dir.mkdir(parents=True, exist_ok=True)
    zip_name = f"webapp6-plugin-{version}.zip"
    zip_path = out_dir / zip_name
    sums_path = out_dir / "SHA256SUMS.txt"

    files = sorted(
        (p for p in PLUGIN.rglob("*") if p.is_file() and "__pycache__" not in p.parts),
        key=lambda p: p.relative_to(PLUGIN).as_posix(),
    )
    stamp = _zip_datetime()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for file_path in files:
            arcname = "webapp6/" + file_path.relative_to(PLUGIN).as_posix()
            info = zipfile.ZipInfo(filename=arcname, date_time=stamp)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3  # Unix
            info.external_attr = 0o100644 << 16
            zf.writestr(info, file_path.read_bytes())

    digest = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    sums_path.write_bytes(f"{digest}  {zip_name}\n".encode("utf-8"))
    return zip_path, sums_path, digest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="Output directory for ZIP and SHA256SUMS.txt")
    parser.add_argument("--check-temp", action="store_true", help="Build twice in temp dirs and verify determinism.")
    args = parser.parse_args(argv)

    if args.check_temp:
        with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
            z1, _, h1 = build_zip(Path(d1))
            z2, _, h2 = build_zip(Path(d2))
            if h1 != h2 or z1.read_bytes() != z2.read_bytes():
                print("ERROR: release ZIP build is not deterministic.", file=sys.stderr)
                return 1
            print(f"OK: deterministic slim ZIP ({z1.stat().st_size:,} B, sha256={h1[:16]}...).")
        return 0

    out_dir = args.out or (ROOT / "dist")
    zip_path, sums_path, digest = build_zip(out_dir)
    print(f"Built {zip_path.name} ({zip_path.stat().st_size:,} bytes) sha256={digest}")
    print(f"Wrote {sums_path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
