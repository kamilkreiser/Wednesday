## What this changes

Two tickets, one branch: RD-835 (CSV cells that a spreadsheet runs as formulas) and RD-861 (server, AI and user-name values written into the page as HTML). Six files: `static/js/index.js`, `static/js/settings.js`, `static/js/first-run-setup.js`, two new test files and the test-count file. No backend file changes.

### CSV exports (RD-835)

**Before:** all ten CSV writers only quoted a value and doubled its inner quotes. A printer, device or user name that started with `=`, `+`, `-`, `@`, a tab or a carriage return opened as a live formula when an administrator loaded the download in a spreadsheet. A device or account named `=HYPERLINK(...)` or `=cmd|' /C calc'!A0` reached the administrator's spreadsheet as a working formula. Those names come from the customer's print and directory data. The ten writers are the eight export closures, the recent prints export and the AI reply export.

**Now:** one shared helper, `csvCell`, writes every cell of those ten writers. If a value starts with one of those characters, the helper puts a single quote in front of it, inside the quotes, so the cell shows as text. Quoting still follows RFC 4180: commas, quotes and new lines inside a value stay inside one cell.

**Exemptions and their limits:** two kinds of value are left as they were, so ordinary rows do not change:
- a plain number: digits, an optional sign, one decimal point and an optional percent sign, such as `-12`, `+5`, `-1.50` or `-5%`
- a run of dashes, the empty-cell marker: `-` or `--`

Neither kind can hold a function call or a DDE string. Anything longer is prefixed: `-1+1`, `-1+cmd`, `-@SUM(1)`, `--1` and `-=1` all are. Some values are not changed by this helper:
- a value that starts with a space, a new line or a Unicode look-alike of `=`
- numeric columns that the exporters write unquoted, outside the helper: sheets, pages, size and cost
- the server-side exports

These are listed for a follow-up. A negative amount that carries a currency sign, such as `-$1.20`, now opens as text and shows the quote mark.

### Settings validation dialog, first-run connection test, user table (RD-861)

**Before:**
- The settings validation dialog and its quick-question twin wrote the validator's suggestion, message, suggestions and saved id as HTML.
- The first-run connection test wrote the server's row count, connection mode, failure message and troubleshooting tips as HTML.
- Its error panels, and the workspace save panel, wrote the error message as HTML.

A value holding `<img src=x onerror=...>` became an element with a handler. Real Chromium ran the handler in each of these places when no CSP was set.

In the user table, a user name went into `data-arg` and `title` attributes through an escape that leaves quote characters alone. A name holding a double quote could close the attribute and add its own attributes. In Chromium, `x" onfocus=... autofocus` ran its handler.

**Now:** each of those dialog and panel values goes through the file's own `escapeHtml`. The user table row, the info button and its class go through a new `escapeAttrValue`, which also writes both quote characters as entities. Text a person reads is unchanged: `A & B`, `O'Brien`, `say "hi"` and `&lt;b&gt;` show exactly as typed, and a new line in a validator message is still a line break.

**Limit:** `settings.js` defines `escapeHtml` twice, and the page uses the second definition. That definition turns a non-string value into text without escaping it. A validator field that arrives as an array or object holding markup would still be written as HTML. The validator sends only strings today, plus one constant array.

## Cells

- `__tests__/rd835-csv-cells-are-not-formulas.test.js`: 22 cells. They cover the helper (each leading character, the number and dash exemptions, text that only begins like a number, and empty values), each of the ten writers, the rows that must not change, and the shipped text.
- `__tests__/rd861-server-text-stays-text.test.js`: 20 cells. They cover the five dialog values, the four connection-test values, the attribute break, the unchanged ordinary output, and the shipped text.
- With the fix removed, 19 of the 22 and 15 of the 20 cells fail, and every cell that pins unchanged output stays green.
- The test-count file moves from 6086 tests in 384 suites to 6128 in 386.

## Left for a follow-up

Other places in `static/js/index.js` still write a user name, a scan file name, a printer host name or server text unescaped. Examples:
- the anomalies table
- the risk query result tables
- the recent scans file name and its `title` attribute
- the printer rows' `data-arg`

They are different statements from the ones fixed here. The strict CSP, on by default, blocks inline handlers there. The chat bubble region has its own ticket.

Not deployed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
