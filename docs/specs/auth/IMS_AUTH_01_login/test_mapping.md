# Requirement → Test Mapping (RTM) — IMS_AUTH_01

**Source:** [spec.md](spec.md) | **Tests:** [test_cases.md](test_cases.md)

## AC → Test Cases Coverage

| AC ID | Acceptance Criteria | Test Cases | Status |
|---|---|---|---|
| AC_001 | Happy path login | TC_001 | ✅ Covered |
| AC_002 | Invalid credentials → 401 | TC_004 | ✅ Covered |
| AC_003 | Lockout sau 5 fails → 423 | TC_006 | ✅ Covered |
| AC_004 | Case-insensitive email | TC_003 | ✅ Covered |
| AC_005 | Remember me → 30d expiry | TC_002 | ✅ Covered |

## BR → Test Cases Coverage

| BR ID | Business Rule | Test Cases | Priority | Status |
|---|---|---|---|---|
| BR_001 | Lockout 5 attempts / 15min | TC_006, TC_007 | P0 | ✅ |
| BR_002 | bcrypt verify (12 rounds) | TC_001, TC_004, TC_SEC_01 | P0 | ✅ |
| BR_003 | JWT expires 24h | TC_001 (assert exp) | 🟡 High | ✅ |
| BR_004 | Email case-insensitive | TC_003 | 🟡 High | ✅ |
| BR_005 | Rate limit 10 req/min/IP | TC_008, PERF_02 | 🟡 High | ✅ |
| BR_006 | Audit log mọi attempt | TC_001, TC_004, TC_005, TC_006 (audit_log assertions) | 🟢 Medium | ✅ |
| BR_007 | Remember me → 30d | TC_002 | 🟢 Low | ✅ |

## State Machine → Test Cases

| State Transition | Test Case |
|---|---|
| Idle → Validating | TC_M01 |
| Validating → Authenticated | TC_001, TC_M01 |
| Validating → Idle (< 5 fails) | TC_004 |
| Validating → LockedOut (5th fail) | TC_006 |
| LockedOut → Idle (15min timeout) | TC_007 |
| Authenticated → Dashboard | TC_001 (verify redirect) |

## API Response → Test Cases

| HTTP Status | Endpoint | Test Cases |
|---|---|---|
| 200 OK | POST /auth/login | TC_001, TC_002, TC_003 |
| 400 Bad Request | Validation error | TC_009, TC_010, TC_011, TC_012 |
| 401 Unauthorized | Invalid credentials | TC_004, TC_005 |
| 423 Locked | Account locked | TC_006 |
| 429 Too Many Requests | Rate limit | TC_008 |

## Security Scenarios

| Attack Vector | Test Case | Severity |
|---|---|---|
| SQL Injection | TC_SEC_01 | 🔴 Critical |
| XSS (reflected) | TC_SEC_02 | 🟡 High |
| RBAC bypass | TC_SEC_03 | 🔴 Critical |
| IDOR | TC_SEC_04 | 🔴 Critical |
| JWT tampering | TC_SEC_05 | 🔴 Critical |
| CSRF | TC_SEC_06 | 🟡 High |
| Timing attack enumeration | TC_SEC_07 | 🔴 Critical |

## Performance Targets

| Metric | Target | Test | Status |
|---|---|---|---|
| Login p95 latency | < 500ms | PERF_01 | 🟡 Pending run |
| Login p99 latency | < 1000ms | PERF_01 | 🟡 |
| Error rate under 50 VU load | < 1% | PERF_01 | 🟡 |
| Rate limit behavior | 429 at req 11 | PERF_02 | 🟡 |

## Coverage Matrix Summary

| Requirement Type | Total | Covered | % |
|---|---|---|---|
| AC | 5 | 5 | 100% |
| BR | 7 | 7 | 100% |
| State transitions | 6 | 6 | 100% |
| HTTP responses | 5 | 5 | 100% |
| Security scenarios | 7 | 7 | 100% |
| Performance targets | 4 | 4 | 100% (pending execution) |

**Overall:** 34/34 requirements mapped to tests = **100% traceability**

## Unresolved

- [ ] IMS_AUTH_03 Refresh Token (out of scope cho spec này) — cross-check khi AUTH_03 ra
