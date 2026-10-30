## NEW SEAT: you are Seat F 19th (lane Secuura/Blockchain-F; Sonnet; trust $TMUX_PANE): SUCCESSOR to Seat F 18th on PR #1835 (KS-1848 + KS-1849, the MFA backup-code burn). Your job is #1835's MERGE PREP with gate 38's three follow-ups folded in, ending at READY TO MERGE.

model: claude-sonnet-5-5 -- merge prep on a gated PR, test cells + a comment (routing row C1) -- P1-P4 -- gauge 88% -- cloud (80-90% band): merge prep needs repo write and a real-Postgres harness; no local tier has either

## START AUTHORITY
Kam, 2026-10-30 10:07:32 AEDT, live board, verbatim: "Decision secuura-wednesday-go-counts-as-kams-word-1030: a — Yes: Wednesday's GO counts for starting work inside my standing grants (recommended)". Merging our own tested work sits inside Kam's 2026-09-11 grant ("you also have my approval to merge anything that has been finished and tested"). Your plan confirmation goes to Wednesday; her GO is the start.

## BLUF
1. READ WHOLE FIRST: F 18th's HANDOVER `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-30_seatF-18th/HANDOVER.md` (FINAL block first) and gate 38's verdict `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-30_gate38-1835/verdict.md` (probes in `probes/` beside it: g38-probe.integration.ts holds the cells to copy).
2. Gate 38 = GO WITH NOTES, FIX BEFORE MERGE: none. Fold in, as ONE commit on #1835's head 598f50ed29d4:
   - **F1:** reword the passwordLoginGate.ts comment "so a lost race is no oracle" to what is true (status, body and lockout are identical; TIME is not: the lost race is ~30 ms faster). COMMENT ONLY. Prove it with a comment-free transpile equal before/after, plus a control that differs.
   - **F2:** add a real-Postgres blind-write cell (tenant_id NULL row, or runWithTenantId(<other tenant>), each expecting 503 with codes unchanged), with a positive control under the row's own tenant expecting ok. Red-proof it against the gate's M6 ("0 rows with the hash still stored counts as spent").
   - **F3:** pin the reverse interleaving (the gate's G3/G4 recipe: hold FOR UPDATE; start the sign-in and wait until its UPDATE queues in pg_stat_activity; start regenerate/disable; wait for 2 queued; release). Red on develop's stale follow-up, green at head.
3. Then a DOCS-ONLY MERGE-IN of the then-current develop (read by ls-remote in the same action): #1835's docs entry is section 124 and develop already has a 124. Renumber at develop's highest + 1; rebuild the docs, never splice. PUSH through the queue with a DETACHED driver (nohup/setsid) and a bounded waiter. Then READY TO MERGE with a blob table: product blob = gated 598f50ed29d4's except the comment-only change, tests, docs. Wednesday checks the delta at source; no new gate for comment + tests + docs.
4. Every fact in the HANDOVER and the verdict is someone else's reading: re-read heads and develop yourself.

RULED BY KAM, NOT YET IN AN ARTEFACT
- None for this lane. Card secuura-docs-section-collision-dirties-every-pr-1030 is OPEN with Kam: until he rules, do not change the docs format.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- The burn ruling (F 18th's lane): a non-NULL set lacking the hash = refusal; NULL / no row / hash still stored = 503. Gate 38 confirmed every leg.
- A docs-section collision = a docs-only merge-in PLUS A PUSH at merge prep (STANDING_LINES headline corrected 2026-10-30 17:5x).
- At most two queue places per seat; drivers DETACHED (the harness kills background tasks at 2 h).
- Throwaway Postgres: as F 18th ran it (127.0.0.1 only, the secuura_app role, RLS live); remove it by its recorded id with before/after counts.
- F 18th's six filing candidates are NOT yours this round (Wednesday routes them to a board pass).

## LIVE SEATS AT SEND
T 8th (auth: oauth.ts KS-1797 #1834, KS-1791, #1826/#1827/#1830 merge prep), W 13th (KS-1384 anchoring/originate), V 11th (#1829 merging; KS-1807 docs), U 7th (#1828, #1833 certifications.ts), E 22nd (authz in kyc/governance/billing/vc-issuer; #1832 guard script), R 66th (eight raise PRs). Your files: passwordLoginGate.ts (comment only) and the KS-1848 test files. T 8th is in services/auth too: re-run the open-PR overlap with a planted control before the push.

## HOLDS
Pushes through the queue, one ticket at a time. Never --no-verify, never force. An EMPTY ls-remote means unreachable (retry), never "moved". Stop only processes and containers you started, by recorded id. No board writes beyond your PR body and one KS-1848 comment. Signature classes pause for Kam.

PROVENANCE:
- F 18th's wrap mail (06:38Z, read whole by Wednesday), history line 1 at its wrap "## 2026-10-30 - Seat F 18th", HANDOVER directory present | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/ | read 2026-10-30
- gate 38 verdict GO WITH NOTES, head 598f50ed29d4 equal at start/end | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-30_gate38-1835/verdict.md | read 2026-10-30
- ordinal: "Seat F 18th" 2 (control), "Seat F 19th" 0, "Seat F 20th" 0 | /usr/bin/grep -i -c over /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md | read 2026-10-30

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-30 17:59
