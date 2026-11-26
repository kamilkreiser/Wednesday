Four commits on `e789995a`; seven paths; no `backend/` or `static/` file, no workflow, nothing deployed.

## RD-1044: `scripts/qa-surface-up.sh`, the first-boot block
- The block's log is now a temp file made by `mktemp` outside the data folder (under `TMPDIR`, or `/tmp`). A failed first attempt that fails before the product writes anything leaves the folder empty, so the retry runs the block again.
- The block's state test accepts exactly `first-boot` and `ephemeral`. A data folder whose path holds `/tmp/` reads as `ephemeral` in `backend/jsonStorage.js` and the product still writes its sentinel there; the old test accepted `first-boot` only and stopped such a first run with exit 13. Any other state still exits 13.
- New file `__tests__/rd1044-qa-surface-first-boot-block.test.js` (7 cells) runs the block itself, by bash, as the script does. Four cells read red before the change and green after; three are controls.

## RD-1043: `__tests__/rd974-undated-job-is-not-off-hours.test.js`
Three cells added: an undated job stays out of the week bucket (with a dated control), and the unusual-time item needs more than 10 dated off-hours jobs (10 raise none, 11 raise it, with or without undated jobs beside them). Each reads red on a copy of `backend/server.js` with the one change named in the ticket and green on the file as it is. `backend/server.js` is not changed.

## RD-1045: the shared harness and the live-store helper
`bootServer` (`rd395-server-harness.js`) and `makeDataDir` (`rd525-live-store.js`) make their data folders with `persistentTempDir` from the existing `persistent-temp-root.js` (byte-unchanged). On a hosted Linux runner `os.tmpdir()` is `/tmp`, where the product never raises its volume-wiped alarm, so a cell that asserts "no alarm" passed there without testing anything. A test cannot move the folder by assigning `process.env.TMPDIR` (jest hands a test a copy of the environment, the core `os` module reads the real one), so the new file `__tests__/rd1045-boot-folders-are-persistent.test.js` (3 cells) replaces `os.tmpdir()` for one call and reads where each helper puts its folder, plus a source pin.
The counts file moves from 6463 tests / 405 suites to 6476 / 407, written by the project's own command.

## Choices made by the coordinator, not by the product owner
One kit for the three tickets; RD-983 is not part of this change (it was already landed by pull request 208); the stand-script log is made by `mktemp` outside the data folder; the state test accepts `first-boot` and `ephemeral`; the harness and the live-store helper change, `persistent-temp-root.js` does not.

## Reviewed
An independent review (Sonnet tier) re-ran the three test files in two shapes (the Linux shape `TMPDIR=/tmp` with a persistent `RUNNER_TEMP`, and a macOS environment) at the base and at the head: seven cells red at the base and none at the head, with the controls green at both. Five one-line mutations (log back in the folder, state test narrowed, harness back to `os.tmpdir()`, threshold read as more than 9, week key taken from the time of the read) each read red on exactly the cells named. No cell is removed, skipped or loosened; no platform or CI condition added; gitleaks clean.

## Named limits
- A failure AFTER the product has written a file into the empty folder (the retry then sees a folder that is not empty and skips the block, so no sentinel is written) is not covered; the cell for a failed first attempt fails before the product runs.
- The log file made by `mktemp` is not removed (one small file in the temp folder per run; the new test file leaves seven per run).
- The 58 other test files that boot a server and still make a folder of their own under `os.tmpdir()` are unchanged. A term scan of them found no "no alarm" cell on a `/tmp/` folder; that scan was not a cell-by-cell read.
- GNU `mktemp` was reasoned equal to the macOS one (the template carries six X, no option), not run.
- The hosted `build` job of this pull request is the FIRST real Linux measurement of the three new files; locally they were run in the Linux shape (33 of 33) but not on a Linux machine. A red there on a new cell is a fix round.

## Deploy
None. The merge touches `scripts/` and `__tests__/`, so the Deploy demo workflow starts on the push; both its jobs are expected to read skipped (the switch variable is not set).
