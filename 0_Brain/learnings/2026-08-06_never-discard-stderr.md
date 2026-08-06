---
date: 2026-08-06
type: correction
source: "w=2 same day: (1) close_wednesday.sh sent python stderr to /dev/null, making the 23:00 inbox failure's root cause unrecoverable — I fixed it in the morning; (2) hours later I WROTE adopt_scoped_identity.sh with `az login … 2>/dev/null`, so Kam got 'LOGIN FAILED (rc=1)' with no reason. The real cause was a 10-second Azure AD secret-propagation delay"
status: live
supersedes: ""
---

# Never discard stderr — a failure you can't diagnose costs more than it saves

**The rule:** no script I write sends error output to `/dev/null`. Errors go to
a log, to the console, or into a variable that gets printed on failure. Quieting
stderr to keep output tidy trades a few clean lines for an undiagnosable failure
later — and the failure always lands on someone else.

**Why this is w=2 on the same day, which is the embarrassing part:** I fixed
exactly this defect in `close_wednesday.sh` in the morning (its inbox check
discarded python's stderr, so the 23:00 "unreachable" had no recoverable root
cause). Hours later I *wrote a new script with the same bug*. The morning's fix
was applied to the instance, not adopted as a class.

**Diagnosis — why the fix didn't generalise:** I treated it as "repair this
script" rather than "this is how I write scripts". A fix stays local unless it
is turned into a rule at the moment of the fix. That is the same shape as the
retro-candidate failure ([[2026-08-04_gitignore-artifacts-at-creation]]): the
lesson exists only where it is written down as a rule.

**How to apply:**
1. Writing any script: stderr goes somewhere a human can read it. If a command
   is expected to fail benignly, capture stderr and branch on its *content*
   (`case "$ERR" in *AADSTS7000215*)`), never silence it.
2. Failure messages state what failed, the actual error, and what to do next —
   "LOGIN FAILED (rc=1)" is a dead end; "not propagated yet, retrying" is not.
3. **Corollary learned in the same incident: distinguish "failed" from "not
   ready yet".** Cloud resources are eventually consistent — a freshly created
   Azure AD client secret took 10 seconds to become usable (measured: failures
   at 0s and 5s, success at 10s). New identity, new DNS record, new role
   assignment: retry with backoff before declaring failure.
4. When a fix like this lands, ask once: *is this a bug in this file, or in how
   I write files?* If the latter, write the rule immediately.

**Related:** [[_ledger]], [[2026-08-06_exercise-mechanisms-before-arming]],
[[2026-08-04_gitignore-artifacts-at-creation]]
