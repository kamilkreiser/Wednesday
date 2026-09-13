## BLUF
- ADDENDUM to your brief (Wednesday, 07:5x AEST) — TWO changes, both inside L9's partition; nothing else in the brief moves.
- **(1) File ONE KS ticket, under the L9 review stream, for the CI-RUNNER ENVIRONMENT GAPS as a class** — the two findings that are not yours to fix and have no ticket by their phrase: (a) `scripts/audit/audit-locks.mjs` cannot start on the runner (`Cannot find package 'semver'` — the seven `gate-exit-codes.test.mjs` reds in run 34426409872 / job 102712486541 step 7, which #940 made legible); (b) `ks949_main_seed_idempotence.test.sh` fails in step 11 because the runner never builds `packages/shared` (s214's #903 head `a4f71cde6`, `PR Security Gates` step 11 — Wednesday relays s214's read). One ticket, checklist inside it (Kam's 2026-09-07 creation rule: one ticket when one test pass proves it), assigned to the board account, priority High, facts-only, 0 at-signs; its id then goes into every CI-red READY of yours under "attributed to". Do NOT fix them in this round — a runner-install fix is a NEW `.github/workflows` edit, Kam-class.
- **(2) #940 / #941 / #942 will be gated as ONE tier-2 pass** (one test pass proves the three; the merge of each is Kam's anyway) — so send #941's and #942's READYs as planned, then Wednesday commissions the combined gate at #942's READY. #887's re-run evidence stays its own item.

## Recommendation
- No reply needed unless the ticket search turns up an existing home for (a) or (b) — then add the evidence there instead of filing (the 2026-09-07 "who already filed it" rule) and tell Wednesday the id.

## Detail
- Your READY for #940 (21:56:50Z) read whole by Wednesday; your "NOT merging develop into this head" stands (merge-tree clean, tree `cae422e6a`, as you measured).
