#!/usr/bin/env python3
"""
generate-attribution-header.py — Add attribution header to ported files.

Usage:
    python generate-attribution-header.py \
        --files "src/middleware/rateLimit.ts,src/lib/tokenBucket.ts" \
        --source "tj/node-ratelimiter@abc1234" \
        --license MIT \
        --mode improve \
        --original-path "lib/limiter.js"

Supports:
    - JS/TS/JSX/TSX  → /** ... */
    - Python         → """ ... """
    - Go/Rust/C/C++  → // ...
    - Ruby/Shell     → # ...
    - HTML/XML       → <!-- ... -->
"""

import argparse
import sys
from datetime import date
from pathlib import Path

COMMENT_STYLES = {
    # ext: (start, mid, end)
    '.ts':   ('/**', ' *', ' */'),
    '.tsx':  ('/**', ' *', ' */'),
    '.js':   ('/**', ' *', ' */'),
    '.jsx':  ('/**', ' *', ' */'),
    '.mjs':  ('/**', ' *', ' */'),
    '.c':    ('/*',  ' *', ' */'),
    '.cpp':  ('/*',  ' *', ' */'),
    '.cs':   ('/*',  ' *', ' */'),
    '.java': ('/*',  ' *', ' */'),
    '.kt':   ('/*',  ' *', ' */'),
    '.swift':('/*',  ' *', ' */'),
    '.go':   ('//',  '//', '//'),
    '.rs':   ('//',  '//', '//'),
    '.py':   ('"""', '',   '"""'),
    '.rb':   ('#',   '#',  '#'),
    '.sh':   ('#',   '#',  '#'),
    '.bash': ('#',   '#',  '#'),
    '.yaml': ('#',   '#',  '#'),
    '.yml':  ('#',   '#',  '#'),
    '.toml': ('#',   '#',  '#'),
    '.html': ('<!--','   ', '-->'),
    '.xml':  ('<!--','   ', '-->'),
    '.vue':  ('<!--','   ', '-->'),
    '.svelte':('<!--','   ', '-->'),
}


def build_lines(source: str, license_id: str, mode: str, original_path: str) -> list[str]:
    today = date.today().isoformat()
    lines = [
        f'Adapted from {source}',
        f'License: {license_id}',
    ]
    if original_path:
        lines.append(f'Original: {original_path}')
    lines.append(f'Ported: {today} by /xia (mode: {mode})')
    if license_id in ('GPL-3', 'GPL-2', 'AGPL-3', 'LGPL-3'):
        lines.append('')
        lines.append(f'NOTICE: This file is derived from third-party source under {license_id}.')
        lines.append('The derivative work MUST comply with license terms. See NOTICE file.')
    elif license_id in ('CC-BY-4.0', 'CC-BY-SA-4.0'):
        lines.append('')
        lines.append(f'Attribution per {license_id} license. See NOTICE file.')
    return lines


def format_header(ext: str, lines: list[str]) -> str:
    if ext not in COMMENT_STYLES:
        return '\n'.join(lines) + '\n'
    start, mid, end = COMMENT_STYLES[ext]
    if ext == '.py':
        return start + '\n' + '\n'.join(lines) + '\n' + end + '\n'
    out = [start]
    for line in lines:
        if mid.strip():
            out.append(f'{mid} {line}'.rstrip())
        else:
            out.append(line)
    out.append(end)
    return '\n'.join(out) + '\n'


def has_existing_header(content: str, marker: str = 'Ported:') -> bool:
    head = content[:1000]
    return marker in head


def add_header(path: Path, header: str, force: bool = False) -> str:
    content = path.read_text(encoding='utf-8')
    if not force and has_existing_header(content):
        return 'skip'
    new = header + '\n' + content
    path.write_text(new, encoding='utf-8')
    return 'added'


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--files', required=True, help='Comma-separated file paths')
    p.add_argument('--source', required=True, help='e.g. tj/node-ratelimiter@abc1234')
    p.add_argument('--license', required=True, dest='license_id')
    p.add_argument('--mode', required=True, choices=['compare', 'copy', 'improve', 'port'])
    p.add_argument('--original-path', default='', help='Original file path in source repo')
    p.add_argument('--force', action='store_true', help='Overwrite existing header')
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args()

    files = [Path(f.strip()) for f in args.files.split(',') if f.strip()]
    lines = build_lines(args.source, args.license_id, args.mode, args.original_path)

    added = skipped = missing = 0
    for path in files:
        if not path.exists():
            print(f'  [MISS] {path}')
            missing += 1
            continue
        ext = path.suffix.lower()
        header = format_header(ext, lines)
        if args.dry_run:
            print(f'--- {path} ({ext}) ---')
            print(header)
            continue
        result = add_header(path, header, force=args.force)
        if result == 'added':
            print(f'  [OK]   {path}')
            added += 1
        else:
            print(f'  [SKIP] {path} (existing header, use --force)')
            skipped += 1

    print(f'\nSummary: added={added} skipped={skipped} missing={missing}')
    sys.exit(0 if missing == 0 else 1)


if __name__ == '__main__':
    main()
