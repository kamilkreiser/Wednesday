STARTABLE: NO as lane B was commissioned (mode FULL). The project's own package cache holds 0 of the 4 EF Core / Npgsql packages. Every restore runs behind the runner's closed proxy, and this commission forbids reaching Microsoft, so nuget.org is out. The refreshed kit therefore carries a STOP-class mode slot, S8. Mode DEVICES-ONLY (the device model, its rules, the clock check, `xunit.v3` only, no package line) IS startable today if Tuesday names it in S8. Mode FULL refuses at Step 0 until the cache holds the packages. `stamp_check.py` exits 0: 206 claims, 206 sidecar lines.

# B1833 drafter report | lane B, seat X15, refresh of kit B1826 (WP1.1 remainder: C1 device registry, C17 state database)

Drafted 2026-11-21, 17:00 to 17:17 AEDT. Clocks are from `date`: 17:00:11, 17:00:55, 17:03:10, 17:04:34, 17:06:27, 17:16:36. Drafter: Opus, read-only. Lanes A, CF, SL, R5 and W3 were not drafted and not read.

## Files
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1833_SEAT-X15_oxpd2-wp11-registry-and-state-database.md`. It is 111,722 bytes and 426 lines, sha256 `0e3892cc...`. It has 9 unfilled slot lines (S1 to S8 and the last line) and 0 non-ASCII bytes.
- Sidecar: the same path + `.measured`. It has 206 claim lines plus `PTR`, `FROZEN`, `TOOLS` and `KIT`.
- Tools for the seat: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s304/d1833/gate/`, 10 files (their sha256 are in the kit).
  - Five are copied unchanged from B1831: `clone.py`, `heavy.py`, `hosted.py`, `run_step.py`, `words.py`.
  - `place.py` is B1831's with two modes.
  - `placeprops.py` is B1826's embedded props program, made a file with refusals.
  - `cachecheck.py` is new.
  - There are two commit messages.
- Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s304/d1833/`. It holds main's tarball, `closure.py`, `ptrcheck.py`, `fill.py`, `sidecar.py`, `jira_get.py`, the gitleaks probes and the hosted logs.

## BLUF
1. **A measurement broke B1826's D2.** That kit's restore fetched EF Core, Npgsql and SQLite from nuget.org. Since kit B1813, every heavy job of this project runs through `heavy.py`, which sets `HTTP(S)_PROXY`/`ALL_PROXY` to `127.0.0.1:9` (lines 79 to 80) and uses the project cache (line 77). This commission also adds "reaches Microsoft" to the fence.
   - **Project cache:** 64 entries, 0 of 4 needed packages (`cachecheck.py`: `CACHE: 0 of 4 present`). The control fired: `xunit.v3 4.0.3 present`.
   - **Machine global cache** (`~/.nuget/packages`, never used): the three Microsoft ids are at 10.0.12, and there is **no Npgsql provider**. So the PostgreSQL half cannot be built from anything on this machine.
2. **The kit is two-mode, with no default (Q24/S8 STOP-class).**
   - **FULL** is B1826's lane, refreshed: 2 libraries, 26 controls, 4 slnx lines and 3 props lines. It is gated by `cachecheck.py` printing `CACHE: 4 of 4 present` as a REFUSE AT ONCE check.
   - **DEVICES-ONLY** is `src/Datasec.Suite.Devices` plus its tests: 11 controls (C01 to C10, C22), 2 slnx lines, no props line, and no new package.
   - My recommendation is DEVICES-ONLY now. The FULL half goes to NOT DECIDED item 6: how the cache gets seeded, which is a question past this commission's fence.
3. **What I re-measured against main `5e36d8dc`:**
   - **Tree:** 291 files. The slnx is 19 lines (sha `765755d6...`). The props file is unchanged (4 pins). `ci.yml` is unchanged (sha `c3894bbc...`, line pointers 7/40/42/45/46/48/70/72/75/76/78/120/192 re-printed). `FLOOR` = 53 = 4+23+26.
   - **Hosted run of main:** `total: 894`, skipped 4 on linux and 19 on windows, `RULES: clean (291 files)`, GUARD 10/11, neutral scan `25 of 25`. `hosted.py` printed PASS; the control printed FAIL 2; without the skipped options it printed FAIL 4.
   - **Design documents:** shas unchanged, all 28 pointers OK (control 0).
   - **CLAUDE.md:** unchanged (10,052 bytes).
   - **OXPD2-12:** unchanged (Backlog, 0 comments).
   - **The secret store is now ON main** (PR 5). The name rule at `SecretNames.cs:7-8` is the same words; it is still re-expressed as text, not referenced as code.
   - **Lane D:** READY at `70c1fad5`. It changes the slnx and `Sessions` paths only, and does not overlap this lane.
4. **Lessons carried from B1829 and B1831:**
   - Every heavy job goes through `heavy.py`, with `-p:NuGetAudit=false` on every restore and publish.
   - `hosted.py` is run with `--skipped-linux/--skipped-windows`.
   - csproj files are frozen blocks T1 to T4, extracted by program.
   - The `words.py` scan is run, with the lock-file `linux-x64`/`win-x64` note (B1829 D5).
   - The STATUS file is due within 5 minutes.
   - The lock folder is fixed by the runner. A `BLOCKED: lock held` after 30 minutes is treated as a relaunch, and the windows allow 60 minutes of lock waits.
5. **Changed from B1826 beyond D2:**
   - Step 5 runs `repo_rules.py` WITHOUT `--source-documents`. On main, the hash half prints 37 R5 findings for HP's kept inputs, and it walks the SDK's `tools/certificates/` key folder (DRAFTER_RULES line 102; B1830 F4). Lane R5 owns that fix.
   - A CodeQL naming rule is added: no `password`/`secret`/`token`/`credential`-named value is stored (GATE-VERIFIER-STANDARD step 7).
   - The history entry stays the seat's (Q18), with B1831's records-pass form as the alternative.

## What I measured and how (instrument in brackets)
- **Origin** [`gh api -X GET`, project GH_CONFIG_DIR, `gh auth status` rc 0, 17:00:55; re-read 17:16:36, unchanged]: main `5e36d8dc`; 8 heads; 0 open PRs; 6 PRs in all; `.private` true, push true. No `b1833` ref. The contents API returns 404 for all four lane folders (control: `src/Datasec.Suite.Secrets` returns 21).
- **Main's files** [tarball by GET into scratch; `cat -n`, `wc`, `shasum`]: the slnx, both props files, `global.json`, `NuGet.config`, `.editorconfig`, `.gitignore`, `ci.yml`, the Core, Core.Tests, Secrets, Secrets.Tests, Cards and Server csproj files, `GlobalUsings.cs`, `SecretNames.cs`, and the `build/tests` def counts.
- **Placement** [`place.py` full and devices; `placeprops.py`; all on scratch copies]:
  - On main: full placed 19 -> 23 lines (sha `a0bc6ff4...`), devices 19 -> 21 (sha `eb19dfe1...`).
  - On lane D's file: full at lines 6/7/18/19, devices at 6/17.
  - Props: 11 -> 14 lines in ordinal order (SqlServer before Sqlite).
  - Each placement program refuses its own output (rc 2), a CRLF file, and a bad version.
- **Cache** [`cachecheck.py` on the project cache and on `--cache ~/.nuget/packages`; `closure.py`, a nuspec walker over the global cache, DERIVED]:
  - SqlServer 10.0.12 depends on `Microsoft.Data.SqlClient` 6.1.6, which depends on `Azure.Identity` and `Microsoft.Identity.Client`.
  - The global cache also lacks `Microsoft.Identity.Client.Extensions.Msal` 4.78.0. This is approximate: the walker is not NuGet's resolver.
- **Reference pack** [grep of the doc XML, control 0]: `T:System.TimeProvider`, `ToUpperInvariant`, `IPAddress.Parse(String)`, `JsonDocumentOptions.MaxDepth` (1 each).
- **gitleaks** [8.30.1, the workflow's four options]: Q1 to Q7 rc 0; a random 40-hex `apiKey` control rc 1. Both commit messages rc 0.
- **Words** [`words.py`]: both commit messages clean (each subject 119 bytes, file 177 bytes). Control 13 of 13.
- **Kit scans:** the underscore-aware ban-name scan has 0 hits (control `x_by_Kreiser_y` fired). Card ids: 0. Non-ASCII: 0.
- **Machine** [17:04:34]:
  - Load 5.38/3.42/2.61; 1003 GiB free.
  - `.tools` had no `b1833` and no lock folder at 17:04. A lock folder existed at 17:16, another seat's job: not mine.
  - 0 OXPd2 panes out of 3.
  - Toolchain: dotnet 10.0.404 (shared framework 10.0.15), gitleaks 8.30.1, Python 3.14.10, git 2.54.0.

## CHAIN INPUTS (each step's inputs, produced earlier or present at BASE)
| Step | Inputs | Produced by / present at |
|---|---|---|
| 0 | the kit, S8 mode, `cachecheck.py` (FULL) | Tuesday's stamp; the drafter's gate folder |
| 1 | the gate folder, `<repo>`'s local identity, blocks T1 to T4 in the Step-0 copy | the drafter's scratch; BASE; Step 0 |
| 2 | the clone | Step 1 |
| 3 | the clone, the placement programs, the frozen blocks, (FULL) the versions from `cachecheck.py` | Steps 1 and 2 |
| 4 | red cells and stubs; (FULL) the Design package in the cache | Step 3; the cache (FULL REFUSES if absent) |
| 5 | the green tree | Step 4 |
| 6 | the staged tree, `words.py`, the mode's commit message | Step 5; the gate folder |
| 7 | the commit; the base's total and skipped counts | Step 6; Step 1's `hosted.py` run on BASE |
| 8 to 9 | the hosted PASS; `ci.yml`'s `neutral_export` | Step 7; BASE |

## Questions for Tuesday (defaults are in the kit; S4 answers Q1 to Q23, and S8 answers Q24 in words)
- **Q24, the mode.** There is NO default (STOP-class). The drafter recommends DEVICES-ONLY.
- Q1: two libraries in FULL.
- **Q2 (CHANGED): cache only, no fetch.**
- Q3: SQLite.
- Q4: one assembly.
- Q5: scratch scaffold.
- Q6: idempotent snapshots.
- Q7: serial 1 to 64 of `A-Za-z0-9-`, upper-invariant key, `NoSerial` refused.
- Q8: two address fields.
- Q9: no transitions.
- Q10: three kinds.
- Q11: 262144 bytes, all kept.
- Q12: six actions, no free text.
- Q13: version token.
- Q14: UTC DateTime.
- Q15: 300 s inclusive.
- Q16: delete with cascade.
- Q17: EF names.
- Q18: the seat prepends history.
- Q19: the runner's lock folder.
- Q20: rebase before the first push.
- Q21: windows of 300/240 minutes for FULL and 210/150 for DEVICES-ONLY, each including 60 minutes of lock waits.
- Q22: `Datasec/OXPd2-X15`.
- Q23: G1.
- **NOT DECIDED item 6 (new): how the project cache gets the FULL packages.** Every route left is a restore with the proxy open, which reaches Microsoft's package host. That is a question for Tuesday or the product owner. The cost of seeding only from the global cache: there is no Npgsql there.

## UNMEASURED and NEVER RUN (each marked in the kit)
- Every dotnet build and test outcome.
- The closed-proxy restore of the new projects.
- (FULL) The scaffold, EF design-time API names, `EF1001`, `HasPendingModelChanges`, the snapshot compare and its line endings on Windows, the regular expressions of C21, the transitive identity packages, and the hosted NuGet audit.
- Whether `TimeProvider` subclassing fits the test clock.
- The default MaxDepth value of `System.Text.Json`.
- Whether hosted CodeQL C# flags the `Oxpd1AdminPassword` kind member.
- `hosted.py` on a head of this lane, the owned-paths property, the boundary scan, and the push.

## Reading load (summed by program)
- The kit is 111,722 bytes.
- Its READ WHOLE list is 89,789 bytes: items 2 to 4 and 6 come to 81,639 (CLAUDE.md 10,052, CLARIFICATIONS 33,300, the runbook 23,227, plus the clone files), and the eight tool headers come to 8,150.
- **The total is 201,511 bytes, about double the ~100 kB guide.** Two things drive it:
  - the files the project's rules make every seat read (CLARIFICATIONS and the runbook);
  - the two-mode text.
- A kit for DEVICES-ONLY alone would be shorter if Tuesday rules the mode before stamping. By how much is UNMEASURED: I did not cut one.

## Corrections to the commission
- "check every package the kit needs against the cache by program": done. The result makes the commissioned lane non-startable.
- Lane D is no longer "not yet pushed". It is READY at `70c1fad5` (STATUS last line `READY B1831: 70c1fad5...`), unlanded.

## What I did not read
- The other lanes' commissions, kits and the B1823 lane plan. The plan was not re-read; I relied on B1826's carriage of it.
- The B1829 and B1831 kits beyond their tools, shared-files, work, refuse, heavy and stamp sections. B1829's STATUS beyond Step 0 to THE SOLUTION FILE and DEVIATIONS.
- The design documents beyond the 28 pointer lines. `BACKLOG.md`. `history.md` beyond its top lines.
- The secret store's source beyond `SecretNames.cs:1-20`.
- Nothing of HPSM-POC, `Source_Documents/`, the NAS library, or any decision card.

## Outside-the-fences disclosure
- I listed directory names in the machine's global NuGet cache `~/.nuget/packages`. `closure.py` and `cachecheck.py` read nuspec files and folder names there. Nothing was written.
- One `ls` of `<project>/3_Access_Keys/` (existence only, output discarded). Nothing inside was listed or opened.
- One Jira GET of OXPD2-12 with an in-process reader of the project `.env`. No value was printed.
- `gh api -X GET` only.
- gitleaks ran on scratch files only.
- I moved (did not delete) my own draft sidecar into scratch.
- No git verb in any project tree, no build, no test, no message.
