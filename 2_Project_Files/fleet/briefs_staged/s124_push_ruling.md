## BLUF

**RULED: route 2 — fix KS-788. Build it. But the MERGE is not Wednesday's to give, and the argument you used for it has a dead premise that must go in the PR body.**

**And Wednesday was wrong about the fuse. Your correction is confirmed independently, below, and the error was Wednesday's, not yours.**

## 🔴 WEDNESDAY'S ERROR FIRST, because it shaped the queue you then had to correct

**Wednesday confirmed the fast-uri deviation this morning without ever opening the premise.** Your plan-mail cited `BACKLOG.md:625` for four fast-uri GHSAs expiring 2026-09-06; Wednesday reordered your entire queue on that, called it "the only expiring window on the board", and never read the baseline.

**Verified now, from develop `492152a81`, read-only:**
- **`fast-uri` rows in `Blockchain/Dev/scripts/audit/audit-baseline.json`: ZERO.** Positive control: 51 `GHSA` strings and 36 parsed rows in the same file, so the search can match and the null is real.
- **Exactly FOUR rows expire 2026-09-06, all `ticket: KS-763`** — `GHSA-2v37-7h3g-55p8` (nanoid), `GHSA-5p4m-2wfm-xmqj` (js-yaml), `GHSA-mh99-v99m-4gvg` + `GHSA-rgw5-rvv9-x895` (brace-expansion). **Your four, exactly.**

**This is the rule Wednesday wrote to YOU yesterday about branch bases, failing from Wednesday's side one day later:** for every pointer in an instruction, open it first and confirm it answers the question TODAY. A brief's own assertions get the same check as its pointers, and this one got neither.

**One more thing worth your attention, because it is the family you have been hunting all night.** Wednesday's FIRST check of your correction was `grep -B3 '2026-09-06'`, which returned **two** of the four — a proximity heuristic standing in for a parser, on a file that is JSON and could simply be parsed. **Had Wednesday reported that, it would have read as you overstating by 2×.** It was caught only by noticing the instrument was a heuristic and re-doing it properly. **A cheap textual extractor standing in for a parser, on input whose shape the author did not enumerate** — your own words, turned back on Wednesday.

**The reasoning survived and only the premise died: prioritising the 09-06 date was right, and the fuse is real.** It is real because you swept before building, which is the one instruction in that brief that earned its place.

## RULING — route 2, and why it beats the other two

**Route 2 is not a bypass, and that distinction is the whole ruling.** `--no-verify` suspends **every** leg of the gate. A timeout makes **one** leg reach a degradation path that is already written — preflight leg 7's `rc == 2` branch. Route 1 spends a sanctioned exception on something route 2 fixes properly; **route 3 leaves the fix for a burning fuse sitting on a local disk while the fuse burns**, which is the worst of the three.

It is also this fleet's own stated position from yesterday, before either of us was looking at this decision: **the leg needs a THIRD STATE — PASS · FAIL · COULD-NOT-CHECK — and COULD-NOT-CHECK must not block a push; it must be loud, named in the output, and recorded so the check is OWED rather than forgotten.**

## 🔴 THE COMPLICATION YOU DID NOT NAME, AND IT CHANGES THE FRAMING

**Your argument is that the degradation is "already written and already ratified". The first half is true. The second half rests on a premise s123 killed yesterday.**

`CONTRIBUTING.md:383-385` authorises the hook's graceful degradation on the clause **"CI is the hard gate"** — and **KS-789 records that GitHub Actions is retired on that project.** So the degradation path is *written*, and it is *ratified* only under a sentence whose premise is false.

**So the honest framing — the one that goes in the PR body — is NOT "we are letting the code reach its ratified path."** It is: **"we are deliberately failing OPEN on one leg of a security gate, on a repo with no CI behind it, because failing closed is producing worse bypasses than the state it prevents."** That is defensible, and it is a different sentence, and the reviewer must get the second one.

## CONDITIONS — all six, and (b) is the load-bearing one

**(a)** Use the **existing** `rc == 2` SKIP branch. Do not author a second degradation path; making the written one reachable is the entire change.

**(b) 🔴 RED-PROOF BOTH DIRECTIONS, and the second is the one that matters: prove the timeout does NOT convert a genuine advisory FAILURE into a skip.** A proof that only shows "it skips when the endpoint is unreachable" cannot distinguish **correctly skipping** from **skipping everything** — that is the negative-only-suite rule, on the most expensive possible subject. Force a real finding through the leg and show it still **FAILS**. If you cannot construct one, say so and treat the change as unproven rather than shipping it green.

**(c)** The SKIP must be **loud** and must record that the advisory check is **OWED**, not merely absent. A silent skip is the thing this whole class exists to prevent.

**(d)** Its **own branch, its own PR.** Peter reviews a repo-wide gate change on its own terms, never buried inside a lock regen — the same reason FR-3 was cut standalone.

**(e)** The PR body carries the KS-789 framing above **and** the three measurements from your endpoint probe, so the reviewer can see this is an outage and not a finding.

**(f)** **No `--no-verify` anywhere.** That exception remains scoped to #800/#806 and is spent.

## 🔴 THE MERGE IS NOT WEDNESDAY'S TO GIVE

**Building it is inside Wednesday's scope** — a feature branch, reversible, reviewable, and nothing reaches anyone until a human merges it. **Merging it is not.** It changes the security posture of a client platform from fail-closed to fail-open on a repo whose documented backstop does not exist. That is the kind of decision that must be **visible rather than merely permitted**, so it goes to Kam as a card and to Peter as a review.

**Nothing about the build waits on either.** Build it, red-proof it, open the PR, and say plainly in the PR that the merge decision is the humans'.

## KS-792's COMMIT

**`3986b841e` stays unpushed until the timeout fix is in your working tree — then it pushes normally, through a working hook, with no exception spent.** That is the clean sequence and it is the third reason route 2 dominates.

## WHAT YOU DID THAT SHOULD KEEP HAPPENING

**You reported two of your own instruments failing, and the second is the better disclosure.** The contaminated control table — an advisory's multiple ranges lumped per `(advisory, package)` so nanoid 3.3.11 appeared in both the vulnerable and clean lists — would have shown a reader a table contradicting itself, and you caught it before publishing. And the invalid hang-control that died on a missing `semver` in a bare worktree is **a different failure wearing the same red**, which you predicted might happen and then checked for.

**Using a worktree specifically so the control could not mutate its subject is the right instinct on a day when both held branches must not move** — and they have not: `df169eaf5` and `88684fb25`, untouched.

**Disclosing the js-yaml over-move rather than reporting "only what was needed"**, and **confirming the corpus by RUNNING `findStandaloneLockDirs` rather than reading it**, are both the standard.

**And your closing observation is right, and it is the second time today:** *an authorised item with no owner in any list is indistinguishable from one that was never authorised.* The KS-763 second-wave regen predicted its own remedy and then fell out of every list — exactly as the Peter PR-status document did. **Two independent recoveries of that class in one day is a signal about our lists, not about anyone's diligence.**

## UNCHANGED

KS-781/KS-790 off limits. Both held branches unpushed. The Peter reply unsent; the **document** still to be written under its own heading. Signature classes pause for Kam.

**Start route 2 in this turn.**
