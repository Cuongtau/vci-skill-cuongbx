# Test Cases — IMS_AUTH_01 User Login

**Source spec:** [spec.md](spec.md) v1.0.0 | **QA Lead:** (TBD) | **Created:** 2026-04-14

## Test Data Prerequisites

```sql
-- Setup cho tất cả tests
INSERT INTO users (id, email, password_hash, role, created_at) VALUES
  ('uuid-1', 'test@example.com', '$2b$12$hashed_bcrypt_secret123', 'user', NOW()),
  ('uuid-2', 'admin@example.com', '$2b$12$hashed_bcrypt_admin456', 'admin', NOW()),
  ('uuid-3', 'Locked@Example.com', '$2b$12$hashed_bcrypt_pwd789', 'user', NOW());

-- Redis cleanup between tests
FLUSHDB lockout:*
```

**Env vars:**
- `JWT_SECRET_PRIVATE` — RS256 private key (test keypair)
- `JWT_EXPIRES_DEFAULT=86400` (24h)
- `JWT_EXPIRES_REMEMBER=2592000` (30d)
- `BCRYPT_ROUNDS=12`
- `LOCKOUT_MAX_ATTEMPTS=5`
- `LOCKOUT_DURATION_SEC=900`
- `RATE_LIMIT_PER_IP_PER_MIN=10`

---

## 1. BDD Test Cases — Từ Acceptance Criteria

### 🟢 Happy Path

#### TC_001 — Login thành công với credentials đúng (AC_001)
**Priority:** P0 | **Category:** Happy | **Automation:** ✅ Playwright

```gherkin
Given user "test@example.com" đã đăng ký với password "secret123"
  And Redis không có key "lockout:test@example.com"
When user POST /api/auth/login với body:
  | email    | test@example.com |
  | password | secret123        |
Then response status = 200
  And response body có `token` (JWT signed RS256)
  And response body có `expires_in: 86400`
  And response body có `user.id: uuid-1`
  And response body có `user.role: user`
  And audit_log có entry mới { user_id: uuid-1, action: "login_success" }
  And JWT decode với public key không throw error
  And JWT payload có `sub: uuid-1`, `exp: now + 86400`
```

#### TC_002 — Login với Remember Me (AC_005, BR_007)
**Priority:** P1 | **Category:** Happy | **Automation:** ✅

```gherkin
Given user "test@example.com" đã đăng ký
When user POST /api/auth/login với { email, password, remember_me: true }
Then response status = 200
  And response body có `expires_in: 2592000` (30 ngày)
  And JWT payload có `exp: now + 2592000`
```

#### TC_003 — Case-insensitive email match (AC_004, BR_004)
**Priority:** P1 | **Category:** Happy | **Automation:** ✅

```gherkin
Given user đã đăng ký với email "Test@Example.COM" (mixed case)
When user POST /api/auth/login với email "test@example.com" (lowercase)
Then response status = 200
  And user match được dù khác case
  And audit_log log email dạng normalized lowercase
```

### 🔴 Negative Path

#### TC_004 — Sai password (AC_002, BR_002)
**Priority:** P0 | **Category:** Negative | **Automation:** ✅

```gherkin
Given user "test@example.com" đã đăng ký
When user POST /api/auth/login với password sai
Then response status = 401
  And response body = { error: "invalid_credentials", message: "Email hoặc mật khẩu không đúng" }
  And response body KHÔNG có `token`
  And audit_log có entry { email, action: "login_fail", reason: "bad_password" }
  And Redis increment counter `failed_attempts:test@example.com`
```

#### TC_005 — Email không tồn tại (Security — timing attack prevention)
**Priority:** P0 | **Category:** Negative-Security | **Automation:** ✅

```gherkin
Given KHÔNG có user với email "notexist@example.com"
When user POST /api/auth/login với email này
Then response status = 401
  And response body = { error: "invalid_credentials" } (GIỐNG TC_004 — không lộ email enumeration)
  And response time delta < 50ms so với TC_004 (prevent timing attack)
  And audit_log có entry { email, action: "login_fail", reason: "user_not_found" }
```

#### TC_006 — Lockout sau 5 lần sai (AC_003, BR_001)
**Priority:** P0 | **Category:** Negative-Security | **Automation:** ✅

```gherkin
Given user "test@example.com" đã sai password 4 lần trong 10 phút
When user POST /api/auth/login với password sai lần thứ 5
Then response status = 423 Locked
  And response body = { error: "account_locked", message: "Tài khoản tạm khóa", retry_after_seconds: 900 }
  And Redis có key "lockout:test@example.com" với TTL ~900s
  And audit_log có entry { email, action: "account_locked" }
  And email notification gửi tới user (theo Notification Rule)
```

#### TC_007 — Lockout timeout (15 phút sau unlock)
**Priority:** P1 | **Category:** Negative | **Automation:** ✅

```gherkin
Given user "test@example.com" bị lockout, Redis TTL lockout key đã expire
When user POST /api/auth/login với credentials đúng
Then response status = 200 (login thành công)
  And Redis không còn key "lockout:*"
  And Redis reset counter `failed_attempts:*`
```

#### TC_008 — Rate limit 10 req/phút/IP (BR_005)
**Priority:** P1 | **Category:** Negative-Security | **Automation:** ✅

```gherkin
Given IP "203.0.113.42" đã gửi 10 requests tới /api/auth/login trong 60s
When IP này gửi request thứ 11
Then response status = 429 Too Many Requests
  And response body = { error: "rate_limit_exceeded", retry_after_seconds: 60 }
  And request KHÔNG query DB (block ở middleware)
```

### 🟡 Edge Cases

#### TC_009 — Email empty
**Priority:** P2 | **Category:** Edge | **Automation:** ✅

```gherkin
When user POST /api/auth/login với email = ""
Then response status = 400 Bad Request
  And response body có validation error: "email is required"
```

#### TC_010 — Email invalid format
**Priority:** P2 | **Category:** Edge | **Automation:** ✅

```gherkin
When user POST /api/auth/login với email = "not-an-email"
Then response status = 400
  And response body có validation error: "email must be valid format"
```

#### TC_011 — Password < 8 chars
**Priority:** P2 | **Category:** Edge | **Automation:** ✅

```gherkin
When user POST /api/auth/login với password = "abc" (3 chars)
Then response status = 400
  And response body có validation error: "password must be at least 8 characters"
```

#### TC_012 — Email > 255 chars
**Priority:** P3 | **Category:** Edge | **Automation:** ✅

```gherkin
When user POST /api/auth/login với email 256 chars
Then response status = 400
  And response body có validation error: "email exceeds max length"
```

---

## 2. State × Button Test Matrix

| Test ID | State | Action on `[Login]` | Action on `[Forgot pw?]` | Action on `[Remember me]` | Expected |
|---|---|---|---|---|---|
| TC_M01 | Idle | Click submit | — | — | → Validating state + API call |
| TC_M02 | Idle | — | Click link | — | Navigate to `/auth/forgot` |
| TC_M03 | Idle | — | — | Toggle on | Checkbox checked, no API call |
| TC_M04 | Validating | Click submit | — | — | No-op (button disabled) |
| TC_M05 | Validating | — | Click link | — | No-op (link disabled) |
| TC_M06 | Validating | — | — | Toggle | No-op (checkbox disabled) |
| TC_M07 | LockedOut | Click submit | — | — | No-op + show countdown |
| TC_M08 | LockedOut | — | Click link | — | Navigate to `/auth/forgot` ✅ |
| TC_M09 | LockedOut | — | — | Toggle | No-op (disabled) |
| TC_M10 | Authenticated | — | — | — | Redirect to `/dashboard` |

---

## 3. Regression Checklist (Impact Matrix)

Chạy sau mọi change tới IMS_AUTH_01:

- [ ] Existing tests `IMS_USER_01` (user registration) still pass
- [ ] JWT issued by login vẫn decode được ở các endpoints sau:
  - [ ] `/api/users/me` (GET)
  - [ ] `/api/inventory/*` (protected routes)
- [ ] Refresh token flow (IMS_AUTH_03 nếu có) vẫn work
- [ ] Password reset (IMS_AUTH_02) không bị ảnh hưởng
- [ ] Rate limit không leak vào các endpoints khác
- [ ] Audit log không lộ password trong logs

---

## 4. Security Test Scenarios

### 🛡️ TC_SEC_01 — SQL Injection trong email field
**Priority:** P0 | **Category:** Security

```gherkin
When user POST /api/auth/login với email = "admin@example.com' OR '1'='1"
Then response status = 401 (không phải 500 hay 200)
  And KHÔNG có SQL error trong logs (parameterized query working)
  And audit_log có entry { email: "admin@example.com' OR...", action: "login_fail" }
```

### 🛡️ TC_SEC_02 — XSS trong password field (reflected)
**Priority:** P1 | **Category:** Security

```gherkin
When user POST /api/auth/login với password = "<script>alert(1)</script>"
Then response body KHÔNG echo password
  And logs KHÔNG chứa raw password (chỉ log email)
```

### 🛡️ TC_SEC_03 — RBAC bypass attempt
**Priority:** P0 | **Category:** Security

```gherkin
Given user thường login thành công
When user gọi `/api/admin/users` với JWT của role "user"
Then response status = 403 Forbidden
  And audit_log có entry { user_id, action: "rbac_denied", endpoint }
```

### 🛡️ TC_SEC_04 — IDOR — access user khác
**Priority:** P0 | **Category:** Security

```gherkin
Given user A login (JWT sub = "uuid-A")
When user A gọi `/api/users/uuid-B`
Then response status = 403 (hoặc 404 để tránh enumeration)
```

### 🛡️ TC_SEC_05 — JWT tampering
**Priority:** P0 | **Category:** Security

```gherkin
Given user có JWT hợp lệ
When user sửa payload (đổi `role: "user"` → `"admin"`) và gọi /api/admin/*
Then response status = 401 (signature invalid)
  And audit_log: { action: "jwt_tampering_detected" }
```

### 🛡️ TC_SEC_06 — CSRF on /auth/login
**Priority:** P1 | **Category:** Security

```gherkin
When cross-origin request tới /auth/login từ `evil.com`
Then CORS block (Access-Control-Allow-Origin check)
  Or CSRF token required nếu form-based
```

### 🛡️ TC_SEC_07 — Timing attack email enumeration
**Priority:** P0 | **Category:** Security | **Depends on TC_005**

```gherkin
Run 100 iterations of TC_004 (email exists) và TC_005 (email not exist)
Then p95(response_time_exists) - p95(response_time_not_exist) < 50ms
  // Không thể phân biệt email tồn tại qua timing
```

---

## 5. Performance Test Scenarios (k6)

### 🚀 PERF_01 — Login p95 latency < 500ms

```javascript
// k6 script (references/patterns/k6-login-p95.js)
import http from 'k6/http';
import { check } from 'k6';
import { Trend } from 'k6/metrics';

export const options = {
  stages: [
    { duration: '30s', target: 50 },   // ramp up
    { duration: '2m', target: 50 },    // steady 50 VUs
    { duration: '30s', target: 0 },    // ramp down
  ],
  thresholds: {
    'http_req_duration{endpoint:login}': ['p(95)<500', 'p(99)<1000'],
    'http_req_failed': ['rate<0.01'],
  },
};

export default function () {
  const payload = JSON.stringify({
    email: `load${__VU}@example.com`,
    password: 'secret123',
  });
  const res = http.post(`${__ENV.API_URL}/api/auth/login`, payload, {
    headers: { 'Content-Type': 'application/json' },
    tags: { endpoint: 'login' },
  });
  check(res, { 'status 200': (r) => r.status === 200 });
}
```

**Target:** p95 < 500ms, p99 < 1000ms, error rate < 1%

### 🚀 PERF_02 — Rate limit stress test

Bắn 100 req/s từ 1 IP → xác nhận 429 trả về sau req thứ 10, đúng theo BR_005.

---

## 6. Automation Skeleton (Playwright)

```typescript
// tests/e2e/auth-login.spec.ts
import { test, expect } from '@playwright/test';

const API = process.env.API_URL || 'http://localhost:3000';

test.describe('IMS_AUTH_01 — User Login', () => {
  test('TC_001: Happy path login', async ({ request }) => {
    const res = await request.post(`${API}/api/auth/login`, {
      data: { email: 'test@example.com', password: 'secret123' },
    });
    expect(res.status()).toBe(200);
    const body = await res.json();
    expect(body).toHaveProperty('token');
    expect(body.expires_in).toBe(86400);
    expect(body.user.role).toBe('user');
  });

  test('TC_004: Invalid credentials', async ({ request }) => {
    const res = await request.post(`${API}/api/auth/login`, {
      data: { email: 'test@example.com', password: 'wrong' },
    });
    expect(res.status()).toBe(401);
    const body = await res.json();
    expect(body.error).toBe('invalid_credentials');
    expect(body).not.toHaveProperty('token');
  });

  test('TC_006: Account lockout after 5 failures', async ({ request }) => {
    // Reset state
    await request.post(`${API}/api/test/reset-lockout`, {
      data: { email: 'test@example.com' },
    });
    // Fail 5 times
    for (let i = 0; i < 5; i++) {
      await request.post(`${API}/api/auth/login`, {
        data: { email: 'test@example.com', password: 'wrong' },
      });
    }
    // 6th should be locked
    const res = await request.post(`${API}/api/auth/login`, {
      data: { email: 'test@example.com', password: 'secret123' },
    });
    expect(res.status()).toBe(423);
    const body = await res.json();
    expect(body.error).toBe('account_locked');
    expect(body.retry_after_seconds).toBeGreaterThanOrEqual(850);
  });

  // ... TC_002, 003, 005, 007-012 follow same pattern
});

test.describe('State machine (UI E2E)', () => {
  test('TC_M01: Idle → Validating → Authenticated', async ({ page }) => {
    await page.goto('/auth/login');
    await page.fill('[data-testid="email"]', 'test@example.com');
    await page.fill('[data-testid="password"]', 'secret123');
    await page.click('[data-testid="login-btn"]');
    // Validating state
    await expect(page.locator('[data-testid="login-btn"]')).toBeDisabled();
    // Redirect to dashboard
    await page.waitForURL('**/dashboard', { timeout: 5000 });
  });
});
```

---

## 7. Coverage Summary

| Category | Count | Automation |
|---|---|---|
| Happy path | 3 (TC_001-003) | ✅ 3/3 |
| Negative | 5 (TC_004-008) | ✅ 5/5 |
| Edge cases | 4 (TC_009-012) | ✅ 4/4 |
| State matrix | 10 (TC_M01-M10) | ✅ 10/10 |
| Security | 7 (TC_SEC_01-07) | 🟡 5/7 (2 manual pentesting) |
| Performance | 2 (PERF_01-02) | ✅ 2/2 (k6) |
| **Total** | **31 test cases** | **29/31 automated (93%)** |

---

## Unresolved

- [ ] Cần confirm với PM: có implement `IMS_AUTH_03 Refresh Token` không → ảnh hưởng TC_002 (remember me) expiry logic
- [ ] Cần security team review: threshold lockout 5 lần có đủ strict cho regulated data không
- [ ] k6 load test setup cần dedicated staging env → block to QA team
