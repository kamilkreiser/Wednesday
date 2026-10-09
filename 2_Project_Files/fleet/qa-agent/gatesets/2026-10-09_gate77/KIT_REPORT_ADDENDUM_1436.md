# gate77 ADDENDUM — #1436 KS-808 joins the gate as row 7 (extension drafter to Wednesday)

- **Drafted:** 2026-10-09 ~14:05–14:30 AEDT (03:05Z–03:30Z). Built and dry-run only. **Not launched.**
  - Nothing was merged, pushed, commented, mailed or routed. tmux was not touched.
  - `inbox_routing.conf` holds 0 copies of the routing line. Control: 177 agentmail lines.
- **Writes:** this kit folder only (each changed file has a `<name>.pre-1009-1436` backup beside it), plus my scratchpad `…/90f837f5-…/scratchpad/gate77x/`.
  - The scratchpad holds a `clone --shared`, worktree `wt1436`, the SIM commits and the arm plants.
  - Nothing was created under `!CODING`, which got READ verbs only. GitHub: GETs only, through the kit's own `lib_gate77.gh_get`, with GH_TOKEN read by name and never printed.

## 0. BLUF
1. **Launch-ready: YES, at the defaults, with ONE gate session for seven rows.** Wednesday still has to rule the open questions in §5 (Q-SEAT77 matters most).
2. **The new launch command** (from a real terminal, after the routing line is added). The `--develop` value is still the DRAFT develop, and `--repin-develop` must be origin develop *at launch*. Today that is 81d2e5f4c415. If #1427 lands first, the script refuses rc 10 and prints the new sha.
   ```
   script -q /dev/null bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-09_gate77/repin_and_launch_gate77.sh \
     --head-1429 1271d9597c43a540bedd6a707b1428b61130e492 --head-1430 d9928f4a8a4dc0ed0e16f967c8ae2df3448de877 \
     --head-1431 d715e5dfbbf2c301373016f2397cc9390c520dfb --head-1432 c4e6f50654fa1405dca3ff02d5905c6ee9cc6bf2 \
     --head-1433 934e20a599b1f734b718a3ac8d172113c789bb7b --head-1434 d7ba337a8ef64b9dafe6ec6231a8b3a1c651f89e \
     --head-1436 90d98754db7bb2addc6b7f83f12e3c6685b026a5 \
     --develop 1e7f90e261379e58eadc3ca0bbcc8d7e9e6938b0 --repin-develop 81d2e5f4c4151f5291a7a9c186d93a02dc5d38d6
   ```
3. **The canonical dry run (seven heads):**
   - Without `--repin-develop` it refuses **rc 10** at 03:20:48Z, printing `re-run with:  --repin-develop 81d2e5f4c4151f5…`.
   - With it, **rc 0** at 03:22:01Z and again at 03:28:08Z. Each run read: c1 57/0, clean 7/0, collide 2/0, the chain rc 0 with final `550d0ef42882`, usage 20% < 90, and launcher `--check` rc 0 with 9 pins EQUAL and 44 keywords.
4. **Refusal arms: repin 26/26 and launcher 28/28 fired.** Each was matched on rc AND its own asserting line, and each set has a positive control. All the original arms still fire, plus 10 new repin arms and 11 new launcher arms for #1436.
5. **#1436's code is disjoint** from the six rows, #1427 and develop's advance. The ONLY shared paths are the two platform HTML docs. A planted overlap control fires.
6. **The composer is still calibrated against gate76:** tree `57c9b5eaec95` and blobs flow `b2bd07dbae40` / cheat `f4503e99d43e`. It also reproduces the ORIGINAL six-row final `8ce413c386c6`. Both are now asserted in `c2 selftest`.
7. **#1436 red-proof re-run by me:** green 5/0, then 3 passed / 2 failed rc 1 (the two counter cells only, three CONTROLs ok), then restored == HEAD with porcelain 0, then green 5/0.
8. **#1436 is a MERGE-IN, not one commit on the raise_base.** Measured from the raise_base, its doc diff is ONE insertion carrying blocks 39 AND 41, so the six-row model would have mis-read it. The kit now measures each row from its own base (`rows.1436.base` = 81d2e5f4c415) and adds two checks:
   - **NO-EVIL-MERGE** (c1 P2M);
   - **BASE-CONTAINED** (c2), which refuses #1436 onto a develop that lacks 81d2e5f4c415. The draft develop can therefore no longer launch: arm r9c, rc 13.

## 1. The seventh row
| PR | ticket | head (verified) | tier + reason (from the diff) | file set (from its base 81d2e5f4c415) | +/- | vs develop 81d2e5f4c415 |
|---|---|---|---|---|---|---|
| #1436 | KS-808 | `90d98754db7bb2addc6b7f83f12e3c6685b026a5`, merge of [`a24efb3c5e04` (ONE commit on 1e7f90e26137), `81d2e5f4c415`], tree `43a9d3089e19` | **T2 + mandatory EXIT-INVARIANT arm**. The file is a deploy-path script (the `migrations` image), but the diff moves only a report counter. `skipped_count` is counted at :122, initialised at :148, subtracted at :175 and printed at :176. `failed_count`, apply_one's return codes, the `exit 3` arm and all SQL are byte-unchanged. `applied_count` feeds two echo lines only, and `git grep` at the head finds 0 non-test, non-doc consumers of `Summary: applied=`. Goes T1 if any decision consumes it (Q-TIER808). | `run-migrations.sh`, NEW `__tests__/ks808_run_migrations_counts_skips_apart.test.sh` (100644), + both docs | +183/-1, 4 | merge-tree rc 0 (it carries that develop); docs-only conflict after any earlier lander |

- The PR API (03:11:06Z) reads head `90d98754db7b`, open, unmerged, base develop, 4 files +183/-1, and body sha256/16 `2b4811c704c5430e`, which equals the seat's claim. The body is in `fixtures_bodies_at_draft/body_1436_at_draft.md`.
- `ls-remote` (03:07:54Z, and again in the dry runs at 03:20:55Z and 03:28:14Z) reads `refs/pull/1436/head` == `refs/heads/feature/ks-808-…-f6-1` == the head. The other six heads and #1427 (`2b6da5f561b0`, still the OLD head) are unchanged, and the API `head.sha` equals each one.
- Doc blocks vs its base: flow ONE insertion of 49 lines before `</body>`, seq `[41]`, balanced. Cheat 22 lines, `[KS-808]`, balanced. Both blocks are identical when measured against 1e7f90e26137, and develop's docs are byte-identical across 1e7f90e26137..81d2e5f4c415.

## 2. Collision and sequence
- **Code sets** (each row from its own base): the six rows; #1436 = {run-migrations.sh, ks808 suite}; #1427 = {04-container-trivy.sh, 3 suites}; develop since 1e7f90e26137 = 5 package-lock.json files (#1435).
  - **Pairwise code overlaps: none** (`m2.py`).
  - Control: a planted row sharing run-migrations.sh is caught by `m2.py` and by c2 selftest S7b.
  - c2 `collide` at 81d2e5f4c415: rc 0, and the shared paths are exactly the two docs, touched by all 7 rows + #1427 + develop.
- **Census** (03:20Z): 30 open PRs on develop. Only #1427 and #1383 touch a watched path, both on the docs only. Unchanged from the six-row draft.
- **Order (Q-ORDER77 amended):** `1432,1433,1429,1434,1436,1431,1430`, i.e. flow 36 37 38 40 **41** 42 43, with T1 first. With #1427 first the tail reads 35..43.

| step | with #1427 (onto 81d2e5f4c415) | tree | | step | without #1427 | tree |
|---|---|---|---|---|---|---|
| 1 | #1427 | `e948c77b8b46` | | 1 | #1432 | `5dbec1d1c3d4` |
| 2 | #1432 | `b244d664c64f` | | 2 | #1433 | `95fdd3ee1f1a` |
| 3 | #1433 | `bd4c46651aab` | | 3 | #1429 | `202db3f45f30` |
| 4 | #1429 | `2fcae7550df3` | | 4 | #1434 | `5c8b5c4afc61` |
| 5 | #1434 | `3e324effa803` | | 5 | **#1436** | `e9f4fec9b1a0` |
| 6 | **#1436** | `eaacabd0d735` | | 6 | #1431 | `d698c76bc955` |
| 7 | #1431 | `eed06aad8692` | | 7 | #1430 | **`408cae8897302aea5ece58f4d0ff7831421d1265`** |
| 8 | #1430 | **`550d0ef42882fd861a9781622681094caa545bf8`** | | | | |

- Both chains: rc 0 and ONEPASS == chain. Every step's readback is clean, the final docs are tag-balanced == develop, and every sequence is unique.
- Full per-step data is in kit.json `predicted_chain7_*` and in `composed_2026-10-09_7row/` (`MANIFEST.txt` has the sha256 of every composed doc).
- **Cross-check:** the composed docs of every step before #1436 are byte-IDENTICAL to the six-row `composed_2026-10-09/` files (18/18 `cmp`). Control: the post-#1436 #1431 flow doc DIFFERS, as it must.
- Every M's push delta now also carries the 5 #1435 lockfiles (OURS..M 14 → 34 paths). The prompt tells the merge seat to run `npm ci` before each push (F 6th's lesson for legs 6/7).

## 3. What changed in the kit (backups `*.pre-1009-1436` beside each)
| file | change |
|---|---|
| `kit.json` | row 1436 (base, parents, pre-merge fields, numstat, tier + reason, `product` red-proof recipe); `merge_order_default` 7; `author_seats` + Seat F 6th; `verdict_subject` (T2 x6, + #1436 KS-808); `develop_moved_NOTE`; `predicted_chain7_with1427` / `_no1427`; all 9 `script_sha256` re-pinned |
| `lib_gate77.py` | `row_base(R)` |
| `c1_pin_gate77.py` | all per-row figures from `row_base`; merge-in P2 (parents == kit) + **P2M NO-EVIL-MERGE**; 4 new self-test arms + a #1436 positive control (9/9 + 2 controls) |
| `c2_merge_gate77.py` | block / code set / CODE-UNMOVED from the row's base; **BASE-CONTAINED**; new arms S5b (moved run-migrations.sh), S7b (shared path), S8b (develop lacking the base); calibration pinned to `develop_at_draft` + a six-row-final control (11/11 + 3 controls) |
| `c3_tamper_gate77.py` | `revert_to_base` reads the row's own base blob |
| `gh_gate77.py` | message text only (row count) |
| `repin_and_launch_gate77.sh` | `--head-1436` REQUIRED; seven-row loops, fetch of #1436's base, render with P x7 |
| `launch_qa_secuura_gate77.sh` | P x7, seven GO strings, keywords + `NO-EVIL-MERGE` `EXIT-INVARIANT` |
| `prompt_gate77.txt` | #1436 throughout: the row, its merge-in shape, EXIT-INVARIANT, red-proof, preflight count, docs (41), body, live-run owed, GO 1436, author F 6th, subject; union-hazard wording corrected |
| `RULINGS_wednesday.md` | the EXTENSION section (Q-TIER808, Q-SEAT77 re-asked, Q-KEY1452, Q-ERRTEXT808, Q-PROSE808, Q-1427REBUILD) + R1/R5/R8 |
| `merge_inputs/` | NEW `1436.squash_subject.DRAFT.txt` (`KS-808: run-migrations.sh no longer counts skipped migrations as applied`, 72, ASCII, no `(#`); MERGE_INPUTS.json row |
| new | `composed_2026-10-09_7row/`, `fixtures_bodies_at_draft/body_1436_at_draft.md`, this file |

- `prompt_gate77.rendered.txt` and `head_at_launch.txt` were re-rendered by the dry run, and their originals are backed up.
- KIT_REPORT.md is unchanged: this addendum supersedes its §0/§2 figures for the launch.

## 4. FOUND / TESTED / HOW
| claim | FOUND | TESTED (rc) | HOW / control that can fail |
|---|---|---|---|
| heads | 7 == expected | ls-remote rc 0 (03:07:54Z; dry runs 03:20:55Z, 03:28:14Z); API GETs ×8 at 03:11:06Z; gh api ×7 5/0 each | repin r6/r6b/r6c (moved #1433 pull, moved #1436 pull, moved #1436 branch) rc 11; launcher l11/l11b rc 6 |
| merge-in honesty | `merge-tree a24efb3c5e04 81d2e5f4c415` = `43a9d3089e19` == M's tree; pre-merge numstat == row numstat | rc 0; c1 P2M PASS | known-conflict pair rc 1 (2 docs); c1 arm "evil-merge" fires P2M |
| c1 | 57/0 at 81d2e5f4c415 | `c1 --all` rc 0; `--selftest` rc 0, 9/9 + 2 positive controls | arms: wrong-tree, dropped/resized path, develop-touches-code (#1431 and #1436), conflict-outside-subset, #1436 head swapped (P3), wrong 2nd parent (P2), evil merge (P2M) |
| clean | six rc 1 docs-only; #1436 rc 0 | c2 clean rc 0 (7/0) | S6 code-conflict arm |
| collide | docs only | c2 collide rc 0 | S7, S7b planted overlaps |
| chain | finals `550d0ef42882` / `408cae889730` | c2 chain rc 0 ×2 (34/0, 30/0) | S1–S4, S5, S5b, S8b refused; calibration ×2 PASS |
| red-proof #1436 | 5/0 → 3/2 rc 1 (cells "one applied + one skipped", "a run that only skips" FAIL; 3 CONTROLs ok) → restored → 5/0 | `c3 run --pr 1436 --recipe product` rc 0 (03:16Z, wt at 90d98754db7b) | c3 selftest 8/8 (rc + asserting line) |
| EXIT-INVARIANT (partial) | rc 0/0/0/3 for one-skipped / all-skipped / clean / one-failed at BOTH base and head (base rcs are printed in the FAIL lines, and the two controls pass at base) | from the red-proof run | sibling `run_migrations_failure_exit_code.test.sh` at head: 7/0 rc 0 |
| canonical dry run | refuses at the moved develop; passes re-pinned | rc 10 (03:20:48Z); rc 0 (03:22:01Z, 03:28:08Z) | r7 / r7b rc 10, r8 stale rc 10, r9 / r9b / r9c rc 13 (`FAIL P7 #1431` / `FAIL P7 #1436`, exactly one P7 line each) |
| repin with #1427 landed | SIM develop+#1427 → "LANDED", order without 1427, final `550d0ef42882` | r10 rc 0 | — |
| usage | 20% < 90 | `usage_gate --check` rc 0 | NOT exercised red |

## 5. For Wednesday to rule (findings in the inputs; none is a drafter verdict)
1. **Q-SEAT77 is stale.** `merge_seat_ordinal` is still `Seat R 20th`, yet R 22nd is live and rebuilding #1427. If R 22nd (or a successor) merges #1427, put that ordinal in kit.json before the repin. It is unpinned, and the launcher checks it is not an author.
2. **Q-TIER808:** T2 + EXIT-INVARIANT (rec), or T1 because the script is on the deploy path.
3. **Q-ERRTEXT808 (F-1436-3):** run-migrations.sh :187-188 (unchanged) still echoes "the remaining applied=N-counts-skips defect is KS-808". After this PR that runtime text is false.
4. **Q-KEY1452 (F-1436-2):** the MERGE commit subject hyphenates the foreign key KS-1452 (c1 MSGKEYS INFO), while the body spaces it deliberately. The squash replaces it; the gate reads whether the integration linked it.
5. **Q-1427REBUILD:** the kit still models #1427's OLD head `2b6da5f561b0`. If the rebuilt #1427 lands with different job-04 bytes, the repin refuses rc 13 (CODE-UNMOVED), which is safe. That means re-draft the pending pin, never force.
6. **Kit-report correction:** the six-row KIT_REPORT/RULINGS R8 said union leaves the flow doc +1 "at EVERY step". The drafter's own `dry_225602.c2chain.out` shows it balanced at #1434 and #1431. Re-measured: 6 of 8 steps (flow), 4 of 8 (cheat). The rule (never union) is unchanged; RULINGS R8 and the prompt are corrected.
7. Also carried: the body's `Generated with` line (Q-ATTR77), the de-hyphenated title `KS 808:` (staged re-hyphenated), the seven prose sites not edited (Q-PROSE808), and the live run owed, so KS-808 does not move to Done (Q-LIVE77).

## 6. NOT tested by me
- the EXIT-INVARIANT arm as a dedicated base-vs-head per-line diff (only the exit codes and the suite's control cells were read);
- a live `migrations` run against PostgreSQL;
- full suites; the preflight on wtFinal; Actions for #1436;
- `cockpit.sh add`, and a real launch (not mine to run);
- the usage refusal arm;
- the Linear link state of KS-1452;
- whether R 22nd's rebuilt #1427 keeps job-04's bytes.
