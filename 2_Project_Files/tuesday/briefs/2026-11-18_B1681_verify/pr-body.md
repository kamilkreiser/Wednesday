## What changed

Four test files and the expected-counts file. No product file, no helper and no workflow changed.

- RD-1002: the header of the three-routes test now names every cell the file holds (it was missing H6, H7 and H8) and carries no cell count, so it cannot go stale again. Comment lines only.
- RD-734: the export cell's stop bound is now 20 s, the time the harness's stop really waits (SIGTERM, up to 20 s, then SIGKILL), and the comment says where the old "5 s each" came from (the failed-boot grace, a different path). The cell's jest budget is now 168000 ms, no longer equal to the sum of its own bounds.
- RD-729 (finding A-F1 only): the boot-deadline cell now fails under a flat 5 s attempt cap. Its bound is the 3 s deadline plus a 1500 ms margin, where it used to be 8 s. The other findings of that ticket are left open.
- RD-730: the gate-table format check now reads past a blank line to the next heading, so a malformed row after a blank line is reported. A tree with no git on the PATH now registers its own title ("GIT NOT AVAILABLE") instead of "NOT A GIT CHECKOUT". Two new control cells pin both.
- Counts: the suite now holds 5870 tests in 377 suites (was 5868 in 377).

## How it was checked

- Full `npm run verify -- --maxWorkers=2` on the branch head: PASS, 5870 tests in 377 suites, equal to the committed pair.
- Each new or changed check was made to fail on purpose: the old format-check line restored turns the blank-line cell red alone; two broken versions of the git probe turn the probe cell red alone; a flat 5 s attempt cap in the harness turns the boot-deadline cell red, and the previous version of that cell stays green under the same plant.

## Risk

Test files only; nothing is deployed by this change. The boot-deadline cell's 1.5 s margin sits between the measured real time (about 3.15 s) and the flat-cap time (about 5.65 s).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
