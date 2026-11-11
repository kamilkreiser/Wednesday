# Spark shadow of gate 307 (PR 2170, KS-1954), 2026-11-11 10:33 to 10:39

Method: blind (the Spark ran after verdict.md was written; its output was not read before). Tunnel: UP at 10:33 (`spark_status.py`: tunnel UP, queue 0, drainer not running; it showed `round LIVE` for another job). I did not start the tunnel or touch the box. Tool: spark_gate.sh (deterministic half) then spark_review.py, base ref `develop` = 0b55401ad5dc, head 52f482a83436. As in gate 306 the tool needs a clone whose `origin` serves `refs/pull/2170/head`: I made a scratch bare repo (`fake.git`: develop + the PR head pushed from my scratch clone) and cloned it as `sparkrepo` (no network, nothing in !CODING written). `--node-modules` = my copied Dev/node_modules. Inputs pre-fetched: PR body = the commit message (the GitHub PR body was NOT readable, no auth); ticket text = NOT AVAILABLE (Linear not read; my file began with a `MISSING:` line plus Wednesday's brief row 9 scope text, and the tool, by design, treated the ticket as MISSING and told the Spark so). No .env was passed.

Tool results
- spark_gate.sh: exit 0. Head: 1 file, 5 passed 0 failed. Base product code with the PR's test: 2 passed 3 failed. Equals mine exactly (R1 R2 R3 red, C1 C2 green). The gate 305 tool gap (no built packages/shared/dist) did NOT hit this suite (the ks1954 test does not import it).
- spark_review.py: exit 0, valid JSON, one attempt, no repetition, 43.1 s, prompt 14,443 tokens (1,536 cached), completion 943. It WAITED about 5.5 minutes (10:33:38 to about 10:39) on `spark/state/round.lock`, held by another round (ks_2021 o133 auth hibp, started 10:35:42): no action of mine; the tool's queue discipline worked.

## Spark shadow PR 2170: verdict NO GO (mine GO WITH NOTES: NOT a match, the Spark is two steps more cautious); recall 1.5/5 of G307-2170-1..5 (-3 found, -4 partly, -1 -2 -5 missed); FP 2 of 5 (one at severity)

Facts match (head 5/0; base 2 pass 3 fail). The verdict does not.

| id | Spark | note |
|---|---|---|
| G307-2170-1 (silent skip: no log, no counter, the admin route answers the same text) | MISSED | needs reading the route response; outside the diff |
| G307-2170-2 (comment names one of three causes; sweep cannot tell a failed read from no workflow) | MISSED | |
| G307-2170-3 (the flagged no-workflow behaviour change is unpinned; mutants break/skip-missing-step survive) | FOUND (Spark 1, in the test_or_reason: "No test covers a step whose workflow is genuinely absent") | the mutants need a run; the gap itself is found |
| G307-2170-4 (Q4: no creator, no fixture, still approvable, no strand path) | PARTLY | the Spark asserts the OPPOSITE conclusion (see FP 1): it read the risk from the body and did not search the creator or the approve path |
| G307-2170-5 (RED in permanent cell names) | MISSED | cosmetic |

Spark findings at source
1. Major, "any step whose workflow cannot be found is left pending forever; nothing repairs it; blast radius widened": the QUOTE is true (it restates the PR's own disclosed behaviour change) but the severity and the NO GO are not supported at source. Measured by me: nothing in the tree creates a no-workflow step (createWorkflowInstance has no caller), no fixture builds one, `processApproval` still approves a step with no workflow, and the stored `timed_out` it replaces was never read by anything and made the step UNapprovable. FP at Major (a disclosed, measured-as-unmeasured behaviour change presented as a defect); the half about the missing cell is TRUE and is my G307-2170-3.
2. Minor, "the fake does not pin the SQL or the due_at filter": TRUE and low value (the cells pin the sweep's decision, the harness is a model of the tables; a dropped filter is a different ticket). Not wrong, not mine.
3. Minor, "the fake returns one hard-coded workflow regardless of step_id, so a wrong-workflow match would go uncaught": TRUE of the fake and IRRELEVANT to this PR (`findWorkflowByStepId` is not changed). FP (padding).
4. Note, "ticket text not provided": TRUE, my doing (Linear not readable); correct handling by the tool.
5. Note, "the description does not quantify or propose a repair": TRUE, restates the body; asking a PR to design a repair is outside the ticket. Padding.

## What the tool or checklist should change
1. Verdict rule: a behaviour change that the PR DISCLOSES and says is unmeasured is a Note unless the review shows a path (from source) that makes it bite. The Spark made a Major and a NO GO out of the body's own disclosure. Instruction for REVIEW_CHECKLIST.md: "a risk the PR body already names is not a Major by itself; name the call path that creates the affected state, or leave it a Note."
2. Context: for a service-level behaviour change the prompt should carry (a) the callers/creators of the affected state (a git grep for the table and the creating method) and (b) the paths that read the state after the change (here processApproval and getWorkflowStatus). Without them the Spark cannot tell a stranded step from a harmless one. Same recommendation family as gate 306 item 2 (callers, spec, docs).
3. A `MISSING:` ticket line makes the tool tell the Spark acceptance was not assessed; that worked. If the ticket cannot be fetched the gate should still pass the brief's scope sentence as the ticket text without a `MISSING:` prefix, labelled as a secondary source, so the Spark can at least check scope.
4. The fake-bare recipe (develop + `refs/pull/<n>/head`) was needed again; a documented `--origin-from-local` would remove a manual step per run (gate 306 item 4 stands).
5. The Spark is busy with the overnight queue: a shadow review can wait minutes on round.lock. Worth the gate noting the wait in the row (done here) rather than treating it as a hang.

Conduct: nothing written under !CODING (every read there was ls-remote/show/diff/log/grep/cat-file/rev-parse/merge-base/for-each-ref); no push, post, comment or mail; no .env opened; no secret printed. The tunnel was only observed. Scratchpad total about 3.6 GB (repo2 1.8G with copied node_modules and built shared dist, repo 354M abandoned first clone, fake.git 275M, spark_work_2170 354M, sparkrepo 1.1M). Pins at the end of the shadow (10:39:46): develop 0b55401ad5dc and PR 2170 head 52f482a83436, both unmoved.
