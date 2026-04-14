# Phase 2: 🗺️ Map — Decompose feature thành layers

**Goal:** Biết chính xác cái gì cần port, cái gì local đã có, cái gì sẽ xung đột.

## Compose skills

| Skill | Mục đích |
|---|---|
| `ck:scout` | Parallel scan local codebase tìm equivalent |
| `spec-to-code-compliance` | Map source intent → local implementation |

## 7 Layers

Mọi feature đều decompose được thành 7 layers:

| Layer | Source content | Typical files |
|---|---|---|
| **1. Core logic** | Pure functions, algorithms | `*.ts`, `*.py` (no I/O) |
| **2. State** | Stores, contexts, reducers | `store.ts`, `state.py` |
| **3. Data** | Models, schemas, DB queries | `models/`, `schemas/` |
| **4. API surface** | Routes, handlers, controllers | `routes/`, `api/` |
| **5. Config** | Env vars, feature flags | `config.ts`, `.env` keys |
| **6. Types** | TS interfaces, type defs | `types.ts`, `types/` |
| **7. Tests** | Unit, integration tests | `*.test.ts`, `tests/` |

## Dependency Matrix

Với mỗi component trong source, classify:

| Status | Meaning | Default action |
|---|---|---|
| `EXISTS` | Local có tương đương | Reuse, skip port |
| `NEW` | Chưa có | Port + user approve |
| `CONFLICT` | Same name, khác semantic | → Challenge Phase 4 |
| `REPLACE_WITH_LOCAL` | Local có nhưng dùng pattern khác | Swap reference |

### Example matrix

| Source | Status | Local equivalent | Action |
|---|---|---|---|
| `authService.login()` | NEW | — | Port core logic |
| `lodash@v5.12` | CONFLICT | `lodash@v3.10` (local) | Challenge: upgrade or inline? |
| `User model (mongoose)` | REPLACE_WITH_LOCAL | `User model (prisma)` | Swap ORM |
| `bcrypt@5.1` | EXISTS | `bcrypt@5.1` | Reuse |
| `jsonwebtoken@9.0` | NEW | — | Add to package.json |

## Steps

### 2.1. Extract source components

Từ Recon cache, list tất cả:
- Functions (public + private)
- Classes
- Exports
- Dependencies (direct)
- Config keys
- Type definitions

### 2.2. Parallel scan local

```bash
ck scout --targets "authService,UserModel,..." --within src/ \
  --output .xia/cache/local-scan.json
```

### 2.3. Build matrix

Cho mỗi source component, match với local scan:
- Exact name match → `EXISTS` hoặc `CONFLICT`
- Semantic match (different name, same role) → `REPLACE_WITH_LOCAL`
- No match → `NEW`

### 2.4. File impact list

Output 3 lists:

```yaml
files_to_create:
  - src/auth/login.ts         # NEW
  - src/auth/token.ts         # NEW
  - src/auth/middleware.ts    # NEW

files_to_modify:
  - src/routes/index.ts       # add /login, /logout routes
  - package.json              # add jsonwebtoken@9

files_to_replace:
  - src/lib/lodash.ts         # REPLACE_WITH_LOCAL pattern
```

### 2.5. Mode-specific adjustments

| Mode | Adjustment |
|---|---|
| `--compare` | Chỉ output matrix, không proceed |
| `--copy` | Minimize REPLACE_WITH_LOCAL — ưu tiên copy + fix imports |
| `--improve` | Aggressive REPLACE — integrate với local patterns |
| `--port` | Rewrite mọi layer cho local stack |

## Output → Phase 3

```yaml
layers_detected: 5  # core, state, config, api, types
matrix:
  exists: 3
  new: 12
  conflict: 2  # → Phase 4 Challenge
  replace: 4
file_impact:
  create: 8
  modify: 3
  replace: 4
estimated_effort: MEDIUM  # LOW <5 files, MEDIUM 5-15, HIGH >15
```
