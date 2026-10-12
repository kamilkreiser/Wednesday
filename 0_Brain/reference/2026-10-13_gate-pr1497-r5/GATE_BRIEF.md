# Gate brief: Secuura Platform K PR #1497 (KS-695 part (ii), organisation erasure), round 5 — OPUS tier 1, DELTA gate

Commissioned 2026-10-13 ~05:2x AEDT by the Wednesday seat. Destructive GDPR path: full weight.

## What you are gating
- Head `dc488c460f794dc476ce3460eabd44c9d6e138fe`, develop `425ad3e00ae40ddbce6ead62c127c610e2e67a16` (both by Wednesday's ls-remote at commission).
- Delta since the round-4 gated head `4ca146545f15`: four commits per the author (Seat J 4th): the fix f4d4152b7, a merge of develop b2085e99ff1c, a tests-only commit df2c279bb (tenant-scoped slow triggers), a merge of develop 425ad3e00ae4. Merged in, never rebased.
- Round 4 verdict (NO GO, Major M-1: an organisation-scoped admin of org A can erase org B): `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-13_gate-pr1497-r4/verdict.md` and its evidence files beside it. Read it first; its attack file `gate1497r4-attack.integration.test.ts.txt` is yours to reuse.
- The author's round-5 claims (NOT evidence; re-measure): (1) a collision guard inside the transaction: if ANY svc_api_keys row for the tenant + connector id is not this organisation's (org-less counts), refuse 403 and write nothing — closes M-1 path 2; (2) N2 wording; (3) m-C wording; (4) G8 cells; (5) the PR states "M-1 PATH 1 IS NOT CLOSED BY THIS PR" and names KS-1533 (path 1 is KS-1533's, fixed separately in PR #1521; do NOT count path 1 against this PR, but DO confirm it is stated, and confirm your P8-style cell still shows path 1 open so the statement is true).
- Author's numbers: unit 39/39; bounds 25/25 and older integration 15/15 both tenancy modes; all 8 integration files --runInBand 88/88 both modes; originate 103 suites / 1254 tests; packages/shared 954; 28 mutants killed; hook 13/16 legs ran, 3 skipped. Author says the integration suite is NOT parallel-safe (1/88 failure single-tenant parallel).

## How to get the code (READ-ONLY on the project)
- Project checkout `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ-ONLY: no git write verbs there. `git clone --shared` into YOUR scratchpad; fetch `refs/pull/1497/head` and develop there with the project's `core.sshCommand`, or use the bundles in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-12_seatJ-4th/`: `ks695b_pr1497_dc488c46_full.bundle` (sha256/16 1379e0d584d363fd, verified) and `..._delta_since_gated_4ca14654.bundle` (bf766f1f934e0c25, verified). Assert the head sha first.
- Real Postgres: run it locally in a container or local instance you start in YOUR scratchpad context, both tenancy modes, as the app role with RLS in the loop, as the previous gates did. Never touch Kintsugi, demo or any remote box. No pushes, no GitHub/Linear writes.

## What to attack
1. The collision guard over the REAL route: org A admin key whose connector id collides with an org B key; org-less key collisions; case/whitespace/encoding spellings of the connector id; same-org rotation (must NOT refuse); a key minted between the guard read and the commit (author says it is a read, not a lock: measure what concurrency does); deleted-key reuse.
2. Confirm the 403 path writes nothing (row counts before/after, audit rows).
3. Re-run the round-4 attack file in both modes; every previous Major/Minor still closed.
4. The tests-only trigger rewrite (AFTER statement triggers with transition tables): are the m-2 and G8 cells still able to fail? Plant the defect they guard and watch them redden.
5. The two develop merges: the PR's 10 files byte-identical across them, and no develop change in the delta touches what this PR reads.
6. N-3 PROPOSAL (not built; Wednesday will rule on it from your read): adding `AND d.parent_document_id IS NOT NULL` to arm (b) of the selector in both SQL copies. Enumerate EVERY writer of `versionedById` and of `parent_document_id` at this head (grep, do not sample) and the values each can write (connector id, user id, NULL). Say whether the author's premise holds ("every ROOT row carrying versionedById was caller-planted; the three version routes that set it also set a parent") and what a legitimate row the predicate would stop reaching, if any.

## Output
- `0_Brain/reference/2026-10-13_gate-pr1497-r5/verdict.md` (this folder only, plus your scratchpad).
- Head under test and how obtained; every number with its instrument and a control; FOUND / TESTED / HOW; what was NOT tested.
- VERDICT: GO / GO WITH NOTE / NO GO, Majors and Minors with file:line, the reproducing shape and the minimal fix; then a separate section "N-3 premise: HOLDS / FAILS / PARTLY" with the writer table.
- This is round 5. The merge itself is held for Kam's card regardless of your verdict; do not recommend merging or deploying.
