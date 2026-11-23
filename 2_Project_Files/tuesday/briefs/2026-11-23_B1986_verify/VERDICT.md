GATE B1986: GO WITH FINDINGS @ 0c65be4 on main cad65b8

Gate G1 (security surface: the first HTTP routes a printer reaches, the per-device credential, the vault binding),
**round 2 of 2 of lane H, the last round**, one Opus reader (claude-opus-5-5), in-session, read-only toward the project,
Jira and GitHub. Kit B1985 (seat X51; S4: Q1 to Q5 the coordinator's defaults, in words). Head
`0c65be474d753713e3e00e6b1726221f5d9a97bd` on `b1974/h-host-composition-v0` = round 1's `685d72b6` + ONE merge commit
`4c415f9a` (parents `685d72b6`, `cad65b86`) + ONE fix commit `0c65be47`. Main `cad65b865fc09b5e75b49d998ff61db594dd1569`
at every read (13:52 and 14:08 AEDT, GET); open pull requests 0; X1's branch at `8f5813bf` (READY B1984) at both reads.
Measured 2026-11-23 13:51 to 14:10 AEDT in my scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s316/g1986/`
(clone by the kit's `clone.py ... draft`: push URL `invalid://no-push`, no identity). Every dotnet job and test
executable through the kit's `heavy.py` (sha256 `31adedc8...`) and `.tools/wave1-heavy.lock.d`, one at a time (lock
waits 0 to 3 polls; no other holder's lock touched). No push, no pull request, no re-run, no Jira, no `cd`, nothing
deleted (the probe and the scanner control moved to `g1986/_quarantine/`). No listener but the tests' own on
127.0.0.1 port 0; the server executable never started.

**BLUF.** The head is exactly what the kit says and nothing more: the merge commit's tree `765182d5` IS `git merge-tree
--write-tree 685d72b6 cad65b86` (no hand edit, `diff --quiet` rc 0); the fix commit is 5 `M` paths, and replaying
`3-round2.diff` (sha256 `67ba3062...`) onto the merge in a temporary index gives the head's tree `a17719c2` byte for
byte; the 8 product files of `src/Datasec.Suite.Server/` are byte-equal to round 1's (no product line changed after
round 1). I ran the 15 cells myself on macOS: `Total: 15, Errors: 0, Failed: 0`; an independent `mutants_h2.py run`:
`MUTANTS: 14 of 14 MATCH, 14 of 14 undone equal`, the two new rows red on H14 alone and H15 alone by assertion
(`Expected: 401 / Actual: 200`). Whole solution at the head (= the merge with main of the moment: `merge-tree cad65b86
0c65be47` = `a17719c2`): `total: 1919`, `failed: 0`, `succeeded: 1915`, `skipped: 4`, the Server test assembly named,
and `Datasec.Suite.Jobs.Transport -> .../bin/Release/net10.0/...` (**gate B1983 FOUND 1 closed**; control: at the merge
commit alone the same build prints `bin/Debug` and the total is 1904 with 0 Server test lines). `RULES: clean (598
files)`, `Ran 111 tests OK`. The head's push run 45101722950, read by the kit's `hosted3.py` myself: `HOSTED 0c65be47...:
PASS`; the Server test assembly named 5 times and `passed` on each leg (linux 2s 686ms, windows 7s 684ms). Scans clean
with fired controls. **One Minor finding, no Blocker** (FOUND 1: one README sentence says 401 where a vault that throws
gives 503; fail closed; text only). Gate B1981 FOUND 1 and 3 are closed; FOUND 2 is narrowed in the README as the
coordinator chose (Q4).

**For a product-owner card (round 2 of 2):** this is GO WITH FINDINGS, so no NO GO card is due. Classification, as
asked: **Blocker: none.** **Minor, can ship with a ticket: FOUND 1** (a one-clause README correction). Every INFO
below ships as is.

## FOUND

1. **Minor (documentation, an overstated "only/none" sentence; ships with a ticket): Server `README.md:21`-`:23` says
   "with none, or with two or more lines, the host hands the adapter no credential and the answer is `401`". With a
   vault that throws the answer is `503`, on both routes, for none, one and two lines.** MEASURED by my probe
   (`g1986/_quarantine/probe/GateProbeB1986.cs`, scratch clone only, never committed): a rig with the host's own store
   and no `Secrets` configuration (H08's shape) answered `down-cb-none=503 | down-cb-two=503 | down-nt-none=503 |
   down-nt-two=503` (one-line controls 503 too). Cause (DERIVED, `CallbackCredentials.cs:74`-`:81`): `Verify` reads the
   stored hash for a rule-valid serial whatever the header (`StoredHash`), so a vault that throws is `Unavailable` before
   the missing credential is judged (`Oxpd2CallbackHandler.cs` step (1); `NotificationEndpoint.cs:31`-`:35`). The same
   README says 503 for a vault that throws (`:43`, `:52`), so the file contradicts itself in that shape. **Not a
   Blocker:** fail closed (no sink reached), not lane code's behaviour changing, and the kit's property is about
   reaching a sink. Fix: one clause, "while the vault answers" (the re-cut squash body in this folder already says it).
   The cells H14 and H15 are right as written (they run with a vault that answers).

## INFO

1. **Merge and fix, by program** (`scratch/struct.py`): first-parent commits after round 1: 2; the merge's parents
   `[685d72b6, cad65b86]`, the fix's parent the merge; messages equal `merge-message.txt` and `commit-message-2.txt`;
   author and committer of both one address, the same as round 1's (masked `***@datasec.com.au`), no override seen.
   Numstat 2/0, 2/2, 13/3, 30/0, 34/0; the 5 files' sha256 equal THE CODE's "At the merge" and "After" columns (10 of
   10; LF counts 36/38, 81/81, 64/74, 304/334, 291/325). Second `apply --check` on the replayed tree: rc 1, `error: patch
   failed: Datasec.Suite.slnx:8`. `685d72b6..HEAD` paths = main's 40 + the 4 round-2 paths main does not touch (slnx is
   both); main `da8d64a8..cad65b86` touched nothing under the Server folders, `README.md` or `.github` (slnx +2 only, L1).
   ls-files 564 (round 1), 587 (main), 598 (merge), 598 (head).
2. **The cells.** H14 (`HostCellTests.cs:287`) and H15 (`:302`) read whole: one-line 200 control, then good+good,
   good+junk, junk+good all 401, then `Assert.Single` on the sink (the control's call only). `RawPostAsync`
   (`HostRig.cs:142`): TCP to `Https.Host:Port` (127.0.0.1), `SslStream` accepting only the served certificate's
   SHA-256, one header line per value, `Connection: close`, status parsed from the first line or throws. Not a test
   selector; no retry; no platform condition. `[Fact]` indented 15.
3. **B1983 FOUND 1 closed (the transport in Release).** Local build at the head:
   `Datasec.Suite.Jobs.Transport -> /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s316/g1986/clone/src/Datasec.Suite.Jobs.Transport/bin/Release/net10.0/Datasec.Suite.Jobs.Transport.dll`;
   hosted linux `.../src/Datasec.Suite.Jobs.Transport/bin/Release/net10.0/Datasec.Suite.Jobs.Transport.dll`, windows
   `D:\a\OXPd_2\OXPd_2\src\Datasec.Suite.Jobs.Transport\bin\Release\net10.0\Datasec.Suite.Jobs.Transport.dll`; lines
   holding `bin/Debug` or `bin\Debug`: 0 and 0 (control `bin/Release`: 88 and 105). (The seat's STATUS prints the
   windows path with `\b` and `\n` eaten by its printer; the log itself is right, my copy is byte-equal to the seat's.)
4. **The hosted legs' Server-assembly lines (both legs), counted by me** (`scratch/hosted_counts.py`, ANSI stripped; my
   GET copies of the four job logs byte-equal to the seat's): linux 5 (control `Datasec.Suite.Core.Tests` 5), windows 5
   (control 5); `failed Datasec.` 0 and 0; `error CS` 0 and 0; `[FAIL]` 0 and 0; `total: 1919` 2 and 2; skipped 4 and 21
   (equal to main's, so no Server cell skipped: succeeded rose by exactly 15 on each leg, 1900 to 1915, 1883 to 1898).
   Round 1's legs printed 0 and 0 (gate B1981 INFO 7). PEM load, H08's store and the raw TLS client ran green on
   Windows.
5. **The README Limits line against gate B1981 FOUND 2:** `README.md:69`-`:74` say what that gate measured (a header
   line with no colon is answered 400 before any route; category `Microsoft.AspNetCore.Server.Kestrel.BadRequests`;
   level `Debug`; value included) and claim nothing about the framework's default level. "The host sets no level for
   that category": true (`git grep` of `AddFilter|SetMinimumLevel|Logging|LogLevel|ClearProviders` over
   `src/Datasec.Suite.Server`: only the README itself). "The host's own code writes no log line": the census
   `ILogger|\.Log[A-Z][a-z]*\(` over the 6 product `.cs` files rc 1 (pathspec control 6 files; control `HostRig.cs:4`).
6. **Root `README.md:14`-`:15` against the tree: true.** `:14` names Core, `Datasec.Suite.Adapters.Oxpd2`,
   `Datasec.Suite.Secrets` and the one package (Server.csproj's three `ProjectReference` and one `PackageReference`);
   `:15`: `Program.cs` runs `ServerHost.Build` (its whole text), Windows-service lifetime (`ServerHost.cs:29`), the
   `Secrets` section (`:30`), three routes (`:49`-`:51`), started in-process by the cells (12 of 15 start the host; H06,
   H10, H12 do not), the executable started by no test (`Program`/`Main(` in the test project: nothing; `ci.yml` has
   no `docker run` and no `Datasec.Suite.Server.dll` line; control `docker build` at `ci.yml:52`). The rest of the layout
   list is still behind main (lists only the Core test project): owed to the records lane, outside this round's 2 lines.
7. **Lane X1 (not mine to judge), the slnx merge:** X1 has pushed (`8f5813bf`, merge `ba15e0f9` of `cad65b86` + fix).
   `git merge-tree --write-tree 0c65be47 8f5813bf`: rc 0, `Auto-merging Datasec.Suite.slnx`, **no conflict**; merge base
   `cad65b86`; the only path both change is the slnx; H adds `:11` (Jobs.Transport) and `:33` (Server.Tests), X1 adds
   Adapters.Oxpd1 above Adapters.Oxpd2 in each folder: not adjacent; merged slnx 34 Project rows, 0 markers; tree
   `7ad207ef`, 628 files. On that tree (scratch worktree by `read-tree -u -m`): locked restore rc 0 with lock files
   unchanged, build 0/0 (Oxpd1 and transport under `bin/Release`), `total: 1940`, `failed: 0`, `succeeded: 1936`,
   `skipped: 4`, `RULES: clean (628 files)`. landing.txt MAIN MOVES (B) carries it.
8. **Seat deviations read (RELAYED, the gate agrees):** DEVIATION 1 (a second locked restore before the test-project
   build) and 3 (the test assembly not recompiled by a product-only undo) are kit wording, not lane faults; my run
   rebuilt the solution after the mutants and ran it green. DEVIATION 6 (`sed -i` on the seat's own scratch file) touched
   no project or repository file.
9. **Cosmetic:** Server `README.md:25` is a new 209-character line (a rewrap left undone in the callback paragraph); no
   rule reads it.
10. **Not checked or not run by me:** CodeQL (no `Analyze` row on a branch push: analyses for the branch ref 0, control:
    main's three rows at `cad65b86`, results 0; read on the pull request, landing.txt step 3); the local publishes and
    `release_guard.py` (the hosted legs' `GUARD: clean (14 files)` / `(15 files)` read by me instead); `run_step.py`'s
    neutral scan locally (the hosted secret-scan row, hardened, read by me: 25 of 25, `not among them 0`); every cell on
    a device; the merged H+X1 tree on Linux or Windows.

## FRAME QUESTION (stamp checklist item 11): each "never / every / only / none" sentence the round adds, three shapes outside the tested one

| Sentence (Server README at the head unless named) | Shape 1 | Shape 2 | Shape 3 |
|---|---|---|---|
| `:18`-`:20` "answer `403` to a request that did not come over HTTPS, before the host's own code reads anything else" | TLS-terminating proxy forwarding HTTP: 403, round 1's named limit H10 | HTTP/2 cleartext: no cell; `IsHttps` false whatever the protocol (DERIVED, `CallbackEndpoint.cs:15`, `NotificationEndpoint.cs:20`) | malformed header over plain HTTP: the framework's 400 before routing (B1981 MEASURED over TLS; over HTTP DERIVED), so 403 is never written: the sentence's "host's own code" scope covers it |
| `:21`-`:23` "credential read only from a request with exactly one `Authorization` line; none or two or more: `401`, whichever line holds it" | three lines (credential x3): **401 both routes, MEASURED by my probe** (was DERIVED) | empty `Authorization:` line, and credential + empty line: **401 both routes, MEASURED**; one comma-joined line: H03 (callback), **notification 401 MEASURED** | **a vault that throws: 503, not 401, for none / one / two lines, MEASURED: FOUND 1** |
| `:69` "The host's own code writes no log line." | Kestrel `BadRequests` at Debug: the next sentence names it | hosting/routing at Trace: H11 (well-formed lines, with its in-cell control) | an exception escaping a handler: no cell; its text UNMEASURED (a named gap, unchanged from the seat's row) |
| `:72`-`:74` "A well-formed `Authorization` line, right or wrong, reaches no log line at `Trace` (H11, on the paths the cells cover ...)" | a wrong line on the notification route: **no captured line held the junk value, MEASURED by my probe** (205 lines at Trace; H11's own control proves capture) | two lines (good+good, good+junk, three lines): **no line held the issued or the junk value, MEASURED** | the Windows event log: not captured (stated in the sentence) |
| root `README.md:15` "the executable itself is started by no test" | `Program` in-process: no test references it (git grep, nothing) | the published executable in CI: no `ci.yml` line runs it | the container image: built at `ci.yml:52`, never run (no `docker run` line) |

## MEASURED (my runs; logs in `g1986/logs/`)

- Tools: `scratch/tools_hash.py`: THE TOOLS 10 of 10 equal to the kit's sha256 in three copies (the drafter's
  `seat-tools`, the seat's `.tools/b1985/gate`, mine); control one byte changed differs.
- Origin (GET 13:52, 14:08): main `cad65b86`; `b1974/h-host-composition-v0` `0c65be47`; `b1976/x1-oxpd1-read-client`
  `8f5813bf`; open pull requests 0 (newest 35, closed); `compare cad65b86...0c65be47`: ahead 3, behind 0, 16 files;
  code-scanning open alerts on main 0.
- Head (`g-*`): `g-restore-locked` (`CI=true`, `--locked-mode --force`) rc 0, 32 projects, `status --porcelain` 0
  lines; `g-sln-build` 0 Warning(s) 0 Error(s), 32 outputs under `bin/Release`; `g-exe-green` `Total: 15, Errors: 0,
  Failed: 0, Skipped: 0, Not Run: 0`.
- Mutants (`mutants-run.out`, an independent run, every job through `heavy.py`): 14 rows, each `Total 15`, each `MATCH`,
  each `undone equal True`; last line `MUTANTS: 14 of 14 MATCH, 14 of 14 undone equal`. After: `status --porcelain` 0
  lines; `g-sln-build2` 0/0 (rebuilt); `g-sln-test` `Test run summary: Passed!`, `total: 1919`, `failed: 0`,
  `succeeded: 1915`, `skipped: 4`, 3 lines holding `Server.Tests.dll`.
- Control at the merge commit (`m-*`, `switch --detach 4c415f9a`): locked restore rc 0; build 0/0 with the transport
  under `bin/Debug`; test `total: 1904`, `failed: 0`, `succeeded: 1900`, `skipped: 4`; lines holding
  `Server.Tests.dll` 0 (control `Core.Tests.dll` passed).
- `repo_rules.py` (no `--source-documents`, after `test ! -e g1986/1_Project_Definition` rc 0):
  `RULES-NOTE: R5 hash half NOT RUN (no supplied-source folder here)`, `RULES: clean (598 files)`;
  `unittest discover build/tests`: `Ran 111 tests`, `OK`.
- Hosted (`hosted3.py 0c65be47... --total 1919 --rules 598 --skipped-linux 4 --skipped-windows 21 --unit 111 --floor
  111 --hardened-scan --guard-linux 14 --guard-windows 15`, GET, run 45101722950, attempt 1 every job): linux 1919 x2 /
  1915 / 4 / `GUARD: clean (14 files)`; windows 1919 x2 / 1898 / 21 / `GUARD: clean (15 files)`; rules `Ran 111`,
  floor 111, `RULES: clean (598 files)`; secret-scan both planted controls, `NEUTRAL-SCAN: stored objects 1561 ...
  not among them 0`, `NEUTRAL-SCAN-REACH ... not among the stored objects 0`; check runs beside the four 0; last line
  `HOSTED 0c65be474d753713e3e00e6b1726221f5d9a97bd: PASS`.
- Probe (`g-probe-*`): `Total: 16, Errors: 0, Failed: 1` (the probe alone, by design: its message carries the
  statuses): `cb-one-good=200 | cb-three-good=401 | cb-empty-line=401 | cb-good-then-empty=401 | cb-none=401 |
  nt-one-good=200 | nt-three-good=401 | nt-empty-line=401 | nt-comma-joined=401 | nt-good-then-junk=401 | sinks cb=1
  nt=1 | log-lines-holding-junk-value=0 | log-lines-holding-issued=0 | log-lines=205 | down-cb-one=503 |
  down-cb-two=503 | down-cb-none=503 | down-nt-one=503 | down-nt-two=503 | down-nt-none=503`. After: probe moved to
  `_quarantine/probe/`, `g-final-build` rc 0, `g-final-exe` `Total: 15, Errors: 0, Failed: 0`; `status --porcelain` 0.
- H + X1 (`hx-*`): as INFO 7.

## SCANS

- gitleaks 8.30.1: control FIRST (a token built by program from two halves and 36 random characters, never printed,
  outside any clone): rc 1, `leaks found: 1`, moved to `_quarantine/gl-control`. Then the head's 5 changed blobs, the
  81 added lines, both commit messages and the patch as `1.txt` to `9.txt` (`scratch/neutral`): rc 0, `no leaks found`;
  `gitleaks git` over `685d72b6..0c65be47`: `4 commits scanned`, rc 0, `no leaks found`.
- `words.py --control` `CONTROL FIRED: 13 of 13`; over `added.txt` (81 lines) and both messages as stored:
  `WORDS: clean (3 files)`.
- My landing texts: `squash-subject.txt` with #36 (167 characters), `squash-body.txt`, `pr-title.txt` (162 bytes):
  `WORDS: clean (3 files)`; `build/squash_scan.py` from the clone's `build/` (equal to main `cad65b86`'s `build/` and
  `.github/`: `diff --quiet` rc 0), subject with #36: control rc 1 found 2, message rc 0 found 0, `SQUASH-SCAN: clean`.
  `pr-body.md` (GitHub text only, never repository text): `coordinator` 2 (the "Who decides" paragraph) and 4 bytes
  outside ASCII (the attribution emoji), as round 1's: expected. gitleaks over every text of this folder under neutral
  names: rc 0, `no leaks found`; re-run after the last edit over all 7 texts (this file included,
  `scratch/neutral-final`): rc 0, `no leaks found`.

## NOT RUN

CodeQL (on the pull request); local publishes and the release guard (read on the hosted legs); any device, printer or
address but 127.0.0.1 and the origin; the merged H+X1 tree on Linux and Windows; the pull request's merge ref (no pull
request exists); `repo_rules.py --source-documents` (forbidden).

## DEVIATIONS

- `mutants_h2.py run` ran as one background shell call (the harness bounds a foreground call at 10 minutes), one
  process, every job through `heavy.py`; no other heavy job until it ended.
- One probe file compiled into MY scratch clone only (never into the head, never pushed), then moved to
  `_quarantine/probe/` and the clone rebuilt and re-run green 15 / 0. Evidence, not a cell.
- Trees left: the scratch clone's work tree and index are at the H+X1 merged tree `7ad207ef` (read-tree, scratch only;
  HEAD is `0c65be47` detached); left so, rather than removing X1's files from the work tree.

## WHO DECIDED

Every choice of lane H (both rounds), the merge-then-fix shape, the two solution lines, the README-only answer to
gate B1981 FOUND 2, and the landing order relative to X1 is the coordinator's (Tuesday's), as coordinator; none is the
product owner's. FOUND 1 is for the coordinator to ticket (one README clause); it does not block this landing.
