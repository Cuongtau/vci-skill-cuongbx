# Cross-stack Gotchas — Common traps khi port cross-language

Cái list này để Phase 3 Analyze tra cứu. Nếu detect 1 trong các pattern này, tự động raise warning trong Phase 4 Challenge.

## TS → Python

### 1. Truthy / falsy differences
```ts
// TS
if (count) { ... }  // false nếu count=0, ''
```
→ Python `if count:` — giống semantic nhưng:
- `if []:` → False (TS: `if [].length` cần explicit)
- `if 0.0:` → False
- `if None:` → False

**Fix:** Port explicit checks: `if count is not None`, `if len(items) > 0`.

### 2. Mutable default arguments
```python
def f(items=[]):  # ❌ bug — shared across calls
    items.append(1)
    return items
```
**Fix khi port từ TS:** `def f(items=None): items = items or []`

### 3. Async context
```ts
// TS top-level await (Node 14+, ESM)
const data = await fetch(url);
```
→ Python phải wrap trong `async def main():` + `asyncio.run(main())`.

### 4. Type system
- TS structural typing vs Python nominal
- TS optional chaining `a?.b?.c` → Python: `a.b.c if a and a.b else None` (or `getattr`)
- TS union types vs Python Union (typing module)

## Node → Rust

### 1. Blocking ops
Node has blocking variants (`fs.readFileSync`) vs non-blocking. Rust tokio:
- Sync code trong async context = freeze runtime
- Must use `tokio::fs::read` (async) or spawn_blocking

### 2. Ownership + references
```js
const list = [1,2,3];
const copy = list;  // reference
copy.push(4);       // list mutated too
```
Rust:
```rust
let list = vec![1,2,3];
let copy = list.clone();  // deep copy
// or let copy = &list; // borrow
```

### 3. No null, no exceptions
- JS: `try/catch` + `null`
- Rust: `Result<T, E>` + `Option<T>` + `?` operator

## React → Vue 3

### 1. Re-render model
- React: re-render whole component khi state change
- Vue: fine-grained reactivity — chỉ update DOM chạm

**Gotcha:** React memoization (`useMemo`) over-apply → Vue không cần, code cleaner.

### 2. Refs .value
```vue
<script setup>
const count = ref(0);
count.value++;  // ❌ dễ quên .value
</script>
<template>
  {{ count }}  <!-- auto-unwrap -->
</template>
```

### 3. Event handlers
- React: `onClick={handleClick}` — prop
- Vue: `@click="handleClick"` — directive

## Django → FastAPI

### 1. ORM
- Django ORM: model-centric, implicit queries
- FastAPI: thường dùng SQLAlchemy / Tortoise — explicit sessions

### 2. Request handling
- Django: class-based / function views, sync default
- FastAPI: async native, type-driven

### 3. Middleware
- Django: class với `process_request/response`
- FastAPI: ASGI middleware, different signature

## Monolith → Microservices

Không phải cross-language nhưng cross-architecture:

### 1. Shared in-memory state
- Monolith: singleton cache OK
- Microservices: needs Redis/distributed cache

### 2. Transaction boundaries
- Monolith: DB transaction across tables
- Microservices: Saga pattern / 2PC / eventual consistency

### 3. Cross-service calls
- Monolith: direct function call
- Microservices: HTTP/gRPC + retry + circuit breaker

## SQL → NoSQL

### 1. Joins
- SQL: `JOIN` at query time
- NoSQL: denormalize at write time, duplicate data

### 2. Transactions
- SQL: ACID
- NoSQL: varies (MongoDB multi-doc tx 4.0+, DynamoDB scoped)

### 3. Schema evolution
- SQL: migrations
- NoSQL: versioned documents + app-side migration

## Signal handlers

- Node: `process.on('SIGTERM')`
- Python: `signal.signal(signal.SIGTERM, handler)`
- Go: `signal.Notify(chan, syscall.SIGTERM)`
- Rust: `tokio::signal::unix::signal(SignalKind::terminate())`

Port gotcha: semantics similar, syntax different — straightforward.

## Environment variables

- Node: `process.env.X` — string or undefined
- Python: `os.environ['X']` — KeyError if missing, `os.environ.get('X')` safer
- Go: `os.Getenv("X")` — empty string if missing
- Rust: `std::env::var("X")` — Result

**Port rule:** Always add explicit validation + default + type cast. Never trust env.

## Time / Date

- JS: `Date` (mutable, milliseconds since epoch)
- Python: `datetime` (timezone aware cần explicit tzinfo)
- Go: `time.Time` (immutable, timezone-aware)
- Rust: `chrono` crate (ecosystem split — std lib có `std::time`)

**Port gotchas:**
- Timezone assumptions
- Locale-dependent formatting
- Leap seconds (rare but real)

## Error handling pattern table

| Lang | Idiom |
|---|---|
| JS/TS | `try/catch` + `throw Error` |
| Python | `try/except` + `raise Exception` |
| Go | `if err != nil { return err }` |
| Rust | `Result<T, E>` + `?` |
| Swift | `do/try/catch` |

Cross-lang port of error paths needs careful review — paradigm shift.

## Detection rules for `/xia`

Phase 3 Analyze scans source cho patterns sau, raise flag:

| Pattern | Flag |
|---|---|
| `eval()` hoặc `Function()` constructor | 🔴 RED — malicious risk |
| `curl ... \| bash` | 🔴 RED |
| `process.env.*` without validation | 🟡 YELLOW |
| Hardcoded URLs `http://...` | 🟡 YELLOW |
| Signal handler in source | 🟡 YELLOW — platform-specific |
| In-memory state (Map, Set singleton) | 🟡 YELLOW — multi-instance? |
| Direct DB connection (no pool) | 🟡 YELLOW — perf concern |
| Synchronous I/O in async context | 🟡 YELLOW |
