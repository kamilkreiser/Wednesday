# B162 drafter report · 2026-10-17 ~06:0x AEDT · for Tuesday
Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B162_SEAT-U_mps-gate-147r2.md` (298 lines). It is NOT launched.

## Launch command (form: `brief_seat.sh:4`)
```
bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/MPS-U "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B162_SEAT-U_mps-gate-147r2.md'"
```

## Instruments (read verbs only on the project checkout; write verbs only in my throwaway clone)
- `git --no-optional-locks -C <repo> ls-remote origin` at 2026-10-17 06:00:15 AEDT (165 refs, saved as `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/4fc01a1b-80dc-4d56-906d-73b9eb0776ff/scratchpad/lsremote-b162.txt`). `b104/mpscalc-147-customisation-r2` = `56a4e3bd67ab99a3212b71784a6b7a3a7898d8d3` = the READY line (`B104_STATUS.md:247`). main = `ec29d51a35873e7082e8e56c94cf6c44a4f710bc` (#68), as you said.
- Throwaway `git clone --shared --no-checkout` at `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/4fc01a1b-80dc-4d56-906d-73b9eb0776ff/scratchpad/b162-clone`, push URL `DISABLED` (`remote -v` read back). `merge-tree --write-tree` and one `commit-tree` scratch merge (`02becb96`) there only, never pushed.
- Slots, load and ports at 06:03: slots 1-3 free; load 2.51 4.40 4.61; `lsof -nP -iTCP:6790-6799 -sTCP:LISTEN` rc 1. No `.tools/qa-B162/` exists yet.
- No `gh`, no HTTP, no Jira, no az, no build or test run.

## Merge predictions (a READING; the gate re-measures)
- 147-r2 alone onto `ec29d51`: clean, tree `45920419` (equal to the builder's).
- After 147-r2: `0d525ad` (160), `161def0` (105), `41af1e3` (183), `916add1` (150-r2), `acd44c9` (158-r2) all clean. None shares a file with 147-r2.
- 140 `a80c91d` conflicts with main ALONE (`docs/IMPORTER.md`) and after 147-r2 on 4 files. The builder owns the rebase.
- The round-1 squash trap is gone: `classLabels.test.ts` has 0 removed lines against main. `2ec1f91`'s patch-id equals round 1's 147-alone patch (`3a5b284b`), so round 1 was re-applied unchanged.

## Traps found (each is in the brief)
1. **`prove`'s refusal cannot see an importer mis-read (open (c)).** `prove` reads only `--workbook` and `--store` (`Program.cs:24` @ `56a4e3b`). It checks the store's panel rows against the `panelBlocks` that the SAME importer wrote (`ParityProof.cs:108-150`). A section bounded wrongly is therefore self-consistent and prints AGREE. It guards against a tampered or stale store, not against the section rule. Item 3 is met to the letter of "the sheet's panel heading block" only if that block may be the importer's own record. The gate measures this blind spot and grades it Minor or Note. It is not the B159-1 Major.
2. **Silent ends survive round 2 (open (b)).** A non-SKU-shaped row ends the section with NO issue (`SynnexBook.cs:221-223`). That is right for a heading, but a malformed panel SKU takes the same path: an NBSP, a zero-width space, `(EOL)`, a dagger, a 2-character SKU, or a map-held SKU with no digit (the builder renamed the fixture `OPT-SPD` → `OPT-SPD2` for exactly this reason). Each one drops that row and every panel row below it. Separately, a SKU cell holding a NUMBER is skipped as blank (`NormalisedText` is null for non-text, `Cell.cs:99`), and the section runs on past it. Check 4a has B-h7 for these. Graded as the B159-2 class (Minor).
3. **A SKU-shaped heading with TEXT in its tier cells imports as a text-marker panel, and the next section follows it in** (`:225` plus `Price(…, numericRequired: false)` at `PriceBookImporter.cs:559-561`). No rule on cell text can tell it from a real "Price on Request" panel. The brief has the gate grade it Minor or Note with a reason. The Major line is kept for the book's own heading shapes (words, spaces, `&`, no digit).
4. **A second marker on one sheet:** `FirstOrDefault` (`:206-207`) reads only the first section, and the second marker ends it, so the second section is lost silently. The British spelling "Colour" finds no section at all (pre-existing since round 1). Both are in 4a as REPORT or grade.
5. **A blank-priced panel now ENDS the section** (open (a), the builder's own flag `B104_STATUS.md:214-216`). B159's panelF imported it at round 1. This follows your ADDENDUM-1 item 1 wording ("neither a numeric nor a marker tier cell"). A Warning is raised, so it is not silent. REPORT.
6. **No-panel stores are not byte-equal:** `panelBlocks` defaults to `[]` and is always written (`ReferenceStoreDocument.cs:83`; `ReferenceStore.JsonOptions` has no ignore condition). Expect field-equal plus one key, so B159-6 is closed for the lineage note only.
7. **Rollback reading:** main's `ReferenceStore.JsonOptions` has no `UnmappedMemberHandling.Disallow` (only `CatalogueMap.cs:69` and `ApiJson.cs:20` do), so main should ignore `panelBlocks`. Check 5 measures it.
8. **Four pre-existing test files are edited**, not two: `ImporterTests.cs`, `SyntheticBooks.cs`, `SyntheticWorkbook.cs`, `classLabels.test.ts`. The API tests' `SourceStores.Imported` comes from `SyntheticBooks`, which now holds panel rows on `SYN-A3`. All of this is in Check 8.
9. **The builder's CI ran on `a6813d7`, not on `ec29d51`.** #68 renders `CLASS_LABELS` in `InventoryPicker.tsx:226,255`. My grep found no main test asserting "Option" as a class label, but the gate's `m147` web line is the first real run.
10. Today's hold rules are written in: no `rm` at all, bash only (and `${M}:path` braced, since zsh's `$M:s` modifier ate my own first `git show` today), a 0-test run is never a pass, and every branch name is read from ls-remote.

## Choices you may want to overrule
- The gate may READ B159's evidence folder (`Briefs/2026-10-16_B159_evidence/`) to learn round 1's shapes. It must build its own books (`SYN-B162-*`), and `.tools/qa-B159/` stays closed. B159's evidence has no book generator (`tools/` lists no `B159Gen.cs`), so the gate writes its own.
- No `gh` grant (the branch has no CI or host leg). Network is limited to npm/NuGet.
- s2 is a figure of the gate's own (cumulative rounding that moves a cent between classes), because the builder's test now encodes s1 (261.07) and so s1 alone is no longer independent.

## What I could not verify
- Jira MPSCALC-147's current acceptance text and comment #39509 (no Jira call). The brief quotes B159's copy and has the gate re-read it.
- Any run: no build, test, import or `prove` was executed. Traps 1-7 come from reading the source at `56a4e3b` and `ec29d51`.
- Whether `ReferenceStore` refuses a hand-edited store before `prove` reaches the panel check. The brief gives an in-process fallback.
- Where a `StoredOption` becomes line class `option` (mutant m5): not located. The gate finds it or says it cannot.
- The real books: the builder's counts (80 rows, 50 SKUs, AGREE) are UNMEASURED by rule.
