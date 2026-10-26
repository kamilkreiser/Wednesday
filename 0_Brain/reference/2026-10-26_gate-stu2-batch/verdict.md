# QA gate (tier 2, findings-only, round 1 of 2): Secuura PRs #1711, #1712, #1714

Repo Secuura/Distributed_Secuura. Model routing: claude-sonnet-5-5, row G2. Findings only: nothing pushed, merged or commented.
Workspace: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate_stu2_batch_20261026/` (clone `repo`, private TMPDIRs `tmp.*`, outputs `out*.txt`, `cold_*`).

## Pins and readings (ls-remote)

| ref | Wednesday pin (21:46:56) | start 21:47 AEDT | end 22:07:28 AEDT |
|---|---|---|---|
| develop | 8661f5d418b23ffb0c63a2504d707eb12189b5ad | equal | equal |
| #1711 | d21a8386de8d7f0be71cebd4a094507c9ed60c05 | equal | equal |
| #1712 | 7788af2aa59183a5f5557999a6a057de89137177 | equal | equal |
| #1714 | 6905f6e67c276e2e18c4be6bd05a6d12f11e8dbf | equal | equal |

No head moved. Load1 stayed 3-7 on the suite runs (one 12.4 reading during the 3rd cold-install pair, not a heavy run of mine).

## BLUF

| PR | ticket | head | verdict | one line |
|---|---|---|---|---|
| #1712 | KS-1731 | 7788af2 | GO | One-line ORDER BY, only product change; Q3 red on develop's text (1 failed/112 passed), green at head 413/413; PR body says "SQL text only". |
| #1714 | KS-1729 | 6905f6e | GO WITH NOTES | Constant on first beforeAll only, no config change; stand-in and 110-cell tamper control reproduce; shape (i) blocked (TS1378). Note: the defect DID show once here (see below), so "unreproduced" is slightly conservative. |
| #1711 | KS-1735 | d21a838 | GO WITH NOTES | Restore now keeps stash, prints, exits non-zero; 15/15, red 10/5 on develop's guard; one LOW: chained-trap caller loses suite's own rc. |

Batch: all three merge-tree clean; recommended order #1712, #1714, #1711 (details at the end).

## #1712 (KS-1731), head 7788af2

**FOUND**
- `Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts:365`: `         ORDER BY created_at DESC, id DESC LIMIT $${idx++} OFFSET $${idx++}\`,` Diff vs develop is exactly this one line in product code (2 files, +20/-2; `git diff --stat origin/develop...pr/1712`). [INFO, claim holds]
- By-hash read `credentialRepo.ts:286`: `         ORDER BY created_at DESC, id DESC` then `LIMIT 1`. Unchanged (not in the diff; it already carried the tie-break). [INFO]
- `ks1683...test.ts:422` regex moved to `/ORDER BY created_at DESC, id DESC LIMIT \$\d+ OFFSET \$\d+$/.test(s)`; new cell `Q3` at ~:522-538 asserts the page statement matches the same regex. [INFO]
- ks1116 needs no edit: `ks1116...test.ts:640` `dbMock.query.mockReset();` and `:648` `await mods.repo.loadFromDb();` so the list statement never enters `mock.calls`; `:649` `/ORDER BY created_at DESC/` is unanchored, so it would match the new text anyway, and it finds `credentialRepo.ts:423` (loadFromDb, untouched). [INFO, claim holds]
- Other `ORDER BY created_at DESC` in product code with no `id` tie-break: `credentialRepo.ts:423` (boot load, no paging) and `routes/presentations.ts:173` (boot load). Not pagination; the PR body names both as out of scope. [INFO]
- PR body "What this does NOT prove": "The new cell asserts the SQL text. No database runs in this suite, so it does not prove that real pages stop repeating." Present. [severity note satisfied]
- PR body says base `444813665a09`; merge-base of #1712 with develop IS `4448136` (develop moved since). Not a defect, merge-tree below covers it. [INFO]

**TESTED / HOW** (vitest 4.1.12, node 26.8.1, `services/vc-issuer`; install proven: `npm ci --ignore-scripts` rc 0, shared build `dist/index.js` present, `deps-present.sh` rc 0 "OK - workspace install present", `--self-test` rc 0)
- A (builder's "red first"): develop's credentialRepo.ts + head's test with only the regex moved back (Q3 added, regex unmoved): **1 failed | 112 passed (113)**, only Q3. Matches claim.
- B: develop's product + head's test (regex moved): 14 failed (Q3 + 13). C: head's product + develop's test file (regex unmoved): **13 failed | 99 passed (112)**: D0, D2, Q1, Q2, E1 x2, E2, K1, X2 x5. Matches the claimed 13 exactly (coupling control: the regex move is load-bearing).
- Green at head: ks1683 file 113/113; whole service **19/19 files, 413/413**. Develop's service run is 412 total, but that first run had the cold-import skips (see #1714), so the clean-develop 412/412 is from the cold-pair worktrees `dev`/`dev2` (412/412 twice).
- Restore control: every tamper restored by sha256 (credentialRepo.ts `ebf5a6ec...`, test `a8ba1625...`), `git status` clean.
- Ratchet `check.cjs services/vc-issuer` at the 1712+1714 merge: rc 0, 0 new errors.
- My first script run mis-restored (relative path to `git checkout --`), which left a tainted tree; I discarded that run's results, force-checked-out head, and redid A-D with sha checks. Reported so the numbers above are the clean ones.

**NOT TESTED**: eslint (builder rc 0 relayed); PGlite page walk (no pglite in vc-issuer, relayed); mutants (builder's matrix not re-run); `pgModel` sort `(x,y)=>y.created_at-x.created_at` observation (not total) not exercised.

## #1714 (KS-1729), head 6905f6e

**FOUND**
- `const KS1729_COLD_IMPORT_BUDGET_MS = 120_000;` at ks1020:89, ks1116:182, ks1683:131; used once each as the hook timeout at ks1020:169, ks1116:291, ks1683:244 (`  }, KS1729_COLD_IMPORT_BUDGET_MS);`). Exactly 2 occurrences per file; `git diff --name-only` = those 3 files; `vitest.config.ts` diff = 0 lines. [INFO, claim holds]
- Each is the first describe-level `beforeAll` that calls `freshModules()` (ks1020:158; ks1116:280; ks1683:229). Other beforeAlls (ks1020:259; ks1116:415,475,525,564,659,706; ks1683:453,624) carry no timeout argument. The module-level sync `beforeAll` at ks1116:267 and ks1683:198 are untouched (no import). [INFO]
- The new JSDoc block is inserted between the existing doc comment `/** Fresh router + errorHandler per describe ... */` and `async function freshModules()` (e.g. ks1020:68 comment, then the new block, then the function at ~:90), so the original one-line doc comment is orphaned from its function. [LOW, cosmetic]
- PR body states plainly: "The ticket's defect did not reproduce on this machine" and "What did NOT reproduce - stated plainly"; it does not claim a fix of an observed red; the red is labelled "a labelled stand-in". [INFO, claim holds]
- Note for Wednesday [LOW, evidence not defect]: my own FIRST vitest run on develop right after `npm ci` + shared build in the shared-clone tree DID reproduce the defect: `Tests 302 passed | 110 skipped (412)`, 3 files failed, hooks ~12.66 s each (ks1683 56 skipped, ks1116 40, ks1020 14 = 110, the ticket's figure). Saved in `v_dev_full.txt`. In four further cold first-runs in fresh worktrees (develop x2, head x2; `cold_run_*.txt`) nothing skipped (412/412 each). So 1 of 3 develop cold runs reproduced, 0 of 2 head cold runs have been exposed to a reproducing condition. The head's protection is shown by the stand-in, not by a natural cold repro. The PR body's "did not reproduce" is true for the builder's machine; it could add "reproduced once in the gate".

**TESTED / HOW**
- Stand-in `--hookTimeout=50` on the 3 files: develop's text `32 passed | 244 skipped (276)`, 3 files failed, 11 x "Hook timed out in 50ms"; head `276 passed (276)`. (Builder got 64/211 at 50 ms; counts are timing-dependent, direction identical.) Default timeout: both 276/276. Whole service at head 412/412 (19/19).
- Tamper control: constant set to `1` in all 3 files at the DEFAULT timeout: `Tests 166 passed | 110 skipped (276)`, 3 x "Hook timed out in 1ms". Exactly 110, as claimed. Restored from copies; `shasum -a 256` diff equal (`bdcb05ea3ad2... 7b1d82a6da51... dea975d3bb79...`, matches the PR body's prefixes); restored run 276/276; `git status` clean.
- Shape (i) blocked: appended `const __p = await Promise.resolve(1);` at module scope of the ks1683 file, ran `node scripts/typecheck-tests/check.cjs services/vc-issuer` in Blockchain/Dev: **rc 1**, "1 errors: 0 in the baseline, 1 new", `ks1683...test.ts(658,24): TS1378: Top-level 'await' expressions are only allowed when the 'module' option is set to 'es2022'...`. Control: same command unmodified rc 0, 0 errors. `services/vc-issuer/tsconfig.json:3-4` `"target": "es2021"`, `"module": "commonjs"`. File restored by sha (`dea975d3...`).
- 1712+1714 combined tree: 413/413; at `--hookTimeout=50` the 3 files 277/277 (276 + Q3); ratchet rc 0.

**NOT TESTED**: that 120 s is enough on a genuinely slow cold run (no run here exceeded ~13 s); the ticket's "second effect"/run E; Node 24; lint/tsc (builder relayed).

## #1711 (KS-1735), head d21a838

**FOUND**
- `systemTest/__tests__/support/generated_guard.sh:49-54`: `if ! cp -R "$GENERATED_GUARD_STASH/." "$GENERATED_GUARD_GEN/" 2>/dev/null; then ... printf ... KEPT ... if [ "$rc" -eq 0 ]; then exit 1; fi; exit "$rc"`; success path still `rm -rf "$GENERATED_GUARD_TMP"` at :56 (reached only if the cp succeeded). Snapshot-failed branch `:38-44` now prints "the partial snapshot is KEPT at" and returns without `rm -rf`. [INFO, claim holds]
- LOW: `generated_guard.sh:37` `local rc=$?` reads the status at trap entry. The only real consumer, `bootstrap_login_diagnosis.test.sh:52` `trap 'stop_stub; generated_guard_restore' EXIT`, runs `stop_stub` first, so `$?` is stop_stub's status, not the suite's. Micro-model (chain.sh): suite `exit 3`, chained trap, restore "fails" -> `f saw rc=0`, process rc 1. So in that consumer a failed restore still exits non-zero (the safety goal holds) but the suite's own status is flattened to 1 (or stop_stub's, e.g. 143). The PR body says "the suite's own status when it had one"; true for a direct trap (the new suite's cell `failrc` rc 3), not for the chained one. Not a regression (before: always the suite's own rc, but silent data loss). Suggest: capture rc inside the chain (`trap 'rc=$?; stop_stub; ...'`) or document. Not blocking.
- `pre_suite.test.sh` and `quarantine_call_sites.test.sh` untouched: `git diff --stat origin/develop...pr/1711 -- <both>` empty; PR touches exactly 2 files (+205/-2). Option A confirmed. [INFO]
- New suite uses `mktemp -d "/tmp/ks1735.XXXXXX"` (own prefix, cleans only its own dir), not `$TMPDIR`. [INFO]

**TESTED / HOW**
- New suite at head: rc 0, `generated_guard_restore.test.sh: 15 passed, 0 failed` (15 `ok` lines counted; the 3 "FAIL" greps are section headings). Also run under `/bin/bash` 3.2.57 (arm64): 15/0; `/bin/bash -n` on both files OK.
- Red/green: develop's guard blob (sha `4829d76f...` per body) swapped in under head's test: rc 1, **10 passed, 5 failed**; the 5 reds are "a failed restore says so", "stash survives a failed restore", "message names where the kept stash is", "suite that exited 0 reports non-zero", "PARTIAL stash survives a failed snapshot". Control cells pass on develop's text: fake cp refuses `/generated/` destination and passes other destinations through; clean run rc 0, sentinel restored, stash removed; "intercepted" cells confirm the fake was reached. Guard restored by sha256 (`6ee51a49...`) and `git status` clean.
- Runner: `scripts/run-shell-suites.sh --check-unreached`: head "OK - all 96 tracked shell suite(s)", develop "all 95" (control: +1). Full runner at head: rc 0, `=== systemTest/__tests__/generated_guard_restore.test.sh ===` reached, its 15/0 line present, `shell suites: 94 passed, 0 failed, 2 skipped (of 96)` (that run was before my `npm ci`; the 2 skips are no PostgreSQL binaries and "workspace install absent", environmental; builder's gate showed 1 skipped).

**NOT TESTED**: Linux/bash 5 (builder says not run either); the `generated_guard_existed=0` restore path (covered only indirectly); a real disk-full/permission cp failure (the instrument is a fake cp); the bootstrap_login_diagnosis suite itself with a failing restore.

## Batch

- merge-tree (`git merge-tree --write-tree`): develop+#1711 rc 0; develop+#1712 rc 0; develop+#1714 rc 0; #1712+#1714 rc 0 (tree 37b7188); (1712+1714)+#1711 rc 0. Only shared file between PRs: the ks1683 test file (#1712 `@@ -419`, `@@ -519`; #1714 `@@ -108`, `@@ -220`); #1711 shares no file with either.
- The merged 1712+1714 tree passes: 413/413, 277/277 at hookTimeout 50, ratchet rc 0.
- Recommended order: **#1712, then #1714, then #1711**. Reason: #1712 is the smallest product change and its base is the oldest; #1714 then merges with develop in (as both authors say), and #1711 is independent (systemTest only) so it can go any time. Order among them is not forced by conflicts.
- Cleanup left in place: worktrees `wt_dev wt_head wt_dev2 wt_head2` and `tmp.*` dirs in the workspace; nothing deleted.

## For Wednesday to decide
1. Whether #1714's PR body should record that the gate reproduced the defect once (1 of 3 cold develop runs).
2. Whether to ask for the #1711 chained-trap rc note (LOW) before merge or file it.
3. Round 2 (or the tier-1 gate) was not run; this is round 1 of 2.
