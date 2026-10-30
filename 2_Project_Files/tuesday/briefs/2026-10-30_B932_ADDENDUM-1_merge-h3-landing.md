From Tuesday (the Datasec coordinator seat) to SEAT-H63, Datasec / HPSM-POC. ADDENDUM-1 to BRIEF B932. Binding.

**H3 HAS LANDED. Bring it in now, per your kit's D-3 rule (merge, never rebase).**

- PR #244 (the shared primitives: customer/parts.tsx StagePill wrapper, ui/Table.tsx classes) landed as a head-pinned squash. HPSM-POC main is now `7365165d50193082ec3daf6eca137cd0ff0d4588` (parent `e21d8044`). Verify it yourself: `git --no-optional-locks ls-remote origin refs/heads/main`.
- Fetch under your lock.sh with the explicit refspec `refs/heads/main:refs/remotes/origin/main`, then in your fix worktree: `git merge --no-ff --no-edit 7365165d50193082ec3daf6eca137cd0ff0d4588`. That is ONE new commit; the push is a plain fast-forward of your own ref `b932/hpsmpoc-372-partner-home`. Never rebase, amend or force.
- Before merging: `compare e21d8044...7365165d` must list ONLY customer/parts.tsx, ui/Table.tsx and their two test files. Any of YOUR PATHS in that list, or a merge conflict, is a STOP: `STOPPED: NEEDS TUESDAY main moved into my paths`.
- After merging: re-run your CI-order checks (lint, typecheck, build, unit, check-shards, the e2e you ran before) and the screenshots on the merged head, read them, and note what the new StagePill and table classes change on your page. Do not put whitespace-nowrap back around a StagePill.
- Push, read back with ls-remote, and end READY FOR QA again with "H3: in base 7365165d" (or "merged origin/main 7365165d"). Your PR is already open; Tuesday commissions its gate from your new READY line.

Nothing else in B932 changes.
