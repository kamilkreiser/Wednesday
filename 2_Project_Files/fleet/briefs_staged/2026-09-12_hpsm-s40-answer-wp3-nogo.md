# WP3 gate: NO GO 0/7/5/3 — round 2 of 2 under the cap; W3-M6 ruled fail-closed (A-51); sequencing for Monday

**BLUF.** **For session 40.** The tier-1 gate on `0523193` returned **NO GO: 0 Blocker, 7 Major, 5 Minor, 3 Polish** (verdict mail 07:51:13Z, spf/dkim/dmarc pass). **Read the report whole before you plan the round:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-12-composer-0523193-wp3-tier1/report.md` (821 lines; §5 holds the findings with their fix shapes, §4 holds the gate's 52 mutants). Tuesday confirmed its verdict line and finding ids against the mail.

**The gate's reachability reading comes first.** None of the Majors is live on the real content release `47ea3e7c…`, because `contentFromBundle` refuses typed tables (D17). On that content the engine is right: Q-19 passes in all three postures. **Every Major IS live on valid typed content**, which includes the synthetic demo content if Kam rules `demo-content`. **So none of them ships to a demo.**

**This is WP3 round 2 of 2 under the cap.** If round 2 returns NO GO, the closed instances ship and the residue is ticketed. There is no round 3 without Kam.

## What round 2 fixes (all RED-first, each with its own fix-removal mutant)
1. **W3-M1 (D8):** your `64a2b09` fix-forward. **Check it against the gate's fix shape:** refuse fact-path-shaped string operands at LOAD, in constraint AND dependency-`when` positions. The contract's own example must raise an issue, never crash `resolve()`. Close any cell the gate lists that `64a2b09` does not.
2. **W3-M2:** severity rules honour their `when`.
3. **W3-M3:** a silent (null) baseline default uses the baseline's constraint, never the strongest value, with no false "overridden" note.
4. **W3-M4:** group-sensitive decidable conflicts: a decision is stale only when it matches no group's conflict.
5. **W3-M5:** exception fingerprints are RECOMPUTED from their terms, never trusted as carried.
6. **W3-M6: RULED by Tuesday — fail closed.** An item whose `high_impact` is unassessed (null / provisional) is treated as **high impact**:
   - High resolves ON **plus** HIGH_IMPACT_APPROVAL;
   - non-High resolves to MANUAL_APPROVAL;
   - an info issue names the unassessed attribute.

   **Why:** architecture A-51's own principle, *"not assessed means not safe"*, applied to the sibling attribute. It narrows nothing Kam ruled: Q-20 reach says high-impact items need the approval, and this makes that hold when the attribute is unknown. **Kam is told; if he loosens it, you get a SUPERSEDES mail.**
7. **W3-M7:** scan every string input at S0 (discovery answers, L8 values). Never echo a rejected value into an issue's detail. Scan the resolution record, and make `no_cloud_persisted_secret_values` measure it.
8. **W3-m1:** at minimum, kill the five Q-20/§1.9 survivors. Report how many of the 27 surviving mutants you kill and why any remaining one is left.
9. **W3-m2** (the seven silently dropped inputs, each gets an issue or a refusal) · **W3-m3** (the detector covers the gate's 11 missed shapes) · **W3-m4** (the purity blind spots) · **W3-m5** (a single-rule enum gets the right code).
10. **Polish W3-p1, W3-p2, W3-p3: BACKLOG.** p3 (an impossible `as_of`) may be fixed if it costs one line.
11. **PQ-07** (the gate's retracted owner question: a severity override on a content-null item): **BACKLOG as an owner question; behaviour unchanged this round.**

## Sequencing for Kam's Monday review
- **Lane A order:** the phantom-field fix (as ruled at 07:08:28Z) → **WP3 round 2** (above) → WP5, the website.
- **You MAY run WP5 as a THIRD lane now** (a subagent in its own worktree, `apps/web` only, against the WP4 OpenAPI contract), **if** you judge the partition clean and your own context can hold three lanes. If not, keep two lanes and say so.
- **Lane B:** unchanged, WP4 to green.
- **ONE WP3 round-2 READY FOR QA**, carrying:
  - every finding above with FOUND / TESTED / HOW;
  - `64a2b09`;
  - the phantom fix, with the old and new content hash;
  - a 40-character head.

## Unchanged
- No push without a GO and Tuesday's word. Never `rm` except under the volume rule. Never `--no-verify`. Never force-push. No bind mounts from the T9.
- The vault hold stands. No Jira. Mail `tuesday-agent@agentmail.to` only, with your seat named in the subject.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-12 17:54

Tuesday
