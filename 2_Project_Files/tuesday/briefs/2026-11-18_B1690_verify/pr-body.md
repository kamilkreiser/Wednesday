## What changed

Four weaknesses in the tests of the log-injection fix are repaired. Two test files change; no product file, helper, route, string a user sees, count or workflow changes.

- RD-980 item 1: the mask on the job line of the business-hours report now matches a date-time shape only. Before, it also swallowed text placed right before or right after the time, or the words Invalid Date in place of the time, so the cell for the off-hours report stayed green. The cell that tests the mask gains five rows: a de_DE-style time and a PM time with a narrow space must still compare equal, and a marker before the time, a marker after it and an unreadable time must compare different.
- RD-980 item 2: the two masks on route 190 (the off-hours paragraph and the digits of the Critical Issues count) are removed. The masked text is fixed inside each pinned state, so the masks hid a change and pinned nothing. Each state (day, night) now freezes its own value. This takes the first-listed of the ticket's two options. The two cells that tested those masks are rewritten in place as negative controls (the two reports must compare different), so they go red if either mask is put back; no cell is added or removed.
- RD-980 item 3: every server boot in the chat-and-learning file now runs the child in the C.UTF-8 locale, so a developer shell in another locale (de_DE turned twelve keys of one cell red) no longer changes the numbers and times the child prints. The shared harness is not touched.
- RD-980 item 4: one cell title in the auth-and-storage file now says what it asserts: the first 8 characters of the state and of the cookie, and MISSING for an absent cookie.

Six cell titles change; the counts of cells are unchanged (65, 23 and 33 in the three log-injection files).

## How it was checked

- Full `npm run verify -- --maxWorkers=2` on the branch head: PASS, 5870 tests in 377 suites, equal to the committed pair.
- The three log-injection files run under a German locale: one cell red before the change (the locale cell), all green after.
- Planting a marker before or after the job time, an unreadable time, a changed Critical Issues count, or a marker in the off-hours paragraph in a scratch copy of the server turns exactly the named cells red at the head and none red before.
- Putting a route 190 mask back, or the old job-line mask, turns the cells that guard them red.
- CodeQL (javascript, security-extended and code-scanning) over the two changed test files: no rows before or after.

## Risk

Test code only. A merge to main starts the demo deploy workflow (these paths are not on its ignore list); nothing is deployed by this branch itself.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
