# QA GATE — Datasec/NexusAI **RD-377** `rd-377-verdict-domain-s47` @ `fabcc93`. **TIER 2, FULL PASS.**

## Scope
    fabcc93   THE SUBJECT — rd-377-verdict-domain-s47
    e032c7d   its base, rd-323-scheduler-failure-vocabulary-s45 (a CLOSED lineage; do not re-gate it)
    NOT main — frozen at a9a8cb6, 250 behind. Nothing merged, nothing deployed. **You may not merge.**

**Round 1 of this ticket.** Claimed `npm run verify`: **PASS 2196/2196 across 114 suites**
(from 2175/113). Evidence comment 37286.

🔴 **THIS ROUND TOUCHES PRODUCT CODE** — three schedulers — which is why it is a full pass and not
through-code. **It is scheduler behaviour, not a rendered surface:** RD-76 gates every authenticated
page, so the artefacts are the suite and the mutation arms driven against the real `runOnce` with
local HTTP stubs. A local run at `fabcc93` is correct here; **do not claim the demo was tested.**

**STACKED:** `rd-323 @ e032c7d` must merge before `rd-377`. Two merges, two blast radii — say which
one you mean.

## What changed
    backend/services/schedulers/healthSweeperScheduler.js   bucketFor(), bucket-driven counts,
                                                            unknown-status row, additive `unknown`
    backend/services/schedulers/morningDigestScheduler.js   healthUnknownStatus      (additive)
    backend/services/schedulers/slaReportScheduler.js       unknownStatusDetections  (additive)
    __tests__/helpers/verdict-domain.js                     NEW — acorn-only static + driven domain
    __tests__/health-sweep-unknown-readers.test.js          NEW — 7 cells
    __tests__/scheduler-failure-vocabulary.test.js          D-4 cell onto the derived domain, +14
    scripts/verify-expected-counts.json                     2175/113 -> 2196/114

---

## 🔴 FIRST JOB — the builder filed a finding against its own work. Verify the ARMING, not the fix.
Its words: *"My `bucketFor()` docblock claims production is TOTAL. A mutation removing that fallback
passed 33/33 — because every verdict today IS mapped, so the fallback is unreachable from the real
classifier and the claim had nothing behind it."* **It closed this with a synthetic arm.**

**This is the fourth appearance of one class in this codebase in twenty-four hours** — a claim with
no cell behind it, each time inside the work written to close the previous one. **So the arm is the
subject, not the fallback.** Specifically:
1. **Remove the `bucketFor()` fallback and confirm something now REDDENS.** If it still passes, the
   arm is decoration and the finding is not closed.
2. **Confirm the arm reddens for the RIGHT reason** — read the failure, do not just observe a red.
3. **Ask what the arm CANNOT see.** A synthetic arm proves the fallback works when driven
   synthetically; it does not prove the fallback is reachable from the product. **Say plainly which
   of those two the arm establishes**, because the docblock's word is "production".

## SECOND — the derived domain must be DERIVED, not written down
`__tests__/helpers/verdict-domain.js` is new and claims an **acorn-only static + driven** domain.
**This is the exact claim that was FALSE one round ago** on RD-323 (the strings were derived; the
probe *inputs* were hand-listed, and a real fifth verdict passed 2175/2175 unnoticed while silently
joining the escalation set). **So do not read the helper — test it:**
- **Add a genuine fifth verdict to `_classify` and confirm something reddens WITHOUT the test being
  edited.** Assert the tamper LANDED first (grep it, and drive the real classifier to see it emitted)
  before believing any result.
- **Confirm the static (acorn) and driven halves AGREE**, and say what happens when they disagree —
  a helper with two sources needs a stated rule for a conflict, or it silently prefers one.
- `acorn-walk` was a round-1 finding on a sibling branch for resting on a transitive dep. **Check how
  this helper resolves acorn** and whether it is declared.

## THIRD — the additive constraint is a RULE, not a preference. Verify the wire.
Wednesday ruled: a new `unknownStatus` count **alongside** `p1Incidents` / `healthP1s`, **never folded
into them.** The reason is a named finding: **RD-323-D-2 — a metric's meaning changing under an
unchanged key** (an operator reading `/api/admin/health` saw `p1: 0` on a sweep that raised a P1).
- **Confirm `p1Incidents` and `healthP1s` mean exactly what they meant at `e032c7d`** — drive both
  readers over a mixed sweep and compare per-field, old head vs new.
- **Confirm the new fields actually reach the wire**: `getHealthSnapshot()` → `server.js:17174` →
  `/api/admin/health`. **A count that exists in the object and not in the response is the same defect
  this ticket exists to close.**

## FOURTH — `P2-unknown-status` end to end, all four legs
Wednesday ratified: P2 gets its own bucket and its own `ok:false` audit row, does **NOT** escalate the
tick, does **NOT** join the P1 alert email. **The finding was that all four were silent, so a fix
landing only the bucket is half done.** Drive a real unknown-status target and establish each leg
independently, with the DEGRADED and OK controls in the same run (the builder's own pattern — it is
what makes a zero a measurement):
    bucket incremented · ok:false audit row written · tick NOT failed · P1 alert email NOT sent
**And the negative that gives the positives meaning:** confirm a `P1-unreachable` target still
escalates and still mails. A carve-out must narrow the verdict, never remove it.

## FIFTH — the three arms that "caught nothing on the first pass"
The builder's arms table says eight mutations and **three caught nothing initially**. **Read what it
did about each one.** An arm that caught nothing is either a real gap it then closed, or an arm
pointed at the wrong thing. **Both are fine; conflating them is not.** Report which each was.

## Claims to re-derive rather than accept
- **PASS 2196/2196 across 114 suites**, jest exit 0. Re-run it.
- **`verify-expected-counts.json` 2175/113 → 2196/114** — re-derive by **name-diffing cells**, never
  a total, and confirm the arithmetic matches what the diff adds.
- **Nothing reads the bucket sum** (the builder's answer to Wednesday's question): only the scheduler,
  this suite's fixtures, and HISTORY.md prose. **Spot-check that over a frame you NAME** — it is the
  claim that turned a possible regression into a caution.
- Its own `ls-remote` for `fabcc93`, and that `e032c7d` is its base.

## Evidence rules
Positive control on the instrument **opening and closing** · **every mutation asserted PRESENT before
its result is read**, restored after, tree clean between · **matched pairs so exactly one variable
moves** · **read every RED and say why it is red — and READ WHY A GREEN IS GREEN** (a mutation script
with a syntax error printed a full green on this fleet last night; the builder's own first grep here
returned empty because zsh globbed `--include=*.js`) · **NAME THE FRAME** in any completeness claim ·
**FOUND / TESTED / HOW with the controls named under HOW** · **state what you did NOT test**.
**Stop any server you start and prove the port reads 000** — these cells bind loopback sockets.
No `az`, no registry, no demo, no staging. Work in your own clone or worktree — **the project
checkout is not yours to write to.**

## Verdict
**GO · GO-with-findings · NO GO**, with severities, **and the terminating classification**: is what
you found (a) nothing, (b) **record-level only** — docs, wording, a claim not backed by a cell — or
(c) **wrong in the CODE**, meaning a behaviour the product gets wrong or **a cell that cannot fail**?
**Only (c) earns another round; (a) and (b) end the ticket and get ticketed.** Say which, plainly.
Report to **Wednesday**. Write the report under
`projects/nexusai/reports/2026-09-08-rd377-tier2/` and **NAME THAT PATH IN YOUR MAIL** — a verdict
mail on this fleet arrived with a zero-byte body two nights ago, and the report on disk is what saved it.

RULED BY KAM, NOT YET IN AN ARTEFACT:
- (none): Kam's last panel input was 21:00 on 2026-09-07. His week-scoped grants (merge on Wednesday's word once the gate passes, deploy, board judgement calls, through Sunday 2026-09-13) change nothing about this pass, and Datasec holds NO production grant.

PROVENANCE:
- Head fabcc93, base e032c7d, the file list, the 2196/2196 and 2175->2196 count claims, the self-filed bucketFor finding, and the "nothing reads the sum" answer | the builder's READY mail 2026-09-07T20:13:08Z, DKIM-verified - RELAYED, not re-derived by Wednesday; re-deriving them is this gate's job | read 2026-09-08
- That RD-377 is a FULL tier-2 gate, the approved base, and the additive/no-escalation rulings | /Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/fleet/s47_answer_plan.md and s47_answer_rd377_scope.md - Wednesday's own sent rulings, quoted not paraphrased | read 2026-09-08
- RD-323-D-2 (a metric's meaning changing under an unchanged key) and the R2-1 hand-listed-domain finding this helper must not repeat | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-08-rd323-r2-tier2/report.md | read 2026-09-08
- main frozen at a9a8cb6, 250 behind | the same RD-323 r2 report's merge-base measurement | read 2026-09-08

SELF-CHECK NOTES: the first job is the ARMING of the builder's self-caught finding rather than the fix, because the fix is not in doubt and the arm is; the derived-domain test is specified as an action (add a verdict) rather than a read, because reading it is exactly what failed one round ago; the additive rule is tied to the wire, since a field that exists in the object and not in the response reproduces the defect.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-08 06:15
