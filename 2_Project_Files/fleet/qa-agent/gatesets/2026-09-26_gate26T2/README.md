# Gateset 2026-09-26_gate26T2 — README for Wednesday

The drafter launched nothing, sent no mail, tapped no pane, merged nothing and committed nothing. It wrote only under `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad/gate26/` (this kit and its
sibling), the scratch clone `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad/g26_sp/clone.git` (a `--no-local` bare clone, no alternates), the control workdirs `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad/g26_controls_*`, the live-shape
fixtures `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad/g26_liveshape_fixtures/` and a scratch vitest install `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad/g26_vitest/` (vitest 4.1.11, `npm --legacy-peer-deps`). npm also wrote its usual
debug logs under `~/.npm/_logs/` (two failed installs, npm arborist peer-set crash) — outside the scratchpad, reported, not touched. One stray copy of fill_gate26.py
made by a drafter slip sits in `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad/gate26/_quarantine/` (not deleted).

This kit is the second of TWO. **gate26T2 = the eight TIER-2 PRs** (exactly the cap of 8; nothing had to wait); the sibling `gate26T1` (#1274, #1280-#1284) holds the tier-1 PRs and has its own README.

| PR | ticket | head (READ: API == ls-remote pull/head == branch == fetched) | commits on merge-base | squash subject chars | why this tier (from the DIFF) |
|---|---|---|---|---|---|
| #1245 | KS-1313 | `cb31a58c190f86aad49b402c1c001429c037ed24` | 3 on `6e2a00bfed57` | 98 | test tooling only; a CHECKER (reader rule). **Round 3 of 3, at the cap.** |
| #1261 | KS-1293 | `0b2fdbb1b8195d4f73467508f8eb6a4c3781b81a` | 2 on `fa25c9b10fb4` | 80 | one originate test file; a CHECKER (hermeticity scan). **Round 2 of 2, at the cap**; PR body not refreshed. |
| #1268 | KS-1318 + KS-1142 + KS-1316 | `5ac42fafeee11dec596e7e7d833ac82b8b478790` | 2 on `4db87c3e4b98` | 90 | two test files; a CHECKER (the ks781 walk). **Round 2 of 2, at the cap**; a third rule (returned escape) accepted as a shape. |
| #1275 | KS-1179 | `d852e56b912f8a14b8f2cf01639dc37f9c9ff6a2` | 1 on `4db87c3e4b98` | 102 | comment + ONE type annotation on the SSRF guard (a T1 surface); rides T2 ONLY on its emit proof. |
| #1276 | KS-794 | `737a4069c6316b10a89fa9c499fac6c2cb20f619` | 1 on `d7cdecf1d2ee` | 67 | published contract (registry + committed yaml); registered for the spec only, not validated at runtime (READ). |
| #1277 | KS-1319 | `702171eaadbeb0a9d830237ec6fd86219311477c` | 1 on `4db87c3e4b98` | 104 | one test file; a CHECKER (reader rule). |
| #1278 | KS-1314 | `c321bcce2a9ae7e2c3d5da65f3c1d64fc3295de9` | 1 on `4db87c3e4b98` | 116 | systemTest test support; a CHECKER (reader rule). |
| #1279 | KS-1306 | `dabde931df5e02e45272b70f2fe75fb3dab6ed38` | 1 on `d7cdecf1d2ee` | 68 | one integration test file; its DB leg is not run (no Docker). |

Routing `QA/Secuura-batch1245`. GO string `GO: merge #1245, #1261, #1268, #1275, #1276, #1277, #1278, #1279 batch` (or the subset). All go to a MERGE SEAT (no author is live for them).

## 1. BLUF
- **Kit: READY to launch** once you add the routing line (§4). `--check` rc 0 (all guards pass:).
  - Controls: **152 controls, OK 152, MISMATCH 0** normally (rc 0); **OK 0, MISMATCH 152** under `--invert` (rc 1 — by design every control must flip).
- **Pinned over develop `00de57baeb405d0081fe8b6f192bd40d35acef61`** (tree `fb4d9f1691451db2cdfab3cae22db2fd675f0f80`) — read by ls-remote AND fetched AND agreed; it is the `00de57baeb40` Wednesday expected (#1270's squash).
  - END_TREE **`d400f96a955ebdfb427fbde2951cd95fc9af13d3`** (14 files changed, 1646 insertions(+), 96 deletions(-)), identical in all 40320 orders (1044 distinct merge-tree calls, memoised).
  - END_TREE_WITH_SIBLING **`5807048824a8e15dce62d8a7a6b0d62e2160a4c1`**: develop + both kits, the same tree whichever kit lands first (measured from both kits).
- **OVERLAPS: NONE.** Measured pairwise: every kit PR vs every other, vs the sibling kit, vs the develop move since its own merge-base, and vs Seat B 30th's in-flight PRs at the pin (none left in flight at the final pin: #1274, #1268 and #1261 were, and each joined a kit at its round 2).
  - NOT STACKED: no head is another's ancestor; every pair's merge-base is on develop (hard check in predict).
  - KS-730 PR3's unpushed worktree `s-b29-ks730c` (adminConfig.ts + the ks730c test) was censused disjoint at the first pin, before it became #1284; #1274, #1268 and #1261 were in flight at the first pin and joined T1 / T2 / T2 at their round 2 (Wednesday 10:2x / 10:3x / 10:5x). Nothing of Seat B 30th is in flight at the final pin.
- **The decisive item the gate owes — #1245 at the cap (a PREDICTION, measured LIVE by the drafter):**
  - Round 3 reads all 42 of gate24T2c's real captures as their oracle says; H1, H1b, H1c read NULL (liveshape_1.out). The KILLED-AFTER-LOOKALIKE blocker looks closed.
  - **ERRORS-LINE-LIVE — a predicted round-3 REGRESSION:** a real vitest 4.1.11 run whose test raises an UNHANDLED error (a throw in setTimeout; an unhandled rejection) ends normally (status 1) and prints `     Errors  1 error` between `Tests` and `Start at`. Round 3's walk-back refuses that line and reads **NULL** on all three live shapes (json oracle {2,0}, {2,0}, {2,1}); `childSuiteCounts` then THROWS. **Round 2 read all three correctly** (liveshape_live_1.out, liveshape_r2cmp_1.out).
  - Under Kam's rule ("a wrong reading of ANY real vitest shape = NO GO") and gate24T2c's precedent (NULL against a count = FAIL), this predicts **#1245 NO GO at the cap — ships nothing** — unless the gate measures otherwise or rules reach. It fails LOUD (a throw), not silent. See §6 decision 1.
  - EXIT-HOOK-AFTER-SUMMARY: a `process.on('exit')` lookalike did NOT reach stdout after vitest's block live (X1); the composed SYN-H4s ({7,0}) is not a real shape until the gate finds a mechanism.
- **#1261 at the cap (round 2 of 2):** round 1's REVERT-SKIPS is addressed by an explicit 9-file manifest failing by NAME + an import-scope base read from the TS AST (two halves, each with its own restore arm). The gate must revert the REAL env lines (not only the seat's temp copies) and probe the AST rule's shapes. **N-1261-c STILL OPEN** (body: KS-1266/1310/1311 hyphenated; round-1 message: KS-1266) and **STALE-BODY-1261** (the body was not refreshed for round 2) — both handled by the mandated squash block.
- **#1268 at the cap (round 2 of 2):** round 1's blocker (the named alias shape read false) is addressed by R1 (never-referenced) + R2 (NewExpression args) + a THIRD rule (returned escape) that Wednesday accepted as a shape. KS-1318/KS-1142 work byte-identical by blob (READ: entrypoint-corpus.test.ts `8a4ce36a3a96` at both rounds; round 2 touches only ks781). **The gate must grade the third rule for OVER-reports** (a returned-but-never-called guard reading true would hide an unguarded path from LEG F) and W19's boundary.
- **#1275 rides T2 on its emit proof:** 2 non-comment changed lines (READ). A different emit = NO GO here and a tier-1 re-gate.
- **TITLE-OVER-92:** #1245 (98), #1275 (102), #1277 (104), #1278 (116) — the kit carries drafter-proposed short subjects (key-scanned, ≤ 92). **NO-REFS-LINE:** #1275/#1277/#1278 bodies lack a Refs line.
- **#1279's DB leg is NOT RUN** (no Docker); its loopback/port guard is measurable without a DB and is owed.
- **Fleet STOP (READ, bounded region, NOT-FOUND control):** #1245 NOT APPLICABLE (systemTest/ push, 7 lines); #1261 28/0 · 6/0 · 49/0 · 60 of 60; #1268 28/0 · 6/0 · 49/0 · 60 of 60; #1275 28/0 · 6/0 · 49/0 · 60 of 60; #1276 28/0 · 6/0 · 49/0 · 60 of 60; #1277 28/0 · 6/0 · 49/0 · 60 of 60; #1278 NOT APPLICABLE (systemTest/ push, 11 lines); #1279 28/0 · 6/0 · 49/0 · 60 of 60. After the merge: 28/0 · 6/0 · 49/0 · 60 of 60 (no shell-suite path in either kit).
- **Fleet at the launch develop:** Wednesday relayed (11:0x) Seat B 30th's measurement at `00de57baeb40` = 28/0 · 6/0 · 49/0 · 60 of 60; the drafter could not find its file (UNMEASURED by the drafter) — the prompt tells the gate to find and quote it.
- **Linear: every PR links `contributes`; NONE `closes`** (measured, both kits). The "closes a ticket it only contributes to" class you saw twice today is NOT present in this batch.
- **MG-3 key scan:** key scan: 8 mandated squash text block(s), each carries only its own key: #1245 ['KS-1313'], #1261 ['KS-1293'], #1268 ['KS-1142', 'KS-1316', 'KS-1318'], #1275 ['KS-1179'], #1276 ['KS-794'], #1277 ['KS-1319'], #1278 ['KS-1314'], #1279 ['KS-1306']

## 2. Pins — predict_2.out (rc 0; predict_1.out is the identical earlier pinned run)
- #1245: 3 commit(s) `1700b5ae7dd5`, `65eb964271b0`, `cb31a58c190f` over `6e2a00bfed577528de1ee02b41cb5a0e99172b35`; 26 behind develop; merged tree `2f6a0c0838dabf4013c400cea13b4f1517a51f28`; every merged blob == its head blob; numstat equal; no mode change; move ∩ own paths EMPTY.
- #1261: 2 commit(s) `eab8d7031b1b`, `0b2fdbb1b819` over `fa25c9b10fb44da6c848a6975d86ebfa523e8602`; 21 behind develop; merged tree `2adface4710416afdefc6484bd1158b3b1a589d1`; every merged blob == its head blob; numstat equal; no mode change; move ∩ own paths EMPTY.
- #1268: 2 commit(s) `a8e0fca70ed4`, `5ac42fafeee1` over `4db87c3e4b98b8e366c3dd60d5f399917bad5086`; 16 behind develop; merged tree `1c436f7804808106c8fa00641276f20c855fa97e`; every merged blob == its head blob; numstat equal; no mode change; move ∩ own paths EMPTY.
- #1275: 1 commit(s) `d852e56b912f` over `4db87c3e4b98b8e366c3dd60d5f399917bad5086`; 16 behind develop; merged tree `0bc24e727cf3c5d948a457830fb48a89b86dbd28`; every merged blob == its head blob; numstat equal; no mode change; move ∩ own paths EMPTY.
- #1276: 1 commit(s) `737a4069c631` over `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9`; 11 behind develop; merged tree `2a58ae47be1d047e16338936b5a4e33adfee7098`; every merged blob == its head blob; numstat equal; no mode change; move ∩ own paths EMPTY.
- #1277: 1 commit(s) `702171eaadbe` over `4db87c3e4b98b8e366c3dd60d5f399917bad5086`; 16 behind develop; merged tree `6f5a870ddad2dcbbe500f8fb62996586256a08eb`; every merged blob == its head blob; numstat equal; no mode change; move ∩ own paths EMPTY.
- #1278: 1 commit(s) `c321bcce2a9a` over `4db87c3e4b98b8e366c3dd60d5f399917bad5086`; 16 behind develop; merged tree `a2831329ff55733808c9342f331ad7afcd10a24e`; every merged blob == its head blob; numstat equal; no mode change; move ∩ own paths EMPTY.
- #1279: 1 commit(s) `dabde931df5e` over `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9`; 11 behind develop; merged tree `37b27d99ea950ef4affa4c9963a4cb6d13ae5d5d`; every merged blob == its head blob; numstat equal; no mode change; move ∩ own paths EMPTY.
- Simulations: develop + a FOREIGN edit of a kit PR's own file → REFUSED (predict_sim_foreign*.out, rc 1); develop BEFORE gate25's six squashes `df5e9f5da6d23411e7b38a79a58aa20c04b6afe2` → PASS (predict_sim_predev.out).
- Superseded runs are kept, never deleted: `*_pre1284*`, `*_pre1274*`, `*_superseded_*` (each names why).

## 3. What the gate owes
- Prompt `2026-09-26_secuura-batch1245-t2.prompt.txt` (54357 bytes) — the per-PR sections, the rules, the MANDATED SQUASH TEXT blocks (key-scanned) and the MG-3 key-set table.
- Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-26-batch1245r3-t2/`; mail subject as in the prompt, FROM coagent@ TO wednesday-agent@.

## 4. Routing line to add (the drafter did NOT write it)
`QA/Secuura-batch1245|coagent@agentmail.to|yes` → `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (absent at drafting, measured: the exact line is absent; `QA/Secuura-batch1245r2` exists for round 2). Also in PROPOSED_inbox_routing_line.txt.

## 5. The ONE launch command
```
/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad/gate26/gate26T2/repin_and_launch_gate26T2.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad/gate26/gate26T2/launch_qa_secuura_batch1245-t2.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad
```
- Dry run (`--dry-run` appended): repin_dryrun_1.out → DRY RUN COMPLETE 2026-09-26T01:07:45Z — every read agrees with the pins; the real run continues with the usage gate, --check and cockpit.sh add
- If develop moves (the sibling kit or any GO lands first), step 3b re-pins in the same action; a move onto an own path, a stack or a pairwise overlap refuses rc 10 (controls RD / RE).
- If you copy the kit into `gatesets/2026-09-26_gate26T2/`, pass the copied paths: step 0b re-measures and re-fills there.

## 6. Decisions for Wednesday (each with the drafter's recommendation)
1. **#1245 and ERRORS-LINE-LIVE.** The drafter's live capture predicts a round-3 regression (NULL, fail-loud) on a real vitest shape round 2 read correctly. *Recommend:* launch as drafted — the gate must measure it through the REAL function; if confirmed, THE READER RULE makes it NO GO at the cap (ships nothing; residue ticketed: anchor on `Start at` but allow vitest's own `Errors`/`Type Errors` summary lines in the gap, plus the status refusal, which is the part that closed H1). Only Kam can soften the rule for a fail-loud NULL; the prompt says "Do not soften the rule yourself".
2. **#1275's tier.** Comment + one type annotation on a T1 surface. *Recommend:* T2 with the mandatory emit proof (as drafted); a different emit = NO GO and a tier-1 re-gate.
3. **TITLE-OVER-92 short subjects.** The four proposals are the drafter's wording. *Recommend:* let the gate ratify or reword them; the key scan must be re-run over whatever is finally mandated.
4. **#1279's DB leg.** Not run (no Docker in this gate); its red proof is READ ONLY. *Recommend:* accept for a test-only PR, or authorise a disposable Postgres on a loopback non-shared port as a separate step.
5a. **Three PRs at the cap in one kit (#1245 r3, #1261 r2, #1268 r2).** Each NO GO ships nothing for that PR only; the kit's other PRs are unaffected (disjoint, order-independent END). *Recommend:* launch as one kit (the cap is 8 and it holds exactly 8); nothing had to be deferred.
5b. **#1268's third rule.** Accepted by you as a SHAPE; the prompt makes the gate test whether it can OVER-report (hide an unguarded path). *Recommend:* if the gate measures an over-report on a real shape, it is a wrong reading under THE READER RULE — NO GO at the cap, and KS-1318/KS-1142 would be held a second time; consider pre-authorising a split (land entrypoint-corpus.test.ts alone: byte-identical and proven in round 1) so proven work is not held twice.
5. **Routing name.** You specified `QA/Secuura-batch<lowest PR>` → `QA/Secuura-batch1245`; round 2 used `QA/Secuura-batch1245r2`. *Recommend:* keep `QA/Secuura-batch1245` (it is distinct; no collision).
6. **READY mails NOT read** (as gate26T1 §6.6).
7. **#1285 KS-766 (Seat B 30th, head read `c7779a33031813cac9dab62abd0cb8fd9d73f2f9`, 1 commit on 00de57baeb40, base-image-watch.sh +60/-38) is NOT in gate26.** T2 is full at 8 and it is a tooling script, not tier 1. *Recommend:* the next kit; it also needs the shell-suite count re-read (a self-testing bash script may be a `run_shell_suites` member).

## 7. Controls: `controls_gate26T2.sh <scratchpad> [--invert]`
- **controls_1.out:** 152 controls, **OK 152, MISMATCH 0** (rc 0).
- **controls_2.out (`--invert`):** **OK 0, MISMATCH 152** (rc 1 by design). Every control can fail.
- Every mutation is independent of the original: doctor() refuses a replacement that contains the text it replaces (rc 98) and refuses when the original still occurs after the plant (rc 97); every wrong head is the real head with ONE hex digit changed (same length, never a superset — the H20 lesson); the launcher's head guard is whole-field.
- Doctored arms are pinned to the launcher's own develop, so a develop move mid-run cannot mask them as exit 17. RD runs the REAL re-pin (predict → fill) from a launcher pinned at predev `df5e9f5da6d2` in a MOVED copy; RE makes a kit PR also a sibling-kit PR (a pairwise overlap) and must refuse rc 10.
- Not controlled: exit 16 (needs a TTY), repin steps 4-6 (usage gate, cockpit add), a `mergeable=False` refusal.

## 8. Files
- Kit: kit.json · COMMISSION.md (the LEGITIMATE SHAPES table) · PROPOSED_inbox_routing_line.txt
- Pins: predict_gate26.py → predict_1/2.out, predict_sim_*.out, pins_gate26T2.json (+ .SIM-*.json)
- Reads: gh_read_gate26.py → gh_read_1.out, gh_body_*.md, gh_comments_*.md · linear_reads_gate26.py → linear_reads_1.out, linear_KS-*.md · capture_mail_gate26.py → capture_1.out, mail_gate26T2_ready.md, stopcounts_gate26T2.json
- Prompt/launcher: prompt_gate26T2.TEMPLATE.txt, launcher_gate26T2.TEMPLATE.sh.txt, fill_gate26.py → 2026-09-26_secuura-batch1245-t2.prompt.txt + launch_qa_secuura_batch1245-t2.sh (fill_1.out; `.pre-*` = earlier fills), launcher_check_1.out
- Repin/controls: repin_and_launch_gate26T2.sh (repin_dryrun_1.out), controls_gate26T2.sh (controls_1/2.out + .rc)
- Drafter probes (PREDICTIONS): drafter_liveshape_g26.sh → liveshape_1.out (42 gate24T2c captures + SYN shapes); drafter_liveshape_g26_live.sh → liveshape_live_1.out (live vitest 4.1.11 captures, json oracle); drafter_liveshape_g26_r2cmp.sh → liveshape_r2cmp_1.out (round 2 vs round 3)
- Shared drafting helpers one level up: make_commission.py, make_readme.py, derive_repin_controls.py, repin_header.txt

## 9. NOT done / NOT measured by the drafter
- No launch, mail, tap, merge, commit, push, routing write, container or port bind. No inbox read. The Secuura checkout was touched only by read verbs (ls-remote, `config --get`, `clone --no-local` as a source); Seat B 30th's worktree only by rev-parse / merge-base / diff / `--no-optional-locks status`.
- **UNMEASURED:** every suite count and every red proof (READ from seat logs and messages); every runtime behaviour through the real modules (the drafter ran only extracted pure functions under node and throwaway vitest projects, never the repo's own suites); tsc, lint, prettier; the usage gate and launch steps 4-6; the post-pin moves of Seat B 30th's in-flight PRs (re-read at every re-pin).
- **UNMEASURED:** the REACH of ERRORS-LINE-LIVE (whether a SLOT_SENSITIVE_FILES child can raise an unhandled error today); #1275's emit; #1279's DB leg; #1276's check:openapi; #1277/#1278 through their real functions.
