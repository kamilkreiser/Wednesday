STARTABLE: YES (on the stamp of Q1 = "a", the default the kit built and measured; the commission's own owned paths for lane IP are NOT startable: two landed cells forbid them, MEASURED)

# B1972 DRAFTER REPORT: lane IP (IPP transport over HTTPS), seat Datasec/OXPd2-X46

Drafter: Opus, read-only toward the project, Jira and GitHub, 2026-11-23 10:31 to about 11:20 AEDT (clocks by `date`: 10:31:45, 10:55:01, 11:03:05; the sidecar's first line holds its write clock). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1972_SEAT-X46_oxpd2-ip.md` (230 lines), sidecar `.measured` beside it (183 claims, `stamp_check.py` exit 0, 183 of 183 measured). Scratch and every program and log: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s315/d1972/` (below `<d>`); the seat's tools `<d>/seat-tools/` (10 files).

## BLUF
1. **The commission's path cannot land (MEASURED).** `src/Datasec.Suite.Jobs/Transport/**` compiles into the Jobs assembly, and two landed cells forbid network code there: `RulesTests.L04_the_library_references_no_network_logging_or_package` (`RulesTests.cs:237` to `:240`) and `SenderTests.J04_the_sender_only_talks_through_the_transport_interface` (`SenderTests.cs:92` to `:93`), plus the README's "no `System.Net.Http`, no `System.Net.Sockets`" (`README.md:112` to `:113`). Probe in `<d>/clone`: a five-line `HttpMessageInvoker`/`SocketsHttpHandler` class there gave `Total: 122, Errors: 0, Failed: 2` (both cells, `Assert.DoesNotContain() Failure`); BASE `Failed: 0`. The probe is quarantined at `<d>/_quarantine/probe-transport-in-jobs`.
2. **The kit's default (Q1 a): a new library project `src/Datasec.Suite.Jobs.Transport/`** (csproj, `HttpIppTransport.cs`, options, exception, README, lock file), referencing Jobs only, no package. **The Jobs test project gains one `ProjectReference`** (its csproj +1, its lock file +6 by the restore), so the cells live in the commission's own `tests/Datasec.Suite.Jobs.Tests/HttpIppTransportTests.cs` and **CI restores, builds and tests the new project with NO slnx line** (MEASURED: the root `restore`, `build` and `test` over the slnx reach it through the reference). This keeps the commission's slnx rule (L1 the only wave-1 owner) and starts now, not after L1.
3. **The transport:** POST `application/ipp` to the host, port and path of the printer address (`ipps://host:port/path`, port required, or `https://`); plain `ipp`/`http` refused before any connection; one pinned LEAF certificate (SHA-256 of the DER, `FixedTimeEquals`, chain not consulted, no accept-all); HTTP/1.1 exact; no proxy, no redirect, no cookie, no retry; a new connection per request; a chunked body written at most once; only a 200 `application/ipp` HTTP/1.1 answer handed back; one exception type, fixed messages, no address, port or pin in any text.
4. **Measured on macOS arm64 in a fresh clone with the frozen patches:** red tree (a permissive first shape) `total: 1839`, `failed: 18` (10 refusal cells, 18 cases, all by assertion); green `total: 1839`, `failed: 0`, `succeeded: 1835`, `skipped: 4`; `mutants_ip.py run` `MUTANTS: 10 of 10 MATCH, 10 of 10 undone equal`; locked restore and `--force` with 29 of 29 lock files equal; `RULES: clean (560 files)`; `Ran 111 tests`; `GUARD: clean (10 files)` / `(11 files)`; `CHECKS: 6 of 6 PASS`; gitleaks rc 0 (control rc 1); `WORDS: clean (2 files)`.
5. **The biggest hosted risk:** this is the first TLS listener any test of this repository runs (`git grep UseHttps` at BASE: 0 hits; control `Listen(IPAddress.Loopback` 1 hit). The Windows and Linux legs are PREDICTED only; the kit's platform line makes a one-leg red a STOP to Tuesday.

## Facts re-measured (instrument, control)
- Origin `main` = `da8d64a83bf9f58e4b02fa2c11526dd6a7c7261b` (clone.py draft listing, twice; no `b1972` ref; control `b1961/...` listed).
- BASE hosted run: `hosted2.py ... --total 1809 --rules 553 --skipped-linux 4 --skipped-windows 21 --unit 111 --floor 111 --hardened-scan` -> `HOSTED da8d64a83bf9f58e4b02fa2c11526dd6a7c7261b: PASS` (10:53:11).
- Jobs executable at BASE `Total: 122, Errors: 0, Failed: 0`; head `Total: 152`.
- `lsof -nP -iTCP:631 -sTCP:LISTEN` and `-iTCP:443` rc 1 each (the refused-address cells use port 9 of 127.0.0.1; at the red tree the permissive shape does try to connect there).
- CLARIFICATIONS grew during drafting (696 -> 720 lines, C-70 and C-71 added by the records seat); the kit cites C-71 (the 10:10 word) at line 718. Subject scan over the 720 lines: `transport` 0, `pinned` 0, `redirect` 0, `proxy` 0, `http/2` 0, `chunked` 0; control `tolerant` 5.
- `kam_rulings_today.sh` (10:34:52): 5 rows; nothing on IPP or the transport; OQ-6 found as the positive control (`datasec-oxpd-oq6-dev22-dev23-1123: a`).
- Lock files at BASE: 28, all without a final line feed (so `checks_ip.py` expects the same of the two lock files).
- The words scanner counts `linux-x64` / `win-x64` in a lock file as seat ids (2 hits when the lock files are kept); the kit leaves the two generated lock files out of the scanned added lines and says why.

## D-decisions (all Tuesday's defaults as coordinator, each a Q at the stamp)
D1 the new project (Q1, STOP-CLASS); D2 leaf-certificate pin, chain not consulted; D3 port and path in the printer address, not a separate setting; D4 one connection per request plus a body-once guard; D5 no proxy; D6 the transport's own exception (`JobServiceException`'s constructor is internal to Jobs); D7 one commit, rebase before the first push only.

## Q-questions for Tuesday (default first)
- **Q1 (STOP-CLASS):** a) the new project referenced by the Jobs tests (built, measured) / b) loosen L04, J04 and the README line (three files outside the commission's paths; gives up a landed boundary) / c) the Lab project after L1 (lab-only, so the product sender still has no transport) / d) REFUSED: `HttpWebRequest` inside Jobs (dodges L04's list; obsolete, a warning-as-error).
- Q2 the slnx line: none now; owed to the first lane that owns slnx after L1 (H by the commission's order).
- Q3 each lane its own pin check (L1's and this one); unify later.
- Q4 pin = the leaf certificate's SHA-256 (matches what L1's `probe` is commissioned to print) vs the public key's.
- Q5 one connection per request (a handshake per status poll) vs pooled with the body-once guard only.
- Q6 FOR RECORDS as written.
- Q7 Opus, READY at Step 0 + 110, push by + 80, pane X46, gate G1 round 1 of 2, hard stop 15:30.
- **Partition note for the stamp:** under Q1 a the lane's paths are `src/Datasec.Suite.Jobs.Transport/**` (new, claimed by no other kit; MEASURED by a grep of the three other wave-1 kits and B1976's X1 kit, which name only the commission's `src/Datasec.Suite.Jobs/**` wording for IP), `src/Datasec.Suite.Jobs/README.md`, `tests/Datasec.Suite.Jobs.Tests/{Datasec.Suite.Jobs.Tests.csproj, HttpIppTransportTests.cs, packages.lock.json}`. The TA and H kits describe IP's paths in the commission's words; no path overlaps either way.

## Chain inputs (every step's input exists at BASE or comes from an earlier step)
| Step | Inputs | From |
|---|---|---|
| 0 | the kit, the stamp (S4 holds Q1) | Tuesday |
| 1 | `<src>` (10 files), `<repo>`'s local values, the origin, BASE's push run | drafter's scratch; `<repo>`; GitHub |
| 2 | the files at BASE | Step 1's clone |
| 3 | `1-red.diff` | Step 1's tools copy |
| 4 | `2-fix.diff`, `mutants_ip.py`, the red tree | Steps 1 and 3 |
| 5 | the green tree, mutants undone and rebuilt; the ten paths staged in Step 5 itself before the lock hashes | Step 4 |
| 6 | the staged tree, `checks_ip.py`, `words.py`, `commit-message.txt` | Steps 5 and 1 |
| 7 | the commit, `origin/main`, `run_step.py`, `hosted2.py` | Steps 7 (a), 7 (b), 1 |

## UNMEASURED
- Every hosted leg on a head of this lane (Windows and Linux TLS with the test's reloaded PKCS 12 certificate above all).
- `run_step.py`'s neutral scan on a commit of this lane; `clone.py` in seat mode; the push; the rebase.
- What his M577 (FutureSmart 5) and any FutureSmart 6 printer answer: the IPP port and path, chunked bodies, HTTP authentication.
- Whether a platform runs the validation callback again on a TLS renegotiation.
- Whether .NET would route a loopback request through `HTTPS_PROXY` if `UseProxy` were true (so the proxy shape is a named limit, not a cell).

## Outside-the-fences disclosure
- Network: two `git clone` reads of the origin into my scratch (`clone.py ... draft`, push URL `invalid://no-push`, no identity); `gh api -X GET` reads by `hosted2.py` under the project's `GH_CONFIG_DIR`. No Jira call, no Azure, no HTTP to any other host; the tests talked only to their own stubs on 127.0.0.1 (and the red tree's permissive shape to 127.0.0.1 port 9).
- Heavy jobs: about 40 dotnet jobs and test runs, every one through `heavy.py` and the shared wave lock (waits 0 to 25 per job); one mutant run went to the background in my own session and was awaited, never run twice at once. I never broke or touched another holder's lock.
- Writes: only my kit, its sidecar, this report, and files under `<d>` (two scratch clones whose index I used: `git add -A` and `git add -N` there, never in a project checkout). The first sidecar skeleton was moved to `<d>/_quarantine/` before a re-init (never deleted).
- Shell: no `cd`. A few read-only calls chained two or three simple reads with `;`, and one piped a grep into `cut` (an advisory hook noted it; the presence it showed was then confirmed by counts). No guard or hook refused anything.
- Read: the project's CLAUDE.md, CLARIFICATIONS.md, BACKLOG.md (counts only), two design documents (grep of named lines), the commission, the sweep, the needs list, the form kits; never `Source_Documents/`, a key folder, the NAS, or another project.
