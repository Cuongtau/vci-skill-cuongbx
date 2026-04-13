---
name: vci-skill-cuongbx
description: |
  Sinh tài liệu PRD/Spec chuẩn .md phục vụ toàn bộ team phát triển sản phẩm
  (BA, Dev, QA, Tester, PM, Tech Lead). Hỗ trợ 10 chế độ: Generate, Structure,
  Update, Audit, Dev Guide (BE/FE), Test Gen, Summary, Track, Report, Mockup.
  Dùng khi user nói "tạo spec", "viết PRD", "tạo tài liệu BA", "dev guide",
  "sinh test cases", "báo cáo tiến độ", "kiểm tra spec", "so sánh code",
  "tóm tắt feature", "scope thay đổi gì", "cập nhật spec", "UAT script",
  "tạo mockup", "mockup UI".
argument-hint: "[mode] [feature description or spec path]"
languages: all
license: MIT
metadata:
  author: cuongbx
  version: "2.0.0"
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

# Instructions

## Bước 0: Nhận diện vai trò & chế độ

Khi user kích hoạt skill, xác định **vai trò** và **chế độ**:

1. Phân tích câu hỏi → tự chọn mode phù hợp
2. Nếu không rõ → hỏi: *"Anh/chị đang ở vai trò nào? (BA / Dev / QA / PM)"*

| Trigger keywords | Mode | Vai trò |
|-----------------|------|---------|
| "tạo spec", "viết PRD", "tạo tài liệu" | **1. Generate** | BA |
| "cấu trúc lại", "có meeting notes", "ghi chú cuộc họp" | **2. Structure** | BA |
| "cập nhật spec", "sửa spec", "thêm BR" | **3. Update** | BA |
| "kiểm tra spec", "so sánh code", "audit" | **4. Audit** | BA + Dev + Tech Lead |
| "dev guide", "implement", "hướng dẫn code", "API", "DB schema" | **5. Dev Guide** | Dev |
| "test cases", "test matrix", "sinh test" | **6. Test Gen** | QA/Tester |
| "tóm tắt", "overview", "summary feature" | **7. Summary** | PM + All |
| "ai đang làm gì", "tiến độ", "status", "track" | **8. Track** | PM |
| "báo cáo PMO", "report", "sprint report" | **9. Report** | PM → PMO |
| "tạo mockup", "mockup UI", "vẽ giao diện" | **10. Mockup** | BA + FE Dev |

Điều chỉnh ngôn ngữ theo vai trò:
- **PM**: ngắn gọn, business-focused, Level 1-2
- **BA**: chuẩn template, đầy đủ Level 1-4
- **Dev**: kỹ thuật, code-centric, Level 3-4
- **QA/Tester**: test-oriented, AC-focused, Level 3-4
- **FE Dev**: tập trung UI, component, mockup

---

## Mode 1: Generate (BA → Sinh PRD mới)

📚 **Template:** `references/templates/prd-template.md`

1. Hỏi BA thông tin tối thiểu:
   - Feature ID & tên (VD: `IMS_NK_01` - Nhập kho vật tư)
   - Mục tiêu nghiệp vụ (bài toán giải quyết)
   - User chính (roles)
   - Luồng nghiệp vụ tổng quát
2. Sinh tài liệu PRD 4 level theo template:
   - **Level 1**: Product Overview (PM, BA)
   - **Level 2**: Epic/Module (Architect, PM)
   - **Level 3**: Feature Detail — User Story, State Machine, Button Matrix (Dev, QA)
   - **Level 4**: Sub-feature — UI Spec, Business Rules, Validation, API, AC (Dev, QA)
3. Tự động sinh Mermaid diagrams:
   - 📚 Mẫu: `references/patterns/mermaid-patterns.md`
   - State Machine, Screen Flow, ERD
4. Tự động thêm: Glossary, Notification Rules, Audit Trail, Risk Assessment, Data Migration Notes
5. Tạo output: `docs/specs/{module}/{Feature_ID}_{tên_snake_case}/spec.md`
   > Mermaid inline trong spec.md. Chỉ tách `diagrams.md` khi > 500 dòng.
6. Tạo/update `docs/specs/{module}/README.md` — index features
7. ✅ VERIFY: Chạy gap detection tự động
   - 📚 `references/rules/gap-detection-rules.md`
   - **AUTO-FIX** gap 🔴 Critical → bổ sung trước khi trả output

---

## Mode 2: Structure (BA → Cấu trúc hóa thông tin rời rạc)

1. Nhận input: meeting notes, Jira tickets, email, text tự do
2. Trích xuất: features, rules, roles, flows, fields, edge cases
3. Sinh PRD chuẩn template (giống Mode 1, bước 2-7)
4. Đánh dấu `[⚠️ CẦN XÁC NHẬN]` ở chỗ AI không chắc chắn
5. ✅ VERIFY: gap detection

---

## Mode 3: Update (BA → Cập nhật spec đã có)

1. Đọc spec hiện tại (user chỉ path hoặc AI tìm trong `docs/specs/`)
2. Thực hiện thay đổi theo yêu cầu
3. **Auto Changelog**: thêm dòng Lịch sử thay đổi (ngày, người, nội dung, version)
4. **Scope Change Detection** (nếu spec đã Approved):
   - So sánh Scope Baseline → tính % thay đổi
   - Nếu vượt baseline → tạo Change Request (phân loại, impact, CR Log)
5. ✅ VERIFY: gap detection sau update

---

## Mode 4: Audit (BA + Dev + Tech Lead → Kiểm tra)

📚 **Quy tắc:** `references/rules/gap-detection-rules.md`

1. Đọc spec → **Gap Detection**: BR↔AC, State↔Button, Field↔Validate, cross-feature consistency
2. **Code-Spec Comparison** (nếu Dev/Tech Lead): đọc source code → sinh RTM + Deviation Report
3. **Tech Lead Review**: architecture, performance, security, tech debt checklists
4. Output: Gap Report + action items ưu tiên

---

## Mode 5: Dev Guide (Dev → Hướng dẫn implement)

📚 **Template:** `references/templates/dev-guide-template.md`

1. Đọc spec → hỏi sub-mode: *"Backend hay Frontend?"*

**5A — Backend:** DB schema, API endpoints, BR implementation, State Machine guards, Validation chain, Caching, Concurrency, Logging

**5B — Frontend:** Route mapping, Component breakdown, Conditional rendering (từ Button Matrix), Form validation UX, UI States, a11y, Keyboard shortcuts, Error boundaries

3. Output: `docs/specs/{module}/{Feature_ID}_{tên}/dev_guide.md`

---

## Mode 6: Test Gen (QA/Tester → Sinh test)

📚 **Template:** `references/templates/test-gen-template.md`

1. Đọc spec → sinh:
   - BDD Test Cases (Given/When/Then) từ AC
   - State × Button Test Matrix
   - Regression Checklist từ Impact Matrix
   - Test Data Prerequisites
   - Security Test Scenarios (SQL injection, XSS, RBAC, IDOR)
   - Performance Test Scenarios (k6 templates)
   - Automation Skeleton (Playwright)
   - Requirement → Test Mapping
2. Output: `test_cases.md` + `test_mapping.md` trong feature folder

---

## Mode 7: Summary (PM → Tóm tắt 1 trang)

Đọc spec → sinh tóm tắt: Feature name, status, owner, mục tiêu, scope metrics, estimation, risk, dependencies, RACI. Output trực tiếp (không tạo file).

---

## Mode 8: Track (PM → Dashboard hoạt động)

📚 **Template:** `references/templates/pm-report-template.md` (Mode 8 section)

Đọc git log + spec changelogs → sinh dashboard: Progress Matrix, Recent Activity, Scope Alerts, Warnings & Risks.

---

## Mode 9: Report (PM → Báo cáo PMO)

📚 **Template:** `references/templates/pm-report-template.md` (Mode 9 section)

Thu thập git log, spec status, CR log → sinh: Executive Summary, Feature Detail, CR Summary, Risks & Blockers, Next Sprint, Release Notes, Communication Template.

---

## Mode 10: Mockup (BA / FE Dev → Code Mockup tĩnh)

📚 **Quy tắc:** `references/patterns/ui-mockup-patterns.md`

1. Đọc spec → tạo React `.tsx` tại `src/mockups/features/.../`
2. Dùng component chuẩn Design System, dummy data, đầy đủ CSS hover/form state
3. **Đồng bộ Chéo**: Mockup↔Spec — **HỎI user trước khi sửa `.md`**
4. Đăng ký route vào `MockupHub.tsx`
5. Auto-Verification: self-healing cho lỗi import/props

---

# Examples

## Ví dụ 1: BA tạo spec mới
> "Tạo spec cho tính năng nhập kho vật tư. Thủ kho tạo phiếu nhập, quản lý duyệt."

→ AI sinh spec 4 level vào `docs/specs/inventory/IMS_NK_01_nhap_kho/spec.md` với State Machine, BR, AC BDD, Button Matrix, gap report.

📚 *Xem đầy đủ: `examples/example-dispatch-order.md`*

## Ví dụ 2: Dev xin hướng dẫn
> "Tạo dev guide backend cho feature nhập kho"

→ AI đọc spec → sinh `dev_guide.md`: DB migration, API endpoints, BR pseudo-code, State Machine guards, Caching strategy.

## Ví dụ 3: PM kiểm tra tiến độ
> "Ai đang làm gì?"

→ AI đọc git log + changelogs → Dashboard: Progress Matrix, Recent Activity, Scope Alerts.

## Ví dụ 4: BA tạo Mockup
> "Tạo mockup cho màn hình đăng nhập, lấy chuẩn từ spec IMS_AUTH_01"

→ AI tạo `IMS_AUTH_01_Mockup.tsx`, đăng ký route vào MockupHub.

---

# Constraints

- 🚫 KHÔNG tự bịa dữ liệu — thiếu thông tin → hỏi user, đánh dấu `[⚠️ CẦN XÁC NHẬN]`
- 🚫 KHÔNG bỏ section template dù không có data — ghi "Chưa xác định"
- 🚫 KHÔNG hardcode API keys, passwords, tokens
- ✅ LUÔN chạy gap detection sau sinh/update spec
- ✅ LUÔN auto-fix gap 🔴 Critical trước khi trả output
- ✅ LUÔN tạo Auto TOC ở đầu `spec.md`
- ✅ LUÔN tạo output theo folder `docs/specs/{module}/{Feature_ID}_{tên}/`
- ✅ LUÔN ghi Changelog khi update spec
- ✅ LUÔN đảm bảo Notification Rules phủ hết State transitions có Side Effect
- ⚠️ Spec đã Approved mà update → PHẢI tạo CR
- ⚠️ Mermaid labels chứa ký tự đặc biệt → PHẢI quote
- ⚠️ SKILL.md reference `references/` cho chi tiết — KHÔNG copy template vào đây

<!-- Version: 2.0.0 -->
<!-- Last reviewed: 2026-04-13 -->
<!-- Powered by ClaudeKit Engineer -->
