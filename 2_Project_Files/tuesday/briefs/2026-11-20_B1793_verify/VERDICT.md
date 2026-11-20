GATE B1793: GO WITH FINDINGS @ b0c914d on main 74b58fd

Independent review, gate G1 Tier 1. Lane N-M, RD-1008: chat error text and the stream error event. Branch
`b1771/nexusai-lane-nm-chat-error-text`, head `b0c914dee0932c55f16374f98b6f853a96df4b14`, lane BASE
`98e6a4d72f5745a17438bdd2788cff5872f6fcaf`, main now `74b58fd5f623ac825133e1980e8b2d8763b2c108`.

Clocks (AEDT, 2026-11-20, from `date`):
- first 18:21:01;
- jest lock acquired 18:35:20 and released 19:06:56, one acquisition;
- Jira read 18:32:47.

Every jest number, probe and verify below came from Node v24.22.2 (npm 11.19.1) first on PATH, with `NODE_OPTIONS`
unset. The browser probe and the unit probes outside the lock ran on Node v26.13.0; the matrix program ran on v24.22.2.

Trees: my own clone (push URL `invalid://no-push`) under
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s300/g1793/`. Worktrees there, all on jest slot 10 (band
26400-27039), printed by the project's own `worktreeSlot()`:
- `h10`: the head;
- `b3`: the BASE;
- `m13`: plants;
- `v3`: the verify.

`node_modules` is symlinked to the builder clone's (not reinstalled: no registry access).

Blocker 0 | Major 0 | Minor 5 | Info 6

## Findings

| Severity | Finding | Recommendation |
|---|---|---|
| Minor | F-1 (item 4, the coverage gap). Each of the five route-side class checks, reverted alone (P2 to P6), turns only the source cells C1 and C2 red. No HTTP cell and no probe row of mine shows endpoint words. C1 and C2 really read the source, but they are not behaviour controls. A revert that keeps the class-check text and adds `\|\| (x && x.code == 'AI_ENDPOINT_REDIRECT_REFUSED')` passes both (P2q to P6q together: C1 and C2 green, only H3 red; P3q or P4q alone would be caught by nothing). A behaviour-preserving rewrite trips C2 (P4r: C2 red, every behaviour row unchanged). Two of the five layers have a visible single-revert effect that no committed cell asserts: P4 and P5 alone change the POST answers from the rule-based fallback to the "I encountered an issue processing your query" text. P2, P3 and P6 alone are dead layers for this input. | Not a landing blocker: no single revert lets an endpoint's words out (measured), and every pair or triple that does is caught by H3, H4 or U cells. For the records, three cells. (a) A unit cell that reads each of the six predicates from the source and evaluates it on errors built by the real client library (this gate's `progs/matrix.js` form): catches every single revert, the `==` forms included. (b) H3 and H4 assert the positive answer (the rule-based fallback served): catches P4 and P5 alone. (c) One H cell on the user-cost or insights path of POST /api/chat: reaches the outer catch (F-5). |
| Minor | F-2 (item 5, sibling, outside the lane, pre-existing). The tool-call status label at `static/js/index.js:3523` can be filled by an AI endpoint today. A stand-in endpoint answered with a `search_users` call whose `pattern` held an image tag with an error handler. `POST /api/chat/stream` forwarded it in the `tool_call` event (`backend/server.js:7950`; the adapter passes the parsed arguments at `backend/llm/azureOpenAIAdapter.js:313`), at the BASE and at the head alike. In a real local Chromium the page's own stream reader wrote it as markup: one `img` created and its handler ran. RD-1008's acceptance names the stream error event only, so this is not a NO GO. The hosted content security policy was not measured (RD-1014 says the strict policy is the default and blocks inline handlers). | Candidate ticket, security, Medium (the same threat model as RD-1008: an endpoint the administrator configured). Fix shape: `escapeHtml` on the label's argument values and on `data.name`. Line in FOR-RECORDS.md. |
| Minor | F-3 (item 3, text). Commit A1 `495ffce3` says the only texts that change "now read the constant". That holds for GET /api/chat/stream. On POST /api/chat and POST /api/chat/stream, measured over HTTP, the user now gets the ordinary rule-based fallback answer, not the constant. The builder's STATUS states the behaviour change correctly (BLUF (b)). | No history rewrite. The merge body and the PR body written here say it plainly, and FOR-RECORDS.md tells the records seat that the ticket's "gives the constant" holds for the GET route only. |
| Minor | F-4 (item 9, process). The builder changed a kit STOP rule on its own reading instead of stopping to ask (Corrections 4; HOLD 31's "a must-be-red plant that stays green after two runs: STOP"). It was open about it and recorded every miss. | Product effect on safety: none (F-1 measured that no single revert leaks). It is how the F-1 gap reached the gate unasked. A kit rule changed by the seat should be a STOP question. |
| Minor | F-5 (records). The kit's MUTATIONS row P3 says the outer catch of POST /api/chat "is reached only by an unparsed body". That is false. A question on the user-cost or quick-insights path calls the analysis outside the inner try (`backend/server.js:7281`, `:7409`). At the BASE that path answered 500 with the endpoint's words in `error` and `details`; with P3+P4+P6 planted at the head it does again. No committed HTTP cell drives that path. | Correct the table in any kit that reuses it; covered by F-1 (c). |
| Info | I-1. `GET /api/ai/status` returns an AI endpoint's error text in `details.error` (the model-list health check copies the SDK message, for example `400 <endpoint text>`). Measured, the same at the BASE and at the head. The setup wizard writes it through its own escape (`static/js/first-run-setup.js:417-419`). | Candidate ticket, Info or Low (FOR-RECORDS.md item 4). |
| Info | I-2. The adapter's own `isRedirectRefusal` (`backend/llm/azureOpenAIAdapter.js:121-127`) renames a stream error event that carries the code, or the message `unexpected redirect`, into the refusal class. It does the same for an `event: error` frame. The user reads the refusal's words, never the endpoint's. Measured over HTTP on GET /api/chat/stream, the same at the BASE and at the head. | As the kit's Q-4: candidate ticket, Low. |
| Info | I-3 (item 6). F3's waits. The 300 ms after each answer is not load-bearing: the stand-in logs the request before it answers, and the server answers the client only after the SDK call ends (every head row read `reached` of 1 or more). The 5 s warm-up wait: here 9 (BASE) and 14 (head) warm-up model calls landed in the first 5 s, and 0 warm-up pings after it. On a slower machine a late warm-up call can make `reached` true for a cell whose route never reached the model, which weakens the control. The absence assertions are unaffected. | Optional: count only calls whose body holds the cell's question. |
| Info | I-4. A message holding a null byte: `escapeHtml` keeps it and the HTML parser drops it on the way back. The bubble shows the rest as text, with no element. | None. |
| Info | I-5. Heads: 15 `wip/*` heads match the builder's three prefixes. 13 touch a lane file, as its census said; `wip/s65-rd464-r3-1` and `-r3-5` do not. Last commits 2026-09-17 and 2026-09-18, behind main by 1052 to 1062, 0 open pull requests. None is live work. | None. |
| Info | I-6 (gate's own process). One `gh` read carried a stray redirect to `/tmp/dummy` (150 bytes, a run list). I moved it into my scratch `_quarantine/`. My probe renamed its 20 temporary data directories instead of removing them; I moved them into `_quarantine/probe-tmpdirs/`. Nothing was deleted. Slot 10: every slot 0 to 18 appears somewhere in the loose brief text of 18 to 20 Nov. Slot 10 is no seat's "yours is" slot and no gate's slot on those days, and it is not 17. Its band was empty before and after. | None. |

## Answer on item 4 (the open judgment)

**The builder's reading is sound on safety and unsound on process.**

On safety, it is right that the POST chat routes are guarded in depth. A hostile code error must pass three layers
before its words reach the caller:
1. a first rethrow (`:9019` on the early model-first path, which every route variant here took, or `:9406`);
2. the outer rethrow (`:9673`);
3. the route's own text choice (`:7599`, `:7654` or `chatErrorText`).

The builder's note says "two layers"; it is three. Measured over HTTP: no single revert lets an endpoint's words out
on any of five route paths. That includes the user-cost and insights paths of POST /api/chat, which the builder did
not drive.

Every leak needs a pair or triple:

| plants | leaks on |
|---|---|
| P2+P4+P6, P2+P5+P6 | POST /api/chat (inner path) |
| P3+P4+P6 | the user-cost and insights paths |
| P1+P4+P6, P1+P5+P6 | POST /api/chat/stream |

Each such combination is caught by H3, H4 or the U cells. For example, P2+P4+P6 turns C1, C2 and H3 red.

On process, changing "any predicted-red cell green: STOP" to "a measured-column miss or a plant no cell catches" was
a change to the kit's rule. It should have been a STOP question to Tuesday.

**C1 and C2 are real reads of `backend/server.js` text, but they pin text, not behaviour:**
- a behaviour-breaking revert that keeps the text slips past both: P2q to P6q together left C1 and C2 green, and only
  H3 caught it;
- a behaviour-preserving rewrite trips C2 (P4r).

So the five route-side layers have no behavioural proof, one by one. That is F-1, Minor, with the three-cell fix
shape for the records. It is not a Blocker, because no single reverted layer lets an endpoint's words out at HTTP
level.

## Item 1. SCOPE (measured by `progs/scope.py` over my clone)

- **Paths:** exactly the 7 paths: `PATHS EQUAL TO THE 7 True`.
- **`backend/server.js`:**
  - 7 added and 6 removed lines;
  - every removed line is one of the six comparison texts (6 distinct);
  - every other line is byte-equal (head rebuilt from the BASE minus the removed and plus the added lines: True);
  - removed at BASE `backend/server.js:1437`, `:7598`, `:7653`, `:9018`, `:9405`, `:9672`;
  - added at head `:68`, `:1438`, `:7599`, `:7654`, `:9019`, `:9406`, `:9673`.
- **`static/js/index.js`:** one line at `:3529`; the only change is `${data.message}` to `${escapeHtml(data.message)}`
  (True).
- **The move of main.** The commit `74b58fd5` (PR 237) changed `HISTORY.md` only (+19, gh api). I rebuilt main's tree
  from the GitHub blob of `HISTORY.md` over the BASE tree. The sha came out equal to main's tree
  (`d9e56e5bda1b9c642c147ecb7209615234fd4936`). A trial merge (`git merge-tree --write-tree`) of the head into a
  scratch commit holding that tree reads rc 0, clean (tree `a4116b97b1d9`). The merged tree differs from the head's
  tree by `HISTORY.md` only.
- **Can the move change what this lane's checks read?** Only through `HISTORY.md`. Four tests read it (`rd385`,
  `rd503`, `boot-probe-log-redaction`, `image-content-exposure`), and PR 237's own Build passed on that `HISTORY.md`.
  CodeQL scans no `.md`. The hosted Build on the PR merge ref is the proof for the merged tree.
- **Compare API at 18:21:35:** main `74b58fd5`; b1771 ref = head; diverged, ahead 5, behind 2; merge base the BASE;
  5 commits; 7 files with the stated numstats; 0 open pull requests.

## Item 2. THE SERVER HALF (attack)

**Every place an error's words go to a caller, enumerated by program** (`progs/sinks_server.js`: route spans
by registration, transitive reach to the adapter by name).

`chatErrorText(` is called at:
- `backend/server.js:7671` (POST /api/chat `details`, development only);
- `:7866` and `:7873` (GET stream);
- `:7992` and `:7999` (POST stream).

The class keeps its message at `:7600` and `:7656`.

Other routes that reach the adapter and write an error message:
- `POST /api/validate-quick-question` `:20798` (development only; its analysis no longer rethrows a hostile code
  error);
- `GET /api/ai/status` `:19382` and its `details` (I-1);
- `POST /api/setup/ai-test` `:17154`;
- `GET /api/service-check` `:17956`;
- `GET /api/setup/validate-all` `:18098`, `:18140`, `:18300` (data-source and storage errors, not the model).

**Can a hostile endpoint choose the MESSAGE of an error that ends up an instance of the class? No.**
- The constructor always passes the adapter's fixed text to `super` (`azureOpenAIAdapter.js:106-113`).
- No code assigns `.message` on an error in `server.js`, the adapter or `aiEnabled.js` (count 0; control fires).
- `gateAdapter` passes errors through unchanged.
- `queryAI` rethrows the raw error (`server.js:10053-10055`).
- `server.js` has 0 `.cause` reads.

**Unit probe** (`progs/unit_adapter_probe.js`): the real adapter against a hostile loopback stand-in, 10 inputs
times 3 call shapes. Every renamed error (a stream data error with the code, an `event: error` frame, a stream error
with message `unexpected redirect`, a real redirect) carries the adapter's words. Every HTTP-status error stays an
`APIError`, which the head maps to the constant.

Edge shapes, each run through the head's `chatErrorText`:

| shape | head result |
|---|---|
| a subclass | the class's words (still the constant text) |
| a second module instance (cache cleared in the probe process) | the constant (fails closed) |
| an error wrapping the class as `cause` | the constant |
| a string rejection | the constant |
| an instance whose message was overwritten | would show the text, but no code path does that (above) |

**HTTP probe** (`progs/g1793-probe.test.js`, the real server, booted twice). 10 inputs on 5 route paths:
- GET stream;
- POST /api/chat, inner path;
- POST /api/chat, user-cost path;
- POST /api/chat, insights path;
- POST stream.

Results:
- At the head, 0 endpoint words in any chat answer or error event, for every input.
- At the BASE, the HTTP 400 and HTTP 500 code bodies leaked on all 5 paths (10 rows).
- The tool-call event carrying a model-chosen argument (F-2) is the only endpoint-chosen string in an event at the
  head. It is not error text; a model's answer chunks are endpoint words by design and the page escapes them through
  `formatAIResponse`.

**Verdict on item 2:** no Blocker.

## Item 3. THE BEHAVIOUR CHANGE: MATRIX before and after

**Decision at the six sites, old/new** (`progs/matrix.js`, Node 24): the predicates are read from each tree's own
source lines and evaluated on inputs built by the real `openai` and the real adapter. Columns in the order of the
BASE lines `1437 7598 7653 9018 9405 9672` (head `1438 7599 7654 9019 9406 9673`).

| input | decisions old/new | chatErrorText old | chatErrorText new |
|---|---|---|---|
| the real refusal | T/T at all six | the refusal words | the same |
| HTTP 400, body code + HTML | T/F at all six | `400 <img ...>hostile` | `Error processing chat message` |
| HTTP 500, body code + HTML | T/F at all six | `500 <img ...>hostile` | the constant |
| stream error event with the code, no status (renamed by the adapter) | T/T at all six | the refusal words | the same |
| an ordinary TypeError | F/F | the constant | the same |
| HTTP 400, code Other | F/F | the constant | the same |
| a plain Error with `.code` set by hand | T/F | `by hand` | the constant |
| a plain object `{code, message}` | T/F | `obj message` | the constant |
| null | F/F except `:7653` THROWS/F | the constant | the same |
| undefined | F/F except `:7653` THROWS/F | the constant | the same |

**What a user saw before and sees now, measured over HTTP** (input by route; the hand-built rows and null cannot be
sent by an endpoint).

| input | GET /api/chat/stream | POST /api/chat (inner) | POST /api/chat (user-cost / insights paths) | POST /api/chat/stream |
|---|---|---|---|---|
| real redirect | refusal words / refusal words | refusal words / refusal words | 500 refusal words / same | `Analysis error: ` + refusal words / same |
| HTTP 400 code + HTML | **endpoint words** / constant event | **endpoint words** as the answer / rule-based fallback answer | **500 with endpoint words in error and details** / 200 rule-based answer | **`Analysis error: ` + endpoint words** / streamed fallback answer |
| HTTP 500 code + HTML (SDK retries: 3 model calls) | **endpoint words** / constant event | **endpoint words** / fallback answer | **500 endpoint words** / 200 answer | **endpoint words** / fallback answer |
| stream data error with the code; `event: error` frame; stream error `unexpected redirect` | refusal words / same (I-2) | server text "I tried multiple lookups..." / same | same / same | streamed answer / same |
| HTTP 400 code Other; HTTP 400 message `unexpected redirect`; connection dropped | constant event / same | fallback answer / same | answer / same | fallback answer / same |
| tool call with a hostile argument | answer / same | answer / same | answer / same | **the argument in the tool_call event / same (F-2)** |

**Does a real refusal lose its refusal? No.** The real redirect reads the refusal words on all 5 paths at the head.
A fallback answers only for errors that are not the class, from the same data the ordinary-failure rows use. Nothing
new is shown.

**RD-516 and RD-523 still pin the real refusal end to end:**
- rd523, rd516 and rd1005 at the head: 3 suites, 78 cells, all green.
- Plant R1 (the helper always answers the constant) turns red rd523 C1, rd523 E4 and rd1005 U2.
- Plant R2 (the three rethrows disabled, so a real refusal falls back on the POST routes) turns red rd523 C1, C2 and
  E4.
- rd516 caught neither: its cells cover the ai-test path.

## Item 5. THE BROWSER HALF (real browser)

**How:** the project's Playwright Chromium 151.0.7922.34, launched by the guard's own `launchBrowser`, opened a local
file page, offline. 0 non-file requests were made. The page runs the real `escapeHtml`, `readAiDisabledRefusal` and
`askAIAssistantStreaming`, lifted from `static/js/index.js` of each tree, with a fetch stub that streams one
`error` event. A handler or script that runs sets `window.__x`, which is reset before each case.

| string | head: ran / img / script / other elements / bubble text equals what was sent | BASE (control) |
|---|---|---|
| img with an error handler (cell B1) | 0 / 0 / 0 / 0 / true | ran, 1 img |
| script element (B2) | 0 / 0 / 0 / 0 / true | 1 script element (inserted scripts do not run) |
| character references (B3) | 0 / 0 / 0 / 0 / true | text differs |
| attribute-breaking `"><img ...>' onmouseover='...` | 0 / 0 / 0 / 0 / true | ran, 1 img |
| entity-encoded markup | 0 / 0 / 0 / 0 / true | text differs |
| null byte around markup | 0 / 0 / 0 / 0 / false (the NUL is dropped, I-4) | ran, 1 img |
| 200,000-character string with markup | 0 / 0 / 0 / 0 / true | ran, 1 img, 1 other |
| svg with a load handler | 0 / 0 / 0 / 0 / true | 1 svg |
| undefined message | 0 / 0 / 0 / 0 / true (reads empty) | text differs (`undefined`) |

**Where the value sits:** it is element content only, the text of `<span class="text-danger">` (`index.js:3529`).
The quotes `escapeHtml` leaves cannot matter there, and the attribute-breaking case created nothing.

**Sibling writes of server- or model-supplied text in the chat region** (all `static/js/index.js` unless named):

| line | what is written | who can choose it today |
|---|---|---|
| `:3523` | the tool-call label | **an AI endpoint**, measured end to end (F-2) |
| `:3466` and `:3478` | `data.message` of the thinking and generating events | nobody: server constants (`backend/server.js:7728`, `:7823`, `:7901`, `:7920`) |
| `:3470` | sub-query types | nobody: constants from `decomposeComplexQuery` (`backend/server.js:717-745`) |
| `:3474` | the model name | the server's model configuration; not an endpoint, not a viewer |
| `:3569` | `error.message` of the catch | nobody: the page's own `HTTP <status>` or a fetch error |
| `first-run-setup.js:1486`, `:4127`, `:4240` | `data.message` of the wizard's answers | an administrator's own setup screen; RD-1014's first-run rows |

## Item 6. CELLS AND MUTANTS (jest JSON judged; suites equal to paths passed)

**Runs** (BASE: the three files copied in untracked):

| run | where | suites / cells | result |
|---|---|---|---|
| red-base | BASE | 3 / 21 | 14 failed, 7 passed |
| new-head-1 | head | 3 / 21 | 21 passed |
| new-head-2 | head | 3 / 21 | 21 passed |
| refusal-head | head | 3 / 78 | 78 passed |

EADDRINUSE 0 in every log. The red set at the BASE: B1, B2, B3, U2, U3, U4, U7, C1, C2, C4, H1, H2, H3, H4. That
equals the kit's table, reproduced on Node 24.

**H cells' answers at the BASE:** H1 and H2 held the endpoint's 400 and 500 text; H3's body was the endpoint text;
H4's events ended in an error event; H5 held the constant.

**H cells' answers at the head:** H1, H2 and H5 held the constant; H3 got the fallback answer; H4 got a streamed
fallback answer. `reached` was true in all ten.

**The rd1005 rewrite is the narrowest:**
- one import line;
- the class bound in the lifting context;
- U2 rewritten in place (+5 -4);
- U1, U3 and the cell count are unchanged.

U2 now asserts that the class keeps its words. A helper that answers the constant for everything turns it red (plant
R1: rd1005 U2 red).

**No asserted field is a constant on both sides:** every compared field is computed in the cell (helper output,
element counts, stand-in log, response text). B4's "before" is built from the old template in the cell, which is a
control.

**Plant table** (head, `m13`; F1 and F3 at every plant, plus my probe on one hostile input; each plant reverted and
proved equal to the HEAD blob: `reverted-equal True` 20 times):

| plant | committed cells red | probe paths that leaked endpoint words |
|---|---|---|
| P1 | U2 U3 U4 U7 C1 C2 H1 H2 | GET stream |
| P2 | C1 C2 | none |
| P3 | C1 C2 | none |
| P4 | C1 C2 | none (POST answers turn to "I encountered an issue" on all four POST paths) |
| P5 | C1 C2 | none (the same on the inner, insights and stream paths) |
| P6 | C1 C2 | none |
| P4+P6 | C1 C2 | none (POST /api/chat "Sorry" constant; user-cost and insights 500 constant) |
| P5+P6 | C1 C2 | none |
| P2+P4+P6 | C1 C2 H3 | POST /api/chat inner |
| P2+P5+P6 | C1 C2 H3 | POST /api/chat inner |
| P3+P4+P6 | C1 C2 | **user-cost and insights paths (500 endpoint words); no H cell** |
| P3+P5+P6 | C1 C2 | insights path; no H cell |
| P1+P4+P6 | U2 U3 U4 U7 C1 C2 H1 H2 H4 | GET stream, user-cost, insights, POST stream |
| P1+P5+P6 | U2 U3 U4 U7 C1 C2 H1 H2 H4 | GET stream, insights, POST stream |
| P2+P3+P4+P5+P6 | C1 C2 H3 | inner, user-cost, insights |
| P2q..P6q (text kept, `==` test added) | **H3 only** | inner, user-cost, insights |
| P1q..P6q | U2 U3 U4 U7 H1 H2 H3 H4 | all five |
| P4r (behaviour kept, text changed) | **C2 only** | none |
| R1 (refusal words dropped) | rd523 C1 E4; rd1005 U2 | not run |
| R2 (refusal rethrows disabled) | rd523 C1 C2 E4 | not run |

## Item 7. FULL VERIFY (head, Node 24)

- **Command:** `npm --prefix v3 run verify -- --maxWorkers=2`, with Node v24.22.2 and npm 11.19.1 first on PATH, under
  `env -u NODE_OPTIONS -u MIN_TESTS -u MIN_SUITES -u VERIFY_EXPECTED_FILE`.
- **Tree:** the head `b0c914d`, tree `d3658fe53749aae4d1daaf0b1e598031549b1168`; porcelain empty before and after.
- **Result:** `VERDICT: PASS - 6216/6216 tests passed across 393 suites (jest exit 0)` (the tool prints an em dash).
  That equals the committed pair 6216/393 (6195 + 21, 390 + 3). rc 0. EADDRINUSE 0.
- **Band:** `lsof` of 26400-27039 read 0 listeners before and after the verify, and before and after every step.
- **Node 24 against the builder's v26.13.0:** no difference.
- **Lock:** one acquisition under the builder's base, `session-tools/locks-laptop-1017` (STATUS Chain log, the same
  `nexusai-lock.sh jest <tag>` form). Tag `b1793-gate`, acquired after 0 s with the queue empty and no NexusAI pane
  live.
- **Load:** load1 4.83 at the start and 2.24 before the verify, both under 7.

## Item 8. CODEQL (`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/tools/codeql/GATE_STEP.md`)

`pr_codeql_check.sh --repo datasecau/Reporting_Dashboard_Au --checkout <my scratch clone> --base 98e6a4d72f5745a17438bdd2788cff5872f6fcaf --head b0c914dee0932c55f16374f98b6f853a96df4b14 --lang javascript --work <scratch>/cq/run1 --threads 4`, rc=0, outside the jest lock:
```
VERDICT TABLE (severity rule: security-severity >= 7.0, else problem.severity == error)
  results   head 29   base 29
  KEPT      total 0   high+ 0   (post-filter: primary or any related location START line is an added line)
  NEW       total 0   high+ 0   (rule,file,primaryLocationLineHash multiset, head minus base)
  GONE      total 0
  RESULT    rc 0 PASS (KEPT high+ 0, NEW high+ 0)
```

- **Added lines:** no open alert's path passes through an added line. My own pass over the head SARIF (every primary,
  related and code-flow location, 1648 read, by region start to end) against the head's added lines and the three new
  files found 0. No result names `static/js/index.js`.
- **Open alerts:** 22 by gh api, `most_recent_instance` at `74b58fd5`; 13 in `backend/server.js`, 0 in
  `static/js/index.js`.
- **Hosted check:** it cannot differ because main moved. Main moved in `HISTORY.md` only, which no CodeQL language of
  this repo scans; PR 237's head read CodeQL and Analyze (javascript-typescript) success.

## Item 9. PROCESS (Corrections 1 to 10, judged by effect on the product)

| Correction | judgment |
|---|---|
| 1. `rm -f` of its own scratch file | a rule breach in its own scratch; no product effect |
| 2. partial Step-0 reading | no product effect found; the gate re-measured everything the skipped files bear on |
| 3. three lock acquisitions | two from its own tool faults; the verify that counts ran whole in the third; no product effect |
| 4. the stop rule | F-4 |
| 5. predictions that missed | recorded honestly; my P1 to P6 reds equal its received column |
| 7. the reflog `reset: moving to HEAD` | written by `worktree add`; harmless |
| 8. the push rc not captured | the remote head is `b0c914dee093...` by my own `gh api -X GET git/matching-refs/heads/b1771` at 18:21:35 |
| `node_modules` symlinked | tooling only (I did the same) |
| the stale `wip/*` heads | I-5; none live |
| 6, 9, 10 | no product effect |

## Item 10. TEXT

Checked over the five commit messages and every added line, each with a control that fires:
- name scan (underscore-aware, ban list): 0;
- B-number, seat and session ids: 0;
- card or decision ids: 0;
- product-owner attribution: 0 (two messages say "the coordinator's default, not an owner ruling");
- ticket keys: `RD-1008` only;
- Cf and bidi characters: 0.

Other text checks:
- **Non-ASCII:** lines added 1, removed 1, net 0 (the cross mark on `index.js:3529`).
- **Dotted quads:** none other than loopback in the added lines.
- **Sensitive words:** one row, the harness env key name in `__tests__/rd1008-hostile-endpoint-chat-routes.test.js:79`,
  with a made-up value.
- **Secret scan:** gitleaks 8.30.1 with the repo's `.gitleaks.toml` over `git diff BASE head` reports "no leaks found",
  rc 0 (control: a planted AKIA-shaped string reports 1, rc 1).
- **Other flags:** no timer, skip marker or `new RegExp(` in added lines. One `new Function(` (F2's lifter, the rd395
  pattern). The `innerHTML` tokens in added lines are F2's constant fixture and test data, plus the product line.

## STATUS claims graded

TRUE:
- 7 paths, +7 -6 and +1 -1;
- red-first 14/7;
- 21 green twice;
- verify 6216/393 PASS (also on Node 24);
- CQ rc 0, 29 and 29;
- non-ASCII net 0;
- the F1 and F2 plant columns, and the H column received for P1 to P6;
- remote head = `b0c914d`;
- 0 open PRs at its read; PR 237 has since merged.

TRUE with a correction: "two layers" (it is three, item 4).

FALSE: the kit's P3 note (F-5).

NOT RE-MEASURED: the 102-file run list, its census frames and the sink census counts. The full verify backstops the
run list.

## FOUND / TESTED / NOT TESTED / HOW

**FOUND:** F-1 to F-5 and I-1 to I-6 above. No Blocker, no Major.

**TESTED:**
- scope and line accounting;
- the trial merge against main's exact tree;
- the server half by program, by a unit probe with the real adapter, and over HTTP with the real server against a
  hostile loopback stand-in (10 inputs, 5 route paths, BASE and head);
- 20 plants, including the pairs, triples and text-keeping forms;
- the browser half in a real Chromium, with 9 strings and the tool-call sibling;
- red-first at the BASE and the new files twice at the head;
- the refusal cells;
- the full verify on Node 24;
- CodeQL;
- text, secret and name scans;
- tickets RD-1008 (To Do, 0 comments, updated 2026-11-19 11:55), RD-1014 (To Do, 0 comments) and RD-1005 (Testing,
  1 comment), read whole by Jira GET.

**NOT TESTED:**
- any hosted instance, a real AI endpoint, Linux;
- the page under a hosted content security policy (the local page had none);
- the hosted Build and CodeQL on the PR merge ref and on the merge commit;
- the Deploy demo run a merge starts (it must read skipped; the last three on main read skipped);
- a slower machine for F3's waits (reasoned only, I-3);
- the merged tree's verify (the four `HISTORY.md` readers are proved only by PR 237's own Build);
- the first-run wizard writes and `GET /api/ai/status` renderers in a browser;
- who may call `GET /api/ai/status`;
- the builder's 102-file run list (the full verify covers it).

**HOW:**
- programs under `.../s300/g1793/progs/`: `scope.py`, `sinks_server.js`, `unit_adapter_probe.js`, `matrix.js`,
  `g1793-probe.test.js`, `plant.py`, `browser_probe.js`, `judge.py`, `runner.sh`, `jget.py`;
- raw outputs under `.../g1793/raw/`, `logs/`, `browser/` and `cq/`;
- one lock acquisition ran every jest run and server boot;
- reads: `gh api -X GET` and Jira GET only;
- no push, no PR, no Jira write, no alert action, no deploy.
