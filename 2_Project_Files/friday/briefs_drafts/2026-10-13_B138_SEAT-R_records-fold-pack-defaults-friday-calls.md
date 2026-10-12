From Friday (laptop seat), Datasec / Datasec Security Composer. Replies and wraps go to friday-laptop-agent@agentmail.to (if this project has no mail key, your STATUS file is the wrap).
# BRIEF B138 · SEAT-R: COMPOSER RECORDS: fold `records/b134`, `b135`, `b136` (with b132, b133) into records main (C15), history for B134–B136 (C16), Kam's 19 pack defaults as C-71, Friday's rulings C3/C5/C7/C8/C9/C10/C13/C14/N1/N2 onto their rows
**Fired: 2026-10-13 03:52 AEDT.** Pane `Datasec/Security-Composer-R`. Your commission is THIS file, at `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-13_B138_SEAT-R_records-fold-pack-defaults-friday-calls.md` (Friday's tree, read-only to you). Step 0: copy it into your `1_Project_Definition/Briefs/` unchanged, as the project's record. **RECORDS ONLY: no product code, no deploy, nothing on Azure, no demo access.** The last SEAT-R seat, B131, is finished (`Briefs/2026-10-12_B131_STATUS.md` ends `RECORDS DONE: records main @ dab4854d…`).
**Report:** `1_Project_Definition/Briefs/2026-10-13_B138_STATUS.md` (BLUF · ITEM 1–5 · UNMEASURED · NOT DONE / NOT COVERED · needs-Friday · Leak + secret scan · worktrees and files left). Last line exactly one of: `RECORDS DONE: records main @ <sha>, folded b132-b136 5/5, history 3, C-71 y, rows <n> lines` · `STOPPED: NEEDS FRIDAY` and ONE question.

## AUTHORITY
- **Kam's pack:** `FRIDAY/0_Brain/reference/2026-10-12_datasec-decisions-pack/decisions-pack.html` §2 (COMP-1…COMP-19) + the words list (COMP-4, COMP-12, COMP-13, COMP-19). Card `composer-decisions-pack-1012`, read by the drafter (`decision_queue.sh show`, 03:4x AEDT): `ruling: choice='a' ruled_ts=2026-10-12T20:12:54.687610+11:00`; option a verbatim: *"All defaults for this project"* / *"Accept every bold default COMP-1 to COMP-19. Friday folds them into the next Composer briefs. New words and looks still come to you on their cards before any demo deploy."* Open the pack read-only and copy text **byte for byte**.
- **Friday's rulings:** `friday-calls-RULED.md` (03:38 AEDT) + rows C1–C17 and N1–N2 of `friday-calls-proposed.md` beside it. Record them as **"Friday's ruling (coordinator), 2026-10-13"**, never as a C-entry. Note RULED's exceptions: **C11 is Kam's card** (`composer-k-q32-refuse-names-1013`): record nothing for it. **C12's prune is NOT ruled** (carded to Kam): record nothing for it.
- **Pack → row map:** `friday-calls.md` §3 "Composer" table (row numbers are `records/b133` lines; BACKLOG is unchanged b133 → b136, see below).
- **Jira: none.** This project has no Jira project (`BACKLOG.md` row #4: key `PCOMP` proposed and on HOLD). Write nothing to any Jira.

## THE RECORDS ROUTE (measured by the drafter, read verbs only, `--no-optional-locks`, 03:4x AEDT)
- Records repo = the **project root** (`ls-tree --name-only main` lists `BACKLOG.md`, `1_Project_Definition`, `5_Project_History`). `.git/config`: **0** `remote` lines. Nothing is pushed.
- Records `main` = **`dab4854dc0442e46cd18b1bd202c300d433a26bf`** (B131's fold).
- Unmerged `records/*` (67 read; `merge-base --is-ancestor <b> main` rc 1):
| branch | tip | `main...<b>` | contains |
|---|---|---|---|
| `records/b132` | `35d2da0c` | 0 1 | B132 STATUS, evidence, history |
| `records/b133` | `e04b0b13` | 0 3 | b132 + C-70, BACKLOG → DEPLOYED, history (B133) |
| `records/b134` | `23419a8f81e7…` | 0 4 | b133 + B134 STATUS + evidence (36 files over b133) |
| `records/b135` | `446cb227d9fa…` | 0 4 | b133 + B135 STATUS + evidence (91 files) |
| `records/b136` | `c6da79ff3e09…` | 0 4 | b133 + B136 STATUS + evidence (507 files) |
  b132 ⊂ b133 ⊂ each of b134/b135/b136; **b134, b135, b136 are mutually divergent** (none is an ancestor of another). Files each adds over b133: **0 overlap** pairwise (`diff --name-only records/b133 records/<b>`, compared). None of them touches `BACKLOG.md`, `CLARIFICATIONS.md` or `history.md` over b133.
- **Not commissioned** (leave, name under needs-Friday as before): `records/b20` `3f3d5cdf` and `records/b58-wip-on-44029f6` `35b83e44`.
- `CLARIFICATIONS.md` on `records/b136`: 1283 lines, last `### C-70` at `:1244`. **Next free = C-71.** `BACKLOG.md` on b136: 310 lines, last row **#314** (`:310`). `history.md` on b136 tops out at the B133 entry (`:3`); **0** entries for B134, B135, B136.
- **Root untracked copies:** of the **752** paths that b134 ∪ b135 ∪ b136 add over main, **142** already sit untracked in the root and every one is content-equal to the branch (sha256 of the root file = sha256 of `git cat-file -p records/<b>:<p>`; differ **0**); **610** are absent. Same case as B131 (quarantine precedent).
- Root tracked status: **UNMEASURED** by the drafter (you measure it in ITEM 5 step 1).

## ITEM 1: build `records/b138` and fold (C15)
1. `git -C <root> worktree add _wt_b138rec -b records/b138 main` (`chmod 700`).
2. In `_wt_b138rec`: `git merge --no-ff records/b134 -m "Records: fold records/b134 (B132, B133, B134) (B138)"`, then `records/b135`, then `records/b136`, each `--no-ff` naming the branch and `(B138)`. Expected: no conflict (disjoint files). **Any conflict: `git merge --abort`, STOP: NEEDS FRIDAY.** Never rebase, force or cherry-pick.
3. Assert: b132, b133, b134, b135, b136 ancestors of `records/b138`; for every path each tip adds, `rev-parse records/b138:<p>` = `records/<tip>:<p>` (count; 0 differ).

## ITEM 2: history entries B134, B135, B136 (C16; one commit)
Top of `history.md`, above B133, newest at top (B136, B135, B134). Shape: the B133 entry (`records/b136:5_Project_History/history.md:3-11`). Heading ends with the STATUS's last line: B134 `READY FOR QA: b134/renderer-titles-fold-trigger-drift @ ed0f531e…` (STATUS 219 lines), B135 `READY FOR QA: b135/web-test-strength-build @ 3983732f…` (223 lines), B136 `READY FOR REVIEW` with `overall: GO WITH NOTES` (424 lines, `:20`). Every bullet is a fact copied from that STATUS with its line cited; no new adjective. Add one line per entry, marked *(B138 records, measured)*: in `2_Project_Files` (`fetch` + read verbs only) `git log -1 --format='%H %P %s'` of the merge commits for **#73 (B134)** and **#74 (B135)**: drafter's reads, GitHub API 03:43: code main `eddb484bc206c830adfa5b75eb3e0d890afb3d45` "Web test strength, harness and build (B135; gate B136 GO WITH NOTES) (#74)", merged 12:29Z; #73's merge SHA is UNMEASURED by the drafter. Write "merged, not deployed" unless a deploy STATUS (B137) exists in `Briefs/` with a `DEPLOYED` last line when you run; if it does, cite it, do not record it as a C-entry.
Commit: `Records: history B134, B135, B136 (B138)`.

## ITEM 3: C-71, Kam's pack (one commit)
`### C-71 — Kam accepts every default of the Security Composer decisions pack (COMP-1 to COMP-19) (2026-10-12, 20:12 AEDT)`. Shape: C-69 (card-ruling entry: card id, choice, `ruled_ts` quoted, option label + detail verbatim, "as relayed by Friday in this brief; this seat did not read the store"). Then a table, one row per COMP-n: question · options · default (verbatim) · "if you pick the default" (verbatim) · K-Q · BACKLOG rows (from the map). Then the words-list rows for COMP-4, COMP-12, COMP-13, COMP-19 verbatim. One Friday's-note line (not Kam's): *"COMP-6's default keeps the id masked although the records lean 'Datasec' (#312); Kam ruled the pack's default."*
Commit: `Records: C-71, Kam's Composer decisions pack defaults COMP-1…COMP-19 (B138)`.

## ITEM 4: BACKLOG lines (one commit; append to the State cell, never rewrite earlier text)
**4a. Pack:** on every row the map names for COMP-1…COMP-19, append ` · Ruled 2026-10-12 (C-71, COMP-n): <default, verbatim>.` State stays as is except: **COMP-10 (#278)** → prefix `CLOSED (C-71, COMP-10: view source does not count)`; **COMP-6 (#312)** → `RULED (C-71, COMP-6): keep it hidden from the auditor`. All others keep their state (builds, cards or deploys follow).
**4b. Friday's rulings** (append ` · Friday's ruling 2026-10-13 (C<n>): <text>`):
| Ruling | Rows | Text | New state prefix |
|---|---|---|---|
| C3 (K-Q20) | #269 | file names stay as they are (stored outputs and e2e downloads pin them; `render.ts:170` held) | — |
| C14 + N1 | #269 | scope built and gated: *"FIXED for worksheet and change report; file names HELD"*; the generation block keeps "Policy <HPSM name>" (a relabel is Kam's words; B136-N1 `:83`, Q(1) `:394`) | `FIXED (worksheet, change report); file names HELD` |
| C5 (K-Q23) | #66, #70, #71 | leave as built; #71 closes as "keep" | #71: `CLOSED (keep)` |
| C7 (K-Q25) | #157, #176 | no change until an external consumer exists | `CLOSED (noted)` |
| C8 (K-Q26) | #197 | monospace allowed for codes in the gate's token rule (gate brief text; no product change) | `CLOSED` |
| C9 (K-Q27) | #246 | leave it (never delete) | — |
| C10 (K-Q28) | #313, #314 | #313 accepted (0.011 px overlap; no CSS change, B135 STATUS `:183`); #314 done (B136 `:13` "B135 #314: GO"; merged #74) | #313 `CLOSED (accepted)`; #314 `DONE (#74)` |
| C13 | #120, #202, #267, #262, #266, #268, #270, #283, #180, #79, #151, #222, #235 | close as done-already; cite the drafter's evidence where measured (`friday-calls-proposed.md` C13: #202/#267 `purity-lint.test.ts:21`; #266 `DEPLOY.md:153`; #268 `types.test.ts:297`; #262 via #266+#268; #270 `policyTarget.ts:31`; #120 `FeedbackWidget.tsx:341-346`), else "closed by Friday's ruling (not re-read)" | `CLOSED` |
| N2 | #212, #164 | #212: the ≤ 2 s blind window of #143's soft check is accepted (B136-N9 `:91`, Q(2) `:395`); #164 closes on the limit-with-reason option, met by B135 (vendor split + limit 540; B136-N15 `:97`, Q(3) `:396`) | #164 `CLOSED (#74)` |
Before each write, `grep -n -E '^\| *<n> *\|'` on your branch and quote the row's current State in the STATUS. If a row's state already says DONE/CLOSED, append nothing and say so. **No new rows**: B136's own proposed tickets (F1, N2, N5, N10, N16; `B136_STATUS.md:57`) are not commissioned; list them under needs-Friday.
Commit: `Records: pack rulings (C-71) and Friday's C3-C14, N1, N2 on rows (B138)`.

## ITEM 5: root copies aside, then fast-forward main
1. Root `git --no-optional-locks status --porcelain --untracked-files=no`; if it lists any path in `git diff --name-only main records/b138`, STOP. Never stash, checkout, switch, reset, `update-ref`.
2. For every path in `git diff --name-only --diff-filter=A main records/b138` that exists untracked in the root: compare content (sha256 vs `cat-file -p`). Equal (142 expected): MOVE to `_quarantine_2026-10-13_B138_root-copies/<same path>` (0700) with a manifest (path, sha256 before/after). Any differ: move nothing, STOP: NEEDS FRIDAY.
3. `git -C <root> merge --ff-only records/b138`. If refused: STOP. Never `--no-ff` on main, never force.
4. Read back: `rev-parse main`; b132–b136 and b138 ancestors of main; unmerged `records/*` = exactly `records/b20` and `records/b58-wip-on-44029f6`; `### C-` count = b136's + 1; history has the 3 new headings. Delete no branch, remove no worktree.

## Leak + secret scan
Over your own commits' diff (not the folded evidence), commit messages and this STATUS: the records leak scan B131 used (counts only, positive control fired) and `gitleaks` with a planted canary. **Never print an avoid list.**

## HOLDS
- **Datasec / Datasec Security Composer only.** No other project's or client's names, tickets or paths.
- No product code; `2_Project_Files`: `fetch` and read verbs only. No push, no PR, no deploy, no Azure, no demo, no Jira, nothing to any human.
- Own worktree `_wt_b138rec` only; the `_wt_b13x` worktrees stay as they are. `CLAUDE.md` untouched. Existing rows, C-entries and history entries are only appended to, never edited. Never delete; quarantine. Never force-push, never dismiss a CodeQL alert. No ports: bind nothing.
- Build seats B139 (SEAT-C) and B140 (SEAT-D) may run beside you in `2_Project_Files`; you touch nothing there.
- If a measurement contradicts this brief, the measurement wins; say so, and STOP if it changes what you would write.
