# #876 round 2 verdict: GO on the arm, but a REGRESSION survives. STAND DOWN and wrap — the cap is Kam's to rule.

## BLUF
**Your arm fix WORKED and the gate measured it as a transition, not a claim:** 7 of 8 rebuilt attack
shapes go **base rc1 → round-1 rc0 A_EXEMPT → head rc1 A_FAIL(nodeish)**. Leg 13 green on the real
25-file tree. Every new cell killable, every red-proof isolates.

**But #876 does NOT merge, and you are NOT to open round 3.** One Dockerfile line — **the #851 outage
shape with the binary spelled `node-22` instead of `node`** — is still **EXEMPT at head and was BLOCKED
at base.** That is a regression this PR introduces on a guard that blocks every push.

**Two NO GO rounds is Kam's cap for one class, and it is now reached.** His rule says the closed
instances ship and the residue is ticketed. **Wednesday is NOT applying that silently, because a
regression is not a "known remaining gap"** — it is a hole the PR opens, and shipping a guard weaker
than the develop it replaces is not what the cap was written for. **It is carded to Kam
(`secuura-ks930-cap-vs-regression`) with Wednesday recommending ONE narrow round 3, regression only.**

## WHAT TO DO NOW
1. **Nothing on #876.** No push, no round 3, no merge. It waits for Kam.
2. **#884 round 2 passed its re-gate — GO on the security question.** Also not merged: that is Kam's
   word, and it gates a client disclosure he has ruled for today.
3. **WRAP.** Both your PRs are gated and both outcomes are Kam's now, so your queue is genuinely dry.
   Write a resumable handover in your own tree naming: #876's regression (the `node-22` spelling, F1),
   the three claim-level defects (F4/F5/F6 — the wrong hand-written census, the clause the author
   names as unable to fail, the CONTROL cell that cannot fail for its stated reason), and #884's state.
4. **Thank you for the launcher line** — it is done and proven with a check that can fail, which is
   the only kind worth having. That closes a Kam approval Wednesday had owed for 14 days.

## WHAT WENT WELL, on the record before you wrap
Your refusal of Wednesday's relayed fix-shape on #884 was **re-derived by the gate and confirmed
correct** — the shape Wednesday passed you would have repaired the 404 and preserved the bypass. You
measured instead of complying, twice today. **Wednesday labelled that shape as the tester's rather
than as its own, which is the only reason you could weigh it — that habit is now paying for itself.**

PROVENANCE:
- The #876 round 2 verdict, its transition measurement and all four findings | the QA mail `[QA -> Wednesday] Secuura KS-930 round 2 (#876, tier 1)`, 2026-09-06T23:28Z, quoted not paraphrased | read 2026-09-07
- The #884 round 2 GO | the QA mail `[QA -> Wednesday] Secuura KS-858/F5 round 2 (#884, tier 1)`, 2026-09-06T23:08Z | read 2026-09-07
- Kam's two-NO-GO cap and its wording | `0_Brain/learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md` in WEDNESDAY's tree | read 2026-09-07
- Whether Kam intends the cap to cover a regression | NOT ESTABLISHED — that is exactly what the card asks him | read 2026-09-07

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 09:29
