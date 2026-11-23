"""Reorganize repo so the library becomes a proper 'roya' package.

Moves core/, components/, templatetags/, theme/, foundation/,
behaviors/, controllers/, effects/, static/, templates/ into roya/.
Creates roya/__init__.py. Idempotent and safe to re-run.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PKG = ROOT / 'roya'

PACKAGE_DIRS = [
    'core',
    'components',
    'templatetags',
    'theme',
    'foundation',
    'behaviors',
    'controllers',
    'effects',
    'static',
    'templates',
]

# Directories that must NOT be moved (demo project, tooling, etc.)
PROTECTED = {'royaproject', 'royaapp', 'roya', '.git', 'venv', '.venv', 'env', 'node_modules'}


def main():
    if PKG.exists() and any(p.name not in {'__pycache__'} for p in PKG.iterdir()):
        print(f'[skip] {PKG} already exists with content; refusing to overwrite.')
        return 0

    PKG.mkdir(exist_ok=True)

    moved, skipped, missing = [], [], []
    for name in PACKAGE_DIRS:
        if name in PROTECTED:
            skipped.append((name, 'protected'))
            continue
        src = ROOT / name
        if not src.exists():
            missing.append(name)
            continue
        dst = PKG / name
        if dst.exists():
            print(f'[warn] {dst} already exists; skipping {name}')
            skipped.append((name, 'destination exists'))
            continue
        try:
            shutil.move(str(src), str(dst))
            moved.append(name)
            print(f'[move] {src} -> {dst}')
        except Exception as exc:
            print(f'[error] failed to move {name}: {exc}')
            return 1

    init_py = PKG / '__init__.py'
    if not init_py.exists():
        init_py.write_text(
            '"""Roya — Material Design 3 component library for Django."""\n'
            '__version__ = "0.2.0"\n',
            encoding='utf-8',
        )
        print(f'[create] {init_py}')

    print()
    print('Summary')
    print('-------')
    print('moved   :', moved or '(none)')
    print('skipped :', skipped or '(none)')
    print('missing :', missing or '(none)')
    print('package :', PKG)
    return 0


if __name__ == '__main__':
    sys.exit(main())
