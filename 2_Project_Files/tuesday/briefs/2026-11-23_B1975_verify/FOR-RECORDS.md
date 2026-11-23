# For the records seat: the signal file read race (gate B1975, after the landing of b1966/nexusai-signal-read-race)

## The NEW ticket (no ticket names the race; B1965 and the seat searched Jira; the gate did not re-read it)
**Summary:** rd711 and rd615 read the slow-audit-flush preload's signal file the moment it exists, so a read between its
create and its write sees an empty file and fails the whole rd711 file on a loaded runner.
**Description:** the preload writes the file with `fs.writeFileSync` (create, then write) at
`__tests__/helpers/rd615-slow-audit-flush-preload.js:28`; `rd711-audit-flush-serialised.test.js:68-69` and
`rd615-audit-flush-cannot-resurrect-erased-entries.test.js:87-88` read it as soon as `existsSync` is true; one hosted
build (pull request 242, 1 red in 20 builds that carried rd711) failed four cells from one `SyntaxError: Unexpected end
of JSON input`. Measured: the probe read 11 and 14 of 2000 empty reads (drafter), 1 of 2000 (seat), tmp-then-rename 0;
under a planted writer that holds the file empty for 700 ms the real files at the old readers read 8 of 8 red (seat's
red-first, and the gate's own run at BASE: 8 of 8 red, every failure `Unexpected end of JSON input`), and with the new
readers 8 of 8 green (seat twice, gate once, plus the real preload 8 of 8).
**Fix:** test-side; both readers wait for "exists and parses" within their existing bound; the preload unchanged (rd711's
header records the product owner's 2026-11-16 answer keeping it; that answer is quoted from the file, in no committed
text). One commit, two files, +16 -4. **Option not taken:** write the signal atomically in the preload (tmp then
rename), which would touch that answer. **Related:** RD-711, RD-615 (origin), RD-787 (CodeQL js/file-system-race class,
test code), RD-911 (wall-clock bounds on a stalled runner, nearest class). **Acceptance:** both readers parse before
they accept; the planted-writer cells red at BASE and green after; no counts change (6235 / 394); hosted checks of the
landing head green.
**Who decided:** the coordinator (test-side, one commit, no ticket key in the commit), under the standing backlog grant.
The product owner is named only through his dated 2026-11-16 answer in rd711's header.

## Relation to RD-711 and RD-615
RD-711 (Testing) is the product fix rd711 pins; RD-615 (Release Ready) is the origin of the preload and of rd615. This
change touches only the two tests' reads; neither ticket's product behaviour moves. Both may take a comment pointing at
the new ticket after the landing. Not edited by the lane or the gate: HISTORY.md, BACKLOG.md, CLARIFICATIONS.md, Jira.

## From the gate's findings (none blocking)
- `rd525-live-store.js:121-123` already tolerates the same race and is untouched.
- rd711's `waitFor` calls the condition once more after the loop to compute its return; with the new condition that is
  a second file read. A second preload write (a second `mark`) in that instant would make `windowOpen` false; marks only
  recur after a SIGTERM the test sends later (rename mode: the next interval flush is 60 s on), so no path reaches it
  today. Info only.
- rd711 `given.what` would throw on a file whose JSON is `null`; the preload never writes that. Info only.
- The hosted rate of the race is unmeasured; the planted writer makes the gap certain, not likely.
