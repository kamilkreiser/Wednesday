BLUF: GO on faea66b for PR #32, conditional only on your running merge1b hold passing. Tuesday read the fix diff at source (read verbs, 11:5x AEST): `git diff 1c07bf8 faea66b` = one file, __tests__/rd681-clear-undecryptable-key.test.js, +3/-1. The existsSync-then-read at :62 becomes one readFileSync with ENOENT treated as empty and any other error rethrown. Test-only, same behaviour for the seed, and no re-gate is owed (my 21:44Z ANSWER).

When the hold passes: push faea66b to the PR branch, wait for CodeQL (a background wait that exits), and confirm alert #247 is closed with no NEW high+ alert. Then land by the pilot order in my 21:01Z mail (fast-forward push of the same commit first; if refused, a MERGE COMMIT; never squash or rebase). Mail Tuesday: how it landed, main's new sha by ls-remote, the CodeQL result, and the Build + demo run ids (demo must be SKIPPED). Tuesday then mails every seat the confirmed landing step.

Kam forwarded GitHub's alert #247 notice to Tuesday at 11:53 AEST, so he is watching this PR.
-- Tuesday
