# B1913 OXPd_2 overnight lanes: the no-hardware work, split into lanes that share no file (sweep, READ-ONLY)

Written 2026-11-22 ~20:30 AEDT by sweep agent B1913 for Tuesday (s310), on the commission `2026-11-22_B1913_OXPD-OVERNIGHT-LANE-SWEEP_COMMISSION.md`. Read-only: nothing was written to the project, Jira or GitHub. Scratch and the programs behind every count: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s310/d1913/` (`tree.json`, `pulls.tsv`, `prfiles.tsv`, `jira.json`, `jira/*.txt`, `partition.py`). Who decided: every lane, order and split below is a proposal for the coordinator to decide. It is not the product owner's word. The only words of his quoted here are C-42 and C-68.

## State read (by GET, with controls)
- Main `bf6b441e30900127487145c3b65b29d8cc9eb5ea` (PR 17, 2026-11-22T08:12:41Z), the same SHA Tuesday read at 20:00. Tree: 669 entries and 500 blobs, `truncated: false`.
- 17 pull requests, all closed and merged, 0 open. Their file lists add up to 555 rows, and each PR's count matches its sum (control: PR 17 = 27, PR 6 = 141).
- Jira OXPD2: 25 issues, all `Backlog`, 0 Done, which matches Tuesday's 19:34 count. Only OXPD2-1 (11 comments), OXPD2-2 (2) and OXPD2-10 (1) have any comments.
- Shared files touched by earlier PRs: `Datasec.Suite.slnx` by PRs 1, 2, 3, 4, 5, 6, 9, 10, 12, 13 and 15. `Directory.Packages.props` by 1, 2 and 12. `.github/workflows/ci.yml` by 1, 8 and 16. `Directory.Build.props`, `NuGet.config` and `global.json` by PR 1 only.
- Each project has its own `packages.lock.json` (24 on main). A lane changes a lock file only when it adds a reference to that project.
- Live seat X27 (B1912) committed at 20:09 (its `.tools/b1912/logs/commit.log`). It owns `tests/Datasec.Suite.Sessions.Tests/Fakes.cs` and `RefreshBoundCellTests.cs` until it lands.
- Machine at 20:09: load 3.86 / 3.69 / 3.67. No `.tools/wave1-heavy.lock.d` exists.

## 1. BLUF
- **Seven lanes can start tonight.** Five are code or test lanes (A1, U, T, S, D), one is a build-guard lane (C) and one is a docs lane (E). All seven are file-disjoint from each other and from X27: 28 pairs checked by `partition.py`, 0 overlaps. The positive control (a lane on `tests/Datasec.Suite.Sessions.Tests/`) did show its overlap with X27.
- **Suggested order:**
  1. **U** (UP registration fix round, G1, S) and **A1** (WP1.4 sign-in state machine, the largest unbuilt package, G1, L) start first.
  2. Then **T** (two held test cells, G2, XS), **C** (rule R6's two shapes plus the Dockerfile digest pin, G1, S), **S** (secret-store guard and owed cells, G1, S) and **D** (audit and duplicate-race limits, G1, S).
  3. **E** (adapter README limits, G2, XS) fits anywhere.
- **A2** (the WP1.4 identity half, C7) is the eighth lane. It is serial with A1 on `Datasec.Suite.slnx` only.
- **No lane touches** `ci.yml`, `Directory.Packages.props`, `Directory.Build.props`, `NuGet.config`, `global.json`, `src/Datasec.Suite.Server/` or any Sessions file. A lane that finds it needs one of these STOPs.
- **The paper packages are already drafted and waiting on the product owner:** WP0.5, WP0.6, WP6.7, WP0.8, WP0.9, WP0.10 and the WP3.5, WP3.6 and WP3.11 first reads. None is a lane tonight.

## 2. The lanes

### Lane A1: WP1.4 sign-in state machine (C5), with the binding rule and the four display-name forms. Jira OXPD2-14
- **Scope (OXPD2-14, verbatim):** "Now, without hardware: the card paths, the binding rule, the four display-name forms, sessions, handles, refresh, events and expiry, unit tests and a restart test with a fake Graph." The sessions part already landed (PR 9, WP1.5), so A1 is the C5 part.
- **Plan wording:** `03:156`, WP1.4: "per-device actor; CSA lookup, known-card paths and a minimal enrolment by device code ...; binding rule; display name in the four forms (F15)".
- **Architecture wording:** `02:365`, C5: "Per-device instance of HPAM's state machine (`AuthPhase`) with the 'stale session' guard ...; triggers: card, QR/phone, panel button, device-code; outcomes: login with identity, enrol, fail, cancel; handles 'same card = sign out', 'other card = switch user', 409 / Concurrency retries, wake-from-sleep races ... a `Channel<T>` per device".
- **Creates:** `src/Datasec.Suite.SignIn/` and `tests/Datasec.Suite.SignIn.Tests/` (neither exists on main). It adds two lines to `Datasec.Suite.slnx`, and **A1 is the single owner of that file tonight**.
- **The identity service (C7):** A1 consumes it only through an interface that A1 defines, with a fake in its own tests. A1 references `Datasec.Suite.Sessions` (`ITokenBroker`) and `Datasec.Suite.Cards` (the read assembler) read-only.
- **Must NOT touch:** any file outside the two new folders and the slnx. In particular nothing under `src/Datasec.Suite.Sessions/`, `tests/Datasec.Suite.Sessions.Tests/` (X27), `src/Datasec.Suite.Server/` (no host wiring) or `Directory.Packages.props` (no new package, because a fetch is supervised: C-61).
- **Card data:** the card key (master list item 1, treated as LIVE) is never used or held. Card data in its cells is synthetic.
- **Depends on:** main only.
- **Review tier:** G1. This is the sign-in path and identity binding, a security surface.
- **Size:** L in the plan ("L: state machine edge cases"). Tonight's realistic target is the actor, the card paths (same card, other card, stale-tap guard), the binding rule and the F15 forms, against fakes. The QR/phone trigger and device-code enrolment can follow in a second commit or night.
- **Authorised by:**
  - C-42 (card option a, "Start the no-hardware work now"; WP1.4 is in its twelve-row table: `BACKLOG.md:406`, `05:264` "Sign-in state machine and token broker against a simulated Microsoft service").
  - C-68 ("keep going if you can").
- **Prior work:** PR 9 (`src/Datasec.Suite.Sessions/`, token broker WP1.5), PR 3 (`src/Datasec.Suite.Cards/`, decoders and assembler), PR 10 (`src/Datasec.Suite.Graph/`). Nothing of C5 exists on main: 0 tree paths under `src/Datasec.Suite.SignIn`.
- **Open points the kit must settle:**
  - The stale-tap fact of owed item 32, which touches the assembler and `02:564`.
  - The panel sign-in page of C-58 (R1-33/R1-34). That page is WP1.6's, not A1's.

### Lane A2 (serial with A1 on slnx only): WP1.4 identity service (C7), the CSA store against a fake Graph. Jira OXPD2-14
- **Scope (`02:367`, C7):** "CSA store (find by card blob, read/write attributes, enrolment, 15-card / 50-value limits, where each phone a user signs in on is a separate card id ...), schema creation cached".
- **Creates:** `src/Datasec.Suite.Identity/` and `tests/Datasec.Suite.Identity.Tests/`, plus two slnx lines **added after A1 lands**, by merging main as B1820 and B1827 did for slnx (history 2026-11-21 09:47 and 15:02).
- **Must NOT touch:** A1's folders, Graph's source (A2 consumes `Datasec.Suite.Graph` read-only), the QR gateway client (WP3.1, not in the twelve), the card key and the Entra auth-code/PKCE flows against a tenant.
- **Review tier:** G1. **Size:** M.
- **Authorised by:** the same C-42 row (OXPD2-14 names C7 "By component: C5, C6, C7").
- **Can start tonight:** only if the coordinator accepts the slnx merge. Otherwise it starts after A1's PR.

### Lane U: Universal Print registration fix round (owed items 52, 53, 54 and 55(1); gate findings B1904 F1/F2 and B1905 F1/F2). Jira OXPD2-18 (WP4.1)
- **Fix 1 (item 52, B1904 F1):** "`DeleteRegistration` does not take the attach lock ... The reader's fix: the delete takes the same lock, plus a cell (a delete during a paused attach leaves no record afterwards)".
- **Fix 2 (item 53, B1904 F2):** "start the issuer call off the caller's path so the bound covers it, plus a cell".
- **Fix 3 (item 54):** the four mutant-killing cells `mNoZeroPkcs8`, `mReadCertLoose`, `mCatchNarrow` and `mFixUndone`; B1905 F2, "no cell pins the chain's own time check or that it runs on the library's clock" (mutants `mTimeIgnored` and `mVerifySystemClock`); and the cheap disposed-token check (probe G03).
- **Fix 4 (item 55(1), B1905 F1):** the s+n signature value, "a named limit, or a rule after the chain build that the signature value lies below the issuer key's modulus, with a cell for s+n". **Which of the two is the kit's choice for the coordinator to make.**
- **Changes:** `src/Datasec.Suite.UniversalPrint/Registration/` (14 files on main, including `RegistrationKeys.cs`, `CloudDeviceTokenHolder.cs` and `README.md`) and `tests/Datasec.Suite.UniversalPrint.Tests/Registration/` (9 files).
- **Must NOT touch:** `src/Datasec.Suite.UniversalPrint/Ipp/`, the UP project file and lock file, `src/Datasec.Suite.Secrets/` (lane S), slnx and ci.yml.
- **Depends on:** main only. Lane S must not change a public member of the secret store (see the partition section).
- **Review tier:** G1. This is key custody and certificate checks.
- **Size:** S (two lock/bound fixes of about 10 to 30 lines each, about 8 cells, one README line).
- **Authorised by:**
  - The items' own text ("owed before the removal flow ... calls `DeleteRegistration`"; "owed before the real device-token issuer lands"; item 54: "test cells and one cheap check, a round of their own with its review").
  - C-42 (WP4.1 is in the twelve: `BACKLOG.md:409`).
- **Prior work:** PR 17 (bf6b441e). Do not rebuild: the custody, the certificate rules and the C01 late-parse fix all landed there.
- **Left out (needs the service or a decision):** items 55(2) to (6) and item 57.

### Lane T: the two held test cells (owed items 47 and 48), test-only
- **Cell 1 (item 47):** "one new theory, `W02_a_body_whose_read_throws_ends_the_receive_typed_and_the_job_is_wiped` (two rows ...) with a private `ThrowingBody` helper, 64 added lines. It kills the named surviving mutant `mReasonDisposed` ... and is green at the head's product code."
- **Cell 2 (item 48):** "A K8 row asserting that an optional null in a client model's body stays `WrongType` closes it" (mutant `mNullStrictToo`).
- **Changes:** `tests/Datasec.Suite.Jobs.Tests/ReceiverTests.cs` and `tests/Datasec.Suite.Contracts.Tests/TolerantReadingTests.cs`. One file each, no product file.
- **Must NOT touch:** any `src/` file, any other test file, slnx and lock files.
- **Review tier:** G2 (tests).
- **Size:** XS. About 64 plus about 20 lines. The W02 cell is named in the third-round kit `1_Project_Definition/Briefs/2026-11-21_B1872_SEAT-X23_oxpd2-wp17-jobs-a03-test-fix.md` and in the B1887 and B1900 records. This sweep did NOT check whether the full 64 lines are held anywhere; the kit drafter should look before a seat rewrites them.
- **Authorised by:** each item's "a later test-only change with its own review". The W02 cell was held out only by the shape of C-65's round ("A small seat fixes only that test helper"), which has since landed. W02 is not on main: 0 lines, per item 47's own control.
- **Prior work:** PR 15 (Jobs) and PR 14 (Contracts tolerant reading).
- **Possible split:** into T1 (Jobs) and T2 (Contracts) if two small seats are free. The two files are disjoint.

### Lane C: rule R6's two quoted-value shapes (OXPD2-25, owed item 51) and the Dockerfile base digest pin (owed item 7). WP0.3, Jira OXPD2-25 and OXPD2-8
- **Fix 1 (OXPD2-25):** "Two shapes leave a value open in YAML while the rule's own quote reading (yaml_scan) reads the line as closed ...". The readers' fix sketches (i) to (iii) are in the ticket. Sketch (i): "take the open-quote reading on the raw line, before the expression [removal]".
- **Fix 2 (item 7):** "the digest is known without a call to that registry (the hosted `linux` job of run `44661506229` printed `mcr.microsoft.com/dotnet/aspnet:10.0@sha256:12b1135f...6586` on 2026-11-20), but the `FROM` line still names the tag; the line stays open until a lane that owns `packaging/` pins it". On main, `packaging/linux/Dockerfile:3` still reads `FROM mcr.microsoft.com/dotnet/aspnet:10.0`.
- **Changes:** `build/repo_rules.py`, `build/tests/test_repo_rules.py` and `packaging/linux/Dockerfile`.
- **Must NOT touch:** `.github/workflows/ci.yml`. Its whole file is fingerprinted (`REVIEWED_WORKFLOW`, 5 hits in `build/tests/test_pipeline_controls.py`), so any edit there needs a person's read. Also off limits: `build/tests/test_pipeline_controls.py`, `build/release_guard.py`, `build/squash_scan.py` and `build/denylist/`.
- **Checked:** neither `repo_rules.py` nor the pipeline-control test names the Dockerfile (0 hits each; control: `ci.yml` names it once, at line 52). Pinning it does not trip a fingerprint.
- **Review tier:** G1 (build and pipeline files: owed item 25's standing rule).
- **Size:** S.
- **Authorised by:** C-67 ("Merge now, the two shapes ticketed as known limits": the ticket is the follow-up) and C-42 (WP0.3).
- **Prior work:** PRs 1, 8 and 16. PR 16 (185b9eef) built R6 to R8, `squash_scan.py`, the second-scan hardening and the release mode.
- **Records point, not a build lane:** OXPD2-20 to OXPD2-24 look largely closed by PR 16. For example, main's README line 79 now reads "the checkout fetches branches and tags, and o[n a pull request ...]". The records seat's item-50 pass should move or comment them.
- **If the C seat is short of time:** split C into C1 (R6) and C2 (the Dockerfile). They are disjoint.

### Lane S: the secret store's removal guard and owed cells (owed items 42(2) and 34 N7, with N2, N3 and N5 if the kit takes them). WP1.1, Jira OXPD2-12
- **The guard (item 42(2)):** the second reader's guard "before any caller is wired: require that the record's key id is a key of this store's ring that is not revoked and that a protect and unprotect round trip of a probe value succeeds under the current key, else `StorageFailed` and nothing removed (about 10 lines)".
- **The cells (item 34 N7):** "cells owed (a revocation alone with no record; the guard with a mixed set of records)".
- **The optional items:** N2 (`RotateKey` can throw after its new key is written), N3 (a partition folder that is a link is not refused) and N5 (the record folder is link-checked at the start only).
- **Changes:** `src/Datasec.Suite.Secrets/` (22 files) and `tests/Datasec.Suite.Secrets.Tests/` (18 files).
- **Must NOT touch:** any public member signature. `Datasec.Suite.Sessions`, `.UniversalPrint` (lane U) and `.Data` build against the store, so a public change would make S serial with U and D. Also off limits: the store's lock file, slnx, and anything Windows/DPAPI-NG (N1, which is UNMEASURED on Windows).
- **Review tier:** G1 (secrets).
- **Size:** S.
- **Authorised by:** C-42 (WP1.1 is in the twelve), and item 42's "each is a later store kit's work".
- **Prior work:** PRs 5 and 11.
- **Left out:** the six product points of item 34 (key lifetime, the 1 MiB limit, the cipher, the DPAPI-NG descriptor, sealed on Linux, rollback). They are questions for OXPD2-1, not code.

### Lane D: the state database's audit-integrity limit and the duplicate race (owed item 43 (1) and (2)). WP1.1, Jira OXPD2-12
- **Fix 1 (item 43 (1)):** "Name the limit ... or close it, for example by refusing in a `ChangeTracker.StateChanged` handler; if 'through the library' is read as any use of `SuiteDbContext`, this is the one item that would be a Major". **The kit decides which, and that decision is the coordinator's.**
- **Fix 2 (item 43 (2)):** "map the key's `DbUpdateException` to `DuplicateDevice` and clear the tracker".
- **Changes:** `src/Datasec.Suite.Data/` (14 files) and `tests/Datasec.Suite.Data.Tests/` (10 files).
- **Must NOT touch:** migrations, which would change both SQL snapshots under `tests/Datasec.Suite.Data.Tests/Snapshots/`. If a fix needs a schema change, it STOPs. Also off limits: `src/Datasec.Suite.Devices/`, `Directory.Packages.props` and lock files.
- **Review tier:** G1 (persistence and audit integrity).
- **Size:** S.
- **Authorised by:** C-42 (WP1.1), and item 43's "a later data kit's work".
- **Prior work:** PR 12 (5bb1418c). The EF Core packages are already in the cache (B1856 fetch record), so no fetch is needed.
- **Left out:** database-level append-only enforcement and runs against real PostgreSQL or SQL Server. Both are CI changes that need a service container and a decision.

### Lane E: the OXPd 2 adapter README's named limits (owed item 45 (1) to (6)), docs only. WP1.2 part
- **Scope (item 45):** "Named limits, to state in the README (today only the timing one is there)", items (1) to (6).
- **Changes:** `src/Datasec.Suite.Adapters.Oxpd2/README.md` only.
- **Must NOT touch:** any `.cs` file, `Generated/` and `contracts/oxpd2/`.
- **Review tier:** G2 (docs).
- **Size:** XS.
- **Authorised by:** item 45's "README sentences ... none blocks the landed adapter".
- **Prior work:** PRs 13 and 14.
- **Optional extension:** add item 46's README lines here, the same file.

## 3. Partition table (each lane's paths against every other)
`partition.py` resolved every path against the main tree: no path is missing and neither new folder exists. It then checked every pair of {X27, A1, U, T, C, S, D, E}: **28 pairs, 0 overlaps.** The positive control lane `tests/Datasec.Suite.Sessions.Tests/` did show its overlap with X27 (1 pair, 2 files).

| | A1 | U | T | C | S | D | E |
|---|---|---|---|---|---|---|---|
| X27 | none | none | none | none | none | none | none |
| A1 | | none | none | none | none | none | none |
| U | | | none | none | none (*) | none | none |
| T | | | | none | none | none | none |
| C | | | | | none | none | none |
| S | | | | | | none (*) | none |
| D | | | | | | | none |

(*) A build dependency, not a shared file: U and D compile against the Secrets library. They stay parallel only while S changes no public member.

**Shared project files, one owner each:**
| File | Owner tonight |
|---|---|
| `Datasec.Suite.slnx` | **A1** only. A2 merges main after A1 lands. |
| `Directory.Packages.props` | **no lane**. A package need means a supervised fetch (C-61), so the lane STOPs. |
| `Directory.Build.props`, `NuGet.config`, `global.json` | **no lane** |
| `.github/workflows/ci.yml` | **no lane**. It is whole-file fingerprinted and needs a person's read for any edit. |
| `README.md` (root) | **no lane** |
| `packages.lock.json` files | Each lane may touch only the lock files of projects it creates (A1, A2). U, T, S, D and E change no lock file. |
| `src/Datasec.Suite.Server/*` | **no lane**. Host wiring is excluded. |

## 4. Owed items 1 to 58 that are agent-actionable now as small lanes
| Item | Lane | Files | Size |
|---|---|---|---|
| 7 Dockerfile digest pin | C | `packaging/linux/Dockerfile` | XS |
| 47 W02 cell | T | `tests/Datasec.Suite.Jobs.Tests/ReceiverTests.cs` | XS |
| 48 K8 cell | T | `tests/Datasec.Suite.Contracts.Tests/TolerantReadingTests.cs` | XS |
| 51 / OXPD2-25 R6 two shapes | C | `build/repo_rules.py`, `build/tests/test_repo_rules.py` | S |
| 52 (B1904 F1) delete under the attach lock | U | `Registration/RegistrationKeys.cs` and cell | S |
| 53 (B1904 F2) issuer off the caller's path | U | `Registration/CloudDeviceTokenHolder.cs` and cell | S |
| 54 (incl. B1905 F2) missing cells and the disposed-token check | U | `tests/.../Registration/*`, `CloudDeviceTokenHolder.cs` | S |
| 55(1) (B1905 F1) s+n: named limit or modulus rule | U | `Registration/` and README | XS to S |
| 42(2) removal guard | S | `src/Datasec.Suite.Secrets/` | S |
| 34 N7 (and N2, N3, N5) | S | `src/Datasec.Suite.Secrets/`, tests | S |
| 43 (1) and (2) | D | `src/Datasec.Suite.Data/`, tests | S |
| 45 (1) to (6), 46 README lines | E | `src/Datasec.Suite.Adapters.Oxpd2/README.md` | XS |
| 37 wire the broker to `ListAll` and `DeleteUnreadable` | **WAITS on X27** (the Sessions test project), then a small G1 lane | `src/Datasec.Suite.Sessions/SecretStoreSessionRecordStore.cs` and a new cell file | S |
| 58 F13 test race | X27 (live, committed 20:09) | | |

**Records-only items, for a records seat and not a build lane:** 33 to 36, 38 to 41, 44, 46 (records half), 49, 50, 56, 57, plus the move or comment of OXPD2-20 to OXPD2-24 after PR 16. These are runbook lines, ticket moves and master-list comments, so they need a coordinator-approved body.

## 5. EXCLUDED, with the reason
- **Needs hardware, a device or the simulator:**
  - WP0.1 (lab) and WP0.2 (spikes; S4 is the printer test, C-68: "Nothing touches the printer before his word on what to run").
  - The rest of WP1.2 (sign-in, USB and notifications on a device; C-63 revisits after Monday's printer test).
  - WP1.6 panel front end, WP1.9 bundle v0 (needs HP's SPU, item 1), WP2.1 to WP2.4 (OXPd 1.x; C# choice "firm after spike S2").
  - The remaining E-tests of WP4.2 to WP4.4 (polling, Direct delivery and 1 GB jobs on a device: OXPD2-18).
  - Items 5, 6 and 8 (docker or Windows on this machine, a person's launch), item 10 (network capture) and item 30.
- **Needs Azure, a tenant or a service:**
  - The rest of WP4.1 (item 57: the real issuer, the app registration, the service's acceptance).
  - WP0.7's other half, WP0.8's tenant export, WP3.2 (customer Function App release), WP5.4 (production licence service).
  - Item 55 (2) to (6).
  - Database runs against real servers (part of item 43/44).
- **Needs a ruling, the product owner or new words for a person:**
  - **WP3.12 localisation.** CLAUDE.md line 86 calls copying Workpath strings "an OPEN point for the brief of that package to settle before any string is copied". P-9 (`05:204`) is "English for Phase 1 (A18)", and OP-21 stays open. A framework-only lane (an English catalogue plus the coverage check, with no copied string) is possible only if the coordinator settles that point in a brief.
  - The paper packages that are drafted and waiting on him: WP0.5 (`HP_QUESTIONS_DRAFT.md`, OXPD2-10 comment "[HP-DRAFT-DONE-20NOV]"; sending is his), WP0.6 (done, report A11; the rest needs a Workpath printer, `05:263`), WP6.7 (`Registers/DEVIATION-REGISTER_DRAFT.md`), WP0.8, WP0.10 (OP-1 to OP-6), WP0.9 (`K3`), and the WP3.5, WP3.6 and WP3.11 first reads (K1, K2, K4).
  - Item 2 (the dev-CA fingerprint: "a seat does not search the library").
  - Items 15, 24 and 25 (organisation or ruleset settings, CLAUDE.md text: the coordinator's).
  - Items 18, 26 and 28 (billing, the launcher text, an origin ref: the coordinator's).
  - Items 27 and 10 (ship `.pdb`/`web.config`? a different test framework? decisions).
  - Item 38 (questions not on OXPD2-1).
  - Items 34's six product points and 42(1) (who may call `DeleteUnreadable`).
  - Items 31 and 32 (design corrections, a pass of their own).
  - Item 13 (the SDK patch lookup: the coordinator places the toolchain).
- **Not in the twelve-row table, so the coordinator's call:** WP1.11 minimal admin API and host wiring (`src/Datasec.Suite.Server/`, migrate-at-start), WP3.1 QR gateway client, WP3.7, WP3.13 and WP4.6 attribute diff. The coordinator has precedent for widening (WP1.2 and WP1.7 parts landed as PRs 13 and 15), but none of these is in C-42's table, so this sweep proposes none of them. The host wiring would also become the single owner of `Program.cs` and the Server lock file.
- **Waits on another lane:** A2 waits on A1 (slnx). Item 37 waits on X27. Lane C's ci.yml follow-ups (items 21 and 22 remainder) wait on a person's fingerprint read.

## 6. PRIOR WORK on main, per lane (do not rebuild)
| Lane | What exists on main |
|---|---|
| A1 / A2 | Sessions and token broker (PR 9, `src/Datasec.Suite.Sessions/`), card decoders and assembler (PR 3), Graph layer (PR 10), secret store (PRs 5 and 11), device registry (PR 12). No C5 or C7 code. |
| U | PR 17 (`src/Datasec.Suite.UniversalPrint/Registration/`, 14 files; tests 9 files) and PR 4 (`Ipp/`). |
| T | PR 15 (Jobs, incl. the round-3 `A03` fix) and PR 14 (`TolerantReadingTests.cs`). |
| C | PR 1 (skeleton, Dockerfile), PR 8 (R5), PR 16 (R6 to R8, `squash_scan.py`, release mode). |
| S | PR 5 (store), PR 11 (`ListAll`, `DeleteUnreadable`, `ISecretStoreInventory`). |
| D | PR 12 (`src/Datasec.Suite.Data/`, `src/Datasec.Suite.Devices/`, both migration sets and snapshots). |
| E | PR 13 (adapter, README with the timing limit only) and PR 14. |

## 7. Machine notes
- **One heavy dotnet job at a time across all seats.** Every `dotnet restore/build/test/publish`, test-executable run and `loop.sh` run goes through each lane's `gate/heavy.py`. That script waits while load1 is 7 or more, then takes `mkdir .tools/wave1-heavy.lock.d` (B1912 kit line 165). The B1912 kit also says to "Allow 30 minutes of waits in all", and to never hold the lock while reading, editing or waiting on a hosted run.
- **Heavy jobs are short on this machine.** X27's logs show `Time Elapsed` of 1 to 5 s per build step and about 7.5 s per test assembly. Its whole red/green/mutant/publish chain ran from 20:03 to 20:08, and a 200-run loop took 38 s. The lock is held for seconds to a few minutes, and seats spend most of their time reading and editing.
- **Recommendation: 4 to 5 build seats at once** (for example U, A1, T, C and S/D), with their G1/G2 readers after them. More than about 6 would mostly queue on the lock and on the hosted runner's four jobs per push. Item 18 (billing of hosted minutes) is UNMEASURED.
- Each seat should test its own project with a filter (`--project` / a filter) before the one full-solution run. A full run includes `Datasec.Suite.Sessions.Tests`, which stays flaky on Linux until X27 lands (item 58).
- Load at 20:09: 3.86, under the runner's 7 threshold.
