STARTABLE: YES

# B2159 DRAFTER REPORT, lane L5 (seat X86): OXPd OneDrive slice 2 (upload into a My Drive folder, download for print)

Drafted 2026-11-27 by an in-session read-only drafter (Opus) for Tuesday s334, commission `tuesday/briefs/2026-11-27_B2159_OXPD-LANEP-FIRST-KITS_COMMISSION.md`, section "Lane L5 (seat X86)". My first `date` printed `Fri 27 Nov 2026 17:39:11 AEDT`. The sidecar's first line gives the write clock (17:57:32). Kit: `tuesday/briefs/2026-11-27_B2159_SEAT-X86_oxpd2-l5-onedrive-slice2.md` (249 lines). Sidecar: `.measured`. `stamp_check.py` exited 0 and printed "172 claims, 172 measured, 0 not measured". Scratch: `fleet/state/s334/d2159-L5/`. The seat's tools are in its `seat-tools/`.

**The report's file name has `X86` in it** because four drafters share B2159. A bare `2026-11-27_B2159_DRAFTER-REPORT.md` would collide, so this departs from DRAFTER_RULES' name form (Q7).

**STARTABLE means the kit is complete and passes stamp_check.** The launch still waits on things outside the kit: the stamp, no other OXPd seat live, and the lock order. B2153's seat X82 is next on the lock. At 17:49 the lock was held by `B2157 | pid 92618 | parallel-heavy-build experiment`, and load1 was 20.

## BLUF
- **Upload (D1).** `MyDriveFiles.UploadAsync(folderId?, fileName, stream, length, tokens, ct)` checks every argument before it sends anything. It then makes ONE `POST me/drive/root:/<name>:/createUploadSession` (or `me/drive/items/<id>:/...`) through `GraphClient.SendAsync`, with the body `{"item":{"@microsoft.graph.conflictBehavior":"fail"}}` (A11 C20). It reads `uploadUrl` (https, no user info, at most 8192 characters, else `MalformedSession` and no piece is sent), and the landed `GraphClient.UploadAsync` sends the pieces with no Authorization header. The final item is read with the browser's own `ReadItem`. It must be a file, and its size must equal the length sent.
- **Download (D2, Q2 STOP-CLASS).** This follows the source app's two-step form (A11 C17). First `GET me/drive/items/<id>` with the token through the Graph layer. The item must be a file within the bound and carry `@microsoft.graph.downloadUrl`. Then ONE plain GET of that address through a caller-supplied `HttpClient`, **with no header added**, bounded by `DefaultMaxDownloadBytes` (100 MiB). The failure kinds are `DownloadStatus`, `TooLarge`, `DownloadLength` and `DownloadTransport`. Cell F09 and mutant `mDownloadBearer` prove that the token never reaches the download host. I chose this over `GET .../content` because with `.../content` the token's fate on the redirect would depend on the host's handler, and no cell here can reach that.
- **Who writes what.** The seat writes the code (C1 to C5), the fake and the cells F01 to F13, to a precise spec: signatures, call shapes, statement forms the mutants hook onto, and failure kinds. It also writes the eight mutant rows (`mutants_l5.json`) from its own code BEFORE the run. **The expected red cell of each mutant is frozen in the kit.** `mutants_c3.py` (B2153's tool, byte for byte) only needs a red outside the suite's 13 F cells to make a row DIFFER, so a landed O-cell turning red is the only extra red that fails a row.
- **One landed line changes:** `MyDriveBrowser.ReadItem` goes from `private` to `internal`. The README is rewritten in part (its "Not in this slice: ... download, print, scan" line).
- **PREDICTED:**
  - OneDrive executable: `Total: 93` (BASE 50, DERIVED from 6 Facts + 44 InlineData).
  - Whole solution: `total: 2474` (BASE 2431, MEASURED by `hosted3.py` PASS; the 2432 control gave FAIL 4).
  - `RULES: clean (684 files)` (679 + 5).
  - These come from 43 new cases: 6 Facts and 7 Theories with 37 rows, recounted by program.

## FACTS RE-MEASURED (instrument, then what it printed)
- **Origin** (`gh api -X GET`, OXPd GH_CONFIG_DIR, 17:41:47): main is `760e1a644ce9...` (tree `8e3985c1`, parent `0ca8c655`, PR 58). Open PRs: 0. `matching-refs/heads/b2159`: 0 rows.
- **BASE tree:** the tarball by `gh api -X GET` has 679 files. A scratch `git write-tree` gave `8e3985c1`, equal to the origin's tree.
- **BASE hosted:** `hosted3.py 760e1a64 --total 2431 --rules 679 --skipped-linux 4 --skipped-windows 21 --unit 117 --floor 117 --hardened-scan --guard-linux 14 --guard-windows 15` gave PASS. The control `--total 2432` gave FAIL 4, rc 1.
- **OneDrive tests at BASE** (`BrowseTests.cs`, by program and by `grep -c -E '^[[:space:]]+\[...'`): Fact 6, Theory 6, InlineData 44, column-1 0.
- **`checks_l5.py`:**
  - On BASE's index: `CHECKS: 2 of 9 PASS`, and all nine controls FIRED.
  - On the simulated staged tree (a never-compiled prototype of the seven files): `CHECKS: 9 of 9 PASS`.
- **`mutants_c3.py`:**
  - `--list` over eight prototype rows: `LIST: 8 mutants, 1 suites, 13 cells`, rc 0.
  - A bad row under `src/Datasec.Suite.Graph`: `LIST REFUSED: rows mBad`, rc 1.
  - `apply`/`undo` of each of the eight on the prototype: `equal True` ×8.
  - I rewrote the prototype rows away from `if (false)`, because TreatWarningsAsErrors would fail that build (CS0162). The kit forbids constant conditions in mutant NEW texts.
- **`words.py`:** `--control` gave `CONTROL FIRED: 13 of 13`. On the commit message: `WORDS: clean (1 files)`. B-number count: 0.
- **gitleaks 8.30.1:** the control gave rc 1 (quarantined). The 8 tools gave rc 0, `no leaks found`.
- **Tools:** six of the eight are B2153's byte for byte (sha256 equal). `heavy.py` is the canonical `31adedc8...`.
- **Seat id X86:** 0 hits in the briefs folder apart from this commission, and 0 in `<project>/1_Project_Definition/Briefs/` (control `SEAT-X81`: 2). It is free.
- **Partition:** the count of `onedrive` (case-insensitive) is 0 in kits B2153, B2155 and B2146. B2156 lines 107 and 118-119 give ONEDRIVE `src/Datasec.Suite.Panel/Apps/OneDrive/**` too, and say Teams/SharePoint consume OneDrive's API. The kit touches neither.
- **A11** (sha256 `170407c3...`): C17 is line 234, C20 line 237, C21 line 238. A11 itself says its calls were "not checked against Microsoft's documentation".

## D-DECISIONS (all are coordinator defaults)
- **D1:** use an upload session for every size.
- **D2:** two-step download with a plain client and no token on the download address.
- **D3:** conflict rule `fail`, as in the source app.
- **D4:** narrow file-name rule: `[A-Za-z0-9._-]`, 1 to 128 characters, no leading or trailing dot.
- **D5:** 100 MiB download bound, as a constructor argument.
- **D6:** one address helper for both answers; the host is not bound.
- **D7:** item rules are the browser's `ReadItem`, made internal.
- **D8:** new cells only; CodeQL not run locally.

## Q-QUESTIONS FOR TUESDAY (each with its default)
- **Q1:** session for every size. Default: yes. Alternative: also the simple PUT under 3.5 MB.
- **Q2 (STOP-CLASS, S4 in words):** download form. Default **a**: two-step, token-free fetch. Alternative **b**: `GET .../content` through the Graph layer; the redirect becomes a named limit, and C1, F09-F12 and two mutants are re-drafted.
- **Q3:** conflict rule. Default: `fail`. Alternative: `rename`.
- **Q4:** name rule. Default: narrow. Alternative: allow spaces.
- **Q5:** download bound. Default: 100 MiB. Alternative: the Graph `MaxResponseBytes` (4 MiB).
- **Q6:** gate and launch. Default: **G1** (a token-path surface), Opus, READY at Step 0 + 240, push at Step 0 + 210, pane `Datasec/OXPd2-X86`, launch after X82, one OXPd seat at a time.
- **Q7:** names. Default: `.tools/b2159-x86`, branch `b2159/x86-onedrive-slice2`, `2026-11-27_B2159-X86_*` STATUS/HANDOVER, and this report's `_X86_` name, because B2159 is shared by four lanes. Alternative: a B-number per lane.

## UNMEASURED (each is named in the kit where it is used)
- No dotnet job ran, so every pin, green, total and mutant expectation is PREDICTED, each with the assertion it must break. The wave lock was never taken.
- **How Microsoft Graph answers any of these calls**, including whether `@microsoft.graph.downloadUrl` comes on a plain item GET, the 409 on a taken name, and the session's expiry. The fake's answers are assumptions, and the README must say so.
- Whether `Uri` keeps `:` unescaped in `root:/<name>:/createUploadSession`. F01 asserts the exact path, so the seat's pin run measures it. If it is escaped, the expectation is the kit's and it is a STOP.
- The prototype (`d2159-L5/sim_tree/src/...`, `gen/mutants_proto.json`) was never compiled. It is NOT given to the seat.
- Whether the release guard counts (14/15) hold. They should, because the server does not reference OneDrive (DERIVED).

## CHAIN INPUTS
| Step | Inputs |
|---|---|
| 0 | stamp (S2 BASE, S3 state, S4 Q2, S8) |
| 1 | `<src>` (exists), `<repo>` values, origin, BASE hosted |
| 2 | BASE files (from 1), A11 (exists) |
| 3 | THE CODE and cells (kit), restored clone (1) |
| 4 | pinned tree (3), README (kit), rows file written in 4 from the Step-3 code before its run, `mutants_c3.py` (1) |
| 5 | green tree (4) |
| 6 | staged tree (5), checks/words/message (1) |
| 7 | commit (7a), origin/main fetch, run_step/hosted3 (1) |

## PARTITION
**This kit owns:**
- added: `src/Datasec.Suite.OneDrive/{MyDriveFiles.cs, DriveFileException.cs, DriveFileBytes.cs}`
- changed: `src/Datasec.Suite.OneDrive/README.md`, `src/Datasec.Suite.OneDrive/MyDriveBrowser.cs` (one line)
- added: `tests/Datasec.Suite.OneDrive.Tests/{FileFake.cs, FileTests.cs}`

**The other side of each boundary:**
- **L0:** slnx and the new project folders, including B2156's wide app projects. None is shared, and no csproj or lock file changes here.
- **L9:** no repo file.
- **L1:** `Adapters.Oxpd1.Agents/**`.
- **B2153:** HostRig, HostCellTests and the three READMEs (Transport, Oxpd1, Lab).
- **B2155:** `build/**`, ci.yml and the root README.
- **B2146:** records files.

None of these is shared, so **there is no STOP for this drafting.**

## OUTSIDE THE FENCES (disclosure)
- **Writes:** only the kit, its `.measured`, this report, and scratch under `fleet/state/s334/d2159-L5/`. The scratch holds the tarball, `src_760e`, `sim_tree` (a scratch git repo with no remote and no commit, plus an alternate index under `gen/baseidx`), `seat-tools/`, `gen/` and `_quarantine/` (the gitleaks control and the first TODO sidecar skeleton, moved there and not deleted). Nothing was written to the OXPd project folder, Jira, GitHub, cards or mail. No push, no PR, no dotnet job, no lock taken.
- **Project reads,** by path only:
  - `CLAUDE.md` (lines 7, 25, 55, 56, 82, 83 and its sha256)
  - `CLARIFICATIONS.md` (sha256 and its last C-ids)
  - `BACKLOG.md` (sha256 and line count only)
  - A11 lines 205-250 and 330-345
  - a grep of `Analysis/` and `Design/` for the upload/download call names
  - `ls` of `Briefs/` and `.tools/` (depth 1), and a recursive `grep -l` of `Briefs/` for `SEAT-X86`/`SEAT-X81`
  - the lock's `owner.txt`
  - `.tools/dotnet --version`

  I never touched `Source_Documents/` or `4_Credentials/` beyond `GH_CONFIG_DIR` for `gh`.
- **Hook refusals,** each refused before anything ran:
  - an unquoted `======` separator (re-issued with `----`)
  - one compound command that held a pointless `git stash list` (re-issued without it)
- **GitHub:** `gh api -X GET` only: commits/main, pulls, matching-refs, one tarball, and check runs and job logs via `hosted3.py`. No other host was contacted.
- **Tuesday-tree reads:** DRAFTER_RULES, the B2159 commission, the B2154 plan (whole), the B2153 kit (whole), its drafter report and the head of its sidecar, a grep of B2156 for OneDrive, a count of `onedrive` in kits B2155 and B2146, the `stamp_check.py` header, `models_latest.json` and `model-routing.md` row G1.
- **Not read whole:** kit B2138 and its sidecar and report. B2153's kit is B2138's form one step on, and I copied B2153's form. That is a departure from the commission's "read both whole", stated here.
- I did NOT read the ledger, the scoreboard, `fleet/briefs_staged/`, any card store, or any WEDNESDAY/FRIDAY tree.
