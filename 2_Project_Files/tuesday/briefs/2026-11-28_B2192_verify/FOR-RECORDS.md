# B2192 FOR RECORDS (for a records seat; Jira writes are that seat's, not the gate's)

The gate did not read Jira: the credentials sit in `4_Credentials/`, which this gate may not open. The states below come from N186's STATUS (`PRIOR WORK`, re-read at 23:54 on 27 Nov): RD-1051 Task, Medium, [test-infra], To Do; RD-1052 Task, Medium, [operations, tooling], To Do; linked as Relates. Re-read both before writing.

## RD-1051 (rd490 port band). AFTER the merge commit M is on main and landing.txt steps 3b, 3c and 4 read as expected
Comment (plain text; no person, seat, card or build id):
> Landed on main by merge commit <M> (pull request #<n>, merge commit pinned to fc5975f6, not squashed). The rd490 browser guard now takes its two server ports from `workerBand()`, its worktree's own band. The fixed band 38900-38939 shared by every copy is gone. A new cell asserts that both servers listen inside that band. Verified: the file was run in two worktrees on different slots (0 and 11) at the same time, both 73/73 green, each pair of servers inside its own band and no port seen on both sides. The full verify was 6655/6655 across 421 suites; the hosted build of the pull request and main's push build were both `VERDICT: PASS` 6655/421; code scanning at <M> read 29 results and 22 open alerts, as on main before. Limits: two worktrees on one slot (1 in 19) still share a band (the listener check names the collision), and any tree from before <M> still uses the fixed band. Nothing deployed: the Deploy demo run at <M> read build skipped and deploy skipped.

Move: To Do -> Done (the project's own transition name; read the transitions first).

## RD-1052 (counted jest slots in nexusai-lock.sh)
Comment now (after the gate; the ticket stays open):
> The candidate script (sha256 52713e55345726abc769c4601cc52daf5b5496eab96b346ebacaada300356260) was reviewed against the live lock (sha256 cf01bafb...4971f). It does what the design asks for, with no `slots-jest` file meaning one slot:
> - slots apply to jest only;
> - first-in, first-out order is kept;
> - stale and ownerless holders are taken over per slot;
> - the owner file records slot= and wslot=;
> - two holders on one worktree slot never run together.
> It was proved in scratch lock bases only. Not installed yet.
> Findings to answer before `slots-jest` is written:
> (1) a tree from before the rd490 change still uses 38900-38939, and the lock cannot see that;
> (2) the worktree slot is read from the caller's working folder, never from the tree its command runs in, so callers that run from elsewhere run alone, or record the wrong slot;
> (3) the stale test is the process id alone, with no start time, as in the live lock.

After the install (install-steps.md, step 6 green): a second comment naming the install time, the pre-copy name `nexusai-lock.sh.pre-b2175-<UTC>`, the live sha256 after the install, and "slots-jest absent (one slot)". Move to Done only if the product decision is that the ticket covers the script and not the slot count. Otherwise leave it In Progress until `slots-jest` is written. This choice is the coordinator's.

## Ticket candidates (create only on Tuesday's word; search first for a duplicate)
1. **Lock: a tree from before RD-1051 runs alone** (VERDICT M-1). When the caller's tree still holds the fixed rd490 band (`PORT_BAND = { start: 38900` in `__tests__/rd490-open-access-banner-browser.test.js`), record `wslot=unknown`. Or the kits must refuse a NexusAI jest tree that does not contain the RD-1051 merge (`git merge-base --is-ancestor <M> HEAD`). This blocks writing `slots-jest`.
2. **Kit wrappers declare the slot of the tree they run** (VERDICT m-2). Set `NEXUSAI_WORKTREE_SLOT` from that tree's own `worktreeSlot()`, never from cwd. The pair form, one acquisition across two trees, declares nothing, so it runs alone. Without this, every current wrapper reads `unknown` and slots buy no parallelism.
3. **Lock: holder start time** (VERDICT m-3). The owner file should record `pstart=`, and the stale test should compare it, as the ticket test does. A recycled process id should not keep a dead holder's slot.
4. **Tests: old band named in two files** (VERDICT I-2). `rd591-cross-seat-isolation.test.js` line 35 and `rd573-jest-port-band-outside-ephemeral-range.test.js` lines 65-70 and 202 still name 38900-38939 as RD-490's band. The tests are green but the wording is out of date. The kit chose to leave them (Q-6).
5. Info only, no ticket unless Tuesday wants one: after kill -9 of a holding lock script, its job keeps running, and a later holder on the same worktree slot can start beside it (gate arm A5). The live lock has the same shape with one slot.
