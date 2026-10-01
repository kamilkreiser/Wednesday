# gate53 COMMISSION — ONE Secuura PR: #1369 KS-530 (T1, round 1); author and merger Seat B 54th, round 53

Filled by fill_gate53.py at 2026-10-01T15:03:39Z from pins_gate53.json (measured 2026-10-01T14:37:32Z). This restates Wednesday's commission to the drafter (2026-10-02), requirement by requirement. The gate prompt carries each requirement by name, and the launcher refuses a prompt that is missing any of the 35 keywords (each matched as a token).

## The PR
| PR | ticket | tier | head | parent | merge-base | ahead / behind | files (+/-) | subject declared -> lands |
|---|---|---|---|---|---|---|---|---|
| #1369 | KS-530 | T1 | `ce051988b787f510c7ca5db5bbc474ef4b8a8492` | `ea6fcecc3a6f` | `ea6fcecc3a6f` | 1 / 0 | 3 (+3/-18) | 83 -> 91 |

- develop `ea6fcecc3a6f71a4f397ea678da54a06df130cd7` (tree `48f5f8afa6ef1f03f2d64e4afa24fd9f75213ad7`) = #1368's merge. 0 behind.
- END_TREE `d0f0389e191820ff3dc2d9c98d9d661336eb90e3` (`3 files changed, 3 insertions(+), 18 deletions(-)`) = the seat's PREDICTED tree. Four instruments agree (end_tree_crosscheck_1.out): merge-tree + commit-tree, the head's own tree (parent == develop), GitHub's `refs/pull/1369/merge`, and the head's diff applied `--cached` onto develop under a temp index (no merge-tree). Control that differs: develop's own tree 48f5f8afa6ef.
- MODES (git ls-tree): all 3 PR paths 100644 at head / alone / END_TREE; control `Blockchain/Dev/scripts/run-migrations.sh` 100755 at develop / head / END_TREE.
- IDENTICAL at develop / head / END: `pre-push` ffc25ebc37d4, `preflight.sh` 270b8913c009.
- BYTE-EQUAL at develop / head / END (pin (K)): `audit/audit-gate.mjs` 8e236ee70ce1, `audit/audit-locks.mjs` aff23b0420ce, `audit/baseline-contract.mjs` ef82d7c5211d, `audit/baseline-contract.test.mjs` 2379c0aeee6e, `audit/expected-case-count` 04f9fe46068b, `audit/lock-discovery.mjs` 3dd903b527f2, `originate/package.json` 930fa8afb9ff, `originate/package-lock.json` 3e088e4e1855, `originate/Dockerfile` ac2fb91bf7d8, `mcp-server/package-lock.json` ec20749768f0, `prisma/schema.prisma` 96c3342fa867.
- Merger: Seat B 54th (the author). Pane: `QA/Secuura-batch1369`. Report dir: `2026-10-02-batch1369-g53`.

## The claim (the ONE READY) and the ruling it rests on
- 3 files, +3/-18: `package.json` +3/-0 (the scoped override `"@prisma/dev": { "@hono/node-server": "^1.19.15" }`), `package-lock.json` 0/-11 (the nested `node_modules/@prisma/dev/node_modules/@hono/node-server` 1.19.11 removed), `audit-baseline.json` 0/-7 (the GHSA-frvp-7c67-39w9 row removed).
- The lock was made by a ONE-ENTRY PRUNE then npm validation, because npm's override is inert against a complete lock — approved by Wednesday 2026-10-02 (`fleet/briefs_staged/2026-10-02_answer_seatB54_method.md`, conditions 1-4), superseding the brief's Q2 regen route.
- Lock delta 0 added / 1 removed / 0 changed / 0 flips; `npm ci` rc 0; the ruled `npm install --package-lock-only` in node:24-alpine (npm 11.19.0) leaves it byte-identical (sha256 `1e418a81ce03…`); an independent from-scratch resolve gives the same dedupe.
- Red-first rc 1 naming frvp; at head contract / leg 6 / leg 7 rc 0; leg 6 reported 11 -> 9, baselined 25 -> 24; CLEANUP now names GHSA-92pp (nothing removed).
- Prisma: resolution from `@prisma/dev` returns the hoisted 1.19.17; `prisma --version`, `prisma generate`, `prisma dev --help` rc 0. No server started.
- Suites: originate jest 90 suites / 1062 tests / 0 failed; mcp-server vitest 5 / 0 failed; tsc rc 0. No image reads the root lock. Trailers: 0 (control `bf277eead268`, 55 bytes).

## What the gate must rule (by name)
1. **NO COLLATERAL**: the root locks' `packages` diffed key by key: 1 removed, 0 added, 0 changed, 0 flips; `@prisma/dev` byte-identical; hoisted 1.19.17 unchanged; the other 44 locks untouched; a planted-change control. (NO-COLLATERAL, PRISMA-DEV-BYTE-EQUAL, OTHER-LOCKS-UNTOUCHED)
2. **The lock is self-consistent and reproducible**: `npm ci` from it; the ruled container command leaves it byte-identical (with a control that npm ran); an independent resolve of prisma 7.8.0 + the override dedupes; without the override it gives 1.19.11. (NPM-CI-HEAD, LOCK-IDEMPOTENT, INDEPENDENT-RESOLVE, COUNTERFACTUAL)
3. **A real fix, not a false one**: external specifier, not bundled; resolution from `@prisma/dev`'s own dir returns the hoisted 1.19.17 (main entry + walk up; `/package.json` throws ERR_PACKAGE_PATH_NOT_EXPORTED); `prisma --version`, `prisma generate` (as the Dockerfile runs it), `prisma dev --help` rc 0; which of them loads the module. No server. (EXTERNAL-NOT-BUNDLED, RESOLVES-HOISTED, PRISMA-RUNS)
4. **The value**: 2.x is published, so `>=` would take the major; `^1.19.15` is right. (CARET-NOT-GTE)
5. **The audit**: red-first rc 1 naming frvp; contract / leg 6 / leg 7 rc 0 at head; frvp neither reported nor baselined; **explain the 11 -> 9**; the CLEANUP line verbatim (GHSA-92pp, nothing removed); the row removal by KEY SET; cohort 2026-10-09 -> 2; no `expires` changed. (RED-FIRST, AUDIT-LEGS, REPORTED-11-TO-9, CLEANUP-VERBATIM, ROW-KEYSET, COHORT-TWO)
6. **Images**: no Dockerfile copies the workspace-root lock (every Dockerfile, a control line that must hit); else build that image only. (NO-IMAGE-READS-ROOT-LOCK)
7. **Suites and tsc**: originate (jest), mcp-server (vitest), 0 new reds; tsc no regression. (SUITES-0-NEW-REDS, TSC-NO-REGRESSION)
8. **PR text**: {KS-530} only, no closing keyword, other keys de-hyphenated; the method stated plainly; NO Co-Authored-By trailer (control `bf277eead268`); the subject lands <= 92. (KEYSCAN-OWN-KEY, NO-CLOSING-KEYWORD, METHOD-STATED, NO-TRAILER, SUBJECT-LANDS-AT, SUBJECT-TRUE-OF-DIFF, PR-BODY-CLAIMS)
9. **The census** of other open PRs touching the 3 paths (report; a rebase they may need is not ours); **NOT TESTED, explicit.** (COLLISION-CENSUS, NOT-TESTED-LIST)
10. **The merge**: clean, END_TREE == the prediction, modes. (CLEAN-MERGE, END-TREE, MODES) Plus TIERING, DISK-ENOSPC, **REPORT-HASH-LAST**; the `## MERGE ADDENDUM` goes LAST. The pass is proportionate (usage 95%, Kam's 17:40:22 grant).
- NOT in scope: a live server, a `prisma dev` server, Schemathesis, any deploy, any DB, the GHSA-92pp cleanup, any re-date.

## GO
The GO string, as the GO mail's SUBJECT: `GO (Seat B 54th): merge 1369 on gate53`. Seat B 54th merges #1369. Verdict mail subject: `[QA -> Wednesday] GATE53 #1369 (Seat B54 author and merger, round 53; T1 dependency resolution: a scoped @prisma/dev override, one nested lock entry pruned, the frvp baseline row removed)`.

## The drafter's predictions (the gate re-derives each and never adopts one)
- pin_gate53.py -> pin_1.out: END_TREE `d0f0389e191820ff3dc2d9c98d9d661336eb90e3`. The measured numstat: +3/-18 over 3 files (the seat claimed +3/-18): 0 11 Blockchain/Dev/package-lock.json; 3 0 Blockchain/Dev/package.json; 0 7 Blockchain/Dev/scripts/audit/audit-baseline.json.
- lockdiff_gate53.py -> lockdiff_1.out: LOCKDIFF PASS: 0 FAIL of 11 checks | base ea6fcecc3a6f head ce051988b787
- auditset_gate53.py -> auditset_1.out: AUDITSET PASS: 0 FAIL of 4 checks | base ea6fcecc3a6f head ce051988b787 | reported 11 -> 9, baselined 25 -> 24, CLEANUP 14 -> 15, red-first fresh ['GHSA-frvp-7c67-39w9']
- registry_gate53.py -> registry_1.out: REGISTRY PASS: 0 FAIL of 4 checks
- images_gate53.py -> images_1.out: IMAGES PASS: 37 Dockerfiles, 0 image(s) copy the root lock, 0 unresolved, control FIRED | tree ce051988b787
- keyscan_gate53.py -> keyscan_1.out: KEYSCAN PASS: 10 checks over 1 PRs, 0 FAIL (trailer control FIRED)
- gh_read_gate53.py -> gh_read_1.out: CENSUS 21 other open PR(s) read | 12 touch a kit path or carry a census key ['KS-530'] | 3 kit paths | client-human PRs named: ['1360'] (all of them in kit.json reported_overlaps; the launch action re-reads it, rc 15 on any hit outside reported_overlaps)
