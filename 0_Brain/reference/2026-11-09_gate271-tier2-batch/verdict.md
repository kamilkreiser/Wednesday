PR 2103: GO; PR 2104: NEEDS TIER 1; PR 2105: GO WITH NOTES; PR 2106: GO WITH NOTES

# Gate 271, tier 2 batch, round 1: findings only (nothing posted, mailed, fixed, pushed)

## Pins (ls-remote at start 06:01 and end 06:10): NONE MOVED
develop 6c9a593df4ab; 2103 head 6de27bab34cd; 2104 head df9493550372; 2105 head 5f1685420cc6; 2106 head a8d19bf3918e. All verdicts stand on these heads.

## Instrument and its limits (read before trusting any ratio)
- Clone: /private/tmp/g271/repo (boot volume, full tree, 538 MB incl. my symlinks). NOT deleted (QA no-rm); also left: /private/tmp/g271/out, run.sh, strip.cjs, ei.orig, /private/tmp/g271/_quarantine/zz-g271-scratch.test.ts (my scratch cell, moved not deleted).
- Deps are the project checkout's node_modules, symlinked in read-only. They are STALE against develop (zod: `z.config is not a function`), so 23 test FILES fail to load on develop in my instrument (729 tests vs the seats' 1597). The red SET is therefore compared like for like (my develop vs my head), NOT against the seats' absolute counts. In my instrument the one failing TEST is the same one the seats name: wallet-signature `verifyMessageSignature (CIP-8/CIP-30) > accepts a valid wallet signature over the message`. I did not reproduce the seats' 1597/1602/1601 figures.
- Node v26.8.1, vitest 4.1.10 (seats: 4.1.12). No network but git fetch/ls-remote; no box; no docker.
- Ledger of my own slips: (1) a first full-suite run was on a sparse tree (invalid, discarded); (2) a second loop's `git checkout` failed silently (no ssh env for the promisor fetch) so three runs were on develop contents; I caught it from the unchanged test counts and redid p2104/p2105 with the env set (counts then moved +5/+4). Results below are only from the redone runs. (3) My first strip-compare "planted code" control was a false control (landed inside a header comment: differs=false); I fixed it (append at EOF) and report only the fixed run.
- Live PR bodies and Linear comments were NOT read (no gh, no Linear: network limit). I read the seats' local final texts (drafts/pr_body_row*.md, pr_body_FINAL.md, comment_row*_final.md) and the comment-record JSONs. "True at the head" below means: those texts against the code at the head. Whether the live text equals the local draft is NOT tested.

---------------------------------------------------------------------

## PR 2103 (KS-2107), head 6de27bab34cd: GO

BLUF: comments only; every changed line in documents.ts is inside a comment; the new words are true of the code.

FOUND
- 6 hunks / 5 comments in routes/documents.ts (+13/-7): emitLifecycleAnchor doc block 1390-1397, custody-transfer 2503-2506, share 2924-2925, revoke 3027-3028, lifecycle-events emitter 3154-3158. Plus the fragment pair (+18/+11).

TESTED / HOW
- Q1 comment-only: strip-and-compare. ts.transpileModule with removeComments:true on develop vs head documents.ts: emit 101,975 B both, sha 893bee61015bc5bd on both, IDENTICAL (my TypeScript version, so the byte count differs from the seat's 105,416; the property is the same). Controls, all with the instrument that produced the zero: a code line appended at EOF -> emit differs (true); a comment line planted -> emit identical (true); one byte planted inside the first string literal after the first import/export -> emit differs (true). Raw source sha 99b707ff1b59e491 -> 7130358cf3edd976, equal to the seat's.
- Also read all hunks by `git diff -U0`: every +/- line begins `*` or `//` inside an existing comment block (no code line, no blank-line change).
- Q2 truth of the new words, against source: emitLifecycleAnchor POSTs to anchoring /api/anchors (documents.ts:1405ff); anchoring's dbPersistAnchor upserts `ON CONFLICT (document_id, network) DO UPDATE SET status = EXCLUDED.status, transaction_hash = EXCLUDED.transaction_hash ...` (anchoring/src/index.ts ~1590) and its own comment says a repeat call "resolves to the SAME row (KS-319 -- keep that)" yet re-arms it (anchorSubmission.ts header; WriteAheadDeclined "a newer call re-armed it"). So "id idempotent, a repeat admitted event may still submit its own transaction, the row then names that one" is supported by source. The comment at documents.ts:700 ("Only an external_id match can be idempotent") is a different subject and untouched, as the fragment says (7 `idempotent` hits remain at the head: 700 + the 6 edited).
- Q5 docs-fragments: check OK on the PR tree; planted-defect control not run on 2103's own fragment (run on 2104 and 2106, same checker, both FAIL as expected with an unclosed div/table; restored by sha, OK again). 
- Q7: merge tree on develop 6c9a593df4ab clean (tree 923a304e19e2).
- Q6: local PR body/comment text: figures consistent with what I measured (1 file +13/-7, 5 comments, line-700 caveat). "Kam ruled that this behaviour stays until stage 2" and the ticket probe are quoted from the card/ticket; NOT checked by me.

NOT TESTED: originate jest suite (seat reports 220 suites / 2592 both sides; I did not rerun); eslint/tsc; the transaction behaviour at runtime (no box; static read only); live PR body/ticket comment 0bb70934; the "83 of 84 commits carry a pair" census.

FINDINGS: none.

---------------------------------------------------------------------

## PR 2104 (KS-1972), head df9493550372: NEEDS TIER 1 (stop line: behaviour beyond what the READY states; my measurement)

### G271-2104-1 (medium) -- at two of the three call sites the change turns "block retried next poll" into "block silently skipped", and the PR/READY/fragments describe only the first site
- WHAT: the READY, PR body and both fragments say "for such a value poll() now resolves and onError is called, instead of poll() rejecting", and call the other sites "the other two isRateLimited call sites in poll()". Source: only ONE call site is in poll() (event-indexer.ts:200). The other two are in processBlock (:223) and processTransaction (:326).
- MEASURED (scratch cell, since moved to /private/tmp/g271/_quarantine/zz-g271-scratch.test.ts): api.blocksLatest -> {height:6}, lastProcessedBlock=5, api.blocksByNumber throws a revoked Proxy (the site-2 path).
  - develop: poll resolves (rejected=false), onError=1 (a TypeError from the revoked-proxy read, caught by poll's own catch), lastProcessedBlock stays 5 -> block 6 is retried on the next poll.
  - head: rejected=false, onError=1 (the constant 'unreadable thrown value'), lastProcessedBlock=6 -> block 6 is SKIPPED (poll's loop advances past it after processBlock's handleError+return).
- So at sites 2 and 3 "poll() now resolves instead of rejecting" is false (it resolved before), and the real change is a lost-retry. That is how any ordinary non-429 Error already behaves in processBlock (handleError; return), so it is arguably consistent, but it is a behaviour change on an event indexer that is not stated, and the seat's own NOT-run list leaves "whether lastProcessedBlock advances at the later call sites" open. I answered it: it advances. Needs Kam/tier-1 judgement on whether skip-on-unreadable is wanted (Wednesday: ruling beyond tier 2, not a security decision).
- FRAGMENT/BODY wording to correct if it goes ahead: flow fragment "poll() calls isRateLimited in its catch at three places, each before handleError" is false (one in poll(), one in processBlock, one in processTransaction; and at :223 the retry path's second blocksByNumber call is not under it). Test header comment ("poll() calls it BEFORE handleError") is true for site 1 only.

### G271-2104-2 (low) -- tests do not pin the status_code / statusCode / response.status arms
- Cells C1/C2 + R1-R3 only exercise `message.includes('429')` among the four arms moved into readsAsRateLimited. My mutant M1 (delete the message arm) is caught only by control C2 (expected 1 to be +0, by assertion). Deleting the other three arms is not caught by any cell. The fragment says the old expression "moved, unchanged": true by diff (the expression is byte-identical), just unguarded.

TESTED / HOW
- Q1: diff read whole: event-indexer.ts +9/-0 = isRateLimited now `try { return this.readsAsRateLimited(err) } catch { return false }`; the old expression moved verbatim into readsAsRateLimited. 5 cells in 1 file.
- Q3 red-first: test file at head: 5/5 pass. Product reverted to develop's blob (git checkout origin/develop -- file): 3 failed | 2 passed; R1,R2,R3 fail, all `AssertionError: expected true to be false` (not crashes); C1,C2 pass. Restored; blob hash-object ebb2ca9a... equals p2104's blob.
- My own mutants (not the seat's): M1 drop the 429-message arm -> 1 failed (C2, assertion). M3 catch rethrows (`throw e`) -> 3 failed (R1-R3, assertion), C1/C2 pass. Restored by sha256 182304ee71d6 (same as the seat's recorded restore hash).
- Q4: whole packages/shared, my instrument: develop 729 tests / 1 red; p2104 734 / same 1 red; the failing-file/test name lists are identical (diff empty). +5 tests = the 5 cells. A control that the diff could fail: the red lists are 23 file-load failures + 1 test on both; an added/removed name would show in `diff` (it did show nothing; I did not plant a new red to prove diff sensitivity beyond the red-first run above, which does show new reds as FAIL lines).
- Q2: quoted lines checked: handleError 'unreadable thrown value' (:357) true; backoff first 429 = (0||1000)*2 = 2000 (:202) true; setInterval(() => void this.poll()) (:146) true; "poll() rejected before" true for site 1 only (G271-2104-1).
- Q5: planted unclosed `<div><table>` appended to the flow fragment -> `FAIL -- 1 finding(s)` (tags not balanced); restored by sha be822240ed53, check OK.
- Q7: merge tree on develop clean (4b0b0dc37911).

NOT TESTED: tsc/eslint figures (25 errors / 38 problems); real Blockfrost; processTransaction site (3) at runtime; the live PR body and ticket comment 26195e09; hook legs.

---------------------------------------------------------------------

## PR 2105 (KS-1974, identus-client part), head 5f1685420cc6: GO WITH NOTES

BLUF: one expression changed; does what it says; the 'narrows' statement is plain. Notes are cosmetic.

FOUND: packages/shared/src/prism/identus-client.ts:134, `errorMessage = String(err instanceof Error ? err.message : err);` (was `err instanceof Error ? err.message : String(err)`); +1/-1; return object (didDocument: null, error: 'notFound', didDocumentMetadata {}) unchanged.

TESTED / HOW
- Q1: diff read: only that expression. Surfaces: Error with string message -> same text; plain string/other thrown -> String(err) as before; non-string message -> now String() (Symbol -> 'Symbol(ks1974)'); object whose toString throws -> inner try catch -> 'unreadable thrown value'. didDocument null and error notFound unchanged (read at :138-144, and by mutants below).
- Q3: head 4/4 pass. Product reverted to develop: 2 failed (R1,R2), assertion errors (`expected {...} to deeply equal {...}`), C1/C2 pass. My mutants: M1 `.toUpperCase()` on the new expression -> 3 failed (C1,C2,R1) by assertion; M2 `didDocument: undefined` at :139 -> 4/4 fail (so the null claim is pinned); M3 `error: 'invalidDid'` -> 4/4 fail (so notFound is pinned). Restored by sha256 c0ee9990e68f4aa3 (= the seat's).
- Q4: shared suite, my instrument: develop 729 / 1 red; p2105 733 / the same 1 red; lists identical.
- Q5: docs check OK with the pair on the PR tree (also OK on the 4-PR merge, 220 new). Planted-defect control run on 2104/2106 fragments only, same checker.
- Q6 'narrows': pr_body_row2 Summary headline "A one-line fix that narrows KS-1974 to its identus-client part. Refs only; the ticket stays open." and "What this does NOT do: KS-1974 names four files; this changes the identus client only" -> plain. Ticket comment 0d041cef (comment_row2_final.md, record id verified in row2_comment_record.json): "covers the identus-client part of this ticket only ... Refs". True. The comment says "KS 1868" try exists: confirmed (commit ee1e1b83 Refs KS-1868 added the 'unreadable thrown value' fallback in this file).
- Q7: merge tree clean (37751f803678).

FINDINGS
- G271-2105-1 (low): test file header comment is garbled mid-sentence ("... an Error whose `message` is a Symbol, an object whose toString throws comes back as that value itself, so `errorMessage` is not text. The fetch stand-in ..."): a wording defect in a comment, not a behaviour defect. The sentence after "Symbol," should read "or an object whose toString throws".
- G271-2105-2 (info): an Error whose message getter returns `undefined` now yields the string 'undefined' where it used to yield undefined. Within "always a string" as stated; not covered by a cell; not wrong.

NOT TESTED: the rest of KS-1974 (verifier catch template, ServiceClient.healthCheck, gateway dashboard); real DID resolution; live PR/comment text; tsc/eslint.

---------------------------------------------------------------------

## PR 2106 (KS-2117), head a8d19bf3918e: GO WITH NOTES

BLUF: no code byte; the 403 statement is true for all three doors; but the "accept/reject" docstring and the "use an accessToken" remedy overstate what the SDK call does against the service.

FOUND: README.md +4/-1 (a note above the approve example; comment "Approve a transfer" -> "Then approve it"), transfers.ts three docstrings.

TESTED / HOW
- Q1 strip-and-compare of transfers.ts: emit 1,225 B both sides, sha 88ae19ec31e0fd9b both, IDENTICAL; controls: code line at EOF differs (true), comment line identical (true). The third (string-literal) control did NOT differ (the first quote after the first import is in a type-only import that the emit elides): that control is not valid for this file and I do not rely on it. README diff read whole.
- 403 truth: transfer service index.ts: refuseNonUserPrincipal (:522) -> 403 "An API key cannot open or act on a transfer."; used by initiate (:535) and by requireCaller (:682) which approve (:708) and cancel (:933) call first. KS-2081's own test DOORS list includes approve and cancel (ks2081-transfer-doors-refuse-non-user-principals.test.ts ~156-166). True. Bearer-vs-key: client.ts:83-86, accessToken wins, X-Api-Key only otherwise: true. 'accept' is in the SDK type `'approve' | 'reject' | 'accept'` (transfers.ts, approve): true of the TYPE.
- Q5 docs check OK; planted unclosed-tag on the KS-2117 flow fragment -> FAIL, restored by sha 1edbfd520e40, OK.
- Q7 merge tree clean (e6697fc99041).

FINDINGS
- G271-2106-1 (medium): the `approve` docstring now says "Approve, reject or accept a transfer" and the fragment says the three actions "are the method's real options"; the README says to build the client with an accessToken "for these calls". Against the service (services/transfer/src/index.ts): POST /api/transfers/:id/approve (:706) has NO `action` field (approveTransferSchema :404 = approverId, approverRole, reason, signature, walletAddress, comment; zod drops unknown keys), reject is a separate route (/reject :794), and the string 'accept' occurs nowhere in the transfer service. Worse for the README advice: approverId and approverRole are REQUIRED (`z.string().guid()`), and the SDK body {action, comment, signature} carries neither, so even with an accessToken the README's own `approve(transferId, 'approve', {comment})` call gets a 400; the service says so itself (index.ts:721: "a body that names nobody, such as the SDK's { action: 'reject' }, keeps its 400"). So: the 403 sentence is true, but the added "use an accessToken" implies that is the fix for approve, and "reject or accept" asserts options the endpoint does not honour. The seat verified 'accept' against the TS type only (as the READY says), which is what was asked, but the type is not the behaviour. Suggest the docstring/fragment say "typed as ..." or drop reject/accept, and the README note not promise success.
- G271-2106-2 (low): "A client built with an `apiKey` is refused with 403" is over-broad: a client built with BOTH apiKey and accessToken sends Bearer only (client.ts:83-86) and is not refused.
- G271-2106-3 (info): PR body/fragment say "Since PR 2077 (KS 2081)": the KS-2081 commit is 76570130 "Refs KS-2081: the transfer write doors refuse a non-user principal"; I could not confirm the number 2077 from the subject (git show of the commit needed a blob fetch my env refused). Not verified either way.
- Reported, not caused by this PR: SDK package has no test files (vitest exits 1), as the seat says; not retested.

NOT TESTED: SDK -> gateway -> transfer service end to end (no box); eslint/tsc for the SDK; other SDK docs/examples that carry a key; live PR text/comment d90aa502.

---------------------------------------------------------------------

## Batch (Q7)
- File-disjoint pairwise: 6 pairs, 0 common paths each (diff --name-only origin/develop...pN). Control: a planted extra path from 2106 added to a 2103 list -> 1 common (instrument can see an overlap). 
- Sequential 4-PR merge on develop 6c9a593df4ab via merge-tree/commit-tree (2103, 2104, 2105, 2106, no conflict; 15 files, +337/-12; docs-fragments check OK, 220 new). Control: same-line edit on develop side vs 2103 -> merge-tree rc 1 with an unmerged documents.ts (instrument detects a conflict). The two new test files pass together on the merged tree (9/9), the full shared run on the merge shows the same single red (23 file-load failures are the stale-deps instrument limit).
- Open PRs sharing any path: NOT TESTED (needs the open-PR list; network limit). The seats' driver quotes "43/44 open PRs, none touches any of the paths" at 15dca468b86f; develop has since moved one PR.
- Merge order: no ordering constraint from file overlap. Docs numbering is merge-order, provisional per the checker.

## Conduct / limits
df DevMASTER start 10.33 GiB, end 10.33 GiB (just above the 10 GiB stop line the whole time; I wrote only this file there). load1 peaked 8.27 once (during the full-suite loops, I paused 45 s), otherwise below 8. No git write verb under !CODING; all writes in /private/tmp/g271. Nothing posted or mailed.
