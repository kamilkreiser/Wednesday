## QA GATE - TIER 2, round 1: GO

**PR:** Secuura/Distributed_Secuura #1824, KS-1733 item 2 (governance, Seat S 8th)
**Head:** `310d26d1e2fcbe13c605240cc380baf04bbb4317`. ls-remote of refs/pull/1824/head matched the claim at the start and at the end.
**Develop:** origin `530f091120d5da749edf972e8e0089e44cfc5589`; merge-base `a786e06e6f6e`.
**Gate:** QA gate 28. Findings only. Nothing fixed, commented, pushed, merged or deployed.

### Counts
1. **Diff:** 3 files, +55/-0 (three-dot stat vs origin/develop): ks1722 test 16/0, flow doc 20/0, cheat sheet 19/0. Product bytes: zero (the diff outside `__tests__` and the two docs is empty). Test bytes: the 16 changed lines (sorted +/-) of the head's test diff equal the canonical Spark `patch.diff`'s 16, line for line (diff rc 0).
2. **The pin is real.** Tamper = the brief's: `, 'i'` on the RegExp at `governance.types.ts` line 353 (anchor count 1, the line printed after planting). Governance jest, the ks1722 file only, 48 cells:
   - Untouched tip: 48 / 48 green.
   - Tampered: 45 pass / 3 FAIL. The 3 reds are exactly R8 (upper-case status, capitalised status, one capitalised part in a list). The two R9 controls (category enum exact-case) and the other 43 cells stay green.
   - Restored by content: sha256 `34d8fe7c8a80...` before and after, equal; `git status` clean.
3. **The claim vs the route.** `GET /api/governance/proposals` (routes, line 141) parses `req.query` with `ProposalListQuerySchema`; `status` is `z.string().regex(PROPOSAL_STATUS_LIST_PATTERN)`, a case-sensitive pattern over the lower-case `PROPOSAL_STATUSES`; a failure answers 400 BAD_REQUEST before `getProposals`. `category` is a `z.enum` of lower-case values, so exact-case as well. So `ACTIVE`, `Active` and `active,Queued` are refused today and never reach SQL. This is the real behaviour, not a bug pinned: the service filters `status = ANY($n)` / `category = $n` on `TEXT` columns (docker/init/04-sprint2-service-tables.sql), a case-sensitive comparison in Postgres, so a capitalised value would match no row. Refusing is therefore consistent with what the data does; the cells pin the policy as the author says (a case-insensitive check turns R8 red on purpose). Not a claim that case sensitivity is the right product choice.
4. **Governance service suite (jest 29, my clone):** head 6 files, 167 / 167, 0 fail, 0 pending. Develop 530f091120d5: 6 files, 162 / 162, 0 fail. Delta +5 cells, all the new ones; no red on either side, so nothing pre-existing to show. Matches the author's 162 / 167.
5. **Predicted merge** (`merge-tree --write-tree`, origin/develop + pr1824): rc 1, CONFLICT in exactly two files, the two Projects Documents html (flow doc and cheat sheet). The test file merges clean. As expected; the merging seat rebuilds the docs (flow doc section renumber: develop highest section is the #1823 one, the PR adds 123 per the author).
6. **spark_gate** (run first, `--node-modules` = my clone's `Blockchain/Dev/node_modules`, the hoisted root): rc 0. Facts: head `310d26d1` tip, diff {3 files, +55, -0}; targeted on HEAD 48 passed / 0 failed (1 file); targeted on BASE product code 48 / 0. Not 0/0, so it measured. The BASE column is the same 48 / 0 because the PR adds no product change (test-only), so the base run is not a red-first signal here; the red-first evidence is my own tamper in point 2.

### TESTED / NOT TESTED / HOW
**TESTED:** head pin at both ends; diff scope and product-bytes-zero; patch equality; tamper red/green with sha256 restore; the route and its schema read against the claim; DB column type; governance suite at head and develop; merge-tree; spark_gate.
**NOT TESTED:** the two html docs (html_docs_check, the section-123 numbering, the cited lines); tsc and eslint; the governance integration files and the four platform suites; a running stack; the pre-push hook legs; Node 24 (ran on this machine's Node); a browser render; the author's PR body / Linear comment text; whether any external client sends a capitalised status (the author did not measure it either).
**HOW:** `git clone --shared` of the checkout into the non-existent `.../scratchpad/gate28/clone`; `rev-parse --show-toplevel` asserted equal before any fetch. The clone's origin URL was reset from the checkout path to the GitHub URL and the checkout's `core.sshCommand` copied into the clone's config; fetched `refs/pull/1824/head` and `develop` only. node_modules: a real directory of symlinks to the checkout's hoisted entries, with `@secuura/*` re-linked inside the clone (relative targets), `packages/shared` built in the clone first (tsc rc 0). TMPDIR=/tmp/g28. Counts read from jest `--json` files; copies beside this file (`tamper.json`, `green_tip.json`, `suite_head.json`, `suite_dev.json`, `spark_facts.json`).

### Instrument errors
- **I1.** The shared clone's `origin` points at the local checkout, so `fetch origin refs/pull/1824/head` failed ("couldn't find remote ref"). I set the clone's origin to the GitHub URL and re-fetched. My setup, not the tool's.
- **I2.** The `pretooluse_no_cd.sh` hook refused `git -C $VAR <write verb>` (fetch, checkout, merge-tree) pointed at my own scratchpad clone, and refused a whole compound command that contained one; each was re-issued with a literal scratchpad path as its own call. Nothing ran under the refused call.
- **I3.** spark_gate ran clean first time with the key in the clone's config; no harness error. Its BASE-product column is uninformative for a test-only PR (see point 6).

### FIX-BEFORE-MERGE
(none)

Notes (non-blocking): at merge the two docs need rebuilding (the conflict above; flow doc section number depends on what develop holds at that moment). The pinned policy (lower-case only) is a decision, not a proof it is right; a later ticket that makes the filter case-insensitive must change R8 on purpose.
