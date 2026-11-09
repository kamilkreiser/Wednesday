PR 2145: GO WITH NOTES; PR 2146: GO WITH NOTES; PR 2147: GO

# Gate 296 (tier 2, Sonnet): PRs 2145 (KS-2066 F3), 2146 (KS-2147), 2147 (KS-2148). Findings only. Nothing posted, pushed or mailed.

Method: the gate-295 blobless clone in this session's scratchpad (`.../scratchpad/r`, wrapper `g.sh`), PR heads at `refs/p/<n>`; a sparse worktree of `Blockchain/Dev` at develop d0b4825cc244 in `.../scratchpad/g296/w/dev`, `node_modules` symlinked from the project's install. Two environment fixes were needed (see NOT TESTED). Nothing written in !CODING. No `cd`, no `rm`. Load1 was kept under 8 before each run (it reached 13.7 during my one whole-suite run).

## PINS (git ls-remote origin, start 23:36:58 AEDT, end 23:53:48 AEDT, diffed): NO HEAD MOVED
develop d0b4825cc244; 2145 47cd344c6942; 2146 20a2e3b32aae; 2147 8a5ab2595c6e. All equal the commission's pins (`pins_start.txt` and `pins_end2.txt`, `diff` empty). Rounds 1-2 heads (2137, 2139-2144) were read again at 23:53:21 and equal gate 295's start pins (diff empty). All three PRs have merge-base f98afb113c2d with develop (`git merge-base`). Develop's move f98afb11..d0b4825c is 2 files, none of them our paths (`git diff --name-only`, grep count 0).

## Diff versus the held Spark diffs
Command: gate 295's `cmp.py` (last ```diff fence of the held READY file, +/- lines per file, against `git diff -U2 d0b4825cc244...refs/p/<n>`).
- KS-2066 (READY_KS-2066-...PASS-9of9) vs PR 2145: 1 file each, same file set, IDENTICAL. No difference.
- KS-2147 (READY_KS-2147-...) vs PR 2146: 1 file, IDENTICAL.
- KS-2148 (READY_KS-2148-...) vs PR 2147: 1 file, IDENTICAL.
Caveat (as in 295): changed lines only, not hunk headers or context.

---------------------------------------------------------------------------------------------------
## PR 2145 (KS-2066 F3): GO WITH NOTES
FOUND: one cell, `CONTROL KS-2066 F3: a rejected plain Error whose message quotes stored text logs the class Error and none of that text`, +11 -0, in `services/api-gateway/src/__tests__/ks1539-create-path-logs-a-thrown-allow-list-read.test.ts`.
TESTED / HOW:
1. Touched set: `git diff --numstat d0b4825cc244...refs/p/2145` = one line, `11 0 <that file>`. One commit, `git log` shows no other path. No product byte changed.
2. Green at head: vitest (api-gateway, `npm --prefix .../services/api-gateway test -- run <file> --reporter=verbose`): 7 of 7, the new cell listed as passing; develop 6 of 6. Also 7 of 7 twice with `--sequence.shuffle`.
3. My own mutant on `routes/verification.ts` line 877 (read at source: `log('warn', 'Connector allow-list settings read threw; ...', { route, errorClass: err instanceof Error ? err.constructor.name : typeof err })`): adding `message: err instanceof Error ? err.message : undefined` to the fields gives 2 failed, 5 passed (7): the new cell and `RED KS-1539 C2` (the SyntaxError cell). This is the seat's claim exactly ("5 of 7 passing"). Restored by `git checkout d0b4825cc244 -- <file>`; `git status` clean of the product path afterwards.
4. Merge: clean alone (tree 4fa0c628); clean in the three-PR chain; clean in the ten-PR chain with 2137, 2139, 2140, 2141, 2142, 2143, 2144 (final blob of the file equals PR 2145's head blob). No path overlap between our three files and rounds 1-2 (`comm -12`, 0). Open-PR census (below) shows no other PR on this path. Planted control: a synthetic develop commit adding a test at the same hunk site conflicts with 2145 (`merge-tree` rc 1, stages 1/2/3 listed) and merges clean with 2146.
5. Bodies and ticket comment 49d70444 (read from the seat's saved `push/pr_body_ks2066.final.md`, `push/linear_comment_ks2066.md`): "+11 -0", "6 to 7 cells", "5 of 7 with the mutant", "product file untouched", "F2 not in this PR", "Refs, KS-2066 stays open": all agree with what I measured. Not checked by me: the whole api-gateway suite 168 files 1880 to 1881 and the 25 tsc lines (not run, see NOT TESTED). Keys in title/body/comment/commit: KS-2066 only; no closing-form word + key (grep on all four texts, 0 hits).
Findings:
- G296-2145-1 (Low): the cell reads the log with `JSON.stringify(logs)` and the string QUOTED. A regression that adds the Error OBJECT as a field (`{ route, errorClass, err }`) keeps all 7 cells green: I ran that mutant (`..., err });` on line 877): 7 passed (7). `JSON.stringify(new Error(..))` gives `{}` because `message` is non-enumerable, so the text never appears in the stringified record even though a logger that formats Error objects (stack/inspect) would print the message. The cell therefore pins "message not logged as a string", not "message never reaches the log". The PR title and body say "never reaches the allow-list read's log line"; that is slightly wider than the assertion. Whether the real `log` helper serialises an Error field is NOT TESTED. Not a defect of the change; the stated mutant does turn it red. Suggest nothing blocking; a note on the wording or one extra assertion on the field set (`Object.keys(meta)` equals route + errorClass) if the seat wants.

---------------------------------------------------------------------------------------------------
## PR 2146 (KS-2147): GO WITH NOTES
FOUND: two cells N1, N2 (+ the helper `pollSiteThree`), +38 -0, in `packages/shared/src/__tests__/ks1972-event-indexer-poll-survives-an-unreadable-throw-at-the-rate-limit-check.test.ts`. Site 3 is the catch in `processTransaction` (event-indexer.ts lines 328-336).
TESTED / HOW:
1. Touched set: numstat `38 0 <that one file>`; one commit; `blockchain/event-indexer.ts` untouched (blob b7516622960b at develop and at the PR cut, `rev-parse`).
2. Green at head: `npm --prefix .../packages/shared test -- <file> --reporter=verbose`: 8 of 8 (develop 6 of 6); shuffled 3 times with the 2147 file: 20 of 20 each time.
3. My own mutants on the site-3 catch (restored each time with `git checkout d0b4825cc244 -- <file>`):
   - M1 (`if (false)`, a 429 is never a rate limit): N1 and N2 red, 6 of 8 pass. Matches the seat.
   - M3 (`try { rl = isRateLimited(err) } catch { rl = true }`): N2 red only, 7 of 8. Matches.
   - M4 (my addition: the 429 branch does not raise backoffMs): N1 red only.
   - M2 (the else branch does `void err;` instead of `handleError`): 8 of 8 pass, nothing red. Matches the seat's number.
4. M2 by reading the code (event-indexer.ts): `processTransaction` catch is `if (this.isRateLimited(err)) {...} else { this.handleError(err); }`; `isRateLimited` (lines 340-347) reads `err?.status_code`, `err?.statusCode`, `err?.response?.status`, `err?.message` with no guard, so an unreadable value throws at the `if`, never reaches the else, and leaves `processTransaction` for `poll()`'s catch (lines 199-216) where the read is guarded and `handleError` runs. The seat's reason is TRUE for the unreadable value. But the else branch IS reachable by a READABLE non-429 error (e.g. `new Error('boom')`), and no cell sends one to site 3 (C1 and C2 use `blocksLatest`, i.e. site 1; C3 is site 2). I ran a scratch probe cell (appended to the test file, then the file restored byte for byte from a saved copy): `pollSiteThree(new Error('boom'))` expects one onError and lastProcessedBlock 6. Unmutated: 9 of 9 pass. Under M2: the probe is red ("expected +0 to be 1"). So M2 is catchable; the PR leaves it uncaught. See G296-2146-1.
5. Merge: clean alone (tree 75681aeb), clean in the three-PR and the ten-PR chains (file blob equals PR head blob). Census: PR 2104 also changes this path and event-indexer.ts, but both blobs at 2104's head equal develop's (f711900ad9ca; b7516622960b): a merged original, not an open PR. Planted control (conflict with 2145, clean with 2146) described under 2145 item 4.
6. Bodies and comment 6145fe6f (saved copies `pr_body_ks2147.final.md`, `linear_comment_ks2147.md`; they are headed with the ticket key, PR number 2146): "+38 -0", "6 of 6 to 8 of 8", "N1 and N2 red for M1, N2 red for M3, M2 not caught", "isRateLimited throws first, so the value leaves site 3 and the outer catch handles it" (confirmed above), "Refs, ticket stays open": agree. The body says the cells "do not claim to pin" the else branch: honest. Keys: KS-2147 only in the four texts; closing-form + key 0.
Findings:
- G296-2146-1 (Low): the body presents M2 as an uncatchable mutation ("because an unreadable value never reaches that branch"). That holds only for the shape N2 uses. A one-line cell with a readable non-429 Error at site 3 (probe above) would catch M2, and nothing else pins the else branch of site 3 today. The PR does not claim to pin it, so this is a coverage note and wording note, not a defect: the sentence reads as "cannot be caught" when it is "is not caught by these two cells".
- G296-2146-2 (Info): N2's name says the block is "left unprocessed"; the assertion is `lastProcessedBlock === 5`, which also holds if the throw leaves any way. It pins the reading in event-indexer.ts lines 190-199 (the for-loop assigns `lastProcessedBlock = height` only after `processBlock` returns). Verified true by reading; no action.

---------------------------------------------------------------------------------------------------
## PR 2147 (KS-2148): GO
FOUND: four cells N1-N4 driving the public `verify()` with a DID resolver that rejects, +44 -0, in `packages/shared/src/__tests__/ks1973-vc-verifier-issuer-lookup-and-ed25519-catches-unreadable-throw.test.ts`.
TESTED / HOW:
1. Touched set: numstat `44 0 <that one file>`; one commit; `vc/verifier.ts` untouched (blob 04f24453c911 at develop and PR cut).
2. Green at head: 12 of 12 (develop 8 of 8), verbose list shows N1-N4 passing; shuffled 3 times: pass.
3. My own mutants on verifier.ts lines 464-470 (the resolver catch), each restored:
   - V1 (`errors.push(`...${String(error)}`)`, unguarded): 4 failed of 12: R1, R2, N2, N3. N1 and N4 green. Matches.
   - V2 (constant text changed to 'changed text'): 4 failed of 12: R1, R2, N2, N3. N1 and N4 green. Matches.
   - V3 (catch body `void error;`): 9 failed of 12 (N1-N4 all red).
   - V4 (prefix text changed): 9 failed. V5 (always the constant reason): 5 failed (R3, C1, C2, N1, N4).
   - V6 (my addition, at the verify() layer: `checks.issuerDID = true;` instead of `= issuerResult.valid`, line 137): N1, N2, N3, N4 red, 4 of 12, R1-R5 stay green. So the four new cells catch something the eight old cells cannot: the public-method wiring. The cells are not redundant.
4. N1 and N4 as the "readable-shape controls": green under V1 and V2, red under V3/V5, so they do discriminate. N2 and N3 are titled `control` although they pin the unreadable shapes (same label as the controls); the body says so ("pin today's behaviour, titled control"). Honest, not a finding.
5. Merge: clean alone (tree ee6cfb1e), in the three-PR and ten-PR chains (blob equal to PR head). Census: PR 2108 changes this path and verifier.ts, both blobs equal develop's (603600a422b3; 04f24453c911): merged original.
6. Bodies and comment 8b04dc0c (saved `pr_body_ks2148.final.md`, `linear_comment_ks2148.md`; PR number 2147): all numbers agree with the above (4 failed of 12, N1/N4 green, 8 to 12). Closing-form check: the PR's commit message contains the plain word "resolves" five times ("... resolves not verified, with ..."), each followed by "not verified", never a key. `grep -i -E "\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\b[: ]+(#?[A-Z]{2,}-[0-9]+|#[0-9]+)"` on the commit message: 0 hits. Title, body and comment: 0 hits for any closing-form word. The commit's only keys are KS-2148 (twice), after "Refs". The added test lines (4) also contain "resolves" (cell titles); GitHub and Linear read titles/bodies/commit messages, not file contents; keyword + key is absent regardless.
Findings:
- None above Info.

---------------------------------------------------------------------------------------------------
## The pre-existing red cell
`src/__tests__/wallet-signature.test.ts > verifyMessageSignature (CIP-8/CIP-30) - KS-278 > accepts a valid wallet signature over the message`: run on a develop-only tree (the worktree with all three PR files reverted to develop, `git status` clean): "1 failed | 4 passed (5)", `AssertionError: expected false to be true`, Node v26.8.1. Red on develop, not from these PRs. Recorded, not diagnosed.

## MERGE TREES (all on develop d0b4825cc244, `git merge-tree --write-tree` chained through synthetic `commit-tree` merges in the scratch repo)
- Alone: 2145 clean (4fa0c628), 2146 clean (75681aeb), 2147 clean (ee6cfb1e).
- All three: clean; `diff --numstat` develop vs merged = 38/0, 44/0, 11/0 on exactly the three files.
- Rounds 1-2 + round 3 (2137, 2139, 2140, 2141, 2142, 2143, 2144, then 2145, 2146, 2147): clean at every step; 14 files, +109 -12; the three round-3 files' blobs equal the PR head blobs. Path overlap rounds 1-2 vs round 3: 0.
- Open-PR sharing: census = every pull ref numbered 2060 and above (88 refs; `ls-remote` heads equal the refs held, plus 2146 and 2147), changed paths vs each one's own merge-base with develop (409 path/PR pairs). Sharing our paths: PR 2104 and PR 2108 only, both merged originals (blob equality with develop shown above). PR 2138 touches `services/originate/src/routes/verification.ts`, a different service from api-gateway's `routes/verification.ts`. No authenticated GitHub here: this cannot tell open from closed beyond blob equality; it covers 2060+ only. Control: PR 2127's three paths (`check_slot_credentials.test.sh`, `check-slot-credentials.sh`, `start-environment.sh`) appear in the census.
- Planted control: described under PR 2145 item 4.

## NOT TESTED (said, not inferred)
- The whole `packages/shared` and whole api-gateway suites with and without the PRs, and so the seat's counts (1623/1, 1625, 1627; 1880 to 1881; 168 files). My one whole-suite run (shared, on develop, `--maxWorkers=3`) is NOT comparable to the seat's: sparse worktree `Blockchain/Dev` only (no repo-root files), a `zod` 4.6.7 installed in scratch because the project's `node_modules` holds zod 3.25.76 and `packages/shared` needs `z.config`, and a `dist` built by `tsc` that printed zod type errors but emitted. Result there: 81 files, 4 failed files (openapi-415-injection and openapi-operation-ids fail to load; threadToken "different seeds" timed out at 81 s under load; wallet-signature), 2 failed tests of 1610. I did not run it again with the PRs. The new cells are test-only in three files nothing else imports, so I judge no other file can change; that is inference, not a measurement.
- tsc / typecheck (the 25 pre-existing lines), eslint, the platform suites, live stack.
- Whether the real api-gateway `log` helper serialises an Error object field (G296-2145-1).
- The posted PR bodies and Linear comments as posted (no `gh` login, no Linear tool): I read the seat's saved copies in `5_Project_History/2026-11-09_seatR-92nd/push/`, which may differ from what was posted. The Linear attachment census (each PR attached to exactly one ticket) was not checked. Comment ids 49d70444, 6145fe6f, 8b04dc0c appear in `push/comment_real_ks*.out`.
- The checker's own plant for PR 2145 (carried from the held READY by the seat, not in the PR). I used my own mutants as the commission asked.
- Another Node line for the wallet-signature cell.
- Spark shadow: not required (commission).
