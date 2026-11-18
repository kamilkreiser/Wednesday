GATE B1710: GO WITH FINDINGS @ 3e2bbab on main 8ae5db6

Head 3e2bbab489bbc415cb26a13ee052b093b4978d47 (branch ls-remote and gh matching-refs equal), one parent 8ae5db6, main re-read at write time still 8ae5db6e (open PR 214 is the sibling b1707, ci.yml only: disjoint). Tier G2.

## Findings
| # | Sev | Finding | Recommendation |
|---|---|---|---|
| F1 | Minor | The word "owed" is true only for devices the proof can see: ParityProof.cs:151-152 says a device with no recorded cell "cannot be seen", so "exactly the owed pairs" is exactly the pairs for the devices the store records cells for. docs/IMPORTER.md:91-93 says so; the note does not. Not false (the earlier sentence glosses the owing), not an overclaim about the proof's own list. | Land as frozen. Optional: list for the product owner with the sentence. No change. |
| F2 | Minor | "counts the section's SKUs per sheet against the store": the per-sheet counts (:203, PanelSheetCount) are reported, and the refusal at :179-186 is the check on SKUs neither imported as a panel nor held by the map. "Counts ... against the store" is a fair short reading, a little less than "refuses a section SKU the store lacks". | Land as frozen; no change. |
| F3 | Minor | Stale neighbour: tests/MpsCalc.Import.Tests/PanelOptionImportTests.cs:12 comment "the parity proof counts them only" (same stale idea; a comment, not a reader). docs/IMPORTER.md:17 "counts them and compares the governed options only" is narrower but true, not contradicting. | One records-pass ticket (comment line :12 plus optionally :17). Not this lane. |
| F4 | Minor | Held stores keep the old note text until their next import (no repository artifact holds it; census below). | Report only, as the kit says. |

No Blocker, no Major.

## Checks (all by program, in my clone /private/tmp/b1710-gate/clone, detached at head)
1. Diff vs base: `numstat` 1/1 on PriceBookImporter.cs, 15/0 on PanelSectionEndTests.cs; paths outside the two: 0 (grep -c -v -x). Source diff -U0: exactly line 150 -1/+1, inside the frozen phrase; test diff exactly the frozen row. Blobs: source 9a9e01dd..., test 8daf8da9... = the kit's predicted blobs. The added test literal equals the frozen replacement.
2. Merge: `git merge-tree --write-tree base head` clean, tree 4cc212a8... equals head's tree (main = base, so nothing else to merge).
3. Words against ParityProof.cs at base, printed: :91-94 governed excludes panel basis, CompareRecords/CompareEngine read only `governed`; no workbook parameter exists in CheckPanels (:115 takes imported and governed), so "does not compare the panel records with the approved workbook" and "does not re-read the book" are true (:112-113, IMPORTER.md:93-95). :175-186, :203: per-sheet SKU counts and the lost-SKU refusal. :190-202: owed from distinct section SKUs x devices less held pairs; `have` is not de-duplicated, `SequenceEqual` fails on a repeated, missing or extra pair, so "each once" is true. Readable to a staff reader: yes, one long sentence, plain words; "owed" glossed by the note's earlier sentence (F1).
4. Build `dotnet build MpsCalc.slnx -c Release` (DOTNET_ROOT .tools/dotnet-10.0.404, version 10.0.404): 0 Warning(s), 0 Error(s). `dotnet test tests/MpsCalc.Import.Tests -c Release --no-build` at head: Passed 198 of 198. Old phrase put back in my clone: build 0 warnings, Failed 1, Passed 197, Total 198; the one failure is the new row, `Assert.Contains() Failure: Sub-string not found`. Restored (git checkout of the file in my clone): blob 9a9e01dd again; rebuild 0/0; 198 passed. Heavy lock slot 1 taken by mkdir and released (holder moved, dir removed); load1 5.5 to 6.6.
5. Census (git grep over head, whole tree): `PANEL-BLOCK` only in PriceBookImporter.cs:150 and PanelSectionEndTests.cs; the old phrase only at :150 at base; `lineage` readers are Import/test files only (none in Api, Engine, web); the only text reader other than the new row is PanelSectionEndTests.cs:176-177 (`any mapped model sheet's`, untouched). No snapshot or store file in the repository holds the text.
6. Scans over the 16 added lines and the commit message: ASCII only; ban list Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite: 0 each, with the `_by_<name>_` control firing for each; no secret/token/password/key/credential words, no ids, no hosts, no B-number; no new RegExp, innerHTML, chmod or child_process. Zero-width characters occur in 3 older test files only (deliberate fixtures), none in added lines. Commit message has the Sonnet attribution once, no B-number or name. Commit `%ae | %ce` is the project's own identity address.
7. Landing texts written (ASCII, no B-numbers, seat ids, card ids or names; authority as asked; says nothing deployed).

## NOT RUN
- `dotnet test MpsCalc.slnx` (Api and Engine tests; no test reads a lineage text, census); load stayed under 24 but optional and skipped. Hosted CI is the proof.
- CodeQL csharp: NOT RUN (cannot extract on arm64); hosted CodeQL is the only C# proof. Hand rows for the CodeQL pre-scan: 0 hits.
- gitleaks, npm, Playwright, package.sh: not run (not needed by the change).

## Landing
SQUASH, head-pinned `--match-head-commit 3e2bbab489bbc415cb26a13ee052b093b4978d47`. Replace `<PR>` and `(#PRNUM)` with the real number (see landing.txt). Re-read main before landing; b1707 (PR 214) may land first and does not overlap. Nothing deploys.

NEW sentence, for the product owner's after-landing list: "They are outside the approved workbook, so the parity proof counts the section's SKUs per sheet against the store and checks that the store holds exactly the owed (device, SKU) pairs, each once, but does not compare the panel records with the approved workbook and does not re-read the book (compatibility basis "...")."
