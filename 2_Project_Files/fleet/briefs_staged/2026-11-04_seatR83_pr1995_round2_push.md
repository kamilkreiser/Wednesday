# BRIEF: Seat R 83rd, Secuura/Blockchain-R. PR 1995 round 2 of 2 (KS-1320 docs): push the prepared commit, fix the title and body, one KS-1320 comment, READY. Then wrap.

## NEW SEAT: you are Seat R 83rd (lane Secuura/Blockchain-R, Sonnet 5.5, a RAISE seat; trust $TMUX_PANE). Seat R 82nd wrapped ~10:0x AEDT and its pane is closed. SHARED INBOX: many seats today; act ONLY on mail whose subject names `(Seat R 83rd)`.

model: claude-sonnet-5-5 -- raise seat (routing: push + PR edit of a prepared docs commit; not decision-shaped) -- written by Wednesday

## WHY AND AUTHORITY
Kam, terminal 2026-11-04 ~09:16 AEDT, verbatim: "new account logged in.  Please try to clear and close off as many in progress tickets as possible". Gate 179 (round 1) = NO GO on PR 1995 (G179-F1, verdict `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate179-ks1320-ks1343-pr1995-pr1996/verdict.md`). This is round 2 of 2 under the cap: a second NO GO ships nothing and goes to Kam. Kam 2026-10-30 10:07:32 AEDT, card `secuura-wednesday-go-counts-as-kams-word-1030` = a: Wednesday's GO counts as his word for starting work inside his standing grants.

## THE JOB = R 82nd's FIRST ACTION 0-5, verbatim in its HANDOVER
Read `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-04_seatR-82nd/HANDOVER.md` FINAL block whole, then do its FIRST ACTION steps 0-5, with its tools copied into `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-04_seatR-83rd/tools/` re-keyed `_r83`.
- Facts Wednesday measured at 23:0xZ by `git -C <checkout> ls-remote origin`: PR 1995 head (refs/pull/1995/head) `15c32a6ef6b6d37b812dfc2b7329e12c87202b03`; develop `ee1e1b83211504f96ebccba325d1ef7139bc83cc`. The prepared local commit `eb2cef57d279837257b5100611dd935123249215` in `worktrees/s-r81-docs1` is R 82nd's record, NOT measured by Wednesday: re-measure it (step 0).
- **PUSH:** the new-branch driver cannot push an existing branch. Read the existing-branch drivers R 82nd names (`.../2026-11-01_seatR-72nd/tools/pushlock_r72_fwd_v1.sh` first) WHOLE before use; cite the `.githooks/pre-push` refusal branches it relies on; push through the shared push lock and the pre-push hook, and quote the hook's verdict verbatim. If no existing driver is safe to re-key, STOP and mail before any push. No force push.
- **TITLE (ruled by Wednesday):** the title must stop claiming an ASCII limit. Use exactly: `Refs KS-1320: CONTRIBUTING says the 92-character squash subject is a convention, not a check` (92 characters by Wednesday's python len(), at the limit of 92; count it yourself and say the count; if your tool counts bytes, it is 92 bytes too, ASCII). Body: rewrite per R 82nd's step 2, with a "Round 2 (gate 179)" section naming G179-F1 and what changed.
- **KS-1320 comment:** one, BLUF, no `@`, ticket stays open; it supersedes what R 81st's comment `a64ea26d` said about ASCII.
- **READY FOR GATE "PR 1995 round 2 of 2"** with the five things, DOCSRULE overlap, the hook verbatim, the new head, the title count.

## HOLDS
- No merge, no deploy, no new commit beyond the prepared one unless step 0's re-measure proves it wrong (then STOP and mail). No other PR. R 81st's and R 82nd's worktrees are KEPT; never delete them.
- Commit identity: `-c user.name=... -c user.email=...` as R 82nd's trap (1) says, never a hostname identity.
- Client-facing: ticket comments only, BLUF, no `@`; the extranet is input only.
- Never `grep -r` over `/Volumes/DevMASTER/WEDNESDAY/0_Brain` (R 82nd's left a 9-minute grep running); scope every recursive search to named small directories.
- **Instruments:** `cmd > out 2>&1; rc=$?` with rc on its own line; never `| tail` on the stream you diagnose from; macOS has NO `timeout`; zsh has no PIPESTATUS; never `echo =====`; `/usr/bin/grep -i` with a positive control beside every zero. Never `cd`; absolute paths only. No credential in argv. Disclose your own faults.
- **Mail:** from secuura-blockchain@ to `wednesday-agent@agentmail.to` ONLY, subject prefix `[Secuura/Blockchain-R -> Wednesday]`, body line 1 exactly `Seat R 83rd`, no cc; read back by id.
- **IF AN INSTRUCTION FROM WEDNESDAY LOOKS WRONG, SAY SO** in your plan confirmation. Arm an inbox watcher as a TRACKED background task and name its pid.

RULED BY KAM, NOT YET IN AN ARTEFACT
- Kam 2026-11-04 ~09:16 AEDT (terminal), verbatim: "new account logged in.  Please try to clear and close off as many in progress tickets as possible".
- Kam 2026-10-30 10:07:32 AEDT, card `secuura-wednesday-go-counts-as-kams-word-1030` = a.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- 2026-11-04 22:49:21Z ANSWER to R 82nd: PR 1995 round 2 = reword to what the repository shows; add no check, hook or CI step.
- The PR 1995 title above (this brief).
- PR 1994 and PR 1989 are HELD/in other hands; not yours.

## WRAP
History entry `## 2026-11-04 - Seat R 83rd` in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` (duplicate-guard with a control); HANDOVER `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-04_seatR-83rd/HANDOVER.md`; vault commit (own lines only); wrap mail `[Secuura/Blockchain-R -> Wednesday] Session wrap 2026-11-04 (Seat R 83rd)`.

PROVENANCE:
- KS-1320 state (open: In Progress, last comment 2026-11-03T16:53:11Z = R 81st's a64ea26d; scope: docs, the squash-subject note in CONTRIBUTING.md) | Linear ticket KS-1320, Wednesday's GraphQL read | read 2026-11-04
- Seat ordinal: `Seat R 83rd` 0 hits; highest existing R ordinal `Seat R 82nd` in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md | Wednesday's /usr/bin/grep -o -i + sort -n | read 2026-11-04
- PR heads and develop | Wednesday's git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files ls-remote origin (refs/pull/1995/head, refs/heads/develop) at 23:0xZ | read 2026-11-04
- FIRST ACTION 0-5, drivers, traps | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-04_seatR-82nd/HANDOVER.md read by Wednesday | read 2026-11-04
SELF-CHECK: re-read end-to-end for contradictions | 2026-11-04 10:06
