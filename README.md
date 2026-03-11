# vci-skill-cuongbx

> 🤖 AI Skill sinh tài liệu PRD/Spec chuẩn `.md` phục vụ toàn bộ team phát triển sản phẩm.

## 🎯 Mục tiêu

Sinh tài liệu PRD/Spec chuẩn trong **10 phút** (thay vì 2-3 giờ), phục vụ toàn bộ team SDLC — từ BA viết spec, Dev implement, QA test, đến PM track progress.

## 👥 Đối tượng sử dụng

| Vai trò | Modes | Điểm chất lượng |
|---------|-------|-----------------|
| BA | Generate, Structure, Update, Audit | 10/10 |
| Backend Dev | Dev Guide (BE) | 10/10 |
| Frontend Dev | Dev Guide (FE) | 10/10 |
| Tech Lead | Audit (Tech Review) | 10/10 |
| QA / Tester | Test Gen | 10/10 |
| PM | Summary, Track, Report | 10/10 |

## 🚀 9 Modes

| # | Mode | Lệnh sử dụng | Mô tả |
|---|------|---------------|--------|
| 1 | **Generate** | `tạo spec [tên feature]` | Sinh PRD 4 level từ mô tả nghiệp vụ |
| 2 | **Structure** | `cấu trúc lại [meeting notes / text]` | Biến thông tin rời rạc thành spec chuẩn |
| 3 | **Update** | `cập nhật spec [feature_id]` | Sửa spec + auto changelog + CR detection |
| 4 | **Audit** | `kiểm tra spec [feature_id]` | Gap detection + Code-Spec comparison + RTM |
| 5 | **Dev Guide** | `dev guide [BE/FE] cho [feature]` | Sinh hướng dẫn implement (BE hoặc FE) |
| 6 | **Test Gen** | `sinh test [feature_id]` | Sinh BDD test + Security + Performance + Automation |
| 7 | **Summary** | `tóm tắt [feature_id]` | Tóm tắt 1 trang cho PM |
| 8 | **Track** | `tiến độ` hoặc `ai đang làm gì` | Dashboard hoạt động từ git + spec |
| 9 | **Report** | `báo cáo PMO` hoặc `report` | Báo cáo tiến độ + Release Notes |

## 📦 Cài đặt

### Yêu cầu

- [Gemini Antigravity](https://gemini.google.com) đã được cài đặt
- Git

### Cách 1: Clone trực tiếp vào thư mục skills (Khuyến nghị)

**Windows (PowerShell):**
```powershell
# Clone repo thẳng vào thư mục skills của Antigravity
git clone https://github.com/Cuongtau/vci-skill-cuongbx.git "$env:USERPROFILE\.gemini\antigravity\skills\vci-skill-cuongbx"
```

**macOS / Linux:**
```bash
# Clone repo thẳng vào thư mục skills của Antigravity
git clone https://github.com/Cuongtau/vci-skill-cuongbx.git ~/.gemini/antigravity/skills/vci-skill-cuongbx
```

### Cách 2: Clone rồi copy thủ công

```bash
# Bước 1: Clone repo
git clone https://github.com/Cuongtau/vci-skill-cuongbx.git

# Bước 2: Copy vào thư mục skills
# Windows (PowerShell):
Copy-Item -Recurse vci-skill-cuongbx "$env:USERPROFILE\.gemini\antigravity\skills\vci-skill-cuongbx"

# macOS / Linux:
cp -r vci-skill-cuongbx ~/.gemini/antigravity/skills/vci-skill-cuongbx
```

### Cách 3: Cập nhật skill (đã cài trước đó)

```bash
# Di chuyển vào thư mục skill và pull bản mới nhất
cd ~/.gemini/antigravity/skills/vci-skill-cuongbx   # macOS/Linux
cd $env:USERPROFILE\.gemini\antigravity\skills\vci-skill-cuongbx   # Windows

git pull origin master
```

### ✅ Kiểm tra cài đặt thành công

Sau khi cài, mở Antigravity và thử nói:

```
Tạo spec cho tính năng đăng nhập
```

Nếu AI nhận diện skill và bắt đầu hỏi thông tin → **cài đặt thành công!** 🎉

## 📁 Cấu trúc output

```
docs/specs/{module}/{Feature_ID}_{tên}/
├── spec.md          ← PRD 4 level (Auto TOC, Changelog, CR Log)
├── diagrams.md      ← Mermaid: State + Flow + ERD + Sequence
├── dev_guide.md     ← Hướng dẫn implement (BE hoặc FE)
├── test_cases.md    ← BDD + Matrix + Security + Performance
└── test_mapping.md  ← Requirement → Test traceability
```

## ⚡ Tính năng nổi bật

- **Auto Gap Detection** — Tự phát hiện spec thiếu AC, State thiếu Button, Field thiếu Validate
- **Mermaid Diagrams** — State Machine, Screen Flow, ERD, Sequence, Data Flow
- **Scope Change Detection** — Tự tạo Change Request khi spec Approved bị sửa
- **Code-Spec Comparison** — So sánh code implement vs spec → RTM
- **Auto Changelog** — Version + Author + Date + Changes tự động
- **BDD Test Cases** — Từ AC sinh Given/When/Then
- **Security & Performance Tests** — SQL injection, XSS, RBAC, load test
- **Automation Skeleton** — Playwright/Cypress template code
- **PM Dashboard** — Progress Matrix, Scope Alerts, Activity tracking
- **Release Communication** — Email/Slack template cho stakeholders

## 🔧 Sử dụng

Chỉ cần chat với AI bằng ngôn ngữ tự nhiên. Dưới đây là các lệnh mẫu cho từng vai trò:

### 👨‍💼 BA — Tạo & quản lý spec
```
tạo spec cho tính năng nhập kho vật tư
cấu trúc lại meeting notes thành spec
cập nhật spec IMS_NK_01 thêm business rule mới
kiểm tra spec IMS_NK_01 có thiếu gì không
```

### 👨‍💻 Developer — Hướng dẫn implement
```
dev guide backend cho feature nhập kho
dev guide frontend cho feature IMS_NK_01
so sánh code với spec IMS_NK_01
```

### 🧪 QA / Tester — Sinh test cases
```
sinh test cases cho feature IMS_NK_01
sinh test matrix cho nhập kho
tạo automation script cho IMS_NK_01
```

### 📊 PM — Theo dõi & báo cáo
```
ai đang làm gì?
tóm tắt feature nhập kho
báo cáo PMO sprint này
tiến độ dự án hiện tại
```

## 📂 Cấu trúc Skill

```
vci-skill-cuongbx/
├── SKILL.md                              ← Skill instructions (9 modes)
├── README.md                             ← This file
├── resources/
│   ├── prd_template.md                   ← PRD 4-level template
│   ├── mermaid_patterns.md               ← 6 loại diagram patterns
│   ├── gap_detection_rules.md            ← Audit rules + Tech Lead checklist
│   ├── dev_guide_template.md             ← BE (8 sections) + FE (8 sections)
│   ├── test_gen_template.md              ← BDD + Security + Perf + Automation
│   └── pm_report_template.md             ← Track dashboard + PMO report
└── examples/
    └── example_dispatch_order.md          ← Full example output
```

## 📝 Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.1.1 | 2026-03-11 | Cải thiện README: hướng dẫn cài đặt chi tiết, lệnh sử dụng rõ ràng |
| 1.1.0 | 2026-03-11 | Nâng cấp: thêm advanced features, 9 modes hoàn chỉnh |
| 1.0.0 | 2026-03-11 | Initial release — 9 modes, 10/10 all roles |

## 📄 License

MIT

## 👤 Author

**CuongBX** — VCI Team

---

> 💡 **Góp ý & báo lỗi:** Tạo [Issue](https://github.com/Cuongtau/vci-skill-cuongbx/issues) trên GitHub
