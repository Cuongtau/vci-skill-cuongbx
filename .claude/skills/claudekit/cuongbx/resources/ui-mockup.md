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

## Quá trình Kích hoạt (Activation)
BA sẽ gọi sử dụng skill này khi cần phác thảo hình hài cho tài liệu hoặc sau khi đã viết spec xong. Các trigger điển hình:
- *"Tạo mockup cho màn hình XYZ"*
- *"Thêm nút X vào file mockup, đồng thời dò xem spec có phải sửa gì không"*
