# COMMISSION — DRAFT the round-21 TIER-2 batch QA gate kit over #1215 #1218 #1220 #1221 #1222 #1223 — do NOT launch

Relayed by Wednesday to the drafter on 2026-09-25 (~13:4x AEST), widened twice mid-draft (#1222 ~13:5x, #1223 ~13:5x: "After this one, freeze the
batch at six"). Recorded here as the gate's commission; the QA agent reads it. Shape copied from the sibling tier-1 kit of the same round
(`gatesets/2026-09-25_gate21T1`: template + pins + fill, self-locating launcher, repin-and-launch, controls) and the tier-2 precedent
`gatesets/2026-09-23_gate20T2_seatB/` (the tier-2 prompt `briefs/2026-09-23_secuura-batch1202-t2.prompt.txt`).

## The batch — TIER 2, ONE gate, SIX PRs (FROZEN at six)
Heads as read by Wednesday with `ls-remote` at 13:4x / 13:5x AEST 2026-09-25 (the drafter re-read every one: identical — lsremote_1..3.out, predict_4.out):
- #1215 KS-1288, head 5e3419a46db5a1a4e7e640aee2e60dd89db3912a (Seat L3; packages/shared ks781 LEG D pins by TEXT; test-only; legs 3/4/8 NOT run, no surface)
- #1218 KS-897 + KS-896, head 999623d28f7cc3f11140cf379cfd3169e6530b57 (Seat L4; `scripts/__tests__/pre_push_hook_base.test.sh`; test-only; no surface; TWO commits)
- #1220 KS-1129, head 9c2021ba3e770abc9ad464b62fdc245a920389cb (Seat L2; `services/anchoring/src/anchorReadback.ts:103` Number() of block_number — a
  response-field TYPE on GET /api/anchors/verify/:hash, so legs 3/4/8 are OWED; the anchoring suite has a known pre-existing failure)
- #1221 KS-1266, head 0a561a5db393e8f0ced82b86af572c7231330d64 (Seat L1; originate tests: ANCHORING_SERVICE_URL hermetic + the port-1 trap in two files
  moved to port 2; test-only)
- #1222 KS-1181 F2, head 9bce90229ad60b4ab988248648530b3b9a0d951d (Seat L3; packages/shared ks727 error-handler canary cells now read `forwarded`;
  test-only; no route surface, legs 3/4/8 NOT run. The seat's red-proof: error-handler.ts made to throw -> develop 1 failed / 8 passed, branch 9 failed.
  The seat found one filter whose forwarding differs across the three shapes (true / false / true); the gate verifies the cells pin that exception.)
- #1223 KS-1118 (F-2 cell + F-3a comment), head 759726d8d046e6098e720d4768c87e114d0c363c (Seat L1; originate test + ONE route comment in
  `routes/verification.ts:739-741`, comment only, no behaviour; legs 3/4/8 NOT run, state it. The seat's red-proof: the gate's T5 tamper (`hash` moved to
  third) gives 1 failed / 14 passed with only the new P3 cell failing; bare 863 / patched 864 (jest). Its PR body carries a record correction: there is
  no #1136 in the file's history.)
Base: develop 6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7.

## Gate-specific rules the brief must carry (Wednesday's, in substance)
1. Tier 2 = through-code: diff review of each PR against its ticket's claim, AND a check that each PR's own red-proof really bites (re-run the named red
   cell at base = RED and at head = GREEN in the tester's own worktree or scratch clone). Per-PR verdict GO / NO GO, findings-only.
2. Worktrees from `refs/pull/<n>/head` shas; never write to the shared checkout; no fetch into it (a clone by sha into the tester's own scratch is fine).
3. Legs 3/4/8: NOT run for #1215, #1218, #1221 (+ #1222, #1223 by the widening) — no surface, stated. OWED for #1220. The tier-1 gate is bringing the
   stack up for its own PRs; if the stack is up when this gate runs, run legs 3/4/8 for #1220; otherwise record them as OWED, never "green".
4. Anchoring wording, mandatory for #1220: "anchoring N passed / 1 failed; the one failure is threadTokenMint.test.ts > … deterministic per-seed
   policyId, pre-existing at develop 6ab9d5021 (KS-562), not caused by this change".
5. Load: a `Test timed out in 5000ms` in the packages/shared repo-walk guards under load is a known false-red (KS-1155). Re-run once; an ASSERTION
   failure is real.
6. #1221 claims the port-1 files now produce a real ECONNREFUSED: check it with the seat's own probe or an equivalent.
7. HOLDS: no merge, no push to any PR branch, no ticket state change, no deploy.

## Deliver (do NOT launch, send, tap, commit or push)
The prompt, the launcher (generated the precedent's way, `bash -n` clean), the gate set contents per the precedent, and a PROPOSED inbox_routing line.
