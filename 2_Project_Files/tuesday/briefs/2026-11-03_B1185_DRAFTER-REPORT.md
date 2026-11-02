STARTABLE: YES (after Tuesday's stamp; the 7 Stamp slots and the last line are four underscores, 8 in all: `grep -o '____' <kit> | wc -l` prints 8, `grep -c -E '_{4}'` prints 8)

# B1185 DRAFTER REPORT (Sonnet drafter, routing row C8, model-routing.md:98) - SEAT-G309, MPS tier-2 gate of b1182

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-03_B1185_SEAT-G309_mps-377-boundary-row-gate-tier2.md` (66 lines, ASCII, 0 non-ASCII bytes by `LC_ALL=C grep -c '[^ -~]'`). Pane `Datasec/MPS-G309`, `BRIEF_SEAT_LEVEL=sonnet` inside the quotes, via `launch_when_cool.sh`, tool tree `.tools/b1185`. G309 was free (`grep -l -w G309` over the briefs: 0; G308 is taken by B1181).

## BLUF
A G2 gate kit for `b1182/mps-377-boundary-at-one-row` @ `89e907eb...` (one commit on main `314b53f6...`, one path, +14 -0), round 1 of 2 on the new class "web: quantity audit counted-set boundary row" (NO GO 0 before). The gate re-derives the row by hand from `quantityAuditModel.ts:100-107` BEFORE reading the kit's derivation, plants PA (`> 1`), PB (`>= 0`), PC (`counted.length < 1`) and PD (`!== 0`, green by design) in its own clone and prints the red rows, runs install/lint/typecheck/test/build at the merge against a base tree, does the census (one path, +14 -0, ASCII, no ticket key or plant id in added lines, product bytes 0), and writes pr-title, pr-body, squash-subject, squash-body (exactly one trailer) and counts.txt on GO. Hosted CI and CodeQL are marked NOT RUN.

## Facts re-measured by me (instrument, then control)
- `git ls-remote origin` and `gh api -X GET git/ref/heads/main` at 06:42 AEDT (`date`): head `89e907ebef17b6b32645aa6983bd50a5e10e77e7`, main `314b53f6ddaaa9005e1015479882ff35e33b631e`. `compare main...head`: ahead 1, behind 0, 1 file, +14 -0; `compare main...main` side: `identical`, 0 files. Open PRs 121, 120. `matching-refs/heads/b1185` 0 (control `b1093` 1).
- Blobs by `git hash-object` of raw `gh api` bytes: main test file `cf83ed2f...` (470 lines), head `9bc39b7a...` (484 lines, the API `.sha` agrees); model `28b9fb44...`; `QuantityAudit.tsx` `d9519c4508...`; `ci.yml` `212b0da1...`.
- Pointers by `awk NR`/`grep -n` over the raw bytes: model `:100`, `:104`, `perDeviceOf` `:17-20`, `isFlagged` `:23-26`, anchors each count 1; screen `:14`, `:76-80`, `:89`; head test `FLAG :41`, `NO_DEVICES :42`, `INVENTORY` keys `:47 :48 :51`, row `(c5)` `:157`, comments `:153-156`, `(c3) :130`, `(c4) :143`, `(d) :167`; `ci.yml :1 :45 :46 :58 :61 :62 :63 :66`; `package.json :12 :14 :16 :17`; `CLARIFICATIONS.md :758 :774 :2214 :2218` printed; model-routing `:98 :109 :111`; `models_latest.json:23`; `brief_seat.sh:24`.
- `diff <(awk 'NR<152||NR>165' head) pin` prints nothing (control with range 153: prints 2 lines); `diff pin head`: 14 `>` lines, 0 `<` lines; non-ASCII in added lines 0 (control 0xC3 line reads 1); `MPSCALC|B11|G30` in added lines 0 (control 1).
- Head commit (local object, `cat-file -t` commit): subject 84 chars, `%G?` N, trailer `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>` via `sed '/^$/d' | tail -n 1`. Its body makes plant-count claims (PA 2 of 20, PB 4, PC 10, PD 0 red): relayed, the gate checks them at Step 7.
- Class count: 355 STATUS first lines, 89 hold `GATE VERDICT`; class-name filter 0; control `zero-quantity device line` 1; ` NO GO @ ` 11.
- Panes at 06:43: tuesday, NexusAI-N93, Security-Composer-G308, MPS-M85, MPS-G307, fleet-monitor. Load 8.89 10.03 7.97 (above 7). `df -g` 244 GiB. Ports listed, none ours. Node 24 copies print v24.21.0 (b1125, b1146); gitleaks 8.30.1; b1125 `heavy.sh hb.sh jira_read.py node24` exist.

## D-decisions
- D-1 Judged as a merge into main (main equals the pin today, so head tree = merge tree); MAIN-MOVE reruns on a later main.
- D-2 No "unedited pin constant" cell as in B1179: this row is new, so the red-first proof is the planted faults (the product owner's 2026-11-02 ruling, `CLARIFICATIONS.md:2214-2218`). Instead I added a before-picture: PA run once on the main test file (no new row) to print the gap the row closes (builder claims only the seeded sweep).
- D-3 The hand derivation is written by the gate from source BEFORE it reads the kit's derivation, then printed side by side (Step 3a).
- D-4 PD is required GREEN by design (item 2, the sign, not built); the new row going red under PD is a Blocker (it would pin the sign).
- D-5 Gate may not run a 13th plant (`> 2`); that cell is reasoned only (Step 5).
- D-6 The word census is narrowed to what this row can actually do: the added strings are already-existing on-screen texts used as test literals; the gate proves they exist at main, that the title/comment prose reaches no non-test surface and no `web/dist`.
- D-7 Landing text may reuse the head's 84-character subject only if every word is traced; plant ids and `hosted`/`CodeQL` words barred from bodies with greps and controls.
- D-8 Rule L copied from B1179 (120 s between load reads, wait for any other seat's `heavy.lock`/`light.lock`), naming G307 (`.tools/b1179`) and M85 (`.tools/b1180`) as the locks to wait for; their trees and `.tools/b1182` are read-forbidden.

## Q for Tuesday (each with a default)
- Q-1 Target READY 150 and hard stop 240 minutes, with the S5 clock yours? Default yes.
- Q-2 Is a 13th plant (`> 2`) wanted? Default NO (reasoned only).
- Q-3 Builder's `rm -f /dev/null` correction (failed, removed nothing) and record-order defect: Note only? Default Note.
- Q-4 The builder's note of 4 Dependabot alerts on the default branch: not the gate's; do you want a separate ticket? Default: mention in FOR TUESDAY only.

## UNMEASURED (by me)
Nothing installed, built, run or planted; the head file was read as raw text and diffed. Not measured: the plants' outcomes and received tables (verdicts in the kit are readings of `:100-107`), that the row is green at the merge, the whole suite and build, the standing heavy/light locks (my `ls` glob aborted under zsh and printed nothing usable; the kit tells the gate to list them with `bash -c`), MPSCALC-377 Jira state at gate time (I ran no Jira reader), the other PRs' file lists, the hosted runner, hosted CI and CodeQL.

## Outside the fences (disclosure)
No fence broken. Reads beyond my two files: DRAFTER_RULES, the B1179 gate kit and DRAFTER-REPORT, the B1182 builder kit and its STATUS in `Briefs/` (commissioned), `model-routing.md` lines, `models_latest.json:23`, `brief_seat.sh` lines, `CLARIFICATIONS.md` lines 758 774 2214 2218, the first lines of all `Briefs/*_STATUS.md` (355 files) into my scratchpad, `tmux list-panes`, `lsof`, `uptime`, `df`, `ls -d` of `.tools/b1179 b1180 b1182 b1185` and `.tools/b1125` names (not opened), `gitleaks version`, `node --version` of two copies. `gh api -X GET` only (ref, compare, pulls, matching-refs, raw contents of the test file at two refs, model, `QuantityAudit.tsx`, `ci.yml`, `package.json`) under the project's `GH_CONFIG_DIR`; read-only git verbs in `R` (`ls-remote`, `cat-file`, `log`). No `cd`, no Jira helper, no card store, no mail, no git write.
