GATE B2050: GO WITH FINDINGS @ 444fe28 on main 04a6b89

# G1 gate, NexusAI lane NX-W (RD-1026, kit B2042, seat N170), round 1 of 2

- **Reader:** G1 on Opus (claude-opus-5-5), one reader, in-session, read-only toward the project, Jira and GitHub.
- **Window:** 15:42:45 to about 15:55 AEDT, Tue 24 Nov 2026.
- **Scratch:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s323/g2050/`. It holds:
  - `g2050.py` and `g2050.out` (the diff, jest JSON, tree, verify and CodeQL reads, by program)
  - `chromium-gate.js`, with `chromium-K.out` and `chromium-BASE.out`
  - `jget.py` and `jira.txt` (RD-1026, GET only)
  - `lane.patch`, `mkctl.py`, `gl-ctl.out`, `gl-lane.out`
  - `index_K.js`, `index_BASE.js`, `server_K.js`, `frs_K.js` (`git show` copies)
  - `_quarantine/ctl-gitleaks-plant.txt`

## The lane, re-measured (gh api -X GET, 15:42 and 15:47)
- **Main:** `04a6b89dcd142eebdb99f441c3840e32d7e0701f`, unmoved at 15:47.
- **Branch:** `b2042/rd1026-chat-tool-label-text` = `444fe281016cdf681681c6befee597da6879990d`. It is the only `b2042` ref.
- **Compare main...branch:** ahead 2, behind 0, merge base = main. Commits `1cce08b1` (A) and `444fe281` (K). Files:
  - `static/js/index.js` 1/1
  - the new test file 214/0
  - `scripts/verify-expected-counts.json` 3/3
- **Open PRs:** 0.
- **Open code-scanning alerts:** 22. None is at `static/js/index.js` (control: `backend/server.js` has 13).

## 1. The diff, read whole (`git log -p 04a6b89d..444fe281`, 15796 bytes)
- **Commit shape:** A's parent is BASE, and K's parent is A. A has two paths (A new test file, M index.js). K has one path (the counts file).
- **The product change is exactly one token.**
  - `git diff -U0` gives one line out and one line in, hunk `@@ -3523 +3523 @@`.
  - The line is equal after swapping `${label}` for `${escapeHtml(label)}`.
  - Over the whole file, the only differing line number is 3523. Control: a planted change at line 101 is detected.
  - Blob at K: `1ef82776...`.
- **`escapeHtml`, line 113, read whole.** There is one definition (control: `formatAIResponse` also has one).
  ```
  function escapeHtml(text) {
      if (text === null || text === undefined) return '';
      const div = document.createElement('div');
      div.textContent = text;
      return div.innerHTML;
  }
  ```
  - `null` and `undefined` become `''`.
  - Anything else is converted by `textContent`'s string conversion: a number becomes its digits, an array is joined with commas, and a plain object becomes `[object Object]`.
  - The output is the HTML text serialisation: `&` becomes `&amp;`, `<` becomes `&lt;`, `>` becomes `&gt;`, and U+00A0 becomes `&nbsp;`. **Quotes are not escaped.**
  - It is already in scope for this function: line 3529, the RD-1008 escape in the same `askAIAssistantStreaming`, calls it in production.
- **The counts file:** `_updated`, `tests` 6280 -> 6300 and `suites` 396 -> 397. Nothing else.
- **No other copy of the sink exists.** `git grep -l "Looking up department"` over the whole tree at K returns only `static/js/index.js`. `static/index.html:21` loads `js/index.js` directly (no bundle, no integrity hash).

## 2. Attack (the attacker controls every tool-call argument and the tool name)

### Where the values come from
- `backend/llm/azureOpenAIAdapter.js` 303-313 parses the model's `arguments` with `JSON.parse`, then fires `onToolCall({ phase: 'tool', name, args })`.
- `server.js` 7948-7950 writes it as `{ type: 'tool_call', ...evt }`. The event carries no `type` key, so the model cannot change the event type.
- `JSON.stringify` escapes newlines, so a model token cannot inject a second SSE `data:` line.
- **Values are therefore JSON values only:** string, number, boolean, null, array, or a plain object. There are no functions, so no hostile `toString` that runs.

### Gate's own real-browser run of the SHIPPED lines
`chromium-gate.js` lifts `escapeHtml` and index.js lines 3515-3523 verbatim (9 lines) from the K blob and from the BASE blob. It runs them in headless Chromium (Playwright, `about:blank`, no network). 16 cases:

| Case | K: children / hostile elements / `window.ran` | BASE control |
|---|---|---|
| image tag with a handler in each of the 5 argument values, and as the tool name | `I` only / 0 / shown as typed | `I,IMG` each |
| array of markup as the pattern; array as the tool name | joined and shown as typed / 0 | IMG and SVG made |
| object as the tool name | `[object Object]…` | same |
| JSON object with a non-callable `toString` | **throws `TypeError` at both K and BASE** (template / `textContent` ToPrimitive). In the page, the inner `catch` logs it and no write happens. Not an element. Pre-existing. | same |
| decimal / hex references `&#60;`, `&#x3e;`, `&lt` without semicolon | shown literally | BASE decoded them |
| `<!--x--><![CDATA[<img ...>]]>` | shown literally | BASE ate it |
| `</div></i><img ...>` | shown literally | BASE made IMG |
| NBSP, a surrogate pair, U+2028 | shown as typed | as typed |
| `${alert(1)}` with backticks | literal; the template is not re-evaluated | literal |
| ordinary `R&D floor > 3 "O'Brien"` | shown as typed | as typed |

- **Totals at K:** hostile elements in the whole document 0; `window.ran` after 700 ms **0**.
- **Totals at BASE (control):** 10 hostile elements; `window.ran` **9**.
- **The `…` suffix:** it is a literal after the escaped text, so nothing can join it.
- **The default branch (tool name as the label):** escaped like every other value, so it is covered.

### Can any value still make an element or attribute through this path?
**No.** The escaped label contains no `<`, so the parser cannot open a tag or an attribute from it. The label sits in element text of a `div` (after `</i> `), not in RCDATA or raw text. Quotes are inert there.

**A side observation (not this lane):** the tool name that can reach the label today is constrained server-side. `onToolCall` fires only when `executors[name]` is a function. `executors` is a plain object literal (`backend/llm/tools.js` 283), so the name is one of the 7 executor keys or an `Object.prototype` method name (`constructor`, `toString`, `hasOwnProperty`, ...). No markup reaches the label through the name today, and H1 "tool name" is defence in depth at the right boundary. Separately, a model can make the server call `Object.prototype.constructor` as an "executor": it returns the arguments, and the other method names throw and are caught. Low hardening candidate (an `Object.hasOwn` lookup). See FOR-RECORDS.

### The ticket, RD-1026, read whole by GET
- Status To Do, Bug, labels `records-pass-1120,security`, 0 comments (paginated), description 5589 characters by this flattener.
- Its acceptance: "an AI endpoint's tool-call arguments cannot add an element or run a handler in the status line, an ordinary pattern reads as typed, a cell for each value on the label, the existing cells and the full verify pass, the suite counts are regenerated by the project's own command".
- **Every clause is met.** "Run a handler" is shown in a real browser (the drafter's proof and this gate's run on the shipped lines), not by a jest cell. That is a stated limit.

### Sibling rows (OUT of this change by the coordinator's Q-3 default; read at K)

| Row | What it writes | Reachable by endpoint or viewer text today? |
|---|---|---|
| index.js 3466 (`thinking`) | `data.message` | **No.** Every `type: 'thinking'` write in server.js is a constant: 7728 and 7901, `'Analyzing your question...'`. |
| index.js 3470 (`decomposed`) | `data.subQueries.join` | **No.** server.js 7765 sends `subQueries.map(q => q.type)`. The types are the six constants of `decomposeComplexQuery` (719-747: `anomaly_detection`, ..., `general`). The user's own query is in `.query`, which is not sent. |
| index.js 3474 (`model`) | `data.name` | **No.** It comes from `getActiveModel().name` (model-config.js 175/203). That is `Azure OpenAI (${AZURE_OPENAI_DEPLOYMENT})`, operator environment configuration. |
| index.js 3478 (`generating`) | `data.message` | **No.** Constants at 7823 and 7920. |
| index.js 3569 (outer catch) | `error.message` | **No.** The outer `try` throws only `HTTP ${response.status}` (a number) or browser-generated fetch and stream errors. Parse and render errors are caught by the inner `catch`. |
| first-run-setup.js 1486 | `data.message` from `GET /api/setup/discover-tables` | **Only by the Azure Log Analytics service's own error text.** `azureLogAnalytics.js` 420-422 returns `maskGuids(error.response.data.error.message \|\| error.message)`; otherwise fixed strings. It is shown on the administrator's setup screen only. Not endpoint- or viewer-chosen; lowest grade. |
| first-run-setup.js 4127, 4240 | `data.message` on `data.success` | **No.** The enforce route's success `message` is two fixed sentences (server.js 4094-4098). |

- **None is reachable by AI-endpoint or viewer text today.** That matches the ticket's own reading. They are hardening candidates (Low), not a NO GO of this lane, because the kit does not claim to cover them.
- **Adjacent row, not on the ticket's list:** first-run-setup.js 1468 and 1471 write `${table}` raw into a `data-arg='...'` attribute and a `<code>`. Table names come from the Log Analytics workspace. Azure's naming rule allows only letters, digits and underscore in table names (the gate did not measure this), so it is not markup in practice. It is named for the hardening ticket.

## 3. Frame (stamp checklist item 11)
**The property:** the status line shows the label as text for every value. Three things the code is handed that are not the tested shapes:
1. **Arrays, plain objects, and objects whose `toString` is a JSON string: COVERED.** By construction (string conversion before the escape), and measured by the gate's Chromium run: arrays and objects show as text with 0 elements. The non-callable `toString` object throws before any write at both BASE and K: no element, and the status line keeps its previous text. **Stated limit:** that one shape leaves the earlier status shown. It is pre-existing and cosmetic.
2. **Other reference spellings and parser-state tricks (decimal and hex references, a named reference without its semicolon, comments, CDATA, a closing `</div>`): COVERED.** `&` always becomes `&amp;`, and `<` always becomes `&lt;`. Measured in Chromium (above); H2 cells cover the named form and the closing tag.
3. **A real browser and attribute contexts (the seat's NOT TESTED): COVERED for this sink; stated limit for others.**
   - Chromium serialises text with the same spec algorithm as jsdom. The drafter's `chromium-proof.log` (fixed: `[[1,true]x4]`, ran 0; base ran 1) and this gate's run on the verbatim shipped lines (ran 0 at K, 9 at BASE) agree.
   - Attribute context: the label is never in an attribute (S1 pins `</i> ${escapeHtml(label)}`).
   - `escapeHtml` is **not** safe for an attribute value (quotes pass). E1 documents that, and any future attribute use must not reuse it as is.
   - **Stated limit:** a future `statusDiv.innerHTML` write with a value in another `case` is outside S1.
   - Not run: a hosted content security policy, a real AI endpoint, Linux.

## 4. The test file
**The cells test the product, not a copy:**
- `extractFunction` reads `static/js/index.js` from the tree under test.
- It lifts `askAIAssistantStreaming`, `readAiDisabledRefusal` and `escapeHtml` brace-balanced and runs them in jsdom with a fetch stub. S1 reads the same file's `tool_call` branch.
- Only collaborators are stubbed (`formatAIResponse`, `LoadingManager`, ...). They are not on the label path.

**Red-proof, read by program from the seat's jest JSON** (`raw/rf.json`, `raw/redproof.json`, `raw/green.json`; not trusting the judge logs):
- rf: 20 tests, 11 failed. Redproof: 20 tests, 11 failed. **The failed title sets are equal.**
- The red cells are exactly H1 x6 (the five values and the tool name), H2 x4 (script, attribute break, closing tag, character references) and S1, with 0 others.
- Green: 26 suites, 346 tests, 0 failed, 0 runtime errors. The new file is present with 20 tests, in the dot-free `b2042-nodot/work`.

**Redproof isolation:**
- `lane.out` shows `revert ... 476128 -> 476116` then `apply ... -> 476128`, with blob `1ef82776...` after.
- `apply2042.py` asserts one anchor.
- Trees now: `rf` at BASE with blob `2c883fa5` plus the new file; `work` at BASE with blob `1ef82776` plus the new file.

**Lock:** the lane ran under one jest-lock acquisition (`b2042-lane`, 14:52:01-14:52:13, `lock-wrapper rc=0`). **No jest re-run by the gate**: the JSON evidence was sufficient. The gate's only executions were node/Chromium on `about:blank`, git reads, Python and gitleaks.

## 5. Verify and CodeQL (from the seat's logs)
- **`verify-update.log` (at A) and `verify-plain.log` (at K)** each read:
  - `Test Suites: 397 passed, 397 total`
  - `Tests: 6300 passed, 6300 total`
  - `VERDICT: PASS — 6300/6300 tests passed across 397 suites (jest exit 0)`
  - `EADDRINUSE` 0. Control: the VERDICT line is present in each.
- **`v-update.out`:** head `1cce08b1`, `verify update rc=0`, `lock-wrapper rc=0`, 14:53:05-15:15:35.
- **`v-plain.out`:** head `444fe281`, `verify plain rc=0`, `lock-wrapper rc=0`, 15:15:56-15:38:44.
- **The pair:** 6300 / 397 = BASE 6280 / 396 plus 20 and 1, and it equals K's committed counts.
- **CodeQL** (`cq/cq1`): base `04a6b89d`, head `444fe281`, CLI 2.27.4, javascript-security-extended.
  - `results head 29 base 29`, KEPT 0, NEW 0, GONE 0, `RESULT rc 0 PASS`.
  - `cq rc=0`, `cq.err` 0 bytes.
  - The verdict json reads `kept [] new [] gone [] kept_high 0 new_high 0`.
  - `runcq.sh` carries the right shas.
  - GONE 0 means CodeQL never saw this sink. It is no witness for the fix; the cells and the browser runs are.

## 6. gitleaks
- **Control:** an AWS key-id plus secret pair built by `mkctl.py` (random, not the docs EXAMPLE keys), scanned alone: **rc 1, `leaks found: 2`**. The plant was quarantined.
- **Lane:** `git log -p 04a6b89d..444fe281` (15796 bytes) through `gitleaks stdin --no-banner --redact`: **rc 0, `no leaks found`**.

## 7. Landing texts (this folder)
`landing.txt`, `pr-title.txt`, `pr-body.md`, `FOR-RECORDS.md`. Key points:
- A merge commit pinned to `444fe281` (C-190, never squash).
- `--min-checks 7` from PR 247's head `5c98e04d`: 8 runs, 7 names.
- Deploy demo: read its jobs by `head_sha=<M>`. PR 247's run 45315569382 skipped build and deploy. If either runs, approve nothing and card it under the C-224 hold.

## Findings (none blocks landing)
- **F-1 (stated limit):** "runs no handler" is shown by real-browser runs (the drafter's, and this gate's on the verbatim shipped lines), not by a jest cell. jsdom proves "no element, no attribute".
- **F-2 (stated limit, pre-existing):** a JSON object with a non-callable `toString` as an argument or the tool name makes the branch throw before the write. No element is made; the status line keeps its previous text. The same happens at BASE.
- **F-3 (follow-up, Low, server-side):** the adapter's `executors[name]` lookup on a plain object accepts `Object.prototype` method names. A model can make the server call `Object.prototype.constructor` with its arguments. That is not a page write and not this ticket. Candidate: `Object.hasOwn(executors, name)`.
- **F-4 (follow-up, Low):** the eight sibling rows, each not reachable by endpoint or viewer text today (table above), plus the adjacent first-run-setup.js 1468/1471 `${table}` attribute write. One hardening ticket.

## Disclosures (the gate's own)
1. The gate ran Playwright's headless Chromium twice from the seat clone's `node_modules` (`.tools/b2042/clone/node_modules/playwright`). That was a read of the module only. It ran on `about:blank` with no server, network or jest, and each browser closed itself. `pgrep -fl chrome-headless-shell` afterwards: none (rc 1).
2. Git reads of the seat's clone used `--no-optional-locks`. Nothing was written under `!CODING`. Jira: one GET (RD-1026).
3. No hook refusal occurred. Two advisory notices from the case-sensitivity grep hook were read. The affected greps were literal code tokens with their own positive results.
