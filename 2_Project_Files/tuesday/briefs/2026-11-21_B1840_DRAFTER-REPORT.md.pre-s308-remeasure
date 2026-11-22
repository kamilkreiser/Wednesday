STARTABLE: YES - the kit is complete and every literal is measured (stamp_check: 203 claims, 203 measured, rc 0; pointers 38 of 38 on their lines, control fires). The lane waits on no other lane at compile time and shares no tracked file with any lane: there is no solution line. ONE stop-class question: Q7, the issuer rule. By default a configured issuer is required and an empty set refuses every certificate. Tuesday must answer it in words at S4. By the plan's landing order the lane lands after lane I.

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
