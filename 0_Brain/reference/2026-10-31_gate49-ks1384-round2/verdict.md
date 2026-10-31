## QA GATE 49, TIER 1, ROUND 2 (delta): KS-1384 F0b #1854 and F0c #1857
(Opus, Sat 31 Oct 2026. Findings only: nothing was fixed, pushed, commented, merged or touched in Linear. Evidence is in `evidence/`.)

**Heads.** I read these with ls-remote at the start and again at the end. They did not change.
- #1854 F0b = **da080d3fbe48** (round 1: 31e7975963a5)
- #1857 F0c = **ab59f2903405** (round 1: dfc0dd61d75e)
- develop = ddc644fb4869
- W's develop merge-in is dc8c210cb29d, an ancestor of develop. The one develop commit after it, KS-1887, is docs fragments only.
- `git merge-tree` of F0c's head with develop ddc644fb is clean.

## VERDICTS
| PR | Head | Verdict |
|---|---|---|
| #1854 F0b | da080d3fbe48 | **GO WITH NOTES**: F1 is CLOSED. Nothing must be fixed before merge. |
| #1857 F0c | ab59f2903405 | **GO WITH NOTES**: no delta of its own. Its round-1 GO stands, and gate 48's N2 still applies. |

F-b #1858 is not in this gate. The train still needs F-b's delta gate, then R1 and R2.

## Q1: is F1 closed? YES
Gate 48's probe file was run verbatim, plus 6 new cells: `evidence/probe/gate49-probe.test.ts`, on gate 48's fake world (the real submitter, the real spendFromView and the real view).

| Cell | Round-1 product (31e79759 anchorSubmission.ts swapped in) | Round-2 head da080d3 | F0c head ab59f29 |
|---|---|---|---|
| P1a (pass-2 build has pass1Inputs=[]) | pass | pass | pass |
| **P1b verbatim** (asserts the FINDING: sent 2, built 2) | **GREEN: finding reproduces** | **RED: got sent 1, built 1** | RED (same) |
| P1c control (u_F set) | pass | pass | pass |
| **P1b'** (P1b inverted: sent 1, built 1) | **RED (sent 2, built 2)** | **pass** | pass |
| G49-R: 10 re-attempts while member 1 is live | RED (2/2) | pass (1/1, no 'failed') | pass |
| G49-LOST: member 1's reply was lost (live), then a re-POST | RED (built 2) | pass | pass |
| G49-NOVIEW: a family member unknown to the view still blocks | RED | pass | pass |
| G49-BOOT: inside the boot window (arm NOT armed), the wait still holds | RED | pass | pass |
| G49-2M: member 1 dead, member 2 (pass 2 again, no u_F) live; member 3 is not built | RED (enough coins that running out cannot mask a build) | pass | pass |

Logs: `probe_r1base.log` (9 failed / 6 passed), `probe_r2head.log` (1 failed, the verbatim P1b, as expected), `probe_f0c.log`.

- **Positive control met.** The same probes go RED on round-1 product code.
- **W's cells, base control reproduced.** On round-1 product code, nf1 is RED and nf2 and nf3 are green (`w_nf_at_r1base.log`). That matches W's claim of RED 1/3.

## Q2: liveness. No wait lasts forever: it is bounded by WAIT_HORIZON_MS (2 h). But the wait never checks member 1's fate itself.
**N1 (MINOR, liveness and readback, not money; F0b `anchorSubmission.ts`, the FamilyWithoutOutpointInFlight check and its catch branch).**

The no-u_F wait is passive. It re-queues every 60 s and re-reads `view.stateOf`. Nothing on that path settles an expired member or polls a member that may have landed:
- `settleExpiredSpenders` runs only inside `spendFromView`.
- The F1 check throws before `deps.submit`, so `spendFromView` never runs on this path.

Measured:
- **L1, idle wallet.** Member 1 is past its TTL by an answered tip and absent on chain. After 5 waiter runs on one submitter, member 1 is still `live` and nothing has been built.
  - Control L1-busy: one spend for another anchor (a real `spendFromView`) settles member 1 `dead`, and the next waiter run builds.
  - Control L1-UF: on the rule-4 path (u_F set), the attempt does reach `spendFromView`, which settles member 1 `dead` by itself.
- **L2, the landed member.** Member 1 is on chain, but its in-lock poll timed out. The wait never confirms the row: it stays `pending` with a NULL hash.
  - Control L2-UF: with u_F set, rule 4's `resolveBlockedFamily` re-polls the family and confirms the row with member 1.
- **L3, the horizon.** I used one submitter instance and a clock moved past 2 h. The row rests: one wait marker, no 'failed' write, no build, no further re-queue, and the row stays (pending, NULL).

Consequence:
- In an idle wallet, a no-u_F wait always runs the full 2 h and then rests the row, whether member 1 died or landed. Recovery is left entirely to F-b's sweep and R6.
- If member 1 landed, the anchor sits in (pending, NULL) beside a confirmed transaction until F-b's R6 adopts it. If F-b's null-hash sweep reaches it first, it is marked 'failed' with "nothing was submitted" (the same class as gate 48's D1.1).
- This is the safe direction against round 1, which double-paid. No money is at risk.
- **W's nf3 does not demonstrate unblocking through the product.** It calls `view.markDead(m1)` directly, so the settle step the product never runs on this path is bypassed. W's claim "the wait cannot block for ever" holds only through the horizon (L3), or when other wallet traffic happens to settle the member (L1-busy).
- Suggested shape, for W to choose; it does not block this gate: run the same family re-poll and settle step on this path that rule 4 uses (`settleExpiredSpenders` plus `repollFamily`, or route it through `resolveBlockedFamily`) before waiting.

**Boot-grace = boot-arm-window edge: UNMEASURED in this gate.**
- `SWEEP_BOOT_GRACE_MS` lives in F-b's `reconciler.ts:131` (still 10 min at 9e7dfdcf). F-b's round 2 is not pushed and is not in scope.
- On the F0b side, G49-BOOT shows the no-u_F wait is not gated by the arm.
- The horizon (2 h from the first wait, which comes after member 1 was signed) is at least member 1's TTL (7200 slots), so member 1's fate can be decided by the time the row rests.
- **F-b's delta gate must test the interplay with L2.** A row rested by this wait, with a landed member, must be adopted by R6 and never swept 'failed'.

## Q3: F0b delta (excluding develop)
- **Exclusion verified independently.** I built a synthetic `merge-tree --write-tree` of develop dc8c210 into the round-1 head 31e79759. It conflicts only in the 2 Projects Documents pages. `git diff <synthetic> da080d3`, excluding the docs pages, is exactly 2 files, +233/-0:
  - `anchorSubmission.ts` +28
  - the new test file `ks1384-f0b-r2-no-shared-coin-waits.test.ts` +205
- The docs pages at the head are byte-equal to dc8c210's.
- The product change is exactly F1's fix:
  - the new error class
  - the in-lock check `fam && !fam.uF && members not dead`
  - the catch branch that waits like rule 4
- **Nothing beyond F1's fix and its tests. No finding.**

## Q4: F0c round 2
- `git diff <merge-tree(dfc0dd61, da080d3)> ab59f29`, excluding the docs pages, is **empty**. F0c's own code patch-id is `cd4e7c0cdf7e` at both round 1 and round 2, which matches W.
- Behaviour on the F0c head:
  - F1 is closed there too (Q1 table).
  - Gate 48's P3 (the real `withWalletLockWithin` times out and never runs late) passes, with its control.
  - P5 (a thread-mint has no TTL: gate 48's **N2 is still present**, as expected) passes.
  - `ks1384-f0c-thread-mint` gives 10/10.
- Its round-1 GO WITH NOTES stands unchanged.

## Q5: mutants on the F1 fix
Each was applied by a unique-anchor replace and restored by sha256 (`dab9f79e…`, verified each time). Logs are in `evidence/mut/`.

| Mutant | Killed by (mine) | W's nf cells |
|---|---|---|
| **Ma**: `!== 'dead'` → `=== 'live'` (a member the view does not know no longer blocks) | **KILLED** by G49-NOVIEW | **survives** nf1, nf2, nf3 |
| **Mb**: `mayLand.length > 0` → `> 1` | **KILLED** by P1b', G49-R, LOST, NOVIEW, BOOT, 2M, L1, L2, L3 | killed by nf1 |
| **Mc**: drop the `return` after the F1 catch branch (falls through to the guard-3 'failed' write) | **KILLED** by G49-R, NOVIEW, L2, L3 | killed by nf1 |
| **Md**: check only the first family member (`.slice(0,1)`) | **KILLED** by G49-2M | **survives** nf1, nf2, nf3 |
| W's "remove the wait" (`false && …`) | killed by 9 of my cells | killed by nf1 (reproduced) |
| W's "a dead member blocks too" (`filter(() => true)`) | killed by G49-2M and L1-busy | killed by nf3 (reproduced) |

**N2 (NOTE, test coverage).** W's cells do not pin the "not in the view" branch (Ma) or the multi-member case (Md). Both survive nf1 to nf3. G49-NOVIEW and G49-2M are the shapes that would pin them.

## COUNTS (instrument named; Node v26.8.1, not LTS)
- **Install:** `npm ci --ignore-scripts` at Blockchain/Dev, at the round-2 lock (1795 packages), then a build of @secuura/shared.

| Check | F0b da080d3 | F0c ab59f29 |
|---|---|---|
| Unit, anchoring (vitest, --maxWorkers=2) | 676/677 | 686/687 |
| tsc, service tsconfig | 0 errors | 0 errors |
| tsc over src plus tests | 0 errors | 0 errors |
| Real Postgres (9 files) | 113/113 | 113/113 |

- **Unit:** the only red is threadTokenMint at both heads ("Unsupported type", host-dependent, unchanged files; gate 48's same finding). This matches W.
- **tsc positive control:** a planted TS2322 gives rc 2.
- **Real Postgres setup:**
  - Container `gate49-pg`, postgres:15-alpine, with repo `docker/init` mounted, throwaway local passwords, and an app role `secuura_app`.
  - `scripts/run-migrations.sh` ran inside the container: applied=57, failed=0.
  - pg_stat_database showed 11008 tuple writes.
  - Bad-URL control: 8 failed files, 4 passed, 109 skipped.

## Spark shadow and calibration
**spark_gate.sh** (`spark_gate.sh repo 1854 da080d3 31e7975963a5 <nf test> --work scratchpad`):
- It printed "merge-base (empty) · diff 0 files", the same **instrument fault for a non-develop base** gate 48 recorded.
- Its BASE side therefore ran head product code and reported 3/3. The truth is RED 1/3 (nf1), which I measured by swapping the product file.
- The head side agrees: 3/3.
- I did not run it for F0c, which has no own delta and would hit the same fault.

**spark_review.py:** one request with the clean 2-file delta diff, and `--linear-env /dev/null` so no credentials file was read and no Linear call was made. It returned NO GO. Copies are in `evidence/spark/`.

| Spark finding | Gate 49 | Calibration |
|---|---|---|
| Major: the check blocks "legitimate" pass-1 families without u_F | A pass-1 first member always sets u_F (`recordMember`). A no-u_F family can only come from pass 2 or an injected submit, and blocking is the intended safe direction. Spark's own quote flag: false. | **False positive** |
| Major: the horizon only logs and returns, so the anchor can be stuck; the horizon is untested | Real direction: L3 confirms the rest and that the horizon is untested by W. But it is bounded, the same rest rule 4 has by design, and it hands off to F-b. It missed the core of N1 (no settle or poll on this path). | **Partial: right area, overstated severity** |
| Minor: nf1 "would pass without the fix" | It contradicts itself; nf1 is RED at the base. | **False** |
| Note: `markDead` may not exist on WalletView | It exists (walletView.ts:156). The real issue, that nf3 bypasses the product's settle step, was not stated. | **False, near a real point** |
| Note: the test passes on base | Produced by the instrument fault above. | **False (bad facts in)** |
| Verdict NO GO | GO WITH NOTES | **Disagrees** |

Score: 0 true, 1 partial, 4 false. It missed N1's root cause and N2.

## UNMEASURED
- Any chain, Blockfrost, wallet or box.
- Real CSL coin selection reaching a pass-2-only build: the probes override `pass1Inputs`, as gate 48's did.
- F-b's sweep and R6 acting on a row rested by this wait (the F-b delta gate).
- The boot-grace edge (F-b).
- The four platform suites, eslint, hook legs and preflight.
- Node 24 LTS: all runs are on Node 26.8.1, not LTS.
- Two processes.
- The product upsert in a live re-POST race.

## HOW
- **Clone:** `git clone --shared --no-checkout` from gate 48's clone into the non-existent `repo/`. Toplevel asserted equal before any fetch. Origin is Secuura/Distributed_Secuura, push URL `no_push_qa_gate`, with the Blockchain deploy key.
- **Fetch:** the refs/pull/{1838,1853,1854,1857}/head refs and develop.
- **Product swaps:** done with `git show <sha>:path > file` in my clone only, and restored by sha. Probes were copied into src only for their runs and kept in `evidence/probe/*.ran`.
- **Hygiene:** no git write verb was run in !CODING. W's container `s-w13-pg` was not touched.
- **Clean-up:** `gate49-pg` stopped and removed by name, the clone removed, and the scratchpad spark worktree dir removed.
