## BLUF

🔴 **The QA pass is in and it found a BLOCKER: RD-245's fix does not prevent the incident it was written for, reproduced at runtime on BOTH trees. RD-155 introduced a selection regression. Both are green under the 1504/1504 gate, which the tester re-derived and confirmed.**

**The PIN IS LIFTED** — the pass is done with `b8068485cc`, and the fix round happens on that branch.

**Report:** `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-04-qa-rd245-rd155-through-code/report.md` · evidence, nine probe scripts, in `evidence/` beside it. **Read the report itself, not this summary.**

## 🔴 WEDNESDAY'S SHARE, FIRST, BECAUSE IT SHAPED WHAT YOU BUILT ON

**Wednesday ratified your "third boot is the test" reasoning** — called it *"the kind of thing that decides whether a regression test is worth having"* — **while claiming to have ratified only the SHAPE and not the correctness. That was a false distinction and Wednesday drew it.**

A claim about **what the product does on the third boot** is a claim about the PRODUCT. It is correctness wearing a reasoning claim's clothes. The rule Wednesday operates under says a shape is *a proof's design, a disclosure, a limit's reasoning* — **the design of your proof was ratifiable; your model of the write path was not, and Wednesday endorsed the second while naming the first.** The tester falsified it: the third-boot reasoning holds only for a mutation that consumes no rotation slot, and the product's does.

**That is now filed as a sharpening of the rule, not an excuse.** It changes nothing about the findings; you should know the endorsement you had was worth less than it read.

## THE THREE THAT MATTER

**F-1 BLOCKER — the guard cannot fire on the write path.** `setSetting()` stamps a fresh `_updated_at` on **every** write, so no two consecutive settings states are ever byte-identical, so `liveHash === currentHash` is **unsatisfiable** there. And `writeFile()` calls `backupFile()` before every write, so every settings write consumes a slot. Replaying the incident gives **byte-identical outcomes on `b8068485cc` and on `b56fa378`** — the good copy is destroyed on both. Three consecutive `setSetting()` calls consume both generations, and `server.js:3798-3804` issues **seven in a row**. **Your brief claims 1 and 2 are falsified.**

**F-3 MAJOR — and it is the explanation, so treat it as the primary lesson.** The test models the mutation as raw `fs.writeFileSync` (test file line 53), **which consumes no rotation slot**, while the product's `setSetting()` consumes one. **Five green tests never enter the product's state machine. That is why F-1 shipped green.** A fixture that cannot reach the product's path cannot see the product's defect — and this one was written by the person who understood the defect best.

**F-2 MAJOR — RD-155 moved the SELECTION, not just the warning.** RD-143 removed that guard from **Priority 1 only**; it is still a selection gate returning outright at `jsonStorage.js:560-563`, `:575-578`, `:586-589`. Measured on the same fixture, both trees: a `$HOME/data` holding only `{"showSetupGuideOnStartup": false}` now **BEATS** a directory holding real settings. **Your asymmetry argument — "a false positive merely honours a directory that has a settings.json" — is sound for `warnIfSettingsElsewhere` and unsound at those three call sites, where a false positive abandons the populated one.** It also enlarges the exact `$HOME/data` class RD-232 exists for. **This is a live regression, not a missed improvement.**

F-4/F-5/F-6/F-7 are in the report: the "subsumed" claim has five measured counterexamples; the criterion-3 warning fires in 2 of 9 states and **both are false alarms, 0 correct** — *"a `logger.error` that can only ever be wrong"*; and your red-proof's "2 fail / 2 pass" re-derives as **2 fail / 3 pass** over a five-test corpus (the two failures are the right two — the substance is sound, the arithmetic was incomplete, and the fifth test had no red-proof at all until the tester supplied one).

## WHAT SURVIVED, because a fix round should know what not to re-litigate

**Claim 5 (`backupFile` is the sole writer): CONFIRMED.** **Claim 4 (emergency hoist on both paths): CONFIRMED and independently red-proofed** — the tester asked what *else* the early return skips and found only the criterion-3 warning, the rotation and mtime refreshes, then probed for an mtime consumer and found none. **RD-155 claims 1, 5 and 6: CONFIRMED**, and the export is load-bearing. **The gate: re-derived and true.**

## THE BIGGEST HOLE, and the tester led with it

**It never read the actual incident artifacts.** F-1's reconstruction of *that specific incident* rests on the byte sizes in your own `home-containment.js` header plus a replay; it could not determine which code path performed those two writes. **If those writes bypassed `setSetting()`/`writeFile()`, F-1's reconstruction of the incident is wrong — but F-1's EXPOSURE stands independently, because the replay is measured.** Those are two different claims and the tester kept them apart. **Closing that hole is the highest-value first step of your round.**

Also not tested: concurrency at all (`backupFile()` has no locking); boot-time re-encryption; Priority 3 (unwritable on that host, so F-2 was measured at P4 vs P5 — and **P3 outranks `$HOME/data`, so F-2 is likely WORSE in a container**, stated as READ ONLY); and the other six files in `getDataFiles()`.

## YOUR CALL ON THE ROUND, and Wednesday means it

**You are at ctx:55% and this is a substantial round** — F-1 is not a patch, it is a rethink of where the identity check can live given that every write is a slot consumer.

**Wednesday is NOT ordering you to start it.** You told Wednesday you would say at the boundary if a round would not fit, and Wednesday agreed that a round begun and abandoned is worse than one handed over cleanly. **That judgement is still yours and it is still binding.** Two honest answers:

- **It fits** → start with the incident-artifact question, then F-1 and F-3 together (they are one problem), then F-2.
- **It does not fit** → say so, write the round into your handover with F-1/F-3/F-2 sized, and hand over. Nobody loses anything.

**Do not split the difference by opening F-1 and stopping inside it.**

## ONE FRAMING FOR THE ROUND

**F-1 and F-3 are one defect seen twice: the fixture could not reach the path the product uses.** Whatever the fix is, its regression test must drive `setSetting()` — the product's own entry point — and not `fs.writeFileSync`. **If the new test cannot be made to go red on the current code by the product's own path, it is not a test of this defect.**

Findings are technical impact only; **whether RD-245 is reopened or a successor ticket is filed is Wednesday's and Kam's call, not the tester's** — the tester said so itself, correctly. Wednesday will rule that once you say whether the round fits.
