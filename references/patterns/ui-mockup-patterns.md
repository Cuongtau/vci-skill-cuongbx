<!-- updated: 2026-05-13 -->

---
description: >
  Skill tạo và quản lý Mockup UI (Code-as-Mockup).
  Sinh giao diện React/Tailwind tĩnh lưu tại folder mockups chung với spec.
  Đảm nhận nhiệm vụ rà soát - đồng bộ chéo giữa Spec (.md) và Mockup (.tsx).
---

# Skill: UI Mockup Generator & Sync (ui-mockup)

> 🚨 **QUY TẮC TỐI THƯỢNG (CRITICAL RULE)** 🚨
> **TUYỆT ĐỐI KHÔNG TỰ ĐỘNG CẬP NHẬT FILE SPEC (`.md`) KHI SỬA MOCKUP.**
> Khi có yêu cầu sửa đổi Mockup (`.tsx`), bạn CHỈ ĐƯỢC SỬA FILE `.tsx`. 
> Mọi can thiệp, đồng bộ hóa sang file Spec `.md` (bao gồm cả nội dung, bảng, cấu trúc dữ liệu và Changelog/Lịch sử cập nhật) **ĐỀU PHẢI ĐƯỢC HỎI Ý KIẾN USER TRƯỚC**. Chỉ khi User tường minh xác nhận "Đồng ý cập nhật spec" thì bạn mới được sửa file `.md`. Việc tự ý sửa file `.md` mà không có sự cho phép là VI PHẠM TÀI LIỆU NGHIÊM TRỌNG.

## Mục đích
Tạo ra các bản Mockup giao diện trực quan bằng code React tĩnh (`.tsx`), bám sát Design System hiện tại của dự án. File mockup này đóng vai trò thay thế cho Figma/Excalidraw, giúp BA dễ hình dung và FE có sẵn cấu trúc JSX chuẩn để render code.

---

## 🔍 GIAI ĐOẠN 0 — ĐỌC TRƯỚC & HỎI TRƯỚC (BẮT BUỘC, KHÔNG ĐƯỢC BỎ QUA)

> 🚨 **NGUYÊN TẮC:** TUYỆT ĐỐI KHÔNG bắt tay code mockup ngay khi BA yêu cầu "Tạo mockup cho XYZ". AI **BẮT BUỘC** phải hoàn thành 3 bước Đọc-Hỏi-Xác nhận trước khi viết dòng code `.tsx` đầu tiên. Bỏ qua giai đoạn này = mockup sai design system, sai persona, sai luồng → BA phải làm lại từ đầu.

### 0.1. ĐỌC TRƯỚC (Pre-Read Checklist) — Tự đọc, không hỏi user

AI **BẮT BUỘC** đọc các nguồn sau theo thứ tự ưu tiên trước khi sinh mockup:

| # | Nguồn | Mục đích | Bắt buộc |
|---|---|---|---|
| 1 | **Spec gốc `.md`** của feature (nếu BA cung cấp Mã_Spec) | Hiểu Business Rules, Data Elements, State Machine, Button Matrix, AC | ✅ Critical |
| 2 | **Design System dự án**: `.agent/workflows/design-system.md`, `docs/UI_UX_DESIGN_SYSTEM.md`, `docs/shared/UI_UX_DESIGN_SYSTEM.md`, hoặc `tailwind.config.ts` + `src/index.css` | Color tokens, typography, spacing, radius, shadow chuẩn dự án | ✅ Critical |
| 3 | **MockupHub** (`src/mockups/MockupHub.tsx`) + 1-2 mockup hiện có cùng module | Học pattern code, naming, import path đã có | ✅ Critical |
| 4 | **Component library**: `src/components/ui/` (shadcn) + `src/components/app/` (nghiệp vụ) | Liệt kê các component sẵn có để tái sử dụng, KHÔNG tự viết lại | ✅ Critical |
| 5 | **Spec mockup-patterns** (file này) — đọc lại quy tắc trước mỗi lần generate | Refresh cross-syncing rules, naming convention | ✅ Critical |
| 6 | **Nếu là Mobile feature**: `docs/specs/mobile/` hoặc dự án có `src/mobile/` | Pattern bottom nav, FAB, touch target, safe-area | 🟡 Khi mobile |
| 7 | **Sibling specs** cùng module (`README.md` của module) | Đảm bảo consistency cross-feature trong cùng module | 🟡 Recommended |
| 8 | **Glossary** (`docs/GLOSSARY.md` hoặc `docs/shared/GLOSSARY.md`) | Hiểu thuật ngữ nghiệp vụ Việt Nam (NXT, VTTC, MTB, OB, IB, HO, TO, MR, SO...) | 🟡 Khi có tiếng Việt |

**Sau khi đọc, AI BẮT BUỘC tóm tắt lại trong 5-7 dòng** cho BA biết:
- ✅ Đã đọc spec X (link)
- ✅ Đã đọc design system (token chính: color/font/spacing đang dùng)
- ✅ Đã tìm thấy N component sẵn có sẽ tái sử dụng
- ✅ Đã xem M mockup tham chiếu cùng module
- ⚠️ Phát hiện vấn đề / điểm chưa rõ (nếu có)

### 0.2. HỎI TRƯỚC (Pre-Mockup Questionnaire) — Bắt BA xác nhận

AI **BẮT BUỘC** đặt 5-8 câu hỏi sau đây (chọn lọc phù hợp), KHÔNG được tự suy đoán. **Nếu BA không trả lời → KHÔNG được code**. Đánh dấu `[⚠️ CẦN XÁC NHẬN]` tại các điểm BA bỏ qua.

#### 🎯 Nhóm 1 — User & Context (Job-to-be-Done)

- **Q1.** **Persona chính** của màn hình này là ai? (vd: QL dự án, QL kho, thủ kho, kế toán...) — có thể có nhiều persona, ưu tiên persona số 1.
- **Q2.** **Job-to-be-Done**: Khi mở màn này, user **cần làm gì trong 30 giây đầu tiên**? (1-2 câu, tránh "xem nhiều thông tin")
- **Q3.** **Tần suất sử dụng**: nhiều lần/ngày? định kỳ? sự kiện?
- **Q4.** **Context vật lý**: user đang ngồi văn phòng / đứng giữa kho / ngoài công trường? (ảnh hưởng tới mobile-first hay desktop-first)

#### 🖥️ Nhóm 2 — Form factor & Platform

- **Q5.** **Form factor chính**: Desktop / Mobile / Tablet / Responsive cả 3? Nếu nhiều — **cái nào ưu tiên thiết kế trước** (mobile-first vs desktop-first)?
- **Q6.** **Density mode**: Dense (nhiều data 1 màn — phù hợp power user enterprise) hay Comfortable (ít data, dễ scan)?

#### 🗺️ Nhóm 3 — Scope & State

- **Q7.** **Loại màn hình**: List / Detail / Create form / Edit form / Dashboard / Wizard nhiều bước? (Chọn 1, không "all-in-one")
- **Q8.** **State cần render**: chỉ Happy path? Hay đầy đủ Empty / Loading skeleton / Error / Permission denied / Offline?
- **Q9.** **Action chính (primary CTA)**: 1 nút quan trọng nhất trên màn hình là gì? Đặt ở đâu? (Header / FAB / Footer)
- **Q10.** **Role-based UI**: có sự khác biệt UI theo role không? (vd Admin thấy nút Xoá, User không thấy)

#### 🎨 Nhóm 4 — Design Direction

- **Q11.** **Có mockup tham chiếu nào không?** (link Figma / app khác / màn cùng module đã có)
- **Q12.** **Dark mode** có cần thiết kế song song không? Hay chỉ light mode trước?
- **Q13.** **Animation/Motion**: cần animation phức tạp (framer-motion) hay chỉ CSS transition cơ bản?

#### ❓ Nhóm 5 — Spec readiness

- **Q14.** Đã có spec `.md` chính thức chưa? Nếu **chưa**, có cần em gọi Mode 1 (Generate Spec) trước, hay BA muốn mockup-first rồi viết spec sau?
- **Q15.** Có conflict/khác biệt nào với spec của module cùng cấp không? (vd Create form của module này nên giống/khác Create form của module khác)

**Format câu hỏi:** Dùng `AskUserQuestion` tool (multi-choice) cho Q1, Q5, Q7, Q8, Q11, Q12, Q14 để BA chọn nhanh. Còn lại dạng text.

### 0.3. XÁC NHẬN ĐẦU RA (Pre-Code Confirmation)

Sau khi BA trả lời, AI **tóm tắt 1 đoạn ngắn** (5-10 dòng) theo format:

```
📋 TÓM TẮT TRƯỚC KHI MOCKUP

Feature: [Mã + Tên]
Persona chính: [Role]
Job-to-be-Done: [1 câu]
Form factor: [Mobile-first / Desktop / Responsive]
Loại màn: [List / Detail / ...]
State render: [Happy / + Empty / + Loading / + Error]
Primary CTA: [Tên nút + vị trí]
Component sẽ dùng: [SmartTable, Button, Sheet, ...]
Mockup tham chiếu: [link nếu có]
⚠️ Risk / Open question: [nếu có]

→ Đồng ý cấu hình trên? (Y/N hoặc góp ý chỉnh sửa)
```

**BẮT BUỘC chờ BA xác nhận "OK" / "Đồng ý" / "Go"** trước khi viết code. Nếu BA muốn chỉnh sửa → lặp lại từ Q của Nhóm tương ứng.

### 0.4. KHI NÀO ĐƯỢC RÚT GỌN GIAI ĐOẠN 0

Giai đoạn 0 có thể **rút gọn** (skip Pre-Read một phần + skip 50% câu hỏi) trong các trường hợp sau, **NHƯNG VẪN PHẢI HỎI ÍT NHẤT Q1, Q5, Q7, Q9**:

- ✅ BA đã cung cấp link spec `.md` chi tiết và đầy đủ Level 3-4
- ✅ Đây là update mockup hiện có (chỉ thêm 1 control nhỏ)
- ✅ Mockup nhỏ <50 dòng (vd: 1 dialog confirm đơn giản)
- ✅ BA tường minh nói "skip hỏi, làm luôn" hoặc "tự quyết định"

Trường hợp 100% không hỏi gì: **CHỈ KHI** BA nói "duplicate mockup A sang B, đổi tên — không sửa logic UI".

---

## 🧩 GIAI ĐOẠN 0.5 — KÍCH HOẠT SKILL HỖ TRỢ (Multi-Skill Orchestration)

AI **chủ động đề xuất** activate các skill bổ trợ trước khi mockup nếu phát hiện match keyword/context. Hỏi BA: *"Em đề xuất activate thêm skill [X] để [lý do]. BA đồng ý không?"*

### Bảng đề xuất skill theo context

| Context phát hiện | Skill đề xuất | Lý do |
|---|---|---|
| Feature lớn, scope chưa rõ | **`brainstorming`** | Clarify JTBD trước khi mockup |
| Có thể có nhiều phương án | **`multi-agent-brainstorming`** | Validate đa góc nhìn (PM, Dev, QA, User) |
| Workflow phức tạp, BA chưa rõ flow | **`ux-flow`** | Vẽ user flow trước |
| Feature mobile | **`mobile-design`** | Mobile-first, touch-first, platform-respectful |
| Dashboard nhiều KPI | **`kpi-dashboard-design`** | Pattern dashboard chuẩn business decision |
| Dùng shadcn | **`shadcn`** | Component patterns, theming |
| Cần microcopy chuẩn | **`ux-copy`** | Button label, empty state, error message |
| Cần đảm bảo a11y | **`ui-a11y`** | WCAG 2.2 AA audit |
| Sau khi mockup xong, cần review | **`ui-review`** + **`ux-audit`** | Design-system compliance + Nielsen heuristics |
| Cần 3-5 variation so sánh | **`magic-ui-generator`** | Sinh nhiều phương án component |
| Mockup demo HTML đơn lẻ (không vào dự án) | **`vci-design`** | Single-file HTML artifact tiếng Việt |
| Cần landing/marketing page | **`landing-page-generator`** | PAS/AIDA/BAB framework |

### Combo gợi ý theo loại feature

| Loại feature | Combo skill |
|---|---|
| **Mobile feature TC.IMS** | `brainstorming` → `ux-flow` → `mobile-design` → **`cuongbx` Mode 10** → `ux-audit` → `ui-a11y` |
| **Web Dashboard enterprise** | `product-design` → `kpi-dashboard-design` → **`cuongbx` Mode 10** → `shadcn` → `ui-review` |
| **Form/Wizard phức tạp** | `ux-flow` → **`cuongbx` Mode 10** → `ux-copy` → `ui-a11y` |
| **Mockup nhanh demo** | `vci-design` → `ux-copy` |
| **So sánh nhiều phương án** | `multi-agent-brainstorming` → `magic-ui-generator` → `ui-review` |

---

## 1. Nguyên tắc Lưu trữ & Cấu trúc Thư mục

Bản mock sẽ được lưu vào hệ thống source code thật của dự án (`src/mockups/`) với cấu trúc thư mục phản chiếu lại cấu trúc của `docs/features/`. Điều này giúp Vite/React build và hiển thị giao diện chính xác mà không bị lỗi strict module.

- **Vị trí:** `src/mockups/features/[đường_dẫn_chức_năng]/`
- **Tên cấu trúc file:** `[Mã_Spec]_Mockup.tsx`

**Ví dụ:**
- 📄 Spec: `docs/features/transfer/internal_transfer/IMS_ITF_03_Create.md`
- 🎯 Mockup: `src/mockups/features/transfer/internal_transfer/IMS_ITF_03_Create_Mockup.tsx`

## 2. Tiêu chuẩn viết Code Mockup (Mockup Standard)

- **Chuẩn Design System:** AI **BẮT BUỘC** phải đọc qua file `.agent/workflows/design-system.md` để dùng đúng thư viện UI (ví dụ Shadcn, Lucide icons, Tailwind config...).
- **Ưu tiên Component dự án:** Sử dụng lại cao nhất các thành phần đã mô tả trong dự án. (Ví dụ: Dùng `SmartTable` thay vì tự viết `<table>`, dùng các Layout component chung).
- **Chỉ tập trung UI, Bỏ qua Logic phức tạp:** 
  - KHÔNG gắn Redux, react-query hay fetch API.
  - Dùng dữ liệu giả (Mock data array, dummy text) để lấp đầy bảng, form.
  - Xử lý mượt các thao tác thị giác (có đầy đủ CSS cho hover, form validation error state fake).

## 3. Cơ chế Đồng bộ Chéo (Cross-Syncing) - BẮT BUỘC
Khi có chỉnh sửa xảy ra ở một phía (Mockup hoặc Spec), Agent phải chủ động rà soát sự khác biệt và thực hiện đối chiếu.

### Kịch bản 3.1: Khi BA cập nhật Mockup UI (Sửa layout, Thêm UI control)
1. Cập nhật file `..._Mockup.tsx` theo comment của BA.
2. AI tự động đọc file Spec `.md` đang liên kết với giao diện này.
3. Rà soát chênh lệch: "Sự thay đổi UI này có làm lệch Data Elements/Business Rules trong Spec không?" (Ví dụ: Thêm 1 trường `Ghi chú phụ` ở UI nhưng trong Spec chưa có).
4. **Agent Action:** 
   - Report tóm tắt những sai khác cho BA biết.
   - Chủ động HỎI BA: *"Sự thay đổi này cần cập nhật lại vào tài liệu Spec (bao gồm cấu trúc dữ liệu và Changelog Mockup), bạn có muốn tôi cập nhật file .md tự động không?"*
   - **Tuyệt đối KHÔNG tự động sửa hoặc thêm bất kỳ nội dung nào vào file Spec `.md` (kể cả lưu vết/changelog) nếu chưa được user đồng ý.**

### Kịch bản 3.2: Khi BA cập nhật Spec (Thêm logic hiển thị, Thêm trường db)
1. Cập nhật file `.md` theo yêu cầu.
2. AI tự động tìm trong cùng folder, xem có file Mockup tương ứng chưa.
3. Rà soát chênh lệch: Cập nhật ở Bước 1 có ảnh hưởng UI không?
4. **Agent Action:**
   - Report tóm tắt sự tụt hậu của UI.
   - Chủ động HỎI BA: *"Spec đã thay đổi, khiến bản Mockup bị outdate thiếu các trường hiển thị, bạn có muốn cập nhật lại file _Mockup.tsx ngay không?"*

## 4. Tích hợp Router & Mockup Hub (BẮT BUỘC)
Sau khi tạo xong file Mockup mới, AI phải có trách nhiệm đăng ký nó vào hệ thống Navigation để BA có thể click vào xem UI ngay trên trình duyệt:
1. Mở file `src/mockups/MockupHub.tsx`.
2. Khai báo import lazy load component mới ở đầu file.
3. Bổ sung đường dẫn (path) mới và tên màn hình tương ứng vào mảng dữ liệu `mockupModules` hiển thị trên giao diện thẻ (Card).
4. Khai báo route mới tĩnh vào trong `<Routes>` ở cuối file.

## 5. Tự động Rà soát Lỗi và Xác thực Code (Auto-Verification)
Sau khi tạo mới hoặc sửa đổi file Mockup `.tsx`, AI **BẮT BUỘC** phải rà soát lỗi để đảm bảo code có thể build/render được trên môi trường Development:
1. **Kiểm tra Import & Props:** Rà soát kỹ các đường dẫn thư mục import (chú ý phân biệt `@/components/ui/` cho các component chuẩn Shadcn và `@/components/app/` cho các component nghiệp vụ). Phải nhận diện Props của các component bằng cách xem trực tiếp code gốc dự án trước khi sử dụng.
2. **Kích hoạt tự sửa lỗi (Self-Healing):** Nếu file `.tsx` phát sinh lỗi TypeScript (ví dụ: màn hình Terminal báo lỗi build, hoặc người dùng báo lỗi "Cannot find module", sai `prop`), AI phải tự động dùng các công cụ tìm kiếm code để tìm ra định dạng xuất chuẩn (export) của Component dự án, từ đó sửa lỗi ở Mockup cho đến khi Code-Clean.
3. Không phó mặc việc fix lỗi cú pháp/import cho FE hay BA.
## 6. Lưu vết Lịch sử Mockup (Mockup Changelog) vào Spec
**Lưu ý quan trọng:** Việc lưu vết này CHỈ ĐƯỢC THỰC HIỆN KHI BA ĐỒNG Ý cập nhật spec ở Bước 3.1. Tuyệt đối không tự động ghi đè file `.md` sau khi vừa render xong Mockup.

Khi có sự đồng ý, AI thực hiện lưu vết theo quy tắc:
1. **Ghi chú liên kết:** Tạo tiêu đề `## Liên kết Mockup & Lịch sử cập nhật` ở ngay cuối file Spec. Ghi rõ đường dẫn file `.tsx` của Mockup.
2. **Lưu vết (Changelog) Gọn Gàng:** Dưới phần liên kết, trình bày một bảng theo cấu trúc: `| Ngày | Các tính năng thay đổi UI |`.
3. **Cơ chế Gom nhóm theo Ngày (Date-based Clustering):** Nếu trong cùng 1 ngày có nhiều lượt tạo/sửa đổi UI lặt vặt liên tiếp, AI KHÔNG tạo ra nhiều dòng ghi chép mới. Thay vào đó, AI đọc dòng của ngày hiện tại, và CHỈ nối thêm (append) Nội dung thay đổi bằng các Keyword ngắn gọn (Ví dụ: `[Thêm-cột-KL]`, `[Gom-Filter-1-Dòng]`, `[Bỏ-StatsBar]`). Tuyệt đối tránh viết quá dài dòng miêu tả.

## 7. Đánh giá hậu Mockup (Post-Mockup Validation)

Sau khi mockup `.tsx` đã render được, AI **CHỦ ĐỘNG GỢI Ý** chạy 1-2 skill review trước khi BA handoff cho Dev:

1. **`ui-review`** — audit code: design-system compliance, spacing discipline, mobile ergonomics
2. **`ux-audit`** — đánh giá theo Nielsen heuristics + mobile UX best practice
3. **`ui-a11y`** — WCAG 2.2 AA: keyboard nav, screen reader, contrast, focus ring
4. **`uxui-principles`** — 168 UX/UI principles, detect antipattern

Format đề xuất: *"Mockup đã render OK. Em đề xuất chạy `ui-review` + `ux-audit` để đảm bảo chất lượng trước khi handoff. BA muốn em chạy không?"*

---

## Quá trình Kích hoạt (Activation)
BA sẽ gọi sử dụng skill này khi cần phác thảo hình hài cho tài liệu hoặc sau khi đã viết spec xong. Các trigger điển hình:
- *"Tạo mockup cho màn hình XYZ"*
- *"Thêm nút X vào file mockup, đồng thời dò xem spec có phải sửa gì không"*

### ⚠️ Phản ứng chuẩn khi nhận trigger "Tạo mockup"

Khi BA gửi câu lệnh trigger, AI **KHÔNG được code ngay**. Phản ứng chuẩn theo flow:

```
1. Nhận trigger → "OK em sẽ tạo mockup cho [feature]. Trước tiên em xin phép đọc trước & hỏi BA một số thông tin để mockup đúng yêu cầu nhất."
2. → Thực hiện Giai đoạn 0.1 (Đọc trước) → tóm tắt cho BA
3. → Thực hiện Giai đoạn 0.2 (Hỏi trước) qua AskUserQuestion
4. → Đề xuất Giai đoạn 0.5 (Multi-Skill nếu phù hợp)
5. → Thực hiện Giai đoạn 0.3 (Xác nhận tóm tắt)
6. → CHỜ BA OK
7. → MỚI bắt đầu code mockup theo Section 1-6
8. → Kết thúc bằng Section 7 (Post-Mockup Validation gợi ý)
```

**Vi phạm flow này = mockup chất lượng thấp, BA mất công làm lại.**
