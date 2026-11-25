## What this changes

Two test tools raised the product's volume-wiped alarm on a data folder that had never held anything.

- `bootServer` (`__tests__/helpers/rd395-server-harness.js`) wrote `.machine-id` into the new data folder with `fs` before the server started. The product counts a `.machine-id` that the booting process did not write as proof the folder already held state, so on a path without `/tmp/` (macOS `os.tmpdir()` is under `/var/folders`) every harness boot logged "Persistence sentinel MISSING" and two more alarm lines at error level, and re-created the sentinel.
- `scripts/qa-surface-up.sh` copied the dataset into the data folder before the first boot, with the same result and a red "Persistent storage check failed" banner on every page of the surface.

The fix is in the two tools. No product file changes (`git diff --name-only` of the branch against main names four paths: the harness, the stand script, one new test file and the counts file).

- **Harness.** A seeded boot now takes its machine identity from the product's own writer: `MACHINE_ID` is set for one synchronous call of `JsonStorage.getMachineIdentifier(dir)` and put back in a `finally`. The seed store and the server still share one identity (the RD-568 cell is unchanged and green). An unseeded boot writes nothing: the server makes its own identity, as on a first deploy.
- **Stand script.** A new block, between `first boot: BEGIN` and `first boot: END` marker lines and before the dataset is copied in, builds the product's store once on the still-empty folder, which writes the sentinel bound to that folder. It does so only when the folder is empty and holds no sentinel. A folder that already holds anything is left alone, so a surface that really lost its sentinel keeps its alarm. If the first boot cannot be made the script stops with exit 13 and names the folder.

## Choices that are the coordinator's

- The product writes the identity and the sentinel; the harness never copies, forges or pre-arms a sentinel.
- A stand folder that already holds data and has no sentinel keeps its alarm.
- No product change (no "test boot" marker, no switch that silences the alarm).
- The stand script now leaves `qa-surface-first-boot.log` and the product's initial store files in a fresh surface's folder before the dataset overwrites them.

## Not in this change (disclosed)

- **Other boots that still raise the alarm.** A measurement taken before this change (an error-line preload over the 116 suites that boot the server; not repeated at review) found 13 data folders in 8 other test files that write their own machine marker or stores before starting the server: 7 files start the server themselves, 1 goes through `__tests__/helpers/rd525-live-store.js` (`makeDataDir` writes `.machine-id` with `fs`). Those files are not touched. They need a shared first-boot folder helper or a change to each caller, and are left for a follow-up ticket. (Beside the 13, one cell of another file boots a foreign identity on purpose and is meant to alarm.)
- **A stand folder inside a path that contains `/tmp/`.** The product treats such a folder as ephemeral and still writes a sentinel there, but the new block reads that first boot as "ephemeral", not as a first boot, so the first run of the script stops with exit 13 and names the folder; the sentinel is then already on disk and the block is skipped from the next run on. Measured by running the block alone on a scratch folder; the script was not run whole. No workflow in the repository calls the script.
- **A first boot that failed leaves its log in the folder.** The block opens `qa-surface-first-boot.log` in the data folder before the product's store is built, so after a failed attempt (measured: `node` missing from `PATH`) the folder is no longer empty, a retry skips the block and writes no sentinel, and a dataset copied in afterwards is the case the ticket names (cell Q3 reads it as wiped).
- Not tested: a Linux or hosted runner (the new cells point `TMPDIR` at `RUNNER_TEMP` or `/dev/shm` so the product can alarm there; they were run on macOS), the whole stand script end to end, a boot with `MACHINE_ID` exported in the shell beyond the review's probes, a real browser.

## The result (14 new cells; one new test file)

- Before (main plus the new file alone): 10 of the 14 cells fail; the 4 controls (the real alarm still fires through the harness on a volume that lost only its sentinel; the product itself still alarms on a folder with a store and no sentinel; the scan sees the old shape; a dataset copied into an empty folder with no first boot is the alarm) pass. After: all 14 pass. With only the two tool edits reverted, the same 10 fail. A wrong fix that re-arms the sentinel after the seed turns only the real-alarm control red.
- Full verify of the merge of this branch into main (`8d8dd76c`): `VERDICT: PASS`, 6463 tests in 405 suites, the pair the counts file carries.
- Local CodeQL (javascript), main against head: NEW 0, KEPT 0 (a local run, not repeated at review).
- gitleaks over the diff and the commit messages: no leaks found; the control fired.

## Files

- `__tests__/helpers/rd395-server-harness.js` (14 added, 2 removed).
- `scripts/qa-surface-up.sh` (25 added).
- New: `__tests__/rd1037-harness-boots-raise-no-sentinel-alarm.test.js` (14 cells).
- `scripts/verify-expected-counts.json`: 6449 / 404 to **6463 / 405**, by `npm run verify -- --maxWorkers=2 --update-counts` (second commit).

## Deploy

None. Merging starts a `Deploy demo` run, because `__tests__/**` and `scripts/**` are not in its `paths-ignore`. Both of its jobs require `vars.CI_DEPLOY_ENABLED == 'true'` and the repository has no Actions variables; the deploy job is also bound to the `demo` environment. The last runs of the workflow all read skipped. No served file changes.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
