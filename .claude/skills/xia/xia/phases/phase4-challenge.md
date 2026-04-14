# Phase 4: 🎯 Challenge — Chất vấn trước khi implement

**Goal:** Ép user face hidden assumptions. Bước này **mandatory** — `--yes` mode cũng KHÔNG skip được.

## Philosophy

Không phải gate để block. Là **forcing function** để user tư duy thay vì copy mù.

> *"Tại sao repo kia làm vậy? Project mình có cần giống không? Nếu khác thì sao?"*

## Compose skills

| Skill | Vai trò |
|---|---|
| `ck:plan --red-team` | Adversarial review of assumptions |
| `code-review adversarial` | Scan ported approach for logical holes |

## 6 Categories (mandatory, generate ≥1 question mỗi category)

### 1. Environment

Target: version compat, platform quirks, runtime constraints.

**Template questions:**
- Source chạy {runtime} {v_source}, local dùng {v_local} — có breaking APIs không?
- Source assume OS = {X}, local chạy trên {Y} — path separators, signal handling, file locking khác?
- Source target {browser/node/edge}, local target {...} — runtime API subset compatible?

### 2. Dependencies

Target: version conflicts, transitive deps, bundle size.

**Template questions:**
- Source dùng `{lib}@{v_source}`, local có `{v_local}` — upgrade, inline, hay skip?
- Port sẽ kéo theo N new deps (tổng bundle +X kb) — có OK không?
- Dep `{lib}` có known CVE — accept, upgrade, hay replace?

### 3. Async model

Target: concurrency semantics khác biệt.

**Template questions:**
- Source dùng threads / workers, local event-loop single-thread — port thẳng an toàn?
- Source `Promise.all` parallel — local throttle? rate limit?
- Source có assumption single-instance (in-memory state) — local multi-instance có break?

### 4. State management

Target: store, context, reducers mismatch.

**Template questions:**
- Source dùng {Redux/Vuex/MobX}, local {Zustand/Context} — rewire pattern hay adapt?
- Source state shape có nested mutation — local immutable-only?
- State persistence: source localStorage, local IndexedDB — migration needed?

### 5. License

Target: legal compat + attribution.

**Template questions:**
- Source {LICENSE_source}, project {LICENSE_local} — copyleft obligations?
- Attribution header format: inline comment, NOTICE file, hay README section?
- Copy tests luôn? (tests có thể có khác license)

### 6. Observability

Target: logs, metrics, tracing mismatch.

**Template questions:**
- Source `console.log`, local structured JSON — map fields?
- Source không có metrics, local Prometheus — expose counters?
- Error handling: source throw Error, local Result<T,E> pattern — translate?

## Decision Matrix Output

Cho mỗi question, present:

```
┌─────────────────────────────────────────────────────────────┐
│ Q3 [Async model]: Source dùng Promise.all song song 10 req, │
│     local có rate limit 5 req/s — có adjust không?          │
├─────────────────────────────────────────────────────────────┤
│ Source answer: Parallel fire 10 request đồng thời           │
│ Local answer:  Throttle với p-limit(5) hoặc rate-limiter    │
│ Risk:          🔴 HIGH — không throttle = 429 từ upstream   │
│                                                              │
│ Options:                                                     │
│   [a] Adjust — add throttling wrapper (recommended)         │
│   [b] Keep source behavior — accept risk                    │
│   [c] Abort — cần discuss với team                          │
└─────────────────────────────────────────────────────────────┘
```

Aggregate risk:
- 0 HIGH + ≤2 MED → **GO** (proceed to Plan)
- 1+ HIGH hoặc ≥3 MED → **REVIEW** (user explicit approve required)
- Blocker detected → **ABORT** (present alternatives)

## Steps

### 4.1. Load context

Input từ Phase 1-3:
- Recon summary (license, deps)
- Map matrix (CONFLICT items)
- Analyze output (implicit assumptions, security flags)

### 4.2. Generate questions

Rule: ≥1 question per category. Nhiều hơn nếu:
- Category có CONFLICT từ Map
- Category có implicit assumption từ Analyze
- Cross-stack mode (`--port`) — tăng Async/State questions

### 4.3. Present + collect answers

For each question, wait for user:
- `[a]` Proceed with adjustment
- `[b]` Accept as-is
- `[c]` Abort

Log answers vào `.xia/cache/challenge-log.md`.

### 4.4. Aggregate decision

Final decision matrix → Plan (Phase 5) hoặc abort.

## Anti-pattern (KHÔNG làm)

- ❌ Ask only technical questions, ignore human concerns (maintenance capacity, team familiarity)
- ❌ Generate generic questions không dùng context từ Phase 1-3
- ❌ Skip category vì "not relevant" — nếu irrelevant thì note "N/A: reason"
- ❌ Force proceed khi user uncertain — present "abort" là valid option

## Output → Phase 5

```yaml
challenges_presented: 7
challenges_passed: 5
challenges_accepted_risk: 2   # user explicit approve
blockers: 0
aggregated_risk: MEDIUM
user_decisions:
  env: "adjust — pin Node 18 in engines"
  deps: "inline utility (avoid new lodash)"
  async: "add throttle wrapper"
  state: "rewire to Zustand"
  license: "add attribution + update NOTICE"
  observability: "map to structured logger"
ready_for_plan: true
```
