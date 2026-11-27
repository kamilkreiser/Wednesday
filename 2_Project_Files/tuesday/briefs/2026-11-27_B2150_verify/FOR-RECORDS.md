# FOR-RECORDS: RD-1016, RD-1015 and RD-1014, for the records pass AFTER the landing (gate B2150, round 1 of 2, lane 3 kit 1)

After the landing, fill in:
- `<n>`, the pull request number;
- `<M>`, its merge commit;
- `<HEAD>`, the head it pinned: K `895da3f4`, or Tuesday's merge-of-main commit M2 if landing.txt step 0b ran.

Take the Deploy demo line from landing.txt step 4, the hosted build line from step 2, and the gate line from the first line of VERDICT.md.

This gate did NOT read or write Jira. It read the drafter's saved RD-1015 text, read-only. Before writing each comment, the records seat reads the ticket's current comments and state. No person's name and no card, seat or build id goes in a comment, and every choice is named as the coordinator's default. No ruling of the product owner rests on this lane (C-307, `CLARIFICATIONS.md` line 3110).

## Ticket state, read against the project's rule
The rule is `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/CLAUDE.md` line 302: "Code change → `Testing` (then Kam / a teammate moves it to `Release Ready` after verification)". The gate re-printed it with awk NR==302 at 14:06.

**RD-1016 (Low): met. Move to Testing.**

**RD-1015 (Low): comment only, do NOT move.**
- Part (1) is met in the words of the ticket's acceptance: each of the eight cells, fed a string that starts with a formula character, is written as text.
- Parts (2) and (3) stay open.
- So does this gate's Finding 1 (below), unless the records pass files it as the new ticket. It is filed there by default.

**RD-1014 (Medium): comment only, do NOT move.**
- Nothing of it is built.
- Its premise in settings.js changed: the `escapeHtml` that its `escapeAttrValue` will build on is now single and escapes a non-string.

## RD-1016: comment
Pull request <n> landed as merge commit <M>, the merge of the reviewed head <HEAD>; commit `08e67b7c` is this ticket's.

**What changed:**
- `static/js/settings.js` now defines `escapeHtml` once.
- The first definition, which the page never ran, is removed.
- The one that remains turns a value that is not a string into its text and then escapes it.

**What did not change.** Strings are escaped as before. `null`, `undefined`, `0`, `false` and the empty string still write nothing (the coordinator's default for the ticket's question about 0). No sink receives a meaningful zero: the saved condition id starts at 1, `backend/jsonStorage.js` line 3756.

**Measured by the gate at the head:**
- No value reaches one of the five sinks unescaped:
  - an array of objects, a nested array, a Symbol;
  - an object whose `toString`, `valueOf` or `Symbol.toPrimitive` returns markup;
  - a Proxy, a String object, an Error.

  Each comes out escaped, and each sink fed one makes no element. A Proxy whose conversion throws throws as before.
- Every scalar prints as it did before.
- The 39 calls in the file all resolve to the one definition, by scope analysis.
- No other script on the settings page defines `escapeHtml`.

**Tests:** `__tests__/rd1016-settings-has-one-escapehtml.test.js`, 13 cells.
- Red first at the base on E1, E2, E3, A1 to A5 and O1.
- Green at the head in both test shapes.
- Four mutations, each red on exactly its cells.

## RD-1015: comment
Pull request <n> landed as merge commit <M>; commit `2ec5fed1` is this ticket's.

**Part (1) is met.** A new helper, `csvNumberCell`, writes the eight raw number cells. A value that `csvCell` would prefix is written through `csvCell`, as text. Every other value is written byte for byte as before.

Measured by the gate:
- 12527 ordinary values gave 0 changed bytes;
- the four exports, fed ordinary rows, are byte-equal at the base and at the head;
- `+1+1` and `-1+cmd` are prefixed;
- `1e5`, `+1` and `-1` stay bare, and a spreadsheet reads them as numbers.

The coordinator chose bare-unless-formula over the ticket's "through csvCell" option, so that no ordinary export changes and the RD-835 cells that pin bare numbers stay as they are.

**Parts (2) and (3) stay open:**
- Part (2): a leading space, a new line or a look-alike before an equals sign. A cell pins this as unchanged; it needs a real spreadsheet first.
- Part (3): the visible quote on a negative amount. The review accepted it.

**Not covered: a number cell that holds a comma, a double quote or a line break** is written raw, as before. A CSV reader then sees a cell that begins with an equals sign:
- a comma gains a column;
- a leading double quote opens a quoted field;
- a line break starts a row.

This is filed as a new ticket (below). Whether outside text can reach these cells is still not measured, as the ticket says.

**Tests:** `__tests__/rd1015-csv-number-cells-are-not-formulas.test.js`, 15 cells.
- Red first at the base on U1 to U3, X1 to X7, C1 and C2.
- Green at the head.
- Ten mutations, each red on exactly its cells.

The one-line change to the RD-835 file's helper list is proven needed: without it, X1, X4, X5, X8 and K3 of that file read red.

## RD-1014: comment
- Not built in pull request <n>; it follows as the next change of this lane.
- Changed premise: `static/js/settings.js` now holds one `escapeHtml`, which escapes a non-string, so the `escapeAttrValue` this ticket adds there builds on a single function.
- Its index.js rows sit in the same file as RD-1015's hunk. Its kit names <M> as its base.

## New ticket to file (one ticket; Low; labels as RD-1015's)
Title: "A number cell of the CSV exports that holds a comma, a double quote or a line break is written raw: the row gains a column, and the extra cell can be read as a formula".

**Finding 6 of the kit, the row split.** It predates this change: at base `279b2235`, `index.js` lines 8903, 8953 and 9003 write `sheets.toLocaleString()`, and lines 5977 and 6145 write the anomalies cells raw; blame names `9b58261f` of 2026-04-25.
- A sheets figure of 1000 or more becomes `1,234`.
- The anomalies row then has 8 columns under a 7-column header.
- Measured: an ordinary anomalies export read by Python's csv reader gave row widths 7, 7, 8, 7. It is byte-equal at the base and the head.

**Gate B2150's Finding 1, the formula through structure.** Measured at head `895da3f4` by running the real exports and reading the output with Python's csv reader:
- `1,=1+1` gives an extra cell `=1+1`;
- `"=1+1"` gives the sheets cell itself as `=1+1`;
- `1\n=1+1` gives a new row whose first cell is `=1+1`.

This is in the job history, scanning, anomalies and all-tabs exports.

**Proposed fix (a proposal, not decided).** `csvNumberCell` also writes through `csvCell` a value that holds a comma, a double quote, a carriage return or a line feed. The gate measured this shape as a mutant: it turns only U2 and U3 of the RD-1015 file red, because those cells pin `1,234`, `a"b` and a leading new line as "as before". So the fix changes bytes only for rows that are already broken.

Not measured: a spreadsheet, and whether outside text can reach the cells.

## Gate findings to file or note (see VERDICT.md for grades)
- **Finding 1 (Major, not blocking):** the new ticket above.
- **Finding 2 (Minor, pre-existing):** the thousands-comma row split; the same ticket.
- **Finding 3 (Info):** the landing order. After pull request 267, this branch conflicts on the counts file, so landing.txt step 0b (a merge of main, then regeneration) is needed. Records text only.
- **Finding 4 (Info):** the kit's "35 other callers" are 34 calls plus one comment line (`settings.js` line 3631 at the head). Records text only.
