#!/usr/bin/env python3
# Roya project diagnostic extractor
# Place this file in the project root, then run init.bat.
from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT_JSON = ROOT / "roya_diagnostic.json"
OUTPUT_TXT = ROOT / "roya_diagnostic.txt"

TARGETS = [
    "pyproject.toml",
    "apps.py",
    "roya/apps.py",
    "roya/core/component.py",
    "roya/components/actions/button.py",
    "roya/static/roya/js/roya.js",
    "roya/templatetags/roya.py",
]

def read_text(path: Path) -> str:
    raw = path.read_bytes()
    for encoding in ("utf-8-sig", "utf-8", "cp1256", "latin-1"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            pass
    return raw.decode("utf-8", errors="replace")

def file_record(path: Path, relative: str) -> dict:
    raw = path.read_bytes()
    content = read_text(path)
    lines = content.splitlines()
    return {
        "path": relative.replace("\\", "/"),
        "exists": True,
        "size_bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "line_count": len(lines),
        "lines": [[i, line] for i, line in enumerate(lines, 1)],
    }

def main() -> int:
    records = {}
    missing = []
    root_resolved = ROOT.resolve()

    for rel in TARGETS:
        candidate = ROOT / Path(rel)
        if candidate.is_file():
            records[rel.replace("\\", "/")] = file_record(candidate, rel)
        else:
            missing.append(rel)

    # Fallback discovery for targets not found at their expected path.
    # This reports candidate paths without scanning file contents.
    fallback = {}
    wanted_names = {
        "component.py", "button.py", "roya.js", "roya.py", "apps.py"
    }
    for current, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in {
            ".git", ".venv", "venv", "__pycache__", "node_modules",
            "dist", "build", ".pytest_cache"
        }]
        for name in files:
            if name in wanted_names:
                p = Path(current) / name
                rel = p.relative_to(ROOT).as_posix()
                fallback.setdefault(name, []).append({
                    "path": rel,
                    "size_bytes": p.stat().st_size,
                })

    # Include a compact root directory listing to diagnose wrong project root.
    root_entries = []
    try:
        for item in sorted(ROOT.iterdir(), key=lambda p: p.name.lower()):
            root_entries.append({
                "name": item.name,
                "kind": "directory" if item.is_dir() else "file",
            })
    except OSError as exc:
        root_entries = [{"error": str(exc)}]

    result = {
        "diagnostic": "roya-project-reader-check",
        "generated_at": datetime.now().astimezone().isoformat(),
        "project_root": str(root_resolved),
        "python": sys.version,
        "platform": platform.platform(),
        "targets": records,
        "missing_expected_paths": missing,
        "fallback_candidates_by_filename": fallback,
        "root_entries": root_entries,
        "notes": [
            "Only the explicitly listed source/configuration files are extracted.",
            "Virtual environments, Git metadata, node_modules, build and cache folders are excluded.",
            "No environment variables, credentials, database files, or user data are collected.",
            "If a target is missing at its expected path, inspect fallback_candidates_by_filename.",
        ],
    }

    OUTPUT_JSON.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    lines = [
        "ROYA PROJECT DIAGNOSTIC",
        f"Project root: {root_resolved}",
        f"Python: {sys.version.split()[0]}",
        f"Generated: {result['generated_at']}",
        "",
        "EXPECTED TARGETS:",
    ]
    for rel in TARGETS:
        record = records.get(rel)
        if record:
            lines.append(
                f"[OK] {rel} | {record['size_bytes']} bytes | "
                f"{record['line_count']} lines | sha256={record['sha256']}"
            )
        else:
            lines.append(f"[MISSING] {rel}")
    lines += ["", "FALLBACK CANDIDATES:"]
    for name, candidates in sorted(fallback.items()):
        lines.append(f"- {name}:")
        for item in candidates[:30]:
            lines.append(f"    {item['path']} ({item['size_bytes']} bytes)")
    lines += ["", "ROOT ENTRIES:"]
    for item in root_entries:
        lines.append(f"- {item.get('kind', 'info')}: {item.get('name', item.get('error'))}")
    OUTPUT_TXT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("Roya diagnostic extraction completed.")
    print(f"Project root : {root_resolved}")
    print(f"JSON report  : {OUTPUT_JSON}")
    print(f"Text report  : {OUTPUT_TXT}")
    print(f"Extracted    : {len(records)} / {len(TARGETS)} expected files")
    print(f"Missing      : {len(missing)}")
    print("\nOpen roya_diagnostic.json and send it back for review.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
