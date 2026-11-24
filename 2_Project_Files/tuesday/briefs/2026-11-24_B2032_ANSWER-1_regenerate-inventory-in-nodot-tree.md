# B2032 ANSWER-1 (Tuesday, s321, 2026-11-24, to seat Datasec/NexusAI-N169): YES, regenerate the inventory once in a dot-free tree

Your question (STATUS last line at 12:04:44): may you regenerate the inventory in a dot-free tree `b2032-nodot/gen`, under one extra jest-lock acquisition, because `res.sendFile` answers 404 for the four page rows when the absolute path holds the `.tools` segment, and take A's two docs files from there?

**Answer: YES, exactly as you proposed, with these bounds.** Tuesday's call (the coordinator's), not the product owner's.

1. **The tree:** `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/b2032-nodot/gen`, a `worktree add --detach` of YOUR clone at BASE `d96a83d3ee6df25f74bcfe2f9ec0d0b42714e029`, plus `apply2032.py <gen> apply` (six lines, as in `work`), plus the frozen new test file, plus the `node_modules` symlink to the clone's. Print its `git status --porcelain` (the same six `M` and one `??` as `work`) and its jest slot before the run.
2. **The run:** ONE extra acquisition, tag `b2032-gen`, running ONLY `node scripts/role-capability-inventory.js --generate` in `gen` (the same command the chain used), `NODE_OPTIONS` unset, `--maxWorkers` not applicable. The lock count becomes 4 (b2032-lane, b2032-gen, b2032-verify-update, b2032-verify-plain); say so in STATUS. HOLD 63 applies to `gen/backups/` (quarantine the backup files, count = the printed count).
3. **The check is chain step 4, unchanged, run on `gen`:** the JSON changes exactly the two rows (`GET /api/debug/data-sources`, `GET /api/setup/data-sources`) and the two meta lines; the page changes its stamp line, the two summary rows the viewer's 403 move makes, and the two route rows; `originMain` is BASE's sha40. **The four page rows (`/first-run-setup`, `/login` and the other two you named) must read as they do at BASE (not 404).** Any other change is a STOP, as written.
4. **Commit A takes the two docs files from `gen`**, the other seven paths from `work` as written (cmp each). The `work` tree's two docs files are NOT used; leave them as they are (no revert needed, never delete).
5. **Record it:** a `## Corrections` entry naming the cause you measured (`backend/server.js` 3028-3056, `send`'s default `dotfiles: 'ignore'` on an absolute path holding `.tools`), and that the drafter's prototype ran in a dot-free path (`fleet/state/s321/d2032/`), which is why it did not see it. This is a kit fault, not yours.
6. Everything else in the kit stands (both verifies run in `b2032-nodot/vupd3` and `chk24`, which are dot-free; CodeQL; the push; no PR).

Then resume the chain at step 4 on `gen`.
