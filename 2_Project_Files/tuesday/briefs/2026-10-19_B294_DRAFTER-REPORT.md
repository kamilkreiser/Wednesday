# B294 drafter report (2026-10-19 ~20:40 AEDT, read-only)

**Wrote:** `2026-10-19_B294_SEAT-W7_composer-records-fold-b292.md` and this file. Nothing else. Tools: Read, Write, read-only git verbs and `ls`/`cmp`/`grep`/`shasum` in the Composer root. No fetch, no network, no `az`, no write verb.

## Read
B278 brief and DRAFTER-REPORT (whole), B289 brief (whole), B292 STATUS (whole), B289 STATUS lines 7, 10, 11 (the gitleaks finding), B278 STATUS root-diff, B287 and B292 history entries (top), brief copies' line 35.

## Verified at source (MEASURED, root repo)
- Root is a git repo, `git remote | wc -l` = 0. Branch `main`.
- `main` `b57b607114ccd6686b2cf9110c58eeb92a3f1ded`; `records/b292` `62c3403159f8d837138384a3101569ea7c6413de`; `records/b287` `a9787105c0863214de7c3377aa38a5aeba8b1de0`. `git log main..records/b292` = exactly two commits (a9787105, 62c34031). `git merge-base main records/b292` = main's sha, so the branch descends from main (fast-forward possible; brief keeps `--no-ff` as B278 did).
- `main`'s top commits: B278's records commit, then the two B278 merges. So B278's fold is already in; this fold is only b287 and b292.
- `git diff --name-status main records/b292`: 29 paths = 26 added + `CLARIFICATIONS.md` (+38), `history.md` (+14), `BACKLOG.md` (+1 row, #319). 29 files, 1018 insertions.
- Collision: all 26 added paths exist untracked in the root. `cmp` against `git show records/b292:<path>`: 25 equal, 1 differs (`B292_STATUS.md`, B292's own "After the commit" block). B287 STATUS root copy equals the committed one. Root evidence folders: B287 17 files (branch 17), B292 5 (branch 5).
- Root `CLARIFICATIONS.md` and `history.md` are clean (`git diff --quiet` rc 0). Root status: 1006 lines, 1003 untracked, 3 tracked-modified: `B26_STATUS.md` (+10 lines, Friday's ADDENDUM-1), `B278_STATUS.md` (+13 lines, B278's "After the commit" block), `BACKLOG.md` (+6 rows).
- BACKLOG: `main` has 308 numeric rows, `records/b292` 309. Root diff is one hunk `@@ -314,0 +315,6 @@` rows 319-324; the branch adds its one row at the same spot (line 315), so a merge would refuse over the dirty file (hence the move-aside in A2). The root rows' text contains `#319` twice (inside old rows 320 and 321, meaning B281-1), which must follow the renumbering.
- Branch C-headings: 81, last C-81 (main: 78).
- No B293/B294 file in Tuesday's `briefs/` or the Composer `Briefs/`; B290 brief, evidence present but no B290 STATUS (seat may be live; `.tools/` has `wt-b290-*`).
- Mail key count 0. `uptime` 20:37, load 6.01. gitleaks installed (`/opt/homebrew/bin/gitleaks`).
- Slot tokens in the brief: 8 distinct, 8 tokens (`/usr/bin/grep -o` count). The stamp section names the slots without tokens, so it does not self-match.

## Corrections to the commission
- **The canary is not at "line ~35" in both copies.** B289's STATUS puts B287's findings at the B287 brief copy `:27` and STATUS `:51` plus `R1-A2-preflight.txt:28,29,30` (5 findings); B292's own STATUS puts its finding at its brief copy `:35`. Total expected in the fold: 6, plus the known `CLARIFICATIONS.md:213`. I read line 35 of the B287 copy (a section heading, not a canary) and line 35 of the B292 copy (the redaction bullet). The brief lists all 6 positions as RELAYED and tells the seat to STOP on any other. The first-hand scan was not run by me.
- B278 did not commit its own "After the commit" block (the root copy of its STATUS is modified now). That is a precedent for leaving root dirt, but it is also records material of the same class as B292's copy-back; see R-W7-3.

## Could not verify
- That the merge is conflict-free (not run). Only the merge-base and path list.
- The gitleaks range-scan result, the words scan, and whether code-repo files or PR #81's text cite rows 319-324 (not searched; brief says record the mapping, do not edit them).
- Whether B290's seat is live. Whether B280/B281/B285 PR and branch state is as the commission says (I did not read their STATUS beyond the file list).
- I did not read the root's six rows beyond the diff head (first 260 chars and grep for `#319`..`#324`).

## Questions for Tuesday
**R-W7-1. Is B290's gate seat (G9) or any other Composer seat live at launch?** Recommendation: confirm from the cockpit before stamping; the brief refuses if a b290/b285 worktree is newer than today and the process is live. B290 has no STATUS in `Briefs/` yet.
**R-W7-2. Commit the six renumbered root rows (320-325), or leave them as uncommitted working-tree rows?** B278's precedent is "touch only your named paths". But this seat is forced to move `BACKLOG.md` aside and re-apply the rows, and they are otherwise uncommitted with 0 remotes (loss risk). Recommendation: **COMMIT** them in their own commit with provenance in the message (default in the brief); LEAVE is supported.
**R-W7-3. Include B278's root STATUS "After the commit" block (13 added lines) in the records commit?** Recommendation: **COMMIT**: it is the same class as B292's copy-back that you asked for, and it is append-only; leaving it keeps a modified tracked file in the root indefinitely.
**R-W7-4. Renumber the root rows (319-324 to 320-325) rather than B287's #319?** Recommendation: **YES** (as commissioned): #319 is cited in committed text (C-79, C-80, C-81, history, two STATUS files) that cannot be amended; the root rows are uncommitted. Cost: the B281, B285, B280 STATUS files and PR #81's text keep citing 319-324; the brief records the mapping in STATUS and the history entry and does not edit them.
**R-W7-5 (for later, not in this brief).** The untracked B280, B281, B285, B289 (and soon B290) briefs, STATUS files and evidence are not on any records branch. Recommend a separate records-collection seat after this one; B294 only lists them.

## Slots Tuesday must stamp: 8
B_NUMBER_CONFIRM, ROOT_MAIN_SHA, B292_SHA, B287_SHA, MODEL, STAMP_TIME, PANE, PANE_SUFFIX. Plus the R-W7-1..4 rulings line (free text, not slot tokens; no ruling recorded = recommended default).
