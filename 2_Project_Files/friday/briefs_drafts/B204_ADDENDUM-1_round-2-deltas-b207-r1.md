From Friday (laptop seat), Datasec / HPSM-POC. Replies go to your STATUS file.

# B204 ADDENDUM-1 (Seat C): GATE ROUND 2 OF 2 (tier 1), deltas only, on `b202/attribution-preview-r1` @ `42b439eca6a7380d8f2af361e01bdd56792a6604`

**To:** Datasec/HPSM-POC-C (you, gate B204). **Builder report:** `Briefs/2026-10-11_B207_STATUS.md` (whole, including its `## ADDENDUM-1` section). **Rulings it built:** `Briefs/2026-10-11_B207_SEAT-B_b202-rebase-and-fix-round-1.md` and `Briefs/B207_ADDENDUM-1_q-b207-1-alias-scope.md`.
**Round 2 of 2 under the cap:** a NO GO here ships the closed items and tickets the residue; there is no round 3 without Kam's word.

## Pins (re-read with `ls-remote` at start and before the verdict; STOP if one moved)
- head `b202/attribution-preview-r1` = `42b439eca6a7380d8f2af361e01bdd56792a6604` (Friday's GitHub compare API at 15:5x: main...head = ahead 11, behind 1, 54 files).
- main = `76acd696a1c99aa449cc040ac11e852648d95efe` (PR #136, the B203 squash; tree `85f6bbfc…`).
- Your round-1 head `62bc3c5` (tree `a50b999fa3fe85018337f71705a322652fa06c2b`). The builder reports the rebased tip `d58fcfc` keeps that tree. Prove it yourself (`git rev-parse d58fcfc^{tree}`), and prove the five replayed trees, because a tree-equal rebase means your round-1 content verdict carries over to `d58fcfc`.

## What to test (deltas `d58fcfc..42b439e`, plus the merge)
1. **M-1:** the reset regression test exists, is green at head, and goes RED under your own a02 on SQLite AND SQL Server.
2. **M-3:** the tag-in-header and zero-guard tests go RED under your w03 and w01.
3. **M-2:** the NEW WORDS table is complete. Use your own rendered-lines probe at 1280 and 390, for Admin, Consultant and Demo, and Partner's role screen. The new notKeyed copy must be true for 0, 1 and N.
4. **N-1:** comment-only (0 non-comment lines).
5. **N-3 + ADDENDUM-1 (the alias ruling):**
   - `getMetricsSummary` carries no `customerName`, and an alias equal to the preview's for every caller (Partner+Demo, Admin, Consultant, Demo); a pre-key customer is null.
   - The linked page shows the alias when the caller holds Demo and the name for a Partner without Demo, decided from `/api/v1/me` roles.
   - Nothing flashes the name while loading or when `getMe` fails.
   - Your own mutants against both.
   - Record A1-F1 (the customer shell's breadcrumb and journey rail still show the name on `/metrics`). It was KNOWN and left out of scope by Friday's addendum, so it is not B207's defect. Grade only what the ruling scoped; Friday takes A1-F1 to Kam.
6. **Contract:** 0.16.0-draft extended, not bumped. Confirm 0.16.0 is not on main before `42b439e`. If it is, that is a finding.
7. **Regression:** the full API suite once at head, the SQL Server classes for Attribution + MetricsSummary + Contract, vitest, and the Playwright set. Treat RequestTimingLogTests as a known runner-timing flake family: record it, do not chase it.
8. **MERGE line against `76acd69`:** `merge-tree --write-tree 76acd69 42b439e` (the builder reports clean, tree `d82e339…`); build and test that tree once.

## Verdict lines (first lines of your STATUS, appended as a `## ROUND 2` section, or a new `2026-10-11_B204_R2_STATUS.md` if you prefer)
`B202-r1 42b439e: GO | GO WITH NOTES | NO GO` and `MERGE 76acd69+42b439e: …`; last line `READY FOR REVIEW`.

## Holds (unchanged)
Findings only; no code, push, PR or comment, Jira, deploy, Azure, mail, or anything to any human. Datasec only. No Restricted documents. Never delete, quarantine. Kill by port and cwd, never by name. Your ports stay 6681–6699; Seat B's are 6720–6729 (containers stopped, not removed: leave them alone).

**One more item, not a test:** Seat B reports it printed your local Azurite emulator key (from `4_Credentials/b204-azurite.env`) to its own terminal transcript only (no file). It is the emulator key of a local container. When you next start that container, say whether you regenerated it. No other action.
