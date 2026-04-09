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
| "tạo spec", "viết PRD", "tạo tài liệu" | **Generate** | BA |
| "cấu trúc lại", "có meeting notes", "ghi chú cuộc họp" | **Structure** | BA |
| "cập nhật spec", "sửa spec", "thêm BR" | **Update** | BA |
| "kiểm tra spec", "so sánh code", "audit" | **Audit** | BA + Dev + Tech Lead |
| "dev guide", "implement", "hướng dẫn code", "API", "DB schema" | **Dev Guide** | Dev |
| "test cases", "test matrix", "sinh test" | **Test Gen** | QA/Tester |
| "tóm tắt", "overview", "summary feature" | **Summary** | PM + All |
| "ai đang làm gì", "tiến độ", "status", "track" | **Track** | PM |
| "báo cáo PMO", "report", "sprint report" | **Report** | PM → PMO |
| "tạo mockup", "mockup UI", "vẽ giao diện" | **Mockup** | BA + FE Dev |

Điều chỉnh ngôn ngữ theo vai trò:
- **PM**: ngắn gọn, business-focused, Level 1-2
- **BA**: chuẩn template, đầy đủ Level 1-4
- **Dev**: kỹ thuật, code-centric, Level 3-4
- **QA/Tester**: test-oriented, AC-focused, Level 3-4
- **FE Dev**: tập trung UI, component, mockup |

---

## Mode 1: Generate (BA → Sinh PRD mới)

📚 **Template chi tiết:** `resources/prd_template.md`

1. Hỏi BA thông tin tối thiểu:
   - Feature ID & tên (VD: `IMS_NK_01` - Nhập kho vật tư)
   - Mục tiêu nghiệp vụ (bài toán giải quyết)
   - User chính (roles)
   - Luồng nghiệp vụ tổng quát
2. Sinh tài liệu PRD 4 level theo template `resources/prd_template.md`:
   - **Level 1**: Product Overview (PM, BA)
   - **Level 2**: Epic/Module (Architect, PM)
   - **Level 3**: Feature Detail — User Story, State Machine, Button Matrix (Dev, QA)
   - **Level 4**: Sub-feature — UI Spec, Business Rules, Validation, API, AC (Dev, QA)
3. Tự động sinh Mermaid diagrams:
   - 📚 Sử dụng mẫu từ `resources/mermaid_patterns.md`
   - State Machine diagram cho vòng đời trạng thái
   - Screen Flow diagram cho navigation
   - ERD cho data model
4. Tự động thêm các section bonus:
   - Glossary (từ điển nghiệp vụ)
   - Notification Rules (ai nhận noti khi nào)
   - Audit Trail (action nào cần log)
   - Risk Assessment + Estimation Hints
   - Data Migration Notes (nếu ảnh hưởng DB hiện có)
   - Review Status: `Draft`
5. Tạo output theo cấu trúc folder:
   ```
   docs/specs/{module}/{Feature_ID}_{tên_snake_case}/
   ├── spec.md          ← Tài liệu PRD chính (có Auto TOC + Mermaid inline)
   └── diagrams.md      ← (Optional) Tách riêng nếu spec > 500 dòng
   ```
   > **Lưu ý:** Mermaid diagrams ĐƯỢC PHÉP nhúng trực tiếp trong `spec.md`.
   > Chỉ tách `diagrams.md` riêng khi spec quá dài (> 500 dòng).
6. Tạo/update `docs/specs/{module}/README.md` — index features
7. ✅ VERIFY: Chạy gap detection tự động
   - 📚 `resources/gap_detection_rules.md`
   - Báo cáo nếu: BR không có AC, State không có Button, Field không có Validate
   - **AUTO-FIX**: Nếu phát hiện gap 🔴 Critical → tự bổ sung ngay vào spec
     trước khi trả output cho user. Chỉ báo cáo gap 🟡 Warning và 🟢 Info.

---

## Mode 2: Structure (BA → Cấu trúc hóa thông tin rời rạc)

1. Nhận input: meeting notes, Jira tickets, email, hoặc text tự do
2. Trích xuất: features, rules, roles, flows, fields, edge cases
3. Sinh PRD chuẩn template (giống Mode 1, bước 2-7)
4. Đánh dấu `[⚠️ CẦN XÁC NHẬN]` ở những chỗ AI không chắc chắn
5. ✅ VERIFY: gap detection

---

## Mode 3: Update (BA → Cập nhật spec đã có)

1. Đọc spec hiện tại (user chỉ đường dẫn hoặc AI tìm trong `docs/specs/`)
2. Thực hiện thay đổi theo yêu cầu BA
3. **Auto Changelog**: Thêm dòng mới vào bảng Lịch sử thay đổi
   - Ngày: lấy ngày hiện tại
   - Người: đọc từ `git config user.name`, nếu không có → hỏi
   - Nội dung: AI tóm tắt thay đổi
   - Version: tự tăng (minor cho thêm section, patch cho sửa nhỏ)
4. **Scope Change Detection** (nếu spec đã Approved):
   - So sánh với Scope Baseline → tính % thay đổi
   - Nếu vượt baseline → tự tạo Change Request:
     - Phân loại: 🔵 Khách hàng / 🟡 Nội bộ / 🟢 Bug fix
     - Tính impact: effort (MD), risk, modules ảnh hưởng
   - Ghi vào CR Log trong spec
5. ✅ VERIFY: gap detection sau update

---

## Mode 4: Audit (BA + Dev + Tech Lead → Kiểm tra)

📚 **Quy tắc chi tiết:** `resources/gap_detection_rules.md`

1. Đọc spec (user chỉ file hoặc feature ID)
2. **Gap Detection** — kiểm tra thiếu sót:
   - Mỗi Business Rule có AC tương ứng?
   - Mỗi State có Button Matrix?
   - Mỗi Field có Validation?
   - Cross-feature consistency (cùng entity nhưng mô tả khác nhau?)
3. **Code-Spec Comparison** (nếu user yêu cầu hoặc là Dev/Tech Lead):
   - Đọc source code liên quan (user chỉ folder hoặc AI tìm theo API endpoints)
   - So sánh: code implement đúng spec chưa?
   - Sinh Requirement Traceability Matrix (RTM): BR → AC → Code → Test → Status
4. **Tech Lead Review** (nếu vai trò Tech Lead):
   - Architecture review checklist
   - Performance checklist (pagination, cache, index)
   - Security review (input sanitize, RBAC, SQL injection)
   - Tech debt flags
5. Output: Gap Report + danh sách action items ưu tiên

---

## Mode 5: Dev Guide (Dev → Hướng dẫn implement)

📚 **Template chi tiết:** `resources/dev_guide_template.md`

1. Đọc spec liên quan (tìm trong `docs/specs/` hoặc user chỉ)
2. Hỏi sub-mode: *"Anh là Backend hay Frontend?"* (nếu chưa rõ)

**5A — Backend Dev Guide:**
   - DB schema suggestion + migration notes (ALTER, INDEX)
   - API endpoints + error codes + HTTP status
   - Business Rule implementation (pseudo-code)
   - State Machine guards + side effects (events)
   - Validation chain (field → cross-field → BR → async)
   - Caching strategy per endpoint
   - Concurrency/Locking guidance
   - Logging standards per level

**5B — Frontend Dev Guide:**
   - Route mapping + breadcrumb
   - Component breakdown (component tree)
   - Conditional rendering rules (JavaScript logic từ Button Matrix)
   - Form validation UX (inline/toast, error messages)
   - UI States (loading, empty, error, success)
   - Accessibility (a11y) requirements
   - Keyboard shortcuts

3. Output: `dev_guide.md` trong feature folder

---

## Mode 6: Test Gen (QA/Tester → Sinh test)

📚 **Template chi tiết:** `resources/test_gen_template.md`

1. Đọc spec liên quan
2. Sinh từ Acceptance Criteria → **BDD Test Cases** (Given/When/Then)
3. Sinh từ State Machine × Button Matrix → **Test Matrix**
4. Sinh từ Impact Matrix → **Regression Checklist**
5. Sinh **Test Data Prerequisites** (data cần seed trước khi test)
6. Sinh **Security Test Scenarios** (SQL injection, XSS, RBAC bypass)
7. Sinh **Performance Test Scenarios**
8. Sinh **Automation Skeleton** (Playwright/Cypress template code)
9. Sinh **Requirement → Test Mapping** table
10. Output: `test_cases.md` + `test_mapping.md` trong feature folder

---

## Mode 7: Summary (PM → Tóm tắt 1 trang)

1. Đọc spec liên quan
2. Sinh tóm tắt 1 trang:
   - Feature name + status + owner
   - Mục tiêu nghiệp vụ (2-3 câu)
   - Scope: số BR, AC, API, States
   - Estimation (S/M/L/XL)
   - Risk Assessment
   - Dependencies + affected modules
   - Stakeholder/RACI map
3. Output: hiển thị trực tiếp (không tạo file riêng)

---

## Mode 8: Track (PM → Dashboard hoạt động)

1. Đọc git log (`git log --oneline --since="1 week ago"`)
2. Đọc spec changelogs trong `docs/specs/`
3. Scan feature folders → tính progress
4. Sinh dashboard:
   - **Progress Matrix**: feature nào có spec/dev_guide/test_cases/code
   - **Recent Activity**: ai commit gì, ai sửa spec gì
   - **Scope Alerts**: feature nào scope tăng, CR nào chưa approve
   - **Warnings**: feature approved lâu nhưng chưa code, test fail

---

## Mode 9: Report (PM → Báo cáo PMO)

📚 **Template chi tiết:** `resources/pm_report_template.md`

1. Thu thập data: git log, spec status, CR log, test results
2. Sinh báo cáo PMO:
   - Tổng quan tiến độ (% features hoàn thành)
   - Chi tiết từng feature (owner, progress, risk)
   - Change Request Summary (tổng CR, % từ khách hàng, impact)
   - Risks & Blockers
   - Kế hoạch tuần/sprint tới
   - Release Notes (nếu có feature done)
   - Release Communication template

---

## Mode 10: Mockup (BA / FE Dev → Tạo Code Mockup tĩnh)

📚 **Quy tắc chi tiết:** `ui-mockup.md`

1. Đọc nội dung spec liên quan (nếu có).
2. Tạo/Sửa Code React (`.tsx`) ở `src/mockups/features/.../` với cấu trúc tương ứng từ `docs/features/.../` để sinh giao diện tĩnh.
3. **KHÔNG Gắn Logic phức tạp**: Dùng dummy text, mock data. Nhưng phải có đủ CSS hover, form state. Sử dụng component chuẩn từ thông tin workflow design system.
4. **Đồng bộ Chéo**:
   - Nếu đổi Mockup UI làm lệch Spec → Cảnh báo BA, **HỎI trước khi sửa `.md`**.
   - Nếu đổi Spec làm lệch Mockup UI → Báo hiệu Mockup hiện đang outdate, gợi ý update `.tsx`.
   - **Tối Kỵ**: KHÔNG TỰ Ý ghi file `.md` khi cập nhật `.tsx` mà chưa có sự đồng ý của User.
5. Cập nhật Router: Ghi nhận lazy load và route tại `src/mockups/MockupHub.tsx`.
6. Tự động kiểm tra Lỗi (`Self-Healing`): Khi lưu component `.tsx` mới nếu gặp lỗi import hay thiếu props, AI tự tìm code gốc để xử lý.
7. Khi BA đồng ý, cập nhật `.md` thêm mục `## Liên kết Mockup & Lịch sử cập nhật`.

---

# Examples

## Ví dụ 1: BA tạo spec mới (Generate Mode)

**Input:**
> "Tạo spec cho tính năng nhập kho vật tư. Thủ kho tạo phiếu nhập, quản lý
> duyệt. Cần track số lượng, đơn giá, VAT."

**Output:** AI sinh spec đầy đủ 4 level vào `docs/specs/inventory/IMS_NK_01_nhap_kho/spec.md`,
bao gồm State Machine (Nháp → Chờ duyệt → Đã duyệt), Business Rules (BR_01 tính tổng tiền),
Acceptance Criteria BDD, Button Matrix, và gap report cuối cùng.

📚 *Xem ví dụ đầy đủ: `examples/example_dispatch_order.md`*

## Ví dụ 2: Dev xin hướng dẫn implement (Dev Guide Mode)

**Input:**
> "Tạo dev guide backend cho feature nhập kho"

**Output:** AI đọc `docs/specs/inventory/IMS_NK_01_nhap_kho/spec.md` rồi sinh
`dev_guide.md` gồm: DB migration (ALTER TABLE), API endpoints + error codes,
BR pseudo-code, State Machine guards, Validation chain, Caching strategy.

## Ví dụ 3: PM kiểm tra tiến độ (Track Mode)

**Input:**
> "Ai đang làm gì?"

**Output:** AI đọc git log + spec changelogs → Dashboard: Progress Matrix,
Recent Activity (dev_A push 3 commits nhập kho, BA update spec xuất kho),
Scope Alerts (IMS_NK_01 scope +35%, 2 CRs chưa approve).

## Ví dụ 4: BA dùng Mockup Gen (Mockup Mode)

**Input:**
> "Tạo mockup cho màn hình đăng nhập, lấy chuẩn từ spec IMS_AUTH_01"

**Output:** AI tạo `src/mockups/features/auth/IMS_AUTH_01_Mockup.tsx` bằng UI Component hệ thống, đăng ký route vào MockupHub, sau đó cập nhật thông báo về Mockup URL.

---

# Constraints

- 🚫 KHÔNG tự bịa dữ liệu — nếu thiếu thông tin → hỏi user, đánh dấu `[⚠️ CẦN XÁC NHẬN]`
- 🚫 KHÔNG bỏ section nào trong template dù không có data — ghi "Chưa xác định" để team biết cần bổ sung
- 🚫 KHÔNG hardcode API keys, passwords, tokens vào bất kỳ output nào
- ✅ LUÔN chạy gap detection sau khi sinh/update spec — vì thiếu AC = tester không test được
- ✅ LUÔN auto-fix gap 🔴 Critical trước khi trả output — user không nên nhận spec có lỗ hổng nghiêm trọng
- ✅ LUÔN tạo Auto TOC ở đầu `spec.md` — spec dài mà không có mục lục rất khó đọc
- ✅ LUÔN tạo output theo cấu trúc folder `docs/specs/{module}/{Feature_ID}_{tên}/` — dễ quản lý khi có 50+ features
- ✅ LUÔN ghi Changelog khi update spec — vì Dev/QA cần biết BA vừa sửa gì
- ✅ LUÔN đảm bảo Notification Rules phủ hết mọi State transition có Side Effect — nếu transition tạo side effect mà không có noti → thêm noti hoặc ghi rõ "Không cần noti" với lý do
- ⚠️ Khi spec đã Approved mà BA update → PHẢI tạo CR, không được update lặng lẽ — PM cần biết scope thay đổi
- ⚠️ Mermaid diagrams PHẢI quote labels chứa ký tự đặc biệt — tránh lỗi render
- ⚠️ SKILL.md reference resources/ cho chi tiết — KHÔNG copy template vào đây

<!-- Version: 1.1.1 -->
<!-- Last reviewed: 2026-03-11 -->
<!-- Generated by Skill Creator Ultra v1.0 -->
