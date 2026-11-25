# FOR-RECORDS: RD-1039 (records pass, after the landing)

Fill in `<N>` (the PR) and `<M>` (its merge commit) after the landing. Take the Deploy demo line from landing.txt step 4. Take the gate line from the first line of VERDICT.md.

**Jira GET at the gate** (13:0x AEDT, 25 Nov; credentials in-process, nothing printed): RD-1039, Task, To Do, labels `records-pass-1124,security`, 0 comments, 0 links. RD-1014 To Do (the first-run "values from outside written as HTML" ticket). RD-1026 Testing.

## RD-1039: result comment

Landed by pull request <N>, merge commit <M>: a merge commit of the reviewed head `8a2d2b88`. A is `1b7c1dcc` (the change and the two new test files); K is `8a2d2b88` (the counts, 6429 / 403).

- **Change (ten writes, one lookup).**
  - `static/js/index.js` (5 lines): the thinking message, the sub-query types, the model name, the generating message and the outer catch's message are written through the page's `escapeHtml`.
  - `static/js/first-run-setup.js` (5 lines): the table name (in the single-quoted `data-arg` and in the `code` element), the no-tables message, and the success message of the two enforce routes, through the script's own `escapeHtml` (which escapes both quotes).
  - `backend/llm/azureOpenAIAdapter.js` (2 lines): the tool lookup reads `executors` with `Object.hasOwn`, so an inherited name (`constructor`, `toString`, `hasOwnProperty`, `__proto__` and the rest) is an unknown tool and fires no tool_call event.
  - Two existing tests re-pinned by one line each (rd1008 C4: the two status writes now escaped; rd395 UI2b: `escapeHtml` added to the lifted list).
- **Behaviour change.** A status or message with no value (missing or null) shows nothing instead of the word `undefined` or `null`.
- **Whose call.** Q-0 each script's own `escapeHtml`, Q-1 the two re-pinned tests, Q-3 missing value shows nothing, Q-4 the unlisted rows left alone, and the HOLD 20 ruling that the new rd1040 suite is not in the partition and runs in both full verifies: all the coordinator's, not the product owner's.
- **Two premises of the ticket, corrected.** (1) The ticket said the setup script's escape has no attribute form: it escapes both `"` and `'` (script lines 2951 to 2952), so no second helper was built. (2) The ticket said the other inherited names throw: at BASE `constructor` returned the model's arguments as the tool's answer and `toString` returned a string; the others threw into a caught error; all but `__proto__` fired a tool_call event.
- **Measured.** New files, 67 cells: red-first at BASE 38 failed / 29 passed; green at head 67 of 67; red-proof (the five edits reverted) the same 38 (names compared by program, by the seat and by the gate). Full verify at the head (behind main 0, so the head is the merge tree): see VERDICT.md. Local CodeQL NEW 0 / KEPT 0. gitleaks none (control fired). Gate B2085: <VERDICT line>.
- **Not tested.** A hosted instance and its content security policy, a real AI endpoint, a real browser in a cell (the seat's drafter ran a Chromium proof of the ten statements, 54 cases; the seat and gate did not).
- **Deploy.** None. Deploy demo run for <M>: <conclusions, from landing.txt step 4>.
- **Move.** To the column the records pass uses for a landed lane awaiting acceptance.

## Drop list for NX-X (RD-1014's lane): rows this lane fixed
`static/js/first-run-setup.js` lines 1468, 1471, 1486, 4127, 4240 (at BASE) and `static/js/index.js` lines 3466, 3470, 3474, 3478, 3569 (at BASE). Per RD-1014's own rule ("whichever of the two lands second drops the rows the first fixed"), NX-X drops these ten. NX-F1 (any lane editing `first-run-setup.js`) must rebase on this one's rows.

## The 27 unlisted rows, for RD-1014 (found by the seat's program, not changed here)
- `static/js/index.js` 3044 (`data.message` in a downloaded text file, not HTML: probably no change needed) and 3750 (`error.message` in `addAIMessage`, the standard path's catch).
- `static/js/first-run-setup.js` 1502 (`error.message` in `discoverTables`'s own catch, the nearest, three lines under a fixed row), 1760, 1764, 1825, 1827, 1854, 1941, 2010, 2014, 2849, 2851, 2855, 3298, 3598, 3872, 3876, 4158, 4163, 4176 (`enforceAuthentication`'s catch), 4277, 4282, 4295 (`turnOnAuthenticationControl`'s catch), 4950, 4951, 4959.
- The gate re-read the catches at 4176 and 4295 at the head: both still write `error.message` raw inside functions this lane edited. Dup-check RD-1014 (To Do) before filing anything: it already lists "80 first-run error lines".

## Info for records (not this ticket's acceptance)
1. The tool lookup still answers an array name `["search_users"]` or an object whose `toString` returns an own name by running that tool (property-key coercion), as at BASE. Only the model can send it, and it runs a tool that was already offered; no new reach.
2. `package.json` has no `engines` field; `Object.hasOwn` (Node 16.9+) is covered by the Dockerfile (`node:24-alpine`) and the three workflows (`node-version: '24'`).
3. `data-arg` values `this` and `event` are substituted by `csp-helpers.js` (a table literally named `this` or `event` would pass the element or event to `selectTable`): pre-existing, unchanged.
