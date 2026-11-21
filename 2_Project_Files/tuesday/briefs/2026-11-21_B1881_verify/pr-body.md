## What changes

Two developer documents, words only. Nothing is deployed and no code, test, template or contract byte changes.

**docs/ENGINE.md, row X-39 (MPSCALC-420).** One clause of one line is replaced. The row said the contract and the screens do not carry the purchase recurring projection. It now says what main does: the contract carries it for a caller with internal-metrics (`purchase.projection`, absent for any other caller) and the purchase result screen shows it to that caller as a table. Every other byte of the file is unchanged.

**infra/README.md (MPSCALC-417).** 16 lines are added and no existing line changes:
- Step 2 is marked as the record of the first deploy, and says that with neither client id exported the command stops at the parameter file; to what-if an existing site, export both ids first, as step 6 does.
- The pinned budget start is stated with what to change if a first create is refused. Whether the budget service accepts a past start on a first create is said to be not measured.
- The differences a what-if of the existing site showed on 2026-11-20 are named (the budget's start Modify and end Delete, and nine site-config Create lines), so a reader counts changes net of them.

## Who reads these files

These are developer documents on the coordinator's reading under the project's standing rule for developer-only documentation; the product owner has not ruled on these words. A probe of the files the build ships or the API serves found no path by which either file reaches a customer (the repository is private; the API serves only the web build folder).

## Checked

Each added sentence was read against the code at main. The hosted facts in the README (what the what-if showed, that an update with the same past start was accepted) are written as read on 2026-11-20, not as always. The Python test files that CI runs (15 files) pass at the head, including the test that reads the README.

## Not tested

Hosted CI and CodeQL (they decide on this pull request). A build of the web bundle. Any hosted probe. A first budget create after October 2026 (said so in the README).

Not deployed. Nothing in this change deploys.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
