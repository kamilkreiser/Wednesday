# Notes, drafter of brief_B142.md (2026-11-12 ~03:2x AEDT)

Brief: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_drafter-seatB142/brief_B142.md (72,791 bytes by wc -c, 164 lines; long lines). Copy-and-change of B 141st's brief; no stamp, no SELF-CHECK. Body (lines 1-87, to the line before `PROVENANCE:`) is 48,011 bytes; the PROVENANCE block after it is 24,780 bytes (23 fact lines + 53 tail rows) and the seat is told not to read it. Body is ~7 KB smaller than B 141st's (about 55 KB): the cost was cut by dropping the PR 2175 / 2179 / 2180 row text and BLUF repetition.

## Could not measure (all in the brief's UNMEASURED paragraph)
- Every merge tree on develop 16a5c67e676e (none computed).
- Linear, PR API state, live PR bodies, suites on the new develop; real file paths of PRs 2181 and 2182 (carried from verdict via B 141st's brief).
- Gate 311, 306, 307 findings beyond headers (carried unread again); R 98th's READY for PR 2178; gate 312 verdict lines 93-121 (ranges carried, not re-read; lines 1-4, 8-11, 54-60, 69-72 re-read and match).
- decision_queue.sh not run (2182's card quoted from the verdict only).
- Launcher preflight; shared-checkout fingerprint (carried from HANDOVER); lane A brief contents (not read); whether B 141st's pane/watchers are gone (HANDOVER says so; not checked).
- Whether the 11 counted edits of patch_setup_b141.py apply to the b141-keyed source: only the seat's dry run answers. This is the main risk to the 7-point set-up aim.
- Set-up cost and per-row costs of 2181 (two sites), 2182 (contract narrative) and 2177: all drafter's arithmetic (see PACE), no seat has measured them.

## Measured this pass
- develop 16a5c67e676eefa3e620c663fee3162941a22fa0 by `GIT_OPTIONAL_LOCKS=0 git ls-remote` of develop + refs/pull/*/head at 03:17 AEDT, 2,106 lines (wc -l). All 8 queued heads and the 53 tail rows equal their brief values by program (53 equal, 0 mismatch, a planted last-digit control rejected for each row). Second ls-remote at 03:22: develop unmoved, 2,107 lines, one new ref refs/pull/2188/head (6e5c116d9b9d...), not read, not queued; brief names it.
- Every 12- and 40-hex token in the brief (96 distinct, wc/regex program) was found in a file I read (lsr, lsr2, HANDOVER, commission, gate 312 verdict, B 141 brief, three B141 mails). Positive control: that program's test for a planted non-existent sha (deadbeef1234) prints False, i.e. it can say not-found.
- Every KS key in the brief (65 by regex) has a provenance line (program check).
- Kit: manifest 31 lines, sha256 prefix 6f9e23b9636270f2 equals the HANDOVER; 33 kit file sizes by wc -c; tools/ 42 and evidence/ 216 regular files (ls -p | grep -v / | wc -l); `drafts/merged_2180_body.txt` does NOT exist (B 141st built its MERGED text; brief says so and points at tools/merged_build_b141.py and B 140th's merged_2175_body.txt, 5,001 bytes).
- history.md ordinals for 142/141/140/139/138 = 0/1/2/2/2. df 2,424 GiB; load 14.44 11.18 9.29 (high).
- Gate 312 verdict is 152 lines by wc -l (B 141st's brief said 153).

## Departures from the B 141st brief, and why
1. Stamp dropped; PRs 2179 and 2180 struck (merged); queue = 2181, 2182, 2177, 2176, 2178, 8zb, 8zc, 2123 on, per commission. Gate 313's PRs 2183-2187 stated NOT in queue until an ADDENDUM (heads from ls-remote; keys of those PRs not named, to avoid unread keys).
2. Set-up section rewritten for the cheap re-key: single source kit (B 141st's folder), the six named set-up scripts are NOT to be read (manifest proves them; open only a refused assert), key lookup for old papers, aim 7 points (my estimate; B 141st 11.3). Honest risk named: patch edits may not apply to a b141-keyed source.
3. Trap (1), the row-specific controls paragraph, promoted to the top of TRAPS with a stale-token grep (with planted positive control) before every send, plus printing the case line's verdict field. Linear includeArchived gap and READY-builder-needs-live-watcher carried.
4. PACE rewritten from B 141st's measured readings. My arithmetic, labelled as such: 2181 10-13 to its MERGED mail, 2182 15-18, 2177 7-10; 2182 only if the 2181 MERGED reading is about 38 or under; 2181+2182+2177 does not fit in any case. The seat must state in its plan how many of 2181, 2182, 2177 it will carry. The 38 figure and the 7-point aim are mine for Wednesday to accept or change; Wednesday sets absolute readings in her plan ANSWER as she did for B 141st (48, 53).
5. Added "if 2182 does not fit but 2177 or 2178 does, ASK in the 2181 READY, never reorder yourself".
6. Live seats updated per commission item 6 (R 100th %62, S 59th %71, o149r, lane-A drafter, possible lane A seat). Lane A brief not read.
7. RULED BY WEDNESDAY: B 141st's plan ANSWER and GOs 2179/2180 replace B 140th's mails. HOLDS: merge tool/names re-keyed to b142; faults counts from B 141st's HANDOVER.
8. HANDOVER title for next seat 'FOR SEAT B 143rd'; folder seatB-142nd.

## For Wednesday to check
- The 38-reading threshold and 7-point aim; the claim that all three of 2181, 2182, 2177 cannot fit.
- The brief quotes gate-312 line ranges 93-121 as carried (unverified).
- The stale pins (4f85ca04c622, 801a2a7145c6, dbde0ac76339) appear in the brief only as history, trap tokens, or the HANDOVER's squash facts.
