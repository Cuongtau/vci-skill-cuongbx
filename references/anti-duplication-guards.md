# Anti-duplication Guards — Hard rules để tránh skill conflict

Các rule bên dưới được AI self-enforce khi detect pattern conflict giữa modes/skills.

---

## Rule 1: Mode 1 vs `business-analyst` skill

**Conflict:** User invoke cả hai cho cùng feature — duplicate BA analysis.

**Rule:**
- **REFUSE** invoke `business-analyst` skill sau khi Mode 1 đã xong
- Mode 1 đã include BA elicitation + documentation
- **Exception**: User explicit request "deep BA analysis trước Mode 1" → OK dùng standalone trước, sau đó chạy Mode 1

**User-facing message khi detect:**
> *"Mode 1 (Generate) đã cover BA analysis cơ bản. Dùng `business-analyst` skill riêng chỉ khi cần elicitation phức tạp (stakeholder interview, process mapping) trước Generate."*

---

## Rule 2: Mode 10 Mockup precondition — PHẢI có Level 4 spec

**Conflict:** User invoke Mode 10 khi spec chưa đủ thông tin UI.

**Rule:**
- **REFUSE** Mode 10 nếu `spec.md` chưa có:
  - Section `## Level 4: Sub-feature`
  - `UI Spec` chi tiết (components, layout, states)
  - `Button Matrix` (ai làm gì ở state nào)
- **Pre-flight check:** `python references/scripts/check-mode-prerequisites.py --mode 10 --spec <path>`

**Exit codes:**
- `0` — OK, proceed
- `1` — WARN (thiếu 1 section, user có thể override)
- `2` — FAIL (hard refuse)

**User-facing message khi FAIL:**
> *"Feature chưa có Level 4 UI Spec. Chạy Mode 1 (Generate) hoặc Mode 3 (Update) để bổ sung UI Spec + Button Matrix trước khi tạo mockup."*

---

## Rule 3: Mode 4 Audit vs `/xia --compare` — DISAMBIGUATION

**Conflict:** Cả 2 đều "so sánh" nhưng scope khác nhau.

**Disambiguation table:**

| Tiêu chí | Mode 4 Audit | `/xia --compare` |
|---|---|---|
| **Scope** | Spec (local) ↔ Code (local) | Local project ↔ External GitHub repo |
| **Mục đích** | Internal consistency, deviation detection | Cross-repo research, pre-port decision |
| **Input** | Path spec.md + source code path | GitHub repo URL |
| **Output** | Gap Report + RTM + Deviation Report | Decision matrix + comparison report |
| **Risk** | Nội bộ, an toàn | External content = untrusted data |

**Decision tree:**
```
User nói "audit feature X" + cung cấp GitHub repo URL  → /xia --compare
User nói "audit feature X" + chỉ có local spec + code  → Mode 4
User không rõ                                            → Hỏi:
  "Anh muốn so với repo external hay audit consistency local?"
```

---

## Rule 4: KHÔNG invoke `/ck:brainstorm` từ Mode 1 hoặc `/xia`

**Reason:** `/ck:brainstorm` tạo separate planning handoff → phá phase ownership.

**Mode 1:** Đã include ideation inside. Alternative:
- Dùng `brainstorming` skill (vci-cuongbx) **TRƯỚC** Mode 1 để ideation
- Sau khi có ideation output, chạy Mode 1

**`/xia`:** Phase 4 Challenge tự handle decision matrix. Alternative:
- Dùng `brainstormer` agent **INLINE** trong Phase 4 (không invoke separate skill)

---

## Pre-flight checks — Chạy trước mỗi mode

Skill check các condition sau trước khi execute:

| Mode | Check | Script |
|---|---|---|
| **Mode 1** | Feature ID chưa tồn tại trong `docs/specs/{module}/` | `--mode 1 --feature-id X --module Y` |
| **Mode 3** | Spec status (APPROVED → require CR, FROZEN → refuse) | `--mode 3 --spec path` |
| **Mode 4** | Spec exists + (optionally) source code path | `--mode 4 --spec path --code-path src/` |
| **Mode 5A/B** | Spec status APPROVED hoặc IN_REVIEW | `--mode 5A --spec path` |
| **Mode 6** | Spec có AC section (required) | `--mode 6 --spec path` |
| **Mode 10** | Spec có Level 4 + UI Spec + Button Matrix | `--mode 10 --spec path` |

**Usage (manual):**
```bash
python references/scripts/check-mode-prerequisites.py --mode 10 --spec docs/specs/auth/IMS_AUTH_01/spec.md
```

**Usage (từ AI invocation):**
AI đọc rule này → tự check điều kiện trước khi bắt đầu mode → nếu fail, REFUSE + inform user.

---

## Enforcement level

| Level | Description | Override? |
|---|---|---|
| 🔴 **REFUSE** | Hard stop — không proceed | Chỉ với explicit flag (VD: `--ack-risk`) |
| 🟡 **WARN** | Surface warning, user confirm | OK với user approve |
| 🟢 **INFO** | Heads-up, proceed anyway | Không cần confirm |

Anti-duplication guards ở **REFUSE** level trừ khi user explicit override.

---

## Examples

### ✅ Correct workflow

```
1. User: "Cần ideation cho feature nhập kho"
   → Use `brainstorming` skill (standalone)

2. User: "Tạo spec IMS_NK_01 với output từ brainstorm trên"
   → Use Mode 1 Generate (vci-cuongbx)

3. User: "Tạo mockup màn nhập kho"
   → Mode 10 pre-flight check → spec có Level 4 ✅ → proceed
```

### ❌ Anti-patterns detected

```
User: "Mode 1 + business-analyst cho feature X"
AI: "Mode 1 đã include BA. Chọn 1: [a] Mode 1 only [b] business-analyst trước rồi Mode 1 [c] Cả 2 riêng biệt cho 2 features khác nhau"

User: "Tạo mockup cho IMS_NEW_01" (spec vừa tạo chưa có Level 4)
AI: "FAIL pre-flight Mode 10: spec thiếu Level 4 UI Spec. Chạy Mode 1 hoặc Mode 3 bổ sung trước."

User: "Audit feature X so với https://github.com/..."
AI: "Có URL external → dùng /xia --compare (không dùng Mode 4). Mode 4 cho local spec ↔ code."

User: "Dùng /ck:brainstorm trong Mode 1"
AI: "Mode 1 đã include ideation. Nếu cần brainstorm sâu → chạy `brainstorming` skill TRƯỚC Mode 1."
```
