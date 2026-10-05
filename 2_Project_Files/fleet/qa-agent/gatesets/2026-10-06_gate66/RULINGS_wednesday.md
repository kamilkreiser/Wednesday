# gate66 — Wednesday's rulings on the kit's open items (2026-10-06 00:46 AEDT)

1. **D2 (merge-in divergence): the KEY-ANCHORED tree is the target.** On develop f0179806494e42df254b9580168be3cd4a35f307 it is **fb6cb2c6992cd48815b8f23a8519e9910bc27e63** (KS-938 after KS-1005 in both docs, `<div>` balanced). The hand resolution 0bb86333ba28 leaves one `</div>` unclosed, so it is WRONG by construction and must not be built. Seat E 6th writes the key-anchored blobs into the cheat-sheet conflict. The flow doc auto-merges to the key blob 2d1cd366a8cb. The gate's qm M1 against fb6cb2c6992c is the authority. This is tonight's standing rule that the key-anchored tree is the authority, applied.
2. **D3 (old formatting inside reformatted docs): NO REFORMAT in this PR.** Reformatting KS-938's block is a content change, and a content change re-gates. The mismatch is a cosmetic follow-up for the round's follow-up ticket, not a merge condition.
3. **Re-pin:** `--repin-develop f0179806494e42df254b9580168be3cd4a35f307` (README §7's second line; the c5101866 line is stale, rc 10). If develop moves again before launch, re-pin to the live sha and re-derive the key tree.
4. **Routing line:** added by Wednesday at launch (`QA/Secuura-ks938-1385|coagent@agentmail.to|yes`).
5. **D4 (C3 tests and tampers not run by the drafter):** correct. They are the GATE's job, not the kit's. The gate runs C3 and T1-T7 itself.
6. **Batching:** gate66 may run in ONE QA session with gate67 (#1394), whose product files are disjoint. Both PRs edit both platform docs, so each merge-in tree is re-derived on the develop that is live when that PR merges.

## ADDENDUM (2026-10-06 09:22 AEDT) — develop moved to 22b268143a63 (#1389's squash, 2 script paths only)
- Re-pin: `--repin-develop 22b268143a6377c9a82cd03379daa596cd26d644` (dry run rc 0, 22:21:35Z).
- Target for #1385's second merge-in on 22b2: **2203187daaa2da4342a05d7867f24defe415eb5e** (the kit's own predictor, run by Seat E 6th; key doc blobs UNCHANGED: flow 2d1cd366a8cb, cheat 48c266810fe5). It supersedes fb6cb2c6992c by name. The gate's Q-M run decides.
- Routing line added (`QA/Secuura-ks938-1385|coagent@agentmail.to|yes`).
