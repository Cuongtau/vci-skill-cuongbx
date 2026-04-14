# Quy trình phát triển sản phẩm VCI — Gate cảnh báo theo Stage

> **Mục đích:** Gợi ý team BA/Dev/QA/PM phối hợp tuần tự, tránh skip stage không cần thiết. AI **warn + hỏi xác nhận**, user có thể override.

---

## 💡 Nguyên tắc khuyến nghị (không cứng)

1. **Khuyến khích tuần tự** — stage 1→2→3→(4‖5‖6)→7→8, skip được nhưng nên có lý do.
2. **Khuyến khích hoàn tất gate trước** — ví dụ spec APPROVED trước khi code; nhưng nếu dự án gấp, Dev có thể bắt đầu với spec DRAFT (AI warn).
3. **Mọi artifact nên reference** — code ↔ dev_guide ↔ spec; test ↔ AC ↔ spec; mockup ↔ L4 UI Spec.
4. **Loopback qua M3 Update + CR khi có thể** — phát hiện vấn đề ở stage sau → nên quay lại Stage 2; sửa trực tiếp → AI warn.

## 🔓 Override mechanism

Khi AI warn về gate, user có các cách bypass:
- Trả lời *"vẫn tiếp tục"* · *"skip check"* · *"tôi biết mình đang làm gì"* · *"override"*
- AI sẽ proceed + ghi log cảnh báo vào output (để audit sau).
- Output có thêm section `⚠️ WARNING OVERRIDE` liệt kê check đã bypass.

---

## 📋 Deep Research Checklist — BẮT BUỘC trước khi viết spec (M1/M2)

BA phải trả lời đủ 10 câu hỏi. Thiếu câu nào → **AI hỏi ngược** trước khi generate:

### 1. Vấn đề nghiệp vụ
- Bài toán thực sự là gì? (không phải "cần tính năng X" mà "vì Y nên cần X")
- Hiện tại đang giải quyết ra sao? (manual? hệ thống cũ? spreadsheet?)
- Pain point cụ thể của ai? (user story format)

### 2. Stakeholders
- Ai bị affected khi triển khai? (users, managers, auditors)
- Ai ra quyết định business? (PM, domain expert)
- Ai sign-off approval? (approvers trong frontmatter)

### 3. Users & Roles
- Những role nào sẽ dùng? (thủ kho, quản lý, kế toán...)
- User journey hiện tại vs target (as-is vs to-be)
- Permission matrix (ai làm được gì ở state nào)

### 4. Gap Analysis
- As-is: hiện trạng thế nào?
- To-be: mục tiêu cụ thể?
- Gap: khoảng cách là gì (functional, technical, data, process)?

### 5. Dependencies
- Feature đã có liên quan? (cross-feature impact)
- API/service phải integrate? (internal + external)
- Data sources nào? (DB nào, external API nào)
- Feature blocker nào chưa làm? (block_by trong frontmatter)

### 6. Edge cases & Error scenarios
- Nghiệp vụ thường fail ở đâu? (dựa trên sự cố đã xảy ra)
- Concurrent user conflict?
- Race condition? Timeout?
- Data inconsistency handling?

### 7. Non-Functional Requirements (NFR)
- Volume expect: số record/giờ, concurrent users?
- SLA: response time, uptime target?
- Security classification: Public / Internal / Confidential?
- Compliance: GDPR, PCI-DSS, SOC2, i18n?

### 8. Constraints
- Thời gian: deadline cứng nào?
- Ngân sách: giới hạn gì?
- Technology stack: ràng buộc framework/language?
- Tài nguyên team: ai làm được?

### 9. Risks
- Nghiệp vụ: decision sai thì hậu quả gì?
- Kỹ thuật: tech debt, migration risk?
- Compliance: vi phạm gì thì phạt gì?
- Mitigation: plan giảm rủi ro?

### 10. Success Metrics
- Đo bằng chỉ số nào? (throughput, error rate, user satisfaction, cost reduction)
- Baseline hiện tại?
- Target sau release?
- Cách đo (analytics event, log query, survey)?

**→ Chỉ khi đủ 10 câu, mới `Mode 1 Generate`. Thiếu → ask-back hoặc `Mode 2 Structure` với `[⚠️ CẦN XÁC NHẬN]`.**

---

## 🛑 Ràng buộc theo Stage — Hard Gates

### Stage 1-2: KHÁM PHÁ & YÊU CẦU (BA)

**Pre-requisites để bắt đầu:**
- ✅ Input: ý tưởng / notes / Jira ticket.
- ✅ Đã research theo [Deep Research Checklist](#deep-research-checklist).

**WARN conditions (WARN + ask confirm sinh spec):**
- 🚫 Chưa trả lời ≥7/10 câu Deep Research → phải ask-back.
- 🚫 Thiếu Feature ID hoặc naming không đúng pattern `{MODULE}_{TYPE}_{NN}`.
- 🚫 Không có roles hoặc user journey rõ ràng.

**Gate chuyển sang Stage 3:**
- ✅ Spec status = `APPROVED`.
- ✅ Đủ approvers sign-off trong frontmatter (min 2: PM + Architect).
- ✅ Gap detection → **0 gap Critical**.
- ✅ Scope Baseline đã lock.

### Stage 3: STAKEHOLDER (PM)

**Pre-requisites:** Spec `APPROVED`.

**WARN:** 🚫 Sinh M7 Summary nếu spec status ≠ `APPROVED`.

**Gate:** ✅ Họp kickoff đã diễn ra, biên bản lưu vào `docs/meetings/`.

### Stage 4: THIẾT KẾ UI (BA + FE)

**Pre-requisites (bắt buộc đủ):**
- ✅ Spec `APPROVED`.
- ✅ Level 4 đầy đủ: UI Spec + Button Matrix + State Machine.
- ✅ Design System component library có sẵn.

**WARN:** 🚫 Mode 10 Mockup WARN + ask confirm nếu thiếu L4/UI Spec/Button Matrix (pre-flight script enforce).

**Gate:** ✅ Design review by UX Designer (comment resolved).

### Stage 5: LẬP TRÌNH (Dev) — **STRICT**

**Pre-requisites (ALL bắt buộc):**
- ✅ Spec `APPROVED` (KHÔNG được code khi spec còn `DRAFT`/`IN_REVIEW`).
- ✅ `dev_guide.md` đã sinh qua M5A/M5B và Dev đã đọc.
- ✅ Nếu FE: Mockup.tsx đã có (Stage 4 pass).
- ✅ Dev confirm hiểu spec (tick checklist "Tôi đã đọc spec L3+L4, BR, API contract").

**WARN conditions:**
- 🚫 **WARN + ask confirm code implementation** nếu spec thiếu API contract hoặc DB schema.
- 🚫 **WARN + ask confirm code** nếu chưa có `dev_guide.md`.
- 🚫 **WARN + ask confirm merge PR** nếu commit message không reference Feature_ID.
- 🚫 Dev tự sửa spec mà không qua M3 Update → **REJECT PR**.

**Gate:** ✅ Code review OK + lint/type-check pass + unit test ≥ 80% coverage.

### Stage 6: CHUẨN BỊ TEST (QA)

**Pre-requisites:**
- ✅ Spec `APPROVED`.
- ✅ Acceptance Criteria đầy đủ trong L4 (≥1 AC/User Story).

**WARN:**
- 🚫 M6 WARN + ask confirm nếu spec thiếu AC.
- 🚫 M6 WARN + ask confirm nếu spec thiếu State Machine hoặc Button Matrix (không sinh được Test Matrix).

**Gate:** ✅ Test plan review by QA Lead + BA.

### Stage 7: QUALITY GATE — **HARDEST**

**Pre-requisites:**
- ✅ Stage 5 + Stage 6 done.
- ✅ Code merged vào branch `feat/{Feature_ID}`.
- ✅ `test_execution.md` đã chạy ≥80% test cases.

**WARN merge vào main nếu:**
- 🚫 Gap Critical > 0 (M4 Audit report).
- 🚫 RTM incomplete (có AC chưa map test).
- 🚫 Test FAILED > 0 chưa có bug ticket + rollback plan.
- 🚫 Security issues Critical chưa resolve.
- 🚫 Performance SLA vi phạm.
- 🚫 Deviation Report chưa approve by Tech Lead.

**Gate:** ✅ Sign-off Tech Lead + QA Lead + Product Owner.

### Stage 8: BÀN GIAO & RELEASE (PM)

**Pre-requisites:**
- ✅ Stage 7 pass với sign-off đầy đủ.
- ✅ All test cases in `test_execution.md` status = PASSED/WARNED (với lý do).
- ✅ Release notes draft qua M9.

**WARN release nếu:**
- 🚫 Còn test WARNED chưa có mitigation plan.
- 🚫 Release note chưa communicate stakeholders.
- 🚫 Rollback plan chưa định nghĩa.

**Gate:** ✅ Release approval → Spec status = `FROZEN`.

---

## 🔁 Loopback — Khi phát hiện vấn đề ở stage sau

**Luật cứng:** KHÔNG được sửa spec trực tiếp ở Stage 5/6/7. PHẢI loopback qua Stage 2 với Change Request:

```
Stage 5 Dev phát hiện spec sai
  ↓
Raise issue → BA mở Mode 3 Update
  ↓
Tạo CR (impact, classification, affected stages)
  ↓
Approvers sign CR
  ↓
Spec update → gap detection → status giữ APPROVED
  ↓
Notify @Dev @QA → họ adjust code/test theo CR
  ↓
Quay lại Stage 5/6 tiếp tục
```

**Classification CR:**
- **Minor** (< 5% scope): 1 approver sign.
- **Major** (5-20% scope): 2 approvers + QA Lead impact review.
- **Critical** (> 20% scope): Steering committee review + re-plan sprint.

---

## 🎯 Enforcement Tool

Pre-flight script tự động check trước khi chạy mode:

```bash
# Check stage prerequisites
python references/scripts/check-mode-prerequisites.py --mode <N> --spec <path>

# Exit codes:
#   0  OK — có thể chạy mode
#   1  WARN — thiếu optional input, vẫn chạy được nhưng output yếu
#   2  FAIL — thiếu required input, WARN + ask confirm chạy
```

Hook `pre-commit` kiểm tra:
- Feature_ID trong commit message.
- Spec reference trong PR description.
- Changelog updated nếu sửa spec.

---

## 📊 Ma trận Stage × WARN rule (tóm lược)

| Stage | Mode | WARN nếu... | Gate qua được |
|---|---|---|---|
| 1-2 | M1/M2/M3 | < 7/10 deep research · thiếu Feature ID · thiếu roles | Spec APPROVED + sign-off + 0 Critical gap |
| 3 | M7 | Spec ≠ APPROVED | Meeting kickoff recorded |
| 4 | M10 | Thiếu L4 / UI Spec / Button Matrix | Design review signed |
| 5 | M5A/5B | Spec ≠ APPROVED · thiếu dev_guide · thiếu API contract · Dev chưa confirm hiểu spec | Code review + test ≥ 80% cov |
| 6 | M6 | Spec thiếu AC · thiếu State Machine | Test plan review signed |
| 7 | M4 | Critical gap > 0 · test FAILED · RTM incomplete · security unresolved | 3-party sign-off (Tech Lead + QA + PO) |
| 8 | M8/M9 | Test WARNED chưa mitigate · release note chưa comm · no rollback plan | Release approved → FROZEN |

---

## 💡 Best practices

- **BA:** Research kỹ TRƯỚC khi mở M1. Đừng generate spec rồi mới hỏi user.
- **Dev:** Đọc spec + dev_guide TRƯỚC khi code. Tạo thói quen "no spec no code".
- **QA:** Sinh test TRƯỚC hoặc SONG SONG với Dev (shift-left testing).
- **PM:** Dùng M8 Track đầu/giữa sprint để phát hiện block sớm.
- **Tech Lead:** Chạy M4 Audit mỗi PR quan trọng, không chờ pre-release.
