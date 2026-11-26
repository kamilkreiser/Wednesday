GATE B2125: GO WITH FINDINGS
@ 408b865 on main 523856d

Gate G1 (Opus), round 1 of 2, on lane 1: RD-893's type-check half and RD-1009's early 400 (kit B2121, seat N179). No Blocker and no Major. Two Minor findings and six Info findings; **none blocks landing**. Nothing I measured contradicts anything the seat reported or Tuesday endorsed (Q-1 to Q-8 all hold at source). On point 2(b), malformed JSON is NOT the only shape that still reaches the final handler on this route: six more parser-refusal shapes do (Minor 1). The pull request's hosted build will be the first real Linux run (Q-8); a red on a new cell there is a fix round.

Re-measured 14:29 to 14:58 AEDT, 26 Nov, by `gh api -X GET` (the project's GH_CONFIG_DIR) and by my own runs:
- main = 523856de056b772696f06c81eb001316d6f87f76 at the first read and the last, 14:58:53. BASE..main is `HISTORY.md` only, an allowed move. `backend/server.js` blob at main is 1cdff5af (= BASE), and the counts blob at main is a2cc964d (= BASE).
- Branch `b2121/lane1-validation` = 408b8655cbd360c8d09fe21ec70d944f56ec8d1b. Compare main...head: ahead 3, behind 2, merge base 89663a44. The files are exactly the four of the commission: server.js 15/0, rd893 test 267/0 (added), rd1009 test 166/0 (added), counts 3/3.
- Open PRs 0. Open code-scanning alerts 22. Check-runs on the head: `audit-production-deps` success only (npm-audit runs on a push to any branch; the seat's Correction 1).
- Commits: A 7867b92c (parent BASE), B f04cbccb (parent A), K 408b8655 (parent B). Author and committer on all three: `88359143+kamilDatasec@users.noreply.github.com` on both sides.

## Measured by me (MEASURED) vs the seat's (RELAYED)
**Trees.** My own clone (`git clone --no-checkout` of the seat's clone) under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s330/g2125/clone`. Four dot-free worktrees `t/base` (BASE plus the two new test files copied from K: blobs c870936f and 79d761ad), `t/head` (K), `t/mut` (K) and `t/full` (K). `node_modules` in each is a symlink to the seat's `npm ci` (disclosed; package-lock sha256 prefix 37e5add354e539f9 equal in both). Each tree has 0 dot segments (control: the seat's `.tools/b2121/clone` reads 1). Slots 1, 3, 12 and 2: each port band had 0 listeners before the runs (control: 12 listeners machine-wide). Node v24.22.2.

**Jest lock.** Two acquisitions, `g2125-lane` (14:33:44 to 14:35:31) and `g2125-full` (14:36:12 to 14:58:26). Both were acquired after 0 s and released, `lock-wrapper rc=0` each. `NODE_OPTIONS` was unset, and `MIN_TESTS`, `MIN_SUITES` and `VERIFY_EXPECTED_FILE` were unset for the verify. No jest ran outside them. Afterwards the lock base lists `queue-docker queue-jest released` (no holder), and 0 listeners remain in 20000-32767.

**(1) The diff, read whole.** In `backend/server.js` a line-level SequenceMatcher BASE -> K finds exactly two pure INSERTS: 3 lines after BASE line 7881, and 12 lines after BASE line 21700. 0 BASE lines are deleted or replaced. So the risk_level check (count 1 = 1), its 400 sentence (1 = 1), the landed lower-casing (1 = 1), the PUT body line (3 = 3 in the file), the hasOwn field read (1 = 1) and the stream field read (1 = 1) are byte for byte BASE's. The added lines, as STATUS shows them, are the three `if` checks and the one-line refusal.

**(2) Red-first and green, both shapes** (my own judge, `gjudge.py`, which compares the exact set of failed cells from jest `--json`):
- Linux shape = `TMPDIR=/tmp` plus `RUNNER_TEMP` set to a persistent dot-free folder. Own shape = this shell's `/var/folders/...` TMPDIR, never unset.
- At BASE, PUT file, both shapes: 19 cells, 5 passed, failed exactly C1 and T1 to T13.
- At BASE, stream file, both shapes: 9 cells, 5 passed, failed exactly C1, R1, R2 and R3.
- At K, both files, both shapes: 19 of 19 and 9 of 9.

**(3) The ten mutations, my own program** (`tools/gmut.py`, written independently against the same anchors; Linux shape). Each read red on EXACTLY the seat's named cells:
- no-text: T1-T4, C1
- no-active: T5-T8, T13, C1
- no-recipients: T9-T12, C1
- truthy-text: T4, C1
- truthy-active: T7, T8, C1
- strict-active: A1, C1
- nonempty-recipients: A1, C1
- stream-no-refusal: R1-R3, C1
- stream-status (422): R1-R3, N4, C1
- stream-refuse-all: N1, N2, N5, C1

After each revert the server blob read 2ac5badf (13 of 13). **Three extra mutants of mine** each turned red ONLY C1, the source-text pin, and no behaviour cell (Minor 2):
- put-strict-text: refuses `''`.
- stream-falsy-only: `if (!req.body)` in place of the shared check.
- put-recipient-elements: also refuses a non-string element.

**(4) Does any present wrong-typed value still reach the store? No, for the three fields' top-level type.** My adversarial file `g2125-adv-put.test.js` (14 cells, run at BASE and at K, Linux shape) sends shapes outside the kit's cells:
- A form-encoded `is_active=false` (text), `condition_text[a]=b` (an object), a single form `email_recipients` value (text), JSON `is_active:"false"`, a JSON duplicate key whose last value is `"yes"`, and a wrong recipients type beside a right `is_active:false`. All six were STORED at BASE (200; for example `is_active` was stored as `"false"`). All six are refused 400 at K with the store byte-identical.
- What still goes through by design (Q-3): elements of the recipients list (`[7,null,{}]` stored at K), and any string text (`''`, `'a'`, 621 characters with quotes, a newline with U+202E: all stored at K, all refused by create).

**(5) Is a right value now refused? No.** Covered by A1 (`false`, `[]`) and A2 (all four fields), plus my X1 (`''` stored at K) and X6 (a form `email_recipients[]=...` list stored at K). An empty string is pinned by no behaviour cell, only by C1's text (Minor 2).

**(6) Does any body the shared check refuses still reach the destructure? No.** The line above the destructure returns for every non-plain-object body. My stream adversarial file (13 cells, development setting, at BASE and at K) found one more unparsed type at K: `application/merge-patch+json` (500 with the thrown text at BASE, 400 `Message is required` at K, 0 model calls). JSON `null` and JSON primitives never reach the route, because the strict parser refuses them (see 2(b)).

**(7) Is any ordinary JSON or form message now refused? No.** N1 and N2 are green at K. My extra shapes also stream (200, 2 model calls each) at K as at BASE: a gzip-compressed JSON message, and a JSON message with an object `conversationId`.

**(8) The RD-1009 refusal is one line.** Over head server.js: the braced `if (!isPlainRequestObject(req.body)) {` counts 1 (= BASE, line 3621), the one-line refusal counts 1, and `function isPlainRequestObject(` counts 1. RD-1007's file passes in the whole-suite run (`PASS __tests__/rd1007-user-add-unparsed-body.test.js`), so its cell C1 reads 1.

**(9) The whole suite, once, by the project command** (`npm --prefix <t/full> run verify -- --maxWorkers=2`, committed counts, Linux shape):
- `verify-suite: expectation — tests=6504 suites=409 (from scripts/verify-expected-counts.json)`
- `Test Suites: 409 passed, 409 total`, `Tests: 6504 passed, 6504 total`
- `VERDICT: PASS — 6504/6504 tests passed across 409 suites (jest exit 0)`
- `EADDRINUSE` 0 (control: `Tests:` 1). `FAIL ` lines 0 (control: `PASS ` lines 409). Porcelain after: 0.

So the counts pair 6504 / 409 equals the project command's measured output. This is the Linux shape; the seat ran its plain verify in the own shape. Both now read PASS.

**(10) gitleaks 8.30.1.** The control (a planted synthetic AKIA key pair, via stdin) ran first: rc 1, `leaks found: 2`. Then `git log -p BASE..K` (534 lines): rc 0. The three commit messages (24 lines): rc 0. My four landing texts: rc 0.

**(11) The word scan, as the kit runs it.** I used `scanlib1114.py` line 20's four plain names, extracted by program and never printed, with the underscore-aware pattern; each name's `x_by_<name>_y` control fired.
- 451 added lines: 0 name hits, 0 build/seat/card/session-id hits (the kit's id regex; control fired), 0 skip/only/platform/CI hits (control fired), 0 non-ASCII, 0 `/Volumes/`.
- Messages: 0 names, 0 ids, ASCII, nothing about the product owner.
- The only removed lines in the whole patch are the counts file's 3 lines.

**RELAYED, not re-run:** the seat's local CodeQL (head 29 = base 29, KEPT 0, NEW 0, rc 0); its own-shape plain verify; its static2121 prints; its push.

## Tuesday's points
**(a) `condition_text` with no length or character rule on the PUT.** Yes, the PUT accepts texts that create refuses. Measured at K: `''`, `'a'`, 621 characters with `'"<>|;`, and a newline plus U+202E were all stored. BASE accepted them too (and worse: any type), so this change only narrows the PUT.

Do the KQL builder or the alert path mishandle such a text? I read them from source; I did not drive them with Log Analytics:
- `generateKQLQueryForCondition` (server.js 5318) strips the text to `[a-zA-Z0-9\s%$.,()-]` and puts only parsed integers into the query, so the text cannot inject KQL.
- Above 500 sanitized characters it throws `Condition text too long`. The three callers that read a stored text catch that: the scheduler's per-condition catch, the list route's catch (empty results) and the execute route's fallback to the database.
- The SQLite path derives fixed templates from the text (`buildRiskSql`).
- The alert email escapes the text in HTML (`escapeHtml`, riskAlertScheduler.js 209).

So it is mishandled in the sense of "silently no results or a fallback", not a crash or an injection. **Graded Info 3; no change asked.** A neighbour I found (Info 4): the PUT never clears or regenerates `kql_query` when the text changes, so on the Log Analytics path an edited condition keeps running its old query. That predates this change.

**(b) The disclosure.** The unparsed-body 500 is gone on this route. But malformed JSON is **NOT the only shape that still reaches the final handler.** Measured at BASE and K alike, in the development setting, each answered with `sanitizeErrorForClient`'s development branch (`message` = the error's own text):
- malformed JSON: 400 `Unexpected end of JSON input`
- a JSON primitive or `null`: 400 `Unexpected token ..., "null" is not valid JSON` (the strict parser; malformed-JSON class)
- `charset=klingon`: 415 `unsupported charset "KLINGON"`
- `Content-Encoding: xyz`: 415 `unsupported content encoding "xyz"`
- a corrupt gzip body: 400 `incorrect header check`, code `Z_DATA_ERROR`
- over the 2 MB chat cap: 413 `request entity too large` (the kit's named "413")
- a form deeper than 32 levels: 400 `The input exceeded the depth`
- 1001 form parameters: 413 `too many parameters`

None of these names a server path, a stack or an internal value: each is the body parser's own words or, for JSON, a snippet of the client's own input. Inside the handler, nothing above the first `try` can now throw for a plain object (the destructure, two `typeof` checks, `chatMessageTooLong`, `writeHead`). **Graded Minor 1, does not block.** It is the same product decision RD-1009 stays open for, and it should be framed as "every parser refusal", not "malformed JSON".

**(c) Code scanning.** Both hunks only add lines. From the SARIF of main's javascript-typescript analysis (id 2253105831, 29 results; 346 server.js locations among the primary, related and flow-step locations):
- The ONLY location inside either hunk window (BASE 7878-7886 and 21692-21706) is server.js 7882, the stream route's field read.
- That line is one of 19 "untrusted data" related locations of open alert **#235** (js/http-to-file-access, **medium**, primary `backend/jsonStorage.js:524`).
- At K that line is byte-unchanged (it moves to 7885). The new line 7884 reads `req.body` only into the boolean check, which does not reach the sink.
- No location of any result falls in the PUT window.

This is RD-1007's history in miniature: that change rewrote server.js 3624, which is also a related location of #235, and the hosted scan then listed alerts as new. Here the line is kept, and the seat's local run read KEPT 0 / NEW 0. The ruleset (`rules/branches/main`) gates on `security_alerts_threshold: high_or_higher` AND `alerts_threshold: errors`; #235 is medium. **Graded Info 2.** The PR's CodeQL run is the authority, and a "no new alert" read there is not a landing condition; main's analysis at the merge commit is.

## Adversarial beyond the kit: three shapes outside each property
**(A), the PUT route:**
- (i) Form-encoded bodies. The kit did not pin them. COVERED by my X5, X6, X7 and X9: text values are refused, `[]` lists are accepted.
- (ii) Duplicate JSON keys, and a mixed body with a right `false`. COVERED by X12 and X14.
- (iii) Values whose type is right but whose content create refuses (empty, long, control characters), and wrong element types. A NAMED LIMIT (Q-3; Info 3 and 5). Also outside: the Log Analytics run of a stored text (not run; RD-893 measurement (1)); `is_active:false` is also the soft-delete flag (`deleteRiskCondition`), unchanged.

**(B), the stream route:**
- (i) Other unparsed content types (`application/merge-patch+json`). COVERED: 400 at K, 500 at BASE.
- (ii) Parser refusals (charset, encoding, gzip, size, depth, parameter count). A NAMED LIMIT (Minor 1).
- (iii) Compressed valid JSON, an empty JSON body, and an object `conversationId`. COVERED: they stream, or answer 400 `Message is required`, the same at BASE and K.

Not covered: the production setting's answer on this route (the stream file and my runs use development; by source, production answers a fixed sentence); real Linux.

## Findings
1. **MINOR, does not block. Parser refusals still reach the final handler on POST /api/chat/stream** and, in the development setting, answer with the parser's own text (eight shapes measured, listed under (b)). The kit and the commit text name only "malformed JSON" and "the 413". No server internals leak, and production answers a fixed sentence. Ticket text: RD-1009 stays open for "every body-parser refusal on the chat prefix", not malformed JSON alone. The pr-body says so.
2. **MINOR, does not block. Three properties are pinned only by C1's source text, not by a behaviour cell:**
   - that an empty `condition_text` is accepted (a mutant refusing `''` turns only C1 red);
   - that the shared plain-object check, rather than a falsy test, guards the stream route (a `!req.body` mutant turns only C1 red; no cell sends a JSON array or a string body to prove the difference, since N4's array is caught by the next check anyway);
   - that recipient elements are NOT checked.

   C1 pins the exact text, so every such edit turns it red and no regression slips today. The protection is textual only: once a later change rewrites these lines (and so must update C1), nothing behavioural holds the `''` acceptance or the choice of the shared check. A follow-up could add a behaviour cell for `''` (accepted). No change asked in this round.
3. **INFO. Point (a):** a type-only PUT accepts texts create refuses. The KQL builder sanitizes, the over-500 throw is caught on all three read paths, and the alert HTML is escaped. A QA and consistency issue, not an injection. Ticket candidate 2 in FOR-RECORDS.
4. **INFO. Neighbour, predates this change:** the PUT does not clear or regenerate `kql_query` when `condition_text` changes (`updateRiskCondition` spreads the update; regeneration happens only when the query is missing or stale by table). So an edited condition keeps running its old Log Analytics query. Read from source, not run. Ticket candidate 1; a neighbour of RD-893's measurement (1).
5. **INFO.** `email_recipients` elements are unchecked (Q-3): `[7,null,{}]` is stored, and the scheduler sends to `"7"` and `"[object Object]"` (it uses String(); null is dropped); it logs the failed sends. The new code comment ("a stored value never reaches a reader that expects another type") reads wider than the code: it holds for top-level types, for writes from now on. The seat said the same; it is not a reason to re-cut a frozen hunk.
6. **INFO. Code scanning:** alert #235's data-flow path lists the stream field read as a source (point (c)). The line is unchanged, and the local CodeQL read KEPT 0 / NEW 0. If the PR's scan names #235 or any alert as new: no merge, read it, never dismiss.
7. **INFO. First real Linux run (Q-8).** My Linux-shape runs (both files in the lane, and the whole suite 6504 / 409) are the closest local proxy. Both new files take their data folder from `persistentTempDir` (the PUT file directly, the stream file through `bootServer`), the same helper the hosted-green RD-878, RD-1007 and RD-1045 files rely on. No cell's premise is a `/tmp/` path. A red on a new cell there is a fix round.
8. **INFO. Records.** Q-6 (both stay open) agrees with the project rule (CLAUDE.md lines 298-302: Testing is for completed work). See FOR-RECORDS.md.

## Not run by the gate
CodeQL (relayed: the seat's local run); any hosted run (none exists for a pushed branch beyond npm-audit); real Linux or GNU userland; the Log Analytics path; the production setting on the stream route; Jira (not read, not written); the seat's own-shape plain verify (mine was the Linux shape, which covers the counts predicate).

## Before landing (Tuesday)
1. Open the PR from `b2121/lane1-validation` with `pr-title.txt` and `pr-body.md`.
2. Wait with `--min-checks 7`, including `build`, the FIRST Linux run. Its log must read `VERDICT: PASS — 6504/6504 tests passed across 409 suites`.
3. Land by merge commit pinned to 408b8655cbd360c8d09fe21ec70d944f56ec8d1b (never squash or rebase, C-190) and never press "Update branch" (strict is false).
4. The Deploy demo run must read both jobs skipped; approve nothing (C-224).
5. Main's javascript-typescript analysis at the merge commit must read 29.

See landing.txt.

Files in this folder: VERDICT.md, landing.txt, pr-title.txt, pr-body.md, FOR-RECORDS.md.

Scratch (dot-free, left in place): /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s330/g2125/
- clone, worktrees t/{base,head,mut,full}, rt/
- adv/ (the two adversarial test files)
- tools/ (gmut.py, gjudge.py, glane.sh, gfull.sh, runlane.sh, runfull.sh)
- logs/ (lane.out, full.out, full-verify-linux.log, per-run json and log)
- out/ (BASE and head server.js, main.sarif, alerts.json, workflows)
- gl/ (gitleaks inputs and outputs)

Nothing was written to the project checkout, Jira or GitHub. No PR and no push. Nothing deleted. No background process and no lock left.
