STARTABLE: YES (AMENDMENT 1, s307: lane E landed as pull request 13, `main` `f01b907e`; the kit was re-measured there and amended in place, `stamp_check.py` rc 0 with 213 claims measured; the prototype re-ran green but for the 5 tests the kit names. Round 1 first line, kept for the record: "STARTABLE: NO (only because its precondition is not met: lane E ... had not landed)".)

# B1863 drafter report: OXPd 2 tolerant reading (seat X27)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1863_SEAT-X27_oxpd2-tolerant-reading.md` (245 lines, 88699 bytes, sha256 `cab8eeb0...02f6`, ASCII only) with its sidecar `.measured` (175 lines; `stamp_check.py` reports 170 claims, 170 measured, rc 0). Tools: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s306/d1863/gate/` (14 files, hashes in the kit). Scratch, logs and the prototype clone are under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s306/d1863/`. Drafted 21:08 to 21:36 AEDT on 2026-11-21. Opus 5.5, read-only drafter.

## BLUF
- I read the ruling card myself with `decision_queue.sh show datasec-oxpd-firmware-unknown-value-callbacks-1121`. It reads `choice='b'`, ruled 21:07:29. Option b is "Accept unknown values". The kit quotes it with no card id. It writes your addition "an unknown value NEVER counts as success" as Tuesday's, in D6.
- **What is different from earlier OXPd kits:** I built a PROTOTYPE of the defaults in a scratch clone of `main` `977cbeb2` and pushed nothing. It is about 185 added lines in two generator files. I regenerated, built and ran the whole suite through `heavy.py` and the wave lock. Results:
  - 11 generated files changed.
  - The build had 0 warnings.
  - `total: 1170, failed: 4, skipped: 4`. The 4 failures are exactly N3, on the 4 operations whose request holds an enum. The regeneration, read-only and static-field tests all pass.
  - A probe of 26 checks of D1 to D8 passed with 0 failures.
- The seat gets the prototype diff to read, not as frozen text. It still has to write the test cells (K1 to K10) and run the 9 mutants. Neither has been run: both are marked NEVER RUN.
- **Design in one line:** each enum of a service target gets a first member `Unrecognized = 0` and stays strict everywhere else.
  - The runtime's own converter matches exact wire names only. Writing `Unrecognized` or any unnamed value throws.
  - An optional property sent as null reads as absent and does not count toward `minProperties`. Required, array-item and top-level nulls stay refused.
  - A new `TryParse` overload reports a count and schema paths. Values are never kept.
  - The 16 device clients stay strict.

## Facts measured (instrument; control)
- **Origin** (`gh api -X GET`, 21:09:10): `main` is `977cbeb2`, with 0 open pull requests. There is no `b1849` ref (lane E has not pushed) and no `b1863` ref.
- **Lane E's STATUS** (read only) ends `WORKING: Step 2 (project files and stubs)`.
- **`hosted.py` on `977cbeb2`** with 1170/368/4/19/60/60 prints PASS. The control `--skipped-linux 5` prints `FAIL 2`.
- **`census.py`** (control `--plant` fired on both counts):
  - 186 enums: 29 under Targets with 877 members, 157 elsewhere.
  - 46 request enum sites (JobStatistics 42, ScanJob 1, UsbAccessories 2, UserPolicy 1) and 0 answer enum sites across the 8 target answer models.
  - 19 success-shaped members in 12 target enums. In lane E's five operations the only enum is `UsbTransferStatus` (`utsOk`), at 2 required sites.
  - References to the 28 target enum type names outside `Generated/`: 0. The control count inside `Generated/` is 381.
  - `Unknown` appears only as HP's own wire value, in `Device`/`Supplies.BooleanOrUnknown`. That is why the member is named `Unrecognized`.
- **Maps:** all 206 `additionalProperties` in the 37 inputs are `false`, so no map site exists.
- **One-of objects:** 11 target objects have `minProperties` 1 and `maxProperties` 1.
- **`pinned.py`** (control fired, 2 of 2): 15 rows in 8 files.
  - The only rows that change are N3 at `InboundTests.cs:109` and `:114`.
  - `ClientTests.cs:260` (N14, device answers), N4 `:135` and N7 `:209` stay.
  - The other 10 rows are noise.
- **P3 measurement:** the stock `JsonStringEnumConverter`, configured as main configures it, throws on `UTSOK`, `utsok` and `UtsOk`. So the runtime needs its own converter: with the stock one, the tolerant walker would end in `Malformed`. The probe found no case-folding risk.
- **Lane E's work in progress** (read at 21:2x in its clone; RELAYED and may change):
  - `CallbackCellTests.cs:217` "unknown-enum" moves out of P01 under the new rule.
  - `:218` "null-optional" also nulls the REQUIRED `usbTransferStatus`, so it stays refused, now as `MissingRequired`.
  - The kit gives the seat the rule, not these rows.
- **Load:** 202876 bytes (about 50.7K tokens) over 23 files and ranges, plus the kit (88699 bytes). Lane E's two files are not counted: they are not on `main` yet.

## D-decisions (all Tuesday's defaults)
D1 representation; D2 report; D3 nulls; D4 targets only; D5 never written; D6 never success; D7 hostile values; D8 arrays and nesting (no maps); D9 pinned Contracts tests; D10 lane E's P01 rows; D11 regeneration (11-file set); D12 code rules.

## Questions for Tuesday (each with its default; STOP-class means S4 must answer it in words)
- **Q1 (STOP-class):** `Unrecognized` first and 0, with an attribute, no raw text, and the reserved name refused at generation.
- Q2: the six-argument report, with 16 paths.
- Q3: an optional null is absent and not counted toward min/max properties.
- **Q4 (STOP-class):** targets only; the device clients stay strict.
- Q5: the converter refuses to write `Unrecognized` and any unnamed value.
- **Q6 (STOP-class):** `Unrecognized` is 0 and the default. K6a pins its shape, K6b scans for comparisons by exclusion, and the census covers lane E's code.
- Q7: exact ordinal matching.
- Q8: the same rule in arrays and nested objects.
- Q9: N3 is renamed `..._reads_as_unrecognized_...`.
- Q10: lane E's rows are moved by the rule in D10, in lane E's TEST file only.
- Q11: the new cells go in a NEW file, `tests/Datasec.Suite.Contracts.Tests/TolerantReadingTests.cs`. The commission names this project only "where a pinned test changes", so please confirm.
- Q12: obey the landed tests.
- Q13: READY at Step 0 + 240 minutes, push by Step 0 + 180, pane `Datasec/OXPd2-X27`, gate G1 with a second reader on D3, D5 and D6.
- Q14: no ticket.

## NOT DECIDED (for the product owner or Tuesday)
1. Device REST answers: should they also be read tolerantly? The ruling's words name callbacks only.
2. A new member of a one-of result (a new kind of sign-in or registration result) is still refused.
3. Who reads or logs the report.
4. What a printer does with a refused callback is UNMEASURED.

## Chain inputs (each produced earlier or present at BASE)
| Step | Inputs | Produced by |
|---|---|---|
| 1 | the gate folder; BASE holding lane E; `<repo>` config | the drafter; Tuesday's stamp; present |
| 1, baseline regen | `<lane>/regen`, `<clone>` | Step 1 copy; `clone.py` |
| 2 | lane E's P01 file and README (found in Step 1); `TestSupport.cs` | BASE |
| 3 | the tests (Step 2); `prototype-generator.diff` | Step 2; the gate |
| 4 | `pre-mutant/` copies | Step 4's first action |
| 5 to 7 | the green tree (Step 3); `commit-message.txt` | Step 3; the gate |

## STOP-severity checks run on my prototype
| Check | Result |
|---|---|
| `owned.py --control` | PASS (13 rows), CONTROL FIRED 3 of 3 |
| `pinned.py --control` | CONTROL FIRED 2 of 2 |
| `census.py --plant` | both controls fired |
| `words.py` on the commit message | clean; control 13 of 13 |
| Regeneration test | green in the suite run |
| `hosted.py` on base | PASS; control FAIL 2 |

**NEVER RUN, and marked so in the kit:** `owned.py` with test, README and lane E rows; the hosted comparison on a lane head; all K cells and mutants; the gitleaks steps.

## UNMEASURED
- The final shape of lane E's landed code: its P01 rows, its README sentence, whether it reads `UsbTransferStatus`.
- BASE's hosted totals once lane E has landed.
- Whether the generator's reserved-name throw fires: no input has a value that would trigger it. It is a named limit.

## Outside the fences (disclosure)
- I made no git write in any project tree. My scratch clone has the push URL `invalid://no-push`, and its working tree holds my prototype edits, uncommitted.
- I made no Jira or GitHub write and sent no message.
- I made 4 `dotnet` runs, all through `heavy.py` and the wave lock: `regen-proto`, `test-proto`, `probe-proto`, `probe-proto2`. Lock waits were 77, 24, 2 and 1. During one wait the lock was held by a B1865 reader. load1 was 2.4 to 6.8.
- I read lane E's in-progress test file and STATUS tail, read only, to see the P01 rows.
- I deleted nothing. A first sidecar is kept in `_quarantine/sidecar/`.
- I read no `Source_Documents/` and used no `cd`.

## AMENDMENT 1 (s307)
Re-measure of kit B1863 against `main` `f01b907e90a72b69386b0184653e6693bd857348` by a second read-only drafter (Opus 5.5, commission B1883), 2026-11-21 23:43 to 23:58 AEDT (clock reads by `date`: 23:43:19, 23:45:36, 23:46:16, 23:53:25, 23:56:52). Before any edit, kit, sidecar and report were copied with `cp -n` to `.pre-s307-remeasure`, and `cmp` returned rc 0 for all three. Scratch, logs, the clone and the programs are under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s307/d1883/`.

### BLUF
- **STARTABLE: YES.** The one blocker in round 1 is gone: lane E landed as pull request 13, and `main` is `f01b907e`. Nothing the kit stands on moved:
  - The three generator files are byte-equal (same sha256).
  - The diff `977cbeb2..f01b907e` over `contracts/`, `src/Datasec.Suite.Adapters.Oxpd2/Generated/` and `tests/Datasec.Suite.Contracts.Tests/` has 0 rows. Control: the same diff over `src/Datasec.Suite.Adapters.Oxpd2/` has 23 rows.
  - BASE's `Generated/` is a fresh generation.
  - `census.py`'s whole log is byte-equal to round 1's.
  - All 14 tool hashes are equal.
- **The prototype at `f01b907e`, re-run through the round-1 `heavy.py` and the wave lock:**
  - The same diff applied cleanly: 185 insertions, 9 deletions.
  - Regeneration changed the same 11 files. The `Generated/` tree is byte-equal to round 1's.
  - The build had 0 warnings.
  - The suite read `total: 1392, failed: 5, skipped: 4`. The 5 failures are N3 on the 4 operations whose request holds an enum, plus lane E's `P01_every_refusal_of_the_parser_is_kept_and_the_sink_is_not_called`. P01 goes red at row `unknown-enum`, at `CallbackCellTests.cs:245` ("the parser itself accepts the case unknown-enum").
  - The 26-check probe printed `26 PASS, 0 FAIL`, line-equal to round 1's.
  - The K cells and the mutants are still NEVER RUN.
- **Lane E's landed rows:**
  - `:217` `unknown-enum` now reads as a value: `Unrecognized`, report count 1.
  - `:218` `null-optional` stays refused: `MissingRequired` at `$.usbCallback.usbRead.usbTransferStatus`.
  - Both readings come from probe 3, and are confirmed by an instrumented scratch run in which P01 passed once the row was removed.
- **New facts the kit now carries:**
  - **`BadBodies` has a second consumer.** `TextCellTests.cs:95` L01 iterates it and asserts more than 40 texts. With the row moved out, L01 collected 47 (MEASURED), so no edit is needed and the file stays outside the owned paths.
  - **P02 cannot take the moved row.** P02 re-serialises `cb.Request` through `Oxpd2Json.Options`, which throws on `Unrecognized` (D5). The kit now requires a new `P03_` case that reads properties instead.
- **New outside-the-frame section** (H13 to H16): 3 or 4 shapes per tolerant path, each measured by probe 3. A new **Q15** turns them into cell rows.

### What changed in the kit (in place: `scratch/amend.py`, 36 exact replacements, each asserted to occur once, then a temp file and `os.replace`)
| Area | Change |
|---|---|
| Header, title | AMENDMENT 1 note with clocks. Lane E landed (pull request 13, `f01b907e`). |
| Line 7 | Lanes SL and B landed. Lane I is not landed (`b1861/...` at `782b3795`). |
| Line 11 | `CLAUDE.md:7` now carries the Opus word (re-printed). It no longer "names Fable". |
| BLUF 2, 4, 5 | Equal-at-`f01b907e` proofs. The consumer census includes lane E's code. The prototype result at `f01b907e`. |
| READ WHOLE item 6 and load | `CallbackCellTests.cs` lines 196-262, `TextCellTests.cs` lines 26-120 (read only) and the README. New load figure. |
| WHAT CHANGES 6 | The README clause is located at `README.md:60-61` (item 5 of the numbered checks). Keep the words before it, the indent, and the 119-character width. |
| D9 | The `pinned.py` census at `f01b907e`: 16 rows in 9 files. `:217` is attributed to B05, a frame artefact. `:218` is not a row (a frame limit). N3's full class name is `InboundShapeTests`. Prototype totals at `f01b907e`. |
| D10 | The RELAYED work-in-progress reading is replaced by the LANDED rows (MEASURED) and their measured new answers. P02 is ruled out as the home of the moved row. The `BadBodies` and L01 margin is measured at 47 against a floor of 40, with a STOP at 40 or fewer. |
| D11, D12 | The regeneration is re-run and equal. Lane E's N02 is named as a second landed static-field test. |
| REQUIRED SECTION | H1: a tolerated callback ends `Answered` (the handling's outcome, not the value's). New rows H13-H16. |
| FACTS 1, 2, 4, 5, 6 | Each gains its AMENDMENT 1 re-measure. New FACT 8: lane E as landed. |
| PRIOR WORK, Step 1, THE TOOLS, owned row 6, line 160 | The landed state. Hosted numbers for `f01b907e`. Tool controls at `f01b907e`. |
| Q15, S2, S4 | A new Question. S2 records this read of `main`. S4 lists the Q15 default. |

Kit now: 251 lines, 100883 bytes, sha256 `8b4eded10a2e6da39d9d69419a780e65ed4c7c912520a5d76c89a8e671985a1b`, ASCII only. The 8 stamp slots are unfilled.

The sidecar was rebuilt by `scratch/sidecar.py` (87144 bytes; it was 52076):
- 52 lines kept, because their id is unchanged.
- 113 moved, with their old text, the new line number and a note.
- 7 sit on an edited line. Their literal was measured in round 1, and the old text is kept with a note.
- 41 are new literals, each with its own measurement.
- Every carried line also gets its family's AMENDMENT 1 re-measure, after `||`.
- Extra lines: LOAD, FROZEN, PROTO, PROTO2, PROBE3, INSTR, TOOLS, KIT.

`stamp_check.py` result: 213 claims, 213 measured, rc 0.

### Re-measured, with instrument and control
- **Origin** (`gh api -X GET`, 23:43:19):
  - `main` is `f01b907e`. Pull requests 11, 12 and 13 are merged (13 at 2026-11-21T12:37:13Z from `b1849/wp12-oxpd2-adapter` `610bb7d2`).
  - Open pull requests: 0. No ref starts with `b1863`.
  - `.private` is `true`.
- **Fresh scratch clone:** made by `clone.py ... draft`, push URL `invalid://no-push`, `HEAD` `f01b907e`, 0 dirty lines.
- **Generator** (sha256 at `f01b907e`):
  - `Oxpd2Generator.cs` `565890ed...`, `Oxpd2RuntimeText.cs` `cf1fc5f9...`, `Oxpd2Unit.cs` `734dc791...`. All equal, and so are the line counts (447, 1109, 999). The pointers `:442 :587 :669 :58 :834 :870 :947` stand.
- **`census.py`:**
  - The log is byte-equal to round 1's (`diff` rc 0): 186 enums, 29 target (877 members), 46 request sites, 0 answer sites, 19 lexicon members, and 0 references to the 28 target type names outside `Generated/`, lane E included.
  - `--plant`: consumers 1, collisions 3, so both controls fire.
  - Independent check: a case-insensitive `UsbTransferStatus` grep outside `Generated/` hits only the JSON key at `CallbackCellTests.cs:217` and `:218`. The control inside `Models.cs` counts 6.
  - Reserved name: 0 target wire values equal `unrecognized` in any case. The control `utsok` counts 1.
- **`pinned.py`:**
  - Result: `PINNED: 16 rows in 9 files (13 methods)`. `--control` printed `CONTROL FIRED: 2 of 2`.
  - The new row is `CallbackCellTests.cs:217`, attributed to B05 because `BadBodies` returns a `List`.
  - `:218` is missed because its line has no refusal-kind word.
  - The kit now says both.
- **By-program census of the tests that pin the OLD strict answer** (the commission's item 3), three instruments:
  1. Behaviour: the prototype run, in which every pinning test goes red. That is N3 x4 and P01 (rows after `unknown-enum` masked). In the instrumented run with that row removed, P01 passes, so `null-optional` stays a refusal.
  2. Text: `pinned.py` (above); the escaped `":null` count in the lane E test folder (2 hits, both on `:218`); and `utsBogus` (1 line, `:217`).
  3. Consumers: `BadBodies` is used at `:242` (P01) and at `TextCellTests.cs:95` (L01).
  - `S03`'s `Result = null!` answer stays `AnswerInvalid`. The options have `WhenWritingNull` (`Oxpd2Json.cs:83`), so the required `result` is absent. It was green in the run.
  - **No lane E cell other than P01 asserts a refusal that tolerance turns into acceptance.**
- **Lane E's outcome list** (`Oxpd2CallbackOutcome.cs`): 14 members, with `BodyFailed` last. `Answered` is member 0 (lane E's own enum, outside D6). README lines 70-71 list the same 14. This lane changes none of them.
- **Hosted run of `f01b907e`** (`hosted.py` with 1392/443/4/19/60/60): `PASS`. The control `--skipped-linux 5` gives `FAIL 2`. It printed `GUARD: clean (10 files)`, `GUARD: clean (11 files)`, `Ran 60 tests`, `UNIT-TEST FLOOR: ran 60, floor 60`, `RULES: clean (443 files)`, and `NEUTRAL-SCAN: stored objects 1001 ...`. `git ls-files` counts 443.
- **Tools:** the 14 sha256 values diffed against the kit table give rc 0. `owned.py --control` on the prototype tree: `OWNED: PASS (13 rows)`, `CONTROL FIRED: 3 of 3`. `words.py --control`: `CONTROL FIRED: 13 of 13`. `words.py` over `commit-message.txt`: `WORDS: clean (1 files)`.
- **Pointers outside the repo, re-printed:** `models_latest.json:17` `claude-opus-5-5`; `model-routing.md:108` G1; `CLAUDE.md:55-56`, `:61`, `:82`, `:83` unchanged, `:7` changed (the kit now says so); `CLARIFICATIONS.md:292` `## C-45` (the quoted phrase counts 1); `B1830_verify/VERDICT.md:36` F5; `B1837...:101` Q1; `ci.yml` has `filter` 0 times (control: `dotnet test` 2).
- **Toolchain:** `.tools/dotnet/sdk/` holds `10.0.404` only. `gitleaks version` prints `8.30.1`.

### The prototype re-run (each a `heavy.py` job, the wave lock taken by `mkdir` of `.tools/wave1-heavy.lock.d`, lock waits 0 each, load1 1.83 to 6.57)
| Label | rc | What it showed |
|---|---|---|
| `regen-base` | 0 | `REGEN: 85 files, 3763086 bytes`; `git status --porcelain` 0 lines, so BASE is a fresh generation |
| `regen-proto` | 0 | After `git apply` of `gate/prototype-generator.diff`: `REGEN: 85 files, 3778287 bytes`. The same 11 files as D11; `diff -rq` against round 1's `Generated/` gives rc 0 |
| `build-proto` | 0 | `0 Warning(s)`, `0 Error(s)`; 22 assemblies, one for each of the 22 solution projects |
| `test-proto` | 2 | `total: 1392`, `failed: 5`, `skipped: 4`; the failures are N3 x4 (ScanJob, UserPolicy applyUserPolicy, JobStatistics, UsbAccessories operationCallback) and P01 |
| `probe-proto` | 1 | Build error: the gate's `probe.csproj` points at the seat's clone path. Its scratch copy was quarantined, not deleted |
| `probe-proto2` | 0 | `RESULT: 26 PASS, 0 FAIL (build prototype)`, line-equal to round 1's |
| `probe3-proto` | 0 | Probe 3 (`scratch/probe3/Program.cs`, new): the lane E rows and the outside-the-frame shapes |
| `build-instr` / `test-instr` | 0 / 2 | Instrumented scratch copies: `unknown-enum` removed, L01's count asserted equal to -1. Results: L01 `Actual: 47`, P01 passed. Both files were restored by `cp` (sha256 `a484fd12...`, `bc3b727f...` equal; `git status -- tests` 0 lines). The edited copies are in `_quarantine/instrumented/` |

**Predicted numbers in the kit that stay PREDICTED:**
- The seat's local and hosted totals after its cells are added (base 1392 plus its new cases).
- Every K cell's red and green.
- Every mutant.
- The hosted comparison on a lane head.

### Outside the frame (DRAFTER_RULES; probe 3 on the prototype at `f01b907e`, now kit rows H13 to H16)
- **Enum path (walker and converter):**
  - `"utsOk"` reads `UtsOk` with count 0, so walker and converter agree after unescaping.
  - A lone surrogate `"\uD800"` is `Malformed` at `$`, with no exception.
  - An empty string reads `Unrecognized`, count 1.
- **Optional-null path:**
  - A duplicate key whose second value is null is `DuplicateKey` at `$.operationContext`.
  - An optional null inside an array item object (`$.jobDetails[0].aFaxInInfo`) reads as a value, count 0.
  - Two null one-of siblings beside one present member read as a value.
- **Report:**
  - An unlisted value in a body refused elsewhere gives a refusal with count 0 and an empty list, whether the refused property comes before or after it.
- **Converter without the walker:**
  - `JsonSerializer.Deserialize` with `Oxpd2Json.Options` reads `Unrecognized` for a target enum with NO report. `src/` outside `Generated/` calls it 0 times; the control inside `Generated/` counts 1.
  - A client enum throws `JsonException`.
  - A nullable target enum or an array holding `Unrecognized` throws `JsonException` on write.
  - A sink that re-serialises its model would throw, and lane E maps that to `SinkFailed` (`Oxpd2CallbackHandler.cs:195-198`, DERIVED). This is a named limit for the sink's lane.

### New Questions (each with its default)
- **Q15 (new):** each outside-the-frame shape of H13 to H16 becomes a row of the cell its table row names (K3, K4, K5, K7, K9), asserting the answer probe 3 printed. H16 (iv) stays a named limit. Alternative: disclose only.
- **Unchanged and still answered by their defaults:** Q1 to Q14. Q1, Q4 and Q6 stay STOP-class and must be answered in words at S4.
- **Q10's default is narrowed by measurement**, not by choice: the moved row goes into a new `P03_` case, never into P02.
- **Q11 still asks Tuesday to confirm** the new Contracts test file.

### Reading load (new)
- The READ-WHOLE items at `f01b907e` total **232141 bytes over 26 files and ranges** (`scratch/load.py`; the rows are in the sidecar's LOAD line). With the kit (100883 bytes), the load is **333024 bytes (about 83K tokens)**.
- Round 1: 202876 + 88699 bytes. The growth comes from lane E's three ranges (18293 bytes) and from the project's `CLAUDE.md`, `CLARIFICATIONS.md` and runbook, which have grown since 21:2x.

### Still UNMEASURED, or for Tuesday
- **Lane I** (CI guards, fix round) is not landed. If it lands before the seat's Step 1, the floor, the rules count and perhaps the guard lines move. The kit tells the seat to read every number from BASE's own run. The rebase rule does not STOP on `build/**` or `ci.yml` changes; it re-reads the hosted run of the new `main`.
- What a printer does with a tolerated or refused callback is still UNMEASURED (Monday).
- The NOT DECIDED items 1 to 5 of round 1 are unchanged.

### Outside the fences (disclosure)
- **Writes:** only the kit, its sidecar, this report, their three `.pre-s307-remeasure` copies, and files under `fleet/state/s307/d1883/`.
- **Inside my own scratch clone** (no ref was written, nothing committed, push URL `invalid://no-push`): one `git apply` (working tree only) and two scratch test edits, restored by copy and proved.
- **Nothing written in the OXPd_2 project folder** but the shared heavy lock. `heavy.py` took it by `mkdir` and released it by moving it into my lane's `_quarantine/locks/`, exactly as the round-1 tool does.
- **No `cd`, no delete.** One wrong scratch `probe.csproj` was moved to `_quarantine/`.
- **GitHub:** `gh api -X GET` only, under the project `GH_CONFIG_DIR`.
- **No git write in any project tree**, no Jira, no message, no push or PR.
- **The ruling card** was read with `decision_queue.sh show <exact id>` into `scratch/card.txt`, inclusion-checked on the id (count 1). The kit holds no card id (count 0).
- **Not read:** `Source_Documents/`, other projects.
- **I read lane E's landed code and tests**, read only.
