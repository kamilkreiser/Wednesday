KITS STARTABLE: B1400 B1401 B1402 B1403 B1404 B1405 B1406 B1407 B1408 B1409 (all ten only after common edit E1; B1406 only before B1410's renamed seat starts, see X1) B1420 B1423 (only after common edits E1 and E2) | HOLD: B1410 (seat id R197 is already used by HPSM B1397, which has a live pane; three template lines forbid the Jira writes that line 1 grants; a `%s` is left unfilled at :73; it races B1406 for the root `main`) B1421 (PCOMP-114's timing fix already landed as PR #110 per Composer C-119, and row #428, whether that settles the ticket, is waiting on the product owner) B1422 (P-d invites fixes to residues that are already ticketed as PCOMP-119 and PCOMP-124 to PCOMP-127, and PCOMP-127 is held for the product owner) B1424 (the Done-move rule leaves out C-112's three conditions; C-120 and C-123 keep both tickets open by design; it cites C-119 for the wrong PR)

# MPS and Composer kit review (read-only), 2026-11-10

The reviewer read everything listed below between 05:5x and 06:1x AEDT. First clock printed: `date` = Tue 10 Nov 2026 06:05:11 AEDT, taken at the origin re-read.
Read whole: all 16 kits; `2026-11-10_mps_composer_sweep/lanes.md` (224 lines); `DRAFTER_RULES.md` (75 lines); MPS `CLAUDE.md` (82 lines); Composer `CLAUDE.md` (33 lines).
Read at source by `grep -n`: MPS CLARIFICATIONS C-79, C-99 and the "one card per deploy" lines (:788, :821); Composer CLARIFICATIONS C-101, C-111/C-112 (:2029, :2049), C-119, C-120, C-123 and C-124.
Origin was read by `gh api -X GET` under each project's own `4_Credentials/.gh-config`. Nothing was written except this file.

## The known risk: were the MPS kits rewritten by the Composer drafter? NO (MEASURED)

I compared each MPS kit against its lane in lanes.md with a program. All ten builder kits match their lane exactly on four counts:
- tickets (fresh plus conditional);
- the owned-glob list, in the same order;
- the repo (`datasecau/MPS-Commercial-Calculator`);
- the project root (`.../Datasec MPS Commercial Calculator`).

Other checks:
- Each kit quotes the landing rule from MPS `CLAUDE.md:50` (count 1 per kit). B1410 is a records kit and has no code landing.
- The nine-lane PARTITION list inside each kit matches lanes.md and the B and SEAT mapping (0 mismatches over 90 rows).
- The only Composer mentions in the MPS kits are three lines each: line 1 (the sweep path), the "OTHER PROJECTS" partition line, and S0.
- File times: the MPS kits are 03:21 and the Composer kits 03:22 to 03:23.
- The Composer kits use a different template and name only `datasecau/Datasec-Security-Composer`.

## Origin facts re-read at 06:05 AEDT (the stamp values rest on these)

| Fact | Value | Instrument |
|---|---|---|
| MPS main | `31234f5f0e17dadcd5d6955055d477e660d204b7` (equal to the drafting read) | `git/ref/heads/main` |
| MPS open PRs | 0 | `pulls?state=open --jq length` |
| MPS refs `heads/b140` | 0. `heads/b14` lists only `b14/infra-ci-deploy-demo` and `b14b/hsts-forwarded`, which are old and not `b1400*` | `matching-refs`; control `heads/b1368` gave 2 |
| MPS tree | 767 entries, 682 blobs, `truncated=false` | `git/trees/main?recursive=1` |
| Composer main | `a54250f48f41b693ab73163531e7ca82425fce69` (equal to drafting) | `git/ref/heads/main` |
| Composer open PRs | #91 (Dependabot, 2 files), #86 (Dependabot, 2 files), #85 (draft "HOLD K6", 57 files) | `pulls?state=open`, `pulls/<n>/files --paginate` |
| Composer refs `heads/b142` | 0 | control `heads/b1249` lists `b1249/composer-pcomp115-db-test-typecheck` |
| Composer tree | 1,037 entries, 966 blobs, `truncated=false` | as above |
| PR #111 / #114 | merged 2026-11-02T01:50:47Z, sha `69b01339...` / merged 2026-11-03T00:07:47Z, sha `2f63b2f6...` (as in B1424:18) | `pulls/<n>` |
| Composer root repo | HEAD `12f7d5e0...`, no remote (0 lines), `JIRA.md` and `history.md` clean, `JIRA.md` 50 lines | `git --no-optional-locks` |
| MPS root repo | HEAD `13db4d11...`, no remote; ` M` on `5_Project_History/history.md`, `BACKLOG.md` and `JIRA.md`; `SETUP_RUNBOOK.md` is tracked and clean; C-79 at `CLARIFICATIONS.md:1712`, C-99 at `:2617` | same |
| Listeners | `lsof -nP -iTCP:9700-9939 -sTCP:LISTEN` printed nothing | control: the unfiltered listing has 11 lines |
| Live panes | 14 `Datasec/HPSM-POC-*` panes, **including `Datasec/HPSM-POC-R197`**, plus `tuesday` and `fleet-monitor`. No MPS or Composer pane | `tmux list-panes -a -F '#{@cockpit_name}'` |

## Check 1: partition (by program, `part.py` in the reviewer's scratchpad)

How the program works:
- It expands every lane glob against origin main's blob list.
- It checks each pair of lanes for (a) a path both match, (b) the same glob, and (c) for wildcard globs whose stems nest, a synthetic probe path that both match.
- It checks each open PR's file list against every lane.
- **Control:** a planted duplicate lane and a planted nested lane were each flagged (3 of 3).

Results:
- **MPS: 10 lanes, 45 pairs, 0 overlaps. PASS.**
  - Per-glob matches equal those printed in each kit. The `LaneM4*`, `LaneM5*`, `LaneM10*` and `LaneM11*` globs match 0 paths, as expected for new files. They sit in distinct stems and folders.
  - MPS has no open PR, so there is no PR overlap.
- **Composer: 4 lanes, 6 pairs, 0 overlaps. PASS.**
  - **Open-PR overlap: PR #85 (draft, HOLD) lists `packages/renderers/src/pdf-fit.ts`, which C1 / B1420 owns** (#85 file list :46).
  - B1420:26 (REFUSE 6) states this as a named exception. Rate it a risk, not a block: whichever of the two lands second will conflict. #86 and #91 overlap no lane.

Partition notes that the path proof does not see (ticket overlaps):
- **X1 (MPS root repo).** Two seats ref-write the root `main`:
  - B1406 (M8, `ROOT:SETUP_RUNBOOK.md`, root branch `records/b1406`, ff-only), per its lane note at B1406:30.
  - B1410 (R1, `records/b1410`, ff-only).
  - B1410:70 (REFUSE 5) stops if root HEAD changes mid-run. A B1406 land during B1410 therefore stops B1410, and a B1410 land first makes B1406's ff-only fail.
  - **Order them:** B1406's root commit lands before the R1 seat's Step 0, or the root edit moves into the R1 records seat.
- **X2 (MPSCALC-207).** It is conditional in both M8 (B1406) and M10 (B1408). B1408 states the rule "whichever seat reaches it first ... ALREADY-ON-MAIN"; **B1406:28 does not.** Add the same sentence to B1406. This is a FINDING, not a HOLD: the paths are disjoint.
- **X3 (shared tickets between records and builder seats).** MPSCALC-178, 189, 203, 358 and 381 are on R1's closed list and are also builder conditionals. Both sides already say so: B1400:50 and the equivalent line in each MPS kit, and B1410:45 and :75. PASS.

## Check 2: holds

**MPS: PASS for all eleven kits.**
- No PR, merge, push to main, deploy, `az`, docker, ssh, hosted HTTP or mail. See B1400:7 and :85; each builder kit has the same lines, shifted by the lane-specific lines.
- The npm registry is allowed for `npm ci` only.
- Jira is read-only in every builder kit (B1400:82).
- The deploy rule matches the project: "MPS hosted is one card per deploy" (MPS `CLARIFICATIONS.md:788`, `:821`), and `CLAUDE.md:56-57` says "no GitHub push to `main` without a brief".
- B1407 (M9) keeps the deploy scripts and bicep modules out of scope. Its lane note forbids `az bicep` and running Entra.
- B1410 writes Jira only, within a closed list of at most 58 writes (B1410:1).

**Composer: PASS on deploy, PR, merge, push, hosted and mail.**
- "Composer deploys only on the product owner's card": B1420:7 cites `CLAUDE.md:30` and C-101 (`CLARIFICATIONS.md:1799`, re-read).
- Jira writes appear only in B1424 (at most four, closed list).
- Docker is used locally, under the project heavy lock.
- One wording conflict: B1420:68 and the matching step in B1421 to B1423 "remove `pc-b142x-*` containers and images by exact name", which sits beside "never delete". Make removal of the seat's own containers an explicit exception, or change it to "stop".

## Check 3: seat ids and ports

- **R197 collision: MEASURED.** `SEAT-R197` is in `2026-11-10_B1397_SEAT-R197_*` (HPSM), and the pane `Datasec/HPSM-POC-R197` is live now.
  - B1410's REFUSE 2 and 3 regexes would not trip on it, because they match `^Datasec/MPS-R`. Records, evidence and run files would still carry a duplicate id: `runs/done-when-<key>-R197.txt` at B1410:56, and "Recorded by B1410 SEAT-R197" at :62.
  - Also seen, outside this review's scope: R196 is used twice (B1386 and B1434).
- **Proposed: MPS R1 becomes `SEAT-R200`, pane `Datasec/MPS-R200`.**
  - R200 does not occur in any 10 Nov kit, report or today's daily note.
  - R199 is free too, but the B1440 report's census names R199..R209 as "no kit exists"; R200 follows the instruction to start at R200. R201 belongs to B1444.
  - Rename every R197 in B1410: file name, title :3, :56, :62, REFUSE 2 and 3 at :67-68, launch :102.
  - Rename the `SEAT-R197` line in each MPS builder kit's PARTITION (B1400:50 and its equivalents).
  - Composer B1420:15, B1423:15 and B1424:13 say "R197 was taken by the MPS sweep's records kit". Change these to "R197 was already in use (HPSM B1397); the MPS records kit is R200".
- **Composer R198: keep.** It is unique: only B1424 holds it. The only other mentions are text in the C9x kits.
- **Ports.** Scanned the non-`.pre-` SEAT kits of 9 and 10 Nov, word-boundary, for `9[7-8][0-9][0-9]`:
  - B1392 to B1395 hold 9700-9739.
  - B1440 to B1442 only mention 9740-9799 as MPS's; they use 9940-9969.
  - B1455 lists 9740-9849 and 9850-9899 as already taken (by these kits).
  - B1391 and B1454 hit only a clock or GUID token (`9834`).
  - The positive control `948[0-9]` hits 1 file (B1368).
  - Nothing is listening in 9700-9939.

| Seat (proposed) | Kit | Port block | Note |
|---|---|---|---|
| M101-M110 | B1400-B1409 | 9740-9749 ... 9830-9839 (as drafted) | free; not in the taken set; no listener |
| **R200** (was R197) | B1410 | 9840-9849 (as drafted) | a records seat opens no listener |
| C90-C93 | B1420-B1423 | 9850-9859, 9860-9869, 9870-9879, 9880-9889 | free |
| R198 | B1424 | **9890-9899** (B1424:9 names the umbrella 9850-9899, which covers the C9x blocks) | records; no listener |

## Check 4: model ids and launch lines

- `models_latest.json:17` = `claude-opus-5-5` and `:23` = `claude-sonnet-5-5`. Both exist.
- The routing rows cited (`model-routing.md:92` C2, `:98` C8, `:108-110` G1 to G3) read as the kits quote them.
- Code lanes run on Opus by Tuesday's sweep instruction, and each kit says so. B1406 and both records kits run on Sonnet.
- **The level is inside the quotes in all 16 kits. PASS.**
- **`CLAUDE_CONFIG_DIR=/Volumes/Datasec_DEV/TUESDAY/4_Credentials/.claude` is inside the launch quotes in all 11 MPS kits (count 1 each) and in 0 of the 5 Composer kits.** These are B1420:13, B1421:13, B1422:13, B1423:13 and B1424:11. **FINDING, fix E2.** The Composer drafter copied the older Composer form (B1249 / B1338). B1371, the MPS form, carries it.

## Check 6: Composer drafter caveats

- **Scope sentences relayed, no Jira read.** All five kits say so (B1420:5, B1424:7) and make the seat's own Jira GET and quote at Step 0 or 0b governing. PASS.
- **PCOMP-114 may already be fixed.** B1421 handles the code side: premise first, then a no-commit READY on main's sha (P-c). **But Composer C-119 (`CLARIFICATIONS.md:2221`) records that:**
  - PR #110 (squash `f3cd568e`, branch `b1084/composer-pcomp114-engine-timing-row`) landed the 60,000 ms timeout plus thread-CPU median.
  - PCOMP-114 was commented and NOT moved, because clause (1), "the full node run under the hog", is NOT MET on the gate's cells.
  - **Row #428, whether the clock change settles PCOMP-114 or the ticket's own shape is still wanted, is NOT RULED and awaits the product owner** (C-119 (5) and "Does not settle (2)").
  - The lane's fix shape is exactly the open question of row #428, so the lane is ruling-bound. lanes.md classed it "fresh" because PR #110's title does not name the key. **HOLD.**
- **No docker-less test route.** B1420:57 states it plainly: "a green there is a lead and not the CI predicate". B1422:42 says db rows have no route ("UNMEASURED: no docker; do not claim P-c"), but does not say what the last line must be. B1421's premise (P-a) needs `docker run --cpus=2` and has no no-docker branch. FINDINGS on those two kits.
- **Close-with-evidence first.** Every kit runs PRIOR WORK, the main read and "do not redo a fixed ticket" before any edit. B1421 has P-c and B1423 has Step 2. B1422 P-d and B1424 are where it goes wrong (see their rows).

## Check 7: name scans

- **MPS builder kits:** step 5(d) asks for "no person's name ... in added lines or any commit message" with **no pattern** (B1400:72, B1401:73, B1402:73, B1403:76, B1404:75, B1405:78, B1406:75, B1407:75, B1408:73, B1409:79).
  - DRAFTER_RULES:40-43 requires every name scan a kit asks for to be **underscore-aware**: `(?<![A-Za-z])<name>(?![a-z])` or split on `_`, with a control that plants `_by_<name>_`.
  - **FINDING, fix E1:** add that pattern and control to 5(d).
- **B1410:62** (records text rule) and **B1424:40 and :50** (TEXT RULE and records text) have the same gap.
  - B1424's regex is "the word list above", which names no person, so a name would pass it.
- **Composer builder kits:** the commit scan is `grep -c -i -E 'B[0-9]{3,4}|PCOMP|Kam|Kreiser|Tuesday|Wednesday|Friday'` (B1420:75, B1421:71, B1422:73, B1423:71).
  - It is a substring match, so it is underscore-aware.
  - But its list leaves out the other people named in the project's own records (the reviewer first name at Composer `CLAUDE.md:22` and `:31`).
  - Its control is "a planted one", not `_by_<name>_`.
  - It covers commit messages only, not added code-comment lines.
  - Fold these into E1.

## Check 8: `@MAIN@` and stamp slots

- **`@MAIN@` occurs 0 times in all 16 kits.**
  - It is the HPSM drafter's convention (B1440 to B1442 only; the B1440 report:49 says so). DRAFTER_RULES names only `@NOW@`.
  - The base sha goes in a slot instead: S2 BASE in the MPS kits (B1400:91 and its equivalents) and "Main head at launch" or "Heads at launch" in the Composer kits (B1420:94, B1424:65).
  - Not a finding. Stamp the full 40-hex sha in that slot.
- **Slot counts (`grep -c -E '_''_''_''_'`):**
  - MPS builders: 11 each (S0 to S9 plus READ-WHOLE), matching "11" at B1400:58 and :88.
  - B1410: 16, matching :86.
  - Composer: 9 each, matching "nine" at B1420:20 and :91.
  - The last line is `READ-WHOLE-BY-TUESDAY: ____` in all 16. PASS.

## Findings per kit (check 5, facts, included: at least 2 re-read at source per kit)

### MPS

| Kit | Result | Findings (file:line) |
|---|---|---|
| B1400 M101 | STARTABLE (E1) | Facts re-read: main sha (B1400:12) MATCH; the 4 `FleetGrid*.test.tsx` blobs MATCH; `ci.yml:45/:58/:61-63/:66` MATCH (web, node 24, the three runs, the entra build). E1 at :72. |
| B1401 M102 | STARTABLE (E1) | Re-read: `smoke.spec.ts:23` MATCH; **MPSCALC-297 looks ALREADY-ON-MAIN**: `smoke.spec.ts:61` already reads `{ name: 'Proposal', exact: true }` with the comment "(B325-2)", and `b46-home.spec.ts:65` already lists the five-item nav including 'Customer proposals'. The kit's PRIOR-WORK step (d) handles this; expect `ALREADY-ON-MAIN`. No browser download is granted (B1401:14): the lane may end NOT RUN if Playwright browsers are absent. E1 at :73. |
| B1402 M103 | STARTABLE (E1) | Re-read: `CareKeyPatternApiTests.cs:15` = `SyntheticCarePack = "care_0123..."` MATCH; `TemplateIsolationTests.cs:63-65` names the unread forms MATCH. E1 at :73. |
| B1403 M104 | STARTABLE (E1) | Re-read: the four owned test files exist (1 blob each) MATCH; `ci.yml:30/:42/:43` MATCH. E1 at :76. |
| B1404 M105 | STARTABLE (E1) | Re-read: `ReferenceDocumentValidator.cs` is under `src/MpsCalc.Import/Validation/` (owned) MATCH; pointers `:166` (product group) and `:203` (cppSupplies link) MATCH; **`:160` and `:162` are bare `{` lines (RELAYED pointers, stale)**. The kit tells the seat to re-print pointers. E1 at :75. |
| B1405 M106 | STARTABLE (E1) | Re-read: `FeedbackEndpoints.cs` and `FeedbackStore.cs` are under the owned `src/MpsCalc.Api/Feedback/`, and `FeedbackStoreTests.cs` matches `Feedback*.cs`, MATCH; **`FeedbackEndpoints.cs:223` is `if (item.Attachments ...` and `:232` is `}`: not the StateOf/SaveTicket lines (RELAYED, stale)**. E1 at :78. |
| B1406 M107 | STARTABLE (E1, X1 order, X2 sentence) | Re-read: **`IMPORTER.md:112` is the table header and `:117` the Price List row; "262" is at `:127`; and "294" occurs 0 times in IMPORTER.md** (control: 262 found), so part of MPSCALC-200 may already be fixed. The seat's prior-work step decides. Root `SETUP_RUNBOOK.md` is tracked and clean (MATCH with the lane note). X1: the root `main` race with the R1 seat. X2: add the 207 sentence. E1 at :75. |
| B1407 M108 | STARTABLE (E1) | Re-read: `test_infra.py:4` (BICEP, then PATH, then az, FAILS never skips) and `:59` (`az bicep build`) MATCH; `entra_apps.py:172/:174` (group created, then the security-only Stop) MATCH; `ci.yml:83` `export BICEP=` MATCH; **`package.sh:45` is the `dotnet publish` line; the N-6 comment is at `:44`** (pointer one off). `.tools/bicep-v0.48.1` exists (MATCH). E1 at :75. |
| B1408 M109 | STARTABLE (E1) | Re-read: **MPSCALC-302 looks ALREADY-ON-MAIN.** At `ParityProof.cs:190-199`, main builds the owed (device, SKU) pair list and compares it with `SequenceEqual` ("a missing pair, an extra pair or a repeated pair all differ ... whatever the counts"), so a count-preserving swap already reads DISAGREE. The kit's step (d) handles this; expect `ALREADY-ON-MAIN`. Readiness files are under the owned `src/MpsCalc.Engine/Readiness/` (MATCH). Not measured: whether `web/src/screens/quote/ReadinessPanel.test.tsx` pins the 295 sentence (not M10's path; the seat's STOP rule covers it). E1 at :73. |
| B1409 M110 | STARTABLE (E1; one pointer fix) | Re-read: `PurchaseValidation.cs:32` = `MaxWalkEntriesListed = 20` MATCH. **`web/package.json` has NO `sync-contract` script.** Its scripts are dev, build, preview, test, test:watch, lint, typecheck, `gen:api` (openapi-typescript over `src/api/generated/openapi.snapshot.json`) and e2e. The sync script is the FILE `web/scripts/sync-contract.mjs` (tree). The kit text "read `web/package.json` scripts to find it" leads nowhere: name `node web/scripts/sync-contract.mjs` and `npm run gen:api`. The sync tests `web/src/api/contract.sync.test.ts` and `contract.test.ts` are not M11 paths; they must go green, not be edited. E1 at :79. |
| B1410 R1 | **HOLD** | (1) **R197 collision** (check 3): rename to R200 throughout. (2) **Self-contradiction on Jira writes.** Line 1 grants at most 58 Jira writes, but the copied builder lines say the opposite: `:79` "Jira: read only, 0 writes (the one records seat R1 is the only Jira writer ...)", and "Landing is Tuesday's: PR, hosted CI, CodeQL" (wrong for a records seat). `:93` S6 "NO: PR, other refs, **Jira write**, ... plain pushes of ONE new branch". `:91` S4 defaults "independent branch, no merge of main" (the seat does merge ff-only into root main). `:95` S8 "Tuesday opens the PR". Replace :79 with records standing lines and rewrite the S4, S6 and S8 labels for a records seat. (3) **`:73` holds an unfilled template `GH_CONFIG_DIR=%s/4_Credentials/.gh-config`.** Write the absolute project path. (4) X1 race with B1406 on the root `main`. (5) E1 at :62. Re-read: C-79 at `CLARIFICATIONS.md:1712` (MATCH, "the product owner's 2026-11-01 ruling"); highest C-entry C-99 at `:2617` (MATCH); root HEAD `13db4d11` (MATCH); the three dirty root files (MATCH). |

### Composer

| Kit | Result | Findings (file:line) |
|---|---|---|
| B1420 C90 | STARTABLE (E1, E2, E3) | Re-read: `change-report.ts` is 661 lines, with `:498` BUDGET 122, `:501` ROWS 2, `:521` HARD_BREAK, `:541` `modelledFooterRows` and `:569` `fitsAboveHash`, all MATCH; the test file is 798 lines (MATCH); #85's list holds `pdf-fit.ts` at :46 and `document-pdf.ts` at :44 (MATCH). The look waits for the product owner, build only (:3, :66, :79): PASS. **E3: `:11` `lsof -nP -iTCP:9850 to 9859` is not valid lsof syntax** (the same in B1421, B1422 and B1423 at :11). Write `-iTCP:9850-9859`. The root `core.sshCommand` names `/Volumes/Laptop-DEV/...` (MATCH with :61); the deploy key `3_Access_Keys/composer_github_deploy_rw` exists (MATCH). PR #85 overlap: a risk, named at REFUSE 6. |
| B1421 C91 | **HOLD** | PCOMP-114 premise: see check 6. **C-119** (`CLARIFICATIONS.md:2221`) shows PR #110 already carries the fix, and **row #428 is NOT RULED (awaits the product owner)**. The kit's FACTS (B1421:40) call it "UNMEASURED: whether PR #106 or a later PR already carries the 60,000 ms edit"; the answer is in the records. Re-scope it to a measurement-only seat (clause (1): the full node run under the hog at main; no commit; P-c), or hold it for the row #428 ruling. Smaller: **`}, 60_000);` is at `performance.test.ts:76`, not `:77`** (`:77` is `});`; the file is 77 lines, MATCH); `:44` carries the 60,000 ms comment (MATCH); `b116-s10-verify-dom.test.tsx:119-120` (MATCH). There is no no-docker branch for P-a (`--cpus=2` needs docker): add "no docker: `STOPPED: NEEDS TUESDAY no docker for the cap`". E2 at :13, E3 at :11. |
| B1422 C92 | **HOLD** | **P-d (B1422:35) says "a code or doc residue remains inside your three paths (then fix it by the same rules)".** C-120 (`:2246`) records that PCOMP-98's owed rows are already **ticketed as PCOMP-119**, and "PCOMP-98 stays open until they land". C-123 (`:2316`) ticketed PCOMP-116's residue as **PCOMP-124 and PCOMP-125, plus PCOMP-126 and PCOMP-127**. **PCOMP-127 is an explicit exclusion in lanes.md:196 ("each item waits on a go or the product owner's words").** P-d would do those tickets' work under another key. Make P-d read-only (name the residue tickets in FOR TUESDAY; edit nothing for 98 or 116). Re-read: `DEPLOY.md` is 652 lines and `:263` is the version sentence (MATCH); `b778...db.test.ts:774` is the row title (MATCH); "row 8" occurs 0 times in both files (MATCH); the pin paragraph is at `DEPLOY.md:223` (MATCH). **The control figure "`pg_restore` prints 12 lines in DEPLOY.md" (B1422:32) is 9 by `grep -c -i`** (stale control). No-docker: give the last line (`BLOCKED: no docker for the db route`), not READY. E2 at :13, E3 at :11. |
| B1423 C93 | STARTABLE (E1, E2, E3; Tuesday answers Q-1 at the stamp) | Re-read: `Discovery.tsx` is 1,230 lines and `:271-273` is the `typedDraftFor` closure with `draftKey(answerKey, null)` (MATCH); no open PR touches it (#85 list: 0 hits). The look question is Q-1 (B1423:95): Tuesday must write an answer, not the default. P-b, the unchanged DOM by program, is the right proof. E2 at :13, E3 at :11. |
| B1424 R198 | **HOLD** | (1) **The move rule is incomplete.** Composer C-111 (3) and C-112 (`CLARIFICATIONS.md:2049`): "A move needs three things: the slot reads MOVE, the Done-when table reads MET, no gate [verdict] line contradicts it". B1424:37 moves on MET alone, and its Q-1 default (:70) is "moves". Both PRs landed after NO GO verdicts on the product owner's land-and-ticket rulings, and C-120 says "PCOMP-98 stays open until [PCOMP-119] land[s]"; C-123 says "PCOMP-116 is commented and stays in the backlog". Add a MOVE-KEYS slot (default NONE) and the three conditions, as B1410:85 does. (2) Both tickets **already carry landing comments** (C-120, C-123), so the expected outcome is "no write"; the kit's PRIOR WORK (1) at :45 allows that. Say so in the BLUF. (3) **`:46` cites "C-119 and C-120 for PR #111"; C-119 is PR #110 (PCOMP-114).** Use C-120 for #111 and C-123 for #114. (4) The port umbrella 9850-9899 at :9 should be 9890-9899. (5) E1 at :40 and :50; E2 at :11. Re-read: the #111 and #114 merge shas and times (MATCH); root HEAD `12f7d5e0` (MATCH); `JIRA.md` 50 lines (MATCH); no remote (MATCH). |

## Common edits

- **E1 (all 16 kits): underscore-aware name scan.** Add to the scan step (MPS 5(d); B1410:62; B1424:40 and :50; the Composer commit-rule line) a sentence like this:
  > Name scan: for each name on the ban list, `(?<![A-Za-z])<name>(?![a-z])` (python `re`, case-insensitive), over added lines AND commit messages; control: a planted `_by_<name>_` must fire.
  - Composer: widen the list beyond `Kam|Kreiser` to the people the project's records name, and cover added code lines as well as messages.
- **E2 (B1420 to B1424): launch line.** Insert `CLAUDE_CONFIG_DIR=/Volumes/Datasec_DEV/TUESDAY/4_Credentials/.claude` as the first word inside the double quotes, at B1420:13, B1421:13, B1422:13, B1423:13 and B1424:11.
- **E3 (B1420 to B1423, :11):** `lsof -nP -iTCP:98N0-98N9 -sTCP:LISTEN`.

## Stamp values each kit needs (Tuesday attests her own reads; values below are the reviewer's reads at 06:05 AEDT, re-read them)

**MPS builders B1400-B1409 (S0-S9 plus READ-WHOLE):**
- S2 = `31234f5f0e17dadcd5d6955055d477e660d204b7`.
- S3 = open PRs 0; main as S2; no `Datasec/MPS-` pane (HPSM-POC panes live).
- S4 = defaults, each kit's own block:

| Kit | B1400 | B1401 | B1402 | B1403 | B1404 | B1405 | B1406 | B1407 | B1408 | B1409 |
|---|---|---|---|---|---|---|---|---|---|---|
| Block | 9740 | 9750 | 9760 | 9770 | 9780 | 9790 | 9800 | 9810 | 9820 | 9830 |

  Each block runs from the number shown to that number plus 9.
- S4 also carries READY / HARD STOP: +150 / +240 for most kits; **+90 / +150 for B1406**; **+240 / +360 for B1409**.
- S5 = load1 and the live panes.
- S6 = the authority.
- S7 = the block plus the level: opus, except B1406, which is sonnet.
- S8 = a gate as a separate kit, then the PR, hosted CI, CodeQL and a head-pinned squash; nothing deployed.
- S9 = the latest start.
- READ-WHOLE = `DONE @NOW@ ...`.

**Launch order:** B1406 first, or land its root commit before the R1 seat starts (X1). HEAVY allows at most 2 machine-wide.

**B1410 (after renaming it to R200):**
- S0 to S9 as for the builders, with S2 = `31234f5f...` (code main) and the root HEAD stated (`13db4d11ef18d72c219da7ab92fe5dd9497ac3e8`).
- COMMENTS FILE or HOLD; MOVE-KEYS (default NONE); CAP-READING; ROW-RESIDUAL; REC-CLAR.

**Composer B1420-B1423 (eight slots plus READ-WHOLE):**
- STAMP and LAUNCH WINDOW.
- Main head = `a54250f48f41b693ab73163531e7ca82425fce69`.
- Branch head = absent (`matching-refs/heads/b142` = 0).
- Open PRs = #91, #86, #85 (draft HOLD).
- Authority and hard stop: READY +180.
- SLOTS = HEAVYLOCK `free` (`.tools/composer-heavy.lock` absent at 06:0x: `.tools` lists 9 entries, no lock, no `b142*`), plus which siblings are live.
- Q-answers:
  - B1420 Q-1: the Done-when for PCOMP-123, P-c; Q-2: the gate tier; Q-3: the PR #85 order.
  - B1423 Q-1: the look-territory confirmation.

**B1424 (after the fix):**
- Heads: root `12f7d5e00fa3a835c9b7b63eddc0805211f1eeca` and code `a54250f4...`.
- `records/b1424` absent.
- Open PRs #91, #86, #85.
- READY +60.
- SLOTS: C3 live or not; landing comments already present per C-120 and C-123.
- Q-1 = NO MOVE unless the C-112 conditions hold; Q-2 = the transition id read from `transitions`.

## UNMEASURED by this reviewer

- No Jira was read (fence), so ticket status, text and Done-when are RELAYED.
- No test or build was run.
- No hosted host was contacted.
- Whether `ReadinessPanel.test.tsx` pins the MPSCALC-295 sentence was not checked.
- PR #85's mergeability against a C1 branch was not checked.
- Machine load for 10 MPS plus 4 Composer lanes was not measured.
