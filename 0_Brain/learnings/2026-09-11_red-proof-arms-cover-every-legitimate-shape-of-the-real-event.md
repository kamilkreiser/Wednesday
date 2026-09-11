---
date: 2026-09-11
type: correction
source: ledger w=2 in one hour (12:08 and 12:4x rows, 2026-09-11) — the #953 push-protocol red-proof
status: live
tier: M
---

# A checker's red-proof needs a CLEAN arm for every legitimate shape of the real event it will guard — and a checker whose failure path is a destructive remedy needs a false-DIFF arm as much as a false-CLEAN one

**The operative case, so the headline matches it:** Wednesday is about to specify, accept or ratify the red-proof arms for a CHECKER — a verify step, a guard, a gate, a protocol — that will then run against a real event (a push, a deploy, a migration, a sync). **Before ratifying, list the legitimate shapes of THAT event from the commission itself, and ask of each: which arm shows the checker reads CLEAN on it?** Then ask the mirror: **if the checker reads DIFF wrongly, what does its failure path DO?** If the answer is "restore", "revert", "delete" or "kill", a false DIFF is a destructive act, and it needs its own arm.

## The two cases, one hour apart, same root cause

1. **12:08 (w=1).** Wednesday's s178 brief specified the arm that should prove `push_protocol.py` was blind to worktree-HEAD rewrites as *"a planted rewrite with config and refs untouched → old verify CLEAN"*. The checker's own CLEAN predicate (`:51`, read by Wednesday that hour) requires exactly ONE added tracking ref, so an untouched-refs plant reads DIFF under the old verify too — **the arm could not show the defect.** s178 caught it from the code and replaced it with (U) expected ref only / (P) expected ref + HEAD rewrite.
2. **12:4x (w=2).** Wednesday ratified (U)/(P) at 02:07Z. **(U) was a FIRST push (tracking ref ADDED); the round's real push was a FAST-FORWARD to an existing branch — the shape Wednesday's own brief had specified.** The predicate, inherited from a first-push script, reads a fast-forward as one removed + one added line for the same ref, so the real push printed **PROTOCOL-DIFF on a clean push.** The protocol's instruction on DIFF was *restore from the snapshot* — which would have written a tracking ref contradicting origin into the shared repo, **the exact damage the protocol exists to prevent.** s178 stopped and asked instead; Wednesday verified read-only (config sha identical to the gate's baseline, refs 798, the one moved ref == origin's head) and ruled it expected, no restore.

## The diagnosis w=2 owes

**Both times the arms were written from the DEFECT, not from the SERVICE.** The finding said "HEADs are unchecked", so the arms were about HEADs. Nobody enumerated what the checker would actually be fed in service — first push, fast-forward, re-push to an existing branch — so the clean arm covered one legitimate shape and the checker shipped blind to the other. **The w=1 lesson was filed as "specify the arm against the full predicate", and it did not fire at the ratification an hour later because the ratification looked like a different act: accepting an agent's better arms, not writing my own.** Receiving a correction lowers exactly the attention that would have caught the next gap.

## How to apply

1. **Enumerate the legitimate shapes of the real event from the commission, in writing, before any arm is accepted.** For a push: first push · fast-forward to an existing branch · push to a branch with an open PR. For a deploy: first deploy · redeploy of the same image · rollback. For a sync: first run · incremental · no-op.
2. **Every legitimate shape gets a CLEAN arm. Every defect class gets a DIFF arm.** A matrix with one clean arm is a checker proven on one input.
3. **Ask what the checker's failure path does.** If DIFF triggers a restore, revert or delete, a false DIFF is destructive — write the arm that proves a legitimate shape does NOT trip it, and until that arm exists, the instruction on DIFF is **STOP and ask**, never the remedy.
4. **Ratifying someone else's arms is writing them.** Apply rules 1–3 to arms an agent proposes, especially one that has just corrected you — the correction is evidence the agent is careful, not that the matrix is complete.
5. **Do not re-aim after the result.** When a real event exposes the gap, the fix goes into the NEXT use of the checker with its new arms written first; the event already verified stays ruled on its evidence.

**Family:** [[2026-08-07_a-check-that-cannot-fail]] (a red-proof that cannot redden for the right reason — and its mirror, a check that cannot pass for the right reason) · [[2026-08-17_check-the-refusal-before-the-kill]] (a destructive remedy behind a refusable check) · [[2026-09-10_a-two-answer-question-hides-a-third-state]] (rule 5: it applies to questions you WRITE — and to matrices you ratify) · [[2026-09-10_i-endorse-things-i-have-not-read]] (a ratification is load-bearing) · [[2026-09-08_a-new-rule-is-most-dangerous-just-after-adoption]] (the w=1 rule failed at its first exception, one hour old).

## EXTENSION 2026-09-11 15:3x (w=3) — the RULE TEXT in a brief is an arm too: put every legitimate shape through it clause by clause
**The case.** The tier-2 gate on `push_protocol.py` @ `d2a53096` reported W-1 as Wednesday's error: the brief's TARGET rule required config IDENTICAL and an UNCHANGED T to equal origin's head, while its item 2 required a refused push and a first push to read CLEAN. A refused push with a stale or absent T, and `git push -u` (which writes `branch.<b>.remote/.merge`), satisfy item 2 and violate TARGET; the file implemented TARGET, and the gate measured three false DIFFs.

**The rule, extended:**
1. **A checker's specification has two halves — the RULE and the SHAPE LIST — and they are written from different sources** (the defect and the commission). Before sending, put every shape in the list through the rule, clause by clause, and write the verdict each clause yields. A shape the rule rejects and the list accepts is a contradiction the builder will resolve silently one way and the gate will report the other.
2. **Ask what the ordinary form of each shape does to the state the rule inspects.** `push -u` writes config; a no-op push can move T; a refused push leaves T stale. The ordinary variants are where a defect-first rule is wrong.
3. **Enforcement candidate (w=3 promotes it):** every brief for a checker carries a LEGITIMATE-SHAPES table — shape · expected verdict · the rule clause that yields it. The table makes rule 1 a thing written down rather than a thing remembered.
