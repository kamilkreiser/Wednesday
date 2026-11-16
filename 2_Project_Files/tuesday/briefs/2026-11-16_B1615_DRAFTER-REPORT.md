STARTABLE: YES (after Tuesday's stamp; five questions, each with a default that lets it start)

# B1615 drafter report: HPSM-POC lane H-1 (HPSMPOC-484 + optional 496), seat H173

Drafted 2026-11-16 from 14:56 to 15:03 AEDT (`date` printed 14:56:59, 14:57:16, 14:58:44, 14:59:32, 15:02:04, 15:02:57).
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-16_B1615_SEAT-H173_hpsmpoc-lane-h1-followup-proxy-startup-warning.md` (315 lines).
- Sidecar: `...startup-warning.md.measured`, 93 claims plus S01-S24. `stamp_check.py <kit>` exits 0 (93 of 93 measured).
- Work folder: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s282/r1615/` (Jira GET copy `jdesc.py`, `jira.txt`, raw files at `678a1153`, a depth-1 clone `repo/`, `mk_sidecar.py`).
- Template: `2026-11-16_B1599_SEAT-H171_hpsmpoc-forwardedproof-race.md` (read whole, with its STATUS, its drafter report and its sidecar).

## BLUF
- **484** is still absent on main `678a1153`: `Program.cs:128-131` hold the two warnings and neither reads `FollowUp:TrustedProxies` (`grep -c -F 'TrustedProxies' Program.cs` is 0, control `ProofKey` is 1). A host that sets only the follow-up list logs nothing, because `forwarded.Enabled` needs the other lists (`ForwardedClientAddress.cs:50`).
- **The build** is one `if` plus `LogWarning` in `Program.cs`, same template as `:131` byte for byte, with `"FollowUp:TrustedProxies"` as the section argument. It reads the list through `IOptions<FollowUpOptions>`, the same object the limiter reads (`FollowUpLink.cs:255`, `:280`), so "names a proxy" cannot diverge. Five test rows read the line through the existing `LogCapture`, both sides (line present once; value set; nothing named; both lists; blank entry).
- **496** (the guard on the forcing test's first request, `ForwardedProofTests.cs:178`) is built by default as D3, with a plant that proves it can fail; the seat may record `496 DECLINED: <reason>`.
- **Two files** (`Program.cs`, `ForwardedProofTests.cs`), one branch `b1615/hpsmpoc-followup-proxy-startup-warning`, one commit, no PR. Sonnet builder (row C2, `model-routing.md:92`), gate G2 (`:109`). Ports 10190-10199. HPSM standing line is in the kit's head and its standing lines.
- Held keys: the pickup and today's note hold no DROPPED or HELD line for 484 or 496. The only hits are records mentions (484 created by B1575, the B1565 gate's Minor 1).

## Facts re-measured with instruments
- **Main.** `gh api -X GET repos/datasecau/HPSM-POC/branches/main --jq .commit.sha` at 14:57 gave `678a1153d28be006a088a3b1fba8f5aab52e8d0e`. The depth-1 clone's `git rev-parse HEAD` printed the same. Its one commit is the squash of #325, subject "Await the forwarded-proof test's reading instead of racing the test server's early response".
- **Open PRs 0** (`pulls?state=open`: HTTP 200, length 0; control `state=all&per_page=3` lists 325, 324, 323; `pulls/99999` HTTP 404). `matching-refs/heads/b1615` length 0 (control `heads/b1585` length 1).
- **Jira (GET only, my own copy of `jdesc.py`, no token printed).** HPSMPOC-484 Backlog (labels `rec-2026-11-15`, `review-finding`); HPSMPOC-496 Backlog (labels `rec-2026-11-16`, `test`; "do when the test server or the test host is next upgraded, or decline"; "Done when: the guard is added, or the item is recorded as declined"). Output in `r1615/jira.txt`.
- **Pointers at `678a1153`** (printed by `awk NR==n` over the raw file): `Program.cs:128-131`, `:134`, `:6`; `ForwardedClientAddress.cs:34`, `:38`, `:50`, `:84`; `ForwardedProofGate.cs:20-21`; `FollowUpLink.cs:19`, `:43`, `:255`, `:280`; `AssessmentModule.cs:120`; `Directory.Build.props:6` (`TreatWarningsAsErrors` true); `LogCapture.cs:8`; `B223DemoNameCheckTests.cs:26`; `ForwardedProofTests.cs:142`, `:178`, `:277`, `:304-305` (313 lines at base). All in the sidecar.
- **No test reads a start-up log line today.** `grep -rn -i -F 'names trusted proxies'` over `api/tests` printed 0 lines; over `api/src` it printed 2 (control).
- **Names:** the log text exists only in `Program.cs` and `ForwardedClientAddress.cs:98` (a different message); no doc or runbook lists the start-up warnings (`grep -rl -F 'no X-Forwarded-For is believed'` over the clone printed only `Program.cs`).
- **Toolchain.** `.tools/dotnet-10.0.404` with `DOTNET_ROOT` and `PATH` printed `10.0.404` at 15:02:04. `global.json:3-4` pin it with `rollForward` `disable`.
- **ci.yml at `678a1153`:** `dotnet test HpsmPoc.slnx` `:87`; the SQL Server `--filter` with `Hosting.` `:252`; judge `bad = sum(...)` `:303`; `MSSQL_IMAGE` `:184`; floor `:314` (100 for `api-assessment`); `validate.sh` `:630`.
- **Ports.** `lsof -nP -iTCP:10190-10199 -sTCP:LISTEN` gave 0 rows (unfiltered 12). The word-boundary scan over 57 SEAT `.md` kits of 15 and 16 Nov for `1019[0-9]` gave 0 (control `1018[0-9]` over the H172 kit gave 2). Panes at 14:58: `%0 tuesday`, `%1 fleet-monitor` and two unnamed; no HPSM-POC pane.
- **The project's own checkout is behind main**: `git cat-file -t 678a1153` there printed `fatal: Not a valid object name`. The kit tells the seat to clone by URL (as the B1599 kit does) and not to read remotes from that checkout.

## D-decisions (the drafter's)
- **D1 Read the list through `IOptions<FollowUpOptions>`, not `builder.Configuration`.** It is the object the limiter reads, so a form the binder ignores (a comma-separated scalar) cannot make the warning fire while the limiter sees an empty list. Fully qualified `Microsoft.Extensions.Options.IOptions`, because `Program.cs` has no such using (0 hits), keeping the product diff to added lines only.
- **D2 The message template is byte-identical to `:131`'s**, only the `{Section}` argument changes. The sweep and the ticket both say "same kind", and any other phrasing stops the seat. Rendered text is written into the kit (and into row 1's assertion).
- **D3 Two lines when both lists name proxies.** The existing line stays untouched; the new line is a separate `if`. Row 4 pins "each once".
- **D4 Blank entry names nothing.** `Any(p => !string.IsNullOrWhiteSpace(p))`, matching how `ClientAddress` only treats parsable entries as proxies (`FollowUpLink.cs:92`). Row 5 pins it (Q-5).
- **D5 `LogCapture` is reused, not edited** (`Support/LogCapture.cs` is outside the lane). Row 4's existing-line count at base is the kit's built-in proof that the capture sees `app.Logger` start-up lines; if it reads 0 the seat stops. I did NOT run this (UNMEASURED below), so the kit makes it a gate on Step 3.
- **D6 Red-first is by assertion for rows 1 and 4 only.** Rows 2, 3 and 5 assert absence, so they are green at base by construction; the kit names row 1 at head as their control, which can fail.
- **D7 496 is proven by a plant.** The hook fires before the response is sent in a scratch copy, so the guarded forcing test must fail in about 30 s with `TimeoutException` and the unguarded one must hang until the seat stops it by pid at 120 s. No plant, no commit of D3.
- **D8 CodeQL for C# is not asked for.** The B1599 builder's STATUS says it cannot run on this arm64 machine; the kit says so once and relies on hosted CodeQL.
- **D9 Run counts are smaller than B1599's** because nothing here is timing-shaped except the forcing test: class x10 at head, `Hosting.` group x5, SQL Server part x3 (once at base), whole `api` once, `infra` at base and head.
- **D10 The kit follows the B1599 gate's findings:** `pr-body.md` and the squash texts name no branch and no work number (F2), and `landing.txt` writes `<PR-NUMBER>` literally with the real pushed sha40.

## Q-questions for Tuesday (each with a default)
- **Q-1 Port block.** Nothing assigned one. **Default: 10190-10199** (first free block after H172's 10180-10189; checked free above). Change it at the stamp if another block is held.
- **Q-2 496.** Build the guard or decline it? **Default: build it (D3), with the plant proof; the seat may decline with a one-line reason** (the ticket's own wording allows either, and it is the same file).
- **Q-3 Gate model for G2.** The row's O55 cell says "1st if the follow-up's mechanism sits on a G1 surface". The surface is the client-address trust control, but the change is a log line and tests. **Default: G2 on Opus**, as B1599's gate was. Alternative: Sonnet G2.
- **Q-4 Two warning lines when both lists name proxies?** **Default: yes, two lines, each once** (the existing line is not reworded or merged; D3).
- **Q-5 Blank `FollowUp:TrustedProxies` entry.** **Default: names nothing, no line** (D4, row 5). Alternative: drop row 5 and test `Any(p => p is not null)`; the seat would need your word, so it is not a seat decision.

## Step input table (MEASURED LITERALS rule 4)

| Step | Inputs | Produced by |
|---|---|---|
| 0 | stamped kit, deploy key, project git config, toolchain at `.tools/dotnet-10.0.404` | exists at BASE / Tuesday's stamp |
| 1 | origin reads, clones | Step 0 |
| 2 | `mut` clone, restore; containers | Step 0; started inside 2(c) |
| 3 | `head` clone, `LogCapture` at BASE | Step 0; exists at BASE (`Support/LogCapture.cs:8`) |
| 3(c) | Step-3 tree with D3, a scratch copy | Step 3 |
| 4 | Step-3 tree plus D1, containers | Step 3; Step 2(c) (or restarted by name) |
| 5 | the Step-4 diff, the name lists | Step 4; project files at BASE |
| 6 | Steps 2-5 green | Steps 2-5 |
| 7 | runs.tsv, red.diff, green diff, pushed sha | Steps 2-6 |

## UNMEASURED
- **Whether a warning written by `app.Logger` during start-up reaches a `LogCapture` added with `ConfigureLogging` in the factory.** B223's factory shows the registration form for request-time logs (`B223DemoNameCheckTests.cs:26`); I ran no test. The kit makes row 4's base count of the existing line the proof, and a miss is a STOP with entries printed.
- Whether `IOptions<FollowUpOptions>` resolves at that point of `Program.cs` without a validation side effect, and whether the new lines compile with 0 warnings (warnings are errors here). No build was run.
- The base total of the `Hosting.` group at `678a1153` (the B1599 STATUS read 221 at its head; this kit says "base total plus 5" and has the seat print the base total).
- The api-assessment SQL Server part's local wall time (carried from B1599).
- Whether the hosted `FollowUp:TrustedProxies` is still empty (RELAYED from the ticket; no hosted read made).
- The `FollowUpSessionLimiter` behaviour of an entry that is not an address (it ignores it through `IPAddress.TryParse`, `FollowUpLink.cs:92`): read, not run.

## Outside-the-fences disclosure
- **Scratch clone.** `git clone --depth 1 git@github.com:datasecau/HPSM-POC.git` into `fleet/state/s282/r1615/repo`, using the project deploy key through `GIT_SSH_COMMAND` for that one command (the B1599 drafter did the same). No fetch, pull, ref write or push in any project repo; nothing in `!CODING` was written.
- **Reads outside the two files.** `gh api -X GET` (branch, pulls, matching-refs, five raw file contents) under the project's `GH_CONFIG_DIR`; a GET-only Jira read of two keys through my own copy of `jdesc.py` and `rg.sh` (copied from the sweep's scratch folder, no token printed); the B1599 STATUS and VERDICT in the project's `Briefs/` and Tuesday's `briefs/`; the pickup and today's and yesterday's notes by `grep -n`; `model-routing.md`, `models_latest.json` and `brief_seat.sh` by `awk NR==n`.
- **Not run.** No build, no test, no docker, no `az`, no mail, no board, no `decision_queue.sh`, no Artifact, no `_ledger.md`, no WEDNESDAY or FRIDAY tree, no `cd`. One `lsof` and one `tmux list-panes` (read only).
- **Not written.** Only the kit, its sidecar, this report and my scratch folder. The `.measured` sidecar was produced by `stamp_check.py --init` and filled by `mk_sidecar.py` in the scratch folder.

DRAFTED B1615: kit 315 lines, sidecar rc 0, questions 5
