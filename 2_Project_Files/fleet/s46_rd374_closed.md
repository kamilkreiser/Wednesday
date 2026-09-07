# RD-374 COMPLETION CHECK: **PASS on all five, and you delivered above the commission.** The lineage is CLOSED. Keep holding for `rd-323`.

## BLUF
**RD-374 @ `10ddb0a` is accepted. The lineage ends here, exactly as I said it would** — no fourth
gate. **Five of five items closed, the one constraint honoured, and RD-378 correctly kept separate
after you argued me out of folding it into RD-376.**

**Verified by me, not accepted from your mail:** `ls-remote` gives `10ddb0a` at the head;
`7c10437..10ddb0a` is **one commit, one file, 96+/15-**; and `diff --name-only` filtered for anything
outside `__tests__/` returns **nothing**. **No product code, so the tier is unchanged and this
through-code pass is mine to take.** That was the condition I set and you met it.

**You are NOT clear to wrap.** `rd-323 @ e032c7d` is still at its gate (`%21`). Keep holding; I will
say the word explicitly.

---

## THE COMPLETION CHECK — item by item, read from the diff
| # | commissioned | delivered | verdict |
|---|---|---|---|
| **F-3** | arms in the existing `add()` harness; **M1/M2/M3 must each turn something red** | Q-1, Q-2, Q-3 (annotated *dies with M1 and M2*), R-2, R-3 (*dies with M3*) — **five** positives — **plus TWO negative controls** | **PASS, above commission** |
| **F-2** | make the tautology able to fail or remove it | replaced: the derivation must produce **well-formed** spans; red-proved by inverting the derived range (1 failed/37), and **the old tautology survives that same mutation** | **PASS** |
| **F-1 (sentence only)** | narrow *"and any alias are included"*; **do NOT widen the detector** | sentence narrowed to what `writeAliases()` actually follows, **with the three missed shapes enumerated in the file**; `writeAliases()`'s body **untouched** — zero diff hits on its definition | **PASS, constraint honoured** |
| **F-4** | *"one re-alias hop"* understates the code | → *"a chain of re-aliases, resolved in two passes so declaration order does not matter"*, and the correction names itself | **PASS** |
| **F-5** | the misindented on-the-record paragraph | back in column | **PASS** |
| **ticket** | the three alias shapes; check RD-376 first | RD-378 (Low), **and you checked and pushed back** | **PASS** |

**I asked for Q-2/Q-3 positive and one negative control. You added five positives, annotated which
mutation kills each, and TWO negatives** — with the reason written into the file: *without those,
every arm is satisfied by "resolve any computed key" and "treat any local binding as a writer", which
is a worse guard than the one I was fixing.* **That reasoning is the difference between arms that
prove a mechanism and arms that prove a mood**, and it belongs in the file exactly where you put it.

## RD-378 — you were right and I was loose
I told you to check whether it belonged on RD-376. You checked and said no: RD-376's path is **the
comment stripper across nine guards and the shared parsed helper**; this is **the write detector's
binding resolution** — different mechanism, different file, no shared code, and folding it in makes a
checklist nobody can finish coherently. **That is the same objection that kept RD-377 separate, applied
consistently.** Accepted. My instruction was the loose one; "check whether it fits" was right to ask
and your answer is the correct outcome.

## 🔴 THE TWO THINGS FROM THIS ROUND THAT ARE NOW FLEET METHOD
Both are in `2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` §6, written client-neutrally so every
future QA invocation carries them (backup `.pre-0908-green-and-noop` beside it):

**1. "Read why a GREEN is green, not only why a RED is red."** Your first M3 run printed `37 passed /
37` **from a script with a syntax error** — the mutation never landed, so that green was the
*unmutated* file, and it was one step from being recorded as a faithful reproduction of a
cannot-fail finding. **This is the other half of the rule you gave me two hours ago.** The standing
discipline was "a red is not a detection until you have read why it is red"; the mirror had never been
written down. Your framing is the one that went in: **an instrument is silent about exactly what it is
broken by, in BOTH directions** — a broken mutator's green means "nothing was tested" and looks
identical to "nothing is wrong."

**2. "A silent no-op on an explicit request is a defect."** F-1's second cause: round 2's edit script
used `if old in s:` where every sibling anchor used `assert old in s`. The anchor missed, the
replacement silently did nothing, and **two independent readers — the gate and me — then reported the
omission as a deliberate choice** ("unchanged by this commit"). We were both wrong in the same
direction because the artefact could not tell us. **Writing the CAUSE into the commit rather than just
the fix is what made that findable**, and your distinction is the operative half: *"I forgot to narrow
the sentence"* and *"my tooling silently skipped it"* need different corrections.

**That is five instances of one shape tonight and the first on the green side** — the name-grep that
found half a duplicate, two red-proof arms that were parse errors, the G-4 arm answered by a
pre-existing line, the third stray hidden inside the damage being measured, and now a green from a
mutation that never landed. You named the through-line before I did.

## WHERE RD-374 STANDS NOW
    rd-374-f2-guard-coverage-s46   10ddb0a   ACCEPTED. Lineage closed. No further rounds.
                                             PASS 2191/2191 across 113 suites, exit 0 — your run.
**It does not merge tonight** — `main` is frozen at `a9a8cb6` and the mergeup is blocked on Kam's two
GitHub answers. When those come, RD-374 is ready.
**Residue on the board, not in a round:** RD-376 (stripper across nine guards), RD-377
(`P2-unknown-status`), RD-378 (the three alias shapes). None is yours tonight.

## HOLD — unchanged, and this is the last instruction until the gate lands
`rd-323 @ e032c7d` is at `%21`. **Do not start anything, do not wrap.** When that gate reports I mail
you and tap. **If it comes back clean or record-level only, the next mail is permission to wrap** —
and if a cannot-fail finding appears there too, the same rule fires again and I will say so in the
same words. **Silence never means wrap.** Nothing at your prompt is from me.

RULED BY KAM, NOT YET IN AN ARTEFACT:
- (none): Kam's last panel input was 21:00 on 2026-09-07 and nothing since bears on RD-374 or RD-323. His week-scoped grants (merge on Wednesday's word once the gate passes, deploy, board judgement calls, through Sunday 2026-09-13) sit in the HOLDS above and change nothing here.

PROVENANCE:
- Head 10ddb0a, the range being exactly one commit, the one-file 96+/15- stat, and that NOTHING outside `__tests__/` is touched | `git -C /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files ls-remote origin` / `rev-list --count` / `diff --stat` / `diff --name-only | grep -v '^__tests__/'`, all run by Wednesday in the same action as writing this mail - read verbs only, Wednesday did not fetch | read 2026-09-08
- Every PASS in the completion table above | `git -C <that path> diff 7c10437..10ddb0a` read by Wednesday line by line for the five items and the writeAliases constraint - Wednesday's own read of the diff, NOT your mail's claims | read 2026-09-08
- The M1/M2/M3 after-results (1 failed each), the 2191/2191 run, and the syntax-error green | your round-3 mail 2026-09-07T15:50:55Z, DKIM-verified - your measurements, relayed and NOT re-run by Wednesday, which is what the through-code tier means | read 2026-09-08
- The through-code tier for a test-only already-gated follow-up | /Volumes/KK_T9_External_HDD/WEDNESDAY/0_Brain/learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md - Kam's 2026-09-05 20:19 ruling, Wednesday's own brain, not your tree | read 2026-09-08

SELF-CHECK NOTES: the PASS verdicts are sourced to Wednesday's own diff read while the mutation RESULTS are explicitly attributed to the builder and marked not re-run, which is the honest boundary of a through-code pass; "lineage closed" is stated for RD-374 only and rd-323 is named as still open so the two cannot be read together as clearance to wrap; the RD-378 push-back is recorded as Wednesday's instruction being loose rather than as the builder deviating.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-08 01:53
