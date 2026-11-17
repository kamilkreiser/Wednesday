STARTABLE: YES (once Tuesday stamps the ten slots)

# B1688 drafter report (SEAT-R265, Composer records pass for PCOMP-74, PCOMP-80, PCOMP-81)
Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-18_B1688_SEAT-R265_composer-records-pcomp-74-80-81.md` (128 lines, sidecar `.measured` 133 lines, `stamp_check.py` exits 0: 133 claims, 133 measured, 0 TODO). Drafted 2026-11-18 06:21 to 06:31 AEDT (`date` printed 06:21:43 to 06:30:42). Shape copied from B1590 (R239).

## BLUF
- **The change is on main and meets all three tickets at source.** Composer PR #125 (branch `b1516/composer-w3b-css-ruled`, merged 2026-11-11T09:13:07Z = 20:13:07 AEDT) is squash commit `5d3bf82ddca5b07a216ace594be4f47af4119ec6` (the sweep's "5d3bf82d, 09:13:06Z" is the commit time; same commit). It is an ancestor of main `b4681297` (compare ahead 5, behind 0, merge base = the squash).
- **Per ticket I read the diff lines and every check is MET at the drafter's reads**; none needs a "comment only" fallback today. The kit still carries the per-key fallback, so a seat read that disagrees stops that key's move and says which row.
- **No C-entry records PR #125** (`PR #125`, `9853954`, `B1516` read 0 0 0 0 over CLARIFICATIONS, BACKLOG, JIRA, history; `5d3bf82d` reads 2 1 0 1 but only as PR #126's base). The ruling itself is C-139 (`CLARIFICATIONS.md:2644`), and the three tickets already hold one comment each (40998, 40999, 41000, all "Recorded; not moved ... stays in Backlog") from that pass.
- **The kit's seat:** one C-entry frozen at **C-153** (highest is C-152 at :2853; `### C-153` count 0), one appended sentence on each of rows #75, #123, #154 (no new row), 3 comments + up to 3 moves (transition 41), JIRA.md bullet, history entry, own records branch `records/b1688`, folded with `merge --no-ff` only if slot REC-MERGE reads MERGE. Sonnet; model row C7 (`model-routing.md:97`) and G3 (`:110`); model id `claude-sonnet-5-5` (`models_latest.json:23`); launch line carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes; pane `Datasec/Composer-R265`.
- **One thing worth your eye: the change is already on the demo** (C-152, deployed 2026-11-16). So the three comment texts say "put on the demo on 2026-11-16" (RELAYED from C-152) instead of the template's "NOT DEPLOYED", and never use the word "deployed" outside the move sentence. The withdrawn list's monospace key was never seen on a demo screen (C-152: "the example has no withdrawn list"); TEXT-81 says so.

## Facts re-measured (instrument, control)
- PR #125 (`gh api -X GET pulls/125`, control `pulls/9999` 404): closed, merged true, `merge_commit_sha` 5d3bf82d..., head `9853954a...`, base `879facda...`, 3 commits, 6 files, +153 -22. Squash tree `12d30532...` equals the head's tree (`git/commits/<full sha>`; the short sha answers 404, which is why the kit says full sha). Code main = `b4681297...` (`branches/main`); open PRs: #85 only; list 130 down to 121, nothing newer than #130.
- Checks: head has CodeQL, Analyze (csharp), Analyze (javascript-typescript) all success before merge; squash has both Analyze runs success; `code-scanning/analyses` filtered by `commit_sha` 5d3bf82d: 2 rows on `refs/heads/main`, `results_count` 0 (control: `alerts?state=fixed&per_page=20` returned 20); open alerts on main 0.
- Diff lines (raw `contents?ref=` at squash and base, saved in the drafter's scratch): `tokens.css:16` `--pc-on-primary: #ffffff;` (count 1; base 0; `:15` `--pc-nav-fg` untouched). The pattern `#fff(fff)?\b` counts 0 in app.css, screens-w1/w2/w3.css, guided.css, feedback.css, b87-shell-dashboard.css, guided-home.css, scale.css at the squash (tokens.css 2) and 11 / 3 / 4 / 2 at base (control: it fires at base). `var(--pc-on-primary)` 11 / 3 / 4 / 2 at the squash, 0 at base. `screens-w3.css:657-659` is the one new rule (`.w3-withdrawn-list .w3-register-key`, declarations 1, font-family only, equal to `app.css:57` `.pc-mono`; `word-break` 0 in the block, control 0 over the sheet, `font-size` 14 and `width` 78 over the sheet so the block's 0 can fail). `border-radius: 50%` and `999px` counts are equal at base and squash in every sheet (3/1, 3/1, 1/1, 1/0).
- Gate (RELAYED, read in part): `2026-11-11_B1516_verify/VERDICT.md` (70 lines, sha256 prefix `3cc99755e45923e6`): line 1 `GATE B1516: GO @ 9853954 on main 879facd`, line 11 `(none) ... No Blocker, no Major, no Minor.`; NOT RUN: CodeQL, stack e2e specs, ci.sh, pixel-diff programs. Builder STATUS 124 lines, prefix `3bf16c8322b877c1`, proposes the Done-when texts at lines 96, 97, 122.
- Ruling (RELAYED by C-139 (2), counts of the exact phrases 1 each): white becomes a token (token change approved), 50 % and 999px kept, monospace key in both lists.
- Jira (GET only, control `PCOMP-9999` 404): all three are Backlog Tasks with one comment each, 0 changelog, labels `composer-seed-1023` + `plan-comp-75` / `-123` / `-154`, transitions 11/21/31/41. The word `Done-when` counts 0 in each (control PCOMP-128: 1). Project: 129 issues, Done 48, held 19, seed marker 94, needs-kam 2, Backlog 81, `labels = "plan-comp-494"` 0 (control `plan-comp-75` 1), `text ~ "composer"` 68, `zzqxvbw` 0.
- Records anchors at root HEAD `a33cc3f1` (B1612 fold): CLARIFICATIONS 2,870 lines; JIRA.md 60 lines (newest `- B1612`; `^- B1688 ` 0, control `^- B1612 ` 1); BACKLOG 489 lines, 483 data rows, highest row #493, rows #75/#123/#154 at :79/:124/:148 each NF 5 and each ending with the C-139 sentence; history 2,236 lines (B1612 entry at :3). Root: no remote (0 lines; control: the code clone prints `origin`), `records/b1688` absent (rc 1; control `records/b1612` resolves), `.tools/b1688` and `.tools/wt-b1688-rec` absent, no index.lock, 129 refs, identity `kamil.kreiser@datasec.com.au` for author and committer.
- Seat id / ports: `R265` and `R266` 0 files in the non-`.pre-` SEAT kits of 11-17 and 11-18 (controls `R264` 1, `R263` 2); no kit of those days names `Security Composer` or `PCOMP` (0 files); no Composer pane live. Ports: none.
- Jira text scan: a drafter scanner with the TEXT RULE families (underscore-aware names) read the six bodies (3 texts x MOVE/STAY) 0, 16 of 16 planted controls fired, a clean phrase read 0. Lengths and sha256 prefixes are in the kit.

## Input table for the chain (rule 4)
| Step | Inputs | Produced by |
|---|---|---|
| 0 | the kit, root repo state, `.tools/b1590/scripts/` | exist at BASE |
| PRIOR WORK | Jira GETs, PR list, record files | exist at BASE |
| 1 | PR, raw style files at the squash and parent, VERDICT.md, B1516 STATUS, C-139, C-152 | exist at BASE (read-only) |
| 2 | Step 0 and 1 prints | Steps 0, 1 |
| 3 | scanner copy from `.tools/b1590/scripts/textscan_b1552.py`, kit texts | BASE, kit |
| 4 | Step 1 raw files and patches, `jira_*` copies | Step 1, Step 0 copies |
| 5 | `payloads.json`, `movechecks.json`, dry-run pass | Steps 3, 4 |
| 6 | Step 5 outcomes (placeholders), `@@DATE@@` from Step 0 | Steps 0, 5 |
| 7 | all of the above | Steps 0 to 6 |

## D-decisions (mine; each reversible by your word)
- D-1: **no new BACKLOG row.** The review had no finding (nothing to record as a row), and C-139 itself recorded these tickets by sentences on #75/#123/#154. The kit appends the same three sentences behind one slot (STATE-ROWS).
- D-2: **three texts say "put on the demo on 2026-11-16"** (RELAYED from C-152) rather than "NOT DEPLOYED", because that would now be false. The seat re-reads C-152 before posting; if it disagrees, that comment holds.
- D-3: **comment and move are one slot each for all three keys** (COMMENT, MOVE); the per-key outcome comes from each key's own five-row Done-when table (rows 1 to 4 by program, row 5's gate part RELAYED).
- D-4: the ticket clauses are the Fix-shape/State line, the ruling and the builder's proposed Done-when (as C-112 (4) did for PCOMP-40/41/43), because none of the three tickets carries a Done-when line. Quote of the Done rule: C-111 (3), `CLARIFICATIONS.md:2029` ("Done here means merged to main, not deployed."), with C-112 (`:2046`) for the three-part move condition.
- D-5: helper copies come from `.tools/b1590/scripts/` (it has the move logic and the live newest-comment compare); `NEWEST` is set to the existing comment ids, since each key already has one comment.

## Q-questions for Tuesday (each with a default)
- Q-1: Should PCOMP-81 move while its monospace key was never seen on a demo screen? Default: yes, MOVE (the rule is merged, not seen; TEXT-81 states the gap). Set MOVE to HOLD to hold all three.
- Q-2: STATE-ROWS APPEND (drafter recommends) or NONE? Default: APPEND.
- Q-3: Is C-153 still the next number at stamp time? Default: yes (nothing newer; the seat STOPs if the number differs).
- Q-4: The product owner's own look at the new styles on a card (C-152 leaves the receipt to you): left open in the C-entry's "Does not settle". Default: unchanged.

## UNMEASURED
- Hosted state of the demo and what any screen shows (fenced; RELAYED from C-152). The stack e2e specs and the pixel-diff programs (not run by the gate). Whether any later seat reads the squash differently (the seat re-measures at Step 1). The kit's `date +%F` date for `@@DATE@@` is the seat's own at Step 0.
- Not re-run by me: the gate's red-first table (28 of 30 rows red at base) and its computed-style comparison; the kit marks both RELAYED.

## Outside-the-fences disclosure
- Wrote only the kit, its `.measured` sidecar (via `stamp_check.py --init`, then filled by a script from my own reads) and this report. Scratch scripts and raw downloads (raw style files at both shas, a Jira dump, text-scan scripts) are in the session scratchpad `/private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/0f6ab911-939a-403c-8cca-13683e6f84b8/scratchpad/`, none in a project tree.
- Jira: GETs only, through a python `-I` script of mine that imports the project's `.tools/b1612/scripts/jira_lib.py` (reads the project `.env` in-process; no token printed); every JQL is `project = PCOMP AND ( ... )`. GitHub: `gh api -X GET` only under the project's own `GH_CONFIG_DIR`. Git: read verbs with `--no-optional-locks`; one `git symbolic-ref` was refused by a hook and replaced by `rev-parse --abbrev-ref`. No `decision_queue.sh`, no briefs_staged, scoreboard or `_ledger.md` read, no WEDNESDAY/FRIDAY tree, no mail, chat, Artifact or Docs, no hosted host probe, no az/ssh/docker. I read the template kit B1590 whole, the Composer project's CLARIFICATIONS (C-112, C-139, C-150, C-152), BACKLOG rows, JIRA.md and history lines, the B1516 gate VERDICT.md and builder STATUS (parts), `model-routing.md` lines 97 and 110, `models_latest.json:23` and `brief_seat.sh:31`.
- The template cited the 2026-11-15 `date` clocks; mine are 2026-11-18 06:21 to 06:30 AEDT. The drafter's own line pointers were printed by `awk NR==n` / `grep -n` over the raw files in the same session.
