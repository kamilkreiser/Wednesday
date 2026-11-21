STARTABLE: YES, once Tuesday answers the four STOP-class questions in words at Stamp S4 (Q24 the four ids, Q25 the versions, Q26 the fetch, Q20 the rebase) and re-prints the ruling at S8. The kit is mode FULL only, and its new Step 3F makes THE ONE FETCH. Two things no instrument of mine could settle before the seat runs: whether EF Core 10.0.15 and Npgsql provider 10.0.4 are on nuget.org (I fetched nothing; GitHub releases exist for both), and how a real NuGet restore behaves under `fetch.py` (rehearse and fetch are NEVER RUN). `stamp_check.py` exits 0: 269 claims, 269 sidecar lines.

# B1856 drafter report | lane B, seat X15, kit B1833 re-drafted to mode FULL with one supervised package fetch

Drafted 2026-11-21, 19:08 to about 19:30 AEDT. Clocks are from `date`: 19:08:19, 19:08:47, 19:10:39, 19:11:13, 19:19:36, 19:29:51. Drafter: Opus, read-only. I fetched no package and ran no restore, build or test.

## Files
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1856_SEAT-X15_oxpd2-wp11-registry-and-state-database-full.md`.
  - 136,563 bytes, 503 lines, sha256 begins `a522b0c6`.
  - 9 unfilled slot lines (S1 to S8, plus READ-WHOLE). 0 non-ASCII lines.
- Sidecar: the same path + `.measured`. 275 lines: 269 claim lines, plus `PTR`, `FROZEN`, `TOOLS`, `LOAD` and `KIT`.
- Tools for the seat: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s305/d1856/gate/`, 11 files. Their sha256 are in the kit and in the sidecar line `TOOLS`.
  - Seven are B1833's, unchanged: `clone.py`, `heavy.py`, `words.py`, `run_step.py`, `place.py`, `placeprops.py`, `cachecheck.py`.
  - `hosted.py` is B1835's (`--unit`, `--floor`).
  - New: `fetch.py`, `fetchrecord.py`.
  - `commit-message.txt` is B1833's FULL message, byte for byte.
- Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s305/d1856/scratch/`. It holds main's tarball, the GitHub reads under `gh/`, the placement copies, the prototype records under `proto/`, the fake lane, `fill.py`, `sidecar.py`, `ptrcheck.py` and `quarantine/`.

## BLUF
1. **The fetch is designed as D25, run by `fetch.py`.**
   - It runs in three modes, in order:
     - `dry`: the checks only.
     - `rehearse`: the same command, network CLOSED. It must fail with package-source codes only and leave the cache unchanged.
     - `fetch`: once.
   - The command is fixed inside the program: `dotnet restore <lane>/scratch/fetch/fetch.slnx --configfile <clone>/NuGet.config -p:NuGetAudit=false -v n`.
   - `fetch.slnx` (frozen block T6) lists the four lane projects plus the scratch scaffold (T5). One command therefore writes every lock file, Design included.
   - The program refuses unless `NuGet.config` is byte for byte main's (one source, nuget.org) and the props lines match the pinned versions.
   - `<lane>/fetch/ONCE` is created with `O_EXCL` once the lock is held. Any later fetch is refused, also after a failed first one.
   - The proxy variables are removed for that one job only. `NUGET_CERT_REVOCATION_MODE=offline` is set and stdin is closed.
   - Afterwards the program checks the log's request hosts (anything but `api.nuget.org` is a STOP) and credential words (any is a STOP).
   - After the fetch, every job goes back through `heavy.py` (unchanged). `fetch.py --list` must print the same sha before and after every later restore, the locked one included.
2. **The record (D27) is written by `fetchrecord.py`** into `<project>/1_Project_Definition/Briefs/2026-11-21_B1856_FETCH-RECORD.md`.
   - **A measured correction to the commission:** the lock file's `contentHash` and the cache's `.nupkg.sha512` are DIFFERENT hashes.
     - Measured on `xunit.v3` 4.0.3 in the project cache: the lock `contentHash` (`GxBopTuV...`) equals `.nupkg.metadata`'s.
     - The `.nupkg.sha512` file (`cpENjBNI...`) equals `shasum -a 512` of the `.nupkg` itself.
     - So the record keeps two pairs: (A) the content hash, lock file against metadata; (B) the file hash, `.nupkg.sha512` against the program's own SHA-512.
     - (B) is the value G1 should compare with nuget.org's published package hash.
   - A new package that no chain of lock-file dependencies reaches from the four is a STOP row. So is a differing pair, or a source other than nuget.org.
3. **Default versions (D26, Q25): EF Core `10.0.15`, Npgsql provider `10.0.4`.**
   - EF 10.0.15 matches the project's runtime, 10.0.15.
   - The project cache already holds every `Microsoft.Extensions.*` id at 10.0.15.
   - EF 10.0.12's nuspec depends on Extensions at its own patch number (10.0.12). So 10.0.12 would add a second patch line of the Extensions packages.
   - Npgsql provider `10.0.4` is the only 10.x whose source pins EF 10.0.15. Its tag's `Directory.Packages.props` names EF 10.0.15, Extensions 10.0.15 and Npgsql 10.0.4, and its `NuGet.config` names nuget.org only.
   - Release dates: dotnet/efcore `v10.0.15` was published 2026-11-10; npgsql/efcore.pg `v10.0.4` on 2026-11-20 (one day before drafting).
   - Whether either is on nuget.org is UNMEASURED. A `NU1102` is a STOP, never a retry.
4. **Re-measured against main `61b17ec0`** (unchanged at 19:29:51):
   - 293 files. `Datasec.Suite.slnx` and `Directory.Packages.props` are unchanged since `5e36d8dc`.
   - `ci.yml` has a new sha (`3e764a37`). `FLOOR=60` at line 192 (4 + 23 + 33). The line pointers 7/40/42/45/46/48/70/72/75/76/78/120 are unchanged.
   - Hosted run (`hosted.py` d1835, 19:11): `--total 899 --rules 293 --skipped-linux 4 --skipped-windows 19 --unit 60 --floor 60` printed PASS. The control without `--unit`/`--floor` printed FAIL 2.
   - Design shas are unchanged, and the pointer check found 28 of 28 (control 0).
   - CLAUDE.md, CLARIFICATIONS.md and SETUP_RUNBOOK.md are the same byte counts as B1833 read.
5. **Kept from B1833's FULL mode:** D1 to D24 (D2 and D5 rewritten), C01 to C26, T1 to T4 (the shas match B1833's), the rebase recipe and the HEAVY rules.
   - **Removed:** DEVICES-ONLY, D25 the mode, and S8 the mode. S8 is now Tuesday's re-print of the ruling.
   - **The rebase recipe now follows B1841's form:** only `Datasec.Suite.slnx` conflicts are resolved by program. A props conflict is a STOP, since the file is this lane's alone.

## What I measured and how (instrument in brackets)
- **Card** [`decision_queue.sh show datasec-oxpd-lane-b-database-packages-1121`, 19:08]: ruled, choice `a`, label "Fetch them once", `ruled_ts` 2026-11-21T19:03:56. It is pasted whole into the kit's THE AUTHORITY, without the id line. The kit's card-id count is 0; a planted id counts 1.
- **Origin** [`gh api -X GET`, project `GH_CONFIG_DIR`, auth rc 0, 19:08:19]:
  - main `61b17ec0`; private true, push true.
  - 12 heads, with lane D at `e9095598`, lane A at `f2b237d0` and lane SL at `a5ba020b`. PRs 1 to 8 are merged; 0 open.
  - No `b1856` and no `b1833` ref.
  - Contents API: 404 for all four lane folders (control: Secrets answers with 21 entries).
  - `compare` for lanes D, A and SL: props 0 and lane paths 0 each; slnx 1, 1 and 0.
- **Main's files** [tarball by GET; `cat -n`, `wc`, `shasum`]: slnx, both props files, `NuGet.config` (7 lines, 217 bytes, sha `f545a7e2`), `global.json`, `ci.yml`, `.editorconfig` lines 18 and 19, the Server csproj, `SecretNames.cs:7-8`, and the `def test_` counts.
- **Placement** [`place.py full`, `placeprops.py 10.0.15 10.0.4`, on scratch copies]:
  - slnx: 19 -> 23 lines (sha `a0bc6ff4`). On lane D's and lane A's files the lines go at 6/7/18/19.
  - props: 11 -> 14 lines (sha `f15ddd42`).
  - Each program refuses its own output (rc 2).
- **Cache** [`cachecheck.py`; `fetch.py --list`; `ls`; nuspec reads]:
  - Project cache: `CACHE: 0 of 4 present` (64 ids, 95 id/version folders, list sha `b600d36a156192e0`). Control: xunit.v3 4.0.3 present.
  - Global cache: EF ids at 10.0.12, SqlClient 6.1.6, no Npgsql.
  - Design 10.0.12's dependencies include `Humanizer.Core`, `Mono.TextTemplating`, `Newtonsoft.Json`, `Microsoft.Build.Framework` and `Microsoft.CodeAnalysis.*`. All are covered as dependencies of the four.
- **GitHub version evidence** [`gh api -X GET` on dotnet/efcore, npgsql/efcore.pg and npgsql/npgsql: tags, releases, and files at tags]:
  - **Caveat:** efcore's `eng/Versions.props` VersionPrefix lags its tag by one from v10.0.14 on (v10.0.15 reads 10.0.14). So the published EF 10.0.15 nuspec's own dependency versions are UNMEASURED.
- **`fetch.py` on a scratch lane** (never the project's lane, no lock taken, no dotnet run):
  - `dry` passed.
  - Each of these was refused with rc 2: props at another version; a changed `NuGet.config`; `fetch` with no rehearsal; `fetch` with a planted `ONCE`. The planted-`ONCE` refusal came before the lock, with `logs/` empty.
  - The host and credential regexes were tested on a synthetic log only.
- **`fetchrecord.py`** on this project's real cache, with main's Core.Tests lock file and `xunit.v3` as a stand-in root:
  - PASS: `new 13 | reachable 13 | ... | STOP 0`.
  - Planted `serilog/4.2.0`: STOP 1.
  - The ruling's own roots: STOP 17.
  - An existing record: refused.
  - The record passed gitleaks (rc 0). Its words copy passed `words.py` (clean).
  - **Why a words copy:** my first record, scanned whole, printed 2 hits, both from my own absolute scratch path. A base64 hash can also spell a seat id by chance, so `--words-copy` blanks the hash cells and gitleaks reads the record whole.
- **gitleaks** 8.30.1 over the commit message: rc 0. **words.py**: commit message clean; control 13 of 13.
- **Kit scans:**
  - Underscore-aware ban-name scan: 0 hits. Control `x_by_Kreiser_y` fired.
  - Non-ASCII lines: 0. Unfilled slots: 9 (the control `STAMPED` counts 2).
- **Machine** (19:10:39):
  - Load 2.18/3.86/4.38. 1002 GiB free.
  - The lock was HELD by `B1853 second reader`, owner line 19:07:57.
  - Panes: X14 and X23 live, no X15.
  - `.tools`: no `b1856`, no `b1833`. `.tools/dotnet/sdk` holds 10.0.404 only.
  - No `Directory.Build.props`, `Directory.Packages.props`, `NuGet.config` or `global.json` in `.tools`, `<project>` or any folder above them (so the scratch scaffold is not reached by any of them).

## D-decisions (new or changed; the rest are B1833's)
- D2 CHANGED: the packages are fetched once into the project cache, then every restore is closed.
- D5 CHANGED: the Tools-package alternative is now outside the ruling.
- D24: the rebase rule, now STOP-class (Q20).
- D25 NEW: the one fetch.
- D26 NEW: the versions.
- D27 NEW: the record, with two hash pairs.

## CHAIN INPUTS (printed in the kit as a table)
- Steps 0 to 2: unchanged from B1833.
- Step 3 before 3F: produces the placed props, the four csproj files, `Scaffold.csproj` (from T5 with `@EF@` replaced) and `fetch.slnx` (from T6).
- Step 3F needs those, plus `<lane>/lists/` from Step 1.
- Step 3 after 3F: needs the filled cache and 3F's lock files.
- Step 4: needs the Design package in the cache, from 3F.
- Step 5: needs 3F's cache listing.
- Step 7: needs the base's unit and floor counts from Step 1's `hosted.py`.

## Questions for Tuesday (each with its default; STOP-class marked; S4 answers in words)
- **Q24, the four ids (STOP-CLASS).** Default: SqlServer, Sqlite, Design and the Npgsql provider. These are B1833's cache-check four, which the card cites.
  - **A conflict for Tuesday to rule:** the commission lists "SQLite" as NOT covered. The kit reads that as any SQLite package other than EF's own provider.
  - If Tuesday meant the EF SQLite provider too, the lane as written cannot be built: it would have no test provider. That needs a new kit.
- **Q25, versions (STOP-CLASS).** Default EF 10.0.15 and Npgsql provider 10.0.4.
  - Alternative A: EF 10.0.12.
  - Alternative B: Npgsql provider 10.0.3 (released 2026-09-14). Pick this if a package published one day before drafting is a supply-chain concern.
- **Q26, the fetch (STOP-CLASS).** Default: `fetch.py` dry, then rehearse, then fetch, run by the SEAT. The card's detail says "Tuesday runs one supervised restore"; the kit reads that as Tuesday's program under Tuesday's stamp.
  - Alternative C: Tuesday runs it himself before launch. That is a different kit, because the projects must exist first.
  - Audit is off during the fetch.
  - Revocation mode is offline.
- **Q20, rebase (STOP-CLASS).** Default: rebase the unpushed commit before the first push; only slnx conflicts are resolved, by `place.py`; never after the push.
- Q27: two hash pairs.
- Q1 to Q19, Q21 to Q23: as B1833, except:
  - Q2 and Q5 are changed.
  - Q3's InMemory alternative is now a fifth package.
  - Q21 windows: 300/240 minutes, with the fetch inside.
  - Q22: a new pane `Datasec/OXPd2-X15`.
  - Q23: G1, with the record as an input.

## UNMEASURED and NEVER RUN (each marked in the kit)
- Whether the four exist on nuget.org at the pinned versions.
- `fetch.py` modes `rehearse` and `fetch`:
  - the codes a closed restore prints (the program accepts only NU1100, NU1101, NU1102, NU1301 and NU1801);
  - whether `-v n` prints request lines in the `GET`/`OK` form the host scan reads (if not, it prints "blind" and the record's source column becomes the instrument);
  - whether the log holds an innocent credential word (that would be a false STOP);
  - whether `--configfile` alone governs the sources (DERIVED from docs);
  - whether a `.slnx` may list projects outside its folder (the rehearsal proves it, closed);
  - whether `NUGET_CERT_REVOCATION_MODE=offline` and signature checks touch any other host.
- `fetchrecord.py` over real lock files of these projects (RID sections, project entries).
- `IncludeAssets="all"` on the Design package.
- Every build, test and scaffold outcome. EF API names, `EF1001`, C19 to C21, line ends on Windows.
- The hosted audit and locked-mode hash check of the new packages.
- `hosted.py` on a head of this lane, and the push.

## Reading load (summed by program)
- Beside the kit: 95,764 bytes.
  - CLAUDE.md 10,052.
  - CLARIFICATIONS 33,300.
  - Runbook 23,227.
  - Item-6 files at `61b17ec0`: 15,060.
  - Ten tool docstrings: 14,125 (`ast.get_docstring`).
- The kit: 136,563.
- **Total: about 232 kB, more than double the ~100 kB guide and larger than B1833's 201,511.**
- What drives it: the project's mandatory reads, the long tool headers of the two new programs, and the fetch design text.
- I did not cut a shorter version.

## Corrections to the commission
1. **The lock-file contentHash and the seat's `.nupkg.sha512` are not one value seen by two instruments.** They are two different hashes (measured). The kit records both pairs and names (B) for the check against nuget.org.
2. **"The first network fetch by a seat in this project":** `SETUP_RUNBOOK.md:50` says "the first restore of the first lane took every package from https://api.nuget.org/v3/index.json". The kit therefore says "the first since every heavy job was closed (kit B1813)" and puts line 50 into FOR RECORDS.
3. **The card's detail says Tuesday runs the restore; the commission says the seat does.** The kit follows the commission and asks it as Q26.
4. **"SQLite" in the not-covered list** may conflict with the four ids (Q24).

## What I did not read
- B1841 and B1851 beyond their headers, BLUF/AUTHORITY, TOOLS, FROZEN, SHARED FILES, OWNED PATHS, WORK Step 0/1 (B1841) and REFUSE to Stamp (B1851).
- The lane plans. Jira (OXPD2-12 is RELAYED from B1833).
- The design documents beyond the pointer check.
- `ptrcheck.py`, `sidecar.py` and `closure.py` of B1833's scratch beyond what I ran or copied.
- Nothing of HPSM-POC, `Source_Documents/`, the NAS or any other card.

## Outside-the-fences disclosure
- I read the project cache's folder names and four files of `xunit.v3/4.0.3` and the testing packages (metadata, `.nupkg.sha512`, and a SHA-512 of the `.nupkg`). I also read the machine's global cache folder names and three EF nuspecs. Nothing was written to either cache.
- `gh api -X GET` was also used on three public non-Datasec repositories (`dotnet/efcore`, `npgsql/efcore.pg`, `npgsql/npgsql`), for tags, releases and two files at tags, under the OXPd_2 `GH_CONFIG_DIR`. That is GitHub, not nuget.org. No package was downloaded.
- I ran `hosted.py` twice (GETs of job logs).
- I ran `py_compile` on `fetch.py`. It wrote `__pycache__` into my gate folder, which I moved to `scratch/quarantine/` (never deleted). The gate holds exactly 11 files.
- Every other replaced scratch file was moved to `scratch/quarantine/`.
- No git verb in any project tree, no Jira, no message, no build, no test, no restore, no lock taken.
