# Gateset 2026-10-06_gate66 — README for Wednesday

Drafted 2026-10-06 by one Wednesday drafting subagent. Every figure names the kit file it came from. Every builder statement is a CLAIM the gate re-measures; the prompt says so.

## 0. What this gate is, and its status

**gate66 is a T1 gate over ONE Secuura/Blockchain PR: #1385, KS-938, "MFA disable and revert NULL the TOTP seed and the backup codes".** T1 because it is the auth surface: second-factor credential material that "MFA disabled" used to leave in the row. **It is the FIRST gate of KS-938's product change** (the PR was ungated at `79c87b8aaa48`; E 5th brief Q-GATE5).
- Head `f6b49d68209d4fa368335d3c2fa3e4928c3efaa1` = Seat E 5th's docs-only merge-in. END_TREE `04fa3e0d1b48`. Parents `[79c87b8aaa48, d784b613c81e]` (`c1_pr1385_devc510_ex1.out`, rc 0, 11/11, origin read).
- `d784..head` is exactly 5 paths, all 100644: the new `ks938-mfa-disable-nulls-seed-and-backup-codes.test.ts` (+237), `routes/mfa.ts` (+14/-4), `routes/users.ts` (+7/-1), the flow doc (+61), the cheat sheet (+27).
- Author: Seat E 5th, wrapping after the READY. Merger: **Seat E 6th** (not yet launched).
- **GO string:** `GO (Seat E 6th): merge 1385 on gate66`. The launcher refuses a prompt naming `GO (Seat E 5th)`, `GO (Seat E 4th)` or `GO (Seat E 3rd)` (exit 8).
- **NO GO string:** `NO GO (gate66): 1385 at f6b49d68209d — <N-1385-n: the blocker, one line>`.
- **develop MOVED before the gate.** The head is current with d784. origin develop is now `c5101866ef5488297c76f198257685eb1f8d69d2` = Peter's merge of #1390 (KS-1408 schemathesis pin bump). It was already there in the READY's own 13:14:28Z read, and the drafter's ls-remote agrees. `d784..c510` is 37 paths: **both platform-k docs reformatted** (flow 2410 -> 2992 lines, cheat 3968 -> 4415) and 35 systemTest paths. That is 0 `Blockchain/` paths, 0 hook paths and 0 skill paths (c1 P10 / P11). **So the merge needs a SECOND docs merge-in.**
- **develop MOVED AGAIN while drafting.** The launcher's `--check` at 13:40Z (UTC clock) read `f0179806494e42df254b9580168be3cd4a35f307` = Peter's merge of #1391. `c5101866..f0179806` is ONE path, `5_Project_History/history.md`, so both docs are byte-identical to c5101866's. The kit predicts on both develops (section 1).

**Status: KIT COMPLETE, NOT LAUNCHED.** The dry run (section 5) returned rc 0 on develop f0179806.
- Every checker's self-test fires on its planted defects and passes the clean case (section 3).
- Wednesday owns the routing line (section 4), the DIVERGENCE ruling (D2) and the launch (section 7).

**What the drafter did:**
- **Writes:** only inside this directory (`_scratch/clone` is a `clone --shared --no-checkout` of the checkout, with origin re-pointed to GitHub and develop c5101866 fetched BY SHA using the checkout's own `core.sshCommand`; SIM commits and predicted trees exist as objects there only; no ref written) and the session scratchpad `…/scratchpad/gate66drafter/`.
- **In `!CODING`:** read verbs only (`ls-remote`, `config --get`, `cat-file`, `rev-parse`), plus the clone source. No worktree, no npm, no vitest, no tsc: **C3 was NOT run by the drafter** (judge + tamper landing only).
- **Network:** GitHub REST GETs (pulls/1385, files, Actions runs at both heads, open-PR census), `ls-remote`, and one SHA fetch into the kit's own clone. No Linear read, no mail, no launch, no routing edit, no `rm`.

## 1. Drafter predictions at f6b49d68209d (the gate re-derives every one)

| check | file | result |
|---|---|---|
| C1 pin | `c1_pr1385_devc510_ex1.out` (rc 0, 11/11, origin read, develop c5101866) | P1 pull/head == branch == head; origin develop c5101866 · P2 parents [79c87, d784], 79c87's parent 46c3e20cfbd2, merge-base(head, develop) = d784 · P3 5 paths exact, both ways + 3-dot · P4 END_TREE (controls differ) · P5 trailers 1 byte at the head AND 79c87 (control bf277eead268 = 55) · P6 0 Co-Authored-By (control 1) · P7 head subject == the merge-in's (**123 chars**; D9), 79c87 subject == the PR title · P8 one `Refs KS-938`, only KS-938, 0 closing · P9 100644 · P10 pre-push / preflight / SKILL.md identical at head, d784 and develop · P11 advance 37 paths, code / hook disjoint. Control: head = 79c87 FAILS P2 P3 P4 P7 (`c1_selftest_ex1.out`, 5/5) |
| C2 product | `c2_pr1385_ex2.out` (rc 0, 5/5) | W1 the hunks exactly: mfa.ts 4 `undefined` out, 4 `null` in; users.ts `mfaSecret: undefined` out, `mfaSecret: null` + `mfaBackupCodes: null` in (+10 / +5 comment lines) · W2 S1 / S2 / S3 null both at the head; the base shape is `undefined` at S1 / S2 and the key ABSENT at S3 · W3 **3** `updateUser*(` objects with `mfaEnabled: false` (mfa.ts:239, mfa.ts:380, users.ts:1121), all null both; 0 `mfa*: undefined` left (base control 5) · W4 users.ts `mfaSecret: undefined,` **:1123 at d784 AND at c5101866** (users.ts blob 68f402bb56f0 identical); hunk `@@ -1120,7 +1120,13 @@` (`-U0`: `@@ -1123 +1123,7 @@`) · W5 userRepo.ts blob 9060b308e6d6 at head == d784 == develop; undefined-skip and string-only encryption guard present |
| C2 W6 attacker facts (INFO) | `c2_pr1385_ex2.out` | /me/mfa/verify refuses with no seed (a disabled account cannot re-arm) · BOTH enable paths OVERWRITE `mfaBackupCodes` (users.ts verify; mfa.ts setup/verify writes pending.secret + hashedBackupCodes) · RESIDUE: users.ts disable verifies the TOTP only `if (user.mfaSecret && …)` · the login gate refuses `mfaEnabled` with no seed · /me/mfa/enable writes a PENDING seed while `mfaEnabled` stays false, and no disable clears it (D7) · S1 revert is the non-throwing `updateUser` (D6) · users.ts /me/mfa/verify stores generated codes with no hash call in the handler (pre-existing; not KS-938) |
| C2 widen (drafter grep) | session read | No raw-SQL writer sets `mfa_enabled` false in any service except demo seed data. `userErasedSubscriber.ts:70-71` nulls both. The `platform_admins` MFA path was NOT read for a disable route |
| C3 | `c3_selftest_ex1.out` (rc 0, 15/15) | **NOT RUN by the drafter.** Judge arms: assertion red, load failure, skipped, failed-without-message, missing cell, no JSON. T1-T7 anchors each occur exactly once in the real head blob and land. Forbidden-root refusal rc 2 (`c3_refusal_forbidden_ex1`) |
| C4 h2 proof | `c4_h2proof_ex2.out` (rc 0, 4/4) | **flow: d784 16 h2 (0 split; old same-line regex 16) → c5101866 16 h2, 5 SPLIT across lines; old same-line regex reads 11 numbered, old same-line key finder 4 of 8 keyed.** Cheat: 6 / 6 at both, 0 split (#1390 split only the flow's h2s; it re-indented the cheat's KS-1005 h2). Planted `<h2>\n      99. … (KS-99999)\n    </h2>`: tolerant HIT, old regex MISS, on both docs |
| C4 docs | `c4_docs_ex1.out` (rc 0, 7/7) | D1 skill · D2 head minus the KS-938 BLOCK == d784 byte for byte, both docs · D3 flow `20. … (KS-938)` after 19. (KS-1005), ascending [1..14, 18, 19, 20] · D4 cheat KS-938 LAST after KS-1005 · D5 test file, `3 failed \| 2 passed (5)`, `5 passed (5)`, 845 in both blocks · INFO D6 the flow block cites users.ts `ea9f8da97a04` (46c3's), not d784's `68f402bb56f0` |
| C4 second merge-in | `c4_predict_*_ex1.out`, `c4_mergetree_devc510_ex3.out` | develop d784 → **04fa3e0d1b48 == END_TREE** (positive control) · **c5101866 KEY-ANCHORED → `36c1a881db305d034404a15fa4246cf6563c5199`** (`--order num` and `--order tail` give the same tree on this develop: KS-1005 is the last section in both docs) · **git merge-tree rc 1, tree-with-markers `edf424d164e8`: FLOW auto-merged == the key blob `2d1cd366a8cb`; CHEAT CONFLICTED** · hand resolution → `4f1b4b999fab`, one `</div>` short · **DIVERGENCE** (section 6) · **f0179806 (current develop): KEY-ANCHORED `fb6cb2c6992cd48815b8f23a8519e9910bc27e63`** (same two doc blobs), merge-tree rc 1 `73f98d063ed2` with the same cheat conflict, hand resolution `0bb86333ba28`: DIVERGENCE (`c4_predict_devf017_key_ex1`, `c4_mergetree_devf017_ex1`; h2proof on f0179806 4/4, c1 on f0179806 11/11) |
| Q-M | `c4_selftest_ex2.out` (rc 0, **30/30**), `c4_qm_goodsim_ex2.out` (rc 0, 8/8), `c4_qm_refuse_absent_develop_ex1.out` (rc 2) | GOOD SIM passes M1-M8 · WRONG-ORDER SIM (cheat KS-938 above KS-1005) fails M1 + M8 · HAND-RESOLUTION SIM fails M1 + M8 · CONFLICT-MARKERS SIM fails M1 + M8 · Co-Authored-By SIM fails exactly [M4] · Signed-off-by SIM fails exactly [M4] · single parent M2 · extra path M1 M3 · two commits M2 M7 · **absent develop refuses `develop unresolvable` BY NAME with 0 checks run**, on a fabricated sha AND on the REAL c5101866 against the shared checkout (where it is genuinely absent) · absent M refuses by name |
| Actions | `gh_actions_ex2.out` (rc 0) | prev 79c87 and head both FAILING `PR Security Gates (KS-168)`, `Security Scanning`, `pr`. **`pr` has CONCLUDED failure at the head** (E 5th saw in_progress). NEW-FAILING NONE. Planted-name control reported. **`gh_actions_ex1.out` (rc 1) is a real instrument event: the head's run list came back EMPTY once (6 runs on the next read).** The tool now re-polls and refuses to read an empty list as green |
| PR / mergeable | `gh_api_ex1.out`, `gh_prtext_ex1.out` (rc 0, 5/5) | open, not merged, **mergeable false / `dirty`**: consistent with merge-tree's cheat CONFLICT against c5101866, not (only) a stale cache · body sha `64d208b5da2c4bfa`, 7,613 chars (7,666 bytes) == the READY · `Refs KS-938` once + URL, 0 closing, only KS-938, title == subject, 0 Co-Authored-By |
| census | `gh_census_ex1.out` (rc 0); dry run | 24 others: 0 OVERLAP, 2 DOCS (#1383 KS-1401, #1393 KS-1278); control fires. At the dry run: 25 others, 0 OVERLAP, **3 DOCS (+ #1394 KS-723)** |

## 1b. The product checks this gate commissions (T1; all are in `prompt_gate66.txt`)

1. **KS-938's change, by site** (C2 W1 / W2). Read in `services/auth/src/routes/mfa.ts` and `routes/users.ts`. MFA disable nulls the TOTP seed AND the backup codes on BOTH disable routes: `POST /api/auth/mfa/disable` (S2) and `POST /api/users/me/mfa/disable` (S3). It does the same at the setup-verify compensating revert (S1). At S3 the `mfaBackupCodes` key was absent at the base and is added.
2. **Red-first at the base** (C3 redfirst). The base overlay is mfa.ts + users.ts at **d784**, not 46c3, because develop moved users.ts. The claim to meet: R1 R2 R3 red BY ASSERTION, C1 C2 green, 5 executed, then 5/5 at the head. A load failure is not a red.
3. **Tampers per conjunct** (C3 tamper, T1-T7). The kit wrote them, because the builder published no table. There is one for each column at each site, plus S3's key-removed and key-undefined shapes. Each must redden exactly its site cell, and a green tamper is a named BLIND SPOT.
4. **The users.ts hunk at its moved site** (C2 W4). It is `:1123` at d784. Re-read it at the develop the gate reads; the drafter found users.ts blob `68f402bb56f0` identical at d784, c5101866 and f0179806.
5. **Cross-route consistency** (C2 W3, widened by the gate). Every `updateUser*(` object with `mfaEnabled: false` must null both columns (the drafter found 3 of 3). The gate then widens it: any other writer of `mfa_*` in any service (raw SQL, `platform_admins`, the erasure subscriber).
6. **Attacker view** (C3b). Can a disabled-then-re-enabled account reuse old backup codes? Can it re-arm an old seed? Can a partial failure leave a seed (one UPDATE statement or not; S1's non-throwing revert)? The login gate with no seed. Existing rows. The pending seed. The TOTP-only-if-seed residue. Each is READ by line and PROBED where a read does not settle it.
7. **GitHub Actions compared against the PR's PREVIOUS head `79c87b8aaa48`** (`gh_gate66.py actions`, E 5th's method). Pre-existing failures are separated from new ones, never compared against develop's tip, with a planted-name control. `pr` is re-polled; the drafter read it CONCLUDED failure at both heads, so NEW is NONE.
8. **`mergeable_state` re-polled** (`gh_gate66.py api`). The drafter read `dirty` / false, which is consistent with the cheat conflict against current develop.
9. **NOT TESTED list, explicit, written first.** At least these:
   - live sweep
   - real PostgreSQL (NULL into TEXT[])
   - preflight legs 3, 4, 8
   - existing-row backfill
   - the four platform suites
   - the `platform_admins` MFA path unless read
   - other seats' worktrees
   - anything skipped for budget

## 2. Doubts for the gate (the drafter rules none; the prompt carries D1-D12)

- **D1 Tier.** T1 (auth surface).
- **D2 THE SECOND MERGE-IN DIVERGENCE: Wednesday rules. This is the most important item.**
  - On the CURRENT develop f0179806 every reading below repeats with the same doc blobs. Key tree `fb6cb2c6992c…`, merge-tree `73f98d063ed2`, hand resolution `0bb86333ba28`.
  - **Key-anchored (tonight's rule, gate60 / gate65 shape), on c5101866:** `36c1a881db305d034404a15fa4246cf6563c5199`. It is c5101866's tree, with the 3 code paths at the head's blobs and each doc = c5101866's doc with the head's KS-938 block inserted after the KS-1005 section. The flow-numbering reading (20 after 19) gives the same tree. Per-doc h2 key order:
    - flow: `KS-666 KS-1015 KS-1404 KS-1333 KS-1345 KS-1388 KS-1210 KS-1005 KS-938`, numbers 1-14, 18, 19, 20
    - cheat: `KS-1404 KS-1333 KS-1345 KS-1388 KS-1210 KS-1005 KS-938`
    - both docs: div balance +0, 0 markers
  - **`git merge-tree --write-tree --name-only f6b49d68209d c5101866`:** rc 1, tree-with-markers `edf424d164e8826bb8457951286183f07480a7b1`.
    - The flow AUTO-MERGES to the same blob as the key tree (`2d1cd366a8cb`).
    - The **cheat CONFLICTS**: #1390 reformatted KS-1005's section exactly where the head appended KS-938. Its key order is the same, but it carries 3 conflict markers and div balance +1.
  - **Hand resolution** (THEIRS hunk + OURS from the KS-938 section on, keeping git's trailing `</div>` context): `4f1b4b999fabc8ae82ec89f7d636e03edb968a0b`. The key order is the same, but the div balance is +1: KS-938 ends up nested inside KS-1005's "Gotcha" note. **It is the natural thing a seat would do by hand, and it is NOT the key tree.**
  - The kit's qm makes the key tree the M1 authority, and M8 fails the other two. If Wednesday rules otherwise, pass `--predicted <the ruled tree>` and say so in the GO.
- **D3 Mixed formatting.** The KS-938 block lands in the OLD hand formatting inside a doc #1390 reformatted (flow `<h2>` split, tables expanded). Is that acceptable? If Seat E 6th reformats the block, M1's tree changes and the kit's prediction is void.
- **D4 Tamper blind spots.** No tamper table was published. T1-T7 are the kit's, one conjunct each. If a cell asserts column NAMES but not bound VALUES, or S1's cell does not separate the seed from the codes, a tamper stays green.
- **D5 Existing rows not backfilled** (the body says so). A T1 auth fix that leaves every previously-disabled account holding its seed and codes: NOT COVERED, follow-up, or blocker?
- **D6** S1's revert uses the non-throwing `updateUser`. A failed revert leaves the account enabled WITH its seed, and it is only logged.
- **D7** `/me/mfa/enable` writes a pending seed while `mfaEnabled` stays false. No disable clears it, because disable refuses when `!mfaEnabled`.
- **D8** PREFLIGHT-INCOMPLETE 12/15 (legs 3, 4, 8) on both pushes of a T1 change.
- **D9** The head subject is the merge-in's (123 chars). The landing subject must be declared, TRUE, and <= 92.
- **D10** The flow block cites the 46c3 users.ts blob `ea9f8da97a04`, while d784's is `68f402bb56f0`. The site line moved :1116 → :1123.
- **D11** The PR body's "Merge ordering — must NOT land before #1382" section is stale (#1382 landed).
- **D12** #1383 (KS-1401, F lane; Q-E5-F4LOCK) and #1394 (KS-723, new at the dry run) are open on both docs. If either lands first, develop moves again and the kit's predictions are void: re-predict.

## 3. Kit files

| file | role | self-test | live run |
|---|---|---|---|
| `kit.json` | pins, blobs, sites, tampers, claims, predictions | — | — |
| `lib_gate66.py` | read-verb `git`; write verbs only outside `!CODING`; GH GET by token name | — | — |
| `c1_pin_gate66.py` | C1 P1-P11 | `c1_selftest_ex1.out` rc 0, **5/5** (positive, must-not-fire, 79c87 control, 2 by-name refusals) | `c1_pr1385_devc510_ex1` rc 0 |
| `c2_product_gate66.py` | C2 W1-W5 + W6 attacker INFO | `c2_selftest_ex2.out` rc 0, **9/9** | `c2_pr1385_ex2` rc 0 |
| `c3_tests_gate66.py` | C3 redfirst / tamper (T1-T7) / suite / tsc, vitest JSON judge | `c3_selftest_ex1.out` rc 0, **15/15** · refusal `c3_refusal_forbidden_ex1` rc 2 | **NOT RUN** (the gate's) |
| `c4_docs_gate66.py` | newline-tolerant h2 reader; h2proof; docs D1-D6; KEY-ANCHORED predict (key / num / tail); mergetree (AGREE / DIVERGENCE + hand-resolution reading); qm M1-M8 | `c4_selftest_ex2.out` rc 0, **30/30**; `c4_selftest_ex3.out` rc 0, 29/29 (after someone fetched c5101866 into the shared checkout, the genuinely-absent arm is NOTE'd as unavailable) | h2proof ex2, docs ex1, predict ex1 ×4, mergetree ex3, qm goodsim ex2, qm refuse ex1 |
| `gh_gate66.py` | api / actions / census / prtext | `gh_selftest_ex2.out` rc 0, **14/14** | api ex1, actions ex2 (ex1 = the empty read), census ex1, prtext ex1 |
| `launch_qa_secuura_ks938_1385.sh` | the launcher (static prompt) | `launcher_arm_noreadme_ex1` rc 8 (README missing → refused) | `launcher_check_ex1` / `ex2` rc 0 |
| `repin_and_launch_gate66.sh` | the launch action (copied from gate65's) | `repin_arms_ex1.out` **5/5** | `dry_console_ex1.out` rc 0 (`dry_134317.*`) |
| `prompt_gate66.txt` | the gate's prompt | — | — |
| `api/` | pull 1385 JSON, files, body, Actions runs at both heads (as read at drafting) | — | — |
| `RESULT.txt` | the drafter's summary | — | — |

`_quarantine/` keeps superseded runs and is never deleted:
- c4 ex1 / ex2: before the hand-resolution reading and the div-balance check.
- `c4_qm_goodsim_ex1`: **M7 false-failed on an abbreviated M**. That was a real defect, fixed: qm now resolves M and D to 40-hex.
- c2 ex1: W3 counted creation defaults as clears.
- `gh_selftest_ex1`: before prtext.

## 4. Routing line — NOT added
Back up the file first. Then add ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`:
```
QA/Secuura-ks938-1385|coagent@agentmail.to|yes
```
Until it is present, step 0 of the real launch refuses rc 1. The dry run reports it instead.

## 5. Launcher check and dry run (drafter, against live origin; nothing launched)
- `launcher_check_ex2.out` (rc 0) is `launch_qa_secuura_ks938_1385.sh --check`. All guards pass: 8 kit files named, 37 by-name keywords, the GO (Seat E 6th) present, no forbidden-seat GO. It recorded origin develop f0179806494e, and prompt sha256/16 `9efd6ec6f3e3a229`.
- `dry_console_ex1.out` (rc 0, `dry_134317.*`) is `repin_and_launch_gate66.sh 1385 f6b49d68… --dry-run --repin-develop f0179806494e…`:
  - routing line missing, reported (0 exact; 155 agentmail lines)
  - API: open, merged False, mergeable False / `dirty`, body sha `64d208b5da2c4bfa`
  - census: 25 others, 0 OVERLAP, 3 DOCS; control fires
  - head agreement on API, pull/head and branch
  - develop MOVED d784 → f0179806, 38 paths, KITHIT none (read from local objects: someone has since fetched f0179806 into the shared checkout)
  - re-pin recorded, plus the kit prediction fb6cb2c6992c and the DIVERGENCE note
  - c1 rc 0, 10/10
  - launcher `--check` rc 0
  - `DRY RUN COMPLETE 13:44:00Z`
- `repin_arms_ex1.out` holds **5/5** refusal arms:
  - wrong PR → rc 9
  - wrong head → rc 11
  - short sha → rc 9
  - no `--repin-develop` → rc 10
  - **the instructed `--repin-develop c5101866…` → rc 10 "stale re-pin"**, because origin develop is f0179806

## 6. The second merge-in: KEY-ANCHORED, NEWLINE-TOLERANT
- Seat E 6th merges develop IN to `f6b49d68209d`: a merge commit M with parents `[f6b49d68209d, D]`. Never a rebase, never a force push.
- **Sections are found by their h2 KS key, read with the newline-tolerant reader.** Never by a same-line regex, never by `<div class="section">`, never by tail position. On c5101866 the old same-line readers see 11 of 16 numbered flow h2s and 4 of 8 keyed ones.
- **Target tree (kit):** D's tree, with the 3 code paths at the head's blobs. Each doc is D's doc with the head's KS-938 block (the gap after KS-1005's section + the KS-938 section) inserted immediately after D's KS-1005 section.
  - On c5101866 the target is `36c1a881db305d034404a15fa4246cf6563c5199`; on f0179806 it is `fb6cb2c6992cd48815b8f23a8519e9910bc27e63`.
  - git CONFLICTS on the cheat, so the seat must reproduce the tree by hand. It is NOT git's auto-merge, and it is NOT the obvious hand resolution (D2).
- **For any later develop D:**
  - fetch D by SHA into your OWN clone
  - run `G66_SCRATCH=<scratch> python3 …/c4_docs_gate66.py mergetree --repo <clone> --develop-after <D>` (it prints both trees, the per-doc key order and AGREE / DIVERGENCE)
  - run `… predict --repo <clone> --develop-after <D>`
  - both refuse `develop unresolvable` BY NAME (rc 2) until D is fetched
- The GO covers M only if `c4_docs_gate66.py qm --repo <clone> --merge-in-head M --develop-after D` passes M1-M8 (`--predicted <tree>` only for a Wednesday-ruled tree). Anything else re-gates.
- `repin_and_launch_gate66.sh` pins the READY's develop d784 and refuses rc 10 on today's develop unless given `--repin-develop <origin develop>`. It is a hard rc 10, not re-pinnable, if:
  - the advance touches a code or hook path, or
  - develop does not descend from d784.

## 7. How Wednesday launches it (after section 4's routing line and the D2 ruling)

Pane `QA/Secuura-ks938-1385`. Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-06-ks938-1385-g66/`. Verdict subject `[QA -> Wednesday] GATE66 #1385 (T1 KS-938: MFA disable nulls the seed and backup codes; author Seat E 5th wrapping, merger Seat E 6th)`.

**Dry run** (no usage gate, no cockpit):
```
script -q /dev/null bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-06_gate66/repin_and_launch_gate66.sh 1385 f6b49d68209d4fa368335d3c2fa3e4928c3efaa1 --dry-run --repin-develop <origin develop 40-hex>
```
**THE launch command as commissioned (NOT run by the drafter):**
```
script -q /dev/null bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-06_gate66/repin_and_launch_gate66.sh 1385 f6b49d68209d4fa368335d3c2fa3e4928c3efaa1 --repin-develop c5101866ef5488297c76f198257685eb1f8d69d2
```
**As of 13:44Z this refuses rc 10 "stale re-pin"** (`repin_arms_ex1.out`, arm 5): origin develop is f0179806494e. The command that passes the dry run on today's develop (not run for real) is:
```
script -q /dev/null bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-06_gate66/repin_and_launch_gate66.sh 1385 f6b49d68209d4fa368335d3c2fa3e4928c3efaa1 --repin-develop f0179806494e42df254b9580168be3cd4a35f307
```
If develop has moved again, both refuse rc 10 and print `re-run with: --repin-develop <new sha>`. Read the printed advance first. The kit predicts only on c5101866 and f0179806 (`kit.json` `merge_in_predicted`); on any other develop the gate predicts.

Exit codes are gate65's:
- 1 routing
- 9 input
- 2 ls-remote
- 3 API, or a blind census control
- 15 OVERLAP
- 11 head moved (RE-DRAFT)
- 10 develop moved / not re-pinnable
- 13 C1, or the launcher's `--check`
- 16 override
- 12 usage gate
- 14 cockpit

Add `WED_USAGE_STOP=…` only with Kam's recorded authority.

**Rung 5 (verify at rung 5 or 6, never below).** Read the pane and find content only THIS gate would produce:
- KS-938 / #1385
- `…/2026-10-06_gate66/README.md` or `QA_AGENT_CHARTER.md` read
- head `f6b49d68209d`
- a `*_gate66.py --selftest`

Rung 6 is `NOT-TESTED.written-first.md` in the report dir.

## 8. Re-draft recipe (the head moved, or develop is not re-pinnable)
1. Re-measure `kit.json`: `head`, `end_tree`, `head_parents`, `files`, `head_blobs`, `base`, `base_blobs`, `sites`, the tamper `from` strings, `claims`, `merge_in_predicted`.
2. Edit the head in `prompt_gate66.txt` and `launch_qa_secuura_ks938_1385.sh`. Both are static.
3. Re-run every `--selftest`, then c1, c2, c4 h2proof + docs + predict + mergetree, gh api / actions / prtext / census, and a `--dry-run`.
4. A merge-in head on top of f6b49d68209d is NOT a re-draft. It is judged by `c4 qm`.

## 9. NOT COVERED by this kit (the gate's, or nobody's)
- **C3 was not run by the drafter**: no worktree, no npm, no vitest, no tsc. Red-first, the seven tampers, the suite figure and tsc are unmeasured here. The claim figures (3 failed | 2 passed → 5 passed; 79 / 845 / 0) are E 3rd's at 79c87 on base 46c3, not at f6b49 / d784.
- No live sweep, no real PostgreSQL. A NULL bound into `mfa_backup_codes TEXT[]` is READ, not executed.
- No attacker PROBE. The C3b items are READ ONLY at the drafter's anchors (c2 W6).
- No Linear read (KS-938). No read of the `platform_admins` MFA routes for a fourth clearing site.
- No independent second implementation of the predictor. The flow agrees with `git merge-tree`. The cheat has no git answer (conflict); its checks are key order, section byte-identity, 0 markers and div balance.
- No predict / qm on a REAL second merge-in M: none exists yet. Q-M is proven on SIM merge-ins only.
- The repin script's rc 3 / 13 / 14 / 12 / 15 paths were not driven, and no real launch was made.
- The four platform suites (Schemathesis, Akto, Playwright, k6): no scan surface.
