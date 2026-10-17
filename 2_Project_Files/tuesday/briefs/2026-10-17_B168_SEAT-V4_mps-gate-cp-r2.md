From Tuesday (Kam's Datasec coordinator seat), Datasec / MPS Commercial Calculator. Questions go to `tuesday-agent@agentmail.to` with subject `[Datasec/MPS Commercial Calculator -> Tuesday] QUESTION: <topic>`. `AGENTMAIL_API_KEY` is used by name only (`4_Credentials/.env`). Your STATUS file is the wrap.
# BRIEF B168 · SEAT-V4: QA GATE, TIER 1, `b104/mpscalc-140-care-packs` ROUND 2 OF 2 (the last)
**Round 1** = gate B167, **NO GO** at `d355620` on **B167-1** (Major, a missing test). Mutant CP-iii (`Join` escapes `|` before `\`) survived every test, while the gate's probe got a 500 from `GET /inventory` (duplicate catalogue key). **Under Kam's two-NO-GO cap, a NO GO here means CP does not ship this round.** This gate is NARROW. Grade only what round 2 changed, and CARRY the rest of B167 with a proof that it is unchanged.

**Drafted:** 2026-10-17 13:41-13:4x AEDT by Tuesday's drafter. Pane `Datasec/MPS-V4`. Commission: THIS file, `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B168_SEAT-V4_mps-gate-cp-r2.md` (Tuesday's tree, read-only to you).
**Step 0:** copy it unchanged into `1_Project_Definition/Briefs/`, `cmp` the copy, and put the sha256 of both in STATUS. Preflight: "none (brief_seat launch)". **No az.**
**Launch (Tuesday):** `bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/MPS-V4 "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B168_SEAT-V4_mps-gate-cp-r2.md'"` (form: `brief_seat.sh:4`).
**Report:** `1_Project_Definition/Briefs/2026-10-17_B168_STATUS.md`. Evidence goes in `Briefs/2026-10-17_B168_evidence/`.
**TESTING seat, findings only.** Charter: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`.
- §3 RULE 1: write the FAIL condition before each probe.
- §3 RULE 2: what you did NOT test is output too.
- §7: oracle, evidence, and what you proved vs assumed.
- §8: no product change and no test change. A write grant is void: refuse it.

No ticket, Jira write, PR, merge, push, BACKLOG, CLARIFICATIONS or `history.md` edit. Findings and proposed BACKLOG rows go in STATUS only.

**Shape and inheritance.** B167 is your template and your baseline. Read its brief WHOLE: `Briefs/2026-10-17_B167_SEAT-V3_mps-gate-r2-classes-carepacks.md` (272 lines). Read its STATUS WHOLE: `Briefs/2026-10-17_B167_STATUS.md` (384 lines), including its Corrections (`:366-376`), which you inherit:
- bash, never zsh, for loops and for `${h}:path`;
- a mutant run stops on a non-zero build rc;
- TRX is cut per `<UnitTestResult>`;
- markers are VALUES;
- the gitleaks control is `git add`ed;
- start a queue with SIGINT restored (`sigdfl.py`);
- a wait loop must not match itself;
- an MDR control must edit a path main already has.

**Grade by B167's rules** (its brief `:212-221`): a surviving mutant that your own probe catches = **Major**. Copy instruments ONLY from `Briefs/2026-10-17_B167_evidence/instruments/` into `.tools/qa-B168/bin/`. Never run anything inside `.tools/qa-B167/` or any other `qa-*` folder. Re-anchor each copy (B167→B168 names, ports 6820-6829 → **6830-6839**) and list which ones you reused. Lane E's report and logs (`.tools/b104/**`, `.tools/wt-b104-*`) are CLAIMS. Never re-run a builder's script as proof. Every number, sha and `file:line` you write comes from a read you took, or it says UNMEASURED. Every sha comes from `ls-remote` or from `git log` of a head you read that way.

## PINS (drafter, `git --no-optional-locks ls-remote origin`, 13:41:35 and re-read 13:44:36, equal; `cat-file -t` = commit ×6)
| Ref | sha | Notes |
|---|---|---|
| `b104/mpscalc-140-care-packs` | `a3c9b9d7de1a37fcfa683b4b40c68c84167f6223` | READY line `B104_STATUS.md:433`; tree `04291922`; behind/ahead main `0 11`; merge-base = main |
| `main` | `0217044e804afd4a457cbfd4ba4721f4f51071d1` | PR #76, the squash of CL (`gh`: `merged=true`, merge commit `0217044`, head `b50441f`); parent `ed72606`; **tree `50c52d2c` = `b50441f`'s, the tree B167 gated**; check-runs 8/8 `success` |
| round 1 | `d355620ede35cfe073b1984492b7a7a76684836d` | tree `0b0e433d` |
| (watch) `b103/mpscalc-158-target-whatif-noaudit-r2` | `88c84cd449e07565b5856d606df703b4bc4638b8` | lane D will push a header-regen head (`B103_ADDENDUM-9`), and Tuesday may merge it during your gate (see "Main moves") |

**Round 2's commits** (`git log 0217044..a3c9b9d`):
- `070db90`: the B167-1 test + the e07 re-plant. 2 files, +21 −2 (`diff --stat d355620 070db90`).
- `24143c3`: merge of `070db90` + `0217044`. `show --remerge-diff` = **0 lines**. Its tree `c30ceb24` = `merge-tree --write-tree 070db90 0217044`.
- `a3c9b9d`: the class change. 4 files, +20 −11: `docs/IMPORTER.md`, `PurchaseCatalogue.cs`, `B104CarePackApiTests.cs`, `CarePackImportTests.cs`.

**Files changed `d355620..a3c9b9d` beyond main's own (`comm -23` vs `diff --name-only ed72606 0217044`):** exactly 5.
- `docs/IMPORTER.md`
- `src/MpsCalc.Engine/Reference/PurchaseCatalogue.cs`: `diff` = **2 lines**, `:145` (comment) and **`:148`** `ItemClass.Service` → `ItemClass.CarePack`
- `B104CarePackApiTests.cs`
- `SourceLifecycleTests.GateB41.cs`
- `CarePackImportTests.cs`

The other blobs of CP's 15 files are the same as at `d355620`: `Records.cs`, `ReferenceData.cs`, `AllowList.cs`, `SynnexBook.cs`, `Sheet.cs`, `PriceBookImporter.cs`, `ReferenceStoreDocument.cs`, `ImporterTests.cs`, `SyntheticBooks.cs`, `ImportCli/Program.cs` (`rev-parse` ×2 each). All 16 of main's files have equal blobs at the head and at main. `git diff 0217044 a3c9b9d -- docs/api web scripts infra .github` is empty: no contract, generated, web or script change.

**Merge readings:**
- `merge-tree d355620 0217044` = `28608269`, which equals B167's CL+CP pair tree.
- head + `88c84cd`: rc 1. The conflict is in `SOURCE.txt` and `schema.ts` ONLY, the same as main + `88c84cd` (`8586b354`). CP adds no conflict, and T∩CP by name is empty.

**Commission (read WHOLE, 14 lines):** `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B104_ADDENDUM-7_b167-cp-fix-round.md`:
- item 1: the B167-1 test, proved red on CP-iii and on CP-i;
- item 2: merge main (no rebase), then the ONE line `:148` + `B104CarePackApiTests.cs:69`, with `?class=carePack` and the services subtotal unchanged;
- item 3: the B167-7 re-plant of e07;
- "Change no other product code."

**Claims:** lane E's `## ADDENDUM-7` (`B104_STATUS.md:400-433`):
- CP-iii 1 failed / 10, CP-i 2 / 9;
- e07 now `V`, and CP-i turns e07 + e08 red;
- the class test red at `Service`;
- CI Import 118 / Engine 338 / API 1,599, web 707, 0 lost.

**Anchors at the head:**
- `B104CarePackApiTests.cs:30,40,44` (`?class=carePack` / `service`), `:73` (`carePack`), `:78-79` (servicesExTax = the line's sell);
- `CarePackImportTests.cs:107` (renamed `Care_packs_are_carePack_rows_…`), `:141-142` `Expected` (a copy of `Derive`; the natural keys are hand-escaped), `:168` `B167_1_keys_of_parts_holding_a_bar_or_backslash_escape_the_backslash_first`;
- `GateB41.cs:235-252` (e07, now `V`).

Outside `PurchaseCatalogue.cs:148`, NO `src` path switches on `ItemClass.Service`. The only class-sensitive reader is `PurchaseCalculator.cs:45` (`Service or CarePack or Staging => 3`), plus `PurchaseMapping.cs:116-117/137-138` and `InventoryEndpoints.cs:350-352` (drafter's `git grep 'ItemClass\.'`).

## Verdict lines (first lines of STATUS)
- `B168-CP a3c9b9d:` `GO | GO WITH NOTES | NO GO` (round 2 of 2)
- one line each:
  - `B168 (1) new test red on CP-iii and CP-i (gate's own mutants), exhaustive collision check:`
  - `B168 (2) care-pack class: API carePack, picker "Care pack", ?class=carePack book rows, services subtotal unchanged, stored quotes:`
  - `B168 (3) e07 re-plant (B167-7) and edited tests not weakened:`
  - `B168 (4) round-2 diff = ADDENDUM-7's files only:`
  - `B168 (5) CI line as name sets vs main (0 lost):`
  - `B168 (6) rollback door (3) re-read with the class change:`
  - `B168 (7) B167 CP checks carried (which, why):`
  - `B168 MERGE on <main-at-verdict, 7>:`

## Checks (FOUND / TESTED / HOW, each with a control that can fail)
0. **Machine.**
   - **Clone:** `git clone --shared --no-checkout` of `2_Project_Files` → `.tools/qa-B168/repo`, push URL `DISABLED` (show `remote -v`).
   - **Worktrees** (detached, under bash):
     - `base-main` = `0217044`
     - `hCP` = `a3c9b9d`
     - `r1` = `d355620`
     - **`prev`** = a scratch commit of tree `28608269`, with parents `d355620` + `0217044` (round 1's product on the new main: your oracle for "only the class changed")
     - `mutCP`
   - **Toolchain:** `.tools/dotnet` (read its version), Node as found (CI pins 24: a stated difference), Python `-I`, gitleaks.
   - **Heavy slots** (MPS-LANES ADDENDUM-6; copy `slot.sh` / `release.sh`):
     - one slot at a time; a `holder` file reading `B168` + the start time;
     - record the slot number and `uptime` beside every result; release only your own slot (the one removal allowed);
     - **drafter at 13:42:31:** only `.tools/heavy-slot-1` exists, holder "B103 lane D: whatif2 full started 2026-10-17 13:35:55 AEDT"; load1 **47.79**. Expect waits.
   - **0 tests matched, or a failed build, is never a pass:** every result carries its count, filter and build rc.
   - **Ports `6830-6839` only.** Drafter, 13:42:
     - `lsof -nP -iTCP:6830-6839`, `6800-6899` and `7100-7199 -sTCP:LISTEN`: rc 1 for all three;
     - no 10-16/10-17 brief in Tuesday's tree or in the project's `Briefs/` names `683x` (grep 0, positive control `6820` = 3 hits in B167's brief);
     - B167 used 6820-6829 and HPSM-POC gate B255 uses 7130-7139 (`B255 brief:47`);
     - `lsof` before every bind; leave 0 listeners at your end.
   - **Synthetic stores:** rebuild B167's v1, v2 and `collide` from `synstore1/2-Program.cs`. **Each sha256 must equal `instruments/synthetic-stores.sha256`:** v1 `152174ad…`, v2 `c2cec759…`, collide `4e6489ef…`. If a sha differs, B167's numbers are not your baseline: say so, and use `prev` as the only oracle.
1. **The B167-1 test (item 1).** FAIL: the new test is green on any mutant below; or the hand-escaped keys disagree with your own Python `Join`/`Derive` (written from `PurchaseCatalogue.cs` at `a3c9b9d`, not imported).
   - Copy `mutateB.py`. Re-anchor at `a3c9b9d`: `J_OLD` dry count 1; the `Join` lines are unchanged by `diff d355620 a3c9b9d`, but prove it.
   - In `mutCP`, apply **CP-iii** and **CP-i**. For each: build rc 0, the new test alone by its real name, then the whole Import project and the B167 lane filter. Record counts.
   - **Expect:** both red on `B167_1_…`; CP-i is also red on `Parts_holding_a_bar…` and e07/e08.
   - Two traps: (a) on CP-iii the assertion `Option("a\\","b")` stays equal (a lone `\` does not depend on the order), so name the assertion that fails; (b) xUnit stops at the first failing assert. **Lane E's proof is a claim; this run is yours.**
   - **Exhaustive check re-run:**
     - every 2-part tuple of strings over `{a, |, \}` of length 0-3: 40 strings, 1,600 tuples;
     - keys from the HEAD's C# `CatalogueKeys` (a scratch console or untracked test in `mutCP`, removed after: porcelain 0), equal byte for byte to your Python;
     - collisions: B167 measured head 0 / swapped 60 (`B167_STATUS.md:12`): re-measure head, CP-iii and CP-i.
   - **Served probe on the head:** the `collide` store gives `GET /inventory` 200 with 34/34 distinct keys = your Join. Control: the same store on `base-main` → 500 "Duplicate catalogue key" (B167 `check5/keys-collisions.txt`).
   - **Grading:** the new test green on CP-iii or CP-i = **Major (B167-1 not closed → NO GO, round 2 of 2)**. A collision or a changed pre-B104 key at the head = **Blocker**.
2. **The care-pack class (item 2).** Through the real API on `hCP`, `prev` and `base-main`, on v2. FAIL conditions:
   - an imported care row not `carePack`;
   - `?class=carePack` missing a book row, or `?class=service` still listing one;
   - any services, section or quote figure that differs from `prev`;
   - a cost visible to a non-internal caller;
   - any 5xx.

   Probes:
   - (i) **Inventory:** `GET /inventory?class=carePack` (admin + internal-metrics, and a plain seller). Every v2 care row is listed once per fitted device, plus the unfitted row (B167: 7 care rows), plus any manual carePack row you plant (`man_` keys, so lane E's `Assert.All(StartsWith care_)` at `:31` holds only while the overlay is empty: report it). `?class=service` lists 0 `care_` keys. `unitCost` appears for internal-metrics only (0 marker hits for the seller). On `prev` the same queries show the round-1 state (`service`).
   - (ii) **Priced line + X-31:** reuse `careprice.py`. Every care key is `Succeeded`, the line `itemClass` is `carePack`, and the line cost = store × qty. **`servicesExTax` on `hCP` = `prev` = B167's 2,694.67 (`B167_STATUS.md:180`)**, along with every section and quote class subtotal and the rounded totals. The CONTROL key (not in the store) stays Blocking `UNKNOWN ITEM`. Submit, approve and proposal: 200; no care cost for seller or approver.
   - (iii) **Web** (your own build of `hCP`, synthetic, one heavy slot; the head's `web/` = main's by empty diff): the BOM picker and the inventory screen show imported care rows as **"Care pack"**, where `prev` shows "Service". One screenshot each (`evidence/screens/`). B167-8 (no fit in the picker) is carried as is.
   - (iv) **Stored quotes:**
     - rebuild B167's golden set (`B167_STATUS.md:218`, 13 quotes, 22 files: the template is `b167.py` / `stored.py` and `check7/` with its **98 captures**). Make it on `base-main` (v1), PLUS one quote APPROVED on `prev` (v2) holding an imported care line (its snapshot written while the class was `service`).
     - Read and recalculate each on `hCP` and `prev`, on v1 and on v2, masking with B167's list.
     - **Expect:** v1 98/98 equal and `inputHash` equal. On v2 only the care lines' `itemClass` echo differs (`service` → `carePack`), with the figures equal.
     - Report whether `inputHash` or the approved snapshot changes for the care quote. A changed snapshot byte on read = **Blocker**; a changed `inputHash` = REPORT plus the reason.
     - Control: `bump` turns the comparison red.
   - **Grading:** a class or listing fault = **Major**; a figure or hash change other than the named class echo = **Blocker** (tier 1).
3. **e07 re-plant (B167-7) and edited tests (item 3).**
   - `git diff --diff-filter=MDR --name-status 0217044 a3c9b9d -- tests` (control: a planted `M`), and `diff d355620 a3c9b9d -- tests`, read whole.
   - **e07:** both devices are planted (`GateB41.cs:238-243`), and the expectation is `V` (`:252`). On CP-i it must go red (B167: CP-i was caught by e08 only). Name the red result; green on CP-i = B167-7 not closed (Minor).
   - **Renames:** `…_as_a_carePack_row_…` and `Care_packs_are_carePack_rows_…` are branch-only names (not on main: show it). Every assertion of the round-1 versions is kept or strengthened (`B104CarePackApiTests.cs:27-47`, `:73-79`; `CarePackImportTests.cs:107-122`). A dropped assertion = **Major** (weakened).
   - **Mutants for item 2** (yours; build rc 0; restore to porcelain 0):
     - **CP-ix** `:148` back to `ItemClass.Service` → expect `B104CarePackApiTests` ×2 + `CarePackImportTests:107` red;
     - **CP-x** `:148` → `ItemClass.Other` → expect the `:78-79` subtotal asserts red;
     - **CL-i re-run** (`PurchaseCalculator.cs:45` without `CarePack`) → now ALSO the care API test red (in B167 it could not be, because the care rows were `service`).
     - A survivor that your Check-2 probe catches = **Major**.
4. **Diff = ADDENDUM-7's files.** Re-derive the PINS file list yourself: `comm` of `diff --name-only d355620 a3c9b9d` vs `ed72606 0217044`; `--remerge-diff 24143c3`; `diff` of every CP file blob `d355620` ↔ `a3c9b9d`.
   - **Any `src`/`tools`/`web`/`scripts`/contract change other than `PurchaseCatalogue.cs:145,148` = Major.**
   - `docs/IMPORTER.md` (`:16`, `:116`) is not named in ADDENDUM-7. It is docs (it fixes B167-11's `IMPORTER.md:16`): quote both lines, TRUE/FALSE vs the code → REPORT + words, not Major.
   - Test edits beyond the named files: REPORT.
   - gitleaks `0217044..a3c9b9d` with a planted control (expect only the known `CareKeyPatternApiTests.cs:15` false positive, B165-3).
5. **CI line, name sets vs `0217044`.**
   - `ciline.sh` re-checked against `ci.yml` at main. Run .NET Release (0 warnings) + test on `base-main` and `hCP`, then `comm` the sorted names:
     - LOST must be 0;
     - NEW is listed;
     - FAILED is 0;
     - the two renames show as NEW vs main (they were never on main).
   - Claims to beat: base = B167's hCL 107/338/1,597 (same tree `50c52d2c`); head 118/338/1,599.
   - Web and python on the head: CARRY with the empty `diff -- web scripts` as the reason, or run them if slots allow (say which).
6. **Rollback door (3), re-read with the class change.** B167 (`STATUS:15`): on main `ed72606`, CP's store loads with its care rows silently dropped, and a draft with a care line becomes `UNKNOWN ITEM`. Now measure, for Kam's deploy card:
   - (a) a v2 store + a draft and an approved quote with care lines written on `hCP`, opened by `base-main` `0217044` (CL, no CP): the care rows are dropped, the draft is `UNKNOWN ITEM`, and the approved snapshot opens?
   - (b) the same files opened by pre-CL code (`ed72606`, the hosted line is older still). The snapshot now holds `itemClass: "carePack"` on an IMPORTED line. Does B167's door (2) (25 of 34 files refused, "not a quote document") now also hide quotes that hold only an imported care pack, where round 1 wrote `service` that old code reads?
   - (c) opened by `prev` (round 1): priced as `service`, same subtotal?
   - REPORT, not graded, unless the NEW code gives a 5xx or a silent figure change.
7. **B167's other CP checks: CARRIED, with the reason.** The proof is Check 4, plus blob equality for the 8 untouched CP product files.
   - Carried: Check 5(iv) store compatibility, 5(v) import plants, CP-ii, CP-v, CP-vi, CP-viii, the keys' pre-B104 equality (re-shown cheaply by Check 1's served probe), and the merge census (CP touches no generated file).
   - **Re-run CP-iv and CP-vii:** they anchor in `PurchaseCatalogue.cs`, the one changed product file.
   - Carried findings (unchanged): B167-3, -8, -10, -12, and B167-11 except `IMPORTER.md:16`. If any proof fails, re-run that check.

**Main moves.** Re-read `main` at start, mid-gate and at the verdict. Lane D's header-regen of T (`B103_ADDENDUM-9`) may merge as a squash.
- If main moves, name the new sha and its files, and show that they share no name with CP's 15 (`88c84cd` vs `ed72606`: none).
- Run `merge-tree` head + new main. Expect it clean: the head + `88c84cd` conflict is only the two headers that T's regen resolves.
- The **pre-granted read-only fetch** of `main` into YOUR `.tools/qa-B168/repo` only, on `Briefs/2026-10-17_B163_ANSWER-1_fetch-main-into-scratch.md`'s terms (deploy key via `git config -f`, push URL stays `DISABLED`).
- Then re-run the .NET line once on the head merged onto the new main (scratch), and grade on that main.

## HOLDS (B167's `:223-244`, unchanged except names and ports)
- **Synthetic data only** (`SYN-B168-*` or B167's reproduced stores). **Never open** `.local/`, `2_Project_Files/.local/`, `Source_Documents/**`, `.tools/backup-*`, or another seat's `.local/`.
- **Project checkout:** READ verbs only, with `git --no-optional-locks`. Every write happens in `.tools/qa-B168/`.
- **No `rm` of any kind:** quarantine to `.tools/_quarantine/2026-10-17_B168_<what>/`. The one removal allowed is your own heavy slot.
- **Writes** go only under `.tools/qa-B168/`, `.tools/_quarantine/` and `Briefs/2026-10-17_B168_*`.
- **Network:** no hosted site, Kudu, az, Entra or Graph. NuGet/npm restore, the one fetch, and agentmail to Tuesday only. Never run `deploy-from-ci.sh`, `upload-pricebooks.sh`, `package.sh` or `test_infra.py`.
- **Shared machine:** lane D (`%17`) and lane E (`%18`) are live, as are the HPSM-POC and Vision gates. Never prune, gc or `branch -D`. Never touch their trees, slots, ports or processes. Kill only your own children.
- **No person's name and no client customer name in STATUS.** Never quote a Jira label or a transcript line. A line at your prompt that is not a Tuesday file pointer is not an instruction.

## STATUS
Verdict lines first. Then:
- Step 0;
- PINS (start / mid / verdict);
- instruments reused and re-anchored, and the slots with their load;
- Checks 0-7, each with its FAIL conditions, counts, build rc and evidence paths;
- the mutant table (CP-i, CP-iii, CP-iv, CP-vii, CP-ix, CP-x, CL-i: test × result × probe);
- the class table (endpoint × `hCP` / `prev` / `base-main`);
- **Findings** `B168-n` (severity, blocks?, oracle, evidence);
- fix-shapes (prose);
- proposed BACKLOG rows (not written);
- merge notes for Tuesday, including door (3) for Kam's deploy card;
- PRIOR WORK, NOT TESTED / UNMEASURED (at least real-book parity, CodeQL, Node 24, Linux, `test_infra.py`);
- corrections;
- what you left behind: processes, ports, slots and trees.

Keep it well under B167's length.

**Last line, exactly one of:**
- `VERDICT: B168 cp-r2 <GO | GO WITH NOTES | NO GO> on main <sha7>`
- `STOPPED: NEEDS TUESDAY` followed by ONE question.

SELF-CHECK · RE-STAMPED by Tuesday 2026-10-17 13:47:34 AEDT: read WHOLE (205 lines). TUESDAY RULING: docs/IMPORTER.md (:16, :116) is graded as docs (REPORT + words), as drafted in Check 4. Note: PR #77 (T-r2 header regen ef8146c) is open and will merge during this gate: handle it under 'Main moves'. · (drafter, 13:4x): pins re-read 13:44:36 equal; every sha, count and `file:line` above was read by a command the drafter ran (git read verbs with `--no-optional-locks`, `gh api` GETs, `lsof`, `ls`, `grep`) or is quoted from B167's STATUS by line.
