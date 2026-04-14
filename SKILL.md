---
name: vci-skill-cuongbx
description: |
  Sinh tài liệu PRD/Spec chuẩn .md phục vụ toàn bộ team phát triển sản phẩm
  (BA, Dev, QA, Tester, PM, Tech Lead). Hỗ trợ 10 chế độ chia theo 5 vùng
  vai trò: Zone BA (Generate, Structure, Update, Audit), Zone Dev (Dev Guide
  Backend/Frontend), Zone QA (Test Gen), Zone PM (Summary, Track, Report),
  Zone Shared (Mockup UI). Dùng khi user nói "tạo spec", "viết PRD", "tạo
  tài liệu BA", "dev guide", "sinh test cases", "báo cáo tiến độ", "kiểm
  tra spec", "so sánh code", "tóm tắt feature", "scope thay đổi gì", "cập
  nhật spec", "UAT script", "tạo mockup", "mockup UI".
argument-hint: "[mode] [feature description or spec path]"
languages: all
license: MIT
metadata:
  author: cuongbx
  version: "2.1.0"
  category: documentation
  tags:
    - prd
    - spec
    - sdlc
    - ba
    - testing
    - project-management
---

# Goal

Sinh tài liệu PRD/Spec chuẩn .md trong 10 phút (thay vì 2-3 giờ), phục vụ
toàn bộ team SDLC — từ BA viết spec, Dev implement, QA test, đến PM track
progress và báo cáo PMO — đảm bảo mọi vai trò đều đọc hiểu và sử dụng được.

---

# Instructions

## Bước 0: Nhận diện Role → Zone → Mode

### Decision Tree

```
User nói gì?
│
├─ "tạo spec / viết PRD / tạo tài liệu" ────────────► 🟦 Zone BA  → Mode 1 (Generate)
├─ "có meeting notes / ghi chú rời rạc" ────────────► 🟦 Zone BA  → Mode 2 (Structure)
├─ "cập nhật spec / sửa spec / thêm BR" ────────────► 🟦 Zone BA  → Mode 3 (Update)
├─ "kiểm tra spec / so sánh code / audit" ──────────► 🟦 Zone BA  → Mode 4 (Audit)
│
├─ "dev guide / implement / API / DB schema" ───────► 🟩 Zone Dev → Mode 5 (Dev Guide)
│     └─ Hỏi sub-mode: Backend (5A) hay Frontend (5B)?
│
├─ "test cases / test matrix / sinh test / UAT" ────► 🟨 Zone QA  → Mode 6 (Test Gen)
│
├─ "tóm tắt / overview feature" ────────────────────► 🟧 Zone PM  → Mode 7 (Summary)
├─ "ai đang làm gì / tiến độ / status / track" ─────► 🟧 Zone PM  → Mode 8 (Track)
├─ "báo cáo PMO / sprint report" ───────────────────► 🟧 Zone PM  → Mode 9 (Report)
│
└─ "tạo mockup / mockup UI / vẽ giao diện" ─────────► 🟪 Zone Shared → Mode 10 (Mockup)
```

### Khi mơ hồ — Hỏi ask-back

Nếu trigger không khớp rõ bảng trên:
> *"Anh/chị đang ở vai trò nào? (BA / Dev / QA / PM / FE Dev)"*
> *"Mục tiêu cụ thể: tạo mới, cập nhật, kiểm tra, hay báo cáo?"*

### Điều chỉnh ngôn ngữ theo vai trò

| Role | Style | Level |
|------|-------|-------|
| **PM** | Ngắn gọn, business-focused | Level 1-2 |
| **BA** | Chuẩn template, đầy đủ | Level 1-4 |
| **Dev** | Kỹ thuật, code-centric | Level 3-4 |
| **QA/Tester** | Test-oriented, AC-focused | Level 3-4 |
| **FE Dev** | UI, component, mockup | Level 3-4 |

---

## 🟦 Zone BA — Business Analyst (Mode 1-4)

### Mode 1: Generate — Sinh PRD mới

📚 **Template:** `references/templates/prd-template.md`

1. Hỏi BA thông tin tối thiểu:
   - Feature ID & tên (VD: `IMS_NK_01` - Nhập kho vật tư)
   - Mục tiêu nghiệp vụ (bài toán giải quyết)
   - User chính (roles)
   - Luồng nghiệp vụ tổng quát
2. Sinh tài liệu PRD 4 level:
   - **Level 1**: Product Overview (PM, BA)
   - **Level 2**: Epic/Module (Architect, PM)
   - **Level 3**: Feature Detail — User Story, State Machine, Button Matrix (Dev, QA)
   - **Level 4**: Sub-feature — UI Spec, Business Rules, Validation, API, AC (Dev, QA)
3. Tự động sinh Mermaid diagrams (📚 `references/patterns/mermaid-patterns.md`):
   State Machine, Screen Flow, ERD
4. Tự động thêm: Glossary, Notification Rules, Audit Trail, Risk Assessment, Data Migration Notes
5. Output: `docs/specs/{module}/{Feature_ID}_{tên_snake_case}/spec.md`
   > Mermaid inline trong spec.md. Chỉ tách `diagrams.md` khi > 500 dòng.
6. Tạo/update `docs/specs/{module}/README.md` — index features
7. ✅ VERIFY: Chạy gap detection (📚 `references/rules/gap-detection-rules.md`)
   - **AUTO-FIX** gap 🔴 Critical → bổ sung trước khi trả output

### Mode 2: Structure — Cấu trúc hóa thông tin rời rạc

1. Nhận input: meeting notes, Jira tickets, email, text tự do
2. Trích xuất: features, rules, roles, flows, fields, edge cases
3. Sinh PRD chuẩn template (giống Mode 1, bước 2-7)
4. Đánh dấu `[⚠️ CẦN XÁC NHẬN]` ở chỗ AI không chắc chắn
5. ✅ VERIFY: gap detection

### Mode 3: Update — Cập nhật spec đã có

1. Đọc spec hiện tại (user chỉ path hoặc AI tìm trong `docs/specs/`)
2. Thực hiện thay đổi theo yêu cầu
3. **Auto Changelog**: thêm dòng Lịch sử thay đổi (ngày, người, nội dung, version)
4. **Scope Change Detection** (nếu spec đã Approved):
   - So sánh Scope Baseline → tính % thay đổi
   - Vượt baseline → tạo Change Request (phân loại, impact, CR Log)
5. ✅ VERIFY: gap detection sau update

### Mode 4: Audit — Kiểm tra spec & code

📚 **Quy tắc:** `references/rules/gap-detection-rules.md`

1. Đọc spec → **Gap Detection**: BR↔AC, State↔Button, Field↔Validate, cross-feature consistency
2. **Code-Spec Comparison** (nếu Dev/Tech Lead): đọc source code → sinh RTM + Deviation Report
3. **Tech Lead Review**: architecture, performance, security, tech debt checklists
4. Output: Gap Report + action items ưu tiên

---

## 🟩 Zone Dev — Developer (Mode 5)

### Mode 5: Dev Guide — Hướng dẫn implement

📚 **Template:** `references/templates/dev-guide-template.md`

Hỏi sub-mode trước: *"Backend (5A) hay Frontend (5B)?"*

**5A — Backend:**
DB schema, API endpoints, BR implementation, State Machine guards,
Validation chain, Caching, Concurrency, Logging.

**5B — Frontend:**
Route mapping, Component breakdown, Conditional rendering (từ Button
Matrix), Form validation UX, UI States, a11y, Keyboard shortcuts,
Error boundaries.

Output: `docs/specs/{module}/{Feature_ID}_{tên}/dev_guide.md`

---

## 🟨 Zone QA — Quality Assurance / Tester (Mode 6)

### Mode 6: Test Gen — Sinh test artifacts

📚 **Template:** `references/templates/test-gen-template.md`
📚 **Execution:** `references/templates/test-execution-template.md`

1. Đọc spec → sinh:
   - BDD Test Cases (Given/When/Then) từ AC
   - State × Button Test Matrix
   - Regression Checklist từ Impact Matrix
   - Test Data Prerequisites
   - Security Test Scenarios (SQL injection, XSS, RBAC, IDOR)
   - Performance Test Scenarios (k6 templates)
   - Automation Skeleton (Playwright)
   - Requirement → Test Mapping
   - **Test Execution Matrix** — checkbox, status (PASSED/FAILED/BLOCKED/UNTESTED), actual result, bug ID
2. Output: `test_cases.md` + `test_mapping.md` + `test_execution.md` trong feature folder
3. `test_execution.md` bao gồm:
   - **Execution Dashboard**: tổng TC, số PASSED/FAILED/BLOCKED/UNTESTED, tỷ lệ %
   - **Execution Matrix**: mỗi TC có checkbox `[ ]`, phân loại (Happy/Negative/Edge), priority, status, actual result
   - QA có thể copy bảng sang Excel/Google Sheets để báo cáo

---

## 🟧 Zone PM — Project Manager (Mode 7-9)

### Mode 7: Summary — Tóm tắt 1 trang

Đọc spec → sinh tóm tắt: Feature name, status, owner, mục tiêu, scope metrics,
estimation, risk, dependencies, RACI. **Output trực tiếp (không tạo file).**

### Mode 8: Track — Dashboard hoạt động

📚 **Template:** `references/templates/pm-report-template.md` (Mode 8 section)

Đọc git log + spec changelogs → sinh dashboard: Progress Matrix, Recent
Activity, Scope Alerts, Warnings & Risks.

### Mode 9: Report — Báo cáo PMO

📚 **Template:** `references/templates/pm-report-template.md` (Mode 9 section)

Thu thập git log, spec status, CR log → sinh: Executive Summary, Feature
Detail, CR Summary, Risks & Blockers, Next Sprint, Release Notes,
Communication Template.

---

## 🟪 Zone Shared — BA + FE Dev (Mode 10)

### Mode 10: Mockup — Code Mockup tĩnh

📚 **Quy tắc:** `references/patterns/ui-mockup-patterns.md`

1. Đọc spec → tạo React `.tsx` tại `src/mockups/features/.../`
2. Dùng component chuẩn Design System, dummy data, đầy đủ CSS hover/form state
3. **Đồng bộ Chéo**: Mockup↔Spec — **HỎI user trước khi sửa `.md`**
4. Đăng ký route vào `MockupHub.tsx`
5. Auto-Verification: self-healing cho lỗi import/props

---

# Examples

## 🟦 Zone BA

### Ví dụ 1 — Mode 1 Generate: BA tạo spec mới
> *"Tạo spec cho tính năng nhập kho vật tư. Thủ kho tạo phiếu nhập, quản lý duyệt."*

→ AI sinh `docs/specs/inventory/IMS_NK_01_nhap_kho/spec.md` với 4 level,
State Machine, BR, AC BDD, Button Matrix, gap report.
📚 *Chi tiết: `examples/example-dispatch-order.md`*

### Ví dụ 2 — Mode 2 Structure: BA có meeting notes rời
> *"Đây là notes meeting phòng kho, cấu trúc giúp em:
> 'Thủ kho nhập phiếu, ghi loại vật tư, số lượng. Quản lý duyệt. Nếu vật tư hết hạn thì cảnh báo...'"*

→ AI trích xuất roles (Thủ kho, Quản lý), states (Draft → Submitted → Approved),
BR (cảnh báo hết hạn), sinh PRD 4 level + `[⚠️ CẦN XÁC NHẬN]` ở chỗ mơ hồ.

### Ví dụ 3 — Mode 4 Audit: Tech Lead kiểm tra spec ↔ code
> *"Audit feature IMS_NK_01 — spec và code có khớp không?"*

→ AI đọc `spec.md` + source code → sinh RTM + Deviation Report:
"⚠️ Endpoint `POST /warehouse-receipts` thiếu validation `BR_003` (kiểm tra hạn sử dụng)".

## 🟩 Zone Dev

### Ví dụ 4 — Mode 5A Backend: Dev xin hướng dẫn
> *"Tạo dev guide backend cho feature nhập kho"*

→ AI đọc spec → sinh `dev_guide.md`: DB migration, API endpoints, BR
pseudo-code, State Machine guards, Caching strategy, Logging contract.

## 🟨 Zone QA

### Ví dụ 5 — Mode 6 Test Gen: QA sinh test
> *"Sinh test cases cho IMS_NK_01"*

→ AI sinh 3 file: `test_cases.md` (BDD 25 cases), `test_mapping.md` (RTM),
`test_execution.md` (checkbox matrix với status/priority/actual result).

## 🟧 Zone PM

### Ví dụ 6 — Mode 8 Track: PM hỏi tiến độ
> *"Ai đang làm gì?"*

→ AI đọc git log + changelogs → Dashboard:

| Feature | Owner | Status | Progress | Last Update |
|---------|-------|--------|----------|-------------|
| IMS_NK_01 | @dev_a | In Progress | 60% | 2d ago |
| IMS_XK_02 | @dev_b | Review | 90% | 1d ago |

### Ví dụ 7 — Mode 9 Report: PM báo cáo PMO
> *"Tạo sprint report tuần này"*

→ AI thu thập git log + CR log → sinh Executive Summary, Feature Detail,
CR Summary, Risks & Blockers, Release Notes.

## 🟪 Zone Shared

### Ví dụ 8 — Mode 10 Mockup: BA tạo mockup UI
> *"Tạo mockup cho màn hình đăng nhập, lấy chuẩn từ spec IMS_AUTH_01"*

→ AI tạo `src/mockups/features/auth/IMS_AUTH_01_Mockup.tsx` (Design System
components, dummy data, form state), đăng ký route vào `MockupHub.tsx`.

---

# Constraints

## Không được vi phạm

- 🚫 KHÔNG tự bịa dữ liệu — thiếu thông tin → hỏi user, đánh dấu `[⚠️ CẦN XÁC NHẬN]`
- 🚫 KHÔNG bỏ section template dù không có data — ghi "Chưa xác định"
- 🚫 KHÔNG hardcode API keys, passwords, tokens
- 🚫 KHÔNG auto-update spec `.md` khi user chỉ sửa mockup `.tsx` (Mode 10) — PHẢI hỏi

## Luôn luôn làm

- ✅ LUÔN chạy gap detection sau sinh/update spec (Mode 1, 2, 3)
- ✅ LUÔN auto-fix gap 🔴 Critical trước khi trả output
- ✅ LUÔN tạo Auto TOC ở đầu `spec.md`
- ✅ LUÔN tạo output theo folder `docs/specs/{module}/{Feature_ID}_{tên}/`
- ✅ LUÔN ghi Changelog khi update spec (Mode 3)
- ✅ LUÔN đảm bảo Notification Rules phủ hết State transitions có Side Effect

## Cảnh báo

- ⚠️ Spec đã Approved mà update → PHẢI tạo Change Request (Mode 3)
- ⚠️ Mermaid labels chứa ký tự đặc biệt → PHẢI quote: `"Node's Label"`
- ⚠️ SKILL.md reference `references/` cho chi tiết — KHÔNG copy template vào đây

<!-- Version: 2.1.0 -->
<!-- Last reviewed: 2026-04-14 -->
<!-- Generated by Skill Creator Ultra v1.0 -->
