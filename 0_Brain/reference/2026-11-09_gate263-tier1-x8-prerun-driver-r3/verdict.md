GO WITH NOTES
Covers pushlock_x8_newbranch_v3.sh sha256 cc29e44bd3823b22ef98a0d593feb2a734be784dfa39fe3e978735e435df64d6 and the other 13 first-use files in driver_built_x8.md (14 of 14 matched at 14:06:34Z and at 14:26:02Z, evidence/sha_start.txt, sha_end.txt; control: one appended byte is seen). A change to any first-use file voids this. Gate 263, tier 1, round 3 (the one narrow third round), 2026-11-09.

## BLUF

**The blocker is closed, and so is every Major, by my own runs and not only by X 8th's.** Gate 237's N1 (a failing `git status` read as clean, carrying a RED commit to `--no-verify`) reproduces on X 7th's shipped files at every read I drove: the pre-run's start read, its 60 s read, its end read, and the driver plus decide together. On X 8th's files each of the same arms ends with no `--no-verify`. X 8th says there are two independent guards. I checked that with my own tampers: blinding the driver alone sends the push to the hook, blinding decide alone makes the driver refuse, and blinding both reaches `--no-verify`. So the arm can fail, and each guard holds on its own.

**No change in the four round-3 diffs lets an instrument error reach `--no-verify`.** That covers a crash, a hang, an empty or unreadable file, and a failing git call (Q3). Every RECORDED call in X 8th's sweep is fail-safe as far as `--no-verify` goes (Q4). One of them, the copy of the hook's changed set, is fail-safe only in a weaker sense, explained below. It is not a blocker.

**The notes do not stop the next step. They change what seats and Wednesday should be told:**
- **G1, out of the tool's scope but the most important thing I found:** the REAL hook at 35bcfa000 skips the preflight entirely when `git diff` fails. It pushes a RED commit with rc 0 (measured). On the same fault the pre-run path still runs the preflight. So this mechanism is stronger than the hook here, not weaker.
- **G3:** the pre-run's "clean tree" means clean as far as `git status` reports. A valid setting (`status.showUntrackedFiles=no`) or an ignored file can feed the preflight unseen, on both paths.
- **G5:** the side-by-side harness is ready, but its output needs reading against a short list of rows (Q6).

Under Kam's card the next steps are the side-by-side run on one real commit, then one real new-branch push, then STANDING_LINES:96.

## Findings

All evidence paths are relative to this folder. MEASURED AT RUNTIME means driven in my scratch worlds (local bare origins, scratch lock and queue). READ ONLY means established from source and not executed. I changed nothing in any tool.

**G1. Note, outside this tool, and Wednesday's to route: the real hook skips the preflight when `git diff` fails.**
- Where: `.githooks/pre-push` at 35bcfa000, lines 129, 143 and 252 (`diff ... || true`).
- MEASURED AT RUNTIME. Evidence: evidence/order.out, script evidence/g263_order.py.
- FOUND: `git config diff.orderFile <missing file>` makes `git diff` exit 128 with empty output, while `status`, `rev-parse` and `merge-base` still exit 0. My probe of 17 `diff.*`/`core.*` faults found this one shape.
- TESTED: the real hook fixture, called directly with a new-branch stdin line on a RED commit:
  - with the fault: rc 0, no preflight ran ("Blockchain/Dev changes detected" is never printed);
  - without the fault: rc 1, the preflight ran and failed.
- The pre-run runs the preflight unconditionally, so on this fault it is the stronger path.
- ACTION: the hook's owner should know. This is a fact about today's push path, not about this tool. It does not affect this verdict.

**G2. Minor, Q4: one RECORDED call, `hook_changed_set_COPY`'s diffs, is not fail-safe in the strict sense.**
- Where: `prerun_x8.py:221, 238`.
- MEASURED AT RUNTIME, evidence/order.out and x8_tampers.out (arm ORDER).
- What the fault does:
  - Under the same fault the copy returns an empty changed set (`('', 0, 1)`), and the format gate is fed nothing.
  - The driver does not stop on the fault while develop has not moved: `develop_gate.sh:31` exits 0 before its diffs.
  - So a qualifying record reached `--no-verify` with the fault live (ORDER).
- Why it is not a blocker:
  - The hook does exactly the same (`|| true`), and on that fault the hook also skips the preflight (G1).
  - The pre-run's preflight still runs.
  - Today the format gate prints `[format-gate] SKIP (advisory) — no systemTest package declares a format:check script` whatever the changed set is.
- It becomes live only if a systemTest package declares `format:check`. That change moves neither pin, so nothing would alert anyone.
- ACTION: on the day a package gains `format:check`, the changed-set copy should treat a failing diff as "cannot say", the way the N1 fix treats status. READ ONLY for that recommendation.

**G3. Note, and a use-note item: "clean" means clean to `git status`, on both paths.**
- MEASURED AT RUNTIME, arm UNTRACKED in evidence/x8_n1.out and x7_n1.out.
- FOUND: `status.showUntrackedFiles=no` (a valid value, rc 0) plus an untracked file the preflight reads. A RED commit went `--no-verify` on x8 and on x7.
- This is not an instrument error: git did what it was configured to do. Ignored files are the same class.
- The hook runs the preflight in the same tree, so it would pass too (READ ONLY, hook:395).
- ACTION: one line in the seats' use note: the pre-run proves the commit plus whatever `git status` cannot see, exactly as the hook does.

**G4. Minor, Q2: X 8th's N1 mid-run and end arms could not show the push path.** X 8th's own arms ("N1 run: the fault appears mid-run" and "... at the very end") use stub records, which never qualify. They check the record fields, which is the right check for the fix, but no `--no-verify` could happen there on either side. My arms MID and END close that gap with NON-stub pre-runs, the production 60 s read, and the real driver (MEASURED AT RUNTIME, evidence/x7_n1.out, x8_n1.out):
- MID (fault plus a seat's edit live only across the 60 s read):
  - x7: `--no-verify` of the RED text.
  - x8: `tree_moved` names "status FAILED rc 128", decide FALL BACK `tree_stable`, hook path.
- END (fault arrives before the end read with the edit present; the seat reverts both before launching):
  - x7: `--no-verify` of the RED text, with `tree_reads=0`.
  - x8: `tree_clean_end=False` (end rc 128), decide FALL BACK `tip`, hook path.

**G5. Minor, Q6: the side-by-side harness is ready, with these limits.** READ ONLY unless a measurement is named.
- HOLDS does not check that the two pre-runs overlapped in time, or that `--min-tree-reads` was left at its default. Both are visible in `sidebyside.json` (`started_utc`/`finished_utc`, `min_tree_reads`), so read them there.
- The hook runs after both pre-runs, not beside them.
- The pre-runs are launched with `--max-load 1000`, which bypasses the load gate.
- The VOLATILE normalisation was measured only against fixtures. A real-output token it misses (for example an `HH:MM:SS` time) gives a false DOES NOT HOLD. That is the safe direction, but it costs a real run.
- Same-text pairing is a multiset match: it ignores line order. That is enough given the rc, legs and verdict rows, but it is order-blind.
- Red on X 7th's shipped harness and green on X 8th's, re-run by me: 9 of 9 each way, evidence/sbs_x7.out, sbs_x8.out.

**G6. Note, Q5: ADOPT is still reachable as a mode, not as a tool.** `X8_ADOPT_PREFIX` (the launcher's 10th argument) gives exit 7: not joined, no ticket, nothing pushed (MEASURED AT RUNTIME, x8_tampers.out). `adopt_x8.py` is not in the first-use set. This is gate 237's N14, unchanged.

**G7. Note, unchanged design: `qualify` sets no minimum on `tree_reads`.** A short run with 0 interval reads qualifies; END on x7 showed that. That is F9's stated bound. Only the side-by-side enforces at least 15 reads, and only for itself.

## Questions

### 1. N1 at every read
FAIL condition, declared before running: on x8, any arm that ends with a `--no-verify` push of RED committed text is a BLOCKER. Fault: real git, `status.showUntrackedFiles=garbage` (status rc 128, empty stdout).

| Read | Arm | X 7th shipped | X 8th |
|---|---|---|---|
| pre-run start (`prerun_x8.py:290-293`) | E1 | run rc 0, `tree_reads=1 moved=0 clean_end=True`; driver `--no-verify`; RED at origin | `run` REFUSE "cannot read the working tree"; no record; driver PRECHECK FAIL rc=1 "git status failed rc=128"; exit 5 |
| pre-run 60 s read (`:265-273`) | MID | `--no-verify`, RED at origin | `tree_moved` = status FAILED; FALL BACK `tree_stable`; hook |
| pre-run end read (`:316-317`) | END | `--no-verify`, RED at origin | `clean_end=False`, `end_rc=128`; FALL BACK `tip`; hook |
| driver precheck plus decide's four reads, qualifying record | T0 | `--no-verify` | PRECHECK FAIL before joining, exit 5 |

Two guards, by my tampers on x8 (evidence/x8_tampers.out):
- T1, driver status rc forced to 0: decide says "git status rc 128". FALL BACK, the hook ran, no `--no-verify`. **X 8th's claim holds.**
- T2, decide accepts rc 128, re-pinned: the driver refuses before joining.
- T3, both blinded: `--no-verify` (the negative control; it shows the arm can fail).
- Controls: E2 and E3 are X 8th's and were not re-run by me. My T0 and E1 on x8 do not depend on them.

### 2. Each Major of gate 237
- **N2:** closed, `sidebyside_x8.py:84-101, 141-147`. A2, A3, A4, A6 and A8 said MATCH on shipped x7 and give DOES NOT HOLD on their own rows on x8. The A6 control holds on both. Re-run by me.
- **N3:** closed, `:51-64`, plus the hook's stderr merged in order at `:140`. A5 gave MISMATCH on x7 and HOLDS on x8 with 0 pairs. The one-changed-word control is still unknown on both.
- **N4a:** closed, `pushlock:126` `--no-optional-locks`. The index was rewritten on x7 and left untouched on x8.
- **N4b:** closed by the lines at `pushlock:84-93, 128-134, 165, 208-209, 225-234, 265-267` and `decide live`.
  - Periodic, turn and under-lock arms: red on x7 (3 of 3), green on x8.
  - The control holds on both.
  - The six x8-only arms (unpinned, hung, exit 0 with no statement, crash, budget, unpinned-clean) pass.
  - Evidence: r3_x7.out, r3_x8.out.
- **N5:** closed, `prerun_x8.py:28-82, 299-301`. The hook, cells, legs and no-legs arms are slow on x7 and refuse fast on x8. The 17-leg pin works at every site; the control runs.

**Closed only by an arm that could pass for the wrong reason:**
- The N1 mid and end record arms (G4); my non-stub arms cover them.
- The N4b arms use stub pre-runs, so "pushed after" always means the hook. That is fine for what they assert (timing: no push before the pre-run finished), but they never show `--no-verify` after a wait. READ ONLY.
- N5's red side also shows `valid_preflight_ran_on_red` False on x8. That is expected and descriptive only.

### 3. New defects in the changed lines
None reaches `--no-verify`. READ ONLY, cross-checked by the arms above.
- The live check only waits, keeps the place, or refuses. Under the lock, a live check that cannot say goes on to decide, which re-reads git and the record itself.
- A dirty or unreadable tree with a live pre-run returns 3. That is "stay queued" only, and under the lock rc 3 exits 5.
- Only one live check runs past the under-lock precheck. The call at `:130` returns 1, 2 or 3 and every one of those exits, so the bound X 8th states, at most 23 s more under the lock, holds.
- A missing or garbled legs pin gives `HEADER` = `(?!)`, so both `leg_headers` and `verdict` refuse. A pin of 1 cannot match "1/16", because `\b` fails.
- `read_cells` errors are caught in decide and in qualify.
- `pin_reasons` only refuses, and it refuses early.

### 4. X 8th's sweep: the RECORDED calls
All are fail-safe toward `--no-verify` by the lines (READ ONLY):
- driver `rev-parse refs/heads/$BR` (`:118`): an error string is not EXPECT, so it refuses;
- `core.hooksPath` (`:135`): refuses;
- `remote.origin.url` (`:151`): an empty URL makes the fetch fail, which is CANNOT SAY;
- `rev-parse HEAD` in the PUSH log line: log only, the push uses the explicit `$EXPECT`;
- the launcher's HEAD read (`:32-33`): STOP;
- prerun's `symbolic-ref` (`:291-292`): empty, so it refuses;
- `develop_gate.sh:34-35`: exits 2 on a failed diff.

`hook_changed_set_COPY` is fail-safe only in the weaker sense: G2, and the hook itself, G1.

### 5. First-use set
- 14 of 14 match at my start and my end. I worked on byte copies in scratch and never ran a tool in X 8th's folder.
- No `slots/` appeared there. Its `__pycache__` is unchanged since 23:54.
- ADOPT: the tool is out of the set; the mode is G6.

### 6. Next steps: is `sidebyside_x8.py` ready?
Yes, for Kam's "if it holds", within G5's limits. The output must show all of the following:
- `HOLDS` and exit 0.
- `2 pre-run(s)`, run with `--second-worktree`.
- For each pre-run, all eight rows `true`.
- `tree read N times (min 15)` with N ≥ 15 and the default `--min-tree-reads` (never lowered).
- Moved 0.
- Headers `16 hook 16 of 16`.
- Decide rc 0.
- At most 2 known lines, each read.
- 0 unknown, with any same-text pairs read.
- In `sidebyside.json`, the two pre-runs' `started_utc`/`finished_utc` overlapping.

Run it:
- from the `fleet/prerun/` copy, re-hashed after copying, so the slot base matches;
- on an unpushed branch commit that changes `Blockchain/Dev`;
- with the short TMPDIR (`/private/tmp/prt`) set for the harness process.

## NOT tested
- The real 16 legs, a real `prerun_x8.py run` on the real repo, the real side-by-side, any real push, `rehearse_push_x8_nb.sh`, a real network stall. All forbidden or not commissioned.
- Whether real legs tolerate a bad `status.*` value.
- Transient dirt from real legs.
- X 8th's whole pass. I re-ran these myself:
  - X 8th's side-by-side arms (9 red, 9 green);
  - its round-3 N4a, N4b and N5 arms (11 red, 17 green);
  - my own N1 arms (E1, MID, END, T0 to T3, UNTRACKED, ORDER, ADOPT).

  I did not re-run its driver tampers (147), library tampers (63), side-by-side tampers (14) or its tools suite.
- E2, E3 and E4 were not re-run by me.
- The G1 hook comparator used the fixture hook at 35bcfa000, not origin develop's current hook. X 8th reads the same pin (74e8d270) at a65ae7ed.
- `QA_AGENT_CHARTER.md` was not read: the commission listed only the template.

## Conduct
- **Scratch:** /private/tmp/g263, one copy each of X 7th's and X 8th's tools. In the harness copies only two constants changed (`X7`/`X8` and `BASE`): my x7 copy matches X 7th's `final_shas.txt` in 33 of 34 files, and the 34th, `test_driver_x7.py`, differs in exactly those two lines (diff checked). Tool bytes are unchanged.
- **Origins:** local bare repos only. The planted guard control refused the real queue path in every run.
- **Audit** (evidence/audit.out and the run outputs):
  - 69 worlds' call logs, 1,664 lines, 16 pushes, 8 of them `--no-verify`;
  - 0 lines naming a real path or host;
  - 0 origin URLs outside /private/tmp/g263 (the stub ssh form `ssh://fakehost/private/tmp/g263/...`);
  - the regex fired on a planted real line.
- **Processes:** 0 left naming g263 or the harness sleepers at the end.
- **Writes:** nothing outside my scratch and this folder (evidence/ is 72 KB). No push, no queue, no lock, no mail.
- **Reads outside the folder:** X 7th's and X 8th's records (copied), `decision_queue.sh show` (read verb).
- **My faults:**
  - One Bash call carried a stray `cd /dev/null`. The hook refused it and nothing ran; I re-issued it without the `cd`.
  - A zsh `=====` separator and an unquoted `set -- $kv` were also refused by hooks and re-issued.
  - My first audit regex counted the stub ssh URLs as "outside". I recounted with the right prefix: 0.
- **Disk:** DevMASTER read 21 GiB free at the start and 21 GiB at the end. The boot volume went from 290 to 286 GiB free. I leave 80 MB at /private/tmp/g263 and deleted nothing.
