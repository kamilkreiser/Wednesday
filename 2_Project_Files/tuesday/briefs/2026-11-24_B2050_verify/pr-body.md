## What this changes

The chat page's stream reader wrote the status line of a tool call with `innerHTML`. The label it wrote is built from the tool name and the tool's arguments (the search pattern, the user name, the printer name, the department), and an AI endpoint chooses those. A value holding markup became markup in the status line: an image tag with an error handler made an element, and its handler ran.

`static/js/index.js` line 3523 now passes the whole label through the page's own `escapeHtml`, the same form the stream error event has used since RD-1008:

```diff
-  statusDiv.innerHTML = `<i class="bi bi-search me-1"></i> ${label}…`;
+  statusDiv.innerHTML = `<i class="bi bi-search me-1"></i> ${escapeHtml(label)}…`;
```

- The label's own fixed text holds no `<`, `>` or `&`, so escaping the whole label gives the same output as escaping each value.
- It also covers the tool name, which becomes the label for a tool the page does not know, and any value a later tool adds to the label.
- The status line keeps its icon, and an ordinary value reads exactly as before.

**The other status writes of the chat region that the ticket lists are not changed. That is the coordinator's default (Q-3), not part of this fix.** They are named below.

## The result for the ticket (RD-1026, from the test cells)

- **Before (main): 11 named cells red.**
  - An image tag with a handler in each of the five values on the label made an element in the status line. The five values are the search_users pattern, the search_printers pattern, the lookup_user userName, the lookup_printer printerName, the lookup_department department, plus the tool name itself.
  - A script element, an attribute break and a closing tag in a search pattern made elements.
  - Character references in a search pattern were read as references.
  - The source wrote the label raw (S1).
- **After: all 20 cells green.**
- **Red-proof:** with only the product line reverted, the same 11 cells are red.
- **Controls (green before and after):**
  - Ordinary values: a plain word, an ampersand, quotes and an apostrophe, an attribute-shaped text, a greater-than sign, a number.
  - A null value, missing arguments, no tool name, a tool without arguments, and a number as the tool name.
  - The thinking-harder status.
  - The page escape's own behaviour.
- **The committed line at K (line 3523):** `statusDiv.innerHTML = `<i class="bi bi-search me-1"></i> ${escapeHtml(label)}…`;`
- **Real browser:** a headless Chromium run of the shipped lines 3515-3523, lifted verbatim, with 16 hostile and ordinary values. Every value showed as typed, no element was made, and no handler ran. The same run on main made 10 elements, and 9 handlers ran.

## Files (3 files; two commits: the change, then the suite counts written by the project's own command)

- `static/js/index.js`: one line, one token (`${label}` -> `${escapeHtml(label)}`).
- New: `__tests__/rd1026-chat-tool-call-label-is-text.test.js` (20 tests). It uses the RD-1008 page-cell form: the shipped functions are lifted from `static/js/index.js` and run in jsdom, with a fetch stub streaming one tool event.
- `scripts/verify-expected-counts.json`: changes from 6280 / 396 to **6300 / 397**, written by `npm run verify -- --maxWorkers=2 --update-counts`.

## Verification

- Full verify, run twice (once at each commit): `VERDICT: PASS`, 6300/6300 tests across 397 suites, `EADDRINUSE` 0.
- The 26 suites that name `static/js/index.js`: 346 of 346 green.
- Local CodeQL (javascript-security-extended), main against head: results 29 / 29, NEW 0, KEPT 0, `rc 0 PASS`. CodeQL never reported this sink on main either, so the evidence for the fix is the cells and the browser run.
- gitleaks over the whole diff: no leaks found. The control fired.

## Not in this change (named)

The ticket's sibling rows, by the coordinator's default (Q-3). None of them takes text an AI endpoint or a viewer chooses today:

- `static/js/index.js` 3466 and 3478: fixed server status messages.
- `static/js/index.js` 3470: fixed sub-query type names.
- `static/js/index.js` 3474: the model name from the server's configuration.
- `static/js/index.js` 3569: an HTTP status or a browser fetch error.
- `static/js/first-run-setup.js` 1486: on the administrator's setup screen, the Log Analytics service's own error text.
- `static/js/first-run-setup.js` 4127 and 4240: fixed success sentences.

Escaping them is a Low hardening, proposed as a follow-up.

**Not tested:**
- a hosted instance and its content security policy
- a real AI endpoint
- Linux
- "no handler runs" as a jest cell. jsdom runs no handler, so that part rests on the Chromium runs.

`escapeHtml` leaves quotes as typed. That is safe here because the label is element text, and a source cell pins that.

## Deploy

None. Merging starts a `Deploy demo` run. Both of its jobs require `vars.CI_DEPLOY_ENABLED == 'true'`, and the deploy job also needs approval from a required reviewer on the `demo` environment.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
