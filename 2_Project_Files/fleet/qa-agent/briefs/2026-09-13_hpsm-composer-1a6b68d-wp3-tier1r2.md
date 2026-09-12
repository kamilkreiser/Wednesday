# QA GATE — TIER 1, round 2 of 2 — Datasec / HPSM — Policy Composer WP3 rules engine @ 1a6b68d

**This is WP3 round 2 of 2 under the two-NO-GO cap.** If this round returns NO GO, the closed instances ship and the residue is ticketed. There is no round 3 without Kam. Kam reviews the platform on Monday 2026-09-14.

**Head under test:** `1a6b68d793b60dbbfa227f35464725790714f42b` on local `main` of `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/6_Policy_Composer`, the engine as `packages/engine` and `packages/canonical`. **Range since your round 1:** `0523193..1a6b68d` is 61 commits, most of them WP4/WP5 (gated in a parallel session); 15 files under `packages/engine` and `packages/canonical` changed. NOT pushed; HPSM-light `main` is `afc10e9`.

PRIOR ROUND: round 1 gated `052319342974fc05aabdf056da73558182b871f0`, verdict **NO GO** (0 Blocker, 7 Major, 5 Minor, 3 Polish).
ITS REPORT IS ON DISK AT: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-12-composer-0523193-wp3-tier1/report.md`
Carried forward: W3-M1…M6 claimed fixed; W3-m1 claimed covered by killer tests; W3-M7 and W3-m2…m5 declared NOT fixed; W3-p1…p3 BACKLOG.

## Target, how to reach it, the shared daemon
- **Your round-1 setup applies:** clone into your own `mktemp -d`, check out `1a6b68d…` plus `052319342974…` for red controls, `scripts/install-hooks.sh`.
- **CI:** `PC_E8_SOW_TEXT=/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Source_Documents/HPSM_Policy_Composer_2026-09-10/_extracted/sow_e8.md` set explicitly. Compose project `policy-composer-qa-wp3r2`, edge port **18980**.
- **🔴 A parallel gate is running** (WP4+WP5, edge 18880, compose project `policy-composer-qa-wp45`), and the builder's `pc-lane-a` stack is on 18580. **Touch neither.** Count volumes at START and END; never stop a container or remove a volume you did not create.
- **Builder evidence** (a claim): `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Architecture/2026-09-10_policy-composer/qa-wp3r2/` (M1..M6 RED/GREEN logs).

## THE BUILDER'S CLAIMS — verify each, relay none (session 40 wrap 2026-09-12T23:02:21Z, spf/dkim/dmarc pass)
1. **Your Majors, each fixed RED-first from your own probes, one commit each, all ancestors of head** (Tuesday checked):
   - W3-M1 `00b3ef6`: fact-path-shaped literals refused in facts-only positions, together with D8 at `64a2b09`;
   - W3-M2 `49bbaba`: min_severity rules apply only where `when` holds;
   - W3-M3 `95df331`: a silent (null) baseline default no longer yields the strongest value;
   - W3-M4 `8c2750f`: a decision is stale only if it matches no group's conflict;
   - W3-M5 `d3e3de7`: exception terms matched by a fingerprint recomputed from the terms;
   - W3-M6 `b654459`: an unassessed `high_impact` is governed as high impact.
2. **W3-M6 is Tuesday's RULING** (2026-09-12T07:54:20Z, A-51 *"not assessed means not safe"*), not an open question. Grade the implementation against that ruling.
3. **W3-m1:** `53ce604` adds killer tests for your 27 surviving mutants (29 tests plus 2 JCS escape tests), GREEN at head.
4. **Real content:** the phantom-field fix changed the content hash `47ea3e7c…` → `79364073d53a90f63184b3905c0060549982d4c7cc8d7f2c2934a4732967dca8` (55 items, 55 fields, 4 empty values). The builder says severities are IDENTICAL for all 55 items. The root cause was `tools/measure_sources.py:128`, with an importer guard added; a wrap-sweep found 7 hyphen splits in Active Ciphers, fixed in the same series.
5. **Clean-clone CI GREEN** on `047b1ed` (15 steps); `1a6b68d` adds only discovery wording.
6. **Declared NOT fixed:** W3-M7 (secret intake), m2 (silent drops), m3 (credential shapes), m4 (purity blind spots), m5 (label). Their RED tests are uncommitted in a builder worktree; Tuesday has asked for them on a branch. **The builder did not rerun your 52 mutants.**

## 🔴 WHAT TO ATTACK FIRST
1. **Re-run your own round-1 probes for M1–M6 at head**, RED at `0523193`, and your 52 mutants. Report which survive now.
2. **Each fix, adversarially, for the next gap of the same shape.**
   - M1: every expression position, not only the ones the fix names.
   - M2: `when` on every other rule kind that carries one.
   - M3: a null default in every branch of §1.7.
   - M4: conflicts in two groups at once, and a decision matching both.
   - M5: every hashed term an approver signs.
   - M6: `remediation_safe` unknown AND `high_impact` unknown together, under all three postures, on REAL content.
3. **The content change:** independently re-derive 55/4, check that severities on all 55 items match the old release, and check the new content hash (your own JCS + SHA-256). Does anything else change because the hash changed (goldens, pins, the real-content test)?
4. **What M7 and m2–m5 being open means for MVP A:** is any of them reachable, silently, through the API on the real or the demo content, now that WP4 exists? Name the path if yes. This decides what ships under the cap.
5. **Clean-clone CI at head.**

## KNOWN — do NOT report as new
- W3-M7, W3-m2…m5 (declared open; grade only what point 4 above asks);
- W3-p1…p3; PQ-07 (owner question); the builder's NOT TESTED limits from round 1;
- WP4/WP5 (the parallel gate); WP6 Preview not built;
- database residue as in round 1.

## Output, controls, logistics
- **Findings-only.** FOUND / TESTED / HOW plus an evidence class on every finding; a control for every zero; never `rm`; head readings at start, mid and end.
- **Run long commands in the FOREGROUND. Never end a turn waiting on a background notice.**
- **Report:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-13-composer-1a6b68d-wp3-tier1r2/report.md`.
- **MAIL YOUR VERDICT** to `tuesday-agent@agentmail.to`, subject `[QA/Datasec-HPSM -> Tuesday] GATE VERDICT — Policy Composer WP3 rules engine round 2 @ 1a6b68d (tier 1, round 2)`. Lead with GO, GO WITH FINDINGS or NO GO, and state what ships under the cap if NO GO. **Never `wednesday-agent@`.** You have no inbox.

PROVENANCE:
- head 1a6b68d, 0523193..head 61 commits, 15 engine/canonical files, M1-M6 and 53ce604 and 64a2b09 ancestors of head, origin afc10e9 | git rev-list / merge-base / diff / ls-remote in Datasec/HPSM 6_Policy_Composer, run by Tuesday s11 09:04 | read 2026-09-13
- round-1 verdict NO GO 0/7/5/3 and finding ids | round-1 report.md line 3 and its finding headings, read by Tuesday s11 | read 2026-09-12
- claims 1, 3-6, content hash change, NOT fixed list | Datasec/HPSM session 40 wrap mail 2026-09-12T23:02:21Z, spf/dkim/dmarc pass | read 2026-09-13
- W3-M6 ruling (a) | Tuesday ANSWER to Datasec/HPSM 2026-09-12T07:54:20Z, verified at destination | read 2026-09-12
- ports 18880/18980 free, pc-lane-a on 18580, E8 SOW text present | lsof + docker ps + ls, run by Tuesday s11 09:04 | read 2026-09-13

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-13 09:09
