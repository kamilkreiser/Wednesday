GATE B1727: GO WITH FINDINGS @ cd019f3 on main 37fb1bc

Gate G1 Tier 1 (Opus 5.5), independent of the builder: every row below was measured by this gate. Head cd019f382c63589c735b0b0bf1add22bfdebec10, main 37fb1bcbec2e19f2404774633349da76b75120d3 (`ls-remote` at 07:23:42 and the branches API at 07:29:13 both read these; Thu 19 Nov 2026, clocks from `date`). Open pull requests: 0.

Work folder `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s291/g1727/`:
- My own clone. Its push URL is set invalid and it was never pushed.
- Trees `head10`, `base12`, `mut9` and `vfy49`, all in jest slot 5 (band 23200-23839), printed by `worktreeSlot()` in each tree.
- No file of 18 or 19 Nov names slot 5 as taken. The only mention is the B1726 kit's line listing it as free (a program over 146 brief files, with controls: B1726 `new31` reads 13, g1724 `head13` reads 11 and `mut10` reads 18).
- `node_modules` is an APFS clone copy of the g1724 gate's install. `package-lock.json` blob 2d7dbece is equal at both heads, and `require('sqlite3')` loads (rc 0).

One lock acquisition: tag `b1727-gate`, acquired after 0 s at 07:28:29, through `nexusai-lock.sh jest` with `NEXUSAI_LOCK_BASE=locks-laptop-1017`. The chain printed `NODE_OPTIONS=[unset]`. The band read 0 listeners before every run and after the last one.

## Ruling
None is cited, and none is needed: two Low bugs, each turning a 500 into a 400 inside its own ticket's recommendation. A scan of all added lines and the five commit messages finds 0 lines attributing any choice to the product owner (regex `product owner|owner decided|ruled|ruling|decided by|the owner`; a control line fires). Every choice is written as "this change's default(s)", in the server.js comment, both test headers and the A5 and A7 bodies.

## Findings
| # | Severity | Finding | Recommendation |
|---|---|---|---|
| F1 | Minor (pre-existing, narrowed by this change) | The RD-523 exception matches the code STRING `AI_ENDPOINT_REDIRECT_REFUSED`. Only `AiEndpointRedirectError` sets it (`backend/llm/azureOpenAIAdapter.js:110`, constant message `:104`; the code base was grepped). But the openai SDK's `APIError` copies `code` from the endpoint's HTTP error body. Measured with `node` and no server: `APIError.generate(400 or 500, {error:{code:'AI_ENDPOINT_REDIRECT_REFUSED', message:<text>}})` has `.code` equal to that value. `namedAoaiError` passes it through unchanged (it carries a numeric status), and `chatErrorText` returns `"400 <text>"`. The control code `Other` gives the constant. So an AI endpoint that answers with that code can still put its own text in a stream error event and in the POST /api/chat `error` field (`server.js:7650`, unchanged). The dashboard writes the event's `message` with `innerHTML` (`static/js/index.js:3512`), and the adapter's own comment says why it avoids angle brackets. Before this change EVERY thrown text reached those sinks. Measured at BASE: GET stream with the model host answering 500 sends `500 "<marker> internal model failure"`; at head it sends the constant. The residual needs an administrator-configured endpoint that answers with exactly that code. | Land as is (strictly better than main). Follow-up: match `error instanceof AiEndpointRedirectError` (or `error.message === REDIRECT_REFUSED_MESSAGE`) in `chatErrorText` and at `:7595` and `:7650`, and escape `data.message` in the chat bubble. |
| F2 | Minor (out of scope, listed) | After this change, a thrown text still reaches a client on the chat routes by these paths, each measured at head in development: (a) POST /api/chat/stream with an unparsed body (vnd.api+json, text/plain) answers 500 from the final handler (`server.js:22486`, `sanitizeErrorForClient` `:22217`), and its `message` is `Cannot destructure property 'message' of 'req.body' as it is undefined.` The same holds at BASE (Q-6, out of this lane). (b) Malformed JSON on either POST route answers 400 from the same handler, with the parser's text in `message` (at BASE too; not a chat-route throw). (c) F1. All of (a) and (b) are development only: `Dockerfile:144` sets `NODE_ENV=production`, where the handler returns only the safe message. | Keep on the follow-up list (the PR body names them). The Q-6 follow-up should cover (a). |
| F3 | Minor (test text) | rd1007 R4's title says "and stores no user" but the cell asserts only status and body. The R4 request carries no email, so nothing could be stored, and this gate's probe measured stored false for it at BASE and head. N2 and N3 likewise do not read `listed`. No field is a constant written into both sides (no B1724 F3 class). | No change needed to land. |
| F4 | Observation (builder STATUS) | The builder's Corrections are judged true. Correction 1: four small ranges printed, against the kit. Its STATUS holds one dotted-quad-shaped string, at line 69: the Chromium version (first octet above 255). It holds no address. Correction 4: the alerts move 11 lines, not 2. Correction 6: two `rm -f` on `/tmp` files of its own, against HOLD 5; process only. | None. |

No Blocker, no Major.

## Measured rows
1. **SCOPE.**
   - `rev-list --left-right --count main...head` reads 0 5. `diff --numstat` lists exactly four paths: `backend/server.js` 20/9, `__tests__/rd1005-chat-message-not-text.test.js` 242/0, `__tests__/rd1007-user-add-unparsed-body.test.js` 127/0, `scripts/verify-expected-counts.json` 3/3.
   - Per commit: 7efc5c6 server.js 17/8, 3dc7807 server.js 3/1, 8dfd12a rd1005 242/0, a469e16 rd1007 127/0, cd019f3 counts 3/3. Parents are linear from 37fb1bc.
   - The head server.js blob is dc23d449baf3f4d7892dc3e0773de35dca703267 (equal to Tuesday's). The `diff -U0` hunks are exactly the kit's: `@@ -1429,0 +1430,9`, `@@ -3607 +3616,3`, then eight one-line swaps at main 7179, 7656, 7668, 7851, 7858, 7867, 7977, 7984. Hunk function headers name only the POST /api/chat, GET and POST /api/chat/stream, and user-add routes.
   - The kit's 9-line frozen block occurs byte-exact once in head, directly after `chatMessageTooLong`'s closing brace.
   - RD-994 block: BEGIN..END 93 lines, sha256 prefix f0bc2a77b68d4743 at main and at head (control: one changed byte gives b18b9d850b2cb784). The mount `app.use(auditFieldGuard);` count is 1.
   - `function isPlainRequestObject(` is defined once at both (calls 1 at main, 2 at head). Non-ASCII characters: 1256 at both.
   - `merge-tree --write-tree main head` is clean, tree 8655bdd0, equal to the head tree. Counts 6009/380 become 6041/382.
2. **RD-1005 REFUSAL.** These are live probes from my own untracked probe file. One open-shape boot per tree with a wire-level model stand-in. Inference is counted at the stand-in per request.
   - POST /api/chat and POST /api/chat/stream, for each of: JSON array, object, number, `true`, `{toString:'..'}`, nested `{toString:{toString}}`, `{toLowerCase,length,trim}`, a duplicate JSON key with the array last, and form `message[]=` (one and two), `message[a]=`, `message=a&message=b`, `message[toString]=`, `message[length]=`, `message[__proto__][x]=`:
     - BASE: 500 with `details` `message.toLower...` (POST chat), or 200 with `Analysis error: (query || "").toLowerCase is not a function` (POST stream).
     - Head: 400 `{"error":"Message is required"}`, JSON, inference 0.
   - `false`, `null`, `''`, form `message=`: 400 at both.
   - GET /api/chat/stream with `message=a&message=b`: BASE 200 with `Stream error: query.toLowerCase is not a function`; head 400, inference 0. `message[]=` (one or two), `message[a]=`, `message[toString]=`, `message=` and no message: 400 at both (the simple query parser keeps bracketed keys literal).
   - JSON with a BOM, a duplicate key with the string last, and `'   '`: 200 at both, an ordinary string message (unchanged).
   - Ordinary requests on all three routes: 200 at both, `done` on the streams.
   - No non-string shape reached a model call, a `.toLowerCase`, or a 200 stream at head.
3. **RD-1005 DISCLOSURE.**
   - POST /api/chat with an unparsed body (vnd.api+json, text/plain): BASE `details` `Cannot destructure ...`; head `details` is the constant.
   - GET stream with the model host answering 500 with a marker: BASE sends the marker text; head sends `Error processing chat message`. With the connection reset: BASE `Connection error.`, head the constant.
   - POST /api/chat and POST stream with the model failing: 200 at both (the routes fall back; no error event, so the POST-stream sinks are proved by U and C only, as the builder said for H2).
   - Remaining paths: F1 and F2. The thrown text still reaches the server log: `logger.error(..., error)` is the first line of each of the five catches (`server.js:7644`, `:7861`, `:7868`, `:7987`, `:7994`), so the constant costs an operator nothing.
   - The RD-523 exception: only `AiEndpointRedirectError` sets the code in the code base. The endpoint-body path is F1.
4. **RD-1007.** Enforced shape, seeded administrator and viewer. "Stored" is read from GET /api/auth/users after each request.
   - Administrator, merge-patch+json, vnd.api+json, text/plain and no content type with no body: BASE 500 `Failed to add user`; head 400 `Email, name, and password are required`. Stored false at both.
   - JSON with no body, `[]`, `[{...}]`, and `{"__proto__":{...}}` (an own key from JSON.parse): 400 at both, stored false.
   - JSON `null` and `"x"`: 400 `Invalid request` from the strict JSON parser before the route, at both (pre-existing).
   - Form-urlencoded add and ordinary JSON add: 200, stored true, at both.
   - Viewer: 403 `Admin access required` for every shape that reaches the route (10 of 12), stored false. The two the JSON parser refuses first get 400, at both.
   - Reusing `isPlainRequestObject` is correct here. It accepts any non-null, non-array object, so a null-prototype or class-instance body is read by destructuring like any other. The parsers never hand the route a prototype-polluted object (the `__proto__` key stays an own key). Plant P8 proves the route calls the shared function, not a copy.
5. **CELLS.**
   - Head, run 1 and run 2: 2/2 suites, 32 cells, 32 passed (rd1005 23, rd1007 9).
   - Plants in `mut9`, each reverted to blob dc23d449baf3 (8 of 8 EQUAL), received red:
     - P1: R01-R05, C2.
     - P2: R11, C2.
     - P3: R06-R10, C2.
     - P4: E1, U1, U3, H1.
     - P5: U2, plus rd523 C1 and E4 (22 green, 2 red of 24 rd523 cells).
     - P6: E1, C1.
     - P7: rd1007 R1-R4, C1.
     - P8: rd1007 R1-R4, plus rd969 H8 only.
   - Correction 2 is true: under P4, `String(null && null.message)` is `null`, so U3 must go red, and it did. Correction 3 is true: rd969's own comment (`__tests__/rd969-three-routes-empty-request.test.js:148`-`:153`) says H6 and H7 cannot tell the check from always-yes. Each cell's proof stands.
   - At main, the U cells find no helper, C1 reads [1,2,1,1,0] old sinks and calls, C2 reads [3,0], and rd1007 C1 reads [0,1,1]: all red. My BASE probes reproduce every R, E1, H1 and rd1007 R1-R4 red answer.
6. **FULL VERIFY.** Ran in `vfy49` at head, tree 8655bdd0, porcelain empty, band 0. Command: `env -u NODE_OPTIONS -u MIN_TESTS -u MIN_SUITES -u VERIFY_EXPECTED_FILE npm run verify -- --maxWorkers=2`, run 07:32:56 to 07:54:46. Result: `VERDICT: PASS - 6041/6041 tests passed across 382 suites`, rc 0, EADDRINUSE 0, porcelain after empty, band 0 after. The pair equals the committed counts 6041/382. Lock released 07:54:47 (one acquisition, lock rc 0). Node is local v26 against hosted Build 24.
7. **CODEQL (local CLI v2.27.4, javascript, BASE and head databases):**
   - `javascript-code-scanning.qls`: 4 and 4 rows.
   - `javascript-security-extended.qls`: 29 and 29 rows, 13 of them on server.js. After the line shift (+9 after main 1429, +11 after main 3607): 0 new, 0 gone.
   - `js/user-controlled-bypass` sits at main 3609 (x3) and 3620, and at head 3620 (x3) and 3631. Alerts 229-231 and 232 move 11 lines, with nothing closed or changed.
   - By hand over the added lines: no `RegExp(`, `eval(`, `new Function`, `child_process`, `innerHTML`, timer or skip token, or secret-shaped assignment. gitleaks over `git log -p main..head`: no leaks (control: 1 leak found).
8. **TEXT.**
   - Over added lines and the five messages: name scan 0, with `(?<![A-Za-z])name(?![a-z])` over the standard ban list (control: `_by_<name>_` fires for all, `Kamikaze` does not).
   - B-number, seat and coordinator ids: 0. Card and decision ids: 0 (controls fire).
   - Non-ASCII: 0. Cf and bidi characters: 0. Dotted quads: 0. Ticket keys: only RD-1005, RD-1007 and RD-523.
   - Trailers read `Co-Authored-By: Claude Sonnet 5.5` (the builder's model).
   - The builder's STATUS holds no address (F4).

Deploy: `deploy-demo.yml:26`-`:32` triggers on a push to main and path-ignores only `**.md`, `docs/**` and `tests/**`. This merge touches `backend/**` and `__tests__/**`, so a Deploy demo run WILL start. Its jobs are gated on `vars.CI_DEPLOY_ENABLED == 'true'` (`:53`, `:91`) and must read skipped (`landing.txt` step 4).

## FOUND / TESTED / NOT TESTED / HOW
- FOUND: F1 to F4 above. The builder's measured claims are graded true where re-measured: scope, blobs, counts, cell colours at both heads, all eight plants, Corrections 2, 3 and 4, and the RD-994 prefix.
- TESTED: everything in rows 1 to 8, in my own trees inside one lock acquisition, NODE_OPTIONS unset, band empty.
- NOT TESTED:
  - Hosted Build and hosted CodeQL. Hosted CodeQL uses default setup; there is no workflow file, and local security-extended stands in.
  - Linux; the production setting (only its handler source was read).
  - A browser render of the chat bubble.
  - A live spoofed-code endpoint (F1 is proved at unit level only).
  - The POST-stream sinks over HTTP: unreachable with a failing stand-in, so they are proved by U and C.
  - The Deploy demo run.
  - The census of 30 other unguarded reads (taken from the builder's list, not re-run).
- HOW: `git` read verbs and `merge-tree` in my own clone; Python and node scripts under `work/`; two untracked probe test files (`probes/`) copied into `head10` and `base12`; `work/plant.js` with line-anchored, content-asserted plants; `work/chain.sh` under `nexusai-lock.sh`; the CodeQL CLI on archived trees; gitleaks.
