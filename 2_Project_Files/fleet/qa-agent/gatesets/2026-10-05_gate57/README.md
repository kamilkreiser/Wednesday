# Gateset 2026-10-05_gate57 — README for Wednesday

Drafted 2026-10-05, work 03:50Z – 04:20Z UTC (14:50 – 15:20 AEDT). Each figure names the kit file it came from.

## 0. What this is, and its status
**gate57 gates TWO Secuura/Blockchain PRs from Seat B 60th's ONE READY** (`fleet/briefs_staged/2026-10-05_seatB60_READY_1380_1381.txt`, sha256 `9a9d4ce39dce…`), one verdict per PR, one GO per PR, #1380 first:
- **#1380 KS-1333, T2.** Head `ac9f67a661eababfff30a1128f14c853803bd584`, branch `feature/ks-1333-blocknumber-pin-b60-1`. A new test-only source guard (3 cells) + Q-27 + N-1375-1 + its own §4 block (flow `12.`).
- **#1381 KS-1345, T1.** Head `7b356195a5e41d530c11f8e9286a6284be55b7c2`, branch `feature/ks-1345-webhooks-list-500-b60-2`. webhooks.ts list query: a DB failure now answers a constant 500, not `200 []` (and a non-UUID userId flips the same way) + its own §4 block (flow `13.`). Needs a MERGE-IN after #1380 lands (Q-M).
- Both cut from `3ce8cd4026a6` (`cut_base`).

**Status: KIT COMPLETE, NOT LAUNCHED.** Every checker self-tested (section 3). The live dry run passes end to end (`dry_console_041808_LIVE.out`, rc 0). Two things are Wednesday's: the routing line (section 4) and the launch (section 5).

🔴 **develop MOVED during drafting.** At 04:05:29Z `fe6daca343c1` landed: #1379 KS-749 (gate58), touching 6 lockfiles + `audit-baseline.json`. None of those is a kit path, and none is under Projects Documents. The launch action accepts that ADVANCE (section 7). **The READY's two END_TREEs are now STALE.** Re-derived by `c4b_predict_dev_fe6daca_ex1.out`:
- #1380 now lands as `dab6adb69ea3c7966ec17111a139bb5bcfadb68c`, not its head tree `0dab53e2…`.
- T2 at fe6daca is `ba3527224ff61c046806e24e3f64708edf30046d`, not `fb53feac…`.

The GOs and Q-M must name the tree for the develop the merge actually lands on.

**What the drafter did.**
- Wrote only to this folder and to the scratch dir `…/707ca275-…/scratchpad/gate57/`.
- In the shared checkout: `ls-remote` and `config --get` only.
- Created a scratch `git clone --shared` and fetched develop, `refs/pull/1380|1381|995/head` into it using the checkout's sshCommand.
- Made one worktree at cut_base inside that clone. Ran `npm ci --ignore-scripts` there (25 s, 1,937 packages) and built `packages/shared`.
- Made read-only GitHub GETs: pulls, files and compare. The token was read by name and never printed.
- No mail was sent. No ticket was touched. No `rm`. The one exploratory overlay file was MOVED to `scratchpad/gate57/explore/`.

## 1. Drafter predictions (REAL heads, the drafter's own runs — predictions for the gate, never its evidence)
| check | file | result |
|---|---|---|
| C1 pin | `c1_pr1380_ex1.out`, `c1_pr1381_ex1.out` (rc 0, 8/8 each, live API + ls-remote) | heads == READY on both instruments; one parent == cut_base; files and +/- exact both ways; head trees == the READY's; 0 trailers (control `bf277eead268` prints one); subjects 81 / 77 chars, byte-equal. `c1_pr1380_ex2_devmoved.out`: develop advanced and disjoint, PASS. |
| C2 golden | `c2a_golden_ex1.out` (rc 0) | test == r2 patch `+` lines == brief ```ts block == golden.diff (33 lines, 2341 B, patch sha `e2c92f8927bc3244`); index.ts untouched by the PR |
| C2 tamper | `c2a_tamper_ex1.out` (rc 0) | anchor unique at :1317. 3/3 at head. Under the tamper, B1 is red with the exact message while C1 and C2 stay green, and all 3 cells ran. Restored: sha256 `31422a6ab3c74804` both sides (== READY), status clean, 3/3 again. |
| C2 suite | `c2a_suite_ex1.out` (rc 0) | anchoring 354/353/1 -> 357/356/1; the only red is threadTokenMint (KS 562) at both ends; 0 new reds |
| C2 docfix | `c2b_gate_ex1.out` (rc 0, 12/12) | Q-27: same length 71, indices [63, 64] are 27 -> 36. KS 1404 test counted as 32 `it(` + 4 `it.each` rows = 36 (control: 32 ≠ 36). N-1375-1: both docs, sentence-only replacement, prefix and suffix byte-identical (8 and 678 chars). Every other line of the KS 1015 and KS 1404 blocks (153 / 113 flow lines, 36 / 54 cheat lines) byte-identical. #1381 leaves the ruled lines. |
| C3 shape | `c3_shape_ex1.out` (rc 0) | exactly the `.catch(... return []; })` line becomes "`;" plus 3 comment lines carrying KS-1345. `.catch(` lines go 4 -> 3, and the other three (incl. deliveries :412, dispatchEvent :513) are byte-identical. Titles: A0 -> RED KS-1345 A0 + control KS-1345 C. |
| C3 red-first | `c3_redfirst_ex1.out` (rc 0) | at base with the head test: exactly 1 red (RED KS-1345 A0), 500 expected / 200 received, 9 ran, 0 loadfail. Restored. 9/9 at head. |
| C3 probe | `c3_probe_ex1.out` (rc 0) | **the gate's own cells.** At base, P1 (rejected query) and P2 (non-UUID userId, 22P02) are RED by assertion (200, empty list) and controls C1 / C2 are green. 4/4 at head. The probe was moved to quarantine. |
| C3 suite / tsc | `c3_suite_ex1.out`, `c3_tsc_ex1.out` (rc 0) | originate 1062/0/90 -> 1063/0/90. tsc 5.9.3 gives rc 0 / 0; the positive control returns rc 2 with TS2322 and was restored (webhooks.ts sha `2f8828ba0246` == READY). tsconfig excludes `src/__tests__`. |
| C4 docs | `c4_pr1380_ex3.out`, `c4_pr1381_ex3.out` (rc 1 each, 1 FAIL) | everything passes EXCEPT **D4 timings cheat** (doubt D3): the cheat-sheet "Figures" row has a date and no host in BOTH PRs (`#1380 head:3800`, `#1381 head:3797`). The flow blocks name the host "Kamil's Mac Studio (2)". |
| C4 predict | `c4b_predict_ex1.out` (rc 0) | T2 re-derived INDEPENDENTLY at cut_base = `fb53feacdf1d…` == READY. The conflict is exactly the two docs (verbatim). Wrong-order control: a different tree (`c1e95c300285`). Read-back: flow h2 1..13; cheat 1404 < 1333 < 1345; `# 36 cells` 1 / `# 27` 0 / `other 27` 0 / `26 remain` 1+1; both blocks byte-identical. **At fe6daca: T2 `ba3527224ff6…`** (`c4b_predict_dev_fe6daca_ex1.out`). |
| C5 static | `c5_static_ex2.out` (rc 1, 2 FAIL) | **L1** two of the three quotes have `-` where the scripts print an EM DASH (transcription). **L3** the READY omits the `legs N N N` line the verdict prints (section 2, R1). L2 / L4 pass. |
| C5 run | `c5_run_pr1381_ex1.out` (rc 0) | **the gate's own preflight at #1381 head** (no stack): `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` / `  legs 3 4 8 — local stack not up; you can clear this by starting it.` — the 3 legs are 3 (spec-auth), 4 (path resolvability) and 8 (served-spec consistency). |
| C6 scope | `c6_pr1380_ex1.out`, `c6_pr1381_ex1.out` (rc 0, 7/7) | own key only (foreign keys de-hyphenated: KS 1015 / 1404 / 562; KS 1333 / 1341 / 466); Refs + URL; 0 closing words; body sha == READY (`4c7ab30afe78e293`, `b32871e0af79840e`); NOT run names the live sweep / §5f (+ deliveries `webhooks.ts:412`); claims in words; tiers consistent |
| census | `census_ex2.out` | 21 other open PRs, 0 OVERLAP, 1 EXPECTED OVERLAP: #995 (kit `reported_overlaps`) |

## 2. Doubts for the GATE, and what in the READY contradicts itself (the drafter rules none)
**READY contradictions / stale claims**
- **R1 (self-contradiction).** "THE 3 SKIPPED LEGS ARE NOT NAMED, on purpose: `.githooks/pre-push:273` says … not enumerated here".
  - The cited line is a COMMENT in the hook.
  - `preflight.sh:757-760` (base blob `270b8913c009`) PRINTS the skipped legs on the line right after the verdict it quotes.
  - The gate's own run prints `legs 3 4 8`.
  - The READY says "quoted exactly", but two of the three quotes replace the script's EM DASH with `-`.
- **R2 (self-contradiction).** PR 1's pathgate "FIRING CONTROL: this head against PR 2's declared set FAILS, naming missing ['documentRepo.ts','routes/documents.ts'] and extra ['ks1333 test','cheat']".
  - documentRepo.ts and routes/documents.ts are **KS-1278's (PR 4's)** files, not PR 2's.
  - Against PR 2's set {ks1341a, webhooks.ts, flow, cheat} the missing paths would be ks1341a and webhooks.ts, and the extra path the ks1333 test only.
  - So the control ran against a different set than stated. #1381's mirror control (1 missing, 2 extra) is consistent.
- **R3 (stale).** "END_TREE 0dab53e2… its OWN head tree … merges CLEAN … nothing predicted about it" and "T2 fb53feac…". Both were true at 3ce8cd4026a6 and are both stale since fe6daca (section 0). The "FUSE 236.2 h, 3 rows" line is also stale: #1379 removed those rows.
- **R4 (stated against the ruling's wording).** The READY measures that T2 "differs from PR 2's head tree only in those two plus PR 1's own ks1333 test file". So a real merge-in head's TWO-DOT diff from its gated head can never be "ONLY the two docs" as Q-M is worded.
  - Doubt **QM**: Wednesday should restate Q-M. The kit judges it as: tree == T2, two parents [gated head, develop-with-#1380], and a two-dot diff == the two docs plus exactly the paths develop brought in, each at develop's blob (`c4b … --merge-in-head`, self-tested Q0-Q4).

**Doubts**
- **D3.** The cheat-sheet "Figures" rows in BOTH PRs state timings with a date and no host. The flow blocks name the host. Is that a §4 defect or acceptable because the flow doc carries the host?
- **D4.** KS-1345's second flip (non-UUID userId). The kit probe makes it red-first by assertion using a MOCKED 22P02 rejection. Which principals carry a non-UUID `userId` is UNMEASURED by everyone. That is a T1 behaviour change with an open reach question.
- **D5.** #1380's timing statement "0 stated timings name the anchoring suite, must-hit control 23 (flow) / 35 (cheat) duration figures".
  - The kit's instruments read 15 / 36 lines with a duration (16 / 39 with gate55's regex) and do NOT reproduce 23 / 35.
  - Duration lines that also say "anchoring" exist at flow :1078 (mermaid tier line) and cheat :1218.
  - #1381's control `auth` 70 / 69 DOES reproduce (C4 D7).
- **D6.** The source-text guard stays green if the two lines are commented out. The PR says so itself.
- **D7.** #995 (KS 741, open) edits `services/anchoring/src/index.ts` COMMENT-ONLY at :505-:513, outside the guard's spans.
  - The brief's P10 census missed this: it listed #995's originate files only.
  - Recorded in kit `reported_overlaps` with its head `b8155636e8e6`. If that head moves, the launch refuses rc 15.
- **D8.** The bodies quote `pathgate55` as PASS. That is the seat's tool and is not re-run by the kit; C1 P4 is the gate's own file-set proof.

## 3. Instruments and self-tests (every arm fires; outputs `*_exN.out` beside each)
- `lib_gate57.py`: `git()` allows read verbs only. `wgit()` allows write verbs only in a repo NOT under /Volumes/DevMASTER (lexical + realpath). Also `guard_out`, `guard_scratch`, `GH` (read-only, offline replay) and `run()` (.out/.err/.rc separate).
- `c1_pin_gate57.py --selftest`: **10/10** (`c1_selftest_ex2.out`). Arms: wrong PR's set, trailer, `(#n)`, wrong parent, develop advance touching a kit doc, disjoint advance allowed, 1-char subject, planted wrong expectation.
- `c2a_ks1333_gate57.py --selftest`: **14/14** (tamper inert, loadfail, C1 red, wrong message, 2 cells; green check; suite new red / totals; golden 1-char and newline plants).
- `c2b_docfix_gate57.py --selftest`: **11/11** (`c2b_selftest_ex2.out`). `_ex1` was 10/11: one plant (T6) was INERT. It was fixed, and an inert-plant guard was added.
- `c3_ks1345_gate57.py --selftest`: **15/15** (`c3_selftest_ex2.out`; `_ex1` crashed on a tuple bug, fixed).
- `c4_docs_gate57.py --selftest`: **12/12 per PR** (`c4_selftest_pr138{0,1}_ex3.out`). The real D4 finding is carried as a BASELINE: an arm passes only on a NEW failure. `--base-vs-base` FAILS D1 + D2 as designed (`c4_basevsbase_*`).
- `c4b_predict_gate57.py --selftest`: prediction **5/5** + Q-M arms **5/5** (good merge-in; extra edit; 13-before-12; single-parent rewrite; trailer).
- `c5_preflight_gate57.py --selftest`: **4/4** (the real READY, em-dash-exact + legs line, missing quote, 13/15).
- `c6_scope_gate57.py --selftest`: **7/7** (#1380), **8/8** (#1381).
- **Refusal arms** (`refusal_arms_ex1.out`, all on SCRATCH paths, nothing created):
  - SIM launcher: stale pin → exit 9; develop moved → 17; head moved → 6; compare wrong → 10; no TTY → 21.
  - repin: short sha → 9; PRs in the wrong order → 9.
  - lib guards (stand-in forbidden root): worktree / clone / --out → rc 2.
- **Dry runs:** `dry_console_041545_SIM.out` (offline fixtures, rc 0), `dry_console_041555_LIVE.out` and `dry_console_041808_LIVE.out` (live API + ls-remote + compare, develop advanced and accepted, the SIM launcher's `--check` passing, rc 0).

## 4. Routing line — NOT added
Back up `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`, then append:
```
QA/Secuura-ks1333-1345-1380|coagent@agentmail.to|yes
```

## 5. Launch
```
bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate57/repin_and_launch_gate57.sh 1380 ac9f67a661eababfff30a1128f14c853803bd584 1381 7b356195a5e41d530c11f8e9286a6284be55b7c2 --dry-run
bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate57/repin_and_launch_gate57.sh 1380 ac9f67a661eababfff30a1128f14c853803bd584 1381 7b356195a5e41d530c11f8e9286a6284be55b7c2
```
Exit codes:
- rc 1: no routing line.
- rc 9: bad input or PR order.
- rc 10: develop advanced into a kit path or Projects Documents, or the fill refused (e.g. the READY or a previous report changed hash).
- rc 11: a head moved.
- rc 15: OVERLAP.
- rc 12 / 13 / 14 / 16: usage gate / --check / cockpit / override.

The real launch writes `pins_gate57.json`, `launch_qa_secuura_ks1333_1345_1380.sh` and `2026-10-05_secuura-ks1333-1345-1380-1381.prompt.txt`.

GOs expected: `GO (Seat B 60th): merge 1380 on gate57`, `GO (Seat B 60th): merge 1381 on gate57`. Verdict subject: kit `verdict_subject_template`.

## 6. Not adapted / not measured
- The preflight was run at #1381's head only, not #1380's.
- No live stack, so legs 3 / 4 / 8 never ran.
- The real merge-in head does not exist yet.
- The 23 / 35 timing control was not reproduced (D5).
- gate58's report was not read: it was in progress, with no report.md at drafting.

## 7. Develop moved before launch
- **Disjoint advance** (no kit path, nothing under Projects Documents): the launch accepts it, records `behind`, and the prompt's DEVELOP AT LAUNCH line tells the gate the READY's END_TREEs are stale. It gives the drafter's re-derivation when kit `predictions_by_develop` has that develop (fe6daca: yes).
- C1 P3 accepts the same advance.
- c2a / c3 runs stay cut_base vs head, which is still correct: each PR is one commit on cut_base.
- **Overlapping advance:** rc 10, RE-DRAFT.
- **If #1380 merges before the gate runs:** #1381's merge-in becomes real. Re-run `c4b … --develop-after <develop> --merge-in-head <sha>` and re-launch for #1381 only.
