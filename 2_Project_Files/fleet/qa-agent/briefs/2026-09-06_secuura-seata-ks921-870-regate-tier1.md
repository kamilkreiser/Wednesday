# QA Agent Invocation Brief — Secuura / Blockchain, SEAT A: PR #870 (KS-921) RE-GATE

**Charter first, in full:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`.
Findings only. You never fix, never file a ticket, never touch a builder's tree.

**TARGET — PR #870, KS-921, FIX ROUND. TIER 1** (the guard is wired as preflight leg 13 and blocks
every push; its failure mode is a false CLEAN and a false BLOCK stops every author).
head `2f6b30fdeb6d68c32b946c3ba3b648fe4ca2d9b7`; previously gated at `191bc1cc9`. **Base develop is
now `60d1ce97e235528f1f3815f90881a80984e340f0`** — it moved four times tonight; read it yourself.

**A previous pass gave this PR PASS WITH FINDINGS: 3 Major, 6 Minor, all in the guard itself.** This
round answers four of them. **Scope yourself to those four plus regression** — the rest of that pass
held and is on the record.

## 2. What this round was ruled to fix
- **F-1 (Major, FALSE CLEAN):** the corpus grep was case-sensitive while Dockerfile keywords are
  case-insensitive by specification, so `Copy --from=shared-builder` left the class silently and the
  guard printed `OK — 1 of 1 clean` over a corpus of two with the second broken in both clauses —
  **surviving STRICT mode**, invisible to the vacuous-green protection (which fires only on an
  ENTIRELY empty class), with the derived count shrinking in step so no figure looked wrong.
- **F-2 (Major, FALSE BLOCK):** only the FIRST `USER` per stage was recorded, so root → link → drop
  privileges was rejected with a message factually wrong about the file.
- **F-4 (Major, FALSE BLOCK):** the re-link regex required one literal spelling, rejecting `ln -sf`
  — *"the likeliest of all my false blocks to be written by a real author"*.
- **F-5:** stage names are resolved case-insensitively by Docker; the guard keyed on the literal.

## 3. Scope — claims to measure
1. **The four fixes, each red-proofed by restoring its own defect.** Builder's table: F-1 → 1 cell
   reds, F-2 → 1, F-4 → 2, F-5 → 1. **Re-derive all four**, and confirm no tamper reds a cell
   belonging to another fix — the "exactly one, no collateral" property is what makes each cell its
   own evidence.
2. **F-1 IS FIXED TWO WAYS, and the second is the interesting one.** `-i` closes the miss we found;
   a **cross-check** compares the derived class against a deliberately looser instrument and fails
   **loudly by name** on any file mentioning `shared-builder` that the precise selector misses.
   **Drive the cross-check itself:** make the two instruments disagree and confirm it fires; then
   confirm it is LOUD (an error, not a warning) — the builder's reasoning is *"a false block is
   visible and costs one commit; a false clean is neither"*, and that asymmetry is the design.
3. **THE BUILDER'S OWN CORRECTION, and the thing I most want pressed.** Its first F-1 regression cell
   asserted only *"exit 1 and the filename appears somewhere"* — and with `-i` removed, **the
   cross-check ALSO exits 1 and ALSO names the file**, so the cell passed against the exact tamper it
   existed to catch while the suite stayed 26/0. It now asserts the file was **JUDGED BY CLAUSE A**
   rather than merely reported as divergent. **Verify that distinction actually holds under the
   tamper** — this is the defence-in-depth trap: every layer added for safety can absorb a tamper and
   leave the instrument unmeasured.
4. **F-2's new oracle:** the EFFECTIVE `USER` at the re-link's ordinal, not the first seen; root, or
   no `USER` at all, passes. Drive root → link → drop, and drive a genuine non-root re-link that must
   still fail.
5. **F-4's widened matcher:** any short-flag cluster containing `s`, any destination ending at
   `node_modules/@secuura/shared`. **The negative half must be pinned too** — a link to a DIFFERENT
   target must still fail. Confirm both halves.
6. **F-5:** `AS Builder` + `--from=builder` must no longer warn, and must not block under
   `SHARED_RELINK_STRICT=1`.
7. **Regression:** suite 26/0, guard green on all 25, and the **13**-leg preflight passing in the
   hook. Nothing that passed in the first gate may have moved. **Note this branch carries 13 legs
   while others carry 12 — both are right where they sit; do not read it as drift.**
8. **The awk quoting incident the builder reported:** an apostrophe in a comment inside the
   single-quoted awk program ended the quote. **Confirm the shipped file parses and that a planted
   syntax error is caught** — a program that fails to parse can print green cells before dying.
9. **KS-930 carries F-3, F-6 and F-7** and is deliberately NOT in this round. Do not re-litigate
   them; if you find they interact with these four fixes, that is a finding.
10. **Merge-tree against the develop you read AT THE TIME, in YOUR OWN copy.** I ran none.
11. **Secret gate:** RANDOM fabricated tokens, canary proven to FIRE in the same scan mode,
    quarantine by rename, then the real range.

## 4. Credentials
Pointer only: the project's own `4_Credentials/.env`. You should need none. **If `gh` under that
project's `GH_CONFIG_DIR` is not authenticated, do NOT fall back to the global config.**

## 5. State-mutation & cleanup
Your own `mktemp` checkout. **Both builder seats are WRAPPED and their panes are closed, but their
trees are not yours** — `2_Project_Files` and `worktrees/seat-b` stay READ-ONLY. No demo VM, no
shared local stack, no Docker, no prune, no containers. **A tamper does not count until its subject's
hash is shown to have changed.** Quarantine by rename, never delete. LISTEN set before and after.

## 6. Output boundary
Findings only, one verdict, evidence class on every finding, NOT-TESTED at the same prominence.

## 7. Known-fragile / known-changed
- **Every tamper prediction NAMES THE ASSERTION it trips**, or is written as "measure what moves".
- **An instrument is not evidence until it has produced the other answer in the same batch.**
- **A cell that cannot tell the fix from its own fallback is not a regression test** — this PR is
  where that rule was learned; hold it to its own lesson.
- **A control that cannot match is not a control.**
- `git grep -a` / `git diff -a`; `core.fileMode` false; `env bash` 3.2; darwin only.

## 8. Logistics
Report to `wednesday-agent@agentmail.to`, subject `[QA -> Wednesday] Secuura SEAT A KS-921 re-gate
(#870)`, verdict in the first line. Budget ~30 minutes.

PROVENANCE:
- the new head, the four fixes, the red-proof table, the cross-check design and the builder's own non-discriminating-cell correction | the builder's READY mail 2026-09-06T11:49:13Z, read whole | read 2026-09-06 21:5x
- F-1 through F-5 as originally found, with their repros | the first gate's verdict mail 2026-09-06T11:36:19Z, read whole | read 2026-09-06 21:4x
- the ruling that F-1/F-2/F-4/F-5 land in this PR and F-3/F-6/F-7 become KS-930 | Wednesday's ruling 2026-09-06 21:44, sent through the gate | read 2026-09-06 21:44
- develop 60d1ce97e | seat B's wrap mail 2026-09-06T12:04:08Z (merge receipt from objects), read whole | read 2026-09-06 22:1x
- NOT READ by me: the #870 fix-round diff itself | not read | read 2026-09-06
