# B266 + B267 DRAFTER REPORT (read-only drafting sub-agent for Tuesday, 2026-10-18 17:10-17:25 AEDT)

## What was drafted
| file | lines | sha256 (at writing this report) |
|---|---|---|
| `2026-10-18_B266_SEAT-T1_hpsmpoc-269-sdk-tooling.md` (HPSMPOC-269 only, tooling, tier 2) | 123 | `ebdf872d641da07094734de292aefde7da37937f7388ef127dc6a059a3681d8e` |
| `2026-10-18_B267_SEAT-H5_hpsmpoc-round3.md` (HPSMPOC-286, -281, -284, -285, -283, -282, -287; tier 1 overall) | 135 | `eb500ec107c4d7ddb9f410a4552a80cfc20b5e27c9898c42fd472048bb9afad4` |
Both carry the template's standing lines (mail-channel line, AUTHORITY C-105 verbatim, PRIOR-WORK CHECK, CodeQL never bypassed / no alert dismissed, no deploy / no Azure, never delete, no `cd`, zsh traps, the HP Restricted hold verbatim from B248 `:26`, STATUS as the channel, `PLAYWRIGHT_BROWSERS_PATH` per run if a browser is ever needed), a REFUSE check that fires while the stamp still reads `RULED: ____` (count 1 in each draft now; 0 once stamped; the `.pre-stamp` copy is the control), and a `## TUESDAY STAMP` with RULED/SELF-CHECK slots and my defaults. Invisible/bidi characters: 0 in each (control: an appended U+202E counts 1).

## Facts that shaped the briefs (each with its instrument)
1. **CI already builds main on SDK 10.0.402.** `gh api --allow-escape-sequences …/actions/jobs/117592136115/logs` (main push run 39099314408 of `dff4019`, 17:13): `:145` `install-dotnet.sh … --channel 10.0`, `:151` `Installed version is 10.0.402` (05:05:18Z); runtime `:140` 10.0.13. So local `.tools/dotnet` (10.0.401) is one patch behind CI, and this closes B262's UNMEASURED "which SDK CI installs today". B266 pins local to CI's SDK.
2. **The bits are already on disk, verified offline.** B255 kept `.tools/b255/sdk-dl/verify/sdk.tar.gz` + `releases.json`. `shasum -a 512` (17:15): `ee0d379c144ebdde…74d00b75` occurs 2× in that JSON, as the `10.0.402` osx-arm64 SDK tarball; control: the 401 entry's hash differs (`69f64eb0…`). The JSON says `latest-sdk 10.0.402`, `latest-release 10.0.13` (2026-10-13). Its AspNetCore pack manifest `:42` (in B255's install of it) = `10.0.1326.50504` = the pin's file version: **a tie**, the condition under which B255's mutants are provable. Hence B266's money line: no download at all by default.
3. **An additive install overwrites exactly 22 files** (`python3 -I` over the tar list vs the directory, 17:16): `dotnet`, `dnx`, `LICENSE.txt`, `ThirdPartyNotices.txt` and 18 under `sdk-manifests/10.0.100/`; the other 4,884 land in new versioned directories. B266 backs up the whole tree first (649 MB; 925 GiB free) and writes THE WAY BACK, proven on a scratch copy.
4. **Every HPSM seat runs `.tools/dotnet`.** `brief_seat.sh:30-32` exports `DOTNET_ROOT=$DIR/.tools/dotnet` and puts it first on PATH; `global.json` @ `dff4019` is `10.0.401` + `rollForward: latestFeature`, which picks the highest 4xx patch present, so 402 takes effect for every build the moment it appears (the brief makes B266 measure this, step 6, with a 401 control).
5. **-287's Done-when has a migration branch.** Jira GET 17:11: *"…either shown safe … and its warning recorded as expected, or changed so a SQLite host start logs 0 such warnings…"*. The second branch = editing migrations (or suppressing the warning in a DbContext): written into B267 as STOP-and-ask, never built; B267 builds only the first branch, last and droppable. The Done-when is the records drafter's (B265 FOR TUESDAY), so it is also ruling R-5.
6. **No .NET product code needed.** -282 can register the wait on the Feedback contexts test-side (`ApiFactory.cs:145-146` already does `services.ConfigureDbContext<…AssessmentDbContext>`; the Feedback contexts are `SqliteFeedbackDbContext`/`SqlServerFeedbackDbContext`, `FeedbackModule.cs:79`, `:84`). So B267's partition excludes all of `api/src/`; the only product file is `web/src/server/formGate.ts`.
7. State re-verified: code main `dff4019…` (`ls-remote` 17:11:55; no `b266*`/`b267*`); records main `d479cb67…`, 115 C-headings, C-113 `:1424` (`gh api` 17:14:29); open PRs 0, open code-scanning alerts 0, check runs on `dff4019` 18 success + 1 skipped; all eight tickets Backlog with 0 comments (Jira GET 17:11:12-15); ports 6990-6999 free (`lsof` rc 1); `b262-mssql`, `b263-*` exited and kept.

## B267's order, by file overlap
-286 → -281 → -284 → -285 → -283 → -282 → -287.
- `formGate.ts` chain (items 1-4, all also touch `formMeter.test.ts`): **-286 first** (tests only: pins the first-name rule `:141` and `headerParams`' null contract `:74-77` before anything moves; green at main, red under B263's m263-276a/-276d); **-281** changes what `isFilePart` counts (`:136-145`); **-284** changes the header limit (`:198`, `:209`); **-285 last** because it rewrites the same scan/carry (`:151-219`) and must keep -284's new test green.
- .NET items, disjoint files: **-283** (`PkcsInPackageTests.cs`, cheapest), **-282** (`HostedDemoRobustnessTests.cs` + one method in `ApiFactory.cs`; needs the SQL Server container), **-287** (one new test file; last, first to drop).
- **Tiers:** -286 t2 · -281 **T1** · -284 **T1** · -285 **T1** (it rewrites the loop that decides the 413) · -283 t2 · -282 t2 · -287 t2 (it would be T1 if it touched migrations: it may not). **Overall tier 1.**
- **Customer-facing words: expected none.** Proof the brief requires: every non-comment string literal added to `formGate.ts` listed (parser tokens / byte constants only, B263 check 13's method); the 413 body asserted byte-equal; `api/src` 0 changed paths (planted-path control), so no API answer can change.

## PARTITION: can B266 and B267 run in parallel? No. Recommend B266 first, then B267.
| dimension | B266 | B267 | disjoint? |
|---|---|---|---|
| repo files | none (no commit, no branch) | branch `b267/…`: `formGate.ts`, web tests, 3 .NET test files | yes |
| `.tools/` paths | WRITES `.tools/dotnet`; `.tools/b266/`, `wt-b266*` | RUNS `.tools/dotnet` (via `brief_seat.sh:30-32`); `.tools/b267/`, `wt-b267*` | **no: `.tools/dotnet`** |
| SDK seen | changes it | would switch from 401 to 402 mid-run (global.json `latestFeature`), invalidating its .NET base/tip/mutant comparisons | **no** |
| ports | none | 6990-6999 | yes |
| containers | none | `b267-mssql[-n]` | yes |
| machine load | build + SQLite suite + 4 mutant publishes | web suites, .NET suites, an amd64-emulated SQL Server shard | **no**: 8 cores, two NexusAI tier-1 QA gates live (gate25, gate26, `cockpit.sh status` 17:12); B262 alone peaked at 9.69, B263 at ~9; the "< 6, one heavy job" rule cannot hold for two HPSM seats at once |
Sequencing also helps B267: its .NET suites then run on the SDK CI uses (10.0.402), -283 can correct the comment `PkcsInPackageTests.cs:156-158` that B266 makes untrue (R-6), and B267's gate can take B266 as item 0. B267's Step 0b refuses to run while the `Datasec/HPSM-POC-T1` pane is alive and records the SDK at start and end. Alternatives offered in the stamp: (b) parallel with B266 confined to its own SDK path and the swap deferred (does not meet -269's Done-when until later); (c) B267 first on 401.

## Stamp defaults (Tuesday decides)
- **B266:** R-1 (a) additive into `.tools/dotnet` beside 401/10.0.12, after a proven full backup · R-2 (a) its gate = item 0 of B267's gate (tier 2 inside tier 1) · R-3 (a) offline bits from B255's kept tarball · R-4 B266 first, alone.
- **B267:** R-1 (a) after B266 · R-2 (a) decode encoded-word names as .NET is measured to, count anything else encoded-word · R-3 (a) value-less skip in `isFilePart` only, `headerParams`/`formBoundary` byte-equal · R-4 (a) -285 counted test-side (spy on `Uint8Array.prototype.indexOf`), no product seam, STOP if impossible · R-5 (a) -287 first branch only · R-6 (a) fix the stale `:156-158` comment only if B266 ends READY · R-7 partition as written · gate tier 1.
- **Decision for Tuesday worth a look:** -285's and -287's Done-whens are the records drafter's, not the gate's (B265 FOR TUESDAY); R-4 and R-5 are where to replace them if wanted.

## What the B266 seat must prove (summary)
`.tools/dotnet` reads SDK 10.0.401 + 10.0.402 and runtimes 10.0.12 + 10.0.13 (read back, dated); the bits' sha512 = `releases.json`; the change = new versioned directories + the 22 named files, nothing removed; main (`dff4019`) builds with 0 warnings and its SQLite suite gives B262's counts for this tree (2,981 passed, 22 Blob skipped) on 402; the Pkcs class green, with the early warning now green on a TIE; **B255's m1, m3, m4a, m4b each RED on 402**, with the publish child observed running 402, and m4b's deps-entry and m3's no-raise-the-pin messages quoted (HPSMPOC-272's clauses on real mutants for the first time); later seats get 402 (fresh `brief_seat` env), with a 401 control.

## Corrections to my own instruments (in the open)
- My first prior-work key grep used `\b` in `git log -E --grep`: its control (`HPSMPOC-260\b` on `dff4019`) returned **0** though `d1fca80`'s subject holds that key. Re-run with `([^0-9]|$)`: control 2, keys `HPSMPOC-(269|28[1-7])` 0. Both briefs now tell seats to use `([^0-9]|$)` and say why.
- My first CI job-log GET returned rc 1 ("terminal escape sequences"); re-run with `--allow-escape-sequences`, escapes stripped by `tr`, 503 lines.
- One command of mine held a stray `cd /dev/null`; the project hook refused it before it ran (no effect). Every other path was absolute.

## Read-only conduct
Wrote only the three files named. Jira: GETs only (`.tools/b265/jira.py`, credentials by name in-process, never printed). GitHub: `gh api` GETs under the project's `.gh-config`. Git: `--no-optional-locks` read verbs in `2_Project_Files` (`ls-remote`, `cat-file`, `show`, `grep`, `log`, `ls-tree`); no fetch, pull or worktree. `4_Credentials/.env`: two name-only `grep -c` counts (mail key 0, Jira URL control 1), no value read. No az, no HTTP to any hosted site, no mail. Not opened: `HP Reporting and Docs/`, `2_Project_Files/HP Docs/`, the SOW, `Source_Documents/`, `4_Credentials/inbound_with_secrets`. Load at 17:23: 3.57 3.67 3.60.

## UNMEASURED
- Whether `dff4019`'s rewritten guard turns all four mutants red on 402 (B255 measured red only against B254's older guard).
- `dff4019`'s full local suite on 402; the live `releases.json` today.
- .NET's encoded-word decoding beyond `=?utf-8?B?…?=`; .NET's exact `HeadersLengthLimit` boundary; whether a test-side spy can see `indexOfBytes`' scans; -287's warning event id and per-migration safety.
- Either seat's duration.
