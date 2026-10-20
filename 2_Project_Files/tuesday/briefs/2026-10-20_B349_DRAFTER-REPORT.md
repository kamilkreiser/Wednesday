# B349 drafter report (SEAT-W19, NexusAI PR #97 forward merge + counts TURN)

Drafted 2026-10-20 about 22:55 to 23:25 AEDT (first live read `date` 23:08:33, second 23:09:57) by a read-only drafting agent (Sonnet 5.5). Wrote only the brief and this report. Nothing launched, mailed, published, fetched or merged. Git in NexusAI: read verbs only (the one non-obvious verb is the LEGACY 3-argument `git merge-tree <base> <a> <b>`, which prints to stdout and writes no object; not `--write-tree`). `gh`: GETs only, `GH_CONFIG_DIR=/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/4_Credentials/.gh-config`. Scratch output: `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/a9f9c97d-40bf-4bdb-8b7d-300c5cdf09be/scratchpad/mt.txt` (the merge-tree text).

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-20_B349_SEAT-W19_nexusai-pr97-forward-merge-counts-turn.md` (45,864 bytes). Slots left: `@MAIN_SHA@` (3 occurrences: the REFUSE line, the Stamp line, RULED 1 area; line numbers 23, 30, 75) and `@STAMP_TIME@` (1, line 30). No `.pre-stamp` copy was written (outside my two-file fence): Tuesday makes it, and the brief's slot-check control (Step 0) needs it.

## 1. Premises re-read (all agree with the commission)

| premise | read | result |
|---|---|---|
| main | `ls-remote origin refs/heads/main`, 23:08:33 | `d463f8817fba925dee7e78c5216df3d5ea8ad073` (agrees) |
| PR #97 head and branch | `ls-remote` branch + `refs/pull/97/head`, 23:08:33 | both `278afc25dda22ed8511d33e3e1cd12b0afde3487` (agrees) |
| PR #97 state | `gh pr view 97 --json …` | `isDraft` true, `state` OPEN, `baseRefOid` `39653db4b56adb6d4e526c90531cd4cdf23022e0`, `mergeable` CONFLICTING, `mergeStateStatus` DIRTY, `changedFiles` 8, 7 commits, title as commissioned |
| ahead/behind | `merge-base` and `rev-list --left-right --count d463f881...278afc25` | merge-base `39653db4…`; `13 7` (behind 13, ahead 7; agrees) |
| objects local | `cat-file -t` on `d463f881`, `278afc25`, `39653db4`, `aa811cf2` | all `commit`; no fetch needed |
| what main did | `log 39653db..d463f881` | 13 commits: #98 merge `d463f881` (tree `53d51c59698401237b1b1573fa942bf9f650b51d`), #99 landing merge `aa811cf2` (tree `18612f22e98388b4a7f9a4d01bcfad24996633b9`), `e80920c2`, HISTORY.md `1bc9e9df`, RD-863 `172d321f`, 8 RD-782..789 commits |
| paths | `diff --name-only 39653db d463f881` / `39653db 278afc25` / `comm -12` | main 38, PR 8, overlap exactly `backend/server.js` + `scripts/verify-expected-counts.json` |
| conflict set | legacy `merge-tree 39653db 278afc25 d463f881` | `changed in both` = those two; `backend/server.js` no markers (main hunks at :7979 +3, :8095 +12/-3 region, the PR's hunks elsewhere); the counts file has one marker hunk (`_updated`, `tests`) |
| counts | `show <c>:scripts/verify-expected-counts.json` | `39653db` 4880/302 (blob `2cc09485…`); `aa811cf2` 4934/303; `d463f881` 4934/303 (blob `a28458ad…`); `278afc25` 4910/303 (blob `57659c6c…`) |
| lock and tools | `shasum`, `ls` of `locks-laptop-1017` | `nexusai-lock.sh` `3c33f5ae…` (same as B343), `c57-id-superset.sh` `1ae84a10…5581`, `c133-accounting.py` `6f938bfc…f972f`; `queue-jest/` empty, `released/` 357, no lock dir |
| panes | `tmux list-panes -a` | no `Datasec/NexusAI-O` pane; four panes in total |

Not in the commission but found: **`worktrees/s101o-rd774` has the local branch `rd-774-risk-sql-templates-s101o` checked out at `278afc2`** (worktree list). The brief therefore uses a new local branch `b349/pr97-turn` in its own worktree and pushes `b349/pr97-turn:refs/heads/rd-774-risk-sql-templates-s101o`; S101O's local branch will lag one merge after the push (Question 4).

## 2. What I read, with line references

- `/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md` (2368 lines, last entry C-218 at `:2362`), each entry read whole: C-57 `:418-428` (amended 09-17 and by C-68's addendum `:668-671`); C-68 `:665-671`; C-112 `:1149-1160`; C-133 `:1434-1447` (with its four addenda); C-184 `:1966-1970`; C-186 `:2009-2023`; C-190 `:2062-2079`; C-209 `:2270-2283`; C-218 `:2362-2368`. Also C-185 `:1971-1975` (known set), cited by line from B343 `:2004-2006`; C-192 `:2095` cited from B343.
- `/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/CLAUDE.md`: grepped (merge, counts, lock, jest, squash) only; it has nothing that decides a counts TURN beyond the verify rule (`:227`, RD-100).
- Prior briefs in `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/`: `2026-10-20_B343_SEAT-W18_nexusai-pr98-landing.md` (213 lines, whole, through the persisted copy), `2026-10-20_S101O_ANSWER-30_rd863-go-land-pr99.md` (whole; `:9` item 4 is the source of "whichever of #97/#99 lands second needs a counts-only TURN, both = 4964/304"), `2026-10-19_S101O_ANSWER-18_rd794-accepted-c170-turn.md` (whole; the closest earlier "counts-only TURN" shape: forward-merge, regenerate counts once, C-57 + C-133, named suites, PR route), `2026-10-20_S101O_ANSWER-28_pr97-codeql-273.md` (whole). Grep for TURN/counts found these plus ANSWER-25 `:3-6` (RD-856/857/476 "each a counts-only TURN on then-main"), and the gate 31 kit `…B327…` `:132` and `:157` (the checklist "whichever of #97/#99 lands second needs a counts-only TURN = a new head = a delta gate"). No separate "counts-TURN brief" exists; the shape is carried by ANSWER-18 and B343.
- `/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-10-20_B343_STATUS.md` (111 lines; read the pins, the merge, the asserts, hold timings: 69 suites about 35 min, verify 28 min, lock method, `DONE:` line).
- Gate 29 kit files: `fleet/qa-agent/briefs/2026-10-20_nexusai-gate29-READY-pr97-278afc2.txt` (whole), `2026-10-20_nexusai-gate29_AMEND-REPORT.md` (264 lines; read `:1-140`, i.e. BLUF, §1-§5 and the open questions; §2a edit list skipped), and `2026-10-19_nexusai-gate29-rd774-rd836.md` (153,791 bytes now; I read only the lines named below by number, not the whole kit: `:5`, `:6`, `:13-16`, `:21`, `:55-56`, `:77-78`, `:96`, `:151-152`, `:229`, `:255`, and the slot/mode grep).
- `fleet/specs/model-routing.md:60-154` (decision table; row C5 at `:95`; launch receipt §6).
- Also: Tuesday's grant file `0_Brain/learnings/2026-10-16_tuesday-inherits-…md:19`; `models_latest.json:22-23`.

## 3. Each premise in the brief and its source

1. "Gate 29's kit uses mode (b) when main moves": kit `:77` T0 text, "(b): Tuesday first asks S101O for the counts-only forward merge and re-pins RD774 (a NEW head = a kit AMENDMENT and a new CodeQL run to read …)". Amend report §5 Q3 recommends (b) when the landing touches `backend/server.js`; #99 did (hunks at :7979 and :8095), so the report's own default points at (b).
2. "Counts conflict, forward merge, regenerate once on the merged tree": C-57 `:418-428`; amendment `:670` and C-68's addendum "regenerate ONCE … REGARDLESS of whether merge-tree reported a conflict".
3. "Id-superset by construction when no test file is content-merged": C-112 corollary `:1156-1160` ("only when every test file is byte-identical to a parent"). MEASURED basis: only two paths are `changed in both`, neither under `__tests__/`. The program that proves it is the seat's (assert (f)/(g)); I did not run it.
4. "13 F-10 names accounted, branch side": the READY mail (`C-133 accounted 13 … still missing 0`, then 32 with C-170's 19); after the base moved to `39653db` only the 13 remain. Expectation only, used in RULED 4 as the fallback.
5. "4964/304": arithmetic (4934 + 30, 303 + 1) and ANSWER-30 `:9` (gate 31's figure). Labelled UNMEASURED and cross-check only.
6. Lock method, tool hashes, base `locks-laptop-1017`, tag containing "merge": B343 brief Standing line 10 and Step 1; hashes re-read today.
7. "Do not land, end at READY": the commission; the final line formats follow B343's (`DONE:` replaced by `READY FOR QA:`). A land of #97 needs the gate first (kit; ANSWER-30 `:9`).
8. Model row: `model-routing.md:95` (C5), the same row B343 used; counter "No second merge attempt on the same head without a new GO".
9. CodeQL control: the amend report §3.9: "PR #58 control #256-#259 `fixed`" (4). B343 used PR #96 (6); both exist, #58 is what the kit and the READY mail use for #97.
10. `node_modules` source: `worktrees/b343-pr98-land/node_modules` and `worktrees/b334-pr98-fix-r2/node_modules` exist (`ls -d`); no `package*.json` path among main's 38 changed paths (`grep -c` 0).
11. "Ports banded by worktree, none to reserve": `__tests__/helpers/test-server.js:47`. B343 said "bind nothing"; the rd774 file does boot servers via `reservePort()`, so the brief says so instead.

## 4. QUESTIONS for Tuesday (each with my recommended answer)

1. **Slot syntax.** You asked for `@MAIN_SHA@` and `@STAMP_TIME@`; B343's brief used `@@MAIN_SHA@@`. I used the single-@ form you gave, and the Step-0 refuse check greps `@[A-Z_]+@` (split-quoted). *Recommend:* keep single-@; if your stamping tool expects `@@…@@`, sed the two tokens and the grep pattern together (the pattern is on one line, line 22).
2. **Full C-57 runner or construction proof?** The brief makes the C-112 by-construction proof primary (no test file is content-merged: `changed in both` = server.js and the counts file only) and runs the three-pass runner only if a test blob equals neither parent. The runner costs about 75 minutes of lock time (kit T1). *Recommend:* by construction first, as written; the verify at 4964/304 and assert (g) are the evidence. Say if you want the runner anyway for symmetry with the earlier TURNs.
3. **`backend/server.js` semantic overlap.** Clean text merge, but both sides edit it. The brief names 11 suites for C-68 (minimum set) and requires the seat's own content scan, then a plain verify. *Recommend:* as written. A gate-side check is still the gate's r1/r12.
4. **S101O's local branch.** After the push, `worktrees/s101o-rd774` (local `rd-774-risk-sql-templates-s101o` at `278afc2`) lags. *Recommend:* tell S101O on resume to fast-forward its local branch to the remote head (`git merge --ff-only`) and not push before doing so; I put nothing in the brief about messaging it (brief fence: no mail).
5. **Which main if main moves again before launch?** RULED 6 says STOP and ask. *Recommend:* if the move is HISTORY.md-only or a test-only PR, issue a new B-number with a re-stamped pin rather than editing this brief; if it touches `backend/server.js` near the risk block, re-run Step 3 before stamping.
6. **PR #97 body.** Step 9 only drafts it; you apply. *Recommend:* as written (precedent: B343 RULED 3).
7. **PR #67.** It is a separate CONFLICTING mover (RELAYED B343 `:41`); not re-read by me today. *Recommend:* leave as is; the seat records its head in Step 1.
8. **Launch order against the gate.** B349 produces H; the gate-29 launcher then needs the re-pin in §4 below before `--check`. *Recommend:* queue the launcher re-pin drafter now (it needs only the sheet B349 returns plus the existing amend-report list), launch B349, then run `--check` on a scratch copy once H exists.
9. **Do you want `.pre-stamp` made and the seat launched with the cockpit line in the brief?** The launch line is copied from B343 with `W19`, `B349` and the new file name. *Recommend:* yes; check the pane name `Datasec/NexusAI-W19` is free (`tmux list-panes -a` showed no `W19`).

## 5. What gate 29's kit needs re-pinned after B349 (exact places)

Source: kit `2026-10-19_nexusai-gate29-rd774-rd836.md` (line numbers as read today) and the AMEND-REPORT §4-§5. Nothing below was edited by me.

**Kit slots (17 occurrences; B349 affects the first four):**
- `@SLOT:MAIN_SHA@` at `:16` (MAIN-STAMP) and `:21` (PIN-HEADS MAIN row): fill with main at stamp. If main is still `d463f8817fba925dee7e78c5216df3d5ea8ad073` when you stamp, that is the new M0; the kit's default value (`39653db…`) is superseded.
- `@SLOT:MAIN_TREE@` (`:16`): `53d51c59698401237b1b1573fa942bf9f650b51d` if main is still `d463f881` (MEASURED tree, B343 STATUS and today's `log`).
- `@SLOT:MAIN_LANDED@` (`:16`, "landed since 39653db"): the list `git log 39653db..d463f881` (13 commits, the #99 and #98 merges named) instead of `none`. The label "landed since 39653db" itself should be re-based to `d463f881` or left and filled with the 13.
- `@SLOT:RULING_T0@` (`:77`): rule **(b)** and re-pin RD774 (kit text: a NEW head is a kit AMENDMENT). With B349's head H, mode 0 becomes true again (H descends from main; `merge-base --is-ancestor d463f881 H` rc 0) and the gate runs on H itself; predicted counts become H's own `<n>/<m>` (expect 4964/304).
- `@SLOT:RULING_T1@` (`:78`): "not needed (no merge)" in mode 0 at H. The kit's wording there references `39653db` as the C-133 base; B349 uses `39653db` as the base for its own accounting, so no text change is needed for B349's report, but r1 should read the new merge (below).
- `@SLOT:REPORT_DATE@`, `RULING_T2..T10`, `SELF_CHECK_STAMP`, `SELF_CHECK_NOTE`: unchanged by B349.

**Kit lines that carry the old head or M0 and must change for H (all are in the amend report's edit list; grep `278afc2`, `39653db`, `ee819f21`, `4910`, `57659c6c`):**
- `:5` RE-PINNED paragraph; `:6`; the item paragraph and "What is new here": head `278afc25…` → H, tree `ee819f2126593465b352d91ae293fb3c55b9a75b` → H's tree, the seven-commit chain → the eight-commit chain with a fourth forward merge (parents `278afc25` + `d463f881`).
- WRONG 1 (`:55`), WRONG 2 (`:56`), WRONG 4 (the 8-path set, `server.js` blob `5fdf2912…` → the merged blob; the counts blob `57659c6c…` → H's), WRONG 5 (counts 4910/303 → `<n>/<m>`; M0 4880/302 → 4934/303, delta +30/+1 unchanged), WRONG 7 (route line numbers shift by main's +3/+12 lines; B349 Step 8 item 8 returns the new anchors), WRONG 12 (CodeQL: new analysis ids at H; the old `1985321634`, `1985312931`, `1985312531` are for `278afc25`).
- `:77` T0 default: `39653db` → `d463f881` as M0; "predicts M0 + 30 / + 1" stays true against `d463f881` (4934 + 30 = 4964; 303 + 1 = 304).
- `:96`/r12/r12b: mode (a)/(b) text unaffected; r12 expected counts → `<n>/<m>`.
- `:151` (r0): range `39653db..<gated>` → `d463f881..H` (8 commits); the gated tree pin `ee819f21…` → H's tree; the 8 paths stay (assert (b) in the brief proves it).
- `:152` (r1): add the fourth forward merge to the list of merges to rebuild (`H` = `278afc25` + `d463f881`, counts blob `57659c6c…` replaced by H's blob; the seat's tree must equal the rebuilt tree with the counts blob substituted). Note the legacy `merge-tree` the kit's r1 uses is the one I ran: conflicts = the counts file only.
- `:229` LANDING CHECKLIST text: "a later landing => re-pin (mode a, M0 + 30 / + 1)" becomes true again only for a later main; the ten expected-fixed alert numbers may change (re-run the heuristic from the amend report §3.10 against H's `server.js`: a main alert on a line that main's +3/+12 shifted can still read the same text).
- `:255` (THE MAIN PIN FIRST) and the launcher: see below.

**Launcher** `launchers/launch_qa_nexusai_gate29.sh` (792 lines; unchanged per the amend report, still pins the old head, main, counts and READY copy): re-pin points are listed in AMEND-REPORT §4 (`READY_774_SHA` :71, READY greps :505-:507, `FLOOR_MAIN`/`FLOOR_TREE` :115, `H774`/`T774` :118, the PIN-HEADS check :277, the MAIN-STAMP regex :286-:289, head-moved check :309-:310, main-ancestry and mode-0 logic :321-:348, chain guards :350-:357, the 8-path set :391, counts and blobs :401-:402, mode-a prediction :405, blob pins :415, anchor counts :421, summary text :748, :780). Nothing in B349 changes that list except that the head, tree, M0 and counts values become H's and `d463f881`'s.

**READY copy:** the kit's READY guard is built around the delivered mail body for `278afc2` (file `…READY-pr97-278afc2.txt`). H has no delivered mail from S101O; B349's STATUS "GATE 29 RE-PIN SHEET" plays that role. *Recommend:* save the sheet as `briefs/2026-10-20_nexusai-gate29-READY-pr97-<H7>.txt` and re-point the launcher's guard at it (AMEND-REPORT §5 Q2).

**Delta-gate nature:** both the kit's verdict line and the gate 31 checklist (`B327 :157`) call this "a new head = a delta gate". The kit is a full tier-1 gate, not a delta; B349's brief does not say which. *Recommend:* run the full kit re-pinned (the commission says gate 29 "can be re-pinned and launched").

## 6. What I could not establish

- Whether the merge in a real store reproduces the legacy `merge-tree` result and passes `--update-counts` mechanics as the brief describes (no merge, jest or npm run).
- The regenerated counts (4964/304 is arithmetic) and whether the C-112 by-construction conditions hold at the blob level (inferred from "only two paths changed in both").
- How the `--update-counts` flow behaves when started from main's counts blob after `checkout --theirs` (I wrote it from C-57 step 2 and the file's own `_why` line; I did not read `scripts/` for the exact flag handling; the brief tells the seat that source wins).
- Whether `rd476-assistant-prompt.test.js` and `index-dark-surfaces.test.js` truly read the changed `server.js` surface: they are on the named list because they appear in the greps (`rd476` is in the previous TURNs' verify set; `index-dark-surfaces` mentions risk markup and #98 edited the dark-surface tests). The seat's own content scan (Step 7) is the backstop.
- S101O's status (no pane); PR #67's current head and mergeability today (relayed from B343 only).
- The launcher's current state (not read; amend report only).
- I read the gate-29 kit by line, not whole (153 KB); anything outside the lines named above I took from the amend report.
