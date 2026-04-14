#!/usr/bin/env python3
"""
fingerprint-manifest.py — Manage `.xia-manifest.json` for idempotency + audit.

Usage:
    # Add new port entry
    python fingerprint-manifest.py --action add --entry entry.json

    # Check if a port already exists (for idempotency)
    python fingerprint-manifest.py --action check \
        --source-repo https://github.com/... --feature rate-limiter

    # Mark port as rolled back
    python fingerprint-manifest.py --action rollback --id port_001 --reason "text"

    # Verify manifest syntax + required fields
    python fingerprint-manifest.py --action verify

    # Generate audit / license report
    python fingerprint-manifest.py --action audit

Exit codes:
    0 — success / match / clean
    1 — partial match / warnings
    2 — no match / errors
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_MANIFEST = Path('.xia-manifest.json')
SCHEMA_VERSION = '1.0'


def empty_manifest(project_name: str = '') -> dict:
    return {
        '$schema': 'https://example.com/xia-manifest-v1.json',
        'version': SCHEMA_VERSION,
        'project': {'name': project_name, 'license': ''},
        'ports': [],
        'stats': {'total_ports': 0, 'active_ports': 0, 'rolled_back': 0,
                  'last_updated': datetime.now(timezone.utc).isoformat()},
    }


def load_manifest(path: Path) -> dict:
    if not path.exists():
        return empty_manifest()
    return json.loads(path.read_text(encoding='utf-8'))


def save_manifest(path: Path, data: dict) -> None:
    data['stats'] = compute_stats(data)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')


def compute_stats(data: dict) -> dict:
    ports = data.get('ports', [])
    active = sum(1 for p in ports if p.get('status') == 'active')
    rolled = sum(1 for p in ports if p.get('status') == 'rolled_back')
    return {
        'total_ports': len(ports),
        'active_ports': active,
        'rolled_back': rolled,
        'last_updated': datetime.now(timezone.utc).isoformat(),
    }


def fingerprint(entry: dict) -> str:
    """Compute fingerprint hash for idempotency."""
    source = entry.get('source', {})
    key = f"{source.get('repo')}|{source.get('commit')}|{source.get('original_path')}|{entry.get('port', {}).get('mode')}"
    files = sorted(entry.get('impact', {}).get('files_created', []))
    key += '|' + '|'.join(files)
    return hashlib.sha256(key.encode()).hexdigest()[:16]


def action_add(args) -> int:
    manifest = load_manifest(args.manifest)
    entry = json.loads(Path(args.entry).read_text(encoding='utf-8'))
    fp = fingerprint(entry)
    for existing in manifest['ports']:
        if fingerprint(existing) == fp:
            print(f'DUPLICATE fingerprint {fp} — port already exists (id={existing.get("id")})')
            return 1
    next_id = f'port_{len(manifest["ports"]) + 1:03d}'
    entry.setdefault('id', next_id)
    entry.setdefault('status', 'active')
    manifest['ports'].append(entry)
    save_manifest(args.manifest, manifest)
    print(f'Added: {entry["id"]} (fingerprint: {fp})')
    return 0


def action_check(args) -> int:
    manifest = load_manifest(args.manifest)
    matches = []
    for port in manifest['ports']:
        src_repo = port.get('source', {}).get('repo', '')
        feat = port.get('feature_name', '')
        if args.source_repo in src_repo or src_repo in args.source_repo:
            if args.feature and args.feature.lower() in feat.lower():
                matches.append(('exact', port))
            else:
                matches.append(('partial', port))
    if not matches:
        print('no_match')
        return 2
    for kind, port in matches:
        print(f'{kind} | {port["id"]} | {port.get("feature_name")} | {port.get("status")}')
    return 0 if any(k == 'exact' for k, _ in matches) else 1


def action_rollback(args) -> int:
    manifest = load_manifest(args.manifest)
    for port in manifest['ports']:
        if port['id'] == args.id:
            port['status'] = 'rolled_back'
            port['rollback_reason'] = args.reason
            port['rollback_date'] = datetime.now(timezone.utc).isoformat()
            save_manifest(args.manifest, manifest)
            print(f'Rolled back: {args.id}')
            return 0
    print(f'Port not found: {args.id}')
    return 2


def action_verify(args) -> int:
    manifest = load_manifest(args.manifest)
    errors = []
    required = ['id', 'feature_name', 'source', 'port', 'impact', 'status']
    for port in manifest['ports']:
        for field in required:
            if field not in port:
                errors.append(f'{port.get("id", "?")}: missing {field}')
        if 'source' in port:
            for f in ('repo', 'commit', 'license'):
                if not port['source'].get(f):
                    errors.append(f'{port["id"]}: source.{f} missing')
    if errors:
        print(f'FAIL — {len(errors)} issue(s):')
        for e in errors:
            print(f'  - {e}')
        return 2
    print(f'OK — {len(manifest["ports"])} port(s) verified')
    return 0


def action_audit(args) -> int:
    manifest = load_manifest(args.manifest)
    ports = manifest['ports']
    if not ports:
        print('No ports tracked.')
        return 0
    print('=== xia Manifest Audit ===\n')
    print(f'Total: {len(ports)} (active: {sum(1 for p in ports if p.get("status") == "active")}, '
          f'rolled: {sum(1 for p in ports if p.get("status") == "rolled_back")})\n')
    licenses = {}
    for p in ports:
        lic = p.get('source', {}).get('license', 'Unknown')
        licenses[lic] = licenses.get(lic, 0) + 1
    print('Licenses present:')
    for lic, count in sorted(licenses.items()):
        print(f'  {lic}: {count}')
    print('\nActive ports:')
    for p in ports:
        if p.get('status') == 'active':
            d = p.get('port', {}).get('date', '?')
            r = p.get('source', {}).get('repo', '?').split('/')[-1]
            print(f'  [{p["id"]}] {p.get("feature_name")} from {r} ({d})')
    return 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--action', required=True, choices=['add', 'check', 'rollback', 'verify', 'audit'])
    p.add_argument('--manifest', type=Path, default=DEFAULT_MANIFEST)
    p.add_argument('--entry', help='Path to entry JSON for add')
    p.add_argument('--source-repo', help='For check action')
    p.add_argument('--feature', help='For check action')
    p.add_argument('--id', help='For rollback action')
    p.add_argument('--reason', help='For rollback action')
    args = p.parse_args()

    actions = {
        'add': action_add, 'check': action_check, 'rollback': action_rollback,
        'verify': action_verify, 'audit': action_audit,
    }
    sys.exit(actions[args.action](args))


if __name__ == '__main__':
    main()
