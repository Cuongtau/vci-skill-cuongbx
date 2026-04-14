# Example 2: `--port` mode — Cross-stack (TypeScript → Python)

## User request

> *"Port rate limiter từ `https://github.com/tj/node-ratelimiter` sang FastAPI project. Em dùng Redis rồi."*

## Command

```
/xia --port https://github.com/tj/node-ratelimiter rate-limiter
```

## Workflow trace

### Step 1: Recon (3 min)

- `ck:repomix` pack `tj/node-ratelimiter@a1b2c3d` → 340 LOC, MIT license
- Locate: `lib/limiter.js` (single-file feature)
- README: Redis-backed rate limiter using sliding window
- License MATCH ✅: MIT → proprietary (local)
- Deps: `redis` (node) → Python `redis-py` EXISTS local ✅
- Cost estimate: 340 LOC × 3 layers × 3.0 cross-lang = **~3 hours**

### Step 2: Map (4 min)

| Source | Status | Local | Action |
|---|---|---|---|
| `Limiter` class | NEW | — | Port as Python class |
| `redis` (node) | REPLACE_WITH_LOCAL | `redis` (python) | Swap client |
| `EVAL` script (Lua) | NEW | — | Port inline (Lua script same) |
| `Promise` pattern | NEW | — | Rewrite to `async def` |
| `options` object | NEW | — | Pydantic BaseModel |

Files to create:
- `src/middleware/rate_limit.py` (core)
- `src/lib/rate_limiter_lua.py` (Lua script embedded)

Files to modify:
- `src/main.py` (add middleware)
- `requirements.txt` (no change, redis-py đã có)

### Step 3: Analyze (5 min)

- Execution flow: request → extract key → Redis EVAL Lua → allow/deny
- Config: `db_index`, `max`, `duration_ms`, `id` (key prefix)
- Async model: Node callbacks → Python `async def` (pattern compatible)
- Security scan: **0 red flags**, **1 yellow** (no key validation — add input sanitize)

### Step 4: Challenge (6 questions, user session)

```
Q1 [Env]: Source Node 14+, local Python 3.11. 
   Any breaking APIs? 
   Source: Node Promise-based
   Local:  Python asyncio ✅ compat
   Risk:   🟢 LOW
   Proceed? [a/b/c]: a

Q2 [Deps]: Source `redis@4.x`, local `redis-py==5.0`.
   Client API compatible?
   Source: `client.multi().incr().expire()`
   Local:  `async with client.pipeline() as pipe: ...`
   Risk:   🟡 MED — API differs, adapt calls
   Proceed? [a/b/c]: a  (adapt)

Q3 [Async]: Source sequential awaits, local async def.
   Any parallelism assumption?
   Source: 1 request = 1 Redis call chain
   Local:  Same, no parallel assumption
   Risk:   🟢 LOW
   Proceed? [a/b/c]: a

Q4 [State]: Rate limiter state in Redis.
   Multi-instance local deploy?
   Source: Assumes shared Redis ✅
   Local:  Same (K8s + Redis cluster)
   Risk:   🟢 LOW
   Proceed? [a/b/c]: a

Q5 [License]: MIT → proprietary.
   Attribution needed?
   Source: MIT requires attribution
   Local:  Will add header + NOTICE
   Risk:   🟢 LOW (standard MIT)
   Proceed? [a/b/c]: a

Q6 [Obs]: Source `console.log`, local structured logger.
   Map events?
   Source: console.log('limit exceeded', key)
   Local:  logger.warn({key, ...}, 'rate limit exceeded')
   Risk:   🟢 LOW
   Proceed? [a/b/c]: a
```

Aggregate: **0 HIGH + 1 MED = 🟢 GO**

### Step 5: Plan (2 min)

`ck:plan --hard` sinh `plans/260414-1430-xia-port-rate-limiter/`:

```
plan.md
phase-01-add-pydantic-config.md
phase-02-port-limiter-class.md
phase-03-embed-lua-script.md
phase-04-fastapi-middleware-wrapper.md
phase-05-tests.md
```

### Step 6: Deliver (~45 min)

- Git branch: `xia/port-rate-limiter-260414-1430`
- `ck:cook` execute 5 phases
- Attribution headers auto-add vào 2 files mới
- Manifest entry:

```json
{
  "id": "port_001",
  "feature_name": "Rate Limiter (sliding window)",
  "source": {
    "repo": "https://github.com/tj/node-ratelimiter",
    "commit": "a1b2c3d",
    "license": "MIT",
    "license_verdict": "MATCH",
    "original_path": "lib/limiter.js"
  },
  "port": {"date": "2026-04-14", "user": "cuongbx@email", "mode": "port", "xia_version": "1.0.0"},
  "impact": {
    "files_created": ["src/middleware/rate_limit.py", "src/lib/rate_limiter_lua.py"],
    "files_modified": ["src/main.py"],
    "loc_added": 287
  },
  "challenges": {"total": 6, "passed": 5, "accepted_risk": 1, "aborted": 0},
  "git": {
    "branch": "xia/port-rate-limiter-260414-1430",
    "final_commit": "ddd444",
    "merged_to_main": false
  },
  "verification": {"security_scan": "pass", "tests_passed": 8, "tests_failed": 0},
  "status": "active"
}
```

## Output to user

```
✅ Port complete: rate-limiter
   Mode: --port (cross-stack TS→Python)
   Branch: xia/port-rate-limiter-260414-1430
   Files: 2 created, 1 modified
   Tests: 8/8 passing (incl. concurrency test)
   Security: 0 red, 1 yellow (key sanitization added)
   License: MIT + attribution header + NOTICE updated
   Time: 58 min total

Review: git diff main...HEAD
Rollback (nếu cần): /xia rollback port_001
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
from typing import Literal


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

## Time: ~62 min total
