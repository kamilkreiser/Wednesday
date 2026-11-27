RD-1016 RD-1015: output escaping in two static scripts

Three commits on `279b2235`, six paths. Two product files change: `static/js/settings.js` (6 lines added, 16 removed) and `static/js/index.js` (14 added, 6 removed). Two new test files hold 28 cells. One line of an existing test file changes, and the counts file is regenerated. No workflow, helper, page or style file changes, and nothing is deployed.

| Commit | Ticket | What |
|---|---|---|
| `08e67b7c` | RD-1016 | settings.js defines escapeHtml once, and it escapes a value that is not a string |
| `2ec5fed1` | RD-1015 | eight number cells of four CSV exports are written as text when they would be read as a formula |
| `895da3f4` | - | counts, 6558 tests in 413 suites |

## RD-1016: one escapeHtml in settings.js, which escapes a non-string
- **The problem.** `static/js/settings.js` defined `escapeHtml` twice in one classic script, so the page ran the second definition. That one turned a value that is not a string into its text and returned it without escaping it. An array holding markup was therefore written as HTML at the five validation sinks: the suggestion, the message, the suggestions, the saved id and the quick question message.
- **The change.** The first definition is removed; the page never ran it. The one that remains turns a non-string into its text and then escapes it like a string.
- **What does not change.** A string is escaped exactly as before. `null`, `undefined`, `0`, `false` and the empty string still write nothing, as before. A number is its digits, as before. The only values that print differently are arrays and objects, and only when their text holds one of `& < > " '`.
- **Tests.** `__tests__/rd1016-settings-has-one-escapehtml.test.js` has 13 cells:
  - E1 to E5: the function itself;
  - A1 to A5: an array holding markup at each sink;
  - O1: an object whose text form is markup, at all five sinks;
  - C1 and K1: controls (a plain object, an ordinary string).

  Nine of the cells are red at the base and all 13 are green at the head. Each of four mutations of the change turns its own cells red.

## RD-1015 part (1): the eight raw number cells
- **The problem.** Eight cells were written outside `csvCell`, unquoted:
  - the sheets cell of the job history export and of the all-tabs export;
  - the pages and size cells of the scanning export;
  - the sheets and cost cells of each anomalies row, in the anomalies export and in the all-tabs export.

  A value that started with an equals sign was written into the file as a working formula.
- **The change.** A new helper, `csvNumberCell`, sits beside `csvCell` and is called at those eight cells. It asks `csvCell` itself whether the value would be prefixed. If so, it writes `csvCell`'s cell, which reads as text. Otherwise it writes the value exactly as before. There is no second formula pattern.
- **No ordinary export changes.** A plain number, zero, the empty string, a dash and a currency text are written byte for byte as before.
- **The existing RD-835 test file.** It lifts the export functions with an explicit list of helpers, so that one list gains the new helper's name. No assertion of that file changes. Without the line, five of its cells read red (X1, X4, X5, X8, K3).
- **Tests.** `__tests__/rd1015-csv-number-cells-are-not-formulas.test.js` has 15 cells:
  - U1 to U3: the helper;
  - X1 to X7: each of the eight cells fed a formula;
  - K1 to K3: rows that must not change (an ordinary scanning row, an ordinary anomalies row, zero sheets);
  - C1 and C2: the shipped text.

  Twelve of the cells are red at the base and all 15 are green at the head. Each of ten mutations turns its own cells red.

## The coordinator's choices
- One change for the two tickets, with no split.
- RD-1014 (the other HTML write sites of the three scripts) is not in this change. It follows as the next change of this lane, because it builds on the function RD-1016 makes single.
- The one-line change to the RD-835 test file's helper list.
- Number cells stay bare unless they are formula-shaped, so no ordinary export changes. The ticket's alternative was `csvCell` for every cell, which would quote every number.
- RD-1015 parts (2) and (3) are not built. Part (2) is a leading space, a new line or a look-alike character before an equals sign, and needs a real spreadsheet before anyone decides it. Part (3) is the visible quote on a negative amount, which the review accepted.
- `0` and `false` still write nothing in `escapeHtml`. No sink receives a meaningful zero: the saved id starts at 1.
- The thousands-comma row split of the anomalies exports is left to a new ticket.

## Named limits (not covered by this change)
- **A number cell that holds a comma, a double quote or a line break is still written raw, as before.**
  - A comma: a text such as `1,=1+1` gains a column whose cell begins with an equals sign.
  - A double quote: a text that starts with a double quote, such as `"=1+1"`, is read by a CSV reader as a quoted field holding `=1+1`.
  - A line break: a new line or carriage return inside the text starts a new row, and that row can begin with an equals sign.

  This is not new: these cells were raw before this change. Its fix, quoting such a cell, also closes the thousands-comma row split, and both go to one new ticket. Whether any outside text can reach these cells is not measured.
- A leading space, a new line or a look-alike character before an equals sign (RD-1015 part (2)) is written as before, and a cell pins that.
- The 34 other calls of `escapeHtml` in settings.js are not fed a non-string by any cell. Each writes into HTML text or a quoted attribute.
- The escape functions of `index.js` and `first-run-setup.js` are unchanged.
- No real browser, the dashboard's content security policy, or a spreadsheet opening a generated file was used.
- The code-summed counters, the sample-data writers, the job rows' cost cell and the server-side audit export are unchanged.

## Measured
- **The whole suite.** It passed in the Linux shape and in the plain shape at the counts commit: `VERDICT: PASS`, 6558/6558 tests in 413 suites.
- **Local CodeQL** (javascript, security-extended) against the base: results 29 at the head and 29 at the base, 0 new, 0 high or higher on an added line.
- **The pull request's own build** is the first run on Linux.
- **Deploy demo.** The merge starts a `Deploy demo` run. Both of its jobs are gated off, and the demo deploy hold stands.
