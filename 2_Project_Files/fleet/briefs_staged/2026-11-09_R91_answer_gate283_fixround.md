Seat R 91st

ANSWER: GATE 283 on PR 2127 (KS-785) is NO GO. FIX ROUND 1 of 2, on this seat, at your next safe point. Your KS-784 push (driver pid 1673, queued) is unaffected: let it run and send its READY as planned.

Verdict: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate283-tier1-pr2127-ks785/verdict.md (read it whole, G283-1 to G283-7). Its headline, G283-1 BLOCKER: on a fresh clone, start-environment.sh's new `source "$PROJECT_ROOT/.env"` under set -e dies at the shipped template's line 236 (`ISSUER_NAME=Secuura Platform`, bash runs `Platform`), rc 127, compose never reached; develop with the same fixture reaches compose. G283-2 MAJOR: a malformed .env line now prints secret text and stops the start. Your evidence otherwise reproduced: the premise, 39/39, exactly your 3 red on develop, your tampers, comment-only checker, fragments OK, PR 2052 clean in both orders.

THE RULING, a change of SHAPE (Wednesday's design call inside Kam's KS-785 ruling; it delivers the same outcome, the credential check and compose agree, and adds no signature-class element). It SUPERSEDES shape (a) from my plan answer:
1. start-environment.sh never executes .env: no `source`, no `.`, no `set -a`, no eval.
2. Instead, for EXACTLY the keys check-slot-credentials.sh validates (read the checker and list them in the READY; if they are more than POSTGRES_PASSWORD and REDIS_PASSWORD, say which), and ONLY those that .env assigns (a literal `^KEY=` line match, the value never read into the shell), `unset` the shell export before `docker compose up`, so compose's own .env read supplies the value the checker reported. Keys .env does not assign keep whatever the shell has (no change from develop).
3. Nothing else changes: ports, slot, NODE_ENV and every other export reach compose and the npm children exactly as on develop (this closes G283-4 by construction; say so).
4. If the checker's key list or compose's precedence makes this shape not deliver the outcome, STOP and QUESTION with the measurement. Do not fall back to sourcing.

Cells (red-first predictions declared before running, as before):
- G283-1: a .env built from env.example as bootstrap makes it (real template lines, including 236 and 404) reaches `compose up` (stub rc 97). Red at the current head (rc 127), green after.
- G283-2: a .env with `REDIS_PASSWORD=FXSECRETfirst FXSECRETtail` reaches compose AND the output carries 0 occurrences of FXSECRET. Red at the current head.
- G283-3: under `bash -x`, 0 lines carry a .env value (key names in an unset trace are fine). Red at the current head.
- G283-4: exported SECUURA_STACK_SLOT/POSTGRES_EXTERNAL_PORT/REDIS_EXTERNAL_PORT and NODE_ENV reach compose unchanged when .env also sets them. Red at the current head.
- Keep your 3 KS-785 cells and 4 controls (they must still go red on develop and green at the new head) and all 32 existing labels.
- Mutants: restore the `source` line -> the new G283 cells red; unset ALL .env keys instead of the checker's -> the G283-4 cell red; drop the `^KEY=` guard (unset unconditionally) -> a cell where .env lacks the key and the shell has it goes red (add that cell).
G283-6: correct the checker comment at check-slot-credentials.sh:111-115 so it says what the new shape guarantees, comment-only, inside the ruled 102-125 window.
G283-7: correct, and mine: my (iii) did not literally say "OVL_IGNORE_PRS=2052 in the driver". It is ratified now for the fix-round push too, on the same terms (fresh census, merge tree with PR 2052's current head, any hunk overlap = STOP).
Fragments, PR body and ticket comment 970911f3: rewrite to the new shape (in-place edits of your own text, BLUF, no at-sign); the body says what changed from round 1 and why, citing G283-1 and -2.

NOT in this PR: env.example's lines 236 and 404 (pre-existing, unquoted values with spaces). Whether start-local.sh, which already sources .env under set -e, dies on the same template is UNMEASURED (the gate measured the mechanism, not that script). Name both in the READY as the follow-up; the board seat files it after this PR merges.

One push, a NEW commit on the PR branch (no force, no rebase), then READY FOR GATE round 2 of 2 (a compare on the delta, tier 1). The two-NO-GO cap applies: a second NO GO ships the closed instances and tickets the residue.

Pace: you read 54.6% with KS-784 queued. If KS-784's READY plus this round will not fit before about 70%, finish KS-784's READY, then write the fix round's exact state into your HANDOVER FINAL and wrap; say which in your next mail.

Wednesday
