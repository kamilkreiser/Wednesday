From Friday (laptop seat), Datasec / Datasec Security Composer. Replies and wraps go to friday-laptop-agent@agentmail.to (if this project has no mail key, your STATUS file is the wrap).
# BRIEF B131 · SEAT-R: COMPOSER RECORDS: fold the eight unfolded `records/*` branches (b119, b124–b130) into records main, three BACKLOG rows (B128-N1, B130-F1, B130-F2), a history entry for the #69/#70/#71 merges, one unrecorded card ruling as C-69
**Written:** @NOW@ AEDT 2026-10-12. **Pane:** `Datasec/Security-Composer-R`. Your commission is the newest file in `1_Project_Definition/Briefs/` whose name contains `_SEAT-R_`.
(Launcher check, read by the draft writer: `Launch_Claude.command:100` sets `SEAT` from a pane name matching `*Security-Composer-?`; `:104` says the commission is "the NEWEST brief in 1_Project_Definition/Briefs/ whose file name contains _SEAT-${SEAT}_ (NOT simply the newest". At drafting, **no** file in `Briefs/` contains `_SEAT-R_` (`ls Briefs/ | grep -i _SEAT-R_` = 0), so this is the first Seat R commission here.)
**Seat:** Seat R (Claude records seat). **RECORDS ONLY: no product code, no deploy, nothing on Azure, no demo access.** One records branch, the fold into records main, your STATUS. Nothing else.
**Report:** `1_Project_Definition/Briefs/2026-10-12_B131_STATUS.md` (BLUF · ITEM 1 · ITEM 2 · ITEM 3 · ITEM 4 · UNMEASURED · NOT DONE / NOT COVERED · needs-Friday · Leak + secret scan · processes started/stopped · worktrees and files left). Its last line is exactly one of:
- `RECORDS DONE: <one line: records main @ <sha from git rev-parse main after the fold>, branches folded 8/8, rows #312-#314, C-69 y/n, history 1>`;
- `STOPPED: NEEDS FRIDAY` and ONE question.

## AUTHORITY
- **Friday commissions this round.** The BACKLOG rows are the gates' own words (`B128_STATUS.md`, B128 seat F; `B130_STATUS.md`, B130 seat E). The history facts are measured below. None of this needs Kam's word.
- **C-69 records a ruling Kam already made** (card text quoted in ITEM 4 from Friday's decision register). Do not compose any wording inside a quote.
- **Jira:** none. This project has no Jira project (`BACKLOG.md` row #4: *"never created; key `PCOMP` was proposed and is on HOLD"*). Write nothing to any Jira.

## READ WHOLE FIRST
- The project `CLAUDE.md`; `1_Project_Definition/CLARIFICATIONS.md` **as it stands on `records/b130`** (`git show records/b130:1_Project_Definition/CLARIFICATIONS.md`; 1225 lines, ends at **C-68**); `BACKLOG.md` on `records/b130` (307 lines, last row **#311**).
- `records/b128:1_Project_Definition/Briefs/2026-10-11_B128_STATUS.md` (276 lines; also in `_wt_b128rec`, byte-equal at drafting): `:25`, `:34`, the B128-N1 table row `:44`, `:120`.
- `records/b130:1_Project_Definition/Briefs/2026-10-12_B130_STATUS.md` (397 lines; byte-equal to the root's untracked copy and to `_wt_b130rec`'s at drafting): `:36-41`, the F1/F2 table rows `:57-58`, its proposed BACKLOG lines `:390-391`.
- C-52…C-64 on main as the shape for a card-ruling C-entry (e.g. C-64 at `main:CLARIFICATIONS.md:1023-1024`).

## THE RECORDS ROUTE (measured by the draft writer, read verbs only, `--no-optional-locks`)
Friday's rule (ledger, 2026-10-11): *"a records instruction names the repo by reading where BACKLOG.md lives and whether it has a remote"*.
- `git ls-tree -r --name-only HEAD` in the **project root** lists `BACKLOG.md`, `1_Project_Definition/CLARIFICATIONS.md` and `5_Project_History/history.md`. So the records repo is the **project-root** git repo, not `2_Project_Files` (that one is the code repo, origin `git@github.com:datasecau/Datasec-Security-Composer.git`).
- `git -C <root> remote -v`: **empty**. **No remote: nothing is pushed in this round.** Commit locally only. (No PR, so the CodeQL/PR line does not apply to the records repo.)
- Root checkout: branch **`main`** = **`441fa893a644885916a7de02ecee87624f887268`** (B123 STATUS, 2026-10-11 13:39). Tracked changes: **one**, ` M 1_Project_Definition/Briefs/2026-09-30_B26_STATUS.md` (+10 lines; no records branch touches that path: `git diff --name-only main...records/<b>` = 0 hits for b125, b128, b130). **Leave it alone.** Untracked: 929 entries.
- **Unfolded branches** (`git for-each-ref refs/heads/records` + `git merge-base --is-ancestor <b> main` = no). All eight branch from `46afbc5c` (B118 STATUS); main is 4 commits past it (B121, B120, B122, B123 STATUS):

| branch | tip | `rev-list --left-right --count main...<b>` | contains | worktree |
|---|---|---|---|---|
| `records/b119` | `8e64b830` | 4 2 | (B119: C-67, deploy a3502002) | `_wt_b119rec` |
| `records/b124` | `ce70da67` | 4 4 | b119 + B124 (C-68, deploy 4e00d573, BACKLOG #298–#311) | `_wt_b124rec` |
| `records/b125` | `a52680d8` | 4 6 | b124 + B125, B125 ADDENDUM-1 STATUS | `_wt_b125rec` |
| `records/b126` | `4ba653c3` | 4 6 | b124 + B126, B126 ADDENDUM-1 | — |
| `records/b127` | `1ffc1989` | 4 7 | b126 + B127 | `_wt_b127rec` |
| `records/b128` | `ac91fb51` | 4 5 | b124 + B128 | `_wt_b128rec` |
| `records/b129` | `fb80a57e` | 4 8 | b127 + B129 | `_wt_b129rec` |
| `records/b130` | `bb648ec2` | 4 9 | b129 + B130 | `_wt_b130rec` |

  So **three tips cover all eight**: `records/b130` (⊇ b129, b127, b126, b124, b119), `records/b125`, `records/b128`. Each of those worktrees was clean (`status --porcelain --untracked-files=no` = 0) at drafting.
- **Not commissioned (also not ancestors of main; leave them, name them under needs-Friday):** `records/b20` (`3f3d5cdf`, 2026-09-29, 211 behind; its 32 files are **not** on main) and `records/b58-wip-on-44029f6` (`35b83e44`; its own subject says *"superseded: renumbered onto e94a35e"*; the renumbered `ecce66d4` IS on main).
- **Collision surface, measured:** from `ce70da67` (B124) up, the only file the three tips AND main all change is `5_Project_History/history.md` (every one inserts at `@@ -1,5`). `CLARIFICATIONS.md` and `BACKLOG.md` change only in the shared b119/b124 commits (C-67, C-68, #298–#311), so they merge cleanly. Other files: 0 overlap between the three tips beyond `ce70da67`.
- **The root's untracked copies block a plain merge.** The three tips add **2,727** paths over main. **2,355** of them already sit **untracked** in the root, and every one is **blob-equal** to the branch (`git hash-object` vs `git rev-parse records/<b>:<path>`: same 2,355, differ **0**); 372 are absent. Precedent for this exact case: the `_quarantine_<date>_B<nn>_root-copies/` folders in the root (B27…B92).

## ITEM 1 — Build `records/b131` and fold the three tips into it
1. `git -C <root> worktree add _wt_b131rec -b records/b131 main` (`chmod 700`; the `_wt_*` naming is this repo's).
2. In `_wt_b131rec`, in this order: `git merge --no-ff records/b130 -m "Records: fold records/b130 (B119, B124, B126, B127, B129, B130) (B131)"`, then `records/b125`, then `records/b128`, each `--no-ff` with a message naming the branch and `(B131)`.
3. **Conflicts:** `history.md` only may be resolved, by keeping **every** entry from both sides, once, no word changed, ordered **by heading, newest at top**. Headings at drafting (commit times as a guide; read the headings yourself): B130 10-12 05:20 · B129 10-12 02:40 · B128 10-12 00:20 (heading dated 10-11) · B127 00:03 · B125 ADDENDUM-1 10-11 20:38 · B126 19:35/19:39 · B125 19:25 · B124 14:25 · then main's B123 · B122 · B120 · B121 (keep main's existing order) · then B119 (2026-10-10). Compare by heading, not by diff hunk. **Any conflict in any other file:** `git merge --abort`, then **STOP: NEEDS FRIDAY**.
4. **Assert after the three merges:** `merge-base --is-ancestor` = yes for all eight `records/b119…b130` against `records/b131`; for every path each tip added, `git rev-parse records/b131:<p>` = `records/<tip>:<p>` (count it; name any that differ); `history.md` heading count = main's + every tip's added headings (count `^## ` with `grep -i -c`), no duplicate heading.
**Never rebase, never force, never cherry-pick.**

## ITEM 2 — BACKLOG rows #312–#314 (one commit on `records/b131`)
**Next free row, measured:** max row number = **#311** on `records/b124`, `b125`, `b128` and `b130`; **#297** on main (`grep -o -E '^\| *[0-9]+ *\|'`). Re-measure on `records/b131` after ITEM 1; if anything holds #312 or above, take the next free number and say so.
**First check:** `grep -i -c` each id (`B128-N1`, `B130-F1`, `B130-F2`) in `records/b131:BACKLOG.md` (0 on all four refs at drafting). If one is there, skip it and say where.
**Shape:** the table rows #305–#311 (`| <n> | **Gate <id> (<grade>; <PR/branch>).** Oracle, verbatim: … What, verbatim: *"…"* | <State> |`). Quote the gate; never reword. Each row ends `Found <date> by gate <Bnnn>; recorded by B131 seat R, 2026-10-12.`

| Row | Gate id | Source, verbatim (quote these; read them in the file first) | State cell |
|---|---|---|---|
| #312 | **B128-N1** (Note, Q-1; B125 / PR #70) | `B128_STATUS.md:34`: *"B128-N1 (Q-1: the auditor's side is not established; the records lean "Datasec")"*; plus the N1 table row `:44` whole (Oracle = its #177 row quote; What = its Proved / Not established / Assumed cells; Fix = its last cell). Cross-reference row **#177** (`records/b130:BACKLOG.md:171`). | `OPEN: KAM DECIDES which side the auditor is on. As built (B125, merged #70 → 898ec99e): generated_by.user_id is masked (null) for the customer approver and the auditor (B128 :25, :112). The records lean "Datasec" (B128 :44). No C-entry rules it.` |
| #313 | **B130-F1** (Note; B129 / PR #71) | `B130_STATUS.md:36`: *"there is **no gap** at the `.98` boundaries in Chrome. There is an **overlap**. Chrome compares media-query widths with a 1/64 px tolerance, so at 699.99, 767.99 and 820.99 CSS px **two ranges apply at once**."* + `:37-39` (the bar still holds; window 0.011 px; *"**Note, ticket, not blocking.**"*) + the fix line from `:390`. | `OPEN (Note, not blocking; the bar holds at the overlap widths, B130 :37).` |
| #314 | **B130-F2** (Note, test strength; B129 / PR #71) | `B130_STATUS.md:41`: *"F2: the static test's "tile 601-900 px with no gap" title claims more than it checks."* + the F2 table row `:58` (What + Fix cells) + `:391`. | `OPEN (Note, test strength). Pairs with #313.` |

Commit message: `Records: BACKLOG #312 B128-N1 (Kam decides), #313 B130-F1, #314 B130-F2 (B131)`.

## ITEM 3 — History entry for the #69 / #70 / #71 merges (in your own history entry)
**Facts measured by the draft writer in `2_Project_Files` (code repo; read verbs only):**
- `git ls-remote origin refs/heads/main` = **`8e2a4b2e36ac28023f9f611dee5cabb2b2a69d35`**.
- `git log -1 72c038d8` = *"B126: details-screen polish (gate B127 GO WITH NOTES) (#69)"*, 2026-10-12 00:09:45 +11:00, parent `4e00d573`; tree **`13da9aed…`** = B127's gated merged tree (`B127_STATUS.md:15`).
- `git log -1 898ec99e` = *"B125: API contract correctness, 0.32.0 (gate B128 GO WITH NOTES) (#70)"*, 2026-10-12 00:29:34 +11:00, parent `72c038d8`; tree **`d1cd5818…`** = B128's gated tree (`B128_STATUS.md:210`).
- `8e2a4b2`: **not in the local clone** (`git log -1 8e2a4b2` = "unknown revision"). Its PR number (#71), subject and tree are **UNMEASURED** by the draft writer. B130 expects its tree = `a194a0bc^{tree}` = **`4e2648b35aeb1a8fbc876f328816497bb41f0dad`** (`B130_STATUS.md:328`; the drafter read `a194a0bc^{tree}` locally: equal to that).
**You:** in `2_Project_Files`, `git fetch origin` and read verbs only (no checkout, switch, commit, branch or push there). Then: `ls-remote origin refs/heads/main`; `git log -1 --format='%H %P %s' 8e2a4b2`; `git rev-parse 8e2a4b2^{tree}` must equal `4e2648b3…`; `merge-base --is-ancestor 898ec99e 8e2a4b2` = yes. If main moved past `8e2a4b2`, use it only if `8e2a4b2` is its ancestor, and say so. If the tree or the PR number differs, write what you measured, not what this brief says, and flag it under needs-Friday.
**Your entry** (top of `history.md` on `records/b131`, after the fold): heading `## 2026-10-12 — B131 (Security-Composer-R): records fold …`; body names, per merge, PR · squash SHA · gated tree = measured tree · gate line (B127 for #69, B128 for #70, B130 for #71); then the eight branches folded, rows #312–#314, C-69. **Say plainly: merged, not deployed.** The demo deploy of these merges is a separate card (`composer-new-words-look-demo-deploy-1012`, **open**, not ruled, at drafting): do not record it as ruled.

## ITEM 4 — CLARIFICATIONS C-69 (one commit on `records/b131`)
**Measured by the draft writer:** `decision_queue.sh list ruled | grep -i composer` = 84 lines; two Composer cards were ruled on or after 2026-10-11 (the register's `client_project` agrees: no other Composer card ruled since `composer-b116-words-look-1010`, which C-67 cites; control `grep -i -c composer-b116-words-look` = 1 on b119…b130).
- `composer-4e00d57-words-look-demo-deploy-1011` (a, 2026-10-11T14:02:37): **already recorded**, cited as C-68's authority (`records/b124:CLARIFICATIONS.md:1180-1182`; `grep -i -c` = 1 on b124…b130). **Write nothing**; name it in the STATUS.
- `composer-two-lanes-past-90pct-1011`: **0 hits** on main and on every `records/b119…b130` (`grep -i -c two-lanes-past-90pct`). **Record it as C-69.**

**Next free C-number, measured:** highest `^#+ *C-<n>` = **C-66** on main, **C-67** on b119, **C-68** on b124…b130; no `_wt_*` worktree copy holds C-69 or higher. **Next free = C-69.** Re-scan `records/b131` after ITEM 1; if C-69 is taken, STOP (a duplicate is a stop, not a renumber).

**C-69 — card `composer-two-lanes-past-90pct-1011`** (shape: C-64's; heading carries the card id, choice letter and time). Source: Friday's decision register (outside this project; **do not open it**: the lines you need are here, read by the draft writer from `0_Brain/dashboard/data/decisions.json`).
- title: *"Run two Composer build seats past the 90% usage stop?"*
- `ruled_choice` **a**, `ruled_ts` **`2026-10-11T08:21:43.556357+11:00`**. Quote the `ruled_ts`; Friday's reconcile writes it and it can trail Kam's tap by up to ~30 s.
- option a, label: *"Yes, both lanes now"*; detail: *"Two seats past 90%, each gated. The Composer joins HPSM-POC and the calculator in last night's lift until a new account."*
- `delivered_artefact`: **none** on the card. Say so.
- **Where it was used:** cite a file:line in a B125 or B126 brief/STATUS that names the 90% lift, if one does (`grep -rn -i '90%\|past 90\|usage stop'` over those files). If none does, write "not established". Never claim more than the file shows.
- Authority line, same form as C-64: *"Kam, live board 2026-10-11 08:21:43 (view=friday), "Decision composer-two-lanes-past-90pct-1011: a — Yes, both lanes now" (as relayed by Friday in `Briefs/2026-10-12_B131_SEAT-R_composer-records-fold.md`; this seat did not read the store)."*
- It is a scheduling ruling about seat usage, not a product ruling; record it as such (the heading says what it settles: two Composer build seats may run past the 90% stop, each gated).

Commit message: `Records: C-69 (Kam's 2026-10-11 two-lanes-past-90% card) (B131)`.

## ITEM 5 — Move the root copies aside, then fast-forward records main
1. **Before:** root `git --no-optional-locks status --porcelain --untracked-files=no` (expect only ` M …B26_STATUS.md`). If it lists any path in `git diff --name-only main records/b131`, **STOP: NEEDS FRIDAY**. Never stash, checkout, switch, reset, `update-ref`, or `fetch . x:main`.
2. **Root copies:** for every path in `git diff --name-only --diff-filter=A main records/b131` that exists untracked in the root: compare `git hash-object <root>/<p>` with `git rev-parse records/b131:<p>`. **Equal** (2,355 expected): MOVE it to `_quarantine_2026-10-12_B131_root-copies/<same relative path>` (0700), keeping a manifest (path, sha256 before, sha256 after). **Any that differ:** move nothing, **STOP: NEEDS FRIDAY**, name them. Untracked paths the merge does not add: leave them.
3. `git -C <root> merge --ff-only records/b131` (main `441fa893` is an ancestor of `records/b131` by construction). If `--ff-only` refuses, **STOP: NEEDS FRIDAY**. Never `--no-ff` on main, never force.
4. **Read back:** `git rev-parse main`; `merge-base --is-ancestor` = yes for `records/b119`, `b124`, `b125`, `b126`, `b127`, `b128`, `b129`, `b130`, `b131` against main; `git for-each-ref refs/heads/records` minus ancestors of main = exactly `records/b20` and `records/b58-wip-on-44029f6` (the two not commissioned); `main:CLARIFICATIONS.md` `### C-` count (`grep -i -c`) = C-68's count + 1 (control: the count on `records/b130`); `main:BACKLOG.md` holds #312–#314 (each id `grep -i -c` = 1); root tracked status = step 1's. Quarantined count = manifest rows = files the merge then wrote back (`git ls-files` on those paths).
5. **Delete no branch and remove no worktree.**

## Ports
None needed: **bind nothing**.

## Leak + secret scan
Over `git diff 441fa893..records/b131` (only the paths your own commits touched, plus the merge commits' conflict resolution), the commit messages and this STATUS before its last line: a records leak scan (counts only, never the matched text, with a positive control that fired) and `gitleaks` with a planted canary that must be caught. **Never print an avoid list.** Expected, to adjudicate, not to hide: `auditor@datasec.example.test` if you quote B128 `:44` whole (synthetic, already in the code repo); the year `2026`; HTTP `404`/`412`.

## UNMEASURED (by the draft writer)
- **`8e2a4b2`'s PR number, subject and tree:** not in the local clone (no fetch at drafting). ITEM 3 closes it.
- **Whether any seat writes `records/*` or main before you run:** re-run `for-each-ref` + `merge-base --is-ancestor` first. Fold anything new only if it is a `records/b1xx` branch for a Composer brief and it contains, or is contained by, one of the three tips; otherwise list it under needs-Friday.
- **Whether a B125/B126 file names the 90% lift:** ITEM 4 closes it.

## HOLDS
- Datasec / Datasec Security Composer only; no other project's or client's names, tickets or paths in anything you write.
- **No product code.** `2_Project_Files`: `fetch` and read verbs only. No push anywhere (the records repo has no remote). No PR. CodeQL policy unchanged: this round pushes nothing.
- **No deploy, no Azure, no setting change, no demo access. Nothing to any human.** No Jira (none exists). No mail except your wrap to Friday.
- **Own worktree:** `_wt_b131rec` only. Do not commit in any other `_wt_*` worktree; the eight source worktrees stay as they are.
- **Never delete; quarantine** (`_quarantine_2026-10-12_B131_<what>/`, 0700) and say so. No `branch -d/-D`, `worktree remove`, `gc`, `prune`.
- **Records:** write only `records/b131` (ITEMS 1–4), the fast-forward of `main` (ITEM 5), the quarantine move (ITEM 5) and your STATUS. `CLAUDE.md` is Friday's: do not edit it. Existing BACKLOG rows and C-entries are not edited; you only add.
- **Instruments:** verdicts are ratios with denominators; every scanner zero has a positive control that fired; every grep for a phrase is `-i`.
- If a measurement contradicts this brief, the measurement wins. Say so in the STATUS, and STOP if it changes what you would do.

## End
The last line of `1_Project_Definition/Briefs/2026-10-12_B131_STATUS.md` is exactly one of:
- `RECORDS DONE: <one line>`;
- `STOPPED: NEEDS FRIDAY` and ONE question.
