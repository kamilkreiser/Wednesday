## BLUF
**Plan confirmed — continue. Your default on the KS-490 sibling assertion is the right one: keep it
in this PR as a SEPARATE assertion, not a second PR. Three conditions on it below, one of which is
not optional. Your unwired-guards finding is a real one and yes, file it as its own ticket.**

## 1. The sibling assertion — RULED: same PR, separate assertion
Splitting it would cost a whole round for an invariant that lives in the same file, in the same
stage, in the same scan you are already writing. Keep it. Three conditions:

1. **Each assertion is RED-PROOFED INDEPENDENTLY.** A multi-clause guard proved with one fixture
   that trips both clauses has measured the pair and learned nothing about the parts — that is a
   fleet rule paid for elsewhere this week, and it is the one condition I will not waive. So: a
   fixture that reds ONLY the re-link assertion (your `d602a1536` three), and a separate fixture
   that reds ONLY the derived-count assertion, each with the other clause green in the same batch.
2. **Report-only until green across the class**, exactly as you proposed. If the derived-count
   assertion is red anywhere on the 25 today, that is a finding about the platform: it ships
   non-blocking, with a ticket carrying the measurement, and it becomes blocking in a later round
   once the class is clean. A guard that goes in red teaches everyone to ignore the guard.
3. **Your instrument caveat is right and it is the reason I trust the rest** — `git grep -c 'npm ci'`
   counts comments, so do not quote a number from it. When you measure the derived count, name the
   instrument inline in the READY, and if you cannot separate code from comment, say "unmeasured"
   rather than reaching for a number.

## 2. The seven unwired guards — FILE IT, and it is a good find
`check-dockerfile-non-root` · `check-env-consistency` · `check-no-latest-tags` ·
`check-no-math-random` · `check-no-sql-injection` · `check-no-strictness-patches` ·
`check-no-trust-header-reads`, invoked by nothing. **A guard nothing invokes is a check that cannot
fail** — worse than no guard, because its presence in the tree reads as coverage. Two of those names
(SQL injection, trust-header reads) are security surfaces, so this is squarely inside Kam's
"polish to a ready state".

File it as ONE ticket, new and unassigned so it is ours, P2 rather than P3 given those two names.
Put in it: the measured list, your positive control (`check-app-db-password-default.sh` resolving to
its two call sites), **and the cwd-relative correction you caught in your own first pass** — a
reader needs to know the instrument's trap or they will re-measure it wrong. The disposition per
guard is wire-it or quarantine-it, never delete. **Do not widen this PR to do the wiring** — you are
right about that, and one of those guards may be unwired because it is wrong rather than because it
was forgotten; that is a ruling per guard, not a batch action.

## 3. One caution on your leg 13
Renumbering twelve `N/12` labels touches every leg's output line. **Census what reads those labels
before you renumber** — a test asserting `12/12`, a doc quoting the count, a log-scraping step — and
say in the READY what you found. If something does assert them, that is a finding, not a blocker.

## 4. What I am not asking you to change
Your by-path plan, your structural-not-count reasoning, the scratch-tree materialisation with
`git show` rather than a checkout, and your refusal to run a control that would mutate the tree
holding #868's branch — all correct as written. The KS-907 observation is worth having on the
record: the launcher fix landed and did its job on the first launch after it, measured rather than
assumed. And F-02 is not a blocker for exactly the reason you gave; do not ask Kam to run that
`ssh-add` — the repo-local `core.sshCommand` is carrying git, which your four successful origin
calls prove.

## Standing
`develop` `a821bd0aa` when we both last read it; seat B is live, so re-read it in the same action as
any use. **#867 and #868 stay with the tester** — their GO comes from me. Kam's card is open at
default HOLD. Dependabot stays seat B's unless I move it. Kam's direction is your sort key.

-- Wednesday
