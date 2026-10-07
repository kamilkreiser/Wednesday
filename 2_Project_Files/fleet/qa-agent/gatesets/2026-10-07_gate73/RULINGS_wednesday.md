# gate73 — RULINGS for Wednesday (drafted 2026-10-07 ~17:20 AEDT, NOT launched)

## RULED (from Wednesday's commission, 2026-10-07 ~16:27 AEDT — binding on the gate, carried into the prompt)

- R1 TIER: all four T2 (through-code + the PRs' own suites re-run by the gate in its own pinned worktrees). #1408 changes runtime request
  validation on a transfer endpoint: the gate ALSO drives its handler in-process for a wrong-typed signature (400) and a correct / absent
  signature (unchanged), not only reads the test. (Kit: `c2 drive1435` + `compare1435`, cells G1-G10.)
- R2 ACTIONS, the standing wording as corrected by Seat E 10th: (1) Security Scanning — Dependency Audit's audit-contract suites, exit 1 on
  every arm including clean, 12 of the last 12 runs across branches: the ADVISORY-FREEZE class, NOT "semver"; (2) PR Security Gates
  (KS-168) — develop fails the same set; (3) `pr` — the head's failing set a SUBSET of develop's. SUBSET, never equality. Any red outside
  the three is a NO GO finding.
- R3 PRE-EXISTING: `VERDICT: MISMATCH — STOP` for `run_shell_suites.test.sh (59, 0)` inside green pushes is BASE-STATE (files byte-identical
  base == head); the gate confirms and records it; NOT a finding against these PRs. (Kit: c1 P13.)
- R4 The four platform suites are UNMEASURED (local stack down); never counted as passing.
- R5 The GO lines name each head and the merge order assumed; the merge seat takes the composed docs VERBATIM from the kit.
- R6 Every control must be able to fail; a zero gets a positive control; one parser for before / after.

## OPEN QUESTIONS — each needs Wednesday's line before (or at) launch. Drafter's recommendation under each.

**Q-SEAT (BLOCKS LAUNCH).** Who is the merge seat? kit.json `merge_seat` is `null`; the launcher refuses rc 8 and the repin script refuses
rc 8 (a dry run reports it) until it is set. The four GO strings are rendered from it: `GO (<seat>): merge <pr> on gate73`.
*Rec:* ONE merge seat for all four, because each later lander's merge-in is built on the develop that holds every earlier landing — one seat
serialises the chain without a cross-lane handoff. The next R seat (R 10th) is the natural holder (the default order lands the two R-lane PRs
first). Never an author seat (R 9th / E 10th — the launcher refuses both by name). After ruling: set `merge_seat` in kit.json, re-pin
`script_sha256` is NOT needed (kit.json is not a pinned file), re-run the repin script (it re-renders).

**Q-ORDER.** The kit predicts the commissioned order 1407 -> 1409 -> 1408 -> 1410 (composed docs in `composed_2026-10-07/`) and all 24 orders
(`predictions/orders_all24_at_147ae442.json`). *Rec:* keep the commissioned order. The four are disjoint in code, so the order is a docs
question only; there is no functional reason to reorder. If you want #1408 (the only runtime change, live sweep owed) isolated in history
for a sweep bisect, land it LAST instead — `c4 chain --order 1407,1409,1410,1408` predicts it.

**Q-5D (the drafter's main finding — rule its weight).** SKILL §5d (MUST): "Every changed line carries a comment saying WHY it changed and
the Linear ticket number … stating the prior behaviour". NONE of the three product lines does: #1407 `check-package-format.sh:180`
(`-qx` -> `-qxF`), #1408 `transfer/src/index.ts:412` (`signature: z.string().optional(),`), #1410 `originate.openapi.ts:1630` (`.uuid()`).
Each whole file mentions its own ticket 0 times (case-insensitive). CONTROL: the sibling line 6 lines above #1408's — approveTransferSchema's
`reason` — carries exactly the KS-518 comment §5d asks for (same class, same file). #1409 changes only a test file.
*Rec:* a named **Minor**, NOT a blocker: the WHY lives in the commit message (`Refs KS-n`), the PR body, the red-first test and both
platform docs, so `git blame` reaches it in one hop; a NO GO would cost a re-gate round on three PRs for three comment lines. Residue: ONE
tier-3 follow-up commit adding the three comments (no gate), and a BRIEF_TEMPLATE line so payload drafters carry the §5d comment. If you rule
it a blocker instead, the three authors' successors amend, and the kit must be re-drafted at the new heads (END_TREEs and every predicted
tree change).

**Q-NOANCHOR.** #1407's suite does not pin the `-x` anchoring: the drafter's ARM NOANCHOR (`grep -qF`) keeps the suite 8/0. The kit's own
label matrix catches it (red `src/a.ts`, push `src/a.tsx`). *Rec:* polish — a follow-up cell; not a blocker (the product line keeps `-x`,
base had it too; the PR's claim is about LITERAL matching, which the suite does pin).

**Q-NULL.** #1408 moves `signature: null` from 200 (stripped, reject RAN) to 400. The published TransferRejectRequest says `type: string`,
optional, not nullable — so it is spec-consistent. *Rec:* accept; the gate names it and the squash body states it.

**Q-UNION (binding rule for the merge seat — please rule).** Measured: `git merge-file --union` of (develop + earlier lander, base, later
head) DROPS the earlier lander's closing `</table>` (and at step 4 a `</div>`) in the CHEAT doc — git's diff3 trims the lines both blocks end
with — and the repo's own `html_docs_matrix.test.sh` PASSES that broken doc (12 / 0; the guard does not check tag balance). The kit's
read-back and `qm` Q3 / Q4 refuse it. *Rec:* RULE that the merge seat takes the composed docs VERBATIM (or re-runs `c4 chain` on the real
develop) and passes `qm` before squashing — never a union merge, never an edit of git's conflict hunk. Residue ticket (not this batch's):
html_docs_check.mjs should check table / div balance.

**Q-1383.** Open PR #1383 (KS-1401, migration 049) touches BOTH platform docs. If it lands before any batch PR, the kit's predicted trees and
composed docs are void. *Rec:* do not hold #1383 for this; the repin script refuses rc 10 on a moved develop and RE-PREDICTS the chain
(proved: a re-prediction from the post-#1407 develop reproduced steps 2-4 exactly), and the merge seat re-runs `c4 chain` on the real develop.

**Q-X9.** #1409's whole performance unit suite (V2) fails 26 cells under a scratchpad TMPDIR — IDENTICALLY at base and head (tsx's IPC socket
path exceeds macOS's 104-byte limit). The kit offers `c3 … --system-tmp V2` (the system TMPDIR, by id) as named exception X9. *Rec:* accept
X9; the subset comparison (`c3 compare`: head failing SET a subset of base's, +7 passed, +1 suite) is ALWAYS run and is sufficient on its
own if you decline X9.

**Q-LANDS (polish).** Seat R 9th's READY says the subjects "land at 85" / "88" with ` (#NNNN)`; that suffix is 8 characters, so they land at
86 / 89 (both <= 92, nothing breaks). *Rec:* polish, named in READY-CLAIMS.

**Q-WRAP (polish).** #1407's and #1409's cheat blocks have no `<div class="section">` wrapper (#1408's and #1410's do; the base tail section
does). *Rec:* polish, as gate71 ruled the same shape on #1404.

**Q-SWEEP.** #1408 owes a live sweep (§5f): KS-1435 stays In Progress until one runs on the correct host. *Rec:* no gate action; name it in
the GO mail and Linear stays untouched by the gate.

## RULED AT LAUNCH — Wednesday (evening seat, booted 17:31 AEDT 2026-10-07), every open question, binding on the gate and the merge seat

- **Q-SEAT: ONE merge seat for all four = `Seat R 10th`** (kit.json `merge_seat` set). Never an author seat. R 10th also carries PR 5 (KS-1164) and the three held Spark passes, but MERGES COME FIRST: its GO strings are `GO (Seat R 10th): merge <pr> on gate73`.
- **Q-ORDER: keep 1407 -> 1409 -> 1408 -> 1410.** Re-predict with `c4 chain` on the real develop before each merge-in.
- **Q-UNION: BINDING.** The merge seat takes the composed docs VERBATIM (or re-runs `c4 chain` on the real develop) and passes `qm` before each squash. Never `git merge-file --union`, never a hand edit of git's conflict hunk. Residue (not this batch, board search first): `html_docs_check.mjs` / `html_docs_matrix.test.sh` should check table/div balance.
- **Q-5D: a named MINOR, not a NO GO — but OWED, not optional.** The project's SKILL §5d is a MUST, so this is Wednesday narrowing WHEN it is met, not WHETHER: Seat R 10th lands ONE comment-only follow-up commit (the three WHY + ticket comments at #1407 check-package-format.sh:180, #1408 transfer/src/index.ts:412, #1410 originate.openapi.ts:1630) straight after the batch merges, tier 3 (through-code read by Wednesday, no gate). Plus a BRIEF_TEMPLATE line so payload drafters carry the §5d comment.
- **Q-NOANCHOR: polish.** A follow-up cell pinning `-x` anchoring; not a blocker. Residue list.
- **Q-NULL: accept.** `signature: null` 200 -> 400 matches the published spec (string, optional, not nullable). The gate names it; the squash body states it.
- **Q-1383: do not hold the batch for #1383.** #1383 itself stays HELD (pickup) until D 16th's demo round settles. If develop moves, the repin refuses rc 10 and re-predicts.
- **Q-X9: accept, by id.** The subset compare always runs as well.
- **Q-LANDS / Q-WRAP: polish**, named in READY-CLAIMS.
- **Q-SWEEP:** KS-1435 stays In Progress until a live sweep on the correct host (the next kintsugi deploy round covers it). The gate does not touch Linear.
