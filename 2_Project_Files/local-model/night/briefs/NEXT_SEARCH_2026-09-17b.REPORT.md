# NEXT SEARCH 2026-09-17b (03:28–03:45 AEST): the next Ornith ticket

**BLUF: KS-1182 FITS as a PARTIAL (F4 only).** It is a code_patch: ONE small product file (`services/demo-service/src/middleware/errorHandler.ts`, 39 lines, one hunk +12/-5) plus ONE new test file (108 lines, 7 🔴 + 2 🟢). All 7 red cells fail at the tip by assertion, and each of the four parts of the fix has its own red. Running the brief's own fences through the real checker gave **RESULT: PASS (7/7)**, twice, the second time with the placed brief and the real input. F7 (the ks844 test's name and markers, called optional in the ticket) is left out, so the PR says "Refs KS-1182 (F4)". The search stopped at the first fit: KS-1181 was read but not briefed, and the candidate-3 tickets were not read.
- Brief: `night/briefs/KS-1182.md` (new). Input: `night/inputs/code_1182.json`. `build_input.sh` rc 0 at 03:43:51, tip `d067725ff`, ~9.2K prompt tokens, ctx 65536. Pins (all required): `product=Blockchain/Dev/services/demo-service/src/middleware/errorHandler.ts ref=services/demo-service/src/__tests__/ks844-demo-service-mounts-no-error-handler.test.ts line=33 ctx=65536`.
- Not queued and not run on the night runner. `queue.md`, `done.md`, `candidates.md`, `IMPROVEMENTS.md`, the checkers and other briefs were not touched. The Secuura porcelain read 0 at every reading (11 readings, 03:28:58–03:44:19). No git write verb ran against the Secuura checkout.
- **One call for Wednesday before queueing:** the disqualifier list refuses "security-guard PRODUCT edits". This handler is not auth, MFA, OAuth or a guard module. It is an error-envelope middleware in demo-service, which refuses to boot under production. But its KS-727 lineage is a message-leak control, and the `expose:false` arm is a redaction change. If you rule that class in, this becomes a REFUSAL, and nothing else in this search was pre-measured.

## Pins
- Tip `d067725ff1c7f036dbf0f726b9bf12f4daefebe7` (#1009). **Origin moved mid-search:** `f7c2f4acb` at 03:29:03, then `d067725ff` at 03:34:49. The GitHub compare shows #1009 changed only three api-gateway `ks864*` tests. In the clone, `git diff --stat` of demo-service + packages/shared between the two tips is empty. Rounds r1–r3 ran at `f7c2f4acb`. **r4, fin1 and fin2 re-ran everything at `d067725ff`** in a fresh clone (`ks1182_pm.FHRiAO`).
- `errorHandler.ts` blob `10528c5be`, sha256 `4399e6dec116726b…`. This blob is the #1006 gate's equality target.
- Scripts and outputs are in `scratchpad/next17b/`: `premeasure.sh`, `final.sh`, `premeasure.r1..r4.out`, `final.fin1.out`, `final.fin2.out`.

## Pre-measure (sandbox-exec, off-host outbound denied; every vitest/tsc/checker run)
- **Tip baseline:** demo-service 72/72. packages/shared `ks727-errorhandler-class-guard` + `ks781-p3-3-body-parser-order`, which drive this handler: 334/334.
- **The test alone at the tip:** 9 run / 7 failed. All 7 failures are the 🔴 cells and all are ASSERTION reds; both controls are green. The result was the same twice. Rows H3 (600) and H11 (99) sit inside merged cells, and each was red by assertion on its own in r1/r2.
- **Golden:** 9/9 twice. demo-service 72 → 81 with no new red. Shared ks727 + ks781-p3-3 stayed at 334/334. tsc: the service program, the checker's standalone command and an including program all gave rc 0 with 0 errors.
- **Partial-fix tampers on the golden, each with anchor count 1→0:**
  - Clamp loosened: H1, H2 and H5 red.
  - Headers line voided: only H9 red.
  - `expose` ternary removed: only H12 red.
  - `headersSent` arm disabled: only H10 red.
  - All reds were by assertion, and the golden ran 9/9 afterwards.
- **decl_splice:** `spliced 0` against the pinned ks844 AND against each of the other 7 demo-service tests.
- **Checker on the brief's own fences:** strict apply rc 0, and the applied product and test were byte-identical to the golden.
  - fin1 used the scratch input and fin2 the placed brief and real input. Both gave PASS A1–A7.
  - A3b: 5 sites. A3c: 12 lines, A3d clean.
  - A4: 7/9 with assertion reds and controls green, no DECL-SPLICE.
  - A5: 9/9. A6: 72→81. A7: rc 0.
  - Between the two inputs, only `ticket.description` differs (it carries the brief text). `defect_line`, `files`, the pins and the tip compare equal.
- The brief's `## Premises (measured)` (P1–P14) names each instrument and clock.

## Rejection table
| ticket | verdict | measured reason |
|---|---|---|
| KS-1182 F4 | **FITS (briefed)** | One product file (39 lines) and one new test. Explicit fix shape. PASS 7/7 twice. Not on Peter's or Stuart's account (assignee kamil.kreiser@secuura.ai). Partition-clear: none of the 18 open PRs touches `services/demo-service/src`, and seat A's held diffs are api-gateway audit/verification and auth users/userRepo. |
| KS-1182 F7 | REFUSED (in the partial) | It edits the EXISTING `ks844-…test.ts`: a rename plus marker changes. That would make a second test file, and code_patch A3 allows exactly one. The ticket calls it "optional". A rename is also not a hunk the checker can grade. |
| KS-1181 | NOT BRIEFED (stopped at first fit) | Read-only facts (Linear 03:28:48): Backlog, 0 attachments, 0 comments, assignee kamil. F2's fix shape asserts a hit count in `driveThroughRoute` inside the **946-line** guard (read at `f7c2f4acb`), which is the "file > ~600 lines modified in place" class. F3 ("parse the header counts in a cell, or reword") is either a new cell in that same file or a comment reword at `:18-21`. The reword is a possible small doc-shaped lead and was NOT measured. |
| Backlog/Todo updated since 2026-09-16T12:00Z (candidate 3) | NOT READ | The search stopped at the first fit, so the count read is 0. `candidates.md`, `done.md` and `queue.md` have 0 mentions of KS-1181 or KS-1182. |

## Wrong in the tickets, gate reports or harness (for Wednesday to file; IMPROVEMENTS.md not edited)
1. **Harness, `build_input.sh` reference note is false for a pinned ref that does not import the product.** The note says ks844 "imports the product module (`middleware/errorHandler`) and drives it in-process with vi.mock stubs … Copy its app-building / import / mock shape". ks844 imports `../app`, and no demo-service test imports `middleware/errorHandler`, which is why `ref=` is required. The brief tells the model to ignore the reference. The note should say when the pinned ref does NOT import the module.
2. **Harness, `suggested_test_file` is derived from the ticket title, and nothing compares it with the brief's `CREATE THE NEW FILE` path.** The first draft named `ks1182-…-status-sanitised.test.ts`. The builder silently suggested `ks1182-demo-service-errorhandler-unchecked-err-status.test.ts` (03:39:58), which would put two conflicting paths in one prompt. The brief was renamed to the builder's path. A builder check (brief path == suggested path, or a `test_new=` pin) would catch this.
3. **Harness, the code_patch checker leaves the clone PATCHED.** After PASS, the product sha == golden (not the tip) and the new test stays untracked (03:42:12, 03:44:19). Test-only mode reverts its tamper; code_patch mode does not revert anything. A reused clone must be cleaned first (`scratchpad/next17b/clean_clone.sh`).
4. **Harness, A6 is blind across packages.** It runs only the service suite, but packages/shared `ks727` + `ks781-p3-3` import and drive demo-service's `errorHandler` / `createApp()`. They stayed green here (334/334 before and after), but the checker would not see a red there. The brief marks this NOT GRADED BY THE CHECKER.
5. **Test-design trap (new):** a backstop error handler that answers with raw `res.end(body)` after the handler's `json()` threw inherits the handler's Content-Length. The client then waits, and the cell fails by TIMEOUT (`Error: STACK_TRACE_ERROR` at the `it(` line), not by assertion (r1, 03:34:57). `res.removeHeader('content-length')` fixes it (r2). The KS-727 guard's backstop calls `res.status(500).json(...)`, which resets the length, so it does not hit this.
6. **Gate report / ticket, cause attribution.** "NaN → process exit 1" is finalhandler 1.3.2's doing, not the handler's alone (READ `node_modules/finalhandler/index.js:238-247`, 03:44:48). The handler throws synchronously for BOTH 99 and NaN. `getResponseStatusCode` maps 99 to 500 but keeps NaN, because `NaN < 400` and `NaN > 599` are both false, so finalhandler's own write throws uncaught. The F4 row reads as if NaN and 99 differ in the handler.
7. **Ticket, two open decisions the brief had to take:** the replacement text for a 4xx with `expose:false` (the brief uses `Request error`), and "or for a typed error" (not taken: a typed 4xx marked `expose:false` is also redacted). Also, `err.status ?? err.statusCode` picks an INVALID `status` over a valid `statusCode` (`{status: 600, statusCode: 404}` → 500). finalhandler checks them separately (→ 404). This edge was not graded; it is recorded in the brief's raise notes as finalhandler parity for headers only.
8. **Previous report (17 Sep, 03:20):** its KS-1181 row says "the #1006 report was not read". It is now read: F2's fix needs a hit count inside `driveThroughRoute` in the 946-line guard, so the refusal class holds. F3's reword option is the only small lead left on that ticket.
