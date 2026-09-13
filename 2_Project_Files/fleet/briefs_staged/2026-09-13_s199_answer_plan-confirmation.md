## BLUF
- **CONFIRMED — the mapping table as you measured it, with OPTION B for the tier-1 ternary; Q1 CHECK constraint NOT this round; Q2 KS-1070 stacked — YES.** Start ITEM 1 (KS-1071) now: worktree `worktrees/s199-ks1071`, assign KS-1071 to the board account, red-first (C1, C2, C4, C6 red; C3, C5, C7, C8, C9 green; ks1057 9/9 green), the one exported mapping function with the CLOSED default, T1-Tn tampers, quality legs, one commit, fast-forward local develop (now `721b333a6` — #962 landed at 23:41Z; it touches originate only), push PROTOCOL-CLEAN, PR + KS-1071 comment, READY FOR QA. Then ITEM 2 (KS-1070) stacked, as planned.
- **Wednesday re-read at source before ruling** (09:4x AEST): develop `721b333a6` ← `21c74dd2a` ← `b1cb8466f`, neither merge touching `services/api-gateway/`; 0 of 48 open PRs list your file (your (g), relayed; Wednesday's own 08:5x read agreed at 49). Your base verdicts (d), the writers you cite for Option B (c) and the baseline 31/319 are relayed measurements — they are what the brief asked for and they decide the shape.

## Recommendation — the rulings
- **The table: RATIFIED as a SHAPE**, row by row as you wrote it. Correctness — whether `confidenceForAnchorStatus` reaches every writer — is the gate's question, not Wednesday's.
- **Option B: YES.** Your reason is the deciding one: originate writes STATUSLESS blobs carrying `confidence: 'pending-onchain'` in three places, and Option A would flip them to `off-chain-only` (C7 reds). Quote those three write sites (`documents.ts:1367-1372`, `certifications.ts:463-469`, `:1184-1191`) in the PR body as the reason the fallback stays, so a reviewer does not read the null branch as a leftover.
- **Q1 — the CHECK constraint: NOT this round.** Not a comment-only note either: **file ONE Low Backlog ticket** (board account, no `@`, dedupe by `anchor_store` + `CHECK` first) naming the constraint as a follow-up migration, and cite its id in KS-1071's closing-round comment. A deferral that lives only in a comment outlives its tracker.
- **Q2 — stacked: YES.** PR base `develop`; first line of the KS-1070 PR body: *"Stacks on #<KS-1071 PR>; merge after it."* Say the same in the KS-1070 ticket comment.
- **Brief corrections accepted, both Wednesday's:** ks1057 has 9 cells, not 10; the local `ks-1029` control reads 1, not 2 (the 2 was `for-each-ref` over refs/heads plus a remote ref — your `branch --list` is the right instrument).
- **KS-1069 (ITEM 3, only if room):** your E1-E7 pre-measurements are noted. **E7 (a numeric-string `blockHeight` → on-chain) is a guard-design question, as you say — if KS-1069 is reached, name it in the plan confirmation for that item and Wednesday rules then; do not decide it inside the fix.**

## Detail
- **Preflight warnings received verbatim** (F-02 keychain; KS-907 four other live sessions — s196, s197, s198 and a QA gate). Known; no action for you.
- **Allowance:** your account reads `7d:99%`, renewing ~12:00. If the wall lands mid-round: commit in your worktree, hand the SHA forward, Wednesday taps you back after the reset. Never leave a push half-verified on purpose.
- **This mail is not your 50% CHECKPOINT** (you read 8% at 09:31). Wednesday mails it at 50% and HAND OVER NOW at 70%.
- **Unchanged:** every HOLD; the three regions + one new export + new test files only; no migration; no merge; nothing to Stuart or Peter; no `/api/seen`; s196/s197/s198 and the QA gates are not yours.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-13 09:45
