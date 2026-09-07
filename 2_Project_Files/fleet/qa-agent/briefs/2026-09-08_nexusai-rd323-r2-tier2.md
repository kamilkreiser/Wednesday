# QA RE-GATE — Datasec/NexusAI **RD-323 DELTA ROUND 2** `rd-323-scheduler-failure-vocabulary-s45` @ `e032c7d`. **TIER 2.**

## Scope — the delta only
    1b6bedb   the round-1 delta head, GO-with-findings tonight   — already gated, NOT your subject
    e032c7d   THE SUBJECT.  Range 1b6bedb..e032c7d = ONE commit, FOUR files, 176+/6-
              __tests__/scheduler-failure-vocabulary.test.js        +122
              backend/services/schedulers/healthSweeperScheduler.js  +32   <- PRODUCT CODE
              docs/automation/scheduled-jobs.md                      +24
              scripts/verify-expected-counts.json                   2173 -> 2175
    NOT main — frozen, RD-367, ~251 behind. Nothing merged, nothing deployed. **You may not merge.**

**Round 2 of this class; round 1 was GO-with-findings, not a NO GO** — the two-NO-GO cap is not
engaged.

**⚠️ THIS ROUND CHANGES PRODUCT CODE, and the previous one did not.** The builder flagged that
unprompted. It is why this is a gate and not a through-code skim.

Round-1 report (the four findings this closes):
`/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-08-rd323-delta-tier2/report.md`

**Verified by Wednesday before this brief** (`ls-remote` from the NexusAI checkout, a read verb):
`rd-374-f2-guard-coverage-s46` `7c10437`, `rd-361-round4-s45` `731aa6e`, `rd-148-round2-s45`
`690bed9`, `rd-322-root-guard-vacuity-s45` `432617a`. **No other branch moved. Confirm it yourself.**

---

## 🔴 FIRST JOB — the builder handed you a mutation table and asked you to check IT rather than the greens
Three mutations, three **distinct** signatures, its own measurement:

    M3  degraded no longer alerts             1 failed   ONLY D-1
    M4  escalates() = "the unreachable set"   1 failed   ONLY D-4
    M5  carve-out removed entirely            3 failed   F-1, D-1, D-4

**M4 is the one that matters.** Under it, **F-1 and its control stay GREEN** — which is the round-1
D-4 finding (*neither cell can distinguish a correct `escalated` filter from one that merely returned
`unreachable`*) **demonstrated by measurement rather than argued**, with D-4's own cell as the only
thing that catches it.

**Reproduce all three mutations yourself and confirm the signatures are DISTINCT.** The claim is not
"three mutations go red" — it is that **each reddens a different, named set**, which is what makes the
cells independent rather than three views of one assertion. **If any two signatures collapse to the
same set, the independence claim fails** and that is the finding. Assert each mutation PRESENT before
reading its result, restore after, tree clean between.

## 🔴 SECOND — the PRODUCT change, which is more than the finding asked for
The inline `p1s.filter(r => r.verdict !== 'P1-degraded')` is now a named static
**`HealthSweeperScheduler.escalates(verdict)`**. The builder's stated reason: asserting the filter
from the suite would mean **re-implementing it**, which is RD-347's defect exactly — *a test helper
that reimplements the product is a mock the moment the product moves.* **Wednesday has ruled the
extraction KEPT** (reasoning in the mail of record). **Your job is not whether to keep it — it is
whether it is CORRECT and whether it changed behaviour it should not have.**

Concretely:
1. **Is `escalates()` behaviourally identical to the inline filter it replaced?** Drive the real class
   over **every verdict `_classify` can emit** and compare old-vs-new decision per verdict. A refactor
   that quietly widens or narrows the escalation set is the whole risk here.
2. **The vocabulary is claimed to be enumerated by DRIVING `_classify`, never hand-listed** — because
   *"a hand-listed vocabulary goes stale the day someone adds a verdict, which is precisely how
   RD-377's gap was created."* **Verify that is what the code does, not what the comment says.** Add a
   new verdict to `_classify` and confirm the assertion picks it up **without the test being edited**.
   Restore after. A hard-coded list here would be the same defect this round exists to close.
3. **`escalates` is now PUBLIC API on the class.** Enumerate its callers over a frame you name.

## THIRD — the D-1 cell's preconditions, and the env-leak the builder raised against itself
The new D-1 cell asserts `liveMode` / `emailService` / `alertEmail` **as preconditions before the
claim** — the thing the F-1 cells could not satisfy. **Confirm the preconditions actually gate the
assertion** (make one false and confirm the cell fails rather than silently passing), and confirm the
clean-sweep arm exists — *"it sends" is satisfied by a scheduler that mails every tick*, so the
negative arm is what gives the positive one meaning.

**The builder raised a risk against itself and tested it:** the D-1 cell swaps `process.env`, and
`health-sweep-urls.test.js` reads the same variables; jest shares a worker across files, so an
imperfect restore leaks between suites. It ran the two together — **26/26, no leak** — plus the full
113-suite run. **Re-run that pairing yourself, and also run them in the OPPOSITE order**, because a
restore bug is order-sensitive and one ordering can hide it. This is the right kind of self-raised
risk; confirm it rather than take it.

## FOURTH — D-2 and D-3, both record-level
- **D-2:** `escalated` is published **alongside** `p1`, not instead of it (renaming would break
  `/api/admin/health` and the persisted rows). `docs/automation/scheduled-jobs.md` carries a dated
  before/after table and the operator sentence: **a sweep can report `p1: 0` having genuinely raised a
  P1.** Confirm the doc matches the code, and that the wire really does carry both fields.
- **D-3:** the missing distinction is now in the test — *a vacuous cell that is WRONG is cover; a
  vacuous cell that is RIGHT is redundancy — only the first is a defect.* Confirm it is in the file.

## The claims to re-derive rather than accept
- **PASS 2175/2175 across 113 suites** (2173 + 2 cells), jest exit 0. Re-run it.
- **`verify-expected-counts.json` 2173 → 2175** — re-derive by **name-diffing cells**, never a total,
  and confirm the arithmetic matches what the diff adds.
- **No other branch moved** — your own `ls-remote`.

## Evidence rules
Positive control on the instrument **opening and closing** · **every mutation asserted PRESENT before
its result is read**, restored after, tree clean between · **matched pairs so exactly one variable
moves** · **read every RED and say why it is red** · **NAME THE FRAME** in any completeness claim ·
**FOUND / TESTED / HOW with the controls named under HOW** · **state what you did NOT test**.
**Stop any server you start and prove the port reads 000** — these cells bind loopback sockets.
No `az`, no registry, no demo, no staging. Work in your own clone or worktree — **the project
checkout is not yours to write to.**

## 🔴 THE TERMINATING CONDITION — Wednesday's ruling, stated up front so this does not regress forever
This is the **third gate in one night on this lineage** (RD-323 → delta → this). Each round has
produced strictly new findings with **zero duplication**, which is why it has been allowed to
continue — Kam's standing criterion is that *"whether the process is working or looping can only be
decided by the outcome."*

**So the outcome decides here, and the rule is set BEFORE the verdict rather than after it:**
- **A clean GO ends the lineage.**
- **A GO-with-findings whose findings are RECORD-LEVEL ONLY (docs, wording, a missing line in a
  docblock) ends the lineage too — those get TICKETED, not fixed in a round 3.**
- **Only a finding that is wrong in the CODE — a behaviour the product gets wrong, or a cell that
  cannot fail — earns another round.**
Say plainly in your verdict which of those three you are returning. **That classification is the most
useful thing you can give Wednesday tonight**, more useful than the findings themselves.

## Verdict
**GO · GO-with-findings · NO GO**, with severities, **plus the terminating classification above**.
A guard real but narrow is **GO-with-findings** — say so rather than failing it for a **stated** limit.
Report to **Wednesday**. Write the report under
`projects/nexusai/reports/2026-09-08-rd323-r2-tier2/` and **NAME THAT PATH IN YOUR MAIL** — a verdict
mail on this fleet arrived with a zero-byte body last night, and the report on disk is what saved it.

RULED BY KAM, NOT YET IN AN ARTEFACT:
- (none for RD-323): Kam's last panel input was 21:00 on 2026-09-07 and nothing since bears on this branch. His week-scoped grants (merge on Wednesday's word once the gate passes, deploy, board judgement calls, through Sunday 2026-09-13) change nothing about this pass, and Datasec holds NO production grant.

PROVENANCE:
- Head e032c7d, the range being exactly one commit, the four-file stat including the product-code file, and that no other branch moved | `git -C /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files ls-remote origin` / `rev-list --count` / `diff --stat`, run by Wednesday in the same action as writing this brief - read verbs only, Wednesday did not fetch | read 2026-09-08
- The M3/M4/M5 mutation table, the escalates() extraction and its RD-347 reasoning, the env-leak pairing result 26/26, and the 2175/2175 claim | the builder's round-2 mail 2026-09-07T15:11:23Z, DKIM-verified - relayed, NOT re-measured by Wednesday; reproducing it is this gate's job | read 2026-09-08
- D-1 through D-4 as round-1 findings with their severities | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-08-rd323-delta-tier2/report.md - the round-1 gate's own report | read 2026-09-08
- Kam's working-or-looping criterion, quoted in the terminating condition | Kam, dashboard panel 2026-09-07 13:27, verbatim in /Volumes/KK_T9_External_HDD/WEDNESDAY/0_Brain/learnings/_ledger.md - Wednesday's own brain, not your tree | read 2026-09-08

SELF-CHECK NOTES: the terminating condition is stated before the verdict rather than invented after it; the product-code change is scoped as "is it correct", not "should it exist", because Wednesday already ruled the latter; the builder's self-raised env-leak is given a stronger test (opposite order) rather than accepted.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-08 01:14
