STARTABLE: YES (after the stamp; Q1 is STOP-CLASS and the kit refuses unless S4 answers it "a" in words)

# B2188 DRAFTER REPORT: seat X97, lane L3a (the host's composition, part A)

Drafter: read-only Opus drafter for Tuesday s336, commission `2026-11-28_B2184-B2189_OXPD-WEEKEND-KITS_COMMISSION.md` section 5. Clocks by `date`: first `Sat 28 Nov 2026 00:07:47 AEDT`; kit written about 00:24; sidecar filled 00:26 to 00:28; this report about 00:30.

Outputs:
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-28_B2188_SEAT-X97_oxpd2-l3a-host-composition.md` (9 unfilled slots, S1 to S8 and the last line; 0 non-ASCII characters; 0 ban-list names, 0 card ids, by program with controls).
- Sidecar: the same path plus `.measured`: 168 claims, 168 measured; `stamp_check.py <kit>` exit 0.
- Seat tools: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s336/d2188/seat-tools/` (eight files; hashes in the kit's THE TOOLS).
- Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s336/d2188/` (tarball of main, `src/`, the scratch repositories `sim/` and `sim-base/`, the check outputs, the prototype mutant rows).

## BLUF
1. **Lane L3a is drafted as a product lane in kit X86's form (THE CODE written by the seat to a spec, frozen red cells, the seat writes its own mutant rows).** Scope: one `Suite` settings section read at build; the HTTPS certificate and key from the secret store when `Suite:Tls` names two secrets, with the host refusing to build unless the certificate is readable, valid now, for server authentication, and named exactly for `Suite:HostName` (CN equal, a SAN DNS match, no wildcard, no IP); and the landed Graph client, OneDrive browser, session record store, token broker (refresher not wired), job spool and scan receiver registered in the host, each made at first use. Twelve owned paths (6 A, 6 M) under `src/Datasec.Suite.Server/` and `tests/Datasec.Suite.Server.Tests/`; cells W01 to W11 (25 cases); nine mutants; H12 edited in two lines.
2. **Narrower than plan r2's sentence (Q1, STOP-CLASS).** The registry and the `IAppModule` lines are left out, each for a reason measured at source: `AddSuiteData` throws at registration on an empty connection string (`src/Datasec.Suite.Data/SuiteDataOptions.cs:35-38`), so wiring it forces a custody decision for the database connection string at build; and `IAppModule` cannot live in Server (an app project implementing it would reference the host that references it: a cycle), while plan B2156's shared touch 2 writes an empty module into five app projects owned by other lanes (OneDrive is X93's, three are X84's new projects).
3. **Base and dependencies:** BASE = `main` `7d652c5f` (X89 landed as PR 59, which plan r2 requires). The lane needs NEITHER L0 nor L5 (none of its paths or references is theirs; it references the LANDED OneDrive project and wires only `MyDriveBrowser`). Its REFUSE allows X84 and X93 beside it and refuses any L3b or other Server-path seat (plan r2 line 87).
4. **Lock files and the release guard move by design.** The Server project gains four references (Graph, OneDrive, Sessions, Jobs); the two lock files change only by ONE unlocked restore at Step 3 and are judged by check 4 (every package already in a BASE lock file: PREDICTED Serilog 4.4.0 and Serilog.Sinks.File 7.0.0 only) and the locked restore. Guard counts are PREDICTED 28 and 29 (14 and 15 plus 14 files); the seat publishes BASE at Step 1 and the head at Step 5 and the listing difference judges.

## Facts re-measured (instrument; clock)
- `gh api -X GET repos/datasecau/OXPd_2/commits/main` -> `7d652c5f0f8d9854aaf49b43df79e77855eccb46`, tree `760295e3...`, parent `760e1a64` (00:08:21). Open PRs 0. `matching-refs/heads/b2188` 0 rows (00:08:21 and again about 00:19). No `b2159` branch (X84 not pushed at 00:08).
- Tarball of `7d652c5f` into `<d>/src`: 679 files; scratch commit `HEAD^{tree}` -> `760295e34a25342af686251b9d72f69e549f6959` (equal to main's tree).
- Main's push run (Tuesday's s335 logs): `hosted.out` last line `HOSTED 7d652c5f...: PASS`; linux `RULES: clean (679 files)`, `GUARD: clean (14 files)`, `succeeded: 2429`; windows `GUARD: clean (15 files)` (grep over `fleet/state/s335/main7d65/`).
- Server.Tests at BASE: 18 indented `[Fact`, 0 `[Theory`, 0 `[InlineData` (checks_l3a.py check 6 and an in-process count).
- `ServerHost.cs:46` `replace?.Invoke(builder.Services);`; `HostCellTests.cs:255` and `:258` the two H12 lines; `README.md:4` the "Nothing else is wired yet" sentence; ci.yml lines 40/70, 46/76, 48/78, 211, 218 (all `grep -n` over BASE).
- Framework members (the project's own ref packs, `grep -n`): `X509Certificate2.MatchesHostname(String, Boolean, Boolean)` with parameters `hostname`, `allowWildcards`, `allowCommonName` (System.Security.Cryptography.xml:21753); `CreateFromPem(ReadOnlySpan<char>, ReadOnlySpan<char>)` (:21584); `X509CertificateLoader.LoadPkcs12` (:22380, :22405); `KestrelServerOptions.ConfigureHttpsDefaults` (Kestrel.Core.xml:1638); `HttpsConnectionAdapterOptions.ServerCertificate` (:2860) and `.ServerCertificateChain` (:2870).
- Machine at 00:17: load `4.57 9.34 6.66`; 834 GiB free; wave lock ABSENT; panes `tuesday`, `Datasec/NexusAI-N187`, `Datasec/OXPd2-X84` and six unnamed; X84 STATUS last line `WORKING: Step 4 (green: the whole solution running, then the mutants)`; X89 STATUS last line `READY B2170: 09b6050...`.
- The sibling kit X93 (B2184) names L3a's two folders as none of its seven paths (`grep` over it, read-only).

## Checks of the kit's own tools (each STOP-severity check run once with its control)
- `checks_l3a.py` over BASE's own index (`<d>/sim-base`): `CHECKS: 2 of 9 PASS`, nine controls FIRED (`<d>/checks-base5.out`).
- Over the simulated staged tree (a never-compiled prototype of the twelve paths, prototype lock files with the PREDICTED entries): `CHECKS: 9 of 9 PASS`, nine controls FIRED (`<d>/checks-proto3.out`).
- The same with a planted `Planted.Package 9.9.9` in the server lock file: check 4 FAIL, `8 of 9` (`<d>/checks-neg4`).
- Check 5 first failed on BASE's own lock files (NuGet writes no final line feed: `}\n}` at the end, `od -c`); fixed in the checker before any kit text quoted it.
- `mutants_c3.py --list` over nine prototype rows: `LIST: 9 mutants, 1 suites, 11 cells` rc 0; a bad row under `src/Datasec.Suite.Graph/`: `LIST REFUSED: rows mBad` rc 1.
- `words.py --control`: `CONTROL FIRED: 13 of 13`; `words.py` over `commit-message.txt` and the prototype `added.txt`: `WORDS: clean (2 files)`.
- gitleaks 8.30.1: control folder with a generated token rc 1; the tools folder rc 0, `no leaks found`.
- NEVER RUN: `mutants_c3.py run`, `checks_l3a.py` over real code and real lock files, every dotnet job, every cell. The kit marks each prediction PREDICTED and each such check NEVER RUN.

## D-decisions (the kit's; each is a Question at the stamp)
D1 width (registry and `IAppModule` out); D2 two PEM secrets, PKCS#12 re-import on every platform; D3 the name rule (CN equal and SAN match, no wildcard, no CN fallback, no IP); D4 validity and server-auth EKU, no chain or revocation; D5 one TLS source at a time; D6 lazy wiring, refusal at first use; D7 broker with a refresher that is not wired; D8 new cells only, H12's two lines the one landed edit, no settings file, no route.

## Q-questions for Tuesday (each with a default)
- **Q1 (STOP-CLASS): the lane's width.** Default **a**: L3a without the registry and without the `IAppModule` lines; the registry moves to L3b with a custody Question for the connection string; `IAppModule` to a small INFRA kit after L0 lands (contract in `Datasec.Suite.Core` or another shared project; one empty module per app project written once). Alternative **b**: re-draft with either piece.
- **Q2: the TLS source.** Default: two PEM secrets, one source at a time. Alternative: one PKCS#12 secret (password custody).
- **Q3: the certificate rules.** Default: strict (as D3, D4). Alternative: a wildcard SAN, or a chain check against a configured root.
- **Q4: lazy refusal.** Default: library settings judged at first use (the host starts and `/health` answers). Alternative: fail-fast at build (changes HostRig, a landed file).
- **Q5: no settings file.** Default: none; keys documented in the README, supplied by the deployment. Alternative: a committed `appsettings.json` (UNMEASURED effect on the landed cells' log levels).
- **Q6: the print sender.** Default: not wired (per printer: `HttpIppTransportOptions.CertificateSha256` is `required`). Alternative: a per-printer factory here.
- **Q7: gate and launch.** Default: G1 (`model-routing.md:108`), Opus, READY Step 0 + 270, push by + 240, pane `Datasec/OXPd2-X97`, launched beside X84 and X93 now (disjoint paths, one shared wave lock, about 120 minutes of waits allowed). Alternative: G2; or hold to Fri 4 Dec Slot B as plan r2's table has it.
- **Q8: the runner.** Default: canonical `heavy.py` (`31adedc8...`), B2172 NOT adopted. Alternative: adopt B2172 (a narrow revision).
- **For Tuesday's stamp, not a kit question:** whether launching L3a now (Sat) instead of Fri 4 Dec is wanted. The kit allows either; three build seats on one wave lock lengthens every seat's waits.

## Chain inputs (MEASURED LITERALS rule 4)
| Step | Inputs | Produced by or present at |
|---|---|---|
| 0 | the kit; Stamp S2, S3, S4, S8 | Tuesday's stamp |
| 1 | `<src>` (eight files); `<repo>`'s local values; the origin (BASE); BASE's push run; the publish lines of `ci.yml` | drafter's scratch (exists); `<repo>` (exists); GitHub; `<clone>` from this step |
| 2 | the files at BASE; `02_architecture.md` | Step 1's clone; the project's design folder (exists) |
| 3 | THE CODE, THE NEW CELLS; the restored and built clone | this kit; Step 1 |
| 4 | the pinned tree; C7; `mutants_c3.py`; the rows file (written in Step 4 before its run) | Step 3; this kit; Step 1; Step 4 |
| 5 | the green tree, every mutant undone; BASE's publish listings | Step 4; Step 1 |
| 6 | the staged tree; `checks_l3a.py`, `words.py`, `commit-message.txt` | Step 5; Step 1 |
| 7 | the commit; `origin/main`; `run_step.py`, `hosted3.py`; the Step-5 guard counts | Step 7 (a); the fetch; Step 1; Step 5 |

## UNMEASURED (the kit names each)
- Whether a PEM-made certificate, after the PKCS#12 re-import, serves TLS on macOS, Linux and Windows (D2): the local run and the two hosted legs judge.
- Whether Kestrel applies `ConfigureHttpsDefaults` set by a delegate that reads a variable assigned after `builder.Build()` (C5): W01 judges.
- Whether Microsoft's container wraps an exception thrown by a factory (W09 reads both forms).
- Whether a Release publish copies `.pdb` files (the guard counts 28 and 29 assume it does); the listing difference judges.
- Whether the compiler or the default analyzers warn on any of the nine mutant NEW texts (a BUILD-FAILED row is a STOP).
- The implicit `DateTime` to `DateTimeOffset` conversion for a `Local` kind in the validity check (W03 judges).
- How the deployment puts the two TLS values into the store; how Key Vault hands out a certificate (R16).
- `gh api -X GET repos/datasecau/OXPd_2 --jq .private` was not run by the drafter (other reads under the same login answered).

## Outside-the-fences disclosure
- Writes: only the kit, its `.measured` and this report under `tuesday/briefs/`, and files under the scratch `fleet/state/s336/d2188/`. In that scratch I ran `git init`, `add` and `commit` (scratch repositories only, with a scratch identity passed by `-c`, never in a project repository) and `git clone` of my own scratch repository. A gitleaks control token file was generated (never printed) at `<d>/gl-control/c.txt` and left in place: not deleted, per the never-delete rule.
- Reads in the OXPd project (read-only): `CLAUDE.md`, the hashes of `BACKLOG.md` and `CLARIFICATIONS.md` (not read whole), `02_architecture.md` by `grep`/`awk` lines, the X84 and X89 STATUS last lines, the X89 STATUS by `grep -c` for the neutral-scan proof lines, the `.tools/` folder listing, and two XML documentation files in `.tools/dotnet/packs/` (the SDK's reference docs). No `Source_Documents/`, no `4_Credentials/` beyond `GH_CONFIG_DIR`, no key folder, no NAS library.
- Tuesday-tree reads: the commission, `DRAFTER_RULES.md`, plan r2 whole, plan B2154 lines 80 to 100, B2156 lines 95 to 125, B2169 lines 36 to 56, B2165 lines 200 to 230, kits X84 (stamped) and X86 whole, the sibling X93 kit's first lines and one `grep`. No card store read, no `fleet/briefs_staged/`, no ledger, no WEDNESDAY or FRIDAY tree.
- GitHub: `gh api -X GET` only (commits, pulls, matching-refs, the tarball). No az, no dotnet, no ssh, no docker, no lock taken, no HTTP to any other host. `tmux list-panes` read once.
