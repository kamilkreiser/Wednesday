## What changed

Three code comments in shipped files no longer carry a demo revision name or a retired VM address, and the identifier guard's list of known findings loses the five entries that described them. One existing guard cell now proves its per-kind property on a different file. Three files changed; no product behaviour, route, string a user sees, helper, count or workflow changed.

- RD-689: two comment lines in `backend/server.js` (the CSP note and the origin allow-list note) and one in the header of `backend/services/schedulers/healthSweeperScheduler.js` are reworded to say the same thing without the value. Each edit replaces one line with one line, so no line number in either file moves, and the comment-stripped text of both files is unchanged.
- The five reviewed entries that described those findings are removed from `__tests__/rd385-shipped-root-markdown-identifiers.test.js` in the same change, with the comment that introduced them. Without that, the stale guard goes red.
- The guard cell "ARM (RD-828 C-F1)" planted its case in `backend/server.js` and asserted that the file still held a finding of the resource-name kind. Once that value leaves the file the precondition is false. The cell now plants a finding of another kind in `backend/marketplaceJwt.js` and still proves that a kind leaving a file that keeps another kind is reported stale for that kind only. Its title is unchanged; no cell is added or removed.

## How it was checked

- Full `npm run verify -- --maxWorkers=2` on the branch head: PASS, 5870 tests in 377 suites, equal to the committed pair.
- The guard test alone: 58 of 58 cells pass at the head. The test edit alone (old comments in place) turns 3 cells red; the comment edits alone (old entries in place) turn 7 cells red; so the two halves are needed together.
- Putting back the old "file only" stale check turns the re-pointed cell red, and so does removing its planted finding.
- The comment-stripped text of both source files is identical before and after; the audit-log region of `backend/server.js` is byte-identical.

## Risk

Comments and one test cell only. A merge to main will start the demo deploy workflow (these paths are not on its ignore list); nothing is deployed by this branch itself.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
