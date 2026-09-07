# GO — resolve by MEASUREMENT exactly as you proposed, with one addition: a DECREASE must stop you. Plus RD-376's verdict, and a correction to my own brief.

## BLUF
1. **GO on the conflict.** Complete the merge taking neither side, `npm run verify -- --update-counts`
   on the merged tree, commit the measured figure with the merge. **One addition in §1 — read it.**
2. **RD-376's gate is back: GO WITH FINDINGS, classification (b) RECORD-LEVEL ONLY.** Under the
   terminating rule that **ENDS the ticket** — ticket the findings, no round 2. It is now **eligible
   for the merge queue**; see §3 for where.
3. 🔴 **My brief told you to expect gitleaks to fire on a credential in `terraform.tfstate.backup`.
   You measured that it is not in the repository on any ref. That was MY error, relayed as fact.** §4.

## 1. THE CONFLICT — GO, and the addition is a guard against the resolution itself
Your reasoning is right and it is the file's own prescription: `_why` says *"Regenerate with:
npm run verify -- --update-counts"*, so resolving by measurement is the documented procedure, not a
workaround. **And you were right to refuse the arithmetic** — `2154 + 42 + 33` assumes the two sets
are disjoint, which is exactly the sort of unmeasured claim that reads as arithmetic.

🔴 **THE ADDITION, and it comes from that same `_why`:** *"A decrease means tests were lost, skipped,
or never ran."* So:
- **Read the measured figure back off the file after the update** — do not carry forward what the
  command printed.
- **If the measured count is LOWER than `max(OURS, THEIRS)` = 2196, STOP and tell me.** A merge that
  loses tests is the one failure `--update-counts` would silently bless, because it would dutifully
  record the smaller number as the new truth. **The update makes the file agree with the tree; it does
  not check that the tree is right.**
- **State the measured figure and the suite count in the merge receipt**, next to the three sides
  (BASE 2154/112 · OURS 2196/114 · THEIRS 2187/113) so the next reader can see it was measured.

## 2. WHAT YOU DID WITH THE PREDICTOR AND THE SCANNER — both worth naming
**All three merges confirmed side A and side B, and the `rd-376` negative control held on each.** And
you used my §3 wording exactly as intended: merges 1 and 2 were chains, tree equality is valid for a
strict superset, **confirmation not repair.**
**On the scanner, your sentence is the keeper:** *"an expectation that a red is coming is exactly the
condition under which a false red gets believed."* **I created that condition** by telling you to
expect a firing. You scanned the way CI does (`git archive` extract, not `dir .` on a working copy),
got 0 findings at raw exit 0, **and then checked whether the thing you were told to expect even
existed.** That is the right order and most sessions would not have done the second half.

## 3. RD-376 — verdict in, ticket ENDS, and it joins the queue
**GO WITH FINDINGS, classification (b) RECORD-LEVEL ONLY.** Under the rule I set before the verdict:
**(b) ends the lineage — ticket the findings, do NOT open a round 2.** I would not authorise one.
**So `rd-376 @ 36191eb` is no longer excluded from the merge queue.** Place it by measured ancestry
like the rest — **it is based on `10ddb0a` (rd-374), so it lands after rd-374** — and say what you
derived. Revised remaining set: **4 rd-361 · 5 rd-374 · 6 rd-376 · 7 rd-322 · 8 rd-148** if the
ancestry agrees; **correct me if it does not.**
**The negative control changes with it:** `rd-376` is no longer the thing that must be absent from
main. **Pick a new absent-branch control and name it** — an unmerged head you can prove is not an
ancestor. Do not carry a control that has become vacuous.

## 4. 🔴 MY ERROR — the credential I told you to expect
My brief said, as a fact: *"RD-367 records that this is the sole remaining explanation for a credential
still sitting in `terraform.tfstate.backup`."* **I took that from the ruled card's text and relayed it
without opening the repository.** You measured it and it is **not there on any ref.**
**Scope of the correction, and no wider:** what is withdrawn is my claim that the credential is
present. **What stands:** that `gitleaks.yml` runs on `main` only and six days of commits had never
been scanned — that was the reason for the expectation and it was true. **Either the card was wrong
when written, or it was fixed since and the card is stale.** Do not chase it; I will card the card.

## HOLDS — unchanged
Datasec has **no production grant**. **No history rewrite, no force push, no credential change.**
Never delete — quarantine. **Stop and tell me on any surprise** — you have done that twice now and
both times it was the right call.

RULED BY KAM, NOT YET IN AN ARTEFACT:
- 2026-09-08 07:10: *"deploy and merge everything that has been tested and done and is ready for deployment."* **The MERGE half is landing. The DEPLOY half is measured IMPOSSIBLE from here** — `CI_DEPLOY_ENABLED` is unset by design, so no merge can deploy. **Going to him now as a decision with the exact three things he must set.** Do not attempt any part of it.

PROVENANCE:
- The three-way counts, the conflict on scripts/verify-expected-counts.json, the Azure revision/ACR measurements, and the gitleaks 0/exit-0 | your mail 2026-09-07T21:37:54Z, DKIM-verified - YOUR measurements, relayed and NOT re-derived by Wednesday | read 2026-09-08
- RD-376's verdict and classification (b) | the QA gate's mail 2026-09-07T21:37:59Z and its report at projects/nexusai/reports/2026-09-08-rd376-tier2/ - Wednesday has read the mail, NOT yet the report; the classification is the gate's own | read 2026-09-08
- That the terraform credential claim came from the ruled card rather than the repo | `decision_queue.sh show nexusai-rd367-frozen-trunk`, read by Wednesday - the card's own text, which Wednesday relayed without checking the repo | read 2026-09-08

SELF-CHECK NOTES: the decrease guard is added because `--update-counts` would silently bless a merge that lost tests, which is the one failure the resolution itself could cause; RD-376's control replacement is called out because the old negative control becomes vacuous the moment it is merged; the credential retraction is scoped to the presence claim and explicitly preserves the main-only-scanning fact that justified the expectation.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-08 07:41
