STARTABLE: YES - nothing the lane needs is missing: main c56f3f3b holds Logging (the logger type and the log scanner); the package cache holds every package the two projects need (xunit.v3 4.0.3, Serilog 4.4.0, Serilog.Sinks.File 7.0.0); no printer, tenant, Azure, spend or open answer; Questions Q1 to Q16 each have a default. stamp_check exits 0 (222 claims, 222 measured).

# B1825 drafter report | lane A, seat X14, WP3.8 shared Graph layer (OXPD2-16, G2)

Drafter: Opus (in-session), 2026-11-21 09:20 to 09:40 AEDT (clocks by `date`). Read-only except the kit, its sidecar, this report and scratch under `fleet/state/s303/d1825/`.

## Files
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1825_SEAT-X14_oxpd2-wp38-graph-layer.md` (315 lines, 92679 bytes; 8 stamp slots, `____`).
- Sidecar: `...wp38-graph-layer.md.measured` (223 lines; `stamp_check.py <kit>` rc 0: 222 claims, 222 measured).
- The seat's tools (READ and COPY only): `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s303/d1825/gate/`, seven files: five are B1820's `gate/` files copied unchanged (heavy.py, clone.py, words.py, run_step.py, hosted.py; sha256 equal to the B1820 kit's table); two are new: `place.py` (puts the two solution-file lines in place by the ordinal rule against the file as it stands, refusing a second placement) and `commit-message.txt`.

## BLUF
1. The kit builds `src/Datasec.Suite.Graph` and `tests/Datasec.Suite.Graph.Tests`. Paging is bounded (same origin only, loop detection, max pages). It retries only 429 and 503, using a strict `Retry-After` grammar (frozen as block R, 25 rows) with a per-wait cap and a total-wait cap. On a 401 it asks for a new token once and retries once, and concurrent calls are not coalesced. Upload pieces carry no Authorization header, retries are bounded, and a resumed upload reads the session status first. The base address is a setting, with four cloud presets.
2. The token comes in through `IGraphTokenSource.GetTokenAsync(sessionHandle)` / `GetNewTokenAsync(sessionHandle)`, named after C6 (`02:366`). C8 is a reflection test plus a source scan proving that no field holds a token and nothing persists. That is the G2 boundary.
3. The REQUIRED SECTION lists N1 to N11, each with a cell or a named limit. It covers: no body, a body that never ends or stalls, a hostile `Retry-After`, a looping or foreign `nextLink`, a 401 storm, a throttle that never clears, a hostile upload session, bad caller input, a seeded random run, and the deny-list's own limit.
4. Every behaviour bound is a Question with its default, its alternative and its cost. Every Graph behaviour in a test is marked as the kit's assumption. E3.3 and OXPD2-16 stay open.

## What I measured, and how
- Origin, by `gh api -X GET` under the project GH_CONFIG_DIR at 09:20:41. main is `c56f3f3b` (46 files). The branches are b1764, b1786 `9fe53569`, b1787, b1788 `ec75619e` and b1789 `bf1a4a24`. PR 3 is open (b1786); PRs 1 and 2 are merged. There is no `b1825` ref. push permission reads true.
- main's build files by GET: slnx (11 lines, sha256 `b5abfa4d...`), Directory.Packages.props (4 PackageVersion lines), Directory.Build.props, global.json, .editorconfig, ci.yml (199 lines, sha256 unchanged from wave 1) and test_pipeline_controls.py. I also read the Logging public API with its line numbers: `SuiteLoggerFactory.cs:18`, `LogScanner.cs:57`, `LogScanResult.cs:24`, `:33`.
- main's hosted run, from job logs by GET: total 192, `Ran 53 tests`, `UNIT-TEST FLOOR: ran 53, floor 53`, `RULES: clean (46 files)`, `GUARD: clean (10 files)`.
- Design lines and report lines, printed by awk and grep. A quote checker confirmed all 33 quotes in the kit against their source lines (0 missing).
- gitleaks 8.30.1 with the workflow's options, run over probe C#/JSON files written in the lane's style (synthetic tokens, `example.test` addresses, a token-shaped value built at run time). rc 0, and rc 0 again under neutral names. The control returned rc 1.
- `place.py`, run on main's slnx and four synthetic slnx files, placed the lines at src 4 and tests 10 on main. On a second placement it printed REFUSED with rc 2, so the control fires.
- A lane-shaped dry run in my OWN scratch clone (made with `clone.py ... draft`, push URL `invalid://no-push`). The tree held the slnx lines, T2, T3 and two probe test files, staged and never committed. Results: `repo_rules.py` printed `RULES: clean (50 files)`; `unittest discover` printed `Ran 53 tests` and `OK`; `run_step.py` (the neutral scan) printed the planted-control line `25 of 25` and `no leaks found`, rc 0; `words.py` over the 58 added lines and the commit message printed `WORDS: clean (2 files)`.
- Jira `OXPD2-16`: one GET with my own in-process helper (status Backlog, 0 comments). Package cache: 64 entries. Lock folder: held by B1824's probe at 09:22. Panes: only `Datasec/OXPd2-X13`.
- No dotnet anywhere: no restore, no build, no test.

## Questions with defaults (all in the kit, each with its source line)
Q1 the token interface `IGraphTokenSource` (null means no new token) · Q2 one refresh and one retry per call, no coalescing · Q3 3 throttle retries, single wait capped at 30 s, total waits capped at 60 s, fallback 1 s doubling to 15 s, no jitter · Q4 the grammar of block R (ASCII delta seconds, or the fixed GMT date form only) · Q5 429/503 retried for every method · Q6 transport errors and timeouts retried for upload pieces only · Q7 100 pages, same-origin next links of at most 8192 characters, loop detection · Q8 4 MiB body bound, 100 s per attempt · Q9 10 MiB pieces (a multiple of 320 KiB), 5 retries per piece, status read before each retry, seekable stream, no token sent to the session address, no resume across a restart · Q10 base address as a setting with Commercial/GCC/GCC High/DoD presets (hosts RELAYED from A1:363) · Q11 logging through Serilog `ILogger` with six properties, by a project reference to Datasec.Suite.Logging · Q12 the kit's names · Q13 caching and queueing (R15) left out · Q14 no records, README untouched · Q15 180 and 140 minutes, pane Datasec/OXPd2-X14, G2 · Q16 a token is printable ASCII 0x21 to 0x7E.
**For Tuesday's eye at the stamp:** Q11 (library logging, plus a project reference to Logging) and Q5 (a POST retried on 503) are the two defaults with the most surface. Q1 shapes lane D's adapter.

## Where the lane plan or the commission does not match what I read
1. The lane plan's scope for A cites `03:266` for the app-modules order. `03:266` is the S2 CoreWCF line; the sentence is at `03:274`. The kit cites `03:274` only.
2. The lane plan says `b1789` puts Secrets after Server. The origin's `b1789` now (`bf1a4a24`) lists Core, Secrets, Server, which is ordinal order. The kit places lines against main as it stands, so nothing depends on this.
3. The newest heavy-job form is B1820's `heavy.py`: load under 7, a mkdir lock, a closed proxy. The wave-1 form kit (B1786) still names lockf and load under 24. The kit follows B1820. Because the proxy is closed, a restore that needs a package not in the cache FAILS. The kit makes that a STOP.
4. `<project>/CLAUDE.md:7` still says Fable. The kit cites the 2026-11-21 Opus word as RELAYED from the commission, plus C-4 and C-5. The 2026-11-21 word is not in CLARIFICATIONS (lane plan difference 8).

## Reading load
220680 bytes, measured with `wc -c` over the kit's 24 READ WHOLE files: the kit (92 kB), PCL, CLARIFICATIONS, the runbook, the six programs counted whole (only their headers are needed), 7 build files and 7 Logging files.

## Checks marked NEVER RUN in the kit (STOP-severity, not run on a real output)
The owned-paths property (4(a)) on a built tree · `heavy.py` for this lane · `clone.py` in mode seat · the hosted comparison `hosted.py` · the C8 source scan · any `dotnet` total (a total of 0 is a STOP).

## UNMEASURED
Every dotnet output (restore, lock files, build, test totals and names). Whether `NonValidated` keeps block R's rows R08, R23 and R25 unchanged. How Graph really shapes `Retry-After`, next links, upload ranges and upload hosts. Whether the 200 ms stall test holds on a slow Windows runner. The Windows leg in general. Whether `Serilog.Core.Logger.None` and `Task.Delay(TimeSpan, TimeProvider, CancellationToken)` compile as named (DERIVED from framework knowledge). What a panel user will accept as a wait.

## Not read
The design documents whole (only the cited lines); the NAS library (not needed: the lane ports nothing); Workpath source; any `Source_Documents/` file content (only `grep -r -l` counts); the B1789 form kit (it is lane B's form); B1824, B1821 and B1822 commissions; other seats' STATUS files; BACKLOG.md; OXPD2-1. I read the B1820 kit only at its TOOLS and HEAVY sections and its Step-1 lines.

## Outside-the-fences disclosure
- I made a scratch clone with B1820's `clone.py` in mode `draft` (no identity copied, push URL invalid). It read the checkout's local `core.sshCommand` in-process to fetch.
- In that clone I staged files (no commit) and ran `python3 -I build/repo_rules.py`, `python3 -I -m unittest discover -s build/tests` and `run_step.py`. These are Python only, with no dotnet. The commission allows a scratch clone of my own; I note the python test run here anyway.
- I used `cp -Rc` and `sed -i` on my own scratch files only.
- One Jira GET. Read-only `grep -r -l` counts over two `Source_Documents/` trees.
- No git write in any project tree, no message, no Jira or GitHub write.
