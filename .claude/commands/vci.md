---
name: vci
description: |
  Sinh tài liệu PRD/Spec chuẩn .md cho team SDLC. 10 modes chia 5 zones vai trò
  (BA/Dev/QA/PM/Shared). Auto-route theo trigger keywords. Pre-flight checks +
  anti-duplication guards. Dùng khi user nói "tạo spec", "dev guide", "test cases",
  "tiến độ", "báo cáo PMO", "mockup", v.v.
argument-hint: "[mode] [feature description or spec path]"
---

# /vci — VCI SDLC Skill Router

Load skill `vci-skill-cuongbx` từ repo này. Route tới đúng mode dựa trên `$ARGUMENTS`.

## Quick routing

| Trigger trong $ARGUMENTS | → Mode |
|---|---|
| "tạo spec / viết PRD" | Mode 1 Generate |
| "meeting notes / cấu trúc" | Mode 2 Structure |
| "cập nhật / sửa spec / CR" | Mode 3 Update |
| "audit / so sánh code" | Mode 4 Audit |
| "dev guide / implement" | Mode 5A (BE) / 5B (FE) |
| "test cases / BDD / UAT" | Mode 6 Test Gen |
| "tóm tắt / summary" | Mode 7 Summary |
| "ai đang làm gì / tiến độ" | Mode 8 Track |
| "sprint report / PMO" | Mode 9 Report |
| "mockup / vẽ UI" | Mode 10 Mockup |

## Usage examples

```
/vci tạo spec cho feature nhập kho vật tư IMS_NK_01
/vci dev guide backend cho IMS_AUTH_01
/vci sinh test cases cho IMS_AUTH_01
/vci ai đang làm gì?
/vci tạo mockup màn đăng nhập
```

## Behavior

1. **Read main SKILL.md:** `SKILL.md` ở root repo (hoặc `~/.claude/skills/vci-skill-cuongbx/SKILL.md` nếu installed global)
2. **Parse $ARGUMENTS** → detect mode qua decision tree
3. **Pre-flight check** (nếu Mode 1/3/4/5A/5B/6/10): chạy `references/scripts/check-mode-prerequisites.py`
4. **Execute mode workflow** theo instructions trong SKILL.md
5. **Output:** `docs/specs/{module}/{Feature_ID}_{slug}/{spec|dev_guide|test_cases|...}.md`

## Compose với zones khác

- Cần diagram phức tạp → `/claudekit mermaid-expert`
- Port feature external → `/xia --compare {repo}`
- Implementation sau Mode 5A → `/claudekit plan` → `/claudekit cook`
- Ship code → `/claudekit code-review` → `/claudekit commit`

## Anti-duplication guards

- ❌ KHÔNG gọi Mode 1 + `business-analyst` cho cùng feature
- ❌ KHÔNG Mode 10 nếu spec thiếu Level 4
- ❌ KHÔNG confuse Mode 4 với `/xia --compare` (khác scope: local vs external)

📚 **Full guide:** [SKILL.md](../../SKILL.md) · [references/quickstart-by-role.md](../../references/quickstart-by-role.md)

$ARGUMENTS
