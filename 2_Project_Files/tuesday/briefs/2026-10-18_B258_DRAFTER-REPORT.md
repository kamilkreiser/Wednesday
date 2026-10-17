# DRAFTER REPORT: HPSM-POC B258 (build round 1 of 2 from the B257 tickets), 2026-10-18 06:37-06:46 AEDT

I am a read-only drafter for Tuesday. I launched nothing and sent nothing. I made no Jira, git or gh writes and no fetch, ran no `az`, and sent no HTTP to any app host, the hosted site or production. The only writes are these two files in `tuesday/briefs/`.

## 1. Files
- **Brief:** `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-18_B258_SEAT-H3_hpsmpoc-bff-imports-zstd-census.md`. Its step 0 copies it into the project's `Briefs/`.
- **STATUS:** `/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-10-18_B258_STATUS.md`. Its last line is `READY FOR GATE: b258/bff-imports-zstd-census @ <sha40>`, or `STOPPED: NEEDS TUESDAY` + ONE question. **Arm the STATUS watcher on that path.**
- **Number:** B258. Across both `tuesday/briefs/` and the project's `1_Project_Definition/Briefs/`, the highest HPSM-POC number is B257 (`ls` of both, 06:37). The B169-B171 files dated 10-17/10-18 are MPS numbering.

## 2. Launch
`bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/HPSM-POC-H3 "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-18_B258_SEAT-H3_hpsmpoc-bff-imports-zstd-census.md'"`
(`cockpit.sh status` 06:4x: only `tuesday`, `QA/Vision-gate23` and `fleet-monitor` were live; no HPSM-POC pane.)

## 3. The 12 tickets, classified (Jira GET 06:38: every one Backlog, 0 comments, 0 links; every cite re-read at code main `787d159`)
| Ticket | Class | Where | Tier |
|---|---|---|---|
| -260 G01 BFF backslash file name not counted | **build now** (B258 #1) | `formGate.ts:93`, `:122-129` hold | 1 |
| -265 guard 403/413 keep-alive + `\b` | **build now** (B258 #2) | `guard.ts:18`, `bff.ts:393` hold | 1 |
| -262 retry exhaustion uncaught in phase 3 | **build now** (B258 #3) | `ImportEndpoints.cs:189` holds | 1 (data) |
| -261 final-save guard test (kills M251-3) | **build now** (B258 #4) | `:187`; test file exists | 2 |
| -264 skippable zstd frame refused + fixture-a | **build now** (B258 #5), drafter's shape pick | `deploy-package.py:456-458` hold; test `def` at `:531` (ticket says `:532`, its docstring) | 1 (deploy tooling) |
| -266 three `$` literals outside the census | **build now** (B258 #6, last, first to drop) | `:940`, `:217`, `:307` hold | 2 |
| -263 phase-2 stores after the sweep failed | **needs a decision**: CARD candidate | the ticket calls it the coordinator's design choice | - |
| -269 local `.tools/dotnet` 10.0.401/10.0.12 | **needs a decision** (Tuesday): CARD candidate; reproducible (`--list-sdks` 10.0.401, AspNetCore 10.0.12, 06:41) | shared SDK swap + download | - |
| -270 Pkcs guard's unbounded output reads | build, **round 2** | `PkcsInPackageTests.cs:66`, `:71`, `:76` hold | 2 |
| -272 Pkcs guard messages | build, **round 2** | `:18-22`, `:43`, `:45` hold | 2 |
| -271 floating CI SDK vs the Pkcs pin | **split**: owner + cadence = CARD candidate; the optional early-warning test = round 2 | `ci.yml:86`, `:125`, `:136`; pin at `Assessment.csproj:30` | 2 |
| -273 `__EFMigrationsLock` CI flake | build, **round 2** (SQL Server under load; heavy) | `HostedDemoRobustnessTests.cs:46`, `:79`; `AssessmentModule.cs:183` hold | 2 |

None of the 12 is "not reproducible at main". `72073da..787d159` touches only the two `.csproj` files and `PkcsInPackageTests.cs` (`git diff --name-only`, 06:45), so every B252 cite holds at `787d159`.

## 4. Why a split, and what round 2 holds
B251 built 6 items in about 1.5 h (06:2x-07:xx; `B251_STATUS.md:3`). Ten buildable items in one seat would double that, and round 2 is a different stack. **Round 2 (suggested B259, not minted)** holds:
- -270, -272 and -271's early-warning test: one file, one logical path.
- -273: the SQL Server shard; it needs load headroom.
- -269 first, if Tuesday rules the SDK swap: m1 needs SDK ≥ 10.0.402 to show the tie.

## 5. Excluded, and why
- **-267:** `needs-kam` (import words before imports are ever on; C-108).
- **-268:** `needs-kam` (hosted runtime; card `hpsmpoc-hosted-runtime-10013-1017` is **OPEN**, `ruled_choice` None at 06:40).

## 6. Card candidates for Tuesday (the tickets' words, no card text)
1. **-263:** after the sweep has failed the run, the upload either stores no more files, or the 3304 count is re-read. The ticket calls it the coordinator's design choice. It is Tuesday's to rule, not Kam's: no words, imports off on hosted.
2. **-269:** swap the shared `.tools/dotnet` to SDK ≥ 10.0.402 / runtime ≥ 10.0.13 (a download, quarantine the old one, and no HPSM-POC seat running during the swap). It is Tuesday's to rule. It gates round 2's m1 proof.
3. **-271:** an owner (a role) and a written cadence for the Pkcs pin, or retire it with the runtime move (tied to the open runtime card).
4. **-264 shape (pre-launch, optional):** the brief picks "skip skippable frames" (no new words; both readers passed row h at base). If you prefer the refusal-wording shape, edit item 5 before launch.
5. **-266:** Tuesday may close it as no-action (B252 `:446`). The brief keeps it last, as a tests-only census widening.

## 7. Corrections to the commission (measured)
1. **AGENTMAIL:** as the commission says, the key is not in HPSM-POC's `.env`: 0 lines by name (06:38). The brief's first line says so, and STATUS + the STOP line are the channel.
2. **The tier key differs from B251's:** under "deploy surfaces = tier 1", `deploy-package.py` work (-264) is **tier 1**, where B251 rated -255 tier 2. The brief says so.
3. **The load threshold:** the template (B251) said "below a 1-minute load of 40". On this 8-core Mac mini (`hw.ncpu` 8) the brief uses **below 8**, one heavy job at a time.
4. **The project root's `CLARIFICATIONS.md` is stale** (file time 29 Sep). C-105…C-111 were read from records main `2e284455` via the GitHub API. The brief forbids reading rulings from the root copy.
5. **Records main moved:** `6f5f0dc` → `2e284455` (#118 = `records/b257` merged 2026-10-17T05:42:55Z). The highest heading is C-111, so the next free is C-112 (owed to the runtime card when Kam rules).
6. **-264's test cite:** the fixture-a `def` is at `infra/tests/test_deploy_hpsmpoc208.py:531`; the ticket's `:532` is its docstring.
7. **-266 is bigger than "allow-list":** the census at `ShapeAnchorTests.cs:200` sees only `^…$` GeneratedRegex. Two of the three do not start with `^`, and `:217` is an inline `Regex.IsMatch`, so "allow-listed by the census" needs the census widened first.
8. **Decision store, undelivered:** 42 ruled `hpsmpoc-` cards carry no delivered mark. 12 have no id match in CLARIFICATIONS (`before-hp-invite-fixes-at-88pct`, `demo-login-role-1006`, `demo-name-check-residue-1012`, `f006-title-trips-compliance-rule`, `hosted-dsteps-start-today`, `hp-doc-figure6-roadmap-1008`, `hp-doc-figure6-second-choice-1008`, `pdf-name-note-1005`, `playbook-module2-readiness`, `qa-gate-at-90pct-stop`, `require-sqlserver-ci-check-1006`, `steve-dbs-pdfs-cleared-for-ai-1016`). The match is by id only; a C-entry may hold one in other words. Two bear on this round and are in the brief. `hosted-words-9-b241-1016` is in C-107 but unmarked: `decision_queue.sh --delivered hpsmpoc-hosted-words-9-b241-1016 "C-107 on HPSM-POC-analysis main 2e284455 (#118)"`.

## 8. Verified facts the brief rests on
- Code main `787d159` (ls-remote 06:39): in the local object store; no `b258*` branch; 18 check runs success + 1 skipped; 0 open PRs; 0 open alerts.
- Prior work: no commit names HPSMPOC-260…273. `5a93aa3` (B192) already handles `RetryLimitExceededException` at start-up, the precedent for -262.
- Ports 6900-6999: nothing listening (06:42). Load 2.51. Docker 29.7.2. `.tools/b250/lock.sh` = `.tools/b198/lock.sh` (cmp).
