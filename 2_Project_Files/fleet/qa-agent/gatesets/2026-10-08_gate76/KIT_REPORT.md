# gate76 KIT REPORT — drafter to Wednesday

- **Rows:** #1427 KS-1274 (Seat R 18th), head `2b6da5f561b05a820bbe1ab5e891bff9f4f531c8`, END_TREE `9b6c3dfef865dfc35b05d4da8fcad7e24249fbb1`, 6 paths +94/-8. #1428 KS-593 (Seat G 4th), head `64eafead891e81f5adb4e46aaa94ff6a6ace1998`, END_TREE `7f6e6fe0ca15702cab1b5e1a0d37ba7ff8f665b5`, 9 paths +421/-4. Each has ONE parent, which IS develop `0a6177ea5482227e83d5045b68b8577a56326ffc`. T2 each, each with its own verdict.
- **Drafted:** 2026-10-08 18:27–19:10 AEDT (07:27Z–08:10Z). Built and dry-run only. **Not launched.** Nothing was merged, pushed, commented, mailed, ticketed or routed.
- **Writes:** only this folder, `briefs_staged/2026-10-08_mergeseat_gate76_DRAFT.md`, and the drafter's scratchpad (`…/scratchpad/g76/`: the clone, worktrees wtA / wtB / wtFinal, SIM commits). Nothing was written under `!CODING`. GitHub: GETs only.
- **Stopped early on Wednesday's instruction (rotation).** See §6, NOT DONE.

## 0. BLUF
1. **Launch-ready at the defaults.** Dry run rc 0 at 08:02:10Z–08:03:13Z, with: 12 pins EQUAL, 45 by-name keywords, launcher `--check` rc 0, and 15/15 launcher and repin refusal arms MATCH. The routing line is NOT added: `ROUTING_LINE.txt` has 0 copies in `inbox_routing.conf` (gate75's line reads 1 as the control).
2. **Refs are unmoved** at 07:28:27Z, 08:02:16Z and 08:08:50Z: develop `0a6177ea5482`, and each pull/head == its branch == its head. Calibration: develop's tree `5f456a0128fe` IS gate75's predicted squash tree.
3. **Landing (default order #1428 → #1427, Q-ORDER76):**
   - Step 1, #1428: NO merge-in. Its tree `7f6e6fe0ca15` == END_TREE.
   - Step 2, #1427: a docs-only KEEP-BOTH merge-in. Predicted tree `57c9b5eaec95ddc86a7d139f9f2d957015a3fd97`. Composed blobs: flow `b2bd07dbae40…`, cheat `f4503e99d43e…` (`composed_2026-10-08/`).
   - **Merge-in sizing:** conflicts on exactly the 2 docs. Flow gets #1428's 57-line block followed by #1427's 44-line block; cheat gets 28 lines then 27.
   - **Push delta:** OURS..M = 9 paths (+421/-4, 7 of them under `Blockchain/Dev`, so the hook runs the full preflight). DEV..M = 6 paths (+94/-8).
   - **Reverse order:** step 2 tree `0f08bed03b8000c4f9f3c5208c423b586ab8be0e`.
   - The guard read 12/0 at every step. The one-pass rebuild == the chain.
   - **Union hazard re-measured on THIS pair:** `merge-file --union` drops a `</td></tr></table>` from FLOW (table/td/tr each go +1 unbalanced), and the guard still reads 12/0.
4. **The seats' red/green, re-run by the drafter at the heads:**
   - **#1427:** suites 6/0, 5/0, 5/0. With the job reverted to base: rc 1, 4/1, ONLY the KS-1274 cell fails and the CONTROL stays ok. The restore is proved.
   - **#1427 stub arms, head vs base:**
     - T1 `{}` and T3 `null` are changed by the fix (CLEAN → FAILED).
     - T4, T6 and T7 read FAILED on both.
     - T0 and T2 read CLEAN on both.
     - **T5 `{"Results":null}` reads CLEAN at the head** (Q-NULLRESULTS, Minor).
   - **#1428:** at the head, 5/5, 5/5, 6/6 and hermetic 10/10.
     - With the routes reverted: 2f/3p, 2f/13p and 3f/3p, all == G 4th's. The share figure is share + hermetic, TWO files.
     - Whole originate suite: 96 suites / 1093 tests / 0 failed.
5. **Preflight by hand on the SIM of the FINAL tree `57c9b5eaec95`:**
   - `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.`
   - `shell suites: 71 passed, 0 failed, 0 skipped (of 71)`, wall-clock 356 s.
   - Legs 3 4 8 SKIPPED (not a pass). 670 `^ok` lines, 0 `^FAIL` lines, 0 `VERDICT: MISMATCH` lines (G 4th's push log had 1: unresolved, for the gate).
6. **Actions (07:54Z–07:57Z):** both rows hold all three classes against base (== develop).
   - Security Scanning: the KS-1148 class, 12 of the last 12 repo-wide runs failed.
   - CI shell step: 65/6 at develop and at both heads, the same 6 FAILED. #1427's failed-scan suite reads 5/0 in CI (develop 3/0).
7. **Docs:** both rows are insertion-only before `</body>`, keyed, balanced on every tag, and only their own key is hyphenated. #1428's cheat block is not a section card (polish).
8. **KS-593 residue:**
   - c1 P8 pins `close KS-593` (negated) in #1428's PUSHED message. The live body has 0.
   - R 17th's builder REFUSES that text in a body (probe P6).
   - The merge seat reads KS-593 before and after the merge, and STOPS if it walked to Done (Q-CLOSE593).
9. **Builder vs each REAL head shape (the item owed from gate75):**
   - Both heads have 0 trailers (1 B vs the 55 B control).
   - R 17th's builder lands either row FIRST: rc 0.
   - Its `merge-in` mode is UNREACHABLE, rc 1 both ways. R 15th's by-SHA read makes the commit its own parent.
   - The ordinal is hard-coded to R 17th. The predecessor tuple lacks R 17th, R 18th and G 4th.
   - **The second row needs a new builder copy (Q-BUILDER76).**
10. **Usage:** 91% (07:27Z) → 93% (dry run) → 94% (08:08Z, rc 3 at the default 90). The repin now EXPORTS `WED_USAGE_STOP=100` after reading the new-account grant (card `secuura-raise-backlog-at-99pct-1008`, clause GATE), so `cockpit.sh add` sees it. That fixes gate75's first-run refusal.

## 1. What was re-keyed from gate75 (and carried from gate73)

| gate75 / gate73 token | gate76 |
|---|---|
| `lib_gate75.py` + `lib_gate73.py` readers | `lib_gate76.py`: G75_/G73_ → G76_, two rows, no default row. `resolvable()` now uses `cat-file -e` (R 18th: `rev-parse --verify` is not a presence check). **The cheat reader reads one heading at a time:** composee5's lazy reader straddles develop's `— KS-1445 (with KS-1367)` and reads 18 keys for 19 headings. |
| `composee5_copy.py` (gate73) | carried byte-identical, `f9ab42d9…` |
| `c1_pin_gate75.py` | `c1_pin_gate76.py`: two rows; P14 GUARD-ONLY → per-row SCOPE + disjointness; P15 the leg-14 baseline → per-row fix invariants (#1428 checks AUTHZ line order); P8 pins #1428's closing residue; P5 trailer pin 55 → 1 B. Self-test 12/12. |
| `c3_guard_gate75.py` | replaced by `c3_redgreen_gate76.py` (`trivy` / `originate`; same bind / saved-bytes / restore-proof shape). Self-test 7/7. |
| `c3_preflight_gate75.py` | `c3_preflight_gate76.py`: `baseline` mode dropped; runs on wtFinal. Self-test 6/6. |
| `c4_docs_gate75.py` (one insertion in a line) | `c4_docs_gate76.py` from gate73's chain composer: 2 rows, 2 orders, gate75 lineage calibration, every-tag attribute-aware balance. Self-test 15/15. |
| `gh_gate75.py` | `gh_gate76.py`: two rows; T5 per-row NOT RUN; new T6 attribution; leg-14 log reader → `suite_tallies` (header and tally sit on different lines; the first version read a false zero); census keys. Self-test 18/18. |
| `fixture_body_1426` | `fixture_body_1427_at_draft.md` (4,598 B, `6a220f76f08f2190`), `fixture_body_1428_at_draft.md` (4,943 B, `b882e9d4a486ed49`) |
| prompt / launcher / repin, `--head-1426`, `GO (Seat R 17th): merge 1426 on gate75` | `--head-1427 --head-1428`; head file P×2 / B / D / S / C / **O / T**; TWO GO strings `GO (Seat R 20th): merge 1428 / 1427 on gate76`; merge lane = any lane whose letter matches the ordinal, never an author; `rm -rf` removed from the repin |
| usage authority `…use-to-100pct…` / card `…89pct…` | `2026-10-08_new-account-push-merge-test-as-much-as-possible.md` / `secuura-raise-backlog-at-99pct-1008`, EXPORTED |
| `QA/Secuura-gate75`, report `2026-10-08-gate75`, verdict subject | `QA/Secuura-gate76`, `2026-10-08-gate76`, `[QA -> Wednesday] GATE76 (T2 x2): #1427 … + #1428 …` |
| merge_inputs (1426) | `merge_inputs/1427.squash_body.DRAFT.txt` (4,531 B, `e56d4333…`, the 🤖 line removed), `1428.squash_body.DRAFT.txt` (5,029 B, `85bf1948…`, +336 → +421 and the authz sentence corrected), the two subject files, `MERGE_INPUTS.json` |

## 2. Open questions for Wednesday (full text: `RULINGS_wednesday.md`; every one has a default the kit already assumes)

- **Q-SEAT76:** rec/default **Seat R 20th**, merge-first, after R 19th wraps. The alternatives are R 19th re-briefed, or G 5th.
- **Q-ORDER76:** rec/default **#1428 → #1427**.
- **Q-CLOSE593:** rec/default: the squash uses the GO-named body only. Read KS-593 before and after. If it walked: STOP and mail; never revert.
- **Q-SUBJ76:** rec/default `KS-1274: job 04 fails a scan when trivy reports neither Results nor ArtifactName` (80) and the #1428 title (82).
- **Q-ATTR76:** rec/default: strip the 🤖 line from the #1427 squash body.
- **Q-CLAIMS593:** rec/default: correct the two #1428 sentences in the squash body. No PR PATCH.
- **Q-BUILDER76:** rec/default: a new copy with a required `RA20_MERGE_IN_HEAD`, the ordinal re-keyed, the tuple extended, plus 9 refusal arms and 2 positive controls.
- **Q-MERGEIN76:** rec/default: R 12th's mergein + pushra1_ff copies. Adopt #1427's branch name for the one push. Full preflight runs in-hook.
- **Q-NULLRESULTS:** rec/default: Minor named limitation. Rides with KS-1274's owed live run.
- **Q-LIMIT593:** rec/default: negative `limit` is out of #1428's claim. Name it in Wednesday's KS-593 comment batch.
- **Q-RACE76:** rec/default: do not hold this batch for other PRs. Re-predict before each step.
- **Q-PREFLIGHT76:** rec/default: one preflight, on wtFinal.
- **Q-LIVE76:** rec/default: neither ticket moves to Done.
- **Q-USAGE76:** as wired.
- **Per Wednesday (08:1xZ): #1429 (KS-1449, E 11th) and #1430 (KS-1328, F 5th) are raised on develop `0a6177ea5482` and go to the NEXT gate, not this one.** Both edit both docs (census, 08:02Z: 26 open PRs).
  - Whichever lands first voids this kit's predicted trees. The repin refuses rc 10 and re-predicts.

## 3. Findings by row (drafter; the gate re-measures)

**#1427**
- **Minor:** T5 `{"Results":null}` reads CLEAN.
- **Info:** the fix also turns `null` stdout into a FAILED scan, a behaviour change beyond the bare-`{}` case.
- **Polish:**
  - the title and commit subject de-hyphenate the own key (the builder refuses that subject; staged subject fixed);
  - the body's 🤖 line;
  - R 18th's "4,567 B" is a CHARACTER count (4,598 bytes).

**#1428**
- **Minor:**
  - `+336/-4` vs the measured +421/-4;
  - the authz-order sentence overclaims for adminConfig and signatories (all routes keep router-level auth first: no authorisation decision moves).
- **Info:**
  - /rights-holders: the guard sits before the `!tenantId` return, so a tenant-less caller with offset=-1 gets 400, not `200 []`;
  - negative `limit` is unguarded (READ ONLY; outside the claim);
  - `isUUID()` may refuse hyphenless or braced uuids that Postgres accepted (READ ONLY).
- **Pre-existing, named in the body:** signatories GET does no org-membership check within a tenant.
- **Polish:** the share ratio is a two-file sum; the cheat block has no section card.

**Batch**
- The R 17th builder's merge-in mode is dead (Q-BUILDER76).
- `VERDICT: MISMATCH` lines: 0 in the drafter's final-tree preflight vs 1 in G 4th's push log.

## 4. Drafter defects, caught and fixed (disclosed)

1. **The cheat reader straddled KS-1445**, so c4 refused at the first self-test. Fixed with a per-heading reader, and kit.json was regenerated: `cheat_seq_base` went from 18 to 19 keys.
2. **c1 P15 counted a COMMENT line quoting `echo '{}'`.** Fixed to code lines only.
3. **c3 originate's share red was judged on ONE file.** G 4th's ratio spans two (share + hermetic). Fixed. Run-1 and run-2 outputs are kept as `*.run{1,2}_instrument_defect.out`.
4. **`jest` without `--verbose` printed no failing names.** Fixed.
5. **gh's CI tally regex read a false zero** (the tally and the suite name are on different lines). Fixed (`suite_tallies`, with a self-test arm). The first runs are kept as `*.run1_extractor_blind.out`.
6. **The repin carried an `rm -rf` of a fresh path.** Removed (quarantine rule), and the kit was re-pinned.
7. **Missing import of `cheat_keys_pinned` in the c4 self-test.** Fixed.

## 5. What I could not measure, and why
- **Live trivy scan and live originate against PostgreSQL:** no daemon, binary or stack.
- **Platform suites and preflight legs 3 4 8:** stack down.
- **bash ≥ 4.1:** the host has 3.2.57.
- **eslint and prettier:** not run.
- **Linear state of KS-593 / KS-1274** (incl. the KS-593 link kind): no Linear read.
- **R 19th's handover and tools:** R 19th was live at draft. The merge brief carries placeholders that Wednesday fills at send.
- **`cockpit.sh add` with the exported stop:** read, not driven (a dry run cannot add a pane).
- **The `RULED BY KAM` card list:** Wednesday regenerates it at send (64 undelivered cards at the drafter's read).

## 6. NOT DONE (stopped on Wednesday's instruction)
- No final re-run of the full dry run after the last kit edit. `finalize_kit.py` re-pinned after the `rm` removal, and the launcher arm run at 08:03:57Z passed 15/15 against those pins (l0 CONTROL rc 0).
- No `orders`-mode run. The reverse order was predicted with `chain`.
- No `qm` exercise on a SIM merge-in M. M `92e4585277322a986c400430c9c4157af02f8a21` exists only in the drafter's clone, used by the builder probe.
- The `format`-gate mode was not run on either row's paths.
- **KIT_REPORT §7 (launch) and §8 (RUNG 5), in short:**
  1. Rule or accept the defaults.
  2. Add `ROUTING_LINE.txt` to `inbox_routing.conf`.
  3. Run `script -q /dev/null bash …/repin_and_launch_gate76.sh --head-1427 2b6da5f561b05a820bbe1ab5e891bff9f4f531c8 --head-1428 64eafead891e81f5adb4e46aaa94ff6a6ace1998 --develop 0a6177ea5482227e83d5045b68b8577a56326ffc`.
  4. Expect ~35–45 min of wall clock: two S-1 installs, ~7 min of preflight, and the Actions waits.
