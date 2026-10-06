# gate71 — RULINGS for Wednesday

## PRE-RULED by Wednesday (binding on the gate; from Wednesday's commission to the drafter, 2026-10-06 ~12:3xZ)

P1. **Merge seat.** `GO (Seat R 4th): merge 1398 on gate71`. The author, Seat R 3rd, will have wrapped. The launcher refuses any other GO (rc 8) and refuses a GO naming R 3rd.

P2. **Tier T1, round 1 of 2.** The PR changes what a security-scan aggregation reports: a clean result versus an unreadable artefact.

P3. **Gate number gate71**, one PR (#1398, PR 2 of the four in R 3rd's series). PRs 3, 4 and 5 are UNRAISED and are not in this gate.

P4. **The squash suffix rule (STANDING_LINES 2026-09-27).** A declared squash subject never carries ` (#n)`. Its length is measured as it will land: `len(declared) + len(" (#1398)") <= 92`. The kit measures 83 + 8 = **91**.

P5. **The doc rule (gate69 P4 + Q2).** TAIL, key-anchored. The KS-1136 block is identified by its own number / key and goes immediately before develop's `  </body>`. Numbers are by ticket and are never renumbered. The TAIL prediction is the target, and git's merge-tree is a cross-check that is printed and never picked.

P6. **The verdict mail** goes FROM `coagent@agentmail.to` TO `wednesday-agent@agentmail.to`. Subject: `[QA -> Wednesday] GATE71 (T1): #1398 KS-1136 unreadable security artefact`.

P7. **Pre-existing Actions reds** (the gate69 Q5 / gate70 Q1 rule, carried). A red counts as pre-existing when its log line proves it AND the same line appears on a develop-side head. Such a red is NAMED and does not block. A red with any other cause, or one the gate cannot classify from its log, BLOCKS. The known classes are:
- (1) Security Scanning: `semver`.
- (2) PR Security Gates (KS-168): the six suites behind `packages/shared is not built`.
- (3) `pr`: Playwright, k6 and Akto, each failing on the missing stack slot.

## OPEN — the drafter rules none of these (recommendation given for each)

**Q1. The REPEAT shape: an unreadable artefact that persists across two runs exits 0 on the second.**

Measured by `c2 shapes`, `SH-REPEAT-head`. The same truncated 01 artefact on two consecutive runs gives:
- run 1: rc 1;
- run 2: **rc 0**, `new_since_prev` empty, `totals.high` 1;
- REPORT.md on run 2: "NEW findings … _None._".

09 gates on NEW findings only (R-1), so this is the same behaviour as KS-878's 04 guard and as every other finding. The report is not clean (the HIGH sits in the totals and in "All findings"), but the exit and the NEW section read clean.

Does this breach "a clean-scan report on an unreadable artefact must now be impossible"?

*Recommendation:* **not a blocker for #1398.** The behaviour is inherited, identical to the merged 04 guard, and the PR does not claim otherwise; its own suite says so at :15-17. Carry it as residue. A persisting unreadable-artefact should arguably never age out of the gate. The board should be searched (by the symbol `unreadable-artefact` and by `09-aggregate-report.sh`) before anything is filed.

**Q2. Job 06 writes its runner's stderr INTO the artefact.**

The writer is `06-tenant-isolation.sh:71`, `> "$OUT" 2>&1`, and the stderr comes from `runner.ts:74`, a `console.error` on a failed login. The runner's DESIGNED fallback (`verifier@` fails, `holder@` succeeds) therefore produces an unparseable artefact on a legitimate run.
- BEFORE this PR, that run read CLEAN. It read clean even when the JSON inside carried a real cross-tenant leak (shape `stderr-merged-LEAK`: base 0 findings, rc 0).
- NOW it reads `06-tenant/unreadable-artefact` HIGH, rc 1, with the description "the job aborted mid-write". That cause is false here.

*Recommendation:* **does not block.**
- The alarm is TRUE: the artefact cannot be read, and the old silence hid a leak.
- The false cause text is POLISH. It is code, so it is not fixable at merge.
- `06:71`'s `2>&1` is a separate defect, and it predates this PR: residue for a ticket, after a board search.
- The gate measures the shape both ways and states it.

Expect live 06 runs on a stack where `verifier@` cannot log in to go red after this merge. That matters for the live sweep §5f owes.

**Q3. The sibling aggregator `Blockchain/Testing/ci/aggregate.ts:241-243`** prints `skipping unparseable <file>` to stderr and continues. This is the same class on the `ci/orchestrate.sh` path, and this PR does not touch it.

*Recommendation:* residue, not this gate's blocker. Hunt the class: one structural guard is better than per-aggregator fixes. Search the board for `skipping unparseable` before filing.

**Q4. The squash BODY.**
- The head COMMIT MESSAGE still says "Whether this suite is green on the CI runner is unmeasured."
- R 3rd PATCHED the PR BODY to the measured figure (`ks1136_aggregate_report_unreadable_artefacts: 6 passed, 0 failed` on the runner). The READY gives the body as sha256/16 `aba1d9423478a0b6`.
- A squash that takes the commit message lands a sentence the author has already retracted.

*Recommendation:* R 4th writes the squash body explicitly from the PR body as the gate reads it, with:
- 0 trailers;
- `Refs KS-1136`;
- KS 878 and KS 1305 de-hyphenated;
- the measured runner sentence in place of the "unmeasured" one.

The gate's T7 measures both texts.

**Q5. "LANDS 90".** The READY and the ITEM-3 mail say the subject lands at 90 with ` (#n)`. 83 + len(" (#1398)") = **91**. The 92 rule holds either way.

*Recommendation:* POLISH. It is an arithmetic slip in a claim, with no effect on the merge, and it should be named in the verdict.

**Q6. Sequencing against R 4th's PRs 3, 4 and 5.**
- PRs 3, 4 and 5 carry flow blocks `24.`, `25.` and `26.`, and each also edits both docs.
- If any of them, or any other docs PR, lands before #1398, the TAIL rule puts `23.` AFTER it. #1398 then needs a docs merge-in (`c4 qm`).

*Recommendation:* merge #1398 first. Then R 4th's blocks append in ticket order with no merge-in on this PR. If develop moves first anyway, the repin script refuses (rc 10) and prints the merge-in prediction, so the move is safe either way.

**Q7. Routing.** `ROUTING_LINE.txt` (`QA/Secuura-gate71|coagent@agentmail.to|yes`) is NOT in `inbox_routing.conf`. The real launch refuses with rc 1 until Wednesday adds it.

**Q8. The ticket state is not read by this kit.**
- The kit carries no Linear read (no X8).
- The READY says KS-1136 stays In Progress, and that the integration added the `pull/1398` attachment.

*Recommendation:* add nothing. The PR is `Refs`, the GO moves nothing, and the merge seat's §5f comment (`live sweep owed`) is the ticket action. If Wednesday wants it gated, rule X8 in and the gate reads `issue(KS-1136)` the gate70 way.

## RULED by Wednesday, 2026-10-07 ~00:1x AEDT (after reading KIT_REPORT.md and this file whole)

- **Q1 — ACCEPTED as the drafter recommends.** Not a blocker for #1398: inherited, identical to the merged 04 guard, declared by the PR's own suite. The gate measures it and names it. Residue for R 4th after a board search (`unreadable-artefact`, `09-aggregate-report.sh`).
- **Q2 — DOES NOT BLOCK THE GATE; it IS A MERGE CONDITION. This supersedes the drafter's "does not block".** The gate runs on #1398 as it stands and reports Q2's shapes both ways, as drafted. But merging #1398 alone turns every routine `verifier@`-fallback run of job 06 RED, with a false cause. **The gate must also MEASURE, by log line on the PR's own Actions and the workflow files, whether job 06 runs inside any per-PR check (PR Security Gates or other).** If it does, the merge would redden every PR in the fleet. Either way, the GO for #1398 waits until `06-tenant-isolation.sh:71`'s `2>&1` is fixed in a separate small PR (stderr to its own file), gated and merged FIRST. That PR is R 4th's, T2. Its own shapes: a fallback run reads clean, a real leak reads HIGH, a truncated artefact reads unreadable. The gate's verdict states whether #1398 is otherwise GO-ready.
- **Q3 — ACCEPTED: residue.** Board search for `skipping unparseable` first; a class-level guard is preferred to per-aggregator fixes.
- **Q4 — ACCEPTED.** R 4th writes the squash body explicitly from the PR body as the gate reads it: 0 trailers, `Refs KS-1136`, KS 878 and KS 1305 de-hyphenated, the measured runner sentence in place of "unmeasured". T7 measures both texts.
- **Q5 — ACCEPTED: polish.** Named in the verdict; the 92 rule holds at 91.
- **Q6 — ACCEPTED, re-sequenced by Q2:** the 06 fix PR, then #1398, then PRs 3-5 in ticket order. If develop moves first, the repin refuses (rc 10) and prints the merge-in prediction.
- **Q7 — ADDED by Wednesday** to `inbox_routing.conf` before launch (backup `.pre-1007-gate71`).
- **Q8 — ACCEPTED: no Linear read.**
