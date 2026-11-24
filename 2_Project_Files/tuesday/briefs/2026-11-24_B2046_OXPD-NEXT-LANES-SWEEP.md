# B2046 SWEEP: Datasec / OXPd 2, the build lanes that can start NOW (after the M577 first run)

In-session Opus sweep for Tuesday (s323), READ-ONLY. Read window 2026-11-24 15:18:53 to 15:24 AEDT by `date`. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s323/b2046/` (`pickup_1406_1390.txt`, `jira_get.py`, `jira_get.out`). Marks: **MEASURED** = printed by a read named in section 6; **DERIVED** = my reading of the source; **RELAYED** = read in another file.

## 1. BLUF

| Item | Value (MEASURED unless marked) |
|---|---|
| `main` | `e2a20aefda7d4356af2b264576a7e3faaf0bce2c` (PR 45, W2 round 2, merged 2026-11-23T22:58:41Z), read with `gh api -X GET repos/datasecau/OXPd_2/commits/main` after `gh auth status` printed `kamilDatasec`, the Datasec account |
| Open PRs | **0**. Control: `state=all` returns 45 PRs, 45 merged. 47 branches on origin, 46 of them lane branches (owed 28) |
| Owed items open | **80 of 117.** Predicate: lines of `BACKLOG.md` matching `^\d+\. - \[ \]` (37 match `[x]`; numbered 1 to 117, no gap, no repeat), read about 15:20, before R316 writes. R316 is due to tick 117 (and 112 under its slot) and add 118 |
| Jira OXPD2 | 61 issues, keys 1 to 61 with no gap. 57 not done (`statusCategory != Done`), 4 done (the control). OXPD2-62 does not exist yet, which matches R316 still at Step 0 |
| **Lanes startable NOW** | **4 disjoint lanes: L1, L2, L3, L4 (section 3).** Launch **L1 and L2 first** (each about 2 h for one seat). L3 and L4 follow as the load allows (load1 4.54 at 15:23:51). Six more OXPd 1.x lanes are queued behind L1 because they need the same two folders (section 4) |

**The constraint that sets the count.** Every OXPd 1.x lab lane edits the same two folders: `src/Datasec.Suite.Adapters.Oxpd1/` and `src/Datasec.Suite.Lab/Commands/Oxpd1/`, plus their two test folders. That covers rows 2, 3 and 4 of the first run, `oxpd1 echo`, W1 round 2, LH round 2 and the W2 findings. The verb dispatch alone is in one file, `Oxpd1Command.cs:217-242`. So only ONE OXPd 1.x lane can run at a time. The other startable lanes are in folders that no lab lane touches.

**R316 conflict (named).** R316 (B2045) writes `CLARIFICATIONS.md`, `CLAUDE.md`, `BACKLOG.md` and `5_Project_History/history.md`, and does Jira POSTs on OXPD2. It also owns `.tools/b2045/`. Its STATUS read `WORKING: Step 0, 15:15` and its HARD STOP is 16:44. None of L1 to L4 writes any of those files: build seats are forbidden the records files by their own kits (form of B2021 and B2014, RELAYED), and they push only a branch of the code repository. **Any records lane, including the closures in section 4 R-1, waits until R316 has ended.**

## 2. Per-lane facts

### L1: OXPd 1.x Test service, first-run row 2 (the service on and off, one panel screenshot). RANK 1
- **Scope, in its own words.** B1968 section 2a row 2: "Turn on the OXPd Test service and take one panel screenshot | write; the service turns itself off at every reboot | reboot, or one disable call". Plan 03 §0.4 row 5: "the Test service on and off with a screen capture ... each reads before it writes, each prints its undo (contracts in pull request 43; owed 96)". `contracts/oxpd1/README.md` at main names the operations `IsServiceEnabled`, `EnableService`, `DisableService` and `GetScreenCapture`, with this rule: "**Read first:** `IsServiceEnabled` ... the undo is owed only when the lane turned it on."
- **Owed item / key:** owed 96 (the step-2 part; 96 stays open for steps 3 and 4). No OXPD2 key: `text ~ "Test service"` 0 issues and `text ~ "screenshot"` 1 issue (OXPD2-31, a Passkey question on another subject).
- **Files it would touch (read at main through X62's clone `.tools/b2044/clone`, HEAD = `e2a20aef`, 0 porcelain lines):**
  - `src/Datasec.Suite.Adapters.Oxpd1/`: `Oxpd1Read.cs` (the operation table; its read-only check `ReadOperations` at :80-102 admits 5 reads and requires a `Get` prefix, so `IsServiceEnabled` needs a deliberate, reviewed widening), `Oxpd1Writer.cs` (write kinds at :11-19, :54-56, undo at :167) or a new sibling file, `README.md`.
  - `src/Datasec.Suite.Lab/Commands/Oxpd1/`: `Oxpd1Command.cs` (825 lines, verbs at :217-242) and `README.md` (its Limits :133-135 say steps 2 to 4 are not built).
  - Tests: `tests/Datasec.Suite.Adapters.Oxpd1.Tests/` and `tests/Datasec.Suite.Lab.Tests/Oxpd1/`. The stub already counts 7 binding ports, Test among them (`StubDevice.cs:167-180`).
- **Size:** S, about 2 h for one seat. DERIVED from W1 (B2005, about 23 min of STATUS time) and W2 (B2011, about 2 h). It follows their dry-run, undo and read-first pattern.
- **Gate:** **G1** (device-writing: `EnableService` and `DisableService`).
- **Printer:** NOT needed to build (stub on 127.0.0.1). Its later RUN is first-run row 2, which is **inside the M577 grant row**: "the set-up the OXPd tests need (the printer needs list's section 2a, B1968)". It is no firmware change, wipe or reset (C-72). The run is a separate kit after landing, like B2044, with `--addressing 2004`.
- **Azure:** no.
- **Prior work:**
  - PR 43 (`c5b103ee`, B2014) committed HP's Test, CertificateManagement and UIConfiguration descriptions with the read-first rules.
  - PR 40 (`2e2feae8`, the `oxpd1 read` client), PR 41 (`b4b4ef60`, the writer pattern) and PRs 44/45 (`b0b26b60`/`e2a20aef`, `write` and `undo-owed` with dry run and printed undo).
  - B2044 STATUS: "Row 2 (the OXPd Test service and one panel screenshot): OPEN, NOT BUILT".
  - No branch for it on origin (branch list read).
- **Why first:** it closes a first-run row today, and the same service carries `oxpd1 echo`, which is gate G2 of the S14 path test (B2001 §4.1).

### L2: follow-ups of landed libraries outside the lab (owed 79, 87, 83, 84). RANK 2
- **Scope, in each item's own words:**
  - 79: "refuse a root whose path is not `/` (`InvalidArgument`, one more DA14 row) or state the rule in the README and the doc comment; and the cheap hardening the reader names (a chain policy with `DisableCertificateDownloads` on and revocation off)".
  - 87: "one more sentence in the adapter README".
  - 83: "two sentences in a later round of the transport".
  - 84 parts (1) and (3): "one clause ('while the vault answers') and one rewrap in a later Server round". Part (2) is "the logging work's" and is NOT in this lane.
- **Owed / keys:** owed 79, 83, 84 (parts 1 and 3), 87. No OXPD2 key: each item records "Jira: none".
- **Files (read at main):**
  - `src/Datasec.Suite.Adapters.Oxpd2/DeviceAuth/DeviceTokenClient.cs` (owed 79 cites :43, :62, :76) and `src/Datasec.Suite.Adapters.Oxpd2/README.md`.
  - `tests/Datasec.Suite.Adapters.Oxpd2.Tests/DeviceAuthCellTests.cs`.
  - `src/Datasec.Suite.Jobs.Transport/IppTransportException.cs` and `README.md`, text only.
  - `src/Datasec.Suite.Server/README.md`.
- **Size:** S, about 1.5 to 2 h. One code change with one cell; the rest is text.
- **Gate:** **G1** (owed 79 changes the TLS chain policy and the device-root rule).
- **Printer:** no. **Azure:** no.
- **Prior work:** PR 33 (`126c95e8`, device token client), PR 38 (`86473f8a`, contract runtime follow-ups), PR 35 (`cad65b86`, IPP over HTTPS transport) and PR 36 (`df762b28`, server host v0). Each review was GO WITH FINDINGS and the findings were filed as these owed items. No fix round since (each item still `[ ]`).

### L3: WP1.8 OneDrive module, first slice (browse My Drive). RANK 3
- **Scope, in the plan's words.** 03 §4: "WP1.8 | C10 OneDrive module (files subset) | browse, scan to folder, print | Graph integration tests | ... | M". The slice proposed is "browse" only, against a fake Graph on the landed Graph layer (WP3.8). It builds **no** Recent and **no** Shared with me: C-82, C-83, and his 14:05 answer "no deprecated Graph calls" (being recorded by R316 as C-84). Week 2 of §0.5.2 names "WP1.8 OneDrive files subset against the test tenant". The tenant test stays with the tenant.
- **Owed / key:** none open for WP1.8. Owed 115 (OP-20, the `remoteItem` tenant test) and 116 are related. No OXPD2 key for WP1.8 by label (`wp1-*` labels: wp1-1, wp1-3, wp1-4-5, wp1-10 only).
- **Files:** new `src/Datasec.Suite.OneDrive/` and `tests/Datasec.Suite.OneDrive.Tests/`, and **`Datasec.Suite.slnx`** (the only lane that touches it). MEASURED: `OneDrive` and `me/drive` are on 0 lines of `src/` at main, against a control of `GraphClient` on 16 lines in 8 files.
- **Size:** M for the package. The slice is DERIVED at about 3 h, so it is NOT one of the two 2-hour lanes.
- **Gate:** G2 (no device write; tokens come through the landed layer). Tuesday may raise it to G1 if the slice takes a token.
- **Printer:** no. **Azure:** no. **Tenant:** not for the slice.
- **Prior work:** PR 10 (`977cbeb2`, shared Graph layer); reports A11 and B1769 (the OneDrive source read, WP0.6); C-82 and C-83 (two places dropped); 02 and 03 B2037 rounds (18 live calls, 19 with the thumbnail).

### L4: release guard, release mode and name rule (WP0.3; owed 14, 23, 11). RANK 4
- **Scope, in its own words:**
  - Owed 14: "the first release leg must not start before a mode exists in which 0 fingerprints is exit 2".
  - Owed 23: "the development-CA name rule is a prefix, not a substring, and ZIP member names are split on a forward slash only; HP's beta library inside ... a tar or a gzip is not seen".
  - Owed 11: "reads ZIP-format files only".
- **Key:** OXPD2-24 ("[WP0.3] Release guard: release mode, the name rule, publish shapes and certificate forms, before the first package", Backlog).
- **Files:** `build/release_guard.py` and `build/tests/test_release_guard.py`. `build/denylist/dev_ca_sha256.txt` is read only: putting the real fingerprint in is owed 2, which needs the SDK CA file and is not in this lane. `.github/workflows/ci.yml` is NOT touched (its :50 and :80 call the guard).
- **Size:** S to M, about 2 to 3 h.
- **Gate:** **G1** (CI and security control; owed 25 asks for a standing review rule for pipeline files).
- **Printer:** no. **Azure:** no.
- **Prior work:** PR 1 (`7bf37526`, CI skeleton and guard), PR 16 (`185b9eef`, CI guard follow-ups), PR 19 (`4a0a9717`, shapes digest pin). Owed 2, 11, 14 and 23 have been open since 2026-11-20.
- **Why it ranks last:** nothing is packaged before the 20 December build (§0.5.2 week 4), so it can wait behind L3.

## 3. The partition (no two lanes share a file)

| Rank | Lane | Folders it owns | 2 h, one seat? | Gate |
|---|---|---|---|---|
| 1 | L1 Test service (row 2) | `src/Datasec.Suite.Adapters.Oxpd1/`, `src/Datasec.Suite.Lab/Commands/Oxpd1/`, `tests/Datasec.Suite.Adapters.Oxpd1.Tests/`, `tests/Datasec.Suite.Lab.Tests/Oxpd1/` | yes | G1 |
| 2 | L2 library follow-ups | `src/Datasec.Suite.Adapters.Oxpd2/` (DeviceAuth and README only), `tests/Datasec.Suite.Adapters.Oxpd2.Tests/`, `src/Datasec.Suite.Jobs.Transport/`, `src/Datasec.Suite.Server/README.md` | yes | G1 |
| 3 | L3 OneDrive browse slice | `src/Datasec.Suite.OneDrive/` (new), `tests/Datasec.Suite.OneDrive.Tests/` (new), `Datasec.Suite.slnx` | no (about 3 h) | G2 |
| 4 | L4 release guard | `build/release_guard.py`, `build/tests/test_release_guard.py` | about 2 to 3 h | G1 |

**Shared, owned by no lane:** `Directory.Packages.props`, `.github/`, `contracts/`, and the root files except `Datasec.Suite.slnx`, which belongs to L3. If L3 needs a package, that is a stop to Tuesday: one supervised fetch, the C-61 form. The heavy build lock (`wave1-heavy.lock.d`) serialises the seats' restore and build steps. It does not merge their work. Each lane is a squash of its own branch.

## 4. EXCLUDED or QUEUED, with the reason

**Queued behind L1 (same four OXPd 1.x folders; one at a time, in this order):**
- **Q-A: `oxpd1 echo`** (B2001 §4.1 G2: `SyncEchoString` and `AsyncEchoString` with a callback listener, guest credential, refuses the admin-password name).
  - It needs L1's Enable and Disable path on the same service.
  - Its LAN run (G3) is also the test of owed 118 (printer to Mac call back, 192.168.8 to 192.168.20).
  - Kam's 14:58 tap was b "Route both ways" with the note "I would prefer not to move unless you need me to" (RELAYED, DELTA 1405).
- **Q-B: first-run row 4** (a top-level test button, `GetTopLevelButtonRecords` read first, then `RegisterTopLevelButton` and `UnregisterTopLevelButton`).
  - Building it is fine.
  - Its RUN registers "a test button pointing at this Mac" (B1968 row 4), which needs the printer-to-Mac path to be pressed.
  - Also see question 3 (the home-screen switch).
- **Q-C: first-run row 3** (development CA: `ExportCertificates` first, then `ImportCertificate` and `RemoveCertificate`).
  - Building it is fine.
  - **Its RUN waits on a word:** owed 103. HP's line reads "self-signed certificates with the OXPd CA Certificate store is not recommended/supported". Plan 03 §0.4 row 5 says it needs "a word on HP's warning ... which CA the lab uses" from the product owner or the team. That is a meeting subject.
- **Q-D: W1 round 2 (gate B2008).**
  - Owed 93 is open: `Oxpd1Writer.cs:131` still tests `value.UserInfo.Length != 0` at main.
  - Owed 94 is half open: the read before a register landed in PRs 44/45; the README named limit is still open.
- **Q-E: LH round 2 (gate B2009), owed 95.**
  - `LabFiles.cs:28` still uses `File.ReadLines` with no regular-file check.
  - BUT the lab README's Limits now name the shape (`Commands/Oxpd1/README.md:142`: "A credentials file that is a named pipe with no writer blocks the run, as for `oxpd1 read`").
  - That meets the item's own close-out ("or name the shape in the README's Limits"), so it is a candidate records tick. Owed 95 needs no build lane unless Tuesday wants the code fix.
- **Q-F: the W2 gate findings** (owed 106 to 111, Minor and Info, a lab round).
  - Lowest priority: the first run carried owed 112's three preconditions without them (B2044 STATUS).

**Excluded:**
- **The Azure test machine (S14):** C-78 says it is "made only after the home rehearsal passes". That needs Q-A built and its LAN run passed. The `oxpd2-dev-rg` grant covers the VM when it comes.
- **The panel sign-in test (C-76):** needs a test tenant user. OXPD2-61 is Kam's action, Backlog.
- **Spike S2 and the WP2.1 agent side:** the choice of HP's library or Datasec's own client is open (C-74, a kick-off decision, §0.4). It also needs the printer-to-Mac call back (owed 118, untested).
- **WP2.3 (p1 template):** waits on the panel test's result (N-1, C-76).
- **WP1.11 and WP2.2 (admin API and onboarding):**
  - Hosting (N-5) and the deployment tool (N-9; WP0.10's OP-1 to OP-6) are open.
  - WP2.2 includes the CA import of owed 103.
  - Both would also need `Datasec.Suite.slnx`, which L3 holds.
- **WP1.2, WP1.6, WP1.9 (OXPd 2 on a device):** no OXPd 2 printer or simulator. That is [HP] [Steve M T-04] [Kam q34].
- **The lab's WS-Addressing default:** B2044 measured that the M577 refuses 2005/08 and answers 2004/08. Changing the default is in L1's folders and is a choice (question 2), not a startable lane.
- **Owed 15** (a required check by a repository setting) and **owed 18** (hosted-minute billing): organisation or settings, Kam's.
- **Anything to HP, Steve M or any person**, any spend, production, and Fable: none of L1 to L4 needs any of them (all Opus, CLAUDE.md line 7).
- **R-1, records closures, after R316 ends (a records lane, not a build lane):**
  - Owed 116 can be ticked. MEASURED at main: `sharedWithMe` on 0 lines, `drive/recent` on 0, `/recent` on 0, all in `src/` and `tests/`, with `GraphClient` 16 lines as the positive control.
  - Owed 95 can be ticked by its README route (above).
  - The two README "UNMEASURED" addressing lines become one measured device line, if Tuesday takes question 2's default into L1.

## 5. Questions for Tuesday (each with a default)
1. **Launch L1 to L4 although the kick-off grant ends at tonight's meeting and the lanes may land after it?**
   - Default: YES. Launch L1 and L2 now and L3 and L4 as load allows.
   - Land after the meeting unless the re-read with Kam changes scope.
   - The M577 grant (row 1) and the Azure grant (row 2) have no end stated. The meeting ends the kick-off and Fable rows only.
2. **The lab's WS-Addressing default (2005 refused by the M577, 2004 answered).**
   - Default: L1 does NOT change the default. It updates the two README "UNMEASURED" lines (`Commands/Oxpd1/README.md:29-30`, `Adapters.Oxpd1/README.md:25-26`) to state the M577 reading with its source (B2044 R03/R03b). Every device run keeps passing `--addressing 2004`.
   - Alternative: flip the default in L1 (one cell, `AddressingTests.cs`).
3. **Row 4's run and the home-screen switch.**
   - B2044's N2 said "before we add a home-screen app". Kam's 14:56 tap was "Later, when needed" (RELAYED).
   - Default: a top-level test button is NOT a default home-screen app (`SetDefaultApplication` is a separate operation, not called). Q-B's run may go ahead inside section 2a once the call back works.
   - Alternative: hold Q-B's run until Steve M answers the switch ticket.
4. **Fold `oxpd1 echo` (Q-A) into L1 so one seat does the whole Test service?**
   - Default: NO. L1 stays at about 2 h and echo is the next lane in the same folders.
   - Fold it in only if a seat can take about 4 h before the 17:00-ish wave limit.
5. **L3 before the meeting rules the 20 December contents (§0.5.3 question 1)?**
   - Default: YES. OneDrive files are in every variant of Tuesday's proposal, and the browse slice drops nothing he could rule back in.

## 6. HOW MEASURED / NOT TESTED
- **Clock and load:** `date` 15:18:53, 15:21:38 and 15:23:51 AEDT; `uptime` load 4.54 3.47 3.05 at 15:23.
- **GitHub:** with `GH_CONFIG_DIR='<OXPd_2>/4_Credentials/.gh-config'`, `gh auth status` printed `Logged in to github.com account kamilDatasec`. GET reads:
  - `commits/main`
  - `pulls?state=open&per_page=100`: 0
  - `pulls?state=closed`: 45
  - `pulls?state=all` merged count: 45
  - `branches?per_page=100`: 47 names
  - Every list was under 100, so one page is the whole list.
- **Code at main:** read through `<OXPd_2>/.tools/b2044/clone` (X62's clone). `git --no-optional-locks rev-parse HEAD` = `e2a20aef...`, equal to origin main; `status --porcelain` 0 lines. Reads: `ls-tree`, `git grep -c` with a control, `sed`/`grep -n` on named files. The project's own checkout `2_Project_Files` is STALE (HEAD `6e2629bc` on branch `b1764/wp03-ci-skeleton`; `e2a20aef` is not a valid object there), so nothing was read from it. I did not fetch (no write).
- **BACKLOG.md:** a Python regex over the whole file (`^\d+\. - \[[ x]\]`): 117 lines, 80 `[ ]`, 37 `[x]`, numbers 1 to 117 with 0 repeats. Items 79, 83, 84, 87, 93 to 96, 103 and 106 to 117 were read whole.
- **Jira:** GET only, `/rest/api/3/search/jql` paginated by `nextPageToken` to `isLast`. The credentials were read by name in-process from `<OXPd_2>/4_Credentials/.env` after `ls -a`; names only were printed (`JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`, `JIRA_PROJECT_KEY`).
  - `project = OXPD2`: 61. Not done: 57. Done (the control): 4.
  - Phrase searches: `"Test service"` 0, `echo` 0, `addressing` 0, `"home screen"` 0, `callback` 0, `"call back"` 0, `screenshot` 1 (OXPD2-31), `button` 1 (OXPD2-31), `certificate` 3 (OXPD2-61, -24, -1).
  - Controls: `zzqxnonexist` 0 and `OXPd` 32 (non-zero), so the zeros are real.
  - Two issue GETs: OXPD2-31 and OXPD2-24.
- **Documents read:**
  - `<OXPd_2>/CLAUDE.md` whole.
  - 03 §0 (lines 7-131) and §4 (lines 255-352).
  - 05: BLUF and "WHAT CAN START" (lines 1-30, 252-273).
  - 02: only the D1 row and C-78 line by grep.
  - CLARIFICATIONS C-72 to C-79 read whole (lines 722-839), plus counts for each lane subject (OneDrive 12, `release guard` 0, `DeviceRoot` 0, `Test service` 0, `screenshot` 4, none on these lanes) and a hold/held scan (no OXPd lane hold found).
  - B2044 STATUS whole.
  - B2045 kit: the write-scope and owed lines by grep (380 lines; not read whole). B2045 STATUS: first 3 and last 5 lines (PENDING; WORKING Step 0 15:15).
  - EXPIRING-GRANTS rows 1-3 and the "move OXPd forward" row whole.
  - The pickup: DELTA 1407 and lines 63-106 (DELTA 1406 to 1390). Its OXPd items are in sections 2 and 4: next lanes per DELTA 1398 item 3, owed 113 and 114 CLOSED (verified `[x]` in BACKLOG), RD-1035 DROPPED (NexusAI, not OXPd), execute hold LIFTED (DELTA 1391), and Q3 "do NOT move OXPD2-60".
  - B1968 section 2a rows 0-6; B2001 §4.1 (the echo verb, G2 and G3).
- **NOT TESTED:**
  - No build, test or run of anything.
  - No lane size was measured (all DERIVED).
  - I did not read 02 beyond two greps, the B2045 kit whole, or the live pane list. The R316 state is from its STATUS file only.
  - I did not confirm that `IsServiceEnabled`, `EnableService` and `GetScreenCapture` need admin and not guest on the M577 (UNMEASURED; B2001 says echo takes guest).
  - The printer, Azure and HP were not contacted, and no Jira or GitHub write was made.
- **Failed reads:**
  - One grep failed by regex limits (ugrep complexity) and one by a hook refusal of an unscoped recursive grep. Both were re-done with narrower reads.
  - One `cd` was refused by the hook, before it ran anything.
