# Enterprise Spec Frontmatter Template

Dùng ở đầu `spec.md` cho enterprise project. Mode 1/2 tự động sinh skeleton này nếu project có `.vci-config.yaml` với `enterprise_mode: true`.

## Full template

```yaml
---
# === Identity ===
feature_id: IMS_NK_01
feature_name: Nhập kho vật tư
module: inventory
slug: nhap_kho
version: 1.0.0          # Spec version (semver)

# === Lifecycle ===
status: DRAFT           # DRAFT | IN_REVIEW | APPROVED | FROZEN | DEPRECATED
created: 2026-04-14
last_updated: 2026-04-14

# === Ownership ===
owner:
  name: Nguyễn Văn A
  role: BA
  email: nguyenvana@company.com
co_owners:
  - name: Trần Thị B
    role: PM

# === Approvers (required for APPROVED status) ===
approvers:
  - name: Nguyễn Văn A
    role: PM
    required: true
    signed: null          # ISO timestamp when signed, null = not yet
    signature: null       # git commit SHA or signature token
  - name: Trần Văn B
    role: Architect
    required: true
    signed: null
  - name: Lê Thị C
    role: QA Lead
    required: true
    signed: null
  - name: Phạm Văn D
    role: Security
    required: false        # Optional, trigger if classification >= Confidential
    signed: null

# === Stakeholders (Informed, no sign-off needed) ===
stakeholders:
  - role: Backend Lead
    team: "@org/backend"
  - role: Frontend Lead
    team: "@org/frontend"
  - role: DevOps
    team: "@org/devops"

# === Project tracking ===
jira:
  id: IMS-123
  epic: IMS-100
  url: https://company.atlassian.net/browse/IMS-123
sprint:
  planned: Sprint-12
  actual: null              # Update post-release
  story_points: 13
release:
  target: v2.4.0
  actual: null
  release_notes: null       # Auto-populated Mode 9

# === Dependencies ===
depends_on:                   # Must be delivered BEFORE this feature
  - IMS_NK_00                 # Previous version
  - IMS_AUTH_01               # Runtime auth dep
blocked_by:                   # External blockers (Jira issues, infra)
  - IMS-456
  - INFRA-78
integrates_with:              # Co-deployed features (parallel work)
  - IMS_NOTIFICATION
  - IMS_REPORTING
impacts:                      # Features affected by this change
  - IMS_XK_01
  - IMS_INVENTORY_VIEW

# === Data classification ===
classification: Internal       # Public | Internal | Confidential | Restricted
data_handled:
  - type: PII
    fields: [user_email, created_by_email]
    classification: Confidential
    retention: 7_years
    regulations: [GDPR, Vietnam-PDP]
  - type: Business
    fields: [warehouse_id, quantity, expiry_date]
    classification: Internal
    retention: 5_years

# === Security flags ===
security_review_required: true
security_findings: []           # Populated post-review

# === Quality gates ===
quality_gates:
  gap_critical: 0                # Must be 0 before APPROVED
  gap_medium: 2                  # Max tolerated
  test_coverage_min: 80          # %
  approver_count: 3              # Min approvers signed
  security_review: passed         # For classification ≥ Confidential

# === Scope & change tracking ===
scope_baseline:                  # Lock at first APPROVED
  acceptance_criteria_count: 12
  business_rules_count: 8
  states_count: 4
  screens_count: 3
  apis_count: 5
scope_current:                   # Auto-updated on change
  ac_count: 12
  br_count: 8
  states_count: 4
  screens_count: 3
  apis_count: 5
change_requests:                 # CR log
  - id: CR_001
    date: null
    type: null                   # Additive | Breaking | Nice-to-have
    reason: null
    impact: null
    approved_by: null

# === Team conventions ===
tags:
  - inventory
  - warehouse
  - workflow
priority: P1                     # P0 (critical) | P1 | P2 | P3
complexity: Medium               # Low | Medium | High | Very High

# === Estimation ===
estimation:
  ba_days: 2
  be_days: 5
  fe_days: 3
  qa_days: 2
  total_days: 12
actual:
  ba_days: null                  # Filled post-completion
  be_days: null
  fe_days: null
  qa_days: null
  total_days: null

# === Automation hooks ===
notifications:
  on_status_change:
    - channel: slack
      webhook: "${SLACK_WEBHOOK_SPECS}"
      mention: "@tech-leads @qa-leads"
  on_cr_created:
    - channel: email
      recipients: [pmo@company.com]
auto_audit:                      # Trigger Mode 4 automatically
  on_code_merge: true
  on_sprint_end: true

# === Metadata ===
language: vi                     # Spec language
readable_by_non_tech: true       # PM/exec can understand
reviewed_external: false         # External review (legal, compliance)
---
```

## Minimal template (for small teams)

```yaml
---
feature_id: IMS_NK_01
feature_name: Nhập kho vật tư
module: inventory
version: 1.0.0
status: DRAFT
owner: { name: BA_Name, role: BA }
approvers:
  - { name: PM_Name, role: PM, required: true, signed: null }
  - { name: TL_Name, role: Tech Lead, required: true, signed: null }
jira: { id: IMS-123 }
sprint: Sprint-12
classification: Internal
---
```

## Field reference

### Identity (required)
- `feature_id`: unique ID theo convention module (VD: `IMS_NK_01`)
- `feature_name`: human-readable name (Vietnamese OK)
- `module`: folder under `docs/specs/`
- `version`: semver spec version (not app version)

### Lifecycle (required)
- `status`: DRAFT/IN_REVIEW/APPROVED/FROZEN/DEPRECATED — enforced by Mode 3

### Ownership (required)
- `owner`: single person responsible — for approval routing
- `co_owners`: backup / secondary ownership

### Approvers (required for APPROVED status)
- `required: true` → blocks APPROVED until `signed` populated
- `signed`: ISO timestamp when approved — auto by Mode 3 CR flow
- `signature`: git SHA of approval commit

### Project tracking (recommended)
- `jira`: link to ticket system — Mode 9 report aggregates
- `sprint`: sprint alignment — Mode 8/9 metrics
- `release`: release targeting — freeze rules

### Dependencies (optional but recommended)
- `depends_on`: must-deliver-first features
- `blocked_by`: external blockers (infra, 3rd-party)
- `integrates_with`: co-deployed siblings
- `impacts`: features this breaks/changes

### Classification (required for regulated data)
- `classification`: access level — determines handling
- `data_handled`: type breakdown — compliance audit uses this
- Regulations: list applicable laws (GDPR, CCPA, HIPAA, PCI-DSS, etc.)

### Quality gates (enforced by Mode 3 before APPROVED)
- `gap_critical: 0` — hard requirement
- `gap_medium: {N}` — team-defined tolerance
- `test_coverage_min` — % for release gate
- `security_review: passed` — for Confidential+

### Scope tracking (auto-managed)
- `scope_baseline`: locked at first APPROVED — reference for CR
- `scope_current`: live counts — Mode 3 diffs against baseline

## Enforcement rules (Mode 3 checks)

1. **DRAFT → IN_REVIEW**: require Level 1-4 complete, gap_critical == 0
2. **IN_REVIEW → APPROVED**: all `required: true` approvers signed
3. **APPROVED → edit**: Mode 3 REFUSE; require CR creation first
4. **FROZEN during release week**: Mode 3 REFUSE all edits except hotfix CR
5. **Classification ≥ Confidential**: require Security approver + security_review == passed

## Migration from basic template

Basic template user → enterprise:
1. Copy current frontmatter
2. Add required enterprise fields: `status`, `approvers`, `classification`
3. Trigger Mode 3 to validate completeness
4. Approvers sign → status to APPROVED

## Integration setup

Để `notifications:` hook chạy:
```bash
# .env.local
SLACK_WEBHOOK_SPECS=https://hooks.slack.com/services/...
TEAMS_WEBHOOK_SPECS=https://company.webhook.office.com/...
JIRA_API_TOKEN=...
```

Mode 3 đọc env → fire webhook khi status change.

## Auto-generated from `.vci-config.yaml`

Project root có `.vci-config.yaml`:
```yaml
enterprise_mode: true
default_approvers:
  PM: @org/pm-team
  Architect: @org/arch-team
  QA_Lead: @org/qa-leads
  Security: @org/security
classification_default: Internal
jira_prefix: IMS
module_teams:
  inventory: "@org/inventory"
  auth: "@org/security"
  billing: "@org/billing @org/finance"
```

Mode 1 đọc file này → pre-populate frontmatter cho spec mới.
