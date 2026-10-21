BLUF: B423 brief drafted (SEAT-W13, narrow third fix round on PR #85). B358-1 is the required fix; B358-4, -3, -2 follow in that order, with -2 droppable. Read-only: no write, fetch or HTTP. Two Tuesday decisions are open (Q1 and Q2 below).

# B423 drafter report · 2026-10-21 ~21:55 AEDT

## Files
1. Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-21_B423_SEAT-W13_composer-pr85-fix-round3.md`. It has 3 stamp lines: REFUSE 2, the Model line and the READY format. `grep -c -E '@(MAIN_SHA|STAMP_TIME)''@'` prints 3, and the `.pre-stamp` control should print 3. The last line is `READ-WHOLE-BY-TUESDAY: PENDING`.
2. This report.

## Read, in order
- **B358 STATUS.** `/Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Briefs/2026-10-21_B358_STATUS.md` (82,828 bytes, modified 04:26), read whole. **The copy named first in the task (`/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-21_B358_STATUS.md`) does not exist**, so the project copy is the only one and there is nothing to compare. The brief says so.
- **B353 brief** (shape copied) and the tail and headings of the B353 STATUS. I did not read the B353 STATUS whole; the brief points the builder at it.
- **Card** `composer-pr85-round2-nogo-one-line-1021` via `decision_queue.sh show`: ruled option a at 2026-10-21T14:46:09+11:00. The label is quoted verbatim. Its detail says: "the one-line fragment split plus the bare-name pattern, and fixes the three Minors if they fit the same commit. A tier-2 gate then checks only that change."
- **Project `CLAUDE.md`** (33 lines, no merge or landing rules in it) and **CLARIFICATIONS** (grep only).
  - The rules that bind this round are K6 / C-92 and "never deploy to the demo without Kam's word".
  - The only `eaff2b7` mentions are in B341, B342, B344 and B330 (Tuesday's briefs). I found no L05 card text; L05 appears in CLARIFICATIONS only as a look row (line 1453).

## Measured (read verbs only)
| fact | value | instrument, time |
|---|---|---|
| PR #85 head | `e969ad38d9eb5508e356dff36f1c65000ab40667` | `gh api repos/datasecau/Datasec-Security-Composer/pulls/85 --jq .head.sha`, and `ls-remote` for the branch and `refs/pull/85/head` (same value), 21:48 |
| base / main | base `main`, base sha `308b7aa60cd8d2a8576b29e0422538cbaf140f24`; main now the same (unmoved) | same `gh api`, and `ls-remote origin refs/heads/main`, 21:48:06 |
| PR state | open, draft, mergeable true, `mergeable_state` clean, 12 commits, 57 files, +38809/-3186 | `gh api …/pulls/85` |
| check-runs at head | 3, all completed success: CodeQL, Analyze (javascript-typescript), Analyze (csharp). No `ci` run (draft). Combined status pending, 0 contexts. | `gh api …/commits/<head>/check-runs`, and `/status` |
| open CodeQL alerts | PR ref 0; main 0 | `gh api …/code-scanning/alerts?ref=…&state=open --jq length` |
| analyses at head | JS/TS `1989767829` and csharp `1989762358`, 0 results each | `…/code-scanning/analyses?ref=refs/pull/85/head` |
| line 68 of the qgate test | `packages/content/test/b330-sm316-qgate.test.ts:68` is the `constraint` pattern; the plant is at line 69 | `git --no-optional-locks show <head>:<path> \| sed -n 68,69p` (output cut to 12 characters on purpose, so the name is not copied into this report) |
| `AGENTMAIL_API_KEY` in project `.env` | 0 (control 1) | `/usr/bin/grep -c -i` |
| origin refs `b423*` / `b358*` | none | `ls-remote` |
| load, tmux, seats | load 1.25 1.34 1.66; tmux shows only the fleet panes; ps grep for `b3[4-9][0-9]\|b42\|pc-b` found nothing | `uptime`, `tmux list-panes -a`, `ps` |
| port block | 7650-7659 free: lsof rc 1; 0 briefs name a 765x port (control `771x` found 11) | `lsof`, `grep -l -w` |

7600-7609, 7640-7649 and 7690-7699 are named in other briefs, so I chose 7650-7659.

## UNKNOWN, with why and what closes each
- **The gate-33 launcher recognises `Datasec/Security-Composer-W13`.** Unknown because `fleet/qa-agent/launchers/` is outside the allowed read scope, so I did not open it. I took it from your task text, and the brief says the label is deliberate. Closing it: grep the launcher's recognised pane patterns for `W13`.
- **State of the L05 card and the `eaff2b74` deploy.** Unknown because the instruction forbids `decision_queue.sh list`, and no id was given. The brief says the deploy waits for L05 and is not this seat's, and marks the card's state UNMEASURED. Closing it: `decision_queue.sh show <the L05 id>`.
- **Weekly gauge and model-routing row.** Unknown because I did not read `models_latest.json` or the routing spec. The brief proposes row C3 (Opus) if B358-2 is in and C1/C2 (Sonnet) if it is struck, and leaves the receipt to you. Closing it: the P2/P3 gauge read at launch.
- **Whether the gate's kit (`.tools/b358/kit/`) is still on disk.** Unknown because `.tools/` is inside the code repo's tree, which I did not enter. The brief tells the builder to copy from it and, if absent, to rebuild from the gate's description. Closing it: `ls` on that folder.
- **The L1 content-release PR text** (`briefs/2026-10-21_B358_PR85-TEXT.md`) was not read. The brief tells the builder it is yours.

## Discrepancies I found
- The card's link says `datasecau/Security-Composer`. The repo that answers is `datasecau/Datasec-Security-Composer` (`git remote get-url origin` and every `gh api`). The brief uses the latter and says so.
- The gate's STATUS redacts the element name as `<schema pattern s10>`. I kept to that. The brief refers to it as "the middle alternative of line 68's second fragment" and never spells it. The builder gets the name by program from the round-1 tip, into `.tools/` only.
- The B353 brief said "mergeable_state clean", the B358 gate saw `blocked` then `clean`, and I now read `clean`. The head has not moved, so nothing turns on it.

## Questions for Tuesday, each with a recommendation
1. **Include B358-2 (the variant bypass) in this round?**
   - The card's detail says "the three Minors if they fit the same commit". B358-2 is the only one that edits product code (`secrets.ts`, inside `matchesDirectiveValue`). It forces the heavy differential, linear-time and db checks, and a larger tier-2 gate.
   - Recommendation: **keep it conditional and last**, as drafted. It sits in its own droppable commit with a written decision gate, and the READY line must say "B358-2 not done: <cost>" if it is dropped. Its claim (the commit's "without opening a new hole") is currently false, and the fix-shape is known. If you want the smallest possible round, strike Step 3.4 and the B358-2 cells, and launch on Sonnet.
2. **Model.** Recommendation: Opus (row C3) only if Q1 is "in". Otherwise Sonnet (C1/C2). The brief's LAUNCH line says to change `BRIEF_SEAT_LEVEL` accordingly.
3. **Tier-2 gate scope.** The card says the gate "checks only that change". Recommendation: tell the gate seat to run the full differential only if `secrets.ts` is in the diff, and otherwise to run the qgate scan, the two mutants T4b and N2, the whole-tree pattern scan, and the content-unchanged proof. The brief's fence and diff-path proof exist to make that cheap.
4. **Cap wording.** I wrote "a NO GO after this round goes to Kam, not to a fourth round". The card only says a third round needs his word, so this is my extrapolation. Recommendation: keep it, or edit it if you read the cap differently.
5. **Landing notes.** The gate's list of untrue sentences (reviewer first name, `994204f7` and `e82903ab` claims, the stale PR text) is Tuesday's, not the builder's. The brief puts only a "proposals" line in STATUS Records. Recommendation: fold them into your squash message and PR-body step.

## Fences kept
Wrote only the two files above, with the Write tool, plus one `sed -i` on the brief to replace a placeholder number (my own file). I used no Artifact, Docs, mail or chat tools. I ran no `gh` writes, no `decision_queue.sh list`, no fetch, pull, push or worktree, no HTTP to any deployed site, no `az`, no npm or node, and no `cd`. I read nothing from the scoreboard, `fleet/`, `briefs_staged/` or `_ledger.md`.
- **Slip, reported:** one early Bash call failed on the zsh `=====` hook, with no effect; I re-ran without it.
- **Outside the named read list:** the tmux, ps and lsof reads, which are local read verbs with no HTTP.
