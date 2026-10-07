# gate73 KIT REPORT — drafter to Wednesday

- **Batch:** #1407 KS-998, #1409 KS-1313 + KS 1326, #1408 KS-1435, #1410 KS-591 custody. All T2. All one commit on base / develop `147ae442074c7f3b5be9ce7ccc4452c8dae34b4f`.
- **Drafted:** 2026-10-07 16:27–17:30 AEDT (05:27Z–06:30Z) by one Wednesday kit-drafting subagent.
- **Built and dry-run only. Not launched.** Nothing was merged, pushed, commented, mailed, ticketed or routed. No tmux, no cockpit.
- **Where it wrote:** this folder, plus the drafter's scratchpad (`…/scratchpad/g73draft/`).
  - Every git write verb ran in a `clone --shared` copy: either the scratchpad's or this kit's `_scratch/clone`, which is gitignored.
  - The shared checkout was only read.
- **GitHub:** GETs only, using GH_TOKEN read by name. No Linear reads at all.
- **Every figure below is a PREDICTION.** The gate re-measures each one.

## 0. Bottom line

1. **Launch-ready, with ONE ruling outstanding (Q-SEAT).** `kit.json merge_seat` is `null` on purpose. Until Wednesday names the merge seat:
   - the launcher refuses with rc 8 "RULING NEEDED";
   - the repin script refuses with rc 8 (a dry run reports it instead).

   With a ruled seat in a stand-in kit (`Seat R 10th`, used only as a test value), the whole path runs to rc 0: dry run 06:23:16Z, launcher `--check` rc 0, 10 pins EQUAL, 43 keywords. The routing line is NOT added; a real run refuses rc 1 until it is (`ROUTING_LINE.txt`).

2. **Pins.** Read 05:28:22Z by hand, then by the dry runs at 06:12:42Z, 06:18:42Z, 06:23Z and 06:24Z.
   - develop `147ae442074c` is unmoved, so it equals the base.
   - Each head equals its `refs/pull/<n>/head` and its branch.
   - Each head has ONE parent, `147ae442074c`, and its END_TREE matches the READY.

3. **Predicted stacked docs merge-in trees.** Order 1407 → 1409 → 1408 → 1410, at develop 147ae442074c. The merge seat takes `composed_2026-10-07/` VERBATIM.

   | step | PR | lands onto | merge-in | predicted tree | guard |
   |---|---|---|---|---|---|
   | 1 | #1407 | develop | NONE (== END_TREE) | `e1d3f4a6424bb21c8d55d2ac3c0a42bc1dc9b14e` | 12/0 |
   | 2 | #1409 | develop + #1407 | docs-only keep-both | `2a0a720361391a6cd736e7fb12264f0170d82967` | 12/0 |
   | 3 | #1408 | + #1409 | docs-only keep-both | `640d33ddd73e3f9eb3e568d21dfb50b668a397a1` | 12/0 |
   | 4 | #1410 | + #1408 | docs-only keep-both | `54c2c6ddb653a33513a81c4b063de340a8826dfe` | 12/0 |

   - **How the prediction was checked:**
     - Each step's read-back passes: the PR's own number or key appears once and LAST, develop's sequence is kept as the prefix, numbers are UNIQUE, and table/div balance is kept.
     - The final docs were also rebuilt in one pass from develop plus every block in order; both docs came out byte-equal to the chain's.
     - Every code path in the last tree equals its own head's blob.
   - **Final sequences:**
     - flow `… 27 28 29 25 30 31` (ascending order is NOT asserted, by design);
     - cheat `… KS-1136 KS-998 KS-1313 KS-1435 KS-591`.
   - **Re-predicting for another order:**
     - Run `c4_docs_gate73.py chain --order a,b,c,d --develop <develop> --heads …`.
     - All 24 orders are tabulated in `predictions/orders_all24_at_147ae442.json`: all rc 0, 24 distinct final trees.
     - Example, #1408 landing last (1407 → 1409 → 1410 → 1408): `e1d3f4a6424b` → `2a0a72036139` → `bdd92402d6abd0986d9fc44727d7ac19c8d724f7` → `dd09c036bbb674035c292e1b66917766f6a55458`.
   - **After a real landing:** run `--develop <new develop> --order <the rows still to land>`. Proved here: re-predicting from the post-#1407 SIM reproduced steps 2–4 exactly.

4. **Calibration (the gate71 converter/composer lineage).**
   - The composer applied to each row alone on the base reproduces that row's END_TREE byte for byte (4/4).
   - The base's two doc blobs, `df566caf8916` and `b938c3291299`, ARE gate71's predicted #1398 targets. In other words, the lineage's last prediction landed byte for byte.
   - No re-composition is needed this round: all four PRs were written on the same base, in the same matrix format.

5. **Main drafter finding: §5d (Q-5D).** None of the three product lines carries the WHY comment with a ticket number that SKILL §5d requires:
   - #1407 `check-package-format.sh:180`;
   - #1408 `transfer/src/index.ts:412`;
   - #1410 `originate.openapi.ts:1630`.

   Each whole file mentions its own ticket 0 times. The control: the sibling line in #1408's own file, `approveTransferSchema.reason` at :398, carries exactly the KS-518 comment that §5d asks for. Recommendation: a named Minor, not a blocker (RULINGS Q-5D).

6. **New hazard found while predicting (Q-UNION).**
   - `git merge-file --union`, and any hand resolution that accepts git's trimmed conflict hunk, drops the earlier lander's closing `</table>` in the CHEAT doc. At step 4 it also drops a `</div>`.
   - The repo's own `html_docs_matrix.test.sh` passes that broken doc at 12/0, because it does not check tag balance.
   - The kit's read-back and `qm` Q3/Q4 refuse it.
   - Recommendation: rule it as binding that the merge seat takes the composed docs VERBATIM.

7. **#1408 in-process drive (Wednesday's ruling) was run here, not just written.** `c2 drive1435` with base vs head and the same parser:
   - G1–G5: a wrong-typed signature (`{}`, `42`, `[]`, `true`, `null`) gets 200 and a rejected transfer at base, and 400 naming `signature` with the transfer still pending at head.
   - G6–G9: a string, absent, empty-string or unknown-key signature gets 200 and rejected at both.
   - G10: an already-invalid body stays 400.
   - Result 11/11 (`drafter_evidence_2026-10-07/c2_compare1435.out`).
   - The `null` case moving from 200 to 400 matches the spec (string, not nullable). Recommendation: accept it (Q-NULL).

8. **Actions, read twice (05:55Z and 06:00Z).** On all four heads every red is inside the three classes under the SUBSET predicate.
   - Class (1): Dependency Audit's only failed step is "Audit-contract suites (the gates' own validator)". Its log carries `expected exit 0 (clean), got 1`, and 12 of the last 12 Security Scanning runs repo-wide failed.
   - Class (2): the failing set is `{Code Security Gates}`, the same as develop's.
   - Class (3): `pr` fails a strict subset of develop's four at #1407 and #1408, where Schemathesis PASSES, and fails all four at #1409 and #1410.
   - 0 pending. A fabricated sha reads 0 runs.

## 1. The kit (this folder)

| File | What it is |
|---|---|
| `kit.json` | All pins. Four rows: head, branch, END_TREE, parents, numstat, modes, subject, flow number, cheat key, READY and ctx mail. Also the tooling paths, the pre-existing-mismatch blobs, the Actions classes, `predicted_chain`, `predicted_orders_final_trees`, `script_sha256` (10 files), and `merge_seat: null` (Q-SEAT). |
| `lib_gate73.py` | Read-verb `git()`. `wgit()` refuses write verbs under `!CODING`. `obj_at` uses ls-tree, never `rev-parse rev:path`. Readers: composee5's newline-tolerant h2 readers, extracted at pinned lines with the copy's sha256 asserted; the cheat reader is widened to `&mdash;` OR U+2014, because the base carries both. Also GitHub GETs (the job-log 302 is followed without auth) and `Tally`. NO default row: a script run without `--pr` refuses. |
| `c1_pin_gate73.py` | P1–P13 per row, with every PR value a required argument. Adds over gate71: P11 DISJOINT across the batch, and P13, the pre-existing MISMATCH files byte-identical base == head (Wednesday R3). |
| `c2_product_gate73.py` | `static` per row (S1–S6, including the §5d reader and #1408's class audit); `labels998` (the gate's own label instrument for #1407); `drive1435` and `compare1435` (#1408's in-process drive); `--selftest`. |
| `c3_suites_gate73.py` | Each row's own suites. Base and head are counted by ONE parser (JSON reporters for vitest and jest). Also: `arm` (swap a path to the base blob, or mutate it, with landed and restored both asserted), `compare` (failing SET as a subset), and `--system-tmp` (X9). |
| `c4_docs_gate73.py` | `docs` (D1–D6, plus tag balance), `calibrate`, `chain` (stacked keep-both prediction with the guard itself, merge-tree as a never-picked cross-check, and an independent `git merge-file --union` comparison), `orders` (all 24), `qm` (Q1–Q6), and `--selftest`. |
| `gh_gate73.py` | `api`, `prtext` (T1–T7), `actions` (the three classes, SUBSET), `census`, and `--selftest` on fixtures. |
| `composed_2026-10-07/` | The 8 composed docs (step × flow/cheat) plus `MANIFEST.txt` with sha256 and git blob per file. The merge seat uses them VERBATIM. |
| `predictions/` | The default chain, the re-prediction from the post-#1407 SIM, and all 24 orders. |
| `prompt_gate73.txt` | The gate prompt template. `prompt_gate73.rendered.txt` and `head_at_launch.txt` are the last real dry run's renders, with seat UNRULED. |
| `launch_qa_secuura_gate73.sh` | The launcher. It holds no PR literal; it reads P×4 / B / D / O / S from the head file and checks each against kit.json. |
| `repin_and_launch_gate73.sh` | The launch action. **Not run except `--dry-run`.** |
| `RULINGS_wednesday.md` | R1–R6 RULED (your commission), plus 11 OPEN questions with recommendations. |
| `ROUTING_LINE.txt` | `QA/Secuura-gate73\|coagent@agentmail.to\|yes` (NOT added to `inbox_routing.conf`). |
| `drafter_evidence_2026-10-07/` | Every final-pass output (`<tag>.out` + `<tag>.rc`), the launcher and repin arm tables, and the dry-run consoles. |

**Pins in `kit.json` `script_sha256`, re-verified after the last edit:**

| File | sha256 (first 16) |
|---|---|
| lib | 2e65b15ae1bd27c2 |
| composee5_copy | f9ab42d9fc25f189 |
| c1 | 9dc65bd1662875a5 |
| c2 | e3a5532b00e357e6 |
| c3 | 969855aa8c7bf98f |
| c4 | 88a0121fbcf3d531 |
| gh | 8fbe2b8385951d67 |
| prompt | 6f011a9f5f6fa0c0 |
| launcher | 1440f192b6eab8fb |
| repin | 8774e185cd70f39b |

All 10 compared EQUAL after the restore described in §5.

## 2. Every arm: expected vs actual

### Self-tests (final pass, pinned files)

| Test | Expected | Actual |
|---|---|---|
| c1 `--selftest` | 10/10 rc 0 | **10/10 rc 0** |
| c2 `--selftest` | 6/6 rc 0 | **6/6 rc 0** |
| c4 `--selftest` | 15/15 rc 0 | **15/15 rc 0** |
| c4 with the PLANTED wrong rule `G73_DOCS_DEMAND_ASCENDING=1` | must FAIL | **14/15 rc 1** (keep-both 29 then 25 refused) |
| gh `--selftest` | 14/14 rc 0 | **14/14 rc 0** |

The planted arms that FAIL inside those self-tests include:
- a wrong head; parents-n 2; a wrong END_TREE; an ancestor develop; another row sharing #1407's code; #1407's tooling change left undeclared;
- an edited pre-existing heading; a wrong-side insert; a double landing; a develop touching #1407 code;
- the guard's own positive control (planted prose → rc 1, 11/1);
- the pinned cheat reader blind to U+2014; an unkeyed h2;
- the UNION HAZARD itself (read-back refuses it, the guard passes it);
- equality vs subset; a red develop lacks; a workflow outside the classes; class (1) with SAST; class (1) with no needles; PENDING; no comparator;
- `Fixes KS-998`; a hyphenated foreign key; `(#1407)` in a title; #1408 with no sweep sentence;
- the §5d text-search trap (:403 vs :412); compare1435 fed no-change and 0-cell inputs.

### Real runs, drafter measured

**#1407:**

| Run | Result | Author's figure |
|---|---|---|
| c1 | 15/15 | |
| c2 static | S1 PASS (one line) | |
| S2 sibling | `grep -q "^systemTest/${p}/"` at :118 (residue) | |
| S3 §5d | **FAIL** | |
| labels998 | 9/9 | |
| L2 red-first (head suite × BASE script) | rc 1, 5/3; reds = the dotted and bracket label cells; 0 CONTROL cells red | 5/3 HOLDS |
| L3 ARM NOANCHOR | **8/0 — no cell pins `-x`** (Q-NOANCHOR) | |
| L4 matrix | head right on 19/19 shapes; base wrong on 5; anchoring probe catches NOANCHOR | |
| L5 sibling | 33/0 with both scripts | |
| L6 verdict and rc | identical base vs head | |
| c3 K1–K8 (head) | 8/0, 33/0, 28/0, 4/0, 12/0, list **71**, `bash -n` rc 0 ×2 | |
| c3 base | 33/0, 28/0, 4/0, 12/0, list **70** | |
| K9 (whole set) | NOT RUN (heavy, X1) | |
| docs | 11/11 | |
| D6 | cheat block has no section wrapper (polish) | |
| api | open, 1 commit, 4 files +203/-1, title == subject | body `1b6c85f1539e2902` == READY |
| prtext | 6/6 | |

**#1409:**

| Run | Result | Author's figure |
|---|---|---|
| c1 | 15/15 | |
| static | S1–S4 PASS; S5 names the hole | |
| V1 | head 10/0, base 3/0 | |
| arm T1 (`endedNormally` → `return true`) | **8/2, reds R1 + R2** | HOLDS |
| arm base file | 3/0 | |
| V3 / V4 / V5 | rc 0 at both | |
| V2 (whole perf unit suite) | 1334/26 head, 1327/26 base; **failing SET identical (26 == 26)**; +7 passed, 248 → 249 suites | 1353 → 1360 delta HOLDS |
| V2 absolute | not reproduced under a scratch TMPDIR (Q-X9) | |
| docs | 11/11; D6 no wrapper | |
| api / prtext | `ca6ed51ece8a9234` == READY | |

**#1408:**

| Run | Result | Author's figure |
|---|---|---|
| c1 | 15/15 | |
| static | S1–S3 PASS; S4 §5d **FAIL**; S6 class audit (all 3 transfer body schemas now declare every published property; at base `signature` was missing) | |
| T1 (the file) | head 55/0 | |
| T2 TRC1 by name | 1/0 | |
| T3 (whole transfer suite) | **79/0, 30 files** | |
| T4 tsc | rc 0 | |
| red-first arm (base index.ts) | **53/2, exactly TR1 + TR2** | the author's 77/2 of 79 is the whole suite: HOLDS |
| drive1435 base → head | 11/11 (§0.7) | |
| docs | 11/11 | |
| api / prtext | `35560d283f8f1f00` == READY; T6 sweep OWED | |

**#1410:**

| Run | Result | Author's figure |
|---|---|---|
| c1 | 15/15 | |
| static | S1–S4 PASS (contract-only: the handler `routes/documents.ts` is byte-identical and already refuses a non-uuid; 0 runtime parses of the registry schema vs 77 control parses); S5 §5d **FAIL** | |
| J1 | 3/0 | |
| J2 | **1077/0, 93 suites** | |
| J3 tsc | rc 0 | |
| J4a check:openapi, generate leg | rc 0 CHECK PASS | |
| J4b check:openapi, examples leg | rc 0 | |
| red-first arm (base product + yaml) | **2/1** | HOLDS |
| YAML-at-base control | J4a **rc 1** | HOLDS |
| docs | 11/11 | |
| api / prtext | `dc05407f32d87bc0` == READY | |

**Batch-wide:**

| Run | Result |
|---|---|
| census | 26 open PRs; **#1383 (KS-1401) touches BOTH docs** (Q-1383) |
| calibrate | 5/5 |
| chain, default order | ALL OK |
| chain, re-predict after #1407 | ALL OK, same trees |
| chain, #1408 last | ALL OK |
| orders | 24/24 rc 0 |

**qm arms** (on a SIM merge-in M for step 2):

| Arm | Result |
|---|---|
| good M | 8/8 rc 0 |
| parents reversed | Q1 FAIL |
| union-resolved cheat | Q2, Q3-cheat, Q4-cheat FAIL |

### Launcher arms: 23, all fire as intended (`drafter_evidence_2026-10-07/LAUNCHER_ARMS.txt`)

| Arm | rc |
|---|---|
| live, stand-in seat | 0 |
| live, real ls-remote | 0 |
| **real kit, seat null** | **8** |
| author seat | 8 |
| bad pin (c4) | 31 |
| missing gh | 30 |
| missing MANIFEST | 30 |
| head file: wrong head | 7 |
| head file: no order | 7 |
| head file: seat mismatch | 7 |
| head file: duplicate order | 7 |
| unrendered prompt | 8 |
| GO names an author | 8 |
| keyword missing | 33 |
| SUBSET predicate rewritten | 33 |
| hold removed | 39 |
| #1409 head moved | 6 |
| #1410 branch moved | 6 |
| develop moved | 17 |
| develop absent | 17 |
| #1407 head absent | 6 |
| moved kit | 2 |
| non-TTY launch | 21 |

### Repin arms: 14, all fire as intended (`REPIN_ARMS.txt`)

| Arm | rc | Note |
|---|---|---|
| short head | 9 | |
| missing develop | 9 | |
| duplicate order | 9 | |
| `--no-api` on a real launch | 9 | |
| wrong #1410 head | 11 | |
| wrong develop argument | 11 | |
| READY not naming the head | 18 | |
| #1408 head moved | 11 | |
| `G73_LSFILE` on a real launch | 16 | |
| develop moved, no repin | 10 | prints the re-predicted chain |
| stale repin | 10 | |
| develop moved and repinned | 13 | the launcher's own live read caught the stand-in |
| develop touching #1407 code | 13 | c1 P12 |
| develop absent after a by-sha fetch | 19 | |

### Dry runs (`drafter_evidence_2026-10-07/dry_runs/`)

| Run | Expected | Actual |
|---|---|---|
| `standin_seat_062316` | rc 0 | **rc 0** (V, A, ls-remote, API ×4, census, c1 ×4 15/15, chain == `predicted_chain`, render, routing reported, launcher `--check` rc 0) |
| `final_realkit_062413` | rc 13, from launcher rc 8 (seat unruled) | **rc 13 / rc 8** |

The final real-kit run is the last render left in the folder: seat UNRULED, so it is not launchable as it stands.

## 3. The authors' claims: HOLD / DO NOT HOLD (drafter's instruments)

**HOLD:**
- heads, END_TREEs and one parent;
- file counts and modes; new suites are 100644;
- trailers 1 raw byte vs a 55-raw-byte control (53 content bytes);
- 0 Co-Authored-By;
- only the own key is hyphenated;
- #1407: red-first 5/3 → 8/0, siblings 33/0, 28/0 and 4/0, discovery 70 → 71;
- #1409: arm T1 8/2, delta +7 tests and +1 suite;
- #1408: 2 red of 79 → 79/79, TRC1 by name, tsc rc 0;
- #1410: 1/2 → 3/3, 1074 → 1077 across 92 → 93 suites, check:openapi rc 1 → rc 0, the one-line YAML diff, every example resolving;
- matrix 12/0 on each head;
- body hashes ×4;
- the Actions classes;
- the pre-existing MISMATCH files byte-identical (`04f87f5e9095`, `cace85142710`, `af021aa7606e`).

**DO NOT HOLD (polish):**
- R 9th's "lands at 85 / 88": it is **86 / 89**, because ` (#NNNN)` is 8 characters.

**Corrections to figures some readers may have:**
- #1408's "79" is the whole 30-file transfer suite; `transfer.test.ts` alone is 52 → 55.
- Base `transfer.test.ts` reads 52, not 76.

## 4. NOT covered by the drafter (the gate owns these, or they are UNMEASURED)

- **The four platform suites** (Schemathesis, Akto, Playwright, Performance): UNMEASURED, because the stack is down. Never a pass.
- **#1408's live sweep** (owed under §5f) and its route behaviour behind the gateway. The drive is in-process only.
- **#1410 scored end to end by Schemathesis.** Not done.
- **#1407 against a real prettier on a real red package.** Fixtures only.
- **#1409 with a genuinely killed child.** Only the pure reader was driven.
- **K9, the whole 71-suite shell set** (needs X1, ~6 min). NOT RUN.
- **V2 absolute counts under a short TMPDIR** (X9). NOT RUN. Only the subset comparison ran.
- **Ticket states:** no Linear read.
- **The CI runner's toolchain.** The drafter measured node v24.7.0 (LTS 24), vitest 4.1.11 (transfer) and 5.0.3 (perf), jest (originate), and git's `merge-file`.
- **The browser render of the composed docs.** The guard is static, and blind to tag balance.

## 5. Drafter defects, caught and fixed

All are disclosed. The final pass re-ran on the pinned files.

1. **kit.json mode guess.** I wrote `check-package-format.sh` as 100755. It is 100644. c1 P9 caught it in the self-test GREEN arm, and the kit was corrected.
2. **L2 red-first predicate.** It wanted every red cell's text to carry the path. The second dotted cell's description does not, so it false-FAILED. Fixed to: exactly 3 reds, 1 dotted, 1 bracket, 0 CONTROL.
3. **Class (1) needle.** `Audit-contract suites` is a STEP name from the jobs API, not a log line, so the needle read 0 and class (1) "did not hold" on all four heads in the first read. Fixed: the failed step now comes from the jobs API, plus the log line `expected exit 0 (clean), got 1`, plus the `##[group]` control. Re-read at 06:00Z: holds ×4.
4. **The §5d reader located the changed line by TEXT search.** On #1408 that found approveTransferSchema's identical `signature: z.string().optional(),` at :403 instead of :412. The verdict happened to agree, but the instrument was wrong. It now uses the `-U0` hunk headers, and a self-test arm pins the trap.
5. **tsx IPC socket path.** A scratchpad TMPDIR makes the tsx CLI's socket path exceed 104 bytes. This broke `npm run check:openapi` (`listen EINVAL`) and 26 perf cells, identically at base and head. Fixed: check:openapi is split into `node --import tsx` legs (the same loader), V2 uses the subset compare, and X9 is offered by id.
6. **A zsh word-split slip during tidying (the one serious one).**
   - What happened: `set -- $P` does not split in zsh, so `mv $G/${S2}*` expanded to `mv $G/*`. That moved every kit file into `drafter_evidence_2026-10-07/dry_runs/final_realkit_/`. Nothing was deleted.
   - Restored by a python move of exactly the 19 kit entries back.
   - After the restore: all 10 pins compared EQUAL, the launcher `--check` read rc 8 on the real kit and rc 0 on the stand-in, and the kit clone still resolves.
   - The two emptied directories were moved to the scratchpad, not deleted.
7. **Bloat.** The repin's chain output (~9 MB of composed docs and guard trees per run) landed beside the kit files. It is now routed to the gitignored `_scratch/`, with `chain.json` and the MANIFEST copied out. Earlier runs' chain dirs were moved to the scratchpad.

## 6. OPEN QUESTIONS for Wednesday

Detail and recommendations are in `RULINGS_wednesday.md`.

- **Q-SEAT — BLOCKS LAUNCH.** *Rec:* one merge seat for all four, the next R seat, never an author.
- **Q-ORDER.** *Rec:* keep 1407 → 1409 → 1408 → 1410. The alternative of #1408 last is predicted.
- **Q-5D.** *Rec:* Minor, not a blocker, plus a tier-3 comment follow-up and a BRIEF_TEMPLATE line.
- **Q-UNION.** *Rec:* rule the composed docs VERBATIM plus `qm`, never a union. Ticket the guard's blindness to tag balance.
- **Q-NOANCHOR.** *Rec:* polish, as a follow-up cell.
- **Q-NULL.** *Rec:* accept; it matches the spec.
- **Q-1383.** *Rec:* don't hold #1383; re-predict if it lands first.
- **Q-X9.** *Rec:* accept, by id. The subset compare always runs.
- **Q-LANDS.** *Rec:* polish.
- **Q-WRAP.** *Rec:* polish.
- **Q-SWEEP.** *Rec:* KS-1435 stays In Progress until a live sweep.

## 7. Launch (Wednesday runs it; the drafter did NOT)

After ruling Q-SEAT (set `merge_seat` in kit.json) and adding `ROUTING_LINE.txt` to `inbox_routing.conf`:
```
script -q /dev/null bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-07_gate73/repin_and_launch_gate73.sh --order 1407,1409,1408,1410 --head-1407 3be1a5317735c11b377b89fa98e1ac5595f84ef0 --head-1409 c8899a95dc445fd3ac87ec3db33835f5acb1e155 --head-1408 ce33ec8b3eae5ea5ad63fc1b4871d8367fe2a95e --head-1410 c976c9f72ba019d76a2a575f2e4ff5c19c7af505 --develop 147ae442074c7f3b5be9ce7ccc4452c8dae34b4f
```
- If develop has moved, the script refuses with rc 10, prints the re-predicted chain, and gives the `--repin-develop <sha>` to pass.
- If the advance touched a row's code or tooling, it refuses with rc 13.

## 8. RUNG 5 (after launch)

- The pane is up under `QA/Secuura-gate73`.
- The prompt's first line is `ultrathink`.
- The gate writes `NOT-TESTED.written-first.md` first, then runs its self-tests.
