# Gateset 2026-10-05_gate62 — README for Wednesday

Drafted 2026-10-05, 09:15Z – 09:5xZ UTC (20:15 – 20:5x AEDT), by a drafting subagent. Every figure names the kit file it came from. Every builder statement below is a CLAIM the gate re-measures; the kit says so in the prompt.

## 0. What this gate is, and its status

**gate62 is a T2 gate over ONE Secuura/Blockchain PR: #1387, KS-1388 §1 only, "both observability env examples point the nginx status URI at :80".**
- The PR NARROWS the ticket. §2 and §3 are untouched, and KS-1388 does not move to Done on this PR.
- Author: Seat B 61st, **WRAPPED** 09:11:57Z. Merger: the B successor, named by Wednesday.
- **GO string (placeholder kept on purpose; it names no wrapped seat):** `GO (Seat <B successor>): merge 1387 on gate62`
- **NO GO string:** `NO GO (gate62): 1387 at 67324c7604fd — <N-1387-n: the blocker, one line>`
- **The head is SINGLE-PARENT on develop**, with no merge-in. Re-measured by the drafter (`c1_pr1387_ex1.out`, rc 0, 9/9 at 09:2xZ):
  - head `67324c7604fd871637b197395139841da9913122`
  - branch `feature/ks-1388-observability-env-examples-status-uri-80-b61-1`
  - parent `f01c1da5717f` == develop (by ls-remote at 09:17:06Z)
  - **END_TREE `fd6eb92cf942ddae9d63fcff94062666d996cc28`**, measured. C1 P4 also asserts the fabricated `0c0f8e5e…` is absent, and the prompt forbids using it.
- **5 paths, all measured:**

  | path | +/- | mode |
  |---|---|---|
  | the KS 971 suite | +16/-0 | 100755 |
  | `observability/.env.example` | +2/-1 | 100644 |
  | `observability/config/alerting.env.example` | +2/-1 | 100644 |
  | flow doc | +92/-0 | 100644 |
  | cheat doc | +35/-2 | 100644 |

**Status: KIT COMPLETE, NOT LAUNCHED.**
- Every helper has a positive control and must-fail arms, and every arm fired (section 3).
- The dry run returns rc 0 and reports only the routing line as missing (section 5).
- Two things are Wednesday's: the routing line (section 4) and the launch (section 7).

**What the drafter did:**
- **Writes:** only inside this directory.
  - `_scratch/clone` is a `git clone --shared --no-checkout` of the checkout, 192 KB. Its alternates point at the checkout's objects, which are read only.
  - SIM commits, trees and blobs went into that clone's object store only. No ref was written and nothing was fetched.
  - Temp indexes were moved to `sim/_quarantine_*`, never removed.
  - Python wrote `__pycache__/` here on import.
- **In `/Volumes/DevMASTER/!CODING/`:** read verbs only (`ls-remote`, `show`, `log`, `diff`, `ls-tree`, `cat-file`, `rev-parse`, `rev-list`, `grep`), plus the clone source read.
  - The checkout's working tree carries 3 untracked `systemTest/akto/...` files that the drafter did NOT create. They were there at first read.
- **Network:** GitHub REST GETs only (pulls/1387, its files, the open-PR census). GH_TOKEN was read by name and never printed.
- **Not done:**
  - no Linear read (X8 is the gate's)
  - no worktree, no suite run, no npm (C3 is the gate's)
  - no launch, no routing edit, no mail, no `rm`

## 1. Drafter predictions at 67324c7604fd over f01c1da5717f (the gate re-derives every one)

| check | file | result |
|---|---|---|
| C1 pin | `c1_pr1387_ex1.out` (rc 0, 9/9) | **P1** origin pull/head == branch == head; develop unmoved. **P2** one parent. **P3** the 5 paths with exact +/-. **P4** END_TREE `fd6eb92cf942` (control: develop tree `ba3527224ff6` differs; `0c0f8e5e` absent). **P5** trailers 1 raw byte (control `bf277eead268` 55). **P6** Co-Authored-By 0 (control 1). **P7** subject 74 chars, no `(#`. **P8** ONE `Refs KS-1388`, only KS-1388 hyphenated. **P9** modes as above. **Real control** `c1_basehead_ex1.out` (develop as head): rc 1, FAIL P2 P3 P4 P7 P8 |
| C2 applied == held | `c2_pr1387_ex1.out` (rc 0, 5/5) | **H1** held patches sha256 `e50bdc17f06010fe` / `e89345ec73eeef75` == the brief's P9. **H2** strict apply rc 0 both; independent tree `04d226e93b48`, == the tree the docs and body cite. **H3** test file byte-equal to the head. **H4** each env example == held hunk **+ exactly one added `# KS-1388:` line**; control: the apply differs from develop. **This contradicts both docs (D3)** |
| C3 suite / red-first / tampers | NOT RUN (the gate's) | the prompt prescribes red-first by content, a per-cell cross-control, three tampers and the shell-suite totals at both ends. **Drafter's READ:** each cell is exact string equality on the FIRST `SECUURA_NGINX_STATUS_URI=` line of its file (`grep -m1`). The `# KS-1388:` line does not contain that string, so it is not read. A second, uncommented `:6882` line appended after it would stay GREEN (D5; predicted, not measured). A missing file → empty `got` → FAIL (fails closed) |
| C4 docs | `c4_docs_pr1387_ex1.out` (rc 0, 8/8) | **D1** skill blob `eaf43dfd4d98` at develop. **D2** one commit, 0 platform-s. **D3** flow = ONE 92-line insert at the `  </body>` line (develop :2158); close tag kept. **D4** flow h2 [1..13] → [1..14], new h2 `14.` (KS-1388), h3 14.1–14.4. **D5** cheat = 2 one-line replacements (develop :3800 `the three cells`, :3830 `the nine cells`), each ONLY the suffix `, host Kamil's Mac Studio (2)` before `</td></tr>`, + ONE wrapped `&mdash; KS-1388` section before `  </body>` (:3849). **D6** both blocks self-contained. **D7** timing zeroes reproduce exactly: run-shell-suites 0/0, shell suite 0/0, prometheus_targets 0/1, must-hit `auth` 71/70. **INFO D8:** `Kamils-Mac-Studio` 3 / `Kamil's Mac Studio (2)` 3 in EACH doc; cheat row `the six cells` has date + host and NO duration |
| C4 predict | `c4_selftest_ex4.out` | unmoved develop → **== END_TREE** (positive control). SIM develop (synthetic 18. KS-1210 block on f01c1da) → number-order tree `8ec810c3a68a`, 14. above 18. in both docs; reverse-order control `531fdf8ff414` differs |
| C5 PR text | `c5_pr1387_ex2.out` (rc 0, 7/7) | `**Refs KS-1388**` + URL; 0 closing refs (body, title, commit message); only KS-1388 hyphenated; title == subject; narrowing stated (§1 only, §2/§3 untouched, live sweep, not Done, "NOT run"); 0 Co-Authored-By; no fabricated tree. Body 4,991 B (`api/pr1387_body.md`). `_ex1` = **instrument history**: 3 false FAILs from the drafter's own regexes (bold `Refs`, "NOT run" wording, the apply-tree `04d226` read as END_TREE), corrected in the open, with new arms added |
| census | `census_ex1.out` (rc 0, 09:27:26Z) | 25 other open PRs. **0 OVERLAP** on the test or either env example, or on KS-1388 in a title (control FIRES on #1387). 4 DOCS, all expected: #1382 (19.; head moved again at 09:33Z to `ba3598df64f7`, see section 5), #1383 (22., **head moved to `32e8459bc0f5`**, round 2), #1384 (18.), #1385 (KS-938, 20.) |

**Drafter's reading.** Every artefact claim in the builder's mail that the kit can read without running the suite reproduces:
- head, develop, END_TREE `fd6eb92cf942`
- 5 paths +/- and modes
- 0 trailers / 0 Co-Authored-By
- 74-char subject, `Refs`-only
- doc numbering 1..14
- both host fixes are suffix-only
- the timing zeroes 0/0, 0/0, 0/1 with control 71/70
- held == applied for the test file

**One builder-adjacent claim does NOT reproduce:** the docs' "all three files `cmp`-equal" (D3).

## 2. Doubts for the GATE to rule (the prompt carries D1–D8), and claim contradictions

- **D1 TIER: T2 confirmed by the drafter.**
  - The two `.example` files are read by no process. `observability/.env.example:6` and README :211/:226 document a `cp` to `.env`, and in that copy the changed line is still a comment.
  - So a runtime effect needs a human to uncomment it, and then it yields `:80`, compose's own default (`observability/docker-compose.yml:331`).
  - The rest is two test cells and docs. No auth, data, migration or service path.
  - The diff gives no reason to raise it to T1.
- **D2 HOST SPELLING (builder-flagged, not fixed).** Each doc carries `Kamils-Mac-Studio` 3× (precedents, incl. cheat :3753) and `Kamil's Mac Studio (2)` 3× (the two fixes + the new block).
  - It is likely the same Mac (hostname vs ComputerName), but that is unmeasured. The gate may read `scutil --get ComputerName` / `hostname`.
  - **OBSERVATION, not a blocker.**
- **D3 "applied == held … all three `cmp`-equal" is FALSE as written in BOTH docs** (flow 14.3, cheat `applied == held` row).
  - The PR body says it correctly: the suite file is equal, and each env example differs by exactly the `# KS-1388:` line.
  - `c2_pr1387_ex1.out` measures the body's version.
  - It is a false sentence in client-facing docs. Severity and blocking are the gate's to rule. A fix is a new head (re-gate) or a follow-up.
- **D4 `the six cells` row** (cheat; flow 14.3 has the same prose): it names a date, host and bash version but **no duration**.
  - §4 says "State the figure, the date … and the host".
  - 14.4 says no stated timing covers this suite, so arguably no figure is owed. Rule it.
- **D5 The cells pin only the FIRST `SECUURA_NGINX_STATUS_URI=` line** (`grep -m1`). The prompt's tamper (f) measures it. Likely polish for §1.
- **D6 Q-M ordering.** Four open PRs append later blocks: 18. #1384, 19. #1382, 20. #1385, 22. #1383 (Kam HOLDS #1383 until the KS-1404 anchor wiring merges).
  - Any landing first means #1387 needs a docs-only merge-in, with 14. ABOVE them in both docs.
  - `c4 predict` does this and was proved on a SIM.
- **D7 PREFLIGHT-INCOMPLETE 12/15** (legs 3, 4, 8: no stack). The builder says so and does not call it a pass. Acceptable named residue for T2? The gate may run preflight (X1).
- **D8 `# 67 suites`** (both docs' run line) vs "67 passed … (of 67)": are these suites, or files? The gate re-measures.

**Claim contradictions found by the drafter:**
1. The docs' "all three `cmp`-equal" vs the body's and c2's "env examples + one line" (D3).
2. The builder's first READY quoted END_TREE `0c0f8e5e…` (fabricated). The corrected `fd6eb92cf942` is what the drafter measures. Recorded only, never used.

**Consistent, for the record:** everything else in section 1's reading.

**For Wednesday (not the gate's):**
- **W1.** The GO names `<B successor>`. Fill it when you sign, and never with B 61st.
- **W2.** If any of #1382 / #1383 / #1384 / #1385 lands before #1387 merges, the merger builds a docs-only merge-in.
  - Copy gate59/61's approach: ONE merge of develop into the branch, both docs resolved in NUMBER order, 0 trailers. The ruling goes under a **Q-M section** in that seat's brief.
  - The GO covers that new head only if `c4_docs_gate62.py qm --merge-in-head M --develop-after <develop>` passes M1–M7, run by the merger or a gate. Otherwise it re-gates.
- **W3.** A launch after develop moves refuses (rc 10, and the launcher rc 17). Launching NOW (develop `f01c1da5717f` unmoved at 09:4xZ) is the clean window.

## 3. The kit's instruments (each exercised; outputs beside it as `<name>_exN.out/.err/.rc`)

| script | what it does | positive control | must-fail arms (all fired) |
|---|---|---|---|
| `lib_gate62.py` | `git()` READ verbs only (raises otherwise; `config` only with `--get`); `wgit()` write verbs only outside `/Volumes/DevMASTER/!CODING` (lexical + realpath); GH GET with the token by name; `Tally` (prints `CHECKED n`, rc 1 on 0 checked); `G62_SCRATCH` routes fixtures / SIM output to the caller's scratch | — | refusal arms in c2 / c4 below |
| `c1_pin_gate62.py` | P1–P9 | `c1_pr1387_ex1` rc 0; T0 | `c1_selftest_ex1` **19/19**: base-as-head, a 6th path, +/- drift, a missing path, two parents, the FABRICATED tree, tree == develop tree, a trailer, a blind trailer control, Co-Authored-By, a blind co-author control, `(#1387)`, 93 chars, a second Refs, KS-971 hyphenated, the test at 100644, develop moved, pull/head moved. Real control `c1_basehead_ex1` rc 1 |
| `c2_held_gate62.py` | H1–H4 (temp index in the caller's OWN clone) | `c2_pr1387_ex1` rc 0; T0 | `c2_selftest_ex1` **4/4**: a held carve with port 8080 (H4), a hash mismatch (H1), and a refusal: apply into the SHARED checkout → rc 2 before any write |
| `c4_docs_gate62.py` | docs D1–D8, predict, qm M1–M7 | `c4_docs_pr1387_ex1` rc 0; T0 on the REAL blobs; predict on the unmoved develop == END_TREE | `c4_selftest_ex4` **23/23**. Docs arms: 14→15, duplicate 13, an older-block line edited, close tag rewritten, the host suffix misspelt, a THIRD row edited, the cheat block unwrapped, the cheat block numbered, live sweep removed, run line removed, timing must-hit blind, timing claim mismatch. Q-M arms on SIM commits: 14 below 18 (M1), single parent (M2), an extra non-kit path (M1+M3), Co-Authored-By (M4), develop touching `.env.example` (M6), two new commits (M2+M7), predict REFUSES that develop. Also `c4_refusal_ex1`: predict into the shared checkout → rc 2. History: `_ex1` = an INERT arm (the live-sweep tamper landed in an OLDER block), fixed by requiring every tamper anchor to occur EXACTLY once (`_ex2` caught a second non-unique anchor, `_ex3` 13/13 docs-only) |
| `c5_prtext_gate62.py` | T1–T7 + FIG info | T0 synthetic clean body | `c5_selftest_ex2` **15/15**: Refs removed, a second Refs, URL removed, "does not close KS-1388" (negation still closes), `Fixes KS-1388` in the commit message, `closes #1387`, KS-971 hyphenated, `(#1387)`, §2/§3 statement removed, live sweep removed, Co-Authored-By, the fabricated tree, a wrong END_TREE, bold + bare Refs |
| `gh_census_gate62.py` | open-PR census (OVERLAP / DOCS) | `census_ex1` control FIRES on #1387 | `census_selftest_ex1` **6/6** |
| `launch_qa_secuura_ks1388_1387.sh` | the launcher: static prompt; re-reads origin; refuses a moved head (6) or develop (17), no TTY (21), overrides (16), kit / prompt defects (8) | `--check` rc 0 (section 5) | `launcher_arms_ex1.out` (section 5) |
| `repin_and_launch_gate62.sh` | the launch action, steps 0–7 | `--dry-run` rc 0 | short sha 9, wrong PR 9, wrong head 11 (section 5) |
| `prompt_gate62.txt` | the gate's prompt | — | — |

`fixtures/`, `sim/`, `api/` and `_scratch/` are drafter exercise output. They are never launched.

## 4. Routing line — NOT added
Back up the file first. Then add ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`:
```
QA/Secuura-ks1388-1387|coagent@agentmail.to|yes
```
Until it is present, step 0 of the real launch refuses rc 1. The dry run reports it instead.

## 5. Dry run and refusal arms
- **Dry run** `dry_console_ex1.out` (09:33:05Z) returned **rc 0**:
  - routing line reported missing
  - census: 25 others, 0 OVERLAP, 4 DOCS, control FIRES
  - API, pull/head and branch all agree with the input head
  - develop unmoved
  - launcher `--check` rc 0 (prompt sha256 `0871c7b6b178510c`)
  - **#1382's head moved between the census (80bafc849a54, 09:27Z) and the dry run (ba3598df64f7, 09:33Z):** a merge-in on that PR's branch. It is still docs-only, so it is not an overlap.
- **Launcher arms** `launcher_arms_ex1.out`, **9/9 as wanted**:
  - real `--check` 0
  - stand-in ls == pinned 0
  - develop moved 17
  - pull/head moved 6
  - no `ultrathink` 8
  - GO placeholder replaced by the wrapped seat 8
  - placeholder kept AND a wrapped-seat GO added 8 (the dedicated check)
  - head not in full 8
  - launch path with no TTY 21 (never reached `exec claude`)
- **Repin arms** `repin_arms_ex1.out`, **4/4 as wanted**: short sha 9, wrong PR 9, develop given as head 11, and a REAL (non-dry) run with a routing stand-in lacking the line 1. That last one refused at step 0, before any census, usage gate or cockpit call.
- **Final self-test sweep** (09:3xZ, `final_*_selftest.out`), each rc 0 with `CHECKED n` > 0: c1 19/19, c2 4/4, c4 23/23, c5 15/15, census 6/6.
- `_quarantine/final_gh_selftest.zsh-nosplit-instrument-error.out` is the drafter's own instrument error, kept rather than deleted: a zsh loop did not word-split, so 5 × rc 2 with nothing run.
- The shared checkout's `git status --porcelain` shows 17 untracked `systemTest/**` files, present before drafting. The drafter ran read verbs only there.

## 6. Re-draft recipe (the head or develop moved before launch)
1. Re-measure kit `head`, `branch`, `develop`, `develop_tree`, `end_tree`, `files` (+/-), `modes`, `head_blobs`, `flow_numbers_*`, and the census.
2. Edit the head / develop in `prompt_gate62.txt` and `launch_qa_secuura_ks1388_1387.sh` (they are static: no fill step).
3. Re-run every `--selftest`, then c1, c2, c4 docs, c5, the census, and a `--dry-run`.
4. A docs-only merge-in (develop moved because another docs PR landed) is a NEW head. Re-draft for it, or, after a GO on 67324c7604fd, judge the merge-in with `c4_docs_gate62.py qm` (M1–M7, Q-M).

## 7. How Wednesday launches it (after section 4's routing line)

**Facts the launch uses:**
- Pane: `QA/Secuura-ks1388-1387`
- Report dir: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-05-ks1388-1387-g62/`, with the verdict in `report.md`. `NOT-TESTED.written-first.md` is written first.
- Verdict mail subject: `[QA -> Wednesday] GATE62 #1387 (T2 KS-1388 s1: both observability env examples point the nginx status URI at :80; author Seat B 61st wrapped, merger <B successor>)`

**Launch commands.** Run them under `script -q /dev/null`, as gate58–61 were, so the TTY guard is satisfied:
```
script -q /dev/null bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate62/repin_and_launch_gate62.sh 1387 67324c7604fd871637b197395139841da9913122 --dry-run
script -q /dev/null bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate62/repin_and_launch_gate62.sh 1387 67324c7604fd871637b197395139841da9913122
```

**Exit codes:**
- rc 1: routing
- rc 9: input
- rc 3: API failure or a blind census control
- rc 15: OVERLAP
- rc 11: the head moved
- rc 10: develop moved
- rc 16 / 12 / 13 / 14: override / usage gate / `--check` / cockpit

Add `WED_USAGE_STOP=…` only with Kam's recorded authority.

**Rung 5 (verify the launch at rung 5 or 6, never below).**
- Ctx, an exit code or a pane existing proves nothing.
- Read the pane (`QA/Secuura-ks1388-1387`) and find content only THIS commissioned gate would produce, such as:
  - the agent naming **KS-1388 / #1387**
  - reading `…/gatesets/2026-10-05_gate62/README.md` or `QA_AGENT_CHARTER.md`
  - quoting head `67324c7604fd`
  - running a `*_gate62.py --selftest`
- **Rung 6** is `NOT-TESTED.written-first.md` appearing in the report dir.
- No such content after its first turns means it is NOT launched, whatever the ctx reads.
