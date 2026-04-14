# Quickstart by Role — Hướng dẫn chi tiết theo vai trò

Mỗi role có workflow khác. Đọc section của vai trò mình đang làm.

---

## 👤 BA (Business Analyst) — 90% use case

### Kịch bản 1: Tạo spec từ yêu cầu mới (Mode 1)

**Trước khi bắt đầu** — chuẩn bị:

```
Feature ID:    IMS_NK_01
Feature name:  Nhập kho vật tư
Module:        inventory
Mục tiêu:      Thủ kho ghi nhận vật tư vào kho, QL duyệt
Roles:         Thủ kho, Quản lý kho, Kế toán
Luồng chính:
  1. Thủ kho tạo phiếu nhập (draft)
  2. Thủ kho submit → Quản lý duyệt
  3. Quản lý duyệt → cập nhật tồn kho
  4. Kế toán nhận thông báo
```

**Prompt:**
```
Tạo spec cho tính năng nhập kho vật tư IMS_NK_01.
- Module: inventory
- Roles: Thủ kho, QL kho, Kế toán
- Luồng: Thủ kho tạo phiếu → Submit → QL duyệt → Cập nhật tồn → Thông báo kế toán
- BR chính: vật tư hết hạn phải cảnh báo, không cho nhập nếu quá hạn
- Notification: email khi có phiếu chờ duyệt
```

**AI sẽ tạo:**
- `docs/specs/inventory/IMS_NK_01_nhap_kho/spec.md` với 4 level
- State Machine (Draft → Submitted → Approved/Rejected)
- Button Matrix (ai làm gì ở state nào)
- BR list (BR_001, BR_002, ...)
- AC BDD (Given/When/Then)
- Mermaid diagrams inline
- Gap Report ở cuối

**Verify trước khi ship:**
- ☐ Gap Report → 0 Critical 🔴
- ☐ State machine có đủ transitions
- ☐ Button Matrix match State machine
- ☐ Tất cả BR có AC cover

### Kịch bản 2: Cấu trúc meeting notes rời (Mode 2)

**Prompt:**
```
Đây là notes meeting phòng kho sáng nay, cấu trúc thành spec giúp em:

"Thủ kho mở form nhập phiếu, ghi tên vật tư, số lượng, ngày hết hạn
nếu có. Bấm lưu, phiếu vào trạng thái nháp. Sau đó submit cho Quản lý
duyệt. QL click duyệt hoặc từ chối, nếu từ chối ghi lý do. Nếu vật tư
hết hạn trong vòng 30 ngày, hệ thống cảnh báo đỏ nhưng vẫn cho nhập.
Thông báo kế toán qua email khi duyệt xong..."
```

**AI sẽ:**
1. Trích xuất roles, states, BR, notifications
2. Sinh spec giống Mode 1
3. **Đánh dấu `[⚠️ CẦN XÁC NHẬN]`** ở chỗ mơ hồ (VD: "ai gửi email? hệ thống tự hay QL click?")
4. Xuất gap report

**Sau khi nhận output:**
- Đọc các `[⚠️ CẦN XÁC NHẬN]` → confirm với stakeholder
- Chạy Mode 3 update với clarification

### Kịch bản 3: Update spec đã có (Mode 3)

**Prompt:**
```
Update spec IMS_NK_01 — thêm BR_005: Không cho nhập vật tư nếu kho đã
đầy > 90%. Cảnh báo từ 80%.
```

**AI sẽ:**
1. Đọc `docs/specs/inventory/IMS_NK_01_nhap_kho/spec.md`
2. Check scope: nếu spec Approved → tạo CR
3. Thêm BR_005 + AC_BR_005
4. Update State machine nếu cần
5. Append vào Changelog: `| 2026-04-14 | cuongbx | Thêm BR_005 | v1.1.0 |`
6. Chạy gap detection sau update

**Nếu spec đã Approved:** AI sẽ tự động tạo `CR_001` entry với:
- Type: Additive / Breaking / Nice-to-have
- Impact: backend + test
- % scope change
- Estimation delta

---

## 💻 Dev — Backend (Mode 5A)

**Sau khi có spec Approved:**

**Prompt:**
```
Tạo dev guide backend cho feature IMS_NK_01
```

**AI sẽ đọc spec, sinh `dev_guide.md` với 8 sections:**

1. **DB Schema** — migration SQL với constraints
2. **API Endpoints** — REST/gRPC signatures, request/response examples
3. **BR Implementation** — pseudo-code cho từng Business Rule
4. **State Machine guards** — function signature check transitions
5. **Validation chain** — input → sanitize → schema → BR → DB
6. **Caching** — Redis keys, TTL, invalidation triggers
7. **Concurrency** — lock patterns, transaction scopes
8. **Logging** — structured fields, log levels

**Dev workflow:**
1. Implement theo dev_guide.md
2. Mỗi BR implement xong → commit với message `feat: implement BR_001 (IMS_NK_01)`
3. Khi xong → trigger Mode 4 self-audit: *"Audit code feature IMS_NK_01"*

---

## 💻 Dev — Frontend (Mode 5B)

**Prompt:**
```
Tạo dev guide frontend cho IMS_NK_01
```

**AI sẽ sinh:**
1. **Route mapping** — URL patterns → page components
2. **Component breakdown** — tree với props, states
3. **Conditional rendering** — từ Button Matrix của spec
4. **Form validation UX** — error states, field-level vs form-level
5. **UI States** — loading, empty, error, success
6. **Accessibility** — ARIA labels, keyboard navigation
7. **Keyboard shortcuts** — cho power user
8. **Error boundaries** — scope + fallback UI

**Workflow:** Tương tự Backend — implement → self-audit → PR.

---

## 🧪 QA / Tester (Mode 6)

**Prompt:**
```
Sinh test cases cho IMS_NK_01
```

**AI sẽ sinh 3 files:**

### 1. `test_cases.md`
- **BDD format** (Given/When/Then) cho mỗi AC
- Phân loại: Happy / Negative / Edge
- Link tới BR_xxx + AC_xxx trong spec

### 2. `test_mapping.md` (Requirement → Test Matrix)
| Requirement | BR | AC | Test Cases | Automation |
|---|---|---|---|---|
| REQ_001 | BR_001 | AC_001 | TC_001, TC_002 | Playwright |

### 3. `test_execution.md`
- **Execution Dashboard** — tổng TC, PASSED/FAILED/BLOCKED/UNTESTED %
- **Execution Matrix** — mỗi TC có:
  - Checkbox `[ ]`
  - Category (Happy/Negative/Edge)
  - Priority (P0/P1/P2)
  - Status (PASSED/FAILED/BLOCKED/UNTESTED)
  - Actual result
  - Bug ID (link Jira/Linear)

**QA workflow:**
1. Nhận test_cases.md → execute manually (lần đầu)
2. Update test_execution.md với status thực tế
3. Copy bảng sang Excel/Google Sheets để báo cáo daily
4. Tự động hóa: dùng Playwright skeleton AI đã sinh

**Tips:**
- Security tests (SQL injection, XSS, RBAC, IDOR) đã có sẵn template
- Performance: k6 templates ở cuối file

---

## 📊 PM — Quản lý dự án

### Mode 7: Tóm tắt 1 trang cho họp

**Prompt:**
```
Tóm tắt feature IMS_NK_01 cho họp sáng mai
```

**AI sẽ output inline (không tạo file):**
- Feature name + ID
- Status + Owner
- Mục tiêu (1-2 câu)
- Scope metrics (story points, features count)
- Estimation vs Actual
- Risks
- Dependencies
- RACI table

### Mode 8: Dashboard tiến độ

**Prompt:**
```
Ai đang làm gì?
```
hoặc
```
Tuần này team tiến độ thế nào?
```

**AI sẽ:**
1. Đọc git log trong period
2. Đọc changelogs của specs trong `docs/specs/`
3. Sinh dashboard:
   - **Progress Matrix** — feature × status × %
   - **Recent Activity** — commits, spec updates
   - **Scope Alerts** — CR pending, spec chưa sync với code
   - **Warnings & Risks** — feature stuck >7 days, blocker

### Mode 9: Báo cáo PMO

**Prompt:**
```
Tạo sprint report tuần này
```
hoặc
```
Báo cáo PMO cho Sprint 12
```

**AI sẽ sinh:**
- **Executive Summary** — 3-5 bullets cao cấp
- **Feature Detail** — table với progress, blocker, next
- **CR Summary** — approved/rejected trong sprint
- **Risks & Blockers** — owner, mitigation
- **Next Sprint** — planned items
- **Release Notes** — user-facing changes
- **Communication Template** — email format gửi stakeholder

---

## 🎨 BA + FE Dev — Mockup (Mode 10)

**Trước khi bắt đầu** — cần spec Level 4 đã approved (có UI Spec + Button Matrix).

**Prompt:**
```
Tạo mockup cho màn đăng nhập IMS_AUTH_01
```

**AI sẽ:**
1. Đọc `docs/specs/auth/IMS_AUTH_01/spec.md` (Level 4)
2. Tạo `src/mockups/features/auth/IMS_AUTH_01_Mockup.tsx`:
   - Dùng Design System components (Button, Input, Form từ project)
   - Dummy data realistic
   - All states: default, hover, focus, error, loading, disabled
   - Form validation visual
3. Đăng ký route vào `src/mockups/MockupHub.tsx`
4. Self-verify: lỗi import/props → AI tự fix

**Sync mockup ↔ spec:**
- Khi BA sửa spec → trigger Mode 10 re-generate mockup
- Khi FE sửa mockup (prototype hơn spec) → **AI HỎI user** trước khi update `.md`

---

## 🔍 Tech Lead — Audit (Mode 4)

**Khi nào chạy:**
- Trước release candidate
- Khi nghi ngờ spec ↔ code drift
- Review PR lớn
- Preparing for audit ngoài

**Prompt:**
```
Audit feature IMS_NK_01 — spec và code có khớp không?
```

**AI sẽ:**
1. **Gap Detection** trong spec: BR↔AC, State↔Button, Field↔Validate
2. **Code-Spec Comparison**:
   - Read spec
   - Scan source code (controllers, services, models)
   - Generate **RTM** (Requirements Traceability Matrix)
   - **Deviation Report** — spec nói X nhưng code làm Y
3. **Tech Lead Review**:
   - Architecture fit
   - Performance bottlenecks
   - Security gaps
   - Tech debt indicators

**Output:**
```markdown
# Audit Report — IMS_NK_01

## Gap Detection
- ✅ BR↔AC: 12/12 mapped
- ⚠️ State↔Button: Missing "Reject" action for QL in "Submitted" state
- 🔴 Field↔Validate: `expiryDate` có BR nhưng chưa có validation trong code

## Deviation Report
- Spec: POST /warehouse-receipts validates expiry_date
- Code: Validation missing (src/controllers/warehouseReceiptController.ts:47)
- Severity: HIGH

## Action Items
1. 🔴 Add expiry_date validation
2. 🟡 Add "Reject" action handler
3. 🟢 Refactor service layer cho testability
```

---

## 💡 Tips cho mọi role

1. **Cung cấp context nhiều nhất có thể** — Feature ID, module, luồng cụ thể
2. **Trust `[⚠️ CẦN XÁC NHẬN]`** — đây là tín hiệu AI không chắc, cần clarify
3. **Gap Report luôn đọc** — đừng ship spec có Critical 🔴
4. **Changelog tự động** — không bao giờ edit tay
5. **Mockup là sandbox** — thử UI trước khi commit design
6. **Mode 4 sau Mode 1** — audit ngay sau viết spec giúp catch gap sớm
7. **Mode 8/9 automate weekly** — đỡ phải viết report thủ công

## Troubleshooting

| Issue | Solution |
|---|---|
| AI hỏi quá nhiều câu | Provide Feature ID + luồng chính ngay từ đầu |
| Output không đúng format | Check template có tồn tại trong `references/templates/` |
| Gap detection fail | Xem `references/rules/gap-detection-rules.md` |
| Mockup render lỗi | AI self-heal tự động, xem `references/patterns/ui-mockup-patterns.md` |
| Changelog entry sai | Mode 3 auto — đừng sửa tay |
| CR không generate | Spec phải có status = "Approved" trong frontmatter |
