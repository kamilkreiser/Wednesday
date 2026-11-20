# FOR-RECORDS (gate B1818, round 1 of 2 on "the refresh of pull request 85")

## What a records pass after this gate should write
1. A ruling line: independent G1 review of PR 85 at `2a58dc5d9c62cc021b01e3fe5ebdcd09e76d7f9a` on main `b4681297d974ac3d8e74a4a12baeb9ea41962c52`: GO WITH FINDINGS (Notes only). The old B424 verdict expired with the old head and this one replaces it, for this head only.
2. The deploy refusal as a standing record: from the squash onward, main carries a changed content release (demo `5db37614…`, draft `5679855b…`). No Composer host deploys it without the product owner's own card. The instrument is `git diff --quiet <last deployed> <to deploy> -- content/release-demo content/release-draft`, and rc 1 refuses. Record the deployed release hash as the demo runs it, once someone measures it; it was NOT measured in this lane.
3. The two Minors that ride with the branch keep their rows (B358-2: BACKLOG #367 / PCOMP-66; B424-1: BACKLOG #368 / PCOMP-67), unchanged by the refresh.
4. New Notes from this gate, for BACKLOG candidates (none blocks):
   - N2: test files are outside the project's `tsc`. At main, `tsc --noEmit` over the engine, content, renderers, canonical and api test files reports 23 errors; at the merge 25, the 2 extra in the PR's own `packages/content/test/b330-sm316-catalogue.test.ts:362,423`. Fix shape: a `typecheck:tests` script with a test tsconfig per package, fix the 25, add it to `ci:node`.
   - N3: main's change report now inherits the PR's table-cell break rule (camel-case boundary, before "("). It is covered by `change-report.test.ts` (green). Fix shape: none needed; if the change report's tables ever pin cell text, pin it at the merged writer.
   - N4: `scripts/test-db.sh` uses an `--internal` network, not `--network none` (by design; no egress). Record it so later kits stop calling every DB run "network none".

## Kit wording to correct in any successor
- **E9 (prediction row):** "any name present at main and absent at the merge is a STOP" contradicts the table header's "a difference you cannot name is a STOP". Successor wording: "lost names: each one must be a title the pull request itself removes, in a file the pull request edits and main does not, with an added title in the same file whose body holds the same assertions re-pointed (printed). Any other lost name is a STOP." Also expect data-driven titles to grow: tests that title themselves by file (`s45-cr-jcs-iterative.test.ts` titles each `content/` file) add names in files neither side edits.
- **The name scan in kits:** the unbounded `B[0-9]{3,4}` matches inside hex hashes (`5db37614` holds `b3761`). Use the word-bounded `\b[Bb]\d{3,4}\b` and keep a planted control.
- **The branch name holds a brief number** (`b330/…`). A landing text that must name no brief number cannot name the branch. Say "the pull request's head branch".
- **The "typecheck" claim in any kit** covers `src` only. Say so, or add the test-file tsc probe.
- **E7's DB-group wording** should say "internal network" for `test-db.sh`.

## Questions decided by nobody
1. Should the repository carry a guard (a test, a script or a record file) that refuses a deploy when `content/` differs from the last deployed release? The builder raised it (its Q-4) and nothing has been built. Today the refusal lives only in deploy orders and records.
2. Which release does the live demo run? It is NOT measured. The records relay main `b4681297` with demo release `05070f1d…`.
3. Are the new release's E8 citations green? The SOW text is withheld, so no lane has measured it at this head.
4. The browser specs under `apps/web/e2e/` that name the release: never run in this lane or the builder's (they need the stack).
5. Whether "HP Security Manager" may appear in a commit message on main: main's history has 0 such messages (and 117 that say "HPSM"). The reviewed squash texts avoid it. The PR body text (not in git) used it before this gate, and the reviewed body says "SM 3.16".
6. The commission asked for the squash subject to end `(#85)`. main's own recent squash subjects do not carry the number. Nobody has ruled on which form the project wants.
