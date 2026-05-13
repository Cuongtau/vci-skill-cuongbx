<!-- updated: 2026-05-13 -->

# 🏢 Cộng tác nhiều vai trò (Enterprise) — RACI & Spec Lifecycle

Project có **nhiều vai trò cùng làm trên 1 repo** → cần guardrails tránh xung đột, đảm bảo compliance.

---

## Ma trận RACI (tóm lược)

| Artifact | R (Chủ trì) | A (Duyệt) | C (Tư vấn) | I (Thông báo) |
|---|---|---|---|---|
| `spec.md` L1-2 | PM | Architect | BA | Dev, QA |
| `spec.md` L3-4 | BA | Tech Lead, QA | PM, FE/BE Lead | Tester |
| `dev_guide.md` | Tech Lead | BE/FE Lead | Architect | Dev team |
| `test_cases.md` | QA Lead | QA Manager | BA, Dev | PM |
| `Mockup.tsx` | FE Dev | UX Designer | BA | PM |

### Giải thích RACI

- **R (Responsible — Chủ trì):** người trực tiếp làm ra artifact. Một artifact có thể có nhiều R.
- **A (Accountable — Duyệt):** người chịu trách nhiệm cuối cùng và ký duyệt. Mỗi artifact CHỈ 1 A.
- **C (Consulted — Tư vấn):** được hỏi ý kiến 2 chiều trước khi finalize.
- **I (Informed — Thông báo):** được báo 1 chiều khi artifact hoàn thành / thay đổi.

---

## Vòng đời Spec

```
DRAFT → IN_REVIEW → APPROVED → FROZEN → DEPRECATED
```

### Mô tả từng trạng thái

| Status | Mô tả | Mode được phép | Quyền edit |
|---|---|---|---|
| **DRAFT** | Mới tạo bởi M1/M2 — chưa review | M1, M2, M3 | Free-edit bởi BA |
| **IN_REVIEW** | Đã submit để stakeholders review | M3 (chỉ comment), M4 (audit) | Lock direct edit, comment qua PR |
| **APPROVED** | Đã duyệt, sẵn sàng implement | M4, M5, M6, M10 (đọc spec) | M3 update **PHẢI tạo Change Request** |
| **FROZEN** | Đã release, lên branch protected | M4 audit, M7 summary | Read-only, chỉ hotfix qua CR |
| **DEPRECATED** | Feature retired | M7 summary (historical) | Archive folder |

### Transition rules

- `DRAFT → IN_REVIEW`: PM/Tech Lead trigger review request
- `IN_REVIEW → APPROVED`: A (Accountable) ký duyệt
- `IN_REVIEW → DRAFT`: A từ chối, gửi feedback
- `APPROVED → FROZEN`: tự động khi merge vào release branch
- `APPROVED → IN_REVIEW`: khi có Change Request mở
- `FROZEN → DEPRECATED`: feature flag off, sunset announcement

---

## CODEOWNERS pattern (gợi ý cho `.github/CODEOWNERS`)

```
# Spec files — BA + Tech Lead
docs/specs/**/*.md           @ba-team @tech-leads
docs/specs/**/dev_guide.md   @tech-leads @senior-devs

# Test files — QA Lead
docs/tests/**/*.md           @qa-leads

# Mockup files — UX + FE
src/mockups/**/*.tsx         @ux-designers @fe-leads

# Skill files (this repo)
SKILL.md                     @cuongbx
references/**                @cuongbx
```

---

## Git branching strategy

```
main (protected)
├── develop
│   ├── feature/IMS_NK_01-nhap-kho           ← BA + Dev work
│   ├── feature/IMS_NK_01-test-cases         ← QA work (split branch)
│   └── feature/IMS_NK_01-mockup             ← FE/UX work
├── release/2.7.x                            ← FROZEN
└── hotfix/IMS_NK_01-validation-fix          ← chỉ với Change Request
```

**Quy tắc:**
- Feature_ID phải có trong commit message: `feat(IMS_NK_01): add inbound spec L4`
- Spec branch và Test branch tách riêng → không conflict khi cả 2 đang update
- PR vào `main` bắt buộc 2 reviewers (R + A)

---

## Handoff Notification

Khi artifact chuyển trạng thái, hệ thống/AI bắt buộc notify:

| Transition | Notify channel | Recipients |
|---|---|---|
| Spec `DRAFT → IN_REVIEW` | Email + Slack #spec-review | A + C (theo RACI) |
| Spec `IN_REVIEW → APPROVED` | Email + Slack #engineering | Dev team + QA Lead |
| `dev_guide.md` created | Slack #dev-handoff | BE/FE Lead |
| `test_cases.md` ready | Slack #qa-handoff | QA Lead + PM |
| Mockup published to MockupHub | Slack #design-review | UX Designer + BA |

---

## Enterprise Frontmatter (gợi ý mở rộng)

Cho project lớn (>20 features), spec frontmatter có thể mở rộng:

```yaml
---
feature_id: IMS_NK_01
title: Nhập kho vật tư
status: APPROVED                  # DRAFT | IN_REVIEW | APPROVED | FROZEN | DEPRECATED
version: "1.2.0"
jira_ticket: PROJ-1234
sprint: "Sprint 2026-W18"
zone: transactions
module: inbound
owners:
  ba: nguyen.van.a@vci.vn
  tech_lead: tran.thi.b@vci.vn
  qa_lead: le.van.c@vci.vn
approvers:
  - architect@vci.vn
  - product_manager@vci.vn
compliance:
  - ISO-27001
  - GDPR
related_features: [IMS_AUTH_01, IMS_NK_02]
created: 2026-04-22
last_updated: 2026-05-13
---
```

📚 **Xem chi tiết:** [enterprise-workflow.md](enterprise-workflow.md) cho CODEOWNERS, Git branching, Handoff notification, Enterprise frontmatter (Jira/Sprint/Approvers), Compliance, Onboarding, KPI.
