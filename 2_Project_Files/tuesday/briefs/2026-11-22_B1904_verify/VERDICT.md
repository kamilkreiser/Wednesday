GATE B1904: GO WITH FINDINGS @ 94fe606 on main 185b9ee

Gate G1, round 1, first reader (whole lane). OXPd 2, lane F: WP4.1 in part, the Universal Print registration
material (kit B1840 as stamped, seat X22), head `94fe606749e25ba7818aef3fb6a19867c68103b5` on branch
`b1840/wp41-certificate-custody` (two commits: `f4cee23b`, then the ONE fix commit `94fe6067`); main
`185b9eef28f8ecbd87e92c6ae6cbe1025468c3e9`. Read and measured 2026-11-22, 18:46 to 19:05 AEDT (clocks by `date`), on
Opus 5.5, in my own clone (session scratchpad `b1904only/clone`, made by the kit's `clone.py ... draft`: push URL
`invalid://no-push`, no identity) and two detached worktrees of it (`wt-probe`: the head plus my probe file;
`wt-stub`: the head with stubbed product bodies). Origin by `gh api -X GET` under the project GH_CONFIG_DIR: branch =
94fe6067, main = 185b9eef, open pull requests 0, `compare main...94fe6067` ahead 2, behind 0, 27 files (Tuesday's
figures). Tools: the six files of `fleet/state/s308/d1898/gate/` copied, six of six equal to the kit's sha256;
`words.py --control` `CONTROL FIRED: 13 of 13`. Every heavy job (26) went through the kit's `heavy.py` UNCHANGED
(sha256 `31adedc8...`): load1 first, the wave lock by `mkdir`, released by a move into my scratch
`_quarantine/locks/` (26 folders there; the project's lock folder absent at the end). `repo_rules.py` never got
`--source-documents`; nothing under `Source_Documents/` and no key folder was opened, listed or hashed; every key,
certificate and token synthetic and made at run time, none printed. No write to any project, GitHub or Jira; no
`az`, no deploy, no message. I did not read the second reader's folder. Evidence in `evidence/`.

**BLUF.** The lane meets THE CONTRACT, D1 to D20 and Stamp S4's answers (Q7 and Q20 as worded). Scope is exactly
the owned paths: T1 byte for byte, the lock rule PASS over the four files with two controls firing. I reproduced
RED FIRST independently (my own stubs: 54 of 54 red), the green suite (1578, 0 failed, 4 skipped), the hosted PASS
(control FAIL 2), and the first head's Linux red as the seat described it. 12 mutants of my choosing: 8 red on their
cells, 4 green, each green one a known or now-recorded test gap with the code right today. My 9 probes found NO
certificate accepted that the property refuses (4527 tampered certificates, 0 accepted, 0 other exceptions) and no
key in a discarded buffer, but TWO holes outside the kit's list, both Minor: a removal that lands during an attach
leaves the record (key and certificate) back in the store (F1), and an issuer that blocks before returning its task
is not bounded by `IssueTimeout` (F2). Neither is a NO GO class (no key in clear, no certificate accepted, no cell
weakened, no red, no scope breach, no false claim of a listed shape); both are owed before the work that wires
removal (WP4.5) and the real issuer. The fix commit swallows nothing that should surface and accepts nothing new. The
seat's two deviations and FOR TUESDAY 4 (a) to (g) are acceptable. Landing texts written. Can it land? Yes, once
B1905 also reads GO or GO WITH FINDINGS; main has not moved.

## Findings

| # | Severity | Finding | Recommendation |
|---|---|---|---|
| F1 | Minor (a hole outside the kit's list; key custody) | **`DeleteRegistration` is not serialised with `AttachCertificate`.** The attach lock (D19) covers the read, the checks and the write of an attach; the delete does not take it. Probe G01 (a store wrapper that pauses the attach's `Put`): `DeleteRegistration` returned **true**, the paused attach then completed **accepted**, and afterwards `uprint/<id>` was in the store again (`recordInStoreAfter=True`, `TryGetCertificate` true, 1 name): the private key and the certificate of a removed registration, at rest under the store's encryption. The REQUIRED SECTION's property says "never a record of a removed registration left in the store"; this concurrent shape is not among H1 to H27 (H19 is the token holder's removal), so it is a shape the seat had to cell or name, and the README names only the two-instance limit. Not NO GO: the key is not in clear, the caller of removal (WP4.5) does not exist yet. | One line: `DeleteRegistration` takes `_attachSync`; plus a cell X02 (delete during a paused attach: no record afterwards; the attach reads `NotFound` or the delete follows it). In a fix round if B1905 calls one; else a follow-up owed before WP4.5 calls `DeleteRegistration`. FOR-RECORDS item 1. |
| F2 | Minor (a hole outside the kit's list) | **An issuer that blocks before returning its task is not bounded.** `RunFlightAsync` calls `_issuer.IssueAsync` on the first caller's thread, and the `WaitAsync(IssueTimeout, ...)` bound starts only on the task it returns. Probe G02: an issuer that blocks synchronously, two callers of one id, the monotonic clock moved 120 s past the 30 s bound: neither caller finished while it blocked; both got the token after release; 1 issuer call. The property says "never a hang beyond `IssueTimeout`"; H16 covers only an issuer that hangs asynchronously. The real issuer (an HTTP call, later work) is UNMEASURED in this respect. | Start the issuer call off the caller's path (for example on the thread pool) so the bound covers a blocking issuer; a cell T11. Follow-up owed before the real issuer lands. FOR-RECORDS item 2. |
| F3 | Records (test gaps; code right today) | Four of my mutants leave every cell green: **mNoZeroPkcs8** (`CreateRegistration` no longer clears the PKCS#8 export: D2 has no cell for its clearing), **mReadCertLoose** (the record reader no longer re-checks a held certificate: no R-row puts a record whose `certificate` member is not a certificate), **mCatchNarrow** (the chain catch back to `CryptographicException`), **mFixUndone** (the field reads' catch made to rethrow, i.e. the first head's behaviour). The last two are expected on macOS: the late parse is OpenSSL's, and only the hosted Linux leg's C01 holds the fix (MEASURED: head 1 red there, head 2 green). | Backlog; FOR-RECORDS item 3. |
| F4 | Records | Measured by me on macOS arm64 (the seat had RELAYED H25 and H26): a trusted-issuer leaf marked **CA:TRUE is accepted**, one with an unknown critical extension is `IssuerNotTrusted`, one with extended key usage server-authentication only is **accepted**, one with no extension is accepted; H26 holds (first form put back: no certificate, a second good one accepted, version 4); two instances over one store both attach in 20 of 20 runs (the README's named limit); a throwing key factory lets `CryptographicException` leave `CreateRegistration`, nothing stored (the seat's 4(f)); an issuer that answers an already disposed token is held and handed out as zeros (G03). | Records items 4 and 5; the pull request body states the extension limit. |

No Blocker, no Major.

## What I re-ran, and the results

**(1) The diff against THE CONTRACT, D1 to D20, Stamp S4, and the owned paths.** Read whole: every product file
under `src/.../Registration/` (12 `.cs`, README) at the head, the fix diff `f4cee23b..94fe6067` (3 files, +50 -7),
and the test helpers (`StoreRoot`, `RegistrationSupport`, `FakeIssuer`, `TestClock`) and the C01 to C06, L03 cells.
- Public surface = THE CONTRACT's names and signatures (`RegistrationId`, `RegistrationRequest`, `IRegistrationKeys`,
  `RegistrationKeys` with one internal key-factory constructor, `RegistrationKeysOptions`, `CloudDeviceToken`,
  `ICloudDeviceTokenIssuer`, `CloudDeviceTokenHolder` with `Invalidate(id, refused)`, `CloudDeviceTokenHolderOptions`,
  `RegistrationException`, `RegistrationError` 1 to 13 in D13's order). Q20 (a) and (b) as worded: the four `Cloud`
  names; `Invalidate` drops the held token only when `refused.Origin` is that entry and its generation is the held
  one (`CloudDeviceTokenHolder.cs:157`).
- D6 order in `AttachCertificate` (`RegistrationKeys.cs:86-143`): (1) id, (2) empty then cap before any parse,
  (3) read under the lock, (4) attached, (5)+(5b) `LoadExact`, (6) SPKI byte-equal, (7) wall clock inclusive in UTC,
  (8) chain; write last. D7 (`:186-223`): empty issuer set returns false; `CustomRootTrust`; `CustomTrustStore` =
  the copied issuers; `NoCheck`; `DisableCertificateDownloads = true`; `VerificationTime` the library clock; no
  `ExtraStore`; every `ChainStatus` `NoError`; `ChainElements.Count >= 2`. Q7 as worded in S4. D5's reader is strict
  (format 1, each member once, no other, nothing after, id equal, key 2048 bits imported, certificate re-checked).
  D11: monotonic only (`GetElapsedTime`), 0.9, `WaitAsync(IssueTimeout, TimeProvider)`, late answers disposed.
  D12, D13, D14 as worded; no public member returns key material (my reading agrees with L02).
- **T1 byte for byte**: extracted by program from the stamped kit (8 lines, 264 bytes, sha256 `6cb8b5a1...`, = FACT
  7) and equal to the head's project file; `--numstat` 3 0. **The owned-path property**: 27 files = 22 `A` under the
  two `Registration/` folders + exactly 5 `M` (the project file and the four lock files); every forbidden path
  (`Ipp`, the store and its tests, `slnx`, `Directory.Packages.props`, `.github`, `build`, `README.md`, `global.json`,
  `Directory.Build.props`, `NuGet.config`, `.gitignore`, `.editorconfig`, both Jobs project files, the test project
  file) `diff --quiet` rc 0 (control: the library's project file rc 1); the 12 existing test `.cs` files rc 0 by
  `:(glob)` (12 files matched by `ls-files`).
- **The lock rule** (`evidence/lockrule.py`, my own program over `git show` of base and head): exactly the four files
  change; every target of each (`net10.0`, `/linux-x64`, `/win-x64`) has equal package entries (0/0, 17/17, 2/2);
  the only added entry `datasec.suite.secrets` (Project), the only changed `datasec.suite.universalprint` (Project,
  gaining `Datasec.Suite.Secrets`); `LOCK RULE: PASS`. Controls: `datasec.suite.secrets` struck from the allowed
  names `FAIL 4`; a planted package row `FAIL 2`.
- Boundary (`evidence/boundary.py`, over the head's blobs): 12 code files, 22 banned words 0 hits, 3 required
  present; controls 25 of 25 fired; string literals of the added lines (327) hold 0 high-variety 32/64-hex or 43+
  base64 (control: a random 32-hex literal made at run time counted 1); 0 key or certificate files; 22 added files
  ASCII, LF, final newline, no tab, no CR. `words.py` over the 3634 added lines and both commit messages:
  `WORDS: clean (3 files)`. Both commits' author = committer, the project's domain (compared in process).

**(2) Re-run in a scratch clone of the head** (project SDK 10.0.404 through `heavy.py`, closed proxy, the project's
package cache, `-p:NuGetAudit=false`; load1 1.1 to 6.8, waits 0 except one job of 14 polls):
- `restore` rc 0 and no file changed; `CI=true restore --locked-mode --force` rc 0, no file changed; `build -c
  Release --no-restore` `0 Warning(s)`, `0 Error(s)`; `test -c Release --no-build` (whole suite, no filter): **total
  1578, failed 0, succeeded 1574, skipped 4** (`evidence/summary-test.txt`).
- **RED FIRST against my own stubs** (`evidence/stubs.py`, worktree `wt-stub`): the bodies of `CreateRegistration`,
  `AttachCertificate`, `TryGetCertificate`, `DeleteRegistration`, `GetAsync`, `Invalidate`, `Remove`, both
  `Dispose`, `TryParse` throw `NotImplementedException`. First run: 51 of 54 red; green: L01's constructor cell (my
  stub kept the constructors' checks), L03 and L04 (green against throwing stubs, as the kit says). With the
  constructors' checks removed and the named first versions of L03 (a static `System.Net.Http.HttpClient` field) and
  L04 (a static settable field) added: **54 of 54 red, total 1578** (`L03: System.Net.Http`, `L04:
  RegistrationKeys.s_writableProbe`; `evidence/summary-stub-test3.txt`).
- `python3 -I build/repo_rules.py '<clone>'` (no option): `RULES-NOTE: R5 hash half NOT RUN (no supplied-source
  folder here)`, `RULES: clean (500 files)` (`ls-files` 500); `build/tests`: `Ran 111 tests`, `OK`. gitleaks 8.30.1
  with the workflow's options over the clone: rc 0 (control first: a value built by program from two halves in a
  scratch folder, rc 1).
- `git merge-tree --write-tree 185b9eef 94fe6067` rc 0, tree `de9817fc...` = the head's tree.

**Mutants of THE CONTROLS I chose** (`evidence/mutants.py`, `mutants.out`; each a program edit of PRODUCT code in my
clone, `dotnet test -c Release` whole suite as one heavy job, undone by writing the original back and proved by
`git diff --quiet` rc 0; reader's run):

| Mutant | Change | Result |
|---|---|---|
| mChainOff | rule (8) never refuses | RED: C01, C06, C08, C11 x2, C13, L01 (7) |
| mStrict | rule (5b) never refuses | RED: C01 |
| mEmptyTrust | no issuer configured passes the chain | RED: C08, C11, L01 |
| mChainLen | one element enough | RED: C13 |
| mKeyMatch | rule (6) never refuses | RED: C05, C06, L01 |
| mDeleteKept | delete does not delete | RED: C10, K03, R04, X01 |
| mInvalidateAny | `Invalidate` drops any copy's token | RED: T03, T09 x2 |
| mTimeoutOff | `WaitAsync` bound infinite | RED: T06 x2 (by the 10 s guard), L01 |
| mFixUndone | the field reads' catch rethrows (head 1's behaviour) | GREEN on macOS (expected: hosted Linux C01 is its red, MEASURED on head 1) |
| mCatchNarrow | chain catch back to `CryptographicException` | GREEN (no cell; refusal-safe either way) |
| mNoZeroPkcs8 | the PKCS#8 export not cleared | GREEN (test gap, F3) |
| mReadCertLoose | the reader skips the held certificate's check | GREEN (test gap, F3) |

After the last undo: `git status --porcelain` 0 lines.

**My own probes** (`evidence/ReaderProbeTests.cs`, scratch only, never pushed; one whole-suite run 1587, 0 failed;
outcomes in `evidence/probe-results.txt`):
- G01 delete during a paused attach: delete true, attach accepted, record back in the store (F1).
- G02 an issuer that blocks before returning its task: both callers held past 120 s of a 30 s bound (F2).
- G03 an issuer that answers a disposed token: handed out, all zero, 27 bytes (F4).
- G04 the record buffer: for 20 certificate sizes from 0 to 1048576 bytes, `ArrayBufferWriter` sized by
  `CapacityFor` never grew (so no copy of the key is left in a discarded buffer).
- G05 beyond C01: every position XOR 0x80, set 0x00 and set 0xFF, plus 2000 random two-byte changes: 4527 tampered
  certificates, **0 accepted, 0 exceptions other than `RegistrationException`** (Malformed 981, KeyMismatch 1719,
  IssuerNotTrusted 1827), the record still version 1.
- G07, G08, G09, G10 as F4.

**(3) The hosted run of 94fe6067** (`hosted2.py` from the gate folder, `--total 1578 --rules 500 --skipped-linux 4
--skipped-windows 19 --unit 111 --floor 111 --hardened-scan`): run 44999270572, four jobs success attempt 1; linux
total 1578 x2, succeeded 1574, skipped 4, failed 0, 0 warnings, `GUARD: clean (10 files)`; windows total 1578 x2,
succeeded 1559, skipped 19, `GUARD: clean (11 files)`; secret-scan both PLANTED-CONTROL lines, `no leaks found` x3,
`objects of this commit not among them 0`, NEUTRAL-EXPORT `wrong 0` x2, NEUTRAL-SCAN-REACH `not among the stored
objects 0`; rules `Ran 111 tests in`, `UNIT-TEST FLOOR: ran 111, floor 111`, `RULES: clean (500 files)`. **`HOSTED
94fe6067...: PASS`.** Control `--skipped-linux 5`: `FAIL 2`. The skipped rows of both legs (4 and 19) all name
`Datasec.Suite.Secrets.Tests` and none names a UniversalPrint test (control: the Secrets count equals the skipped
count). Head 1 `f4cee23b` re-read: `FAIL 6`, linux only, `failed: 1`, the trace `X509Certificate.GetNotBefore()` <-
`RegistrationKeys.AttachCertificate` (`RegistrationKeys.cs:130` of that head): the seat's account holds. CodeQL: the
branch has no analyses (push runs carry no Analyze rows); main's open alerts 0; landing step 3 reads them on the pull
request.

**(4) The fix commit's widening.** Two catches widen. (a) `LoadExact` now reads `PublicKey.ExportSubjectPublicKeyInfo`,
`NotBefore` and `NotAfter` once inside a `catch (Exception)` that returns null (rule (5): `CertificateMalformed`);
(b) a chain build that throws anything is `IssuerNotTrusted`. **Swallowed that should surface?** No: D13 lets only
`RegistrationException` (and the two named exceptions) leave after construction, and both catches turn a platform
exception into a refusal; the cost is diagnosability only (a platform fault reads as Malformed or IssuerNotTrusted),
recorded. Neither catch is around the caller's cancellation or the store. **Accepted that rules (5) to (8) refused
before?** No: the fix changes no condition on the accepting path; every value rules (6) and (7) compare is the same
value read earlier, and an input that made a field read throw was a thrown exception before (never an acceptance).
G05's 4527 tampered certificates at the head: 0 accepted.

**(5) The seat's deviations and FOR TUESDAY 4.**
- DEVIATION 1 (Step 6(a)'s pathspec): ACCEPTABLE. Reproduced: `'tests/Datasec.Suite.UniversalPrint.Tests/*.cs'`
  rc 1 because git's `*` crosses `/` (it matches 9 new `Registration/` files); the `:(glob)` form rc 0 over the 12
  existing files. A wording defect of the kit; the property holds. Records.
- DEVIATION 2 (L03 reads the tracked project file): ACCEPTABLE. A tracked source file with no secret, read only, to
  count `PackageReference`; SECRETS point 1 is about credentials and the environment. Records (kit wording).
- 4 (a) option ranges (`IssueTimeout` up to 1 day, `MaxTokenBytes` 1 to 1048576, `MaxLifetime` up to 365 days):
  acceptable (the defaults sit inside; the kit said only "validated"). (b) null copy and default id
  `InvalidArgument`, unknown id a no-op: acceptable. (c) `Remove` true when the holder knows the id: acceptable
  (note: any `GetAsync` creates an entry). (d) `Dispose` does not cancel a running issuer call (its answer is
  disposed; the bound still cancels it): acceptable. (e) the reader re-checks a held certificate and imports the key
  at every read: acceptable, D5's wording; its check has no cell (F3). (f) a key-generation failure is not wrapped:
  acceptable as the named limit it is (G09); a QUESTION for Tuesday whether D13 should give it a reason. (g) the fix
  commit: acceptable (point 4). FOR TUESDAY 1's reading (issuers copied once by the constructor; C11 shows a later
  change has no effect): acceptable; the README says so.

## THE LANDING TEXTS (in this folder)

`pr-title.txt` (227 bytes), `pr-body.md` (what it adds; the fix commit `94fe6067` named; what does not change; limits
stated plainly, F1 and F2 among them; "Who decides": every choice the coordinator's, never the product owner's),
`squash-subject.txt` ending `(#PRNUM)`, `squash-body.txt` ending `Co-Authored-By: Claude Opus 5.5
<noreply@anthropic.com>`, `landing.txt` (`pr_retrigger.sh --check` MATCH on 185b9eef; `pr_checks_wait.sh
--min-checks 8` with pull request 16's eight check names, read by GET; the merge-ref job logs and their numbers;
CodeQL analyses at the head first, then alerts 0; the head-pinned squash; after-merge reads; MAIN MOVES; no deploy,
there is no host), `FOR-RECORDS.md`. Scans: `build/squash_scan.py` (from the clone, `#17` in place of the number)
`SQUASH-SCAN: clean` (control found 2, rc 1); `words.py` over the squash subject, squash body and title `WORDS: clean
(3 files)`; over `pr-body.md` 7 hits, all by design (the attribution line's emoji bytes; "product owner" 1 and
"coordinator" 2 in "Who decides"); gitleaks over neutral copies of the five texts rc 0. No person is named in any
landing text.

## What I did NOT test

The Linux and Windows legs locally (their only run is the hosted one, re-read); CodeQL (no analysis exists on the
branch; it runs on the pull request); the probes and mutants on Linux or Windows (macOS arm64 only); a real issuer,
a real device certificate, Universal Print or any Microsoft endpoint (none exists in the code); D6, D7 and the raw
scan in the depth assigned to B1905 (my own G05 and G07 aside); two processes over one store; the server and the
publishes (the hosted guards read 10 and 11 files; the server references only Core). Nothing under
`Source_Documents/` or a key folder.
