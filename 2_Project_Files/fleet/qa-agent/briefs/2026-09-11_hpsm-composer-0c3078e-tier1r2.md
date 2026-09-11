# QA GATE — TIER 1, round 2 of 2 — Datasec / HPSM — Policy Composer fix round @ 0c3078e

**Head under test:** local `main` of `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/6_Policy_Composer` @ `0c3078e8398d016cbbf250712da56585938d734f`. **Range:** `a06ada3..0c3078e`, 2 commits: `014f112` (tests only) and `0c3078e` (migration `0004`, the bootstrap TEMP revoke, and m2–m5). **NOT pushed** (HPSM-light main is still `a06ada3`); that is deliberate. **Round 2 of 2 under the cap:** a NO GO ships nothing new and goes to Kam as the residue list. There is no round 3 without him.

PRIOR ROUND: round 1 gated `a06ada39c4554655607f658b81fe5d367a1bfe90`, verdict **NO GO** (0 Blocker, 4 Major, 6 Minor, 3 Polish).
ITS REPORT IS ON DISK AT: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-11-composer-a06ada3-tier1/` (report.md + evidence/, including your `mutate.py` and the R1–R4 SQL).
Findings carried forward and their disposition (the builder's claims, to be verified): **M1, M2, M3 and M4 fixed on `0c3078e`** (tests on `014f112`) · **m1** covered by tests · **m2, m3, m4 and m5** fixed on `0c3078e` · **m6, p1–p3, Q2 and Q3** moved to the builder's BACKLOG, unchanged.

## Charter
`/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` — read in full.

## Target, how to reach it, and the shared daemon
Everything in round 1's brief sections 1, 4 and 5 still applies. Read round 1's brief at `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-11_hpsm-composer-a06ada3-tier1.md`. The differences:
- Clone into your OWN `mktemp -d` and check out `0c3078e8398d016cbbf250712da56585938d734f`, **plus `a06ada3` for red controls**. Never write into the original repo or its `.git`.
- Compose project `policy-composer-qa2`, edge port `18181`. Remove only what you start.
- **After cloning, run `scripts/install-hooks.sh` in your clone:** m3's fix makes `up.sh` and CI refuse a clone without the hook. That refusal is part of what you test; running the install step is not a workaround.
- `PC_E8_SOW_TEXT=/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Source_Documents/HPSM_Policy_Composer_2026-09-10/_extracted/sow_e8.md`.
- **The builder's own evidence** (logs, mutant runs, tools): `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Architecture/2026-09-10_policy-composer/qa-round2/README.md`. **Read it; never write there.** It is the builder's claim, not evidence you rely on.

## THE BUILDER'S CLAIMS — verify each, relay none (READY FOR QA mail 2026-09-10T23:59:45Z, spf/dkim/dmarc pass)
1. **Red and green, each in a fresh clone with the product's `scripts/test-db.sh`:** commit A on the `a06ada3` schema gave 18 failed / 40 passed; head's tests on the `a06ada3` schema gave 20 failed / 40 passed; head gave 60/60. **Clean-clone CI at head is GREEN 13/13** (npm ci came from cache).
2. **M1:** 16 single-column FKs are replaced by composite tenant FKs; a structural check (0 offenders at head, 16 at `a06ada3`); a coverage test (every catalog reference has a behavioural case); 26 cross-tenant cases refused with 23503/23514, with 26/26 same-tenant controls accepted; writes into B's released version refused; the existence oracle closed for FKs (B's real id and an unknown id fail identically); A cannot squat B's key.
3. **Label key (same class):** `UNIQUE NULLS NOT DISTINCT (tenant_id, label, version)`.
4. **M2:** the policy is split by command. 0 of 5 tenant attacks change a platform row, B still sees all 3, and own-profile controls pass.
5. **M3:** `forbid_column_change` on the 6 version-scoped tables plus `policy_version`, and `assert_version_editable` checks OLD and NEW. 0 of 8 re-parentings succeed at head.
6. **M4:** every pc function pins `search_path = pc, pg_temp`; `REVOKE TEMPORARY ON DATABASE FROM PUBLIC` is in `bootstrap.sql`. Four shadow attacks were run with TEMP granted back to isolate the pin. Probe X2 claims the revoke binds even after a superuser initialised the temp namespace.
7. **Mutants:** your three survivors now go RED (LIT-M4 2, LIT-M5 1; LIT-M6 stays GREEN because it lands in dead code, and PORT-M6 goes RED 2). One fix-removal mutant per fix goes RED. Secret-scan mutants T1–T3 go RED.
8. **m2–m5:** as listed in the mail and the evidence README.

## DEPARTURES FROM YOUR ROUND-1 FIX SHAPES — the builder's design; Tuesday accepted them as SHAPES only, so whether they are correct is YOUR question
- **(a)** `discovery_answer` binds `(tenant_id, engagement_id, device_group_id)`. **No fix-removal mutant was run for it.**
- **(b)** Brand-profile owner, declarative: a generated `owner_key = COALESCE(tenant_id, nil-uuid)`; `release_artifact.brand_profile_owner` with two CHECKs and a composite FK; `tenant_id <> nil-uuid`; a BEFORE INSERT **fill trigger** that "decides nothing". **No fix-removal mutant was run for the trigger.** Attack it: can a forged owner get through when the trigger fills it, and can nil-uuid be abused?
- **(c)** `assert_version_editable` fails closed on an unseen version, with the same message for another tenant's id and an unknown id.

## 🔴 WHAT TO ATTACK FIRST
1. **Re-run your own round-1 reproductions (R1–R4) and all 7 of your mutants against `0c3078e`**, using your `mutate.py`, not the builder's port. Anything still green is the finding.
2. **What the fix could have broken:** legitimate same-tenant flows. Create an engagement with a policy, edit a draft, submit for review, approve, release, supersede, clone from a released version, and cite a platform brand profile from a release artefact. Each must still work at head. A security fix that blocks the product is a Major.
3. **Frames the builder's sweeps may not cover:** tables or functions added by `0004` itself (do the new functions pin search_path? are new columns covered by the isolation sweeps?), and FKs INTO `brand_profile` or `device_group` beyond the ones named.
4. **Upgrade path, READ ONLY unless cheap:** the builder did not test `0004` against a database already holding `a06ada3` data. If a one-tenant seed at `a06ada3` followed by `0004` is quick, run it; otherwise mark it NOT TESTED with the reason.

## KNOWN — do NOT report as new
- **Residue, ruled BACKLOG by Tuesday at 23:53:36Z:** a caller-supplied uuid primary key is a cross-tenant existence oracle (23505 with B's real id, success with an unused one). MEASURED by the builder on `bridge_registration` (probe X1); READ ONLY for hpsm_instance, customer_approver, policy_version, device_group, validation_run, exception_record, exception_decision, approval, brand_profile, release_artifact and import_artifact. **Verify the builder's measurement if you like; do not grade the class.** If you find a DIFFERENT oracle, that is new.
- The running stack connects as the superuser and applies no migrations (WP4). m6, p1–p3, Q2, Q3, and whether exception_record and local_value_requirement freeze after release are in BACKLOG. m5's regex misses passwords containing `$ : @ /`, quotes or whitespace, or shorter than 6 characters (builder-disclosed). The `.gitleaksignore` and `gitleaks:allow` silencers are still honoured.

## Output, controls, logistics
Findings-only: no commits, no tickets. Every finding carries FOUND / TESTED / HOW and an evidence class (MEASURED AT RUNTIME · PROBED · READ ONLY). Every zero gets a control. Never `rm`. Report head readings at start, mid and end, with the branch beside each SHA.
**Report:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-11-composer-0c3078e-tier1r2/report.md`.
**MAIL YOUR VERDICT** to `tuesday-agent@agentmail.to`, subject `[QA/Datasec-HPSM -> Tuesday] GATE VERDICT — Policy Composer round 2 @ 0c3078e (tier 1, round 2)`. Lead with GO, GO WITH FINDINGS or NO GO. **Never `wednesday-agent@`.** You have no inbox.

PROVENANCE:
- head 0c3078e, range 2 commits, claims 1-8, departures, NOT TESTED | datasec-hpsm READY FOR QA 2026-09-10T23:59:45Z spf/dkim/dmarc pass | read 2026-09-11
- round 1 verdict + report path | QA verdict mail 23:13:38Z + report.md read by Tuesday | read 2026-09-11
- KNOWN residue ruling | Tuesday ANSWER 2026-09-10T23:53:36Z (briefs_staged/2026-09-11_hpsm-s34-answer-pk-residue.md) | read 2026-09-11
- round 2 of 2 cap | learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md | read 2026-09-11

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-11 10:01
