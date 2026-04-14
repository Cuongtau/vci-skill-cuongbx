# Challenge Framework — Chất vấn trước khi port

Dùng các prompt bên dưới để stress-test quyết định port trước khi nó thành implementation.

## Universal Challenges — Luôn luôn hỏi 5 câu này

1. **Necessity (Cần thiết?):** Ta cần **feature** này, hay chỉ cần **ý tưởng** đằng sau nó?
2. **Simpler alternative (Đơn giản hơn?):** Local codebase có thể đạt 80% value với complexity ít hơn không?
3. **Existing overlap (Đã có sẵn?):** Mình đã có một phần của hành vi này chưa?
4. **Maintenance burden (Ai maintain?):** Ai sẽ own ported code sau port?
5. **Dependency chain (Deps kéo theo?):** Port sẽ thêm gì: deps mới, services, operational costs?

## Architecture Challenges — Cho mọi port non-trivial

| Câu hỏi | Red Flag 🔴 | Green Flag 🟢 |
|---|---|---|
| **Architecture match?** | Paradigm / lifecycle / state model khác | Patterns giống / rất gần |
| **Coupling?** | Trải rộng nhiều module không liên quan | Phần lớn self-contained |
| **New patterns?** | Yêu cầu ORM mới, state manager, auth model | Reuse local patterns |
| **Blast radius?** | Đụng auth, payments, core data flows | Failure isolated |
| **Scaling model?** | Assumption source conflict với local tenancy/scale | Operationally compatible |

## Cross-stack Challenges — Khi `--port` giữa stacks khác

| Source → Local | Câu hỏi cần hỏi |
|---|---|
| TS → Python | Async model khác? GIL issues? Type system bridge (TS interface → pydantic)? |
| Node → Rust | Blocking I/O trong async context? Ownership model? Exception → Result? |
| Go → TS | Goroutines → event loop? Channels → Queue? Error handling idiom? |
| React → Vue 3 | Re-render model? Refs .value? Event handler syntax? |
| Django → FastAPI | ORM (Django ORM vs SQLAlchemy)? Sync → async default? Middleware signature? |

## Compliance Challenges — Khi có regulated data

| Câu hỏi | Trigger condition |
|---|---|
| License compat? | Source license (GPL/AGPL) → Local license (proprietary)? |
| Attribution needed? | MIT/Apache/BSD → cần header + NOTICE? |
| Data classification match? | Source handle PII/PCI/PHI? Local có compliance framework? |
| Secret exposure risk? | Source có hardcoded secrets không? `.env` files? |

## Decision Matrix Template

```markdown
| # | Decision | Cách source | Cách local | Hybrid | Risk | Choice |
|---|---|---|---|---|---|---|
| 1 | Auth | passport.js | existing auth | wrapper | low | local |
| 2 | Schema | 5 tables | 2 tables + join | partial | medium | hybrid |
| 3 | Async | threads | event-loop | throttle wrapper | medium | hybrid |
```

Cột `Choice` có thể là: `source` | `local` | `hybrid` | `abort`.

## Risk Scoring

| Critical Count | Risk Level | Action |
|---|---|---|
| 0-2 | 🟢 LOW | Proceed với port |
| 3-4 | 🟡 MEDIUM | Resolve critical assumptions trước |
| 5+ | 🔴 HIGH | Start với `--compare` hoặc STOP |

**Treat as critical** khi sai sẽ gây:
- Data loss
- Security issue
- >2 ngày rework

## Question Categories — Pick ≥1 từ mỗi category

### 1. Environment
> Source chạy {runtime} {v_source}, local {v_local} — breaking APIs nào?

### 2. Dependencies
> Source dùng `{lib}@{v}`, local `{v_local}` — upgrade / inline / replace?

### 3. Async / Concurrency
> Source {threads/event-loop/goroutines}, local {...} — port thẳng OK?

### 4. State management
> Source Redux, local Zustand — rewire hay adapt?

### 5. License
> Source {LICENSE_src}, project {LICENSE_local} — compat? Attribution?

### 6. Observability
> Source console.log, local structured JSON — map fields?

## Presentation Format

Khi trình bày challenge cho user, dùng format này:

```
┌──────────────────────────────────────────────────────────────┐
│ Q{N} [{category}]: {question}                                │
├──────────────────────────────────────────────────────────────┤
│ Source: {source_answer}                                      │
│ Local:  {local_answer}                                       │
│ Risk:   {🟢/🟡/🔴} {LOW/MED/HIGH} — {reason}                  │
│                                                               │
│ Options:                                                      │
│   [a] {recommended adjustment}                                │
│   [b] Accept as-is                                            │
│   [c] Abort port                                              │
└──────────────────────────────────────────────────────────────┘
> Chọn [a/b/c]:
```

## Aggregate Decision

Sau khi collect answers:
- 0 HIGH + 0-2 MEDIUM → 🟢 **GO** → proceed Plan (Phase 5)
- 1+ HIGH **AND** user accept all → 🟡 **GO_WITH_EXPLICIT_APPROVE**
- 1+ HIGH **AND** user chọn `[c]` → 🔴 **ABORT**
- User chọn `[c]` bất cứ câu nào → 🔴 **ABORT**

## Anti-patterns — KHÔNG làm

- ❌ Generic question không dùng context từ Phase 1-3 ("Is this safe?")
- ❌ Ép user chỉ có option `[a]` (loại bỏ `[c]` abort)
- ❌ Skip category vì "không relevant" — ghi "N/A: reason" thay vì ẩn
- ❌ Questions quá dài (>3 dòng) — user skim fail
- ❌ Show Risk trước Source/Local context (biased framing)
- ❌ Challenge "for show" (chỉ copy paste generic questions)
