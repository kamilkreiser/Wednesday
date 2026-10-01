# Gateset 2026-10-01_gate52 — README for Wednesday

Written by the drafter on 2026-10-01. All times are UTC from `date -u`. Every figure below comes from the kit's own output file, which is named beside the figure.

## 0. Status and what remains

**KIT COMPLETE. It is READY to launch once the routing line (section 4) is added.**
- Launcher `--check`: rc 0 before AND after the controls (launcher_check_1.out, launcher_check_2.out).
- Launch-action `--dry-run`: rc 0 before the controls (repin_dryrun_0_before_controls.out, 09:50:26Z) and after (repin_dryrun_1.out, 10:13:51Z). The ONLY thing it reports is the missing routing line. It reads `BOTH INSTRUMENTS AGREE with the pins, 2 of 2`, and the census reads `0 touch a kit path or carry a kit key outside reported_overlaps`.
- Controls: normal **rc 0, 135/135 OK**; `--invert` **rc 1, 135/135 MISMATCH** (section 5).
- **Still Wednesday's: the routing line (section 4) and the launch (section 9).** A real launch also needs `WED_USAGE_STOP=100` (usage read 92% at 09:36Z; Kam's 17:40:22 grant is the authority).

Drafted **PINNED**. Wednesday named #1367 at head `ac3ceee7f440478431a317d3a31a42ab737f57c7` and #1368 at head `2a3dcd912a33b1ced6b6769368d87fce82ab64bc`, siblings on develop `0736d8b7849ef6c725c891d7254f2a3e21f42eb6`. The drafter re-read all of them:
- by `ls-remote` in the scratch clone (09:33:20Z, 09:38:00Z) and by the launch action's own `ls-remote` from the checkout (09:49:55Z): each branch == its `refs/pull/<n>/head`;
- by the PULLS API (gh_read_1.out, 09:42:07Z): both open, base develop @ 0736d8b7849e, `mergeable True` / `unstable`.

A new head on either PR means a RE-DRAFT (section 8).

**What the drafter did and did not do.**
- It launched nothing and added no routing line. It sent no mail, posted nothing, and changed no ticket or PR.
- It merged, committed and pushed nothing, and deleted nothing.
- It wrote only to this kit directory and to `g52_sp/` in its session scratchpad (`/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/79817561-2a8e-42cd-8745-2ef3ab0b0516/scratchpad/g52_sp/`). Every git write verb (fetch, merge-tree --write-tree, commit-tree, `apply --cached` under a temp index, hash-object, the control plants) ran in the scratch clone only.
- In `/Volumes/DevMASTER/!CODING/` it ran only `ls-remote` (directly once, then through the launcher and the launch action), a read-only `clone --shared` as a source, and file reads (gate51a's report, for its sha256).
- External reads were GitHub REST GETs only: both PRs, files, commits, the open-PR census, compare, and one GET of #1362. GH_TOKEN was read by name and never printed. Linear was not read.
- No install, suite, tsc, generator or vitest/jest run happened in drafting. Those are the gate's.

## 1. The PRs and the BLUF

| PR | ticket | role | tier | head | parent | ahead / behind | files | subject declared -> lands |
|---|---|---|---|---|---|---|---|---|
| #1367 | KS-1015 (Refs, narrows 1 of 28 pairs) | A, merged FIRST | T2 | `ac3ceee7f440478431a317d3a31a42ab737f57c7` | `0736d8b7849e` (= develop, #1365's merge) | 1 / 0 | 3, **+127/-2** | 75 -> 83 |
| #1368 | KS-1364 (Refs, 13 of 17 once landed) | B, merged SECOND | T2 | `2a3dcd912a33b1ced6b6769368d87fce82ab64bc` | `0736d8b7849e` | 1 / 0 | 5, **+98/-0** | 83 -> **91** |

- Pane: `QA/Secuura-batch1367` (**not routed**, see section 4). GO string (the GO mail's SUBJECT): `GO (Seat B 53rd): merge 1367 1368 on gate52`.
- Report dir: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-01-batch1367-g52/` (it does not exist yet).
- Verdict mail: FROM coagent@ TO wednesday-agent@, subject `[QA -> Wednesday] GATE52 #1367 #1368 (Seat B53 author and merger, round 52; T2 OpenAPI: the referral lookup 200 envelope, two more request bodies required, 3 new spec-rendering tests, the generated yaml)`.

**END_TREE_A `d1f03c3714541097834e37e2786527c2c1b71573`** (A alone on develop; `3 files changed, 127 insertions(+), 2 deletions(-)`).
**END_TREE_B `48f5f8afa6ef1f03f2d64e4afa24fd9f75213ad7`** (B merged after A; `7 files changed, 225 insertions(+), 2 deletions(-)`) **== the seat's PREDICTED tree.**
end_tree_crosscheck_1.out (rc 0, `ENDTREE AGREE`) reads each three ways:
- A: pin (F) merge-tree + commit-tree over develop; A's own tree (parent == develop, 0 behind); GitHub's `refs/pull/1367/merge` (`cfa97d5ee8c4`).
- B: pin (F) merge-tree of B onto A's simulated squash + commit-tree; `merge-tree --write-tree A B` (the seat's way); B's full diff applied `--cached` onto END_TREE_A under a temp index (independent of merge-tree).
- Controls that differ: develop's own tree `da849aa1d5c3` (= gate51a's END_TREE, as it should be); GitHub's `refs/pull/1368/merge` = B ALONE, tree `bf016acccf53`.

**Drafter predictions (the gate re-derives each one):**
- **pin_1.out `PASS`:** siblings (neither head an ancestor of the other, same merge-base); each alone merges clean; B onto A's squash merges with no conflict; 8 PR mode pins 100644 (the shared yaml pinned per PR) + control `scripts/run-migrations.sh` 100755; hook / preflight / generator / spec-examples / package.json identical in all 5 trees; **14 unchanged pins byte-equal in all 5 trees** (referrals.ts, referralService.ts, referral errorHandler.ts and index.ts, tenant-provisioning index.ts, originate verificationV2.ts and index.ts, shared responses.ts, the generator, package.json, and the root + 3 service lockfiles).
- **specdiff_1.out `SPECDIFF PASS: 0 FAIL of 17 checks`:** A changes only the GET {code} 200 (one removed `ReferralCodeSchema` line; yaml +30/-1 all inside `(/api/referrals/{code}, get, 200)`); B only INSERTS 2 `required: true,` (0 replacements; yaml +2/-0 directly under `requestBody:` at the tenants PATCH and v2 verify); the three goldens' sha256 == the READY's (45a105d11745, 495e6df123ed, cc6dc4880a66), each applies onto develop with 0 offsets and gives every non-yaml path blob-equal to its head (A 2/2, B 4/4; the yaml is the control that differs); YAML sha256: A `43c71cf6d5f213b6` 39889 lines 71 required, B `39f027b63d4aa804` 39862 / 73, END_TREE_B `e761a0b3c1eac6a5` 39891 / 73 (develop `7089242840e35885` 39860 / 71, the control); RED cells A1 A2 A3 (+3 controls) and TP1 VV1 (+6 controls); 0 runtime paths (control: develop~2..develop~1 names #1364's 2 audit paths).
- **handlers_1.out `HANDLERS PASS: 8 checks, 0 FAIL`.** Locks: root, referral, tenant-provisioning and originate all express 4.22.3 / body-parser 1.20.8 (express-validator 7.3.2 root + originate). Mounts: referral `index.ts:57`, tenant-provisioning `:19`, originate `:103`.
  - RL1 (#1367): handler `referrals.ts:95-120` writes 404 `:101`, 200 `:105`, `next(error)` `:118`; 200 top keys and the six `data` keys == the spec's; the yaml's two `required:` lists == the spec's non-optional keys; every status the handler writes is declared; the 404 body fits `ErrorResponseSchema` (responses.ts:45).
  - TP1 (#1368): `tenant-provisioning/src/index.ts:440`, parse `:442`, every schema field optional, the "No fields to update" 400 at `:455` -> REJECTS-EMPTY.
  - VV1 (#1368): `verificationV2.ts:427`, `validationResult` `:439`, every chain field optional, 4xx branches `:440` and `:452`; coalesce `:451` and destructure `:450` name all four aliases -> REJECTS-EMPTY.
  - **Control RG-CTL** (POST /api/referrals/generate, PR B's claim): `referrals.ts:49`, parse `:61`, 4 optional fields `:17-:20`, **NO 4xx branch after the parse** -> ACCEPTS-EMPTY, as expected.
- **keyscan_1.out `KEYSCAN PASS: 17 checks over 2 PRs, 0 FAIL (trailer control FIRED)`.** Each title/body/branch/commit carries only its own hyphenated key; no closing keyword; both commits' `%(trailers)` empty with 0 Co-Authored-By; `bf277eead268` reads a 53-byte trailer.
- **gh_read_1.out:** 21 other open PRs, **0** touch a kit path or carry KS-1015 / KS-1364. `reported_overlaps` is EMPTY. #1360 (PeterObeden) reported as client-human. **#1362 is no longer open: CLOSED UNMERGED at 2026-10-01T08:39:15Z** (one PULLS GET, recorded in kit.json client_human_note).

## 2. What the gate must rule

The prompt names each item, and the launcher refuses a prompt that is missing any of the 31 keywords.
1. **ENVELOPE-MATCHES-HANDLER, ERROR-CODES-MATCH** (#1367, file:line, every listed status accounted for).
2. **HANDLER-REJECTS-ABSENT, BODY-PARSER-DEFAULT, ALIASES-COVERED** (#1368; body-parser's `req.body || {}` from the installed package).
3. **GENERATE-NOT-REQUIRED** (PR B's claim, verified from source; also requirement 2's control).
4. **GOLDENS-BYTE-EQUAL, GENERATOR-REPRODUCES, CHECK-OPENAPI-RC, YAML-SHAS.**
5. **RED-FIRST, CONTROLS-GREEN, SUITES-BASE-HEAD, TSC-NO-REGRESSION** (referral + tenant-provisioning vitest, originate JEST).
6. **SEQUENCE-A-THEN-B, CLEAN-MERGE, END-TREE, BOTH-MERGEABLE, MODES.**
7. **KEYSCAN-OWN-KEY, NO-CLOSING-KEYWORD, NO-TRAILER, SUBJECT-LANDS-AT, SUBJECT-TRUE-OF-DIFF, PR-BODY-CLAIMS, NO-RUNTIME-CHANGE.**
8. **COLLISION-CENSUS.** 9. **NOT-TESTED-LIST.** Plus TIERING, DISK-ENOSPC, REPORT-HASH-LAST.

**Doubts the drafter found (all are in the prompt for the GATE to rule; the drafter rules none):**
- (a) **The GET {code} 404 is described "Code not found / inactive"**, but the handler's 404 condition is `if (!referralCode)` (`referrals.ts:100`) and `dbGetCodeByString` (`referralService.ts:222`) does not filter `is_active`. An inactive code looks like it answers 200 with `isActive: false`. Pre-existing text, but #1367's claim is "the spec follows the runtime".
- (b) `dbGetCodeByString` swallows a DB error and `isDbAvailable() === false` as `null`, so a database outage answers **404**, not the 500/503 the spec lists. Runtime information, not this PR's change.
- (c) The spec lists 400, 429, 500, 502, 503 for the GET; the handler writes none of them itself (401 is `jwtAuthenticate` at `/api`, `index.ts:81`; others via `next(error)` / limiter / gateway). The gate says who writes each.
- (d) `customLabel` is `r.custom_label || undefined` (`referralService.ts:116`), so it is ABSENT, never `null`, when unset: consistent with `z.string().optional()`. The gate confirms. `.passthrough()` on `data`: does it render `additionalProperties` in the yaml? (The drafter sees none.)
- (e) The envelope is hand-rolled instead of the shared `successEnvelope()` (`responses.ts:119`). Polish at most.
- (f) **gate51a's TENANT control read ACCEPTS at the validator** on the very handler #1368 now marks required (gate51a N-1365-3 caught it). This kit's instrument reads every 4xx branch after the parse; HD3g plants a branch into `/generate` to prove the instrument sees one.
- (g) VV1 is **express-validator, not zod**; a type error 400s at `:440`, an empty body at `:452`. gate51a's N-1365-4 cited `routes/documents.ts:1490` for the aliases: the gate says which handler serves `/api/v2/verification/verify` (the drafter reads the mount at `originate/src/index.ts:277`).
- (h) Spec path `/api/platform/tenants/{id}` vs handler `/api/tenants/:id`: the prefix mapping is the gateway's; NOT TESTED unless the gate reads it.
- (i) The seat's absent-body probes ran on a **replica at body-parser 1.20.6**; every lock resolves **1.20.8**. The prompt requires the installed source line.
- (j) **#1368's subject lands at 91**, one under the 92 limit.
- (k) Neither commit message carries a `Refs` line (the merger composes the squash body). Information.
- (l) **NOT the gate's (Wednesday rules them):** KS-1015 moved itself to In Progress at 09:08:04Z; `mergeable_state: unstable` on both (cause unreadable, 403); the usage quota (92%, Kam's grant).

## 3. Pins and what the gate owes
- `fill_gate52.py` FILLS the prompt `2026-10-01_secuura-batch1367.prompt.txt`, the launcher `launch_qa_secuura_batch1367.sh` and COMMISSION.md (fill_1.out rc 0). It refuses unless:
  - gate51a's report still hashes to `24981bf5bc5f…`;
  - END_TREE_B == kit.json `end_tree_after_b_predicted` (the seat's prediction);
  - `end_tree_crosscheck_1.out` carries both END trees and ends `ENDTREE AGREE`;
  - specdiff / handlers / keyscan / gh_read each end in their PASS / OK line, at this develop and these heads.
- The launcher's exits are re-keyed from gate51a's: **7** also requires the sibling order; **26** also requires `ONE AT A TIME, A FIRST`; **31** requires develop, END_TREE_A and END_TREE_B in full; **32** requires both tickets in prompt AND capture; **36** is the SPEC-TRUTH rule (a spec that disagrees with its handler is a Major; the generate control; "never from memory"); **38** requires the usage figure and Kam's grant.
- Named exceptions: X1 (`npm ci` registry reads), X5 (≤2 read-only Linear queries: KS-1015, KS-1364), X6 (read-only GitHub GETs).
- `reported_overlaps` and `sequenced_out_of_kit` are EMPTY. An overlap at launch refuses with rc 15.

## 4. Routing line — NOT added
Back up the file first (`inbox_routing.conf.pre-<date>`). Then add this ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`:
```
QA/Secuura-batch1367|coagent@agentmail.to|yes
```
Until that line is present, step 0 of the launch action refuses with rc 1 (control R1). R8 shows a routed temp file passing step 0 and stopping after 3b.

## 5. Controls: `controls_gate52.sh <scratchpad> [--invert]`
- **135 controls, one unedited script**: `controls_gate52.sh`, sha256 `a04c2812b67e…`. controls_sha.txt shows it identical before and after both runs.
  - Normal run (controls_1.out): **rc 0, `135 controls, OK 135, MISMATCH 0 | ssh-denied retries 0`**.
  - `--invert` run (controls_2.out): **rc 1, `135 controls, OK 0, MISMATCH 135 | ssh-denied retries 0`** (run 1 09:53:35Z–10:03Z, run 2 10:03:32Z–10:13:16Z).
- Both runs wrote to the scratchpad first and were then copied in, byte-checked with `cmp`.
- Side effects, kept: R1 and R8 wrote `launch_<HHMMSS>.*` step outputs here; the PN simulations wrote `pins_gate52.SIM-*.json`.
- **Coverage:**
  - **PN0–PN8** (pin): the real heads as a simulation (END_TREE_B, shortstat, the second instrument, 9 mode pins, a handler blob BYTE-EQUAL); `--develop` refused without `--simulate`; a runtime handler file (`verificationV2.ts`) edited -> (K); a develop move on the yaml -> (C); B's yaml recorded 100755 -> MODE MISMATCH; **an unrelated develop move -> END_TREE_B != the seat's prediction (refused) while (C) reads NONE**; a path outside the prefixes -> (B); **B stacked ON A -> (B2) not siblings**; **B editing A's yaml line -> (F) does NOT merge cleanly after A**.
  - **SD0–SD7** (specdiff): the real heads 17/17 (goldens 4/4, A's GET-200-only, the union sha); a second key in A's GET block -> S2; a replacement in B's tenants spec -> S2; an extra yaml line -> S3; one byte of the tenants golden -> S4 3 of 4; develop as A's head -> S1; develop's tree as END_B -> S8; a handler file in A -> S7.
  - **HD0–HD6** (handlers): the real heads 8/8 with RG-CTL ACCEPTS and the lock versions; the tenants guard removed -> TP1 ACCEPTS FAIL; `documentHash` dropped from the coalesce -> VV1 ALIASES MISSING; a `/generate` field made required -> the CONTROL fails; **a 400 branch planted after `/generate`'s parse -> the CONTROL fails** (the gate51a lesson); an extra 200 data key -> RL1 FAIL; a 409 write -> undeclared status; the spec's `customLabel` made required -> yaml required lists disagree.
  - **KS0–KS8** (keyscan, including NO-TRAILER on a planted Co-Authored-By and the trailer control pointed at a commit without one -> DID NOT FIRE); **ET0** (endtree).
  - **L0–L23b + LK1–LK31** (launcher): every exit, including 7 (sibling order), 26 (A FIRST), 31 (END_TREE_A), 36 (generate control), 38 (Kam's grant), and the filename rule. L9 is the real non-TTY path.
  - **R0–R8** (launch action): census; routing refusal; an extra kit path -> OVERLAP #1360; a title key -> OVERLAP; sequenced right / wrong head; DISJOINT; wrong head rc 11; old develop rc 10; a bad scratchpad rc 9; routed stop-after-3b.
  - **PNZ / KJZ / PRZ**: the pins, kit.json and the filled prompt are unchanged.
- **Not controlled:** on a real launch, the usage gate (12), `cockpit.sh add` (14) and the override refusal (16); a `mergeable=False` refusal; a real re-pin across a develop move (only the dry run's rc 10 and PN5's refusal are controlled). gh_read and fill are exercised by their real runs, not by plants.

## 6. Could not measure (the drafter)
- No install, suite, tsc, generator, vitest, jest or red-first run happened. Requirements 4 (b)-(c) and 5 are entirely the gate's, and the seat's figures are claims until the gate runs them.
- The handler and envelope readings are static. No request was sent. The gateway's path mapping was not read.
- Linear was not read.

## 7. Files
- **Config:** kit.json (written by the drafter's `g52_sp/mkkit.py` in its scratchpad) · COMMISSION.TEMPLATE.md -> COMMISSION.md · README.md (this file) · READY_1367_1368_mail.md (Wednesday's; unchanged).
- **Pin:** pin_gate52.py -> pin_1.out, pins_gate52.json (+ `pins_gate52.SIM-*.json`) · endtree_gate52.py -> end_tree_crosscheck_1.out.
- **Instruments:** specdiff_gate52.py -> specdiff_1.out; handlers_gate52.py -> handlers_1.out; gh_read_gate52.py -> gh_read_1.out / gh_read_1.json / gh_body_1367.md / gh_body_1368.md; keyscan_gate52.py -> keyscan_1.out; each with its .err and .rc.
- **Prompt and launcher:** prompt_gate52.TEMPLATE.txt + launcher_gate52.TEMPLATE.sh.txt, filled by fill_gate52.py (fill_1.out) -> `2026-10-01_secuura-batch1367.prompt.txt`, `launch_qa_secuura_batch1367.sh` and COMMISSION.md. Checks: launcher_check_1.out (before the controls) and launcher_check_2.out (after).
- **Launch:** repin_and_launch_gate52.sh -> repin_dryrun_0_before_controls.out, repin_dryrun_1.out.
- **Controls:** controls_gate52.sh -> controls_1.out / controls_2.out (+ .err, .rc), controls_sha.txt.
- **Provenance:** gh_read and repin are NEW COPIES of gate51a's, re-keyed by quoted python; pin, specdiff, handlers, keyscan, endtree, fill, the templates and the controls are new for two sibling PRs; gate51a's kit is untouched.

## 8. Re-draft recipe (a new head on either PR, or ANY develop move)
**Any develop move changes END_TREE_B, so pin (F) refuses until kit.json `end_tree_after_b_predicted` is re-set** (the launch action's step 3b therefore refuses rc 10 on a move; control PN5). A move is a re-draft, with a new prediction from the seat or the drafter.
1. Keep kit.json as `kit.json.pinned-ac3ceee7-2a3dcd91`.
2. Set `prs.<n>.head` (and, on a move, `end_tree_after_b_predicted` and the `yaml_sha256_prefix` / `yaml_lines` values).
3. Run, in order: `pin_gate52.py <sp>` -> `gh_read_gate52.py` -> `specdiff_gate52.py <sp>` -> `handlers_gate52.py <sp>` -> `keyscan_gate52.py <sp>` -> `endtree_gate52.py <sp>`.
4. Run `fill_gate52.py`.
5. Run the controls both ways. Update the head-specific patterns first: PN0k's blob, the S4 / S8 figures, and the handler line numbers if the handlers moved.
6. Run `--check`, then the dry run.

## 9. The ONE launch command (run it after the routing line in section 4 is added)
```
WED_USAGE_STOP=100 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-01_gate52/repin_and_launch_gate52.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-01_gate52/launch_qa_secuura_batch1367.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/79817561-2a8e-42cd-8745-2ef3ab0b0516/scratchpad
```
- `WED_USAGE_STOP=100` is there only on Kam's 17:40:22 grant (until the account switch, Fri 2026-10-02 morning). Drop it once usage is under 90% or the grant has expired.
- Append `--dry-run` for a dry run.
- Argument 2 may be ANY existing Claude session scratchpad. If `g52_sp/clone` is absent there, pin_gate52.py rebuilds it from the checkout on a re-pin.
- After the gate's verdict and a GO, the squash key sets are exactly {KS-1015} for #1367 and {KS-1364} for #1368, merged A first.
