# Gateset 2026-10-05_gate64 — README for Wednesday

Drafted 2026-10-05 10:59Z – 11:2xZ by a first drafting subagent (it died when its parent session rotated), FINISHED 11:3xZ – 12:xxZ by a second. Every figure names the kit file it came from. Every builder statement is a CLAIM the gate re-measures; the prompt says so.

## 0. What this gate is, and its status

**gate64 is a T2 gate over ONE Secuura/Blockchain PR: #1389, KS-1330, "re-land round-2 signal handling; the SIGINT-to-pid arm can now run".**
- Two paths: `Blockchain/Dev/scripts/run-shell-suites.sh` (+102/-6) and `Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh` (+206/-0), both 100644 (`c1_pr1389_ex2.out`).
- Author: Seat G 1st, **WRAPPED** 11:04Z. Merger: **Seat G 2nd** (not yet launched). Re-keyed from G 1st in kit.json (old file: `_quarantine/kit.json.pre-rekey-G2nd`).
- **GO string:** `GO (Seat G 2nd): merge 1389 on gate64`. The launcher refuses a prompt that carries `GO (Seat G 1st)` (exit 8).
- **NO GO string:** `NO GO (gate64): 1389 at a7f5965a7b3f — <N-1389-n: the blocker, one line>`
- Tier: T2 as commissioned; the builder's brief PROPOSED T1 (`seatG1_scripts_lane.md` :79, Q-TIER :267). The gate grades it.
- head `a7f5965a7b3fd94b25a26e73c250052db4be6aa0`, END_TREE `273ec1c0ee3a54a5d797125a9d2307bd7ef0593c`. Its ONE parent is `0f2422925317` (#1382), **not develop**: every merge of #1389 needs a merge-in first.
- **develop MOVED during finishing:** `32e058975d4e` (READY, first drafter) → **`3cb93b9c731ed6b514ed88829e11dbfd1c073cd5`** (#1384 KS-1210 merged 11:35:39Z, then #1392 KS-1411; read by ls-remote 11:41:08Z). 28 paths, both platform-k docs among them, 0 kit paths, 0 hook paths, 67 runner-globbed suites before and after.

**Status: KIT COMPLETE, NOT LAUNCHED.** Every checker's self-test fires on planted defects and passes its clean case (section 3). The dry run is in section 5. Wednesday owns the routing line (section 4) and the launch (section 7).

**What the drafters did:**
- **Writes:** only inside this directory, plus `/private/tmp` scratch (the second drafter's own `git clone --shared` in its session scratchpad, where it fetched develop for the prediction on `3cb93b9c731e`; and `/private/tmp/g64ref/clone` for the c4 refusal test). `_scratch/clone` (+ worktrees `wt_head`, `wt_develop`, `wt_simmerge`) is the first drafter's shared clone; SIM objects went into its store only.
- **In `/Volumes/DevMASTER/!CODING/`:** read verbs only (`ls-remote`, `show`, `log`, `diff`, `ls-tree`, `cat-file`, `rev-parse`, `merge-base`, `config --get`) and the clone sources.
- **Network:** GitHub REST GETs (pulls/1389, files, the open-PR census, pulls/1384), `ls-remote`, and one `git fetch` of develop into the /private/tmp clone. No Linear read, no mail, no launch, no routing edit, no `rm`.
- An orphaned process from the first drafter was checked: none remains (`ps` 11:33Z shows only another seat's preflight). Its unfinished whole-runner run at the SIM merge-in had no rc and is quarantined (`_quarantine/c3_whole_simmerge_ex1.INCOMPLETE-*`).

## 1. Drafter predictions at a7f5965a7b3f (the gate re-derives every one)

| check | file | result |
|---|---|---|
| C1 pin | `c1_pr1389_ex2.out` (rc 0, 12/12, develop 32e0); `c1_pr1389_dev3cb9_ex1.out` (rc 0, 12/12, develop 3cb9, origin read) | P1 origin agrees, #1250 untouched at 2b8dcb824dd2 · P2 one parent 0f2422925317 · P3 2 paths exact both ways · P4 END_TREE 273ec1c0ee3a · P5 trailers 1 byte (control 55) · P6 0 Co-Authored-By · P7 75 chars · P8 one `Refs KS-1330` · P9 100644 · P10 NO new leg (hook blobs equal) · P11 advance disjoint (31 paths at 3cb9). INFO: the commit message still says "2 use `read`". Real control `c1_basehead_ex1.out`: rc 1, FAIL P2 P3 P3-3dot P4 P7 P8 |
| C2 re-landed | `c2_pr1389_ex1.out` (rc 0, 6/6) | R1-R6 PASS. INFO: the interrupt cell asserts `rc != 0`, never `== 130` (D7); `rss_suite_log=` re-indented to column 0 inside its loop |
| C3 red-first | `c3_redfirst_head_ex1.out` / `_develop_ex1.out` (rc 0 each) | head 61/0, develop 54/7, harness `INT installable=yes` both; head arms rc 143 / 130 / 130, kill_to_exit 0s |
| C3 tampers | `c3_redfirst_tamper_ex1.out`, `_tamperfg_ex1.out` | rule2: 60/0 with 1 UNREACHABLE (landed by sha). fgsuite: 59/2, the two latency cells red (12s, 11s), interrupt cells green |
| C3 inherit | `c3_inherit_ex2.out` (rc 0) | head: INT in suite installable=no, fd0 == /dev/null (dev 1863792391 ino 336 rdev 3,2). develop CONTROL: INT yes, fd0 == the marker file |
| C3 whole runner | `c3_whole_head_ex1.out`, `c3_whole_develop_ex1.out` | **66 passed, 1 failed (of 67) at BOTH ends**, the red `ks949_main_seed_idempotence.test.sh` both times (D3). Head: the run_shell_suites section reads `INT installable=no`, 2 UNREACHABLE INT arms (D2) |
| C3 coupling census | `census_head_ex3.out` (rc 0) | 67 suites; read-head 16, INHERITED 0, MANUAL 1; trap-INT 9, all 9 also TERM/EXIT; control FIRES (5 read-heads in run_shell_suites.test.sh); ks1401_049 at #1383: 0 / 0 |
| C4 docs | `c4_docs_pr1389_ex1.out` (**rc 1**, 3/4) | D1 skill quotes at :362-:363 / :417-:418 PASS · D2 0 doc paths PASS · **D3 FAIL**: `systemTest/CLAUDE.md` 3 hits (:1156, :1541, :2592), `Blockchain/Dev/CLAUDE.md` ABSENT from the tree; akto (-i) 71 / 83 / 170 / 16 · D5 PASS (0 KS-1330 keys, 25.-32. unused). INFO D4: develop's docs carry `run-shell-suites.sh # 67 suites` (flow :2191, cheat :3862) |
| C4 predict | `c4_predict_dev32e0_ex1.out`, `c4_predict_dev3cb9_ex1.out`, `gitmerge_dev3cb9_ex1.out` | develop 32e0 → **bc8774cbe5cd** (== kit / READY); develop 3cb9 → **`d1f3c5cb6c1c9d1f84f52ed65e8189f595806e7a`** == `git merge-tree --write-tree` rc 0; headdocs CONTROL `2b51ba85bef1` differs |
| C5 PR text | `c5_pr1389_ex1.out` (rc 0, 8/8) | T1-T8 PASS on the live body (8494 bytes, byte-equal to `api/pr1389_body.md`). INFO figures printed for the gate |
| census | `gh_census_ex1.out` (rc 0) | 26 others: 0 OVERLAP, 1 EXPECTED (#1250 at kit head), 0 NEAR, 3 SUITES (#1383, #1253, #927), 4 DOCS (#1390, #1388, #1385, #1383); control FIRES |

## 2. Doubts for the gate (the drafter rules none; the prompt carries D1-D11)

- **D1 Tier.** T2 commissioned; T1 proposed because the runner is leg 14 for every seat.
- **D2 Subject truth.** "the SIGINT-to-pid arm can now run" holds in a direct foreground run (`c3_redfirst_head_ex1`). Inside the runner itself, so inside leg 14, the harness reads `INT installable=no` and both INT arms print UNREACHABLE (`c3_whole_head_ex1`). Leg 14's 67/0/0 is no evidence for item 1.
- **D3 Whole runner.** 66/1/0 at both ends here vs the claimed 67/0/0. The red is the same suite at both ends, so it is probably environmental, but that is UNMEASURED.
- **D4 Coupling table.** Body: 0 read-head suites and 10 of 10 INT trappers. Drafter's instrument: 16 read-heads (0 INHERITED) and 9 of 9. Is that a different definition or a false table?
- **D5 Grep claim false as stated.** See C4 D3. Also, the control figures 70/82/16 do not match the drafter's 71/83/16 (-i).
- **D6 Stale commit message.** It says "2 use `read`". The squash body must not carry it.
- **D7 Interrupt cell.** It passes on `rc != 0`. The 130/143 appear only in its label.
- **D8 Merge-in tree label.** The handover says bc8774 was "computed at develop 0f2422925317". But predict(0f24) == END_TREE, and bc8774 == predict(32e0). The label is wrong, and develop has since moved (d1f3c5cb6c1c).
- **D9 Q-DOC (b).** Tooling suites are none of "backend unit, integration, or systemTest". But the runner globs `systemTest/__tests__`, and develop's docs now name the runner.
- **D10** PREFLIGHT-INCOMPLETE 12/15 for a change to the pre-push runner itself.
- **D11** `/tmp/rss.*` residue: 88 on this host per the handover. The gate counts before/after its own runs.
- **Kit doubt K1.** The census treats a CLOSED #1250 as a blind control (rc 3, the launch refuses). If #1250 is closed on purpose before launch, re-key `gh_census_gate64.py` (section 8).
- **Kit doubt K2.** A moved HEAD is never re-pinnable by `--repin-develop`. Every kit figure is about a7f5965a7b3f, so a new head is a re-draft.

## 3. Kit files

| file | role | self-test (planted defects fire, clean passes) | live run |
|---|---|---|---|
| `lib_gate64.py` | read-verb `git`, write verbs only outside `!CODING`, GH GET | — | — |
| `c1_pin_gate64.py` | C1 P1-P11 | `final_c1_selftest.out` rc 0, **25/25** | `c1_pr1389_ex2` rc 0; `c1_pr1389_dev3cb9_ex1` rc 0; control `c1_basehead_ex1` rc 1 |
| `c2_relanded_gate64.py` | C2 R1-R6 | `final_c2_selftest.out` rc 0, **11/11** | `c2_pr1389_ex1` rc 0 |
| `c3_redfirst_gate64.sh` | red-first, tampers (foreground guard G1-G3) | firing control `c3_redfirst_firing_bg_ex1.rc` = 4 (backgrounded → refused) | head / develop / tamper / tamperfg ex1 rc 0 |
| `c3_inherit_gate64.sh` | item-3 probe | firing control `c3_inherit_firing_bg_ex1.rc` = 4 | `c3_inherit_ex2` rc 0 |
| `c3_wholerunner_gate64.sh` | whole runner from its real path | same G1 guard (code-read, not separately fired) | head / develop ex1 rc 0 |
| `c3_census_gate64.py` | coupling census | `final_census_selftest.out` rc 0, **17/17** | `census_head_ex3` / `_develop_ex3` / `_mergetree_ex3` rc 0 |
| `c4_docs_gate64.py` | docs D1-D5; KEY-ANCHORED predict; qm M1-M8 | `c4_selftest_ex2.out` rc 0, **33/33** (13 docs arms + key parser + duplicate-key refusal + predict(0f24)==END_TREE + predict(32e0)==bc8774 with headdocs control + SIM develop + Q-M positive + 10 Q-M arms incl. tail-moved / edited / KS-1330-slipped sections + 2 predict refusals) · refusal `c4_refusal_ex1.rc` = 2 (/private/tmp stand-in root) | `c4_docs_pr1389_ex1` rc 1 (D3, a predicted finding) |
| `c5_prtext_gate64.py` | C5 T1-T8 | `c5_selftest_ex2.out` rc 0, **18/18** | `c5_pr1389_ex1` rc 0 |
| `gh_census_gate64.py` | collision census | `gh_selftest_ex1.out` rc 0, **12/12** | `gh_census_ex1` rc 0 |
| `launch_qa_secuura_ks1330_1389.sh` | the launcher (static prompt; refuses a moved head 6, non-descendant develop 17, no TTY 21, overrides 16, prompt defects 8 / 33 / 39 / 25) | arms in section 5 | `--check` rc 0 |
| `repin_and_launch_gate64.sh` | the launch action, steps 0-7 | arms in section 5 | `--dry-run` section 5 |
| `prompt_gate64.txt` | the gate's prompt | — | — |

History kept, never deleted: `_quarantine/c4_selftest_ex1.*` (an arm whose text did not match the builder's regex: an arm defect, fixed); `_quarantine/c5_selftest_ex1.*` (an arm with the key BEFORE the closing word, which is not a closing reference: an arm defect, fixed); the first drafter's census / c1 instrument trips.

## 4. Routing line — NOT added
Back up the file first. Then add ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`:
```
QA/Secuura-ks1330-1389|coagent@agentmail.to|yes
```
Until it is present, step 0 of the real launch refuses rc 1. The dry run reports it instead.

## 5. Dry run and refusal arms
- **Dry run WITHOUT re-pin** `dry_console_norepin_ex1.out` (11:4xZ) returns **rc 10**, as designed. It prints:
  - `DEVELOP MOVED 32e058975d4e -> 3cb93b9c731e`
  - the advance, read by GitHub compare: ahead 5, behind 0; 28 paths; both docs; KITHIT none; SUITES none
  - the MERGE-IN REQUIREMENT
  - `re-run with: --repin-develop 3cb93b9c731ed6b514ed88829e11dbfd1c073cd5`
- **Dry run WITH re-pin** `dry_console_repin_ex1.out` (11:49:48Z – 11:50:40Z) returns **rc 0**:
  - routing line reported missing (0 of 153 agentmail lines)
  - census rc 0: 26 others, 0 OVERLAP, 1 EXPECTED, 3 SUITES, 4 DOCS; control FIRES
  - API, pull/head and branch agree with the input head; #1250 untouched
  - develop RE-PINNED, recorded in `dry_114948.repin.txt`
  - C1 at the head rc 0, 11 checked
  - launcher `--check` rc 0, prompt sha256 `0a57a1ced6d8c15c`
- **Launcher arms** `launcher_arms_ex1.out`, **10/10**:
  - real `--check` 0
  - stand-in ls == real 0
  - pull/head moved 6
  - develop not a descendant 17
  - GO names Seat G 1st 8
  - a G 1st GO added beside the G 2nd one 8
  - keyword missing 33
  - hold missing 39
  - no `ultrathink` 8
  - launch path with no TTY 21
  - Earlier: README missing → 8 (`launcher_arm_noreadme_ex1.*`)
- **Repin arms** `repin_arms_ex1.out`, **9/9**:
  - short sha 9
  - wrong PR 9
  - develop as head 11
  - stale `--repin-develop` 10
  - stand-in develop UNMOVED 0
  - stand-in develop BEHIND, not re-pinnable 10
  - stand-in #1250 moved 15
  - Two REAL (non-dry) runs refused at step 0, rc 1, before any census, usage gate or cockpit call: one with `G64_LSFILE` set, one with a routing stand-in. Because routing refuses first, the `G64_LSFILE`-on-a-real-run refusal (rc 16) was NOT itself reached.

## 6. The merge-in (develop moved): KEY-ANCHORED, never div-anchored
- The merge ALWAYS needs Seat G 2nd to merge develop in first, even if develop stops moving: the head's parent is 0f2422925317.
- #1389 carries no doc hunk. So the target is develop's tree with the 2 kit paths at the head's blobs, and every doc at M equals develop's doc, key for key. Sections are found by their h2 KS key, never by `<div class="section">` or tail position. Tonight's rule: the cheat sheet has no readable ordering invariant. The gate's key-anchored predicted tree is the authority.
- Predictions: develop 32e0 → `bc8774cbe5cd`; **develop 3cb9 → `d1f3c5cb6c1c9d1f84f52ed65e8189f595806e7a`**. For any later develop: `G64_SCRATCH=<scratch> c4_docs_gate64.py predict --repo <own clone> --develop-after <D>`.
- The GO covers M only if `c4_docs_gate64.py qm --repo <clone> --merge-in-head M --develop-after D` passes M1-M8. Anything else re-gates.
- `repin_and_launch_gate64.sh` refuses rc 10 on a moved develop unless `--repin-develop <that sha>` is given. It is a hard rc 10 (not re-pinnable) if the advance touches a kit or hook path, or develop does not descend from 32e0.

## 7. How Wednesday launches it (after section 4's routing line)

Pane `QA/Secuura-ks1330-1389`. Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-05-ks1330-1389-g64/`. Verdict subject `[QA -> Wednesday] GATE64 #1389 (T2 KS-1330: re-land round-2 runner signal handling + SIGINT-to-pid arm; author Seat G 1st wrapped, merger Seat G 2nd)`.

**Dry run** (no usage gate, no cockpit):
```
script -q /dev/null bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate64/repin_and_launch_gate64.sh 1389 a7f5965a7b3fd94b25a26e73c250052db4be6aa0 --dry-run --repin-develop 3cb93b9c731ed6b514ed88829e11dbfd1c073cd5
```
**THE launch command:**
```
script -q /dev/null bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate64/repin_and_launch_gate64.sh 1389 a7f5965a7b3fd94b25a26e73c250052db4be6aa0 --repin-develop 3cb93b9c731ed6b514ed88829e11dbfd1c073cd5
```
If develop has moved again, both refuse rc 10 and print `re-run with: --repin-develop <new sha>`. Read the printed advance, then re-run with that sha.

Exit codes: 1 routing · 9 input · 2 ls-remote · 3 API / blind census control · 15 OVERLAP or #1250 moved · 11 head moved (RE-DRAFT) · 10 develop moved (re-pin) or not re-pinnable · 13 C1 or launcher `--check` · 16 override · 12 usage gate · 14 cockpit. Add `WED_USAGE_STOP=…` only with Kam's recorded authority.

**Rung 5 (verify at rung 5 or 6, never below).** Read the pane and find content only THIS gate would produce: KS-1330 / #1389, `…/2026-10-05_gate64/README.md` or `QA_AGENT_CHARTER.md` read, head `a7f5965a7b3f`, a `*_gate64.py --selftest`. Rung 6 is `NOT-TESTED.written-first.md` in the report dir.

## 8. Re-draft recipe (the head moved, or develop is not re-pinnable)
1. Re-measure kit `head`, `end_tree`, `files`, `modes`, `head_blobs`, `parent*`, `r2_*`, `claims`, and the C3 evidence. Use `_scratch/mkkit.py` as a starting point.
2. Edit the head in `prompt_gate64.txt` and `launch_qa_secuura_ks1330_1389.sh`. Both are static.
3. Re-run every `--selftest`, then c1, c2, c4 docs + predict, c5, the census, and a `--dry-run`.
4. A merge-in head on top of a7f5965a7b3f is NOT a re-draft. It is judged by `c4 qm`.

## 9. NOT COVERED by this kit (the gate's, or nobody's)
- The C3 runs above are the DRAFTER's, on this host, `/bin/bash 3.2.57`. The gate re-runs them; none is evidence.
- No whole-runner total at the merge-in tree: the first drafter's run died unfinished. No coupling census at the 3cb9 merge-in prediction (the census at 32e0's SIM merge exists).
- No Linear read (KS-1330 / KS-1302). No PR #1250 gate-report cross-read beyond its hash.
- No preflight run. Legs 3 / 4 / 8 need a stack.
- No PTY / real-terminal ^C (KS 1325's). No non-macOS bash, no CI host.
- No `/tmp/rss.*` before/after count around a drafter run.
- No check that `ks949_main_seed_idempotence.test.sh` fails for an environmental reason (D3).
- `c3_wholerunner_gate64.sh`'s G1 guard was code-read, not fired separately.
- The repin script's rc 2 / 13 / 14 / 12 paths were not driven. Its rc 16 path for `G64_LSFILE` on a real run was not reached either: routing refuses first.
- No independent second implementation of the key-anchored predictor. It agrees with `git merge-tree` on both real develops, and that is the only cross-check.
