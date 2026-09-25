# Gateset 2026-09-26_gate25T2 — README for Wednesday

The drafter launched nothing, sent no mail, tapped no pane and committed nothing. It wrote under
`/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4f2cdc54-acc3-4f26-989e-2c407e677824/scratchpad/gate25/` (plus `…/scratchpad/g25_sp/` and
`…/scratchpad/g25_controls_*`). **One stray file outside it:** `/tmp/claude-501-wl.sh` (451 bytes, a drafter slip) — reported, not deleted.

This kit is the second of TWO. **gate25T2 = three TIER-2 PRs + one TIER-3 PR** (Seats L7, wrapped; B 29th). The sibling `gate25T1` holds the
four tier-1 PRs (#1267, #1269, #1272, #1274).

| PR | ticket | head | tier: why (from the diff) |
|---|---|---|---|
| #1268 | KS-1318 + KS-1142 + KS-1316 | `a8e0fca70ed41ef061cc99a325b610d27f08c7fb` | **T2**: 2 files under packages/shared/src/__tests__ only. It changes a CHECKER (the ks781 walk), so THE READER RULE applies. |
| #1270 | KS-1275 | `448b8b7fdd87a145acc895c4138811f34aa53c59` | **T3**: 20 changed lines, all comments (port), in 2 originate product files. An already-gated follow-up of #1252. |
| #1271 | KS-1164 | `c9ea1dc1705f10f4b40ccc786604da6768a2c2fb` | **T2**: systemTest/performance tooling plus its tests. No product code. |
| #1273 | KS-1321 | `b800791a3295f048b40f920435b080a270c65106` | **T2**: 1 originate test file. It changes a CHECKER (the description verb matcher), so THE READER RULE applies. |

- Routing: `QA/Secuura-batch1268`.
- GO string: `GO: merge #1268, #1270, #1271, #1273 batch` (or the subset).
- #1268 and #1271 go to a MERGE SEAT, because L7 has wrapped. #1270 and #1273 go to B 29th if it is LIVE at the GO (it opened #1279 at 20:32Z), otherwise to the merge seat.

## 1. BLUF
- **Kit: READY to launch** once you add the routing line (§4).
  - `--check` rc 0.
  - Controls: 116/116 OK normally, and 116/116 MISMATCH under `--invert`.
- **Pinned over develop `df5e9f5da6d23411e7b38a79a58aa20c04b6afe2`.**
  - Seat M1's five are all merged, and the tree equals the expected `6942101caa7b…` (measured).
  - **No overlap:** the four PRs' paths are disjoint from each other, from gate25T1 and from M1's #1262-#1266 (measured). There is no declared overlap in this kit.
- **Findings the drafter READ (the gate rules on them):**
  - **MAGIC-WORD-CLOSES (#1271).** The body says "`#1200` closed KS-1164's original class". Linear therefore linked KS-1164 to #1271 as **`closes`**; every other PR in both kits reads `contributes`. A squash with that body would close KS-1164 on merge.
  - **TITLE-OVER-92 (#1271).** The title is 93 chars, so the squash subject is 101 chars, over MG-11's limit. The merge addendum must shorten it.
  - **NO-REFS-LINE (#1268).** The body has no `Refs` line and names a foreign key, KS-1143.
  - **KS1329-TSC (#1268).** L7's own KS-1329 says #1268 brings three TS errors into test files that no CI leg type-checks.
- **Predictions (the gate measures them):**
  - **BACKTICK-SPAN (#1273).** A LIVE probe of the function, extracted from the head blob, over-reports on back-quoted spans that merely END in a verb (`` `subversion` ``) and on closing/opening back-quote pairing.
    - This is the safe direction, on shapes that are not named, so it is graded by REACH.
    - Every shape the PR names reads correctly.
  - **#1268 walk.** The drafter could not predict whether these count as "invoked": function DECLARATIONS, `.call`/`.bind()()` and `fn?.()` (COMMISSION.md table).
- **Fleet STOP (READ, bounded region):**
  - #1268, #1270 and #1273: 28/0 · 6/0 · 49/0 · 60 of 60, and "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed."
  - #1271: NOT APPLICABLE. It was a systemTest/ push, and its push log is 11 lines.
  - After the merge the count is unchanged: 28/0 · 6/0 · 49/0 · 60 of 60. That count was measured on develop d7cdecf1 by Seat L8.

## 2. Pins: predict_2.out (rc 0, 2026-09-25T20:43Z)
- **Develop:** `df5e9f5da6d2…`, 10 ahead of the PRs' parent `4db87c3e4b98`.
- **Shape:** each PR is ONE commit on the parent. The API and ls-remote agree on every head.
- **Merged trees:**

| PR | merged tree |
|---|---|
| #1268 | `91726010bc61…` |
| #1270 | `777d0499843c…` |
| #1271 | `bf0fb8d437b3…` |
| #1273 | `7b6ef67f5e48…` |

- **Checks:** checks (1)-(3) hold, and every merged blob equals its head blob.
- **END_TREE `8624ef60b994062290ff3772f568dddc63889b19`:** 9 files, +390/-42, identical in all 24 orders.
- **Simulations:**
  - Foreign edits of #1270's and #1273's own files: REFUSED.
  - Pre-M1 develop `d7cdecf1`: PASS, with the same END_TREE_AFTER_M1.
- **Coupling by content (not by path), carried into the prompt:**
  - #1271 edits `k6_docker.ts`. M1's #1265 has just pinned that file's redaction with four rows.
  - #1270's comments sit in `documents.ts`. M1's #1262 cell drives that file.

## 3. What the gate owes (prompt `2026-09-26_secuura-batch1268-t2.prompt.txt`, ~32 KB)
- **THE READER RULE for #1268 and #1273.** It runs through the real walk and the real function; a wrong reading on a REAL or NAMED shape = NO GO.
  - #1268 also gets the call-shape table.
  - K1b is a source-text read: the gate plants CORPUS in three disguises (commented out, in a comment, split across lines) and grades how the check reads each.
- **Red proofs:**
  - #1268: ARM A/B, the K1b arms, and W9 alone red under develop's walk.
  - #1271: S1/S2 and L1/L3 red with the guard removed.
  - #1273: the three arms.
- **#1270 TIER-3 PROOF (EMIT-PROOF):**
  - `transpileModule` with removeComments; parent == head.
  - A DIFFERENT control at identical emit size.
  - A `-U0` line check with its own control.
  - The originate suite equal.
  - COMMENT-CLAIMS: both pointer targets exist (read).
- **Rulings owed:**
  - MAGIC-WORD-CLOSES and TITLE-OVER-92: the gate names the squash body and subject the merger must use.
  - SYMLINK-SAMEPATH, graded by reach.
  - KS1329-TSC.
- **Suites:** re-measured on the launch develop. For example, systemTest/performance should read 1108 → 1114 now that M1's #1265 is in.
- **Rules:**
  - No Docker, no port.
  - Legs 3/4/8 NOT run.
  - Load: one re-run allowed.
  - Holds.
  - Addendum with 4 lines.
  - Subject: `[QA -> Wednesday] TIER-2 GATE batch #1268 #1270 #1271 #1273 (Seats L7 B29, round 25)`.

## 4. Routing line to add (the drafter did NOT write it)
`QA/Secuura-batch1268|coagent@agentmail.to|yes` → `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (absent at drafting, measured).

## 5. The ONE launch command
```
/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4f2cdc54-acc3-4f26-989e-2c407e677824/scratchpad/gate25/gate25T2/repin_and_launch_gate25T2.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4f2cdc54-acc3-4f26-989e-2c407e677824/scratchpad/gate25/gate25T2/launch_qa_secuura_batch1268-t2.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4f2cdc54-acc3-4f26-989e-2c407e677824/scratchpad
```
- **If develop moves (for example, gate25T1's GO lands first), step 3b re-pins in the same action.**
  - Proven by control RD: the real re-pin from a `d7cdecf1` pin, then `--check` rc 0.
  - A move onto any own path, or a pairwise overlap, refuses with rc 10 (control RE).
- **If you copy the kit into `gatesets/`,** pass the copied paths. Step 0b re-fills there.

## 6. Decisions for Wednesday
1. **#1271's Linear link.** Decide whether its delivered scope closes KS-1164. The gate will rule on it. If the answer is no, the squash body must avoid the closing word, and it may be worth unlinking in Linear.
2. **B 29th's merge authority for #1270 and #1273:** it merges its own PRs if LIVE at the GO, otherwise the merge seat does. Name which in the GO.
3. **#1270 as tier 3.** It is comment-only, in product files. You could rule it needs no gate at all (the tier-3 lesson says the builder's own proof stands). The kit gives it the cheap emit proof instead.
4. **Merge order between the kits does not matter.** They are disjoint.
5. **Open round-25 PRs in neither kit:** #1275, #1276, #1277, #1278 and #1279 (gh_read_1.out). They are not in this batch.
6. **READY mails NOT read.** No message ids exist in the seat records. The capture uses PR bodies, commit messages and the L7 and L8 handovers, each with its sha256.

## 7. Controls: `controls_gate25T2.sh <scratchpad> [--invert]`
- **controls_2.out:** 116 controls, **OK 116, MISMATCH 0** (rc 0).
- **controls_3.out (`--invert`):** **OK 0, MISMATCH 116** (rc 1 by design).
- **The mutations are independent.**
  - A wrong head changes one hex digit. It is never a superset of the real head (the gate24T2d H20 lesson).
  - doctor() refuses any replacement that still contains the original.
  - The launcher's head guard is whole-field.
- **Superseded runs, kept:**
  - controls_0_superseded_E2.out: 115/116. The E2 control's phrase also sat inside kit rule 48, so rule 48 fired first (exit 48 where 25 was wanted). The guard held, but the attribution was wrong. Rule 48's phrase was re-cut, and the run above is clean.
  - controls_0_aborted_inv.out: an aborted run.
- **Not controlled:** exit 16, repin steps 4-6, `mergeable=False`.

## 8. Files
- **Kit:** kit.json · COMMISSION.md (the LEGITIMATE SHAPES tables) · PROPOSED_inbox_routing_line.txt
- **Pins:** predict_gate25.py, predict_1/2.out, predict_sim_{foreign1270,foreign1273,m1base}.out, pins_gate25T2.json (+ .SIM-*)
- **GitHub reads:** gh_read_gate25.py → gh_read_1.out, gh_body_*.md, gh_comments_*.md
- **Linear reads:** linear_reads_gate25.py → linear_reads_1.out, linear_KS-*.md
- **Capture:** capture_mail_gate25.py → capture_1.out, mail_gate25T2_ready.md, stopcounts_gate25T2.json
- **Prompt:** prompt_gate25T2.TEMPLATE.txt
- **Launcher:** launcher_gate25T2.TEMPLATE.sh.txt, fill_gate25.py (fill_1..3.out), the filled prompt and `launch_qa_secuura_batch1268-t2.sh`, launcher_check_1/2.out
- **Repin:** repin_and_launch_gate25T2.sh (repin_dryrun_1.out)
- **Controls:** controls_gate25T2.sh (controls_*.out/.rc)
- **Drafter probe:** drafter_nodeprobe_g25t2.sh → nodeprobe_1.out (a PREDICTION)

## 9. NOT done / NOT measured by the drafter
- **Nothing sent or changed:** no launch, mail, tap, commit, push, routing write, container or port. No inbox read.
- **The Secuura checkout was only read:** ls-remote, `config --get`, and use as a `clone --no-local` source.
- **UNMEASURED:**
  - every suite count and red proof (READ only);
  - #1270's emit (the line port only);
  - #1268's walk on any shape;
  - #1273's cell through vitest (the probe ran the extracted function under plain node, over a fixed verb list, not the registry);
  - SYMLINK-SAMEPATH;
  - tsc, lint and prettier;
  - the usage gate and launch steps 4-6.
