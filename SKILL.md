---
name: vci-skill-cuongbx
description: |
  Sinh tài liệu PRD/Spec chuẩn .md phục vụ toàn bộ team phát triển sản phẩm
  (BA, Dev, QA, Tester, PM, Tech Lead) theo quy trình end-to-end từ lên spec
  đến bàn giao test. Hỗ trợ 10 chế độ chia theo 5 vùng vai trò: Zone BA
  (Generate, Structure, Update, Audit), Zone Dev (Dev Guide Backend/Frontend),
  Zone QA (Test Gen), Zone PM (Summary, Track, Report), Zone Shared (Mockup UI).
  Dùng khi user nói "tạo spec", "viết PRD", "tạo tài liệu BA", "dev guide",
  "sinh test cases", "báo cáo tiến độ", "kiểm tra spec", "so sánh code",
  "tóm tắt feature", "scope thay đổi", "cập nhật spec", "UAT script",
  "tạo mockup", "mockup UI", "handoff test", "quy trình phát triển". English
  triggers: "create spec", "write PRD", "generate test cases", "dev guide",
  "sprint report", "spec audit", "mockup".
argument-hint: "[mode] [feature description hoặc đường dẫn spec]"
languages: all
license: MIT
metadata:
  author: cuongbx
  version: "2.6.1"
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

Sinh tài liệu PRD/Spec chuẩn `.md` trong **10 phút** (thay vì 2-3 giờ), phục vụ
toàn bộ team SDLC — từ BA lên spec, Dev implement, QA kiểm thử, đến PM theo
dõi tiến độ và báo cáo PMO — đảm bảo mọi vai trò đều đọc hiểu và sử dụng được.

**Trọng tâm:** chuẩn hóa quy trình end-to-end từ lúc có ý tưởng → spec → design
→ code → test → release, với đầy đủ handoff gate giữa các vai trò.

---

# Khởi đầu nhanh — 30 giây

| 👤 Vai trò | Câu mở đầu điển hình | → Mode | File output |
|---|---|---|---|
| **BA** | *"Tạo spec cho tính năng nhập kho vật tư"* | [M1](#mode-1) | `docs/specs/{module}/{Feature_ID}/spec.md` |
| **BA** | *"Em có meeting notes rời, cấu trúc giúp em"* | [M2](#mode-2) | Như trên + `[⚠️ CẦN XÁC NHẬN]` |
| **BA** | *"Cập nhật spec IMS_NK_01, thêm BR_005"* | [M3](#mode-3) | Same path + auto changelog |
| **Tech Lead** | *"Audit feature X — spec ↔ code có khớp?"* | [M4](#mode-4) | Gap Report + RTM |
| **Dev BE** | *"Dev guide backend cho IMS_NK_01"* | [M5A](#mode-5) | `docs/specs/.../dev_guide.md` |
| **Dev FE** | *"Dev guide frontend cho màn login"* | [M5B](#mode-5) | `docs/specs/.../dev_guide.md` |
| **QA** | *"Sinh test cases cho IMS_NK_01"* | [M6](#mode-6) | `test_cases.md` + `test_mapping.md` + `test_execution.md` |
| **PM** | *"Tóm tắt feature X cho họp sáng mai"* | [M7](#mode-7) | Output inline (không tạo file) |
| **PM** | *"Ai đang làm gì?"* · *"Tuần này tiến độ?"* | [M8](#mode-8) | Dashboard markdown |
| **PM** | *"Tạo sprint report cho PMO"* | [M9](#mode-9) | Executive summary + release notes |
| **BA + FE** | *"Tạo mockup màn đăng nhập IMS_AUTH_01"* | [M10](#mode-10) | `src/mockups/features/.../Mockup.tsx` |

📚 **Walkthrough đầy đủ từng vai trò:** [references/quickstart-by-role.md](references/quickstart-by-role.md)

---

# 🏢 Quy trình phát triển sản phẩm VCI — từ Spec tới Bàn giao Test

Quy trình **khuyến nghị của công ty VCI**, áp dụng cho mọi feature. **8 giai đoạn tuần tự**, mỗi giai đoạn có gate cảnh báo — AI sẽ **warn + hỏi xác nhận** khi thấy thiếu điều kiện, nhưng user có thể **override** để tiếp tục nếu biết đang làm gì.

📚 **Ràng buộc chi tiết từng stage + Deep Research Checklist 10 câu:** [references/vci-workflow-gates.md](references/vci-workflow-gates.md)

```
┌─ Stage 1: KHÁM PHÁ ──────────────┐
│  Ý tưởng / Notes / Jira ticket   │  BA dùng M2 nếu rời rạc, M1 nếu rõ
└──┬───────────────────────────────┘
   ▼ Gate: Stakeholder review
┌─ Stage 2: PHÁT TRIỂN YÊU CẦU ────┐
│  Spec DRAFT → IN_REVIEW          │  BA iterate qua M3 Update
└──┬───────────────────────────────┘
   ▼ Gate: Approval sign-off → APPROVED
┌─ Stage 3: HỌP STAKEHOLDER ───────┐
│  Pre-sprint briefing             │  PM dùng M7 Summary
└──┬───────────────────────────────┘
   ▼ Gate: Sprint kickoff
┌─ Stage 4: THIẾT KẾ UI ───────────┐ ┌─ Stage 5: IMPLEMENTATION ──────┐ ┌─ Stage 6: CHUẨN BỊ TEST ──┐
│  Mockup tĩnh (song song 5+6)     │ │  BE + FE code (song song 6)    │ │  Sinh test artifacts       │
│  BA + FE dùng M10 Mockup         │ │  Dev dùng M5A/M5B Dev Guide    │ │  QA dùng M6 Test Gen       │
└──┬───────────────────────────────┘ └──┬─────────────────────────────┘ └──┬─────────────────────────┘
   ▼ Gate: Design review              ▼ Gate: Code review              ▼ Gate: Test plan review
┌─ Stage 7: QUALITY GATE ──────────────────────────────────────────────────────────────────────┐
│  Pre-merge audit: spec ↔ code ↔ tests                Tech Lead + QA Lead dùng M4 Audit       │
└──┬───────────────────────────────────────────────────────────────────────────────────────────┘
   ▼ Gate: Gap Critical = 0 · RTM đủ · Tests PASSED
┌─ Stage 8: BÀN GIAO TEST → RELEASE ───────────────────────────────────────────────────────────┐
│  QA chạy test_execution.md checklist · PM dùng M8 Track + M9 Report · Status → FROZEN        │
└───────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Bảng tra cứu nhanh — Stage × Mode × Role × Gate:**

| Stage | Tên | Mode | Vai trò chính | Điều kiện vào | Gate chuyển tiếp |
|---|---|---|---|---|---|
| 1 | Khám phá | M2 / M1 | BA | Có notes hoặc yêu cầu | Stakeholder duyệt sơ bộ |
| 2 | Phát triển YC | M3 | BA | Spec DRAFT | Approvers sign → APPROVED |
| 3 | Họp stakeholder | M7 | PM + BA | Spec APPROVED | Vào sprint |
| 4 | Thiết kế UI | M10 | BA + FE | L4 spec + UI Spec + Button Matrix | Design review OK |
| 5 | Lập trình | M5A / M5B | Dev | Spec APPROVED + Mockup (nếu FE) | Code review OK |
| 6 | Chuẩn bị test | M6 | QA | Spec APPROVED | Test plan OK |
| 7 | Quality gate | M4 | Tech Lead + QA Lead | Code + tests ready | Gap Critical=0 + RTM đủ |
| 8 | Bàn giao + Release | M8, M9 | PM | All tests PASSED | Release approval → FROZEN |

**Ghi chú quan trọng:**
- Stage 4, 5, 6 **chạy song song** sau khi spec APPROVED — không block lẫn nhau.
- Mỗi gate có artifact cụ thể (spec.md, dev_guide.md, test_cases.md, Mockup.tsx, Gap Report).
- Bug/CR phát sinh ở bất kỳ stage nào → quay lại **Stage 2 qua M3 Update** với Change Request bắt buộc — **KHÔNG được sửa spec trực tiếp ở stage sau**.

## ⚠️ Warning Gates theo Stage (tóm lược)

AI sẽ **cảnh báo + hỏi xác nhận** khi gặp các case dưới. User trả lời *"vẫn tiếp tục"* → AI proceed, có log cảnh báo kèm output:

| Stage | WARN nếu... |
|---|---|
| 1-2 Spec | Chưa trả lời ≥ 7/10 Deep Research · thiếu Feature ID · thiếu roles/user journey |
| 3 Stakeholder | Spec status ≠ `APPROVED` |
| 4 Mockup | Spec thiếu L4 / UI Spec / Button Matrix |
| 5 Dev | Spec ≠ `APPROVED` · chưa có `dev_guide.md` · thiếu API contract · Dev chưa xác nhận đã đọc spec |
| 6 Test | Spec thiếu Acceptance Criteria hoặc State Machine |
| 7 Quality | Gap Critical > 0 · test FAILED chưa có ticket · RTM incomplete · security Critical unresolved |
| 8 Release | Test BLOCKED chưa mitigate · release note chưa communicate · no rollback plan |

📚 **Chi tiết + override mechanism:** [references/vci-workflow-gates.md](references/vci-workflow-gates.md)

---

# Bảng Input/Output — Cần gì, được gì

| Mode | Input tối thiểu | Output chính |
|---|---|---|
| **M1 Generate** | Feature ID + roles + luồng | `spec.md` 4 level + Mermaid + Gap Report |
| **M2 Structure** | Text rời rạc | `spec.md` + `[⚠️ CẦN XÁC NHẬN]` |
| **M3 Update** | Path spec + nội dung sửa | Updated `spec.md` + Changelog + auto CR |
| **M4 Audit** | Path spec (+ source code) | Gap Report + RTM + Deviation |
| **M5A Backend** | Path spec | `dev_guide.md` + DB migration + API + BR |
| **M5B Frontend** | Path spec | `dev_guide.md` + Component tree + Route + UX |
| **M6 Test Gen** | Path spec | `test_cases.md` + `test_mapping.md` + `test_execution.md` |
| **M7 Summary** | Path spec | Tóm tắt 1 trang inline |
| **M8 Track** | — (auto git log) | Progress dashboard |
| **M9 Report** | Period (sprint/release) | Executive summary + Release notes |
| **M10 Mockup** | Path spec L4 | `Mockup.tsx` + MockupHub route |

---

# 🔗 Gợi ý Cross-zone

4 zones: **vci** (SDLC) · **claudekit** (core dev) · **xia** (feature heist) · **others** (UI/design).

- **M1/M2 PRD** → `mermaid-expert`, `brainstorming` · **xia --compare** nếu có repo tham chiếu
- **M4 Audit** → `spec-to-code-compliance`, `ck:security`, `code-review`
- **M5A BE** → `api-documentation-generator`, `ck:plan` · **M5B FE** → `frontend-design` (others)
- **M6 Test** → `acceptance-orchestrator`, `test-automator`, `tdd-workflow`
- **M10 Mockup** → `radix-ui-design-system`, `react-ui-patterns` (others)
- **M8/M9 PM** → `ck:loop` (tự động chạy định kỳ)
- **Sau khi code xong** → `code-review` → `simplify-code` → `commit`

📚 **Bản đồ đầy đủ:** [references/cross-zone-suggestions.md](references/cross-zone-suggestions.md)

---

# Instructions

## Bước 0: Nhận diện Vai trò → Zone → Mode

### Cây quyết định

```
User nói gì?
│
├─ "tạo spec / viết PRD / tạo tài liệu" ────────────► 🟦 Zone BA  → M1 Generate
├─ "có meeting notes / ghi chú rời rạc" ────────────► 🟦 Zone BA  → M2 Structure
├─ "cập nhật spec / sửa spec / thêm BR" ────────────► 🟦 Zone BA  → M3 Update
├─ "kiểm tra spec / so sánh code / audit" ──────────► 🟦 Zone BA  → M4 Audit
│
├─ "dev guide / implement / API / DB schema" ───────► 🟩 Zone Dev → M5 (Hỏi: BE 5A hay FE 5B?)
│
├─ "test cases / test matrix / UAT / sinh test" ────► 🟨 Zone QA  → M6 Test Gen
│
├─ "tóm tắt / overview feature" ────────────────────► 🟧 Zone PM  → M7 Summary
├─ "ai đang làm / tiến độ / status / track" ────────► 🟧 Zone PM  → M8 Track
├─ "báo cáo PMO / sprint report / release notes" ───► 🟧 Zone PM  → M9 Report
│
└─ "tạo mockup / mockup UI / vẽ giao diện" ─────────► 🟪 Zone Shared → M10 Mockup
```

### Khi mơ hồ — Hỏi ngược lại

Nếu trigger không khớp rõ:
> *"Anh/chị đang ở vai trò nào? (BA / Dev / QA / PM / FE Dev)"*
> *"Mục tiêu cụ thể: tạo mới, cập nhật, kiểm tra, hay báo cáo?"*

### Điều chỉnh ngôn ngữ theo vai trò

**PM:** ngắn, ngôn ngữ nghiệp vụ (L1-2) · **BA:** đầy đủ template (L1-4) · **Dev:** code-centric (L3-4) · **QA:** tập trung AC (L3-4) · **FE Dev:** UI/component (L3-4)

---

## 🟦 Zone BA — Nghiệp vụ (Mode 1-4)

### <a id="mode-1"></a>Mode 1: Generate — Sinh PRD mới

📚 **Template:** `references/templates/prd-template.md` · **Deep Research Checklist (BẮT BUỘC):** [references/vci-workflow-gates.md](references/vci-workflow-gates.md)

**⚠️ PRE-CHECK (khuyến nghị):** Trước khi generate spec, AI **nên hỏi BA đủ 10 câu Deep Research** (vấn đề nghiệp vụ, stakeholders, users, gap analysis, dependencies, edge cases, NFR, constraints, risks, success metrics). Thiếu ≥ 3/10 câu → AI cảnh báo + gợi ý Mode 2 với `[⚠️ CẦN XÁC NHẬN]`. User muốn skip → xác nhận *"vẫn tạo spec"* để bypass.

1. Hỏi thông tin tối thiểu: Feature ID + tên (VD `IMS_NK_01`), mục tiêu nghiệp vụ, roles, luồng tổng quát.
2. Sinh PRD **4 level**:
   - **L1**: Product Overview (PM, BA)
   - **L2**: Epic/Module (Architect, PM)
   - **L3**: Feature Detail — User Story, State Machine, Button Matrix (Dev, QA)
   - **L4**: Sub-feature — UI Spec, Business Rules, Validation, API, Acceptance Criteria (Dev, QA)
3. Tự sinh Mermaid diagrams (📚 `references/patterns/mermaid-patterns.md`): State Machine, Screen Flow, ERD.
4. Tự thêm: Glossary, Notification Rules, Audit Trail, Risk Assessment, Data Migration Notes.
5. Output: `docs/specs/{module}/{Feature_ID}_{tên_snake_case}/spec.md`
   > Mermaid inline trong spec.md. Chỉ tách `diagrams.md` khi > 500 dòng.
6. Tạo/cập nhật `docs/specs/{module}/README.md` — index features.
7. ✅ **VERIFY:** chạy gap detection (📚 `references/rules/gap-detection-rules.md`) → **tự fix gap 🔴 Critical** trước khi trả kết quả.

### <a id="mode-2"></a>Mode 2: Structure — Cấu trúc hóa thông tin rời rạc

1. Nhận input: meeting notes, Jira tickets, email, text tự do.
2. Trích xuất: features, rules, roles, flows, fields, edge cases.
3. Sinh PRD chuẩn template (giống M1 bước 2-7).
4. Đánh dấu `[⚠️ CẦN XÁC NHẬN]` ở chỗ AI không chắc.
5. ✅ **VERIFY:** gap detection.

### <a id="mode-3"></a>Mode 3: Update — Cập nhật spec đã có

1. Đọc spec hiện tại (user cho path hoặc AI tìm trong `docs/specs/`).
2. Thực hiện thay đổi theo yêu cầu.
3. **Auto Changelog:** thêm dòng lịch sử (ngày, người, nội dung, version).
4. **Scope Change Detection** (nếu spec đã APPROVED):
   - So sánh Scope Baseline → tính % thay đổi.
   - Vượt baseline → tạo Change Request (phân loại, impact, CR Log).
5. ✅ **VERIFY:** gap detection sau update.

### <a id="mode-4"></a>Mode 4: Audit — Kiểm tra spec & code

📚 **Quy tắc:** `references/rules/gap-detection-rules.md`

1. Đọc spec → **Gap Detection:** BR↔AC, State↔Button, Field↔Validate, cross-feature consistency.
2. **Code-Spec Comparison** (nếu Dev/Tech Lead): đọc source code → sinh RTM + Deviation Report.
3. **Tech Lead Review:** architecture, performance, security, tech debt checklists.
4. Output: Gap Report + action items ưu tiên.

---

## 🟩 Zone Dev — Lập trình (Mode 5)

### <a id="mode-5"></a>Mode 5: Dev Guide — Hướng dẫn implement

📚 **Template:** `references/templates/dev-guide-template.md`

**⚠️ PRE-CHECK (khuyến nghị):**
- ⚠️ Nên có spec status = `APPROVED` (chạy khi `DRAFT`/`IN_REVIEW` → AI warn).
- ⚠️ Nên có đủ L4 + API contract (nếu BE) hoặc UI Spec + Button Matrix (nếu FE).
- ⚠️ Thiếu spec → AI hỏi xác nhận trước khi sinh dev_guide.
- 💡 Khuyến khích sinh `dev_guide.md` TRƯỚC khi code để Dev không miss requirement.

User muốn skip check → xác nhận *"vẫn tạo dev guide"* để bypass warning.

Hỏi sub-mode trước: *"Backend (5A) hay Frontend (5B)?"*

**5A — Backend:** DB schema, API endpoints, BR implementation, State Machine guards, Validation chain, Caching, Concurrency, Logging.

**5B — Frontend:** Route mapping, Component breakdown, Conditional rendering (từ Button Matrix), Form validation UX, UI States, a11y, Keyboard shortcuts, Error boundaries.

Output: `docs/specs/{module}/{Feature_ID}_{tên}/dev_guide.md`

---

## 🟨 Zone QA — Kiểm thử (Mode 6)

### <a id="mode-6"></a>Mode 6: Test Gen — Sinh test artifacts

📚 **Template:** `references/templates/test-gen-template.md` · **Execution:** `references/templates/test-execution-template.md`

**⚠️ PRE-CHECK (khuyến nghị):**
- ⚠️ Nên có spec status = `APPROVED`.
- ⚠️ Nên có đủ Acceptance Criteria + State Machine + Button Matrix (cần cho Test Matrix đầy đủ).
- ⚠️ Thiếu AC → AI warn + sinh test cases với coverage thấp hơn; gợi ý BA bổ sung qua M3.

User muốn skip → xác nhận *"vẫn sinh test"* để proceed.

1. Đọc spec → sinh:
   - BDD Test Cases (Given/When/Then) từ Acceptance Criteria.
   - State × Button Test Matrix.
   - Regression Checklist từ Impact Matrix.
   - Test Data Prerequisites.
   - Security Test Scenarios (SQL injection, XSS, RBAC, IDOR).
   - Performance Test Scenarios (k6 templates).
   - Automation Skeleton (Playwright).
   - Requirement → Test Mapping (RTM).
   - **Test Execution Matrix** — checkbox, status (PASSED/FAILED/BLOCKED/UNTESTED), actual result, bug ID.
2. Output: `test_cases.md` + `test_mapping.md` + `test_execution.md` trong feature folder.
3. `test_execution.md` gồm:
   - **Execution Dashboard:** tổng TC, số PASSED/FAILED/BLOCKED/UNTESTED, tỷ lệ %.
   - **Execution Matrix:** mỗi TC có checkbox `[ ]`, phân loại (Happy/Negative/Edge), priority, status, actual result.
   - QA có thể copy bảng sang Excel/Google Sheets để báo cáo.

**Handoff test:** Sau khi Dev hoàn thành code → QA mở `test_execution.md` → tick từng TC → update status. Bug phát sinh → tạo ticket, nếu cần sửa spec → quay về M3 Update.

---

## 🟧 Zone PM — Quản lý (Mode 7-9)

### <a id="mode-7"></a>Mode 7: Summary — Tóm tắt 1 trang

Đọc spec → sinh tóm tắt: Feature name, status, owner, mục tiêu, scope metrics, estimation, risk, dependencies, RACI. **Output inline (không tạo file).**

### <a id="mode-8"></a>Mode 8: Track — Dashboard tiến độ

📚 **Template:** `references/templates/pm-report-template.md` (phần M8)

Đọc `git log` + spec changelogs → sinh dashboard: Progress Matrix, Recent Activity, Scope Alerts, Warnings & Risks.

### <a id="mode-9"></a>Mode 9: Report — Báo cáo PMO

📚 **Template:** `references/templates/pm-report-template.md` (phần M9)

Thu thập git log, spec status, CR log → sinh: Executive Summary, Feature Detail, CR Summary, Risks & Blockers, Next Sprint, Release Notes, Communication Template.

---

## 🟪 Zone Shared — Chia sẻ (Mode 10)

### <a id="mode-10"></a>Mode 10: Mockup — Mockup tĩnh bằng code

📚 **Quy tắc:** `references/patterns/ui-mockup-patterns.md`

1. Đọc spec → tạo React `.tsx` tại `src/mockups/features/.../`.
2. Dùng component chuẩn Design System, dummy data, đầy đủ CSS hover/form state.
3. **Đồng bộ Chéo:** Mockup ↔ Spec — **PHẢI hỏi user trước khi sửa `.md`**.
4. Đăng ký route vào `MockupHub.tsx`.
5. Auto-Verification: self-healing cho lỗi import/props.

---

# 🏢 Cộng tác nhiều vai trò (Enterprise)

Project có **nhiều vai trò cùng làm trên 1 repo** → cần guardrails tránh xung đột, đảm bảo compliance.

### Ma trận RACI (tóm lược)

| Artifact | R (Chủ trì) | A (Duyệt) | C (Tư vấn) | I (Thông báo) |
|---|---|---|---|---|
| `spec.md` L1-2 | PM | Architect | BA | Dev, QA |
| `spec.md` L3-4 | BA | Tech Lead, QA | PM, FE/BE Lead | Tester |
| `dev_guide.md` | Tech Lead | BE/FE Lead | Architect | Dev team |
| `test_cases.md` | QA Lead | QA Manager | BA, Dev | PM |
| `Mockup.tsx` | FE Dev | UX Designer | BA | PM |

### Vòng đời Spec

```
DRAFT → IN_REVIEW → APPROVED → FROZEN → DEPRECATED
```

- **DRAFT:** M1/M2 — free-edit · **IN_REVIEW:** lock direct edit, comment qua PR
- **APPROVED:** M3 update → **PHẢI tạo Change Request** · **FROZEN:** release branch
- **DEPRECATED:** feature retired → archive

📚 **CODEOWNERS, Git branching, Handoff notification, Enterprise frontmatter (Jira/Sprint/Approvers), Compliance, Onboarding, KPI:** [references/enterprise-workflow.md](references/enterprise-workflow.md)

---

# Lỗi phổ biến

📚 14 anti-patterns + cách đúng: [references/common-pitfalls.md](references/common-pitfalls.md)

---

# Examples

## 🟦 Zone BA

**VD 1 — M1 Generate:** *"Tạo spec cho tính năng nhập kho vật tư. Thủ kho tạo phiếu nhập, quản lý duyệt."* → AI sinh `docs/specs/inventory/IMS_NK_01_nhap_kho/spec.md` với 4 level, State Machine, BR, AC BDD, Button Matrix, gap report. 📚 *Chi tiết: `examples/example-dispatch-order.md`*

**VD 2 — M2 Structure:** *"Notes meeting phòng kho, cấu trúc giúp em: 'Thủ kho nhập phiếu... QL duyệt...'"* → AI trích xuất roles/states/BR → PRD 4 level + `[⚠️ CẦN XÁC NHẬN]`.

**VD 3 — M4 Audit:** *"Audit feature IMS_NK_01 — spec và code có khớp?"* → AI đọc `spec.md` + source code → sinh RTM + Deviation Report: "⚠️ Endpoint `POST /warehouse-receipts` thiếu validation `BR_003`".

## 🟩 Zone Dev

**VD 4 — M5A Backend:** *"Tạo dev guide backend cho feature nhập kho"* → AI đọc spec → sinh `dev_guide.md`: DB migration, API endpoints, BR pseudo-code, State Machine guards, Caching, Logging.

## 🟨 Zone QA

**VD 5 — M6 Test Gen:** *"Sinh test cases cho IMS_NK_01"* → 3 file: `test_cases.md` (BDD 25 cases), `test_mapping.md` (RTM), `test_execution.md` (checkbox matrix).

## 🟧 Zone PM

**VD 6a — M7 Summary:** *"Tóm tắt IMS_NK_01 cho họp sáng mai"* → Output inline 1 trang A4 (Status + Owner + Scope + Risks + RACI).

**VD 6b — M8 Track:** *"Ai đang làm gì tuần này?"* → Dashboard: Progress Matrix (IMS_NK_01 80%, IMS_AUTH_01 60%), Recent Activity (3 commits, 2 PR), Scope Alerts (CR-002 pending approval), Warnings (QA thiếu test data cho IMS_NK_01).

**VD 6c — M9 Report:** *"Tạo sprint report tuần này cho PMO"* → Executive Summary (2 features delivered, 1 delayed), Feature Detail table, CR Summary (3 CR, 2 approved 1 pending), Risks & Blockers, Next Sprint plan, Release Notes draft, Communication Template gửi stakeholders.

## 🟪 Zone Shared

**VD 7 — M10 Mockup:** *"Tạo mockup màn đăng nhập từ IMS_AUTH_01"* → `src/mockups/features/auth/IMS_AUTH_01_Mockup.tsx` + MockupHub route. Pre-flight check: spec phải có L4 + UI Spec + Button Matrix.

---

# Constraints

## 🚫 Không được vi phạm (tuyệt đối cứng)

- **KHÔNG tự bịa dữ liệu** — thiếu thông tin → hỏi user, đánh dấu `[⚠️ CẦN XÁC NHẬN]`.
- **KHÔNG bỏ section template** dù không có data — ghi "Chưa xác định".
- **KHÔNG hardcode** API keys, passwords, tokens.
- **KHÔNG auto-update spec `.md`** khi user chỉ sửa mockup `.tsx` (M10) — PHẢI hỏi.

## ⚠️ Cảnh báo — khuyến nghị quy trình VCI (user có thể override)

AI sẽ warn + hỏi xác nhận; user trả *"vẫn tiếp tục"* để bypass:

- ⚠️ **Sinh spec (M1) khi chưa đủ 7/10 Deep Research** — gợi ý ask-back.
- ⚠️ **Chạy M5/M6/M10 khi spec ≠ `APPROVED`** — gợi ý hoàn thiện spec trước.
- ⚠️ **Code FE/BE khi chưa có `dev_guide.md`** — gợi ý sinh guide M5A/M5B trước.
- ⚠️ **Sửa spec trực tiếp ở Stage 5/6/7** — gợi ý loopback qua M3 Update + Change Request.
- ⚠️ **Skip stage trong quy trình VCI** — gợi ý tuần tự 1→2→3→(4‖5‖6)→7→8.
- ⚠️ **Merge PR thiếu Feature_ID trong commit message** — gợi ý thêm để audit trail.

## ✅ Luôn luôn làm

- **LUÔN chạy gap detection** sau sinh/update spec (M1, M2, M3).
- **LUÔN tự fix gap 🔴 Critical** trước khi trả output.
- **LUÔN tạo Auto TOC** ở đầu `spec.md`.
- **LUÔN tạo output** theo folder `docs/specs/{module}/{Feature_ID}_{tên}/`.
- **LUÔN ghi Changelog** khi update spec (M3).
- **LUÔN đảm bảo Notification Rules** phủ hết State transitions có Side Effect.

## ⚠️ Cảnh báo

- **Spec đã APPROVED mà update** → PHẢI tạo Change Request (M3).
- **Mermaid label chứa ký tự đặc biệt** → PHẢI quote: `"Node's Label"`.
- **SKILL.md reference `references/`** cho chi tiết — KHÔNG copy template vào đây.

## 🛡️ Anti-duplication Guards (4 hard rules)

AI tự enforce khi phát hiện conflict:

1. **M1 vs `business-analyst`** — REFUSE invoke cả 2 cùng feature (M1 đã bao BA).
2. **M10 precondition** — REFUSE nếu spec thiếu L4 + UI Spec + Button Matrix.
3. **M4 vs `/xia --compare`** — Phân biệt: local audit vs external repo compare.
4. **KHÔNG invoke `/ck:brainstorm`** từ M1 hoặc `/xia` (phá phase ownership).

## 🔍 Pre-flight check

```bash
python references/scripts/check-mode-prerequisites.py --mode 10 --spec <path>
```

Exit codes: `0` OK · `1` WARN · `2` FAIL (refuse).

📚 **Chi tiết + enforcement rules:** [references/anti-duplication-guards.md](references/anti-duplication-guards.md)

<!-- Version: 2.6.1 -->
<!-- Last reviewed: 2026-04-14 -->
<!-- Generated by Skill Creator Ultra v1.0 -->
<!-- Changelog:
     2.6.1 (2026-04-14): Relax hard BLOCK → WARN + ask confirm. Override mechanism ("vẫn tiếp tục"/"skip check"). Cho phép flexible workflow với warning log. Giữ 4 hard rules (bịa data/secrets/auto-edit spec).
     2.6.0 (2026-04-14): Quy trình phát triển sản phẩm VCI — strict sequential enforcement; Deep Research Checklist 10 câu BẮT BUỘC trước M1; Hard gates per stage với BLOCK conditions; Pre-check cứng cho M5/M6/M10 (spec APPROVED required); Loopback bắt buộc qua M3+CR khi phát hiện vấn đề; vci-workflow-gates.md mới.
     2.5.0 (2026-04-14): Việt hóa section headers; thêm "Quy trình end-to-end" 8-stage (Khám phá → Requirements → Stakeholder → Design‖Impl‖Test Prep → Quality Gate → Handoff → Release); shrink Enterprise section; thêm M8/M9 examples; English triggers cho global activation.
     2.4.0 (2026-04-14): All 10 modes in SDLC pipeline (added M7 Summary); SDLC Stage × Mode Matrix.
     2.3.0 (2026-04-14): Enterprise multi-role: RACI, CODEOWNERS, spec lifecycle, git branching, handoff, compliance.
     2.2.0 (2026-04-14): Quick Start, Pipeline diagram, Input/Output Contract, Common Pitfalls.
     2.1.0 (2026-04-14): Restructured 10 modes into 5 zones with decision tree.
     2.0.0 (2026-04-13): 10 modes consolidated.
-->
