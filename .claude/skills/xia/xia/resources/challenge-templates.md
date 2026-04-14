# Challenge Question Templates

6 categories × 3+ templates each. Skill picks based on context từ Phase 1-3.

## 1. Environment

### 1.1 Runtime version
> Source chạy **{runtime} {v_source}**, local **{v_local}**.
> Breaking APIs nào có thể ảnh hưởng?
> - Source answer: _{e.g., uses `Array.prototype.at()` — Node 16+}_
> - Local answer: _{e.g., Node 18 has it ✅}_
> - Risk: 🟢 LOW

### 1.2 OS / Platform
> Source assume **{os_source}**, local **{os_local}**.
> Path separators, signal handling, file locking khác?
> - Risk: 🟡 MED nếu khác OS family (Unix vs Windows)

### 1.3 Runtime target
> Source target **{browser/node/edge/deno}**, local **{...}**.
> Subset API compatible (e.g., no `fs` in browser)?

## 2. Dependencies

### 2.1 Version conflict
> Source dùng `{lib}@{v_source}`, local có `{v_local}`.
> Upgrade, inline, replace?
> - Upgrade risk: _{breaking changes list}_
> - Inline risk: _{bloat, can't patch}_
> - Replace risk: _{feature loss}_

### 2.2 New dep weight
> Port sẽ thêm **{N} new deps**, total bundle **+{X} kb**.
> Worth the feature?
> - Alternative: smaller lib / inline / skip feature

### 2.3 CVE / security
> `{lib}@{version}` có **CVE-{id}** ({severity}).
> - Upgrade to {safe_version}
> - Replace với {alternative}
> - Accept + mitigate

## 3. Async model

### 3.1 Concurrency model mismatch
> Source **{threads/event-loop/goroutines}**, local **{...}**.
> Port thẳng hay rewrite concurrency layer?

### 3.2 Parallelism assumption
> Source `Promise.all([...10 requests])` — fire parallel.
> Local có rate limit 5 req/s — adjust?
> - Risk: 🔴 HIGH nếu không throttle (429 errors)

### 3.3 Single-instance assumption
> Source có in-memory cache — assume single-instance deploy.
> Local multi-instance (K8s N pods) — sẽ break?

## 4. State management

### 4.1 Store pattern mismatch
> Source **{Redux/Vuex/MobX}**, local **{Zustand/Context/Signals}**.
> Rewire pattern hay adapt?
> - Adapt: keep source shape, wrap với local store
> - Rewire: rewrite store integration

### 4.2 State shape
> Source **nested mutation**, local **immutable**.
> Enforce immutability trên ported code?

### 4.3 Persistence
> Source **localStorage**, local **IndexedDB / SQLite**.
> Migration plan cho data đã có?

## 5. License

### 5.1 License compat
> Source **{LICENSE_source}**, project **{LICENSE_local}**.
> {verdict từ matrix}
> - Obligation: attribution, NOTICE, source disclosure?

### 5.2 Attribution placement
> Attribution đặt ở:
> - Inline comment top of file
> - NOTICE file
> - README
> - All of above

### 5.3 Test files license
> Source tests có thể có khác license hoặc copied from framework.
> Port tests hay regenerate?

## 6. Observability

### 6.1 Logging format
> Source **`console.log`**, local **structured JSON (pino/winston)**.
> Map fields?
> - Source: `console.log('user', email)`
> - Local: `logger.info({ user: email }, 'user logged in')`

### 6.2 Metrics
> Source **không có metrics**, local có **Prometheus**.
> Expose counters cho ported feature?

### 6.3 Error handling pattern
> Source `throw new Error(...)`, local `Result<T, E>` pattern.
> Translate:
> - `throw X` → `return err(X)`
> - `try/catch` → `.andThen()` chains

### 6.4 Tracing
> Local có OpenTelemetry — inject spans vào ported code?

## Risk aggregation rules

Per question, user chọn:
- `[a]` Proceed with adjustment (acknowledge, apply)
- `[b]` Accept as-is (acknowledge, skip mitigation)
- `[c]` Abort (stop port)

**Aggregate:**
| Condition | Result |
|---|---|
| 0 HIGH + 0-2 MED | 🟢 **GO** → proceed Plan |
| 1+ HIGH AND user accept all | 🟡 **GO_WITH_EXPLICIT_APPROVE** |
| 1+ HIGH AND user `[c]` | 🔴 **ABORT** |
| User `[c]` any | 🔴 **ABORT** |

## Presentation format

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
> Choose [a/b/c]:
```

## Anti-patterns

- ❌ Generic question không dùng context ("Is this safe?")
- ❌ Force only `[a]` option (remove `[c]` abort)
- ❌ Skip category vì "không relevant" → note "N/A: reason" thay vì ẩn
- ❌ Questions quá dài (>3 dòng) — user skim fail
- ❌ Show Risk before Source/Local context (biased)
