# B305 drafter report (Tuesday's read-only drafter, 2026-10-20 ~09:2x AEDT)

Brief written: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-20_B305_SEAT-G5_mps-gate-pr84-tier1.md` (tier 1, round 1 of 2, Opus: launch WITHOUT `BRIEF_SEAT_LEVEL`; pane `Datasec/MPS-G5`, ports 7350-7359, findings B305-n, report `<project>/1_Project_Definition/Briefs/2026-10-20_B305_STATUS.md`).

## What I read
- RELAYED: `B303_STATUS.md` whole (131 lines); B162 STATUS `:340-390` (B162-1..-7, fix shapes); B304 gate brief whole (conventions, verdict vocabulary, last-line shape); B303 builder brief lines 1-12 and 36-44 (REFUSE shape, standing line 11 heavy-slot rule, launch line); B170 gate brief head (MPS gate shape); evidence file `rows-byte-equal-base-vs-head.txt` (24 shapes).
- MEASURED code (`git --no-optional-locks show/diff/grep` at `b371060`): the full `src` + `docs` diff vs `21c2aec`; `SynnexBook.PanelRows`/`SkuShaped`/`HeadingShaped`; `PriceBookImporter.ImportPanelOptions` and the device/option/supply row builders; `ParityProof.Run`/`CheckPanels`; `Cell.Normalise`.
- Not opened: `.local/`, `Source_Documents/`, `4_Credentials`, `3_Access_Keys`, any `.tools/` working file, the real book.

## Measurements (09:1x, read verbs only)
- `ls-remote`: main `21c2aec71e66…`; `refs/heads/b303/lane-e-price-book` and `refs/pull/84/head` both `b371060c4ace…`; `refs/heads/b305*` = 0.
- `gh api pulls/84` (project `.gh-config`): open, draft false, commits 3, changed_files 7, +430/-17, base `21c2aec`.
- Check runs on the head: `CodeQL` completed neutral; `Analyze (actions)`, `(javascript-typescript)`, `(python)` completed success; `dotnet (build Release…; test)`, `web`, `python (demo harness…)`, `Analyze (csharp)` in_progress. CI verdict is therefore conditional by design.
- `git diff --stat`: 7 files as the builder says (3 Import src files, 1 Api test, 2 new Import test files, IMPORTER.md); no Engine/Api product path.
- `lsof 7350-7359`: 0 listeners. `heavy-slot*` in the project `.tools/`: 0. Load1 `4.14` at 09:12.

## Drafter's own reading, written into the brief as traps to attack (not as findings)
1. `Cell.Normalise` splits on all .NET whitespace: NBSP becomes a space, ZWSP survives. The builder's NBSP case therefore reaches `HeadingShaped` as a spaced string.
2. `HeadingShaped` has two failure directions. False Warning: any real heading with a digit, hyphen, slash, colon, apostrophe or accent (rows unaffected). Silent drop: any plain-letters cell of 3+ characters that is not a heading: a prose note, `EOL`/`TBD`, `ABC *` (footnote trims to a no-digit part), a hyphen-free map-held option SKU. The silent class is identical to base. The live Done-when names the hyphenated `OPT-SPD`, which is met.
3. `CheckPanels`: I found no importer-produced store it falsely refuses. `governed` keeps `Cells`, supplies are filtered to the device's own sheet, and `expected` mirrors `ImportPanelOptions`' loop. The real risk is the other side: a device with no option, supply or panel record is unseen, so a store missing all its records still AGREEs (stated in IMPORTER.md). The brief makes the gate try to break this reading with 10 probes, including the builder's dropped fixture (pair held for one of two devices).
4. `PanelSection` gained a 5th positional member: a 4-element deconstruction elsewhere would not compile (build is green per the builder); the gate greps for it.
5. Whether a Warning blocks anything, and which screen shows import Issues, is UNMEASURED; the brief makes the gate read both, since they decide the severity of a false Warning and whether the 11 sentences are staff-only.

## Numbered open questions with recommended answers
1. **Model.** Brief says Opus (routing G1) and omits `BRIEF_SEAT_LEVEL`. Recommended: launch as written; the B297 brief says `brief_seat.sh` pins an Opus id (RELAYED), but I did not read `brief_seat.sh` itself. Tuesday should confirm with one look at it.
2. **Severity of a false Warning on a real heading.** The brief grades a heading from the builder's/B162's list that warns as Major, an invented one as Note. Recommended: keep. Say so if you want a lower bar, since the real book is out of reach.
3. **Silent hyphen-free class.** Graded Minor at most (equals base, outside the live Done-when's example). Recommended: accept; it becomes BACKLOG row (i) from the builder, fix-shape "importer knows the map's option SKUs".
4. **Real-store `prove` and real-heading count.** Left UNMEASURED by design. Recommended: assign a seat allowed into `.local/` before the first hosted import, as the builder's FOR TUESDAY 3 asks; not a precondition for this gate.
5. **Tuesday-side prep before launch.** The brief assumes the three Jira comment ids 39714-39716 and the CLARIFICATIONS C-32/C-33/C-43 as the builder cites them (RELAYED only; I did not GET Jira). The gate re-reads them at source. No action needed.
6. **Slot.** The brief gives the gate the B303 rule with the holder name `B305`. No slot is held by me. Recommended: launch when load1 is stably under 8; Composer B301's CPU hog is the likeliest delay.

## UNMEASURED
Jira ticket state and the three comments; CLARIFICATIONS text; `brief_seat.sh` and the cockpit launch behaviour; `decision_queue` ruling (the brief repeats the builder's relay); which screen shows importer Issues and whether a Warning blocks anything; the real book and store; CI results beyond the 8 states listed above; production behaviour of any probe (I ran none and built nothing).

Files written: the brief and this report only.
