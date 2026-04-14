# Ví dụ: Error recovery — Repo private + fallback paths

## User request

> *"Port auth implementation từ `https://github.com/acme-corp/internal-auth` về project em"*

## Lệnh

```
/xia --improve https://github.com/acme-corp/internal-auth auth
```

## Trace workflow — Nhiều failure points

### Step 1: Recon — FAIL 1 (repo private)

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

Recon tiếp tục.

### Step 2: Map — Encounter CONFLICT

```
MATRIX:
- `AuthService` class: CONFLICT (local có `AuthService` khác semantic)
- `bcrypt@4.0`: CONFLICT (local có `bcrypt@5.1`)
- `User` model: REPLACE_WITH_LOCAL
```

2 CONFLICTs → forward to Phase 4 Challenge (normal handling).

### Step 3: Analyze — Security finding 🟡

```
$ ck security --scan .xia/cache/internal-auth-sha/
Findings:
  YELLOW: Hardcoded JWT secret trong src/config/jwt.ts:12
  YELLOW: Không có rate limit trên /login endpoint
  YELLOW: Missing account lockout sau N failed attempts
```

**`/xia` response:**

```
🟡 SECURITY WARNINGS (3 items) — xem Phase 4 Challenge để quyết
```

### Step 4: Challenge — User aborts ở Q5

```
Q1 [Environment]: ... [a] proceed
Q2 [Dependencies]: bcrypt 4.0 → 5.1 upgrade? [a] upgrade
Q3 [Async]: ... [a] compat
Q4 [State]: ... [a] adapt

Q5 [License + Security]: Source có hardcoded JWT secret.
   Ported code sẽ có vulnerability (default secret in prod).
   Source: HARDCODED 'supersecret123'
   Local:  Nên dùng env var JWT_SECRET
   Risk:   🔴 HIGH — production security hole
   
   Options:
     [a] Replace hardcoded với env var reading (recommended)
     [b] Keep hardcoded (accept risk — DEV ONLY)
     [c] Abort — review với security team
   
   Chọn: c
```

User chọn `[c]` — abort.

### Step 4 result: ABORT

```
❌ Port aborted ở Challenge phase.

Nguyên nhân: User aborted Q5 (security concern — hardcoded JWT secret)

Cleanup:
   .xia/cache/ giữ lại để review
   Không tạo git branch
   Không tạo manifest entry

Next steps:
   1. Review source code: cat .xia/cache/internal-auth-abc/src/config/jwt.ts
   2. Coordinate với security team
   3. Nếu fix upstream: retry /xia --improve ...
   4. Nếu port anyway: /xia --copy với --ack-security-risk flag

📄 Full recon report: .xia/cache/recon-summary.md
```

## Fallback thay thế — Paste snippet

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

## Decision tree error recovery

```
Recon fetch fails?
├─ Private repo → gh auth login → retry
├─ Repo 404 → fix URL HOẶC alternative source
├─ Rate limit → wait + retry
└─ Offline → prompt paste snippet

Map finds CONFLICT?
└─ Always proceed → Challenge Phase

Analyze finds RED flag (eval+network+obfuscation)?
└─ REFUSE port (không override — malicious code)

Analyze finds YELLOW flag?
└─ Surface ở Challenge → user quyết

Challenge aborts?
├─ Keep .xia/cache/ để review
├─ Không tạo git branch
├─ Không tạo manifest entry
└─ Suggest next steps (alt source, fix upstream, security review)

Deliver fails mid-phase (nếu dùng /ck:cook)?
├─ Stop ở last checkpoint
├─ git reset --hard {checkpoint_sha}
├─ Log failure vào .xia/audit.log
└─ Present options: retry phase / rollback all / manual fix
```

## Bài học

1. **Graceful degradation** — không fail hard, luôn có fallback
2. **User agency** — abort là option valid ở mọi step
3. **Preserve state** — cache giữ lại cho review, manifest không touch
4. **Clear next steps** — nói rõ user làm gì tiếp
5. **Security > speed** — 1 RED flag = REFUSE, không override
