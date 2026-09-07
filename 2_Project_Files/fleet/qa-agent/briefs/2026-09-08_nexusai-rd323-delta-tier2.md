# QA GATE — Datasec/NexusAI **RD-323 DELTA** `rd-323-scheduler-failure-vocabulary-s45` @ `1b6bedb`. **TIER 2.**

## Why this gate exists — read this first, it is the whole reason
**RD-323 has a GO-with-findings, and it is on `99fb518`. The head is now `1b6bedb`.**
The fix for that gate's own Major (**RD-323-F-1**) was landed **WITH** the change on Wednesday's
instruction, so **no verdict currently describes what would ship.** That staleness is Wednesday's to
carry, not the builder's — it did exactly what it was told and said so in the same breath
(*"head MOVED off your GO (99fb518), re-queue the delta"*).

**Your subject is the DELTA ONLY: `99fb518..1b6bedb`.** One commit, three files, 108 insertions.
Everything under `99fb518` already has its verdict; do not re-gate it.

    99fb518   the GO-with-findings head       — already gated, NOT your subject
    1b6bedb   rd-323-scheduler-failure-...    — THE SUBJECT
    NOT main — frozen, RD-367, ~251 behind. Nothing merged, nothing deployed. **You may not merge.**

**Round 1 of this class.** The two-NO-GO cap is not near; judge it on its merits.
Through-code only — no browser surface in this change.

## What the delta is
`RD-323-F-1: healthSweeper's p1 counted P1-degraded, so the code did the opposite of the comment
four lines above it.`

    backend/services/schedulers/healthSweeperScheduler.js   +27 -7
    __tests__/scheduler-failure-vocabulary.test.js          +84 -1
    scripts/verify-expected-counts.json                     2171 -> 2173

The one-line mechanism: `p1` was `p1s.length`, and `p1s` filters `verdict.startsWith('P1')`, which
**includes `P1-degraded`** — so `p1 >= degraded` **always**, and `_failed()` failed the tick on a
target that merely answered DEGRADED, four lines below its own comment promising the opposite. The fix
is `const escalated = p1s.filter(r => r.verdict !== 'P1-degraded')`.

## 🔴 THE THREE THINGS THAT ACTUALLY DECIDE THIS GATE

### 1. THE FRAME — and it is the highest-value check here
The commit says **`p1` is read in exactly two places (this `_failed` and the suite), so the change is
contained; checked rather than assumed.** That is a **completeness claim with no frame on it**, and it
is the claim the whole change rests on. **Re-derive it yourself and NAME THE FRAME you derived it
over.** `result.p1`, the destructured `p1`, and the object's `p1` key travel under different spellings
— a grep for one finds a fraction. Look specifically at: the health snapshot / `getHealthSnapshot`,
the alert-email path, any API or dashboard surface that renders a sweep result, any persisted audit
or metrics row, and the frontend. **A reader outside `backend/` is exactly the shape this fleet has
been caught by three times this week.**

### 2. THE CARVE-OUT IS A STRING EQUALITY — enumerate every verdict the class can emit
`escalated` excludes **exactly one literal**, `'P1-degraded'`. **Enumerate every `P1-*` verdict
`runOnce` can produce** (read the class, do not infer from the tests) and confirm that (a) each one
that SHOULD escalate still does, and (b) `P1-degraded` is spelled identically at the producing site
and the filtering site. **A one-string carve-out is correct only over an enumerated vocabulary**, and
the builder did not enumerate it in the mail.

### 3. THE SECOND HALF OF THE CLAIM IS UNTESTED — check whether that is true
The docblock and the commit both promise: *"a degraded target STILL gets its own `ok:false`
`p1-detected` audit row **and still triggers the alert email** — only the tick verdict changes."*
The new cell asserts the **audit row** (`p1Rows` length 1, `ok:false`, summary matches `P1-degraded`).
**Wednesday read the test and could not find an assertion for the alert email.** Establish whether one
exists anywhere; if it does not, that is a **claim in a docblock with no cell behind it** — say so with
its severity. Do not take Wednesday's reading as the finding: **re-read it and report what you find,
including that Wednesday was wrong if Wednesday was wrong.**

## What is GOOD here, so you calibrate rather than hunt
The builder did the strong thing rather than the asked-for thing, and it is worth verifying it holds:
**it stopped writing a shape at all.** Told to *"rewrite the assertion against a shape `runOnce`
actually emits"*, it instead **drives the real `runOnce` against a real local stub** and feeds whatever
comes out into the **real `_failed`**. Its words:

> *"A hand-written shape cannot notice it is impossible; a driven one cannot be written for a state the
> product cannot reach."*

It also added a **negative control** — an unreachable target, same instrument, opposite answer —
because *"without this the fix is satisfiable by 'never fail': the carve-out must narrow the verdict,
not remove it."* **Verify both cells genuinely drive the product** (no stub of the class, no
re-implemented logic) and that the control **can** fail — mutate the fix and confirm the control
reddens for the intended reason.

## The removed arm — a deletion inside a test file, so check it honestly
The old cell's fifth arm, `expect(f({ probed:1, healthy:0, degraded:1, unreachable:0, p1:0 })).toBe(false)`,
was **deleted**. The builder's stated reason is that it asserted a state the product cannot reach.
**Confirm that reasoning against the code at `99fb518`** rather than accepting it, and confirm the new
driven cell covers what the deleted arm was there to protect. Counts: **2171 → 2173** — re-derive by
**name-diffing cells**, never by trusting the total, and confirm the arithmetic (one arm removed from
an existing cell, two whole cells added) matches what the diff actually does.

## Smaller things, stated so they are not mistaken for the main event
- The control test **binds a port, reads it, closes it, then probes it** to get a guaranteed-dead
  address. That is a race with anything else on the machine. Judge whether it matters here.
- `HEALTH_SWEEP_URLS` is saved and restored in `finally` in both cells. Confirm no other process-wide
  state is left mutated, and that the suite passes in a **different cell order** if you can force one.
- `verify-expected-counts.json` is the CI gate's own expectation. Its `_updated` moved and `tests`
  rose by 2. Confirm it was regenerated rather than hand-edited to match.

## Evidence rules
Positive control on the instrument **opening and closing** · **every mutation asserted PRESENT before
its result is read**, restored after, tree clean between · **matched pairs so exactly one variable
moves** · **read every RED and say why it is red** — a parse error, a throw, or a pre-existing
condition answering first is **not** a detection · **NAME THE FRAME** in any completeness claim ·
**FOUND / TESTED / HOW with the controls named under HOW** · **state what you did NOT test**.
Counts re-derived by **name-diffing cells**, never a total.
**Stop any server you start and prove the port reads 000** — this change starts two.
No `az`, no registry, no demo, no staging. Work in your own clone or worktree.

## Verdict
**GO · GO-with-findings · NO GO**, with severities. A guard that is real but narrow is
**GO-with-findings** — say so rather than failing it for a **stated** limit. A docblock promise with no
cell behind it is a finding against the RECORD, and this fleet has learned to rate those on what the
next reader would do with them, not on whether the code works today.
Report to **Wednesday**. Write the report under
`projects/nexusai/reports/2026-09-08-rd323-delta-tier2/` and **NAME THAT PATH IN YOUR MAIL** — a verdict
mail on this fleet arrived with a zero-byte body last night, and the report on disk is what saved it.

RULED BY KAM, NOT YET IN AN ARTEFACT:
- (none for this gate) — no Kam ruling since 21:00 2026-09-07 bears on RD-323. His week-scoped grants (merge on Wednesday's word once the gate passes, deploy, board judgement calls, through Sunday 2026-09-13) are already in the standing lines below and change nothing about this pass.

PROVENANCE:
- Head 1b6bedb at refs/heads/rd-323-scheduler-failure-vocabulary-s45, and the GO's head 99fb518 | `git -C /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files rev-parse` over a fetch S46 took at 00:10, read by Wednesday - Wednesday's read of a fetch it did not run; re-derive with your own ls-remote | read 2026-09-08
- The diff, the 108 insertions, the three files, the deleted arm, and the absent alert-email assertion | `git -C /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files diff 99fb518..1b6bedb` read by Wednesday in the same action as writing this brief | read 2026-09-08
- RD-323-F-1 as a Major, and that the GO-with-findings was taken on 99fb518 | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-07-rd322-rd323-tier2/report.md - the previous gate's own report, not re-derived by Wednesday | read 2026-09-08
- The builder's reasoning and its two quoted sentences | the builder's mail 2026-09-07T14:08:37Z, DKIM-verified - relayed, not re-measured by Wednesday | read 2026-09-08

SELF-CHECK: re-read end-to-end for contradictions; the delta is the subject and 99fb518 is not; every SHA carries the instrument that produced it | 2026-09-08 00:42
