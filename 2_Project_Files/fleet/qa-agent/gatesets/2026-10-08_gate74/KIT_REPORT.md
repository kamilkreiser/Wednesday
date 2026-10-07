# gate74 KIT REPORT — drafter to Wednesday

- **Member:** #1423 KS-1164, the locale/count cell. Tier 2, with the PREFLIGHT WEIGHT. Seat R 13th, branch `feature/ks-1164-locale-count-cell-ra13-2`, head `d76b4a7586fb51b3f67823cbfc28d796bd7812c5`, END_TREE `39c96de3cb40c4a8426c0eb44cda64a3ba4f266f`, ONE parent `b280b74ff07b6aa48c0d1f55b4a931842a0e368c`.
- **Also measured, not gated:** #1422 (§5d comments, tier 3). Head `26589c851846d69c26638e3dd4ff36a5db54a9d3`, same base. It is measured here for the merge brief.
- **Drafted:** 2026-10-08 03:29–04:45 AEDT (2026-10-07 16:29Z–17:45Z) by one Wednesday kit-drafting subagent.
- **Built and dry-run only. Not launched.** Nothing was merged, pushed, commented, mailed, ticketed or routed. No tmux, no cockpit, no Linear.
- **Where it wrote:** this folder (its `_scratch/` is gitignored and holds only the dry runs' outputs) plus the drafter's scratchpad (`…/scratchpad/g74/`).
  - Every git write verb ran in the scratchpad's `clone --shared` copy: merge-tree, commit-tree for SIMs, worktree, archive.
  - Nothing was written under `!CODING`.
- **GitHub:** GETs only, with GH_TOKEN read by name.
- **Every figure below is a PREDICTION.** The gate re-measures each one.

## 0. Bottom line

1. **Launch-ready, with ONE ruling outstanding: Q-SCHEMA74, the Actions comparator.**
   - `kit.json actions_comparator` is `null` on purpose. The launcher refuses rc 8, and a real repin refuses rc 8.
   - The final real-kit dry run (17:27:54Z) went rc 13, from launcher rc 8.
   - With a stand-in kit (comparator `base`, a test value only), the whole path runs to rc 0: dry run 17:13Z, launcher `--check` rc 0, 11 pins EQUAL, 43 keywords.
   - The routing line is NOT added: `ROUTING_LINE.txt` holds it, and a real run refuses rc 1 until it is added.
   - `merge_seat` = `Secuura/Blockchain-R`, ordinal `Seat R 15th`, per the commission and gate73 Q-SEAT. GO string `GO (Seat R 15th): merge 1423 on gate74`.

2. **develop read at START and END, unmoved.**
   - Instrument: `ls-remote` from the checkout with its own `core.sshCommand` and `GIT_SSH_COMMAND` unset.
   - develop: `eae08a3f441c9d9570061df560eefe146ad50d2d` at 16:29:56Z, 17:12:03Z, 17:27:59Z and 17:28:34Z.
   - `refs/pull/1423/head` and its branch both read `d76b4a75…`; `refs/pull/1422/head` and its branch read `26589c85…`; #1383 is unmoved at `32e8459bc0f5`.
   - develop is base + 3 Peter merges (#1421 / #1424 / #1425): 24 paths, 1 of them under `Blockchain/Dev/` (`scripts/base-image-watch.sh`). It moved both platform docs and touched 0 of #1423's paths (c1 P12).

3. **The merge-in and leg-14 measurement — the commission's critical question.**
   - **#1423: NO merge-in is needed.**
     - `c4 merged` M1-M7 on develop eae08a3f: 11 checked, 0 FAIL.
     - `merge-tree --write-tree` gives rc 0, tree `a6227cb3e8e759de15a4aaac4393fbfe2f5ea6b1`. The control pair (gate73 #1407 + #1409 heads) gives rc 1 on both docs.
     - diff(develop, merged) is exactly the PR's 3 paths.
     - **M4 is a BYTES check:** each merged doc equals develop's blob plus the head's exact fragment inserted before `</body>`.
       - flow `3f8f3c0ce95b…` = `e3eae857b248…` + 81 lines.
       - cheat `e4c8ee75a4bf…` = `c3a8e89a636f…` + 55 lines.
     - So git's auto-merge IS the keep-both composition, and the docs need no recomposition. Develop's doc edits were mid-document (KS-1445, KS-1439); #1423 appends at the tail.
     - GitHub agrees: `mergeable: true`, `mergeable_state: unstable` (failing non-required checks; this is no testing claim).
     - **The squash is an API call and runs no local hook, so leg 14 is NOT in its path.**
     - A merge-in push WOULD be refused. Its `@{upstream}..HEAD` carries develop's whole advance, which includes `Blockchain/Dev/scripts/base-image-watch.sh`; that selects the full preflight, and leg 14 fails (measured on the SIM, below).
   - **#1422: NO merge-in is needed.**
     - `t3check_1422.py` C1-C7: 6 checked, 0 FAIL. merge-tree rc 0, tree `2c8b09845a1aa4700ad5fb55ea39a2966365af9b`, 3 paths, blobs == head.
     - It touches no doc.
     - Its OWN changed set has 2 `Blockchain/Dev/` paths, so any push to its branch would run the full preflight and be refused. The squash is an API call.
   - **Both PRs, either order:** final tree `d6ee60d91e2f0850523b9ba59cc4cc998209b97a` (order-independent).

4. **The preflight's weight, MEASURED by the drafter.**
   - Runner: `preflight_run.py`, the hook's exact invocation, after S-1 (Blockchain/Dev `npm ci` + shared build, dist PRESENT; all four `systemTest/*` installed). Real worktrees in the scratch clone.

   | tree | shell suites | verdict |
   |---|---|---|
   | HEAD `39c96de3` | `71 passed, 0 failed, 0 skipped (of 71)` | `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` (the 3 = the stack legs; the local stack is down) |
   | SIM squash (develop + #1423, `a6227cb3`) | `70 passed, 1 failed, 0 skipped (of 71)`, `FAILED: systemTest/__tests__/no_hardcoded_slot_literals.test.sh` | `PREFLIGHT FAILED on leg(s) 14 … (12/15 legs ran)` |
   | SIM both (+ #1422, `d6ee60d9`) | identical to the SIM squash: 70/1 of 71, leg 14 only | — |

   - So the squash adds NO failing leg: the SIM's only red is develop's own KS-1450 red, the same line R 14th's push printed at eae08a3f.
   - The pre-existing `VERDICT: MISMATCH` line (gate73 R3) was NOT printed in any of the three runs: case-insensitive `mismatch` 0, against 21 `verdict` lines in the same files.

5. **Leg 14, two ways, in REAL worktrees.**
   - `no_hardcoded_slot_literals.test.sh`:

   | tree | result | files scanned |
   |---|---|---|
   | base | 9/0 | 1202 |
   | head | 9/0 | 1203 (one more: the new suite) |
   | develop | 8/1 | 1205 |
   | SIM | 8/1 | 1206 |

   - Lines carrying `slot2` in the baseline file: base 0, head 0, develop 8, SIM 8 (14 occurrences). The planted-literal CONTROL fires in all four.
   - **#1423 adds no leg-14 literal.**
   - ⚠ **TRAP found and recorded.** Run on a `git archive` export, the suite refuses: "not a git work tree", 0 files scanned. That FALSE red would read as 8/1 on base and head too. c3 `leg14` refuses a non-worktree.

6. **The package's own suites, one parser (vitest JSON; files = testResults), through `npm run test:unit` only.**

   | tree | files | tests (all passed) |
   |---|---|---|
   | base | 75 | 1360 |
   | head | 76 | 1363 |
   | develop | 76 | 1386 |
   | SIM | 77 | 1389 |

   - Subset compare: base→head and develop→SIM both hold (0 → 0 reds); the new suite has 3 cells, all passed, absent before.
   - The author's "249 → 251 suites" are vitest's describe-block counts (`numTotalTestSuites`), not files.
   - `tsc` (the two `lint` legs): rc 0, 0 lines each.
   - The pre-push format gate on the push list: rc 0, `1 package(s) checked, 0 skipped, 0 failed`.

7. **Red-first by TAMPER, one arm per conjunct** (c3 `tamper`, report.ts:104, anchor count 1). Arms: both counts, passes only, fails only.
   - Each arm: rc 1, 3 total, 2 passed, 1 failed. The red is exactly `RED KS-1164 F-3`, and both CONTROLs pass.
   - After each arm the file was restored sha256-equal (`c18d61313c2ae42e`) and `git status` was clean.
   - Untampered (`onefile`): 3/3.

8. **Docs at the head** (c4 `docs` D1-D7): 16 checked, 0 FAIL.
   - One insert per doc, immediately before `</body>`: flow 81 lines, cheat 55.
   - Flow 26 and cheat KS-1164, each unique and absent at the base.
   - Per-tag balance holds in each fragment and across the whole doc.
   - The control is built from the DOCUMENT: the base's own last flow number 31 and last key KS-591 each read 1.
   - Planted arms each REFUSED: a `</h2>` deleted, the block placed after `</body>`, the block doubled.
   - Calibration: the base's doc blobs `812ad45d…` / `368db61c…` ARE gate73's step-4 composed targets (R 12th GO 1410 v2), so the lineage's last prediction landed byte for byte.
   - `html_docs_matrix` 12/0 at every tree is quoted as the guard's tally, NOT as tag-balance evidence.

9. **Actions** (gh `actions`, read at ~17:05Z): Security Scanning is class (1) and HOLDS (Dependency Audit, the audit-contract step, the log needle, `##[group]` present). PR Security Gates is class (2) and HOLDS. For `pr`, class (3) depends on the comparator:
   - **vs develop eae08a3f: does NOT hold** (rc 1). Schemathesis is red at the head and green on develop.
   - **vs the base: HOLDS** (rc 0).
   - **vs the union: HOLDS** (rc 0).
   - → Q-SCHEMA74.
   - One FALSE ZERO observed: a develop runs read returned 0 runs at 16:35:23Z and 2 on the immediate re-read. gh now re-reads a 0-runs comparator.

10. **The merge tool chain** (for the brief; measured with COPIES in the scratchpad).
    - `mergera1.py --dry` (sha256/16 `aaf230e7d1975213`, unchanged), with `--repo` = the scratch clone and hand-written addenda:
      - **#1423: rc 0.** Docs declared `merged_blob_paths` with the MERGED targets; predicted tree == `a6227cb3`; subject 73; MG-3 {KS-1164}.
      - **#1422: STOP.** "the PR body carries no `Refs KS-####` line". With a body carrying three Refs lines (a one-line SIMULATION in a further copy, disclosed): rc 0.
    - **`build_addendumra12_gate73.py` cannot produce either addendum** (Q-BUILDER74). Both heads sit BEHIND develop with no merge-in. It hardcodes `merged_blob_paths: []`, takes one own key, and demands both docs.

## 1. The kit (this folder)

| File | What it is |
|---|---|
| `kit.json` | All pins. One row (head, branch, END_TREE, parent, numstat, modes, subject, flow 26, key KS-1164, report.ts blob, the KS-1164 fix commit, the READY and ctx mails). Also: tooling paths; pre-existing MISMATCH blobs; the leg-14 block; the Actions classes plus the observed false zero; `merge_tree_control`; `predicted_squash`; `predicted_both`; `t3_1422` (#1422's pins for the merge seat's instrument); `merge_seat` / `merge_seat_ordinal`; `actions_comparator: null` (Q-SCHEMA74); `script_sha256` (11 files). |
| `lib_gate74.py` | Carried from lib_gate73 and re-keyed. Read-verb `git()`; `wgit()` refuses write verbs under `!CODING`; composee5's readers extracted at pinned lines with sha asserted; the cheat reader widened; GH GETs; `Tally`. There is no default row. |
| `composee5_copy.py` | Byte-identical to gate73's (`f9ab42d9…`). |
| `c1_pin_gate74.py` | P1-P14 (P10 head == base on 21 tooling paths, with develop's moves REPORTED; P11 disjoint from #1422; P14 TEST-ONLY). Self-test 9/9. |
| `c3_suites_gate74.py` | `perf` / `perfcmp` / `onefile` / `tamper` (3 arms) / `tsc` / `format` / `preflight` / `pfcmp` / `leg14`. Every worktree mode is BOUND to an `--expect-tree` (rc 11 otherwise). `preflight` refuses rc 12 without S-1. Self-test 9/9 on CAPTURED lines. |
| `c4_docs_gate74.py` | `docs` (D1-D7) and `merged` (M1-M7, with the `MERGE-IN NEEDED` / `LEG-14 EXPOSURE` verdict lines). `cheat_split` reads one heading at a time and treats develop's unkeyed KS-1445 heading as BASE-STATE. Self-test 8/8. |
| `gh_gate74.py` | `api`, `prtext` (T1-T7), `actions` (`--comparator develop\|base\|union` REQUIRED; all three verdicts printed), `census`. Self-test 16/16, using the REAL #1423 body as the fixture. |
| `t3check_1422.py` | The merge seat's READ-BACK for #1422 (C1-C7: pins, hunks, comment-only with two controls, no docs, merge-tree, base..develop, leg-14 exposure). NOT a gate. Self-test 5/5. |
| `fixture_body_1423_at_draft.md` | The live #1423 body, GET at draft, sha256/16 `bcfec623a2b7d646`. |
| `prompt_gate74.txt` | The gate prompt template. `prompt_gate74.rendered.txt` and `head_at_launch.txt` are the LAST real-kit dry run's render, with comparator UNRULED. |
| `launch_qa_secuura_gate74.sh` | The launcher. It holds no PR literal; it reads P / B / D / S / C from the head file and checks each against kit.json. |
| `repin_and_launch_gate74.sh` | The launch action. **Run only with `--dry-run`.** `G74_CLONE` (dry-run only, refused under `!CODING`) let the drafter point it at its scratch clone. |
| `merge_inputs/` | DRAFT squash/PR bodies for the brief: `1423.squash_body.DRAFT.txt` (5,277 B, == the live body) and `1422.pr_body_with_refs.DRAFT.txt` (4,375 B, Q-1422-REFS). |
| `RULINGS_wednesday.md` | Carried rulings R1-R7, plus 13 OPEN questions with recommendations. |
| `ROUTING_LINE.txt` | `QA/Secuura-gate74\|coagent@agentmail.to\|yes`. NOT added to `inbox_routing.conf`; the drafter measured 0 copies there, with gate73's line at 1 as the control. |
| `drafter_evidence_2026-10-08/` | Every run's console and JSON (`runs/`), the 25 launcher/repin arms, the mergera1 dry runs and draft addenda, the PR bodies at draft, and the drafter's helper scripts. |

`c2_product` is NOT carried. Its content for a test-only row is c1 P14 (the product is untouched) plus c3 `tamper` (the product drive).

## 2. Arms: expected vs actual

**Self-tests on the pinned files** (final pass, 17:2xZ):

| Test | Result |
|---|---|
| c1 | 9/9 |
| c3 | 9/9 |
| c4 | 8/8 |
| gh | 16/16 |
| t3check | 5/5 |

All rc 0.

**Launcher and repin arms: 25, all fire as intended** (`launcher_repin_arms/`):

| Arm | rc |
|---|---|
| live, stand-in kit | 0 |
| real kit, comparator unruled | 8 |
| head-file wrong head | 7 |
| head-file comparator mismatch | 7 |
| author seat | 8 |
| comparator not in the enum | 8 |
| GO names the author | 8 |
| keyword missing | 33 |
| runner-trap rule removed | 33 |
| `--no-verify` hold removed | 39 |
| pull/head moved | 6 |
| develop moved | 17 |
| bad pin | 31 |
| missing file | 30 |
| non-TTY launch | 21 |
| moved kit | 2 |
| repin: short head | 9 |
| repin: missing develop | 9 |
| repin: wrong head | 11 |
| repin: wrong develop argument | 11 |
| repin: `--no-api` on a real launch | 9 |
| repin: `G74_LSFILE` on a real launch | 16 |
| repin: `G74_CLONE` on a real launch | 16 |
| repin: clone under `!CODING` | 16 |
| repin: head moved per the stand-in ls-remote | 11 |

- The first missing-file run read 31: MY arm reused the bad-pin directory, so the pin check fired first. Re-run on a clean copy: 30 (`L_missing_file2.out`). This was an arm defect, not a tool defect.

## 3. The authors' claims: HOLD / DO NOT HOLD (drafter's instruments)

**HOLD:**
- head, END_TREE, one parent;
- 3 paths +238/-0, the new suite 100644 (blob `cdc33036…`);
- report.ts `ac59af37cbc6` at base, head and develop;
- `f3bf8698d628` (#1271) an ancestor of the base;
- 0 trailers (1 B vs the 55 B control), 0 Co-Authored-By, only KS-1164 hyphenated;
- the tamper 2/1 of 3, restored 3/3;
- base 1360 → head 1363 tests;
- tsc rc 0;
- html_docs_matrix 12/0 (the guard's tally only);
- exactly one block per doc;
- flow 31. → 26.; cheat KS-591 → KS-1164 (the author wrote "KS 591", de-hyphenated);
- the runner trap (the config's 15,000 ms vs vitest's 5,000 ms default);
- the four platform suites UNMEASURED;
- "no runtime branch moves".

**Correction to a reader's figure:** "249 → 251 suites" is describe blocks, not files (75 → 76 files).

**DO NOT HOLD:** none found.

**Correction to the COMMISSION:**
- #1423 does NOT carry the "writeGateReport overwrite fix". It is test-only; that fix landed earlier as `f3bf8698d628` (#1271).
- #1422's TS file is `services/transfer/src/index.ts`, not api-gateway.

## 4. NOT covered by the drafter (the gate owns these, or they are UNMEASURED)

- **The four platform suites, and the preflight's 3 stack legs:** UNMEASURED (stack down). Never a pass.
- **The preflight at the BASE:** NOT RUN by the drafter. The gate runs it as the comparator; the head's run is already 71/0.
- **eslint, knip, `npm run quality`:** NOT RUN.
- **The suite under a non-grouping locale:** NOT RUN (Q-LOCALE).
- **The CI runner's toolchain:** NOT read. The drafter ran node v24.7.0 against the package's `engines >=24.11.0` (Q-ENGINES).
- **Ticket states:** no Linear read.
- **#1422's Actions:** read once (16:35Z), not re-read at the end.
- **Whether R 15th's inherited tools re-key cleanly:** UNMEASURED. Only the R 14th hashes were re-read.

## 5. Drafter defects, caught and fixed (disclosed)

1. **The archive trap (§0.5).** The first leg-14 reads ran on `git archive` exports, where the suite refuses, giving a FALSE 8/1 on every tree. Re-run in real worktrees, and c3 refuses a non-worktree.
2. **The c4 cheat reader raised on develop.** The pinned reader requires the key at the END of the heading; develop's KS-1445 heading violates that. I fixed the instrument (one heading at a time, unkeyed headings compared as base-state), not the measurement.
3. **c4 self-test count.** I wrote a threshold of `>= 20` for a 16-check run, which false-FAILed. Fixed to `== 16`.
4. **`slot2` count predicate.** The kit first said "8" without a predicate. It is 8 LINES / 14 occurrences, and both are now stated.
5. **gh wording.** class (2)/(3) rows said "develop's" whatever the comparator was, and X4 claimed develop "PASSES" a workflow it has no run of. Both are fixed.
6. **The zsh word-split slip, again** (gate73's defect 6 family). My final self-test loop passed `"script --flag …"` as ONE word, and every call failed to start. Nothing was moved or deleted. Re-run as five explicit calls; all rc 0.

## 6. OPEN QUESTIONS for Wednesday (detail and recommendations in `RULINGS_wednesday.md`)

| Question | Recommendation |
|---|---|
| **Q-SCHEMA74 — BLOCKS LAUNCH** | `base` |
| Q-SEAT74 | confirm Seat R 15th |
| Q-SUBJ | `KS-1164: assert the k6 status-code breakdown prints locale-grouped counts` (73) |
| **Q-BUILDER74** | a new builder copy with `RA15_LANDING=behind`, `RA15_DOCS`, `RA15_OWN_KEYS`, with arms |
| **Q-1422-REFS** | PATCH three Refs lines into #1422's body on your word |
| Q-1422-SUBJ | `KS-998, KS-1435, KS-591: add the 5d WHY comments to the three gate73 lines` (74) |
| Q-ORDER74 | #1422 first |
| Q-UNKEYED | polish |
| Q-ENGINES | polish |
| Q-LOCALE | polish |
| Q-OTHER-SITES | polish |
| Q-BRIEF-WORDING | a correction, no ruling |
| Q-PREFLIGHT-BUDGET | accept |

## 7. Launch (Wednesday runs it; the drafter did NOT)

After ruling Q-SCHEMA74 (set `actions_comparator` in kit.json) and adding `ROUTING_LINE.txt` to `inbox_routing.conf`:
```
script -q /dev/null bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-08_gate74/repin_and_launch_gate74.sh --head-1423 d76b4a7586fb51b3f67823cbfc28d796bd7812c5 --develop eae08a3f441c9d9570061df560eefe146ad50d2d
```
- **If develop has moved** (for example, #1422 landed first), the script refuses rc 10, prints the re-predicted squash, and gives the `--repin-develop <sha>` to pass.
- **If the advance makes a merge-in necessary,** it refuses rc 13 ("RE-DRAFT, never --no-verify").
- **The first real run creates `_scratch/clone`** (gitignored) inside this folder.

## 8. RUNG 5 (after launch)
- The pane is up under `QA/Secuura-gate74`.
- The prompt's first line is `ultrathink`.
- The gate writes `NOT-TESTED.written-first.md` first, then runs its self-tests.
- Expect about 25 minutes of preflight wall clock, plus about 1.6 GB of installs per worktree.
