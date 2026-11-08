PR 2113: GO WITH NOTES

Gate 276, tier 2, Secuura/Blockchain. Findings only; nothing pushed, posted or mailed. Clone: /private/tmp/g276/r (538 MB on the boot volume, left in place, no rm per QA rule).

## Pins (read at start 10:06 and end 10:11, via ls-remote)
- develop 4e529633d0a19a3efe626adfe05684fbd964e595: did NOT move.
- PR 2113 head 521ffe0f777fe3f290e9656b637491d9a82f38fc (one commit, parent a1bfe7a7df25): did NOT move.
- df DevMASTER 108 GiB at start and at end. load1 3.6 at start, 4.8 at end (under 8).

## Q1 Scope
Files (diff-tree): the new test, services/transfer/src/index.ts, and the two KS-2055 fragments (cheat, flow). Nothing else. The product hunk:

    +  const previousStatus = transfer.status; // KS-2055: captured before the assignment below ...
       transfer.status = 'cancelled';
    -    fromStatus: transfer.status,
    +    fromStatus: previousStatus,

One sentence: the cancel route's history entry now records the status the transfer was cancelled from (pending_approval or draft) instead of 'cancelled'. Stop line checked: the hunk touches nothing before it (requireCaller, refuseUnlessEntitled, the draft/pending_approval allow-list, the status assignment, notification, save, response all unchanged). Who may cancel, what is authorised, and what is deleted or overwritten are unchanged. Not NEEDS TIER 1.

## Q2 Does it do half 1; overstated words
Yes. Half 1 is the from-status in the cancel history entry. The fragments and READY say plainly it is half, the reason bound is undecided, KS-2055 stays open. I found no claim of half 2 in the fragments, the READY or the test names. NOT READ: PR body and ticket comment 872bc167 and the ticket body (no gh auth in this seat, no Linear read verb tried); their words are untested.

## Q3 Red-first and suite
- Develop 4e529633d0a1 alone: services/transfer 16 files, 460 passed, 0 failed.
- Develop plus ONLY the new test file: R1 and R2 FAIL by assertion ("expected 'cancelled' to be 'pending_approval'"); C1, C2, C3 pass (2 failed, 3 passed).
- Merge of the head on develop (merge-tree and a real merge, rc 0): 17 files, 465 passed, 0 failed. Matches the seat's 460 -> 465.
- Own mutants, each applied to index.ts after the merge, restored by sha (hash-object equals blob 881816d848e2 afterwards, git status clean of index.ts):
  M1 fromStatus: previousStatus -> fromStatus: 'draft': R1 and R2 red (2 failed, 3 passed).
  M2 previousStatus = 'cancelled' (the original bug re-introduced by value): R1 and R2 red.
- tsc --noEmit -p services/transfer on the merged tree: rc 0, no output.
- Instrument note: I used the s-t17-d1 worktree's Dev/node_modules (zod 4.6.7) via symlink, read-only; the main checkout's node_modules has zod 3.25 and gave 21 spurious failures on develop (not the PR's; my environment). Node v26.8.1.

## Q4 Merge tree and shared paths
- merge-tree develop 4e529633d0a1 + head: rc 0, tree 3c76d38c1da4.
- PR 2110 (touches only the ks2081 test file) and PR 2112 (transferAccess.ts plus two KS-2120 fragments): zero shared paths with 2113; merge-tree of (develop+2113) with each of them rc 0. Controls: both really fetched and their path lists printed non-empty.
- Other open PRs: NOT enumerated (no gh auth; the seat's gatetest says none of 47 touch the 4 paths, unverified by me).

## Q5 Consumers of the history entry's fromStatus
Enumerated by git grep of the whole tree at develop for fromStatus, statusHistory, status_history and the history route (all file types):
- Writer sites: transfer index.ts lines 573 (create, null), 754/831 (reject/approve paths, literals), 886, 902, 952 (this one).
- Sole reader: GET /api/transfers/:id/history (index.ts ~975) returns the array as stored; plus the in-memory/PG persistence (JSONB status_history, written and read back unchanged; DDL in docker/init and migrations has no logic on the value).
- Tests reading the route: transfer.test.ts (only checks the route), ks2038 (reads toStatus and changedBy, never fromStatus), ks2081 (status 200 only), schemathesis test_get_by_id_object_authorization (peer refusal only). None asserts fromStatus on a cancel entry; none breaks (full suite 465 green).
- OpenAPI (transfer.openapi.ts, secuura-api.yaml): fromStatus is a nullable string with example text; no enum or constraint the new value could violate.
- Billing's fromStatus (chargeable-events.ts, svs-types.ts) is certification status, unrelated.
- No frontend, export or admin view reads the field in the tree. Entries already stored keep the old wrong value (change does not rewrite them; stated in the READY and fragments). Not measurable here: consumers outside this repo.

## Q6 Fragments
docs-fragments.mjs check on the merged tree: rc 0, "lint clean, render passes html_docs_check". It prints 2 ADVISORY lines (flow and cheat committed-vs-render differences at a range inside the rendered block); the identical count of 2 appears on develop without the PR, so not caused by it. Words true at the head: the bug description, the +2 -1 and +134 figures, 460 -> 465, 2 of 5 red by assertion all match what I measured.

## Findings
- G276-1 (low, wording): the cheat fragment says "Product code changes, by one line" and the flow fragment says "The product change is two lines"; the diff is +2 -1 (one added line, one changed line, plus the comment on the added line). Harmless but the two fragments disagree.
- G276-2 (info, coverage): no cell cancels a draft transfer. The route allows draft, but create always sets pending_approval (index.ts 572), so draft appears unreachable in-process; a mutant hard-coding 'pending_approval' would pass all five cells. The fix itself (read the live status) is correct for both.
- G276-3 (info, test): R1 does not assert the cancel call returned 200 (R2 does); it still cannot pass vacuously, because without a successful cancel the last entry has fromStatus null and the assertion fails.

## NOT TESTED
PR body and ticket comment 872bc167 text; the ticket body; other open PRs beyond 2110 and 2112; a real PG database; the pre-push hook legs; Node 24; anything outside the in-process server; consumers outside this repo.

## Conduct
Read-only against !CODING (ls-remote, fetch only inside /private/tmp/g276/r). My clone has local scratch merge and mutant edits, restored. Two moved-aside symlinks sit in /private/tmp/g276 (unused-link, unused-link2); nothing deleted.

PR 2113: GO WITH NOTES
