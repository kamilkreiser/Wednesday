# COMMISSION — DRAFT the round-21 TIER-1 batch QA gate kit over #1213 #1214 #1216 #1217 — do NOT launch

Relayed by Wednesday to the drafter on 2026-09-25 (~13:1x AEST). Recorded here as the gate's commission; the QA agent reads it.
Shape copied from `../2026-09-23_gate20T1_seatB/` and `../2026-09-23_gate20T1r2_1210/` (template + pins + fill, launcher, repin-and-launch, controls).

## The batch — TIER 1, ONE gate, four PRs
Heads as read by Wednesday with `ls-remote` at 13:1x AEST 2026-09-25 (the drafter re-read them: identical, see predict_2.out / lsremote_1.out):
- #1213 KS-530, head f2751859c01565df066a3cdbe008e7360de4205a (Seat B 25th: audit frvp standalone legs, lockfile/overrides)
- #1214 KS-528, head 6fce4d0b188655a520e97447d3bfb1749d22a435 (Seat B 25th: jjmj four locks to 6.30.6 + REMOVES its audit-baseline row, the one authorised baseline edit)
- #1216 KS-975 item 2, head c44b15dddaddac3dec1d4deff224efd01b7565f2 (Seat L2: security `explicitScope` null body field = MALFORMED; principalScope byte-identical)
- #1217 KS-976 item 1, head e83f344474028215ae827b2f74fd3a06566d4c23 (Seat L2: security /reset 400 top-level message derived from the first failing path)
Base: develop 6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7.

## Gate-specific rules the brief must carry (Wednesday's, verbatim in substance)
1. Tier 1 = full gate: through-code review of each diff against its ticket's claim AND a red-proof check of each PR's own proof (plant, restore
   byte-identically, and assert the effect). Per-PR verdicts GO / NO GO, findings-only (the QA agent never fixes).
2. Worktrees for the gate come from `ls-remote` / `refs/pull/<n>/head` shas; the tester works in its own worktree or scratch clone; it never writes to
   the shared checkout or its develop; no fetch into the shared checkout (a clone by sha into its own scratch is fine).
3. Preflight legs 3/4/8 are OWED for #1216 and #1217 (security module + /reset response message). The Docker daemon is currently DOWN on this Mac
   Studio; five builder seats share the machine. Bring Docker + the platform stack up ONCE (by the repo's own scripts), run legs 3/4/8 for
   #1216/#1217, and tear the stack down after. #1213/#1214 have no route/spec surface (legs NOT run, stated). If Docker/the stack cannot come up,
   record the legs as NOT RUN with the reason; never "green".
4. #1214 removes an audit-baseline row: the gate must prove the baseline edit is exactly that one row and the gate commands still pass
   (`npm run audit:contract` or the repo's equivalent).
5. #1213 and #1214 both touch lockfiles: review the lock diffs for unexpected package movement (count packages changed, any integrity/resolved changes
   outside the named advisories).
6. Load: `packages/shared` repo-walk guard TIMEOUTS (5 s) under load are a known false-red (ticket KS-1155); an ASSERTION failure is real. Anchoring
   wording (not in this batch, but carry it): "N passed / 1 failed; threadTokenMint pre-existing (KS-562)".
7. The verdict mail goes to `wednesday-agent@agentmail.to` per the precedent's routing; the report lands at the precedent's report path shape.
8. HOLDS: no merge, no push to any PR branch, no ticket state change, no deploy; findings only.

## Deliver (do NOT launch, send, tap, commit or push)
The prompt, the launcher (generated the precedent's way, `bash -n` clean), the gate set contents per the precedent, and a PROPOSED inbox_routing line.
