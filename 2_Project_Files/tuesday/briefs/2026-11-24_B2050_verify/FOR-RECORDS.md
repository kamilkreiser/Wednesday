# FOR-RECORDS: RD-1026 (records pass, after the landing)

Fill in `<N>` (the PR) and `<M>` (its merge commit) after the landing. The Deploy demo line comes from landing.txt step 4.

## RD-1026: result comment

Landed by pull request <N>, merge commit <M>, a merge commit of the reviewed head `444fe281`.

- **Change.** `static/js/index.js` line 3523 writes the tool-call status label through the page's own `escapeHtml`. The old text was `${label}`; the new text is `${escapeHtml(label)}`. This is the form the stream error event (line 3529) has used since RD-1008.
- **Why one escape at the sink instead of one per value.** The label's own fixed text holds no `<`, `>` or `&`, so the output equals the ticket's per-value form. The sink escape also covers the tool name, which becomes the label for an unknown tool, and any value a later tool adds to the label.
- **Measured: the 11 named cells at the base.** All 11 were red at the base:
  - An image tag with a handler in each of the five values on the label made an element. The five values are the search_users pattern, the search_printers pattern, the lookup_user userName, the lookup_printer printerName and the lookup_department department.
  - An image tag with a handler as the tool name itself also made an element.
  - A script element, an attribute break and a closing tag in a pattern each made an element.
  - Character references in a pattern were read as references.
  - The source wrote the label raw (S1).
- **Measured: after the change.**
  - All 20 cells are green at the head.
  - With only the product line reverted, the same 11 cells are red.
  - The controls are green at both: ordinary values, null, missing arguments, no tool name, a number as the name, and the thinking-harder status.
- **Real browser.**
  - The G1 gate ran the shipped lines 3515-3523, lifted verbatim, in headless Chromium with 16 values. These included each field, the tool name, arrays, objects, decimal and hex references, comment and CDATA, a closing `</div>`, NBSP and an ordinary value.
  - Head: 0 elements made, 0 handlers ran.
  - Base: 10 elements made, 9 handlers ran.
  - The drafter's separate Chromium proof agrees.
- **Verification.**
  - Full verify PASS, 6300 tests in 397 suites, at both commits. The counts file was written by the project's own command.
  - Local CodeQL: NEW 0, rc 0.
  - G1 gate: GO WITH FINDINGS (below).
- **Q-3.** The coordinator's default: the ticket's sibling rows are not changed in this change. See the follow-up below.
- **Deploy.** None. Deploy demo run for <M>: <build / deploy conclusions, from landing.txt step 4>.
- **Not tested.**
  - A hosted instance and its content security policy, a real AI endpoint, and Linux.
  - "Runs no handler" is shown by the Chromium runs, not by a jest cell.
  - `escapeHtml` leaves quotes as typed. It is safe here only because the label is element text, which S1 pins.

## Follow-up candidates (for the records pass to file or fold in; none is decided here)

1. **Chat-region and setup-screen hardening (Low), the ticket's sibling rows.**
   - None of these rows is reachable by AI-endpoint or viewer text today; the G1 gate read the source at the head.
   - Proposed: one Low ticket to write each row through `escapeHtml` or as text.

   | Row | The gate's reachability reading |
   |---|---|
   | `static/js/index.js` 3466 (`thinking`) | Every server write is the constant `'Analyzing your question...'` (`backend/server.js` 7728, 7901). Not reachable. |
   | `static/js/index.js` 3478 (`generating`) | Constants (7823, 7920). Not reachable. |
   | `static/js/index.js` 3470 (`decomposed`) | The server sends `subQueries.map(q => q.type)` (7765). The types are six constants from `decomposeComplexQuery` (719-747). The user's query text is in `.query` and is not sent. Not reachable. |
   | `static/js/index.js` 3474 (`model`) | `getActiveModel().name` is `Azure OpenAI (<AZURE_OPENAI_DEPLOYMENT>)`, from the operator's environment configuration (`model-config.js` 175). Not endpoint text or viewer text. |
   | `static/js/index.js` 3569 (outer catch) | `HTTP <status>` (a number) or a browser-generated fetch or stream error. Parse and render errors are caught by the inner catch. Not reachable. |
   | `static/js/first-run-setup.js` 1486 | `data.message` from `GET /api/setup/discover-tables`. That is fixed strings or the Log Analytics service's own error message (`maskGuids(...)`, `backend/azureLogAnalytics.js` 420-422). It shows on the administrator's setup screen only. Lowest grade. |
   | `static/js/first-run-setup.js` 4127 | The enforce route's success message, fixed sentences (`server.js` 4094-4098). Not reachable. |
   | `static/js/first-run-setup.js` 4240 | The same as 4127. Not reachable. |
   | Adjacent, not on the ticket's list: `static/js/first-run-setup.js` 1468 and 1471 | `${table}` written raw into a `data-arg='...'` attribute and a `<code>`. Table names come from the workspace. Azure's naming rule allows only letters, digits and underscore; the gate did not measure this. Fold it into the same hardening ticket. |

2. **Server-side tool dispatch (Low, a new candidate, not a page write).**
   - `backend/llm/azureOpenAIAdapter.js` 307 looks up `executors[name]` on a plain object literal (`backend/llm/tools.js` 283).
   - A model-chosen name such as `constructor` therefore passes the `typeof fn === 'function'` check. The server then calls `Object.prototype.constructor` with the model's arguments. It returns them, and the other `Object.prototype` names throw and are caught.
   - The impact read is none beyond an odd tool result, but it is an unintended dispatch.
   - Candidate fix: `Object.hasOwn(executors, name)`, or a null-prototype map.
   - The same check means that no markup can arrive as a tool name today, so the page's tool-name escape is defence in depth.
3. **Hosted content security policy (RD-1014's note).** It is still not measured on a hosted instance. RD-1026's own text says the strict policy is the default.
