STARTABLE: YES (after Tuesday's stamp: S2 must name `main` with the six Mailflow files of FACTS 3 unchanged, S4 must answer Q1 "a" in words)

# B2200 DRAFTER REPORT: seat X103, the Mailflow library against fakes, slice 1

Commission: `tuesday/briefs/2026-11-28_B2197-B2201_OXPD-WAVE2-KITS_COMMISSION.md`, section 4. Drafter: read-only, Opus, for Tuesday s337. First `date`: Sat 28 Nov 2026 02:51:54 AEDT; report written after 03:20:59 AEDT (by `date`). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s337/d2200/` (below `<d>`).

Outputs:
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-28_B2200_SEAT-X103_oxpd2-mailflow-slice1.md` (270 lines, sha256 `d5571ca3f44ab42d17f9b9aafaae9b47296160b02030a4b1be75938a1b86888d` at 03:20:59)
- Sidecar: `...SEAT-X103_oxpd2-mailflow-slice1.md.measured` (220 claims, 220 measured; `stamp_check.py <kit>` rc 0, `<d>/gen/stamp_check.out`)
- Seat tools: `<d>/seat-tools/` (eight files; sha256 in the kit's THE TOOLS)

## BLUF
1. **Slice 1 = LIST + READ-HEADER, read only.** `MailReader.ListAsync` reads one page of a folder's messages, newest first. `ListMoreAsync` reads the next page through a `MailCursor`. `ReadAsync` reads one message's header. Every call is a GET through `GraphClient.SendAsync`. Each message is read by explicit rules, or the read fails. No `ToString` or failure message holds user data. 15 cells (55 cases) and nine mutants. The commit changes 10 paths (7 A, 3 M), all inside the two Mailflow folders.
2. **The project file and the two lock files must change.** Lane L0 gave Mailflow no Graph reference (MEASURED: its project file has only `InternalsVisibleTo`). The kit freezes the source project file as OneDrive's with the name changed (MEASURED equal by program), and NuGet rewrites both lock files. This follows the landed precedent of PR 62 (L2 Entra), which changed its own project file and both its lock files (MEASURED by `compare/cf224e1f...d9f89115`: +5, +39/-1, +42). No `slnx` or `Directory.*` line changes. **Only the Mailflow test project references Mailflow** (MEASURED by `git grep` at BASE), so no other project's lock file moves. That is a Step-1 STOP condition and part of the rebase rule.
3. **Q-RUNNER: NO, keep the canonical runner.** Proof is below.
4. **`words.py` misses two shapes:** B-numbers of the 2000s (`B2nnn`: its pattern is `B1` plus three digits, `words.py:17`) and three-digit seat ids (`X103`: its pattern is `X` plus one or two digits, `words.py:20`). This kit's `checks_mf.py` check 11 counts both, with planted controls. **Siblings X100 to X102 and any later kit with a seat id of X100 or more have the same gap.**
5. The scope is the design's own. Every quote is verbatim: `<d>/gen/quotes.out` printed `quotes verbatim: 26 of 26 True`. They cover F35 (02:96), F86 (02:175), C10 (02:371), §5.6.2 (02:540), the scope row (02:741), WP3.6 (03:308), A2:122/124/145-147/395, and CLARIFICATIONS:476 (C-58 item 14).

## Q-RUNNER (the commission's one fact): does the counting runner B2172 exclude a holder of the OLD single lock?
**Answer: not when it is switched on.** The two schemes never hold three heavy slots at once. But with `heavy-slots` = 2, the counting runner runs a second heavy job BESIDE an old-lock holder. It does not exclude it.

Proof from source (`fleet/state/s335/d2172/heavy.py`, sha256 `89223aca...`):
- `slot_dir(1)` is EXACTLY `wave1-heavy.lock.d`, the canonical runner's only lock. A canonical holder therefore occupies slot 1, and the counting runner takes `wave1-heavy.lock.d.2`. Its total stays at `SLOTS` or fewer. The canonical runner itself only ever `mkdir`s slot 1.
- With the `heavy-slots` file absent, `SLOTS` = 1 and the job takes the `TODAY` branch, which is the canonical rule byte for byte.
- Its same-checkout refusal cannot see a canonical holder, because the old `owner.txt` has no `cwd` line. B2172's REPORT line 10 says this too.

Proof by run (`<d>/qrunner/harness.py`, sha256 `d54d42e9...`, output `<d>/gen/qrunner.out`, `Q-RUNNER HARNESS: 6 of 6 as required`):
- All locks were under a SCRATCH root (`HEAVY_LOCK_ROOT`). The canonical runner was a patched COPY whose LOCK line and load read point at the scratch root and a load file.
- The only program run was `/bin/sleep`.
- Nothing was taken under `<project>/.tools`.

Results:
- **T1, slots absent:** a counting job waited behind a canonical holder (peak 1 folder; the counting job's `lock waits 3`).
- **T2, slots = 2:** peak 2 (`wave1-heavy.lock.d` and `.d.2`). The counting job ran BESIDE the canonical holder.
- **T3, slots = 2, two counting jobs holding both slots:** the canonical job waited (peak 2, `t3-canon ... lock waits 1`).
- **CONTROL:** B2172's own mutant (slot 1 renamed `.d.1`) reached peak 3, so the instrument can fail.

The harness's first two versions were wrong, and I corrected them before trusting any result:
- v1 let the canonical copy read the real load (load1 was 8.58, so it never took the lock and T1 passed vacuously).
- v2 ran both counting jobs in one checkout (exit 96 `checkout busy`).

**Default per the commission: NO** (the canonical runner, S8 `31adedc8...`). `<project>/.tools/heavy-slots` is absent (MEASURED). Adopting the runner now would change nothing but the process-group kill at a time-out.

## Facts re-measured (instrument; the kit's FACTS hold the full list)
- **main** = `d9f89115333bbed2ade723e4c11d523b2a9cd079`, tree `aa53e949...`, parent `cf224e1f` (`gh api -X GET`, 02:52:22). The scratch repository `<d>/sim` from its tarball has `HEAD^{tree}` `aa53e949...` and 762 files.
- **BASE's push run:** `hosted3.py` PASS at `--total 2539 --rules 762`, skipped 4/21, guards 14/15. Control `--total 2540`: FAIL 4.
- **Open PRs:** 0 at 02:52. At 03:17:50 there was 1: **PR 63 (L1c, `b2185/x94` @ `f4aacb5e`)**, 17 files under `contracts/oxpd1/` and `tests/Datasec.Suite.Adapters.Oxpd1.Tests/`, none of this lane's.
- **L3a's head `ef1eb24d`:** the server project references Graph and OneDrive, not Mailflow.
- **The six L0 Mailflow files:** sha256 printed. Each folder holds 3 entries (`gh api contents`); the OneDrive control holds 10.
- **Machine:** load `10.17 15.86 13.16` at 03:17:50. 830 GiB free. Lock absent. `<lane>` absent.
- **Panes at 03:17:50:** `tuesday`, **`Datasec/OXPd2-X102`** (the Teams sibling: live) and unnamed panes. At 03:08 they were X99 and N188.
- **Seat id X103** appears only in the commission (an underscore-aware scan; its planted control fired).

## What I ran (STOP-severity checks, on prototype output)
- `checks_mf.py`:
  - over BASE's own index: `CHECKS: 3 of 11 PASS`, all 11 controls FIRED (`<d>/gen/checks-base.out`);
  - over the SIMULATED staged tree: `CHECKS: 11 of 11 PASS` (`<d>/gen/checks-sim.out`). The simulated tree is the prototype's seven files, the frozen project file, and two simulated lock files: the source lock is OneDrive's, and the test lock is OneDrive's with its project entry renamed. NuGet writes the real ones.
- `words.py`: `CONTROL FIRED: 13 of 13`, and `WORDS: clean (2 files)` over `added.txt` and the commit message.
- `mutants_c3.py --list`: `LIST: 9 mutants, 1 suites, 15 cells` rc 0. The bad row gave `LIST REFUSED: rows mBad` rc 1. `apply`/`undo` of all nine over the prototype printed `equal True` 9 times (`<d>/gen/apply-undo.out`).
- **NEVER RUN:** any compile, any cell, any mutant run, NuGet's lock files. Every total is PREDICTED: Mailflow exe `Total: 56`, solution `total: 2594`, `RULES: clean (769 files)`.

## Chain inputs (each step's inputs exist at BASE or come from an earlier step)
| Step | Inputs | From |
|---|---|---|
| 0 | kit, stamp slots S2/S3/S4/S8 | Tuesday's stamp |
| 1 | `<src>` (8 files, exist), `<repo>` local values, origin, BASE push run, L0's six files | scratch; `<repo>`; GitHub; BASE |
| 2 | BASE files; A2, 02, 03 | Step 1 clone; project folders |
| 3 | THE CODE/CELLS; `CSPROJ` in `checks_mf.py`; restored clone | kit; Step 1 |
| 4 | pinned tree; C7; rows file (written in Step 4 before its run) | Steps 3, 4 |
| 5 | green tree, mutants undone | Step 4 |
| 6 | staged tree; `checks_mf.py`, `words.py`, message | Steps 5, 1 |
| 7 | commit; `origin/main`; `run_step.py`, `hosted3.py` | Step 7a; fetch; Step 1 |

## D-decisions (each Tuesday's default as coordinator; the kit's THE DECISIONS)
- **D1:** list + read-header only.
- **D2:** no `$filter`, because whether Graph accepts a filter together with `$orderby` on messages is UNMEASURED. General knowledge says it restricts that combination, and I did not check Microsoft's page.
- **D3:** a cursor, one page per call.
- **D4:** header only; nothing is marked read.
- **D5:** id rule `[A-Za-z0-9=+_-]`, 1 to 512 characters, refused rather than escaped.
- **D6:** next-link rule in `MyDriveBrowser.Followable`'s form, bound to `me/mailFolders/<id>/messages`. It fails closed on another form.
- **D7:** page size 25, at most 50.
- **D8:** new cells only.

Why not the layer's `GetPagesAsync`: it walks every page in one call and returns no next link (`GraphPage` holds the items and a delta link only). It cannot serve "read more".

## Next Mailflow slices (named; none drafted)
- **S2:** the body with a hand-written sanitiser, plus inline images (A2 calls 5 and 7; 03:308 "security review of sanitiser").
- **S3:** the folder list (calls 1 and 2), and the filters and unread counts after a tenant run measures filter-with-order.
- **S4:** compose. This is draft, then attachments through an upload session, then send, with the draft deleted on failure (02:540; calls 12 to 17, 19). It is plan r2's "Mailflow compose" of Mon 7 Dec, and the first slice that would carry a send path: its kit must hold "no mail sent by a test or seat" by fakes only.
- **Later:** mark-read (call 8), search (9), people (10), reply-all (18), attachments for print (6, 20), and the panel pages and the host line.

## Questions for Tuesday (each with its default; the kit's Questions)
- **Q1 (STOP-CLASS): the slice scope.** Default **a**, list + read-header. Alternative b adds the body and sanitiser. Alternative c adds the three filters.
- **Q2: next-link form.** Default: `me/...` only.
- **Q3: id rule.** Default: the narrow set.
- **Q4: page size.** Default: 25 and 50.
- **Q5: the gate.** Default: **G1**, the user's mail under the user's token and the rule deciding where the token goes. G2 is arguable for a read-only, fake-only library. Other defaults: no local CodeQL, Opus, READY at Step 0 + 300 minutes, push by Step 0 + 270, pane `Datasec/OXPd2-X103`.
- **Q6: names.** Default: `.tools/b2200-x103`, `b2200/x103-mailflow-slice1`, `2026-11-28_B2200_X103_*`, owner word `B2200 seat X103`. The commission assigned only B2200 and X103; the rest follows kit X96's form.
- **Q7 (Q-RUNNER).** Default: NO.
- **Q8: BASE.** Default: exactly S2, with the rebase rule before the push. There is no moved-`main` rule at Step 1, because siblings (L1c PR 63, L3a, X100 to X102) may land and only Tuesday's S2 read knows their totals.
- **Extra, for Tuesday's planning:** the X102 pane was live at 03:17. S3 should name it, and any other sibling, as allowed beside this lane. They share only the lock.

## UNMEASURED
- Every Microsoft Graph behaviour the cells script: the page shape, ids, next-link form, whether a well-known name stays in the next link, page size bounds, the order's acceptance.
- The .NET `Uri` forms the cells assume:
  - `UnescapeDataString(PathAndQuery)` of the built address;
  - `AbsoluteUri` round-tripping for M04 and M08;
  - `file:` parsing of the `relative` row on Unix.
- That the analyzers accept the prototype's forms with `TreatWarningsAsErrors`: no compiler has read it.
- NuGet's real lock files.
- The load under four or more concurrent OXPd seats: load1 reached 15.86 at 03:17.

## Outside-the-fences disclosure
- Writes: only `<d>/**` (scratch: the tarball and its extraction, `sim`/`sim-base` scratch repositories with their own local identity `drafter-scratch`/`scratch@example.test`, proto files, tools, harness runs, gen outputs, the mutant keep folders) and the kit, its `.measured` and this report.
- In the project: nothing written. Its local checkout was not touched, and no project lock or `.tools` file was created. The Q-RUNNER harness ran copies of both runners against a scratch lock root.
- Read verbs only toward GitHub (`gh api -X GET` under the project `GH_CONFIG_DIR`). No az, Jira, mail or device. No HTTP but GitHub's API.
- `'<project>/.tools/dotnet/dotnet' --version` was run twice. It is a version print, not a build or test job, as kit X96's drafter did.
- `Source_Documents/`, `4_Credentials/` (beyond `.gh-config`), key folders and the NAS were not opened.
- I did not use `cd` and deleted nothing. One git write in `<d>/sim` was refused by the hook (`git -C $D/sim init` and `stash list`). The variable form was not expanded for the hook; I re-ran with literal scratch paths, and no `stash` was ever executed.
