From Friday (laptop seat), Datasec / HPSM-POC. Replies and wraps go to friday-laptop-agent@agentmail.to.

# BRIEF B224 (SEAT D): HPSM-POC: make `HostedDemoSlowFirstLoginTests` deterministic (test only). ROW 1 (first; it blocked a deploy): `A_first_read_whose_retry_also_times_out_warns_once_after_exactly_one_retry` · ROW 2: the same class's two sibling reds (`A_start_whose_first_sql_login_outlasts_…`, `Only_a_first_login_that_timed_out_is_retried`)
**From:** Friday, @NOW@ 2026-10-12 (DRAFT by Friday's drafter; pins read 2026-10-11T18:56Z–18:58Z UTC; Friday re-pins at launch). **Seat:** Datasec/HPSM-POC-D, pane Datasec/HPSM-POC-D. The launcher picks the newest `Briefs/` file whose name contains `_SEAT-D_` (`Launch_Claude.command:106`, `:110`). The newest one now is `2026-10-11_B213_SEAT-D_…`, so this file is the newest once it is copied into `Briefs/`. **B224 is free:** `ls Briefs | grep -ci b224` → 0; `ls briefs_drafts | grep -ci b224` → 0; `ls .tools | grep -ci b224` → 0.
Report `Briefs/2026-10-12_B224_STATUS.md` (BLUF · FOUND · TESTED · HOW · NOT TESTED · PRIOR WORK · NEW WORDS · Records). Write it as a file in the project's records folder (`1_Project_Definition/Briefs/`, the project-root repo); do not commit records. Evidence goes in `Briefs/2026-10-12_B224_evidence/` (summaries only); kits and raw logs stay in `.tools/b224/`, and no scripts go in the records (B100). Last line exactly `READY FOR GATE: b224/slow-first-login-deterministic <sha>` (the sha read by `ls-remote` after your last push), or `STOPPED: NEEDS FRIDAY` and ONE question.
**Tier 2** (through-code gate). Test code only: no product behaviour changes. A QA gate follows, and Friday opens the PR. **Nothing is deployed in this brief.**

**Premise key:** `(ls-remote HH:MM:SSZ)` = read by the drafter with that verb at that time · `(git <verb>)` = a read verb on `2_Project_Files` with `--no-optional-locks` · `(read: file:line)` = quoted from that file at `598a91a` · **UNMEASURED** = not established by the drafter; the reason and the instrument that closes it are given. Re-check every premise at your start. A wrong one is a finding. A moved pin is a STOP unless a rule below covers it.

## AUTHORITY
- Friday's order. Main `ci` run `38148442673` attempt 1 went red on this class and **stopped a hosted deploy** (B221 Q-B221-1, read: `2026-10-12_B221_STATUS.md:18`; Friday's note 2026-10-12 01:58 / 02:09: "On a second red: no deploy; the flake fix seat first"). A red `ci` on main blocks the deploy lane.
- `BACKLOG.md:39-43` (root checkout, uncommitted; the row is on `records/b221`): "the test's owner (B192/B195 lane) must find the cause before any bound changes". **This brief is that owner's work: cause first, then a deterministic test. No Kam ruling is involved; it is test hygiene, and the test must keep catching what it was written to catch (Rules below).**

## PRIOR WORK (read these first; cite each in your STATUS PRIOR WORK)
- **The test and its helper:** `api/tests/HpsmPoc.Api.Tests/Assessment/HostedDemoRobustnessTests.cs:362-641` (class `HostedDemoSlowFirstLoginTests`, B192 Task 2 / B195 item 6), last changed by `a50b22d` (B195, #133); before that `5a93aa3` (B192, #132), `6f6bc96` (B152), `e804ebb` (B74) (`git log --oneline 598a91a -- <file>`). `api/tests/HpsmPoc.Api.Tests/Support/StallingTcpProxy.cs` (106 lines), used ONLY by this class (`git grep -n StallingTcpProxy 598a91a -- api` → :398, :437, :497, :525 and its own file).
- **The code under test (NOT yours):** `api/src/HpsmPoc.Api/HostedDemo/HostedDemoStartup.cs` (`SeedAsync` `:70-117`, `LookForCompleteSeedAsync` `:121-135`, `WarnIfReadersWouldBlockAsync` `:148-170`, `FirstLoginTimedOut` `:185-187`); `api/src/HpsmPoc.Modules.Assessment/Showcase/ShowcaseSeeder.cs:301-306` (`CompleteSeedInPlaceAsync`); `ShowcaseSeedLock.cs:236` (`ReadCommittedSnapshotAsync`); `AssessmentModule.cs:101` (`EnableRetryOnFailure()`).
- **Records:** `Briefs/2026-10-12_B221_STATUS.md:18` (the red, verbatim), `:172` (deferred to BACKLOG); `.tools/b221/ci-failed-test.txt` (the full stack, quoted below); `BACKLOG.md:38-43` ("Follow-ups from B221"); `Briefs/2026-10-11_B213_STATUS.md:102` (the `Only_a_first_login…` load red); `Briefs/2026-10-12_B222_SEAT-G_records-catchup-1011.md:59-62`, `:66` (the two flake rows and the Jira filing). Friday's notes `0_Brain/daily_friday/2026-10-11.md` 14:09 / 14:16 and `2026-10-12.md` 01:58 / 02:09 / 02:40 (Friday's copies; quoted in the table).
- **Sibling flake fixed the same way:** B213 Row 1 (`RequestTimingLogTests` bounds; brief `Briefs/2026-10-11_B213_SEAT-D_…`, STATUS `2026-10-11_B213_STATUS.md`, gate B218, merged as `da58da9` #140). Mirror its discipline: cause measured, no retry/skip, mutants red.
- **Jira (B222 is filing now):** at drafting, `project = HPSMPOC AND text ~ "HostedDemoSlowFirstLogin"` = 0 and `… "HostedDemoSlowFirstLoginTests"` = 0; `… "Only_a_first_login_that_timed_out_is_retried"` = 1, HPSMPOC-207 (the start-up retry ticket, which names that test as a guard) (read: B222 brief `:66`, Friday's search). B222 (records seat G) is filing ONE ticket per flake, linked to each other and to HPSMPOC-207. **At your start, run the read-only board search `project = HPSMPOC AND text ~ "HostedDemoSlowFirstLoginTests"` and quote the key(s) and count. Do NOT file a ticket, even if the search is still 0**: then say "B222's ticket not yet filed at <time>" in PRIOR WORK and carry on; Friday links it.

## PINS (read by the drafter; instrument inline)
| What | Value | Instrument |
|---|---|---|
| `main` | `598a91ae035f28100e04fca6d19bcd19bdedcc8d` (#142 "B219: the hosted demo reset alone waits 90 s in the BFF"); tree `bf26f63bb191233d09766941b9148d3797837869` (= gate B220's merged tree); parents in order `6ba2ec0` (#141 B215), `da58da9` (#140 B213), `4229be3` (#139 B208) | `git ls-remote origin refs/heads/main` (ls-remote 18:56:49Z UTC) = the brief's expected `598a91a…`; `git log -1 --format='%H %T %s' 598a91a`; `git log --oneline -8 598a91a` |
| `598a91a` in `2_Project_Files`' object store | present (`cat-file -t` → commit) | (git cat-file) |
| Other branches | `b215/demo-alias-headings-and-pdf` = `1da119f6…` (merged as squash `6ba2ec0`); no `b22*` branch | `ls-remote origin 'refs/heads/b22*' 'refs/heads/b215*'` (18:56:49Z) |
| `.tools/.git-lock` | absent (free). Lock script: `.tools/b213/lock.sh` | `ls` (18:58Z) |
| Test file at `598a91a` | 641 lines | `git grep -c "" 598a91a -- <file>` |

**At your start, re-read main** (`ls-remote`). If it is `598a91a`, proceed. If it moved, read `git diff --name-only 598a91a <new>`. If none of them is under `api/tests/HpsmPoc.Api.Tests/Assessment/HostedDemoRobustnessTests.cs`, `api/tests/HpsmPoc.Api.Tests/Support/**`, `api/src/HpsmPoc.Api/HostedDemo/**`, `api/src/HpsmPoc.Api/Program.cs`, `api/src/HpsmPoc.Modules.Assessment/{Showcase,HostedDemo}/**`, `AssessmentModule.cs`, `.github/workflows/ci.yml`, base on `598a91a` anyway and report a read-only `git merge-tree --write-tree <new main> <your tip>` in BLUF. Otherwise **STOP**.

## THE OBSERVED FAILURES (re-quote each from its log in FOUND)
| # | Test (class `HostedDemoSlowFirstLoginTests`) | Where | Instrument | Quoted |
|---|---|---|---|---|
| 1 | `A_first_read_whose_retry_also_times_out_warns_once_after_exactly_one_retry` (`:484`) | main push `598a91a`, run `38148442673` attempt 1, job `api on SQL Server (api-assessment)`, 1/627; attempt 2 green on every job (Friday's note 2026-10-12 02:09) | `.tools/b221/ci-failed-test.txt` (re-read with `friday_as.sh datasec gh run view 38148442673 --attempt 1 --log-failed` if Friday gives you that; otherwise the file) | `Failed … 00:00:17.8239997` · `SqlException : Connection Timeout Expired. … pre-login handshake acknowledgement … [Pre-Login] initialization=0; handshake=4999;` · `Win32Exception : Unknown error 258` · `at …ShowcaseSeeder.CompleteSeedInPlaceAsync … ShowcaseSeeder.cs:line 303` ← `FindCompleteSeedAsync … :line 320` ← `HostedDemoStartup.LookForCompleteSeedAsync … HostedDemoStartup.cs:line 128` ← `SeedAsync … :line 89` ← `Program.cs:line 87` ← test `:line 501` |
| 2 | `A_start_whose_first_sql_login_outlasts_Connect_Timeout_reads_the_snapshot_setting_on_one_retry_and_warns_nothing` (`:424`) | PR #135 `b200` `f18359b`, run `38106540702`, job `api on SQL Server (api-assessment)`, 1/571; attempt 2 green (Friday's note 2026-10-11 14:09, 14:16) | `gh run view 38106540702 --log-failed` (Friday's read) | `HostedDemoRobustnessTests.cs:444`, "the first read did not fail and retry: 3213=0 3214=0 3211=0" |
| 3 | `Only_a_first_login_that_timed_out_is_retried` (`:517`) | B213's local base load copy (c2-3), not CI | read: `B213_STATUS.md:102` | `HostedDemoRobustnessTests.cs:534`, `Expected: -2` `Actual: 258` |

**The second CI red the brief asked about is #2 (2026-10-11, PR #135): a DIFFERENT method of the same class, not a second red of #1.** UNMEASURED: whether #1 also failed elsewhere; close it by listing failed `ci` runs since 2026-10-09 for this class name, if Friday gives you read-only `gh`.

## THE TIMING ASSUMPTION (the drafter's reading from code; you measure it before you change anything)
**Row 1 (#1): two equal 5 s timers race, and a wall-clock window decides whether they meet.**
1. The proxy's stall is a **wall-clock window from the proxy's construction**: `_started = Stopwatch.GetTimestamp()` (`StallingTcpProxy.cs:21`) and `stall = n <= _stalled || Stopwatch.GetElapsedTime(_started) < _stallWindow` (`:60`). The test sets `stalled: 0`, `stallFor` 8 s and `stallWindow: ConnectTimeoutSeconds * 2.5` = **12.5 s** (`HostedDemoRobustnessTests.cs:497-498`), with `ConnectTimeoutSeconds = 5` (`:374`, applied at `:410`). The window does not start when the host makes its first connection. It starts before the host is even built (`:499-501`).
2. The start does this in order: the RCSI read, which fails after about 5 s, then ONE retry, which fails after about 5 s and warns 3213 (`HostedDemoStartup.cs:151-168`). Then the look runs (`:89` → `:128`). So **the look opens its connection at about a + 10 s**, where *a* is the delay from the proxy's construction to the first connection (host build + DI, UNMEASURED). If a < 2.5 s, the look's connection falls inside the 12.5 s window and is stalled too. The test's own summary says a third connection "would still be stalled" (`:481-482`), so the look normally meets the stall.
3. A stalled look then races two 5 s timers. One is `look.CancelAfter(LookWait)`, where `LookWait` = 5 s (`HostedDemoStartup.cs:52`, `:125`). Its `OperationCanceledException` is caught at `:130`, which warns 3211 and falls through to the seed lock, whose connection at about a + 15 s is forwarded, so the test passes (`:504-505` do not assert 3211). The other is SqlClient's `Connect Timeout` = 5 s (test `:410`). Its `SqlException` (handshake=4999 < 5000) is **not** caught at `:130`, escapes `:128` and fails the start: **that is red #1**. Which timer fires first depends on thread-pool scheduling, so a loaded 2-vCPU runner can flip it. **Hosted does not have this race:** its Connect Timeout is 30 s (`:373`, C-77) against the 5 s LookWait. The race appears only because the test sets the two to the same 5 s.
- **UNMEASURED, and what closes it:** *a* and the accept time of each proxy connection relative to `_started` (add a timestamped accept log in your measuring copy, not on your branch); how often each timer wins, alone and under load; whether `EnableRetryOnFailure()` (`AssessmentModule.cs:101`) re-runs the look's query.

**Row 2 (#2, #3), the drafter's guesses only:**
- #2: `stalled: 1` stalls the **first accepted** connection (`StallingTcpProxy.cs:60`). If the pool's background minimum fill (`HostedDemoStartup.cs:140-142`, `SqlServerPool`) or any other open takes accept #1 before the RCSI read's own login, the read gets a forwarded connection, does not fail, and 3214 = 0. That fits "3213=0 3214=0 3211=0". It is ordering by arrival, not by caller. UNMEASURED.
- #3: `Connect Timeout=1` against a never-answering socket (`:525-526`). Under load SqlClient's timer can expire in the pre-login phase and report `Number` 258 (a Win32 wait timeout) instead of -2. `:534` asserts -2 exactly. UNMEASURED.
- **Possible product finding: report it, do not fix it.** #1's escaping exception is a pre-login timeout carrying `Win32Exception 258`. `FirstLoginTimedOut` accepts only `SqlException { Number: -2 }` or the pool wait (`HostedDemoStartup.cs:185-187`). **Measure the `Number` of #1's and #3's exceptions.** If a real first-login timeout can arrive as `Number` 258, hosted's RCSI read would not retry it (it would warn 3213). That is a product question about HPSMPOC-207's guard. Production code is not yours, so put it in BLUF as `PRODUCT QUESTION` with file:line and evidence, and keep going on the test.

## RULES FOR THE FIX (all of them)
1. **Deterministic, not luckier.** The verdict must not depend on runner speed. No retry, no skip, no `Skip=`, no `[Trait]` / filter exclusion, no move out of the SQL Server leg (`ci.yml:247` runs `HpsmPoc.Api.Tests.Assessment.`), no re-run loop, no blanket widening of a timeout or window "to be safe".
2. **What #1 must keep proving (state it in BLUF in your words):** on a first read whose retry also meets a login that outlasts Connect Timeout, the start retries **exactly once** (3214 = 1), warns 3213 **exactly once**, and still starts, serving the seed already there ("already in this database; nothing was written"). The doc comment's mutant must stay red: **an unbounded retry warns nothing** (`:481-482`).
3. **Shapes to weigh (measured, not guessed; pick one, say why the others lose):**
   - (a) **event-gated stall instead of a wall-clock window.** The proxy stalls until the test opens it, and the test opens it on a signal from the start (e.g. the 3213 entry arriving in `LogCapture`, or the N-th accepted connection counted per phase). Then the look and the lock always meet a forwarded connection, and an unbounded retry still meets stalls until 3213, which it never writes;
   - (b) **separate the two 5 s timers.** Make the test's Connect Timeout differ from `LookWait` by a margin you measure, in the same direction as hosted (30 s vs 5 s), so the look's outcome is fixed whatever the scheduling. State the added test time, and show the window arithmetic still makes a 3rd RCSI attempt stall;
   - (c) a test seam the product **already** offers, such as a `lockWait` overload (`HostedDemoStartup.cs:70`). **`LookWait` is `internal static readonly` (`:52`) and there is no `TimeProvider`: adding an injectable clock or timer to product code is NOT yours.** If determinism needs one, **STOP: NEEDS FRIDAY** and name the seam with file:line.
   - For Row 2: #2 is stalled by **caller or phase, not arrival order**, or it asserts on what it actually proves. #3 is made deterministic, or (only if you show from SqlClient's source or measured runs that both numbers are a genuine "login timed out") asserts the set the guard accepts. **If that set is wider than the product's guard, it is the PRODUCT QUESTION above, not a test edit.**
4. **No weakening:** every `Assert` in the class keeps its meaning. If one is changed, quote it before and after in HOW with the reason, and prove with a mutant that the new form fails where the old one did.
5. **Production code is not yours** (PARTITION). If your measurement shows the product misbehaves (e.g. the look's `SqlException` escaping `:128` is reachable on hosted's 30 s), **STOP** with file:line evidence.

## THE WORK, in order
1. **FOUND, before any change, at `598a91a`:** re-quote the three failures. Confirm or refute each step of THE TIMING ASSUMPTION with file:line, and correct the drafter where wrong. Do the Jira search (PRIOR WORK).
2. **Measure at base** (a base worktree at `598a91a`, with an instrumented copy of the proxy in your measuring copy only): the class alone ×30 and under deliberate load ×10 (state the load, e.g. 3 concurrent copies of the Api suite, and the load average), **on your SQL Server 2025** (`@@VERSION` in the log, password masked; the SQL Server branches are the ones that race, and SQLite returns early at `:488-494`). Also run once on SQLite. Report per test: the accept times relative to `_started`, which timer won the look, and the exception `Number`s. **If load reproduces a red at base, keep that log: it is the flake's red.**
3. **Change the test** per the rules (Row 1 first, as its own commit(s), pushed first, so Friday can take Row 1 alone; then Row 2).
4. **Red-proof** in a mutant worktree, never on your branch. Each mutant must go red under the NEW test, then be restored EQUAL by `git diff --quiet` plus a byte compare. Mutants are made in product code in the mutant worktree only:
   - **W1 unbounded retry:** `attempt == 1 &&` removed from `HostedDemoStartup.cs:159` → #1 red (3213 = 0). **This is the brief's "warn-once broken" proof.**
   - **W2 no retry:** the `:159` catch never matches (e.g. `false &&`) → #1 red (3214 = 0) and #2 red.
   - **W3 warn twice:** `ReadCommittedSnapshotUnknown` logged twice at `:166` → #1 red (3213 = 2).
   - **W4 retry warns:** `:161` also logs 3213 → #2 red.
   - **W5 guard too wide / too narrow:** the `Source` clause dropped, and separately the `Number: -2` clause dropped, at `:186-187` → #3 red for each.
   - And the reverse proof: under **base timing at your new test's settings**, the race is gone. Show 0 failures in ×30 alone and ×10 under the SAME load as item 2.
5. **Green after:** the class ×30 alone and ×10 under the same load, on SQL Server and once on SQLite: **0 failures**. Then the full Api suite once on each provider. If any run is red, it is a finding: report it, never re-run it away.

## BASE
- Branch **`b224/slow-first-login-deterministic`** from **`598a91ae035f28100e04fca6d19bcd19bdedcc8d`**.
- Worktree `.tools/wt-b224`; a base worktree `.tools/wt-b224-base` at `598a91a`; a mutant worktree `.tools/wt-b224-mut`; scratch `.tools/b224/`.
- Every code-repo ref write (fetch, worktree add, branch create, commit, push) runs under the shared lock `.tools/.git-lock`. Copy `.tools/b213/lock.sh` to `.tools/b224/`, and never remove another seat's lock. In `2_Project_Files` itself, use read git verbs only, with `--no-optional-locks`.
- Push a NEW branch: `git push origin b224/slow-first-login-deterministic`. No `--force`, no `--force-with-lease`, no `+refspec`; every later push is a fast-forward. Run `ls-remote` before and after each push and record the lines. A refused push → STOP.
- Read-only, in your scratch: `git merge-tree --write-tree <your tip> <B223's head>` once B223 has pushed (`ls-remote 'refs/heads/b223/*'`). State the exit code and whether any path is shared; expected 0 shared (PARTITION).

## PORTS: 6970–6979 only
The drafter checked at 2026-10-11T18:58:05Z UTC:
- `lsof -nP -iTCP:6970-6979` → 0 lines;
- `lsof -nP -iTCP -sTCP:LISTEN`: no listener on any 69xx port;
- `docker ps -a` ports: no container bound in 69xx;
- `grep -hoE '\b697[0-9]\b'` over every HPSM-POC `Briefs/*.md` and Friday's `briefs_drafts/*.md` → 0 hits.

Plan: **6970** SQL Server 2025 `b224-mssql` (CI's image by digest, as B213 / B211); **6971** Azurite `b224-azurite` (CI digest), only if the full suite needs it; 6972–6979 spare. **B223 is not in this range:** B223's ports are whatever its brief names, and none of them is yours.
**Re-check with `lsof` before every bind**, and state the checks in STATUS. Containers `b224-*` only (new). Secrets go in `4_Credentials/b224-*.env`, read by name only. Never start, stop, reuse or remove any other seat's container (`b2[0-2][0-9]-*`, `b223-*`).

## PARTITION (from both sides)
- **Yours (B224):**
  - `api/tests/HpsmPoc.Api.Tests/Assessment/HostedDemoRobustnessTests.cs`, **the `HostedDemoSlowFirstLoginTests` class only (`:362-641` at base)**. The file's other classes (`:1-360`) are not changed.
  - `api/tests/HpsmPoc.Api.Tests/Support/StallingTcpProxy.cs` (its only user is this class), and a new test-only helper beside it if needed.
- **NOT yours: B223 (parallel seat, Demo name-check fix round: the web PDF / name check + `getAssessmentResult`).** These are the files B215 / B220 touched (read: `git diff --name-only 4229be3 1da119f` = B215's 22 files; B220 STATUS `:41`, `:48`, `:58` N-5, `:68`, `:79`):
  - `api/src/HpsmPoc.Modules.Assessment/Endpoints/ReportingEndpoints.cs` (`DemoCopyNamesCustomer` `:491`, the gate `:463`);
  - `api/src/HpsmPoc.Modules.Assessment/Endpoints/AssessmentEndpoints.cs` (`Result`, `getAssessmentResult` mapped at `AssessmentModule.cs:215`);
  - `api/src/HpsmPoc.Modules.Assessment/Narrative/NarrativeReview.cs`, `Pdf/**`, `CustomerNameAtRender.cs`;
  - `api/tests/HpsmPoc.Api.Tests/Assessment/B215DemoAliasPdfTests.cs`, and any B223 test file;
  - `web/src/components/customer/**`, `web/src/components/screens/**`, `web/src/components/shell/**`, `web/e2e/**`, `web/src/lib/**`, `web/src/server/bff.ts` + `bff.timing.test.ts` (B219), and the contract copies / `openapi.merged.json` / `schema.gen.ts`;
  - B223's ports, containers, `.tools/b223*` and `.tools/wt-b223*`.
  - **Prove it:** `git diff --name-only 598a91a..<final>` lists only your two (or three) files; grep it for `Endpoints/|web/|Narrative|Pdf|contract` → 0.
- **Not yours either:** every file under `api/src/**` (including `HostedDemoStartup.cs`, `ShowcaseSeeder.cs`, `ShowcaseSeedLock.cs`, `AssessmentModule.cs`, `Program.cs`, `SqlServerPool`), `Migrations/**`, `.github/workflows/**`, `appsettings*.json`, `Support/LogCapture.cs` and every other shared `Support/**` file except `StallingTcpProxy.cs` (if you need a hook there, say why and keep it additive), and every other seat's worktree, kit, container or port, including `.tools/wt-b213*` and `b213-*` (leave them).

## SUITES AND REPORT
- The class on your SQL Server 2025 (items 2, 5) and the full Api suite on SQLite and on SQL Server once each (all 5 projects, 0 skipped).
- gitleaks over `598a91a..<final>`. A raw scan of the added lines with Python (not BSD grep, B205 N-4).
- Known flakes elsewhere (HPSMPOC-247 `ImportRobustnessTests.R2_2`; `NarrativePipelineTests.B170_…`; `RequestTimingLogTests`): if one goes red, re-run it alone and report it. Never skip one.

## HOLDS (verbatim)
- No HP Restricted document (the executive deck, the financial model, anything HP marks Restricted) is given to ANY AI tool — Claude seats, subagents, the product's model, Ornith or the Spark — without HP's written approval (signed SOW §4.1.4(c)).
- Datasec only; no other client's names, tickets or paths.
- CodeQL policy: Push your branch only. Friday opens the PR and lands it once CodeQL and the checks are green; never push an unscanned commit to main. Never dismiss an alert.
- No deploy, no Azure, no setting change; nothing to HP or any human.
- Never delete; quarantine. **Never delete a file.**
- Never print a secret.
- Stop any process of yours by port + cwd (check its working directory first); never by name; never another seat's.
- No force-push of any kind, no branch delete, no history rewrite.
- Fixtures are synthetic; no real customer data.
- **Never edit a running script** (copy it, then edit the copy). **Your own worktrees only; never `gc`, `prune`, `worktree remove` or `reset` anything of another seat's** (or `2_Project_Files` itself).
- No Jira or BACKLOG write (B222 files the ticket; Friday links and closes). No re-run of a CI job to make it green.

## REPORT
`Briefs/2026-10-12_B224_STATUS.md`:
- **BLUF:** main at start and end; the property #1 protects, in your words; the CAUSE of each red (measured), with file:line; the shape chosen and why the others lose; W1–W5 results; the class result alone and under load on both providers; the Row-1-only sha; the Jira key found (or "not yet filed"); any `PRODUCT QUESTION`.
- **FOUND:** the three quoted failures; the timing assumption confirmed or corrected step by step; the measured accept-time and timer-winner tables at base.
- **TESTED:** a red-first log (the base race reproduced, or the reason it could not be); each mutant red, then restored EQUAL; suites with counts.
- **HOW:** commits, each with its files; every changed timeout, window or assert, before and after, and the measured number that justifies it.
- **NOT TESTED:** honestly. Every UNMEASURED names why and the instrument that would close it.
- **PRIOR WORK:** as listed above, file:line at `598a91a`; the Jira query, count and key.
- **NEW WORDS:** none expected (test code only); say "none" or list each.
- **Records:** containers left, worktrees, ports free at the end by `lsof`, the lock free.
- Last line exactly `READY FOR GATE: b224/slow-first-login-deterministic <sha>` (sha from `ls-remote` after your last push), or `STOPPED: NEEDS FRIDAY` and ONE question.

## UNMEASURED at draft time (why, and what closes each)
- **The cause of each of the three reds.** The drafter read code and logs and ran nothing. Closed by THE WORK items 1–2.
- **Delay *a* (proxy construction to first connection) and which 5 s timer wins the look.** Closed by an instrumented proxy copy in item 2.
- **Whether a first-login timeout can carry `Number` 258 in production SqlClient** (the guard accepts -2 only). Closed by item 2's exception census and SqlClient's source; it is a PRODUCT QUESTION if so.
- **Whether #1 also went red in another run** (no `gh` for the drafter). Closed by a read-only run list if Friday provides it.
- **The Jira key B222 files.** Closed by your start-of-brief board search.
- **Ports 6970–6979 free at your start; main unmoved; `.tools/.git-lock` free.** These were read at 18:56–18:58Z UTC only. Closed by your `lsof`, `ls-remote` and `ls` re-checks.
