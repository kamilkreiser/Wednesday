# B560 drafter report (SEAT-M6, MPS lane L3), written 2026-10-24 ~06:55 AEDT

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B560_SEAT-M6_mps-importer-source-version-pins.md` (+ `.pre-stamp`, byte-equal, 8 four-underscore lines: 7 slots and the last line). Read-only drafter; no build, test, mutant or probe run.

## Facts measured
- MEASURED main = `a5b4bbb5d377f29dd63bf0c64d54b44c122a6055` (gh git/ref, 06:45:56). Open PRs: #102 only (head `275349907500...`, 21 paths, listed whole in the brief). Overlap of Yours with the 21: 0 (anchored grep, control QuoteEndpoints.cs = 1). Branches `b560*` on origin: 0; `b44*`: 3 (REFUSE control). `.tools/b560`, `wt-b560-*`: absent; no `heavy-slot-*` dirs exist; panes: tuesday, fleet-monitor, HPSM-POC-G71 only. Port block 8970-8979: lsof empty, not named in any 10-24 brief.
- MEASURED local clone is stale (no `a5b4bbb5`); all source read from a GET tarball of that sha. `dotnet` not on PATH; project-local SDK reports 10.0.401. Local `dotnet` absent means the seat must use `.tools/dotnet/dotnet`.
- MEASURED line anchors at main (each count 1): `SourceDocumentChecks.cs:132` `IsNullOrEmpty(id)`; `ComposedPairs` const (428 triples per ticket/test, RELAYED); `ReferenceDocumentValidator.cs:211` `price >= 0`; `SynnexBook.cs:289` `PanelRows`, `:334` `HeadingShaped`; `PriceBookImporter.cs` `book.PanelRows(layout)` and the Warning code.
- MEASURED -303 still reproduces in code: a heading-shaped (plain letters) cell, including a hyphen-free map code, ends the section with no Warning; merged B206 rows cover only the hyphenated map code. Fix needs `PriceBookImporter.cs` (call site) as well as `SynnexBook.cs`; the lane screen named only SynnexBook.cs.
- MEASURED -200 has moved: "294" and "until the class" read 0 in `docs/IMPORTER.md` at main (control `HP Care Services` = 4, nonsense = 0). The 262 care rows (line 127) vs 371 care SKUs (line 132) and the A4 25/22 (line 115), A3 23/8 (line 116) gaps are the live residue. -219's importer line (line 16) appears already true.
- MEASURED the tickets' Done-when text (318, 319, 320, 303, 200, 219) and 318/319 labelled tier-1, 320 tier-2, 303 tier-1, 200 and 219 tier-2.
- RELAYED B547 gate lines 305-335 (mutant shapes); Api run 12m29s under load (N-f).

## Judgement calls for Tuesday at the stamp
1. Gate tier: lane has three tier-1 tickets; I wrote "drafter reading: tier 1", left to the stamp.
2. `PriceBookImporter.cs` added to Yours (call site) though the lane screen listed SynnexBook.cs only; src/MpsCalc.Import/** is L3's, 0 overlap with #102.
3. -303 ruled as Warning-only (no member/keep-panel), existing Warning code and sentence unchanged; a more precise staff-only sentence is a word pack. Say if you would rather rule the data change.
4. -320 ruled as an independent literal list (python unicodedata 16.0.0) rather than "accept the coverage".
5. -200: the seat may not open real books; a count needing one is "owed" (FOR TUESDAY), not guessed. This may leave -200 partly open.
6. Forbidden set includes lane L2 paths too (conservative); L1 per request.
7. "Just below zero" price: seat picks a synthetic constant in (-0.001, 0); I read "no price value" as "no real-book value", synthetic constants allowed and listed.
8. Compile coupling: new tests use `ReferenceStoreDocument` (a #102 path); landing order is yours.
9. Hard stop 6 h / target 4 h (Api project ~12 min per pass); load1 < 7 per your instruction (earlier briefs used 8).
10. Test names: words only, no ticket key or mutant id (web-brief rule extended to .NET; the repo's own `B520_189_` prefix habit is not to be continued).

## UNMEASURED
Baseline test counts; whether the rows are green at head and die under mutants; `unicodedata` version on the box; whether the synthetic map accepts a hyphen-free digit-free option code and `SYN786` can hold it; the commit that fixed IMPORTER.md:16; whether the A3/A4 gaps are explainable without a real book; Jira changes after ~06:55; CodeQL state of a branch before a PR exists.

## Files written
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B560_SEAT-M6_mps-importer-source-version-pins.md`
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B560_SEAT-M6_mps-importer-source-version-pins.md.pre-stamp`
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B560_DRAFTER-REPORT.md`
