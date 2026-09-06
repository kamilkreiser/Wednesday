# QA Agent Invocation Brief — Secuura / Blockchain, SEAT B: PR #871 (KS-720)

**Charter first, in full:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`.
Findings only. You never fix, never file a ticket, never touch a builder's tree.

**TARGET — PR #871, KS-720. TIER 1** (it puts authentication on two routes that had none — an auth
surface). head `6845b1cd382e129845df7ae7affe547bef159e30`, cut on `a821bd0aa`; **develop has since
moved to `a8aa723a0fdc70db26177bd91a9c81dbec6640d2`** and may move again.

## 2. Spec / DoD
`POST /api/auth/wallet/link` and `DELETE /unlink` can never succeed today. **Two defects, one
logical path:** the routes carry no `authenticate()`, and `/unlink` calls
`updateUser(..., { walletAddress: undefined })`, which the write loop skips — so **no UPDATE is
issued at all** and the handler returns success having persisted nothing. Both are fixed here: auth
on those two routes only (never the four public ones), and `null` in place of `undefined`.

## 3. Scope — claims to measure. Each is a CLAIM UNDER TEST.
1. **The red-proof PAIR, and why neither alone would do.** Builder's figures: tamper A
   (`authenticate()` removed from both routes) → **5 failed / 2 passed**, the two green being the
   public-route CONTROLS which must not change; tamper B (`null` reverted to `undefined`, auth left
   INTACT) → **1 failed / 6 passed**, only the write cell, with CONTROL 3 green. **Re-derive both.**
   The reasoning to check, not just the counts: under A the write cells red as COLLATERAL (without
   `req.user` the handler never reaches its write), which is exactly why A alone cannot prove the
   second defect fixed.
2. **CONTROL 3 is what makes B readable** — it asserts `/link` DOES issue an UPDATE, so "unlink
   issues an UPDATE" can neither pass because the harness sees every write nor fail because it sees
   none. Verify that control can produce the other answer.
3. **The four public routes must be unchanged.** Enumerate them and confirm none gained
   `authenticate()`, in the code and in the cells.
4. **THE BUILDER'S OWN LOAD-BEARING READ, which it flagged as a read and not a driven test:**
   `walletAddress` is not in the encryption map, which is what makes "`updateUser`'s behaviour is
   unchanged for every other caller" true. **Check it, and check the claim it supports** — if the
   field were in that map, `null` would take a different path.
5. **`userRepo.updateUser` is untouched** — the builder deliberately fixed the CALLER because the
   `undefined` skip is shared semantics with a deferred defect in BACKLOG.md. Confirm the function
   is byte-identical, and say whether any OTHER caller passes `undefined` expecting a clear (i.e.
   whether the deferred defect is live elsewhere).
6. **HUNT — what does `null` actually write, and what reads it back?** Name the assertion first.
   `wallet_address = NULL` versus the column's constraints, any unique index over it, and anything
   that reads the field expecting a string. A clear that violates a constraint fails at runtime, not
   in a unit test with a stubbed `db`.
7. **HUNT — the stubbed `db` is the boundary of every cell here.** The builder says the cells drive
   the real handlers and the real `updateUser` against a stubbed `../db`, with a **gating** stand-in
   for `authenticate`. **Say what that stub cannot see** — parameter binding, SQL validity, the
   actual set clause reaching a real driver — and whether any claim in the PR overreaches it.
8. **No spec change is claimed:** both operations already declare `security: [{ bearerAuth: [] }]`
   and both 400 and 401, so the published contract was already correct and the code did not match
   it. **Verify that** — if the spec does need a change, that is a finding.
9. **The fixture near-miss, for your awareness rather than as a claim:** an earlier iteration mocked
   table `wallet_challenges` where the product uses `wallet_auth_challenges`; the lookup returned
   undefined, the handler threw NotFound, and the control cell reported "link issued no write" —
   **indistinguishable from the defect it guards.** Check that every fixture object in the shipped
   cells is named from the product's own schema.
10. **Full `services/auth` suite** is claimed at 43 files / 595 tests / 0 failed. Verify by SET where
    you can. **If any suite in this repo is red on develop, prove whether it is this PR's doing** —
    the same class of pre-existing red has bitten twice tonight.
11. **Merge-tree against the `develop` you read AT THE TIME, in YOUR OWN copy.** It has moved twice
    tonight. I ran none; nothing here is predicted.
12. **Secret gate:** fabricated RANDOM tokens (never a documented example pair — gitleaks allowlists
    those), prove the canary FIRES in the same scan mode, quarantine by rename, scan the real range.

## 4. Credentials
Pointer only: the project's own `4_Credentials/.env`. **If `gh` under that project's `GH_CONFIG_DIR`
is not authenticated, do NOT fall back to the global config** — report PR-body items as UNVERIFIED,
or use the REST API with the project's own token if one is available to you.

## 5. State-mutation & cleanup
Your own `mktemp` checkout. **Never touch seat A's tree (`2_Project_Files`) or seat B's worktree
(`worktrees/seat-b`)** — both live. No demo VM, no shared local stack, no Docker, no prune, no
containers, and **no writes to any database.** Restore every tamper by INVERSE EDIT, proven by
sha256 — **a tamper does not count until its subject's hash is shown to have changed.** Quarantine
by rename, never delete. Report the LISTEN set before and after.

## 6. Output boundary
Findings only, one verdict, evidence class on every finding, NOT-TESTED at the same prominence.

## 7. Known-fragile / known-changed
- **Every tamper prediction NAMES THE ASSERTION it trips**, or is written as "measure what moves".
- **An instrument is not evidence until it has produced the other answer in the same batch.**
- **A fixture naming the wrong object fails in the same shape as the defect it guards** — a control
  reporting exactly the expected defect is a suspect until its subject is verified.
- **A red-proof harness names its own subject in its output.**
- `git grep -a` / `git diff -a`; `core.fileMode` false; `env bash` 3.2; darwin only — no Linux timing.

## 8. Logistics
Report to `wednesday-agent@agentmail.to`, subject `[QA -> Wednesday] Secuura SEAT B KS-720 (#871)`,
verdict in the first line. Budget ~30 minutes.

PROVENANCE:
- the head, the base, both tamper results and the builder's two stated limits | the builder's READY mail 2026-09-06T11:41:07Z, read whole | read 2026-09-06 21:4x
- the two defects and the ruling that both ship as one logical path, with red-proofs in both directions | Wednesday's ruling to the builder 2026-09-06 21:26 and its by-path confirmation 2026-09-06T11:22:39Z, both read whole | read 2026-09-06 21:2x
- develop a8aa723a0 | `git -C worktrees/seat-b ls-remote` + `cat-file -p` (READ verbs only) | read 2026-09-06 21:4x
- NOT READ by me: the #871 diff itself — I have read only the builder's description of it | not read | read 2026-09-06
