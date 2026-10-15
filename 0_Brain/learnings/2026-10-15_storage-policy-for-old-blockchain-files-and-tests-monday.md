---
date: 2026-10-15
type: grant
source: Kam, terminal 2026-10-15 ~15:4x AEDT
status: live
tier: W
---

# On Monday 19 Oct, write a storage policy for old Blockchain files and old tests: what is not needed going forward may be REMOVED, and the clean-up runs regularly

**His words, verbatim:** *"on monday, please create an efficient policy to create more efficient storage of old blockchain files and old tests.  If we do not need them going forward, they can be removed and this can / should be done regularly"*

**The operative case, so the headline matches it:** a Wednesday seat on Monday 2026-10-19 (`date -j`: Monday), or any seat about to tidy Secuura/Blockchain storage before the policy exists. **The deliverable on Monday is a POLICY (a document plus the mechanism that runs it), shown to Kam. It is not a clean-up run.** Nothing is removed under this file until the policy exists and Kam has seen it.

**How to apply (Wednesday's reading, receipted on the panel with a correction offer):**
1. **Scope:** Secuura/Blockchain (Platform K): old worktrees and scratch clones, old run dirs and gate evidence, superseded test artefacts and fixtures, old local-model run dirs for Secuura tasks, and old build or docker leftovers on the boxes. Measure each class first (sizes, counts, ages) and write the numbers into the policy.
2. **"If we do not need them going forward, they can be removed":** this NARROWS [[2026-08-26_never-delete-cleanup-means-quarantine]] for the classes the policy names. Every class carries its predicate for "not needed" (age, merged state, superseded-by, regenerable). The rest of the never-delete rule stands: files we are working on, records, the brain, credentials, anything unmerged, and anything a live seat holds are never in scope.
3. **Order of preference:** regenerable leftovers are removed ([[2026-09-29_regenerable-build-leftovers-are-not-kept]]); bulky but possibly useful items go to G-DRIVE first and are cleared after about a month ([[2026-10-07_archive-bulky-leftovers-to-g-drive-clear-after-a-month]]); only then outright removal.
4. **"Regularly" = a scheduled mechanism, not an intention** ([[2026-08-07_a-promise-is-not-a-mechanism]]): a dry-run report on a cadence (proposed: weekly), with the actual removal by the project's own seat under the policy. Exercise both branches before arming it. It cannot remove anything outside its named classes.
5. **Hard rule 1 holds:** Wednesday writes the policy and the dry-run tool in her own tree. Removals inside the Secuura project are the project seat's acts.
6. **Monday's output:** the policy file, the dry-run's first report with the numbers, and a card to Kam with the policy's BLUF and the first run's proposed removals (default: run the dry-run weekly and remove nothing until he taps).

**Family:** [[2026-08-26_never-delete-cleanup-means-quarantine]] (narrowed, not retired) · [[2026-09-29_regenerable-build-leftovers-are-not-kept]] · [[2026-10-07_archive-bulky-leftovers-to-g-drive-clear-after-a-month]] · [[2026-09-06_a-scoped-override-carries-its-own-expiry]] (the Monday date is the trigger) · [[2026-08-03_go-slow-earn-autonomy]] (rule 5: every grant recorded).
