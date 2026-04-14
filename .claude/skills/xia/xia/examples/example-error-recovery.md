# Example 3: Error recovery — Private repo + fallback

## User request

> *"Port auth implementation từ `https://github.com/acme-corp/internal-auth` về project em"*

## Command

```
/xia --improve https://github.com/acme-corp/internal-auth auth
```

## Workflow trace — Multiple failure points

### Step 1: Recon — FAIL 1

```
$ ck repomix --remote https://github.com/acme-corp/internal-auth
ERROR: 404 Not Found or Repository is private
```

**`/xia` response:**

```
❌ Repo không fetch được. Nguyên nhân có thể:
   1. Repo private — cần `gh auth login` + access grant
   2. Repo không tồn tại — sai URL
   3. Rate limit — retry sau 60s

Options:
   [a] Đã authenticate — retry
   [b] Paste snippet code trực tiếp (fallback --copy mode)
   [c] Provide alternative repo URL
   [d] Abort
```

User chọn `[a]` — đã run `gh auth login`.

### Step 1 retry — SUCCESS

```
$ gh repo view acme-corp/internal-auth
Access granted. Repo: 2.3k LOC, license: MIT
```

Recon proceeds.

### Step 2: Map — Encounter CONFLICT

```
MATRIX:
- `AuthService` class: CONFLICT (local có `AuthService` khác semantic)
- `bcrypt@4.0`: CONFLICT (local có `bcrypt@5.1`)
- `User` model: REPLACE_WITH_LOCAL
```

2 CONFLICTs → pass forward to Phase 4 Challenge (normal handling).

### Step 3: Analyze — Security finding 🟡

```
$ ck security --scan .xia/cache/internal-auth-sha/
Findings:
  YELLOW: Hardcoded JWT secret in src/config/jwt.ts:12
  YELLOW: No rate limit on /login endpoint
  YELLOW: Missing account lockout after N failed attempts
```

**`/xia` response:**

```
🟡 SECURITY WARNINGS (3 items) — see Phase 4 Challenge for decisions
```

### Step 4: Challenge — User aborts at Q5

```
Q1 [Env]: ... [a] proceed
Q2 [Deps]: bcrypt 4.0 → 5.1 upgrade? [a] upgrade
Q3 [Async]: ... [a] compat
Q4 [State]: ... [a] adapt

Q5 [License + Security]: Source có hardcoded JWT secret.
   Ported code sẽ có vulnerability (default secret in prod).
   Source: HARDCODED 'supersecret123'
   Local:  Should use env var JWT_SECRET
   Risk:   🔴 HIGH — production security hole
   
   Options:
     [a] Replace hardcoded với env var reading (recommended)
     [b] Keep hardcoded (accept risk — DEV ONLY)
     [c] Abort — review với security team
   
   Choose: c
```

User chose `[c]` abort.

### Step 4 result: ABORT

```
❌ Port aborted at Challenge phase.

Reason: User aborted on Q5 (security concern — hardcoded JWT secret)

Cleanup:
   .xia/cache/ kept for review
   No git branch created
   No manifest entry
   
Next steps:
   1. Review source code: cat .xia/cache/internal-auth-abc/src/config/jwt.ts
   2. Coordinate với security team
   3. If fixed upstream: retry /xia --improve ...
   4. If porting anyway: /xia --copy với --ack-security-risk flag

📄 Full recon report: .xia/cache/recon-summary.md
```

## Alternative fallback — Paste snippet

Nếu repo không access được, user có thể fallback:

```
/xia --copy --source-text - <<'EOF'
// From internal doc
class TokenBucket {
  constructor(capacity, refillRate) {
    this.capacity = capacity;
    // ...
  }
}
EOF
```

`/xia` xử lý như source ẩn danh:
- Source meta: user-provided snippet
- License: "user-attested" (user tự xác nhận có quyền dùng)
- Attribution: generic "Provided by user on {date}"
- Manifest entry với `source.repo: "user-provided"`

## Error recovery decision tree

```
Recon fetch fails?
├─ Private repo → gh auth login → retry
├─ Repo 404 → fix URL OR alternative source
├─ Rate limit → wait + retry
└─ Offline → prompt for snippet paste

Map finds CONFLICT?
└─ Always proceed → Challenge Phase

Analyze finds RED flag?
└─ REFUSE port (can't override — malicious code)

Analyze finds YELLOW flag?
└─ Surface in Challenge → user decides

Challenge aborts?
├─ Keep .xia/cache/ for review
├─ No git branch
├─ No manifest entry
└─ Suggest next steps (alt source, fix upstream, security review)

Deliver fails mid-phase?
├─ Stop at last checkpoint
├─ git reset --hard {checkpoint_sha}
├─ Log failure to .xia/audit.log
└─ Present options: retry phase / rollback all / manual fix
```

## Key lessons

1. **Graceful degradation** — không fail hard, always có fallback
2. **User agency** — abort is valid option at every step
3. **Preserve state** — cache kept for review, manifest untouched
4. **Clear next steps** — nói rõ user làm gì tiếp
5. **Security > speed** — 1 RED flag = REFUSE, không override
