<!-- updated: 2026-05-13 -->

# BẢNG THEO DÕI VÀ THỰC THI TEST CASE (TEST EXECUTION TEMPLATE)

*ID: `<Feature_ID>` | Module: `<Module_Name>`*

Template dành cho QA/Tester dùng để **viết**, **thực thi (execute)**, **đánh giá trạng thái (status)** từng test case và **theo dõi tiến độ** (checkbox).

---

## 📊 1. Kiểm soát tiến độ (Test Execution Dashboard)

Cập nhật bảng này sau mỗi vòng test để team có snapshot nhanh.

| Metric | Số lượng | Tỷ lệ (%) |
|--------|----------|-----------|
| **Tổng số Test Cases** | 0 | 100% |
| 🟩 **PASSED** (Đạt) | 0 | 0% |
| 🟥 **FAILED** (Lỗi) | 0 | 0% |
| 🟨 **BLOCKED** (Bị chặn/Chưa dev) | 0 | 0% |
| ⏳ **PENDING** (Chờ BA/Dev confirm) | 0 | 0% |
| ⬜ **UNTESTED** (Chưa test) | 0 | 0% |

---

## 🛠 2. Bảng Test Case Thực Thi Chi Tiết (Execution Matrix)

| Số thứ tự | TC ID | Module / Tính năng | Phân loại | Kịch bản | Đk đầu vào | Các bước | Kết quả mong muốn (Expected Result) | Mức độ ưu tiên | Trạng thái (Status) | Kết quả thực tế / Bug ID / Notes |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| 1 | **TC_01** | *<Tên>* | Happy Case | *<Mô tả>* | *...* | 1.<br>2.<br>3. | *<Kết quả mong đợi>* | 🔴 Critical | ⬜ `UNTESTED` | |
| 2 | **TC_02** | *<Tên>* | Negative | *<Mô tả>* | *N/A* | 1.<br>2. | *<Kết quả mong đợi>* | 🟡 Med | ⬜ `UNTESTED` | |
| 3 | **TC_03** | *<Tên>* | Edge Case | *<Mô tả>* | *N/A* | 1.<br>2. | *<Kết quả mong đợi>* | 🟡 Med | ⬜ `UNTESTED` | |

### Phân loại (Classification)
- **Happy Case** — Luồng chính, user đi đúng flow
- **Negative** — Input sai, flow không hợp lệ
- **Edge Case** — Ranh giới, giá trị biên, concurrency, rỗng/đầy
- **Luồng chính** — Business logic cốt lõi (phê duyệt, trừ kho...)
- **Permission** — RBAC, quyền truy cập
- **Performance** — Load, response time

### Mức độ ưu tiên
- 🔴 **Critical** — Block release nếu fail (VD: phê duyệt + cộng kho)
- 🔴 **High** — Ảnh hưởng user flow chính
- 🟡 **Med** — Nice-to-have, UI polish
- 🔵 **Low** — Cosmetic

---

## 📋 3. Hướng dẫn sử dụng

**Ý nghĩa Status:**
- 🟩 `PASSED` — Chạy trơn tru đúng Requirement.
- 🟥 `FAILED` — Vỡ UI, sai logic, không khớp AC. **BẮT BUỘC ghi Bug ID** cột cuối.
- 🟨 `BLOCKED` — API tạch, chờ FE code, data prerequisite chưa sẵn.
- ⏳ `PENDING` — Chờ BA/Dev confirm spec hoặc quyết định scope.
- ⬜ `UNTESTED` — Chưa thực thi, queue chờ test.

**Copy qua Excel / Google Sheets:**
Bôi đen toàn bảng mục 2 → `Ctrl+C` → paste vào Excel/Sheets. Các dòng sẽ tự gom vào cell rất gọn.

---

## 🗄️ 4. Test Data Prerequisites

Liệt kê dữ liệu/tài khoản cần chuẩn bị trước khi chạy test.

- **Tài khoản:**
  - *<Role 1 — VD: Người tạo phiếu>*
  - *<Role 2 — VD: Người phê duyệt>*
  - *<Role 3 — VD: Admin kho>*
- **Dữ liệu chuẩn bị (Seed Data):**
  - *<VD: ≥ 3 vật tư active, 2 kho, 1 nhà cung cấp>*
  - *<VD: ≥ 1 phiếu ở mỗi status Draft/Pending/Approved/Rejected/Cancelled>*
- **Môi trường:**
  - *<VD: DB staging, version v1.2.x>*
  - *<VD: Feature flag `X_ENABLED=true`>*

---

## 🔗 5. Cross-Module Impact & Regression Testing

Nếu feature có side-effect lên module khác → list ra để QA test regression.

| Module Liên Đới | Điểm Giao Tiếp | Kịch Bản Test Kéo Theo | Mức rủi ro |
|---|---|---|---|
| **<Module>** | `<API / DB table / UI>` | - *<Kịch bản regression>* | 🔴 Critical |
| **<Module>** | `<...>` | - *<...>* | 🟡 Med |

---

## 🚦 6. Test Matrix (State Machine × Button Matrix)

Map từ `State Machine` + `Button Matrix` trong spec để đảm bảo coverage mọi tổ hợp.

| Current State | Role/User | `[Action 1]` | `[Action 2]` | `[Action 3]` |
|---|---|---|---|---|
| **<State 1>** | <Role> | Khả dụng | Ẩn | **Khả dụng** |
| **<State 2>** | <Role> | Ẩn | Khả dụng | Ẩn |

**Rule:** Mỗi ô "Khả dụng" phải có ≥ 1 TC tương ứng trong mục 2.

---

## ✅ 7. Regression Checklist (Impact Matrix)

Checklist ngắn khi có bug fix hoặc hotfix, chạy lại các flow liên quan.

- [ ] **<Hạng mục 1>:** *<Chi tiết flow cần re-test>*
- [ ] **<Hạng mục 2>:** *<Chi tiết>*
- [ ] **Permission regression** — login với mọi role, verify button matrix không đổi
- [ ] **Data migration** — nếu có schema change, verify data cũ vẫn đọc được
- [ ] **Cross-browser** — Chrome, Edge, Firefox (nếu có UI thay đổi)

---

## 📎 8. Screenshots & Evidence

Convention: lưu screenshot/video evidence tại thư mục `test_cases_<Feature_ID>_screenshoot/` cạnh file test case.

- `TC_01_pass.png`
- `TC_02_fail_bugXYZ.png`
- `TC_03_flow.gif`

---

*Template này generate từ skill `vci-skill-cuongbx` Mode 6 (Test Gen). Xem `references/rules/gap-detection-rules.md` để audit test ↔ spec.*
