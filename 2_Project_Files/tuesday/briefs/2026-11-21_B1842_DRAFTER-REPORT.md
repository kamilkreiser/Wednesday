STARTABLE: YES - kit B1842 (lane K, seat X24) is drafted for one documents-only seat; `stamp_check.py` exits 0 (86 claims, 86 measured); the one tool `doccheck.py` fired 9 of 9 planted faults and passed clean on a real-shaped prototype; S4 has to answer Q3 (whether the WP0.9 licence read may use the web) in words before launch.

# B1842 DRAFTER REPORT | lane K of wave 3: the seven documents

Drafted 2026-11-21, 17:08 to 17:22 AEDT (clock by `date`), by a read-only drafter (Opus) for Tuesday s304, under commission `2026-11-21_B1840-B1842_OXPD-WAVE3_DRAFTER_COMMISSION.md`.
Files: kit `2026-11-21_B1842_SEAT-X24_oxpd2-wave3-documents.md` (56326 bytes, 198 lines, sha256 `90878df7...633a`), its sidecar `.measured` (86 claim lines plus a header and a KIT line), this report. Scratch is at `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s304/d1842/`: `gate/doccheck.py`, the controls, the prototype, the gitleaks control.

## BLUF
1. **The kit's scope is the plan's lane K and nothing more.** It covers seven new files in `1_Project_Definition/`: D1 the WP6.7 register (`Registers/`), D2 the WP0.8 map (`Design/`), D3 the WP3.6 first read, D4 the WP3.5 first read, D5 the WP0.9 licence read, D6 the WP3.11 first read (`Analysis/K1` to `K4`), and D7 the WP0.10 note (`Design/`). The seat drafts all seven in its lane folder and places them only after every check passes. No repository work, no heavy job, no lock.
2. **Acceptance is checked by a program, and the drafter ran it.** `doccheck.py` checks five things: every claim line has a citation that resolves to a real line (or the line says UNMEASURED or QUESTION); every cited file is pinned by sha256; key paths are refused without being opened; no ban-list names appear; every decision word cites `CL`, `03` or `B1817`. Its `--excerpts` output, each citation with the line it cites, is what the G2 review reads, because no program can tell whether a line actually supports its claim (REQUIRED SECTION N1).
3. **Correction to the plan, MEASURED:** OQ-6 is at `03:378`, not `03:375`; line 375 is OQ-3. The kit follows the measurement.
4. **Two facts the seat could not have known from the plan:**
   - No converter candidate is named anywhere in the project except the retired Gotenberg / LibreOffice service (`A2:218`, `03:344`). That is why Q3 exists.
   - The Workpath class `StatisticsJobData`, whose JSON form is the reporting record, has no source in the library (0 files define it; control: 4 files name it). Its field list is UNMEASURED unless the bounded places Q5 names hold it.

## Facts re-measured (instrument, control)
- **Origin main:** `5e36d8dca42966395ea3dd014c7f788409eb585f` (`gh api -X GET` at 17:10:21). 0 open PRs, 8 branches, 0 named b1842. Equal to the commission's main.
- **Design documents** (`wc -l`, `shasum -a 256`): `02` 1276 lines, `03` 667, `05` 304, `CL` 370 lines / 33300 bytes, last entry C-54. Hashes are in kit FACT 2.
- **Absence of the seven documents:** the `find` census in kit BLUF 3. Every pattern returned 0, and three controls fired.
- **Sources each document rests on,** read by `awk`, `grep -n` and `python3 -I`:
  - The template's 17 and 3 columns (`main.bicep:374-428`), the rule's `TimeGenerated = now()` (`:457`, `:463`), and `deviceInfo` typed `dynamic` (`:401`).
  - The jobStatistics target: `statisticsData` has 16 properties; 14 names overlap the template.
  - `ReportingClient.kt:66-90`.
  - `isSIOEnabled`: 16 hits in 5 Teams files and 5 in MailFlow; the definition is in `WorkpathAccessService.java` (2 hits).
  - `SendFragment.kt:603-606`.
  - The common library: scan options 20 files / 4892 lines, print options 17 / 3479, pdf 4 / 256; `PrintViewItems.java:83`.
  - The Manager: 266 `.cs` files / 28176 lines, 29 `.xaml`, Engine 3 files / 1411 lines, README 30 lines, test catalogue 3593 lines.
  - `03` rows 145, 146, 147, 182, 183, 188, 224, 374, 378, 395-400, 434, 450, 654.
  - CL headings C-7 through C-45.
- **Jira** (GET, in-process helper; key names only, no value printed): `OXPD2-19` and `OXPD2-11` are both in Backlog with 0 comments.
- **Key-path pruning:** prunes over the Manager, the Utility, Teams and the common library found 0 key paths each. The `doccheck.py` control proves the SDK's `tools/certificates/...key` is refused without being opened.
- **Tools:** gitleaks 8.30.1. The planted token gave rc 1; the prototype gave rc 0 under both its name and a neutral name.
- **Machine:** load 2.66, 1003 GiB free, 0 panes named `oxpd2-x24` (control: 1 `oxpd2` pane).

## D-decisions (coordinator defaults in the kit; each one is also a Q)
- D-1: One seat, documents in the order D1 to D7, READY at Step 0 + 240 minutes, with a context band and HANDOVER.
- D-2: Citations are machine-checkable: `ALIAS:N` for 02/03/05/CL and the report and review ids, `ROOT:path:N` for PD/SRC/LIB, plus a sha256 pin for every cited file.
- D-3: First-read findings must cite the source line (LIB or SRC), never only a report (N4, counted by program).
- D-4: Drafts live in `<lane>/drafts`. They are placed with `cp -n` only after `DOCCHECK: clean (7 files)`, gitleaks and the N4/N5 checks. A manifest and an excerpts file go to `Briefs/`. Placement is proved with `find -newer` and a before-list of sha256 hashes.

## Q-questions for Tuesday (each with its default)
| Q | Topic | Default |
|---|---|---|
| Q1 | Paths | `Registers/DEVIATION-REGISTER_DRAFT.md`, `Design/WP0.8_..._DRAFT.md`, `Design/WP0.10_..._DRAFT.md`, `Analysis/K1..K4_*` |
| Q2 | Seats | One seat |
| **Q3 (STOP-CLASS, S4 in words)** | WP0.9 web read | **No web read:** D5 is a constraints and licence checklist, with every candidate's terms UNMEASURED and the candidate list marked as owed. Alternative A: Tuesday names the candidates and one public licence page each. Alternative B: drop D5 |
| Q4 | Register statuses | A closed list, never APPROVED |
| Q5 | WP0.8 bounds | OXPd 2 vs the template. The Workpath side from `ReportingClient`, `StatsRepository` and A1 §4.18 only. OXPd 1.x from C1, else UNMEASURED |
| Q6 | WP0.10 bounds | A bounded Manager read; build check not done; the contract part is a proposal for lane H to reconcile; OP-1 to OP-6 as QUESTION lines (answers cited at 03:397/399/400); OQ-2 vs C-24 stated, not resolved |
| Q7 | First reads | Source only, no binaries |
| Q8 | Library copy | The in-project copy, not the NAS (`<project>/CLAUDE.md:38` still names the NAS); the common library from SRC master-2, with the LIB copy compared by `cmp` |
| Q9 | Jira | Two GETs, no write |
| Q10 | Pane / level / gate | Pane `Datasec/OXPd2-X24`, opus, G2 |
| Q11 | Records | No records written |
| Q12 | Acceptance | `doccheck.py` plus the excerpts file |

## UNMEASURED / NEVER RUN
- Nobody has run this lane, so these are NEVER RUN on a real output: the placement proof, `DOCCHECK` over seven documents, and the N4/N5/language checks.
- `doccheck.py` has run only on its own controls and on one prototype.
- Not established: whether the Workpath SDK class field list exists anywhere in the library; the shape inside each dynamic column; any printer, tenant or binary evidence.
- The size of each document and whether all seven fit one window: UNMEASURED. The band and HANDOVER cover that case.

## What I did not read
- The B1831 kit beyond its section outline and its NOT DECIDED and Stamp sections. It is a G1 code form; lane K borrows only the frame.
- The B1829 STATUS beyond DEVIATIONS.
- `02`, `03` and `05` beyond the rows named above; the analysis reports beyond the named lines.
- The Manager, Teams, MailFlow and common-library source beyond censuses and the cited lines.
- `OXPD2-1`; the B1816 kit; the NAS library. Nothing of HPSM-POC was opened.

## Reading load (summed by program)
- Seat boot load: the kit (56326 bytes) plus 54464 bytes (project CLAUDE.md 10052, CLARIFICATIONS 33300, `doccheck.py` 11112): **110790 bytes, about 28K tokens.**
- The drafter's own reads: the commission, the plan (~30K), the B1832 commission, DRAFTER_RULES, the wave-1 and wave-2 commissions, the B1829 kit whole (97647 bytes), project CLAUDE.md, and B1831's outline; about 190K bytes in all, not counting program outputs.

## Outside the fences
None. I wrote only the kit, its sidecar, this report and scratch under `d1842/`. No git, Jira or GitHub write; Jira was read twice; `gh api` was called with `-X GET` only. No build, test, Azure call or message. No key folder was opened, listed or hashed (a single `-prune -print` counted 0 key paths per tree). No secret was printed. `.env` was read in-process for key names and the Jira login only.
