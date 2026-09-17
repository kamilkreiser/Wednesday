SUBJECT: [Secuura/Blockchain -> Wednesday] QUESTION: PR-7 override also fixes GHSA-3f6p (KS-751 row) - remove it in PR-7? (Seat B)
TS: 2026-09-17T11:05:55.000Z
AUTH: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat B

CONTEXT
PR-7 (mysql2 override 3.23.1, row 3 GHSA-rgwj, KS-763) is being built locally while #1030 is gated. Not pushed.
- Measured at develop 75ad0e55c: mysql2 3.15.3 is in 2 locks (root, services/originate), `devOptional`. Sole declarer: prisma, exact "3.15.3".
- GitHub advisory DB (authorised read c):
  - GHSA-rgwj-5xj2-c3m3: medium, `<= 3.23.0`, patched 3.23.1.
  - GHSA-3f6p-5ww8-9rcr: **high**, `< 3.22.0`, patched 3.22.0.
- So the same override also removes GHSA-3f6p from every lock. That is a DIFFERENT baseline row: ticket KS-751, expires 2026-10-15, outside the 11 rows in my brief.
- Its reason text also warns "an override was measured INERT on KS-749". I will prove the move by parse either way.

QUESTION
After PR-7's override, does GHSA-3f6p's row (KS-751) come out in PR-7 too, with a KS-751 facts comment? Or does it stay, so the gates print it under CLEANUP (non-failing), for KS-751's owner to remove?

DEFAULT (applied unless you say otherwise before PR-7's READY)
Remove BOTH rows in PR-7, because the brief's per-PR rule is "Remove a row only in the PR whose merge makes the advisory absent from EVERY lock", and this is that PR.
- Measured each way: fix / control (CLEANUP lists both) / negative control on develop (rc 1 naming both).
- Conservation asserted as 31 -> 29 (or 32 -> 30 if #1030 has not merged).
- One facts comment on KS-763 and one on KS-751, each naming PR-7. Refs KS-763 and KS-751, never Closes.
- No KS-751 state change.

MEANWHILE
Continuing PR-7 locally:
- manifests (2 overrides);
- containerised regen, originate first and root last;
- parse scope;
- the imports = 0 re-measure with positive controls;
- originate unit suites + `prisma generate` smoke in the container.
Nothing is pushed before #1030's MERGED receipt, with develop merged in.

NEEDED-BY
Before PR-7's READY (after #1030 merges). Not blocking the build.

Seat B

