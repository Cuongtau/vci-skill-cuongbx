# Dev Guide Template

Template cho AI khi sinh Dev Guide (Mode 5). Bao gồm cả Backend và Frontend
sub-templates, đảm bảo 10/10 cho Dev roles.

---

## Cấu trúc output

File: `docs/specs/{module}/{Feature_ID}_{tên}/dev_guide.md`

```markdown
# DEV GUIDE — {Feature_ID}: {Tên tính năng}

> Auto-generated from spec `{spec_path}`
> Generated: {DD/MM/YYYY}
> Spec Version: {version}
```

---

## 5A — BACKEND DEV GUIDE

### 1. DB Schema & Migration

```markdown
## 1. DB Schema & Migration

### New Tables
| Table | Description |
|-------|-------------|
| `{table_name}` | {mô tả} |

### Schema Detail
| Column | Type | Nullable | Default | Index | Note |
|--------|------|----------|---------|-------|------|
| `id` | UUID | NO | gen_random_uuid() | PK | |
| `code` | VARCHAR(50) | NO | | UNIQUE | Auto-gen: {pattern} |
| `status` | ENUM | NO | 'draft' | INDEX | Values: draft, pending, approved, cancelled |
| `version` | INT | NO | 1 | | Optimistic lock |
| `created_at` | TIMESTAMP | NO | now() | INDEX | |
| `updated_at` | TIMESTAMP | NO | now() | | |
| `created_by` | UUID | NO | | FK → users.id | |

### Migration Script
```sql
-- UP
CREATE TABLE {table_name} (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    -- ... columns
    version INT NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_{table}_status ON {table_name}(status);
CREATE INDEX idx_{table}_created ON {table_name}(created_at);

-- DOWN (Rollback)
DROP TABLE IF EXISTS {table_name};
```

### ALTER TABLE (nếu sửa table hiện có)
```sql
-- UP
ALTER TABLE {table} ADD COLUMN {column} {type} {constraint};
CREATE INDEX idx_{table}_{column} ON {table}({column});

-- DOWN
ALTER TABLE {table} DROP COLUMN {column};
```
```

---

### 2. API Endpoints

```markdown
## 2. API Endpoints

### Endpoint List
| # | Method | Path | Auth | Description | Spec Ref |
|---|--------|------|------|-------------|----------|
| 1 | GET | /api/v1/{resource} | JWT + RBAC | Danh sách (paginated) | 4.4 |
| 2 | GET | /api/v1/{resource}/:id | JWT + RBAC | Chi tiết | 4.4 |
| 3 | POST | /api/v1/{resource} | JWT + RBAC | Tạo mới | 4.4 |
| 4 | PUT | /api/v1/{resource}/:id | JWT + RBAC | Cập nhật | 4.4 |
| 5 | PATCH | /api/v1/{resource}/:id/status | JWT + RBAC | Chuyển trạng thái | 4.4 |
| 6 | DELETE | /api/v1/{resource}/:id | JWT + Admin | Xóa (soft delete) | 4.4 |

### Request/Response Detail

#### POST /api/v1/{resource}
**Request Body:**
```json
{
  "field_1": "string (required, max 255)",
  "field_2": "number (required, > 0)",
  "items": [{
    "product_id": "uuid (required)",
    "quantity": "integer (required, > 0)",
    "unit_price": "decimal (required, >= 0)"
  }]
}
```

**Success Response:** `201 Created`
```json
{
  "data": {
    "id": "uuid",
    "code": "IMP-2024-001",
    "status": "draft",
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

**Error Responses:**
| HTTP | Error Code | Condition | Message |
|------|-----------|-----------|---------|
| 400 | VALIDATION_ERROR | Field validation fail | `{field}: {message}` |
| 403 | FORBIDDEN | Không đủ quyền | "Bạn không có quyền thực hiện thao tác này" |
| 404 | NOT_FOUND | Resource không tồn tại | "{Resource} không tồn tại" |
| 409 | DUPLICATE_CODE | Mã trùng | "Mã {code} đã tồn tại" |
| 409 | CONFLICT | Optimistic lock fail | "Dữ liệu đã bị thay đổi, vui lòng tải lại" |
| 422 | BUSINESS_RULE_VIOLATION | BR check fail | "{mô tả lỗi nghiệp vụ}" |
```

---

### 3. Business Rule Implementation

```markdown
## 3. Business Rule Implementation

### BR_{ID}: {Tên rule}
**Spec ref:** Section 4.2
**Logic:**
```typescript
// Service layer
async function applyBR_{ID}(input: CreateDTO): Promise<void> {
  // Step 1: Validate precondition
  if (!condition) {
    throw new BusinessRuleError('BR_{ID}', 'Message');
  }
  // Step 2: Calculate
  const result = field_a * field_b * (1 + vat_rate);
  // Step 3: Side effects
  await this.stockService.updateQuantity(product_id, quantity);
}
```

### Validation Chain (thứ tự validate)
| Order | Type | Check | Error |
|-------|------|-------|-------|
| 1 | Field | Required fields present | 400 VALIDATION_ERROR |
| 2 | Field | Type + format (email, phone) | 400 VALIDATION_ERROR |
| 3 | Cross-field | date_from <= date_to | 422 CROSS_FIELD |
| 4 | Business Rule | Stock >= requested quantity | 422 BUSINESS_RULE |
| 5 | Async | Unique code check (DB) | 409 DUPLICATE |
| 6 | Permission | Role + status check | 403 FORBIDDEN |
```

---

### 4. State Machine Guards

```markdown
## 4. State Machine & Guards

### Transition Guards
| From | To | Guard Logic | Side Effects |
|------|----|-------------|-------------|
| draft | pending | `createdBy === currentUser` | Notify approver |
| pending | approved | `user.role in ['manager', 'admin']` | Update stock, Emit `order.approved` |
| pending | draft | `user.role in ['manager', 'admin']` | Notify creator with reason |
| approved | cancelled | `user.role === 'admin'` AND `hasNoChildren` | Reverse stock, Emit `order.cancelled` |

### Guard Implementation
```typescript
// State machine guard middleware
function canTransition(entity: Entity, targetStatus: Status, user: User): boolean {
  const transitions: TransitionMap = {
    'draft→pending': () => entity.createdBy === user.id,
    'pending→approved': () => ['manager', 'admin'].includes(user.role),
    // ...
  };
  const key = `${entity.status}→${targetStatus}`;
  return transitions[key]?.() ?? false;
}
```
```

---

### 5. Caching Strategy

```markdown
## 5. Caching Strategy

| Endpoint | Cache? | Strategy | TTL | Invalidate When |
|----------|--------|----------|-----|-----------------|
| GET /api/v1/{resource} (list) | ❌ No | - | - | Data thay đổi liên tục |
| GET /api/v1/{resource}/:id | ✅ HTTP ETag | `If-None-Match` | - | Entity updated |
| GET /api/v1/categories | ✅ Redis | Key: `categories:all` | 1h | Category CRUD |
| GET /api/v1/lookup/{type} | ✅ Redis | Key: `lookup:{type}` | 24h | Lookup updated |

### Cache Implementation Notes
- Redis key pattern: `{service}:{entity}:{id_or_filter_hash}`
- Cache invalidation: Pub/Sub hoặc event-driven
- Cache warming: Chạy sau deploy cho lookup tables
```

---

### 6. Events & Side Effects

```markdown
## 6. Events & Side Effects

| Trigger | Event Name | Consumers | Async? | Payload |
|---------|-----------|-----------|--------|---------|
| Tạo phiếu | `{resource}.created` | AuditService | ✅ Queue | `{ id, code, createdBy }` |
| Gửi duyệt | `{resource}.submitted` | NotificationService | ✅ Queue | `{ id, code, approvers[] }` |
| Duyệt | `{resource}.approved` | StockService, NotificationService, AuditService | ✅ Queue | `{ id, code, approvedBy, items[] }` |
| Từ chối | `{resource}.rejected` | NotificationService | ✅ Queue | `{ id, code, reason, rejectedBy }` |
| Hủy | `{resource}.cancelled` | StockService, AuditService | ✅ Queue | `{ id, reversalItems[] }` |
```

---

### 7. Concurrency & Locking

```markdown
## 7. Concurrency & Locking

| Scenario | Strategy | Implementation |
|----------|----------|----------------|
| 2 users update same record | Optimistic Lock | `version` column + `WHERE version = :current` → 409 if mismatch |
| 2 users approve same order | Optimistic Lock | Check status before UPDATE → 409 if already changed |
| Stock deduction race condition | Pessimistic Lock | `SELECT ... FOR UPDATE` on stock row during transaction |
| Concurrent code generation | Application Lock | Redis distributed lock `SETNX lock:{entity}:{id}` TTL 30s |

### Optimistic Lock Pattern
```typescript
async function updateWithLock(id: string, dto: UpdateDTO, currentVersion: number) {
  const result = await db.query(
    `UPDATE {table} SET ..., version = version + 1 
     WHERE id = $1 AND version = $2
     RETURNING *`,
    [id, currentVersion]
  );
  if (result.rowCount === 0) {
    throw new ConflictError('Dữ liệu đã bị thay đổi, vui lòng tải lại');
  }
  return result.rows[0];
}
```
```

---

### 8. Logging Standards

```markdown
## 8. Logging Standards

| Level | When | Template | Example |
|-------|------|----------|---------|
| ERROR | Exception, unexpected failure | `[{Service}] Failed to {action}: {error} | userId={} entityId={}` | `[OrderService] Failed to create: DB connection timeout | userId=abc orderId=xyz` |
| WARN | Validation fail, business rule block | `[{Service}] {Rule} blocked: {reason} | context={}` | `[OrderService] Stock insufficient: requested=100 available=50` |
| INFO | State change, CRUD success | `[{Service}] {Entity} {id} {action} by {userId}` | `[OrderService] Order IMP-001 status: draft → approved by user123` |
| DEBUG | Query, cache hit/miss, detailed trace | `[{Service}] {operation}: {detail}` | `[OrderService] Cache miss: order:abc, fetching from DB` |

### Structured Logging Fields
```json
{
  "timestamp": "ISO8601",
  "level": "INFO",
  "service": "OrderService",
  "action": "status_change",
  "entityType": "import_order",
  "entityId": "uuid",
  "userId": "uuid",
  "metadata": { "from": "draft", "to": "approved" },
  "traceId": "uuid"
}
```
```

---

## 5B — FRONTEND DEV GUIDE

### 1. Route & Navigation

```markdown
## 1. Route & Navigation

### Routes
| Path | Component | Menu | Breadcrumb | Auth |
|------|-----------|------|-----------|------|
| /{module}/{feature} | {Feature}ListPage | ✅ | Home > {Module} > {Feature} | `view_{feature}` |
| /{module}/{feature}/new | {Feature}CreatePage | ❌ | Home > ... > Tạo mới | `create_{feature}` |
| /{module}/{feature}/:id | {Feature}DetailPage | ❌ | Home > ... > {code} | `view_{feature}` |
| /{module}/{feature}/:id/edit | {Feature}EditPage | ❌ | Home > ... > Chỉnh sửa | `edit_{feature}` |
```

---

### 2. Component Breakdown

```markdown
## 2. Component Breakdown

### Component Tree
```
{Feature}ListPage
├── PageHeader (title + action buttons)
├── FilterToolbar
│   ├── StatusFilter (multi-select)
│   ├── DateRangeFilter
│   └── SearchInput
├── DataTable
│   ├── TableHeader (sortable columns)
│   ├── TableRow × N
│   │   ├── StatusBadge
│   │   └── ActionDropdown
│   └── Pagination
└── DeleteConfirmModal
```

### Component Responsibilities
| Component | Props | State | API Calls |
|-----------|-------|-------|-----------|
| `{Feature}ListPage` | - | filters, data, loading | GET list |
| `{Feature}Form` | mode: create/edit, data? | formState, errors | POST/PUT |
| `StatusBadge` | status: enum | - | - |
| `ActionDropdown` | entity, onAction | - | - |
```

---

### 3. Conditional Rendering (from Button Matrix)

```markdown
## 3. Conditional Rendering

### Button Visibility Logic
```typescript
const buttonConfig = {
  edit: {
    visible: (entity, user) => 
      entity.status === 'draft' && 
      (entity.createdBy === user.id || user.role === 'admin'),
    label: 'Chỉnh sửa',
    variant: 'outline',
  },
  submit: {
    visible: (entity, user) => 
      entity.status === 'draft' && 
      entity.createdBy === user.id,
    label: 'Gửi duyệt',
    variant: 'primary',
    confirm: 'Bạn có chắc muốn gửi duyệt phiếu này?',
  },
  approve: {
    visible: (entity, user) => 
      entity.status === 'pending' && 
      ['manager', 'admin'].includes(user.role),
    label: 'Phê duyệt',
    variant: 'success',
  },
  // ... derived from Button Matrix in spec
};
```
```

---

### 4. Form Validation UX

```markdown
## 4. Form Validation UX

### Validation Rules (derived from spec Field Mapping)
| Field | Rules | Error Message | Display |
|-------|-------|---------------|---------|
| `code` | required, max(50), unique | "Mã phiếu là bắt buộc" / "Mã đã tồn tại" | inline |
| `quantity` | required, integer, min(1) | "Số lượng phải > 0" | inline |
| `date` | required, date, >= today | "Ngày không được trong quá khứ" | inline |

### Validation UX Pattern
- **Trigger**: On blur (field-level), on submit (form-level)
- **Display**: Inline error below field, red border
- **Toast**: Only for server errors (409, 422, 500)
- **Focus**: Auto-focus first error field on submit
- **Cross-field**: Validate on change of dependent field
```

---

### 5. UI States

```markdown
## 5. UI States

| State | Trigger | UI |
|-------|---------|-----|
| Loading | API call in progress | Skeleton layout (not spinner) |
| Empty | List returns 0 items | Empty state illustration + CTA "Tạo mới" |
| Error | API 5xx or network fail | Error banner + "Thử lại" button |
| Success | CRUD success | Toast notification (auto-dismiss 3s) |
| Submitting | Form submit in progress | Button disabled + loading spinner |
| Partial | Some items loaded, more available | "Xem thêm" or infinite scroll |

### Skeleton Layout
- Match actual layout structure (not generic spinner)
- Animate with pulse (shimmer effect)
- Show for minimum 300ms to avoid flash
```

---

### 6. Accessibility (a11y)

```markdown
## 6. Accessibility (a11y)

| Component | Requirement |
|-----------|-------------|
| Form fields | `aria-label`, `aria-required="true"`, error linked via `aria-describedby` |
| Status badge | Không chỉ dùng màu → thêm text + icon (🟢 Đã duyệt, 🔴 Đã hủy) |
| Action buttons | `aria-disabled` when disabled, `title` tooltip mô tả action |
| Data table | `role="grid"`, `aria-sort` cho sortable columns |
| Modals | `aria-modal="true"`, focus trap, ESC to close |
| Toast | `role="alert"`, `aria-live="polite"` |
| Loading | `aria-busy="true"` on container |
```

---

### 7. Keyboard Shortcuts

```markdown
## 7. Keyboard Shortcuts

| Shortcut | Action | Screen | Implementation |
|----------|--------|--------|----------------|
| `Ctrl+S` | Lưu nháp | Form tạo/sửa | `useHotkeys('ctrl+s', save)` |
| `Ctrl+Enter` | Submit (Gửi duyệt) | Form tạo | `useHotkeys('ctrl+enter', submit)` |
| `Esc` | Đóng modal / Cancel | Mọi modal | Built-in modal handler |
| `Tab / Shift+Tab` | Di chuyển giữa fields | Form | Native browser |
| `Enter` | Mở chi tiết row | Danh sách | Row click handler |
| `/` | Focus search | Danh sách | `useHotkeys('/', focusSearch)` |
```

---

### 8. Error Boundaries

```markdown
## 8. Error Boundaries

| Component Scope | Fallback UI | Recovery |
|----------------|-------------|----------|
| Page-level | "Trang gặp lỗi. [Tải lại trang]" | `window.location.reload()` |
| Table/List | "Không thể hiển thị danh sách. [Thử lại]" | Re-fetch data |
| Form | "Có lỗi xảy ra. Dữ liệu đã nhập được lưu tạm. [Thử lại]" | Restore from localStorage |
| Widget/Card | "Lỗi hiển thị. [Ẩn]" | Remove widget |

### Implementation
```typescript
<ErrorBoundary fallback={<ErrorFallback onRetry={refetch} />}>
  <DataTable data={data} />
</ErrorBoundary>
```
```
