STARTABLE: YES (after your stamp: the six slot lines of the kit hold four underscores; one Q-item below changes what the seat is allowed to do, defaults given)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-02_B1076_SEAT-R122_mps-records-batch-4c.md` (125 lines). Seat `Datasec/MPS-R122`, evidence suffix `R122`, model row C8 (`model-routing.md:98`), `BRIEF_SEAT_LEVEL=sonnet` inside the launch quotes, `claude-sonnet-5-5` from `models_latest.json:22-23`. No ports.

## BLUF
The nine keys of the B1067 wrap re-derive to **7 keys + 2 dropped**: MPSCALC-35, 36, 48, 51, 57, 95, 101 (kit order). Dropped: MPSCALC-13 (Epic, no landing named, one comment that says "Not merged") and MPSCALC-69 (Q-03, a question for the product owner, label `question-for-kam`, no merged change). Expected result: 7 comments, 2 moves (MPSCALC-95, -101), 4 holds (35, 36, 48, 51), 1 conditional (57). Max 14 writes.
Correction to the relayed list: MPSCALC-95 and -101 are not "merged, no PR number". Their comments name MPS #33 (bf60fe83) and MPS #35 (13d8fd8b4a80f47cfb2e7ea30e4beec374672ba1); the earlier regex missed "Merged as". The other five name branches they call "not merged"; I identified them by head branch (GET pulls?head=...; nonsense branch returns an empty list): #3, #6, #7, #11, #15, #16 exactly, #18 and #20 by title and B20's lines (a reading, said so in the kit).

## Facts re-measured (instrument; control)
- Root main `b76b9d1a98d879f539cde0f0aee7a4a45241e83e` (B1067's ff; `rev-parse`); HEAD refs/heads/main; remote count 0; 50 branches, newest `records/b1067`; `records/b1076` absent (rc 1; control `records/b1067` prints b76b9d1); `.tools/b1076`, `.tools/wt-b1076-records` absent (control `.tools/b1075` listed); `.tools/.git-lock`, MERGE_HEAD, index.lock absent; `git status --short` 873; numstat BACKLOG +2576, JIRA +407, history +471, CLARIFICATIONS empty; CLARIFICATIONS 2038 lines, 79 C-headings, C-79 at 1712 (C-78 once as control, C-80 0 on all 50 branches), C-79 text at 1714 and 1716, B1067's section at 2001 (item 1 at 2005, readings (o)-(r); item 3 at 2030).
- Jira (GET, 357 issues, 633 of 633 comments): Done 125, Backlog 232; `zzqxnonexist` 0, `key = MPSCALC-341` 1, `-357` 1, `B1076` 0, label 0, `B1067` 21, `B1064` 30; myself and project 200.
- Code main `3496da33...` unmoved; open PRs [121, 120] (dependabot bumps; body regex over both: false, control string fires); `pulls/99999` and `compare/nonsense...main` 404.
- Ten PRs read (#3, 6, 7, 11, 15, 16, 18, 20, 33, 35): all merged, base main; every squash `ahead` of code main and of `e027ebd0` (control: #73 squash `ahead`); check-runs all success (2/2, 2/2, 6/6, 3/3, 8/8 x6); `ci` push run success attempt 1 for #15, 16, 18, 20, 33, 35; **no `event=push` run listed for #3, #6, #7, #11** (UNMEASURED why; the kit tells the seat to re-query without the event filter).
- Batch census (frame: 232 Backlog keys, comments only, no records marker): `merged|squash|MPS #n|(#n)` hits exactly 11 = the 9 + MPSCALC-78 + -202 (control: all fire; -64 and -195 do not).
- CI predicate re-read at code main: `ci.yml` 123 lines, jobs dotnet/web/python/package, `dotnet test` 1, `npm test` 1, Playwright 0.
- Live panes (tmux, 01:00 AEDT): tuesday, fleet-monitor, MPS-G268, MPS-M68, MPS-G265, plus HPSM-POC-G266/G267/H95, NexusAI-G264, Security-Composer-J38. No MPS records seat.

## Live-pane test of every REFUSE line (the point you asked for)
- The B1067 form of REFUSE 7 (`grep -i 'Datasec/MPS'` on panes or ps) would FIRE on M68, G265 and G268: measured 3 pane hits and 3 ps hits. The kit replaces it with an anchored `^Datasec/MPS-R[0-9]+$` (must print 1 after launch = own pane; before launch 0; control `^Datasec/MPS-M68$` 1) and a ps filter on `SEAT-R[0-9]+_mps-records` (0 now; control `SEAT-M68_mps` lists the M68 launch), and says in words that M68/G265/G268 are expected.
- REFUSE 5 `.git-lock`: absent now, but M68 pushes under it and the gates clone; the kit makes a held lock a 15-minute poll, not a refusal (as the B1067 template already did, now stated with the three seats named).
- REFUSE 2, 3, 4, 6, 8, 9 tested against the numbers above; none depends on a sibling's state. REFUSE 9 treats a landed M68 PR as information.
- Partition both ways: from the kit's side (seat touches 7 keys, root records, Jira, `.tools/b1076`); from the siblings' side, read in their kits: B1074 lines 62 and 68 (M68 holds CLARIFICATIONS, BACKLOG, records branches and Jira as forbidden), B1070 and B1075 ("write no Jira"; their lines 14 and 15 describe the B1067 records seat as the root-repo/Jira writer, so they expect this footprint). Their keys (300, 215, 317, 253) are not in the kit.

## D-decisions
- D-1: 7 keys in one kit; hard stop 120 min (B1067 did 21 in about 40).
- D-2: dropped -13 and -69 with reasons (kit THE BATCH); the seat re-reads both and STOPs on a contrary finding.
- D-3: removed the INCLUDE-340 slot; MPSCALC-340 is excluded outright (its reading is still not ruled).
- D-4: MPSCALC-95 lead is MOVE with a carried subtlety: clause 2 (PRE-1 counts an empty `by`) is NOT in the #33 squash (4 files, no `scripts/`); at code main it is `scripts/deploy-package.py:450`, from MPS #72 (798fe98, MPSCALC-183) by `git log -S`. So the move rests on reading (a) with #72 and on clause 3 = MPSCALC-100 (Done by B1067 under its reading (p)). Stated in the kit and as an overturnable reading.
- D-5: lessons carried: path quoting (my own `$B` slip below), Edit/Write only for scripts, JIRA.md one-blank-line boundary, Done-when table forms incl. NOT RE-DERIVED, squash-vs-gated-blob compare (B71 gated 3a037e2, squash bf60fe83), run_attempt, B1067's stale-record check, backtick/placeholder scan, re-narrowing copied figures; new copy list from `.tools/b1067` (adds `lib1067.py`, `rawget1067.py`; not `data1067.py`, `status1067.py`, `dump1067.py`).

## Q-questions for Tuesday (each with a default)
- Q-1: Drop MPSCALC-13 (epic) and -69 (question)? Default: drop both, as the kit has it. If you want -13 recorded, it is a comment-only HOLD and the seat's budget stays within 14.
- Q-2: **Finding.** A wider regex (branch name, "PR is", "pushed", "gate B<n>") finds 35 Backlog keys with a comment and no records marker, 24 beyond the 11. They are pushed-branch comments of the same shape as MPSCALC-36 (for example MPSCALC-26, 32, 40-42, 45, 46, 54, 62, 64, 65, 74, 177, 195 and epics 6, 8, 11); `b08/web-ui-showcase` merged as MPS #7 and `b10` is #8, so B1064's "37 show no merged change" does not hold for them. Default: NOT in this kit; the seat records them by key as one BACKLOG row `[B1076-OPEN-1]` and in the section. Say if you want a batch 4d (I did not identify their landings).
- Q-3: Slot `ROW-RESIDUAL` default NO. It bears only on MPSCALC-57 (the F-1 residual held as a BACKLOG row); with NO, -57 is comment-only.
- Q-4: MPSCALC-95's clause 3 leans on B1067's reading (p) for MPSCALC-100. If you overturn the -100 move, -95 should not move either. Default: proceed.

## UNMEASURED
Squash trees against the Done-when clauses (leads are from Jira text, gate lines and a few file counts); the gates of MPS #3 and #11 and the later round of B11's NO GO on #7; which of #18/#20 carries a given proposal line; why the push-run list is empty for the four oldest PRs; hosted state (relayed only); the 24 further keys' landings; port block (none assigned); whether M68's PR lands first.

## Outside-the-fences disclosure
- Wrote only the kit and this report, plus one helper script and its JSON dump in my session scratchpad (`/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/19d607c8-1023-4b31-827b-70fad6cf9eba/scratchpad/jdump.py`, `mps_dump.json`): a read-only Jira GET reader of `.env` in-process (I did not import `j1067.py` because its `call()` appends to B1067's heartbeat file). No token printed.
- Slip: one `ls`/`grep` chain used an unquoted `$B` holding the project path (space and `!`), the exact lesson-1 failure; it printed "No such file" for the pieces and wrote nothing; I redid it quoted. No `cd` typed.
- Read-only git on the project root and on `2_Project_Files` (local object `3496da33` via `git show`/`git grep`/`log -S`); `gh api -X GET` under the project `GH_CONFIG_DIR` (confirmed logged in as the Datasec account); `tmux`, `ps`, `ls`. Read the B1074, B1070, B1075 kits' relevant lines and their STATUS first/last lines (other seats' briefs; read only). No decision_queue, no briefs_staged, no scoreboard, no ledger, no other project's tree, no Artifact/Docs/mail tool, no HTTP to any app host.
