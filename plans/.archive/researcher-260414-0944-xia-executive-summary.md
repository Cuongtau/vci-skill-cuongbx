---
name: /xia Skill Research — Executive Summary
description: High-level findings and recommendations for cross-repo porting skill
type: research
---

# /xia Skill: Executive Summary

## What the Research Covered

✅ **Prior art:** git subtree/submodule, Copybara, real-world porting patterns, failure modes  
✅ **Security:** Prompt injection, supply chain threats, guardrails checklist  
✅ **Cross-stack:** TS→Python, React→Vue, Java→Go gotchas + mitigations  
✅ **Decision framework:** Challenge phase template (6 categories, ≥5 questions)  
✅ **License/tracking:** Compatibility matrix, manifest file format (JSON)  

---

## Key Findings

### 1. Copy-Paste Dominates (60-70% of industry practice)
- **Reality:** Most devs manually port. 2-4 hours per feature.
- **/xia opportunity:** Automate boilerplate, highlight risks via Challenge phase.
- **Trade-off:** --copy mode (quick, minimal changes) vs --improve (local refactors).

### 2. Silent Failures Are the Main Risk
| Failure Type | Cause | Prevention |
|---|---|---|
| Diverged copies | No tracking | **Manifest file** (records source, date, changes) |
| Version incompatibilities | Forgot env check | **Challenge phase** (Dependency Alignment Q) |
| Async model mismatch | Missed in analysis | **Challenge phase** (Async Model Q) |
| License violation | No pre-check | **Challenge phase** (License Q) + pre-port scan |

### 3. Untrusted Code ≠ Blocked Code
- **Don't refuse ports.** Instead: sandbox + approve gates.
- No execute, no auto-install. User reviews diffs before commit.
- All outputs labeled with source + attribution.

### 4. Idempotency Enables Re-Porting
- Manifest file tracks: source commit, files ported, local changes made.
- **Next time source updates,** /xia reads manifest → only patches changed files.
- Prevents overwriting user edits.

---

## Critical Design Decisions

### Decision 1: Refuse or Warn?
**Options:**  
A) Strict refusal for GPL→proprietary, incompatible versions  
B) Warn only, let user decide  

**Recommendation:** Use Challenge phase to surface risks. User decides. Log refusals for compliance audit.

### Decision 2: Idempotency Detection
**Options:**  
A) Recompute diffs every time (slow, risky if user modified files)  
B) Use manifest + git fingerprint (safe, skips already-ported files)  

**Recommendation:** Fingerprint-based. If drift detected, ask user before overwrite.

### Decision 3: MVP Scope
**Must have:**
- --compare, --copy, --improve modes
- Challenge phase (≥4 questions)
- Manifest file (.xia-manifest.json)
- No execute, user approval for installs

**Defer to v1.1+:**
- --port mode (full rewrite; AI-intensive)
- Advanced checkpoints & resume
- Secret heuristics

---

## Challenge Phase Template (Proven)

6 question categories, ~30 lines per port:

```
1. Environment Assumptions (Node/Python/Go version)
2. Dependency Alignment (lodash v3 vs v4?)
3. Async Model (Promise vs callback vs sync?)
4. Cross-Cutting (Redux vs MobX?)
5. License & Compliance (MIT vs GPL vs proprietary?)
6. Observability & Rollback (can we detect if port broke prod?)
```

Output: Risk matrix (LOW/MEDIUM/HIGH) + recommended mode (--copy vs --improve vs --port).

---

## Guardrails Checklist

**Fetch Phase:**
- [ ] Shallow clone (`--depth 1`)
- [ ] NO auto-install packages
- [ ] NO code execution
- [ ] Verify GitHub URL exists

**Analysis Phase:**
- [ ] Flag suspicious patterns (process.exit, external fetch, SQL injection)
- [ ] Sandbox regex parsing
- [ ] Separate code summary from recommendations

**Output Phase:**
- [ ] Label all code: source + date + mode
- [ ] User reviews diffs before commit
- [ ] NO auto-commit/push
- [ ] Preserve license headers

**Refused Operations:**
- [ ] NO npm/pip install without explicit approval
- [ ] NO execution of downloaded scripts
- [ ] NO global installs
- [ ] NO credentials in output

---

## Manifest File: Single Source of Truth

```json
{
  "ports": [
    {
      "id": "port_001",
      "feature_name": "Auth Flow",
      "source_repo": "https://github.com/user/auth-service",
      "source_commit": "abc123...",
      "port_date": "2026-04-14",
      "port_mode": "improve",
      "source_license": "MIT",
      "files_ported": ["src/auth/login.ts", ...],
      "changes_made": ["Replaced lodash v3→v4", ...],
      "status": "completed",
      "rollback_commit": "def456..."
    }
  ]
}
```

**Benefits:**
- Idempotency (only update changed files)
- Compliance audit trail
- One-click rollback
- Dependency graph (prevent circular ports)

---

## Open Questions (Product Owner Decision)

1. **Refused port policy:** Strict vs. warning-only?
2. **Idempotency:** Fingerprint hash vs. manifest trust?
3. **Manifest location:** Root `.json` vs. hidden dir vs. external DB?
4. **Checkpoints:** Support mid-port resume, or restart required?
5. **Secret detection:** Heuristics + noise OK, or user review only?

---

## Next Steps

**Phase 1 (Immediate):**
1. Finalize Challenge phase questions (template ready; iterate with product)
2. Define manifest JSON schema (provided above)
3. Implement --compare mode (analysis only, no writes)

**Phase 2 (1-2 weeks):**
1. Implement --copy mode (paste + minimal fix)
2. Build manifest writer + idempotency checks
3. Security sandbox + approval gates

**Phase 3 (2-4 weeks):**
1. Implement --improve mode (copy + local refactor)
2. Advanced license compliance checks
3. Rollback mechanisms

---

**Research Date:** 2026-04-14  
**Research Format:** 4 deep-dive areas + 5 critical open questions  
**Report Location:** `plans/reports/researcher-260414-0944-xia-skill-patterns.md` (full details)
