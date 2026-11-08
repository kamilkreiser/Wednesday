GO WITH NOTES

# Gate 253, tier 1, round 2 of 2: PR 2064, KS-1205

| PR | Ticket | Head | Develop (re-pinned) | Verdict |
|---|---|---|---|---|
| 2064 | KS-1205 F-5 | 6c8856baf1025d8048969a4facc7101ea30cbb7b | a65ae7ed1d6083bde60c4198a60a528129277c40 | **GO WITH NOTES**. Nothing blocks. |

Heads read from origin with ls-remote at 2026-11-08T09:35:12Z (start) and 09:41:54Z (end). Both times: develop a65ae7ed1d60, refs/pull/2064/head 6c8856baf102, and the branch `feature/ks-1205-document-and-pin-the-audit-row-of-a-refused-request-t14` at the same SHA. The head did not move, so this verdict holds. A verdict covers these SHAs only.

Severity is mine; priority is not. Substrate: macOS, Node v26.8.1, vitest 4.1.10, BSD grep. Dependencies are symlinked read-only from the Blockchain checkout (see NOT tested).

## BLUF
All four round-1 findings are closed, by my own read and my own run. The product edit is comments only: four SHAs compile to the same output. The new cells go red for the right reasons on behaviour defects in audit.ts. The merge tree on the re-pinned develop is clean. I have three things to note, and none of them blocks:
- One sentence in ticket comment 195d740a is now out of date.
- One path class falls outside every text. Outside production, a refused write spelled `/API/...` leaves no row.
- The order pin reads index.ts as text, so an audit mount that is commented out or disabled for production passes all 16 cells.

## 1. F64-1 to F64-4, closed?
- **F64-1 CLOSED.** The comment (`rateLimitEnforce.ts:168-179`), both fragments, the PR body and the ticket comment now say what audit.ts does. It audits POST, PUT, PATCH and DELETE on `/api/` paths that are not excluded (`audit.ts:58`, `:209-212`). GET, HEAD and OPTIONS are not audited, nor are the excluded paths or anything outside /api. My run at head: 16 of 16 green. The GET, HEAD, OPTIONS, audit-path, admin-audit-path and non-/api cells each measure statuses [200,429] with 0 rows. MEASURED AT RUNTIME.
- **F64-2 CLOSED as a stated limit.** `auth.ts:572` gives userId `connector:<id>`, and `audit.ts:65` turns that into a null user_id. A cell pins it. READ plus MEASURED.
- **F64-3 CLOSED as a stated limit.** It is pinned by a cell, and the text says reachability is not established. That is true.
- **F64-4 CLOSED.** The pin now anchors on the first `/api` router mount and names the batch (`index.ts:833`) and notifications (`:834`) mounts. The in-test control ran green. Its limits are in N253-2.

**Is every sentence about which refused requests write a row true, by measure, on every method and path class?** Yes for the lowercase `/api` spelling, with one path class outside the text:

**F253-1, Minor, does not block, pre-existing: in non-production, a case-variant `/api` path is served and refused but writes no row.** `audit.ts:210` tests `req.path.startsWith('/api/')` case-sensitively, while express routing is case-insensitive (index.ts:548 says so itself). The `/api/v1/` rewrite (`:552`) lowercases only versioned spellings.
- I measured this in a composition: real versioningMiddleware, the rewrite copied from `:550-553`, the real audit middleware and the real limiter, a router at `/api/documents`, limit 1, two POSTs (evidence_probe_path_spelling.txt).
- With NODE_ENV test or development, `/API/documents` and `/Api/documents` gave statuses 200,429 and **0 rows**, while `/api/documents` gave 2 rows. With NODE_ENV production, the folded 307 (`routes/versioning.ts:49-61`) answers them, and `/API/v1/documents` is rewritten and audited. So production is closed and other environments are not.
- This holds for admitted writes too, so it is an audit gap rather than this PR's error. It is outside the texts' "on an /api path" only if /api is read literally.
- Fix shape (READ ONLY for the fix): ticket it separately. Fold case at `audit.ts:210-212` or add a "NOT audited" line. Do not hold this PR for it.
- NOT established: which NODE_ENV the demo and kintsugi gateways run.

Other methods and paths, all READ ONLY:
- TRACE and custom methods are not audited. The texts list positively what IS audited, so that stands.
- A trailing slash (`/api/documents/`) is audited (measured: 2 rows).
- The exclusions also include `/api/csrf` and `/api/csrf-token` (`audit.ts:70-74`). The flow fragment names them. The code comment and ticket comment list "health" and not CSRF. That is an omission, not a falsehood.

## 2. Comment only, by my own compiled compare
I ran `rateLimitEnforce.ts` through TypeScript `transpileModule` with removeComments. Base 9cdb9321, round 1 836e21a7, head 6c8856ba and the re-pinned develop a65ae7ed all give sha256 **54c5f398af8a5d19**, 7688 bytes. A one-line planted control gives ebbb6b174cafa3c7. In the diff against the merge base, 12 added lines are all `//` and there are 0 other lines. The other three files are a test and two html fragments. MEASURED AT RUNTIME (evidence_comment_only_compare.txt).

## 3. Ticket comment 195d740a, read line by line against this head
The record (`evidence/p3_ks1205/round2/comment_record.json`) shows body_sha1 0546cf01…. That equals the sha1 of `mail/ticket_comment_ks1205_round2_correction.md` with its trailing newline stripped, so I read that file as the posted body. I did not read Linear.
- **F253-2, Minor, does not block: one stale sentence.** The BLUF's last sentence reads: "A corrected commit is built and queued to push; PR 2064 still shows the old head until it lands." It was true at 20:38Z. The push was verified at 22:00Z, and the PR has shown 6c8856baf102 since then. **Edit to:** "The corrected commit is PR 2064's head `6c8856baf102`." Leave the rest of the text alone.
- Every other sentence is true at this head by my read and runs: the method and path rule, the excluded list (minus CSRF, as above), the user_id null, the default tenant, "not every 429 row is this limiter's" and the global limiter writing none. So are: 6 comment lines becoming 12, 4 cells becoming 16, the cell list, "emitted JS byte-identical to develop" (true against a65ae7 too) and the "Refs" sentence. The PR title says Refs, and no closing keyword is in the body draft.
- Not confirmed by me: "1751 of 1751" (see NOT tested) and "10 of 10 killed, 8 survive round 1". I reproduced 1 of the 10.

## 4. The new cells: can they fail, and for the right reason?
All mutants ran against head copies, one at a time (evidence_mutants.txt). MEASURED AT RUNTIME.
- Seat's M1 reproduced, with AUDITED_METHODS cut to POST: **3 red** (PUT, PATCH, DELETE), as the seat claimed.
- **Mine:** audit.ts skips a 429 row for DELETE only: **1 red** (the DELETE cell, AssertionError). The right cell, for the right reason.
- **Mine, which survived:** the audit mount in index.ts wrapped in `/* … */`: **16 of 16 green**.
- **Mine, which survived:** the audit mount wrapped in `if (process.env.NODE_ENV !== 'production') { … }`: **16 of 16 green**.
- **N253-2, Minor, does not block: why the last two survive.** The order pin locates `app.use(createAuditMiddleware(` with `indexOf` on the source text. A disabled mount still has that text, and the composition cells never load index.ts. The comment says the pin is "read from index.ts's source text", so this is a stated limit. But a production gateway with no audit at all would pass the file.
- Fix shape (READ ONLY): assert the mount is live code, for example with a TS AST walk to a top-level ExpressionStatement, or by importing the app. Ticket it; do not hold this PR for it.

## 5. Merge tree on develop a65ae7ed1d60
- `git merge-tree --write-tree origin/develop origin/pr2064` gave tree 72aa741fe99c and exit 0. Clean.
- The merge base is 9cdb9321. Develop has 70 changed files since then, and none of them is one of this PR's 4 paths (`git diff --name-only`, which printed 70 as its own positive control).
- I checked no other open PRs (network was git only). Gate 247 found that heads 1970 and 1985 touch `rateLimitEnforce.ts`. I did not re-check them.

## Notes, READ ONLY
- N253-1. The seat did not name the verification limiter (`index.ts:573-584`). It is `express-rate-limit` mounted before the audit mount (`:588`), so its 429s write no row. The brute-force guard (`security.ts:251`, mounted `index.ts:459`) answers 429 before the audit mount too. Both fall under "not every 429 row is this limiter's" and "the global limiter writes none". The texts are incomplete here, not false. Also, an upstream service's own 429 relayed through a proxy on a POST would write a 429 row. I did not establish whether any upstream does that.
- The card's premise ("today every refused request still writes one audit entry") is still Wednesday's error, as the commission says. The texts now say what is true. Whether refused reads should go untraced is still Kam's question, as gate 247 put it.

## NOT tested
- **Whole api-gateway suite: NOT RUN validly. Blocker:** the read-only checkout's `@secuura/shared` is older than the head. My run gave 73 failed of 166 files, with causes `boundedJson is not a function` and `Cannot find package '@secuura/shared/zod-compat'`. That is my substrate, the same as gate 247's, and not evidence against the PR. The ks1205 file is not among the failures, and the dedicated run gave 16 of 16. The seat's 1751 of 1751 is unconfirmed.
- I did not boot the real gateway, use a real key, or stand up a database. The audit_logs.tenant_id question about the deployed schema stays open. Not run: Node 24, tsc, eslint, check:test-types, the seat's other 9 mutants, and Linear itself (I read the seat's record, not the posted comment).

## My conduct
- I ran no `cd` and no `rm`, and did no fetch in the read-only checkout. Network was git only. I posted nothing and changed no ticket or PR.
- Two of my calls were refused by hooks and never ran: an unquoted `====`, and git write verbs on a `$VAR` path. I reissued both with literal paths. `merge-tree` ran in `/private/tmp/g253`.
- My probe test and mutants live only in my scratchpad lab (`/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/02fe044e-b48b-4f7e-8397-447f163806d4/scratchpad/lab`, 171 MB including a second partial copy). There, the node_modules folders are directories of symlinks into the read-only checkout, so caches landed in my lab. Nothing was written to the checkout.
- Load stayed under 8 (peak load1 about 4.4).
- **Clone left in place: /private/tmp/g253, 187 MB** (blobless partial clone, no checkout).
