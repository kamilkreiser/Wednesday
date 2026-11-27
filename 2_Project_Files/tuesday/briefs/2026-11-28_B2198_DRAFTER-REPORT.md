STARTABLE: YES (lane L0 has landed: the SharePoint source and test projects exist on `main` `d9f89115`; no shared file is edited; the seat waits only on the heavy slots).

# B2198 DRAFTER REPORT: seat X101, the SharePoint library against fakes, first slice, for Tuesday s337

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-28_B2198_SEAT-X101_oxpd2-sharepoint-library-slice1.md` (271 lines; sidecar `.measured` beside it: `stamp_check.py` printed `183 claims, 183 measured, 0 not measured`, rc 0, last at 03:13:48 AEDT). Seat tools: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s337/d2198/seat-tools/` (8 files). Scratch: `fleet/state/s337/d2198/` (below `<d>`). Clocks by `date`: first `Sat 28 Nov 2026 02:51:50 AEDT`; sidecar written 03:13:31; last check 03:13:48.

## BLUF
1. **A product lane of the X96 form**, 16 owned paths (13 A, 3 M) inside `src/Datasec.Suite.SharePoint/` and `tests/Datasec.Suite.SharePoint.Tests/`: the seat writes 11 source files (C3 to C13) and 2 test files to a full specification; NuGet writes the two lock files; C1 adds ONE project reference (Graph) to L0's project file (frozen bytes in `checks_sp.py`). Cells S01 to S16: 6 Facts + 10 Theories of 40 rows = 46 cases; ten mutants with frozen red cells.
2. **The slice** (commission: "site, drive, folder list, upload to a library folder with its column values"): A8 calls G1 (site search, every page, `$top=500`, `*`), G2 (libraries, first page), G3 (the list behind a library: web address, then display name, else the only list), G4 (editable columns: not read-only, not `_Hidden`, one of five kinds), G5 (folder listing, `$top=20` + A8's `$select`, every page, list-item key from the eTag GUID), G17 (one upload session, conflict `fail`, pieces via `GraphClient.UploadAsync` with no token), G8 (`PATCH .../items/{key}/fields` after every value is checked against the columns). Every call through `GraphClient.SendAsync` / `GetPagesAsync` / `UploadAsync` (public API). No OneDrive reference (D9).
3. **No test-project or shared-file edit needed**: `tests/Datasec.Suite.SharePoint.Tests` EXISTS on main (3 entries); the cells reach Graph types through the SharePoint project's reference, as the landed Entra tests do (their project file names only Entra; `EntraTests.cs` uses `GraphClient` on 3 lines). Of 56 lock files at BASE only the SharePoint test project's lists `datasec.suite.sharepoint`, so no other lock file moves.
4. **PREDICTED:** SharePoint executable `Total: 1` -> `Total: 47`; whole solution 2539 -> 2585; `RULES: clean (762 files)` -> 775; guards 14/15 unchanged (the server does not reference SharePoint).
5. **Q-RUNNER: the counting runner DOES exclude old-lock holders (never three); default ADOPT** (Stamp S8 `89223aca...`), the seat never writes `heavy-slots`. Proof below.

## Q-RUNNER (the commission's one fact)
**Answer: the counting runner B2172 counts a job that holds the OLD single lock; the two schemes together never run three heavy jobs.**
- **From source** (`fleet/state/s335/d2172/heavy.py`, sha256 `89223aca309c11b228f99460c5209167840b45483281eb3c05f7b7e94bca3e5d`, re-hashed): `LOCK = TOOLS + '/wave1-heavy.lock.d'` and `slot_dir(k)` returns `LOCK if k == 1 else '%s.%d' % (LOCK, k)`: slot 1 IS the canonical runner's folder (`31adedc8...`: `LOCK = P + '/.tools/wave1-heavy.lock.d'`). The counting loop reads free slots by `os.path.isdir`, takes the lowest by `os.mkdir` (atomic), and a `FileExistsError` loops back. The canonical runner only ever `mkdir`s slot 1. So total heavy holders <= heavy-slots (2).
- **By run** (`<d>/qr/prove.py`, output `<d>/qr/prove.out`, 02:55:04 to 02:55:44 AEDT; a scratch `HEAVY_LOCK_ROOT` with `heavy-slots` 2, a load file of 1.0, `HEAVY_TEST_GAP=1`, three jobs of `sleep 6`, the canonical runner rebased to the scratch root by the same two-line change as B2172's `today_rebased.py`): case A canonical first then two counting -> **max concurrent 2** (third started +8.7 s, after the first ended +6.1 s); case B two counting first then canonical -> **max 2**; control C, a counting runner whose slot 1 is renamed `.lock.d.1` -> **max 3** (the measure can fail). Printed `RESULT: ... EXCLUDES OLD-LOCK HOLDERS (never 3)`. No project path was touched; every lock lived under `<d>/qr/run-*/tools`.
- **The one way past two:** the light-project bypass (`dotnet test --project tests/<X>.Tests/...` with `<X>.Tests` listed in `heavy-light-projects`) runs a job beside two heavy holders by design. The kit forbids that form and forbids writing either start file.
- **Consequence:** adopting v2 in this kit changes nothing until an OXPd seat writes `heavy-slots` = 2 (absent = the canonical runner exactly, B2172 P6). Q8-b (canonical) is the alternative. Who writes `heavy-slots` and when is yours (B2172 ADOPTION item 2), not this lane's.

## Facts re-measured (instrument; outputs in `<d>/gen/`)
- Origin (`gh api -X GET`, 02:52:33): `main` `d9f89115333bbed2ade723e4c11d523b2a9cd079`, tree `aa53e949...`, parent `cf224e1f`; open PRs 0 (`--jq length`); `matching-refs/heads/b2198` 0; recent PRs 62, 61, 60 closed; branches in gate `b2185/x94...` @ f4aacb5e (16 files vs main) and `b2188/x97...` @ ef1eb24d (12 files; its Server csproj references Core, Adapters.Oxpd2, Secrets, Graph, OneDrive, Sessions, Jobs: NOT SharePoint). No SharePoint path, slnx, `Directory.*` or Graph path in either.
- BASE (tarball of `d9f89115` into `<d>/src`, 762 files; scratch repo `<d>/sim` tree `aa53e949...` = GitHub's). L0's six SharePoint files hashed (kit FACTS 3); slnx lines 25 and 57.
- Main's hosted numbers RELAYED from Tuesday's `fleet/state/s337/maind9f8/hosted.out`: total 2539 both legs, succeeded 2535/2518, skipped 4/21, RULES 762, floor 117, GUARD 14/15, `HOSTED d9f89115...: PASS`.
- `checks_sp.py`: BASE index `CHECKS: 2 of 10 PASS`, all ten controls FIRED, rc 1 (`checks-base.out`); simulated staged prototype `CHECKS: 10 of 10 PASS`, rc 0 (`checks-sim.out`). Prototype = anchors and stubs, NO compiler has read it; its lock files were made by program from OneDrive's (only to exercise check 4).
- `mutants_c3.py --list`: `LIST: 10 mutants, 1 suites, 16 cells` rc 0 (`list-ok.out`); bad row `LIST REFUSED: rows mBad` rc 1 (`list-bad.out`); apply then undo of all ten: 10 `applied`, 10 `equal True`, 0 unstaged changes after (`apply-undo.out`).
- `words.py`: `--control` `CONTROL FIRED: 13 of 13`; commit message + prototype `added.txt` `WORDS: clean (2 files)`; `x64` probe `WORDS: 3 hits` (lock lines kept out, as X96).
- `gitleaks dir` 8.30.1: control (a random `ghp_` token from two halves) rc 1; seat tools rc 0; the synthetic values (prototype fakes + rows) rc 0; control folder moved to `<d>/_quarantine/`.
- Toolchain: `.tools/dotnet/dotnet --version` 10.0.404; gitleaks 8.30.1. Load 6.76 (02:55), 15.55 (03:04); 831 GiB free; no OXPd lock folder, no `heavy-slots`, no `heavy-light-projects`; panes: only `tuesday` named; `.tools/b2198*` absent; X101 in 1 briefs file (the commission), 0 in the project's Briefs (control X96: 20 and 8).
- Five common tools `cmp`-equal to `fleet/state/s336/d2187/seat-tools/` and to `s334/d2159-L5/seat-tools/`; `heavy.py` `cmp`-equal to `s335/d2172/heavy.py`.
- PRIOR-WORK controls at BASE: `git grep -c -F '/lists/'` rc 1 (none); `createUploadSession` 3 lines, all OneDrive (`prior.out`). No file outside the two SharePoint folders names `Datasec.Suite.SharePoint` (git grep -l: 4 hits, all inside them; the slnx is outside `src tests`).
- Spec lines printed by `awk` (`a8-lines.out`): A8 102, 105-109, 153-155, 206-210, 213, 222, 233; 02 100, 200, 203, 543, 743; 03 306; CLARIFICATIONS 98 (C-16), 240 (C-38); B2156 50, 108, 114, 115, 122, 162, 164; plan r2 70, 75, 83, 88; CLAUDE.md 7, 25, 55-56, 82, 83. Source sha256s in `sources.sha256`.

## Chain inputs (DRAFTER_RULES MEASURED LITERALS 4)
| Step | Inputs | Produced by or present at |
|---|---|---|
| 0 | kit, Stamp S2, S3, S4 (Q2, Q8 in words), S8 | Tuesday's stamp |
| 1 | `<src>` 8 files; `<repo>` local values; origin with L0's six files; BASE push run | drafter scratch; `<repo>`; GitHub (exists now) |
| 2 | BASE files; A8, 02, 03 | Step 1 clone; project folders |
| 3 | THE CODE, THE NEW CELLS; `CSPROJ` in `checks_sp.py` | kit; Step 1 tools |
| 4 | pinned tree; C13; `mutants_c3.py`; rows file written in Step 4 before its run | Steps 3, 1, 4 |
| 5 | green tree, mutants undone | Step 4 |
| 6 | staged tree; `checks_sp.py`, `words.py`, message | Steps 5, 1 |
| 7 | commit; origin/main; `run_step.py`, `hosted3.py` | Step 7a; fetch; Step 1 |

## D-decisions (Tuesday's defaults in the kit)
D1 every call through `GraphClient`'s public API. D2 site search every page; `*` as written, a typed query escaped and bounded. D3 libraries, lists, columns: first page only (as the source). D4 folder listing: all pages of 20 up to the page bound; no thumbnails; no path form. D5 list-item key = GUID inside the eTag. D6 every upload through one session, conflict `fail`. D7 column values checked (known, same kind, once, at least one; text <= 255, finite numbers, UTC date). D8 the module's own id rules (site id allows `,` `.`). D9 no OneDrive reference. D10 new cells only.

## Questions for Tuesday (each with its default; the kit's Q1 to Q10)
- **Q1 slice scope:** default **a** the commission's list (upload + column values in slice 1). Source conflict for you: B2156:164 and plan r2:75 put "SharePoint and Teams scan-to-destination calls" on Mon 7 to Tue 8 Dec. Alt b: browse only now.
- **Q2 (STOP-CLASS) list-item addressing:** default **a** the GUID inside the stored item's eTag (A8 row 21 states it for the listing; for the upload path it is UNMEASURED). Alt b: the drive item's list-item relation (not in the source); c: a filtered list-item read.
- Q3 folder listing: default all pages. Alt: one page + continuation.
- Q4 libraries/lists/columns: default first page only. Alt: every page.
- Q5 uploads: default sessions only. Alt: also the simple PUT under 3.5 MB (G16).
- Q6 OneDrive reference: default none. Alt: reference it for its public static rules.
- Q7 gate G1, Opus, READY Step 0 + 330, push + 300, pane `Datasec/OXPd2-X101`, about 90 min of slot waits (about 37 heavy jobs). Alt: G2.
- **Q8 (STOP-CLASS) = Q-RUNNER:** default **a** adopt B2172 (`89223aca...`), never write `heavy-slots`. Alt b: canonical `31adedc8...`.
- Q9 base `main` at the stamp, beside the panes S3 names (all lanes of this commission are disjoint by path). Alt: wait for L1c and L3a to land.
- Q10 query: `*` as written for nothing typed, a typed `*` escaped. Alt: a typed `*` as written.
- **Next slices (for your planning, not drafted):** 2 print path (G14, G15 with the 80/40 MB limits); 3 listing column values (G6 batch, G7) + write-permission read (G9, F93); 4 create/rename/delete (G11-G13) + library search (G10); then G16, G18, recent sites/terms (roaming store, F41), panel pages.

## UNMEASURED (named in the kit's R11 to R13 and Limits)
How Microsoft Graph answers every call: the site search with `*` and an escaped query, the site, drive and list id forms, the eTag form and whether the GUID in it addresses the list item after an upload, the column definition facets (`text`, `number`, `currency`, `boolean`, `dateTime`, `readOnly`, `columnGroup`), the value forms the fields write accepts, the status for a name already taken. Whether `Uri` keeps `*`, `$` and `,` unescaped in the recorded `PathAndQuery` (DERIVED from the OneDrive cells' `?$select=` assertion; the cells measure it). Every total, count and mutant red is PREDICTED (no build, no test).

## Notes for the stamp
- Card ids (report only): C-16 is card `datasec-oxpd-q15-release-one-scope-1118`, C-38 `datasec-oxpd-sensitivity-labels-1120`; the kit cites them without the ids.
- The kit's REFUSE control for S2 counts `tests/Datasec.Suite.SharePoint.Tests` = 3 entries (control OneDrive.Tests = 7), both MEASURED by `gh api -X GET` at main.
- `heavy-slots` absent at drafting: with Q8 a the seat runs exactly as the canonical runner until someone writes it.

## Outside-the-fences disclosure
- Git write verbs (`init`, `add`, `commit`, `clone` of my own scratch repos) ran ONLY under `fleet/state/s337/d2198/` (`sim`, `simstage`, `simbase`), with `-c user.name=drafter -c user.email=drafter@example.test` on the ONE scratch commit of `sim` (a repo with no remote, never pushed; no project identity used).
- One `sed -i ''` edited my own scratch program `<d>/fill.py` (a regex fix); my own scratch outputs that misled the sidecar filler (`gen/claims.out`, the filler's temp folders) were MOVED to `<d>/_quarantine/`, nothing deleted.
- Two commands were REFUSED by hooks before running (an unquoted `=====` separator; an unscoped recursive grep over `fleet/state`); redone in scoped form.
- The harness saved two long tool outputs (plan r2 and B2156 printed with line numbers) under `/Volumes/Datasec_DEV/TUESDAY/4_Credentials/.claude/projects/.../tool-results/`; I read those two files with the Read tool; they held only those briefs' text.
- In the OXPd project: read-only (`ls`, `cat`, `awk`, `sed -n`, `grep`, `shasum` of CLAUDE.md, CLARIFICATIONS.md, A8, 02, 03; a `python3` listing of `.tools/` names and lock owners); `--version` of the project's dotnet (not a dotnet job). `gh api -X GET` under the project GH_CONFIG_DIR only. No `Source_Documents/`, no key folder, no NAS, no `4_Credentials/` beyond GH_CONFIG_DIR, no az, no dotnet build/test/restore, no lock taken in the project, no device, no mail, no Jira, no card store call, no network but `gh api`.
- The Q-RUNNER proof started python runner processes and `sleep` jobs in scratch only; all ended (each printed rc 0; lock roots empty but `heavy-slots` afterwards).
