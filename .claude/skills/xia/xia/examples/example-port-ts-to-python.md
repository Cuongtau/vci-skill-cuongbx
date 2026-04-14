# Ví dụ: `--port` mode — Cross-stack (TypeScript → Python)

## User request

> *"Port rate limiter từ `https://github.com/tj/node-ratelimiter` sang FastAPI project. Em dùng Redis rồi."*

## Lệnh

```
/xia --port https://github.com/tj/node-ratelimiter rate-limiter
```

## Trace workflow

### Step 1: Recon (3 phút)

- `ck:repomix` pack `tj/node-ratelimiter@a1b2c3d` → 340 LOC, license MIT
- Locate: `lib/limiter.js` (single-file feature)
- README: Redis-backed rate limiter dùng sliding window
- License check: **MATCH ✅** (MIT → proprietary local)
- Deps: `redis` (node) → Python `redis-py` **EXISTS** local ✅
- Ước tính cost: 340 LOC × 3 layers × 3.0 (cross-lang factor) = **~3 giờ**

### Step 2: Map (4 phút)

| Source | Status | Local equivalent | Action |
|---|---|---|---|
| `Limiter` class | NEW | — | Port thành Python class |
| `redis` (node client) | REPLACE_WITH_LOCAL | `redis-py` | Swap client |
| `EVAL` script (Lua) | NEW | — | Port inline (Lua script giữ nguyên) |
| `Promise` pattern | NEW | — | Rewrite thành `async def` |
| `options` object | NEW | — | Pydantic BaseModel |

**Files to create:**
- `src/middleware/rate_limit.py` (core logic)
- `src/lib/rate_limiter_lua.py` (Lua script embedded)

**Files to modify:**
- `src/main.py` (add middleware)
- `requirements.txt` (no change — redis-py đã có)

### Step 3: Analyze (5 phút)

- **Execution flow**: request → extract key → Redis EVAL Lua → allow/deny
- **Config**: `db_index`, `max`, `duration_ms`, `id` (key prefix)
- **Async model**: Node callbacks → Python `async def` (pattern compatible)
- **Security scan**: 0 red flags, **1 yellow** (thiếu key validation — sẽ add input sanitize)

### Step 4: Challenge (6 câu, user session)

```
Q1 [Environment]: Source Node 14+, local Python 3.11.
    Có breaking APIs nào không?
    Source: Node Promise-based
    Local:  Python asyncio ✅ compat
    Risk:   🟢 LOW
    Proceed? [a/b/c]: a

Q2 [Dependencies]: Source `redis@4.x`, local `redis-py==5.0`.
    Client API có compatible không?
    Source: client.multi().incr().expire()
    Local:  async with client.pipeline() as pipe: ...
    Risk:   🟡 MED — API differs, cần adapt calls
    Proceed? [a/b/c]: a  (adapt)

Q3 [Async]: Source sequential awaits, local async def.
    Có parallelism assumption nào không?
    Source: 1 request = 1 Redis call chain
    Local:  Same, no parallel assumption
    Risk:   🟢 LOW
    Proceed? [a/b/c]: a

Q4 [State]: Rate limiter state trong Redis.
    Local multi-instance deploy chứ?
    Source: Assume shared Redis ✅
    Local:  Same (K8s + Redis cluster)
    Risk:   🟢 LOW
    Proceed? [a/b/c]: a

Q5 [License]: MIT → proprietary.
    Cần attribution không?
    Source: MIT requires attribution
    Local:  Sẽ add header + NOTICE file
    Risk:   🟢 LOW (standard MIT)
    Proceed? [a/b/c]: a

Q6 [Observability]: Source `console.log`, local structured logger.
    Map events ra sao?
    Source: console.log('limit exceeded', key)
    Local:  logger.warn({key, ...}, 'rate limit exceeded')
    Risk:   🟢 LOW
    Proceed? [a/b/c]: a
```

**Aggregate risk:** 0 HIGH + 1 MEDIUM = 🟢 **GO**

### Step 5: Plan (2 phút) — Delegate `/ck:plan`

`ck:plan --hard` sinh `plans/260414-1430-xia-port-rate-limiter/`:

```
plan.md
phase-01-add-pydantic-config.md
phase-02-port-limiter-class.md
phase-03-embed-lua-script.md
phase-04-fastapi-middleware-wrapper.md
phase-05-tests.md
```

### Step 6: Deliver — Delegate `/ck:cook`

```text
Plan ready at ./plans/260414-1430-xia-port-rate-limiter/plan.md.
To implement, run /ck:cook ./plans/260414-1430-xia-port-rate-limiter/plan.md.

Source manifest: tj/node-ratelimiter@a1b2c3d (MIT)
Source anatomy: 3 layers (core, state/Redis, config)
Dependency matrix: 1 NEW (Limiter class), 1 REPLACE (redis client), 3 EXISTS
Decision matrix: Prefer async def, adapt Redis pipeline, Pydantic config
Risk score: 🟢 LOW (1 MED accepted)
```

## Ported code sample

```python
"""
Adapted from tj/node-ratelimiter@a1b2c3d
License: MIT
Original: lib/limiter.js
Ported: 2026-04-14 by /xia (mode: port)
"""

from __future__ import annotations
from pydantic import BaseModel
from redis.asyncio import Redis


class LimiterConfig(BaseModel):
    id: str
    max: int
    duration_ms: int = 3600_000
    db_index: int = 0


class Limiter:
    """Sliding-window rate limiter backed by Redis."""

    LUA = """
    local count = redis.call('INCR', KEYS[1])
    if count == 1 then redis.call('PEXPIRE', KEYS[1], ARGV[1]) end
    return count
    """

    def __init__(self, redis: Redis, config: LimiterConfig):
        self._redis = redis
        self._cfg = config

    async def get(self, key: str) -> dict[str, int]:
        full_key = f"limit:{self._cfg.id}:{key}"
        count = await self._redis.eval(self.LUA, 1, full_key, self._cfg.duration_ms)
        return {
            "total": self._cfg.max,
            "remaining": max(0, self._cfg.max - count),
            "reset": await self._redis.pttl(full_key),
        }
```

## Tổng thời gian: ~62 phút

- Recon: 3 min
- Map: 4 min
- Analyze: 5 min
- Challenge: 8 min (6 questions + user decisions)
- Plan: 2 min (delegate ck:plan)
- Deliver: ~40 min (ck:cook execute)
