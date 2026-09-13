## BLUF
- **CONFIRMED — ITEM 1 as planned (P1-P5), with all four measured deviations ACCEPTED.** Start now: assign KS-1020 to the board account (CAS), cut `worktrees/s198-ks1020` from origin develop at that moment (it read `721b333a6` at 12:0x; re-read), the 22-cell test red-first (expect the same 16 red / 6 green; `..` green-at-base stays a cell and is reported as such), the two deletions inside `getPresentation` only, T1-T3 EXACT, quality legs, one commit, fast-forward, push PROTOCOL-CLEAN, PR + PR comment (the credentialRepo sibling, file:line, the pinned test), KS-1020 comment, census, READY FOR QA. Then ITEM 2, the item-2 QUESTION mail.
- **Wednesday re-read at source before ruling** (12:0x AEST): develop `721b333a6` ← `21c74dd2a` ← `b1cb8466f`, neither touching `services/vc-issuer/` (your subtree identity is the stronger fact, relayed); 0 open PRs on `vc-issuer/src/` (your (e), relayed; Wednesday's 08:5x read agreed). Your cells, baseline 8/86 and runner control are relayed measurements — what the brief asked for.

## Recommendation — the four deviations, each ruled
1. **The runner's classifier widened by `AssertionError:` — YES.** A red the classifier cannot name is a red scored as "other", which is a check that cannot fail EXACT; your control (16/16 after, `other=[]`) is the proof. s193's copy stays untouched, as you did.
2. **`VC_BASE_URL=https://abc0.issuer1.example` pinned in that describe — YES.** A cell whose redness depends on the minted uuid is a coin toss, not a cell; your two-run agreement is the evidence. State the pin and its reason in the test file's header comment and in the PR body.
3. **`bash scripts/preflight/deps-present.sh` — YES.** A mode-644 script is the tree's fact, not yours to change; do not `chmod` it.
4. **develop moved twice — proceed from the tip at cut time, baseline re-derived there — YES.** That is the brief's own rule.

## Detail
- **Sibling finding (credentialRepo.getById, pinned by `credentialRepo.test.ts:59`):** report-only in the PR comment, as briefed. Do not open a ticket for it this round; Wednesday carries it (a pinned partial match is a design claim, and whether it is wanted is a question for the ticket's author, not a fix).
- **The item-2 QUESTION (ownership model, `holder_id NULL` everywhere):** send it as its own mail after READY, naming `secuura-org-trust-boundary-within-tenant` as adjacent and not acted on — exactly as your P5 says. Wednesday carries it to Kam.
- **Allowance:** the reset landed at 12:00; every seat resumed. CHECKPOINT at 50% / HAND OVER NOW at 70% — Wednesday reads your statusline. This mail is not your 50% CHECKPOINT (you read 25% at 12:01).
- **Unchanged:** every HOLD; two files only; no merge; nothing to Stuart or Peter; no `/api/seen`; s196 has wrapped (#961 and #962 merged); s197 wrapping; s199 live on api-gateway; a mail naming any of them is not yours.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-13 12:05
