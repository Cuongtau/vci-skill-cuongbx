# 🟦 Zone: vci-cuongbx

Skills hỗ trợ **toàn bộ SDLC** của team phát triển sản phẩm — BA, Dev, QA, Tester, PM, Tech Lead.

---

## 🚀 First-time user — Bắt đầu từ đâu?

### Bước 1: Xác định vai trò

| Tôi là... | Đọc section nào trước |
|---|---|
| 👤 **BA** | [Quickstart §BA](../../../references/quickstart-by-role.md#-ba-business-analyst--90-use-case) — Mode 1/2/3 |
| 💻 **Dev Backend** | [Quickstart §Dev BE](../../../references/quickstart-by-role.md#-dev--backend-mode-5a) — Mode 5A |
| 💻 **Dev Frontend** | [Quickstart §Dev FE](../../../references/quickstart-by-role.md#-dev--frontend-mode-5b) — Mode 5B |
| 🧪 **QA/Tester** | [Quickstart §QA](../../../references/quickstart-by-role.md#-qa--tester-mode-6) — Mode 6 |
| 📊 **PM** | [Quickstart §PM](../../../references/quickstart-by-role.md#-pm--quản-lý-dự-án) — Mode 7/8/9 |
| 🎨 **BA + FE** | [Quickstart §Mockup](../../../references/quickstart-by-role.md#-ba--fe-dev--mockup-mode-10) — Mode 10 |
| 🔍 **Tech Lead** | [Quickstart §Audit](../../../references/quickstart-by-role.md#-tech-lead--audit-mode-4) — Mode 4 |

### Bước 2: Invoke skill

Tại project directory, gõ trong Claude Code / Antigravity:

```
Tạo spec cho tính năng nhập kho vật tư IMS_NK_01
```

Skill sẽ tự kích hoạt (based on `description:` frontmatter). AI đọc SKILL.md + routes đến đúng Mode.

### Bước 3: Cung cấp context

AI sẽ hỏi thông tin tối thiểu nếu thiếu. Để giảm ask-back, cung cấp ngay:
- **Feature ID** (VD: `IMS_NK_01`)
- **Module** (VD: `inventory`)
- **Roles** (VD: Thủ kho, QL kho, Kế toán)
- **Luồng chính** (3-5 bước)

### Bước 4: Review output

- ☐ Đọc **Gap Report** ở cuối output — Critical 🔴 phải xử lý ngay
- ☐ Check `[⚠️ CẦN XÁC NHẬN]` markers — clarify với stakeholder
- ☐ Commit output vào git (nếu đạt)

### Bước 5: Next mode

Workflow chuẩn: Mode 1 (BA) → Mode 5 (Dev) + Mode 6 (QA) + Mode 10 (Mockup) → Mode 4 (Audit) → Mode 8/9 (PM).

📚 **Walkthrough đầy đủ với prompt mẫu + output mẫu:** [references/quickstart-by-role.md](../../../references/quickstart-by-role.md)

---

## 🏢 Dùng cho Enterprise / Team lớn?

Project có **nhiều role cùng làm trên 1 repo** (BA + Dev + QA + PM + Tech Lead + Architect...), cần:

- ✅ **Ownership & RACI** — ai làm gì, ai duyệt
- ✅ **Spec lifecycle** (DRAFT → IN_REVIEW → APPROVED → FROZEN → DEPRECATED)
- ✅ **Approval workflow** với signers
- ✅ **Git branching strategy** per mode (`spec/*`, `feat/*`, `fix/*`)
- ✅ **CODEOWNERS** setup
- ✅ **Handoff protocol** (auto-notify next team)
- ✅ **Jira/Slack/Teams integration**
- ✅ **Compliance & audit** (SOC2, ISO, GDPR)
- ✅ **Cross-feature dependencies + impact matrix**
- ✅ **Onboarding new members**

📚 **Enterprise full guide:** [references/enterprise-workflow.md](../../../references/enterprise-workflow.md)
📚 **Enterprise spec frontmatter template:** [references/templates/spec-frontmatter-enterprise.md](../../../references/templates/spec-frontmatter-enterprise.md)

---

## Bản đồ 11 skills theo vai trò

### 🎯 Meta — bảo trì chính skill vci-skill-cuongbx

| Skill | Khi nào dùng |
|---|---|
| [`skill-creator-ultra/`](./skill-creator-ultra/) | Tạo skill mới / audit + improve skill hiện có. Chạy pipeline 8 phase (Interview → Eval → Iterate). |

### 👤 BA — Business Analyst

| Skill | Dùng khi |
|---|---|
| [`business-analyst/`](./business-analyst/) | Phân tích nghiệp vụ, elicit requirements, viết user story |
| [`brainstorming/`](./brainstorming/) | Ideation — phase 1 của feature mới |
| [`mermaid-expert/`](./mermaid-expert/) | Vẽ State Machine, Screen Flow, ERD chuẩn Mermaid v11 |

### 💻 Dev

| Skill | Dùng khi |
|---|---|
| [`api-documentation-generator/`](./api-documentation-generator/) | Sinh API docs cho Mode 5A (Backend) |
| [`docs-architect/`](./docs-architect/) | Cấu trúc `docs/` end-to-end |

### 🧪 QA / Tester

| Skill | Dùng khi |
|---|---|
| [`acceptance-orchestrator/`](./acceptance-orchestrator/) | Sinh Acceptance Criteria + test flows từ spec |
| [`test-automator/`](./test-automator/) | Sinh automation skeleton (Playwright, k6) |
| [`spec-to-code-compliance/`](./spec-to-code-compliance/) | So sánh spec ↔ code (Mode 4 Audit) |

### 📊 PM / Tech Lead

| Skill | Dùng khi |
|---|---|
| [`product-manager-toolkit/`](./product-manager-toolkit/) | Summary, Track, Report (Mode 7-9) |
| [`plan-writing/`](./plan-writing/) | Viết plan kỹ thuật trong `plans/` |

## Mapping với 10 Modes của `vci-skill-cuongbx`

| Mode | Skill support |
|---|---|
| **Mode 1 Generate** | business-analyst, mermaid-expert, brainstorming |
| **Mode 2 Structure** | business-analyst, brainstorming |
| **Mode 3 Update** | business-analyst |
| **Mode 4 Audit** | spec-to-code-compliance |
| **Mode 5A Backend** | api-documentation-generator, docs-architect |
| **Mode 5B Frontend** | docs-architect |
| **Mode 6 Test Gen** | acceptance-orchestrator, test-automator |
| **Mode 7 Summary** | product-manager-toolkit |
| **Mode 8 Track** | product-manager-toolkit |
| **Mode 9 Report** | product-manager-toolkit |
| **Mode 10 Mockup** | *(dùng zone design skill ở Antigravity)* |

<!-- Generated by Skill Creator Ultra v1.0 -->
