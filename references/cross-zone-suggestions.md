# Cross-zone Suggestions — Compose skill từ các zones

Project có **3 zones**:
- 🟦 **vci** — SDLC team (BA/Dev/QA/PM + design)
- 🟩 **claudekit** — Core dev tools (ck:plan, ck:cook, ck:debug, ck:security...)
- 🟣 **xia** — Feature heist (port từ external repo)

Skill **không tự động invoke** skill khác — user phải gọi explicit. Section này liệt kê **khi nào nên compose**.

---

## 1. Zone BA (Mode 1-4) — Cross-zone hints

### Mode 1 Generate

| Tình huống | Compose với | Zone |
|---|---|---|
| Cần vẽ diagram phức tạp (state machine, ERD, flow) | `mermaid-expert` | vci |
| Ideation trước khi viết spec | `brainstorming` | vci |
| Feature lấy cảm hứng từ open source repo | `xia --compare` hoặc `xia --port` | xia |
| BA chưa rõ business rules | `business-analyst` | vci |
| Sau khi Mode 1 xong → cần plan implement lớn | `ck:plan --hard` | claudekit |

### Mode 2 Structure

| Tình huống | Compose với | Zone |
|---|---|---|
| Notes meeting đa ngôn ngữ, cần dịch nghĩa trước | `ck:research` | claudekit |
| Notes có nhiều ý tưởng rời → cần ideation tổng hợp | `brainstorming` | vci |

### Mode 3 Update

| Tình huống | Compose với | Zone |
|---|---|---|
| Update liên quan scope CR lớn → cần plan lại | `ck:plan` | claudekit |
| Sau update → audit lại spec | `spec-to-code-compliance` | vci |

### Mode 4 Audit

| Tình huống | Compose với | Zone |
|---|---|---|
| Deep code-spec comparison | `spec-to-code-compliance` | vci |
| Security compliance check | `ck:security` (STRIDE+OWASP) | claudekit |
| Full adversarial code review | `code-review` (claudekit) hoặc `code-reviewer` | claudekit |
| Pre-push audit | `codebase-audit-pre-push` | claudekit |

---

## 2. Zone Dev (Mode 5) — Cross-zone hints

### Mode 5A Backend

| Tình huống | Compose với | Zone |
|---|---|---|
| Cần sinh OpenAPI spec | `api-documentation-generator` | vci |
| API docs chi tiết | `api-documentation`, `api-documenter` | vci |
| Implementation plan phức tạp >5 phases | `ck:plan --hard --parallel` | claudekit |
| Deploy backend sau impl | `ck:cook` → `devops-deploy` | claudekit |
| Port utility từ open source (rate limiter, JWT helper, etc.) | `xia --port` hoặc `xia --improve` | xia |

### Mode 5B Frontend

| Tình huống | Compose với | Zone |
|---|---|---|
| Port UI component từ repo khác (auth flow, dashboard) | `xia --port` | xia |
| Design system mới | `frontend-design` (nếu cài) | external |
| A11y audit | `accessibility-compliance-accessibility-audit` | claudekit |
| Performance opt component | `react-component-performance` | claudekit |

---

## 3. Zone QA (Mode 6) — Cross-zone hints

### Mode 6 Test Gen

| Tình huống | Compose với | Zone |
|---|---|---|
| Full acceptance criteria pipeline | `acceptance-orchestrator` | vci |
| Automation skeleton chi tiết hơn | `test-automator` | vci |
| TDD cycle (red/green/refactor) | `tdd-workflow`, `tdd-workflows-tdd-cycle` | claudekit |
| Security test deep | `security-scanning-security-sast` | claudekit |
| Performance test | `k6-load-testing`, `performance-profiling` | claudekit |

---

## 4. Zone PM (Mode 7-9) — Cross-zone hints

### Mode 7 Summary

| Tình huống | Compose với | Zone |
|---|---|---|
| Summary cho nhiều feature cùng lúc | Batch invoke Mode 7 per feature → aggregate manually |
| Executive pitch deck | `frontend-slides` (nếu cài) | external |

### Mode 8 Track

| Tình huống | Compose với | Zone |
|---|---|---|
| Autonomous weekly tracking | `ck:loop` (weekly interval) | claudekit |
| Track cross-project | Batch invoke Mode 8 per project |

### Mode 9 Report

| Tình huống | Compose với | Zone |
|---|---|---|
| Compliance report (SOC2, ISO) | `ck:security audit --compliance` | claudekit |
| Release notes auto-publish | `commit` + `ck:cook` | claudekit |

---

## 5. Zone Shared (Mode 10) — Cross-zone hints

### Mode 10 Mockup

| Tình huống | Compose với | Zone |
|---|---|---|
| UI polish + design system | `ui-ux-designer`, `frontend-design` (nếu cài) | external |
| Port UI từ reference app | `xia --port` | xia |

---

## 6. Post-all-modes — Finalize workflow

Sau khi chạy xong các modes chính, workflow chuẩn:

```
Mode 1/3 (BA) done ──┐
Mode 5A/B (Dev) done ├──► code-review (claudekit) ──► simplify-code ──► commit ──► deploy
Mode 6 (QA) done ────┘                                 (claudekit)    (claudekit) (claudekit)
```

---

## Demo end-to-end — Scenario thực tế

**Context:** Team cần thêm rate limiter vào feature mới (IMS_NK_02 — Nhập kho batch).

### Bước 1: Ideation + Spec (Zone BA)

```
> /brainstorming rate limiter cho batch nhập kho
→ brainstorming skill (vci) đưa ra 3 approaches

> Tạo spec IMS_NK_02 cho batch nhập kho với rate limit
→ Mode 1 Generate — sinh spec 4 level với BR rate limit
→ Gọi mermaid-expert vẽ state machine
```

### Bước 2: Check open source pattern (Zone xia)

```
> /xia --compare https://github.com/tj/node-ratelimiter rate-limiter
→ xia --compare: analysis + decision matrix
→ Output: MIT license ✅, Redis-backed pattern, worth porting
```

### Bước 3: Port + adapt (Zone xia → delegate ck)

```
> /xia --port https://github.com/tj/node-ratelimiter rate-limiter
→ Recon → Map → Analyze → Challenge (6 questions, pass) → Plan (via ck:plan) → Deliver (via ck:cook)
→ Auto attribution header + .xia-manifest.json update
```

### Bước 4: Dev Guide + Test (Zone Dev + QA)

```
> Tạo dev guide backend cho IMS_NK_02
→ Mode 5A — sinh dev_guide.md với rate limiter integration
→ Compose api-documentation-generator cho OpenAPI

> Sinh test cases cho IMS_NK_02
→ Mode 6 Test Gen
→ Compose test-automator sinh Playwright skeleton
→ Compose acceptance-orchestrator validate AC pipeline
```

### Bước 5: Audit + Ship (Zone Dev + claudekit)

```
> Audit IMS_NK_02 — spec ↔ code
→ Mode 4 + spec-to-code-compliance + ck:security scan
→ Gap Report 0 Critical, 1 Medium (add rate limit monitoring)

> /code-review (claudekit)
→ Adversarial review → 0 blocker

> /commit (claudekit)
→ Conventional commit + PR created
```

### Bước 6: PM Track + Report (Zone PM)

```
> Tuần này tiến độ thế nào?
→ Mode 8 Track — dashboard

> Tạo sprint report
→ Mode 9 Report — aggregate git log + CR log
```

**Tổng:** 7 skills từ 3 zones, workflow end-to-end ~2 giờ thay vì 1 tuần thủ công.

---

## Anti-patterns cross-zone

- ❌ Gọi `/ck:brainstorm` từ trong `/xia` — phá phase ownership của xia
- ❌ Dùng Mode 10 (Mockup) mà chưa có Level 4 spec — mockup fail validation
- ❌ Chạy `ck:cook` mà chưa có plan từ `ck:plan` — cook thiếu context
- ❌ Mode 4 Audit mà không có source code path — audit ảo
- ❌ `xia --port` mà project có uncommitted changes >10 files — phá local work

## Anti-duplication guidance

| Tránh dùng cùng lúc | Thay vì | Lý do |
|---|---|---|
| `Mode 1` + `business-analyst` | Mode 1 đã include BA analysis | Duplicate, bloat spec |
| `ck:plan` + Mode 5A details | Mode 5A đã là "plan implement" | Compose: 5A → ck:plan cho phases |
| `xia --compare` + Mode 4 | Mục đích khác nhau | xia = external compare, Mode 4 = spec↔code local |
| `brainstorming` + `multi-agent-brainstorming` | Chỉ 1 | Trùng chức năng |

---

## Quick compose commands

**BA workflow:**
```
/brainstorming → Mode 1 Generate → (optional) /xia --compare {ref-repo} → Mode 4 Audit
```

**Dev workflow:**
```
Mode 5A/B → (optional) /xia --port → ck:plan → ck:cook → code-review → commit
```

**QA workflow:**
```
Mode 6 Test Gen → acceptance-orchestrator → test-automator → (CI auto-run)
```

**PM workflow:**
```
Mode 7 Summary → Mode 8 Track (daily) → Mode 9 Report (sprint end)
```

**Port workflow (xia):**
```
xia --compare → (approve) → xia --improve/--port → ck:plan → ck:cook → Mode 4 audit → Mode 6 test
```
