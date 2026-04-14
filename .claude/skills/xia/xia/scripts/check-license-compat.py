#!/usr/bin/env python3
"""
check-license-compat.py — Verify license compatibility between source and target.

Usage:
    python check-license-compat.py --source-license MIT --target-license Apache-2.0
    python check-license-compat.py --verify-manifest .xia-manifest.json

Exit codes:
    0 — MATCH (OK to proceed)
    1 — WARN (surface in Challenge phase)
    2 — BLOCK (default refuse, user can override)
    3 — ERROR (unknown license or parse failure)
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Canonical license identifiers (SPDX subset most common)
CANONICAL = {
    'mit': 'MIT',
    'apache-2.0': 'Apache-2.0',
    'apache 2.0': 'Apache-2.0',
    'bsd-3-clause': 'BSD-3',
    'bsd-3': 'BSD-3',
    'bsd-2-clause': 'BSD-2',
    'lgpl-3.0': 'LGPL-3',
    'lgpl-3': 'LGPL-3',
    'gpl-3.0': 'GPL-3',
    'gpl-3': 'GPL-3',
    'gpl-2.0': 'GPL-2',
    'agpl-3.0': 'AGPL-3',
    'agpl-3': 'AGPL-3',
    'unlicense': 'Unlicense',
    'cc0-1.0': 'CC0',
    'cc0': 'CC0',
    'cc-by-4.0': 'CC-BY-4.0',
    'cc-by-sa-4.0': 'CC-BY-SA-4.0',
    'proprietary': 'Proprietary',
    'none': 'None',
    '': 'Unknown',
}

# Compatibility matrix: MATRIX[source][target] = verdict
MATRIX = {
    'MIT':          {'MIT': 'MATCH', 'Apache-2.0': 'MATCH', 'BSD-3': 'MATCH', 'BSD-2': 'MATCH', 'LGPL-3': 'MATCH', 'GPL-3': 'MATCH', 'AGPL-3': 'MATCH', 'Proprietary': 'MATCH'},
    'Apache-2.0':   {'MIT': 'MATCH', 'Apache-2.0': 'MATCH', 'BSD-3': 'MATCH', 'BSD-2': 'MATCH', 'LGPL-3': 'MATCH', 'GPL-3': 'MATCH', 'AGPL-3': 'MATCH', 'Proprietary': 'MATCH'},
    'BSD-3':        {'MIT': 'MATCH', 'Apache-2.0': 'MATCH', 'BSD-3': 'MATCH', 'BSD-2': 'MATCH', 'LGPL-3': 'MATCH', 'GPL-3': 'MATCH', 'AGPL-3': 'MATCH', 'Proprietary': 'MATCH'},
    'BSD-2':        {'MIT': 'MATCH', 'Apache-2.0': 'MATCH', 'BSD-3': 'MATCH', 'BSD-2': 'MATCH', 'LGPL-3': 'MATCH', 'GPL-3': 'MATCH', 'AGPL-3': 'MATCH', 'Proprietary': 'MATCH'},
    'LGPL-3':       {'MIT': 'WARN',  'Apache-2.0': 'WARN',  'BSD-3': 'WARN',  'BSD-2': 'WARN',  'LGPL-3': 'MATCH', 'GPL-3': 'MATCH', 'AGPL-3': 'MATCH', 'Proprietary': 'WARN'},
    'GPL-3':        {'MIT': 'WARN',  'Apache-2.0': 'WARN',  'BSD-3': 'WARN',  'BSD-2': 'WARN',  'LGPL-3': 'WARN',  'GPL-3': 'MATCH', 'AGPL-3': 'MATCH', 'Proprietary': 'BLOCK'},
    'AGPL-3':       {'MIT': 'WARN',  'Apache-2.0': 'WARN',  'BSD-3': 'WARN',  'BSD-2': 'WARN',  'LGPL-3': 'WARN',  'GPL-3': 'WARN',  'AGPL-3': 'MATCH', 'Proprietary': 'BLOCK'},
    'Unlicense':    {'MIT': 'MATCH', 'Apache-2.0': 'MATCH', 'BSD-3': 'MATCH', 'BSD-2': 'MATCH', 'LGPL-3': 'MATCH', 'GPL-3': 'MATCH', 'AGPL-3': 'MATCH', 'Proprietary': 'MATCH'},
    'CC0':          {'MIT': 'MATCH', 'Apache-2.0': 'MATCH', 'BSD-3': 'MATCH', 'BSD-2': 'MATCH', 'LGPL-3': 'MATCH', 'GPL-3': 'MATCH', 'AGPL-3': 'MATCH', 'Proprietary': 'MATCH'},
    'CC-BY-4.0':    {'MIT': 'WARN',  'Apache-2.0': 'WARN',  'BSD-3': 'WARN',  'BSD-2': 'WARN',  'LGPL-3': 'WARN',  'GPL-3': 'WARN',  'AGPL-3': 'WARN',  'Proprietary': 'WARN'},
    'CC-BY-SA-4.0': {'MIT': 'WARN',  'Apache-2.0': 'WARN',  'BSD-3': 'WARN',  'BSD-2': 'WARN',  'LGPL-3': 'WARN',  'GPL-3': 'WARN',  'AGPL-3': 'WARN',  'Proprietary': 'BLOCK'},
    'Proprietary':  {'MIT': 'BLOCK', 'Apache-2.0': 'BLOCK','BSD-3': 'BLOCK', 'BSD-2': 'BLOCK', 'LGPL-3': 'BLOCK', 'GPL-3': 'BLOCK', 'AGPL-3': 'BLOCK', 'Proprietary': 'WARN'},
    'Unknown':      {},   # always BLOCK (fallback)
    'None':         {},
}

VERDICT_EXIT = {'MATCH': 0, 'WARN': 1, 'BLOCK': 2, 'ERROR': 3}


def canonicalize(license_str: str) -> str:
    """Normalize license string to canonical identifier."""
    if not license_str:
        return 'Unknown'
    key = license_str.strip().lower()
    if key in CANONICAL:
        return CANONICAL[key]
    # Try fuzzy match
    for k, v in CANONICAL.items():
        if k in key or key in k:
            return v
    return 'Unknown'


def check_pair(source: str, target: str) -> tuple[str, str]:
    """Return (verdict, explanation)."""
    s = canonicalize(source)
    t = canonicalize(target)
    if s == 'Unknown' or t == 'Unknown':
        return 'BLOCK', f'Unknown license ({source} or {target}) — require manual review'
    verdict = MATRIX.get(s, {}).get(t, 'BLOCK')
    exp = {
        'MATCH': f'{s} -> {t}: compatible, proceed with attribution.',
        'WARN':  f'{s} -> {t}: compatible with conditions (attribution, notice, maybe source disclosure).',
        'BLOCK': f'{s} -> {t}: copyleft viral or terms incompatible. Default refuse.',
    }[verdict]
    return verdict, exp


def verify_manifest(path: Path) -> int:
    """Verify every port entry in manifest has valid license + attribution."""
    data = json.loads(path.read_text())
    errors = []
    for port in data.get('ports', []):
        pid = port.get('id')
        src_license = port.get('source', {}).get('license')
        verdict = port.get('source', {}).get('license_verdict')
        attribution = port.get('attribution', {}).get('header_added')
        if not src_license:
            errors.append(f'{pid}: missing source.license')
        if not verdict:
            errors.append(f'{pid}: missing license_verdict')
        if verdict in ('WARN', 'BLOCK_OVERRIDDEN') and not attribution:
            errors.append(f'{pid}: {verdict} requires attribution header (missing)')
    if errors:
        print('Manifest verification FAILED:')
        for e in errors:
            print(f'  - {e}')
        return 1
    print(f'Manifest verified: {len(data.get("ports", []))} ports OK.')
    return 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source-license', help='Source repo license')
    p.add_argument('--target-license', help='Local project license')
    p.add_argument('--verify-manifest', type=Path, help='Path to .xia-manifest.json')
    p.add_argument('--json', action='store_true', help='Output JSON')
    args = p.parse_args()

    if args.verify_manifest:
        sys.exit(verify_manifest(args.verify_manifest))

    if not args.source_license or not args.target_license:
        p.error('--source-license and --target-license required (or use --verify-manifest)')

    verdict, exp = check_pair(args.source_license, args.target_license)
    if args.json:
        print(json.dumps({'source': args.source_license, 'target': args.target_license,
                          'verdict': verdict, 'explanation': exp}))
    else:
        icon = {'MATCH': '[OK]', 'WARN': '[WARN]', 'BLOCK': '[BLOCK]', 'ERROR': '[ERR]'}[verdict]
        print(f'{icon} {args.source_license} -> {args.target_license}: {verdict}')
        print(f'       {exp}')
    sys.exit(VERDICT_EXIT[verdict])


if __name__ == '__main__':
    main()
