# B565 drafter report (SEAT-M8, MPS lane L2, Sonnet builder, row C2, tier 1 gate after)

Drafted 2026-10-24 about 08:05-08:40 AEDT, read-only. Brief: `2026-10-24_B565_SEAT-M8_mps-readiness-reconciliation-hardening.md` (106 lines; 8 lines carry the four-underscore pattern, 7 slots plus the last line; non-ASCII bytes 0 by `python3 -I`). No `.pre-stamp` copy was written (the task named two files only): Tuesday makes it before stamping if the REFUSE control is wanted.

## Reads
- Templates (whole): B561 brief (123 lines) and its DRAFTER-REPORT; the lanes file `2026-10-24_mps-next-lanes.md` (131 lines, section 4 L2 at :110-115); B560 brief (lines 7-9, 36, 46, 58-64, 98-111), B562 brief (ports, slots, #104 lines), B560 ADDENDUM-1 (head).
- Main read with `git --no-optional-locks ls-remote origin refs/heads/main` in `2_Project_Files` at 08:0x: `a5b4bbb5d377f29dd63bf0c64d54b44c122a6055` (equals the expected sha). The clone already has the object (`cat-file -t` = `commit`); its checked-out HEAD is an older commit, so every file was read as `${REF}:path` (first attempt with `$REF:path` was mangled by zsh; the brief now tells the seat to use braces).
- Jira GET (credentials by name, in-process): MPSCALC-291, -292, -293, -294, -295, each whole (description, 0 comments, Backlog, updated 2026-10-20). Scope and Done-when are quoted in the brief. -247/-248/-249 (host tickets) NOT read: UNMEASURED.
- Code at `a5b4bbb5`: `PurchaseRecomputation.cs` (223 lines, whole), `QuoteReconciler.cs:1-40`, `ReadinessEvaluator.cs:60-111`, `ReadinessPanel.tsx:30-139`, `ReadinessPanel.test.tsx:103-125`, `ReconciliationTests.cs:440-490`, `docs/RECONCILIATION.md` (55 lines, whole), `B324_STATUS.md:482-489`; greps for `at least one device line` (1, evaluator only), `HAS DEVICES` (evaluator plus `ReadinessTests.cs:33,41,141-145,214,226`), `readinessCsv|READINESS_CSV` (panel, its test, `QuoteScreen.readiness.test.tsx` imports the file-name constant only), `QuoteReconciler` over `src` (only the Reconciliation folder, so the Api project does not use it). `git log` over all Yours paths: one commit, `1b32bbe` (#87).
- Fact checks with a control (the brief's REFUSE list): 7 strings counted; all read as the brief says (`ContractSuppliesCost` reads 2, stated); control `zzz-no-such-string-7f3a` reads 0.

## Decisions I made (Tuesday strikes any at the stamp)
1. **-291:** contract-scale compare inside the existing MonthlyCost measure; nine measures stay nine; tolerance stays one cent inclusive. Seat chooses "scale both sides" vs "scale the tolerance" and records it. STOP with one question if any existing pass row goes red (a rounding or tolerance question), or a calculation-register row seems needed (the lanes file's stop rule).
2. **-294:** docs and XML summary only; the optional cross-check defaults to NOT built (a behaviour change on tier-1 verification code; the ticket allows the docs route).
3. **-292:** ADD a reflection row (IL tokens), keep the regex row byte-equal; plants P2/P3/P6 must turn the new row red, P4 must leave it green.
4. **-293:** one expression in `ReadinessPanel.tsx:55`, using the existing word `Passed` (no new header). One existing row (`ReadinessPanel.test.tsx:104-118`, the last data line) is re-expected. **Everything else stays.**
5. **-295 builds nothing.** You said build with the EXISTING sentence and put new words in a WORDS-DRAFT. Taken literally, there is then no code to change: the new Review check also needs a message (a new word) and would re-expect four existing rows (`ReadinessTests.cs:33, 41, 214, 226` pin the id list and order). So the brief makes -295 a WORDS-DRAFT-295 (the ticket's sentence, the check spec, the message left blank for the product owner) plus a measured table, and the READY line says "-295 NOT built". **Tuesday should decide at the stamp whether to keep -295 in the round or drop it; the lanes file's Done-when for L2 ("readiness sentence ... is the ruled one") is not met by this round.**
6. Ports **9120-9129**, pane `Datasec/MPS-M8`, branch `b565/mps-readiness-reconciliation-hardening`, trees `.tools/b565`, `wt-b565-{base,fix,mut}`.

## Port check (how)
- Blocks named in `briefs/2026-10-2[34]_*.md` (Python token scan, 0 hits for `912x`/`913x`; control `9119` reads 7): 8480-8499 reserved; B543/B550/B561 8830-8989; B560 8970-8979; B562 9110-9119. `lsof -nP -iTCP:9100-9199 -sTCP:LISTEN` printed nothing (rc 1); `9120-9129` printed nothing, then a `127.0.0.1:9120` bind control was listed and, after 6 s, freed (rc 1). Unused block: 9120-9129.

## Partition intersection (program `scratchpad/inter.py`, glob-vs-glob, base tree `a5b4bbb5` via `git ls-tree`, plus literal-prefix collision test for new files)
```
B561/L1 Yours (B561 brief line 67): other globs 14, shared base-tree files 0, glob-prefix collisions 0
B560/PR104/L3 Yours (B560 brief line 58): other globs 6, shared base-tree files 0, glob-prefix collisions 0
PR102 21 files (B560 brief line 60): other globs 11, shared base-tree files 0, glob-prefix collisions 0
L2 globs 7 matching base-tree files 13
TOTAL 0
CONTROL (planted ReadinessEvaluator.cs in the other list): shared base-tree files 1, glob-prefix collisions 1, TOTAL 2
```
Intersection = EMPTY. The 13 L2 files: `docs/RECONCILIATION.md`; Readiness `ReadinessCheck.cs`, `ReadinessEvaluator.cs`; Reconciliation `OwnArithmetic.cs`, `PurchaseRecomputation.cs`, `QuoteReconciler.cs`, `ReconciliationTypes.cs`, `RentalRecomputation.cs`; tests `ReadinessTests.cs`, `ReconciliationScenarios.cs`, `ReconciliationTests.cs`; web `ReadinessPanel.tsx`, `ReadinessPanel.test.tsx`. Note: #104's real file list was NOT read (no `gh`); its list is the B560 brief's Yours (7 paths per the B562 brief), so a new file #104 gains outside that list is invisible to this check. The brief makes the seat re-run it live with `gh` at start and before the push. The partition is also written from both sides in the brief (Yours, and an explicit NOT-YOURS list naming B561's Yours, #104's Yours, #102's 21 files).

## UNMEASURED (why)
- No build, test, mutant or probe (drafter rule). Whether the contract-scale cost compare keeps every pass row green (rounding risk) is the main unknown; the brief turns it into a STOP.
- No `gh` call: auth, open PRs, the real #104 file list, the b5* branch list, whether B561's branch is pushed or its seat live. Panes at 08:1x: `%0 tuesday`, `%361 Datasec/MPS-G72`, `%1 fleet-monitor` (no MPS-M7 pane).
- The line of the 2026-10-20 ruling 6 in `CLARIFICATIONS.md` (only `BACKLOG.md:2143` [B340-6b] was found); `models_latest.json` (model id RELAYED from the B561 brief); the host tickets -247/-248/-249.
- The squash-message line you asked me to cite **does not exist in the MPS `CLAUDE.md`** (82 lines; `grep -i squash` reads 0; also 0 in the Datasec and `!CODING` `CLAUDE.md` files). The brief cites what is there (lines 50-52: seats push a branch only, the coordinator merges once CodeQL is green) and the B561 brief's standing line 4 and identity paragraph for the plain-words, no-percent, ASCII message rule, and says so plainly. If a `CLAUDE.md` line was meant, it is not at this commit of the file.
- Heavy slots at 08:0x: `heavy-slot-1` held by `B562 08:06:06 ci-merge-test`; 2 and 3 free (B560's was moved to `_quarantine`). load1 4.17 at 08:05.

## What the reviewer checks first
1. Reading 5: is "-295 builds nothing" what you meant, or should the Review check be built with a placeholder message?
2. The -291 STOP condition and the "scale both sides vs scale the tolerance" freedom; is the effective-tolerance statement in NOTES right (before: one cent times the term at the contract; after: one cent).
3. The IL walker's limits (a compiler-inlined constant leaves no token) and that its mutants must compile.
4. That the three new test files match the lane glob `Reconciliation*.cs` (they do by name) and the web rows stay in `ReadinessPanel.test.tsx`; `readiness.ts` (holds `READINESS_CSV_COLUMNS`) is outside the lane's globs and is read-only in the brief.
5. The squash-line discrepancy above.

## Files written (and nothing else)
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B565_SEAT-M8_mps-readiness-reconciliation-hardening.md`
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B565_DRAFTER-REPORT.md`
(Scratch only under the session scratchpad: Jira reader, intersection script, file extracts. No Artifact/Docs/mail/chat tool, no `decision_queue.sh`, no `cd`, no git write verb, no fetch, no HTTP to a hosted site, Jira GET only.)
