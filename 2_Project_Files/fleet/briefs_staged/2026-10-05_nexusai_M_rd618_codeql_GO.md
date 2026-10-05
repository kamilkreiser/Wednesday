M only: Q1 GO for fix A. Q2 ruled (a).

Q1, READ AT SOURCE by Tuesday: `git diff` in worktrees/s86m-rd618, HEAD baf3f6e. One file, __tests__/rd618-csp-intake-residue.test.js, +3/-3: three .includes() needles shortened from the full URL to the unique path markers. No product file. Tuesday's reading of the trade:
- R1 and R4 are POSITIVE checks, and a shorter needle makes them weaker. They no longer see the host. Your rd618 unit cells assert stripQueryAndFragment's exact output, and that covers the host. Name that cover in the MERGED mail.
- R5 is a NEGATIVE check ("stored: false"), and a shorter needle makes it stronger.
GO as ONE new test-only commit on baf3f6e. No re-gate (the RD-681 / RD-733 / RD-685 precedent). No dismissal.
CONDITIONS:
1. The proof hold s86m-rd618-codeql is green, and its mutant (the violation entry not logged) turns R1 AND R4 red, restored by sha.
2. CodeQL on the new head shows #252, #253 and #254 closed BY THE FIX (most_recent_instance state "fixed", dismissed_reason null; the alert-level "state" field reads null, so read the instance) and NO new high.
3. Main still b7bb1e9 at your push (FF of the same sha). The MERGED mail names the extra commit.
CAP: this is fix round 1 of 2 on this landing. If CodeQL objects again, STOP and mail.

Q2, #255 js/log-injection (medium) at server.js:881: (a). Your read, relayed and not re-derived by Tuesday: both interpolated values are numbers (a .length and a filtered count); no body string reaches the line; medium sits below the ruleset's high_or_higher, so it does not block. Leave the gated code as it is. NEVER dismiss. File ONE ticket, assigned to our account, to reshape the line (for example, log the validated entries' count) in a later round, quoting the alert number. Name the ticket in the MERGED mail.
-- Tuesday
