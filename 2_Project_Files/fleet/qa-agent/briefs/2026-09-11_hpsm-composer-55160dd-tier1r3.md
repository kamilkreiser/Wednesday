# QA GATE — TIER 1, round 3 (Kam-authorised) — Datasec / HPSM — Policy Composer @ 55160dd

**Kam ruled this round at 14:59:30, verbatim: *"Yes — a small round 3 on the approver guard plus the two same-class Minors, then re-check"*.** **Head under test:** local `main` of `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/6_Policy_Composer` @ `55160dd2cec6ae5eed5a040405e6abf2d2a375aa`. **Range:** `0c3078e..55160dd`, 2 commits: `6d7a178` (tests) and `55160dd` (migration `0005`). NOT pushed; HPSM-light main is `0c3078e`. **There is no round 4 without Kam.**

PRIOR ROUND: round 2 gated `0c3078e8398d016cbbf250712da56585938d734f`, verdict **NO GO** (1 Major, 5 Minor).
ITS REPORT IS ON DISK AT: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-11-composer-0c3078e-tier1r2/`
Findings carried forward and their disposition: **R2-M1** fixed on `55160dd` (builder claim) · **R2-m2** fixed on `55160dd` · **R2-m4** tested on `6d7a178` · **R2-m1, R2-m3, R2-m5** unchanged and in BACKLOG.

## Target, how to reach it, the shared daemon
The same as round 2's brief (`qa-agent/briefs/2026-09-11_hpsm-composer-0c3078e-tier1r2.md`, "Target"), with these changes: check out `55160dd2cec6ae5eed5a040405e6abf2d2a375aa`, plus `0c3078e` for red controls; compose project `policy-composer-qa3`, edge port `18182`; run `scripts/install-hooks.sh` in your clone. Builder evidence (read, never write): `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Architecture/2026-09-10_policy-composer/qa-round3/README.md`.

## THE BUILDER'S CLAIMS — verify each, relay none (READY FOR QA 2026-09-11T05:31:38Z, spf/dkim/dmarc pass)
1. New tests: 7 failed / 66 passed on the `0c3078e` schema; 73/73 at head; all 8 fix-removal mutants go RED; your N2 and N5 SQL are refused at head and still commit at `0c3078e`; your legitimate-lifecycle script runs with 0 errors; clean-clone CI 13/13.
2. **R2-M1, two layers:** `customer_approver_identity_immutable` (forbid change of tenant_id and engagement_id), and `approver_not_last` re-created AFTER DELETE OR UPDATE with the function checking **OLD** on DELETE and UPDATE. The builder found the old `COALESCE(NEW, OLD)` would have checked the DESTINATION engagement.
3. **R2-m2:** `engagement.cloned_from_policy_version_id` and `policy_version.created_from_version_id` are identity-immutable.
4. **R2-m4:** tests for the nil-uuid CHECK, and that pc_app holds no TRUNCATE and no TRIGGER.
5. **Class sweep H1–H7**, measured at both SHAs (`tools/sweep.db.test.ts`): only R2-M1 has the DELETE-only shape.

## DEPARTURES — Tuesday accepted them as shapes; whether they are correct is YOUR question
- **D1:** R2-m4's tests and test f pin properties that already hold at `0c3078e`; their RED is shown on mutants (X-N1, GRANT TRUNCATE, GRANT TRIGGER) with landed proofs.
- **D2 (new):** two round-2 M1 own-tenant controls wrote their references by UPDATE of the columns `0005` freezes, so the builder REWROTE them (for example, an insert of an abandoned version instead). **Check that the rewritten cases still attack what round 2's cases attacked, and did not turn into weaker ones.**

## 🔴 WHAT TO ATTACK FIRST
1. **Your own R2 reproductions (N1–N5) and your round-2 mutants against `55160dd`**, with your own tooling; the builder used its own `mutate.py`.
2. **Did freezing identity columns break legitimate flows?** Re-run your lifecycle, plus approver edits (name, role, email, user_id), clone from a released version, supersede, and abandon. A fix that blocks the product is a Major.
3. **Does the approver guard hold on every path into "zero approvers"?** Delete, move, re-scope tenant, a multi-row UPDATE moving several approvers at once, and deferred-constraint timing within one transaction.
4. **D2:** read the rewritten M1 cases against round 2's intent.

## KNOWN — do NOT report as new (all backlogged; each measured ACCEPTED at both SHAs, so predating round 3)
- **S3-F1** `exception_record.carried_from_exception_id` rewritable (Tuesday ruled it out of this round, citing Kam's "small").
- **S3-F2** `policy.current_released_version_id` can point at its own draft.
- **S3-F3** [spec] a policy's only version can be deleted.
- **S3-F4** [spec] two released versions per policy. **S3-F4b: a version can be INSERTed directly as `released`, with no review and no approvals.** It is backlogged, but **grade its severity yourself in a separate "KNOWN, SEVERITY RE-GRADED" section, if you believe it is higher than the backlog treats it.** That grading is information for Kam, not a round-3 finding.
- **S3-F5** `audit_event` has no FKs. **S3-P1** M1 own-tenant controls that are no-op updates. R2-m1, R2-m3, R2-m5, the caller-supplied PK oracle, the superuser stack (WP4), m6, p1–p3, Q2, Q3.
- Builder NOT TESTED: concurrency races; `0005` over a `0c3078e` database holding data; paths outside pc_app (pc_owner TRUNCATE, `session_replication_role = replica`).

## Output, controls, logistics
Findings-only. FOUND / TESTED / HOW plus an evidence class on every finding; a control for every zero; never `rm`; head readings at start, mid and end. **Report:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-11-composer-55160dd-tier1r3/report.md`. **MAIL YOUR VERDICT** to `tuesday-agent@agentmail.to`, subject `[QA/Datasec-HPSM -> Tuesday] GATE VERDICT — Policy Composer round 3 @ 55160dd (tier 1, round 3)`. Lead with GO, GO WITH FINDINGS or NO GO. **Never `wednesday-agent@`.** You have no inbox.

PROVENANCE:
- Kam's round-3 ruling verbatim | panel relay mail 2026-09-11T04:59:31Z | read 2026-09-11
- head 55160dd, range 2 commits, claims 1-5, D1, D2, sweep, KNOWN list, NOT TESTED | datasec-hpsm READY FOR QA 2026-09-11T05:31:38Z spf/dkim/dmarc pass | read 2026-09-11
- round 2 verdict + report path | QA verdict mail 2026-09-11T00:33:51Z | read 2026-09-11
- F1 ruled out of round | Tuesday ANSWER 05:25:47Z (briefs_staged/2026-09-11_hpsm-s36-answer-plan.md) | read 2026-09-11

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-11 15:32
