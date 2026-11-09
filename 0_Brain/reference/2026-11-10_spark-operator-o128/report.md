# Spark o128 report (operator's final message, CONDENSED by Wednesday; the operator wrote no file here, WED-158)
**3 briefed, 3 PASS (3 held), 0 FAIL.** Spark idle after, with a written reason: everything left with a spelled-out shape is held, owned or in an open PR.

## Tunnel
Listener ssh pid 47986 alive throughout; the 10 s /v1/models probe intermittently returns http=000 (once at 07:04, then 200). Two rounds (KS-1922, KS-2075) hit it at the first model call: rc 5 HARNESS, re-run unchanged, PASS; no counter spent. Both at load1 8.25-8.75. Intermittent 000 UNRESOLVED (owed to Wednesday).

## Step 1 harness (built, opt-in)
Measured: round.sh built packages/shared and the node_modules farm only for code_patch/code_patch2/test_only/test_only_input; bash tiers got a bare clone; ks949_main_seed_idempotence.test.sh on a bare clone at d0b4825cc244 = 0/27, "packages/shared is not built". Fix: a brief dir containing `spark.farm` makes round.sh run new spark/prepare_bash_farm.sh (reuses tasks/code_patch/prepare_clone.sh; asserts packages/shared/dist/index.js and node_modules/.bin/tsx). round.sh changed by copy+mv (backup spark/round.sh.pre-1110-bashfarm); IMPROVEMENTS row; README note (backup README.md.pre-1110-bashfarm). Red proof: 0/27 -> 27/27; KS-1145 --control fails without spark.farm, passes with; KS-1988 control unaffected. No arm file under tests/.

## Step 2 screen
554 KS Todo+Backlog read (515 Backlog, 39 Todo, paginated); 307 name 2-8 paths; ~35 screened; descriptions read for KS-1145, 1922, 1945, 1879, 1982, 1587, 1921, 2078, 1112, 1812, 1815, 2100, 1599, 2075, 1251. PR census 70/330 -> 71/331 (new PR 2149 touches none of these files), control PR 2125 fired both ends. develop moved d0b4825cc244 -> 0d286210f98b during the run (only the ks1858 auth test changed: PR 2117's merge). Rejected with reasons: KS-1812 (held READY KS-1175-1805-1 pins the same shape), KS-1815 (anchorSubmission.ts in PR 2081), KS-1587 (real Postgres), KS-1921 (transaction restructure), KS-2078 (ruled record-and-leave), KS-1112/1879 (decisions), KS-1945 (measurement first), KS-1982/2100/1599 (no fix shape), KS-1251 (CI config).

## Held pieces (Wednesday read each PRODUCT hunk at source 07:3x and ACCEPTED the hold)
- **P1 KS-1145 item 2** (test-only, TIER 2): Blockchain/Dev/scripts/__tests__/ks949_main_seed_idempotence.test.sh, cell ID4 + TOTAL_CELLS 28; startup-migrations.ts plant-only. PASS 10/10, golden TREE-identical (model dropped the diff --git header). READY_KS-1145-KS-1145-O128-P1_...PASS-10of10_2026-11-10.diff.md. Needs spark.farm. UNMEASURED: CI runs it with PostgreSQL?; item 1 (ID3) not done.
- **P2 KS-1922** (TIER 2): analytics services/exportService.ts catch at line ~165: exportResult.error = 'Export failed' (wording the brief's own), real text to logger.warn; + 6-cell vitest (R1-R4 red, C1-C2). PASS 7/7, golden BYTE-identical. READY_KS-1922-KS-1922-O128-P2_...PASS-7of7_2026-11-10.diff.md. UNMEASURED: whether a UI reads the error text; warn level; neighbour dbSave* sites.
- **P3 KS-2075** (TIER 1: edited line sits in the redis-password lookup region; prints no value): observability/scripts/observability.sh:151 `$(resolve_redis_password || true)` + new bash suite Blockchain/Dev/scripts/__tests__/observability_down_survives_an_absent_redis_container.test.sh (stub docker). PASS, golden BYTE-identical. Side effect: `up`/`start` with the container absent no longer abort at that line. READY_KS-2075-KS-2075-O128-P3_...PASS-10of10_2026-11-10.diff.md. UNMEASURED: real Docker; the Postgres lookup; callers relying on the abort; which runner picks up the suite; the hold printed cat_ok=False (not chased).

## Step 3
KS-902's O101 READY was moved by commit 556f464d8e (2026-11-09 03:52) to local-model/night/_quarantine_2026-11-09/stale/READY_KS-902-O101-P1_..._2026-11-04.diff.md; WHY.md line 655: PREMISE-FALSE (KS-902 comment 2026-11-03T16:15Z). RECONCILED: not missing.

Scratch: spark/cache/work/o128-scratch/ (untracked, kept); operator logs in Wednesday's session scratchpad o128/ (session-only).
