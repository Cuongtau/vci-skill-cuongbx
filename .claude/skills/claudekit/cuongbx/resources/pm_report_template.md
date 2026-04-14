# PM Report Template

Template cho AI khi sinh báo cáo PM (Mode 8: Track, Mode 9: Report).
Đảm bảo 10/10 cho PM role.

---

## Mode 8: Track Dashboard

```markdown
# 📊 ACTIVITY DASHBOARD

> Generated: {DD/MM/YYYY HH:mm}
> Period: {from_date} → {to_date}
> Project: {Project Name}

---

## 1. Progress Matrix

| Feature ID | Feature Name | Owner | Spec | Dev Guide | Test Cases | Code | Review | Status |
|-----------|-------------|-------|------|-----------|-----------|------|--------|--------|
| IMS_NK_01 | Nhập kho vật tư | BA_A | ✅ v1.2 | ✅ | ✅ | 🔄 70% | ⬜ | In Dev |
| IMS_XK_01 | Xuất kho vật tư | BA_A | ✅ v1.0 | ⬜ | ⬜ | ⬜ | ⬜ | Spec Done |
| IMS_TK_01 | Tồn kho | BA_B | 🔄 draft | ⬜ | ⬜ | ⬜ | ⬜ | Drafting |

**Legend:** ✅ Done | 🔄 In Progress | ⬜ Not Started | ⚠️ Blocked

---

## 2. Recent Activity (from git log + spec changelogs)

### 📝 Spec Changes
| Date | Who | Feature | Change | Version |
|------|-----|---------|--------|---------|
| {date} | {BA name} | {Feature_ID} | {mô tả thay đổi} | {version} |

### 💻 Development Activity
| Date | Who | Feature | Commits | Key Changes |
|------|-----|---------|---------|-------------|
| {date} | {Dev name} | {Feature_ID} | {n} commits | {summary} |

### 🧪 Test Activity
| Date | Who | Feature | Tests Added | Pass Rate |
|------|-----|---------|------------|-----------|
| {date} | {QA name} | {Feature_ID} | +{n} TCs | {X}% |

---

## 3. Scope Alerts ⚠️

| Feature | Baseline | Current | Change % | CRs | Action Required |
|---------|----------|---------|----------|-----|-----------------|
| IMS_NK_01 | 10 BR, 15 AC | 13 BR, 22 AC | +35% | 2 pending | PM review CRs |

### Pending Change Requests
| CR # | Feature | Source | Description | Impact (MD) | Status |
|------|---------|--------|-------------|-------------|--------|
| CR_001 | IMS_NK_01 | 🔵 Khách hàng | Thêm field "Mã PO" | +2 MD | ⏳ Pending |
| CR_002 | IMS_NK_01 | 🟡 Nội bộ | Sửa logic tính VAT | +0.5 MD | ⏳ Pending |

---

## 4. Warnings & Risks 🚨

| Type | Feature | Warning | Severity | Recommendation |
|------|---------|---------|----------|----------------|
| ⏰ Stale | IMS_XK_01 | Spec approved 2 tuần, chưa có dev guide | 🟡 | Assign Dev tạo guide |
| 🧪 Quality | IMS_NK_01 | 3 test cases FAIL | 🔴 | Hotfix trước release |
| 📈 Scope | IMS_NK_01 | Scope tăng 35% | 🟡 | Review CRs, adjust timeline |
| 🔒 Blocked | IMS_TK_01 | Waiting for API từ team B | 🔴 | Escalate to PM team B |
```

---

## Mode 9: Report PMO

```markdown
# 📋 BÁO CÁO TIẾN ĐỘ DỰ ÁN

> **Project:** {Project Name}
> **Sprint/Period:** {Sprint X} ({from} → {to})
> **Author:** {PM Name}
> **Date:** {DD/MM/YYYY}
> **Status:** 🟢 On Track | 🟡 At Risk | 🔴 Delayed

---

## 1. Executive Summary

**Tóm tắt 3-5 câu:**
- Sprint này hoàn thành {X}/{Y} features planned.
- {Feature chính} đã release thành công.
- {Risk chính nếu có}.

### Key Metrics
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Features completed | {n} | {n} | 🟢/🟡/🔴 |
| Bug found / fixed | - | {found}/{fixed} | 🟢/🟡/🔴 |
| Test pass rate | >95% | {X}% | 🟢/🟡/🔴 |
| Scope changes (CRs) | 0 | {n} | 🟢/🟡/🔴 |
| Sprint velocity | {planned SP} | {actual SP} | 🟢/🟡/🔴 |

---

## 2. Feature Detail

### 2.1. Completed Features ✅
| Feature ID | Name | Owner | Spec Ver. | Test Pass | Release Date |
|-----------|------|-------|-----------|-----------|-------------|
| {ID} | {Name} | {Dev} | v{X} | {X}% | {date} |

### 2.2. In Progress Features 🔄
| Feature ID | Name | Owner | Progress | ETA | Blockers |
|-----------|------|-------|----------|-----|----------|
| {ID} | {Name} | {Dev} | {X}% | {date} | {blocker or "None"} |

### 2.3. Not Started ⬜
| Feature ID | Name | Planned Sprint | Reason |
|-----------|------|---------------|--------|
| {ID} | {Name} | Sprint {X} | {Reason if delayed} |

---

## 3. Change Request Summary

| Metric | Count |
|--------|-------|
| Total CRs this period | {n} |
| From Client 🔵 | {n} ({X}%) |
| Internal 🟡 | {n} ({X}%) |
| Bug Fix 🟢 | {n} ({X}%) |
| Approved | {n} |
| Pending | {n} |
| Rejected | {n} |
| Total Impact | +{X} MD |

### CR Detail
| CR # | Feature | Source | Description | Impact | Status |
|------|---------|--------|-------------|--------|--------|
| {CR#} | {Feature} | {🔵/🟡/🟢} | {Desc} | {MD} | {Status} |

---

## 4. Risks & Blockers

| # | Risk/Blocker | Impact | Probability | Owner | Mitigation | Status |
|---|-------------|--------|-------------|-------|-----------|--------|
| 1 | {Description} | 🔴 High | 🟡 Medium | {Name} | {Action} | 🔄 In progress |

---

## 5. Kế hoạch Sprint/Tuần tới

### Planned Features
| Feature ID | Name | Assignee | Priority | Dependencies |
|-----------|------|----------|----------|-------------|
| {ID} | {Name} | {Dev} | {P0/P1/P2} | {deps} |

### Key Milestones
| Date | Milestone | Owner |
|------|-----------|-------|
| {date} | {milestone} | {owner} |

---

## 6. Release Notes

*(Chỉ khi có feature done trong period)*

### Version {X.Y.Z} — {DD/MM/YYYY}

#### ✨ New Features
- **{Feature Name}**: {Mô tả 1-2 câu cho end user}

#### 🐛 Bug Fixes
- **{Bug description}**: {Fix description}

#### ⚠️ Breaking Changes
- {Nếu có}

#### 📝 Known Issues
- {Nếu có}

---

## 7. Release Communication Template

### Email/Slack thông báo cho Stakeholders

```
Subject: [Release] {Project} v{X.Y.Z} — {DD/MM/YYYY}

Kính gửi các bên liên quan,

Chúng tôi vừa release phiên bản {X.Y.Z} với các thay đổi sau:

✨ Tính năng mới:
• {Feature 1}: {mô tả ngắn}
• {Feature 2}: {mô tả ngắn}

🐛 Sửa lỗi:
• {Bug 1}

⚠️ Lưu ý:
• {Breaking change nếu có}
• {Migration steps nếu cần}

📅 Kế hoạch tiếp theo:
• Sprint {X+1}: {feature plans}

Mọi thắc mắc xin liên hệ: {PM contact}

Trân trọng,
{PM Name}
```

---

## 8. Stakeholder Map / RACI

| Stakeholder | Role | Responsible | Accountable | Consulted | Informed | Communication |
|------------|------|-------------|-------------|-----------|----------|---------------|
| {Name} | Product Owner | | ✅ | | | Weekly sync |
| {Name} | Tech Lead | ✅ | | | | Daily standup |
| {Name} | BA | ✅ | | | | As needed |
| {Name} | Dev Team | ✅ | | | | Daily standup |
| {Name} | QA | ✅ | | | | Sprint review |
| {Name} | PMO | | | | ✅ | Bi-weekly report |
| {Name} | Client | | | ✅ | ✅ | Release email |
```
```
