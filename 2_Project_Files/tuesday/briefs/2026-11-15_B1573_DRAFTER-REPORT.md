STARTABLE: YES

# DRAFTER REPORT B1573 (round 2 of the MPS lane M-A pool-determinism fix), drafted 13:48 to 13:55 AEDT 2026-11-15

## BLUF
Kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-15_B1573_SEAT-M139_mps-ma-round2-pool-determinism.md` (83 lines), sidecar `.measured` beside it (60 claims, 60 measured, `stamp_check.py <kit>` rc 0). Seat `SEAT-M139` (the highest earlier `SEAT-M<n>` in the briefs folder is 138, found by program: `ls | grep -o 'SEAT-M[0-9]*' | sort -n | tail`), pane `Datasec/MPS-M139`, work number B1573, port block 9910-9919, model Sonnet. Gate after: G2, ROUND 2 OF 2 (the cap), said in the kit. Stamp slots and `READ-WHOLE-BY-TUESDAY: ____` are left for Tuesday.

## Design of the kit
- Base is the EXISTING branch head `ced69979...`: ONE forward commit, plain fast-forward push, no merge of main (main `ee447909...` is web only; the gate's I4 merge-tree was clean). Re-read at launch; a head that differs, or main touching `src/`, `tests/MpsCalc.Api.Tests/` or `.github/`, is a STOP.
- The kit names PROPERTIES, not a design: P1 a free-thread floor read back and failing loudly (F2), P2 no harness-made stall reaches the 500 ms margin at any pool size (F1), P3 every kill stays, P4 each row prints pool facts. Forbidden to pass: any loosened threshold, fixed sleep, skip, lenient late count.
- **A tension I derived and wrote into the kit (DERIVED, not run):** the kill needs more held waits than free threads (16 steps hold 15 threads under m0), yet 80 to 128 answers fall due at one instant, so merely raising free threads removes the kill. The kit makes the seat resolve it (spread arrival, burst no larger than the floor, another proven design) rather than hand it the obvious fix that would break P3.
- **F2 mechanism (DERIVED):** the group fixture sets the pool minimum to `ProcessorCount + 8` (`OverlayResidueTests.B54.cs:386`), so it is 10 at 2 CPUs and 12 at 4, and `LeaveFree(12)` (`LaneMAParkedPool.cs:32`) parks nothing on a cold small pool; the burst then runs on injected threads (one per about 0.5 s above the minimum). The kit tells the seat to REPRODUCE F1 first (up to 30 runs at 4) and print min, `ThreadCount` and parked, because a design never seen to fail is unproven.
- **Proof matrix:** U unchanged code at the new head, at least 30 runs at 4 and 20 at 2 and unset, 0 red (the commission's floor is 10; the gate's 1-in-9 flake passes 10 clean runs about 31 percent of the time, so I raised it: Q2); M each mutant at each size 3 runs (27 runs; m0 batch also runs the four existing LaneM5 rows, which doubles as the F3 re-measure); W the whole Api project once at 4 and once unset. Load printed before and after every run.
- F3 correction goes in the seat's OWN STATUS as a quoted correction section; the round-1 STATUS file is not edited (not that seat's file; Q1).
- Round 1's "no removed line" check is replaced for the three `LaneMA*.cs` files by "every removed line is inside those three files" (a fix edits them); a new `LaneMA*.cs` helper is allowed only if the property needs it, stated.
- C# CodeQL row: NOT RUN with the x86_64-extractor reason, hand rows done with planted controls (kit FACT 6); the kit says "pre-scan by hand", never "CodeQL".
- Launch line carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes. HEAVY protocol kept (`.tools/.heavy-lock-1` and `-2`, two jobs machine-wide, load1 under 24 on two reads, load printed per run).

## Facts re-measured with instruments (sidecar has each)
- Branch head `git ls-remote origin refs/heads/b1564/mps-lane-ma-source-wait-pins` -> `ced69979a0080816f1e5a911bce1cdbf1fe591b0` (13:49). Main -> `ee447909c2f3cda510e856608cf1aeaa62316d41` (13:49). Control: the same `ls-remote` printed both refs; the clone has no `ee447909` object (`cat-file -t` fatal), so product line pointers were printed from the head, and "same at main" is RELAYED from the gate's web-only finding.
- Pointers printed by `awk NR==n` over `SourceLifecycle.cs`: `:122`, `:602`, `:630`, `:650`, `:665`, `:667`, `:696`, `:705`. **The commission said m2 at `:665`; the line that holds the mutated statement is `:667` (`:665` is the `GiveUpTurn` signature)**; the kit says so (source beats the task text).
- Model row `model-routing.md:92` (C2) and G2 `:109`; model id `models_latest.json:23`; `brief_seat.sh:31` default Opus.
- Ports: `lsof -nP -iTCP:9910-9919 -sTCP:LISTEN | wc -l` -> 0 at 13:49 and again at 13:52; control unfiltered listener count 17 then 14. Word-boundary scan of the non-`.pre-` SEAT kits of 14 and 15 Nov for `991x` -> 0 files; control `980x` over the B1564 kit -> 5. Live panes: no `Datasec/MPS-*`; NexusAI-N129 and N130 are live.
- `.tools` heavy locks: none visible at drafting (`ls | grep -E 'heavy|git-lock'` printed nothing; control: `.tools` lists entries).

## Chain-step input table (rule 4)
| Step | Inputs | Produced by |
|---|---|---|
| 0 | the kit, project root | Tuesday's stamp, exists |
| 1 | branch head, clone, main-tree | origin, Step 0 |
| 2 reproduce | clone build at head | Step 1 |
| 3 predictions | Step 2's printed pool numbers | Step 2 |
| 4 fix | Step 2 and 3 | Step 3 |
| 5 matrix U, M, W | the fix build, main-tree with mutants (copied rows) | Step 4, Step 1 |
| 6 checks and push | matrix tables, one commit | Step 5 |
| 7 STATUS | all of the above | Steps 0 to 6 |

## D-decisions (mine)
- D1: no merge of main (web only, disjoint paths); the squash landing handles it.
- D2: model Sonnet, tier G2 round 2 of 2, same as round 1 (nothing security-shaped).
- D3: READY target Step 0 + 240 min, fix pushed by +210 (the matrix is about 80 batches of about 13 s plus 27 mutant runs of up to 2 min plus two full-suite runs of about 8.5 min plus builds; UNMEASURED as a whole).

## Q-questions for Tuesday (each with a default)
- Q1: Where does the F3 correction live? Default: in the seat's own STATUS (a quoted correction section); the round-1 STATUS file is not touched. Alternative: allow an appended dated line to the round-1 STATUS, which is a write outside the seat's files.
- Q2: Matrix size. Default: 30 runs at 4, 20 at 2, 20 unset (the commission's floor of 10 is in the kit as the minimum it is exceeding). Cut to 10 each only if time forces it, and then say the 31 percent miss chance in the gate.
- Q3: Stamp slots S9 (hard stop) and S5 (launch window) are Tuesday's; default: absolute hard stop 14:30 is TOO EARLY for this kit (about 4 hours of work), so Tuesday should stamp a later hard stop (the drafter does not set it).
- Q4: Is the whole Api project at both settings (W) required? Default: yes, both (round 1's own red appeared only in the full suite); drop the unset run if the time is short.

## UNMEASURED
Whether a staggered-arrival or a raised-minimum design actually clears F1 (the kit leaves the design to the seat and requires the matrix); whether the pool minimum of the fixture is 10 and 12 at 2 and 4 CPUs (DERIVED from the fixture and `DOTNET_PROCESSOR_COUNT` semantics; the seat prints it); how long the matrix takes; the rows on a real 2- or 4-vCPU Linux runner; main's tree at `ee447909` (not fetched; the gate's web-only claim is RELAYED).

## Outside the fences
None. Read: the rules file, the VERDICT, the round-1 kit and STATUS, the three branch files and `OverlayResidueTests.B54.cs` and `SourceLifecycle.cs` and `ci.yml` and `global.json` through the round-1 seat's clone (`.tools/b1564/clone`, read only; the kit forbids the NEW seat from opening another seat's `.tools`, and it works from its own clone), `model-routing.md`, `models_latest.json`, `brief_seat.sh`, the briefs folder listing, `lsof`, `tmux list-panes`, `git ls-remote` and read-only git on the clone. No project write, no ref write, no Jira, no az, no hosted HTTP, no message. One hook refusal during drafting (an unquoted `====` in an echo); no effect. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s277/d1573/` (`fill.py`, the init backup of the sidecar).

DRAFTED B1573: kit 83 lines, sidecar rc 0, questions 4
