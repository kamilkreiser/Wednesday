--- comment 5841784889 by linear[bot] at 2026-09-26T01:04:44Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-766/base-image-watch-self-test-cannot-red-the-db-age-producer-the-f-5">KS-766 base-image-watch self-test cannot red the DB-age PRODUCER — the F-5 clamp can be re-introduced with the suite green</a></summary>
<p>

## BLUF

`base-image-watch.sh`'s self-test can red on the **consumer** of the DB-age value but **not on the producer**. The QA F-5 fix (a future timestamp answers INDETERMINATE instead of printing "0.0h old" inside a CLEARED verdict) is therefore **half-guarded**: reverting `decide()`'s future arm reds the suite; reverting the producer clamp does **not**.

Found and stated while fixing F-5 on PR #793, rather than left as an implied coverage claim.

## Why the producer cannot be red-proved today

`run_case` calls `decide "$tmp/report" "$ref" "$age" 72` — the age is passed **directly as a string**. So every case exercises `decide()` and none of them runs the age-computation block, which is inline `$( python3 -c '...' )` command substitution rather than a callable unit.

Concretely: restoring `print(f"{max(age, 0.0):.2f}")` in the producer leaves the self-test at **20 PASS / 0 FAIL**, while deleting `decide()`'s `if db_age_future:` arm correctly reds the F-5 case.

## The consequence, stated plainly

The producer is the half that turns a real clock-skewed cache into the sentinel. If someone re-introduces the clamp — which is exactly what F-5 was — nothing fails. The gate would go back to printing *"the vulnerability DB is 0.0h old"* immediately before telling an operator to run the ACR leg against the live registry, and the suite would stay green.

## Done means

1. The age computation is extracted into a shell function (or a small script) that the self-test can call with a synthetic `trivy` metadata timestamp.
2. A case pair: a **future** stamp yields the `future` sentinel; a normal stamp yields a numeric age.
3. **Red-proof:** restoring `max(age, 0.0)` reds case 1 and leaves case 2 green.

## Related

PR #793 (the F-5/F-6 fixes and this gap's evidence) · KS-365 (the base-image gate) · the same family as the vacuous-control findings in the sibling guards PR #795 — an assertion that cannot fail on the input it exists to reject.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-766-red-prove-the-base-image-watch-db-age-producer-not-only-its-c285ea4d2339">Review in Linear</a></p>

