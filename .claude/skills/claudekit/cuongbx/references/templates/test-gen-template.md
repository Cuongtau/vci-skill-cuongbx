# Test Gen Template

Template cho AI khi sinh Test Cases (Mode 6). Đảm bảo 10/10 cho QA/Tester role.

---

## Cấu trúc output

```
docs/specs/{module}/{Feature_ID}_{tên}/
├── test_cases.md       ← BDD + Matrix + Security + Performance
└── test_mapping.md     ← Requirement → Test traceability
```

---

## 1. Header & Test Summary

```markdown
# TEST CASES — {Feature_ID}: {Tên tính năng}

> Auto-generated from spec `{spec_path}`
> Generated: {DD/MM/YYYY}
> Spec Version: {version}

## Test Summary
| Metric | Count |
|--------|-------|
| Total Test Cases | {n} |
| Happy Path | {n} |
| Edge Cases | {n} |
| Negative Cases | {n} |
| Security Tests | {n} |
| Performance Tests | {n} |
| Estimated Execution Time | {X}h |
```

---

## 2. Test Data Prerequisites

```markdown
## Test Data Prerequisites

### Required Seed Data
| Data | State | Setup Method | Cleanup |
|------|-------|-------------|---------|
| User `admin_kho` | Active, role: warehouse_admin | Seed script: `seed/users.sql` | Auto-rollback |
| User `viewer` | Active, role: viewer | Seed script: `seed/users.sql` | Auto-rollback |
| Product "Xi măng" | Active, unit: Tấn, stock: 100 | Seed script: `seed/products.sql` | Auto-rollback |
| Category "Vật liệu XD" | Active | Seed script: `seed/categories.sql` | Auto-rollback |
| Warehouse "Kho chính" | Active | Seed script: `seed/warehouses.sql` | Auto-rollback |

### Environment Requirements
| Requirement | Value |
|------------|-------|
| DB | PostgreSQL 15+ with test schema |
| Redis | Running on localhost:6379 |
| API Server | Running on localhost:3000 |
| Frontend | Running on localhost:5173 |
```

---

## 3. BDD Test Cases (từ Acceptance Criteria)

```markdown
## Functional Test Cases

### TC_{Feature_ID}_001: [Happy Case] {Tên scenario}
**Priority:** 🔴 Critical
**Spec Ref:** AC 4.5 Scenario 1
**Precondition:** {User logged in, data exists}

| Step | Given | When | Then |
|------|-------|------|------|
| 1 | User `admin_kho` đã đăng nhập | Navigate to /{feature}/new | Form tạo mới hiển thị, các field rỗng |
| 2 | Form hiển thị | Nhập đầy đủ thông tin hợp lệ | Không có validation error |
| 3 | Thông tin đã nhập | Click "Lưu" | Toast "Tạo thành công", redirect danh sách |
| 4 | Redirect danh sách | Verify danh sách | Record mới xuất hiện đầu tiên, status = "Nháp" |

---

### TC_{Feature_ID}_002: [Edge Case] {Tên scenario}
**Priority:** 🟡 Medium
**Spec Ref:** AC 4.5 Scenario 2

| Step | Given | When | Then |
|------|-------|------|------|
| 1 | {edge condition} | {action} | {expected behavior} |

---

### TC_{Feature_ID}_003: [Negative] {Tên scenario}
**Priority:** 🟡 Medium
**Spec Ref:** BR_01, AC Scenario 3

| Step | Given | When | Then |
|------|-------|------|------|
| 1 | User đã đăng nhập | Submit form với field bắt buộc trống | Validation error inline hiển thị |
| 2 | Error hiển thị | Cursor | Auto-focus vào field lỗi đầu tiên |
```

---

## 4. State × Button Test Matrix

```markdown
## State × Button Test Matrix

Sinh từ State Machine + Button Matrix trong spec:

| TC # | Current State | Button/Action | User Role | Expected Result | Priority |
|------|--------------|---------------|-----------|-----------------|----------|
| SM_001 | Nháp | Sửa | Người tạo | ✅ Form edit mở | 🔴 |
| SM_002 | Nháp | Sửa | Người khác | ❌ Button hidden | 🟡 |
| SM_003 | Nháp | Xóa | Admin | ✅ Modal xác nhận → xóa | 🔴 |
| SM_004 | Nháp | Xóa | Non-admin | ❌ Button hidden | 🟡 |
| SM_005 | Nháp | Gửi duyệt | Người tạo | ✅ Status → Chờ duyệt | 🔴 |
| SM_006 | Chờ duyệt | Duyệt | Quản lý | ✅ Status → Đã duyệt | 🔴 |
| SM_007 | Chờ duyệt | Duyệt | Non-manager | ❌ Button hidden | 🟡 |
| SM_008 | Chờ duyệt | Từ chối | Quản lý | ✅ Status → Nháp + lý do | 🔴 |
| SM_009 | Đã duyệt | Sửa | Any | ❌ Button hidden | 🔴 |
| SM_010 | Đã hủy | Any action | Any | ❌ All buttons disabled | 🟡 |
```

---

## 5. Regression Checklist

```markdown
## Regression Checklist

Sinh từ Impact Matrix — test các module bị ảnh hưởng:

| # | Module ảnh hưởng | Test Case | Priority | Auto? |
|---|-----------------|-----------|----------|-------|
| REG_001 | Tồn kho | Sau khi duyệt nhập kho → tồn kho tăng đúng SL | 🔴 | ✅ |
| REG_002 | Tồn kho | Sau khi hủy nhập kho đã duyệt → tồn kho giảm đúng SL | 🔴 | ✅ |
| REG_003 | Báo cáo | Phiếu mới hiện trong báo cáo XNK | 🟡 | ❌ |
| REG_004 | Dashboard | Counter thay đổi sau tạo/duyệt/hủy | 🟢 | ❌ |
| REG_005 | Notification | Noti gửi đúng người, đúng content | 🟡 | ❌ |
```

---

## 6. Security Test Scenarios

```markdown
## Security Test Scenarios

| # | Attack Vector | Input / Action | Expected Response | Priority |
|---|--------------|---------------|-------------------|----------|
| SEC_001 | SQL Injection | field: `'; DROP TABLE orders--` | 422 validation error, no DB impact | 🔴 |
| SEC_002 | XSS (Stored) | field: `<script>alert(1)</script>` | HTML escaped in response & UI | 🔴 |
| SEC_003 | XSS (Reflected) | URL param: `?q=<img onerror=alert(1)>` | Param sanitized | 🔴 |
| SEC_004 | RBAC Bypass | User `viewer` → POST /api/v1/{resource} | 403 Forbidden | 🔴 |
| SEC_005 | IDOR | User A → GET /api/v1/{resource}/{userB_id} | 403 or scoped query | 🔴 |
| SEC_006 | Mass Assignment | POST body with `{"role":"admin"}` | Extra fields ignored | 🟡 |
| SEC_007 | Rate Limiting | 100 requests/second to create endpoint | 429 Too Many Requests | 🟡 |
| SEC_008 | JWT Expired | Request with expired token | 401 Unauthorized | 🔴 |
| SEC_009 | CSRF | Cross-origin POST request | Rejected by CORS/CSRF token | 🟡 |
```

---

## 7. Performance Test Scenarios

```markdown
## Performance Test Scenarios

| # | Scenario | Endpoint | Load | Expected | Tool |
|---|----------|----------|------|----------|------|
| PERF_001 | List with 10K records | GET /api/v1/{resource}?page=1 | 1 user | < 500ms P95 | k6 |
| PERF_002 | List with filters | GET /api/v1/{resource}?status=draft&search=xi | 1 user | < 800ms P95 | k6 |
| PERF_003 | Concurrent create | POST /api/v1/{resource} | 50 users, 10s | < 1s P95, 0 conflicts | k6 |
| PERF_004 | Export large dataset | GET /api/v1/{resource}/export | 1 user, 50K rows | < 10s, memory < 512MB | k6 |
| PERF_005 | Dashboard aggregation | GET /api/v1/dashboard | 20 users | < 2s P95 | k6 |

### k6 Script Template
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 50,
  duration: '30s',
  thresholds: {
    http_req_duration: ['p(95)<1000'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get('http://localhost:3000/api/v1/{resource}?page=1&limit=20');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
```
```

---

## 8. Automation Skeleton (Playwright)

```markdown
## Automation Skeleton

### Setup
```typescript
// tests/{feature}.spec.ts
import { test, expect } from '@playwright/test';

test.describe('{Feature Name}', () => {
  test.beforeEach(async ({ page }) => {
    // Login
    await page.goto('/login');
    await page.fill('#username', 'admin_kho');
    await page.fill('#password', 'password');
    await page.click('#btn-login');
    await page.waitForURL('/dashboard');
  });
```

### Test Cases
```typescript
  test('TC_001: Create {resource} successfully', async ({ page }) => {
    // GIVEN - Navigate to create page
    await page.goto('/{module}/{feature}/new');
    await expect(page.locator('h1')).toContainText('Tạo mới');

    // WHEN - Fill form
    await page.fill('#field_1', 'Test value');
    await page.fill('#quantity', '100');
    await page.selectOption('#category', 'vat-lieu');
    
    // AND - Submit
    await page.click('#btn-save');

    // THEN - Verify success
    await expect(page.locator('.toast-success')).toBeVisible();
    await expect(page).toHaveURL(/{module}\/{feature}$/);
  });

  test('TC_002: Validate required fields', async ({ page }) => {
    await page.goto('/{module}/{feature}/new');
    
    // WHEN - Submit empty form
    await page.click('#btn-save');
    
    // THEN - Show validation errors
    await expect(page.locator('#field_1-error')).toContainText('bắt buộc');
    await expect(page.locator('#field_1')).toBeFocused();
  });

  test('SM_006: Approve order', async ({ page }) => {
    // GIVEN - Order in pending status (use API to create)
    const orderId = await createTestOrder({ status: 'pending' });
    await page.goto(`/{module}/{feature}/${orderId}`);
    
    // WHEN - Click approve
    await page.click('#btn-approve');
    await page.click('#btn-confirm'); // Confirm modal
    
    // THEN - Status updated
    await expect(page.locator('.status-badge')).toContainText('Đã duyệt');
  });
});
```
```

---

## 9. Requirement → Test Mapping

File: `test_mapping.md`

```markdown
# REQUIREMENT → TEST MAPPING — {Feature_ID}

## Traceability Matrix
| Requirement | Type | Spec Section | Test Cases | Coverage |
|-------------|------|-------------|------------|----------|
| BR_01: Tính tổng tiền | Business Rule | 4.2 | TC_001, TC_005 | ✅ Covered |
| BR_02: Chặn sửa khi đã duyệt | Business Rule | 4.2 | SM_009 | ✅ Covered |
| BR_03: Auto-gen mã phiếu | Business Rule | 4.2 | TC_001 | ✅ Covered |
| AC_01: Tạo phiếu thành công | Acceptance | 4.5 | TC_001 | ✅ Covered |
| AC_02: Validate required | Acceptance | 4.5 | TC_002 | ✅ Covered |
| AC_03: Approve flow | Acceptance | 4.5 | SM_006 | ✅ Covered |
| RBAC: Viewer cannot create | Security | 3.4 | SEC_004 | ✅ Covered |
| PERF: List < 500ms | NFR | NFR | PERF_001 | ✅ Covered |

## Coverage Summary
| Category | Total | Covered | Uncovered | % |
|----------|-------|---------|-----------|---|
| Business Rules | {n} | {n} | {n} | {X}% |
| Acceptance Criteria | {n} | {n} | {n} | {X}% |
| State Transitions | {n} | {n} | {n} | {X}% |
| Security | {n} | {n} | {n} | {X}% |
| Performance | {n} | {n} | {n} | {X}% |
| **Total** | **{n}** | **{n}** | **{n}** | **{X}%** |

### ⚠️ Uncovered Requirements
| Requirement | Reason | Action |
|-------------|--------|--------|
| {BR_XX} | {Lý do chưa cover} | {Cần thêm TC_XXX} |
```
