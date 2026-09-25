# COMMISSION — DRAFT the round-21 SECOND TIER-1 batch QA gate kit over #1224 #1226 #1228 (+ #1230 by widening) — do NOT launch

Relayed by Wednesday to the drafter on 2026-09-25 (~14:52 AEST), WIDENED mid-draft (~15:2x AEST: "WIDEN the gate21T1b kit to FOUR PRs, then freeze at
four. Add #1230 KS-1131 … Do NOT wait for L4's KS-1127+1089+1135; it goes in a later batch"). Recorded here as the gate's commission; the QA agent reads
it. Shape copied from the sibling tier-1 kit `gatesets/2026-09-25_gate21T1/` (template + pins + fill, self-locating launcher with asserting checks,
repin-and-launch, controls) with the tier-2 sibling's lessons (`gatesets/2026-09-25_gate21T2/`: moved-kit re-fill, doctored control phrases outside the
by-name ladder) and the base-invariant checks of Wednesday's 04:35Z ANSWER to Seat B 25th (`answer_seatB25_movedbase`).

## The batch — TIER 1, ONE gate, FOUR PRs (FROZEN at four)
Heads as read by Wednesday with `ls-remote` at 14:5x / 15:1x AEST (the drafter re-read every one: identical — lsremote_1.out, lsremote_2.out, predict_3.out):
- #1224 KS-1179, head d4862b3eee3566635c61cf9d0b810131140e4fa2 (Seat L3, WRAPPED; security ssrf-guard — a security surface, which is why it is tier 1)
- #1226 KS-872, head fcda1a6ef7e4fde33215466a29b730025fcd6233 (Seat L3, WRAPPED; type-only change)
- #1228 KS-1171, head 43279280f76ed9982782ad7652288d2c3d522b71 (Seat L2, WRAPPED; anchoring; Kam ruled option c on card
  `secuura-ks1171-when-is-an-anchor-absent`: an anchor is ABSENT only with >=2 answered polls AND an answer >=60 s after the 400; the seat rewrote 4 cells
  and added 9 incl. a "real-poller" cell; its READY says legs 3/4/8 are OWED)
- #1230 KS-1131, head 1116dab0466da48ce96c4811f8086b061a49aa70 (Seat B 25th, tier 1; the Ornith fix, F-A + F-B CALLSHAPED in services/auth; two commits)
Develop at commissioning: ecb1aa75aefae35a8e2d8694f303adac7c17ab55 (MOVED today: #1216 feb5cf0c4, #1217 bc092c667, #1214 ba4016fb8814, #1213 ecb1aa75).
Every head was cut from the OLD develop 6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7 — MEASURED (merge_base via the GitHub compare API, behind 4; parents
via the scratch clone): the kit's merge checks are base-invariant.

## Gate-specific rules the brief must carry (Wednesday's, in substance)
1. Tier 1 = full gate: diff review of each PR against its ticket's claim + each PR's red-proof really bites (RED at base, GREEN at head, in the tester's
   own worktree/scratch clone) + legs 3/4/8 where there is a surface. Per-PR verdict GO / NO GO / GO WITH FINDINGS, findings-only. Round 1 of 2 under
   the two-NO-GO cap.
2. Worktrees from refs/pull/<n>/head shas; never write to the shared checkout; no fetch into it.
3. Stack: bring Docker + the local stack up ONCE in a free slot (2-4), run legs 3/4/8 on the surfaced PRs, tear it down. The previous tier-1 gate found
   leg 4 NOT RUN because the demo login was refused (401): record leg 4 honestly the same way if it recurs, never "green".
4. #1228: run the KS-1171 integration cells under `jest.integration.config.js` against the stack's real Postgres, and verify the rewritten cells
   implement Kam's ruling (c) exactly (both conditions). Anchoring wording, mandatory: "anchoring N passed / 1 failed; the one failure is
   threadTokenMint.test.ts > … deterministic per-seed policyId, pre-existing (KS-562), not caused by this change" — only if that failure appears; measure it.
   (DRAFTER'S MEASUREMENT, carried into the prompt as "measure first, then run or record": no integration cells and no jest.integration.config.js exist
   under services/anchoring — README section 6.)
5. #1224: a security guard — red-proof the guard against the product's own path (tamper the guard, the named cells must go red), and check what an EARLY
   RETURN or new check does to existing callers' negative-asserting cells (the 2026-09-20 early-return lesson).
6. #1226: type-only — confirm zero runtime change (tsc + emitted JS or equivalent), and that it touches no dependency/lockfile (no package.json/lockfile
   in this round).
7. Load false-red: `Test timed out in 5000ms` in packages/shared repo-walk guards under load is KS-1155's class; re-run once; an assertion failure is real.
8. Orphaned `login_stub.mjs` listeners: reap ONLY the gate's own (by cwd + ppid, never by name; never pid 1); report the count before/after.
9. HOLDS: no merge, no push, no ticket state change, no comment on any PR or ticket, no deploy.
10. The GO string verbatim: `GO: merge #1224, #1226, #1228, #1230 batch` (widened from the three-PR string by the widening).
11. Routing name `QA/Secuura-batch1224`; the PROPOSED routing line in the sibling's format — NOT written into inbox_routing.conf by the drafter.
12. (widening) #1230: red-proof one arm per conjunct as the seat did (arm A both red / B only F-B red / C all green); the seat's MEASURED residual (a
    comment with a paren inside the `!user` block still false-greens property 1; the same shape in the gap false-reds) — record it as a KS-1131 residual
    or red-prove it, never green; F-A strictly RELAXES property 2 on the reset-token path — red-prove that blind spot or record it as a KS-1131
    residual. Legs 3/4/8 have no surface for #1230. #1231 / #1232 (same READY mail) are tier 2 and NOT in this gate.

## Deliver (do NOT launch, send, tap, commit or push)
The prompt, the launcher (generated the precedent's way, `bash -n` clean), the gate set contents per the precedent, controls run both ways, a `--dry-run`
of the repin script, and a PROPOSED inbox_routing line.
