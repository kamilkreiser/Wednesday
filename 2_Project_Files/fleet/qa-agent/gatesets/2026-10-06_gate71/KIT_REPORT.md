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

## WIDENED 2026-10-07

**BLUF.**
- **Launch-ready: YES (dry run only, not launched).** Final dry run `ev_widen/dry_run_console_widen_ex3.txt` rc 0 at 2026-10-06T15:37:32Z: both heads at pull/head == branch, develop unmoved, c1 13/0 for both rows, c2 guard rc 0, c5 guard06 rc 0, c4 targets == kit pins, routing line present (1 exact line), launcher `--check` rc 0 with 12 pins EQUAL and 47 keywords. One condition: RULINGS W-Q1 (the skill accepted by name) — the kit implements the recommendation; reverse it and C1 refuses.
- **develop used: b39051390ff6f252601d6f7b45f0ea6c21c31023** (NOT the commissioned 40270d263ab0): #1405, `5_Project_History/history.md` +36 only. Instrument: one ls-remote 15:03:46Z, confirmed by Wednesday's message.
- **Target trees (key-anchored, re-composed, guard-green):** #1404 onto b3905139 -> **d717255d5376c7c8cf22e57c0bc88b7437b2553d**; #1398 onto (b3905139 + #1404, SIM 391bdbffa023), flow 23. -> 28. per Wednesday's ruling -> **960e71800ea1e9bce95c681d8547293147c6010b**. Guard on each: `html_docs_matrix.test.sh` 12 passed, 0 failed, rc 0. Instrument: `c4_docs_gate71.py targets` (`ev_widen/c4_targets_devb390_ex1.out`).
- **DIVERGENCE:** git merge-tree conflicts on BOTH docs for BOTH PRs (rc 1; outside the docs 0 paths differ). Printed, never picked; RULINGS W-Q6. A second, larger divergence was ruled mid-widening: develop holds `23.` itself, so #1398 is renumbered 28 (RULINGS, quoted).
- Q2's merge condition is MET in the drafter's fixtures: with both PRs, a designed fallback run of job 06 reads CLEAN; with #1398 alone it reads `06-tenant/unreadable-artefact` HIGH (the false alarm).

### W1. Pins (instrument: ls-remote 15:03:46Z, then `git -C <kit clone>` reads)
| | #1404 (T2, merges FIRST) | #1398 (T1, round 1 of 2) |
|---|---|---|
| head | c117c0160684d1ae72b220a8d2ccfe9aafb8eb8d = pull/head = branch | 9414aa54e92ca243565d0d967aad991dc4c13840 = pull/head = branch (unchanged) |
| tree | ec95d19958803c4f6f00b5ce097949e3dc18bc3a | 2ee602cba3c9 |
| parent | ONE, d75bfe2deb80 (c1 P2) | ONE, d75bfe2deb80 |
| numstat | 4 paths +177 -1: suite +98 (A 100644), 06 +4/-1 (100755 -> 100755), flow +46, cheat +29 (c1 P3, P9) | +349 -0 |
| pre-docs tree | 5d1ca2fe9ece78a9 (drafter-measured; no author claim) | 074705eebd81 == author |
| subject | 66 chars, LANDS 74 with ` (#1404)` (c1 P7) | 83, LANDS 91 |
| trailers | 0 content bytes; control bf277eead268 53 bytes (c1 P5) | same |
| keys | only KS-1436 hyphenated; KS 1136, KS 1382 de-hyphenated; one `Refs KS-1436`; 0 closing (c1 P8) | only KS-1136 |
| GO | `GO (Seat R 5th): merge 1404 on gate71` | `GO (Seat R 5th): merge 1398 on gate71` |

develop move d75bfe2 -> b3905139: 190 paths (189 at 40270d26: the author's figure HOLDS). 0 shared with either row's code paths; the one tooling path moved is the skill (accepted by name, W-Q1); both docs moved (c1 P12/P12a/P12d).

### W2. Every arm and its rc
**Self-tests (`ev_widen/*selftest*`), all rc 0:** c1 13/13 (x2 rows), c2 11/11, c3 7/7 (x2), c4 19/19 (x2), c5 14/14, gh 17/17 (x2), recompose 7/7. New planted arms include: an unaccepted skill blob, a head that edits the accepted path, a tooling path not in the list; a runner `2>&1` vs the harmless `command -v node 2>&1`; a non-unique tamper anchor; a planted `pull_request` trigger; leak + unreadable together (OTHER); a duplicate flow number; a de-hyphenated key in the own h2; two `</body>`; the pinned cheat reader BLIND on develop (0 keys) vs the widened one (11); a planted live job-06 log line.
**The ascending arm:** `G71_DOCS_DEMAND_ASCENDING=1 c4 --selftest` -> rc 1, 18/19, the one FAIL is "THE RULE accepts the BY-DESIGN order `… 22. 27. 23.`" (`ev_widen/c4_selftest_ARM_demand_ascending_ex1.out`).
**Calibration:** `recompose_gate71.py --calibrate`: base KS-1305 old blocks -> develop's #1402 blocks BYTE FOR BYTE, flow 7236 B and cheat 3851 B, rc 0. Across all old blocks: 4 of 32 byte-identical, visible text equal for 25 of 32 (#1402 hand-edited the rest).

**Real runs at (c117c0160684, 9414aa54e92c, b39051390ff6):**
| Run | Result |
|---|---|
| c1 #1404 / #1398 vs develop | 13/0, 13/0 |
| c5 guard06 (ex2) | 6/0: ONE replacement at :71; WHY comment carries KS-1436; runner `2>&1` head 0, base 1; header + swallow lines kept; 100755; G6 5 run-dir glob/upload lines (internal-audit.yml uploads audit-runs/latest/) |
| c5 suite06 | S1 5/0 rc 0 (2.62 s); RED-FIRST base blob 4d077ab3 rc 1, 1/4, cells 2-5 red, CONTROL cell 1 green; DEVNULL 4/1 cell 4; WRONGNAME 4/1 cell 4; re-run 5/0. Author's 1/4 -> 5/0 and 4/1 HOLD |
| c5 chain (ex2) | 36/36. BOTH: fallback-clean CLEAN, both-logins-fail CLEAN, fallback-leak and quiet-leak LEAK (critical, rc 1), truncated and crash UNREADABLE. #1398 alone: fallback-clean and both-logins-fail UNREADABLE (the false alarm), fallback-leak UNREADABLE with the leak id NOT emitted. #1404 alone: fallback-leak LEAK where BEFORE read CLEAN; truncated still CLEAN. Sidecar holds exactly the stderr; 09 ids equal with it removed. Summary `tested=3 cross-tenant_findings=0` (head) vs `tested=? …` (base). CONTROL: 3 BEFORE violations |
| c5 chain --stack-tree 960e7180 | 37/37 (the stacked tree's 06 and 09 == the heads') |
| c2 shapes --on-tree 960e7180 | 90/90, CONTROL 51 base violations, REPEAT unchanged (run 2 rc 0, NEW [], high 1) |
| c5 reach06 at develop and both heads | 17 workflows; 2 reach job 06 (api-contract-tests via ci/orchestrate.sh, internal-audit via run-internal-audit.sh), both workflow_dispatch only; 0 per-PR; fabricated token 0 |
| c4 docs #1404 / #1398 | 11/0 each; #1404 flow ..22 27, cheat ..KS-1305 KS-1436; D6 INFO: #1404 cheat block NOT section-wrapped (W-Q4) |
| c4 targets | T1, T2, T2x (as-authored 23 REFUSES on UNIQUE), T-CTL (old format FAILS the guard 10/2, 7 `prose outside a table`) |
| c3 list | 67 -> 68 for each row, the difference is exactly that row's suite, `--check-unreached` OK |
| stacked worktree (SIM 8f4f0d7b on tree 960e7180, scratch clone) | runner `--list` 70 (develop 68 + 2); `--check-unreached` OK on 70; html_docs_matrix 12/0, tenant_isolation_stderr_own_file 5/0, ks1136 6/0, aggregate_report_trivy_artefact 5/0, orchestrate_jobs 18/0 |

**Launcher arms (`ev_widen/LAUNCHER_ARMS_WIDEN.txt`), all FIRE:** rendered live 0; badpin (c5) 31; nopin (recompose) 30; missing c5 30; unrendered 8; **GO naming R 4th in a merge string 8**; **a bare `GO (Seat R 4th)` 8** (the R 4th refusal message); GO naming R 3rd 8; only one GO 8; head file with one P 7; no D 7; **#1404 head moved 6**; #1398 head moved 6; #1404 branch moved 6; develop moved 17; absent #1404 head 19; absent develop 19; keyword missing 33; **the doc rule rewritten to demand ascent 33**; moved kit 2; non-TTY launch 21.
**Repin arms, all FIRE:** short head 9; missing row 9; `--no-api` real launch 9; head not in the READY 18; **#1404 head moved 11**; #1398 head moved 11; develop not a descendant 13 (P2b); develop touching job 06 13 (P12); **develop with a different skill blob 13 (P10 NOT ACCEPTED)**; develop moved without repin 10 (prints the chain); stale repin 10; develop absent after a by-sha fetch 19; develop moved and repinned 13 (the launcher's own live read caught the stand-in).
**Docs arms:** C01 ascending-demanding rule rc 1; **C02 #1398 keeping `23.` fails UNIQUE rc 1**; C03 #1398 at 28 predicts 960e7180 rc 0.

**Every zero has a control:** runner `2>&1` 0 at head vs 1 at base; per-PR reach 0 vs 2 workflows that reach 06; fabricated token 0; merge-tree outside-docs 0 vs both docs conflicted; pinned cheat reader 0 vs widened 11; R 3rd/R 4th GO strings in the prompt 0 vs R 5th 1+.

### W3. The skill (instrument: `git diff d75bfe2 b3905139 -- .claude/skills/secuura-test-discipline/SKILL.md`)
The only change is `### 6e. Runtime versions — LTS only` (+17/-0). The MUSTs that touch this gate, quoted from b3905139:
- §4: "**Every test change updates its platform's two HTML docs, in the same commit — not a follow-up.**" and "**Both files, every time.**" (unchanged)
- §4: "**MANDATORY — the HTML docs carry the TIMINGS, and stale timings are a defect.** … **must also appear in both HTML docs, and must agree**." (unchanged)
- §5b: "**Every fix is proven by a test that was red on the broken code and green after.**" (unchanged)
- §5d: "**Every changed line carries a comment saying WHY it changed and the Linear ticket number** … stating the prior behaviour" (unchanged; #1404's comment carries both, guard06 G2)
- §5f: "**A runtime-behaviour change is not done — and the ticket does not move to Done — on offline quality-gate green alone.** It needs a live sweep on the correct host" and "**say so explicitly and name what is unverified.**" (unchanged)
- §6e (NEW): "**Always run, build and test on Long-Term-Support versions** … Node: an even-numbered LTS line (24 today)" and "**It changes no test and no result.** Quote every measurement as taken on LTS versions; if one was not, say so in the Test Evidence block". The drafter ran node v24.7.0 (LTS line 24), bash 3.2.57, jq-1.7.1-apple.

### W4. Findings for the gate (drafter's, all PREDICTIONS)
- **N-1404-a (polish):** the cheat block has no `<div class="section">` wrapper (c4 D6; W-Q4).
- **N-1404-b (polish):** the doc block and the commit message cite base line numbers (:71, :74-:75); at the head they are :74 and :77-:78 (W-Q5).
- **N-1404-c (INFO):** the new sidecar `06-tenant-isolation.json.stderr` lands in the run dir that internal-audit.yml uploads on failure; it holds runner diagnostics (login failure lines with the email and status). Name it; not a blocker.
- **N-both (merge):** each docs merge-in is a re-composition onto the matrix format; merge-tree cannot be used (W-Q6). #1398's merge-in must be predicted on the REAL post-#1404 develop (W-Q8).
- Extra observation from a superseded run (`ev_widen/c5_chain_ex1_SUPERSEDED_stub-order.out`): if stderr is written AFTER the JSON, base 09 reads the leak through jq's first value, and #1398's 09 emits leak + unreadable together. The real runner writes stderr first (runner.ts :74 before :262).

### W5. My own defects caught while widening (each fixed and re-run)
1. c5 G3 counted `command -v node >/dev/null 2>&1` as the runner's `2>&1` (ex1 FAIL); narrowed to the runner invocation (ex2).
2. The c5 tsx stub wrote stdout before stderr for every shape (chain ex1: 3 FAILs); now stderr first for the login shapes, as runner.ts does (ex2 36/36).
3. A first `python3 -I` run wrote `__pycache__` into the kit (`-I` ignores PYTHONDONTWRITEBYTECODE); moved to `_superseded_2026-10-07/pycache_from_drafter_python_-I_run`.
4. One dry run under `script -q /dev/null` failed in `tcgetattr` (`ev_widen/dry_run_console_widen_ex2_SCRIPT-FAILED-tcgetattr.txt`); re-run without `script` (dry runs need no TTY) rc 0. The real launch still runs under `script`.
5. The kit's pinned cheat reader was blind on develop (U+2014 for `&mdash;`), and the old close-tag match `  </body>` failed there (develop writes `</body>`). Both widened in lib, with controls.

### W6. NOT tested, and why
- Everything on GitHub (API, bodies, mergeable_state `dirty`, Actions at either head, job logs, `gh job06`, census): no GitHub identity. Self-tested only.
- The whole 68-suite set at each head, and the 70-suite set on the stack: needs X1 (npm ci) and ~6 min each; the gate runs it. Run on the stack: 5 suites (W2).
- c2 `suite` and `callers` for #1398: not re-run (head and 09 unchanged; evidence in `_superseded_2026-10-07/outputs/`).
- A real runner.ts, a live stack, a real mid-write abort: fixtures with stubs only.
- The browser render of the re-composed docs (the guard is static by its own header).
- Ticket states (KS-1436 attachments 0 at PR open, reported by the author as may-lag): not read.

### W7. Files
- New: `c5_job06_gate71.py`, `recompose_gate71.py`, `recomposed_2026-10-07/` (4 blocks + MANIFEST), `ev_widen/`. Rewritten: `c4_docs_gate71.py`, `launch_qa_secuura_gate71.sh`, `repin_and_launch_gate71.sh`, `prompt_gate71.txt`, `kit.json` (rows, targets, pins x12). Edited: lib, c1, c2, c3, gh.
- Superseded (moved, nothing deleted): `_superseded_2026-10-07/outputs/` (211 pre-widen outputs), `kit_pre_widen/` (the 15 files as pinned before).
- Scratch: SIM commits 391bdbffa023 (develop + #1404) and the arm SIMs are objects in `_scratch/clone`; worktrees and SIM 8f4f0d7b live in the drafter's session scratchpad. No write verb ran in the shared checkout.

### W8. Launch command (Wednesday runs it; NOT run by the drafter)
```
script -q /dev/null bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-06_gate71/repin_and_launch_gate71.sh 1404:c117c0160684d1ae72b220a8d2ccfe9aafb8eb8d 1398:9414aa54e92ca243565d0d967aad991dc4c13840
```
