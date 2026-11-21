STARTABLE: NO (only because its precondition is not met: lane E, kit B1849, has not landed; at 21:09 it had not even pushed. The kit is complete, `stamp_check.py` exits 0, and it is written to be stamped against the `main` that holds lane E. Hold the launch until then, which is the commission's default.)

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
