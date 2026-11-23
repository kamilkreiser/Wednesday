STARTABLE: NO (as commissioned). It becomes YES when the stamp answers Q1 IN: widen the owned paths by `StubDevice.cs` lines 180 and 182, the test pin that counts binding ports. The kit is fully drafted, measured and built on that default.

# B2014 DRAFTER REPORT: lane CT, HP's OXPd 1.x descriptions for first-run steps 2 to 4 (seat `Datasec/OXPd2-X60`)

Read-only drafter (Opus), 2026-11-23 22:57 to 23:46 AEDT. Kit: `tuesday/briefs/2026-11-23_B2014_SEAT-X60_oxpd2-ct.md`, sha256 `517e740f...` (64446 bytes before the stamp). Sidecar: `.measured`, where `stamp_check.py` reports 119 claims, 119 measured, rc 0. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s319/d2014/`. Seat tools: `<d>/seat-tools/`, 12 files.

## BLUF
- **The nine files are taken from the pinned jar and checked, MEASURED.** `fetch_ct.py` hashes the jar (`f2bb325f...`, equal to the README pin) and runs `unzip -p` on nine named entries. Result: `FETCH: 9 of 9 equal` against B2012's list.
- **STOP-CLASS finding (Q1).** `tests/Datasec.Suite.Adapters.Oxpd1.Tests/StubDevice.cs:180` (BASE) throws unless the committed bindings hold exactly **4 ports**. With 7 bindings, 26 of the 40 Oxpd1 cells go red (C07 and every cell that starts the stub). This was MEASURED twice: in the prototype, and in the frozen clone with `2-fix.diff` reversed. The commission owns only `ContractTests.cs`, and only for a count or list pin. C01 is such a pin (`14` at line 66), so that change is in scope. `StubDevice.cs` is not owned. Without moving its pin (`4` to `7`, and the message text "four" to "seven"), the lane cannot be green. The kit builds that change and REFUSES unless S4 answers Q1 IN.
- **A README sentence becomes false (Q2).** `src/Datasec.Suite.Adapters.Oxpd1/README.md:74-76` says the step 2 to 4 descriptions are "not under `contracts/oxpd1/hp/`". This commit makes that untrue. The kit's default is a separate 2-line patch, `3-adapter-readme.diff`, applied only with Q2 IN. Reason: the commission's "no adapter source" is read as meaning `.cs` files, not READMEs.
- **Frozen run (`<d>/clone2`, MEASURED):**
  - Red first (list and count, no files): Oxpd1 `Total: 40, Errors: 0, Failed: 2`. C01 has 9 `missing:` entries; C02 has `Actual: 11`.
  - Files added, port pin not moved: `Failed: 26`.
  - All patches applied: `Failed: 0`.
  - Red proof: `REDPROOF: 9 of 9 MATCH, 9 of 9 undone equal`. Each row changes the first CR of one file to a space, and only C01 and C02 go red.
  - Whole solution: `total: 2054, failed: 0, succeeded: 2050, skipped: 4`. No new cell, so the total is unchanged.
  - Lock files: 34 of 34 equal.
  - Rules and unit tests: `RULES: clean (656 files)` (647 + 9) and `Ran 111 tests OK`.
  - Release guard: `GUARD 14 / 15` for the two publish folders.
  - `checks_ct.py`: 7 of 7. Without the README option it gives 6 of 7, which is the control.
  - `WORDS: clean (2 files)`. Gitleaks rc 0, with the control rc 1.
- **Authority, per the ADDENDUM of 23:24.** The ruling is C-56: heading at CLARIFICATIONS line 382, his words at line 394, the settlement at line 414. His tap was option b, "Keep HP's files in the repository", and his words were "hp files have been provided to us" and "we can store them where we want (and will try to do it safely)". C-74 (line 754) is his 17:56 note. The kit's AUTHORITY section says C-56's card was about the OXPd 2 files, and that reading it as covering these 1.x files is the coordinator's reading. The README and the commit body quote his words with their dates but no C-number, because the frozen `words.py` counts clarification ids as hits (Q4).
- **No licence text names these files or the WSDL folder.** I counted lines in `1_Project_Definition` (excluding Source_Documents and Briefs) that hold a licence word and "wsdl": 4. I read all four; none is a licence on these files. R32 (the reverse-engineering clause) is the known open item already covering the 14 files. This is not a STOP under the commission's rule.

## Facts re-measured (instrument)
- **Origin main**
  - `e39396f91dbfba3c46cc43d7790adb59581d2853`, tree `4af54a4b...` (`gh api -X GET .../commits/main`, 22:59). The `clone.py` reference listing at 22:59 and 23:15 shows the same.
  - 0 open pull requests. Pull requests 41 and 42 are merged. 0 `b2014` refs.
- **BASE hosted run**
  - `hosted3.py` (23:16) prints `HOSTED e39396f9...: PASS` at `--total 2054 --rules 647 --skipped-linux 4 --skipped-windows 21 --unit 111 --floor 111 --hardened-scan --guard-linux 14 --guard-windows 15`.
  - Run 45167272161.
- **ContractTests.cs**
  - C01 pins the count: `ContractTests.cs:66`, `Assert.Equal(14, ...)`.
  - `Fingerprints` is called by C01 and C02 only.
  - The list check is by hash and by membership. There is no hard-coded list.
- **Test binding**
  - `TestSoap12Binding.wsdl` holds 17 live operations.
  - B2012's count of 19 includes 2 operations inside XML comments: `AsyncEchoBinaryComplete` and `AsyncEchoStringComplete`.
- **The nine files and their bindings**
  - Each new binding has 1 port, and its EndpointReference uses the 2005 namespace, so C07's 2004 namespace use stays at 0.
  - 48 new soapActions, distinct within each binding.
  - `uiconfiguration.wsdl` and `uiconfiguration.xsd` hold bytes above 0x7E (3 and 9). All nine use CRLF line ends, so the kit copies them with a program rather than a patch (D1).
- **Rulings today**
  - `kam_rulings_today.sh` has 19 lines.
  - Counts: contract 0, wsdl 0, certificate 0, button 0, test service 0, licen 1 (the 17:56 note). The control `printer` counts 4.
- **Source hashes**

| File | sha256 |
|---|---|
| commission | `5797c47c...` |
| B2012 | `f49ee742...` |
| B2005-B2006 commission | `86d99993...` |
| B2006 stamped kit | `54439952...` |
| B1944 commission | `4107e8d0...` |
| DRAFTER_RULES | `1c51fc0f...` |
| CLARIFICATIONS | `cdfb76f2...` (830 lines) |

## D-decisions (the coordinator's defaults, in the kit)
- **D1.** The files come from the jar through `fetch_ct.py`, never through a patch.
- **D2.** The list is sorted by path, with BASE's 14 lines kept byte for byte.
- **D3.** The port pin is set exactly to 7, not loosened.
- **D4.** The adapter README is made true.
- **D5.** The red proof makes a 1-byte change (CR to space) that keeps the XML valid.
- **D6.** No new cell: C01 already does the job, and it was proven red on each of the 9 files.
- **D7.** One commit, with the rebase rule applied before the first push.
- **Gate:** I recommend **G2 on Opus**. The change is data and docs plus two test pins, with no device code and no secret. Opus rather than Sonnet because it fixes the project's contract source.

## Q-questions (default in brackets)
- **Q1 (STOP-CLASS):** widen the owned paths to `StubDevice.cs:180,182`. [IN]
- **Q2:** apply the adapter README fix. [IN]
- **Q3:** the files go in `contracts/oxpd1/hp/`. [yes]
- **Q4:** repository text quotes his words by date, never by C-number. [yes]
- **Q5:** landing order with W2 and the records lane. [either]
- **Q6:** seat setup. [Opus; READY at Step 0 + 90 min; push by Step 0 + 60 min; pane X60; G2 on Opus, round 1 of 2; hard stop 03:30]

## UNMEASURED / NEVER RUN
- `clone.py` in seat mode.
- The commit and its identity.
- The `run_step.py` neutral scan on this lane's commit.
- The push and its read-back.
- Every hosted leg on this lane's head.
- The rebase.
- `fetch_ct.py`'s two refusals: wrong jar, and file already present.
- Windows and Linux: the drafter ran macOS arm64 only.
- Whether HP's "self-signed ... not recommended/supported" excludes a development root CA.
- The M577's Test-service MinorRevision.

## Outside the fences (disclosure)
- **NAS:** I read only the jar, by `shasum` and `unzip -p` / `unzip -l` on it. I wrote nothing to the NAS. I opened nothing else in HP's library.
- **Project:** I read files under `1_Project_Definition`, excluding Source_Documents (never opened or listed).
- **Lock and heavy jobs:** I used the shared heavy lock through `heavy.py` for every dotnet job, with lock waits of 0 to 4.
- **Commands outside my two files:** I ran `kam_rulings_today.sh`, which is read-only.
- **What I wrote:**
  - the kit, its `.measured` sidecar and this report;
  - scratch under `<d>/` (clones, logs, seat-tools, the quarantined gitleaks control).
- **Hook refusals:** two, both honoured.
  - A `=====` echo was refused. I replaced it with `----`.
  - `git -C $C apply` was refused because the hook could not resolve the variable. I re-ran it with the literal absolute path inside the drafter's scratch, which is inside TUESDAY.
- Nothing was sent to any human, GitHub received GET requests only, and nothing was deleted.
