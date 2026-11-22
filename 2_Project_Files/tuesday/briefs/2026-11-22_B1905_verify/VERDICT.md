GATE B1905: GO WITH FINDINGS @ 94fe606 on main 185b9ee (second reader)

Gate G1, round 1, second reader, deep on D6, D7 and the raw scan. OXPd 2, lane F (kit B1840 as stamped, seat X22):
Universal Print registration material, branch `b1840/wp41-certificate-custody` at head
`94fe606749e25ba7818aef3fb6a19867c68103b5` (two commits: the kit's `f4cee23b`, then one fix commit), on main
`185b9eef28f8ecbd87e92c6ae6cbe1025468c3e9`. Read and measured 2026-11-22, 18:45 to 18:58 AEDT (clocks by `date`), on Opus 5.5, in
my own clone (session scratchpad `b1905only/clone`, made by the kit's `clone.py ... draft`: push URL `invalid://no-push`, no
identity), detached at the head. Origin by `gh api -X GET` under the project GH_CONFIG_DIR: branch = 94fe6067, main = 185b9eef
(read at 18:46 and again at 18:58), open pull requests 0, `compare main...94fe6067` ahead 2, behind 0, 27 files (Tuesday's
figures); open code-scanning alerts on the branch ref 0. Tools: the six files of `fleet/state/s308/d1898/gate/` copied with
`cp -Rc`, six of six equal to the kit's THE TOOLS by sha256; run unchanged. Every heavy job (17) went through the kit's
`heavy.py`: load1 first (1.50 to 6.21, always under 7), the wave lock by `mkdir`, released by a move into my scratch
`_quarantine/locks/`; lock waits 0 on 16 jobs, 2 polls on one. `repo_rules.py` never got `--source-documents`; nothing under
`Source_Documents/` and no key folder was hashed, listed or opened. Every key, authority and certificate synthetic and made at
run time; none printed (the probe log holds reasons and counts only). No write in the OXPd_2 project but the shared lock; no
git write outside my scratch clone; no GitHub write, no Jira, no mail. I did not read B1904's folder.

**BLUF.** D6 and D7 are built as the kit and Stamp S4 say, in the kit's order, and the private key is not at rest in any form I
could look for. My eleven probes and eleven mutants found no certificate accepted that the kit's property refuses, no key part
under the store's folder at any of eight stages, and nothing the fix commit now swallows that should surface. Three things the
cells do not cover: (F1) on macOS arm64 a certificate whose signature value is moved to s+n (the same length, the TBS untouched)
is ACCEPTED and kept, so the held bytes are not the issuer's bytes; (F2) no cell pins the chain's own time check or that it runs
on the library's clock: two mutants leave every lane cell green, only my probe P02 goes red; (F3) D20 stops a one-element chain
only, and under H23's misconfiguration a second leaf signed with the registration's own key is accepted (it needs the private
key, which only the library holds). All three are Minor or records; the code meets D6, D7 and the property as the kit defines
them. Whole suite 1578 / 0 failed / 4 skipped; hosted PASS (control FAIL 2). The two DEVIATIONS and FOR TUESDAY 4 (a) to (g):
all acceptable. Can it land? Yes, on my side, once B1904 is GO or GO WITH FINDINGS.

## Findings

| # | Severity | Finding | Recommendation |
|---|---|---|---|
| F1 | Minor (platform behaviour; no breach of the property as the kit defines it) | **A signature value of s+n is accepted on macOS arm64.** P06a: the good leaf rebuilt by `AsnWriter` with the signature BIT STRING's value replaced by s+n (n = the trusted issuer's modulus; still 256 bytes, so (5b) and the DER reader pass; the rebuild of the unchanged value equals the good bytes, the control) attaches: `ACCEPTED`, version 2, and `TryGetCertificate` returns the s+n bytes, not the issued ones (MEASURED). s+2n (257 bytes) and a leading zero byte (257 bytes) are `IssuerNotTrusted`. The signed part, the key and both dates are byte for byte what the configured issuer signed, so rules (6) to (8) as written are met; but the PKCS#1 range rule (a signature value at or above n is invalid) is not enforced by the platform chain here, and no rule of D6 pins it. Linux and Windows: UNMEASURED (I have no leg but macOS). | Records (`FOR-RECORDS` of B1904 or the next pass): a named limit, or a later rule after the chain builds: the signature value below the modulus of chain element 1's key, with a C01-like cell for s+n. Not a fix-round blocker: no one gets a certificate kept that the issuer did not sign over this key. |
| F2 | Minor (test gap) | **No cell pins D7's time check.** Mutants `mTimeIgnored` (`VerificationTimeIgnored = true`) and `mVerifySystemClock` (`VerificationTime = DateTime.UtcNow` instead of the `TimeProvider`'s) leave all 54 cells of the lane green; only my probe P02 reddens (a configured issuer outside its own window, the leaf inside its window: `IssuerNotTrusted` at the head, accepted under each mutant). Rule (7) covers the leaf's window, so C07 cannot see the chain's clock. The code is right today (P02 green at the head). | A C11 or C07 row: an issuer expired by the library's clock while the leaf is in its window is `IssuerNotTrusted` (a later fix round or a follow-up). |
| F3 | Records | **D20 closes the one-element case only.** P04: with H23's misconfiguration (a self-signed authority over the registration's own key configured as the issuer), attaching that authority's own certificate is `IssuerNotTrusted` (C13, reproduced), but a DIFFERENT leaf over the registration key, signed by that authority (a two-element chain) is `ACCEPTED`, version 2. D20's wording ("a certificate that is itself one of the configured issuers") is met; H23's row reads wider. Making that leaf needs the registration's private key, which no public member returns (L02) and which I found nowhere at rest (P08), so no one but the library could make it. | Records: H23's row narrowed to D20's words, or a later rule refusing a chain whose issuer key equals the stored key. |
| F4 | Records | **H25 now MEASURED by a reader** (the seat relayed it from the prototype): on macOS arm64 a leaf from the trusted issuer marked `CA:TRUE` is `ACCEPTED` (P10a), a leaf with an unknown critical extension is `IssuerNotTrusted` (P10b); the same builder without either is accepted (control). Matches the README's named limit and Q24. Linux and Windows UNMEASURED. | Records only. |
| F5 | Records | **The fix commit fails closed and silently.** A configured issuer object the host disposes after construction makes every certificate `IssuerNotTrusted` (P09) with no signal of a configuration fault; any platform exception in the chain build reads the same. Two of my mutants are equivalent on macOS (`mStatusIgnore`: the `ChainStatus` loop ignored; `mOuterHasData`: the outer trailing-data check removed): both leave every test green, because `Build` already returns false on any flag with the default verification flags, and rule (5)'s `RawData` equality already refuses trailing bytes. Defensive lines, not holes. | Records: the host wiring lane gives a configuration check for the issuer set; no change here. |

No Blocker, no Major.

## What I re-ran, and the results

**(1) The diff against THE CONTRACT and the owned paths.** `git diff --name-status 185b9eef HEAD`: 27 rows, 22 `A` under the two
`Registration/` folders, exactly five `M` outside them (the library's project file and the four lock files). T1 extracted by
program from the kit (8 lines, 264 bytes, sha256 `6cb8b5a1...` = FACT 7) equals the head's project file byte for byte;
`--numstat` `3 0`. My lock-rule program over the four files against BASE: every target's package entries equal (UniversalPrint
0/0 x3; its tests 17/17, 2/2, 2/2; Jobs 0/0 x3; Jobs tests 17/17, 2/2, 2/2); added or changed entries only `datasec.suite.secrets`
(ADDED, Project) and `datasec.suite.universalprint` (CHANGED, Project), none removed: `LOCK RULE (reader): PASS`; control
(`datasec.suite.secrets` struck from the allowed names) `FAIL 4`. `git diff --name-only BASE -- '*packages.lock.json'` 4 files.
The forbidden list of Step 6(a) with the Jobs project files and the test project file added, with `:(glob)` on the `*.cs`
pathspec: rc 0; the plain pathspec rc 1 (it matches the new `Registration/*.cs`: the seat's DEVIATION 1 reproduced), the glob
form matches 12 existing files by `ls-files`; control (the project file) rc 1. Boundary words over the 12 library `.cs` files:
`ExtraStore`, `X509RevocationMode.Online`, `new X509Certificate2(`, `System.Net`, `HttpClient`, `File.`, `Console.`, `SignData`,
`SignHash`, `DateTime.Now` 0 each; `DisableCertificateDownloads = true` 1, `X509ChainTrustMode.CustomRootTrust` 1. Added key,
certificate or PEM files 0.

**D6, the rules and their order** (`RegistrationKeys.cs:86-143`, `RegistrationRecord.cs:139-229` at the head): (1) id valid; (2)
empty then cap, before any parse; (3) record read inside the attach lock (D19); (4) already attached; (5) loader, then the key and
both dates read once inside a guarded parse, then `RawData` equal to the input; (5b) `AsnReader` DER: one outer SEQUENCE with
nothing after it, the signed part, an outer algorithm byte-equal to the inner one (version `[0]` skipped, then serial, then the
inner algorithm), a bit string with 0 unused bits and nothing after it; (6) SPKI byte-equal; (7) `GetUtcNow()` inside `NotBefore`
to `NotAfter`, both ends included; (8) the chain. Nothing is written unless all pass (C01, C02 and my probes check the version).
The order is the kit's; the fix moved the reads of the key and dates inside (5), which can only change a refusal reason, never
turn a refusal into an acceptance (below).

**D7, the chain policy** at the lines the seat names: `RegistrationKeys.cs:188` `if (_issuers.Count == 0)` returns false; `:195`
`CustomRootTrust`; `:196` `CustomTrustStore.AddRange(_issuers)` (the issuers copied once by the constructor, C11); `:197`
`RevocationMode = NoCheck`; `:198` `DisableCertificateDownloads = true`; `:199` `VerificationTime = now.UtcDateTime`; `:200`
`VerificationTimeIgnored = false`; `:203-212` `Build` false or any exception: refused; `:214-220` every `ChainStatus` must be
`NoError`; `:222` `ChainElements.Count >= 2`. No `ExtraStore` anywhere. As the seat states.

**(2) The re-run** (macOS arm64, the project's SDK 10.0.404, the closed package cache, `-p:NuGetAudit=false`, `CI=true`):
`dotnet restore --locked-mode --force` rc 0, `git status --porcelain` 0 lines after it; `dotnet build -c Release --no-restore`
rc 0, `0 Warning(s)`, `0 Error(s)`; `dotnet test -c Release --no-build`, the whole suite: total 1578, failed 0, succeeded 1574,
skipped 4 (the seat's claim, MEASURED). `python3 -I build/repo_rules.py '<clone>'` on the clean tree (my probe file moved out to
my quarantine first; `status --porcelain` 0 lines): `RULES-NOTE: R5 hash half NOT RUN (no supplied-source folder here)`,
`RULES: clean (500 files)`; `ls <clone>/1_Project_Definition/Source_Documents`: no such file or directory.

**Red first, where I could.** The seat's stubs are not in the repository, so I made my own: `stubAttach`, `AttachCertificate`
throwing `NotImplementedException` before rule (1): 31 red, every certificate cell of the lane among them (C01 to C13, K03 to
K05, L01, R01 to R04, X01) and my probes P01, P02, P05, P07, P08, P10.

**Mutants of THE CONTROLS I chose** (each one edit on product code in my scratch clone, the whole suite as one heavy job
`dotnet test -c Release --no-restore` with my probe file present, then undone by `git show HEAD:<path>` and proved by
`git diff --quiet -- <path>` rc 0; all eleven undone and proved; `evidence/mutants-red.txt`):

| Mutant | Change | Red tests |
|---|---|---|
| mTrustSystem | `TrustMode = System` | 13: C01, C10, C11, C12, K03, K04, K05, L01, R02, R04, X01, P08, P10 |
| mChainAlwaysTrue | the chain rule returns true | C01, C06, C08, C11 x2, C13, L01, P01, P02, P08 |
| mChainLenOne | `Count >= 1` | C13 |
| mAlgEq | (5b)'s algorithm equality always true | C01 |
| mUnusedBits | (5b)'s unused-bits check removed | C01 |
| mRuleSevenOff | rule (7) never refuses | C07, L01, P07 |
| mTimeIgnored | `VerificationTimeIgnored = true` | **P02 only** (F2) |
| mVerifySystemClock | `VerificationTime = DateTime.UtcNow` | **P02 only** (F2) |
| mStatusIgnore | the `ChainStatus` loop ignored | none: equivalent (F5) |
| mOuterHasData | the outer trailing-data check removed | none: equivalent, rule (5) covers it (F5) |
| stubAttach | the red-first stub above | 31 |

**My probes** (`evidence/ProbeB1905Tests.cs`, scratch only, never committed; outcomes in `evidence/probes.log`, reasons only;
the suite with them: total 1589, failed 0, skipped 4). Probes that try to make a certificate accepted that the property refuses:

| Probe | Handed | Outcome at the head |
|---|---|---|
| P01a | an issuer with the trusted issuer's exact name (RawData equal) and another key, its own AKI | `IssuerNotTrusted` |
| P01b | the same, with the trusted issuer's AKI copied into the leaf | `IssuerNotTrusted` |
| P02a, P02b | a configured issuer expired, or not yet valid, by the library's clock; the leaf in its window | `IssuerNotTrusted`, `IssuerNotTrusted` (F2: the only test that sees the chain's clock) |
| P03a, P03b | a configured issuer marked `CA:FALSE`; one with no extensions at all | `IssuerNotTrusted`, `IssuerNotTrusted` |
| P04a, P04b | H23's misconfiguration: the configured self-signed authority over the registration key; a different leaf it signs | `IssuerNotTrusted`; **`ACCEPTED`** (F3) |
| P05a, P05b | the outer SEQUENCE length, or the signature BIT STRING length, re-encoded in non-minimal long form | `CertificateMalformed`, `CertificateMalformed` |
| P06a, b, c | the signature value as s+n (256 bytes); a leading zero (257); s+2n (257) | **`ACCEPTED`** (F1); `IssuerNotTrusted`; `IssuerNotTrusted` |
| P07 | a `NotAfter` inside the repeated local hour (zone `Australia/Canberra`, `IsAmbiguousTime` true), the clock 30 minutes after it | `CertificateNotTimeValid`; the `NotAfter` read back equal (offset 0): no daylight-saving slip in rule (7) |
| P09 | a configured issuer object disposed by the host after construction | `IssuerNotTrusted` (F5) |
| P10a, P10b | H25: a leaf marked `CA:TRUE`; a leaf with an unknown critical extension | `ACCEPTED` (the named limit); `IssuerNotTrusted` (F4) |

**THE RAW SCAN (K04, X01).** Read: the lane's `StoreRoot.FilesHolding` reads every byte of every file under the store's root for
the needle as raw bytes, hex both cases, base64 and base64url with and without padding; K04 uses the PKCS#8 and the PKCS#1 export
of the key the library stores (taken by the internal key factory), X01 the PKCS#8 and the certificate; both write and find a
clear marker before the needles are counted. My probe P08, the key at rest, is stronger: the needles are the PKCS#8, the PKCS#1
and each private component (D, P, Q, DP, DQ, InverseQ), each as raw bytes, reversed bytes, hex both cases, and base64, base64url
and UTF-16 base64 at all three byte alignments; the scan covers the whole test folder (the store's root AND the key file beside
it); its control FIRST (a random 300-byte needle written base64 at offset 1 inside a text file) is found in exactly 1 file. Over
eight stages, after create; after three refused attaches (`CertificateMalformed`, `CertificateKeyMismatch`, `IssuerNotTrusted`);
after a failing put at attach and at create (`StoreFailed` each); after the good attach; after a read; after the delete; after
both deletes: key-part hits 0 at every stage, and the certificate 0 after the delete. P11, a control of the lane's own scan: over
a store wrapper that also writes each put in clear under the root, the lane's `FilesHolding` finds the PKCS#8 in 1 file after
create and after attach. So the scan can see the record's form, and the store keeps none.

**(3) The hosted run of 94fe6067.** `hosted2.py 94fe6067... --total 1578 --rules 500 --skipped-linux 4 --skipped-windows 19
--unit 111 --floor 111 --hardened-scan`: four jobs completed success, attempt 1 (run 44999270572); linux `total: 1578` x2,
`succeeded: 1574`, `skipped: 4`, `failed: 0`, `GUARD: clean (10 files)`; windows `total: 1578` x2, `succeeded: 1559`,
`skipped: 19`, `GUARD: clean (11 files)`; secret-scan 25 of 25, `objects of this commit not among them 0`, `no leaks found` x3,
both `NEUTRAL-EXPORT` lines `wrong 0`, `not among the stored objects 0`; rules `Ran 111 tests in`, `UNIT-TEST FLOOR: ran 111,
floor 111`, `RULES: clean (500 files)`; check runs beside the four 0; last line `HOSTED 94fe6067...: PASS`, rc 0. Control
`--skipped-linux 5`: `FAIL 2` (`succeeded: 1573`, `skipped: 5`), rc 1. The UniversalPrint test assembly `passed` on linux (11 s
122 ms) and windows (10 s 858 ms); skipped lines naming `Registration` 0 on each leg. The first head `f4cee23b` re-read: `FAIL 6`
on linux only; its log shows `CryptographicException` from `OpenSslX509CertificateReader.ExtractValidityDateTime` <-
`X509Certificate.GetNotBefore()` <- `RegistrationKeys.AttachCertificate` (`RegistrationKeys.cs:130` of that head) <- C01: the
seat's account is accurate. CodeQL had not run on the branch (no pull request): that reading is the landing's.

**(4) The fix commit's widening** (`f4cee23..94fe606`: 3 files, 50 insertions, 7 deletions, no test changed). Rule (5) now reads
`PublicKey.ExportSubjectPublicKeyInfo()`, `NotBefore` and `NotAfter` once inside a `catch (Exception)` that returns null
(`CertificateMalformed`); rules (6) and (7) compare those same values with the same expressions as before; the chain receives the
same certificate object. The chain's catch widened from `CryptographicException` to `Exception`, returning false. **Nothing is
accepted that rules (5) to (8) refused before:** both catches can only refuse, the values compared are computed by the same calls,
and every mutant and probe above gives the same acceptance set (P05 to P10 at the head). **Is anything swallowed that should
surface?** On input bytes: no; an exception while parsing caller-handed bytes is exactly what D13 says must become a typed
refusal (the first head's red is that breach). On configuration: yes, silently (F5: a disposed issuer refuses everything as
`IssuerNotTrusted`), which fails closed; a records point for the host wiring. One side effect: `RegistrationRecord.Read` also
runs `LoadExact` over a held certificate, so a stored certificate whose dates a platform cannot parse would now read
`UnreadableMaterial`; such a certificate can no longer be attached, so this cannot arise from this library's own writes.

**(5) The seat's DEVIATIONS and FOR TUESDAY 4.** DEVIATION 1 (Step 6(a)'s pathspec): acceptable; reproduced above, the property
(no existing test file changed) holds by the `:(glob)` form and by `ls-files`; a kit-wording defect for records. DEVIATION 2 (L03
reads the tracked library project file): acceptable; read only, a tracked source file with no secret, and the hosted legs pass it.
FOR TUESDAY 4: (a) the holder's option ranges (`IssueTimeout` at most a day, `MaxTokenBytes` 1 to 1048576, `MaxLifetime` at most
365 days): acceptable; (b) `Invalidate` with a null copy or the default id `InvalidArgument`, an unknown id a no-op: acceptable;
(c) `Remove` true when the id is known, token held or not: acceptable; (d) `Dispose` gives waiters `ObjectDisposedException` and
does not cancel a running issuer call (its answer disposed on arrival): acceptable, the answer is never held; (e) the reader
re-checks a held certificate with (5) and (5b) and imports the key at every read: acceptable (D5's wording; one parse per read);
(f) a failure of the platform's key generation inside `CreateRegistration` leaves as the platform's exception: acceptable as the
named limit it is (not a handed-in shape; D13 names no reason for it), a records item; (g) the fix commit: acceptable, ruled in
(4). None is a question that blocks; each is the coordinator's to keep.

## Not run

Linux and Windows locally (the hosted legs are their only run; F1, F4 and P01 to P11 are macOS arm64 only, UNMEASURED
elsewhere); a chain build with an intermediate present in a machine certificate store (whether a custom-root chain on Windows or
macOS draws intermediates from the system stores is UNMEASURED; it would still need a configured root, so it cannot breach the
property); CodeQL; the publishes and the release guard (B1904's whole-lane run; the hosted guards read 10 and 11 files); the word
scan and gitleaks over the diff (B1904's); any real issuer, service or tenant.

## Return summary (10 lines)

1. GATE B1905: GO WITH FINDINGS @ 94fe606 on main 185b9ee (second reader); 0 Blocker, 0 Major, 2 Minor, 3 records.
2. Scope: 27 files, 22 under `Registration/` and exactly the five others; T1 byte for byte; lock rule PASS over four files (control FAIL 4).
3. Local: restore locked rc 0, build 0 warnings, whole suite 1578 / 0 failed / 4 skipped; `RULES: clean (500 files)`, no source-documents option.
4. Hosted 94fe6067 PASS on four jobs (control FAIL 2); the first head's linux red is as the seat says (OpenSSL, `GetNotBefore`, C01).
5. D6 order and D7 policy lines (`RegistrationKeys.cs:188-222`) as the kit and S4 say; empty issuer set refuses all; no `ExtraStore`.
6. Raw scan: P08 (key components, three base64 alignments, eight stages, whole test folder) finds 0; P11 proves the lane's scan sees a clear leak.
7. F1 Minor: on macOS a signature value of s+n (same length, TBS untouched) is ACCEPTED and kept; Linux and Windows UNMEASURED.
8. F2 Minor: no cell pins the chain's clock; `mTimeIgnored` and `mVerifySystemClock` red only my P02.
9. F3 records: D20 stops the one-element chain only; a second leaf signed with the registration's own key is accepted (needs the private key).
10. Fix commit: fails closed, accepts nothing new; DEVIATIONS 1 and 2 and FOR TUESDAY 4 (a) to (g) acceptable. Lands once B1904 agrees.
