--- comment 5852995230 by linear[bot] at 2026-09-27T05:28:54Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1350/webhooks-fail500-docblock-three-sentences-that-are-stale-or-only-now">KS-1350 webhooks fail500 docblock: three sentences that are stale or only-now-true after KS1341 part C</a></summary>
<p>

**BLUF: the** `fail500` **docblock in** `services/originate/src/routes/webhooks.ts` **(:549-:561) makes three statements that no longer describe the file.** Part C was raised byte-identical to its golden and deliberately did not touch them (Q-DOCBLOCK ruling (a)); this ticket is the follow-up that was owed.

## The three

1. *"KS-1341: the only place in this router that turns a caught error into a 500."* — false after parts A and B, and **true only now** that part C has landed. Worth keeping, but it was asserted before it was true.
2. *"Declared at the END of the file on purpose"* — it sits immediately before `export default webhooksRouter;`, which is the last statement, so "the end" is approximate rather than wrong; reword or drop.
3. *"Seven catch blocks above put the thrown error's own text in the 500 body with NO NODE_ENV guard"* — after part C this describes **history**, not the file. All seven now go through the helper.

## State

All seven sites are on develop as of `f3a93b9fc8f31911a6c99c5345261e8f5aee4087` (#1292, part C), after #1288 (part A) and #1290 (part B). Measured on develop: `message: err.message` x0, `fail500(` x8 — one declaration and seven calls.

Docs only. Refs KS1341.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1350-correct-the-three-stale-sentences-in-the-webhooks-fail500-49545593c738">Review in Linear</a></p>

