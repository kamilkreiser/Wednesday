# gate77 KIT REPORT — drafter to Wednesday

- **Rows (six, each its own verdict):** #1429 KS-1449 (E 11th), #1430 KS-1328 (F 5th), #1431 KS-1355 (F 5th), #1432 KS-1410 (R 19th), #1433 KS-1139 (R 19th), #1434 KS-1171 (G 5th).
  - Each is ONE commit whose ONE parent is RAISE_BASE `0a6177ea5482227e83d5045b68b8577a56326ffc`.
  - Tiers: #1432 is T1; the other five are T2.
- **Drafted:** 2026-10-09 09:20–10:05 AEDT (2026-10-08T22:20Z–23:05Z). Built and dry-run only. **Not launched.**
  - Nothing was merged, pushed, commented, mailed, ticketed or routed.
  - `inbox_routing.conf` is untouched (ROUTING_LINE.txt: 0 copies in it).
- **Writes:** only this folder, plus the drafter's scratchpad (`…/scratchpad/gate77/`: the clone, the worktrees wt1431 and wt1433, SIM commits and arm plants).
  - Nothing was written under `!CODING`: read verbs only there, and every write verb ran in a scratch clone or in this kit's gitignored `_scratch/`.
  - GitHub: GETs only.

## 0. BLUF
1. **Launch-ready at the defaults.**
   - Canonical dry run: rc 0 at 22:56:02Z–22:57:05Z. It read c1 48/0, c2 clean 6/0, collide 2/0, the chain == the kit prediction, usage 5% < 90 at the DEFAULT stop (no override), and launcher `--check` rc 0 with 9 pins EQUAL and 42 by-name keywords.
   - Refusal arms: repin **16/16** and launcher **17/17** fired. Each arm was matched on rc AND its own asserting line.
2. **All six heads verified** == Wednesday's records, by `ls-remote` from the checkout at 22:20:32Z and again inside the dry run at 22:56:08Z. Each head also matches the API `head.sha`, and `refs/heads/<branch>` == `refs/pull/<n>/head`.
3. **No row merges cleanly into current develop `1e7f90e26137` (#1428), and none has a code conflict.**
   - `merge-tree --write-tree` gives rc 1 for all six, and the conflict set is exactly the two platform HTML docs.
   - Control: each row against raise_base gives rc 0 with tree == END_TREE.
   - The code-path sets are pairwise DISJOINT. They are also disjoint from #1427 and from develop's advance.
   - So **every row needs a docs-only keep-both merge-in**, landed in sequence.
4. **The composer is calibrated.** Modelling #1427 onto develop reproduces gate76's predicted tree `57c9b5eaec95` and gate76's composed blobs (flow `b2bd07dbae40`, cheat `f4503e99d43e`) byte for byte.
   - Predicted final trees for the default order: `8ce413c386c691dcb7e2e349c3d4d4e696ca7888` with #1427 first, `8304089bf1b7ef734d18d3e31d619dec997aaf56` without it.
5. **Red-proofs re-run by the drafter on the two shell rows.** Both used `c3_tamper_gate77.py`, with the tamper landed, the restore == HEAD, porcelain empty, and the green reproduced:
   - #1431: 27/0 → 25 passed, 2 failed, only the two new cells failing and the CONTROL ok.
   - #1433: 6/0 → 3 passed, 3 failed, the three controls ok.
   - The four node rows need S-1 (~1.6 GB each). The gate runs them.
6. **The polish item is confirmed at source.** #1430's and #1431's bodies say the skipped legs are "unnamed". Their push logs name them: `s-f5-ks1328-d9928f4a8a4d-push.out:1650` and `s-f5-ks1355-d715e5dfbbf2-push.out:1653` both read `legs 3 4 8 — local stack not up`. The kit treats it as a BODY-CORRECTION, not a code defect.
7. **Usage:** gate76's override grant has expired. Its EVENT, the account renewal, happened: the gauge read 1–5% at draft. gate77 carries no override (Q-USAGE77).

## 1. The six PRs
Head verification: `git -C <checkout> ls-remote origin refs/pull/<n>/head` (22:20:32Z) == the API `head.sha` (gh_gate77 A3) == `refs/heads/<branch>` (dry run 22:56:08Z) == c1 P1. The merge-clean instrument is `merge-tree --write-tree <develop 1e7f90e26137> <head>` in the scratch clone (c1 P8 / c2 `clean`).

| PR | ticket | head (verified) | tier + reason | file set (code; + both docs) | +/- | vs current develop |
|---|---|---|---|---|---|---|
| #1429 | KS-1449 | `1271d9597c43a540bedd6a707b1428b61130e492` == expected | **T2**: published-contract change (6 × `required: true` in nft-certificate.openapi.ts + the regenerated YAML, +6 lines); no handler line moves | `docs/openapi/secuura-api.yaml`, `nft-certificate.openapi.ts`, 2 new vitest files (`ks591-*`, `ks1364-*`) | +225/-3, 6 paths | rc 1, docs only |
| #1430 | KS-1328 | `d9928f4a8a4dc0ed0e16f967c8ae2df3448de877` == | **T2**: tests-only (one kyc test file: describe timeout + one cell) | `services/kyc/src/__tests__/db.retry.test.ts` | +77/-1, 3 | rc 1, docs only |
| #1431 | KS-1355 | `d715e5dfbbf2c301373016f2397cc9390c520dfb` == | **T2 + mandatory DECISION-INVARIANT arm**: dev script in the KS-666 guard, but only the informational `list_other_stacks()` changes, and `blocked`/rc never read it (Q-TIER1355) | `scripts/stack_guard.sh`, `scripts/__tests__/stack_guard.test.sh` | +123/-1, 4 | rc 1, docs only |
| #1432 | KS-1410 | `c4e6f50654fa1405dca3ff02d5905c6ee9cc6bf2` == | **T1**: SECURITY SURFACE. Thrown error text leaves 10 api-gateway 500 bodies (public edge, index.ts:780-782). Runtime product change; no rendered surface, so in-process driving, no browser | `routes/{audit-export,batch,notifications}.ts`, 2 new vitest files | +372/-10, 7 | rc 1, docs only |
| #1433 | KS-1139 | `934e20a599b1f734b718a3ac8d172113c789bb7b` == | **T2**: script (`smoke-test.sh` counters `((X++))` → `X=$((X + 1))`; Makefile/npm smoke targets, not a deploy path or guard) | `scripts/smoke-test.sh`, new `smoke_test_counters_survive_errexit.test.sh` (100644, == its sibling's mode) | +162/-3, 4 | rc 1, docs only |
| #1434 | KS-1171 | `d7ba337a8ef64b9dafe6ec6231a8b3a1c651f89e` == | **T2**: tests-only (anchorSubmission.ts untouched; pins the money boundary at :345 without changing it). G 5th's "TIER 1" is the raise scale (Q-TIERSCALE) | new `services/anchoring/src/__tests__/ks1171-b1-absent-boundary-is-inclusive.test.ts` | +234/-0, 3 | rc 1, docs only |

- Every file count and +/- equals the seat's READY claim, and every PR body hash equals the seat's claim (fixtures_bodies_at_draft/).
- Trailers: 0 on all six (1 B vs the 55-B control `bf277eead268`).

## 2. Collision and sequence
- **Shared paths:** only `Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html` and `…/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html`.
  - Both are touched by all six rows, by #1427 (pending) and by develop's advance (#1428).
  - **No code path is shared** by any two of: the six rows, #1427, develop since raise_base (c2 `collide` rc 0; a planted overlap arm fires).
- **Census** (gh GET, 22:5xZ): 29 open PRs on develop. Only #1427 (gate76) and #1383 (KS-1401, HELD) touch a watched path, both on the docs only.
- **Default landing order (Q-ORDER77): `1432, 1433, 1429, 1434, 1431, 1430`**, ascending flow number (36 37 38 40 42 43), with the T1 row first.
  - With #1427 first, the tail reads 35..43 ascending (39 is #1428, already on develop).
  - Each step is a docs-only keep-both merge-in M with parents [head, develop-so-far]. Its push delta carries Blockchain/Dev paths, so the full preflight runs in-hook.

| step (with #1427) | PR | onto | predicted tree | OURS..M / DEV..M paths |
|---|---|---|---|---|
| 1 | #1427 | `1e7f90e26137` | `57c9b5eaec95` (== gate76) | 9 / 6 |
| 2 | #1432 | SIM `61455ad6f427` | `48f80b12a3fe` | 13 / 7 |
| 3 | #1433 | SIM `dc50c2906ab9` | `07fdf43b9663` | 18 / 4 |
| 4 | #1429 | SIM `fd17f0555141` | `7f5dd2973f5a` | 20 / 6 |
| 5 | #1434 | SIM `f4a3a8afeef7` | `af82ffa3215b` | 24 / 3 |
| 6 | #1431 | SIM `3600c6dc2fd7` | `9c694a72cef6` | 25 / 4 |
| 7 | #1430 | SIM `20d43427c665` | **`8ce413c386c6`** final | 27 / 3 |

- Without #1427 the final tree is `8304089bf1b7`. Per-step trees, blobs and the composed docs are in `composed_2026-10-09/{with1427,no1427}/` + `MANIFEST.txt`.
- **The merge seat re-runs `chain --drop <landed rows>` on the REAL develop before every step.** The kit's composed docs are valid only on the develop they were composed on.
- **Union hazard, re-measured on this batch:** `merge-file --union` leaves table/tr/td +1 on the flow doc at every step, and div/table/tr/td +1 on the cheat doc from step 3. Keep-both is balanced at every step.

## 3. The kit
| file | what | self-test |
|---|---|---|
| `kit.json` | rows (heads, END_TREEs, numstats, tiers + reasons, red-proof recipes), predicted chains, pins | — |
| `lib_gate77.py` | read-only `git`, `wgit` (refuses write verbs under !CODING), composee5's pinned flow reader, the per-heading cheat reader, the keep-both `block_of` / `compose`, tag balance, GH GETs | — |
| `c1_pin_gate77.py` | P1-P8 per row (+ INFO subject / closing / keys) | **5/5 arms + positive control** |
| `c2_merge_gate77.py` | `clean`, `collide`, `chain [--drop]`, `selftest` | **8/8 arms + gate76 calibration + real chain** |
| `c3_tamper_gate77.py` | generic red-proof: W0 refusals, S-1 gate, G / T (tamper landed) / R / X (restore == HEAD) / G2 | **8/8 arms (rc + asserting line)** |
| `gh_gate77.py` | `api`, `census`, `actions` (SUBSET, by-id), `selftest` | **4/4** |
| `repin_and_launch_gate77.sh` | the REPIN + launch action | **16/16 arms** |
| `launch_qa_secuura_gate77.sh` | the pane launcher (pins, rulings, head file P×6/B/D/S/C/O/T/Q, prompt guards, origin re-read, TTY) | **17/17 arms** |
| `prompt_gate77.txt` | the gate prompt (rendered → `prompt_gate77.rendered.txt`) | launcher guards |
| `merge_inputs/` | six squash-subject DRAFTS + MERGE_INPUTS.json (body rules) | asserted ASCII, <= 92, no `(#`, own key first |
| `fixtures_bodies_at_draft/` | the six live PR bodies at draft | hashes == seats' claims |
| `composed_2026-10-09/` | predicted composed docs + chain.json (7.1 MB) | — |
| `RULINGS_wednesday.md`, `ROUTING_LINE.txt` | open questions; `QA/Secuura-gate77\|coagent@agentmail.to\|yes` | — |

## 4. Dry-run results (FOUND / TESTED / HOW)
| check | FOUND | TESTED (rc) | HOW / control that can fail |
|---|---|---|---|
| heads | six == expected | `ls-remote` rc 0 (22:20:32Z, 22:56:08Z); gh api ×6 rc 0 (5/0 each) | repin r6 (moved #1433 head) rc 11 `MOVED HEAD`; launcher l11 rc 6 |
| c1 pins | 48/0 | `c1 --all` rc 0 | selftest: wrong tree / dropped path / resized path / develop touching code / conflict outside subset — all FAIL as planted; P6 control 55 B; P8 known-conflict pair rc 1 |
| merge-clean | all six rc 1, docs only | c2 `clean` rc 0 (6/0) | S6: a SIM develop editing #1431's own line → `CODE CONFLICT` |
| collision | docs only; code disjoint | c2 `collide` rc 0 | S7: a planted row sharing stack_guard.sh → FAIL |
| chain | final `8ce413c386c6` (with #1427) / `8304089bf1b7` (without); 29/0 and 25/0 | c2 `chain` rc 0 ×2; one-pass == chain | S1-S4 (non-insertion, wrong anchor, duplicate number, dropped `</td>`) all refused; S5 moved code path refused; calibration == gate76 |
| red-proof #1431 | 27/0 → 25/2 (two new cells FAIL, CONTROL ok) → restored → 27/0 | `c3 run --pr 1431 --recipe product` rc 0 | c3 selftest 8/8 (dirty / moved HEAD / existing out / anchor absent / wrong needle / forbidden root) |
| red-proof #1433 | 6/0 → 3/3 (3 RED cells FAIL, 3 controls ok) → restored → 6/0 | `c3 run --pr 1433 --recipe product` rc 0 | same |
| repin moved develop | SIM develop+#1427: c1 P7 clean, chain re-predicted (order without 1427: content-decided "LANDED"), final `8ce413c386c6` | r7 rc 10 (no `--repin-develop`), r8 rc 10 (stale), r10 rc 0 `RE-PINNED` | r9: a SIM develop touching stack_guard.sh → rc 13 `C1 FAILED` (RE-GATE) |
| usage | 1% (22:2xZ), 5% (22:56Z) < 90 | `usage_gate.sh --check` rc 0, WED_USAGE_STOP unset | NOT exercised red (needs >= 90%) |
| routing | line absent (0 copies), 173 agentmail lines in the conf (control) | r15 real run rc 1 `add the routing line first` | — |

**Drafter defects caught by the arms (disclosed):**
1. c2 `collide` counted #1427-vs-develop overlap as a code collision once #1427 had landed. Repin arms r7/r8/r10 caught it (rc 13). Fixed: only overlaps a gate77 row is party to count, and the pending row is reported LANDED by blob.
2. The repin's dry run did not hand its ls-remote stand-in to the launcher's own re-read, so r10 refused rc 17. Fixed: a dry run passes `GATE77_LSFILE` as `GATE77_LS`.
3. The c3 self-test's "moved HEAD" arm committed nothing (identical content) and did not fire. Fixed: a real later commit.
4. The c3 arms first matched rc only. Fixed: rc AND the asserting line (STANDING_LINES, R 17th).

**NOT tested by the drafter:**
- the four node red-proofs (#1429 `ts`/`yaml`, #1430, #1432, #1434: they need S-1);
- full suites; the preflight on wtFinal; Actions classification (`gh actions` was not run);
- #1431's DECISION-INVARIANT arm (READ only, plus the 25 pre-existing cells passing on both sides);
- #1432 in-process driving; the usage refusal arm;
- the `GATE77_CLONE`-under-!CODING arm (rule: never plant a sibling of a real project path);
- `cockpit.sh add` (a dry run cannot add a pane); bash >= 4.1 (none on the host); Linear state.

## 5. Defects / findings in the INPUTS (for the gate to rule; none is a drafter verdict)
1. **#1430 and #1431 bodies: "unnamed by this push's output" is false.** The push logs name legs 3 4 8 (above), and F 5th's READY repeats the claim. BODY-CORRECTION.
2. **#1430 / #1431 titles are de-hyphenated** (`KS 1328:`, `KS 1355:`), and the head subjects open `test(KS-1328):` / `fix(KS-1355):`. The staged squash subjects are re-hyphenated (Q-SUBJ77).
3. **#1429 code carries 0 KS-1449.** Its added code lines carry 8 × KS-591 and 12 × KS-1364 (the test files are named and keyed for the register keys), and the six `required: true` lines have no comment. SKILL §5d (Q-KEYS1449; rec Minor).
4. **#1429's body hyphenates a foreign key, KS-656.** Four bodies (#1429 #1430 #1431 #1434) carry `Generated with` lines (Q-ATTR77).
5. **#1430's doc blocks hyphenate a foreign key, KS-1155**, so gate76's D4 "only own key" rule fails: polish.
6. **Tier-scale collision.** READY mails and raise briefs say "TIER 1" for test-only rows, which is the raise scale, not the QA scale (Q-TIERSCALE).
7. **Trap for the gate:** `services/api-gateway`'s `test` script is bare `vitest` (WATCH mode). The recipe uses `npx vitest run`, and the prompt forbids `npm test` there.
8. **#1433 cannot be reproduced at bash >= 4.1 on this host**: `/opt/homebrew/bin/bash` and `/usr/local/bin/bash` are absent. CI is the only witness (Q-1433BASH).
9. **#1429's most relevant preflight leg (8, served spec) is UNRUN** on every push (Q-1429LEG8).

## 6. Open questions (full text in RULINGS_wednesday.md; every one has a default the kit already assumes)
- **Q-1427FIRST:** rec (a) land #1427 (gate76 GO 2) first, then repin with `--repin-develop`. (b) launching now also works: #1427 is modelled as step 1, content-decided.
- **Q-ORDER77:** rec/default `1432,1433,1429,1434,1431,1430`.
- **Q-SEAT77:** rec/default Seat R 20th, or whichever R seat merges #1427; edit `merge_seat_ordinal`.
- **Q-MERGEINS77:** rec accept six merge-ins with six in-hook preflights; `chain --drop` before every step.
- **Q-TIER1355:** rec T2 + DECISION-INVARIANT arm (T1 if it fails).
- **Q-TIERSCALE:** rec the gate uses the QA scale.
- **Q-KEYS1449:** rec Minor, not a blocker; an optional one-commit follow-up.
- **Q-UNNAMED:** rec correct the squash bodies; no PR PATCH.
- **Q-SUBJ77:** rec as staged.
- **Q-ATTR77:** rec drop the attribution lines and de-hyphenate KS-656.
- **Q-COMP77:** rec comparator = develop.
- **Q-1433BASH:** rec CI as the witness; live run owed.
- **Q-1429LEG8:** rec a named limitation; KS-1449 stays open.
- **Q-USAGE77:** rec no override.
- **Q-PREFLIGHT77:** rec one preflight on wtFinal.
- **Q-LIVE77:** rec none of the four runtime tickets moves to Done.

## 7. Launch steps (Wednesday runs these; the gate76 shape)
1. Rule or accept the defaults in RULINGS_wednesday.md. If the merge seat changes, edit `kit.json` `merge_seat` / `merge_seat_ordinal` (unpinned).
2. (Q-1427FIRST (a)) let #1427 land, and verify it at source.
3. Add the routing line, exactly the content of `ROUTING_LINE.txt`, to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`:
   `QA/Secuura-gate77|coagent@agentmail.to|yes`
4. Run the REPIN + launch from a real terminal (the launcher refuses a non-TTY with rc 21). The `--develop` value is ALWAYS the draft develop:
   ```
   script -q /dev/null bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-09_gate77/repin_and_launch_gate77.sh \
     --head-1429 1271d9597c43a540bedd6a707b1428b61130e492 --head-1430 d9928f4a8a4dc0ed0e16f967c8ae2df3448de877 \
     --head-1431 d715e5dfbbf2c301373016f2397cc9390c520dfb --head-1432 c4e6f50654fa1405dca3ff02d5905c6ee9cc6bf2 \
     --head-1433 934e20a599b1f734b718a3ac8d172113c789bb7b --head-1434 d7ba337a8ef64b9dafe6ec6231a8b3a1c651f89e \
     --develop 1e7f90e261379e58eadc3ca0bbcc8d7e9e6938b0
   ```
   - If #1427 (or anything) has landed, it refuses rc 10 and prints the exact `--repin-develop <origin develop>` to add.
   - It refuses rc 11 on any moved head (that row is re-drafted, never re-gated on a stale pin), and rc 13 if develop moved a row's CODE path (RE-GATE).
5. RUNG 5: the pane `QA/Secuura-gate77` is up (pane census printed), and `head_at_launch.txt` D/O/T/Q equal the repin's printout.
6. The verdict arrives as `[QA -> Wednesday] GATE77 (T1 x1, T2 x5): …` from coagent@agentmail.to. Expect a long gate: four S-1 installs + wtFinal, ~7 min of preflight, the Actions waits.
