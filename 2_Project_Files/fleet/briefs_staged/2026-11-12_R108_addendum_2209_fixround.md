Seat R 108th

## BLUF
ADDENDUM 1 (Seat R 108th): a FIX ROUND for PR 2209 (KS-2021), round 2 of 2 under the cap, FIRST in your queue (before row 19). Gate 331 (tier 1, Opus) = "PR 2209: GO WITH NOTES (at head 2db221d43ad8; tier 1)", first line of /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_gate331-tier1-pr2209/verdict.md (read it WHOLE: findings section and the probe table). Wednesday rules its Minor is fixed BEFORE merge: make the match FAIL-CLOSED and pin it.

## Recommendation
Do exactly the change below on PR 2209's existing branch, one NEW commit, re-raise for a tier-1 re-gate.

## Detail
1. THE CHANGE (gate 331 measured it: Q2(b) YES): in `Blockchain/Dev/services/auth/src/services/password.ts`, the match becomes `hashSuffix === suffix && countText?.trim() !== '0'` (the optional-chain form; NOT the bare `countText.trim() !== '0'`, which throws on a row with no colon and the catch then ALLOWS: G331-2209-2; NOT `!(Number(countText) === 0)`, which allows an empty count). Read the head's line first and state it beside the new one. Effect, measured by the gate on its 25-shape corpus: differs from develop ONLY on rows whose count reads exactly `0` (the KS-2021 padding case); every malformed own-suffix row (`S:`, `S`, `S:abc`, `S:-1`, `S:1,234`, `S:3abc`) REFUSES again, as at develop.
2. ONE NEW CELL (table) in the ks2021 test: the user's own suffix with counts `['', <no colon>, 'abc', '-1', '1,234']` each expecting the password REFUSED (breached = true). Red-first: at the CURRENT head 2db221d43ad8 this cell must FAIL (it pins G331-2209-1); green after your change. Keep R1, R2, C1-C3 green.
3. Optional, only if it costs under 2 points: one more cell that kills a G331-2209-3 survivor (trim removed / trimEnd / parseInt / case-insensitive compare); say which, or say "not added".
4. PR BODY: replace the behaviour-change paragraph with the new truth (malformed own-suffix rows REFUSE, as at develop; only count exactly 0 is skipped); add the literal token `NO-PAIR` (G331-2209-6); state that the fetch-failure path is unchanged (fails open at develop, by ruling, no log line). Keep the tier-1 statement first. Refs only.
5. GIT: a NEW commit on branch feature/ks-2021-auth-hibp-check-the-range-body-match in worktrees/s-r107-ks2021 (R 107th's kept tree: it is YOURS for this round only; read its status first, must be 0). Never amend, rebase or force. The existing-branch driver family; `OVL_IGNORE_PRS="2209"` by your counted exactly-once declared edit (your STAMP's call 4). Whole services/auth suite after (rc 1 with every test green = the known seedDemoUsers timer, G331-2209-5: say so, not a fail).
6. Then READY FOR GATE round 2, tier 1, PR 2209 alone; then row 19.

RULED BY KAM, NOT YET IN AN ARTEFACT
- Kam 15:01:00 2026-11-12 (live board, verbatim): "please archive anything that is ready and continue with Secuura tickets.  Try to clear the board ASAP". Card secuura-wednesday-go-counts-as-kams-word-1030 = a: Wednesday's GO counts for starting work inside his standing grants.

PROVENANCE:
- KS-2021 | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_gate331-tier1-pr2209/verdict.md (line 1 + findings G331-2209-1..6) | read 2026-11-12

SELF-CHECK: re-read end-to-end for contradictions | 2026-11-12 15:59 (Wednesday; this is the ADDENDUM your STAMP reserves the top slot for; sent as a mail AFTER your BRIEF (04:59:03Z); your brief's ADDENDUM slot is this; the staged copy of your brief carries a line naming it too)
