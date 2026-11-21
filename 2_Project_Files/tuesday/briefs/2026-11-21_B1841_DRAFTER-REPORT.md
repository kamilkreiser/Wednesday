STARTABLE: YES - the kit can be stamped and launched against main 5e36d8dc now; Q1 (where the spool key lives) is STOP-CLASS and Stamp S4 must answer it in words, because the default departs from the plan's "(key from C15)".

# B1841 DRAFTER REPORT | lane G of commission B1840-B1842 | Datasec / OXPd_2 WP1.7 in part (scan receiver, encrypted spool, Print-Job sender)

Drafted 2026-11-21, 17:07 to 17:24 AEDT (clocks by `date`), by a read-only Opus drafter for Tuesday. Files: kit `2026-11-21_B1841_SEAT-X23_oxpd2-wp17-scan-and-print-jobs.md` (107973 bytes, 394 lines), sidecar `.measured` (202 claims, 202 measured; `stamp_check.py` exits 0), this report. Scratch: `fleet/state/s304/d1841/` (main tarball, a draft-mode scratch clone of the origin that cannot push, the lane's `gate/` folder, pointer and sidecar programs, gitleaks rows, hosted-run logs).

## BLUF
1. The kit builds ONE library `src/Datasec.Suite.Jobs` and ONE test project: an encrypted spool (per-job AES-256-GCM chunks, a per-job key, wiped per job, per session, at expiry and at start), a streaming multipart scan receiver (the shared framework's `MultipartReader`, caps counted on bytes received, a 10-minute bound, a per-job secret compared in constant time over SHA-256), and an IPP Print-Job sender with Get-Job-Attributes tracking over an `IIppTransport` interface that has only a test fake. No package, no workflow change, two slnx lines (after `Core` and `Core.Tests` on 5e36d8dc, MEASURED by `place.py`).
2. **Two corrections to the wave-3 plan (MEASURED at 5e36d8dc):** (a) the landed `IppRequestBuilder` builds Get-Jobs and Acknowledge-Job only (`IppOperation.cs:4`), so "a Print-Job sender over the landed request builders" is not possible as worded: the lane builds Print-Job and Get-Job-Attributes from the public `IppPacket`/`IppValue` types; (b) `IppReader` holds a reader forever on a source that never returns (`IppReader.cs:19-20`), so every read of a printer answer is bounded by this lane.
3. **Q1 departs from the plan's wording on purpose:** the default keeps the per-job key in memory only (no job survives a restart, so a stored key buys only a key on disk, a store write per job, and the `ISecretStore.ListNames()` throw on one unreadable record that seat X18 measured). Alternative A is the plan's words (key through `ISecretStore`, frozen text T1A provided); Alternative B is Data Protection.
4. The kit carries B1831's form and tools, plus three lessons from lanes C and D: words scan without the lock files (`linux-x64`/`win-x64`), the local `repo_rules.py` run WITHOUT `--source-documents` (the key-folder rule and the 37 R5 rows on main are lane R5's), and 30 minutes of lock waits inside the windows (READY at Step 0 + 270, push by + 210).

## Facts re-measured, with instruments
- Origin (`gh api -X GET`, project `GH_CONFIG_DIR`, 17:07:56): main `5e36d8dca42966395ea3dd014c7f788409eb585f`; PRs 1 to 6 merged, 0 open; branch `b1831/wp15-token-broker` at `70c1fad5`; no `b1841` ref; `.private` true, `.permissions.push` true.
- Main's hosted run by the lane's `hosted.py` (17:11:10): `HOSTED 5e36d8dc...: PASS` with `--total 894 --rules 291 --skipped-linux 4 --skipped-windows 19`; control `--skipped-linux 5` -> `FAIL 2`.
- `place.py` (lane G copy; `diff` against B1831's: 3 lines) on a scratch copy of main's slnx: `PLACED: 2 lines (src at 6, tests at 16)`, both folders ordinal; after `--write`, `--dry` -> `REFUSED: already present`, rc 2; on lane D's branch slnx: src at 6, tests at 17.
- `repo_rules.py <scratch clone>` (no flag): `RULES-NOTE: R5 hash half NOT RUN (no supplied-source folder here)`, `RULES: clean (291 files)`, rc 0. The seat's `<lane>` has no `1_Project_Definition/` beside it either, so the seat gets the same NOT RUN line (DERIVED from `repo_rules.py:198`).
- `words.py --control`: `CONTROL FIRED: 13 of 13`; the commit message: `WORDS: clean (1 files)`; `round 2` counts, `RoundTrip` does not (measured, kit corrected).
- Reference packs 10.0.15: `MultipartReader` and its three limits, `MultipartSection`, `MediaTypeHeaderValue`, `ContentDispositionHeaderValue`, `AesGcm` (+ctor, `IsSupported`), `FixedTimeEquals`, `TimeProvider`, `Base64Url`: 1 each; control 0. Package cache: 64 entries, the two ASP.NET Core runtime packs present, nothing matching `webutilities|multipart|pdf|ipp`.
- Lock files of Secrets and UniversalPrint at main list no package (framework reference and project reference fetch nothing: DERIVED for Jobs).
- gitleaks 8.30.1, 12 synthetic shapes (G01 to G12): only the random-looking key and secret literals fire (`generic-api-key`).
- Pointer table: 33 fragments on their lines (pointers.py), control False; `02` 1276 lines, `03` 667.
- Toolchain 10.0.404; load 2.58; 1003 GiB free; no `.tools/b1841`, no lock folder; 0 OXPd2 panes.

## Chain inputs (DRAFTER_RULES MEASURED LITERALS item 4)
| Step | Needs | Produced by |
|---|---|---|
| 0 | the stamped kit, CLARIFICATIONS, design lines | BASE (Tuesday's stamp) |
| 1 | gate folder, clone, frozen blocks, slnx | the drafter's `gate/` (exists); `clone.py`; the Step-0 copy |
| 2 | T1/T1A, T2 | Step 1 extraction |
| 3 | the projects and stubs | Step 2 |
| 4 | red cells | Step 3 |
| 5 | green tree | Step 4 |
| 6 | staged tree, `commit-message.txt` | Step 5; gate |
| 7 | commit; base hosted numbers | Step 6; Step 1 |

## D-decisions (all Tuesday's defaults as coordinator, each a Question)
D1 key in memory; D2 GCM chunk format with job/file/chunk/final in the associated data; D3 generated names only; D4 caps 512 MiB / 1 GiB / 500 files / 20 GiB / 8192 header bytes / 16 headers / boundary 1-70; D5 monotonic clock only, 10/30/60 min, no timer; D6 one secret, several uploads, one `JobNotFound`; D7 everything under the root removed at start; D8 key cleared before the folder is deleted; D9 IPP 2.0, six operation attributes, job attributes limited to main's `CreatableJobAttributes` and refused otherwise; D10 transport interface; D11 send 30 min, answer 60 s, 64 KiB header bound, main's success list, `PrinterBusy` returned; D12 poll 5 s, 30 min, 3 failures; D13 a failed upload wipes the whole job; D14 masks; D15 no log/network/package; D16 `JobBusy`; D17 18 reasons; D18 code rules.

## Questions for Tuesday (each with its default)
Q1 STOP-CLASS spool key: memory only (A: `ISecretStore`, T1A; B: Data Protection). Q2 GCM chunks. Q3 names discarded. Q4 the caps above. Q5 monotonic; 10/30/60 min. Q6 secret serves several uploads (vs `02:528` "one-time"). Q7 remove at start. Q8 key first. Q9 list refused otherwise. Q10 interface and fake. Q11 30 min / 60 s / 65536. Q12 5 s / 30 min / 3. Q13 whole job wiped. Q14 masks, no printer text. Q15 G1, second reader on D2, D6, C06. Q16 `JobBusy`. Q17 18 reasons. Q18 names. Q19 270/210, pane X23. Q20 start before lane F lands (F does not change `Ipp/` and adds no slnx line).
Not decided by the kit: where the host reads the scan secret (`02:528` against `02:623` "Never in ... URLs"); the spool root and Windows ACLs; who calls `Sweep`/`WipeSession`; what HP devices send (Monday's printer test).

## UNMEASURED
How `MultipartReader` treats a missing closing boundary, a boundary-less preamble and its own defaults (cells C01-C03 settle it); `AesGcm.IsSupported` on the seat's Mac; the build of T1/T1A/T2; every hosted figure for the lane's head; how HP devices post scans (`tmJob`/`tmImage`); whether a model accepts the Print-Job as built; Microsoft's or HP's sizes and rates behind the caps and bounds.

## What I did not read (disclosure)
- Kit B1829 NOT whole: its headings, its Q10 and C7 rows, and its STATUS DEVIATIONS only (B1831, read whole, carries its tool set and wording lessons). The verdicts B1809 and B1824 not read (named by the commission for lane F's secrets form; this lane does not use the secret store under Q1's default). The wave-1 and wave-2 commissions, B1831's commission and kit, B1837's plan, B1832-B1837's commission, DRAFTER_RULES and the B1840-B1842 commission were read whole.
- `02` and `03` beyond the 33 pointer lines and the C15/C17 rows and section 6.2; A3 beyond lines 26, 182-200, 315; no Workpath source; nothing of `Source_Documents/`, the NAS library, any key folder, HPSM-POC or another client.
- Lane B1838/B1839 gate commissions, lanes E/F/H/I/K kits (being drafted), the B1816 records kit.

## Outside the fences
Nothing written outside my three files and `fleet/state/s304/d1841/`. The scratch clone was made by `clone.py ... draft` (push URL `invalid://no-push`, no identity copied); no git write in any project tree; no build or test run; no Jira, no message. `gh` GET only. The gitleaks sample rows G06/G07 hold random values made by program in scratch (never printed, not secrets).

## Reading load
Seat: the kit (107973 bytes) plus 133582 bytes over 27 files (sidecar `LOAD`), about 60,000 tokens with the pointer lines. The kit is over the wave-1 guide of "about 100 kB" by about 8 kB (B1831 was 107084).
