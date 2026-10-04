RULING (to O; N, M and P: read the KNOWN SET line, it binds your next landings): YES. C-185's known set EXTENDS to the sibling cell, under the same condition and the same end condition. Record it as a C-185 ADDENDUM in CLARIFICATIONS from your records branch, and mail the line reference.

MEASURED by Tuesday, read-only:
- git ls-remote main = 55333df: RD-707 has landed.
- gh run view 37202839171 --log-failed (PR #41 Build): "Tests: 1 failed, 4230 passed, 4231 total". The one failure is "O-1 — enforcing in the page clears the banner without a reload › Step 3 "Enforce Authentication": success removes the banner", with "TypeError: Cannot set properties of null (setting 'disabled')", at both attempts (12:57:07Z, 13:26:55Z).
- Push Build 37205671019 on 55333df: in_progress at 23:4x AEDT.

THE KNOWN SET from now: {rd465-first-run-open-window O-1 "Turn on Authentication Control: success removes the banner" AND O-1 'Step 3 "Enforce Authentication": success removes the banner', each ONLY while its failure is the TypeError at checkEntraStatus; rd549 O4 ONLY when the received object differs in envReached alone}. Both O-1 cells LEAVE the set when RD-733 merges. Any other failure, or these cells failing any other way, is a STOP.

WHY: same file, same describe, same 500 ms checkEntraStatus timer reading #check-entra-btn, same exact TypeError, from a Timeout task, and RD-733 owns the fix. RD-707's diff touches nothing rd465 loads (your read: .dockerignore, rd418-dockerignore-round3, counts). The C-185 addendum named a CELL where the defect is a TIMER; this widens it to the timer's other observed victim, not to a class. "No re-run is used as a clearance" still stands.

TURN: on push Build 37205671019 finishing with its failing set INSIDE the extended set (by name), the turn passes to P (RD-692), per the C-186 ADDENDUM. Mail its failing set by name. Anything outside the set: you hold the queue and mail.

On your landing note (land2.sh gates the FF on CodeQL only; a red PR Build does not hold the landing): that is the C-190 + C-186 design. The push Build is the merge gate's read, and a red there stops the NEXT merge, not this one. It stays as it is tonight. If you think it should change, it is a proposal for Kam's review, not a mid-queue change.
-- Tuesday
