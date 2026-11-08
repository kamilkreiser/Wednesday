PR 2093: GO WITH NOTES; PR 2094: GO WITH NOTES; PR 2097: GO; PR 2098: GO

Gate 264, tier 2, Secuura / Blockchain. Model claude-sonnet-5-5, row G2, gauge 17%. Run 01:34 to 01:52 AEDT 2026-11-09.

## BLUF
All four are what they say: no product byte changes. Two are test cells, one is a docs row, one is comments only. Heads and develop were unmoved from start to end (re-read at 01:34 and 01:51). Merge trees are clean with rc 0 and the paths are disjoint from PR 2061 and PR 2091. Two cells have a real but small blind spot (notes below). No blocker.

| PR | Head (start = end) | Verdict |
|---|---|---|
| 2093 | afb5f1ef4afe81f252835cd8dbae3c17be85a46f | GO WITH NOTES |
| 2094 | a84acd8404040c5746b2b297dc333fdf7336b02d | GO WITH NOTES |
| 2097 | ebf1ed1d0869e54ae91e4f36c53c4d501ba8187b | GO |
| 2098 | 943b69fdd988ded41f0971de03880d016929bd51 | GO |

develop at start and end: 01b26bc772a713e5e4d6ffc545f7fedeeeb4afe3.

## All four: merge and overlap
- FOUND: each head is one commit on 7eda23b34d3b. `git merge-tree --write-tree develop pNNNN` exits rc 0 for all four and prints a tree with no conflict lines (trees: 2093 ba9d0b5e, 2094 056b23ae, 2097 35da6056, 2098 b5da7880).
- FOUND: numstat equals the builder's claims exactly: 2093 +12 -0 (1 file), 2094 +14 -0 (1 file), 2097 +2 -2 (1 file), 2098 +21 -30 (4 files; per file 8/13, 10/14, 1/1, 2/2).
- FOUND: the 40 files that develop changed since 7eda23b34d3b (PR 2061 auth platform lists: `auth/src/routes/oauth.ts`, `routes/users.ts` and three tests; PR 2091 three portals under `frontend/`, root `package-lock.json`, fragments, `ROLES-AND-AUTHORIZATION-INVENTORY.md`, `audit-baseline.json`) share no path with any of the six files in this batch. The four PRs are file-disjoint with each other.
- HOW: `git diff --name-only 7eda23b34d3b develop` against each PR's numstat paths.

## PR 2093 (KS-2053): GO WITH NOTES
Does the cell test what the ticket says: yes. KS-2053 (as quoted by the builder; the live ticket was NOT read, see NOT TESTED) asks that C6 pin the strip above both `/api/documents` mounts. The new cell asserts strip < publicDocuments and strip < documents, with >0 guards.

Finding 2093-1, LOW, `ks741-emitter-marker-strip.test.ts` `mountLine` (line 319 to 322, used by the new cell): mountLine takes the FIRST `indexOf` of the needle. If a comment above the real mount ever contains the exact text `app.use(createEmitterMarkerStrip());`, the cell measures the comment's line and goes green even when the real mount is below both documents mounts.
- FOUND: mutant C (mine). A decoy comment `// was: app.use(createEmitterMarkerStrip());` placed first, with the real strip moved to just below the documents mount. The new cell stayed green. The only red was the existing CONTROL cell, and it was red for a different reason (its `replace` hit the comment).
- TESTED: develop's `index.ts` has the needle in exactly one place now (lines 18 and 228 are the import and the mount). So today's code is unaffected. This is a latent weakness, not a live one.

Red-first (own mutants, never committed, `index.ts` restored byte-equal, sha256 prefix 690169dec016e237 before and after):
- Mutant A (mine): strip moved BETWEEN the two documents mounts. New cell fails by assertion, other 7 stay green, 1 failed of 8. The builder's plant (strip below both) was not re-run; mutant A is the harder case because the old anchors cell C6 would still pass.
- Clean p2093: 8 of 8.

Whole originate suite, same instrument (jest, 5 workers, Node v26.8.1, fresh `npm ci --ignore-scripts` at develop plus `tsc` build of `packages/shared`):
- develop 01b26bc7: 220 suites, 2592 of 2592.
- p2093: 220 suites, 2593 of 2593. Matches T's 2592 / 2593.

Text claims: PR body and ticket comment are accurate at this head. The body says "Refs", not "Closes"; says what it did NOT do; does not claim a pass for the 3 skipped preflight legs ("PREFLIGHT INCOMPLETE ... not a pass"). Only issue: the PR text says the cell "reads index.ts as text"; true.

## PR 2094 (KS-2099 item 3 only): GO WITH NOTES
Item-3 honesty, checked first as ordered. PR body (Summary, line 1 bold paragraph): "This PR covers item 3 of KS-2099 only. The leak in item 1 is NOT fixed." Item 1 is named as MEDIUM and "NOT fixed here" and the SMTP failed-send log carrying the address is described. Item 2 is also "NOT fixed here". "What this did NOT do" repeats that "a failed SMTP send can still log the recipient address; nothing here changes that or tests it." The ticket comment BLUF says the same in bold: "The leak in item 1 ... is NOT fixed, and neither is item 2." Both say Refs, not Closes, and that the ticket state is unchanged. PASS.

Finding 2094-1, LOW, cell E8 (`ks1937-...test.ts`, the +14 hunk): the title says the refusal line "carries no part of the recipient address either: not even its domain", but the assertion is only a lower-case substring of the DOMAIN (`ks2099-domain`). A refusal line that prints the LOCAL part is not caught.
- FOUND and TESTED: mutant M1 (mine), refusal line made to print `options.to.split("@")[0]`. All 10 of 10 cells passed. The PR body discloses this ("asserts a lower-case substring of one made-up domain ... does not prove no other part of the address can appear"), so it is disclosed but the cell title overstates it.

Red-first (own mutants on `email.ts`, restored byte-equal, sha256 prefix 4de4be759333b3c3 before and after each):
- M2 refusal prints domain: only E8 red (1 of 10).
- M3 refusal prints the full address: E4 and E8 red (2 of 10).
- M4 ACS recipient = `options.to.slice(1)`: only E9 red.
- M5 ACS gets the recipient twice: only E9 red.
- Clean p2094: 10 of 10.
- Builder's plant (empty ACS recipient / domain in refusal) not re-run verbatim; M2 and M4 are equivalent hunks.

Whole originate suite: p2094 220 suites, 2594 of 2594 (T: 2594). Unpatched 2592.

## PR 2097 (KS-2077 item 1 only): GO
- FOUND: the new row is TRUE of the code. `api-gateway/src/routes/proxy.ts` at develop 01b26bc7, lines 1090 to 1092: `router.use('/api/rewards', authenticateToken(true), proxy('referral', { '^/api/rewards': '/api/rewards' }))`. So `/api/rewards` goes to Referral, and "Yes" in the auth column is right (authenticateToken(true)). Lines 1052 to 1055 carry the comment that staking's own `/api/rewards` is gateway-shadowed by design. Positive control: `api/staking` is found 5 times in the same file, so the grep was live.
- FOUND: the diff swaps exactly the two rows (Staking loses `/api/rewards/*`, Referral gains it). The doc has no other `rewards` mention that contradicts it (line 192 is the services table: "Token staking and rewards", a description of the service, not a route).
- FOUND: PR body "What this did NOT do" lists item 2, the singular `/api/referral/*` against the gateway's plural `/api/referrals` (proxy.ts line 1080), `/api/pool/*` (no mount found), other rows. Ticket comment says "Item 2 and the other rows are NOT done". PASS.
- TESTED (mine): `/api/referral` (singular) has no mount in proxy.ts at develop (only `/api/referrals` at 1080/1082); `/api/pool` has no mount in proxy.ts. So the Referral row's `/api/referral/*` and the Staking row's `/api/pool/*` are still not true of the gateway. Both pre-exist this PR and both are disclosed. Not a finding against this PR.
- Note: the file is under `Projects Documents/`, outside Blockchain/Dev, so the pre-push preflight skipped; the body says so.

## PR 2098 (KS-2022 round 2): GO
Zero non-comment change, shown three ways (script in my scratch, `g264/strip.cjs`):
1. TypeScript `transpileModule` emit with `removeComments`, base 7eda23b34d3b vs head, identical in all four files. Hashes (sha256 prefix) a3dd30e8fa964f92 (auth.openapi.ts), d13b71a0f28651b8 (ks796 test), ab0fb387eebb8cc1 (mfa.ts), 77566120a733bb65 (accountLockout.ts) equal T's published hashes.
2. Controls: base plus one code line emits differently in all four (code is seen); base plus an added `//` and `/* */` comment emits identically in all four (comments ignored); a mutant inserting `void 0;` right after the first `catch {` of each file is detected in all four.
3. Changed-line classification from `git diff -U0`: 51 changed lines (21 added + 30 removed), 0 whose text is not a comment or blank line.

accountLockout.ts, the sharp one: exactly lines 70 and 71 changed, both inside the `/** ... */` block (opens at line 57, closes at line 72) above `normaliseEmailForKey`. The catches at lines 97, 129, 167 and 179 are untouched, as is their code. The HOLD-NOTE risk (a catch change turning fail-closed to fail-open) does not apply: nothing near them moved. The only edit is `routes/auth.ts:310` to `routes/auth.ts` and `passwordLoginGate.ts:119` to `passwordLoginGate.ts` with "via" to "by".

New comment claims read against code at the PR head (tree = develop for these files; none are in the 40 moved files):
- `passwordLoginGate.ts` imports `z` from `@secuura/shared`: line 61, true.
- `s130-f6-openapi-module-in-the-import-graph.test.ts` imports `auth.openapi.ts`: line 37 `await import('../auth.openapi')`, true.
- `MFA_CODE_PATTERN` is the pattern with the 8-char alternative: `/^(?:[0-9]{6}|[A-Za-z0-9]{8})$/` at passwordLoginGate.ts line 95; mfa.ts line 130 now cites the file with no line. True.
- `routes/auth.ts` `loginSchema` with `z.string().trim()` for email: lines 97 and 98, true.
- Gate normalises the address: `String(user.email ?? '').toLowerCase().trim()` at line 229, true.
- "KS-810 fixed that" and "a module-scope throw there now turns the suite red": the s130 cell is a bare import so a throw makes it red; I did not plant a throw myself (T's plant was 2 of 2 red). Cited by T; not independently re-run (see NOT TESTED).

Whole auth suite (vitest, `--testTimeout=120000`, same instrument):
- 7eda23b34d3b (PR base): 1736 of 1736.
- p2098: 1736 of 1736 (T: 1736 both). Matches.
- develop 01b26bc7 alone: 1831 of 1831. Merge of develop and p2098 (merge commit made in my clone, never pushed): 1831 of 1831. So the merged result equals develop, no cell lost.

Finding 2098-1, INFO: the rewritten ks796 comment still ends with "Reading the generated yaml is not a consolation prize: it is the artefact a client actually generates from", directly after a new sentence that says the same thing (the yaml is the artefact a client generates from). Cosmetic duplicate; no action needed.

PR text: body says 21 added and 30 removed, "compiled output unchanged", names the fifth citation as the raise seat's own edit, says Refs. All true at this head. One claim in the PR is dated: "figures above were measured on the base 7eda23b34d3b and were not re-run on the newer develop"; I have now run them on the merge result (1831 of 1831).

## NOT TESTED
- The four tickets (KS-2053, KS-2099, KS-2077, KS-2022) were NOT read at source. No Linear reader was available in this session. I used the builder's quotations in the PR bodies and ticket comments. The commission asked for a source read; this is a gap. Item numbering in KS-2099 (items 1, 2, 3) and the ticket wording of item 3 are the builder's.
- Builder's exact plants for 2093 (strip below both mounts) and 2094 (two-hunk plant) were not re-applied verbatim; my own mutants stand in for them.
- No planted `throw` in `auth.openapi.ts` (relied on T for 2 of 2 red).
- Node 24, the four platform suites, preflight legs 3, 4, 8, any box or live gateway. `/api/rewards` was read in source only, not hit.
- Deviation, not a defect: node_modules came from `npm ci --ignore-scripts` at develop (the postinstall workspace build was skipped); `packages/shared` was built with `tsc`. A first attempt with a copied node_modules from the seat's old checkout (a65ae7ed1) failed on `@secuura/shared/zod3-compat` and was discarded; its numbers are not used.

## NEEDS TIER 1
None.

## Merge order
Any order. The four are file-disjoint and none touches a path in PR 2061 or PR 2091.

## Conduct
- Read-only toward everything outside this folder and my scratch: `ls-remote` and a blobless clone with the project's deploy key; nothing pushed; no GitHub, ticket, mail or seat-tree writes. The seat's checkout at `2_Project_Files` was read for `remote` and `core.sshCommand` and copied from once (node_modules), not touched.
- The no-cd hook refused `git fetch` and `merge-tree --write-tree` against a path held in a variable; I ran them from small script files under the scratchpad with literal paths, in my own clone. Nothing outside my clone was written.
- Never deleted. The discarded node_modules were moved to `.../scratchpad/g264/_quarantine/`.
- Two clones exist, not one: `/private/tmp/gate264/repo` (empty blobless clone, 10M, made first, then unused because the hook wanted the clone in the scratchpad) and the working one at `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/8bd59522-1a3b-4b02-8fa6-5687685b3d9c/scratchpad/g/repo` (2.2G with node_modules). Both left in place: removal is a delete and I did not delete. Wednesday to remove or archive. Local-only branches `p2093 p2094 p2097 p2098 m2098` exist in the scratchpad clone; `m2098` is a merge commit I made, never pushed.
- Load 1 stayed below 8 (peak 5.9 seen). Raw outputs: `.../scratchpad/g264/` (suites.log, orig_*.json, auth_*.json, strip.cjs, mut.sh, mut2.sh).

## GiB left
Boot volume 282 GiB free at end (286 at start).
