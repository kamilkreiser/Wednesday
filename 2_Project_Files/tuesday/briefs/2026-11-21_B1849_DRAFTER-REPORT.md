STARTABLE: YES - the kit can be stamped and launched against main 0804860b now. Q1 is STOP-CLASS and Stamp S4 must answer it in words: the landed contract tests forbid the adapter any project reference, so the default keeps the refresh value out of `ISecretStore` until the host binds the lane's own vault interface. That departs from the plan's "kept only through `ISecretStore`".

# B1849 DRAFTER REPORT | wave 3, lane E | Datasec / OXPd_2 WP1.2 in part (the OXPd 2 adapter beyond its generated clients)

Drafted 2026-11-21, 18:25 to 18:47 AEDT (clocks by `date`), by a read-only Opus drafter for Tuesday. Files: kit `2026-11-21_B1849_SEAT-X25_oxpd2-wp12-adapter.md` (122655 bytes, 383 lines, ASCII), sidecar `.measured` (243 claims, 243 measured; `stamp_check.py` exits 0), this report. Scratch: `fleet/state/s305/d1849/`. It holds the lane's `gate/` (seven files), a draft-mode scratch clone of the origin that cannot push, the hosted-run logs of main and their two controls, the gitleaks rows, `pointers.py`, `sidecar.py`, `owned_check.py`, the frozen blocks and the slnx copies.

## BLUF
1. The kit adds code to the EXISTING project `src/Datasec.Suite.Adapters.Oxpd2` in two new folders, both outside `Generated/`, and adds ONE new test project:
   - `Device/` holds a per-device solution-token holder and a `DelegatingHandler`. The handler attaches a bearer header. On a 401 it refreshes once, with one refresh in flight per device, and retries once. A second 401 sets `NeedsRepair`. A rotated refresh value is written to the vault before it is used.
   - `Callbacks/` holds a per-device callback credential (43 base64url characters; only its SHA-256 is kept; it is checked with `FixedTimeEquals` and a dummy compare for unknown serials). It also holds one dispatcher for five printer callbacks. The dispatcher checks the credential before reading any body byte, does a bounded read, parses only through `Oxpd2Json.TryParse`, applies a stale-read guard on HID card sequences, calls the sink under a deadline, and type-checks and re-parses the answer.
   - Changes to existing files: one slnx line (`tests/`, placed first, before `Cards.Tests`) and one `InternalsVisibleTo` line. No package, no project reference, no workflow change.
2. **The main finding came from reading the landed `tests/Datasec.Suite.Contracts.Tests/` at 0804860b.** Those tests run reflection over the WHOLE adapter assembly, so they bind lane E's code even though the folder is not lane E's:
   - The adapter project file may hold no `ProjectReference` (`ClientTests.cs:432`, `:436`). So the adapter cannot reference the secret store. This drives D1/Q1.
   - No public parameter may be named `token`, `accessToken`, `authorization`, `bearer` or `credential` (`:351`).
   - No static field may be writable, compiler-made types included (`:421`, no skip). So the product code may contain no lambda and no method-group conversion. That is DERIVED from the compiler's lowering and not measured on SDK 10.0.404; cell N02 and mutant mLambda settle it.
   - The assembly may not reference the web host, identity or logging libraries (`:403`).
   - Public static lists must be read-only (`ReadOnlyListTests.cs:77`).
   - Nothing may be added under `Generated/` (`RegenerationTests.cs:38`).
   - The summary of that control even reads "the token, its refresh and the callback check are another package's" (`ClientTests.cs:348`).
3. **Three corrections to the wave-3 plan (all MEASURED):**
   - (a) There is no inbound operation for "solution notifications". The catalogue has 12 operations over five targets, and `ntAuthCode`/`ntDeviceBoot`/`ntWalkup*` appear only in the Solution Manager's outbound enum. So they are OUT.
   - (b) "Kept only through `ISecretStore`" collides with the boundary test (D1).
   - (c) The device's token endpoint is in none of the 37 in-repo specifications. They hold 198 paths, and only one has `token` in its name: the dev-only `sdkSupport` `/functions/solutionToken`. So the refresh call is an interface with a test fake only.
4. Form: B1841's kit shape, with these differences:
   - B1835's `hosted.py` (`--unit`/`--floor`), because R5 may land and move `Ran`/floor to 60.
   - `place.py` cut down to one line.
   - The pre-push rebase rule with the slnx-only recipe. It adds a STOP if the new main touched the adapter csproj, `Generated/`, the generator or `Contracts.Tests`.
   - `repo_rules.py` run without `--source-documents`.
   - 30 minutes of lock waits allowed (READY at Step 0 + 270, push by + 210).

## Facts re-measured, with instruments
- Origin (`gh api -X GET`, project `GH_CONFIG_DIR`, 18:25:57 and 18:36:59):
  - main is `0804860b8993f6d7fd393cb64c44afcd2f9c8f05`. PRs 1 to 7 are merged (PR 7 at 07:10:03Z); 0 open; 0 open code-scanning alerts.
  - Branches b1831, b1832 and b1836 are not landed. There is no `b1849` ref.
  - `.private` true; `.permissions.push` true.
- The hosted run of main, by `hosted.py` (18:29:48): `HOSTED 0804860b...: PASS` with `--total 899 --rules 293 --skipped-linux 4 --skipped-windows 19 --unit 53 --floor 53`. Controls: `--skipped-linux 5` gives `FAIL 2`; `--unit 60 --floor 60` gives `FAIL 2`. Secret-scan wordings: `25 of 25`, `objects of this commit not among them 0`, `no leaks found` x3.
- Scratch clone (`clone.py ... draft`, push `invalid://no-push`):
  - `git ls-files` gives 293.
  - `repo_rules.py` (no flag) gives `RULES-NOTE: R5 hash half NOT RUN (no supplied-source folder here)` and `RULES: clean (293 files)`, rc 0. No supplied-source folder sits beside the scratch clone (`test -d` rc 1; the control on the project's folder gives rc 0).
  - `unittest discover -s build/tests` gives `Ran 53 tests`, `OK`.
- `place.py` (lane E copy; diff against B1841's is 13 lines):
  - On main's slnx (19 lines, sha256 `765755d6...`): `PLACED: 1 line (tests at 12)`. The folder is ordinal before and after.
  - After `--write`, `--dry` gives `REFUSED: already present: ...`, rc 2.
  - On lane A's branch slnx: tests at 13. On a CR LF file: `REFUSED: not LF with a final newline`, rc 2.
  - The placed file is 20 lines, 1325 bytes, sha256 `f15a35f2...`.
- `words.py --control`: `CONTROL FIRED: 13 of 13`. The commit message (186-byte subject, 3 lines, 244 bytes) gives `WORDS: clean (1 files)`. Sample identifiers are clean, and `round 2` counts.
- Adapter project file at main: 5 lines, 141 bytes, sha256 `ff23cd00...`. It holds only `InternalsVisibleTo Datasec.Suite.Contracts.Tests`. The server references only Core, so the release-guard counts cannot move.
- Inbound surface (program over the two service-target files and the catalogue):
  - The five handled operations map to `PrePromptResult`, `PostPromptResult`, no body, `RegistrationResponse` and `OperationCallbackResponse`.
  - The five service-target files declare no security scheme. The device services use bearer `e2-claims` (JWE).
  - Sensitive fields: `SessionAccessToken` (Auth `Models.cs:106`, `:159`), HID `Data` (Usb `Models.cs:25`), `AccessToken` (Usb `:14`, `:40`), `password` (Auth `:282`).
- Parser at main: `Oxpd2Json.TryParse<T>` is public (`Oxpd2Json.cs:21`). The limits default to 1048576 bytes and depth 32 (`Oxpd2ParseLimits.cs:10`, `:13`), and the parser expects "the caller has already bounded" the read (`:6`). The generated clients add no credential (`Oxpd2ClientCore.cs:6`).
- Reference pack 10.0.15, one name each (control 0): `FixedTimeEquals`, `ZeroMemory`, `SHA256.HashData`, `RandomNumberGenerator.GetBytes(Int32)`, `DelegatingHandler`, `AuthenticationHeaderValue`, `TimeProvider`, `Base64Url.EncodeToString`/`IsValid`, `CancellationTokenSource(TimeSpan,TimeProvider)`, `Task.WaitAsync(TimeSpan,TimeProvider,CancellationToken)`, `Task.Delay(...TimeProvider...)`, `HttpContent.LoadIntoBufferAsync(Int64,CancellationToken)`.
- Package cache: 64 entries. There is no `microsoft.aspnetcore.testhost`; the only `testhost` match is `microsoft.testplatform.testhost`, and 10 entries match `xunit` (control). This lane needs none of it.
- gitleaks 8.30.1 with the workflow's options, 12 synthetic shapes:
  - Only a random 43-character base64url literal and a random 64-hex literal fire (`generic-api-key`).
  - Quiet: the `Bearer synthetic-...` header literal, `sessionAccessToken` JSON, `AccessToken =`, `Password =`, a base64 card read and `AuthenticationHeaderValue`.
- Pointer table: 26 fragments on their lines (`pointers.py`); control False. `02` is 1276 lines and `03` is 667.
- Toolchain: 10.0.404; gitleaks 8.30.1.
- Machine: load 10.94 (other seats were building); 1002 GiB free. There is no `.tools/b1849` and no lock folder. Panes X23 (lane G), X20 (SL) and X18 (D) are live.
- Drafter prototype, in the scratch clone only, never committed or pushed: T1, T2, one placeholder `.cs` and the slnx line, staged. Results:
  - 6(a) name-status is 2 M plus A rows only; numstat is 1/0 for each M; `--quiet` over the forbidden paths gives rc 0, and the control on the slnx gives rc 1.
  - My owned-paths checker gives PASS. With a planted `M .../Generated/Runtime/Oxpd2Json.cs` row it gives FAIL (control FIRED).
  - `repo_rules.py` gives `RULES: clean (295 files)`. `words.py` over the added lines plus the commit message gives `WORDS: clean (2 files)`.
  - T1 has 0 `PackageReference|ProjectReference` (the landed C8 predicate).

## Chain inputs (DRAFTER_RULES MEASURED LITERALS item 4)
| Step | Needs | Produced by |
|---|---|---|
| 0 | the stamped kit, CLARIFICATIONS, design lines | BASE (Tuesday's stamp) |
| 1 | gate folder, clone, constraint files at BASE, frozen blocks, slnx, base hosted numbers | the drafter's `gate/` (exists); `clone.py`; the Step-0 copy; `hosted.py` |
| 2 | T1, T2 | Step 1 extraction |
| 3 | projects and stubs | Step 2 |
| 4 | red cells (Contracts.Tests green) | Step 3 |
| 5 | green tree | Step 4 |
| 6 | staged tree, `commit-message.txt` | Step 5; gate |
| 7 | commit; base hosted numbers (re-read after any rebase) | Step 6; Step 1 |

## D-decisions (all Tuesday's defaults as coordinator, each one a Question)
- D1: the code goes in the existing project with the lane's `IDeviceSecretVault`, which mirrors `ISecretStore`'s Put/TryGet/Delete, and no reference.
- D2: obey the landed contract tests.
- D3: vault names `oxpd2/solution-refresh/<sha256-hex(serial)>` and `oxpd2/callback-hash/<...>`; the serial rule is 1 to 64 of `A-Za-z0-9._-`.
- D4: a lazy refresh, one refresh plus one retry on a 401, then `NeedsRepair`, with every later call refused until a new refresh value is stored.
- D5: the endpoint is an interface (a null grant means refused, which sets repair; a throw is transient); 30 s bound.
- D6: store the new refresh value before using the new access value.
- D7: refuse a request that already carries `Authorization`; buffer up to 1 MiB for the replay.
- D8: 43 characters, only the hash stored, rotation by re-issue.
- D9: `Bearer` in any letter case, one space, `FixedTimeEquals`, a dummy compare, one `false` for every failure; a vault failure is reported apart.
- D10: the host supplies the serial and the credential binds it; no source address is used.
- D11: five operations; everything else is `NotHandled`.
- D12: check order: credential, operation, content type, read, parse, guard, sink, answer.
- D13: 1 MiB, depth 32, a 30 s read bound; the declared length is never trusted.
- D14: the landed parser only; refusals of an unknown enum or a null are kept.
- D15: per (serial, context) strictly increasing `HidReadSequence`; reset on `usbClosed`; memory only; cap 16384.
- D16: 5 s answer deadline, no fallback answer, the answer type-checked and re-parsed, at most 1 MiB.
- D17: monotonic clock only, no timer.
- D18: masks and fixed messages; no log.
- D19: no lambda or method group, no static state, no I/O, no sockets.
- D20: 13 outcomes and 5 token reasons. How `HttpClient` passes a handler's exception is settled by cell T10, or the seat STOPS.

## Questions for Tuesday (each with its default; STOP-CLASS marked)
- **Q1 STOP-CLASS:** the existing project, the lane's vault interface, no reference; the host binds it to `ISecretStore` later. Alternative A is a new project `src/Datasec.Suite.Adapters.Oxpd2.Device` referencing Secrets: a partition change, and the kit must be re-drafted. Alternative B is an edit of the landed C8 test, which is not lane E's.
- Q2: obey the landed tests.
- Q3: hashed-serial vault names.
- Q4: lazy refresh, one refresh, `NeedsRepair`.
- Q5: endpoint interface, null means repair, 30 s.
- Q6: store first.
- Q7: refuse a carried header; 1 MiB replay.
- Q8: 43 characters, hash only.
- Q9: Bearer and `FixedTimeEquals` (Basic is the alternative).
- Q10: serial from the host.
- Q11: five operations (all ten JSON operations is the alternative).
- Q12: credential first.
- Q13: 1 MiB, depth 32, 30 s.
- Q14: landed parser, refusals kept.
- Q15: per-context guard, 16384.
- Q16 (the plan's Q2): 5 s, no fallback, answer checked.
- Q17: monotonic.
- Q18: masks.
- Q19: 13 outcomes, 5 reasons.
- Q20: the names, G1 with a second reader on D4, D9 and D12, 270/210, pane X25.

Not decided by the kit (none defaulted):
- (1) Who binds the vault and the endpoint (host wiring; the plan's Q7 default is no).
- (2) How the host learns the serial: a route segment or `$DEVICE(ID)$` (Monday's test plus onboarding).
- (3) Solution notifications: no inbound shape in the repository; the `ntAuthCode` delivery depends on it.
- (4) For the product owner: B1830 F5, tolerant reading of an unknown enum value or a null after a firmware change.
- (5) Device/HP-facing items: the deadline, what a device does with a refused or late answer, whether rotation invalidates the old refresh value, and the scope of the card-read sequence.
- (6) The plan's Q3 (C-24 against OQ-2) stays out.
- (7) No customer-facing word.

## NEVER RUN (STOP-severity checks of the kit not run on a real output of this lane)
- The owned-paths property, the 6(a) name-status and numstat checks, and the word scan. The drafter ran each on a placeholder prototype tree only: PASS, control FIRED.
- The boundary scan 6(e).
- The neutral object scan of a lane commit.
- The whole heavy chain through `heavy.py`: restore, build, test, publish, `release_guard`.
- Every cell and every mutant, including T10 (HttpClient and handler exceptions) and N02 (compiler caches).
- `hosted.py` on a lane head.
- The rebase recipe on a moved main.
- `place.py --write` in a real seat clone. It was run on scratch copies only.

## UNMEASURED
- The build of T1/T2.
- Whether the C# compiler's lambda caches are writable static fields on 10.0.404 (DERIVED that they are).
- How `HttpClient` passes a `DelegatingHandler` exception.
- Every hosted figure of the lane's head.
- Everything about a device: the `Authorization` form it sends, how it names itself, its deadlines, the scope of its card-read sequence, what it does with refused or late answers.
- The device OAuth endpoint and its answers.
- The test total.

## What I did not read (disclosure)
- Kits B1829, B1831, B1835 (beyond its hosted.py and REBASE lines, found by grep), B1840, B1842 and the other wave-3 kits were not read whole. B1841 (the stamped kit, its pre-stamp diff and its drafter report) was read whole.
- The wave-1 and wave-2 drafter commissions were not re-read. Their binding rules reached me through B1832-B1837's FORM AND RULES, which I read whole along with DRAFTER_RULES.md.
- B1837's plan was read whole.
- `02` and `03` only on the 26 pointer lines, plus `02` lines 248-252, 598-626 and 793-812. CLARIFICATIONS only by grep (C-42, C-45, C-51 lines). The B1830 VERDICT only its F5 row.
- Generated code beyond Runtime, Targets models (by grep), SecurityClient, SolutionManager auth models (by grep). The 37 HP specification files in the repository only by program (paths, security schemes, service-target request/response refs).
- Lane D's code, `05`, BACKLOG, any verify folder but B1830's VERDICT rows.
- Nothing of `Source_Documents/`, the NAS library, any key folder, HPSM-POC or another client.

## Outside the fences
- I wrote nothing outside my three files and `fleet/state/s305/d1849/`.
- The scratch clone is mine (draft mode, push URL `invalid://no-push`, no identity copied). In it I created a local branch `proto/b1849-draft` and staged a placeholder tree. Nothing was committed or pushed, and it was never in a project tree.
- No git write in any project tree, no build or test (`repo_rules.py` and `unittest` ran over my scratch clone only), no Jira, no message. `gh` was used with GET only.
- One hook refused a `git switch` written with a shell variable in its path. I re-ran it with the literal scratch path inside TUESDAY.
- The gitleaks rows G07/G08 hold random values made by program in scratch. They were never printed and are not secrets.

## Reading load
- Seat: the kit (122655 bytes) plus 174219 bytes over 33 files or line ranges (sidecar `LOAD`), plus about 14 unique design lines. That is 296874 bytes, about 74,000 tokens.
- The kit is over the wave-1 guide of "about 100 kB" by about 23 kB (B1841 was 107973). The extra is mostly the landed-constraint material (D2, N01-N03) that this lane alone needs.
- Drafter's own load: the commission (5914), the plan (31441), the B1832-B1837 commission (10255), DRAFTER_RULES (17216), the B1841 kit (112831) and its report (8922), plus the code and design excerpts above.
