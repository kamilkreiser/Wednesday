# B172 DRAFTER REPORT: SEAT-E2, MPSCALC-231, the stale CARE-PACKS class clause
Drafted 2026-10-18, 06:38 to 06:46 AEDT. Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-18_B172_SEAT-E2_mps-carepacks-rule-text.md` (98 lines, 19,598 B; sha256 `9739f4c5…c0c224` before this report was written; Tuesday's stamp will change it).

I wrote nothing under `!CODING/`. Tools used:
- git read verbs with `--no-optional-locks` (`ls-remote`, `cat-file`, `rev-parse`);
- `gh api` GETs under the MPS `GH_CONFIG_DIR` (`kamilDatasec`): contents at e6f92a5, the e6f92a5 tarball (extracted to my scratchpad), and `pulls/76`, `pulls/78`, `pulls/78/files`, `pulls?state=open`, `pulls/83`;
- Jira read-only GETs through a scratch client that reads `JIRA_*` by name and never prints them;
- `decision_queue.sh list` / `show` (read).

No fetch, no worktree, no az, no hosted call, no mail.

## B number
B172 is free in both `tuesday/briefs/` and the MPS `Briefs/` (ls + grep 06:44:12: no `B172`…`B179`, no `B258+`).

## Measured
- **Main** `e6f92a5f7568b2f2d72f454524b8e09406357957` (ls-remote 06:39:08, 06:43:57). It is not in the local store. No open PR; #83 = 404.
- **`PriceBookImporter.cs:140` at e6f92a5** ends `Item class: service (default K-05, until MPSCALC-142).` (contents API = tarball, `cmp` equal).
- **The code's rule:**
  - `PurchaseCatalogue.cs:145`/`:148` `ItemClass.CarePack`;
  - `PurchaseCalculator.cs:45` (services group);
  - ENGINE X-31 `:147`;
  - `IMPORTER.md:16`: *"Item class **carePack** ("Care pack", MPSCALC-142); it totals under Services with service and staging (X-31)"*.
- **No test pins the text** (tarball grep: 1 hit each, the line itself). No API, web or openapi reference to lineage at all (0; control 130).
- **Jira:** MPSCALC-231 read WHOLE (Backlog, `lane-e` `tier-2`, 0 comments).
- **Same-file / lane-E search:** 182 (tier 1), 207, 200, 219, 227. None added (reasons in the kit).
- **Decision store:**
  - the e6f92a5 hosted card is open;
  - 15 MPS cards are ruled and undelivered. 9 are found by id in CLARIFICATIONS and 6 are not (listed in the kit as Tuesday's records item, nothing for the seat).

## The fix
`Item class: service (default K-05, until MPSCALC-142).` -> `Item class: carePack ("Care pack", MPSCALC-142); it totals under Services with service and staging (X-31).` The new text is IMPORTER.md:16's merged sentence. The change also adds one pinning `[Fact]` in `CarePackImportTests.cs`: RED at main, GREEN at head. Tier 2, 2 files.

## Brief or card?
**Brief.** The note is staff-only. It is written into the reference store document and is carried by no route, contract or screen. That answers W2's "UNMEASURED" with: none. No customer-facing wording decision is needed. The sentence is still listed as NEW WORDS (staff-only) for the next words list, the #80 precedent (merged with new words pending the deploy card).

## Corrections to the commission
1. **"Stale since PR #78" is only half right.** #78 ADDED the clause (`PriceBookImporter.cs` +128/-0). It was true when lane E wrote it on 16 Oct, before the class existed (MPSCALC-140 comment 39470, branch `a80c91d`). The Care pack class came in **#76** (02:27:05Z), and #78 (03:43:53Z) moved care packs into it in `PurchaseCatalogue.cs` without updating the note. So it was stale on arrival in main, via #78.
2. **The heavy slots are under the PROJECT ROOT's `.tools/`**, not `2_Project_Files/.tools/` (MPS-LANES ADDENDUM-6). None exists at 06:4x. The worktrees are under `2_Project_Files/.tools/wt-*`.
3. **The READY line form is the lane convention** `READY FOR REVIEW: <branch> @ <sha> (MPSCALC-n, tier t)` (B104 lane brief DO 4), not `READY:`.
4. **The seat must `git fetch origin main`** (e6f92a5 is not local). ADDENDUM-3 allows that for lane seats; only this drafter was barred.

## For Tuesday
- **Merge timing vs words.** The kit lets the branch be READY with the staff-only sentence listed, not approved. If you want the merge to wait for Kam's yes on the next words list, say so at the stamp.
- **Cockpit pane name** `Datasec/MPS-E2` is new; lane E's `MPS-LE` was closed at 05:35.
