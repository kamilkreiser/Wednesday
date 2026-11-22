STARTABLE: YES - AMENDMENT 1 (s308) re-measured the kit against main 185b9eef and ran its prototype (1572 total, 0 failed; 26 mutants): it fixed four defects a seat would have hit (hosted.py FAIL on a green main, four lock files not two, rule (5b), concurrent attach), and Stamp S4 must answer Q7 AND the new STOP-class Q20 (lane E landed a colliding DeviceTokenHolder; default the Cloud names and Invalidate(id, refused)) in words. Round 1 text follows; the amendment is the last section.

# B1840 drafter report | Datasec / OXPd_2 | wave 3, lane F (WP4.1 in part: key pair, CSR, certificate custody through the secret store, the device-token holder) | drafter Opus, 2026-11-21 17:08 to 17:26 AEDT

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1840_SEAT-X22_oxpd2-wp41-certificate-custody.md` (104610 bytes, 338 lines, ASCII only). Its sidecar `.measured` holds 203 claim lines plus `FROZEN` and `KIT`. Tools for the seat: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s304/d1840/gate/`. That folder holds 6 files: five copied from B1831 unchanged, plus this kit's `commit-message.txt`. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s304/d1840/`.

## BLUF
1. **The precondition holds.**
   - `main` = `5e36d8dca42966395ea3dd014c7f788409eb585f`, read at 17:08:20 and again at 17:26:12. It has not moved, there are 0 open pull requests, and there is no `b1840` ref.
   - The hosted run of `main` is green: `HOSTED ...: PASS` with `--total 894 --rules 291 --skipped-linux 4 --skipped-windows 19`. The control `--skipped-linux 5` printed `FAIL 2`.
   - The secret store and `src/Datasec.Suite.UniversalPrint` are both on `main`. Nothing under any `Registration/` path exists, and nothing at `main` mentions `CertificateRequest`, `ExportPkcs8PrivateKey`, `X509Chain` or `uprint/` (0 files each; the control `LocalSecretStore` finds 16).
2. **One seat** (X22, branch `b1840/wp41-certificate-custody`, level opus, gate G1, windows 240/180).
   - It adds `src/Datasec.Suite.UniversalPrint/Registration/` and `tests/Datasec.Suite.UniversalPrint.Tests/Registration/`.
   - The library's project file gains ONE project reference, to Secrets (frozen text T1: 3 lines added, 0 removed).
   - The restore rewrites TWO EXISTING lock files, and only by adding project entries. The expected shape was MEASURED on lane D's head `70c1fad5`. The kit states a program rule that keeps the package rows unchanged; that rule is marked NEVER RUN.
   - It adds no package and no solution line, and makes no workflow change.
3. **What is built:**
   - `RegistrationKeys`: an RSA-2048 key pair and a PKCS#10 request (Workpath's fixed subject, SHA-256 with PKCS#1, `A3:141-142`). The key is kept only as one secret-store record, `uprint/<32 hex>`. A certificate is accepted only if all four hold: it parses as exactly one DER certificate, its public key equals the stored key's, it is inside its window, and it chains to a configured issuer (custom root, no revocation check, `DisableCertificateDownloads`). It can be attached only once. The record is deleted on removal.
   - `DeviceTokenHolder`: holds the token in memory and renews it at 90% of its stated lifetime on the monotonic clock (`A3:164`). Renewal goes through an `IDeviceTokenIssuer` interface (a fake in the tests), one call at a time, with a 30 s bound.
   - No public member returns a private key. The test K04 scans the raw files under the store's root for the PKCS#8 bytes.
4. **THE KEY PROVIDER POINT (Q2).**
   - `02:544` says the key is "generated in C15's key provider".
   - The store on `main` holds values only; it cannot generate keys or sign. `02:618` (b) describes keys "wrapped under the escrowed secret-store key".
   - Default: generate the key in process and store it only through C15. What this gives up: the key is in clear in memory during two calls.
5. **Q7 (stop-class).** Which certificate signs Universal Print's device certificates is UNMEASURED: `A3:146` says only "Microsoft is the signer".
   - Without an issuer check, a certificate with a byte changed in its signature still carries the right key, so the plan's own test ("a tampered certificate refused") needs the issuer.
   - Default: no issuer configured means every certificate is refused. The product therefore accepts no real certificate until a later lane configures the issuer from a test tenant.
   - Alternatives A and B weaken this.
6. **A correction to how the commission frames lane F:** the plan's partition reads "no slnx line (existing projects)", and that is right. What changes instead is TWO EXISTING LOCK FILES (UniversalPrint and UniversalPrint.Tests). The B1831 form says "no existing lock file may change"; this kit replaces that line with the project-entry rule.

## FACTS RE-MEASURED (instrument in brackets)
- **Origin** [gh api -X GET, project GH_CONFIG_DIR, 17:08:20 and 17:26:12]
  - private and push both true.
  - Pull requests 1 to 6 are merged; 0 are open.
  - Lane D's `b1831/wp15-token-broker` is at `70c1fad5`: ahead 1, behind 0. Its hosted jobs are all success, `total: 947` on both legs (read by hosted.py; the program's FAIL rows came from the totals I gave it, not from the jobs).
- **Main's tree** [tarball by GET]
  - 291 files.
  - The UniversalPrint library: its project file (5 lines, no PackageReference), its lock file (8 lines), and 14 files under `Ipp/`.
  - The test project: 12 `.cs` files, 7 of them with `using Xunit;` and no GlobalUsings. It has 137 test methods by the indented pattern and 0 at column 1.
  - The Server references Core only, so the GUARD counts 10/11 cannot move.
  - The solution file lists both UniversalPrint projects (lines 9 and 17).
  - `ci.yml` is 199 lines, sha256 `c3894bbc...`. The relevant lines are 40/42/45/46/48, 70/72/75/76/78, 192 and 199. `repo_rules` runs without `--source-documents`; the kit follows that, so no key folder is hashed.
  - R5 extension list at `repo_rules.py:60-61`: `.pfx .p12 .key .pem .crt .cer .der` and others.
- **Store surface** [cat -n at main]: `ISecretStore.cs:15/21/27/32`; `SecretStoreException` constructor is internal (`:9`); `MaxValueLength` is 1048576; `TestRoot.cs:16` sets `LOCAL=user`; `FormsOf` is at `:117-127`.
- **Reference pack 10.0.15** [grep -c of documented names; control 0]. Each of these is present once:
  - `CertificateRequest`: the 4-argument constructor, `CreateSigningRequest`, `LoadSigningRequest` (hash, options, padding), `Create(issuer, ...)`, `CreateSelfSigned`.
  - `X509CertificateLoader.LoadCertificate(ReadOnlySpan<byte>)`.
  - `ExportPkcs8PrivateKey`, `ImportPkcs8PrivateKey`, `RSA.Create(int)`, `PublicKey.ExportSubjectPublicKeyInfo`, `RSACertificateExtensions.GetRSAPublicKey`.
  - On `X509ChainPolicy`: `CustomTrustStore`, `VerificationTime`, `DisableCertificateDownloads`; also `CustomRootTrust` and `X509RevocationMode.NoCheck`.
  - `SYSLIB0057` appears in the reference dll once. The kit therefore forbids `new X509Certificate2(byte[])`; that the marker applies to that constructor is DERIVED.
- **Transitive project reference** [GET of lane D's head]: lane D's test csproj references only its library, yet its tests open `LocalSecretStore` (`Support.cs:3`, `:37`), and its hosted jobs pass. The UniversalPrint test project file therefore does not change.
- **Scanner shapes** [gitleaks 8.30.1, the workflow's four options, one file per row; random values never printed]: 12 rows.
  - Quiet (rc 0): the PKCS#8 export call, CSR creation, the subject literal, a PEM header literal alone, synthetic device-token words, a `uprint/000...1` literal, and one 32-hex sample.
  - Fired: `generic-api-key` on a 44-character base64 literal, and `private-key` on a whole PEM key made by openssl (the control).
- **Commit message**: subject 190 bytes; file 248 bytes, 3 lines, ASCII. gitleaks rc 0. `words.py` printed `WORDS: clean (1 files)`, and its control printed `13 of 13`.
- **Machine** [17:14:56 / 17:15:06]
  - Load 2.34, 2.61, 2.55; 1003 GiB free.
  - No `.tools/b1840` folder and no lock folder.
  - 4 panes, 1 of them OXPd2 (`Datasec/OXPd2-X19`, lane CF's seat launched during drafting), 0 for X22.

## D-DECISIONS (Tuesday's defaults; each has a Question, an alternative, a cost and a cell)
| D | Decision |
|---|---|
| D1 | The library knows a registration id only (the "key reference" of `02:372`). |
| D2 | RSA-2048 made in process, kept only in the store. |
| D3 | The id is 16 random bytes as 32 hex. |
| D4 | Workpath subject, SHA-256/PKCS#1, no extension. |
| D5 | One record `uprint/<id>` in the library's own JSON (format, id, key, certificate), read strictly. |
| D6 | Eight ordered certificate rules, with a `RawData` byte-equality check and a 64 KiB cap. |
| D7 | Issuer required. |
| D8 | The certificate's clock is the wall clock (a named limit). |
| D9 | A certificate is attached once. |
| D10 | Delete is the store's delete. |
| D11 | Token in memory, 90% monotonic, single-flight, 30 s, answer rules, held token kept while it lives. |
| D12 | Store failures map to `StoreFailed` / `UnreadableMaterial`. |
| D13 | 13 typed reasons. |
| D14 | Masks; no private-key-returning member. |
| D15 | No logging, network or package. |
| D16 | Own partition (README only). |
| D17 | Build code rules. |

## Q-QUESTIONS FOR TUESDAY (defaults are already assumed in the kit; S4 must answer Q7 in words)
| Q | Default |
|---|---|
| Q1 | Id only. |
| Q2 | Key in process, stored in C15 (the alternative is to wait for a non-exportable provider). |
| Q3 | 32 hex. |
| Q4 | Workpath subject. |
| Q5 | One record. |
| Q6 | D6 rules. |
| **Q7** | **Issuer required; an empty set refuses everything (STOP-CLASS).** |
| Q8 | Wall clock for the certificate. |
| Q9 | Attach once. |
| Q10 | Two removal calls. |
| Q11 | Token in memory (`02:618` and `A3:369` pull toward persisting it). |
| Q12 | No app registration of anyone's (OQ-9/N-14/N-12). |
| Q13 | No signing of the device-token assertion (the next lane adds it inside this library). |
| Q14 | No listing until SL lands. |
| Q15 | Store-failure rules. |
| Q16 | 13 reasons. |
| Q17 | The names, namespace `Datasec.Suite.UniversalPrint.Registration`. |
| Q18 | Own partition. |
| Q19 | 240/180, X22, G1 with a second reader on D6, D7 and the raw scan. |

## UNMEASURED
- Every build and test outcome.
- `X509Chain` with a custom root on macOS, Linux and the hosted Windows image. The kit says to STOP, never skip, if a good certificate does not chain.
- Whether the registration service accepts the request, and the encoded attribute order.
- The real issuer.
- The exact bytes the restore writes into the two lock files.
- RSA generation time on the runners.
- The local and hosted totals: 894 plus the seat's tests, with skipped 4 and 19 unchanged (predicted).

## CHAIN INPUTS (each produced earlier or present at BASE)
| Step | Inputs | Produced by or present at |
|---|---|---|
| 1 | gate folder; `<repo>`'s local identity; T1 in the Step-0 copy; BASE lock files | drafter scratch; BASE; Step 0; BASE (`git show`) |
| 2 | T1 block | Step 1 |
| 3 | stubs; saved BASE lock files | Step 2; Step 1 |
| 4 | red cells | Step 3 |
| 5 | green tree | Step 4 |
| 6 | staged tree, `words.py`, `commit-message.txt` | Step 5, gate |
| 7 | commit; the base's hosted numbers | Step 6; Step 1 |

## THE CHECKS I RAN, AND THE CHECKS THAT ARE NEVER RUN
Each check I ran had a control that fired:
- `hosted.py` PASS on main, with its FAIL control;
- `words.py --control`;
- the gitleaks shapes, with the openssl private-key control;
- the pointers checker (38 of 38, the absent-fragment control false);
- the slot count (8 unstamped slots, as the kit says);
- the ASCII scan of the kit (0);
- the T1 extraction compared against main's file by `diff` (3 added).

Marked NEVER RUN in the kit:
- the owned-paths property;
- the lock rule;
- the boundary scan on code;
- every heavy job;
- `hosted.py` on a head of this lane;
- the push.

## READING LOAD
The kit (104610 bytes) plus about 118 kB:
- items 2 to 4 and 6: 104881 bytes (`CLARIFICATIONS.md` is the largest);
- the five tool docstrings: 4748 bytes;
- the 19 pointer lines: 8171 bytes.

This is about the B1831 size, and over the wave-1 guideline of about 100 kB. I kept it because the D, Q, H and cell sections are what the earlier verdicts asked for.

## WHAT I DID NOT READ
- The B1829 kit body: only its seat's STATUS DEVIATIONS. The B1831 kit and its report I read whole.
- The design beyond the pointer lines, 02 §5.6.5 (540-552), the §6.2 head and line 618, and the open-question rows.
- `A3` beyond lines 1-58 by grep, 141-170 and 360-372.
- The rest of the secret store's source.
- Lane D's code beyond its project file, lock files, `Support.cs` grep lines and `TestClock.cs` member lines (fetched only to check feasibility; the kit tells the seat to copy nothing).
- `OXPD2-18` in Jira: RELAYED from the plan; no Jira call.
- Nothing of HPSM-POC, the NAS library, `Source_Documents/` or any key folder. No decision card.

## CORRECTIONS TO THE COMMISSION / PLAN
- Lane F changes two existing lock files (BLUF 6). The B1831 form's "no existing lock file may change" does not fit this lane, and the kit replaces it.
- The plan names "the device-token holder behind an interface" but not the signed device-token assertion (`A3:162`). The kit keeps the assertion OUT (Q13): it is a request to a Microsoft endpoint.
- `02:618` lists device tokens with the keys in C15, but the kit's default holds the token in memory (Q11). That is a pull for Tuesday.

## OUTSIDE-THE-FENCES DISCLOSURE
I wrote only the kit, its sidecar, this report and files under `fleet/state/s304/d1840/`:
- `main.tar.gz` and its extract;
- `gate/` (6 files);
- `scratch/`: the programs `frozen.py`, `pointers.py`, `sidecar.py` and `glrows.py`; the gitleaks rows; `panes.txt`; lane D's `TestClock.cs` copy;
- `logs/`: hosted logs of main, of the control run and of lane D's head.

Other actions to disclose:
- One throwaway RSA key made by openssl for the scanner control. It and its row folder were MOVED to `fleet/state/s304/d1840/_quarantine/`. That path is gitignored (`.gitignore:44`), and the key was never printed.
- One Bash call was refused by a hook (a `$S/..` move) and re-issued with an absolute path.
- `gh api -X GET` only. No Jira call, no git verb in any project tree, no build, no test, no message.

## AMENDMENT 1 (s308)
Re-measure of kit B1840 against `main` `185b9eef28f8ecbd87e92c6ae6cbe1025468c3e9` by a second read-only drafter (Opus 5.5, commission B1898, re-commissioned by s309 after the first B1898 run died with s308's rotation), 2026-11-22 17:13 to 17:42 AEDT (clock reads by `date`: 17:13:50, 17:14:22, 17:14:34, 17:20:39, 17:25:11, 17:31:16, 17:35:34, 17:39:33). Scratch, logs, the clone, the prototype and the programs are under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s308/d1898/r2/`. The new tool folder is `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s308/d1898/gate/`.

Round-1 first line, kept here: "STARTABLE: YES - the kit is complete and every literal is measured (stamp_check: 203 claims, 203 measured, rc 0; ...)".

### State found, and what was reused
- The three `.pre-s308-remeasure` copies already existed from the dead run (16:55). `cmp` against the originals gave rc 0 for all three. I did not overwrite them.
- The dead run's clone at `d1898/clone` was at HEAD `185b9eef`, but its tree was NOT clean: 7 porcelain lines, the same 4 lock files and the Registration folders. So I did not reuse it. I made a fresh clone at `r2/clone` with the round's `clone.py ... draft`: push URL `invalid://no-push`, HEAD `185b9eef`, 0 dirty lines, 478 files.
- The dead run's prototype sources (`d1898/proto`, about 75 kB) were read and used as a starting point. Every number below is from my own runs. None of the dead run's logs is cited.
- The orphan pid 2177 (`/private/tmp/b1839-gate`, 0.0% CPU) holds 243 descriptors, 0 of them network or the lock path. The lock folder was absent at the start. It holds neither the lock nor a port. I did not touch it.

### BLUF
- **STARTABLE: YES**, once Stamp S4 answers Q7 and the new **Q20** in words. Every literal is measured: `stamp_check.py`: 224 claims, 224 measured, rc 0.
- **The overlap question (Q20, STOP-class).**
  - Lane E's landed `DeviceTokenHolder` holds a DIFFERENT token: the printer's OXPd solution token, per serial, with its refresh value kept through `IDeviceSecretVault`. Lane F's holds Universal Print's device token, per registration id. No behaviour is duplicated or contradicted.
  - Two things do have to change. Neither has been built yet:
    - (a) The two public names `DeviceTokenHolder` and `DeviceTokenHolderOptions` collide. A scratch project that imports both namespaces fails with `CS0104` on both names; the control, with one name written in full, builds.
    - (b) Round 1's `Invalidate(id)` repeats the race that lane E's fix round closed with its completed-flight count. N callers refused with one token cause N+1 issuer calls: 2 gave 3 and 100 gave 101 on the prototype.
  - Default: the `Cloud` prefix on the four token types, plus `Invalidate(id, refused)`. The kit now says both.
- **Four defects of round 1 that a seat would have hit, each MEASURED at `185b9eef`:**
  1. The kit's `hosted.py` requires `Ran 53 tests`, so it printed `FAIL 2` on the green main (FLOOR is now 111). It is replaced by `hosted2.py` with `--unit 111 --floor 111 --hardened-scan`, which printed `PASS`; its control printed `FAIL 2`.
  2. FOUR lock files change, not two. Lane G's landed `Jobs` references this library (Q22). The lock rule PASS and both its controls fire.
  3. With D6's rules (1) to (8) only, cell C01 is RED. Two one-byte changes outside the signature are accepted: the outer algorithm's NULL parameter, and the bit string's unused-bits byte. Fix: new rule (5b), D18 (Q21).
  4. Two concurrent attaches both win: 20 of 20 runs, ending at version 3. Fix: D19 (Q23), cell C12.
- **Smaller corrections:**
  - A self-signed certificate over the right key, configured as an issuer, was accepted. Fix: D20 (Q24), cell C13.
  - L04 missed a static auto-property, because its backing field is compiler-made. L04 now also checks static setters.
  - The locked restore needs `--force`: without it, an up-to-date tree passes a stale lock file. The `git diff --quiet` check in Step 5 reads rc 1 by construction (nothing is staged yet), so it is replaced by a sha256 comparison.
  - The literal clause of Step 6(e) contradicted cell C10's own 32- and 64-character ids. It now counts only literals with more than two distinct characters.
  - L03 and L04 are green against stubs, as their own first versions say.
  - The format string `"x32"` counts as a seat id in `words.py`.

### What changed in the kit (in place: `r2/scratch/amend.py`; each replacement asserted to occur once on its line; a temp file, then `os.replace`)
| Area | Change |
|---|---|
| Whole kit before the Stamp | The Q20 (a) rename: 23 names (`CloudDeviceToken`, `ICloudDeviceTokenIssuer`, `CloudDeviceTokenHolder`, `CloudDeviceTokenHolderOptions`). Lane E's names appear only where lane E is meant |
| Lines 1, 3, 7, 9, 11 | AMENDMENT 1 header with clocks. Title: four lock files. All lanes landed, no live OXPd pane. The Jobs lock-file exception. `CLAUDE.md:7` now carries the Opus word |
| BLUF 1, 2, 4, 5 | Four lock files; Q20; D18 to D20; H22 to H27 |
| READ WHOLE item 8; load | `ISecretStoreInventory.cs`, and lines 166 to 300 of lane E's holder (read only). New load figure |
| Cut (listing row) | SL landed: `ListAll()` never throws, and it is on `LocalSecretStore`. Q14 stays OUT |
| D6, D9, D11, D16, D17 line | Rule (5b) with the measured hole. D19. `Invalidate(id, refused)` with the measured counts. README line 20. D18, D19 and D20 written out |
| Contract | `Invalidate(RegistrationId id, CloudDeviceToken refused)` |
| REQUIRED SECTION | New rows H22 to H27 (outside the frame) |
| CONTROLS, mutants | Chain on macOS MEASURED; C12, C13, T09, T10; L03/L04 stub note; L04 static setters; the mutant re-measure and 7 new mutants |
| TOOLS | New folder `s308/d1898/gate/`. The `hosted2.py` row and hash. Its measured PASS and control |
| T1, SHARED FILES | T1 unchanged and built. slnx lines 14/28; `xunit.v3` line 12; ci.yml 218 lines, sha256 `c25bdbb2...`, FLOOR line 211, rules line 218; the hosted numbers of `185b9eef`; the four-file lock rule; README line 49; repo_rules `:95-96`; `.gitignore:16` |
| SECRETS | F10 is value-dependent. Words traps |
| FACTS 1 to 5, PRIOR WORK | Each gains its [A1] re-measure. New PRIOR WORK row for lane E's holder |
| OWNED PATHS | Five existing files change. Rows 7 and 8 (the Jobs lock files) |
| WORK Steps 1, 3, 5, 6(a), 6(e), 7(e) | 478 files; `hosted2.py`; predictions (111/111, four lock files, L03/L04); the `--force` locked restore and sha256 check; `Ran 111`; ci.yml:218; the chain measured; five `M` rows; the boundary scan run and its literal clause fixed |
| LANE, REFUSE, HEAVY, HOLDS | G landed and references the library. S4 must answer Q20 in words. More than 70 runner jobs. No edit of lane G's files but the lock files |
| Questions | Q20 (STOP-class) to Q24 |
| Stamp slot notes | The drafter's read of `185b9eef` (S2), lane states (S3), Q20 to Q24 defaults (S4). Every slot is still four underscores |

Kit now: 352 lines, 124731 bytes, sha256 `9e0ab545e5325cb411dbfb5b750a4f21fcdd06cd26206b9bf3858381f7d12a31`, ASCII only. 8 unfilled slot lines, as the kit says. The T1 block is unchanged (`6cb8b5a1...`, 8 lines, 264 bytes).

The sidecar was rebuilt by `r2/scratch/sidecar2.py` (234 lines):
- 56 kept (the same id).
- 141 moved (the same literal on a new line number, the old id named).
- 98 of the kept and moved lines sit on an edited line and carry their family's [A1] re-measure after `||`.
- 27 new literals, each with its own measurement.
- Extra lines: FROZEN, LOAD, TOOLS, PROTO, MUTANTS, PROBES, CHAIN, SCANS, KIT.

`stamp_check.py`: 224 claims, 224 measured, rc 0.

### Re-measured, with instrument and control
- **Origin** (`gh api -X GET`, project `GH_CONFIG_DIR`, 17:14:34):
  - `.private` and `.permissions.push` are both `true`.
  - `main` is `185b9eef`. Pull requests 1 to 16 are merged; 16 is lane I's, at 2026-11-22T04:08:36Z. Open pull requests: 0. No `b1840` ref.
- **Hosted run of `185b9eef`:**
  - `hosted2.py` with `--total 1524 --rules 478 --skipped-linux 4 --skipped-windows 19 --unit 111 --floor 111 --hardened-scan` printed `PASS`. The control `--skipped-linux 5` printed `FAIL 2`.
  - The round-1 `hosted.py` with the right totals printed `FAIL 2` (`Ran 53 tests in`, `UNIT-TEST FLOOR: ran 53, floor 53`).
  - The scan's proof lines `25 of 25`, `objects of this commit not among them 0` and `no leaks found` still stand, beside the hardened `NEUTRAL-EXPORT` / `NEUTRAL-SCAN-REACH` lines.
- **Tree** (git, fresh clone):
  - 478 files.
  - The UniversalPrint library and its tests are unchanged: 14 `Ipp/` files; 12 `.cs` test files, 7 of them with `using Xunit;`; 137 methods by the indented pattern, 0 at column 1.
  - 0 files name `CertificateRequest`, `ExportPkcs8PrivateKey`, `X509Chain` or `uprint/`. The control `LocalSecretStore` finds 18.
  - The Server still references only Core.
  - `Jobs` references UniversalPrint. No project references both Adapters.Oxpd2 and UniversalPrint.
  - Lane E's store names begin `oxpd2/`, lane D's `sessions/`. Nothing else uses `uprint/`.
- **Secret store:** the four `ISecretStore` members are on the same lines. Lane SL added `ISecretStoreInventory`. README: "in clear" is at 57-58, the key ring at line 20. `MaxValueLength` is at `:31`, the name rule at `SecretNames.cs:7`, the internal constructor at `:9`.
- **Design pointers:** round 1's `pointers.py`, re-run unchanged, printed `POINTERS: 38 ok, 0 bad`, and its control was False. No new `CLARIFICATIONS.md` entry after C-45 names Universal Print, certificates or device tokens (by grep).
- **Toolchain:** `.tools/dotnet` 10.0.404, gitleaks 8.30.1, reference pack 10.0.15. The documented members are present (control 0). `SYSLIB0057` gives 1 hit (control 0). The package cache holds 121 entries.
- **Machine:** at 17:25:11, load 6.69 (my runs), 995 GiB free. 6 panes, no OXPd2 pane. The lock folder was absent between jobs.
- **Gitleaks rows** (round 1's `glrows.py`, re-run):
  - Same result as round 1, except F10: rc 0 on this random sample (1 in round 1). The kit now says so.
  - F12 (the openssl private key, the control) fired `private-key`. The key file was moved to `r2/_quarantine/gl/` and never printed.

### The prototype (every job through the round's `heavy.py` unchanged, lane folder `r2`, wave lock by `mkdir`, every lock wait 0, load1 1.36 to 6.27)
| Label | rc | What it showed |
|---|---|---|
| `restore-t1` | 0 | T1 placed (`cmp` 0, numstat 3/0). The restore changed 4 lock files. `lockrule.py`: PASS. Controls: a planted package row gave FAIL 4; `datasec.suite.secrets` struck from the allowed names gave FAIL 4 |
| `build-stubs` / `test-stubs` | 0 / 2 | 0 warnings. `total: 1570, failed: 44, skipped: 4`: every new cell red except L03 and L04 |
| `build-green` / `test-green` | 0 / 0 | `total: 1570, failed: 0, skipped: 4` |
| `mut-*` (26) | see the sidecar line MUTANTS | Every kit mutant is red on its cell, except mRaw. mRaw is GREEN because (5b) also refuses trailing bytes; it is red as mRawStrict. mStatic was GREEN until the L04 property check, then red as mStaticProp. Each mutant was undone by copy (`cmp` equal) |
| `probeStrictOff` | 2 | Probe P1 with (5b) off, 4 runs: accepted one-byte changes at 513 (05 to 04) and 519 (00 to 01). The probe file was quarantined |
| `probe-collision` / `-ctl` | 1 / 0 | `CS0104` on `DeviceTokenHolder` and `DeviceTokenHolderOptions`. The control builds |
| `test-frame` | 2 | The outside-the-frame probe (below). Quarantined |
| `build-green2` / `test-green2` | 0 / 0 | With D19, D20, C12, C13 and the L04 setter check: `total: 1572, failed: 0, succeeded: 1568, skipped: 4` |
| `restore-locked*` | 0 / 0 / 1 / 0 | Without `--force`: "All projects are up-to-date for restore." even over BASE's lock file. With `--force`: the control gave `NU1004`, the real files rc 0, lock sha256 4 OK |
| `build-chain`, `test-chain`, `publish-linux`, `publish-windows` | 0 | `GUARD: clean (10 files)` and `(11 files)`. Unittest `Ran 111 tests`, `OK`. `repo_rules.py` without `--source-documents`: `RULES: clean (484 files)`. Controls in a throwaway copy: R5, R7 and R8 fired |

**Scans on the prototype:**
- gitleaks over the clone: rc 0. The 11 changed files under neutral names: rc 0.
- `boundary.py`: clean; controls 19 of 19 fired.
- High-variety literals: 0; control 1.
- `words.py` over the 1880 added lines gave 6 hits, all in the prototype's own names (`x32`, `x1`, a `...Gate()` helper, `round`). The kit now warns of them. `commit-message.txt` is clean, and `--control` printed 13 of 13.

**Still PREDICTED or UNMEASURED:**
- The seat's totals: 1524 plus its cases. The prototype added 48.
- Every hosted leg of a lane head.
- `X509Chain` with a custom root on Linux and on the hosted Windows image (MEASURED on macOS arm64 only).
- DPAPI-NG under these cells.
- The real issuer.
- Whether the service accepts the request.
- The neutral scan of a lane commit (I made no commit).

### Outside the frame (DRAFTER_RULES; stamp checklist item 11): what each custody path is handed that is not the tested shape (probe `r2/scratch/probe2/FrameProbeTests.cs`, now kit rows H22 to H27)
- **Key record write (`CreateRegistration`):**
  1. A store whose older stored form is put back after an attach. `TryGetCertificate` reads false and a second attach is accepted (H26, a named limit of the store).
  2. A `Put` that throws after the key exists in memory. D12 covers it: no id returned, buffer cleared (R04).
  3. A second process over the partition. This is the store's named limit.
- **Certificate attach (`AttachCertificate`):**
  1. Two concurrent attaches: both accepted 20/20 (fixed by D19, C12).
  2. A self-signed certificate over the right key configured as an issuer: accepted (fixed by D20, C13).
  3. A leaf marked `CA:TRUE` by the trusted issuer: ACCEPTED. It is kept a named limit (Q24), because the real certificate's extensions are UNMEASURED.
  - Also: a leaf with an unknown critical extension is refused by the chain (`IssuerNotTrusted`), and changes outside the signature were accepted before (5b) (H24).
- **Device-token custody (`CloudDeviceTokenHolder`):**
  1. N callers refused with one token: N+1 renewals before Q20 (b).
  2. A caller cancelling its own wait: it gets `OperationCanceledException`, the flight continues, one issuer call (H27, T10).
  3. A late answer after `Remove`. This is T08 and the mutant mLateRemoved; the late answer is disposed.

**What the seat must never print or write (locations only, never values):**
- No private key, PKCS#8 form, PEM text, synthetic CA or leaf certificate bytes, or token bytes, in STATUS, a log, an exception text, test output (`SequenceEqual` only, never `Assert.Equal` on bytes), a file outside a test's own temporary folder, or a commit.
- No record of the store and no store key file is ever copied out of the test folder.
- A scanner control key is made at run time in the lane's scratch, never printed, and moved to `_quarantine`.
- Name only the locations: `uprint/<id>` as a pattern, the store root as a path, `3_Access_Keys/` and `4_Credentials/` by name only.
- I followed the same rule: no key, certificate or token value was printed in any log I read or wrote (the probes print positions, reasons and counts only).

### New Questions (each with its default; Q1 to Q19 unchanged)
- **Q20 (STOP-CLASS, S4 in words):** (a) the `Cloud` prefix on the four token types; (b) `Invalidate(id, refused)` with the completed-flight rule. Alternative: the round-1 names and `Invalidate(id)`. The state table and the evidence are in the kit.
- **Q21:** add rule (5b), D18.
- **Q22:** the Jobs lock files are rewritten by the restore and judged by the lock rule.
- **Q23:** attach is serialised by one lock per instance, D19.
- **Q24:** a one-element chain is refused (D20). A leaf marked `CA:TRUE` stays a named limit.
- **STOP-class at S4:** Q7 and Q20, both in words.

### Reading load (new)
- This kit, 124731 bytes.
- Items 2 to 4 and 6 at `185b9eef`: 122572 bytes.
- The five docstrings of the new gate folder: 4975 bytes.
- The 19 pointer lines: 8171 bytes.
- New item 8: 7825 bytes.
- **Total: 268274 bytes, about 67K tokens.** Round 1 was 104610 plus about 118 kB.

### Outside the fences (disclosure)
- **Writes:**
  - The kit, its sidecar and this report, each through a temp file and `os.replace`. The three `.pre-s308-remeasure` copies were left as they were.
  - Files under `fleet/state/s308/d1898/`: the new `gate/` (6 files copied, unedited) and `r2/` (the clone, logs, scratch programs, the prototype, publish outputs, `_quarantine`).
- **Inside my own scratch clone** (push URL `invalid://no-push`; no commit, no ref written): files added and edited; one `git add` of `src` and `tests` (index only, for `repo_rules`); and a throwaway local clone of it, used for the rule controls, now in `_quarantine/ctl/`.
- **The one write in the OXPd_2 project folder:** the shared heavy lock, which `heavy.py` took by `mkdir` and released by moving it into `r2/_quarantine/locks/`. The project's package cache was read by the restores.
- **GitHub:** `gh api -X GET` only.
- **Not done:**
  - No git verb in any project tree.
  - No Jira call, no message.
  - No `cd`, no delete. Probes and stubs were moved to `_quarantine`.
- **One throwaway RSA key** was made by `openssl` for the scanner control, never printed, and moved to `_quarantine/gl/`.
- **Not read:** `Source_Documents/`, the NAS library, any key folder, any other project, any decision card.
- **Hook refusals:** two Bash calls were refused by hooks (a `..` path, and an unquoted `$H` command word) and re-issued.
