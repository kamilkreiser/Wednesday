# Gateset 2026-10-06_gate71 — README for Wednesday

**gate71** is a **T1 gate, round 1 of 2**, on one Secuura/Blockchain PR: **#1398 (KS-1136 item 2, R-3, author Seat R 3rd)**.

**What the PR does.** `Blockchain/Testing/jobs/09-aggregate-report.sh` gains a 14-line loop. For each of jobs 01 02 03 05 06 07 08, an artefact that EXISTS but does not PARSE now emits `<job>/unreadable-artefact` at HIGH (`[ -f "$_f" ] && ! jq -e . "$_f"`). Before, such an artefact gave 0 findings and rc 0, which is a clean scan. The PR also adds a 6-cell shell suite and appends one block to each platform doc (flow `23.`, cheat KS-1136).

**Why T1.** The PR changes what a security-scan aggregation reports.

**Merge seat:** Seat R 4th.

**How to read the figures.**
- The kit was drafted by one Wednesday drafting subagent, 2026-10-06 ~12:37Z–13:05Z (host clock UTC).
- The drafter holds **no GitHub identity**. Its PR facts are `git ls-remote` and the author's mails only. Nothing from the PR API or Actions was read by the drafter.
- Every author figure is a **claim**. Every drafter figure names its instrument and is a **prediction**.
- The drafter's own account (every arm, every unverified claim, the open questions) is **`KIT_REPORT.md`**.

## 0. Bottom line

**Status.**
- The kit is complete.
- All 5 self-tests are green: 9/9, 11/11, 7/7, 11/11, 15/15. Each has planted arms that FAIL.
- The dry run passed, rc 0 (`dry_run_console_ex2.txt`).
- 17 launcher arms and 9 repin arms fire as intended (`LAUNCHER_ARMS.txt`).
- The gate has **not** been launched.
- The routing line has **not** been added.

**Launch command (Wednesday runs it; NOT run by the drafter).** Run it in a real terminal, under `script -q /dev/null`:
```
bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-06_gate71/repin_and_launch_gate71.sh 9414aa54e92ca243565d0d967aad991dc4c13840
```
- Add the routing line first (§7), or the launch refuses with rc 1.
- A real launch reads the PR API (gh_gate71 `api` + `census`). `--no-api` is refused outside `--dry-run`.
- If develop has moved past d75bfe2, the script refuses with rc 10. It prints the docs merge-in prediction and the `--repin-develop <sha>` to pass.
- It refuses outright (rc 13, c1 P12) if the move touched 09, the new suite or any tooling path.

**What the launch re-reads, refusing on any mismatch:**
- the READY;
- `refs/pull/1398/head`, the branch and develop, by ONE `ls-remote` with GIT_SSH_COMMAND unset and the checkout's own `core.sshCommand`;
- the API;
- the objects, by sha in the kit clone. An absent object is **refused by name**, rc 19.

The launcher then re-hashes the 10 pinned kit files against `kit.json` and re-reads origin itself. It refuses on:
- a moved head (rc 6);
- a develop different from the one the prompt was rendered for (rc 17);
- an absent head or develop (rc 19).

**Pins** (drafter `ls-remote` at 12:37:53Z, 13:00:17Z and 13:02:27Z, all identical):

| | |
|---|---|
| head | `9414aa54e92ca243565d0d967aad991dc4c13840` (pull/head == branch `feature/ks-1136-aggregate-unreadable-artefacts-ra3-2`) |
| tree | `2ee602cba3c99b3a75fa62e623011dc5d8b57665`; pre-docs tree `074705eebd81` (== the author's ITEM-0 prediction) |
| parent | ONE, `d75bfe2deb8075583cfb55af0921e4964e7c6f0e` == develop at every reading → **no merge-in** |
| files | 4: suite +164 (A 100644), 09 +14/-0 (100755 → 100755), flow +105, cheat +66; +349 -0 |
| subject | 83 chars, **lands 91** with ` (#1398)` (the READY says 90); 0 trailers (1 raw byte; control bf277eead268 55 raw); 0 Co-Authored-By |
| GO (pre-ruled) | `GO (Seat R 4th): merge 1398 on gate71` |
| verdict subject | `[QA -> Wednesday] GATE71 (T1): #1398 KS-1136 unreadable security artefact`, FROM coagent@ TO wednesday-agent@ |

## 1. Drafter predictions

All predictions are at (head 9414aa54e92c, develop d75bfe2deb80). Evidence files sit beside this README.

| Gate check | Instrument / evidence | Drafter result |
|---|---|---|
| C1 pin | `c1_pin_gate71.py`, `c1_head9414_devd75b_ex1.out` | 14/14. P1 live ls-remote. P4b pre-docs tree 074705eebd81. P10: 22 tooling paths identical. P12: 0 |
| 1 guard read | `c2 guard`, `c2_guard_head9414_ex1.out` | 6/6. A pure 14-line insertion at :216-:229, after `is_baselined()` :211 and before `ALL_FINDINGS=` :231. The 7 loop names == the file's own blocks minus 04, and each id == that block's first `emit`. Guard x1 with 2 conjuncts. 04's block byte-identical |
| 2 red-first + arms | `c2 suite`, `c2_suite_head9414_ex1.out` | 9/9. Suite 6/0. RED-FIRST (base blob via the suite's own `AGG_SH`) rc 1, cells **1, 2, 3** red. Arm A 2/4 (cells 1, 2, 5, 6). Arm B 4/2 (cells 4, 5). Arm C (08 out of the loop) 4/2 (cells 2, 3). Arm D (loop moved below ALL_FINDINGS) cells 1-3 red. `AGG_SH=''` rc 2 |
| 3 shapes | `c2 shapes`, `c2_shapes_head9414_ex1.out` + `.matrix.json` | 90/90 at the head (see the matrix below). CONTROL: the head rules applied to the base column report 51 violations |
| 4 callers | `c2 callers`, `c2_callers_head9414_ex1.out` | 4/4. EXECUTES-09: run-internal-audit.sh, the trivy suite, the new suite. CALLS-RUNNER: internal-audit.yml, github-actions-snippet.yml. K4: 69 baseline fingerprints, 0 `unreadable-artefact`. K3: the trivy suite 5/0 against head AND base, so it never reaches the loop |
| 5 shell set | `c3 list`, `c3_list_head9414_ex1.out` | 67 → 68, exactly the new suite; `--check-unreached` OK. **`full` NOT RUN by the drafter** (KIT_REPORT §4) |
| 6 docs | `c4 docs`, `c4_docs_head9414_ex1.out` | 11/11. Boundary-free: flow +8,161 B, cheat +5,446 B, each once, and the 1-byte-altered control is FALSE. Flow 1-16 18-23. Cheat tail KS-1136. Split-h2 control hit/missed. Only KS-1136 in each block (KS 878 de-hyphenated). Flow 88 distinct keys |
| 7 merge-in | `c4 predict/mergetree`, `MERGE_IN_PREDICTION.txt` | develop == base: squash tree == END_TREE, merge-tree AGREE. SIM moved develop: TAIL tree d67e85459d10, merge-tree DIVERGENCE (both docs) |
| 8 PR text | `gh prtext` / `api` (NOT RUN: no identity) | The commit message passes c1 P7/P8. The claims parser finds all 7 figures in it, all equal to the drafter's measurements. The commit message still carries the superseded "is unmeasured" sentence (RULINGS Q4) |
| 9 Actions | `gh actions` (NOT RUN: no identity) | Self-tested only: an unread log (0 `##[group]`) reads UNREAD, never clean; the needle at the head only is UNCLASSIFIED; the 302 is followed without auth |

**The shape matrix** (each row is one fixture; base = what it did BEFORE, head = NOW):

| shape, per job 01 02 03 05 06 07 08 | BEFORE | NOW |
|---|---|---|
| absent / valid-zero / the job's own SKIP JSON / two valid values | 0 findings, rc 0 | identical (clean stays clean) |
| valid WITH findings | own ids, rc 1 | identical, no extra id |
| 0-byte, whitespace, truncated, JSON null, JSON false, mode 000 | **0 findings, rc 0: the clean-scan silence** | exactly `<job>/unreadable-artefact` HIGH, rc 1 |
| valid + trailing garbage | own ids (the first value parsed) | own ids + the unreadable HIGH |
| 06 stderr merged (clean, and carrying a LEAK) | **0 findings, rc 0, the leak swallowed** | `06-tenant/unreadable-artefact` HIGH, rc 1 (RULINGS Q2) |
| 04 truncated | 04-trivy/unreadable-artefact x1 | the same, not doubled |
| REPEAT (the same unreadable 01 artefact on 2 runs) | rc 0 / rc 0 | run 1 rc 1; **run 2 rc 0**, NEW empty, totals.high 1 (RULINGS Q1) |

## 2. Claim defects the drafter measured (polish unless Wednesday rules otherwise)

- **D-1 "LANDS 90".** The real figure is 83 + 8 = **91**. The 92 rule holds. RULINGS Q5.
- **D-2 The arm-A explanation.** The PR body says dropping `[ -f ]` "breaks both main cells and both well-formed controls". Measured red cells are **1, 2, 5, 6**:
  - cells 1 and 2 are the main cells;
  - cell 5 is the well-formed 08 control;
  - cell 6 is the TRUNCATED-04 control;
  - cell 4, the all-seven-well-formed control, stays GREEN.

  The figure 2/4 holds. The explanation is half right.
- **D-3 The finding text** "exists but is not valid JSON - the job aborted mid-write" asserts a cause the aggregator never observes. Other measured causes:
  - 06's merged stderr;
  - mode 000;
  - JSON null / false;
  - the 0-byte artefact that jobs 02 / 03 / 05 / 08 leave when their own `jq … > "$OUT"` normaliser fails.

  Polish (it is code: not fixable at merge).
- **D-4 The commit message** still says the runner result "is unmeasured". The PR body was patched. RULINGS Q4.
- **D-5 Suite coverage gaps** the kit's matrix fills: valid-with-findings for 01-07 (only 08 is covered), 0-byte, whitespace, null / false, mode 000, trailing garbage, and 06 stderr. The fix-shape for the owner is more cells. Not a blocker.
- **D-6 The sibling** `ci/aggregate.ts:241-243` (RULINGS Q3) and **06's `2>&1`** (RULINGS Q2) are pre-existing defects in the same class, not in this PR.

## 3. Kit files and pins

`kit.json` `script_sha256` pins 10 files. The launcher refuses rc 31 on a mismatch and rc 30 on a missing, empty or unpinned file. `kit.json`, `README.md`, `RULINGS_wednesday.md` and `KIT_REPORT.md` are not pinned: Wednesday may edit the docs, and kit.json holds the pins.

| File | What | Self-test (drafter) |
|---|---|---|
| `kit.json` | pins, the PR spec, numstat + modes, the guard spec, the loop map, the consumers, the sibling class, the docs spec, tooling paths, the KS-168 six, the Actions known classes and develop-side heads | — |
| `lib_gate71.py` | read-verb git; write verbs only outside `!CODING`; `blob_at` (ls-tree, never `rev-parse <rev>:<absent path>`); absent-object refusal BY NAME; the composee5 readers extracted at the pinned lines; GitHub GETs with the log 302 followed without auth | via the five |
| `composee5_copy.py` | the reader source, copied from gate69 (sha256 f9ab42d9… identical) | — |
| `c1_pin_gate71.py` | P1-P12 + P4b | `c1_pin_selftest_ex1` 9/9 |
| `c2_product_gate71.py` | `guard`, `suite`, `shapes`, `callers` | `c2_product_selftest_ex1` 11/11 |
| `c3_suites_gate71.py` | `list`, `full`, `classify` | `c3_suites_selftest_ex1` 7/7 |
| `c4_docs_gate71.py` | `docs`, `predict`, `mergetree`, `qm` | `c4_selftest_ex1` 11/11 (SIM develop, objects only) |
| `gh_gate71.py` | `api`, `prtext`, `actions`, `census` | `gh_selftest_ex1` 15/15 |
| `prompt_gate71.txt` | template: `{{HEAD}}` x15, `{{DEVELOP}}` x1 | — |
| `launch_qa_secuura_gate71.sh` | per-kit launcher with `--check` | 17 arms |
| `repin_and_launch_gate71.sh` | the launch action, with `--dry-run [--no-api]` | 9 arms + 2 dry runs |

- `_scratch/` is gitignored. `_scratch/clone` is the kit clone (`--shared --no-checkout`, origin = the GitHub URL); it now also holds the SIM develop objects 4f7cb2adeb47 used by the arms. `_scratch/arms/` holds the stand-ins.
- The drafter's worktrees and fixtures are in the drafter's session scratchpad, not here.
- The shared checkout was verified unchanged: `rev-parse --all` sha256 `a48b7bc4…` and `.git/config` `4f624a21…` match before and after (cmp rc 0).

## 4. How the 8 commissioned checks map onto the kit

1. **Pin:** the launcher plus the repin script (moved head rc 6/11, moved develop rc 17/10, absent object rc 19), and c1.
2. **Product:** c2 `guard`, `suite` (red-first, one arm per conjunct, plus arms C and D) and `shapes`.
3. **Callers:** c2 `callers`.
4. **Whole shell set:** c3 `list`, `full` and `classify`.
5. **Docs:** c4 `docs`.
6. **Merge-in:** c4 `predict`, `mergetree` and `qm`.
7. **Body / subject:** c1 P7 / P8, gh `prtext` and `api`.
8. **Actions:** gh `actions`, plus c3 `classify` on the KS-168 log.

## 5. UNMEASURED by the drafter

See `KIT_REPORT.md` §4 for the full list with reasons. In short:
- everything GitHub: API, body, Actions, job logs, census;
- the whole 68-suite run;
- the ticket state;
- the push / preflight / lock figures (out of the kit's scope);
- the CI runner's jq version;
- any real scanner or live 06 run.

## 6. Dry run and arms

- **Dry run** (`dry_run_console_ex2.txt`, rc 0, plus `dry_130221.*`; ex1 `dry_run_console_ex1.txt` / `dry_130002.*` is identical in substance):
  - READY names the head (1 line) and #1398 (2 lines);
  - ls-remote rc 0: develop d75bfe2, pull/head == branch == 9414aa54e92c;
  - API NOT READ (`--no-api`);
  - develop UNMOVED;
  - kit clone: head, develop and base PRESENT;
  - c1 13/0;
  - c2 guard rc 0;
  - c4 predict == END_TREE and merge-tree AGREE;
  - render HEAD x15 DEVELOP x1;
  - routing line ABSENT (reported);
  - launcher `--check` rc 0 with **10 pins EQUAL** and 36 keywords.
- **Arms:** `LAUNCHER_ARMS.txt`.

## 7. Routing line (NOT added)

Back up `inbox_routing.conf`, then add the line from `ROUTING_LINE.txt`:
```
QA/Secuura-gate71|coagent@agentmail.to|yes
```

## 8. Pane, report and rung 5

- **Pane:** `QA/Secuura-gate71`.
- **Report directory:** `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-06-gate71/`.
- **Rung 5, in the pane:**
  - #1398 and KS-1136 named;
  - the charter or this README being read;
  - the head `9414aa54e92c`;
  - a `*_gate71.py --selftest` run;
  - its own clone and worktrees under `/private/tmp/claude-501/`, never `worktrees/s-ra3-ks1136`.
- **Rung 6:** `NOT-TESTED.written-first.md`.
