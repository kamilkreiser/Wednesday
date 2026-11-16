# Drafter notes: Seat B 191st brief (2026-11-16 11:50 to 12:15 AEDT)

Brief: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-16_seatB191_merge.md (49,871 bytes; STAMP blank; SELF-CHECK 12:14; `SEND_BRIEF_DRY_RUN=1 send_brief.sh` all gates PASSED, negative control with PROVENANCE removed REFUSED). Work dir `_work/` (clone `d` = local no-hardlinks clone of the B190 drafter's clone, push URL disabled; `scripts/`; `kit191/`; `pre/`; `blocks/`). Nothing written under !CODING; read verbs, gh api and one read-only Linear read only.

## What I read
Commission, B187 and B188 commissions, B 190th's STAMPED brief (whole), Wednesday's ANSWER x2 and GO to B 190th, B 190th's HANDOVER (whole), K 38th's notes and brief RE-KEY section, K 38th's HANDOVER (head), K 38th GO and ANSWER, C 44th brief (head), gate 374 verdict (head), gate 246 section for PR 2080, derive_engines_b190.py, mk_derive_b190.py, rekey_b190.py, setup_b190.py (matcher step), finish_by_hand_2158_b185.sh, send_brief.sh gates.

## Measured
- develop moved: 72aeaec533dd (K 38th's PR 2248, 00:49:28Z, parent f487e52fd15e, tree e8b87c674e24), read 11:51, 11:52, re-read 12:14 unchanged. K 38th WRAPPED (HANDOVER FINAL 11:52), K 39th unlaunched.
- 18 heads unmoved vs B 190th's table; trees 18/18 rc 0 both orders same tree; stacked chain 18/18; plants 10/10 positive, 20/20 negative; 6 pairs; both-sided 7 rows / 11 paths; K 39th's 20 x 18 = 360 pairs, 0 shared; develop's 8-path move meets 0 rows; 57 open PRs; sharers PR 2249 and 2138 (row 8), PR 2099 (rows 14, 15). PR-V NOT pushed. 2249 head 10057c4f63c3 unmoved; 2249 vs 2161 rc 0 both orders tree 8d5d6334908c.
- Matcher: 783 entries; own B 191st present; B 190th absent; all five neighbours absent; n 788; self-test 797/797; plain-th variant reads 797/797 but classifies a real GO as OTHER; bare rule gives 787 distinct.
- Kit: 93 files, 88 with b190 (569 hits), B190 26 in 9, 190th 302 in 91, 190TH 2 in 2, dir token 71 in 66; b191 0 in 0; b190 digit-preceded 0 in 0; b188 residue 1 in 1; adjacency 117 files 10 hits 4 files; sed vs python 93/93; kit191 manifest sha16 17ca995d27b6cae8; leftovers: B 190th's session id 9d03ab3d (5 files), gg190, brief id.
- Maker FORMS is a plain `%` list (th trap); engine's form()/sfx() is correct; sed-digits literal hard-codes th.
- Row 1 PR 2080: m365 vitest, 1 commit, +321 -5, index.ts both-sided vs PR 2129; finish_by_hand_2158_b185.sh exists (5,635 bytes), absent from REC186-190; shift counts taken.

## Slips
1. zsh word-splitting on `$QB` in the first fetch loop (fixed with `${=QB}`; no harm). 2. Several grep|cut advisories (no absence claims rested on them). 3. `sed -i.bak` left .bak files inside _work (gates.py.bak, lin.py.bak, body2.md.bak, trial.md.bak). 4. First assembled draft was 60 KB and was trimmed in many passes to 49.9 KB. 5. A dry run of Wednesday's send_brief.sh was used as a lint (it stops before any network call; its decision-queue read is read-only).

## UNMEASURED
Any install, suite, mutant, tsc, eslint; the inbox; K 39th; PR-V; whether Wednesday has stamped; the REAL kit's derive and matcher step (only scratch copies and kit191); finish-by-hand survival of a shift; 2080's blob check.
