# Gate 252 verdict, tier 2 batch round 1 (Secuura/Blockchain)

Develop a65ae7ed1d60 (re-pin). Heads re-read with ls-remote at clone (20:3x) and at the end (20:41 AEDT): all four unchanged, no verdict voided.

| PR | Ticket | Head | Verdict |
|---|---|---|---|
| 2088 | KS-1797 | 0f0933afd24b | GO WITH NOTES |
| 2089 | KS-1493 | 3796e4b90c6a | GO |
| 2090 | KS-692 | 4c4f696f7699 | GO |

NEEDS TIER 1 stop line: not triggered for any PR. No product line in any diff; no push-path guard touched.

## Shared path / merge (item 3)
Merge tree: `git merge-tree` is a write verb and the session hook refused it. Substitute (READ ONLY): for each PR, files changed on develop a65ae7ed1d60 vs the PR's base 9cdb9321aa8a = 70; overlap with each PR's own paths = 0 for all three (positive control: the 70-file list is non-empty and printed). So each applies cleanly by construction. The three PRs touch six distinct paths and share none. Any order.

## PR 2088 (KS-1797) GO WITH NOTES
Diff read whole: 1 test file +35, 1 fragment line. Does what it says; no product line.
- F1 (Low, doc): cheat fragment `Projects Documents/fragments/cheat/KS-1797-post-authorize-refuses-an-array-state-or-code-challenge.html` line 4 still says "12 cells in one new file; 8 of 8 mutants killed" while the same PR takes the file to 16 cells (`it(` count 12 -> 16, FOUND by grep on pr2088~1 and pr2088 with the PIN count as positive control). The sentence directly above it was edited in this PR. The flow fragment's "12 cells" is a dated measurement and is fine. READ ONLY.
- F2 (Info): the READY lists "null removed from P8 stays green" as an uncounted tamper. It stays green against the product, true, but null is load-bearing for a mutant: a state-only `!= null` mutant is admitted only by P8's null and nothing else. TESTED on a model (below): with null in P8 that mutant is RED, without it green. So the tamper shows P8 needs its null, not that it is redundant. No action needed beyond knowing it.
- Guard claim, READ ONLY then confirmed on source: `routes/oauth.ts:663` is `(state !== undefined && typeof state !== 'string') || (code_challenge !== undefined && typeof code_challenge !== 'string')`, so null, 0, false, numbers, booleans are all refused on both fields. The new fragment sentence "present and not a string ... the guard refuses every non-string, on both fields" is true. The cells pin existing behaviour and are green on develop by design; they do not mislead.
- TESTED (MODEL, not the suite): the real predicate and the READY's mutants G3 `!= null`, G4 `typeof === 'object'`, truthiness, run over the P8 to P11 value lists in plain node (`evidence_predicate_model.mjs` / `.out`). Real: all four green. G4: all four red. G3 and truthiness: P8 and P10 red, P9 and P11 green. This matches the READY's kill claims (G4 by the new cells, G3 by 2, truthiness by 2). Control: the real predicate admits 'x', '' and undefined.
- NOT TESTED: the real vitest file. I archived pr2088 auth and shared into the scratchpad and tried; the read-only checkout's installed node_modules predate the repo's zod 4 / zod3-compat (`z.config is not a function`, tsc errors in zod3-compat.ts), and `npm ci` needs network, which the commission forbids. So no real red reproduction and no planted defect in the actual file: NOT RUN, blocker named. Also not run: whole auth suite, tsc, eslint, docs-fragments check, deny-path with these values (guard sits before the split, READ ONLY), Node 24.

## PR 2089 (KS-1493) GO
Diff read whole: one hunk, lines 13 to 17, inside the leading `/** */` header; no code line touched (hunk bounds from `git diff -U6`, READ ONLY).
- The comment is true. N2-C1 (file lines ~108-111): first two versioned calls not 429, third equals `[429, 'RATE_LIMIT_EXCEEDED', 'Too many verification requests, slow down.']`, which is the armed-limiter proof in this boot; the new header gives it to N2-C1. N2-C2 asserts only that all six unversioned `code` values are null. "Pins no more than that" and "does not prove the limiter is armed" are both accurate.
- F3 (Info): N2-C2 is weaker than its `it()` title ("real redirects"): a 307 has no JSON body, so `code` is null regardless. The new header is honest about this ("adds little beyond PIN"); the title string was not changed and is outside this PR.
- Not run: the file (same blocker as above, plus it boots the whole gateway). Byte-identity outside the comment is the seat's claim (sha256) and I confirmed it by reading the diff, not by hashing.

## PR 2090 (KS-692) GO
Diff read whole: two lines, one in each of cheat and flow fragments; no code.
- Sentence 1 "reads 400 ('credentialId is required and must be a string'), not 403": true of the code. `vc-issuer/src/routes/status.ts:305` (revoke) and `:366` (unrevoke) throw that 400 (line 265 is allocate, the READY's list of 265/305/366 is right but 265 is not a row of the test). The router gate (lines ~77-84) lets a signed-in POST to `/:id/revoke|unrevoke` through to the handler (`CREATOR_BOUND_WRITE`), so a tenant ISSUER_ADMIN reaches the shape check before `refuseUnlessCallerMayChange` (404). Bodies in `systemTest/schemathesis/tests/support/status_list_authz.py:50-51` are `{index, reason}` and `{index}`: no credentialId. `is_role_refusal` returns `status == 403` only, so the test stays red. All READ ONLY at origin/develop a65ae7ed1d60.
- Sentence 2 (flow fragment): "its request bodies carry no credentialId, so the shape check answers before the ownership gate does" true as above.
- F4 (Info, wording): "stays red either way" is true for 404 vs 400 against this change; read alone it could suggest the test was red before KS-692 step 2 too, when the platform-role gate gave it a 403 and it was green. Not wrong, slightly ambiguous.
- Stale-text sweep: `grep -i "reads 404|404, not 403|not 403"` over fragments on pr2090 finds only the two edited lines plus an unrelated legacy fragment (0006-oauth-app-scopes); no other fragment keeps the old claim.
- NOT TESTED: the 400 through a running stack or the gateway (READY says the same; gateway could answer first). Docs-fragments check not run. The pre-push hook not running preflight on a docs-only push is as designed; nothing here is a Blockchain/Dev path.

## Own conduct
- Fresh clone `/private/tmp/g252`: blobless (`--filter=blob:none`), sparse-less, no checkout, 193 MB at the end, left in place (no rm). Repo-local `core.sshCommand` set in that clone for blob fetches, same deploy key as the project.
- The session hook refused `git merge-tree` and `git checkout` in the clone (write verbs outside Wednesday's folder). I did not work around it with --git-dir tricks; I used `git archive` (reads) into the scratchpad for the PR 2088 attempt and substituted path-overlap for the merge tree.
- Scratch: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/02fe044e-b48b-4f7e-8397-447f163806d4/scratchpad/w88` (archive extract with symlinked node_modules; a tsc build of shared wrote dist there only). Nothing written to the project checkout, nothing pushed, no comment, no ticket touched, no mail, no cd, no rm.
- No planted defect was run against a real test file (see blocker). The only plant-equivalent is the model run in `evidence_predicate_model.out`.
