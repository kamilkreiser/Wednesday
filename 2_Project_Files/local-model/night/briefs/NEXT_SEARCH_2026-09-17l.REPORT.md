# NEXT SEARCH 2026-09-17l (16:20-16:47 AEST): stale-reason re-reads and the post-17j pool

**BLUF: TWO FITS, both test-only vitest in services/api-gateway, briefed and proven. Nothing queued.** No third fit exists at the new tip `f8c7aaa39`.
- **KS-1123 F-1002-1**: pins a `0` and a `false` anchor status as off-chain-only on the tier-1 verify route. Tamper at `routes/verification.ts:624`. **Ready to queue.**
- **KS-1205 F-3 (G-BUCKET-HASH)**: pins that an API key's limiter bucket is never `api_key:` plus the bare sha256 of the key. Tamper at `middleware/auth.ts:300`. **Needs one partition call from Wednesday first** (see "Wednesday must read", item 1).
- **Tip moved during the search:** `d7e95cd9f` became `f8c7aaa39` (#1020, KS-769 fuse, one file `scripts/audit/lock-discovery.mjs`). Both product files have the same blob at both tips. Every checker run ran at `f8c7aaa39`.
- Rejection table appended to `night/candidates.md` as `## SEARCH 17l` (backup `candidates.md.pre-1646-search17l`).

## Wednesday must read
1. **KS-1205 partition call.** The 15:0x ruling ("a test-only tamper target does not count unless the test collides or the tamper is within 10 lines of a READY's hunks") names READY-held files. `middleware/auth.ts` is not in any READY or open PR, but it IS in seat A's LIVE heads: KS-1207 `0f8b699b4` `@@ -277,10 +277,14 @@` and KS-744 `6252f06ac` `@@ -389`/`@@ -394`. The tamper line `:300` is 14 lines below KS-1207's last hunk line, and the new test file collides with nothing.
   - If the ruling covers live heads: queue it as is.
   - If it does not: hold it until KS-1207 merges, then rebuild (the tamper moves to `:304`).
2. **Checker A4 gap (harness, not fixed).** A4 passes when ANY declared red cell reds, even if another declared red cell stays green under the tamper. Measured: KS-1123 wrong_emptytwin (R1 fed `''` instead of `0`, so R1 is green under the tamper) returned **RESULT: PASS (7/7)** with `1 failed / 4 run` (16:33:02-16:33:24). The checker should refuse when a declared red cell does not red.
3. **The checker changed between rounds.** Its sha256 is `c6ee07e4c2cd2abc6064ace32d8161de49c595c14564e5c9fd3927af1116371b`; DEFAULTS2 recorded `f3ce186cf515…` at 15:5x. The sha was identical before and after all 17 of my runs.
4. **KS-1123 file name.** The builder's slug `ks1123-api-gateway-verify-an-empty-string.test.ts` is the name the 09-15 READY_KS-1123-F2/F3 diffs carried. Those were merged as #1002 under renamed files, so nothing collides at the tip. Rename at raise.
5. **KS-1205's cell reads `req.user.rateLimitBucket`, not the gate's fake-Redis keys.** A tamper inside `rateLimitEnforce.ts` that rebuilt the Redis key would not red it. This is stated in the brief's notes.
6. No new product defect was found outside the remit.

## FOUND

| ticket | verdict | why | instr |
|---|---|---|---|
| **KS-1123 F-1002-1** | **FITS, briefed** | Stale refusal ("held / PR attached"): READY F2/F3 merged as #1002 (`dd66863dd`). The 09-16 13:43 and 14:02 comments name `0`/`false` as still owed. | measured |
| **KS-1205 F-3 G-BUCKET-HASH** | **FITS, briefed, partition call** | 17f's "plant in middleware/auth.ts (seat A)" predates the 15:0x ruling. The fix shape is the gate's "cell to add". | measured |
| KS-1205 other rows | refused | RAW-2's tamper does not compile (TS6133; my CONTROL cell reds it anyway). G-OAUTH waits on A.1, G-UNKOPT is KS-1207's, G-JWTCATCH is a hang. The product rows sit in seat A's heads. | measured + read |
| KS-1209 (new, 06:27Z) | refused | `fail=1` at 27 sites with no per-leg record: a multi-site edit plus a whole-preflight stubbed harness. `preflight.sh` is in 09-16 READYs. Its Polish half is `.mjs`. | measured |
| KS-1140 / KS-1131 | stand (17k) | Already re-derived by BRIEFS 17k and refused on shape; not re-read. | record |
| KS-1147 | refused (the stale partition reason is replaced) | The subject is the ks860 guard test, the `+` regex carries backslashes, and the fix is "the gate's PROPOSAL". | read |
| KS-947 / KS-811 | refused (the stale partition reason is replaced) | Two findings plus a spec-binding design; a multi-service derived-set design. | read |
| KS-1000 | refused | PR #874 is merged, but item 1 is "Decide the shape". | read |
| KS-1143 / KS-1144 | stand | `ks781-p3-3` is still in seat A head `4d551f104`. | measured |
| KS-864 / KS-960 / KS-1129 residues | refused | The PRs are merged. What remains is decisions, gate Records ("No build owed"), 17 call-site edits, or held READY_KS-864-F1009. | read |
| 21:0x title-level rows (47) | refused | Screened by instrument; KS-825, KS-758 and KS-748 were read in full. None is single-file vitest with a spelled shape. | screened |

**Pool counts:**
- 327 KS Backlog/Todo at 16:21:12 (first:50, 7 pages, hasNextPage false).
- 328 at 16:29:31 (first:25 with comments, 14 pages, hasNextPage false); the +1 is KS-1209.
- Updated after 02:27Z: 1 (KS-1209).
- Pool tickets with a PR attachment: 14, all read at title level or deeper.

## TESTED

Both proofs ran the real `tasks/code_patch/checker.sh` under `sandbox-exec` (off-host outbound denied) in the scratch clone `/private/tmp/claude-501/night/s17l/clone` at `f8c7aaa39`.

**KS-1123:**
- Premeasures:
  - tip: 4/4 green;
  - under the tamper: R1 and R2 red by assertion (`expected [ 200, true, 'on-chain' ] to deeply equal [ 200, false, 'off-chain-only' ]`), CONTROL green;
  - **gap:** the whole suite is 454/454 green under the tamper without the file;
  - canary: 57/454 red.
- Checker, draft input: fin0 golden **PASS 7/7** (A4 2 failed / 4; A6 454 to 458, NEW reds []; A7 tsc rc 0).
  - wrong_blind: `FAIL A4 RED-FIRST`
  - wrong_product: `FAIL A3 (test-only)`
  - wrong_control: `FAIL A4 … CONTROL cell(s) red`
  - wrong_count: `FAIL A4 … COMPLETENESS`
  - wrong_emptytwin: PASS (the harness gap above)
- Checker, placed input: fin1 golden **PASS 7/7** (16:35:42-16:36:07); wrong_blind `FAIL A4`; wrong_product `FAIL A3`.

**KS-1205:**
- Premeasures:
  - tip: 3/3;
  - under the tamper: R1 red by assertion, CONTROL green;
  - RAW-2 row: CONTROL red, tsc rc 2;
  - **gap:** the whole suite is 454/454 green under the tamper;
  - canary: 14/454 red.
- Checker, draft input: fin0 golden **PASS 7/7** (A4 1 failed / 3; A6 454 to 457; A7 rc 0).
  - wrong_blind (one substitution in `bareHash`): `FAIL A4 RED-FIRST`
  - wrong_control: `FAIL A4`
  - wrong_product: `FAIL A3`
- Checker, placed input: fin1 golden **PASS 7/7** (16:43:03-16:43:26); wrong_blind `FAIL A4`; wrong_product `FAIL A3`.
- After a premise-text-only brief fix, I rebuilt the input and ran fin2 golden **PASS 7/7** (16:44:31-16:44:53).

**Instruments:**
- Checker sha256 `c6ee07e4c2cd…`, the same before and after every run.
- Builder `build_input.sh` sha `52afcfbdec99`, rc 0 on every build.
- Source porcelain 0 at 16:34:33, 16:42:14 and 16:45:59.
- Scratch clone clean (untracked 0) after every run; leftover test files moved to `k1123/quarantine` and `k1205/quarantine`.

## NOT tested
- No model round (nothing queued).
- KS-1205's wrong_control and wrong_count were not run on the placed input.
- KS-1205's placed wrong variants ran on the input built before the premise-text fix; they were not re-run on the rebuilt input.
- Tier-2 `0`/`false` for KS-1123 (read at `:722` as unreachable under this tamper since KS-1073).
- A tamper inside `rateLimitEnforce.ts` for KS-1205.
- No live stack.
- KS-947, KS-811 and KS-1147 were read, not driven.
- The 43 screened title-level rows were not read in full.

## HOW
- **Partition, measured, not trusted:**
  - open PRs by REST GET, paginated (16:21:39 and 16:45:52);
  - seat A's heads by `git diff --name-only` (three-dot for the stale-based KS-1050 head) and `-U0` for the hunks;
  - 09-17 READY `+++` paths;
  - KS-839/805/744's named auth files added by hand.
- **Linear and GitHub:** GraphQL reads with the Secuura key read inside Python, never printed. GitHub REST GET only. No git write verb against `!CODING`; checkout ran only in the scratch clone, via a script.
- **Scripts:** `s17l/k1123/` and `s17l/k1205/`: `pre.sh`, `variant.py`, `mkouts.py`, `runck.sh`, `clean.sh`, `assemble.py`. The brief header clock comes from `date`, and the fence is asserted equal to the golden test.
- **Controls:**
  - each tamper has an INERT/tip row and a canary positive control;
  - each brief carries one CONTROL cell (green under the tamper) and a COMPLETENESS cell.
- **Files written:**
  - `night/briefs/split_1123F1002/KS-1123.md` (sha256 `4e75f958…`)
  - `night/inputs/code_1123F1002.json` (`7be645c9…`, ~26.8K tokens)
  - `night/briefs/KS-1205.md` (`0f774311…`)
  - `night/inputs/code_1205.json` (`71c80dad…`, ~12.1K tokens)
  - the `candidates.md` block and this report.
- **Not touched:** `queue.md` (mtime 16:02), `night_run.sh`, `build_input.sh`, any checker. Nothing was deleted; nothing was sent.

## Queue lines (NOT added; Wednesday appends)
```
KS-1123 input=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/inputs/code_1123F1002.json task=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/code_patch/task.md ctx=65536
KS-1205 input=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/inputs/code_1205.json task=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/code_patch/task.md ctx=65536
```
- **Raise:**
  - KS-1123: "Refs KS-1123 (F-1002-1)", tier 2.
  - KS-1205: "Refs KS-1205 (F-3 G-BUCKET-HASH)", tier 2, and only after the partition call.
- **Rebuild pins:**
  - KS-1123: `NIGHT_BRIEFS_DIR=night/briefs/split_1123F1002`, `product=Blockchain/Dev/services/api-gateway/src/routes/verification.ts ref=services/api-gateway/src/__tests__/ks1123-f3-empty-status-is-off-chain.test.ts line=624 ctx=65536`
  - KS-1205: `product=Blockchain/Dev/services/api-gateway/src/middleware/auth.ts ref=services/api-gateway/src/__tests__/ks480-connector-auth.test.ts line=300 ctx=65536`
