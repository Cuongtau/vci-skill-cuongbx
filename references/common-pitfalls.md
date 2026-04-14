# Common Pitfalls — Các lỗi phổ biến khi dùng vci-skill-cuongbx

| ❌ Anti-pattern | ✅ Đúng cách | Tại sao |
|---|---|---|
| Chạy Mode 1 với input `"tạo spec đăng nhập"` | Cung cấp Feature ID + roles + luồng | Thiếu context → AI bịa, output không dùng được |
| Mode 3 update spec Approved mà không tạo CR | Auto CR được generate + log vào CR Log | Scope Baseline = audit trail legal/PMO |
| Bỏ section template vì "không có data" | Ghi "Chưa xác định" | Template = contract giữa BA ↔ Dev ↔ QA |
| Mode 10 sửa `.tsx` rồi auto-update `.md` | **HỎI user** trước khi sync ngược | Mockup có thể khác intent BA |
| Mode 6 sinh test mà không có spec trước | Tạo Mode 1 spec trước, rồi Mode 6 | Test phải trace tới AC có trong spec |
| Mode 4 audit mà không có code | Cung cấp path source code trong prompt | Audit = spec ↔ code, thiếu vế nào cũng fail |
| Mode 9 report mà chưa có git log | Chạy Mode 8 Track trước để warm-up | Report cần changelogs + commits context |
| Hardcode API key vào spec/mockup | **KHÔNG bao giờ** — dùng `.env.example` | Commit lên git = leak production |
| Mermaid label chứa `:`, `(`, `"` không quote | Wrap trong `"..."`: `"Node's Label"` | Parser fail, diagram không render |
| Skip gap detection vì "đã xong rồi" | Luôn chạy — auto-fix Critical 🔴 | Gap = bug tiềm ẩn trong spec |
| Mode 7 Summary tạo file `.md` | Output inline only, không tạo file | Summary = ephemeral, cho 1 lần họp |
| Dùng Mode 1 cho scope nhỏ (1 task) | Mode 3 update section nhỏ | Mode 1 overkill → bloat spec |
| Mode 5A và 5B chạy separate người, không sync | Assign 1 Tech Lead review cả 2 | Contract mismatch BE↔FE → bug integration |
| Feature ID không theo convention | Check `.vci-config.yaml` module_prefix | Audit trail + cross-feature dep lookup fail |
