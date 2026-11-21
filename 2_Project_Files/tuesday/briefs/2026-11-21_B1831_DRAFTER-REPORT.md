STARTABLE: YES - the kit is complete and every literal is measured (stamp_check 196 of 196, rc 0; pointers 25 of 25 and quotes 31 of 31 on their lines). The design agrees with the N-4 reading at every point but ONE, the subject check (Q1, stop-class): the kit defaults to the subject the grant STATES, so the broker reads no token. Tuesday must answer Q1 in words at S4. If Tuesday reads the design as requiring the broker to read the token's claims, the answer is NO and the point goes to the product owner on a card.

# B1831 drafter report | Datasec / OXPd_2 | wave 2, lane D (WP1.5 token broker, C6, WP1.5 half) | drafter Opus, 2026-11-21 15:55 to 16:16 AEDT

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1831_SEAT-X18_oxpd2-wp15-token-broker.md` (105034 bytes, 375 lines; its sidecar `.measured` holds 196 claim lines plus `FROZEN` and `KIT`). Tools for the seat: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s304/d1831/gate/` (7 files, sha256 listed in the kit). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s304/d1831/` (main's tarball, programs, logs).

## BLUF
1. **The precondition holds.** `main` = `bb91433481718652bf808884fb56a7ffa2754386`. Pull request 5 (the secret store) was merged at 04:51:30Z. The hosted run of `main` is green: `total: 762` on both legs, skipped 4 on linux and 19 on windows, `RULES: clean (151 files)`, `HOSTED ...: PASS` from the corrected reader. No `Sessions` path exists on `main` (404 from the contents API; control: `src/Datasec.Suite.Secrets` answers). There is no `b1831` ref. I re-read the origin at 16:15:56: nothing had moved.
2. **One kit and one seat** (X18, branch `b1831/wp15-token-broker`, level opus, gate G1, window 240/180).
   - The seat builds `src/Datasec.Suite.Sessions` and `tests/Datasec.Suite.Sessions.Tests`, and adds two solution lines placed by `place.py` (after Server and after Secrets.Tests on `main` as it stands).
   - It adds no package and changes no workflow.
   - It uses the secret store only through `ISecretStore`, behind the lane's own `ISessionRecordStore` interface.
   - The real `ITokenRefresher` is out of scope; the seat writes a test fake only.
3. **THE N-4 READING, and where the design pulls.** The design agrees with the reading on holding tokens, persisting them encrypted, and refreshing "before expiry and on 401". Refresh means CALLING `ITokenRefresher`, whose real implementation is WP1.4's (Microsoft's library). The supporting text is `02:366`, the overlays `02:1225` and `02:1223` ("designs no new token handling"), and P-3 at `03:431` ("Microsoft issues and refreshes; we hold and present"). **It pulls at one point.**
   - `02:638` makes "token subject = session user" Workpath's rule [A1 §4.8].
   - Workpath's rule READS the token: `A1:245` says the token's `unique_name`, `upn` or `preferred_username` must equal the platform's user.
   - The revised design also says, at `02:1220` (about C7, not C6), that reading "the token Microsoft returns" "does not change the flow".
   - **The default (D9, Q1): the subject travels beside the token in the grant WP1.4 hands over, and the broker compares that.**
   - What this gives up: a caller that states the wrong subject is not caught.
   - Alternative A (the broker decodes the claims) is outside the reading, so it goes to the product owner on a card.
4. **A TOOL FINDING, outside this lane:** kit B1829's `hosted.py` cannot print PASS on any head built on today's `main`.
   - Measured on green `main` `bb914334`, it printed `FAIL 3`.
   - Two of those rows: it requires `succeeded: <total>`, but the secret store's tests skip 4 on linux and 19 on windows.
   - The third row: it fails the three code-scanning runs that sit beside the four ci jobs.
   - Lane C's READY head `48120e58` is based on `ddbdf800`, which is older than the secret store. If it is rebased onto `main` and checked again with its own copy, it will FAIL there too.
   - My copy adds `--skipped-linux` and `--skipped-windows`, and prints `CodeQL` / `Analyze (...)` runs without failing them. On `main` it printed PASS; with `--skipped-linux 5` it printed `FAIL 2` (the control).
5. **The two board lines are NOT in `CLARIFICATIONS.md`.** These are the 21:59:41 line ("mirror the flow") and the 22:04:02 line ("revise all docs"). I found 0 hits for each; the control `C-45` gave 1. The commission asked me to read them "at source in CLARIFICATIONS.md and the revised design". They stand only in the design: `02:1136`, `02:1141`, `03:598`, `03:603`, and the B1817 change list `:7`, `:12`. The kit quotes them from there. Adding them to `CLARIFICATIONS.md` is a job for a records pass.

## FACTS RE-MEASURED (instrument in brackets; 15:55 to 16:16)
- **Origin** [gh api -X GET, the project's GH_CONFIG_DIR]
  - `.private` true, push true.
  - Branches: main `bb914334`; the five wave-1 branches (all landed); `b1829/wp04-oxpd2-clients` `48120e58` (ahead 1, behind 1, its base `ddbdf800`).
  - Open pull requests 0; pull requests 1 to 5 all merged.
- **Main's tree** [tarball by GET]: 151 files. The solution file is 17 lines, sha256 `a94ad1ac...`. `ci.yml` is 199 lines, sha256 `c3894bbc...` (the same as at lane C's drafting). Lines 40/42/45/46/48 and 70/72/75/76/78, 192 (`FLOOR=53`) and 199 were re-printed.
- **The store's public surface** [cat -n at main]:
  - `ISecretStore` at lines 15/21/27/32; `SecretValue` mask `[secret]` (`:11`).
  - `MaxValueLength` 1048576 (`LocalSecretStore.cs:31`); `KeysFolderName` is internal (`:33`).
  - The name rule is at `SecretNames.cs:7`.
  - The store's tests use `LOCAL=user` on Windows (`TestRoot.cs:16`). The verdict of review B1824 (item 9, RELAYED) says the default descriptor was refused on the hosted runner. So the kit's cells use `LOCAL=user` and expect no skipped test of their own.
- **Ticket OXPD2-14** [own GET helper, credentials in-process, 16:04:47]: Backlog, 0 comments, parent OXPD2-4. Its description names "sessions, handles, refresh, events and expiry, unit tests and a restart test".
- **Reference pack 10.0.15** [grep -c of documented names, control 0]: `TimeProvider` (`GetTimestamp`, `GetElapsedTime`, `GetUtcNow`, `CreateTimer`), `ITimer`, `Task.WaitAsync(TimeSpan, TimeProvider, CancellationToken)`, `Base64Url`, `FixedTimeEquals`, `ZeroMemory`, `System.Threading.Lock`, `Utf8JsonWriter.WriteBase64String`, `Utf8JsonReader.TryGetBytesFromBase64`. Each is present once. Whether `TimeProvider` can be subclassed the way the test clock needs is UNMEASURED; the kit says to STOP if it cannot.
- **Package cache** [ls]: 64 entries. 0 match `timeprovider|identity.client|msal|microsoft.identity`; the control `xunit` matches 10.
- **Scanner shapes** [gitleaks 8.30.1, the workflow's four options, one file per row]: 11 rows. 9 are quiet; `jwt` fires on a JWT-shaped literal and `generic-api-key` on a 43-character base64url literal. Control: a token built from two halves gave rc 1.
- **Commit message**: subject 146 bytes, file 204 bytes, 3 lines. gitleaks rc 0; `words.py` printed `WORDS: clean (1 files)`; `--control` printed `CONTROL FIRED: 13 of 13`.
- **place.py on scratch copies**: on main's file it printed `PLACED: 2 lines (src at 8, tests at 16)`. With lane C's lines already placed it printed `src at 9, tests at 18`. On the placed file, `--dry` printed `REFUSED: already present`, rc 2 (the control). A CRLF file was refused (control).
- **Machine** [16:01:34]: load averages 0.96/1.37/1.42; 1004 GiB free; `.tools/` has no `b1831` and no lock folder; 0 OXPd2 panes out of 3.

## D-DECISIONS (all Tuesday's defaults; each has a Question, an alternative, a cost and a cell)
| D | Default |
|---|---|
| D1 | The token is opaque. |
| D2 | The key is ordinal ASCII. |
| D3 | A 32-byte base64url handle, OXPd 1.x only. Only its SHA-256 is kept, and it is bound to its device. |
| D4 | Lazy refresh at a read, margin 5 minutes. |
| D5 | Single-flight refresh with a 30 s bound on `TimeProvider`, plus acceptance rules. On failure the held grant is kept; another subject ends the session. |
| D6 | 256 KiB per token part. |
| D7 | Two clocks, and the earlier deadline wins. A record dated later than the clock is dropped at restore. No timer: `Sweep()` is for the host to call. |
| D8 | One session per device. |
| D9 | The stated subject, compared exactly. |
| D10 | The caller's idle timeout; no lifetime cap. |
| D11 | Restart window of 10 minutes (`02:639`). |
| D12 | One record per session through `ISecretStore`, named `sessions/<32 hex>`. |
| D13 | The activity write is at most once per 60 s. |
| D14 | Masks; the events carry no token, handle or subject. |
| D15 | Store failures: sign-in is refused; a refresh is kept in memory; a failed delete is retried and the call throws. |
| D16 | Events are synchronous; handler exceptions are dropped. |
| D17 | Nine typed reasons. |
| D18 | No logger, no `System.Net`, no package. |
| D19 | The build's code rules. |

The time rule follows the lesson of the B1806 verdict: a step of the clock never lengthens a life.

## Q-QUESTIONS FOR TUESDAY (defaults already assumed in the kit; S4 must answer Q1 in words)
| Q | Default |
|---|---|
| Q1 | The stated subject, read from no token (stop-class). |
| Q2 | Ordinal key. |
| Q3 | 32-byte handle. |
| Q4 | Lazy, 5 minutes. |
| Q5 | Single-flight, 30 s. |
| Q6 | 262144 bytes. |
| Q7 | Two clocks, no timer. |
| Q8 | One session per device. |
| Q9 | Exact comparison. |
| Q10 | Caller's idle timeout, no cap. |
| Q11 | 10 minutes. |
| Q12 | One record through the secret store. |
| Q13 | 60 s. |
| Q14 | Masks, no subject in events. |
| Q15 | The store-failure rules. |
| Q16 | Synchronous events. |
| Q17 | Nine reasons. |
| Q18 | The names. |
| Q19 | 240 and 180 minutes, X18. |
| Q20 | G1, with a second reader on F08, F09 and D9. |

## UNMEASURED
- Every build and test outcome.
- Whether the store's framework reference flows through T1's project reference.
- Whether `TimeProvider` can be overridden for the test clock.
- Microsoft token sizes.
- The forms of the subject that the platform and Microsoft's library each state.
- The hosted Windows leg under the lane's cells.
- Step 1's predicted totals: 762 plus the seat's tests, skipped 4/19 unchanged.

## CHAIN INPUTS (each produced earlier or present at BASE)
| Step | Inputs | Produced by or present at |
|---|---|---|
| 1 | gate folder; `<repo>`'s local identity; T1/T2 in the Step-0 copy | the drafter's scratch; at BASE; Step 0 |
| 2 | blocks | Step 1 |
| 3 | stubs | Step 2 |
| 4 | red cells | Step 3 |
| 5 | green tree | Step 4 |
| 6 | the staged tree, `words.py`, `commit-message.txt` | Step 5 and the gate folder |
| 7 | the commit; the base's skipped counts | Step 6; Step 1's `hosted.py` on BASE |

## THE CHECKS I RAN, AND THE CHECKS THAT ARE NEVER RUN
Each check I ran had a control that fired:
- the refuse slot count (8 on the unstamped kit; the control `STAMPED` counts 2);
- `place.py` and its refusal;
- `words.py --control`;
- `hosted.py` PASS on main and its FAIL control;
- the ASCII scan (0 on a clean file, 1 with a planted U+200B);
- gitleaks and its control;
- the pointers and quotes checkers.

Marked NEVER RUN in the kit: the owned-paths property; every heavy job through the runner; `hosted.py` on a head of this lane; the push.

## READING LOAD
The kit (105034 bytes) plus about 117 kB:
- `CLAUDE.md`, `CLARIFICATIONS.md` and `SETUP_RUNBOOK.md`;
- the clone's build files and `ci.yml`;
- six public files and the README of the store, plus `LocalSecretStore.cs` lines 1 to 110;
- the store's test csproj and `TestRoot.cs`;
- the six tool headers.

Measured total for those files: 105930 bytes, plus 5980 for the headers, plus 5212 for the store lines. **The kit is 5% over the wave-1 limit of "about 100 kB".** I did not cut it further: its D, Q and H sections are what earlier verdicts asked for.

## WHAT I DID NOT READ
- The design documents whole: only the cited lines, section 6.2's rows, section 6.4, D6, the B1817 overlay rows 1215 to 1235, P-3, N-4, E1.4 and E1.7.
- `05_readiness-to-build.md`, beyond one grep hit.
- The B1817 change list, beyond lines 7, 12, 24 to 26, 312 and 350 to 356.
- The analysis reports, beyond A1 section 4.8 and A1:464, and A7's token lines by grep.
- The secret store's source, beyond its public files and `LocalSecretStore.cs` up to line 40 and its member list.
- The B1829 kit's sidecar and its drafter report, beyond the first 4 kB of each.
- The kits B1786, B1810 and B1825.
- Lane C's branch code (only its solution file).
- Nothing of HPSM-POC, the NAS library or `Source_Documents/`. I opened no decision card.

## CORRECTIONS TO THE COMMISSION
- The two board lines are not in `CLARIFICATIONS.md` (BLUF 5).
- The B1829 tool set is not usable unchanged for any head on today's `main`: `hosted.py` FAILs (BLUF 4).
- "Read N-4's default as ..." is Tuesday's reading. The design's own C7 overlay (`02:1220`) treats reading a token as non-interfering, and the kit says so.

## OUTSIDE-THE-FENCES DISCLOSURE
I wrote only the kit, its sidecar, this report and files under `fleet/state/s304/d1831/`:
- `main.tar.gz` and its extract;
- `gate/` with 7 files: 4 copied unchanged, `place.py` and `hosted.py` changed, and a new `commit-message.txt`;
- `scratch/`, `logs/`.

Other actions to disclose:
- One `sed -i ''` on my own scratch file `jira_get.py`.
- One planted scanner control file in `scratch/glctl/`.
- `gh api -X GET` only. One Jira GET of OXPD2-14.
- No git verb in any project tree, no build, no test, no message.
