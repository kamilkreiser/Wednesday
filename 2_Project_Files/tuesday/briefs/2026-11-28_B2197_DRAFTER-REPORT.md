STARTABLE: NO (the kit is complete and stampable: `stamp_check.py` exits 0 with 238 of 238 claims measured. It cannot START until its base exists: lane L1c (seat X94, gate B2195) has to LAND on `main` first, and the kit's L1c test REFUSES on today's `main` `d9f89115` by design. Once L1c lands it is startable after the stamp answers Q1 and Q3 in words.)

# B2197 (seat X100, lane L1 slice 1) drafter report: the OXPd 1.x authentication agent on the server

Read-only drafter (Opus) for Tuesday s337. Commission: `tuesday/briefs/2026-11-28_B2197-B2201_OXPD-WAVE2-KITS_COMMISSION.md`, section 1. First `date`: Sat 28 Nov 2026 02:51:46 AEDT; kit written about 03:05, sidecar written 03:14 (its first line holds the clock `date` printed in the writing process), this report from 03:14:47 AEDT. Outputs: the kit `2026-11-28_B2197_SEAT-X100_oxpd2-l1-agent-auth-slice1.md` (sha256 at 03:14:47 `c9b33ee7...`, 260 lines, about 106 KB, 9 stamp slots unfilled), its `.measured` (238 claim lines plus a clock line), and this report. Scratch: `fleet/state/s337/d2197/` (below `<d>`).

## BLUF
1. **The slice:** the smallest piece of lane L1 that lands on its own is the SERVER side of HP's authentication agent, the three SOAP operations the device calls (GetPrePromptResult, GetPostPromptResult, SignOutNotification), against L1c's committed description, with no client call, no HID, no route and no `Succeeded`. ONE new file `src/Datasec.Suite.Adapters.Oxpd1.Agents/Oxpd1AuthenticationAgent.cs` (`Oxpd1AuthenticationAgentEndpoint.AnswerAsync(Stream, contentType, ct)` plus the request, two answer types, a handler interface and a reply) and ONE new file `tests/Datasec.Suite.Adapters.Oxpd1.Agents.Tests/AuthenticationAgentTests.cs` (G01 to G09: 2 Facts, 7 Theories, 41 rows, 43 cases), nine mutants. No project file, lock file, package or slnx line moves.
2. **The design call that makes it land alone (D1, Q1 STOP-CLASS):** the landed Agents project has NO reference of any kind (its `.csproj` is 5 lines, `InternalsVisibleTo` only; its lock file lists no dependency; MEASURED). So the endpoint is transport-free: base class library only, a `Stream` in, status + content type + bytes out; the ASP.NET Core route is lane L3b's. Cost: the strict reader and the envelope writer are COPIED in form from `Oxpd1Soap.cs` (internal, not reachable). Alternatives (b) a `FrameworkReference` (csproj M, no lock change: DERIVED from a landed test project that has one and 0 `aspnetcore` lock lines) or (c) a `ProjectReference` to `Adapters.Oxpd1` (two lock files move).
3. **No `Succeeded` in slice 1 (D4, Q3 STOP-CLASS):** HP's `AuthenticationInfo` requires `authenticatedUserInfo` (`authenticationagent.xsd:16`); a `Succeeded` without it is schema-valid (`authenticationInfo` minOccurs 0, `:159`, `:202`) but what a device does with it is UNMEASURED and could sign a user in as nobody. Slice 2 adds it.
4. **Never beside L1x? It MAY run beside L1x.** Plan r2 line 87 lists L1 as never beside AZ-1X and L8 only ("L1, AZ-1X and L8 (one project, Slot A in order); L1x with L6 or OX-A"), lines 84-86 do not pair L1 with L1x either way, and the folders are disjoint (L1x: new files in `Adapters.Oxpd1/**` and its tests; this slice: the two Agents folders). This slice does not call L1x's class (no reference to that project). Slice 3, the client calls, needs L1x LANDED.
5. **Q-RUNNER: the counting runner provably counts an old-lock holder as slot 1; it never runs three heavy jobs.** Default in the kit: ADOPT (Stamp S8 `89223aca...`). Proof below.

## Q-RUNNER (the commission's one fact): does B2172's counting runner exclude jobs on the OLD single lock?
**Answer: yes, by counting them. The two schemes together never run more heavy jobs than `heavy-slots` says; never three.**
- **From source** (`fleet/state/s335/d2172/heavy.py`, sha256 `89223aca309c11b228f99460c5209167840b45483281eb3c05f7b7e94bca3e5d`, re-hashed tonight): `slot_dir(k)` returns `LOCK if k == 1` (line 79), and `LOCK = TOOLS + '/wave1-heavy.lock.d'`, the exact folder the canonical runner (`31adedc8...`, re-hashed) takes by `mkdir`. The counting branch lists free slots by `os.path.isdir(slot_dir(n))`, so a canonical holder makes slot 1 not free; the v2 job takes slot 2 or waits; `os.mkdir` is the atomic test both runners use, and a lost race is a `FileExistsError` that loops. With `heavy-slots` ABSENT the v2 code takes the `TODAY` branch, the canonical runner's code (one lock). Light-project locks (`wave1-proj-*.lock.d`) are a deliberate third job, but only when `heavy-light-projects` exists (absent at drafting, MEASURED by `ls`).
- **From a run** (`<d>/qrunner/prove.py`; output kept at `<d>/runs/qrunner.out`, 03:11:44 to 03:12:40 AEDT; a first identical run 02:55:17 to 02:56:13): each case under its own scratch lock root (`HEAVY_LOCK_ROOT`), load from a file, fake 4-second jobs writing start/end markers, a sampler counting running jobs every 0.05 s. The canonical runner was run as a copy changed on exactly the two lines B2172's own control changed (`LOCK` under `HEAVY_LOCK_ROOT`; `load1` from the file), the harness asserting each line occurs once before replacing it. Results: **A** canonical first then two v2 (`heavy-slots` 2): max running **2**; **B** two v2 first then canonical: **2**; **C** canonical, v2, canonical, v2: **2**; **D** `heavy-slots` absent, canonical then two v2: **1**; **control** v2 with slot 1 renamed `.d.1` (a mutant): **3** (the property failed as it must). Last line `Q-RUNNER PROOF: A 2 B 2 C 2 (each must be 2), D 1 (must be 1), control 3 (must be 3): AS REQUIRED`. No live lock, no project folder, no dotnet.
- **Not proved:** real dotnet load and the 120 s gap (the gap was 1 s by `HEAVY_TEST_GAP`); a runner killed by a signal while holding a slot (B2172 REPORT: the folder stays behind, the same as today). The kit's seat NEVER writes `heavy-slots` (B2172 ADOPTION item 2); with the file absent, adopting v2 changes only the process-group kill and the `ORPHAN` report.

## Facts re-measured (instrument named)
- **Origin** (`gh api -X GET`, 02:52:23 and 03:13:50 AEDT, `<d>/runs/origin-and-facts.out`): `main` `d9f89115333bbed2ade723e4c11d523b2a9cd079` (tree `aa53e949...`, PR 62); open PRs 0; `b2185/x94-oxpd1-contracts-l1c` at `f4aacb5e...` (behind main 1, ahead 1, merge base `cf224e1f`, 16 files: 12 A, 4 M, MEASURED by `compare`); `b2188/x97-l3a-host-composition` `ef1eb24d` (12 files, all Server and Server.Tests); `matching-refs/heads/b2197` 0 rows.
- **Main's tree:** tarball 762 files (= gate B2194's squash tree count). **Simulated BASE** (main plus L1c's 16 files, a scratch repository, NOT L1c's landing): 774 files, tree `58145d4f...`.
- **The Agents project at `d9f89115`** (`cat -n`): `AssemblyMarker.cs`; `.csproj` 5 lines, `InternalsVisibleTo Include="Datasec.Suite.Adapters.Oxpd1.Agents.Tests"` (line 3) and nothing else; lock file no dependency; the test project references the Agents project (line 7) and `xunit.v3` (line 10); `SkeletonTests.cs` ONE `[Fact]`. Both projects in `Datasec.Suite.slnx` (lines 4, 31). The Server project references neither (`Server.csproj` lines 3 to 5): the release guards' counts do not move.
- **L1c's authentication-agent description** (`cat -n` at `f4aacb5e`): three operations; each output `wsaw:Action` EQUAL to its input action (`authenticationagent.wsdl:47/49, 61/63, 77/79`), which fixes the answer's `Action` header; binding `soapAction` lines 26, 36, 46; schema imports `common.xsd` and `securitydomain.xsd` (lines 5, 6), both committed. `inputs.sha256` lines naming the folder: 3 at `f4aacb5e`, 0 at `d9f89115` (the L1c test's count and control).
- **HP's own time-out note** (`authentication.xsd:80` to `:83` at `d9f89115`): no retries of pre/post-prompt, "short timeouts (1-5 seconds) are recommended"; sign-out "may specify additional retry parameters". Both are named limits (R12, R14) and FOR-TUESDAY lines for L3b.
- **Schema reading by libxml** (`/usr/bin/xmllint --schema`, libxml 20913, `<d>/xsdcheck/*.out`): seven request and answer bodies of the kit's shapes `validates`; `resultCode` `Maybe`, a post-prompt `Continued`, language `en-us`, a 31-character context id each `fails to validate`. .NET's validator was NOT run (no dotnet).
- **`words.py` and a three-digit seat id** (`<d>/runs/words-x100-*.out`): a bare `X100` is NOT counted (`WORDS: clean`), `SEAT-X100` is. The kit adds a `grep -c -i x100` beside the B-number count at Step 6 (a).
- **Machine at 02:56:20:** load `7.44 7.01 7.60`; slot-1 lock held by L1c's gate reader (`G2195 gate reader (Tuesday s337) | pid 17577`); panes `tuesday`, `Datasec/OXPd2-X99` and four unnamed.

## What the drafter ran (all in scratch, none dotnet, no lock)
`gh api -X GET` (origin, two tarballs, compares); a scratch git repository `<d>/sim` (init, add, commit, a second index by `read-tree`; all writes inside `<d>`); `checks_l1a.py` over the BASE index (`CHECKS: 3 of 9 PASS`, 9 controls FIRED) and the prototype staged (`CHECKS: 9 of 9 PASS`; the first staged run FAILED check 4 on two non-ASCII characters the editor wrote for `￾`/`￿`: the prototype now holds escapes, and the kit tells the seat to write every non-ASCII character as an escape); `words.py --control` (`13 of 13`) and over the added lines and the message (`WORDS: clean (2 files)`); `mutants_c3.py --list` (`LIST: 9 mutants, 1 suites, 9 cells`, rc 0; a bad row `LIST REFUSED: rows mBad`, rc 1) and `apply`/`undo` of all nine over the prototype (`equal True` 9 of 9); `gitleaks dir` (planted control rc 1, moved to `<d>/_quarantine/`; the two prototype files, the message, the checks tool and the rows file rc 0, `no leaks found`); `xmllint`; the Q-RUNNER proof; `stamp_check.py --init`, then every TODO filled by `<d>/fill_measured.py` (a `grep -c -F` of each literal over the drafter's sources and runs, first hit named) and 41 lines by hand (`<d>/manual.py`), then `stamp_check.py` rc 0.

## CHAIN INPUTS (DRAFTER_RULES "MEASURED LITERALS" item 4)
| Step | Inputs | Produced by or present at |
|---|---|---|
| 0 | the kit, Stamp S2 (BASE, L1c's sha), S3, S4 (Q1, Q3 in words), S8 (runner sha) | Tuesday's stamp |
| 1 | `<src>` 8 files; `<repo>` local values; origin; BASE's push run | `<d>/seat-tools/` (exists, hashes in THE TOOLS); `<repo>`; GitHub (after L1c lands) |
| 2 | BASE's files; L1c's three description files | Step 1's clone |
| 3 | THE CODE, THE NEW CELLS; restored and built clone | the kit; Step 1 |
| 4 | pinned tree; `mutants_c3.py`; rows file (written in Step 4 before its run) | Step 3; Step 1; Step 4 |
| 5 | green tree, mutants undone | Step 4 |
| 6 | staged tree; `checks_l1a.py`, `words.py`, `commit-message.txt` | Step 5; Step 1 |
| 7 | the commit; `origin/main`; `run_step.py`, `hosted3.py` | Step 7 (a); the fetch; Step 1 |

## D-decisions (each Tuesday's default as coordinator, each a Q)
D1 transport-free endpoint, no project file change (Q1 STOP-CLASS). D2 hand-written SOAP 1.2, no package (K9). D3 answer in the request's addressing version; none when none; both refused (Q2). D4 no `Succeeded` (Q3 STOP-CLASS). D5 SOAP 1.2 `mustUnderstand` honoured; `ReplyTo`/`To` read for nothing; fault statuses 400/500 (Q4, Q5). D6 every refusal before the handler with one of nine fixed texts; handler failure a `Receiver` fault, cancellation passes through. D7 no id in any `ToString`. D8 cell prefix `G`.

## Questions for Tuesday (each with a default; also in the kit)
- **Q1 (STOP-CLASS)** transport: default **a** transport-free, no csproj change. Alt b FrameworkReference; alt c ProjectReference.
- **Q2** answer addressing: default the request's version.
- **Q3 (STOP-CLASS)** no `Succeeded` in slice 1: default **a** yes (none).
- **Q4** `mustUnderstand` honoured: default yes.
- **Q5** fault statuses 400 / 500 and fixed texts: default yes.
- **Q6** bounds 64 KiB, 64 levels: default yes.
- **Q7** one G1 gate, Opus, READY +240 / push +210, pane `Datasec/OXPd2-X100`, launched after L1c lands, beside L1x / L3a / app lanes / AZ-1 / records as S3 allows, never beside AZ-1X or L8.
- **Q8** names `.tools/b2197-x100`, `b2197/x100-l1-agent-auth`, `2026-11-28_B2197_X100_*`.
- **Q9 (Q-RUNNER)** default ADOPT the counting runner `89223aca...`; this seat never writes `heavy-slots`.
- **For Tuesday, not in the kit:** who writes `<project>/.tools/heavy-slots` = 2 and when. Until someone does, every runner (old or new) runs one heavy job at a time, and last night's 250-poll wait will recur.

## Next slices of lane L1 (named, NOT drafted)
1. **Slice 2:** `Succeeded` with HP's `authenticationInfo` / `authenticatedUserInfo` (securitydomain types; which Microsoft claims fill which field; never a Graph token in `opaqueAuthenticationToken` without a decision). G1.
2. **Slice 3:** the client calls `ReserveAuthenticationContext` / `ReleaseAuthenticationContext` through L1x's `Oxpd1ContextCaller` (needs L1x LANDED; a `ProjectReference` Agents -> `Adapters.Oxpd1`, two lock files move: the first L1 slice that touches project files).
3. **Slice 4:** HP's `HidReportEvent` callback endpoint (L1c's `accessoriesCallback.wsdl:31`) and `HidOpen` / `HidStartReading` through L1x; overlaps L8's card path, so it may fold into L8.
4. **Not L1's:** the prompt-page target is a registration value (HP `authentication.xsd:95` `userPromptTarget`) plus a panel page (L4); every route, TLS and the time bound on the handler are L3b's; the caller credential is AZ-1X's; the device run is L1d.
Plan r2 sized L1 at about 3 lock-days; slice 1 is about 1 (ESTIMATE: two files, 43 cases, nine mutant builds of one small test project).

## UNMEASURED
- How an M577 frames the three calls (content type, WS-Addressing version, headers, time-outs), and whether it accepts each fault status: UNMEASURED until L1d.
- Whether .NET's `XmlSchemaSet` reads L1c's schema exactly as libxml does (G01 is the check): UNMEASURED by the drafter.
- The W3C SOAP 1.2 media type and the fault-to-status table (D5, D6): written from the drafter's knowledge, UNMEASURED (no fetch was allowed); the kit says so.
- Whether the prototype compiles with 0 warnings (xUnit analyzers, nullable): NEVER RUN; the kit hands the seat the warning rule.
- BASE's totals after L1c (and after L3a, if it lands first): Stamp S2.
- `dotnet --version` of the project toolchain: RELAYED from kit B2186 (no dotnet program run).

## Outside-the-fences disclosure
- Wrote only: the kit, its `.measured`, this report, and scratch under `fleet/state/s337/d2197/`. No write in the OXPd project, Jira, GitHub, Azure, cards or mail. No lock taken; no dotnet job; no az; no `cd`; nothing deleted (the gitleaks control token was moved to `<d>/_quarantine/`).
- Git write verbs ran ONLY in `<d>/sim` (a scratch repository inside the Tuesday tree); one attempt to run `git stash list` there and one `git init` with an unexpanded variable were refused by the no-cd hook before running; both were re-run with literal paths or dropped.
- Read in the project: `<project>/CLAUDE.md` (hashed and lines 7, 25, 55, 56, 61, 82, 83 by `awk`), `BACKLOG.md` and `CLARIFICATIONS.md` (hashed only), `ls` of `<project>/.tools/`, the slot-1 `owner.txt` (read only), `ls` of `<project>/1_Project_Definition/Briefs/`. Never read: `Source_Documents/`, `4_Credentials/` beyond `GH_CONFIG_DIR`, key folders, the NAS library.
- Tuesday-tree reads: the commission, DRAFTER_RULES, the weekend commission, kit B2186 whole (as the form) and the headings of B2188, plan r2 whole, B2154 whole, B2172 commission and REPORT, gate B2194's `landing.txt`, two lines of the 11-28 daily note. Card ids: none read.
