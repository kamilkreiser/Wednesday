STARTABLE: YES (after the stamp; three things for Tuesday to settle AT the stamp are named under BLUF)

# B1810 DRAFTER REPORT: OXPd 2, WP1.3 round 2 of 2, the read assembler's time rule and what follows a refusal

Second drafter on this commission (a re-commission). The first ended with its session at about 21:03 before it wrote a kit. It left NO kit, NO sidecar and NO report; it left scratch under `fleet/state/s301/d1810/` (the copy of the review's files, a Python model `prog/asm_model.py`, a mutant census program, their outputs). Nothing of it was deleted, moved or overwritten except `gate/MANIFEST.sha256`, which its own copy program rewrote with the same 174 lines when I re-ran it. I read its programs whole, re-ran each one I rely on, and continued from them.

Files written: the kit `2026-11-20_B1810_SEAT-X10_oxpd2-wp13-round2-assembler-time-and-refusal.md` (95189 bytes, 307 lines, 8 unfilled slot lines), its sidecar `.measured` (21060 bytes, 104 claims, `stamp_check.py` rc 0: 104 measured, 0 not), this report, and scratch.

## BLUF
1. **The two defaults of the commission, built exactly as worded, do NOT meet their own properties in the model.** A step treated as a discontinuity plus "discard until the end or one quiet window" still gives the tail of a read as a card when ONE call carries a wrong time (290 partial cards in 3000 reads; 15 in 3000 for one Tick a day ahead), because the wrong time itself makes the quiet window look passed. The kit therefore adds D2b (the end is owed until seen; the quiet window counted on the timeline the next call confirms): 0 in the same rows. This is more mechanism than the commission asked for and its evidence is a MODEL's, not a run's. **Tuesday must choose at the stamp (Q3): build D2b, or leave it out and name "one wrong time in the middle of a read" as a limit.**
2. **A third fault the review did not report (D3):** a held event delivered into a read that has already begun does not move the read's start, so one card can hold bytes stamped 1998 ms apart (model row T16). It breaks the time property as the commission words it. In the kit as a red-first cell; DERIVED, the seat must see it red.
3. **The refusal property cannot be met absolutely by any rule.** A read that stops for one whole window and then goes on is given out in part (model: 161 partial cards in 3000 reads when 5% of reads pause 1200 ms, before AND after). Nothing in the report formats marks the start of a read. The kit says so in plain words, makes the comment say exactly that, and lists it with three more limits under Q10. **A reviewer who reads the property literally will find this; the kit's defence is that it is named, with its cell.**
4. **Step 7(b) of the kit points at "the first seat's step program" for the neutral-name scan without a file name.** I did not open the first seat's scratch files and did not find which one it is (the listing shows `checks.py`, `hosted.py`, `extract.py`, `heavy.py`, `clone.py`, `mutant.sh`, no `run_step.py`). Tuesday: name the file at the stamp or the seat will ask.

## What I measured, and how
| What | Instrument | Result |
|---|---|---|
| Earlier output | `ls` of the kit path and the scratch folder, 21:11:54 | no kit, no sidecar, no report; scratch present |
| The origin | `gh api -X GET` under the project `GH_CONFIG_DIR`, 21:27:35 to 21:27:38 | main `7bf37526`, the lane branch `6499bd19`, 6 branches, ahead 1 behind 0, 33 files, 4 check runs success, 1 pull request (closed), 0 tags |
| The review's clone | `git --no-optional-locks rev-parse`, `status --porcelain` | HEAD `6499bd19...`, 0 lines |
| The source | read whole: `CardReadAssembler.cs`, `CardRoutine.cs`, `CardRead.cs`, `CardReadOutcome.cs`, `CardRefusalReason.cs`, `HeldEvent.cs`; the five routines by every code line (comment and brace lines filtered out) | the pointers of the kit, each by `awk NR==n` or `grep -n` |
| The copy of the review's files | the first drafter's `prog/copy_gate.py`, re-run 21:29:14 | 174 files, 674578 bytes, each byte-equal to its source; 0 copied files hold a value of the three pairs (control: fires on the pairs file) |
| The review's mutants | `prog/mutant_census.py` over the head | 52 entries, 52 apply; control (one line changed in a scratch copy): 51 apply, g27 does not |
| The model against the review's log | `prog/asm_model_v2.py control` | 9 sections of `asm.log` compared, 9 equal (A7, A10, A13 by common prefix); a changed token is seen |
| The model's rows | the same program, `cells`, `legacy`, `fuzz`, `soak` (Python, no build, no test; load1 2.7 at the first run) | `model_v2.out`; every number in the kit's tables T, R, I and in D1 to D3 |
| ASCII | `LC_ALL=C grep -c -v -x -E '[ -~]*'` over 27 `.cs` files | 0; control 1 |
| The golden file | `shasum -a 256` | `4cb0c569...`, 1298 lines, 29935 bytes |
| The subject | `wc -c`; `gitleaks dir` run alone | 85 bytes; rc 0 |
| Toolchain, neighbours | by path, 21:27:53 | dotnet 10.0.404, gitleaks 8.30.1, git 2.54.0, python 3.14.10; no `.tools/b1810`; no lock folder; no OXPd2 pane; load 5.86 |
| The reading load | summed by program | 406502 bytes (kit 95189 + 35 files 311313) |
| The sidecar | `stamp_check.py` | rc 0 |

## What in the kit is proven by a run, and what is not
- **Proven by a run of mine:** the origin facts; the pointers; the copy and its counts; that the 52 mutant texts apply at the head; that the model's head variant gives the review's own log tokens; the ASCII and sha256 figures.
- **NOT proven by any run:** every "head" and "after" result of tables T, R and I (a model's; R06, R13b to R13e, I05 and I06 were not even run in the model); that the fix can be built as D1 to D5 describe; that the other 126 tests stay green; the five existing cells said to change; every cell M01 to M09; D6's attribute; anything on a hosted leg. The model covers `keyboard`, `legacy-hp` and `legacy-rfideas` only.

## STOP-severity checks of the kit NOT run on a prototype (each marked NEVER RUN in Step 6)
6(b) the scope program and the `diff --cached --quiet` pair; 6(c) the golden comparison at the seat's head; 6(f) the baseline and the locked restore; 6(g) the scanner over the seat's tree; 6(h) the name scan; 7(b) the scans of the commit; 7(c) the fast-forward proof; the REFUSE check on `permissions.push`; the red-first table of Step 2 (its expectations are a model's; Step 1(e) tells the seat when a difference is a go-on and when a STOP). Run on real output: 6(a) the census, 6(d) the ASCII check, the golden sha256 at the old head.

## The state table (ruling 4)
"Owed" = a refusal that dropped a read was given and no end has been seen since.
| State | A time EARLIER than the last | A window runs out | A bound, the cap or a malformed report | The routine sees an end | One quiet window | `Reset()` |
|---|---|---|---|---|---|---|
| Idle | no result; new reference; to Discarding only if an end is owed | - | one refusal; to Discarding (hp-text: Idle) | result given | - | as new |
| Pending | ONE refusal, all dropped, to Discarding | one refusal, all dropped, to Discarding (Idle if a quiet window already passed) | one refusal, all dropped, to Discarding | result given | - | as new |
| Discarding | no result; stays; quiet window counted anew | - | no result; stays | no result, that event's results thrown away; to Idle or Pending | to Idle, the end stays owed | as new |
The two rules interact in three places, each a cell: a step while discarding (I01), a refusal by the step followed by the tail (I02, I03, I04: one refusal, never two), one wrong time in the middle of a read (I05, I06).

## Questions for Tuesday, each with its default
Q1 time rule: a step is a discontinuity (the difference shape is blind to one wrong time: 325 partial in 3000). Q2 refusal rule: discard to the end or a quiet window, the end event booked. **Q3 D2b: built.** Q4 D3: built. Q5 the time type: `DateTimeOffset` stays (the verdict's choice h says "re-think"; a public change). Q6 the reason at a step: the lane's rule (the commission's default said `Incomplete`; I kept `MissingSequence` when an event is held). Q7 UUID: unchanged. Q8 `CardString`: one attribute and a cell if two lines and no package, else a named limit. Q9 `Reset()` in the middle of a read: named limit. Q10 four limits named. Q11 G1 round 2. Q12 180 and 150 minutes, pane `Datasec/OXPd2-X10`.

## Where the verdict differs from the commission's summary
1. The twelve survivors: the summary lists six kinds; the verdict's twelve also hold g6 (a key twice in one step), g8 (keys after Enter in the same step), g17 (usage 0x27 of the older RF IDeas routine) and g45 (`Reset` forgetting the time, which the review itself calls "a mutant that would be a FIX").
2. TWO comments are untrue, not one: the class comment (`CardReadAssembler.cs:15` and `:16`) and the enum comment (`CardReadOutcome.cs:11`); the verdict also contradicts the first STATUS's FOR TUESDAY item 12b.
3. The verdict's finding 2 names four refusals (the held-events bound, the window, the cap, the byte bound). It does not name the malformed two-byte report; the kit covers it (row R06) because the commission asks.
4. The verdict's fix for finding 1 ends what is pending and re-bases; it does NOT discard after a step. With that fix alone the model gives the tail as a card after a step.
5. The verdict asks to "re-think the time type with the fix" (choice h); the commission is silent: Q5.
6. The mutant file holds 52 entries (the first seat's 7 and the review's 45); g27 has two log rows (a build failure, then the run).
7. FOR-RECORDS names sequence A2 (the cap) among the cells for finding 2; the summary does not.

## Inputs per step (each exists at BASE or is made by an earlier step)
| Step | Inputs | From |
|---|---|---|
| 0 | this kit; CLARIFICATIONS entries C-42, C-45 | exist |
| 1 | the origin; the first seat's `clone.py`, `heavy.py`; toolchain | exist (FACT 8, 10) |
| 2 | the tables of this kit; the copy of `Asm.cs`, `asm.log` | exist (the gate copy) |
| 3 | the cells of Step 2 | Step 2 |
| 4 | the copy of `mutants.py`; `mutant_census.py` | exist |
| 6 | the staged tree | Steps 3 to 5 |
| 7 | the first seat's step program (**file name not given: BLUF 4**) | exists, unnamed |
| 8 | `5_Project_History/history.md` | exists (not opened by me) |

## NOT read
The form kit B1798 lines 183 to 222 (its section THE CONTROLS); the B1798 drafter commission; the first kit B1786 beyond its headings, its line 324 and one grep; the first STATUS beyond its line count, last line and the two `TMPDIR` lines; the kit B1802; `CardLimits.cs`, `ReaderCatalogue.cs` beyond line 4, three small type files; the body of every test; the golden file; the review's `GateModel.cs`, `Port.cs`, `Program.cs`, `Stubs.cs`, `Pairs.cs`; of `Asm.cs` only the lines a grep printed; `soak.log` and `asm.log` cut at 400 and 700 characters per line; the Workpath source, `CardValidator.kt`, any keystore, the pairs folder: never opened.

## Outside the fences, and my slips
1. One Bash call was refused by the workspace hook (an unquoted `=====`); re-sent with quoted separators. Nothing ran.
2. One return code was read after a pipeline (`gitleaks ... | tail`); re-run alone: rc 0.
3. I copied the head's 16 library `.cs` files into scratch (`census_control2/`) for the census control, as the first drafter had. They are the lane's own files, not the Workpath source; they sit in Tuesday's tree.
4. I moved (not deleted) the first sidecar skeleton to `d1810/sidecar-skeleton-1.measured.aside` and made a new one after the kit changed.
5. The form was not read whole (above). The kit follows B1798's shape from the parts I read.
6. A first version of my model variant for "discard after a step only when an end is owed" did not clear the debt at a normal end; I dropped that variant from the kit rather than cite its numbers.
7. I chased the model three times (the wrong-time rows went 290, 50, 0). The mechanism in the kit is where it stopped at 0 with one named residue (two wrong times in one read, 1 in 3000). I did not prove there is no fourth hole.
8. The kit's line pointer for `LegacyHpRoutine.cs` was first a filtered-line number; removed before the sidecar ran.
9. No build, no test, no git write, no Jira or GitHub write, no message. Hosted reads: `gh api -X GET` only.

## Ten lines
1. STARTABLE YES after the stamp; kit 95189 bytes, sidecar 104 of 104, reading load 406502 bytes.
2. Rule C9 (ii) is retracted by name in a section of its own.
3. The commission's two defaults leave tails in the model when one time is wrong; D2b closes it; Q3 is Tuesday's.
4. D3 is a new fault: a late event stretches one card over almost two windows.
5. The refusal property is unreachable for a read that pauses a window; named, with a cell.
6. Cost at the printer is stated: repeat a slow or interrupted tap; deaf at most 999.9999 ms after the last byte, unbounded under chatter.
7. Twelve survivor cells M01 to M09 plus the time cells; g27 and g45 stop applying and get stand-ins.
8. Five existing cells change by the model, one is replaced; the seat measures.
9. Every table row is a model's; nine STOP checks are marked never run.
10. Step 7(b) needs a file name from Tuesday.
