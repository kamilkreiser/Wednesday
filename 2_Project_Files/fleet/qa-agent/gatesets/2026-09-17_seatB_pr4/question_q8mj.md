auth: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat B

CONTEXT
PR-4 (qs) is built with develop 3961c2add merged in, at c93d84c9b in WT1. NOT pushed.
- Re-measure at the merged head: 29/29 locks bad 0; qs >= 6.16.0 in all 29 carriers; mysql2 3.23.1 and vitest >= 4.1.11 preserved; suites 24/25 (anchoring = KS-562); clean-room 35/35.
- Merge-in: the baseline conflict was resolved as develop minus GHSA-4mjr + GHSA-x5fp. Root and originate were regenerated from develop's blobs in the container on npm 11.19.0 (verified at runtime; host is 11.5.1), and both are byte-identical to the automerge.

Its gates surfaced a THIRD row the same bump fixes: GHSA-q8mj-m7cp-5q26 (qs, moderate). Its row ticket field is "KS-531 (owner of the express 4 → 5 call: KS-775)"; expires 2026-11-11.
- Advisory DB (authorised read c): qs `>= 6.11.1, <= 6.15.1`, patched 6.15.2. PR-4 moves every qs to 6.16.0.
- At develop 3961c2add it is in 26 standalone locks. The root was never in range; audit-gate never reported it.
- On PR-4's head, with the baseline as built (27 rows), audit-locks prints "CLEANUP — 1 baseline entry is no longer reported … GHSA-q8mj-m7cp-5q26".
- Removing it as well (27 -> 26):
  - fix: audit-locks rc 0, audit-gate rc 0 (26 reported / 26 baselined), 0 CLEANUP.
  - negative control (WT2 = develop, baseline minus all 3): audit-locks rc 1, naming GHSA-q8mj "in 26 lock(s)" plus the two qs rows "in 28 lock(s)".
- The row's own reason says "Moving the remaining 26 requires express 5". That is now false for this advisory: express 4.22.3 declares qs `~6.16.0`.
- KS-531 is Done/archived (it takes no comment). KS-775 is the express 5 decision your ruling keeps untouched except one exact-sentence comment.

QUESTION
Does GHSA-q8mj's row come out in PR-4 too?

DEFAULT (applied unless you say otherwise)
Yes, by the brief's per-PR rule ("remove a row only in the PR whose merge makes the advisory absent from EVERY lock"), the same shape as GHSA-3f6p on #1033:
- baseline 29 -> 26 on develop 3961c2add; conservation asserted.
- The PR body names all three rows. It states in one line that q8mj's "requires express 5" premise is measured false, and that the express 5 migration ruled 2026-09-03 is unchanged.
- The KS-775 comment stays exactly your sentence, ONE comment, no other change to KS-775.
- The q8mj facts go in the KS-763 comment (KS-531 is archived).

MEANWHILE
Holding the commit of that row and the push until your ANSWER. Drafting the PR body and comments. If the answer is "keep it", I push with 27 rows and GHSA-q8mj under CLEANUP (non-failing), and name that in the READY.

NEEDED-BY
Before PR-4's push. The row lapses nothing: it expires 2026-11-11.

Seat B

