# QA GATE — Datasec/NexusAI **RD-376** `rd-376-stripper-reconcile-s47` @ `36191eb`. **TIER 2, FULL PASS.**

## Scope
    36191eb   THE SUBJECT.  Range 10ddb0a..36191eb = ONE commit, TEN files, 199+/46-
    10ddb0a   its base, rd-374-f2-guard-coverage-s46 (a CLOSED lineage; do NOT re-gate it)
    NOT main — frozen at a9a8cb6, 250 behind. Nothing merged, nothing deployed. **You may not merge.**
**Round 1.** Claimed `npm run verify`: **PASS 2191/2191 across 113 suites**. Evidence comment 37287.

## 🔴 WHY THIS IS A FULL PASS THOUGH IT TOUCHES NO PRODUCT CODE
Wednesday measured it: **tests and helpers only, nothing outside `__tests__/`.** Under the standing
tiering that reads as through-code. **Wednesday overrode it deliberately, and the reason is the blast
radius:** this change does not ADD tests — **it replaces the reader that TEN call sites use to see the
code they guard**, and one of them is `auth-gate-fail-closed.test.js`. **If the shared helper is
subtly wrong, ten guards go quietly blind at once**, and that is precisely the defect this ticket
exists to close (the old two-regex stripper made a guard fail OPEN by deleting the text it was
searching). A silent weakening here is invisible by construction.

**STACKED:** `rd-374 @ 10ddb0a` must merge before `rd-376`. Two merges, two blast radii.

## What changed
    __tests__/helpers/strip-comments.js   NEW, 115 lines — the single shared helper
    __tests__/helpers/erasure-write-guard.js       stripCommentsParsed -> delegates
    __tests__/auth-gate-fail-closed.test.js        codeOnly -> delegates
    + seven guard files converted off their own two-regex copies

---

## 🔴 FIRST JOB — behavioural identity per CALL SITE, not in aggregate
A reconciliation's whole risk is that one call site quietly changes behaviour while the suite stays
green. **For each of the ten call sites, establish that the shared helper returns what that site's
previous implementation returned** — or that the difference is intended AND stated in the commit.
**The three prior implementations were not identical to each other** (that is why this ticket exists),
so "they now share one helper" necessarily changed at least two of them. **Which two, and how?**
That question is the gate.
- Do it as A/B on real inputs from the repo, not synthetic strings.
- **Where behaviour changed, say whether the NEW behaviour is the correct one** — do not assume the
  parsed version wins on every axis just because it is parsed.

## SECOND — the X-2 flip, reproduced independently
The builder's table claims the defect is closed:
    BASELINE  no payload            10/10 GREEN  ->  10/10 GREEN
    X-1  L2090, OUTSIDE the spans    1f CAUGHT   ->   1f CAUGHT
    X-2  L1107, INSIDE 1097-2062    10/10 MISSED ->   1f CAUGHT
**Reproduce X-2 yourself**, deriving the spans from the guard's own regex at this commit rather than
inheriting the numbers. Baseline and X-1 must NOT move — that is what makes X-2's flip one variable.

## THIRD — the FRAME, and the builder has already moved it twice
The ticket said nine guards. The builder reports **an eleventh instance the list does not name**, and
that **`import-graph-reader.test.js` must NOT be converted** because its `legacyStrip` is a deliberate
historical stand-in. **Both are frame corrections and both need checking:**
1. **Verify the eleventh exists**, and say whether it is in this commit, ticketed, or neither.
2. **Verify the import-graph exclusion is right** — read what that guard asserts and confirm
   converting it would break the thing it exists to demonstrate. **An exclusion is a claim too.**
3. **Then run your OWN census, over a frame you NAME, by SHAPE not by name** — the two regexes, not
   the word `stripComments`. The last gate on this class found the shape hiding under a different
   name inside another function, and a grep for the helper's name found half of it.

## FOURTH — the builder's own caught error, and whether the amend actually closed it
Its first commit message said both prior implementations *"now delegate to"* the shared helper.
**They did not** — it had converted the seven downstream guards and left the two originals untouched,
which is **requirement 1 of the ticket**. It caught this before push and amended.
**Verify the amend did the reconciliation and not just the sentence:** `stripCommentsParsed()` and
`codeOnly()` must both actually delegate now. **This is the fifth appearance of "a claim with nothing
behind it" in this codebase in 24 hours, and this one was in the commit message closing that very
class** — so read the code, not the message.

## FIFTH — the per-guard red-proof table
Six guards are shown with legacy-vs-new arms. **Spot-check at least two independently**, and note that
`local-date-single-definition` shows a **1f baseline** the builder attributes to its own planted
harness being counted by that guard (it asserts over every harness in `__tests__/`). **Confirm that
explanation** — a baseline red that is waved past invalidates the row, and it says it chased this one.

## Claims to re-derive rather than accept
- **PASS 2191/2191 across 113 suites**, exit 0. **Note the suite count is UNCHANGED** — a 199-line
  change that adds no cells. Confirm that is a refactor and not lost coverage: **name-diff the cells**
  at both heads, never trust a total.
- The base: `codeOnly()` exists on `10ddb0a` **and nowhere else** (the builder's reason for the base).
- Your own `ls-remote` for `36191eb`, and that `10ddb0a` is its base.

## Evidence rules
Positive control **opening and closing** · every mutation **asserted PRESENT before its result is
read**, restored after, tree clean between · matched pairs, one variable · **read every RED and say
why — and READ WHY A GREEN IS GREEN** · **NAME THE FRAME** · **FOUND / TESTED / HOW with controls named
under HOW** · **state what you did NOT test**. Stop any server you start and prove the port reads 000.
No `az`, no registry, no demo, no staging. Work in your own clone — the project checkout is not yours.

## Verdict
**GO · GO-with-findings · NO GO** with severities, **plus the terminating classification**: (a) nothing,
(b) **record-level only**, or (c) **wrong in the CODE** — a behaviour the product gets wrong, or a cell
that cannot fail. **Only (c) earns another round.** Say which, plainly.
Report to **Wednesday**, under `projects/nexusai/reports/2026-09-08-rd376-tier2/`, and **NAME THAT PATH
IN YOUR MAIL.**

RULED BY KAM, NOT YET IN AN ARTEFACT:
- (none): Kam's last panel input was 21:00 on 2026-09-07. Datasec holds NO production grant; nothing merges until his two GitHub answers land.

PROVENANCE:
- Head 36191eb, base 10ddb0a, one commit, ten files, and that NOTHING outside `__tests__/` is touched | `git -C /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files ls-remote origin` / `rev-list --count` / `diff --stat` / `diff --name-only`, run by Wednesday in the same action as writing this brief - read verbs only, no fetch | read 2026-09-08
- The X-1/X-2 table, the per-guard arms, the eleventh instance, the import-graph exclusion, the amended commit message, and the 2191/2191 claim | the builder's READY mail 2026-09-07T20:42:33Z, DKIM-verified - RELAYED, not re-derived by Wednesday; re-deriving is this gate's job | read 2026-09-08
- That the old stripper made a guard fail OPEN, and that a name-grep found half the instances | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-08-rd374-tier2/report.md (G-2c) | read 2026-09-08

SELF-CHECK NOTES: the full-pass override is argued from blast radius with the measurement that shows it is test-only, so Kam can overrule it knowingly; the frame section treats the builder's two corrections as claims to check rather than as facts, including the exclusion; the first job is per-call-site identity because "they now share one helper" necessarily changed at least two implementations.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-08 06:44
