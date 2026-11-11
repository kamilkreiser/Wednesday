# notes.md: drafter for Seat A 24th, 2026-11-12 ~10:2x AEDT

Output: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_drafter-seatA24/brief_A24.md` (81 lines, 23,788 bytes; under 55 KB). Copy-and-change of A 23rd's stamped brief; no SELF-CHECK line; blank STAMP block (five empty fields); PROVENANCE block has one `KS-NNNN | <absolute path> | read 2026-11-12` line for every KS key named (checked by script: 0 keys without a line; keys only in lowercase slugs such as ks1347 or ks812 are not named as keys).

## Re-measured (read-only)
- `ls-remote` in the Blockchain 2_Project_Files checkout: develop `d35f75875275158ce3b20b636b4198a4c8834968` (UNMOVED since A 23rd's wrap; equals Wednesday's ~10:1x read). PR heads: 2199 `4a0a166b95a1`, 2191 `96ac07b0cd0d`, 2193 `b6397499151d`, 2196 `fed1d35ce95c`, 2137 `8dfe859d9c7`, 2079 `0fffdfba0f95` (all unchanged).
- API (`gh pr view`, read-only, under the project's own GH_CONFIG_DIR): PR 2191 state OPEN, mergedAt null, head `96ac07b0cd0d`, so A2 is NOT startable. PR 2199 OPEN, MERGEABLE, head `4a0a166b95a1`.
- Gate 322 verdict line 1: GO for PR 2199 (tier 2 stands). Findings carried: O142 already in develop via PR 2182, O141 superseded (Wednesday to retire); pin is a tight EQUALS.

## Decisions in the brief
- KS-2170 / PR 2199 is declared NOT A 24th's (goes to B 147th); its kept tree `s-a22-ks2170` is added to the protected list beside `s-a21-ks2125` and `s-a20-base`.
- Queue: A4 first (ruled scope verbatim, with a per-file open-PR census before any edit, per the commission); A2 only after 2191 MERGED; ADDENDUM-only fix rounds.
- Carried verbatim: the whole RULED BY KAM section; TMPDIR lesson (with an added assertion to print the final TMPDIR length after the a23 to a24 re-key); DRIVE RUNBOOK (13 min uptime proof, four proofs for a dead lock); PACE 60 with "stop starting at 55".
- Arithmetic note for you: A 23rd's meter says plan about 22 to 25 plus kit 4 to 6 plus A4 12 to 15 plus push/PR/READY 4 to 6 gives READY near 45 to 55, so A2 is unreachable under the 55 line even if 2191 merges; the brief tells the seat to say so. Forecast, not measured.

## For Wednesday to decide at the stamp
1. The A4 start line (A 23rd's "40 or under at the previous READY" rule does not map onto a fresh boot; I wrote "your own meter at the cut and the 55 line" and left the rule line to your STAMP block).
2. The FLOOR and pane ids (not read; B 146th replaced by B 147th is my inference from the commission).
3. The ordinal check: A 23rd wrote a wrap, so `Seat A 23rd` should read at least 1 in history.md; I did NOT read history.md, so the brief tells the seat to read and report rather than asserting a number.

## Not measured / caveats
- A4 census (line counts and per-file open-PR overlap): NOT run. 2137 touches check-shared-relink.sh (read in HANDOVER, not re-diffed).
- State of PRs 2193, 2196, 2137, 2079 at the API: heads only.
- Lock and queue, drive health, disk, panes, Linear, model id: not read.
- I did not re-read the A 22nd brief, A 21st/20th/19th briefs or the COMMON reboot file; the brief cites them by path only (A 22nd's row (c) text came through A 23rd's HANDOVER, which holds the ruled scope verbatim; I confirmed line 39 of the A 22nd brief opens with the same quote).
- The kit file list (`REC23/tools`) was read by `ls` and the HANDOVER map, not diffed; `REC23/tools/wrap/` contains `window_monitor_a23.sh` (the 13-minute uptime monitor) and `release_stale_a23.py`, as the brief says.
- Stamp note: the A 23rd brief's HOW TO READ cites the A 22nd brief for row (d) A2 text; I kept that chain rather than inlining it (A2 is carried text, not startable).
- Drafter slip: my first Bash attempt contained a stray `cd` and was refused by the hook before anything ran; the brief was then written with the Write tool. Nothing was changed outside the output folder. Shell hazards hit: a zsh `=====` word and the no-cd hook, both refused cleanly.
