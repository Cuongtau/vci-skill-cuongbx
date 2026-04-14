# Test Execution Tracker — IMS_AUTH_01

**Spec:** v1.0.0 | **Tester:** (assign) | **Started:** — | **Target sprint:** (TBD)

## 📊 Execution Dashboard

| Metric | Value |
|---|---|
| **Total TCs** | 31 |
| **Executed** | 0 / 31 (0%) |
| ✅ PASSED | 0 |
| ❌ FAILED | 0 |
| 🚫 BLOCKED | 0 |
| ⏸️ UNTESTED | 31 |
| **Pass rate** | — |

**Priority breakdown:**
- 🔴 P0 (Critical): 9 TCs
- 🟡 P1 (High): 7 TCs
- 🟢 P2 (Medium): 10 TCs
- ⚪ P3 (Low): 5 TCs

---

## 📋 Execution Matrix

Legend: `[ ]` untested · `[x]` passed · `[F]` failed · `[B]` blocked

### Happy Path (3 TCs)

| # | TC ID | Name | Priority | Category | Status | Actual Result | Bug ID |
|---|---|---|---|---|---|---|---|
| 1 | TC_001 | Login thành công credentials đúng | 🔴 P0 | Happy | `[ ]` UNTESTED | — | — |
| 2 | TC_002 | Login với Remember Me (30d) | 🟡 P1 | Happy | `[ ]` UNTESTED | — | — |
| 3 | TC_003 | Case-insensitive email match | 🟡 P1 | Happy | `[ ]` UNTESTED | — | — |

### Negative Path (5 TCs)

| # | TC ID | Name | Priority | Category | Status | Actual Result | Bug ID |
|---|---|---|---|---|---|---|---|
| 4 | TC_004 | Sai password → 401 | 🔴 P0 | Negative | `[ ]` UNTESTED | — | — |
| 5 | TC_005 | Email không tồn tại → 401 (timing) | 🔴 P0 | Negative-Sec | `[ ]` UNTESTED | — | — |
| 6 | TC_006 | Lockout sau 5 fails → 423 | 🔴 P0 | Negative-Sec | `[ ]` UNTESTED | — | — |
| 7 | TC_007 | Lockout timeout 15min | 🟡 P1 | Negative | `[ ]` UNTESTED | — | — |
| 8 | TC_008 | Rate limit 10 req/min → 429 | 🟡 P1 | Negative-Sec | `[ ]` UNTESTED | — | — |

### Edge Cases (4 TCs)

| # | TC ID | Name | Priority | Category | Status | Actual Result | Bug ID |
|---|---|---|---|---|---|---|---|
| 9 | TC_009 | Email empty → 400 | 🟢 P2 | Edge | `[ ]` UNTESTED | — | — |
| 10 | TC_010 | Email invalid format → 400 | 🟢 P2 | Edge | `[ ]` UNTESTED | — | — |
| 11 | TC_011 | Password < 8 chars → 400 | 🟢 P2 | Edge | `[ ]` UNTESTED | — | — |
| 12 | TC_012 | Email > 255 chars → 400 | ⚪ P3 | Edge | `[ ]` UNTESTED | — | — |

### State × Button Matrix (10 TCs)

| # | TC ID | State + Action | Priority | Category | Status | Actual | Bug |
|---|---|---|---|---|---|---|---|
| 13 | TC_M01 | Idle + `[Login]` click | 🔴 P0 | UI | `[ ]` UNTESTED | — | — |
| 14 | TC_M02 | Idle + `[Forgot pw?]` click | 🟢 P2 | UI | `[ ]` UNTESTED | — | — |
| 15 | TC_M03 | Idle + `[Remember me]` toggle | 🟢 P2 | UI | `[ ]` UNTESTED | — | — |
| 16 | TC_M04 | Validating + `[Login]` (disabled) | 🟡 P1 | UI | `[ ]` UNTESTED | — | — |
| 17 | TC_M05 | Validating + `[Forgot]` (disabled) | 🟢 P2 | UI | `[ ]` UNTESTED | — | — |
| 18 | TC_M06 | Validating + `[Remember]` (disabled) | ⚪ P3 | UI | `[ ]` UNTESTED | — | — |
| 19 | TC_M07 | LockedOut + `[Login]` (countdown) | 🟡 P1 | UI | `[ ]` UNTESTED | — | — |
| 20 | TC_M08 | LockedOut + `[Forgot]` (enabled) | 🟢 P2 | UI | `[ ]` UNTESTED | — | — |
| 21 | TC_M09 | LockedOut + `[Remember]` (disabled) | ⚪ P3 | UI | `[ ]` UNTESTED | — | — |
| 22 | TC_M10 | Authenticated → Dashboard | 🔴 P0 | UI | `[ ]` UNTESTED | — | — |

### Security (7 TCs)

| # | TC ID | Attack Vector | Priority | Automation | Status | Actual | Bug |
|---|---|---|---|---|---|---|---|
| 23 | TC_SEC_01 | SQL Injection email | 🔴 P0 | ✅ Auto | `[ ]` UNTESTED | — | — |
| 24 | TC_SEC_02 | XSS password field | 🟡 P1 | ✅ Auto | `[ ]` UNTESTED | — | — |
| 25 | TC_SEC_03 | RBAC bypass | 🔴 P0 | ✅ Auto | `[ ]` UNTESTED | — | — |
| 26 | TC_SEC_04 | IDOR user access | 🔴 P0 | ✅ Auto | `[ ]` UNTESTED | — | — |
| 27 | TC_SEC_05 | JWT tampering | 🔴 P0 | ✅ Auto | `[ ]` UNTESTED | — | — |
| 28 | TC_SEC_06 | CSRF | 🟡 P1 | 🟡 Manual pentest | `[ ]` UNTESTED | — | — |
| 29 | TC_SEC_07 | Timing attack enumeration | 🔴 P0 | 🟡 Manual (statistics) | `[ ]` UNTESTED | — | — |

### Performance (2 TCs)

| # | TC ID | Target | Priority | Status | Actual | Bug |
|---|---|---|---|---|---|---|
| 30 | PERF_01 | Login p95 < 500ms (k6) | 🟡 P1 | `[ ]` UNTESTED | — | — |
| 31 | PERF_02 | Rate limit at req 11 | 🟡 P1 | `[ ]` UNTESTED | — | — |

---

## 🎯 Execution Plan

### Phase 1: Smoke (P0 only, ~2h)
Run: TC_001, TC_004, TC_005, TC_006, TC_M01, TC_M10, TC_SEC_01, TC_SEC_03, TC_SEC_04, TC_SEC_05, TC_SEC_07

**Gate:** Tất cả P0 PASS trước khi proceed P1.

### Phase 2: Regression (P1 + P2, ~1 ngày)
Run tất cả TC_002-012, TC_M02-M09, TC_008, TC_SEC_02, TC_SEC_06, PERF_01, PERF_02.

### Phase 3: Edge + Low priority (~4h)
Remaining P3 tests.

### Automation run

```bash
# E2E tests (29 automated)
npx playwright test tests/e2e/auth-login.spec.ts

# Security SAST scan
semgrep --config=auto src/auth/

# Performance
k6 run references/patterns/k6-login-p95.js
```

### Manual tests (2)
- TC_SEC_06 CSRF — security team verify bằng Burp Suite
- TC_SEC_07 Timing attack — run 100 iterations, phân tích distribution

---

## 📤 Reporting template

Copy bảng "Execution Matrix" trên sang Google Sheets / Excel cho daily stand-up:

```
Sheet: QA_Dashboard
Range: A1:G32 (Execution Matrix)
Conditional formatting:
  - UNTESTED → grey
  - PASSED  → green
  - FAILED  → red
  - BLOCKED → yellow
```

**Daily update protocol:**
1. QA tester update column `Status` + `Actual Result`
2. Nếu FAILED → tạo bug trong Jira, paste ID vào `Bug ID`
3. Run `/vci ai đang làm gì?` để sync dashboard với PM

---

## ✅ Definition of Done (QA sign-off)

- [ ] P0 pass rate = 100% (9/9)
- [ ] P1 pass rate ≥ 95% (6.65/7, làm tròn 7/7)
- [ ] P2 pass rate ≥ 90% (9/10)
- [ ] Automated tests integrated vào CI pipeline
- [ ] Performance targets met (PERF_01 p95 < 500ms)
- [ ] Security review signed off bởi security team
- [ ] No open 🔴 Critical bugs
- [ ] Regression checklist (`test_cases.md` §3) chạy + PASS

## Unresolved

- [ ] Assign QA lead cho IMS_AUTH_01
- [ ] Staging environment ready cho k6 load test
- [ ] Security team availability cho manual pentest (TC_SEC_06)
