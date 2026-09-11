# QA GATE — TIER 1, round 4 (Kam-authorised) — Datasec / HPSM — Policy Composer @ afc10e9

**Kam ruled this round at 08:50:50 AEST, verbatim: *"Yes — round 4 on the commit-time approver hole and the forged-release rule, then re-check"*.** **You are that re-check.** **Head under test:** local `main` of `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/6_Policy_Composer` @ `afc10e98c51505be1f1943335370cf2de3b47d44`. **Range:** `55160dd..afc10e9`, 2 commits: `3cd27d0` (tests and fixtures) and `afc10e9` (migration `0006`). NOT pushed; HPSM-light main is still `55160dd`. **This round runs beyond the two-NO-GO cap on Kam's word, and there is no round 5 without Kam.** Your verdict decides whether `afc10e9` is pushed.

PRIOR ROUND: round 3 gated `55160dd2cec6ae5eed5a040405e6abf2d2a375aa`, verdict **NO GO** (0 Blocker, 1 Major = R3-M1, 2 Minor).
ITS REPORT IS ON DISK AT: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-11-composer-55160dd-tier1r3/report.md`
Carried forward: **R3-M1** fixed on `afc10e9` (builder claim) · **S3-F4b**, which you re-graded Major, fixed on `afc10e9` including the `superseded` path (builder claim) · R3-m1 and R3-m2 unchanged, in BACKLOG.

## Target, how to reach it, the shared daemon
Round 2's brief "Target" section still applies (`/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-11_hpsm-composer-0c3078e-tier1r2.md`), with these changes: check out `afc10e98c51505be1f1943335370cf2de3b47d44`, **plus `55160dd` for red controls**; compose project `policy-composer-qa4`, edge port `18183`; run `scripts/install-hooks.sh` in your clone. Builder evidence (read it, never write there; it is a claim, not evidence you rely on): `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Architecture/2026-09-10_policy-composer/qa-round4/README.md`. **The Docker daemon is shared with other Datasec seats: never stop a container or remove a volume you did not create. The 81 pre-existing volumes are record-only.** Count the daemon's volumes at START and END and report both numbers.

## 🔴 RE-SEED F1 BEFORE THE SCRIPTS THAT READ IT
Your round-3 `F1-fixtures-as-app.sql` writes a version straight to `released`, and `0006` now refuses that: at head it stops at line 37 (`b2_v`, from=draft), psql exit 3 (the builder's measurement). **Ten of your round-3 scripts read F1's ids:** `N1, N2, N3, N5, P-D2, Q1, Q3, R3, R5, U5`. That is Tuesday's own `grep -l "FROM qa_fixture.ids"` over your round-3 `evidence/sql`; it returned exactly these ten, which agrees with the builder's list. **At head, seed F1 through the LEGITIMATE path** (technical review, then a technical and a customer approval bound to that version's `manifest_hash`, then release), and re-run all ten. **A script that still fails after a legitimate re-seed is a finding. A script that fails only because F1 did not seed is not.** Keep the unchanged F1 run as evidence that the forged path is refused. The builder's reading, for you to check: Q1's A9–A11 are the same cases as Q2's G1–G3.

## THE BUILDER'S CLAIMS — verify each, relay none (READY FOR QA 2026-09-11T23:31:21Z, spf/dkim/dmarc pass)
1. **Tests:** 8 RED of 78 at `55160dd`; 86/86 at head; 7 of 7 fix-removal mutants RED; mutant (viii) (pin kept, `EXISTS(engagement)` restored) is EQUIVALENT, with a landed proof. Clean-clone CI 13/13.
2. **R3-M1:** `assert_engagement_has_approver()` sets `pc.tenant_id` to the queuing ROW's tenant (`NEW.tenant_id` on INSERT, `OLD.tenant_id` on DELETE and UPDATE) for its read, restores the transaction's value, and raises when the engagement has no approver. `EXISTS(engagement)` is dropped. `create_engagement_with_policy` raises `ENGAGEMENT_REQUIRES_CUSTOMER_APPROVER` at the call when it wrote 0 approvers.
3. **S3-F4b:** `assert_release_transition()`, BEFORE INSERT OR UPDATE on `policy_version`, fires after `policy_version_guard` **by trigger-name order**. `released` only from `approved`, AND only with an `outcome='approved'` technical and customer approval carrying `NEW.manifest_hash`; `superseded` only from `released`; fails closed on an approval it cannot see. Errors are 23514.
4. **Your reproductions at head:** Q2 G1–G4 refused, G5 refused at the call; C1, C2, C4 refused, C3 commits with 1 approver; K-F4b refused at K1; F1 stops at line 37. At `55160dd` all behave as you recorded.
5. **Class sweep:** 2 deferrable non-internal triggers, both on the pinned function; 12 deferrable internal RI triggers; no SECURITY DEFINER trigger function. A structural test now fails on any new deferred non-FK trigger.
6. **S3-F4's other half** (two released versions on one policy, the builder's P3) is NOT closed. It stays BACKLOG.

## DEPARTURES and the one miss — Tuesday received them; whether they are correct is YOUR question
- **A row-tenant pin instead of the start-of-transaction pin Kam's card recommended.** The builder's argument: a start-of-transaction value written into a `pc.*` setting can be overwritten by `pc_app`, which is the hole itself. Tuesday received this as a design, not as a verified fix.
- **D1:** both release fixtures now take the legitimate path through `releaseThroughApprovals()` in `support.ts`. **D2:** 5 new tests are GREEN at `55160dd` by construction (the two approver controls, the structural check and its positive control, the release control).
- **Q1, Tuesday's ruling (2026-09-11T23:09:59Z):** your `L-legit-lifecycle.sql` was to run UNCHANGED at head, with its refusal at line 64 read as the rule working, plus a copy whose only change routes L6's v2 through review and both approvals. **The builder reports the copy at 0 errors with every label, and the unchanged run at 7 ERROR lines where it had predicted 3.** Its account: lines 64, 67 and 69 as predicted; 70–72 are psql cascades on an unset `:'v3'`; the read-back at 74–80 fails on `:'ce'` and `:'cv'`; line 65 moves `current_released_version_id` to a draft (S3-F2). **Tuesday ruled that any difference is a finding. Grade it.**

## 🔴 WHAT TO ATTACK FIRST
1. **Your own round-3 reproductions and mutants against `afc10e9`,** with your own tooling: Q2 (G1–G5, A-45, C1–C4), K-F4b, the unchanged F1, and your round-3 mutants. Red controls at `55160dd`.
2. **The row-tenant pin, adversarially.** Can `pc_app` change which tenant the guard reads: through the row it queues (its tenant or engagement identity columns), through a second row in the same transaction, or through `SET CONSTRAINTS … IMMEDIATE` mid-transaction followed by more writes (builder NOT TESTED)? Does the restore of `pc.tenant_id` leave the session in a different state (`''` instead of NULL; builder READ ONLY)? Then walk every path into zero approvers from your round-3 §4 again.
3. **The release rule on every path:** INSERT and UPDATE into `released` and into `superseded` from every state; approvals for another hash, rejected, or changes_requested; a superuser; and the **name-order dependency** (what happens when a trigger is added or renamed so that order changes?). **Then: does it break the legitimate product?** Lifecycle, clone from a released version, supersede, abandon. **A fix that blocks the product is a Major.**
4. **The ten F1-dependent scripts after a legitimate re-seed** (section above). No round-3 refusal may regress.
5. **Claims 1 and 5:** plant a new deferred non-FK trigger and show the structural test fails; decide for yourself whether mutant (viii) is truly equivalent.
6. **Clean-clone CI at head.**

## KNOWN — do NOT report as new (all BACKLOG)
S3-F1 · S3-F2 · S3-F3 · **S3-F4's other half (two released versions per policy, P3)** · S3-F5 · R3-m1 · R3-m2 (the `test-db.sh` volume leak) · U-0005 (a migration over a database already holding data) · R2-m1, R2-m3, R2-m5 · the WP4 PK oracle · **R4-L1** (a later customer rejection on the same hash does not block a release) · builder NOT TESTED: concurrency races; owner and superuser paths outside `pc_app` (`session_replication_role`, owner `DISABLE TRIGGER`, owner `TRUNCATE`); pooled connections and the API's tenant handling (WP4); the rest of `release_allowed`.

## Output, controls, logistics
Findings-only. FOUND / TESTED / HOW plus an evidence class (MEASURED AT RUNTIME · PROBED · READ ONLY) on every finding; a control for every zero; never `rm`; head readings at start, mid and end. **Run long commands in the FOREGROUND; never end a turn waiting on a background notice.** **Report:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-12-composer-afc10e9-tier1r4/report.md`. **MAIL YOUR VERDICT** to `tuesday-agent@agentmail.to`, subject `[QA/Datasec-HPSM -> Tuesday] GATE VERDICT — Policy Composer round 4 @ afc10e9 (tier 1, round 4)`. Lead with GO, GO WITH FINDINGS or NO GO. **Never `wednesday-agent@`.** You have no inbox.

PROVENANCE:
- Kam's round-4 ruling verbatim | kam_rulings_today.sh 2026-09-12 (08:50) + panel relay mail 2026-09-11T22:50:52Z | read 2026-09-12
- head afc10e9, range 2 commits (3cd27d0, afc10e9), 55160dd ancestor, porcelain 0, 10 reachable | git rev-parse / rev-list / log on the Composer repo, run by Tuesday s9 | read 2026-09-12
- HPSM-light main == 55160dd | git ls-remote origin on the Composer repo, run by Tuesday s9 | read 2026-09-12
- claims 1-6, D1, D2, the Q1 miss, F1 stopping at line 37, NOT TESTED, R4-L1 | datasec-hpsm READY FOR QA 2026-09-11T23:31:21Z, spf/dkim/dmarc pass | read 2026-09-12
- round-3 verdict NO GO 0/1/2/0 resting on R3-M1 | round-3 report.md lines 3 and 16 | read 2026-09-12
- the ten F1-dependent scripts | grep -l "FROM qa_fixture.ids" over round-3 evidence/sql, run by Tuesday s9 (control: F1-fixtures-as-app.sql names the table) | read 2026-09-12
- the Q1 and Q2 rulings | Tuesday ANSWER 2026-09-11T23:09:59Z (briefs_staged/2026-09-12_hpsm-s38-answer-plan.md) | read 2026-09-12
- port 18183 free, docker responding, E8 SOW text present, qa-round4 README present | lsof + docker info + ls, run by Tuesday s9 | read 2026-09-12

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-12 09:38
