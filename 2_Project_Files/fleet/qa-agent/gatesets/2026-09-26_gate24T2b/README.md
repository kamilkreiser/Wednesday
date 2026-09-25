# Gateset 2026-09-26_gate24T2b — README for Wednesday

The drafter launched nothing, sent no mail, tapped no pane and committed nothing. It wrote only under
`/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/9df682b4-df07-4cdb-b01c-fee44dc335fd/scratchpad/gate24T2b/`.

This kit is ONE tier-2 BATCH gate over SEVEN PRs from THREE seats. Your two ADD messages widened it, and it is FROZEN at seven:
- **#1249** KS-1144 (L6), `6eb283d058184f1f0fabdc3c3184a817db4fb94b`: **STACKED on #1248** (`2b4960172644`), same ks781 file, +81/-14 over #1248.
- **#1250** KS-1302 + KS-1303 (L5), `c78f4093fb531bceb94a8e9defb59350d8c60b73`: `run-shell-suites.sh` + its suite. run_shell_suites goes from 49 to 55.
- **#1251** KS-1147 (L6), `8020adae99129f4b7194fef32f1ea5b762819d90`: the ks860 host regex + 2 cells.
- **#1252** KS-1275 + KS-1299 (B 28th), `ca7337fa04e04e5438bc79a5abe215424fcb33ef`: 2 descriptions, the regenerated yaml and cells. Parent is develop `77c6426b9`.
- **#1253** KS-1297 (L5), `6b88e4f03e82e3da0672efb1bb757ba5da912d6a`: the fixture guard. fixture_guard goes from 6 to 10.
- **#1254** KS-1155 (L6, ADDED), `da0c94968a7423c340b3a3b76244bda536d1f6d2`: `vitest.config.ts` setupFiles + 2 new files, all in packages/shared.
- **#1255** KS-1301 (B 28th, ADDED), `59245ff0b11c6b760ba5e2a9daedc5927e915e10`: test-only, 1 file. Parent is develop `77c6426b9`.

Routing: `QA/Secuura-batch1249`. GO string: `GO: merge #1249, #1250, #1251, #1252, #1253, #1254, #1255 batch` (or the subset). The GO must also
carry **"#1249 after #1248"**.

## 1. BLUF
- **Kit: READY to launch** once you add the routing line (§4). It is pinned over develop `fa25c9b1`, AFTER your #1243, #1244 and #1248 squashes.
  The stack is already `merged`. Every head was re-read from origin at 15:46Z.
- **The widen cap is used by NONE of Seat L5's items.** The batch holds 7 of the 8 allowed PRs. At pin, NO L5 widen item had a PR on origin:
  - ks-1201 was pushed at `d1db0d41ac52` and ks-1296 at `ff90fbf9d7e3`, but neither has a PR;
  - ks-906 and ks-1139 were not pushed.
  - The capture script reads mail by message id only, so it could not locate any of their READY mails. All four go to the NEXT batch (§6.5).
- **#1249 handles BOTH stack states, and the launch re-derives the state itself** (your message: #1248 is GO and merging now).
  - While #1248 is unmerged, #1249 is graded over develop + #1248's head.
  - Once #1248 has been squashed, develop's ks781 blob must equal #1248's head blob `f79132cc…` **byte-exact**. #1249 is then graded over the new
    develop: its own delta is 81/-14, and its equality target is the MERGED blob, which equals its head blob `e9621536…`.
  - Any OTHER blob on that path refuses: that would be a foreign move, and it needs a re-predict by hand.
  - **This is now MEASURED on the real develop:** predict_7 rc 0 in `merged` mode. Control P1248m had proved the same state by simulation first.
    Control P1248 proves that a foreign edit of the path refuses.
- **#1250 — predicted NO GO: TRAP-SWALLOWS-TERM.** This is the drafter's live probe, a PREDICTION; the gate measures.
  - `trap rss_cleanup_tmpdir EXIT INT TERM` catches the signal, and the handler neither exits nor re-raises.
  - SIGTERM to #1250's runner mid-suite gave: **rc 0**, the running suite's log deleted from under it, the next suite RAN, and the verdict
    `shell suites: 2 passed, 0 failed`.
  - develop's runner gave rc 143, no further suite, and the dir left behind (KS-1302 reproduced).
  - Preflight leg 14 runs this runner on every push, so a killed runner reads as a pass. The seat disclosed that it never exercised INT/TERM.
  - The drafted rule makes this blocking (§6 decision 1).
- **#1253 — predicted NO GO under THE READER RULE: TRAILING-PIPE** (a port, so a PREDICTION).
  - Cell 9's ERE `(\(|\$\(|\|)[[:space:]]*build_fixture ` matches a wrapper only BEFORE the call.
  - So it misses `build_fixture … | cat`, which is the pipeline shape the commit itself names as defeating the guard. It also misses `&`, backticks,
    and a `(` on its own line.
  - It flags the safe shape `false || build_fixture`.
  - Reach today is none: all 12 call sites are bare (§6 decision 2).
- **#1252 — legs 3/4/8 NOT run (no Docker, no DB). Predicted GO WITH FINDINGS.**
  - The drafter READ leg 8's script: it compares only the version, the path set, the path count and the operation count.
  - A PyYAML port shows those fields, and every operation's `security`, IDENTICAL from develop to head. With descriptions removed the specs are EQUAL.
  - So the gate owes a LEG-8-PORT through the preflight's own `yaml` package in place of the legs (§6 decision 3).
- **#1249, #1251, #1254, #1255 — predicted GO WITH FINDINGS.** The leads, all READ or port:
  - LENGTH-ONLY (#1249);
  - ESCAPE-MISMATCH (#1251, disclosed);
  - NESTED / DERIVE-MARKERS / BUDGET-LEAK (#1254; BUDGET-LEAK is UNREAD);
  - ROUTE-ISOLATION (#1255).
- **#1255's push record is GONE.**
  - Seat B 28th's next push reused `raise/s-b28-cells-push.out` from 15:13:28Z.
  - The drafter had READ it complete at 15:10:16Z (predict_3.out): 28/0, 6/0, 49/0, 60/60, INCOMPLETE 12/15, legs 3 4 8.
  - That read is the only surviving evidence (lead STOP-RECORD-OVERWRITTEN).

## 2. Pins — RE-PINNED by predict_7.out at 15:46:17Z over the MOVED develop (the first pin, predict_6 at 15:29Z over 77c6426b9, is superseded)
- **Develop moved while the kit was drafted.** At 15:45Z it was `fa25c9b10fb44da6c848a6975d86ebfa523e8602`, 5 commits ahead of BASE `6e2a00bfed57`:
  - #1246 and #1247, as before;
  - then #1243, #1244 and #1248 squashed (your GO).
  - The move ∩ every PR's own paths is EMPTY, with ONE exception: #1249's ks781 file. That is the DECLARED overlap, and develop's blob there equals
    #1248's head blob `f79132cc…` byte-exact.
  - **So the stack mode is `merged`:** develop itself is #1249's grading base, and #1249's own delta over it is 81/-14.
  - The first controls run was invalidated by this move mid-run and quarantined as controls_0_aborted_devmove.out (§7).
- **Parents** (every PR is ONE commit):
  - on BASE: #1250, #1251, #1253, #1254;
  - on `77c6426b9`: #1252, #1255;
  - on #1248's head `2b4960172644`: #1249.
- **Merged trees over develop `fa25c9b1`:**
  - #1249 `2e5bce28e9c355f6e7003d6f61b1074160062349`;
  - #1250 `c404f3359adcebadf3123005479c9f4d5bbf8fba`;
  - #1251 `c9ee3e550d227badae9c426f14048c63c90205a6`;
  - #1252 `863ccf2f24b95b0ada99adf6dfec8897aa9cbafd`;
  - #1253 `fdef1ba7d4462b48328eb21960596f7db3b6374f`;
  - #1254 `9fa9760b6242fbb8497331262d6dbc8c10fd69d3`;
  - #1255 `5fdc777f56a8de86fe0e8043e8aeba5a6f232f71`.
  - Checks (1)-(3) hold for all seven. Every merged blob equals its head blob, and every mode is unchanged (100644).
- **END_TREE `e4de98f1637580367eb1e1e035f70b9cc3834949`** (develop + all seven): 12 files, +631/-37.
  - It is identical in 53 orders. Those orders are every ORDERED PAIR of the 7 PRs merged first, plus every rotation of the sorted order and of its
    reverse. The drafter did not run all 5,040 orders (about 7 min per run); that is in §9.
  - `apply --cached` agrees.
  - END_TREE_NOSTACK `ddce03467ce569c099dff657df5fe82520bb97f1` is the END state without #1249 (for a #1249 HOLD).
- **PAIRWISE:** all 21 pairs are path-disjoint. #1254 couples to #1249 and #1251 by CONTENT only: its derived walker list equals the configured one over
  the END_TREE (port). Co-residence is at DIRECTORY level only.
- **GitHub compare** develop...head, launcher `--check` rc 0 (launcher_check_3.out):
  - merge_base BASE, ahead 1 (2 for #1249), behind 5 for the BASE-parented five;
  - merge_base `77c6426b9`, ahead 1, behind 3 for #1252 and #1255;
  - files == own paths on all seven.
  - `mergeable` was True ×7, and #1248's head was unchanged, at 15:25Z (repin_dryrun_1.out, over the old develop).
- **Instruments:**
  - `ls-remote` from the Secuura checkout (a read verb);
  - a scratch clone at `_sp/g24b_sp/clone.git` (`git clone --bare --no-local`, NO alternates), fetched from origin;
  - REST GET;
  - Linear queries only;
  - the seat records read as plain files;
  - PyYAML 6.0.3 for the #1252 port;
  - the drafter's trap probe in `_sp/trapprobe/`.

## 3. What the gate owes (the prompt `2026-09-26_secuura-batch1249-t2.prompt.txt`, 57 KB)
- **THE READER RULE**, for every PR that parses text or output: #1253 cell 9 and cell 7, #1254's derivation, #1250's note reader, #1252's verb read.
  - A shape counts as REAL if it occurs in the tree OR the PR's own text names it.
  - A wrong reading on a real shape is NO GO. The rule is run through the REAL suite (`SUBJ_SH=<probe copy>`), never a port.
- **#1250 TRAP-SWALLOWS-TERM** (mandatory): SIGTERM and SIGINT to the runner's pid, develop's runner vs #1250's.
  - The rule: rc 0, a green verdict, or a further suite after the signal = NO GO.
- **Red proofs per PR, in the tester's own clone:**
  - #1249: B1-B4 + a LENGTH-ONLY probe;
  - #1250: R-0..R-3;
  - #1251: C0, C1, C2, C4 + ESCAPE-MISMATCH;
  - #1252: V0, A1-A3, B1, B2, generate-openapi `--check`, SUBSTRING-VERB;
  - #1253: G0 + the seat's three arms in copies;
  - #1254: D1-D6 asserted APPLIED, the 6 s end-to-end probe, BUDGET-LEAK;
  - #1255: P0 + the two by-line arms, red sets read from `--json` fullName.
- **Suites, serial:**
  - packages/shared: 928 → 930 (#1248) → 934 (#1249) / 930 (#1251) / 933 (#1254). END predicted 48 files / 941.
  - originate jest `--runInBand`: 869 → 870 (#1252) / 877 (#1255). END 878.
  - The two changed shell suites standalone in the tester's worktrees, the ONE allowed standalone run: 49→55 and 6→10, and both on END.
  - lint / tsc / shellcheck / prettier deltas.
- **Fleet STOP:** claimable for all seven BY READ, and it changes.
  - The push logs were READ anchored with a NOT-FOUND control: every push shows 28/0 and 60/60, with INCOMPLETE 12/15 (legs 3 4 8 skipped).
    fixture_guard read 6/0 except #1253's own push (10/0); run_shell_suites read 49/0 except #1250's own push (55/0).
  - #1255's record was overwritten (see §1).
  - **The NEW counts after merge are: pre_push_hook_base 28/0, fixture_guard 10/0, run_shell_suites 55/0, and 60 of 60** (no PR adds a suite file).
    The MERGE ADDENDUM must carry them.
- **The gate24T2a lessons are carried:**
  - STREAM-SEPARATED captures;
  - PRESUITE-URLPATH is environmental;
  - ONE re-run on a COLD CACHE for KS-1155 5000 ms timeouts. At #1254's head and END such a timeout is a finding against #1254.
- **No Docker, no DB.** Time-box 210 min. The report dir is `reports/2026-09-26-batch1249-t2b/`.

## 4. The routing line is NOT written by the drafter. Add it FIRST (`PROPOSED_inbox_routing_line.txt`)
    QA/Secuura-batch1249|coagent@agentmail.to|yes
The drafter's read found `QA/Secuura-batch1249` ABSENT (grep -c 0, rc 1; routing_read_1.out). Without it, repin step 0 refuses with rc 1. Controls R4
and R4b prove that.

## 5. THE ONE LAUNCH COMMAND (copy to gatesets/ + re-pin + launch; run it in a shell that can reach tmux)
    /usr/bin/rsync -a --exclude '_sp' /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/9df682b4-df07-4cdb-b01c-fee44dc335fd/scratchpad/gate24T2b/ /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-26_gate24T2b/ && /bin/bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-26_gate24T2b/repin_and_launch_gate24T2b.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-26_gate24T2b/launch_qa_secuura_batch1249-t2.sh <your session scratchpad under /private/tmp/claude-501/>

**The moved kit.** Step 0b sees a MOVED KIT and re-runs predict and fill at the new home, in the same action. Predict makes a fresh `--no-local` clone
under `<scratchpad>/g24b_sp` (about 15 s). Controls R6 and F1 prove that the moved kit works.

**Develop has ALREADY moved** (#1243, #1244 and #1248's squashes, and the kit is pinned there). If it moves again, 0b and 3b re-derive over it.
A move on any PR's own path refuses and must be re-predicted by hand. The one exception is #1248's byte-exact squash on #1249's path.

The steps and their refusal codes:
- 0 routing (1)
- 0b moved kit: predict + fill (8)
- 1 ls-remote, including refs/pull/1248/head (2)
- 2 the PULLS API, including #1248 (3)
- 3 heads == pins on both instruments, open, not `mergeable:false`, and #1248's head == the stack pin (11)
- 3b develop moved → predict + fill, then develop re-read (10)
- 4 usage gate (12)
- 5 `--check` (13)
- 6 `cockpit.sh add QA/Secuura-batch1249` (14), then a pane census

**Rehearsal:** append `--dry-run`. repin_dryrun_1.out ended rc 0 at 15:25:30Z.

## 6. Decide or know before launching
1. **#1250 TRAP-SWALLOWS-TERM is drafted as BLOCKING.**
   - Rule: "a runner that, after SIGTERM or SIGINT, exits 0 OR prints a green verdict OR runs a further suite = NO GO".
   - The drafter predicts NO GO, round 1. The fix-shape is INT/TERM handlers that clean up and then `exit 130`/`143`, with EXIT kept for the cleanup,
     plus one cell per signal.
   - To grade it by reach instead, edit that sentence in the prompt TEMPLATE, and the launcher template's exit-41 anchor, and re-fill.
   - KS-1302/KS-1303 stay In Progress either way.
2. **#1253 TRAILING-PIPE falls under THE READER RULE as drafted**, because the commit NAMES `bf | cat`. The drafter predicts NO GO for #1253.
   - The alternative is reach grading: reach is 0 today (12 bare sites). To use it, edit the "NAMES it" clause in the prompt TEMPLATE and the exit-40
     anchor, and re-fill.
   - The drafter recommends launching as drafted. It is the same "a check that cannot fail on its own named shape" class that L5 lists four times.
3. **Legs 3/4/8.** All seven pushes read 12/15 (local stack not up). The kit records them as NOT run, with a LEG-8-PORT owed for #1252.
   - If the port finds a changed field, #1252 is NO GO until the legs run.
   - The seats' standing question stays yours/Kam's: is 12/15-nothing-failed the verdict for test-only packages/shared changes? Seat L6 asked 3×,
     Seat B 28th flagged leg 8 for #1252.
4. **#1249 and #1248.** #1248 is already squashed onto develop (`fa25c9b1`), so #1249's dependency is MET and there is no HOLD from it.
   The GO string still names "#1249 after #1248" for the record.
5. **Next batch, named:**
   - KS-1201: branch `feature/ks-1201-login-stub-parent-shell-l5-1` @ `d1db0d41ac52`, no PR;
   - KS-1296: `feature/ks-1296-pg-isready-missing-binary-l5-1` @ `ff90fbf9d7e3`, no PR;
   - KS-906 and KS-1139: not pushed at 15:17Z.
   - Their counts are L5's declared ones (captured as mail_l5_declared_counts.md).
   - Seat B 28th's item 4 (KS-1159) was being pushed at 15:13Z.
6. **MG-11:** these titles are too long for squash subjects: #1249 is 99 chars, #1251 is 93, #1254 is 94. The gate proposes subjects from the bytes.
7. **Hygiene:**
   - #1250's and #1253's PR bodies carry NO `Refs` line; their commits do.
   - #1250's commit body names KS-1127 and KS-1135 hyphenated, and they must be un-hyphenated in the squash body (MG-3).
   - #1255's push log was overwritten by the same seat's next push. That is a record-keeping slip for Seat B 28th.
8. **The audit fuse:** Seat L6 flags that both audit rows lapse at `2026-09-30T00:00Z`. After that, every Blockchain/Dev push is refused. This is
   Kam's call only, and it is outside this gate.
9. **`mergeable: null` policy** is as in gate24T2a: null is reported after 3 reads, not refused; `false` refuses.
10. **A leftover the drafter made:** its develop-runner probe arm left `/tmp/rss.3XtM0B`. That is KS-1302 reproduced, and it was not deleted (never
    delete). There were already about 30 `/tmp/rss.*` dirs on the box from the seats' runs.

## 7. Controls: `controls_gate24T2b.sh <scratchpad> [--invert]`
CONTROLS_SUMMARY

## 8. Files
- COMMISSION.md (with the LEGITIMATE SHAPES tables) · README.md · PROPOSED_inbox_routing_line.txt · routing_read_1.out
- **Pins:**
  - predict_gate24T2b.py;
  - predict_1.out (rc 1: the drafter's own anchor bug, fixed) and predict_2.out (rc 0, six PRs);
  - predict_3.out (rc 0, with #1255; **the only read of #1255's push record**);
  - predict_4.out (rc 1: #1255's log was being overwritten — handled);
  - predict_5.out and predict_6.out (rc 0, over 77c6426b9, superseded);
  - predict_7.out (rc 0, **the pinned run**, over fa25c9b1, stack `merged`);
  - predict_sim_*.out (merged1248: rc 1 then rc 0 after the fix; foreign1248: rc 1);
  - pins_gate24T2b.json and its SIM files.
- **Prompt and launcher:**
  - prompt_gate24T2b.TEMPLATE.txt and launcher_gate24T2b.TEMPLATE.sh.txt;
  - fill_gate24T2b.py with fill_1..3.out (rc 0; fill_3 is the pinned fill);
  - the rendered prompt `2026-09-26_secuura-batch1249-t2.prompt.txt`;
  - the launcher `launch_qa_secuura_batch1249-t2.sh` (`bash -n` rc 0);
  - launcher_check_1..3.out (rc 0). `.pre-*` files are earlier fills.
- **Repin and controls:** repin_and_launch_gate24T2b.sh with repin_dryrun_1.out; controls_gate24T2b.sh with controls_1.out, controls_2.out and
  their .rc files.
- **Captured reads:**
  - capture_mail_gate24T2b.py → mail_gate24T2b_ready.md, mail_ready_<n>.md and mail_l5_declared_counts.md (TEXT_SHA256 each, plus 7 prior-report
    sha256s);
  - raw_ready_*.txt and raw_l5_declared.txt (the first reads, same form, same sha256);
  - gh_read_gate24T2b.py with gh_read_1/2.out, gh_body_<n>.md and gh_comments_<n>.md;
  - linear_reads_gate24T2b.py with linear_reads_1/2.out and linear_KS-*.md;
  - lsremote_1..3.out.
- **Drafter's live probe (PREDICTION only):** drafter_trapprobe_g24b.sh with trapprobe_1.out.
- `_sp/`: the scratch clone, the probe trees, the control workdirs, and scratch copies of two develop files. The launch command excludes it.

## 9. NOT done / NOT measured by the drafter
- No launch, mail, tap, commit, push or routing-conf write.
- The Secuura checkout was touched only by read verbs: ls-remote, config --get, show, and `clone --no-local` reading it as a source.
- The seat records were read as plain files.
- The inbox was read only in the one permitted form (`inbox_digest.sh full wednesday-agent@agentmail.to '<id>'`): 8 ids (the 7 READYs, and L5's
  counts mail). Each was read twice: once by hand, and once by the capture script.
- **UNMEASURED:**
  - every red arm of every PR;
  - every package / suite count;
  - lint, tsc, shellcheck, prettier;
  - THE READER RULE through the real suite (the #1253 shapes were read through a port only);
  - TRAP-SWALLOWS-TERM with SIGINT, and with the real suite's own fixtures (the drafter ran SIGTERM on a 2-suite throwaway tree only);
  - BUDGET-LEAK and the 6 s end-to-end probe (#1254);
  - #1255's route isolation;
  - the LEG-8-PORT through the preflight's own `yaml` package (the drafter used PyYAML);
  - legs 3/4/8 themselves (never run);
  - KS-1155's load >= 30 bar (the seat does not claim it);
  - END_TREE over all 5,040 orders (53 were run);
  - the usage gate and the machine load at launch;
  - the real launch path (steps 4-6);
  - #1255's push record after 15:13:28Z (overwritten);
  - the L5 widen items' READY mails (never read);
  - whether any L5 widen PR opened after 15:17Z.
- **Not controlled:** exit 16 (it needs a TTY), the repin's `mergeable=False` refusal, steps 4-6, and a real `merged`-state launch (only the simulation
  P1248m).
