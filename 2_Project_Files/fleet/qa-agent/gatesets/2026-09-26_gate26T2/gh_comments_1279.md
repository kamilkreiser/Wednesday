--- comment 5839166344 by linear[bot] at 2026-09-25T20:32:17Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1306/ks-980-n-1-the-role-attribute-cell-reads-rolbypassrls-only-so-a">KS-1306 KS-980 N-1: the role-attribute cell reads rolbypassrls only, so a superuser on the admin path is not caught by it</a></summary>
<p>

Raised as a non-blocking finding by the review of PR #1242 (merged as `33ccff807eb2`), recorded so it is not lost.

**What it is.** The role-attribute cell in `ks597-issuer-organization-id.integration.test.ts` asserts on `rolbypassrls` alone. A Postgres **superuser** bypasses RLS regardless of `rolbypassrls`, so a superuser connection on the admin path satisfies this cell while still being exactly the thing the cell reads as "not permitted to bypass".

**Why it is non-blocking.** That case is caught by the GUC cell, not by this one, so the path is covered — but by a different cell than a reader of this one would assume.

**What a fix looks like.** Either assert `rolsuper` alongside `rolbypassrls`, or state in the cell why `rolsuper` is out of its scope and name the cell that does cover it.

Refs KS-980
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1306-assert-rolsuper-alongside-rolbypassrls-on-both-dsns-d43d781675ca">Review in Linear</a></p>

