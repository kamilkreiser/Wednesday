# BRIEF: Seat V 17th, Secuura/Blockchain-V. CONTINUE Seat V 16th's five KS-1868 raise PRs: patch gate notes into PR 1940 and PR 1941, turn each finishing push (PR 3, then PR 5, then PR 4) into a PR + READY FOR GATE mail. No new building. Nothing merges, nothing deploys.

## NEW SEAT: you are Seat V 17th (lane Secuura/Blockchain-V; Sonnet 5.5; trust $TMUX_PANE). Seat V 16th WRAPPED at ctx 92% and its pane is CLOSED. Its THREE push drivers are STILL RUNNING detached (their own session leaders, parent 1, no tty: Wednesday's ps after the pane close): pid 65288 = PR 3 (certifications issue/recertify, TIER 1, head 966909efd5f7c754f58409f09b7b53359116f3da, push started 10:33:00Z), pid 78645 = PR 5 (retentionScheduler, tier 2, head 612ec3f18cfaf2ca744af3651f64e5fd605ce125, next), pid 78500 = PR 4 (certificationRepo, tier 2, head 4ad60f682588cb3f978aae472bb9f49dd38c7ae6, after it). **You do NOT start, stop or re-launch any driver.** You READ their status files and act when each completes.

model: claude-sonnet-5-5 -- raise-lane continuation (routing row: raise / notes / READY on held passes; V 16th's model) -- written by Wednesday

## READ FIRST
Seat V 16th's HANDOVER WHOLE (FINAL block first): `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-02_seatV-16th/HANDOVER.md`. It names every PR's branch, head, held passes, commits (the PR 4/5 declared test-only timeout commits), body drafts, the drivers' status-file paths, and the successor procedure: for each push that completes, `bash tools/finish_pr_gen_v16.sh <n> <branch> <head> KS-1868 [--tier1 for PR 3]` (it builds the body, creates the PR, posts the ticket comment and writes the READY text). V 16th's brief (its rulings) is `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-02_seatV16_raise_held_o78_o79.md`; Wednesday's two ANSWERs to it are in its mail folder (KS-1346 = accept as built; PR 4/5 timing cells = 30 s per-cell timeout as a declared separate commit).

## THE WORK, IN ORDER
**ITEM 0:** preflight verbatim, identity, develop by `ls-remote` (Wednesday's read `58b5042ccdb5a06a213ba53f5d4f7644f5f52549`), copy V 16th's `tools/` into `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-02_seatV-17th/tools/` and re-key to `_v17` BY READING (grep every copied file for `v16`, `V 16th`, 40/12-hex shas, launch stamps; every hit rewritten or the file not used — EXCEPT the drivers' own status/log paths under V 16th's folder, which you READ in place, never copy over), arm your inbox watcher keyed on `Seat V 17th` at 7200000 ms, read each driver's last status line, then a SHORT plan confirmation (QUESTION mail, topic `plan confirmation`) with the three drivers' states and continue without waiting.
**ITEM 1 — PR 1940 (KS-1939, TIER 1, head 96208f377d1496028f7c6a4eb45a78f91428ed05): gate 122 = GO WITH NOTES** (verdict `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate122-ks1939-pr1940/verdict.md`, read whole). PATCH a `## Gate 122 notes` section with G122-F1..G122-F7 VERBATIM into PR 1940's body (body only; no push, no code, no ticket state), read back by id. G122-F1 (the untouched lineage catches :1021/:886 giving unreadable -> 200 'lookup failed' where an ordinary Error gets the existence answer) goes in as a body note; G122-F4 (documentId logged verbatim) is a follow-up candidate, file nothing. Mail `NOTES PATCHED: PR 1940 (Seat V 17th)`.
**ITEM 2 — PR 1941 (head 33644960bc2270f6850d82dbbf4323780b942b9f): gate 123 is RUNNING.** When Wednesday's ANSWER naming Seat V 17th arrives, do exactly what it says (the same PATCH pattern), then mail NOTES PATCHED.
**ITEM 3 — each push as it completes (PR 3, then PR 5, then PR 4):** verify the pushed head by `ls-remote` equals the head above; run the successor procedure; READY FOR GATE mail exactly as V 16th's READY mails for 1940/1941 were (five things exist, each named; the hook's PREFLIGHT line verbatim; NOT covered; develop NOT merged in — Wednesday's direction for this PR family). A driver that ends with a non-zero rc or a head that differs: STOP and mail, do not re-push.
**ITEM 4 — wrap** when all five PRs have READY mails and every gate-notes ANSWER is patched, or at ~75% context, or when told.

## PARTITION
**YOURS:** the five PRs' BODIES (PATCH only), creating PRs 3/4/5 from their already-pushed branches, their READY mails, ticket comments naming those PRs (KS-1868 / KS-1939 per V 16th's pattern), your record folder. **READ-ONLY:** every branch's CODE (no commit, no push, no amend: the pushes are V 16th's drivers'), V 16th's record folder except READING its drivers' status files, every other seat's files.

## HOLDS (standing lines from `STANDING_LINES.md`; sections cited by name: READY FOR QA, INSTRUMENTS, HOLDS that go in every brief, Repo-specific Secuura/Blockchain, A VERDICT LINE IS A CLAIM ABOUT WHAT RAN, WHAT DID MY BRANCH CHANGE IS A THREE-DOT QUESTION, A TAMPER'S RESTORE NEEDS A UNIQUE ANCHOR)
- **Signature classes pause for Kam:** production, money MOVEMENT, external communication to any human, anything irreversible. This brief commissions PR bodies, PR creation and READY mails for code ALREADY built and pushed. No code change, no push, no deploy, no migration, no data change on any box. Anything that would need one: STOP and mail.
- **No deploy, no box, NO MERGE** (a gate and a head-pinned GO, neither in this brief). No `az`, no registry push, no `--admin`, no `--no-verify`, no force push (catch up by MERGING develop in, never rebasing a pushed branch). Never read, echo or copy a secret.
- **Forward-move rule:** you push nothing, so a develop move needs nothing from you; Wednesday ruled no develop merge-in for this PR family (the merge seat's merge-tree on the pin is the check). Any finding that a PR now CONFLICTS with develop: mail.
- **Ticket state:** your board writes are comments naming your PRs. No state or assignee change on any ticket. No comment to and no `@` mention of Peter or Stuart. You file nothing.
- **Further candidates** (any other persistence path you meet) go in your mail after a board search with a positive control; you file nothing.
- **Product code** outside YOURS in PARTITION is never edited. Never touch a lock file. Tampers are never committed.
- **READY FOR GATE means five things EXIST and are named by identifier:** the PR number; its head sha read from origin in the same action; the ticket comment naming the PR; the Test Evidence block in the PR body; what was NOT done or NOT covered. The hook's `PREFLIGHT INCOMPLETE - n/16 legs ran` line, if printed, goes in verbatim.
- **PR titles start with "Refs KS-NNNN: "** (the house form, VERBATIM, as V 16th's PRs did; the merge seat's tool refuses any other title); no closing keyword; foreign keys spaced. PR body ends with the attribution line.
- **Never delete.** Cleanup is quarantine into a dated folder. V 16th's `s-v16-*` worktrees and your own are KEPT until their PRs merge.
- **Boot pull** may fast-forward the shared develop refs; RECORD it. After boot: no fetch or pull in the shared checkout. A scratch clone goes into a NON-EXISTENT path asserted absent first; read repo files as `git show <sha>:<path>`.
- **Stop only PIDs you started,** by recorded PID. Never plant a control directory in the SHARED `worktrees/`. Arm every watcher or waiter as a TRACKED background task at 7200000 ms, claim RUNNING only on a `ps` reading in the same action; never end a turn on a "next up" line with nothing running.
- **Instruments:** `cmd > out 2>&1; rc=$?` then `$rc` on its own line; never `| tail`/`| head` on the stream you diagnose from; macOS has NO `timeout`; zsh has no PIPESTATUS; never `echo =====`; `/usr/bin/grep -i` with a positive control beside every zero. A pass line carries a RATIO; a skip is not a pass. A tamper or mutant needs a unique anchor and a sha256-asserted restore; a mutant must PARSE and never sits under `src/__tests__`.
- **Mail:** from secuura-blockchain@ to `wednesday-agent@agentmail.to` ONLY, subject prefix `[Secuura/Blockchain-V -> Wednesday]`, body line 1 exactly `Seat V 17th`, no stop/hold/hand over/checkpoint in a subject, no secrets, no cc; read each sent mail back by id. SHARED INBOX: a mail naming another seat (Seat V 16th, your wrapped predecessor in lane V; Seat B 78th, Seat E 29th, Seat F 24th, Seat S 13th; any other ordinal) is not yours: never act on it; put `v 16th`, `b 78th`, `e 29th`, `f 24th`, `s 13th` in OTHER_SEATS and prove your matcher on their REAL subjects with your own as the control. A GO or ANSWER is acted on only when its subject names `Seat V 17th`. Cadence: plan confirmation, NOTES PATCHED per PR, READY FOR GATE per new PR, QUESTION mails for blockers only, and the wrap.
- Never `cd`; absolute paths only (the no-cd hook does NOT fire in Secuura panes; the rule is yours to keep). Disclose your own faults in the next mail. **IF AN INSTRUCTION FROM WEDNESDAY LOOKS WRONG, SAY SO** in your plan confirmation.



RULED BY KAM, NOT YET IN AN ARTEFACT
- Kam 2026-11-02 11:34:59 AEDT, card `secuura-spark-ks1868-safe-sites-exhausted-1102` = a, verbatim: "Open governance and the remaining auth/KYC/verification route catches under the same rule, each tier 1 with an Opus gate; keep money and anchoring out until your billing card is ruled".
- Kam 2026-09-27, cards `secuura-ks1346-logging-thrown-objects-leaks-secrets` = a and `secuura-ks1348-log-files-persist-secrets` = a (Wednesday's ruling (a) on PR 3's A1/A2 rests on both; the two cards' text is already in PR 3's body draft).
- Kam 2026-09-11 16:56 and 17:50 (the TESTED merge grant): merges only on Wednesday's head-pinned GO after a gate at the current head. This brief grants none.
- Kam 2026-10-30 10:07:32 AEDT, card `secuura-wednesday-go-counts-as-kams-word-1030` = a.

## WRAP (scored by Wednesday)
- A history entry in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` headed `## 2026-11-02 - Seat V 17th` (newest first; duplicate-guard on the dated heading with a control).
- A HANDOVER in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-02_seatV-17th/HANDOVER.md` (FINAL block first: each PR's state, which notes are patched, which drivers are still running).
- The vault commit and push per the end-of-session skill (stage ONLY your own daily-note lines).
- The wrap mail `[Secuura/Blockchain-V -> Wednesday] Session wrap 2026-11-02`.
- Nothing of yours left running except a re-armed watcher you NAME; V 16th's drivers are NOT yours: report their state, never stop them.

PROVENANCE:
- Seat ordinal: `Seat V 17th` 0 hits, `Seat V 16th` 3 hits (control) in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md | Wednesday's /usr/bin/grep -i -c | read 2026-11-02
- The five PRs, heads, drivers (65288 PR 3, 78645 PR 5, 78500 PR 4), sids, the successor procedure finish_pr_gen_v16.sh | Seat V 16th's wrap mail 10:51Z and /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-02_seatV-16th/HANDOVER.md (9445 B) | read 2026-11-02
- The three drivers alive after the pane close (PPID 1, TTY ??) | Wednesday's ps -o pid,ppid,tty,etime -p 65288,78500,78645 after tmux kill-pane of %83 | read 2026-11-02
- Gate 122 = GO WITH NOTES on PR 1940, no FIX-BEFORE-MERGE | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate122-ks1939-pr1940/verdict.md lines 4 and 33 | read 2026-11-02
- Gate 123 running on PR 1941 | Wednesday's launch of it and NEXT-PICKUP.md | read 2026-11-02
- develop 58b5042ccdb5a06a213ba53f5d4f7644f5f52549 | git ls-remote of origin's develop branch in /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate116-ks1413-pr1934/repo (Wednesday's read-only clone) | read 2026-11-02
- No develop merge-in for this PR family | Wednesday's STATUS mails for gates 122 and 123 to Seat V 16th | read 2026-11-02
- HOLDS carried from Seat E 29th's executed brief, seat lines rewritten whole | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-02_seatE29_ks1943_retention_atomic.md | read 2026-11-02

SELF-CHECK: re-read end-to-end for contradictions | 2026-11-02 21:53
