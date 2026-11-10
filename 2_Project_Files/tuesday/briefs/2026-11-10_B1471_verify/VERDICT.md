GATE B1471: GO WITH FINDINGS @ 79c2a09 on main dad9024

Tier 2 (docs sentences and two generated header lines). No security-shaped issue found. Own clone, push URL set invalid, never pushed. Node v24.22.2 (npm 11.19.1) for every node command; ci.yml node-version: 24 at lines 58 and 107.

## Findings
| # | Sev | Finding |
|---|---|---|
| 1 | Minor | Process: the kit said STOP where the source does not support the ticket words. The builder found the ticket reading wrong for the duplicate route, wrote the source's sentence in its own commit (cde7f77) and flagged it instead of stopping. Verified: the source's reading is the true one (below). The commit is separable if the ticket reading is wanted. The coordinator decides; the ticket text for clause 2 should be corrected, not the docs. |
| 2 | Minor | "A body sent to new-version is ignored" is a source reading only: no test sends a body to that route and dotnet is not on this machine, so it was not run. Source: the handler takes no body parameter and reads none (QuoteEndpoints.cs:455-492), and the only body readers in src/MpsCalc.Api are the Read<T> sites and the feedback and source-admin endpoints. |
| 3 | Minor | Open PR state was not read over HTTP (fence). Evidence instead: refs/pull/*/head on origin runs 1 to 174 only (174 refs), the kit reads 174 as merged, so no PR above 174 exists. No sibling-lane branch exists on origin yet; the sibling lane's two paths (scripts/deploy-from-ci.sh, scripts/tests/test_deploy_pre1.py) share nothing with this diff. |

No Blocker. No Major.

## Step results
1. Refs: git ls-remote of the branch = 79c2a09b0d1b026bac518178e0b19d6ce382ed54 = READY sha. Main read now = dad902441014bda81d4eed39dc9a6bcea1439989 (unchanged). merge-base = main, 3 commits ahead, 0 behind. Changed paths 3 of 3 allowed: docs/API.md, web/src/api/generated/SOURCE.txt, web/src/api/generated/schema.ts.
2. Merge: git merge-tree --write-tree main head is clean (rc 0); the resulting tree 16e53e3d equals the head tree, so merge = main plus the head blobs, and the web results at head are the results at merge.
3. CI: web job (npm ci offline from a copy of the builder's npm cache, lint, vitest, entra build + check-bundle) at main and head: lint rc 0 both; vitest 144 files, 1492 tests, 1492 passed, 0 failed both; set of (file, test, status) rows: lost 0, gained 0; contract-sync rows (3 in contract.sync.test.ts, 1 in contract.test.ts) passed at head; build + check-bundle rc 0 both, 8 files, 1108407 bytes, markers 0/57 both. Control: a planted failing test made vitest rc 1 (file moved out). Reproduction: running sync-contract.mjs with dad90244 in a head worktree left git status clean (head's generated files are exactly the script's output). openapi.snapshot.json blob 8d8b9207 at main = head = docs/api/openapi.json. Readers of docs/API.md: no test reads it (search over tests, tools, infra, scripts, web/src, web/scripts, .github: every hit is a comment or string, none opens the file). Readers of the generated files: web/src/api/contract.test.ts, contract.sync.test.ts, test/noBrowserPricing.ts and its test, all in the web job. Repo-wide hidden-character scan over 690 tracked text files: Cf characters 17 at main and 17 at head, bidi 6 and 6 (no change; control U+200B reads Cf).
4. Red without the fix: no test was added or changed; the docs reading is the red (below). The header: main (without the fix) is green too; the instrument is the reachability check below.
5. Closed lines at main: clause 1 (docs/DEMO.md S4 footer, lines 61 and 76) and clause 3 (docs/IMPORTER.md:143 points at the API Source lifecycle section) hold; main log shows the two commits that name the ticket (#47 and the importer pointer commit 94b24e8).
6. Probes (docs sentences at source, head tree): next section.
7. Scans on 14 added lines and 3 commit messages: names Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite: 0 each (underscore-aware, planted _by_<name>_ control fires 1 each); non-ASCII 0; Cf 0; secrets, uuids, tenant ids 0; B-numbers 0; hosts 0 (the only ".com" is the attribution address in the trailers); CodeQL pre-scan (new RegExp(, replace hand-escape, innerHTML, child_process) 0. Each of the 3 messages carries one Co-Authored-By: Claude Sonnet 5.5 trailer. Author identity is the repo's noreply identity, same as main.
8. Claims graded below.
9. Tier 2: no security-shaped issue; nothing found that needs tier 1.

## Sentence-by-sentence (source: head tree)
| Changed sentence (docs/API.md) | Code fact at source | Grade |
|---|---|---|
| Lifecycle events: a body with lifecycleEvents is refused 400 BAD_REQUEST as an unknown member on every quote route that reads a body | QuoteEndpoints.cs Read<T> sites at lines 72, 125, 222, 304, 370, 423, 511, 605, 658 (create, draft, calculate, submit, approve, reject, duplicate, outcome, outcome correction) all go through Read (line 1274) with ApiJson.cs:23 UnmappedMemberHandling.Disallow; BodyRefused answers 400 BAD_REQUEST. LifecycleEvents exists only on the response QuoteDto (Dtos.cs:189), on none of the request records | true |
| ...including the optional bodies of duplicate and approve | Duplicate (509-516) and Approve (366-370) read a body when ContentLength > 0 or a Transfer-Encoding is present, via Read<DuplicateRequest> / Read<ApproveRequest>; DuplicateRequest holds only QuoteRef, ApproveRequest only Comment, so lifecycleEvents is an unmapped member and is refused | true |
| POST new-version reads no body: a body sent to it, with lifecycleEvents or anything else, is ignored, not refused | NewVersion (460-492) is synchronous, its parameters are HttpContext, quoteId and three services, no body read, no body binding; no middleware reads a request body in src/MpsCalc.Api outside the Read<T> sites and the feedback and source-admin endpoints | true by source; not run (finding 2) |
| Rate limit: counted from stored items by submittedBy plus that caller's other requests still being written, each holding one place until it is stored or fails | FeedbackStore.cs Submit: Counted(...).Count + _reserved.Values.Count(r => r.User == candidate.SubmittedBy) >= limit; the reservation is taken under the lock and removed in the finally block on every path | true |
| Retry-After gives the seconds until one more item may be stored, worked out from stored items only, so while those requests are still being written it can be shorter than the real wait | FeedbackEndpoints.cs sets the header from store.RetryAfterSeconds; that method uses Counted (stored items only) and returns 1 when leave <= 0; in-flight reservations are not counted | true |
| Order: under the store's lock the idempotency check, the rate limit, and the taking of the key and of one place in the limit (held until stored or failed) | Submit loop: _byKey replay/KeyReused check, then _reserved wait, then the limit check, then _reserved[key] = mine, all inside lock (_lock) | true |
| the lock is then let go while the attachments are written into the item's own new folder, and taken again for the item file; attachments, then the item file last (the commit point) | Submit: the attachment writes (CreatePrivateDirectory, QuoteFileStore.Write per attachment) are outside any lock; the item file write and the _items / _byKey update are inside a second lock (_lock) and come last | true |

No new quoted user-facing string: the 8 backticked tokens in added lines (BAD_REQUEST, Idempotency-Key, lifecycleEvents, the approve, duplicate and new-version routes, Retry-After, submittedBy) each read at least 1 in docs/API.md at main (a planted absent token reads 0). No double-quoted or italic strings added. Unchanged neighbours were not graded (for example "Any refusal stores nothing", just before the order sentence).

## Header
SOURCE.txt line 2 and schema.ts line 2 differ from main in that one line each and nothing else; they name dad902441014bda81d4eed39dc9a6bcea1439989, reachable from origin/main (merge-base --is-ancestor passes). The old commit 7e9afb18... is not an object in a fresh clone of origin (cat-file fails).

## Builder claims
| Claim | Grade |
|---|---|
| Head 79c2a09b, 3 commits ahead, 0 behind, 3 allowed files | true |
| Base never moved | true (main still dad90244) |
| Header diff is exactly 2 files, 1 line each; snapshot byte-equal | true |
| vitest 1492/1492 at main and head, lost 0 gained 0 | true |
| build + check-bundle 1108407 bytes, markers 0/57 | true |
| No test reads docs/API.md | true |
| duplicate reads an optional body and refuses other members; approve same; new-version reads none | true |
| new-version "ignored" | not shown by a run (source reading only) |
| Retry-After can read 1 while the real wait is up to an hour (code, not docs) | true by source (RetryAfterSeconds ignores reservations); not touched, correct |
| Names, ASCII, secrets, B-number scans 0 | true |
| gitleaks canary then range | not shown (not re-run here; the regex scan above is 0) |
| 195 item 3 text not given | not checked by this gate (Jira is outside the fences); left unbuilt, consistent with the kit's default |
| gh api readback after push | not re-read (fence); git ls-remote equals the sha |

## NOT RUN
- dotnet build and test (dotnet is not on this machine): hosted CI is the proof for the dotnet job; no test there reads a changed file.
- python job and package job (no test reads a changed file; the python job needs bicep).
- Hosted CI, CodeQL, e2e, any hosted site. This repo has only ci.yml, so a merge triggers no deploy workflow.
- A body sent to new-version over a running server.
- Jira reads and open-PR state over HTTP (fences).
- Landing: only after the PR, hosted CI and CodeQL are green; head-pinned squash per landing.txt.
