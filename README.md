# vci-skill-cuongbx

> AI Skill sinh tài liệu PRD/Spec chuẩn `.md` phục vụ toàn bộ team phát triển sản phẩm.

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

| # | Mode | Trigger | Mô tả |
|---|------|---------|--------|
| 1 | **Generate** | "tạo spec", "viết PRD" | Sinh PRD 4 level từ mô tả nghiệp vụ |
| 2 | **Structure** | "cấu trúc lại", "meeting notes" | Biến thông tin rời rạc thành spec chuẩn |
| 3 | **Update** | "cập nhật spec", "sửa spec" | Sửa spec + auto changelog + CR detection |
| 4 | **Audit** | "kiểm tra spec", "so sánh code" | Gap detection + Code-Spec comparison + RTM |
| 5 | **Dev Guide** | "dev guide", "hướng dẫn code" | Sinh hướng dẫn implement (BE hoặc FE) |
| 6 | **Test Gen** | "sinh test", "test cases" | Sinh BDD test + Security + Performance + Automation |
| 7 | **Summary** | "tóm tắt", "overview" | Tóm tắt 1 trang cho PM |
| 8 | **Track** | "tiến độ", "ai đang làm gì" | Dashboard hoạt động từ git + spec |
| 9 | **Report** | "báo cáo PMO", "report" | Báo cáo tiến độ + Release Notes |

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

## 📦 Cài đặt

### Cách 1: Copy thủ công
```bash
# Clone repo
git clone https://github.com/cuongbx/vci-skill-cuongbx.git

# Copy vào thư mục skills
cp -r vci-skill-cuongbx ~/.gemini/antigravity/skills/
```

### Cách 2: Cài từ Skill Creator
```
/install-skill vci-skill-cuongbx
```

## 🔧 Sử dụng

Chỉ cần nói với AI:

```
# BA tạo spec mới
"Tạo spec cho tính năng nhập kho vật tư"

# Dev xin hướng dẫn
"Tạo dev guide backend cho feature nhập kho"

# QA sinh test
"Sinh test cases cho feature IMS_NK_01"

# PM kiểm tra tiến độ
"Ai đang làm gì?"

# Audit spec
"Kiểm tra spec IMS_NK_01 có thiếu gì không"
```

## 📂 Skill Structure

```
vci-skill-cuongbx/
├── SKILL.md                              ← Skill instructions (9 modes)
├── README.md                             ← This file
├── resources/
│   ├── prd_template.md                   ← PRD 4-level template
│   ├── mermaid_patterns.md               ← 6 đồng diagram patterns
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
| 1.0.0 | 2026-03-11 | Initial release — 9 modes, 10/10 all roles |

## 📄 License

MIT

## 👤 Author

**CuongBX** — VCI Team
