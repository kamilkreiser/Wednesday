--- comment 5834392886 by linear[bot] at 2026-09-25T14:49:58Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1297/pre-push-fixture-guard-three-gaps-the-new-six-cell-suite-does-not">KS-1297 pre-push fixture guard: three gaps the new six-cell suite does not close (unanchored abort line, worktree write, exempt errexit)</a></summary>
<p>

## BLUF

PR **#1218** (KS-897 + KS-896, merged `1609ecbf61e1`) made the pre-push base suite abort with rc 2 and a named line when a fixture build step fails, and added a six-cell guard that runs on every push. **Three gaps in that guard were measured by the gate and left open**, all non-blocking, all in the same suite and the same fix pass — so they are items of one ticket rather than three tickets, per Kam's 2026-09-07 rule that the unit is the test pass.

## The three items

1. **NB-1218-a — GUARD-UNANCHORED.** The guard counts the abort line **unanchored**, so an abort line that is *prefixed* by anything still satisfies it. This is the same shape the fleet's own STOP predicate had to be sharpened for on 2026-09-25 (line-start `^FIXTURE BUILD FAILED`, superseding the loose substring). **A guard that matches mid-line can be satisfied by output it did not cause.**
2. **NB-1218-b — FIXTURE-GITENV-WORKTREE.** The fixture can no longer write to the caller's repository *by the path the gate tested*, but a **worktree-only write** to the caller's repo is not pinned by any cell. The fix closed the shape that was found, not the class.
3. **NB-1218-c — FIXTURE-ERREXIT-EXEMPT.** `errexit` suspended **at a call site** is not pinned. This matters because the original KS-897 defect was exactly an errexit assumption that did not hold — `( … ) || { exit 2; }` tests only the subshell's last command.

## Why it is worth a ticket rather than a note

The guard runs on **every push by every author** and costs about ten seconds. Its value is entirely in what it would catch; each item above is a way the property it asserts can be false while it stays green. Item 1 in particular makes the guard satisfiable by a line it did not produce.

## NOT claimed

None of these is a live failure. The suite passes 6/0 at the merged head, and the shipped behaviour is an improvement on what preceded it. These are **coverage** gaps in a new guard, measured by the gate at the same time it approved the change.

## Board search before filing (team Secuura-PK, 1,286 issues incl. archived, 3,631 comments, literal match on titles, descriptions and comments)

* `pre_push_hook_base_fixture_guard` -> **0**. `fixture-abort` -> **0**. `FIXTUREABORT` -> **0**. So nothing on the board names this suite.
* `GIT_WORK_TREE` -> 6 total / 2 open (**KS-1034**, KS-485). **KS-1034 read in full and is NOT a duplicate** — it is `check-stack-safety.sh` resolving the wrong repo root under a hook's `GIT_DIR`.
* `errexit` -> 5 total / 2 open (**KS-1139**, KS-485). **KS-1139 read in full and is NOT a duplicate** — it is bare `((X++))` under `set -e` at ten sites in two host scripts.
* Controls that fire: `KS-1229` -> 5; `consumeResetToken` -> 3. A nonsense control (`zzz-nonexistent-zzz`) -> **0**. So the search discriminates in both directions.

`Refs KS-897`, `Refs KS-896`; closes neither.

## Provenance

Tier-2c QA gate `2026-09-25-batch1218-t2c` (report sha256 `70dc4c987f04…`), raised as a **non-blocking** finding and recorded at the merge. Filed on the coordinator's instruction after the batch landed; it did not hold the merge.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1297-guardgaps-anchor-the-abort-counts-cover-the-worktree-pin-bare-051cc85c340e">Review in Linear</a></p>

