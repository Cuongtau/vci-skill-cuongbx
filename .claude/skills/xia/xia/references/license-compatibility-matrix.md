# License Compatibility Matrix

Source license → Target license (local project). Verdict: ✅ MATCH · ⚠️ WARN · ❌ BLOCK.

## Quick reference

| Source \ Target | MIT | Apache-2.0 | BSD-3 | LGPL-3 | GPL-3 | Proprietary |
|---|---|---|---|---|---|---|
| **MIT** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Apache-2.0** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **BSD-3** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **LGPL-3** | ⚠️ | ⚠️ | ⚠️ | ✅ | ✅ | ⚠️ (linking OK, modify triggers LGPL) |
| **GPL-3** | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ✅ | ❌ (viral copyleft) |
| **AGPL-3** | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ (network use triggers) |
| **Unlicense / Public Domain** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **CC-BY-*** | ⚠️ (attribution) | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| **CC-BY-SA** | ⚠️ (ShareAlike) | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ |
| **Custom / Unknown** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

## Rules

### ✅ MATCH (green-light)
- Proceed với attribution header
- No additional obligations beyond attribution

### ⚠️ WARN (yellow-light)
- **Action**: Surface warning trong Phase 4 Challenge
- User có thể override nếu:
  - LGPL → proprietary: chỉ link, không modify source code
  - CC-BY-*: tuân thủ attribution requirements
  - Custom license: user đã review + approve
- Attribution BẮT BUỘC cho tất cả WARN cases

### ❌ BLOCK (red-light — default refuse)
- GPL/AGPL → proprietary: copyleft viral, không tương thích
- Custom license chưa review
- **User có thể override** qua explicit `--ack-license-risk` flag + Challenge confirmation

## Special cases

### 1. GPL/LGPL — Static vs dynamic linking
- **Static link** (copy code vào binary): LGPL triggers — must release LGPL parts
- **Dynamic link** (import library): LGPL OK với proprietary
- **`/xia` always copies code** → treat LGPL as WARN

### 2. CC licenses (không phải software license)
- CC-BY: OK nếu thêm attribution
- CC-BY-SA: ShareAlike = phải release project cùng license → usually ❌
- CC0: public domain equivalent → ✅
- **Cảnh báo**: CC licenses không design cho code, có thể ambiguous

### 3. Proprietary source (không có LICENSE)
- **Default**: ❌ BLOCK (no rights granted)
- **Exception**: User có explicit written permission → override qua flag

### 4. Dual-license (MIT OR Apache)
- User choose permissive option → treat as MIT
- Auto-pick more permissive nếu không ambiguous

### 5. Third-party code in source
- Source có sub-licenses (vendored deps, snippets) → check transitively
- `check-license-compat.py` scan `**/LICENSE*`, `**/COPYING*`

## Attribution template (mandatory cho WARN+)

```js
/**
 * Adapted from {owner}/{repo}@{sha}
 * License: {source_license}
 * Original: {file_path}
 * Ported: {YYYY-MM-DD} by /xia (mode: {mode})
 *
 * NOTICE: This file is derived from third-party source.
 * See NOTICE file for full attribution.
 */
```

For GPL/LGPL copies (if user overrides):
```js
/**
 * This file contains code adapted from {repo} ({license}).
 * The derivative work MUST comply with {license} terms.
 * Original: {url}
 * Modifications: see git log
 */
```

## NOTICE file template

Maintain `NOTICE` file ở project root:

```
This project includes code adapted from:

1. {repo-name} ({url})
   License: {license}
   Files: {paths}
   Commit: {sha}
   Ported: {date}

2. ...
```

## Verification

Skill auto-update `NOTICE` + add attribution headers per entry in `.xia-manifest.json`.

Pre-release check: `python scripts/check-license-compat.py --verify-manifest .xia-manifest.json`
