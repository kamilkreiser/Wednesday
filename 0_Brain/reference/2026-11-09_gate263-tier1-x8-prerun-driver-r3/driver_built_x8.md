Seat X 8th

# DRIVER BUILT, round 3 (the one narrow third round, Kam's card secuura-prerun-push-third-round-1106 = a)

Your gate reads this next; I stop here. Nothing was pushed. No --no-verify ran outside a scratch repo. No ADOPT against a real queue. No ticket moved, no human mailed, no cc. Pushes stay on the hook until you say otherwise. A NO GO ends the mechanism for good.

## ONE CLEAN PASS

The THIRD full pass, 2026-11-08T12:54:28Z to 14:02:37Z (`python3 -I -B tools/run_all_x8.py`). Summary: evidence/final_summary.txt; each suite's output: evidence/final_<suite>.out. The two void passes before it are under "THE ROUTE", below.
- rekey rc 0: the residual scan is OK per file; its control finds 12 hits on the pristine v3.
- tools 114 of 114; launcher 14 of 14; prerun 154 of 154; sidebyside 33 of 33; driver arms 106 of 106; adopt 36 of 36.
- driver tampers 147 of 147 (146 tampers; coverage 122 changed logic lines, 0 uncovered); library tampers 63 of 63; side-by-side tampers 14 of 14.
- reds against shipped x6: 28 of 28 reproduced. Round 3 reds on X 7th's shipped files: 29 of 29 as declared.
- rename: 5 files equal X 7th's re-keyed text (pins masked); 4 changed by round 3 (diffs at evidence/round3_diff_*.txt). Control: a one-letter change is seen.
- audit: 370 worlds; 9,837 git calls (196 pushes, 105 of them --no-verify, all into scratch origins); 3,881 ssh stub calls in 264 worlds; 0 lines naming a real path or host; 0 origin URLs outside scratch. Control: the regex fired on a planted real line.
- FILES UNCHANGED DURING THE PASS: 41 files hashed before and after. Re-hashed again before this mail: 0 of 41 differ (control: one byte more is seen).
- I counted `^FAIL|CRASH|Traceback` in all 14 final_*.out, not only the summary: 0 in each. The same count reads 1 on pass 2's tamper output.

## N1 to N5, each by its id

**N1 (BLOCKER) FIXED.** A `git status` that fails is no longer read as clean, at every read that can reach --no-verify:
- prerun_x8.py: the start read refuses ("cannot read the working tree ... rc 128"); so does a HEAD that cannot be read. A failing 60 s read is recorded as moved, so qualify refuses tree_stable. A failing end read gives tree_clean_end false, and its rc is kept in the record (`tree_end_status_rc`).
- prerun_decide_x8.py: the four worktree reads (HEAD, symbolic-ref, tip, status) honour their rc. A failure is reason `git`, which means FALL BACK to the hook, never QUALIFIES and never REFUSE.
- The driver's precheck (the template edit `x8r3-n1-clean`; v3's line 111): a status rc other than 0 refuses, with a message that names the rc.
- Red first, on X 7th's SHIPPED files, through X 7th's own harness (tools/red_x7.py; each red must ALSO show the world reached the defect, N6). Arms: N1 E1 (the verdict's defect: the RED commit went --no-verify on shipped; here `run` refuses and the driver refuses), N1 E2 and N1 E3 (controls, hold on both), N1 E4 (the comparator: the same hole on today's hook path, also closed by the precheck fix), "N1 a good record and a clean tree that cannot be read", "N1 decide reads a failing status as clean", "N1 run: the fault at the start / appears mid-run / appears at the very end". Library cells R3 N1 x6, decide cell and mutant in test_tools.
- Two independent guards, measured: with the driver's rc check tampered off, decide's own N1 fix still sends the push to the HOOK, never --no-verify. The tamper row pins that as a check that must NOT flip.
- SWEEP (grep of every git call in the first-use set, counted on the re-keyed files BEFORE the fixes; positive control: every file that calls git returned its lines, the driver 15, decide 10, prerun 14, sidebyside 8, develop_gate 5, launcher 1):
  - FIXED, could reach --no-verify: the driver's status read; decide's four reads; prerun's start, interval and end reads.
  - FIXED, harness only: sidebyside_x8.py's precondition reads (rev-parse, status, for-each-ref) now read rc; a status that fails cannot compare.
  - RECORDED, fail-safe, unchanged: the driver's `rev-parse refs/heads/$BR` (any failure != EXPECT, refuse); `config --get core.hooksPath` (failure != .githooks, refuse); `config --get remote.origin.url` (empty URL, fetch fails, CANNOT SAY); `rev-parse HEAD` in the PUSH start log line (log only); the launcher's HEAD read (empty != HEAD, STOP); prerun's `symbolic-ref` (empty, refuse); develop_gate.sh (reads rc already); hook_changed_set_COPY's diffs (an empty set on failure, as the hook's own `|| true`: gate 237 Q4, not a second blocker).
- NOT TESTED: whether the real 16 legs tolerate a bad `status.*` value.

**N2 (Major) FIXED.** sidebyside_x8.py prints no bare MATCH. It computes gate 237's Q8 checklist per pre-run against the one hook output and prints HOLDS only if every row of every pre-run is true. The rows are rc (pre 0 AND hook 0), format_gate (rc 0 and the same [format-gate] lines), unknown, known (at most 2, each printed), tree (moved == [] and reads >= --min-tree-reads, default 15), clean_end, legs (N headers and a verdict in both), and decide (prerun_decide_x8.py beside the tool says QUALIFIES, `DECISION path=no-verify`, no reason lines). Exit 0 HOLDS, 1 DOES NOT HOLD, 2 could not compare.
- Kam's card asks for TWO pre-runs: `--second-worktree WT_C` runs a second pre-run AT THE SAME TIME in a third checkout of the sha (one slot each, measured overlapping), against the same hook output; HOLDS only if both hold.
- Q8 item 2 and N15, taken under this Major as ruled: a sha already on the remote (a develop sha) cannot compare (A1's refusal stands); the usage line names only flags the parser takes.
- Red first on X 7th's shipped sidebyside_x7.py: A2, A3, A4, A6, A8 each said MATCH there; here each is DOES NOT HOLD on its own row. A6's control (one postmaster line) still passes on both.
- Where decide is the second guard: the rc, format_gate, tree and clean_end rows each flip under their own tamper, but HOLDS still fails through the decide row, because decide refuses those records too. The tamper rows declare the row; the first runs are kept (evidence/sbs_tampers_first.out, sbs_tampers.out).
- --min-tree-reads is a CLI knob (default 15, printed in the result) so scratch tests can run in seconds; the real run uses the default.

**N3 (Major) FIXED.** The hook runs with stderr merged into stdout IN ORDER, the way the pre-run writes its output file. A differing line whose same text appears on the other side is a same-text PAIR, read off and printed before anything is called unknown. A5 (one stderr line mid-run, identical runs) was MISMATCH on shipped and is HOLDS here with 0 pairs needed. A real difference (one changed word) still reads as unknown on both: the control. Each of the two fixes has its own tamper: the pair count shows the in-order merge, which the pairing would otherwise hide.

**N4 (Major) FIXED, in both parts.**
- N4a: `--no-optional-locks` on the driver's status read (its only status read). The arm measures the mechanism, not the flag alone: a plain status rewrites a stat-stale index (it held index.lock for that moment); the flagged one does not (probe at evidence/n4a_probe.out). Red on shipped, green here, tamper.
- N4b, the shape you confirmed:
  - The slot holder names its worktree. decide's new subcommand `live WT` (through the driver's existing decide pin) answers with a statement AND an exit code: exit 0 + `LIVE-CHECK LIVE slot=n pid=p wt=W`, or exit 1 + `LIVE-CHECK NONE wt=W`. Anything else, including a crash (exit 1 with no statement), is "could not say". One correction to my plan's wording: I had written "exits 1 when none does", and a crash also exits 1, so the statement is required too.
  - Periodic precheck: dirt while a pre-run is live in my tree is not judged. The other checks still run, the driver stays queued, the place is kept, and it is not counted against NETMAX. Dirt with no pre-run live still exits 5, as in v3. A live check that cannot say is CANNOT SAY (rc 2, counted), as for a network read.
  - At MY TURN: wait while a pre-run is live, holding NO lock, within the lock wait's own budget (MAXPOLL x 3 s from MY TURN; the budget is carried into the mkdir loop). A pre-run that outlives it costs the place (exit 1), and nothing runs beside it.
  - Under the lock, just before decide: one more read. A pre-run started after my turn refuses (exit 5, nothing pushed, no hook beside it). A read that cannot say goes on as before round 3.
  - New bound: each live check runs under LIVE_BOUND (20 s, knob X8_LIVE_BOUND; normally ~0.2 s). At most one live check happens under the lock on any path, so your measured under-lock bounds grow by at most 23 s: --no-verify 2,626 to 2,649 s; hook 4,686 to 4,709 s. No new KILL. Nothing the hook guards changed.
  - Arms red on shipped: "a leg's file during the periodic precheck: the place is kept"; "the turn arrives during a live pre-run: wait, never the hook beside it"; "a pre-run started in the tree under the lock is refused". Control: "dirt with no pre-run still leaves the queue". x8-only arms (nothing to red on shipped): an unpinned decide's live answer is never read; a hung live check is bounded (CANNOT SAY); live exit 0 with no statement and live crash are CANNOT SAY; the wait is the lock wait's budget; an unpinned decide with a clean tree goes on as before (the hook). Library cells R3 N4b x6 (a pre-run is live from the moment it holds its slot, through its format gate), decide live cells and mutants.
- OPEN, named:
  - A pre-run started after decide (during the hook push) is not seen; that rests on the seats' rule, one tool per tree.
  - A pre-run run from another copy of the tool uses another slots/ folder and is not seen.
  - A slot whose holder file is not yet written names no worktree (microseconds).
  - Transient dirt from real legs is UNMEASURED.
  - The use note (verdict Q7) is yours to give.

**N5 (Major) FIXED (the part that is mine).**
- `run` checks the three pins FIRST (after the start reads, before the format gate and before any leg), for non-stub runs, and refuses within seconds with one plain line, so a seat does not spend about 20 minutes on a slot only to land on the hook. The pins: the hook's sha at HEAD; the cells pin's blob of `Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh` at HEAD (your ruling: the cells file gains a blob line; decide and qualify still read the count from line 1); and preflight.sh's own `TOTAL_LEGS=` line at HEAD against the legs pin.
- The leg count has one source: `prerun_expected_legs_x8.txt` beside the tool (16), read once, used at every site that said 16 (the header pattern, the verdict rule incl. its sum, leg_headers, the PR line). A missing or garbled pin fails safe: no record qualifies, `run` refuses fast, no crash.
- Measured at develop a65ae7ed: 82 run_shell_suites cells at RUNTIME (scratch export; evidence/cells_runtime_a65ae7ed.out: `run_shell_suites: 82 passed, 0 failed`, 82 ok lines); blob 2c03e3dc; hook 74e8d270 (= the pin; last changed a3e6e0474, 2026-10-19); `TOTAL_LEGS=16` at preflight.sh line 185.
- Both directions you measured rest on one unchanged rule: decide compares the hook blob AT THE PUSHED COMMIT with the pin, and any difference takes the hook path at the turn. That covers a branch built after a hook merge with the pin not edited, and a pin edited with the branch on the old hook. X 7th's F10 arm in this pass shows no --no-verify, path hook, the hook ran. `run` now says so first, in seconds. I did not re-measure the two directions separately.
- Not mine, yours: a named owner and trigger for pin edits; a periodic count of FALL BACK rules (Q6b).

## RECORDED, not commissioned (one line each)

- N6: taken where N1's reds needed it. Every round 3 red must also show the world reached the defect (valid_ checks); X 7th's red_x6 reds are unchanged.
- N7: the cells count is still whatever file the seat names (decide, launcher); `run` reads only the pin beside the tool.
- N8: a .pyc can still answer for the pinned library (malice).
- N9: a long TMPDIR still costs the place (wording item 1 says so).
- N10: line 404's wording, in the proposal.
- N11: the fallback PR line is still jargon.
- N12: `run` still has no overall bound; with N4b a hung pre-run now also makes a driver at its turn wait out the lock budget (exit 1).
- N13: __pycache__ beside the tools (the driver runs decide without -B); seen in my own tools folder.
- N14: ADOPT's mode is still reachable by a 10th launcher argument; ADOPT stays out of first use.
- F6 / Q10: five wording edits at drafts/standing_lines_proposal_x8.md (proposal only).
- Q6a: the partition HOLD is dropped; this round touched no preflight.sh.

## FIRST-USE SET (no ADOPT)

sha256 of the 14 files, all in tools/ of the record folder, as the pass hashed them:

```
cc29e44bd3823b22ef98a0d593feb2a734be784dfa39fe3e978735e435df64d6  pushlock_x8_newbranch_v3.sh
f0e5be5cca525601a7570445e0c38fc4decc1b5506cb60daefdf06e99664028d  launch_driver_x8.py
0b7a0be68a3bcc3652c0d8a6c81496a08672fb300749f2375831f4d71a2265d0  rehearse_push_x8_nb.sh
1e3cb73a1198bc002b014c08fef1753f52c287945fe8e1e3bad35baecb293c8c  develop_gate.sh
ed2cfc5258337c3b8c8b1b5eae4f3bd394a2ecd88562ae80aa485cc6856e73f4  overlap_gate.sh
c7f54f36f1e5d4821fbcafca2c00498c7afa29ca96c7d6eb7fa7ef315e3330c4  bound_x8.py
68bb7c6da31e867af08eb0bc8f6bb2473a9aa823744e558fe9950138730eb4de  sshv_x8.sh
fc335d76cf4ba6389885c9033ebe7047a036918a22f7e703d26af7bb4fc20894  prerun_decide_x8.py
71ba3d8de71c34ad3f75b724a61da0482d16ca547dbfc4291875776452bc9f22  prerun_prline_x8.py
338b5d98afb255ec26da0a5d5db575ba41775412bcbef0bb5bb019f7c16f1cea  prerun_x8.py
9b5d0af4762881060dd8feefffebfb59d6e58aaeb088a52e1355483accf19d41  prerun_expected_hook_x8.txt
05c3ebf1c18d3569afea9cd340f9d3ecbe461ff18fac8d96fc20b20202011311  prerun_expected_cells_x8.txt
e6c21e8d260fe71882debdb339d2402a2ca7648529bc2303f48649bce0380017  prerun_expected_legs_x8.txt
91e5895845504763f77681f6683db444cb815f2cab1aaad9cc7f3b692c60c3b0  sidebyside_x8.py
```

- The pins inside them agree: the driver's DECIDE_PIN equals prerun_decide_x8.py, and its PRLINE_PIN equals prerun_prline_x8.py. Both tools pin prerun_x8.py (338b5d98).
- The hook pin reads 74e8d270, the hook at 35bcfa000 (and at a65ae7ed). The legs pin reads 16. The cells pin reads 82, then `blob 2c03e3dcb2a0... Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh`.
- adopt_x8.py (61c8c2f4cf4e4e34) is NOT in the set. All 41 shas: evidence/final_shas.txt.

## NOT TESTED

- The real 16 legs against a bad `status.*` value.
- Two preflights in one tree on real legs, and transient dirt from real legs.
- `rehearse_push_x8_nb.sh` (it reaches the real gates and gh; never run by me).
- The real side-by-side and any real push.
- `prerun_x8.py run` on the real repo.
- A real network stall.

## THE ROUTE AND WHAT WENT WRONG ON IT (own faults)

- **A FIRST PASS WAS VOID** (11:06:04Z to 11:35:52Z; kept at evidence/pass1_voided_x8/). Four suites failed, all mine:
  - make_x8.py skips every line that names LINEAGE, and four CODE lines did (`if "LINEAGE" not in l`), so their x7 names survived. Its own leftover scan had the same blind spot. That broke the launcher proof (12 of 14) and the static arm, and the static arm's crash stopped the driver tampers.
  - Two of X 7th's library tamper rows anchored on the `range(1, 17)` that N5 replaced.
  - The hung-decide arm ran into two live checks at the 20 s default, because the worlds never set X8_LIVE_BOUND.
  - The static arm's knob list lacked X8_LIVE_BOUND.
  Each was fixed at its root, and the failing suites were re-run green before the second pass. A compile sweep I first trusted was blind (`tail -1` of a traceback is a blank line); it was redone on exit codes, with a broken file as the control.
- **THE SECOND PASS WAS VOID TOO** (started 11:38:40Z; kept at evidence/pass2_voided_x8/, with WHY_VOID.txt). 1 of 147 driver tampers failed: `decide-pin-check` flipped says_71 but not says_not_pinned.
  - Cause, measured (evidence/probe_pinmsg_x8.out): my N4b live-check line under the lock says "prerun_decide_x8.py is not the pinned file, so its live answer is not read". X 7th's F2 arm counted ANY "is not the pinned file" as the decide pin's message. With the decide pin check tampered off, the live line still satisfied it. The guard itself held: the mutant pushed --no-verify on the unpinned decide (hook_ran flipped).
  - The same FAIL was line 16 of pass 1's tamper output. I did not read it then, because that suite crashed later and I read only the crash.
  - Fix: each check names its own site. F2 reads the decide-site text `is not the pinned file (sha256`; the round 3 unpinned arm reads `so its live answer is not read`. The row now also requires hook_ran to flip, and pins the live line as a check that must NOT flip. Control: under the live-message tamper, that check goes False and F2's check stays True (evidence/fix_pinmsg_x8.out). The touched arms and tamper rows were re-run green before this pass; every FAIL line in every pass 2 output was counted, and this was the only one.

- Rename first: make_x8.py, count-asserted. Run 1 protected an `# X7` comment to the end of a SOURCE line, which froze code built on that line; it was quarantined (quarantine/make_x8_run1) and redone. rename_equiv_x8.py shows that 5 files equal X 7th's re-keyed text and that the 4 changed files are exactly round 3's diff (evidence/round3_diff_*.txt).
- Six tamper or arm declarations were wrong on the first run (a seventh, decide-pin-check, is the void second pass above), all for reasons I can name, and each first run is kept:
  - a missing pin file returns before the tampered line;
  - decide is a second guard (N1, and four side-by-side rows);
  - the carried budget still exits 1;
  - a fast loop also prints the outlived line;
  - a bare "waited " matched other status lines;
  - one tamper was aimed at the wrong arm.
- Boot: three `cd` calls before the brief, and a stray `cd /` at ~10:05Z. One more after pass 3, at ~14:05Z: a `(cd tools; true)` in a subshell, inside the re-hash command. It changed nothing (the subshell's cd is discarded; every path was absolute), but the rule is no `cd`. The first shared-checkout reads ran without GIT_OPTIONAL_LOCKS=0. I read the inbox before the watcher. One re-hash instrument (by basename) was thrown away.
- Reads outside REC: `git ls-remote origin` (boot) and `git archive a65ae7ed Blockchain/Dev/scripts` (for the runtime cell count) through the shared checkout, read verbs only; `push_queue.sh list` once (empty); STANDING_LINES lines 96, 404, 418, 438; the gate's verdict and evidence.
