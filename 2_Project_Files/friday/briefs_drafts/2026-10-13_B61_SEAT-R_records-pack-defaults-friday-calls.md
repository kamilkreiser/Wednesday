From Friday (laptop seat), Datasec / MPS Commercial Calculator. No mail key in this project: the STATUS file is the wrap.
# BRIEF B61 · SEAT-R: MPS RECORDS: Kam's 11 pack defaults (MPS-1…MPS-11) as C-23, Friday's rulings M1/M2/M4/M7/M8/M9 into BACKLOG, fold `records/b46` + `records/b53` into records main, Jira M1 + M6 + MPS-10 (read first)
**Fired: 2026-10-13 03:52 AEDT.** Pane `Datasec/MPS-R`. Your commission is THIS file, at `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-13_B61_SEAT-R_records-pack-defaults-friday-calls.md` (Friday's tree, read-only to you). Step 0: copy it into your `1_Project_Definition/Briefs/` unchanged, as the project's record. **RECORDS ONLY: no product code.** The last SEAT-R seat, B44, is finished (`Briefs/2026-10-12_B44_STATUS.md` ends `RECORDS DONE: records main @ 38efff2f…`).
**Report:** `1_Project_Definition/Briefs/2026-10-13_B61_STATUS.md`. Last line exactly one of: `RECORDS DONE: records main @ <sha>, C-23 y, rows <n>, folded b46+b53 y/n, Jira <keys> read back` · `STOPPED: NEEDS FRIDAY` and ONE question.

## AUTHORITY (verbatim sources; quote, never reword)
- **Kam's pack.** `FRIDAY/0_Brain/reference/2026-10-12_datasec-decisions-pack/decisions-pack.html`, section 1 (MPS-1…MPS-11) and the words list (MPS-11). Card `mpscalc-decisions-pack-1012`, read by the drafter with `decision_queue.sh show` (03:4x AEDT): `status: ruled`, `ruling: choice='a' ruled_ts=2026-10-12T20:12:58.023381+11:00`; option a, verbatim: *"All defaults for this project"* / *"Accept every bold default MPS-1 to MPS-11. Friday folds them into the next MPS briefs. Nothing deploys or changes on the hosted site without its own card."* You may open the pack HTML/PDF read-only to copy each row's question, options, default and "if you pick the default" text **byte for byte**.
- **Friday's own rulings.** `FRIDAY/0_Brain/reference/2026-10-12_datasec-decisions-pack/friday-calls-RULED.md` (03:38 AEDT: "Every row is ruled AS PROPOSED … except" C12, M1, C11, N1–N4) and the rows in `friday-calls-proposed.md` beside it (MPS table, M1–M10). These are Friday's, not Kam's: record them as **"Friday's ruling (coordinator), 2026-10-13"**, never as a C-entry.
- **Source map for every pack ID** (which BACKLOG row each one rules): `friday-calls.md` §3 "MPS" table beside the pack.

## THE RECORDS ROUTE (measured by the drafter, read verbs only, `--no-optional-locks`, 03:4x AEDT)
- `BACKLOG.md` is at the **project root** (`git ls-tree --name-only main` at the root lists it), so the records repo is the **project-root** git repo. `<root>/.git/config`: **0** `remote` lines. **Nothing is pushed.** Commit locally only.
- Records `main` = **`01ef80353144ce4363d28eb63b8f0ebd6118e4e2`** (B50, `Design: MPS one-pager proposal mockup for Kam`).
- `records/*` NOT ancestors of `main` (each `merge-base --is-ancestor <b> main` rc 1): **`records/b46`** `31a84774ff13d64f947973c1a3f3e686831b2ef8` (`main...` = `4 1`; forks at `222c73eb`, B45; adds `history.md` +7, `BACKLOG.md` +30 over its base); **`records/b53`** `d05a2896bba5e2cdf439034c5042244f9111c852` (`0 1`; `BACKLOG.md` +59); **`records/b54`** `1129a250…` (`0 1`; +21); **`records/b58`** `c267f27121c7…` (`0 2`, contains b54; +63). No other `records/*` is unmerged (17 branches read).
- **Fold `b46` and `b53` only.** Their code is merged (PR #28 B46/B49; PR #29 B53 = code main `d711b42c`, GitHub commits API 03:43). **Do not fold `b54` or `b58`**: B54's code is NOT merged (gate B57 NO GO; fix round B58 `727c7c89` is awaiting gate B59). Name them under needs-Friday.
- `CLARIFICATIONS.md` on main: `### C-` count **23** (C-01…C-22 plus C-06a), last `### C-22` at `:298`, file 313 lines; the same count (23) on `records/b46`, `b53`, `b54`, `b58`. **Next free = C-23.** Re-count on your branch after the fold; a duplicate is a STOP, not a renumber.
- **Root tracked status: UNMEASURED by the drafter** (no `status` taken). Your step 1 measures it.

## ITEM 1: branch and fold
1. Root `git --no-optional-locks status --porcelain --untracked-files=no` (record it). Worktree `.tools/wt-B61-records` on new branch `records/b61` from `main` (`chmod 700`).
2. In the worktree: `git merge --no-ff records/b53 -m "Records: fold records/b53 (B53 remainders) (B61)"` (main is its ancestor), then `git merge --no-ff records/b46 -m "Records: fold records/b46 (B46 remainders) (B61)"`. A conflict in `history.md` or `BACKLOG.md` may be resolved **only by keeping both sides' entries/rows, once, no word changed** (history newest at top by heading). Any other conflict: `git merge --abort`, STOP: NEEDS FRIDAY. Never rebase, force or cherry-pick.
3. Assert: `records/b46`, `records/b53` are ancestors of `records/b61`; `BACKLOG.md` holds `[B46-R1]`, `[B46-Q2]`, `[B46-R4]` (drafter: `records/b46:BACKLOG.md:687, :682, :702`) and `[B53-R7]` (`records/b53:BACKLOG.md:783`) once each (`grep -c -F`).

## ITEM 2: C-23, Kam's pack (one commit)
Heading: `### C-23 — Kam accepts every default of the MPS decisions pack (MPS-1 to MPS-11) (2026-10-12, 20:12 AEDT)`. Shape: C-21's (`main:1_Project_Definition/CLARIFICATIONS.md:287-296`): card id · channel (Kam, live board) · `ruled_choice` **a** · `ruled_ts` quoted · option label + detail verbatim · source line naming this brief as the relay ("this seat did not read the store").
Then a table, one row per ID, **MPS-1 … MPS-11**: `ID | the question (verbatim) | default ruled (verbatim, bold text) | "If you pick the default" (verbatim) | BACKLOG row(s) it rules (from the source map)`. The words list rows for MPS-11 go under the table verbatim (*"1 quote"* / *"1 quote needs follow-up"*; "0 and 2+ stay quotes").
Add one line, marked as Friday's note, not Kam's: *"MPS-7's default came from the lane table (an Approver may change or clear it); the B46 brief's own default was 'not possible (409)' (`records/b46:BACKLOG.md:685`). Kam ruled the pack's default."* (source: `friday-calls.md` §2 item 3).
Commit: `Records: C-23, Kam's MPS decisions pack defaults MPS-1…MPS-11 (B61)`.

## ITEM 3: BACKLOG lines (one commit). Add, never edit or delete existing text.
**3a. Pack rows.** Under each row the source map names, add one dated line: `  - Ruled 2026-10-12 (C-23, MPS-n): <the default, verbatim>. <"If you pick the default", verbatim>.` Rows (drafter's lines on `main`; re-find them by id on your branch): MPS-1 `[B42-L5]` :581 · MPS-2 `[B21-2]` :215 · MPS-3 `[B46-R1]` (b46 :687) · MPS-4 `[B21-4]` :229 · MPS-5 `[B38-N3]` :439 · MPS-6 `[B38-N4]` :445 · MPS-7 `[B46-Q2]` (b46 :682) · MPS-8 `[B40-R4]` :496 · MPS-9 `[B47-D3]` :694, `[B47-D4]` :700 · MPS-11 `[B46-R4]` (b46 :702). MPS-10 has no BACKLOG row (its tickets are Jira, ITEM 4). **Tick nothing for the pack**: a row may carry more than the one question (e.g. `[B40-R4]` is also lane A3's overlay measure), so every pack row stays `[ ]` with its ruling line; Friday closes rows when the work they name is done.
**3b. Friday's rulings** (each line: `  - Friday's ruling (coordinator), 2026-10-13 (friday-calls-RULED.md, row Mn): <what>; evidence: <the row's STATE NOW, verbatim>.`):
| Row | Line (main) | Write | Tick? |
|---|---|---|---|
| M2 | :46 "CodeQL ruleset did not block the first push" | CLOSED-ALREADY: org ruleset `24139430` "Security scan rule" active on MPS `main` with `code_scanning` (CodeQL) and `non_fast_forward`; the 09-30 miss was the branch-creating push, before coverage | `[x]` |
| M3 | :162 leak scanner | RULE-OTHER: version it as `tools/leakscan/` + a test via a CodeQL PR (build seat B62) | stays `[ ]` |
| M4 | :195 `[B08A2-6]` | RULE-OTHER: standing brief line "build with `-nodeReuse:false -p:UseSharedCompilation=false`; nobody runs `dotnet build-server shutdown` while another seat is live"; `ps` 03:2x showed 0 such processes | `[x]` |
| M7 | `[B42-L4]` :574 | CLOSED-ALREADY: refused (Friday's default), built in B53, gate B57 "(9) B42-L4 duplicate keys refused: GO WITH NOTES", merged in `d711b42c` (#29). Add: "Residue: `[B53-R7]` (a document validated before B53 with a repeated key still activates, last key wins)." | `[x]` |
| M8 | `[B43-Q5]` :649 | CLOSED-ALREADY: B53 built it route-local, no `Program.cs` change (B53 STATUS `:17`); gate B57 CLOSED-WITH-NOTES; merged #29 | `[x]` |
| M9 | `[B27-H4]` :286 | CLOSED-ALREADY on the merits: the `GET /inventory/audit` 503 arm is "not needed" (audit serves the last good in-memory document; `B54_STATUS.md:137-139`). **Do not tick**: B54 is not merged (B58 awaits gate B59) | stays `[ ]` |
| M1 | find the row naming MPSCALC-61 if any (`grep -n -i 'MPSCALC-61'`; the drafter found none on main) | if a row exists: "dependency + code scanning measured ON (code_security, Dependabot alerts 204, security updates, CodeQL default setup); DAST not adopted this phase; secret scanning NOT enabled (paid on a private repo = Kam's switch; not carded)". If none: write nothing in BACKLOG; Jira carries it (ITEM 4) | — |
| M6 | none expected | Jira only (ITEM 4) | — |
Re-read each cited STATUS line before you quote it (`B53_STATUS.md:17,:20`, `B57_STATUS.md:9,:12`, `B54_STATUS.md:137-139`); if a line moved, cite the line you read.
Commit: `Records: pack rulings on rows (C-23) and Friday's M1-M9 rulings (B61)`.

## ITEM 4: Jira (read first; write only if the row still applies; quote the read)
Credentials by name only: `4_Credentials/.env` `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN` (B44's helper method, a fresh copy in your scratchpad). Never print, log or write the token.
For each key: (1) `GET /rest/api/3/issue/<key>?fields=status,summary,comment` and `GET …/transitions`; quote status name + newest comment id in the STATUS. (2) If it is already Done / already carries this text, SKIP and say so. (3) Write. (4) Read back by id, byte-equal.
| Key | Write (one ADF paragraph, verbatim) | Transition |
|---|---|---|
| MPSCALC-61 (M1) | `Friday's ruling 2026-10-13: the scanning half is already on for datasecau/MPS-Commercial-Calculator: code security enabled, Dependabot alerts on (API 204), Dependabot security updates enabled, CodeQL default setup configured (csharp, js/ts, python, actions). DAST: not adopted for this phase. Secret scanning: not enabled (a paid feature on a private repo; Kam's switch if wanted).` | to Done **only** if the workflow offers a Done transition; else comment only and say so |
| MPSCALC-56 (M6) | `Entra SSO has been live since PR #10 (#11 9fe66dc, #12 98d829f). Moved to Done by Friday's ruling 2026-10-13.` Before writing, `git -C 2_Project_Files log -1 --format='%H %s' 9fe66dc` and `98d829f` (read verbs): if either is not found, comment WITHOUT the SHAs and say so | Done |
| MPSCALC-66, -81, -84 (MPS-10) | `Closed by Kam's decisions pack 2026-10-12 (MPS-10, default a: "Close all three"; C-23). <MPS-10's "If you pick the default" text, verbatim>.` | Done |
No other Jira write. No ticket is created.

## ITEM 5: fold into records main
1. Re-run root tracked status; if it lists any path in `git diff --name-only main records/b61`, STOP: NEEDS FRIDAY. Never stash, checkout, switch, reset, `update-ref`.
2. `git -C <root> merge --ff-only records/b61` (main is its ancestor by construction). If refused: STOP.
3. Read back: `rev-parse main`; `records/b46`, `b53`, `b61` ancestors of main; `### C-` count = 24; `records/b54`, `b58` still NOT ancestors (untouched). Delete no branch, remove no worktree.

## Leak + secret scan
Copy `.tools/qa-B58/tools/{leakscan.py,qalib.py}` (sha256 `71a7a64e…` for leakscan.py, equal in qa-B57/B58/B59) and `leak58.py` into `.tools/qa-B61/`; lists read-only by path; counts only; a positive control that fired; plus `gitleaks` with a planted canary. Scope: `git diff 01ef803..records/b61` (your commits and merge resolutions), commit messages, the Jira texts, this STATUS. **Never print an avoid list.**

## HOLDS
- **Datasec only.** No other client's names, tickets or paths.
- No product code; `2_Project_Files`: read verbs only. No push anywhere, no PR, no deploy, no Azure, no hosted access. Nothing to any human beyond the Jira writes in ITEM 4.
- Own worktree `.tools/wt-B61-records` only. MPS-B (B60) and MPS-E (B59) are live: never touch their worktrees or branches.
- `CLAUDE.md`, `JIRA.md` untouched. Existing C-entries, rows and history entries are never edited; you only add lines. Never delete; quarantine (`.tools/_quarantine/2026-10-13_B61_<what>/`, 0700). Never force-push, never dismiss a CodeQL alert. No ports: bind nothing.
- If a measurement contradicts this brief, the measurement wins: say so, and STOP if it changes what you would write.
