STARTABLE: YES - main 5e36d8dc holds what the lane needs (the Logging library; xunit.v3 4.0.3 and Serilog 4.4.0 are in the package cache); there is no b1832 or b1825 ref; the base's hosted run reads PASS. stamp_check exits 0 (262 claims, 262 measured). ONE stamp answer is required in words: Q1, the token interface, which changed from B1825 because of a measurement (the kit refuses at once without it).

# B1832 drafter report | lane A (refresh of B1825), seat X14, WP3.8 shared Graph layer (OXPD2-16, G2)

Drafter: Opus (in-session), 2026-11-21, 17:00:45 to 17:16:42 AEDT (clocks by `date`). Read-only except the kit, its sidecar, this report and scratch under `fleet/state/s304/d1832/`.

## Files
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1832_SEAT-X14_oxpd2-wp38-graph-layer.md` (335 lines, 111525 bytes, 8 stamp slots of `____`).
- Sidecar: `.measured` beside it. It holds 262 claim lines plus the `FROZEN`, `KIT` and `LOAD` lines. `stamp_check.py <kit>` returns rc 0.
- The seat's tools: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s304/d1832/gate/` (8 files, sha256 listed in the kit).
  - Five come unchanged from B1831: clone, heavy, words, run_step, and hosted with its `--skipped-*` options.
  - Two come unchanged from B1825: `place.py` (the Graph lines) and `commit-message.txt`.
  - One is new: `nocopy.py`.
- **B1825 is superseded and must never be launched.** The kit says so on its first line.

## BLUF
1. **The refresh keeps every B1825 decision except Q1.** T2, T3 and block R are byte-identical (cmp rc 0), and the R model's re-run equals the block. Every literal was re-measured against main `5e36d8dc`:
   - solution file: 19 lines, `place.py` → src at 6, tests at 16;
   - 291 files;
   - hosted run: total 894 on both legs, skipped 4 on linux and 19 on windows, GUARD 10 and 11 files, RULES 291 files;
   - ci.yml unchanged, sha `c3894bbc`;
   - design lines unchanged, 41 quotes checked, 0 missing.
2. **Q1 changed because of a measurement.** Lane D's broker (READY on `b1831/wp15-token-broker` `70c1fad5`, not landed) has these calls:
   - `GetTokenAsync(SessionKey)` and `GetNewTokenAsync(SessionKey)`, which return `AccessToken` bytes (ITokenBroker.cs:15 and :21);
   - `SessionKey` is a three-part struct.

   B1825's `string sessionHandle` cannot be met by a one-class adapter. The new default:
   - `IGraphTokenSource` is bound to one session and passed into each `SendAsync` / `GetPagesAsync`;
   - the client holds no source;
   - no session handle ever reaches the Graph layer.

   The adapter is not this lane's work.
3. **Correction: B1825's control C8 would have FAILED a correct library.** I compiled a scratch console with the project's SDK 10.0.404, outside any project tree, and it showed:
   - the async state machine keeps a token local in field `<t>5__2`;
   - a closure keeps a captured token in a field;
   - the lambda cache `<>c.<>9__2_0` is a writable static.

   C8 now checks every type that is NOT `[CompilerGenerated]`, and still checks static fields on all types. Mutant mKeep is still caught.
4. **New decision Q17:** a `GetTokenAsync` that throws ends the call as `Unauthorized` before any send. B1825 left this unsaid.
5. **Lessons carried from B1829, B1830 and B1831:**
   - `-p:NuGetAudit=false` on every restore and publish;
   - `repo_rules.py` runs only with no option or with an empty folder, never on the real `Source_Documents`. The key-folder rule is F4; and at main R5 prints the 37 HP inputs (RELAYED).
   - The no-copy check is the new `nocopy.py`, which prunes key folders before opening them;
   - `hosted.py` runs on the base first, with the skipped counts;
   - the words check excludes the two lock files (the `linux-x64` / `win-x64` seat-id hits, MEASURED 2 per lock file);
   - STATUS within 5 minutes;
   - the window is 240/200 (was 180/140) to allow for the shared lock; `BLOCKED: lock held` means relaunch.

## What I measured, and how
- **Origin**, by `gh api -X GET` under the project GH_CONFIG_DIR at 17:00:45 and again at 17:16:42 (nothing moved):
  - main `5e36d8dc`;
  - PRs 1 to 6 merged, 0 open;
  - b1831 at `70c1fad5`: ahead 1, behind 0, 35 files; its STATUS ends `READY B1831`;
  - private true, push true.
- **Main tree**, by tarball: 291 files. 0 paths contain `graph`. Of 206 `.cs` files:
  - 22 contain `HttpClient`, all lane C's generated clients, generator and tests;
  - 0 contain `Retry-After`, `nextLink`, `graph.microsoft` or `createUploadSession`;
  - control: 204 contain `namespace`.
- **Logging API**: SuiteLoggerFactory.cs:18, SuiteLogOptions.cs:13, LogScanner.cs:49/:57, LogScanResult.cs:24/:33. `P:Serilog.Core.Logger.None` is documented in the cached Serilog 4.4.0 xml at line 1779.
- **hosted.py on main**: PASS. Control: `--skipped-linux 5` gave FAIL 2.
- **Scratch .NET consoles**, outside any project tree (17:03 to 17:04):
  - `NonValidated` keeps R08, R09, R10, R17, R23 (2 values) and R25 unchanged;
  - `Task.Delay(TimeSpan, TimeProvider, CancellationToken)` compiles and runs;
  - the C8 compiler-generated fields above.
  - The consoles' own package folder held 0 files afterwards, so nothing was fetched.
- **Lane-shaped dry run** in my own no-push scratch clone, with no dotnet. Placed lines, T2, T3 and two probe test files, staged:
  - `RULES: clean (295 files)` in both forms;
  - `Ran 53 tests`, `OK`;
  - nocopy: 34616 hashed, 25 key folders pruned, matches 0; with `--plant`, matches 1;
  - neutral scan: 25 of 25, no leaks;
  - words: clean on 2 files (control 1 hit);
  - ASCII: 0 (control 1);
  - gitleaks: 0 on the clone, on neutral copies and on the message (control 1).
- **Jira OXPD2-16**: one GET with my helper. Backlog, 0 comments.
- **Machine**: cache 64 entries; load 2.15; 1003 GiB free; no lock folder; 0 OXPd2 panes out of 3.

## Questions with defaults (all in the kit)
| Q | Default |
|---|---|
| **Q1 (answer in words)** | Per-session token source, passed per call |
| Q2 | One refresh per call, no coalescing |
| Q3 | 3 retries, 30 s / 60 s caps, fallback 1 to 15 s, no jitter |
| Q4 | Block R |
| Q5 | Every method retried on 429/503 |
| Q6 | Transport retries for upload pieces only |
| Q7 | 100 pages, same origin, 8192-character link limit |
| Q8 | 4 MiB, 100 s |
| Q9 | 10 MiB pieces, 5 retries, seekable stream, no Authorization header |
| Q10 | Base address as a setting plus 4 presets |
| Q11 | Serilog logging, six properties |
| Q12 | The kit's names |
| Q13 | Caching and queueing out |
| Q14 | No records, README untouched |
| Q15 | 240/200 minutes, X14, G2 |
| Q16 | Printable ASCII token |
| Q17 | A throwing source means `Unauthorized` |

Not decided by the kit:
- who writes the broker adapter, and where it lives;
- whether the broker's distinct failures should map to different outcomes.

## Reading load
The kit is 111525 bytes. Its 24 READ WHOLE files total 133858 bytes. Together: **245383 bytes**. **The kit is about 11% over the wave-1 limit of "about 100 kB".** I did not cut it: the added parts are the Q1 change, the C8 correction and the carried tool lessons.

## NEVER RUN (STOP-severity, marked in the kit)
- the owned-paths property;
- every heavy job through the runner;
- `nocopy.py` on a real output of this lane;
- the C8 source scan;
- `hosted.py` on a head of this lane;
- any dotnet total (a total of 0 is a STOP).

## UNMEASURED
- every dotnet result for this lane;
- the Windows leg, including `NonValidated` on Windows and the 200 ms stall test;
- how Graph really shapes `Retry-After`, next links and upload ranges;
- what a panel user accepts as a wait.

## Not read
- the design documents whole (only the cited lines);
- lane D's code beyond ITokenBroker.cs, AccessToken.cs and SessionKey.cs (public lines);
- the B1830 VERDICT;
- other seats' STATUS files, beyond B1829's DEVIATIONS / CHAIN / HOSTED sections and the tail of B1831's;
- the B1831 kit, beyond lines 1 to 34, 104 to 116 and 180 to 375;
- the B1829 kit (its lessons came from its report and STATUS);
- `SETUP_RUNBOOK.md` (it is on the seat's list; I cite nothing from it);
- BACKLOG.md;
- any `Source_Documents` content (only `nocopy.py` hashed files, with key folders pruned);
- the NAS library;
- HPSM-POC.

## Outside-the-fences disclosure
- **Scratch clone**: `clone.py ... draft` (push URL invalid), switched to a local branch, staged files, no commit. In it I ran `repo_rules.py`, `unittest` and `run_step.py`, all Python.
- **Two scratch .NET consoles** under `d1832/scratch/csgen*`, built and run with the project's dotnet, with their own HOME and package folder and a closed proxy. They are not a project tree and not lane code, but they are a dotnet run, so I disclose them here.
- **`nocopy.py`** hashed `Source_Documents` files with key folders pruned (25 folders were never opened).
- **The kit file was edited once by a Python `os.replace`**: four `٥` escapes had been turned into raw characters by the Write tool, and I restored them. Every other edit used Write or Edit.
- Temporary sidecar files were moved into scratch, not deleted.
- One Jira GET. `gh api -X GET` calls only. No git write in any project tree, no message.
