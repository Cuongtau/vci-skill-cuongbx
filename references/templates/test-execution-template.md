# BẢNG THEO DÕI VÀ THỰC THI TEST CASE (TEST EXECUTION TEMPLATE)

Template này được thiết kế để QA/Tester không chỉ viết Test Case mà còn có thể **thực thi (execute)**, **đánh giá trạng thái (status)** cụ thể và có **checkbox theo dõi** tiến độ (đã test hay chưa).

## 📊 1. Kiểm soát tiến độ (Test Execution Dashboard)

Cập nhật bảng này để theo dõi tiến độ tổng thể của đợt Test.

| Metric | Số lượng | Tỷ lệ (%) |
|--------|----------|-----------|
| **Tổng số Test Cases** | 0 | 100% |
| 🟩 **PASSED** (Đạt) | 0 | 0% |
| 🟥 **FAILED** (Lỗi) | 0 | 0% |
| 🟨 **BLOCKED** (Bị chặn/Chưa dev) | 0 | 0% |
| ⬜ **UNTESTED** (Chưa test) | 0 | 0% |

---

## 🛠 2. Bảng Test Case Thực Thi Chi Tiết (Execution Matrix)

*Mẹo sử dụng trong Markdown: Dùng `[ ]` cho các case chưa test và `[x]` cho case đã test xong để dễ nhìn.*

| Đã Test? | TC ID | Module / Tính năng | Phân loại | Kịch bản | Đk đầu vào | Các bước | Kết quả mong muốn (Expected Result) | Mức độ ưu tiên | Trạng thái (Status) | Kết quả thực tế (Actual Result) / Bug ID / Notes |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| [ ] | **TC_01** | *<Tên>* | Happy Case | **Mô tả:** *...* | *...* | 1.<br>2.<br>3. | *<Kết quả mong đợi>* | 🔴 High | ⬜ `UNTESTED` | *<Ghi chú hoặc mã Bug>* |
| [ ] | **TC_02** | *<Tên>* | Negative | **Mô tả:** *...* | *N/A* | 1.<br>2. | *<Kết quả mong đợi>* | 🟡 Med | ⬜ `UNTESTED` | *<Ghi chú hoặc mã Bug>* |
| [ ] | **TC_03** | *<Tên>* | Edge Case | **Mô tả:** *...* | *N/A* | 1.<br>2. | *<Kết quả mong đợi>* | 🟡 Med | ⬜ `UNTESTED` | *<Ghi chú hoặc mã Bug>* |

---

## 📋 Hướng dẫn sử dụng

**1. Ý nghĩa các cột:**
- **Đã Test?**: Checkbox `[ ]` hoặc `[x]` để đánh dấu nhanh case nào đã thực thi, tránh sót.
- **Trạng thái (Status)**:
  - `🟩 PASSED`: Tính năng chạy trơn tru đúng Requirement.
  - `🟥 FAILED`: Kịch bản test bị xịt, vỡ UI, sai logic... (Nhớ ghi Bug IDE ở cột cuối).
  - `🟨 BLOCKED`: Bị gián đoạn, API tạch, chờ FE code... nên ko test được lúc này.
  - `⬜ UNTESTED`: Đang chuẩn bị test.

**2. Copy qua Excel / Google Sheets:**
Nếu phải báo cáo bằng File `.xlsx`, bạn chỉ cần bôi đen nguyên cái Bảng số 2 rồi Ctrl C, sau đó dán thẳng vào trang tính Excel/Google Sheets. Excel sẽ tự động gom các dòng text vào chung 1 ô rất ngăn nắp và rõ ràng.
