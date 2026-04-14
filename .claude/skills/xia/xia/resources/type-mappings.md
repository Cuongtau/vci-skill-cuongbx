# Type System Bridging — Cross-stack mappings

Dùng cho `--port` mode khi source/local khác language.

## TypeScript ↔ Python

| TS construct | Python equivalent |
|---|---|
| `interface User { id: string }` | `class User(BaseModel): id: str` (pydantic) / `@dataclass` |
| `type Status = 'a' \| 'b'` | `Status = Literal['a', 'b']` |
| `string` | `str` |
| `number` | `int` / `float` |
| `boolean` | `bool` |
| `string[]` | `list[str]` |
| `Record<string, T>` | `dict[str, T]` |
| `Partial<T>` | `T \| None` per field (pydantic `Optional`) |
| `Promise<T>` | `Coroutine[Any, Any, T]` / `Awaitable[T]` |
| `async function` | `async def` |
| `await x` | `await x` (syntax OK) |
| `null \| T` | `Optional[T]` / `T \| None` |
| `undefined` | — (không có direct equivalent, dùng `None`) |
| `enum Color { Red, Green }` | `class Color(Enum): RED = 'red'` |
| `class Foo { constructor() {} }` | `class Foo: def __init__(self): ...` |
| `private _x` | `_x` (convention only, không enforce) |
| `readonly x: number` | `Final[int]` (typing_extensions) |

**Gotchas:**
- Python không có truthy `0` / empty string → rewrite boolean checks
- Python dict không preserve insertion order trước 3.7 (target ≥3.7)
- TS `any` → Python `Any` (typing) — avoid both

## TypeScript ↔ Go

| TS | Go |
|---|---|
| `interface User` | `type User struct { ... }` |
| `string` | `string` |
| `number` | `int` / `float64` |
| `T[]` | `[]T` |
| `Record<string, T>` | `map[string]T` |
| `null \| T` | `*T` (pointer, nilable) |
| `async function` | `func` + goroutine + channel |
| `try/catch` | `if err != nil { return ... }` |
| `Promise.all` | `sync.WaitGroup` + goroutines |
| `class Foo` | `type Foo struct` + methods với receiver |
| `enum` | `type X int; const (A X = iota; B)` |

**Gotchas:**
- Go không có exception → rewrite error paths
- Go strict typing — no implicit conversion
- Go no generics trước 1.18 (check target version)

## TypeScript ↔ Rust

| TS | Rust |
|---|---|
| `interface` | `struct` |
| `string` | `String` / `&str` |
| `number` | `i32` / `f64` |
| `null \| T` | `Option<T>` |
| `async function` | `async fn` + tokio/async-std |
| `class Foo` | `struct Foo` + `impl` |
| `try/catch` | `Result<T, E>` + `?` operator |
| `Promise.all` | `futures::join_all` |
| `throw new Error` | `Err(MyError::Kind)` |

**Gotchas:**
- Rust ownership — no direct port of mutable shared state
- Lifetimes — explicit where TS implicit
- No null, no exceptions — paradigm shift

## Python ↔ Go

| Python | Go |
|---|---|
| `class` (with methods) | `struct` + methods |
| `list[T]` | `[]T` |
| `dict[K, V]` | `map[K]V` |
| `async def` | `func` + goroutines |
| `asyncio.gather` | `sync.WaitGroup` |
| `try/except` | `if err != nil` |
| `Optional[T]` | `*T` |
| `@dataclass` | `struct` + tag |

## React ↔ Vue 3 (Composition API)

| React | Vue 3 |
|---|---|
| `useState(0)` | `ref(0)` |
| `useEffect(() => {}, [deps])` | `watchEffect(() => {})` / `watch(deps, ...)` |
| `useMemo` | `computed` |
| `useCallback` | inline function (Vue auto-memoizes) |
| `useContext` | `inject` / `provide` |
| `useReducer` | custom `reactive` object |
| JSX | `<template>` with `v-*` directives |
| `props` interface | `defineProps<{}>()` |
| `useRef` | `ref` (DOM ref) |

**Gotchas:**
- React re-render whole component vs Vue reactive tracking — perf implications
- Vue refs `.value` access — port carefully
- Hooks rules (top-level only) vs Composition API flexibility

## React ↔ Svelte

| React | Svelte |
|---|---|
| `useState(x)` | `let x` (auto-reactive) |
| `useEffect` | `$: { ... }` reactive statement |
| `useMemo` | `$: derived = expensive(x)` |
| Controlled input | `bind:value={x}` |
| `{condition && <X />}` | `{#if condition}<X />{/if}` |
| `{items.map(...)}` | `{#each items as item}...{/each}` |

## Async model compatibility matrix

| Source | Target | Compat | Notes |
|---|---|---|---|
| JS event loop | Python asyncio | ✅ | Similar semantic |
| JS event loop | Go goroutines | ⚠️ | True parallelism — careful |
| JS event loop | Rust tokio | ⚠️ | Ownership + async mix complex |
| Python threads | JS worker_threads | ⚠️ | JS workers are isolated — state share via msg |
| Go goroutines | JS event loop | ❌ | Go concurrency không map — rewrite |
| Go channels | Python asyncio.Queue | ⚠️ | Buffering semantic khác |

## When to use --port vs --improve

Nếu bảng mapping có >50% rows "⚠️" hoặc "❌" → force `--port` mode (rewrite).

Nếu rows đa số "✅" → `--improve` đủ (adapt imports + conventions).
