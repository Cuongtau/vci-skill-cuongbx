# Example 1: `--compare` mode — Analyze auth approach

## User request

> *"So sánh cách xử lý auth của repo `https://github.com/vercel/next-auth` với project em. Em dùng FastAPI."*

## Command

```
/xia --compare https://github.com/vercel/next-auth auth
```

## Workflow trace

### Step 1: Recon
- `ck:repomix` pack `vercel/next-auth@main` → 18k LOC, MIT license
- Locate feature: `packages/next-auth/src/` (main package)
- README: "Authentication for Next.js apps"
- License MATCH: MIT → Apache-2.0 (local) ✅

### Step 2: Map
- Source layers:
  - Core: session management, JWT, CSRF
  - State: session storage (cookies + DB adapter)
  - Data: User/Account/Session models
  - API: `/api/auth/[...nextauth]` catch-all handler
  - Config: `NextAuthOptions` + providers array
  - Types: full TS type system
  - Tests: integration tests

- Local equivalents scan:
  - `src/auth/` — FastAPI Depends-based auth
  - `src/users/` — SQLAlchemy User model
  - No middleware pattern (FastAPI uses `Depends`)

### Step 3: Analyze (không chạy vì --compare)

### Step 4: Challenge → Compare decision matrix

Phase 4 được skip cho --compare, thay bằng **comparison matrix** output.

## Output

```markdown
# Auth Approach Comparison — NextAuth.js vs FastAPI (local)

| Dimension | NextAuth.js | Local (FastAPI) | Verdict |
|---|---|---|---|
| **Session storage** | Cookies + optional DB adapter | JWT in header only | 🟡 Different; local stateless |
| **Token refresh** | Auto-refresh with callbacks | Manual `/auth/refresh` endpoint | 🟡 Local less ergonomic |
| **Provider abstraction** | Plugin architecture (30+ providers) | Hardcoded 2 providers | 🔴 Local much weaker |
| **CSRF** | Built-in CSRF token | Relies on SameSite cookies | 🟡 Local weaker |
| **Middleware integration** | `middleware.ts` global | Per-route `Depends` | 🟡 Different paradigms |
| **Typing** | Full TS types | Pydantic models | 🟢 Local strong |
| **Test coverage** | 85% + e2e | 60% unit only | 🔴 Local weaker |
| **Dep surface** | @auth/core, providers, adapters | passlib, python-jose | 🟢 Local lean |
| **Account linking** | Built-in | Not supported | 🔴 Missing |
| **Email verification flow** | Built-in | Manual | 🟡 Local incomplete |

## Gaps worth porting (nếu user quyết port sau)

1. **Provider abstraction pattern** — extensible for OAuth providers
2. **Account linking** — merge multiple auth methods per user
3. **CSRF built-in** — prevent common vuln
4. **Email verification flow** — standard UX

## NOT worth porting

- Session storage — paradigm clash (stateful vs stateless)
- Middleware pattern — FastAPI Depends is more pythonic

## Suggested next action

`/xia --port https://github.com/vercel/next-auth providers` (just port provider abstraction to FastAPI)

Estimated effort: 6-8 hours.
```

## Files changed

**Zero**. `--compare` mode chỉ output analysis, không ghi file.

## Manifest impact

Không update manifest — chỉ port modes (--copy/--improve/--port) update manifest.

## Time: ~8 minutes

- Recon: 3 min (fetch + parse)
- Map: 4 min (local scan + matrix)
- Output: 1 min
