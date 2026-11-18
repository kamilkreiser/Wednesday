GATE B1697: GO WITH FINDINGS @ 7e4845b on main b746cb9

Tier G2, MPS Commercial Calculator, branch b1671/mps-lane-mi-panel-block-note. Own clone /private/tmp/b1697-gate/clone (push URL invalid, nothing pushed). Toolchain dotnet 10.0.404 from the project .tools; heavy slot 1 taken by mkdir, holder file moved, own dir removed.

## Findings
| # | Sev | Finding | Recommendation |
|---|---|---|---|
| F1 | Minor | Main moved after the READY: 863e0337 -> b746cb92 by #211 (docs/API.md, tests/MpsCalc.Api.Tests/QuoteApiTests.V0Home.cs). Neither is one of the lane's two paths. merge-tree origin/main + head: clean, tree 6fe65b3d; differs from main in exactly the two lane paths; those blobs equal the head blobs (b28b2b9a, 3ed8d982); the two #211 blobs equal main's. Squash onto b746cb9 is clean. | Land the squash as head-pinned; the base differs from the kit's S2 only by #211. |
| F2 | Minor | Wording reads slightly oddly ("every row of any mapped model sheet's section") but it is the ticket's acceptance phrase and the words of docs/IMPORTER.md:17, which the owner's ruling covers. | None. |
| F3 | Info | Parity sentence at the end of the note ("does not compare them") is untouched (the diff is one phrase). It is still incomplete since the later proof work; a separate words ticket is warranted (Tuesday records it; nothing filed). | Records pass. |
| F4 | Info | CodeQL csharp NOT RUN (cannot extract on arm64); hand rows over added lines are clean (no RegExp, innerHTML, Process, secret-named values). Hosted CodeQL is the only C# proof. | Watch hosted CodeQL on the PR. |

No Blocker, no Major.

## Checks by rule
1. Diff = frozen patch: numstat source 1/1, test 11/0; python: old phrase count 1 -> 0, new phrase 0 -> 1, base.replace(old, new) == head byte for byte; blobs b28b2b9a (source) and 3ed8d982 (test) equal the kit's predictions. Two paths of 2 allowed (lane OWNS). Open PRs overlapping: #211 only, disjoint (and now merged). Remote ref (gh matching-refs) = 7e4845b2...; one commit, one parent (863e0337); author and committer = the repo's Datasec address.
2. Truth to code: ImportPanelOptions (PriceBookImporter.cs:651-) loops over map.Devices grouped by ModelSheet, i.e. every MAPPED model sheet, and for each calls SynnexBook.PanelRows (SynnexBook.cs, marker 'Optional Color Panel Accessories'); sheets with no layout or no section are skipped, sheets the map does not name are never read. The note is added only when panelBlocks.Count > 0 (line 147). "any mapped model sheet's ... section" is accurate and does not overclaim. docs/IMPORTER.md:17 says "each row of any mapped model sheet's `Optional Color Panel Accessories` section": same words.
3. Test: Import tests at head 197 passed, 0 failed (build 0 warnings, 0 errors). Mutant in my clone only (old phrase back): 1 failed of 197, exactly PanelSectionEndTests.The_panel_block_note_says_any_mapped_model_sheet, "Assert.Contains() Failure: Sub-string not found". Restored: blob b28b2b9a again, 197 passed. The row is not vacuous (it reads the real Run() store text, Ordinal).
4. Census at head by git grep: old text "every row of a model sheet" 0 in every tracked file; new phrase in 3 files (docs/IMPORTER.md:17, the importer :150, the new test); the note's other text ("section is an option of each mapped device") only in the importer; "PANEL-BLOCK" read by Code only in PanelSectionEndTests (:164, :166, :176); no 'lineage' reader in src/Api, Engine, web or tools; tracked .xlsx/.xlsm/.zip/.pdf 0, tracked .json 23, none hold the text. 0 readers of the text.
5. Whole solution (load1 9.28 at 09:06 and 8.30 at 09:09, 3 min apart; not independent): build 0 warnings 0 errors; Engine 743, Import 197, Api 3663 passed, 0 failed (Api took 8m14s).
6. Parity sentence untouched (see F3).
7. Scans over the 12 added lines and the commit message: names (underscore-aware, with planted control firing), B-numbers, secrets/tenant/host patterns, non-ASCII and Cf characters: 0 hits. git diff --check rc 0. Commit message carries one Co-Authored-By line (Claude Sonnet 5.5), no names, no B-numbers, no card ids.
Authority: decision_queue.sh show: card mps-410-openapi-195-wording-1117 status ruled, choice a, ruled 2026-11-18T08:38:02+11:00, detail "Yes to all three: contract changes with the docs; 195 recorded as agreed; 207's three words added with a test". The shipped change is exactly the "207's three words added with a test" part and nothing more (words = the three added words "any mapped"; one test row; no docs, no contract, no parity edit).

## Builder STATUS claims (read via the commission's summary; the 104-line file itself was not opened)
Import base 196 / RED 1 of 197 with "Sub-string not found" / GREEN 197 / mutant red then green blob: true (reproduced). Both head blobs equal predictions: true. Census 0 readers in code: true. Whole-solution not run by builder: now run by the gate, green.

## NOT RUN
- CodeQL csharp (cannot extract on arm64; hosted CodeQL is the proof). Web/npm/Playwright, scripts/package.sh: not in scope, no changed file read by them.
- gitleaks not run (no secrets pattern in the 12 added lines by hand scan).
- Builder STATUS file not read line by line.
