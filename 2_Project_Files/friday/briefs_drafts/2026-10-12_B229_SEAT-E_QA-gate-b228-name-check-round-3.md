From Friday (laptop seat), Datasec / HPSM-POC. Replies go to friday-laptop-agent@agentmail.to.

# BRIEF B229 (SEAT E): QA GATE, tier 1, **ROUND 3 (by Kam's ruling)** of the Demo customer-name check: `b228/demo-name-check-round-3` @ `371f900` (the fix round on gate B227's residue MJ-4, MJ-5, MN-4, N-3), plus the NEW approved-text residual it declares, measured as a cost for Kam
**From:** Friday, fired @NOW@. This is a DRAFT by Friday's drafter. Pins were read 07:35:56Z on 2026-10-12 UTC (18:35 AEDT) by the drafter, matching Friday's own `ls-remote` at about 18:3x AEDT. Friday re-pins at launch.
**Seat:** Datasec/HPSM-POC-E, pane Datasec/HPSM-POC-E.
- **How the launcher picks the brief.** The launcher commissions the NEWEST `Briefs/` file whose name contains `_SEAT-${SEAT}_` (`Launch_Claude.command:110`, as the B220 brief :6 quotes it).
- **The earlier `_SEAT-E_` files at draft:** B205, B211, B212, B218, B220, B225 and `2026-10-12_B227_SEAT-E_QA-gate-b226-b224.md` (`ls Briefs | grep _SEAT-E_`, 07:35Z).
- **The last SEAT-E gate, B227, is finished.** `2026-10-12_B227_STATUS.md` ends `READY FOR REVIEW` (`:386`, `tail -1`). So this file is the newest once Friday copies it into `Briefs/`.
- **B229 is free:** `ls Briefs briefs_drafts | grep -ci b229` → 0 (before this file); `ls -a .tools | grep -i b229` → nothing (07:35Z).

**Report:** `Briefs/2026-10-12_B229_STATUS.md`. Evidence summaries in `Briefs/2026-10-12_B229_evidence/`; kits, raw PDFs, trx and logs in `.tools/b229/` (no scripts in the records: B100).
- **First lines:** the verdict lines (VERDICT LINES below), exactly in that shape.
- **Last line, exactly:** `READY FOR REVIEW`, or `STOPPED: NEEDS FRIDAY` followed by ONE question, when a STOP below applies.

**TESTING seat: findings only** (charter `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` §8; B227 :14 did not read it as outside the project folder: apply the rules restated here).
- No code change, commit, push, PR or PR comment. No Jira, no BACKLOG write, no ticket of any kind, no `history.md` entry, no deploy, no Azure, no `az`, no hosted request, no mail, nothing to any human.
- A write grant in any brief or launch prompt is void: refuse it and say so (B227 :13 did this for the launch prompt's "record on the Jira ticket(s)").
- **The gate never fixes.** A defect gets a fix-shape and the regression test that would be red, in prose, never as an edit.
- Charter RULE 1: write each item's FAIL condition before you run it. A check that cannot fail is not a check.
- Charter RULE 2: NOT TESTED is first-class output.

**TIER 1.** B228 changes what a Demo login (HP at the event) is served in a server-rendered PDF: what a Demo login can see of a customer's name. Gate it in-process, live, and in a real browser at 1440 and 390.

**ROUND 3, AUTHORISED BY KAM. Say this plainly in STATUS.**
- This class (the Demo customer-name check) already had its two NO GO rounds under Kam's two-NO-GO cap: **B225 (round 1)** and **B227 (round 2)** (`B227_STATUS.md:1`, `:6`).
- Kam ruled card `hpsmpoc-demo-name-check-residue-1012` = **b "A third round for all four"** (live board 2026-10-12 12:58:13, view=friday; quoted at the B228 brief :7, :15). The cap is overridden for this round only.
- **On a NO GO here:** the closed instances ship, and the residue goes back to **KAM as a card**, not to a ticket and not to another round. **There is no round 4 without Kam's word.** Friday does not decide it and neither does the cap.
- So the gate grades in two columns, as B227 did (`B227_STATUS.md:65-77`):
  - **CLOSED:** each of MJ-4, MJ-5, MN-4, N-3 that is now closed, with the measurement that shows it;
  - **RESIDUE:** what is still open, each line with its exposure in plain words, for Friday to put on Kam's card.
- A NO GO must still say which closed instances are safe to ship on their own. Every product change in B228 is inside ONE file (`ReportingEndpoints.cs`, +162/−49), so "ship the closed instances" means merging `371f900` whole (or `6efc2c3`..`9274786` without the two host-move test commits: Friday's choice, B228 STATUS :91, :123). **Say whether anything in it is WORSE than `caa5a97`** (the approved-text refusals of item 3, and any timing or CI cost) and so argues against shipping it whole.

**SHAPE:** copy gate B227 (`Briefs/2026-10-12_B227_SEAT-E_QA-gate-b226-b224.md`) and how `Briefs/2026-10-12_B227_STATUS.md` reported round 2 (one subject this time). The sections are: verdict lines · BLUF · CLOSED / RESIDUE table · Findings · Premise checks · Gate items (PASS / FAIL each, item 3 MEASURED) · Mutants table · KNOWN · NOT TESTED · NOTES FOR FRIDAY (hosted) · HOW · Housekeeping · Fixed / Deferred / Open · last line.
- Write your own new kits in `.tools/b229/`.
- **Two kinds of instrument, kept apart:**
  - **B227's kit, re-used ON PURPOSE for the close-check only** (item 1: "B227's ORIGINAL FAIL conditions and instruments"). B227 is this seat's own finished gate. Copy what you run (`.tools/b227/kit/ana227.py`, `cases227.py`, the probe `.tools/b227/probe/B227ProbeTests.cs`) into `.tools/b229/b227copy/` and run the copies, sha256 of each copy = its original. Never edit or run the files in `.tools/b227/`.
  - **Your own independent reader, probe and expected values** wherever B228 built its own (item 1 (c), items 2–8). **Never reuse B228's kit, probe, reader or numbers** (`.tools/b228/`: `ana228.py`, `B228ProbeTests.cs`). Read `Briefs/2026-10-12_B228_evidence/` as data only and re-derive every number.

**Premise key:**
- `(ls-remote 07:35:56Z)` = read by the drafter with that verb at that time (UTC, 2026-10-12).
- `(git <verb>)` = a read verb on `2_Project_Files`' object store, with `--no-optional-locks`.
- `(read: file:line)` = quoted from that file at `371f900` unless the line says otherwise.
- **UNMEASURED** = the drafter did not establish it; the line says what closes it.

Re-check every premise. A wrong one is a finding. A moved pin is a STOP unless a rule below covers it.

## AUTHORITY (verbatim, as the B228 brief relays them; re-read there, :14-18)
- **Kam's ruling:** `hpsmpoc-demo-name-check-residue-1012` = **b "A third round for all four"** (12:58:13). "All four" = MJ-4, MJ-5, MN-4, N-3.
- **Standing ruling C-89** (`hpsmpoc-customer-names-alias-1011`): **(a) "Keep names; alias wherever data leaves the partner"**: *"ORG-nnnnn on anything HP or an export sees."* B228 found C-89 not in `1_Project_Definition/CLARIFICATIONS.md` (`grep -n "C-89"` → 0 lines; cited from the B226 brief `:20`: B228 STATUS :108). Re-run the grep; cite whichever holds.
- **The design constraint:** Demo side only, FAIL CLOSED, never change what partners can write (B228 brief :17). No change to `NarrativeReview.cs`, generate, or any partner path.
- **Gate 1 and the 409 unchanged:** byte-identity to the stored report, the 409's title, detail and field error, the four audit reasons (B228 brief :18; at the tip the 409 is `ReportingEndpoints.cs:492-494`, read by the drafter; B228 STATUS :75 says `:489-494`).
- **The oracle per item** is B227's verbatim finding text, its FAIL conditions, its matrix and its regression test (`B227_STATUS.md:90-139`, `:88`; the B228 brief's THE FOUR table :20-31 quotes them).
- **LEFT, not ruled into round 3 (record in NOT TESTED with the B227 line; do not grade as B228 defects):** N-6 (`:140-144`), N-7 (`:145-149`), N-8 the 409's words (`:150-153`, Kam's NEW WORDS), N-11 (`:162-165`), N-12/N-13 records, MN-3 / F-3 (Kam's). The exception B228 used (N-9, N-10 rows added because the code they guard was touched: B228 brief :33) is in scope for you to verify.

## TARGETS (re-read with `git ls-remote origin` in `/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC/2_Project_Files` at the start, mid-gate and before the verdict; name the instrument and time on each)
| What | Value | Instrument |
|---|---|---|
| **Head:** `b228/demo-name-check-round-3` | `371f9005e7528e06c8fc0d7a371706de540bbfad`, tree `728c8b3366dbdc2a500fe998a4075d440991ab43` | ls-remote 07:35:56Z (= B228 STATUS :128, its last line); git rev-parse `^{tree}` |
| Commits (6 on `caa5a97`, linear) | `6efc2c3` the matcher + `B228NameMatchingTests` · `29246aa` row "ANZBank" · `c4a6bbb` N-10 multiset row · `9274786` lunate row on "Cafe" · `67322f8` B228 class on one host per class · `371f900` B226 class on one host per class | git log --format='%H %P %s' `caa5a97..371f900`; rev-list --count = 6 |
| Files vs main (3, +481 / −61) | `Endpoints/ReportingEndpoints.cs` +162/−49 · `B226NameMatchingTests.cs` +15/−12 · `B228NameMatchingTests.cs` +304 (new) | git diff --numstat `caa5a97 371f900` |
| Unchanged vs main | `web/`, `.github/`, `HpsmPoc.Modules.Reporting/`, `AssessmentEndpoints.cs`, `B223SeededCustomersOpenByAliasTests.cs` | `git diff --quiet caa5a97 371f900 -- <those>` rc 0 (07:38Z); 0 added `process.env` / `Configuration[` / `GetValue<` lines in `api/src` |
| **main** | `caa5a9713d4e5257d68d2a91ee1d331e3a1fc5d9`, tree `e57d6c991b610f66da154d15fb58ec985c9b5a29` (= B227's combined tree, `B227_STATUS.md:5`) | ls-remote 07:35:56Z; git rev-parse; `merge-base caa5a97 371f900` = `caa5a97` |
| Round 2's subject and round 1's | `bef5f7e` (B226, = PR 143 head), `2f51c36` (B223) | ls-remote 07:35:56Z |
| Objects present | `caa5a97`, `371f900` → `commit` | git cat-file -t |
| PRs | none for `371f900`. Highest `refs/pull/144/head` = `ddd693d` (B224); `143` = `bef5f7e` | ls-remote `refs/pull/14*` 07:35:56Z |
| `ReportingEndpoints.cs` at the tip | 1,164 lines (1,051 at `caa5a97`, B228 STATUS :105) | git show `371f900:<path> \| wc -l` |
| `.tools/.git-lock` | absent (only `.git-lock-last-owner-{A,B60,B61,C}`) | `ls -a .tools` 07:35Z |

**The drafter's merge tree: UNMEASURED.** The drafter's guard refused `merge-tree` even in a scratch clone. Prediction: `merge-base` = `caa5a97`, so `merge-tree --write-tree caa5a97 371f900` = `728c8b33…` (the head's own tree), rc 0, a fast-forward. Item 9 closes it.

**Rules:**
- **The head moved** → STOP, and say to what.
- **Main moved** → read `git diff --name-only caa5a97 <new>`. STOP, and say which path, if any path overlaps B228's 3 files or falls under `api/src/HpsmPoc.Modules.Assessment/Endpoints/**`, `api/src/HpsmPoc.Modules.Reporting/**`, `api/src/HpsmPoc.Api/HostedDemo/**`, `web/src/components/customer/**`, `web/src/server/**`, `web/e2e/**`, `.github/workflows/**` or `api/tests/HpsmPoc.Api.Tests/{Assessment/B2*,Support/**}`. Otherwise re-derive the merge tree against the new main, build and test that tree once (item 9).
- **A conflict** → STOP, and say where.

## VERDICT LINES (the first lines of STATUS, in this order)
```
B228 371f900: GO | GO WITH NOTES | NO GO
  MJ-4 (case + lookalike): CLOSED | RESIDUE            (rows refused / run, B227 kit and own reader)
  MJ-5 (no-decomposition letters): CLOSED | RESIDUE
  MN-4 (short name glued): CLOSED | RESIDUE
  N-3 (approved text naming the customer): CLOSED | RESIDUE
  adjacent forms (item 2): PASS | FAIL                 (n rows, n served with a readable name)
  approved-text residual (item 3): MEASURED            (n names / n reports refused; a cost for Kam, not pass/fail)
  must-open + seeded + "(sample)" aliases (item 4): PASS | FAIL
  no-Demo reads (item 5): PASS | FAIL
  suites + CI projection (item 6): PASS | FAIL         (n/n; projected s against 900)
  mutants (item 7): PASS | FAIL                        (killed / run, survivors)
  Demo copy timing (item 8): RECORDED                  (cold / warm medians vs caa5a97, load1)
MERGE caa5a97+371f900: GO | GO WITH NOTES | NO GO | STOP   (tree, rc; fast-forward or not)
Round 3 (Kam's ruling, card hpsmpoc-demo-name-check-residue-1012 = b, 12:58:13). On NO GO: closed instances ship, residue to Kam as a card; no round 4 without his word.
overall: GO | GO WITH NOTES | NO GO
```

## GIT DISCIPLINE
- **In `2_Project_Files` itself, READ verbs only:** `ls-remote`, `log`, `show`, `diff`, `cat-file`, `ls-tree`, `rev-parse`, `rev-list`, `merge-base`, `grep`, and `git --no-optional-locks status`, always with `--no-optional-locks`. No fetch, checkout, switch, branch, merge-tree, commit-tree, worktree add/prune or gc there.
- **Everything else goes in a `git clone --shared`** (or a bare `--shared` clone) under `.tools/b229/`: `merge-tree --write-tree`, any fetch of a moved main, worktree adds.
- **Your detached trees** are made under `.tools/b229/lock.sh`, a byte copy of `.tools/b227/lock.sh` (sha256 `d9366256…` = `.tools/b225/lock.sh`, drafter's `shasum` 07:3xZ), on the shared `.tools/.git-lock`. Never remove another seat's lock.
  - `.tools/wt-B229-head` (`371f900`)
  - `.tools/wt-B229-base` (`caa5a97`: round 2's merged tree, the "before" for every B227 finding)
  - `.tools/wt-B229-r1` (`2f51c36`: only for the MJ-4 regression record column)
  - `.tools/wt-B229-pre` (`9274786`: the last host-per-row tip, for item 6's row/assert count and timing)
  - `.tools/wt-B229-mut` (`371f900`, mutants)
- **Do not use or touch:** `.tools/wt-b228*` and `.tools/b228/` (Seat A's; read its files as data only); `.tools/wt-B227-*` and `.tools/b227/` (beyond copying, item 1); `.tools/b225/`, `.tools/b226/`; any other seat's tree, kit or container.
- Every SHA you write is one you read, with its instrument inline.

## PARTITION / PORTS: 6981–6990, yours only (B227's range, re-used by the same seat)
- **The drafter's check, 07:3xZ:** `lsof -nP -iTCP:6960-6999` → 0 lines. `docker ps -a`: `b228-azurite` Exited (0) about 07:25Z; `b227-azurite`, `b227-mssql`, `b226-azurite`, `b225-azurite`, `b224-*`, `b223-azurite`, `b220-azurite` all Exited. No 69xx binding is up.
- **Why 6981–6990:** B227's range (`B227_STATUS.md:15`), this seat's own finished gate; its housekeeping reads `lsof -iTCP:6981-6990 -sTCP:LISTEN` = 0 lines (`:366`). B228 used 6960–6969 (B228 STATUS :80, :114).
- **Never yours:** 6960–6969 (B228), 6970–6979 (B224), 6950–6959 (B220), 6980, 6991–6999, and every other seat's.
- **Plan:**

  | Port | Use |
  |---|---|
  | 6981 | head web, proxy mode (showcase shape) → 6983 |
  | 6982 | base web (`caa5a97`), proxy → 6984, only when a no-Demo DOM check needs it |
  | 6983 | API at `371f900`, Development sign-in, one role set per arm, restarted per arm, `Showcase__Enabled=true` as `scripts/showcase.sh` sets it |
  | 6984 | API at `caa5a97` (and at `2f51c36` for the one MJ-4 record column, one at a time) |
  | 6985 | `b229-mssql`: new, CI digest `mcr.microsoft.com/mssql/server:2025-CU9-ubuntu-24.04@sha256:2b5b5816…d726` (read: `.github/workflows/ci.yml` `MSSQL_IMAGE`, job `api-sqlserver-shard`, at `371f900`); sa password in `4_Credentials/b229-sql.env`, mode 600, value quoted, read by name only. Drop its test databases between series (only databases older than 10 min with no session: B227 HOW :355's slip) |
  | 6986 / 6987 | hosted standalone + Entra stub (`E2E_HOSTED_PORT` / `E2E_STUB_PORT`) |
  | 6988 | `b229-azurite`: new, CI digest `mcr.microsoft.com/azure-storage/azurite:3.37.0@sha256:830430c1…71fd5` (read: `ci.yml:43` at `371f900`), a NEW random key in `4_Credentials/b229-azurite.env`, mode 600, value quoted, read by name only. **Never start `b228-azurite`, `b227-*` or `b225-azurite`** |
  | 6989 | mutant web / Playwright's own web |
  | 6990 | merged-tree API, only if main moved (item 9) |

  Both new containers are stopped, not removed, at the end.
- **Re-check with `lsof` before every bind.** Log each in `.tools/b229/run/lsof-checks.txt` and in STATUS. If any of 6981–6990 is taken at launch: STOP and say by what.
- **Never open `4_Credentials/.env`.** Your own `b229-*.env` files are written by your kit and read by name only; print env files by shape only.

## BUILDER'S CLAIMS (read whole first; trust no count in them)
- Brief `Briefs/2026-10-12_B228_SEAT-A_demo-name-check-round-3.md` (122 lines).
- STATUS `Briefs/2026-10-12_B228_STATUS.md` (128 lines): BLUF 1–9, FOUND 1–4 (incl. the N-3 variant table :30-37), MATRIX (:51-61), TESTED (:63-72), HOW (:74-81), THE CI TIMEOUT (:83-91), NOT TESTED, PRIOR WORK, NEW WORDS, Open 1–5 (:121-126).
- Evidence `Briefs/2026-10-12_B228_evidence/` (`matrix.tsv` 457 rows, `found.tsv`, `n3-variants.txt`, `lookalike-and-spellings.txt`, `mutants.tsv`, `red-first-{base,tip}.txt`, `seeded.txt`, `no-demo-reads.tsv`, `code-checks.txt`, `suites.txt`, `timing.txt`, `pins.txt`, `lsof.txt`).
- The gate it answers: `Briefs/2026-10-12_B227_STATUS.md` (386 lines; findings :90-139; RESIDUE :77; mutants :267-293; Open :377-384). Its evidence `Briefs/2026-10-12_B227_evidence/` (`matrix-remade.tsv` 127 rows, `adversarial.tsv` 98 rows, `mutants-subject1.tsv`, `timing.tsv`, `no-demo-and-seeded.txt`, `shots/`).

### The drafter's reading of B228 STATUS (each is for the gate to confirm or refute; none is a finding until measured)
1. **"Every row is pinned by a test" (:59) vs the matrix's own pin column.** In `evidence/matrix.tsv`, column "test that pins it", the 108 (a) rows split 59 `B226NameMatchingTests` · 41 `B228NameMatchingTests` · **8 "-" (no test)** (drafter's `awk` on column 12). And the class holds 45 must-refuse theory rows (:10), not 49. Name the 8 unpinned must-refuse rows, and say whether each is pinned anywhere else (B223 tests, a unit fact) or not at all. An unpinned must-refuse row that only the probe guards is a Note at least (N-9/N-10's class).
2. **Must-open: 89 in the matrix (:15, :55) = 54 + 35 pinned by `B228NameMatchingTests`, but the class has 37 must-open rows (:10).** Kam's count of the new must-open rows is 30 (:15 "30 must-open customers with all three narratives approved"). Reconcile 30 / 35 / 37.
3. **The residual (c) "13 → 17 → 75 of 158" (:15, :56) does not sum from FOUND 4 (:43-48):** 15 (approved common-word) + 37 (template words) + 3 (extra names) = 55 new, against 75 − 17 = 58 more; and 16 + 16 + 47 + 14 = 93 rows, not 158. The drafter's tally of `matrix.tsv` (c) by kind gives 71 + 37 + 10 + 9 "all three approved as generated" rows (127), 15 + 1 + 2 "approved", 5 + 1 "edit", 6 "none (summary approved as generated)", 1 "edit+approved". Re-make the 158 and name every row's set.
4. **MN-4 "CLOSED for the host and case shapes" (:13) vs B227's MN-4 statement** ("a 2–4-letter single-word name glued into a longer token", `B227_STATUS.md:22`). B228 serves the same finding in lower case with no host shape ("anzbank runs…": 200, `n4-lower-glued`; :13, :100, :124; code comment `ReportingEndpoints.cs:678`). Grade whether MN-4 is CLOSED or CLOSED-with-residue by B227's own words, not B228's.
5. **MJ-5 adjacent served:** "Marsk" typed for "Mærsk" (`g1-ae2`, æ read as a) is a B227 row expected refused and still served (:57). B227's closed list maps æ→ae only (`:125`). Grade it by B227's severity guide (plausibly typed, no special character → Minor or more), not by the closed list.
6. **"No row, assert, skip, split or trim" (:18, :91) vs the diff.** The drafter's `git diff caa5a97 371f900 -- B226NameMatchingTests.cs` shows one assert CHANGED: the audit read `SingleAsync(e => e.Action == "report.demo-rendition")` became `… && e.TargetId == issued.Report`. On a fresh host the old assert also proved that the request wrote no OTHER `report.demo-rendition` audit row; on a shared host the new one cannot. Judge whether that is a weakening. Also the "Org" must-open row now "types its own alias" (:60, :91): read how it gets the alias (from the API, or a literal).
7. **Static counts the drafter took (re-take them by trx):** `B226NameMatchingTests` 113 `{ "…" }` rows and 14 `Assert.` lines at both `caa5a97` and `371f900`; `B228NameMatchingTests` 80 → 81 → 82 rows from `6efc2c3` to `c4a6bbb`, then 82 at `9274786`, `67322f8`, `371f900`, 19 `Assert.` lines throughout; 0 `Skip =` in either (`git show` + `grep -ci`). `IClassFixture` 0 → 1 in each.
8. **CI projection (:18, :83-91):** series D has a base median of 329 s against 293–382 in A–C: the base moved 30 % with load, so one series decides. 852 s is the WHOLE job (restore, build, Azurite, test; :96 says the step time is UNMEASURED), multiplied by a test-step ratio. And the tip is faster than base only because B226's class (on main already) was moved too, so the ratio also says main's own job would shrink. The SQL Server shard (`api-sqlserver-shard`, part `api-assessment`, `timeout-minutes: 20`, read: `ci.yml` at `371f900`) runs both moved classes too, on SQL Server, and B228 did not run it (:20, :71: SQLite + Azurite only).
9. **"The partner's way out: re-generate or rename" (:49).** For a template-provider narrative, re-generate writes the same deterministic sentences (`Providers.cs:66-101`), so re-generate may not be a way out at all. Measure it (item 3).
10. **"0 of the must-open set" (:16) vs the reader on open copies (:61):** four one-word report-word names ("Not", "Are", "Risks", "Section") open with a phrase form on the page, explained by a control "with fewer narratives". B228's reader is control-relative (:24): a copy NAMES only when a form occurs more often than in the same tree's unedited control. A control that itself prints the word hides it. Your own reader must not be control-relative only (item 1 (c)).
11. **Reader slips v1 → v3, disclosed (:25):** v1 one-sided by case (blind to the Cyrillic rows, B227's own v1 slip, `B227_STATUS.md:86`), v1 confusables before ASCII spellings (þ read as "p"), v2 ASCII letters through confusables ("l" → "i"). Item 1 (c) verifies v3 against controls from B227's kit, not from B228's.
12. **Timing is not comparable across gates (:19):** B228 measured live Kestrel + curl (warm 104 / 96 ms); B227 in-process (warm 478 / 538 / 348 ms, `B227_STATUS.md:51`). Name your instrument and compare only within it.
13. **Disclosed by B228, re-measure, do not re-grade:** the `metrics-dashboard.spec.ts:24` red under load (:71, :126); the two brief citation slips (:108, :125); B228 deletions (:115).

## THE GATE MUST, INDEPENDENTLY, AT `371f900`

### 1. Close-check MJ-4, MJ-5, MN-4, N-3 with B227's ORIGINAL FAIL conditions and instruments
**FAIL conditions (B227's, `B227_STATUS.md:88`, unchanged; write them into STATUS before the runs):**
- a must-refuse row 200 at the tip with a readable name form (by the reader or by a crop);
- a must-open row 409 at the tip;
- a must-open row 200 with a name form on the page;
- for B227's adversarial rows, its `expect` column.

**(a) B227's instruments, re-run (copies, item SHAPE):** B227's probe journey (`B227_STATUS.md:81`) and reader `ana227.py` v2 with its UNEDITED control per name (`:84`), over:
- B227's matrix as data (`evidence/matrix-remade.tsv`, 127 rows) and adversarial set (`evidence/adversarial.tsv`, 98 rows), at `371f900` and `caa5a97`;
- the rows that decide each finding: MJ-4 `:97-104` (5 rows + the same-case control), MJ-5 `:116-123` (6 rows + "İzmir"/"Izmir"), MN-4 `:130-133` (3 rows + "it@agl.com.au", "anz@x.com"), N-3 `:77` (b) (the 4 seam rows `g10-n3-seam1`, `-seam2`, `-seamword`, `-short`);
- B227's regression tests as written (`:111-113`, `:126`, `:139`): confirm each is in B228's classes verbatim (B228 STATUS :59 says so) by reading the rows.

**(b) B228's new rows:** its **49 new must-refuse rows** and **30 new must-open rows** (B228 STATUS :15, :59-60; `evidence/matrix.tsv` (a) and (b), re-made as data; reconcile 30 / 35 / 37 first, drafter's item 2). Run each on YOUR probe at `371f900`, `caa5a97` and (MJ-4 rows only) `2f51c36`.

**(c) Your own independent reader and expected values.** Your own reader (not `ana227.py`, not `ana228.py`): `pdftotext` default mode (`-raw` is blind, B225 :39) + a raw scan (Info dict, outlines, inflated streams, UTF-16BE), with BOTH:
- an absolute test (any F1 phrase / F2 joined form of the bare name on any page or in metadata = NAMES), and
- a control-relative test for single name words (more often than the same tree's unedited control).
Report both columns; where they differ, say which and why (drafter's item 10).
- **Your expected values** are written from B227's finding text and the severity guide, per row, BEFORE any run, in `.tools/b229/cases/expect.tsv`. Diff them against B228's `expected` column: every disagreement is listed.
- **Verify B228's reader v3 against a control drawn from B227's kit, not B228's:** run a COPY of `ana228.py` v3 (read-only, from `.tools/b229/b228copy/`, sha256 = original) over the PDFs B227's base control read NAMES on (B227's 30 `2f51c36` leaks `:33`, and its MJ-4/MJ-5/MN-4/N-3 rows at `bef5f7e`; regenerate the PDFs with B227's probe copy if `.tools/b227/` does not hold them). **FAIL (of B228's evidence, a Note at least):** v3 reads any of those as not naming. Also run it on B227's v1-blind case (a capital Cyrillic В, `:86`).
- **Base control first:** your reader must read NAMES on every MJ-4 / MJ-5 / MN-4 / N-3 row at `caa5a97` (each 200 there, B228 STATUS :26). Where it cannot (a □ case), use a PNG crop. If neither sees it, the row is blind: say so.

**Per finding, CLOSED or RESIDUE**, with the row ids that decide it, in B227's columns (`598a91a` is gone from this round; use `2f51c36` / `caa5a97` / `371f900`).
- **MJ-4:** CLOSED only if all 5 rows are 409 and the unit fact holds (for every key of `Lookalikes`, `Plain(upper) == Plain(lower)`, `B227_STATUS.md:113`) by your own run of the class AND by your own enumeration over `Lookalikes` + `OtherReading` (`ReportingEndpoints.cs:563`, `:578`).
- **MJ-5:** CLOSED only if all 6 rows + the reverse direction + þ/ð/ħ are 409, and "Mærsk (sample)" unedited is 200. Re-derive the closed list from the code (`NoDecomposition`, `:583`) against B227 `:125`.
- **MN-4:** CLOSED / CLOSED-WITH-RESIDUE per drafter's item 4. "Tanzania", "zapper", "innovation", "it@tanzania.gov", "ANZAC" stay 200.
- **N-3:** CLOSED only if all 4 seam rows + B228's 5 seam-per-form rows are 409 at the tip, 200 + NAMES at `caa5a97`. Read `NarrativeTextLeftOut` (`:549`, = ".") and its use (`:457`, `:474`): confirm through code that the selector does not skip a "." text (B228 STATUS :79 cites `NarrativeReview.cs:70-75`) and that the provenance lines of the compared model equal the copy's.

### 2. Adjacent forms the builder did not list (each FAIL condition first; diff your list against `matrix.tsv` and B227's `adversarial.tsv`: 0 overlap)
**Red-proof every row:** each row must be 200 + NAMES at `caa5a97` by your reader or a crop (else it proves nothing), or, where `caa5a97` already refused it, say so and keep it as a guard.
- **Other scripts** (B228 NOT TESTED :98): a Hebrew, Arabic, Devanagari, Thai and Hangul customer name typed exactly, in another normalisation (NFC vs NFD Hangul jamo), and with a Latin transliteration; Armenian / Cherokee lookalikes in a Latin name (B227 N-7's rows, re-graded only if B228 touched them).
- **Mixed separators:** "ANZ·bank", "ANZ–bank" (en dash), "anz‐bank" (U+2010), "Bettong Hollow", "Bettong Hollow", a TAB, "it@anz-bank.com.au", "it@my.anz.com.au", "it@myanz.com.au", "anz.bank" with no "@", "ANZ_bank", "ANZ2026", "2026ANZ", "@ANZ".
- **URL-encoded and web forms:** "Bettong%20Hollow", "bettong+hollow", "https://x.example/?q=Bettong+Hollow", "%41NZ", "xn--" punycode of a non-ASCII name ("Café Zürich"), an HTML entity ("Bettong&nbsp;Hollow", "&#65;NZ").
- **Zero-width and joiners:** U+200D ZWJ, U+200C ZWNJ, U+FEFF, U+180E, U+034F (CGJ, Mn), U+FE0F (variation selector), each inside a one-word and a two-word name, and between the two parts of a glued short name ("ANZ‍bank").
- **Fullwidth Latin:** "ＡＮＺｂａｎｋ", "ｉｔ＠ａｎｚｂａｎｋ．ｃｏｍ．ａｕ", "Ｍａｅｒｓｋ" for "Mærsk", fullwidth with mixed case ("ＡＮＺＢａｎｋ").
- **Homoglyph digits:** "0RA" for "ORA (sample)", "AN2" / "ANZ" with a mathematical or fullwidth digit, Arabic-Indic and Devanagari digits in a name with digits ("Bettong٢٠٢٦" for "Bettong2026"), "B3tt0ng" (N-7, LEFT: record only).
- **MJ-4 neighbours:** a name mixing Latin and Cyrillic letters in one word typed all-Latin; Greek with tonos in capitals ("ΑΚΡΌΠΟΛΗ"); a Greek final sigma typed in capitals mid-sentence; Cyrillic "Ё"/"Й" (which decompose) typed without marks.
- **MJ-5 neighbours:** "Marsk" (drafter's item 5), "KIRKLARELİ" typed with I, "GROẞ" vs "Gross", "ŁOMŻA" typed "lomza", ø typed as "oe" in a one-word name, ŋ and ĸ (outside the list, NOT TESTED at B228 :99: run them, a Note under the guide).
- **N-3 neighbours:** the name in an approved text of EACH narrative kind; split across two approved narratives; an approved text that is exactly "." (collides with `NarrativeTextLeftOut`); an approved text equal to the fallback's words; approved text holding the alias string ("ORG-nnnnn") beside the name.
- **Severity guide (B225's, unchanged):** a plausibly typed form that serves a readable name to Demo is at least Minor, and Major if it needs no special character; an exotic form is a Note; **a form B228 CLAIMS closed that serves the name is at least Major.**

### 3. The NEW residual (B228 BLUF 4, :16): one-word names that are ordinary words of approved text, refused on unedited reports. MEASURE it; grade it as a finding with its cost, not pass/fail
B228 says: 37 of the 47 words of the deterministic template's fixed text, used as one-word customer names, are refused to Demo at the tip and 0 at `caa5a97`; 15 of 16 common-word names with their ordinary sentence as APPROVED text are refused; 0 must-open and 0 seeded customers are hit. It fails closed (no leak). It is Kam's trade-off (B228 Open 1, :122).
- **Re-derive the 47 words yourself** from the code (the deterministic narrative `Providers.cs:66-101`, the provenance lines `NarrativeProvenance.cs:15-28`, the fallback `ReportModelBuilder.cs:99-117`, read at `371f900`): list the words, how you tokenised, and diff against `evidence/n3-variants.txt`'s `vocab` set. Explain any count other than 47.
- **For each word as a one-word name "<Word> (sample)", all three narratives approved as generated:** status at `caa5a97` and the tip, on the seeded report shape AND a fresh report. Then the shape:
  - **which names** (the full list refused, and the 10 not refused with why);
  - **which narrative kind and which string triggers it** (bisect by approving one kind at a time; through code, not by editing the product);
  - **which reports:** every report of that customer, or only some (does it depend on the score band / which sentences the template picks?);
  - two-word names made of template words ("Target State", "Priority Actions", "Material Risks": the last is B227's `g7-template-exact`).
- **Widen to plausible business names:** ≥ 50 one-word names a real partner's customer could have ("Apex", "Summit", "Pacific", "Core", "Vision", "Metro", "Unity", "Harbour", "Key", "Focus", "Insight", "Pulse", "Prime", "Target", "Priority", "Current"…). Count the intersection with the template vocabulary and the refusals. State the share.
- **What a Demo user sees:** in a real browser, showcase shape, service Partner+Demo, Demo sign-in, at 1440 and 390: the 409's words verbatim (title "This report changed after it was issued", the detail and the field error, `ReportingEndpoints.cs:492-494`), "Make a new copy" beside / below, and the new copy refused again. Screenshots captioned with the caller as the SERVICE saw it. **Say whether each sentence is true for this cause** (B228 NEW WORDS :111: "changed after it was issued" is false here too; N-8 is Kam's).
- **The partner's way out (drafter's item 9):** measure re-generate (same deterministic text: refused again?), re-approve, edit the narrative (which edit opens it), and rename. Say which actually opens the copy.
- **The AI-provider class** (B228 :16, "any one-word name that is an ordinary word the model writes"): NOT TESTED by HOLD (no live AI call). Give the reasoned exposure only, labelled UNMEASURED.
- **N2 (B228's measured alternative, :42):** cut 37 → 12 at the price of serving a short lower-case name in approved text. Re-measure the 4 N2 cost rows (`matrix.tsv` (e)) at the tip. Do not build N2.
- **Output for Friday's card (one table + one sentence):** names refused / names tried, reports affected, seeded affected (expect 0), what the Demo user reads, the way out, and the cost of the alternative. *"Today a customer named X is refused on every Demo copy because the approved template text uses X; the only way out is Y."*

### 4. Must-open: no ordinary report wrongly refused beyond item 3's class
- B227's 54 must-open rows (incl. "B223 Harbour City Council") and B228's 30/35/37 must-open rows: 200 by alias at the tip, 0 phrase forms of the name on any page, by your reader (both columns).
- **The seeded control:** `B223SeededCustomersOpenByAliasTests.Every_seeded_customers_report_opens_by_alias_for_Demo` green at the tip, file unchanged (`git diff --quiet` rc 0). Live on the showcase seed: every seeded customer and the partner-self record (read `ShowcaseSeeder` for the list), the seeded 17-page report plus a fresh report each with all three narratives approved, as Demo, Partner+Demo and Admin+Demo: all 200, 0 pages naming any seeded customer, and the stored copies DO name them (your reader is not blind).
- **The "(sample)" alias customers** (every fixture name with the "(sample)" suffix used in B227 / B228's must-open sets, and MN-2's 6 names): open by alias.
- **FAIL:** any must-open 409 at the tip that is not in item 3's class (one-word name = a word of approved text). Every refusal outside that class is a finding.
- B228's 110 "defaults" (unedited, all three approved): 6/110 refused at `caa5a97`, 9/110 at the tip (`n3-variants.txt`). Name the 3 new ones and confirm each is item 3's class.

### 5. No-Demo reads unchanged (Partner and other roles byte-equal vs base)
- One seed copy loaded into both trees (`371f900`, `caa5a97`). **PDF:** Partner, Admin and Consultant get the stored bytes, sha256 = the row's, same file name, `Content-Disposition`, `Digest` and `ETag`.
- **JSON:** `getAssessmentResult`, `getCustomer`, `listCustomers`, `listNarratives`, `listReports`: sha256 head = base for the three no-Demo arms (`traceId` removed and said).
- The report step's DOM for a Partner at 1440 (web unchanged, so equal by construction: show it once, B228 NOT TESTED :101 did not).
- **FAIL:** any difference.

### 6. Non-regression: suites, CI projection, and the host move
- **At `371f900` (once each):** API all 5 projects, SQLite + `b229-azurite`, 0 skipped, 0 not executed (B228: 2,886 = 2,788 + 98); vitest full `--maxWorkers=4` (1,661 / 172 files); typecheck, lint, build (9 warning lines, identical to `caa5a97`); contract-drift (7/7); Playwright desktop + tablet, the 7-spec set (48/48), `report-demo-refused-live-api.spec.ts` with `E2E_LIVE_API` (2/2), `E2E_TIMED=only` (2/2), the hosted project on 6986/6987 (6/6); gitleaks `--log-opts=caa5a97..371f900` (6 commits); a Python raw scan of the 162 added product lines (B228: 22 non-ASCII, all Latin letters in comments; 0 raw Cyrillic/Greek/invisible).
- **The SQL Server shard, which B228 did not run:** `api-assessment` part as `ci.yml` `api-sqlserver-shard` filters it, on `b229-mssql` (6985), at `caa5a97` and `371f900`, once each, wall time recorded against its 20-min cap. **FAIL:** any red, or a moved class that behaves differently on SQL Server than on SQLite.
- **The host move did not skip, merge or trim any row (drafter's items 6, 7; BACKLOG risk: the api job ran 14m12s on B226):**
  - Per class, from the trx: tests discovered, executed, passed, skipped, not executed, for `B226NameMatchingTests` at `caa5a97` vs `371f900` (expect 114 = 114) and `B228NameMatchingTests` at `9274786` (host per row) vs `371f900` (expect 98 = 98). Each row's display name and outcome equal, row for row.
  - Assertions: count `Assert.` call sites per test method at the base-equivalent and the tip, and list every changed assert line (the drafter found one: the audit filter). Grade it (drafter's item 6).
  - **Row isolation on the shared host:** run ≥ 20 rows of each class ALONE (`--filter` on the row) and in the full class; outcomes equal. Run the class twice in one process order and once with the theory data reversed in a scratch copy of the test file (in `wt-B229-mut` only, restored equal). **FAIL:** a row whose outcome depends on another row (alias numbering, customer-name uniqueness per partner, audit rows).
- **CI projection** (the B228 brief's instrument: `dotnet test HpsmPoc.slnx -c Release --no-build`, SQLite + Azurite): `caa5a97`, `9274786` and `371f900` interleaved, ≥ 3 runs each, load1 per run, at a comparable load. Report the medians, the per-class trx durations (critical path), and the projection 852 s × (tip ÷ base) AND × (`9274786` ÷ base) (what the product commit costs without the move). State plainly that 852 s is the whole job (drafter's item 8). **FAIL:** a projection ≥ 900 s at the tip; ≥ 870 s is a margin under 30 s, said in BLUF.

### 7. Mutants (B228's killing sample, re-run, plus ≥ 8 of your own)
- **Runner** as B227's (exact anchors, count 1, restore by a fresh write, sha256 = the head blob AND `git diff --quiet`, a new mtime; controls green). Suite = `B215DemoAliasPdfTests` + every `B223*` + `B226NameMatchingTests` + `B228NameMatchingTests` (B228: 271 tests at `371f900`, :65).
- **Re-make at least 8 of B228's killing mutants** (`evidence/mutants.tsv`), including `n-lookfirst`, `n-trname`, `n-trtext`, `n-umlaut`, `n-mn4`, `n-hoststart`, `n-case-after` (1 red: fragile), `n-n3`; and B227's `m6`, `m7`, `m9`, `m10` (killed at B228 by its new rows). Give red counts against B228's.
- **At least 8 of your own**, for example:
  - `NarrativeTextLeftOut` = "" (a blank text: the selector skips it, the fallback prints: does a test notice?);
  - the compared model leaves out APPROVED text only, keeping edited (V3-like);
  - `OtherReading` dropped, or `HasOtherReading` always false;
  - `NoDecomposition` applied to the name only (and to the text only, if B228's `n-trname` / `n-trtext` are not exactly that);
  - ø → "o" only (the second reading's "oe" dropped);
  - `GluedParts` without the case split; the "before the last capital" split dropped;
  - the alias taken out AFTER `GluedParts` (does "ORG" re-appear?);
  - the final-sigma fold dropped; the lunate pre-NFKD replace dropped;
  - the provenance lines left out of the compared model (V1's shape: does `g7-template-exact` reopen and does a test see it?).
- Any SURVIVOR is a finding with a fix-shape and the regression test that would be red; an equivalent mutant is proved, not asserted.

### 8. Timing on the Demo copy (cold / warm) vs base, stated with load
- The seeded 17-page report AND a fresh report with all three narratives approved (N-3 now checks every narrative string): ≥ 5 cold (fresh API starts) and ≥ 50 warm per tree, `371f900` vs `caa5a97`, interleaved, `load1` per sample. Name the instrument (in-process or live Kestrel + curl; drafter's item 12).
- Also time `DemoCopyText.Of` + the checks in-process with a Stopwatch in your probe; report the added time as `371f900 − caa5a97` (median, IQR), and CPU per read.
- Compare only within an instrument: B227 `:51` (in-process), B228 `:19` (live).

### 9. MERGE line: main + head in a scratch clone
- In `.tools/b229/merge.git` (`git clone --bare --shared`): `merge-tree --write-tree caa5a97 371f900` → expect `728c8b3366dbdc2a500fe998a4075d440991ab43`, rc 0, the head's own tree (fast-forward: `merge-base` = `caa5a97`). Re-derive against main as it is at verdict time.
- If main has not moved, the merged tree IS the head's tree: items 1–8 cover it; say so. If it moved (TARGETS rules allow it), build and test the merged tree once in `.tools/wt-B229-merged` on 6990: API suite, vitest, typecheck, lint, build, contract-drift.

## NOTES FOR FRIDAY (hosted; all UNMEASURED by HOLD)
Write a short section of what may differ on the hosted site, each line UNMEASURED with the instrument that would close it (Friday's, not yours):
- **Azure SQL vs SQLite:** collation and case behaviour of stored names and narrative text (does a stored name come back byte-equal, so `Plain` sees the same runes?); the shared-host test move is SQLite/SQL Server only.
- **Blob storage vs Azurite:** the stored PDF bytes the Demo check reads (`DemoCopyText.Of`) come from Blob; any difference in the bytes read changes nothing in the check only if byte-identity (gate 1) holds.
- **The hosted seed's names** (same `ShowcaseSeeder`): expect 0 hit by item 3's class; say whether any seeded word is a template word.
- **Time:** the Demo copy's cold and warm cost against the BFF's 30 s `/content` budget (re-cite `web/src/server/bff.ts` `NAMED_WRITE_TIMEOUT_MS` / `DOWNLOAD_READS`, B227 `:234`: `:151`, `:171-178`), given item 8's added time.
- **The AI provider on the hosted site** (if one is configured there): item 3's class widens to any one-word name the model writes. UNMEASURED by HOLD.

## KNOWN (Kam's or Friday's to rule; confirm and record, do not grade)
- The narrative-edit / free-text rules, MN-3, F-3; N-8's words (the 409 for the common-word and approved-text causes): Kam's.
- N-6, N-7, N-11, N-12/N-13: LEFT, not ruled into round 3.
- The Dependabot high on main (B228 pins.txt: "1 high").
- Known flakes: HPSMPOC-247 `ImportRobustnessTests.R2_2`; `hosted-entra.spec.ts:65` ordering; `metrics-dashboard.spec.ts:24` under load (B228 :126). Re-run alone, never skip.
- B226's transcript key slip (`b225-azurite`): Friday's. Do not open that env file.

## FINDINGS FORMAT
- Each finding has: severity (Blocker / Major / Minor / Note), `file:line` at `371f900`, the instrument, the FAIL condition it met, a prose fix-shape, and the regression test that would be red.
- Severity yes, priority no (charter §8). One defect per finding (charter §9).
- **A route that serves a readable form of the customer's name to a Demo-holding caller, where B228 claims it is closed, is at least Major.**
- Item 3 is graded as a COST (names, reports, words, way out), with a severity for the user-facing harm, never as PASS/FAIL.
- Every claim carries its source line or UNMEASURED.

## HOLDS
- No HP Restricted document (the executive deck, the financial model, anything HP marks Restricted) is given to ANY AI tool — Claude seats, subagents, the product's model, Ornith or the Spark — without HP's written approval (signed SOW §4.1.4(c)). Every PDF here is the product's own synthetic report. Do not open `HP Reporting and Docs/` or the SOW file in the project root.
- Datasec only; no other client's names, tickets or paths.
- **Findings only:** no code, commit, push, PR, Jira, BACKLOG, ticket or `history.md` write; no deploy, no Azure, no setting change, **no hosted request**; nothing to HP or any human. Fixtures synthetic ("(sample)" suffix, as B225/B227/B228). No live AI call; seam text through the test database only.
- **Never open `4_Credentials/.env`.** Never print a secret; env files by shape only.
- **Never delete: quarantine** (`.tools/b229/quarantine/`). **Never edit a running script.** Copies of B227's / B228's kits are run as copies, never edited in place.
- **Ports 6981–6990 only, `lsof` before each bind.** Processes: kill by port + cwd, never by name. Stop everything you started before READY.
- No force-push, no branch delete, no history rewrite, no ref write in `2_Project_Files`.
- Seat A's (B228) worktrees, kits, ports and containers are never touched.
- **Round 3, Kam's ruling:** on NO GO the closed instances ship and the residue goes to Kam as a card; no round 4 without his word.
- *(Time-box)* about 3.5 h of gate time. Anything not reached is NOT TESTED with the reason, never a silent PASS.

## UNMEASURED at draft (each closes as stated)
- **Whether the Datasec/HPSM-POC-E pane is free to launch:** Friday, at launch.
- **Whether main or the head moves before your verdict:** your `ls-remote` at start, mid-gate and end, then the TARGETS rules.
- **The merge tree** (the drafter's guard refused `merge-tree`): item 9.
- **The 8 unpinned must-refuse rows and the 30 / 35 / 37 must-open count:** drafter's items 1, 2.
- **The 158-row residual's composition:** drafter's item 3.
- **Whether the shared-host classes run green and isolated on SQL Server:** item 6.
- **Whether re-generate is a way out of item 3's refusal:** item 3.
- **Whether B228's reader v3 sees B227's base-control leaks:** item 1 (c).
- **Whether ports 6981–6990 stay free:** your `lsof` at each bind.
