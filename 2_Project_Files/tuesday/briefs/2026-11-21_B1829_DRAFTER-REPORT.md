STARTABLE: YES - the kit is complete and every literal is measured (stamp_check 194 of 194, rc 0); the generator is decided on a measurement (nothing exists without a download, so the seat writes a BCL-only C# generator); ONE stamp answer is required first: Q1, because committing HP's files collides with the repository's own rule R5 (MEASURED: 37 R5 findings) and with `<project>/CLAUDE.md:50-51`.

# B1829 drafter report | Datasec / OXPd_2 | wave 2, lane C (WP0.4 cut) | drafter Opus, 2026-11-21 14:39 to 15:0x AEDT

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1829_SEAT-X17_oxpd2-wp04-clients-and-gateway-stub.md` (94998 bytes, 314 lines; sidecar `.measured`, 194 claim lines plus `FROZEN` and `KIT`). Tools for the seat: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s304/d1829/gate/` (8 files, sha256 in the kit). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s304/d1829/` (programs and logs, no HP bytes) and the session scratchpad (see the disclosure).

## BLUF
1. **Lane C is startable as one kit in four parts** (P1 inputs and fingerprints, P2 generator and the inbound G1 parser, P3 gateway stub, P4 the 16 outbound clients and the regeneration check), on branch `b1829/wp04-oxpd2-clients`, seat X17, level opus, gate G1, window 240/200 minutes (Q12: longer than the wave's 180/140 because the seat writes a generator).
2. **Generator decision (Q2): a C# generator written by the seat, base class library only** (`System.Text.Json`, `JsonDocument` with `AllowDuplicateProperties = false`, a .NET 10 member, MEASURED in the reference pack), at `contracts/oxpd2/generator/`, compiled into the test project, so the hosted run regenerates in-process and compares with the committed `Generated/` on both legs. MEASURED: no OpenAPI generator in the package cache (64 entries, 0 match `openapi|nswag|kiota|swash`, control `xunit` 10), 0 `*openapi*` files in the drive-local SDK (control 4 SignalR dlls). Alternatives costed: Python stdlib generator (the drift check would not run in `dotnet test`; a `build/tests` test is no lane's and moves FLOOR); a package (download plus package line: refused).
3. **THE FINDING FOR TUESDAY (Q1, stop-class).** `build/repo_rules.py` R5 refuses any tracked file whose sha256 equals a `Source_Documents/` file. On my scratch clone of main with the 37 files staged: with `--source-documents` 37 lines `RULES: R5 contracts/oxpd2/hp/...`, rc 1, set-equal to the fingerprint list (control fires); with an empty folder and with no folder (the hosted `rules` job, `ci.yml:199`) `RULES: clean (152 files)`, rc 0. So the hosted run stays green, but every local R5 run will show 37 findings, and the project rule `<project>/CLAUDE.md:50-51` still reads "Nothing under `Source_Documents/` is ever committed or copied". The commission does not mention either. **Default: a closed-list exception in this lane (exactly those 37, proven by program), no change to `repo_rules.py` or CLAUDE.md, and a `build/**` follow-up plus a records amendment for Tuesday.** The kit REFUSES AT ONCE if S4 does not answer Q1 in words.
4. **The ruling is quoted** (his 09:40 board line, RELAYED from the commission; the card's option label and detail, MEASURED by `decision_queue.sh show` of that one card: `choice='b'`, ruled 09:41:45). Neither is in `CLARIFICATIONS.md` yet (0 hits for `hp files`, control `C-45` 1): a records item.

## FACTS RE-MEASURED (instrument in brackets; all at 14:39 to 14:58)
- Origin [gh api -X GET, project GH_CONFIG_DIR]: `.private` true, push true; main `ddbdf8009d0df77d084ef4834bb78d7c4a80b5b0` (PRs 1 to 4 closed and merged; Cards, Logging, UniversalPrint on main); open PRs 0; no `b1829` ref; tree 113 files, 0 under `contracts/`, the Adapters or Contracts.Tests paths, 0 `.gitattributes`. Hosted run of main [check runs + job logs by GET]: 4 ci jobs success, linux `total: 694`, `GUARD: clean (10 files)`, rules `Ran 53 tests`, `RULES: clean (113 files)`.
- The SDK copy [find/ls]: `<spec>` 273 files, 16 service + 20 types folders; 16 bundles + 5 targets (the commission's counts hold); the private key exists by NAME at `tools/certificates/ExtSDKRootCA.key` (never opened). Project copy and NAS copy of the 37 inputs sha256-identical, 37 of 37 [python]. So the NAS was not needed.
- The inputs [copyspecs.py, my program, run on a scratch clone]: 37 files, 7682881 bytes, list sha256 `6760314d...5b5013d7e`; references: bundles 3819 internal, 0 external; targets + reached types 365 internal, 146 external; 0 unresolved (report B3:295's broken references do not occur in these 37). 0 repeated keys; LF only; no final newline; 60 non-ASCII bytes, all in `description`.
- What the generator meets [python census]: 201 bundle operations, 1483 bundle schemas; 12 target operations (10 with bodies), max schema depth 9, no recursion; 13 composition shapes only; types object/string/array/integer/boolean (no `number`); 175 `$opMeta` properties, 141 keyword properties, 7 non-identifier schema names; HP's 4068 names pass `words.py` clean.
- Secrets [gitleaks 8.30.1, the workflow's options]: the 37 files rc 0 by name and under neutral names (control rc 1); the whole scratch clone rc 0; the workflow's neutral-scan step via `run_step.py` on the staged clone: `NEUTRAL-SCAN: stored objects 357 ...`, `no leaks found`, rc 0; stub probe values rc 0.
- Stub feasibility [ls]: ASP.NET Core shared framework 10.0.15 in the SDK and its runtime packs (linux-x64, win-x64) in the cache; 4 SignalR server dlls; NO SignalR client and NO `Microsoft.AspNetCore.TestHost` in the cache, so the test talks the SignalR JSON protocol over `ClientWebSocket` against Kestrel at `127.0.0.1:0`. `heavy.py` sets `HTTP_PROXY` to a closed port: the kit makes every test client `UseProxy = false`.
- Solution file [place.py on main's slnx]: `PLACED: 2 lines (src at 3, tests at 12)`; second run `REFUSED: already present`, rc 2.
- Machine [uptime, df, ls, tmux at 14:48:50]: load 1.66, 1004 GiB free, no lock folder, no `b1829`, 0 OXPd2 panes.
- Ticket [Jira GET, own helper, credentials in-process]: `OXPD2-9` Backlog, 0 comments.

## D-DECISIONS (Tuesday's as coordinator; each is a Question with a default in the kit)
Inputs by rule (16 bundles + 5 targets + 16 reached types); `contracts/oxpd2/hp/` + `inputs.sha256` (sha256sum form); `.gitattributes` `* -text` in `contracts/oxpd2/` and `Generated/` (line ends; whether the Windows image converts is UNMEASURED); one namespace per input; the runtime (parser, limits, refusal) EMITTED into `Generated/` because wave 2 owns only the csproj and `Generated/` of the Adapters project; no HP description text emitted; parser limits 1 MiB, depth 32, duplicates refused, unknown properties ignored, unknown enum values refused, `anyOf [ref, {}]` strict, `pattern`/`format` not validated (named limits); clients with no token, no `Authorization`, no retry; non-JSON bodies raw; stub in the test project only.

## QUESTIONS FOR TUESDAY (each with its default; full text in the kit)
- **Q1 (STOP-class) R5 / CLAUDE.md:50-51:** default the closed-list exception; alternatives a `build/**` kit first, or back to the product owner.
- Q2 generator: C# BCL-only. Q3 inputs: 37 files. Q4 layout. Q5 `.gitattributes`. Q6 parser rules (above). Q7 no descriptions. Q8 raw non-JSON. Q9 no token in clients. Q10 loopback stub at `/printerhub`, 500 for a body without `realm` (real behaviour UNMEASURED). Q11 positive payloads built from the schema. Q12 one kit, 240/200 (alternative: split P4 off). Q13 no records, README untouched. Q14 names. Q15 X17, G1. Q16 scan documents raw.

## CHAIN TABLE (every step's inputs exist at BASE or come from an earlier step)
| Step | Inputs | From |
|---|---|---|
| 0 | the kit, Stamp slots | Tuesday's stamp |
| 1 | gate folder; `<repo>` local config; origin main; Jira | drafter's scratch (exists); project (exists); GitHub; Jira |
| 2 | `<spec>`; `<clone>`; `copyspecs.py` | exists; Step 1; Step 1 copy |
| 3(a) | frozen T2/T3/T4 (Step 1 extraction); `<lane>/regen` (Step 1 folder, written here); generator (written here) | Steps 1, 3(a) |
| 3(b) to 3(e) | lock files (3(b) restore); `Generated/` (3(a)/3(c) regen); empty folder (made in 3(e)(ii)); `inputs.sha256` (Step 2) | earlier steps |
| 4 | staged tree; `commit-message.txt` | Step 3; Step 1 copy |
| 5 | the commit (5a); the push (5c) | Steps 5(a), 5(c) |

## UNMEASURED (said so in the kit)
Every dotnet result (no build, no test run by me); generated code size and compile time; whether xunit.v3 + `FrameworkReference Microsoft.AspNetCore.App` restores with no fetch (DERIVED: yes); Kestrel loopback and WebSocket on the hosted Windows runner; the Windows checkout's line-end default; real printer payload sizes/depths; what the real gateway does with a body lacking `realm`; STJ default-options behaviour on duplicates (only the member's existence measured); hosted.py and heavy.py on this lane (NEVER RUN here, RELAYED from earlier seats).

## CORRECTIONS TO THE COMMISSION AND THE LANE PLAN
1. The commission orders copying from `Source_Documents/` and says nothing of R5 or of `CLAUDE.md:50-51`: both still forbid it (Q1).
2. The lane plan's lane C row (`contracts/oxpd2/**` "NOT HP's files") and its Out are superseded by the ruling, as the commission says; the 37 files, not "the 16 service folders and 5 target files", are what generation needs (the 5 targets reach 16 types files by external `$ref`; the bundles need nothing else).
3. The NAS fallback is not needed: the project copy is complete and identical.
4. The window: 240/200, not the wave's 180/140 (Q12).
5. The lane plan's ownership "Adapters csproj and `Generated/` only" forces the parser runtime to be generated text; the kit says so.

## READING LOAD
Kit 94998 bytes + READ WHOLE items 2 to 6 117805 bytes (18 files, the seven tool programs counted whole) = **212803 bytes**. The 37 inputs (7682881 bytes) are data for programs, never read into context (longest line 61660 bytes).

## WHAT I DID NOT READ
`SETUP_RUNBOOK.md` (the kit puts it on the seat's list; I cite nothing from it); `CLARIFICATIONS.md` beyond greps (C-4, C-5, C-42, C-45 located, quotes counted); `02`, `03` beyond the cited rows; reports A9 (lines 40 to 60 and 272 to 296 only), A12 (grep lines), B3 (line 295), B4 (grep lines); the B1764 first kit and B1779 kit (the wave-2 commission makes the stamped B1786 kit the form; I also used the unstamped wave-2 kit B1825 lines 1 to 30, 77 to 107 and 166 to 315 for the current tool set); the in-flight B1826 kit; HP's libraries, examples, demos, documentation, and every SDK file but the 37 (parsed by program only) and the five names under `tools/certificates/`.

## OUTSIDE-THE-FENCES DISCLOSURE
- I made a no-push scratch clone of main (`clone.py ... draft`, push URL `invalid://no-push`) and wrote into it the 37 HP files, `inputs.sha256` and `.gitattributes`, staged (blobs written to its object store), no commit; plus symlink folders, a names list derived from HP's identifiers and logs. **All of it is in the SESSION scratchpad `/private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/947d827a-dd93-4d69-a9ed-35dea0ff8584/scratchpad/`, not in the commission's scratch folder**, on purpose: to keep HP's bytes out of Tuesday's own tree. Nothing was pushed, nothing deleted. Tuesday may quarantine that folder.
- `decision_queue.sh show` of the ONE card named in the commission, into scratch (`card.txt`); no `list`.
- One Jira GET (`OXPD2-9`), gh GETs only, no git write in any project tree, no build, no test, no message. Nothing of HPSM-POC opened.
