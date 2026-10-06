# gate71 KIT REPORT — drafter to Wednesday

- **Target:** #1398 (KS-1136), head `9414aa54e92ca243565d0d967aad991dc4c13840`, base / develop `d75bfe2deb8075583cfb55af0921e4964e7c6f0e`, END_TREE `2ee602cba3c9`.
- **Drafted:** 2026-10-06 12:37Z-13:05Z UTC by one drafting subagent.
- **Built, not launched.** Nothing was merged, pushed, commented on or mailed.
- **GitHub identity: none held.** PR facts come from `git ls-remote` and R 3rd's four mails only.
- **Writes:** only `gatesets/2026-10-06_gate71/` and the drafter's scratch dir. One exception is disclosed in §5.

## 1. What I built

A single-PR T1 kit with the gate70 shape. gate69's doc merge-in machinery is put back, because this PR edits both platform docs.

- **`repin_and_launch_gate71.sh`** is the launch action.
  - It re-reads the READY, then ls-remote (develop, `refs/pull/1398/head`, the branch), then the API (dry-run may pass `--no-api`).
  - It fetches by sha into the kit clone only if an object is absent, and **refuses by name (rc 19)** if any object is still absent.
  - It runs C1, the guard read, and the docs merge-in prediction plus merge-tree on the develop it read.
  - Then it renders the prompt, checks routing, runs the usage gate and the launcher's `--check`, and does the cockpit add.
  - `--dry-run` stops before the usage gate.
- **`launch_qa_secuura_gate71.sh`** checks 10 pins, the head file (P + D lines), the prompt's rules and keywords, and the GO. It then does its own live ls-remote:
  - a moved head refuses rc 6;
  - develop != the rendered develop refuses rc 17;
  - an absent head or develop refuses BY NAME, rc 19.
- **`c1_pin_gate71.py`** checks:
  - P1-P12: pin, parent, numstat, END_TREE, trailers, Co-Authored-By, subject (it LANDS 91), keys, modes, NO-NEW-LEG over 22 tooling paths, forbidden-class paths, base..develop;
  - plus P4b, which rebuilds the author's pre-docs tree from base + the 2 code blobs.
- **`c2_product_gate71.py`** has four modes:
  - `guard`: the pure insertion, the placement, the loop == the file's own blocks minus 04 with matching emit ids, two conjuncts, 04 untouched.
  - `suite`: red-first through the suite's own `AGG_SH` hook, run on the base blob, so the worktree is never touched. Then one mutated copy per conjunct (A, B), plus arm C (08 removed from the loop) and arm D (the loop moved below ALL_FINDINGS), the suite's `AGG_SH=''` refusal, and a determinism re-run.
  - `shapes`: the legitimate-shapes matrix, base vs head, real `bash jobs/09-aggregate-report.sh` in fresh fixtures.
  - `callers`: every consumer by path, classified on an invocation (never on a comment or a grep). Baselines are checked for a masking fingerprint, and the trivy-suite blindness arm is run.
- **`c3_suites_gate71.py`**:
  - `list` measures 67 -> 68, the difference, and `--check-unreached`.
  - `full` runs the whole set, classifies each red, and re-runs every red ALONE at the base as the control.
  - `classify` attributes per-suite summaries to `=== path ===` headers. It works on a local or a CI log, and checks the failing SET against the KS-168 six, not just the count.
- **`c4_docs_gate71.py`**:
  - `docs` covers: boundary-free with an altered-fragment control, the line block, order, the split-h2 control, keys, h2/div balance.
  - `predict`, `mergetree` and `qm` cover the merge-in (TAIL, key-anchored), on a SIM develop in the self-test.
- **`gh_gate71.py`** (self-tested only):
  - `api`;
  - `prtext`, including T7: the stale "unmeasured" sentence;
  - `actions`: every failing job's log, the `##[group]` positive control, a fabricated-needle control, own-path tokens, the known-class needle at the head AND at a develop-side head;
  - `census`.
- **Docs and rulings:** README.md, RULINGS_wednesday.md (P1-P7 pre-ruled, Q1-Q8 open), LAUNCHER_ARMS.txt, MERGE_IN_PREDICTION.txt, ROUTING_LINE.txt.

## 2. Every arm and its result

**Self-tests:** c1 9/9, c2 11/11, c3 7/7, c4 11/11, gh 15/15, all rc 0. Each includes planted arms that must FAIL:
- an extra path;
- a `(#1398)`-suffixed subject;
- `Closes` / `Fixes` + a trailer;
- a non-unique tamper anchor, which refuses;
- a head silent on an unreadable shape;
- a head flagging a clean shape;
- a doubled finding;
- a seventh red;
- a count-equal set-different red;
- an unread log (0 `##[group]`);
- a needle present at the head only;
- the wrong doc order;
- an edited pre-existing heading;
- a develop touching 09.

**Real runs at (9414aa54e92c, d75bfe2deb80):**

| Run | Result | Author's claim |
|---|---|---|
| C1 | 14/14 | |
| guard | 6/6, span :216-:229 | |
| suite | S1 6/0 rc 0 (1.36-1.60 s) | 6/0, 1.332 s |
| red-first | rc 1, cells 1-3 red, 4-6 green | 3 red, controls green |
| arm A | 2/4 | 2/4 |
| arm B | 4/2 | 4/2 |
| arm C | 4/2, cells 2-3 | (extra arm) |
| arm D | cells 1-3 red | (extra arm) |
| `AGG_SH=''` | rc 2 | |
| shapes | 90/90; the control shows 51 base violations | |
| callers | 4/4 | |
| list | 67 -> 68, `--check-unreached` OK | 67 -> 68 |
| docs | 11/11 | |
| predict | == END_TREE | |
| merge-tree | AGREE | |
| `bash -n` on both changed shell files | rc 0 (control: a broken file, rc 2) | rc 0 |

**Moved-develop exercise (SIM 4f7cb2adeb47, objects only):**
- c1 13/0, with P12d naming the docs merge-in;
- the predicted tree d67e85459d10, flow ...22 24 23;
- merge-tree DIVERGENCE on both docs (expected; the TAIL tree is the target);
- c1 with an ancestor develop (f556373b9418): P2b FAIL, rc 1.

**Launcher: 17 arms, all firing.**

| Arm | rc |
|---|---|
| rendered, live | 0 |
| badpin | 31 |
| nopin | 30 |
| missingfile | 30 |
| tamperedfile | 31 |
| unrendered | 8 |
| forbiddenGO | 8 |
| headfileMalformed | 7 |
| headfileNoD | 7 |
| lsReal | 0 |
| **headMoved** | **6** |
| branchMoved | 6 |
| devMoved | 17 |
| **absentHead** | **19** |
| **absentDevelop** | **19** |
| movedKit | 2 |
| launchNonTTY | 21 |

**Repin: 9 arms, all firing.**

| Arm | rc | Note |
|---|---|---|
| headMoved | 11 | |
| wrongHead | 11 | |
| shortHead | 9 | |
| noApiRealLaunch | 9 | |
| devNotDescendant | 13 | |
| **devAbsent** | **19** | the fetch by sha failed, so it is refused by name |
| devMovedNoRepin | 10 | prints the prediction |
| devMovedStaleRepin | 10 | |
| devMovedRepinned | 13 | the launcher's own live read caught the stand-in |

**Dry runs:**
- ex1 (13:00:02Z) rc 0;
- ex2 (13:02:27Z, the final one, re-rendered at the real pins) rc 0;
- 10 pins EQUAL, 36 keywords.

**Every zero has a control:**
- trailers 1 raw byte vs control 55;
- fabricated consumer token: 0 files, vs 09 naming itself;
- 0 `unreadable-artefact` baselines vs 69 fingerprints;
- docs: 1-byte-altered fragment FALSE vs the real one TRUE;
- KS-9999 planted and found;
- base..develop 0 paths vs the SIM's 2.

## 3. The author's claims: HOLD / DO NOT HOLD (drafter's instruments)

**HOLD:**
- head == pull/head == branch at origin;
- END_TREE 2ee602cba3c9, one parent == develop;
- 4 files with the stated numstat and modes (the test 100644 A; 09 100755 -> 100755);
- the pre-docs tree 074705eebd81;
- subject 83 chars, ASCII, no closing verb;
- 0 trailers: 1 raw byte, against the control at 55 raw bytes (the 53 content bytes + 2 newlines; the author's 55 is the raw count);
- 0 Co-Authored-By;
- Refs not Closes; only KS-1136 hyphenated in the message;
- suite 6/0;
- red-first: 3 red (cells 1-3), controls green;
- arms A 2/4 and B 4/2;
- `--list` 67 -> 68;
- `bash -n` rc 0;
- boundary-free docs (both TRUE, once each, altered-control FALSE);
- flow 1-16 18-23 with `17.` a gap; cheat tail KS-1136;
- only KS-1136 hyphenated inside each block, with KS 878 de-hyphenated;
- the newline-tolerant reader's split-h2 control;
- "88 distinct keys" holds for the FLOW doc (88). The cheat reads 99, and the sentence does not say which doc.

**DO NOT HOLD (polish, README §2):**
- "LANDS 90": it is 91.
- Arm A "breaks … both well-formed controls": the measured red cells are 1, 2, 5, 6, and the all-well-formed cell 4 stays green.

## 4. Claims I could NOT verify, and why

- **Everything on GitHub:**
  - PR #1398 open / unmerged / on develop;
  - HTTP 201 / PATCH 200;
  - the body sha256/16 `aba1d9423478a0b6` and its text;
  - 1 commit / 4 files / +349 -0 by the API;
  - the 7 Actions runs and their conclusions;
  - every log line and `##[group]` count (19 / 24 / 21 / 30 / 31);
  - the six-suite failing set on the runner;
  - `ks1136_…: 6 passed, 0 failed` on the runner;
  - the nine develop-side logs;
  - "none of my paths in any log".

  Why: I hold no GitHub identity, and the brief forbids using one. The kit's `gh_gate71.py` reads all of these at launch (X6).
- **The whole shell-suite set, 68/68 in 342 s.** NOT RUN. Why:
  - The runner re-points a TMPDIR longer than 80 chars to `/tmp/rss.*`. My scratch path is about 100 chars, so a run would write outside my allowed area.
  - Getting 68/68 needs `npm ci` plus a `packages/shared` build in a worktree.
  - The gate runs it (CHECK 5, X1), with a base re-run control for each red.
- **The sibling timings** (trivy 0.842 s, orchestrate 3.965 s). The trivy suite ran (5/0 at head and base), but its time was not printed. orchestrate_jobs was not run.
- **The KS-1136 ticket state:** In Progress, attachments 1 -> 2, assignee and comments unchanged. No Linear read (RULINGS Q8).
- **"Item 1 merged as #1051".** Not looked up.
- **The push:**
  - `.rc` 0;
  - 6m32s;
  - PREFLIGHT 12/15 with legs 3 / 4 / 8 skipped;
  - legs 6 and 7 OK;
  - format gate 4/0/0;
  - 13 code guards.

  Why: these are the author's logs, in its worktree, which I must not touch. The gate does not depend on them.
- **The KS-991 range figures** (132 paths, 4 systemTest packages): same reason.
- **gatelinesra1 `--want`, the lock census, twolockra1 163/27:** the author's tools, out of this kit's scope.
- **pathgatera1 VERDICT PASS with its firing control.** Not re-run (the author's tool). C1 P3 / P9 / P11 independently prove the exact 4-path set, modes and no forbidden class.
- **§4 timings census** (0 stated; Akto 4 / pre-merge 7 / Schemathesis 2). Not re-measured.
- **The CI runner's jq version.** The guard's semantics rest on `jq -e` exit codes, which I measured on jq-1.7.1-apple only: empty 4, null / false 1, truncated 5. The runner's jq is unread.

## 5. My own defects caught while drafting (disclosed, each fixed and re-proved)

1. **`rev-parse <rev>:<absent path>` echoes the argument.** My c4 "did develop move a code path" check compared two such echoes for the NEW suite (absent at base and at the SIM), and refused a valid develop. This is exactly STANDING_LINES 2026-09-27. Fixed with `blob_at` (ls-tree) in lib, used by c1 P10 and c4. Re-proved by c4's self-test: the SIM predicts, and a develop touching 09 refuses.
2. **c2's emit-id regex was lowercase-only.** A planted wrong id `02-WRONG` read as "no emit" instead of a mismatch, and my own self-test arm caught it. Widened.
3. **The callers classifier first counted a COMMENT and a `grep` of run-internal-audit.sh as calls** (orchestrate.sh, orchestrate_jobs.test.sh). Now an invocation only.
4. **A stray `-o true` fragment in one launcher guard line.** Removed before pinning. Every launcher arm ran on the fixed, pinned file.
5. **Write boundary.** My first exploratory suite runs (before c2 pinned `TMPDIR` under `--out`) let the suite's own `mktemp` land in the system TMPDIR (`/var/folders/…/T/`). The suite's EXIT trap removed it. Every pinned-version run writes under `--out`: the final `ev_c2suite/tmp` holds 0 entries.

   One more scope note: the kit clone `gatesets/2026-10-06_gate71/_scratch/clone` holds the SIM objects (4f7cb2adeb47 and its child) for the arms. The shared checkout's `rev-parse --all` and `.git/config` were cmp-identical before and after.

## 6. Questions Wednesday must rule (detail and evidence in RULINGS_wednesday.md)

- **Q1** REPEAT shape: an unreadable artefact that persists across two runs exits 0 on run 2 (NEW empty, totals.high 1). *Rec:* not a blocker (inherited R-1 semantics, the same as KS-878's 04 guard); residue after a board search.
- **Q2** Job 06 merges stderr into its artefact. A legitimate login-fallback run now reads HIGH "aborted mid-write". Before, it read CLEAN even with a real leak inside. *Rec:* does not block (a true alarm; a false cause text is polish); 06:71 `2>&1` is residue. Expect live-sweep reds.
- **Q3** The sibling `ci/aggregate.ts:241-243` has the same silence, untouched here. *Rec:* residue, not a blocker.
- **Q4** Squash body: the commit message still says the runner result "is unmeasured". *Rec:* R 4th writes the squash body from the PR body as the gate reads it, with 0 trailers, `Refs KS-1136` and keys de-hyphenated.
- **Q5** "LANDS 90" is really 91. *Rec:* polish, named.
- **Q6** Sequencing against R 4th's PRs 3-5 (flow 24-26, both docs). *Rec:* merge #1398 first. Otherwise a docs merge-in plus `c4 qm` is required (the kit predicts it).
- **Q7** The routing line is not added. *Rec:* Wednesday adds it at launch.
- **Q8** No Linear read in this kit. *Rec:* leave it out (Refs-only PR; the §5f comment is the merge seat's).
