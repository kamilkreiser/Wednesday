--- comment 5835115602 by linear[bot] at 2026-09-25T15:38:39Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-906/case-6s-cd-tmp-is-inert-the-leg-uses-git-c-dollardev-dir-so-the-case">KS-906 CASE 6's `cd /tmp` is inert — the leg uses `git -C "$DEV_DIR"`, so the case does not test what its name says</a></summary>
<p>

## BLUF**CASE 6 of the KS-859 suite changes directory to** `/tmp` **to simulate "outside a work tree", but the leg resolves its root with** `git -C "$DEV_DIR"` **— the process's cwd is irrelevant.** The case passes for a different reason than the one it [documents.It](<http://documents.It>) is not a false green in the dangerous direction: the case still exercises a genuine not-a-work-tree path, because the fixture directory it points `DEV_DIR` at is itself outside any repository. But the mechanism in the cell's name is wrong, and a reader copying it will write an inert precondition.## Fix shapeMake the precondition explicit: assert `$TMPDIR`/the fixture path is outside a work tree (`git -C "$dir" rev-parse` fails) rather than relying on `cd`, and rename the case to say so. Drop the `cd`.Residue of the #858 tier-2 gate (F-QA-04, Polish). Parent: KS-859, merged at `34347a8fafb5feca69d59dcee12b8aca9ce4a69d`.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-906-case6cwd-drop-the-inert-cd-and-pin-that-the-leg-ignores-the-6f119bbf14a7">Review in Linear</a></p>

