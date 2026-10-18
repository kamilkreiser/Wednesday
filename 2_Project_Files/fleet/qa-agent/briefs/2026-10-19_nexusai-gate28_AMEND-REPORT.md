# Gate 28 (RD-476 / RD-856+RD-857 / C-170 delta) — AMENDMENT 1 report, for Tuesday

Drafted 2026-10-19 from 07:17:52 AEDT (by `date`) by a read-only drafting agent (Opus 5.5). This agent only read and measured. It wrote the files listed in §1, plus the `.pre-amend` copy. Nothing was launched, mailed or published, and `inbox_routing.conf` was not edited.

## 0. BLUF

- **Main is `888203c8c50e13938ca557e8aa0f1faf2101ff31`, not the predicted `2facd7c`.** `ls-remote` read it at 07:17:52 AEDT (rc 0, first attempt). The kit now re-pins to it and recomputes every prediction from its counts (4660/291). It checks the chain 36a0dc0 → 5eb80a7 → 888203c by **ancestry**, never by first-parent (gate 27's topology note).
- **The kit no longer predicts main. Tuesday stamps it.** The MAIN pin is a slot: a `MAIN-STAMP:` line plus the PIN-HEADS MAIN row, and the two must agree. Gate 27 is running on `888203c` now and holds the jest lock (`qa-g27-C1`), so RD-778 may land first. The launcher refuses unless origin main equals the stamped sha and tree exactly.
- **Conflicts against `888203c`: the counts file only, for all three heads.** I measured this with the legacy stdout-only `git merge-tree c7ca0ed 888203c <head>`. The `.git/objects` count was 44 before and 44 after.
- **Item D (the C-170 test delta) is added at tier 2, through code.** It is PR #96, `fd8ff2a` → `f15217c`: 4 test paths and 0 product bytes. Rows d0-d6 cover it. The kit states that C-170's product was gated by gate 26, and that D's merge into main is not part of this gate.
- **The two risks are kept as rows:**
  - **r10P:** the new suites boot `LLM_PROVIDER: 'ollama'`. RD-794 has now landed, so this is measurable.
  - **r10N:** RD-476's headline question never reached a model. This stays NOT RUN, named.
- **There are now three verdict lines plus ORDER/TURN:** RD-476; RD-856+RD-857 as one stack; C-170 DELTA.
- **The four READY bodies are copied into `briefs/`, sha256 verified.** Each one is byte-identical to the builder's own `mail-*` file.
- **Launcher:** `bash -n` passes (rc 0). The slotted `--check` passes every content guard and then refuses at 32S + 40, as intended (§4). A scratch stamped copy passes, and two planted errors refuse.

## 1. Files written

| file | what | sha256 |
|---|---|---|
| `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-18_nexusai-gate28-batch-rd476-rd856-rd857.md` | the kit, AMENDED (230 → 251 lines, 39 diff hunks) | `4244530a7dba00f972dfa438fac5dd491e8b5458c3b036990a597be88e2f5d48` |
| `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-18_nexusai-gate28-batch-rd476-rd856-rd857.md.pre-amend` | `cp -p` copy, identical to the pre-edit kit | `b9af3bb3da91163ca4e296df1453223380d258554e0dd7d4086983ae1ef0f305` |
| `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate28.sh` | NEW launcher (815 lines) | `e0a972c6052b3f1887faee093bb2a2a70c216f1b616f64b5b6db7ac5d07cfe6d` |
| `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-19_nexusai-gate28-READY-rd476-r2.txt` | READY copy, 2657 bytes | `c43893cd6694b40723300ced6eadd598ecfeff05cf46f53c5bfcf7614cfd0821` |
| `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-19_nexusai-gate28-READY-rd856.txt` | READY copy, 6813 bytes | `c8f502245764b548b3d72074780dee208086ce1794c1f18084c683a8484955e2` |
| `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-19_nexusai-gate28-READY-rd857.txt` | READY copy, 6190 bytes | `7cf6c411d2b3605851143bed9aea54560ce7ea5defe0cd9ae0af70217ac76256` |
| `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-19_nexusai-gate28-READY-c170-delta.txt` | READY copy, 6686 bytes | `a2e8a037fef584b675724542fe06b8dc313d687f713c515bcfc2277548ad0cdd` |
| this report | — | — |

The launcher is mode `-rw-r--r--`: I did not `chmod` it, because my commission allowed Write/Edit only. It is launched via `bash '…'`, so the execute bit does not matter.

## 2. What changed in the kit

- **Top of file:**
  - The title now names four items.
  - A new **AMENDMENT 1** paragraph covers: the measured chain; the ANSWER-18 quote; re-pin at stamp; D added; the two risks as rows; one verdict line per item; the READY copies; and the list of amended places.
  - Line 3 no longer carries a literal at-sign slot token.
- **Item list:**
  - A/B/C now point to the READY copies, each with its sha256.
  - A new item **D** gives: the head pair and tree, the 4 paths, 0 product bytes, tier 2, the "product gated by gate 26 / merge not part of this gate" statement, and the READY copy.
- **THE RE-PIN STEP:** rewritten. The MAIN pin is stamped; the launcher's refusal conditions are stated; D is not merged.
- **Stamp lines:**
  - The MODEL line now tells Tuesday to stamp a bare model ID from `models_latest.json` (sonnet or opus level).
  - A new `MAIN-STAMP: sha … | tree … | landed since 888203c: …` line replaces `Main as Tuesday read it at stamp`.
- **PIN-HEADS:**
  - The MAIN-AT-DRAFT and MAIN-EXPECTED rows are replaced by one `MAIN` row with the stamped slot.
  - A new `C170D` row: `rd-460-c170-turn-s101o | f15217c… | fd8ff2a… | 1 | IN`.
  - The "main is NOT a pin" sentence is reversed.
- **TIER:** a new paragraph for D, quoting ANSWER-19. D is PROVISIONAL if d1, d2 or d3 did not run.
- **WRONG items:**
  - The head-check line gains the amendment's reading.
  - **1**: the measured chain, with trees and parents. Gate 27 is running.
  - **2**: merge sets re-measured against `888203c`, with hunk locations. The prompt is unchanged at `888203c`.
  - **5**: the RD-794 premises at `888203c`; now row r10P.
  - **9**: `888203c` counts and recomputed predictions; D's counts blob.
  - **11**: #91's Build is now success.
  - **12-14**: evidence-class words only. Without them the launcher's "every WRONG item is marked" guard refuses. Gate 27's amender did the same for its item 5.
  - **New 16**: D's facts and my own equivalence re-derivation.
  - **New 17**: D's CodeQL state.
  - **New 18**: the builder's M1-M5c design, the M4 caveat carried, and the mutant anchors.
  - **New 19**: corrections (instrument sources, object count, tools, load, CLARIFICATIONS size).
- **T-rulings:**
  - **T1**: M0 = the stamp; D needs no C-57.
  - **T2**: adds D's coverage, (a) the 19 suites only, (b) plus a full verify V4 of `f15217c`.
  - **T3**: adds PR #96 reads.
  - **T6**: adds `g28/d0` and `g28/d1`. `f15217c` is named only by `refs/remotes/origin/rd-460-c170-turn-s101o`, which a mirror copies.
  - **T7**: (v) C-170's TURN sits outside the batch arithmetic (+147/+7).
  - **Every `RULED:` slot is untouched.**
- **Elsewhere in the kit:**
  - **Properties:** D1-D6.
  - **Carried ruling (b):** pinned to the stamp.
  - **THE MODEL RULE:** last sentence made model-agnostic.
  - **Charter:** D's failure states; verdicts now one per item.
  - **PRIOR ROUND:** D is round 1 of the delta. It quotes gate 26's product verdict and lists the 19 suites.
  - **§1:** M0 and D's target.
  - **§2:** D's severities.
- **§2a rows:**
  - r1's expected value is re-based to `888203c`.
  - r8's predictions are now 4695/292, 4682/293, 4717/294.
  - **r10 is split into r10P (provider, measurable), r10R (routing) and r10N (headline question on a real model, NOT RUN, named).**
  - r13 gains D's READY claims.
  - **New rows d0-d6.**
- **§3:** D's controls.
- **§3a:**
  - H3 now covers r10P and r10R.
  - New H8 (d2 + d3) and an optional H9 (V4).
  - The instrument-source correction (§3 below).
- **§3b:** item (5) for D.
- **§7:** object count; D's builder evidence hashed.
- **§8:** (vi)-(viii), D's landing, which is the seat's later.
- **§11:**
  - Four lead lines: RD-476; RD-856+RD-857 STACK; C-170 DELTA; ORDER/TURN.
  - New limits L-D1, L-D2, L-D3.
  - The NOT TESTED line is extended with D's clauses.
- **PROVENANCE:** the amendment's actions.
- **FILL AT STAMP:** rewritten so it names the slots without at-signs. The READY and launcher items are marked done (✓).

Everything else is verbatim: §2b, C1-C7, r0, r2-r7, r9, r11, r12, §9, §10, the H-rules and the clarification quotes.

## 3. Measurements, with sources

All NexusAI reads used `git --no-optional-locks` read verbs under `/bin/bash`, plus the legacy stdout-only `merge-tree`. All `gh` calls were GETs, with `GH_CONFIG_DIR='/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/4_Credentials/.gh-config'` on repo `datasecau/Reporting_Dashboard_Au`, account `kamilDatasec`.

1. **Heads** (`ls-remote origin`, 07:17:52 AEDT, rc 0, 1 attempt; again by the launcher's `--check`, 1 attempt):
   - main `888203c8c50e13938ca557e8aa0f1faf2101ff31`.
   - The three batch heads, all unchanged:
     - `rd-476-assistant-prompt-s101o` = `f9649dcf9d30ea12af58ff60007b0c67318866fd`
     - `rd-856-user-pattern-verb-guard-s101o` = `f4026fba5598ad5355b1daf21def9b651ee7bdc9`
     - `rd-857-whole-word-skip-list-s101o` = `1da0bd4684b804ccbb36f358e246759ed9a5ef8c`
   - `rd-460-c170-turn-s101o` = `f15217cba52a97cfa55cea2155e14d690c2bd87e`.
   - `refs/pull/91|92|93|96/head` equal their heads.
2. **Chain** (`cat-file -t`, `rev-parse ^{tree}`, `log -1 --format=%P`, `merge-base --is-ancestor`):

   | commit | tree | parents |
   |---|---|---|
   | `888203c` | `428f042b34fb…` | `2facd7c` + `5eb80a7` |
   | `5eb80a7` | `2d2caa3f6106…` | `537741c` + `36a0dc0` |
   | `36a0dc0` | `fb8197a78a94…` | `7f1881e` + `c7ca0ed` |

   - The is-ancestor chain holds.
   - `be0fe37` is not an ancestor of `888203c`.
   - `merge-base(888203c, each of A/B/C)` = `c7ca0ed`.
3. **Merges onto `888203c`** (legacy `merge-tree c7ca0ed 888203c <head>`, 07:18:55, git 2.54.0; `.git/objects` 44 before and after, newest mtime unchanged):
   - **A:** rc 0, 348 lines. Three changed-in-both sections: preload and `model-config.js` have no markers; the counts file has markers.
   - **B:** rc 0, 161 lines. `server.js` has no markers; counts has markers.
   - **C:** rc 0, 380 lines. `server.js` has no markers; counts has markers.
   - Main's `server.js` hunks (:795-:988, :14643-:18439) do not overlap B/C's (:7420-:8153).
4. **Prompt** (node regex extraction): `SYSTEM_PROMPT` is 7686 chars, `666399e1…` at both `c7ca0ed` and `888203c`; 9956 chars, `f36881dd…` at `f9649dc`.
5. **Counts** (`git show <c>:scripts/verify-expected-counts.json`):
   - `888203c`: 4660/291, blob `f3f387b`.
   - The heads: 4594/288, 4566/288 and 4581/289.
   - `fd8ff2a` and `f15217c`: 4807/298, blob `0e50ac0`.
   - **Predictions at `888203c` (arithmetic): V1 4695/292; M0+B 4667/292; V2 4682/293; V3 4717/294.** The launcher recomputes these in-guard from M0's own counts.
6. **Provider premise (r10P)**, at `888203c`:
   - `model-config.js` :8-:9 says `LLM_PROVIDER=ollama now resolves to azure-openai with one boot warning.`
   - The preload's `checkDeployment` stand-in exists only for `azure-openai` (:84).
   - `aiTuning_${provider}` appears at `server.js` :1896 and :1916.
   - The suites still set `LLM_PROVIDER: 'ollama'`: rd476 :85, rd856 :76, rd857 :98.
   - The override cell sets `KEY = 'aiTuning_ollama'` (rd476 :204).
7. **D's scope:**
   - `rev-list --count fd8ff2a..f15217c` = 1, with no merges. `fd8ff2a`'s parents are `88153c0` + `888203c`.
   - The numstat lists exactly the 4 paths. 0 paths fall outside `__tests__`. The counts, package, lock, deploy-demo and `marketplace-package-build.sh` blobs (`40ec7de3`) are unchanged.
   - `/__tests__/helpers/` is in jest's `testPathIgnorePatterns`.
   - D's paths ∩ A/B/C's paths = 0.
   - All 19 gate-26 suites exist at `f15217c`: 16 blobs equal `fd8ff2a`'s, and the 3 touched suites differ.
8. **D's equivalence** (my re-derivation in node, using the real constants from `f15217c`):
   - For all 7 whole-regex site/input pairs, old `.source` equals new `.source`. Both match the literal line, and both reject dots→x, one-dot→X, slash→Z and first-char-dropped.
   - Control: `"a+b\c.d"` is not matched by the dot-only escape and is matched by the full escape.
   - Second control: an unescaped `DEV` matches its dots→x line, so the comparator can see a wildcard.
   - **The builder counts "9 site/input pairs" because it lists #269's type and #270's image separately. That is a counting difference, not a disagreement.** This is METHOD for d1; the gate re-derives it.
9. **D's CodeQL** (`gh api`, 07:22:10):
   - Analyses at `f15217c`: js/ts `1976695201`, python `1976690395`, actions `1976689801`, all with results 0. At `fd8ff2a`, js/ts `1976472415` had **results 6**.
   - Open alerts on `refs/pull/96/head`: 0.
   - **#266-#270 are `js/incomplete-sanitization` and #271 is `js/incomplete-hostname-regexp`** (warning / high). Each one's instance on the PR ref is `fixed`, and none has an instance on main.
   - PR #58 control: 4 alerts, all fixed.
   - The check runs on `f15217c` all completed/success: CodeQL, the three Analyze runs, build, arm-ttk, scan and audit.
   - **PR #96 is open, NOT a draft, and `mergeable: true`.**
   - #91's Build `117653610831` is now success.
10. **READY copies:**
    - Source: AgentMail GET of `tuesday-agent@`, field `text`, made inside `python3 -I` (key read by name, never printed).
    - Staged in the scratchpad, written with the Write tool, then re-hashed and compared with `cmp`: identical.
    - Each copy's sha256 also equals the builder's own file: `mail-21-ready-rd476-r2.txt`, `mail-10-ready-rd856.txt`, `mail-14-ready-rd857.txt` and `mail-28-ready-c170-delta.txt`.
    - Message times:

      | copy | time |
      |---|---|
      | RD-476 r2 | 2026-10-18T10:38:33Z |
      | RD-856 | 03:45:49Z |
      | RD-857 | 05:25:01Z |
      | C-170 delta | 20:15:22Z |

11. **Floor:**
    - `/Volumes` = Laptop-DEV, Macintosh HD, Recovery (T9 unmounted).
    - Load 7.25 at 07:17.
    - Tools unchanged: lock `3c33f5ae`, c57 `1ae84a10`, c133 `6f938bfc`.
    - Node v26.8.1; gitleaks 8.30.1.
    - Gate 27's report line 3 reads `STATUS: IN PROGRESS`.

**Observations for Tuesday (not amended, or only partly):**
- **The kit's instrument list was wrong for two files.** `qa-lockcheck.py` and `qa-names23.py` are **not** in gate 26's `inst/`; they are in gate 25's (and gate 24's). I corrected the §3a source list, and the launcher checks them at gate 25's path.
- **The alert objects' top-level `state` read `null`** through `--jq .state`. The instance list is what carries `fixed`. Row d5 tells the gate to read both.
- **The launcher's merge-tree marker parser was proven on the real counts conflicts only.** I did not plant a non-counts conflict, because that would need new objects. The gate's own r1 control (a planted `model-config.js` conflict in its store) covers it.
- **`.git/objects` holds 44 files** (gate 27's amender read 35). S101O is live, so the gate accounts for any change.

## 4. Launcher verification (quoted)

- `bash -n /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate28.sh` gives rc 0.
- **Earlier `--check` runs** refused on three gaps, which I fixed:
  - the kit did not quote ANSWER-18's *"RD-794 land ACCEPTED, no delta gate."*, so I added it to AMENDMENT 1;
  - the kit did not carry `package.json`'s full sha, so I added it to WRONG 16;
  - the prompt did not carry `C57_ROOT`, so I added it to property (4).
- **Final `--check`**, run with the kit still slotted (`/bin/bash … --check`, exit 40):

```
NOTE: the Laptop-DEV jest lock is held now by 'qa-g27-C1' (FIFO; the gate waits behind it)
NOTE: no tmux pane named 'Datasec/NexusAI-M' — not a negative control this launch
NOTE: no tmux pane named 'Datasec/NexusAI-N' — not a negative control this launch
NOTE: no tmux pane named 'Datasec/NexusAI-P' — not a negative control this launch
NOTE: no tmux pane named 'Datasec/NexusAI-R' — not a negative control this launch
NOTE: fleet-monitor has no single live claude — not a negative control
NOTE: QA/NexusAI-gate27 has a live claude — added as a negative control (FIFO, never touched)
guards pass (9 MODEL 40 18T 18 6 18M 7 8 90 91 22 93 70 70N 31 10 17 11 12 13 14 15 20 41 82 19 24 53 71 76 77 78 79 38R 86); stamp and/or route NOT complete.
  ls-remote attempts this run: 1 (C-192); origin main 888203c (M0 888203c tree 428f042; ancestry carries 36a0dc0/fb8197a, 5eb80a7/2d2caa3, 888203c/428f042; C-170 not on M0); RD-476 f9649dc; RD-856 f4026fb; RD-857 1da0bd4; C-170 delta fd8ff2a->f15217c; conflicts onto M0 = counts only x3 (legacy merge-tree); M0 counts 4660/291 -> predicted V1=M0+A 4695/292 · M0+B 4667/292 · V2=M0+B+C 4682/293 · V3=M0+A+B+C 4717/294; lock tool 3c33f5ae58e1…; c57 1ae84a108334…; c133 6f938bfcf255…; READY copies 4/4 sha256 match; model UNSTAMPED
  PROVISIONAL (unstamped slots, --check ran against): MODEL(unstamped) MAIN(unstamped: guards ran against origin main 888203c8c50e) REPORT_DATE(unstamped)
  NEG seats (38R, derived live; coordinator pane 'tuesday'): `78171` (Datasec/NexusAI-O); `53331` (tuesday); `64607` (QA/NexusAI-gate27);
REFUSING (32S): 17 at-sign SLOT placeholder(s) remain in the brief (MAIN pin x2 + tree + landed, MODEL, REPORT_DATE x2, RULED: T1-T8, the SELF-CHECK line and the Self-check note), or the SELF-CHECK line is not in the fleet's form — the coordinator re-reads end-to-end and stamps them before launch
REFUSING (40): no 'QA/NexusAI-gate28|tuesday-agent@agentmail.to|no' line in /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/inbox_routing.conf — answers to the gate would have no route; Tuesday adds it at stamp (this launcher never writes it)
EXIT=40
```

**Controls on the stamped path.** These used scratchpad copies only: a stamped copy of the kit and a copy of the launcher pointed at it plus a scratch routing file. The real kit and `inbox_routing.conf` were untouched.

| test | result |
|---|---|
| Positive: stamped with main `888203c`, tree `428f042`, model `claude-opus-5-5`, date 2026-10-19 | `all guards pass`, exit 0, report path resolved to `…/reports/2026-10-19-gate28-batch-rd476-rd856-rd857/report.md` |
| Negative: wrong stamped tree | `REFUSING: M0 888203c's tree is '428f042b34fb', not the stamped tree '111111111111'` |
| Negative: unknown model | `REFUSING: the stamped MODEL 'claude-opus-9-9' is not one of models_latest.json's sonnet/opus ids (claude-sonnet-5-5 claude-opus-5-5) …` |

**What the launcher refuses on:**
- **Origin main ≠ the stamped MAIN pin.** The PIN-HEADS MAIN row and the MAIN-STAMP line must also agree.
- **Main's chain:**
  - 888203c, 5eb80a7 or 36a0dc0 missing from M0's ancestry, or their trees wrong;
  - M0's tree ≠ the stamped tree;
  - any C-170 commit on M0, or `arm-ttk.yml` present;
  - M0 ≠ 888203c while the stamp says `landed since 888203c: none`.
- **Heads:**
  - any branch ≠ its pin;
  - the A/B/C chains or the stack broken;
  - D not `f15217c` on `fd8ff2a`.
- **Merge and file sets:**
  - a both-sides set changed;
  - the legacy merge-tree showing markers outside the counts file;
  - D touching a product path.
- **Content premises:** the counts, blob, prompt, provider, helper and mutant-anchor checks.
- **The 19 suites:** any of them absent.
- **READY copies:** any sha256 mismatch.
- **Rulings and quotes:** the carried rulings and the ANSWER/CLARIFICATIONS quotes (each grep'd in both the source and the kit).
- **Instruments:** tool pins, or instrument files absent.
- **Machine:** the T9 mounted.
- **Stamp and route, LAST:**
  - any at-sign SLOT left in the kit;
  - the route line missing;
  - the report already existing.

## 5. Left for Tuesday

**At-sign SLOT placeholders remaining in the kit: 17 occurrences, 15 names.**

| slot | where | fill with |
|---|---|---|
| `SLOT:MAIN_SHA` ×2 | MAIN-STAMP line, PIN-HEADS MAIN row | origin main at stamp (the same sha in both places) |
| `SLOT:MAIN_TREE` | MAIN-STAMP line | `git rev-parse <sha>^{tree}` |
| `SLOT:MAIN_LANDED` | MAIN-STAMP line | `none` if `888203c`; otherwise what landed (e.g. RD-778) |
| `SLOT:MODEL` | MODEL line | a bare ID from `models_latest.json`: `claude-sonnet-5-5` or `claude-opus-5-5` (tier 2; your call) |
| `SLOT:REPORT_DATE` ×2 | T4 and §11 | the same `YYYY-MM-DD` in both |
| `SLOT:RULING_T1` … `SLOT:RULING_T8` | TUESDAY'S RULINGS | "default" or the ruling. **T2 now also decides D's coverage** ((a) the 19 suites only, (b) plus a full verify of `f15217c`) |
| `SLOT:SELF_CHECK_STAMP`, `SLOT:SELF_CHECK_NOTE` | top | LAST, by hand; keep the fleet form `SELF-CHECK: re-read end-to-end for contradictions | …` |

**Route line.** Add this exact line to `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/inbox_routing.conf`, directly after gate 27's line, which is the file's last line at :233 (233 lines). The new line becomes :234. I did not edit the file.

```
QA/NexusAI-gate28|tuesday-agent@agentmail.to|no
```

**Sequencing:**
- **If RD-778 lands before you stamp:** stamp its main in the MAIN-STAMP line and name it in the landed field. The launcher recomputes the predictions and re-checks the conflict sets against it.
- **If C-170 lands first:** the launcher refuses. ANSWER-19 holds C-170 behind this gate.
- **If any head moves (including a new PR #96 head):** re-pin the kit and the launcher together. Never `sed` a sha blindly.

## 6. Hard limits kept

- **NexusAI repo:** read verbs only, with `--no-optional-locks`, plus the legacy stdout-only merge-tree. No fetch, worktree, checkout, commit or `--write-tree`. `.git/objects` was 44 files before and after.
- **gh:** GETs only.
- **AgentMail:** GETs only (1 listing and 4 messages); the key was never printed.
- **No HTTP** to any live or hosted host.
- **Datasec only.** I read only the files the commission, the kits or the launchers name. I globbed no shared fleet folder for other clients' material.
- **Scratch work** was in my session scratchpad only: the staged mail bodies, measurement scripts, the equivalence driver, and the stamped-copy launcher tests.
- **Nothing launched, mailed or published.** `inbox_routing.conf` was not edited.
