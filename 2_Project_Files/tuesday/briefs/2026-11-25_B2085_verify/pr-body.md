## What this changes

The change that made the chat's tool-call label text (RD-1026) left ten more writes of the same kind in the page scripts, and one tool lookup that accepts more names than the tool list holds. None takes a value an AI endpoint or a viewer chooses today; each now cannot become markup or a tool.

**The ten writes (escape at the sink, each script's own `escapeHtml`; no new helper):**

- `static/js/index.js`, the chat's streaming reader (5): the thinking message, the sub-query types, the model name, the generating message, and the message of the outer catch.
- `static/js/first-run-setup.js` (5): the table discovery's table name (written into a single-quoted `data-arg` attribute and into a `code` element), its no-tables message, and the success message of the two enforce routes. The setup script's escape already covers both kinds of quote, and the attribute is read back by `getAttribute`, so a table name holding `&`, `'` or `"` still selects the right table (pinned by cells T1 and C2).

**The lookup:** `backend/llm/azureOpenAIAdapter.js` read `executors[name]` on a plain object, so a tool name every object inherits (`constructor`, `toString`, `hasOwnProperty` and the rest) found a function: the adapter called it with the model's arguments and told the page a tool by that name was running. It now reads only the tool list's own entries (`Object.hasOwn`); such a name gets the unknown-tool answer and no tool_call event. Every tool the list holds, a list with no prototype and a missing list behave as before. The project's Docker image and CI use Node 24; `Object.hasOwn` needs 16.9.

## Behaviour change

A status line or message with no value (missing or null) now shows nothing (the icon alone, or an empty paragraph) instead of the word `undefined` or `null`.

## Choices that are the coordinator's

- Each script's own `escapeHtml` is used; no shared helper.
- Two existing test files are re-pinned by one line each (a chat error-event cell that counted the two raw status writes now counts none; a lifted-function list gains `escapeHtml`).
- A missing value shows nothing.
- The rows this ticket does not list are left alone (next section).

## Not in this change (disclosed)

- **27 more lines hold the same kind of raw write** and are not changed: 2 in `static/js/index.js` (a downloaded text file, which is not HTML; and the standard-mode catch) and 25 in `static/js/first-run-setup.js`, among them the catch of `discoverTables` three lines below a fixed row. They belong to the open follow-up for first-run error lines.
- **Two premises of the ticket were wrong and are corrected here:** the setup script's escape does have an attribute form (it escapes both quotes), so no second helper was needed; and the other inherited names do not all throw (`constructor` returned the model's arguments as the tool's answer and `toString` returned a string; the rest threw into a caught error).
- Not tested: a hosted instance and its content security policy, a real AI endpoint, a real browser in a cell.

## The result (67 new cells in two files)

- Before (main): 38 of 67 fail, all on the properties. After: 67 of 67 pass. With only the five product and pin edits reverted, the same 38 fail.
- The 121 suites that read the changed files, plus the two new files: all pass. Full verify: `VERDICT: PASS`, 6429 tests in 403 suites (the head is the merge tree; the branch is behind main by 0).
- Local CodeQL (javascript), main against head: NEW 0, KEPT 0.
- gitleaks over the diff and the commit messages: no leaks found; the control fired.

## Files

- `static/js/index.js`, `static/js/first-run-setup.js` (5 lines each), `backend/llm/azureOpenAIAdapter.js` (2 lines).
- `__tests__/rd1008-endpoint-error-code-is-not-trusted.test.js`, `__tests__/rd395-ai-disabled-ui.test.js` (re-pinned).
- New: `__tests__/rd1039-chat-and-setup-status-lines-are-text.test.js`, `__tests__/rd1039-tool-lookup-reads-own-names-only.test.js`.
- `scripts/verify-expected-counts.json`: 6362 / 401 to **6429 / 403**, by `npm run verify -- --maxWorkers=2 --update-counts` (second commit).

## Deploy

None. Merging starts a `Deploy demo` run, because `static/**`, `backend/**` and `__tests__/**` are not in its `paths-ignore`. Both of its jobs require `vars.CI_DEPLOY_ENABLED == 'true'` (the repository has no Actions variables) and the deploy job also needs approval from a required reviewer on the `demo` environment. The last runs of the workflow all read skipped.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
