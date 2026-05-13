<!-- updated: 2026-05-13 -->

# 📁 Folder Convention v2.7.0 — Tách Spec vs Tests vs Templates

**QUAN TRỌNG:** Từ v2.7.0, **spec** và **test artifacts** tách thành 2 cây thư mục độc lập để BA/Dev không đụng Tester và ngược lại.

---

## Cấu trúc đầy đủ

```
docs/
├── specs/                                  ← 🟦 BA + Dev
│   └── {zone}/{module}/{Feature_ID}_{tên}/
│       ├── README.md                       (index features trong module)
│       ├── {Feature_ID}_List.md            (L4 spec)
│       ├── {Feature_ID}_Detail.md
│       ├── {Feature_ID}_Create.md
│       ├── {Feature_ID}_Update.md
│       └── dev_guide.md                    (M5A/M5B output)
│
├── tests/                                  ← 🟨 QA + Tester
│   └── {zone}/{module}/{Feature_ID}_{tên}/
│       ├── test_cases_{Feature_ID}_List.md (M6 output, per-screen)
│       ├── test_cases_{Feature_ID}_Detail.md
│       ├── test_mapping.md                 (RTM — gộp cả feature)
│       ├── test_execution.md               (Execution Dashboard — gộp cả feature)
│       ├── gap_detection_report_{ID}.md    (M4 output khi chạy QA audit)
│       └── test_cases_{Feature_ID}_{screen}_screenshoot/
│           ├── TC_01_pass.png
│           └── TC_02_fail_bugXYZ.png
│
└── templates/                              ← 🟪 Shared — copy từ skill khi init project
    ├── test-execution-template.md          (cloned từ skill)
    ├── prd-template.md
    └── dev-guide-template.md
```

---

## Định nghĩa Zone & Module

**Zone** = nhóm domain cấp 1: `master_data` · `transactions` · `transfer` · `reports` · `auth` ...

**Module** = subdomain trong zone: `items` · `warehouses` · `inbound` · `outbound` · `handover` ...

---

## Quy tắc áp dụng theo Mode

| Mode | Output đi vào | Ghi chú |
|---|---|---|
| M1/M2/M3 Spec | `docs/specs/{zone}/{module}/{Feature_ID}_{tên}/` | Spec chia theo màn hình (List/Detail/Create/Update/Import) |
| M4 Audit | Gap Report ở `docs/tests/.../gap_detection_report_{ID}.md` (nếu audit từ QA lens) hoặc inline reply |
| M5 Dev Guide | `docs/specs/{zone}/{module}/.../dev_guide.md` | Đi kèm spec, không tách vì Dev đọc cùng lúc |
| M6 Test Gen | `docs/tests/{zone}/{module}/{Feature_ID}_{tên}/` | Per-screen test_cases + shared test_mapping + shared test_execution |
| M10 Mockup | `src/mockups/features/{zone}/{module}/...` | Không vào `docs/` |

---

## Tại sao tách?

- **QA/Tester có branch riêng** (`Tester` branch) — khi restructure test không conflict với Dev đang update spec.
- **CODEOWNERS rõ ràng** — `docs/specs/**` owner là BA/Tech Lead, `docs/tests/**` owner là QA Lead.
- **Index riêng** — `docs/specs/README.md` cho dev/BA nhìn scope, `docs/tests/README.md` cho QA nhìn coverage + pass rate.
- **Search không nhiễu** — grep "TC_" chỉ ra test, grep "BR_" chỉ ra spec.

---

## Migration từ structure cũ (`docs/features/{module}/{feature}/`)

Dùng script: [scripts/migrate-split-specs-tests.sh](scripts/migrate-split-specs-tests.sh) — `git mv` tự động tách file theo pattern `test_cases*.md` / `test_mapping*.md` → `tests/`, còn lại → `specs/`.

**Cách dùng:**

```bash
cd /path/to/project
./migrate-split-specs-tests.sh --dry-run .   # preview
./migrate-split-specs-tests.sh .              # thực thi
```
