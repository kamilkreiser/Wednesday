# BRIEF: Seat K 15th, Secuura/Blockchain-K. KS-911 + KS-912 (KS-907 launcher + suite residues). VERIFY-AND-GATE the already-built by-hash change; do not rebuild.

## NEW SEAT: you are Seat K 15th (lane Secuura/Blockchain-K; trust $TMUX_PANE; pane id is in Wednesday's launch mail, UNMEASURED here). Seat K 14th wrapped 2026-11-05 (highest K ordinal in history.md). SHARED INBOX: act ONLY on mail whose subject names `(Seat K 15th)`.

model: claude-sonnet-5-5 (DECIDED by Wednesday; launched with SEAT_MODEL_ENV=claude-sonnet-5-5). Drafter's reasoning, kept: The tickets show both fixes are ALREADY BUILT (2026-09-06) and live in the launcher; what is left is hash reconciliation, a re-run of the guard suite, and a gate hand-off. That is verification-shaped, so claude-sonnet-5-5 is proposed. Use claude-opus-5-5 ONLY IF the seat finds it must change `Launch_Claude.command` (the seat-boot path for every future seat: tier 1 class) or the evidence contradicts the tickets. Set `SEAT_MODEL_ENV` to match what Wednesday picks.

## SCOPE (quoted from the tickets; this brief commissions exactly that)
- KS-911 (In Progress): "Two residues in `Launch_Claude.command` from the KS-907 by-hash gate (F1, F2 - both Minor). One is a comment describing a test that does not exist; the other is a `2>/dev/null` placed *after* the append it is meant to silence, so a failed open still prints." Fix shapes: F1 delete the sentinel claim (preferred); F2 move the redirection ahead of the target at both sites.
- KS-912 (In Progress): "Three residues in `Launch_Claude.seats.test.sh` from the KS-907 by-hash gate (F3, F4, F6 - all Polish). The worst is F4: CASE 2 ... never asserts the thing it is named for." F4 assert dead pid absent from `$SEAT_FILE` plus live pid present; F3 print the launcher-run count, not the cell count; F6 replace `grep -qc ... ; echo $?` with `grep -q ... && echo YES || echo NO`.
- KS-907 (Tested Not Deployed, ARCHIVED 2026-09-14) is the parent: reference only, not in scope. F5 (scan matches the project dir as an argv substring) is a DECLARED LIMIT on KS-907, not worked.
- The tickets are NOT narrower or wider than "KS-907 launcher + suite residues". Nothing about the boot git-sync design is in scope (see EVIDENCE below).

## FINDINGS THE DRAFTER MEASURED (the seat re-measures; none is a ruling)
1. Both tickets carry a 2026-09-06T11:15Z comment "BUILT and READY FOR QA - ships BY HASH with KS-911/KS-912 as one change": launcher sha256 `932a2cc3...f55c`, `.pre-ks911` `9609c845...29f1`, suite `b93b2c83...8888`, `.pre-ks912` `a5d5d9ef...4901`. Neither ticket has a PASS/NO GO verdict comment and both are still In Progress. Whether the narrow tier-2 gate on the diff ever ran: UNMEASURED.
2. THE LAUNCHER HAS MOVED SINCE. Current `Launch_Claude.command` is 39,821 B, mtime 27 Oct 19:53, sha256 `4f519a6b631623221f64b0dfc61321c3dbf6378f463e9f60dcb8f42022cd42c2`, NOT `932a2cc3...`. Later `.pre-` copies exist: `.pre-0914-keepalive`, `.pre-0922-1814-nofetch`, `.pre-1027-model`. So "the hash that passed is the hash that runs" no longer holds literally; the seat must reconcile the 911/912 diff against the current file, not the 09-06 one.
3. Fix present in the current launcher (read-only grep, drafter): sentinel `the test extracts here` count 0 (case-insensitive) against control `SECUURA_LAUNCH_DRY_RUN` count 3; redirect-first at `Launch_Claude.command:307` and `:310` (`printf ... 2>/dev/null > "$SEAT_FILE"` / `>> "$SEAT_FILE"`). Suite (current sha256 `b93b2c838e8766a8dc2b72e24d2f6fab21f9b912772e52328d43996414f18888` = the ticket's shipped suite hash, so unchanged) has `LAUNCH_RUNS` (line 53, incremented in `run_launcher` line 65), CASE 6 (line 246) and its CONTROL (line 274). F4/F6 in the suite: seat verifies by reading and by the red-proof, not by trust.
4. THE LAUNCHER IS OUTSIDE GIT. `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/` is not a repo (`git rev-parse` fatal there); `2_Project_Files` rejects `../Launch_Claude.command` as outside the repository. So there is no PR, no branch and no pre-push hook for this file. The usual "own worktree + PR + merge" shape CANNOT apply literally; the by-hash shape is the project's equivalent (see METHOD).

## EVIDENCE FOR THE BOOT-SYNC QUESTION (facts, NOT a ruling; the tickets say what is defect vs intended)
- Launcher: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/Launch_Claude.command` (path verified, exists). KS-907 block is `:244` "KS-907 SEAT REGISTRY" to `:380` "end KS-907 seat registry". Line 350: `preflight_warn "[KS-907] ${OTHER_SEAT_COUNT} other live session(s) on this project: ${OTHER_SEATS}."`; line 351: "The boot git-sync is READ-ONLY this launch - it will NOT pull in 2_Project_Files."; `GIT_SYNC_STEP` for that case (lines ~352-370) says run `git status` + `git ls-remote origin <branch>`, "DO NOT pull ... no fetch, no pull", sync your own worktree. With no other seat live, the `else` branch (line ~371) keeps the original instruction: `git status`, `git fetch`, "If safe ... pull latest on the current branch".
- Seat D 54th (launch 2026-11-05 03:19:21Z) HANDOVER `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-05_seatD-54th/HANDOVER.md` "Slips" (line 41): "the launcher's boot pull fast-forwarded the shared checkout 07a2d62be -> 5fc5569ed (accepted by Wednesday as the KS-907 / KS-911 launcher class)". From the history headings, U 13th wrapped ~14:1x AEDT (about 03:1xZ), before D 54th's 14:19 AEDT start, which is consistent with no other seat live at that boot (the read-write branch ran as written). UNMEASURED: the actual preflight text of D 54th, and whether S 21st (launch 13:48 AEDT) was still live.
- U 13th and S 21st preflights show the "[KS-907] 1 other live session(s) ... READ-ONLY this launch" line (per Wednesday's note; the drafter did not re-open those preflight files).
- Consequence for scope: KS-911/KS-912 do NOT change that behaviour. If the seat concludes the unconditional pull when alone is itself a defect (the pull lands before the seat reads its brief; the checkout can move under a seat that boots seconds later), that is a NEW finding: write it as a candidate in the wrap for Wednesday to route, do NOT widen this change.

## WHY AND AUTHORITY
- Kam 2026-11-04 ~09:16 AEDT, verbatim: "new account logged in.  Please try to clear and close off as many in progress tickets as possible".
- Kam 2026-11-02 12:44:58 AEDT, verbatim: "please archive anything done and merged".
- Card `secuura-wednesday-go-counts-as-kams-word-1030` = a (ruled_ts 2026-10-30T10:08:25+11:00): "Yes: Wednesday's GO counts for starting work inside my standing grants (recommended)"; signature classes (production, money, comms to people, irreversible) still pause for him. This brief, once Wednesday sends it, is that GO.
- Done rule (lesson `/Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-10-12_secuura-done-when-tested-works-deployed-and-never-idle.md`): Done once fully tested + works + deployed, BLUF evidence comment BEFORE the move. Kam 2026-09-06 10:24: you change no assignee.
- Kam 2026-09-07 13:23: the unit is the test pass / the fix (one ticket per defect).

## DEMO IS FROZEN FOR REDEPLOYS (binding, verbatim)
Kam, live board 2026-11-05, card `secuura-ks1401-058-merge-demo-billing-1104` = a, 07:08:03 AEDT: "Merge; I stop every demo redeploy until you say". 07:08:39 AEDT: "but deploy everything now.  so both systems have all changes.  new demo rule takes affect after this deploy". Kintsugi now runs `5fc5569ed96a` (D 54th HANDOVER line 4), demo stays at `07a2d62be6a0`. This task has NO box contact at all: no ssh, no `az`, no docker on either box, no deploy, no mail to a human.

## HOLDS (binding)
- OTHER_SEATS: none. Wednesday's pane list at 2026-11-05 15:26 shows only the coordinator and the fleet monitor (D 54th, S 21st and U 13th have all wrapped and their panes are closed). If `ps`/the launcher's own preflight shows another seat live, say so in the plan confirmation.
- **Do NOT edit the live `Launch_Claude.command` in place.** Never edit a running script. Any change is made on a copy in your own folder (`/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-05_seatK-15th/work/`), a new `.pre-` baseline copy is taken beside the live file, and the swap into place happens only after the gate verdict and Wednesday's/Kam's GO. The next launch delivers it.
- **Do not run the guard suite against the live registry carelessly:** it launches the launcher in DRY_RUN with a `TMPDIR`-scoped registry; run it with `TMPDIR` pointed at your own work folder, record the `TMPDIR` value, and confirm `2_Project_Files/.git/config` and `.launch_preflight_last.txt` are byte-identical before and after (the suite asserts the first; do the second yourself).
- No push, no merge by the seat. Do not touch `Launch_Claude.command.*parked*` files (tamper copies; parked by rename on purpose) or any other seat's folder.
- Do not touch other projects' launchers (per-project copies of a master template; fixing this copy fixes none of them). Name that as a limit, do not act.
- Board writes: BLUF evidence comments on KS-911 and KS-912 only; Done only after the gate verdict; archive only what the work completed (Done + verdict). No field edits beyond state, no relations, no new tickets (findings go in the wrap as candidates).
- Read every write back (body equal to the draft, 0 mention nodes). Client-facing: none.
- Instruments: `cmd > out 2>&1; rc=$?` with rc on its own line; macOS has no `timeout`; zsh has no PIPESTATUS; the launcher runs under `/bin/bash` 3.2, so test redirect behaviour under `/bin/bash`, not zsh (the Bash tool is zsh; `BASH_VERSION` empty is the tell); `/usr/bin/grep -i` with a positive control beside every zero; a count carries its predicate; never `cd`; absolute paths; never `grep -r` over `5_Project_History` or `0_Brain`; stop only processes you started, by recorded PID.

## METHOD (by hash, the project's equivalent of PR + gate)
1. Reconcile first. Hash the live launcher, `.pre-ks911`, `.pre-ks907`, the suite and `.pre-ks912` (`shasum -a 256`); compare to the ticket comments (`932a2cc3...` shipped launcher no longer matches the live one). `diff` `.pre-ks911` (= `9609c845`, KS-907's gated file) against the nearest ancestor of the live file and decide, with the diff in hand, which of the 23 KS-911 lines are present and which later edits (`0914-keepalive`, `0922-nofetch`, `1027-model`) sit on top. State it as a table.
2. Re-prove each finding on the current file with a control: F1 grep (0 vs control), F2 under `/bin/bash` 3.2 with a read-only registry file (`chmod 444`, as KS-911's fixture) AND a writable control, F3/F4/F6 by reading the suite and by the parked red-proof `Launch_Claude.command.KS912-TAMPER-noprune.parked` (read it, do not delete or run it from the project root; copy to your work folder).
3. Run the suite (`Launch_Claude.seats.test.sh`) against the current launcher with the isolation in HOLDS; expect 18/0 at the ticket's baseline, record the actual number and which cells changed if the launcher has moved. A pre-fix launcher (`.pre-ks911`) must flip CASE 6 alone (the ticket's red-proof): re-run it once so the guard is shown able to fail in the same batch.
4. If anything is missing or the later edits broke a cell, make the narrow fix on a COPY, take a new `.pre-` copy, and produce the three hashes (new launcher, new `.pre-`, suite). Only then escalate model to Opus.
5. QA gate: this touches the seat-boot path, so it is **tier 1** (CONFIRMED by Wednesday). Hand to the gate by hash: the three hashes, the diff, the suite result, the red-proof. The seat does NOT merge or swap the live file.
6. Evidence comments on KS-911 and KS-912 (BLUF, hashes, facts only). Done/archive only after the gate verdict.

## PACE AND END
At ctx 70% finish the item in hand and write the HANDOVER naming what is left; wrap by 75%. **End at READY FOR GATE**: mail `[Secuura/Blockchain-K -> Wednesday] READY FOR GATE KS-911 KS-912 (Seat K 15th)`, body line 1 exactly `Seat K 15th`, with hashes, the reconciliation table, the suite numbers, the diff path, and the candidate on the boot-sync question if you hold one. No merge, no swap, no push by the seat.

## MAIL
From secuura-blockchain@ to `wednesday-agent@agentmail.to` ONLY (Secuura keeps Wednesday, not Tuesday), subject prefix `[Secuura/Blockchain-K -> Wednesday]`, body line 1 exactly `Seat K 15th`, no cc, no secrets, no stop/hold/hand over/checkpoint in a subject; read each sent mail back by id. **Plan confirmation:** QUESTION mail, topic `plan confirmation`, with the launcher's preflight warnings VERBATIM, your note on any instruction that looks wrong (known candidates: the tickets' hashes no longer match the live launcher; "own worktree + PR" cannot apply to a file outside git), and your queue. Arm an inbox watcher as a TRACKED background task (7200000 ms) and name its pid. IF AN INSTRUCTION LOOKS WRONG, SAY SO. Approval-class actions (the live swap, anything irreversible) pause for Kam.

## WRAP (scored by Wednesday)
- History entry `## 2026-11-05 - Seat K 15th` in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` (newest first; duplicate-guard matches `^## 2026-11-05 .*Seat K 15th`, with a control).
- HANDOVER `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-05_seatK-15th/HANDOVER.md` (FINAL block first) plus `evidence/hash_reconcile.tsv` and `evidence/writes_k15.tsv` (every board write and every file written, with undo or "none").
- Vault commit and push per the end-of-session skill (only your own lines). Wrap mail `[Secuura/Blockchain-K -> Wednesday] Session wrap 2026-11-05 (Seat K 15th)`.

PROVENANCE:
- Ticket text (KS-907, KS-911, KS-912: title, state, description, all comments sorted by createdAt, attachments) | Linear GraphQL read-only, drafter | read 2026-11-05
- Launcher, hashes, grep counts, lines 296-311 and 340-372 | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/Launch_Claude.command (and its siblings listed by ls in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/) | read 2026-11-05
- D 54th slip, seat ordinals and K lane (K 14th 1 hit, K 15th 0 hits, case-insensitive, anchored) | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-05_seatD-54th/HANDOVER.md and /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md | read 2026-11-05
- Routing: `Secuura/Blockchain-K` exists, row 215 | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf | read 2026-11-05
- Standard sections (RULED BY KAM, demo freeze, HOLDS, instruments, mail, wrap) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-05_seatU13_postdeploy_live_checks.md | read 2026-11-05
- KS-907 state: Tested Not Deployed (archived 2026-09-14) | Linear | read 2026-11-05
- KS-911 state: In Progress (last comment 2026-09-06 BUILT/READY, no verdict) | Linear | read 2026-11-05
- KS-912 state: In Progress (last comment 2026-09-06 BUILT/READY, no verdict) | Linear | read 2026-11-05
- UNMEASURED by the drafter (the seat measures them): whether a KS-911/912 gate ever ran; the diff between the live launcher and `.pre-ks911`; the suite's current run result; a PR link on the tickets (an attachment points to KS-926 PR 874, unrelated) | the drafter's Linear read and /Volumes/DevMASTER/!CODING/Secuura/Blockchain/Launch_Claude.command | read 2026-11-05

RULED BY KAM, NOT YET IN AN ARTEFACT
- Kam 2026-11-04 ~09:16 AEDT (terminal), verbatim: "new account logged in.  Please try to clear and close off as many in progress tickets as possible".
- Card secuura-wednesday-go-counts-as-kams-word-1030 = a: Wednesday's GO counts as his word inside his standing grants; signature classes still pause for him.
- Kam 2026-11-05 07:08 demo-freeze words, quoted above.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- 2026-11-05: model Sonnet, gate tier 1; the live launcher swap is approval-class and waits for the gate verdict plus Wednesday's GO.
- 2026-11-02 03:16:10Z: a follow-up with its own ticket does not keep the parent open.

SELF-CHECK: re-read end-to-end for contradictions | 2026-11-05 15:26 (Wednesday read it WHOLE; model decided Sonnet; gate tier 1 confirmed; floor re-checked: no Secuura seat live)
