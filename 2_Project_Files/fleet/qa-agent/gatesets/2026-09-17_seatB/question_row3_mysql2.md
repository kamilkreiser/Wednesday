SUBJECT: [Secuura/Blockchain -> Wednesday] QUESTION: audit row GHSA-rgwj-5xj2-c3m3 mysql2 (Seat B)
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat B

CONTEXT
Row 3 of the 15: GHSA-rgwj-5xj2-c3m3, mysql2. Ticket KS-763. expires 2026-09-24, which lapses Thu 24 Sep 10:00 AEST and blocks every Blockchain/Dev push from then.

The advisory:
- [G] gh api /advisories: medium, mysql2 <= 3.23.0, patched 3.23.1. An unbounded zlib inflate in the compressed-protocol handler (decompression-bomb DoS).

What we carry:
- mysql2 3.15.3 in services/originate/package-lock.json and the root Blockchain/Dev/package-lock.json. Class devOptional, reached via @prisma/client's optional peer on prisma.
- The row's own 2026-09-06 measurement: it SHIPS in the originate runtime image, and NOTHING loads it. There are 0 source imports (with positive controls), and prisma's datasource provider is postgresql. I did not re-measure that.

Why no in-range fix exists:
- [V] npm view prisma@<v> dependencies: prisma 7.8.0, 7.9.0, 7.9.1 and 7.10.0 (latest stable 7.x) all declare mysql2: 3.15.3 EXACT. The only 8.x is a dev prerelease.
- Open Dependabot PR #949 (prisma 7.10.0) does not change mysql2.
- So 3.23.1 can only be reached by an `overrides` entry that contradicts prisma's declared dependency. Your brief puts that decision with Kam.

Records: 5_Project_History/2026-09-17_seatB-audit/step1/fixability-table.md (row 3), step1/npmview/prisma_7.*.

QUESTION
Which does Kam choose for row 3?
(a) FIX BY OVERRIDE (recommended). Add `"mysql2": "3.23.1"` to the `overrides` of TWO manifests:
  - services/originate/package.json, for its standalone lock;
  - Blockchain/Dev/package.json, for the root lock. originate is a workspace member (`services/*`), and npm reads overrides only from the root manifest of the tree it resolves; the root already carries 6 override keys (fast-uri, node-forge, path-to-regexp, express, @cardano-sdk/crypto, postcss).
  Then regen both locks in the bounded container, run originate's unit suites, and remove the row once both gates read it gone. A `prisma generate` smoke runs only if you rule it allowed.
  - Why: it removes the vulnerable code from the image instead of recording a decision to live with it. That is Kam's own 2026-09-09 "bump beats accept" ruling, delivered as #915.
  - The risk is bounded by the measurement above: we never load mysql2, so prisma's exact pin protects a MySQL path we do not use.
  - What it breaks: prisma's declared contract, only for a MySQL datasource.
(b) RE-DATE WITH A REASON, pending a prisma release that moves mysql2. This is Kam's or Wednesday's call, never mine, and the row stays present in the image.
(c) Something else Kam names.

MEANWHILE
Continuing with the other rows: waiting on your ANSWER to the fixability STATUS for the block order, and drafting the Sep-30 row QUESTIONs (11, 12, 14, 15).

NEEDED-BY
Mon 21 Sep 18:00 AEST to you, so it reaches Kam by Tue 22 Sep 18:00 AEST. If (a) is ruled, it needs one tier gate before Thu 24 Sep 10:00 AEST.

Seat B
