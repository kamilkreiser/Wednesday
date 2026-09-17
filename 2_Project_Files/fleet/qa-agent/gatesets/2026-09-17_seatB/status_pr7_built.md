SUBJECT: [Secuura/Blockchain -> Wednesday] STATUS: PR-7 mysql2 built locally at 9fd3cb924, waiting on #1030 GO (Seat B)
TS: 2026-09-17T11:23:39.000Z
AUTH: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat B

BLUF
PR-7 (mysql2 override, rows GHSA-rgwj / KS-763 and GHSA-3f6p / KS-751) is BUILT and committed locally at 9fd3cb924 in WT2, on develop 75ad0e55c. NOT pushed; it waits for #1030's GO and merge (one PR open at a time). Your 11:07:34Z proof points all hold. Nothing else is in flight: I am idle on the lane until #1030's GO.

PR-7, AS BUILT (evidence: 5_Project_History/2026-09-17_seatB-succ1/pr7/)
- Manifests: "mysql2": "3.23.1" added to `overrides` in services/originate/package.json and Blockchain/Dev/package.json.
  - Parse delta = that one key each. Key order kept.
  - The root manifest did not round-trip through a JSON dump, so the key went in by a single-anchor text insert, parse-checked.
- Resolution by parse (your item 2): mysql2 is 3.23.1 in BOTH locks (root, services/originate), 3.15.3 absent, nothing below 3.22.0.
  - originate: `npm install --package-lock-only --ignore-scripts --no-workspaces` moved it.
  - root: the same install returned rc 0 and left the lock BYTE-IDENTICAL at 3.15.3, which is the KS-749 "inert override" trap. `npm update mysql2 --package-lock-only --ignore-scripts` then moved it.
- Scope: each lock moved exactly 4 entries, all in mysql2's own dependency subtree (mysql2, +sql-escaper 1.5.2, -seq-queue, -sqlstring). Flag classes are unchanged (devOptional).
  - The only unsatisfied declarer range is prisma's exact "3.15.3", which is the ruled override.
  - Controls fire: out-of-scope plant rc 1, flag-change plant rc 1. My first flag control picked denque, which ioredis shares and which carries no flag, so it could not fail; it was re-pointed before any reading was taken.
- Reachability re-measured at 75ad0e55c: 0 imports of mysql2 under services, packages, frontend and connectors (controls ioredis 16, pg 44, @prisma/client 1). 0 "mysql" in originate/src (control postgres 87). The one schema.prisma: provider "postgresql".
- Tests:
  - host root npm ci (hoisted mysql2 3.23.1): originate jest 63/63 suites, 656/656; packages/shared 851/851.
  - Container (node:24-alpine, Dockerfile builder emulation, no image, no apk), shared built, originate's OWN lock: mysql2 3.23.1 installed, `npx prisma generate` rc 0 (Prisma Client 7.8.0).
  - jest --runInBand in the container: 63/63, 656/656.
  - My first container jest run (parallel workers) was VOID: 32 of its 35 FAILs were "jest worker ... terminated ... SIGKILL" (memory in the shared Docker VM). I killed my own container by exact name and re-ran in band.
- Gates (the base is 32 rows until #1030 merges):
  - fix, rows removed: audit-gate rc 0 (29 reported / 30 baselined), audit-locks rc 0.
  - control, rows present: rc 0 with both under CLEANUP.
  - negative control, develop's two lock blobs with the rows removed: audit-gate rc 1 and audit-locks rc 1, naming exactly GHSA-3f6p [high] and GHSA-rgwj [moderate] (locks: services/originate).
  - My locks were then restored from saved copies, sha256-verified.
  - Conservation 32 -> 30, 0 added, 0 other rows altered.
- Proposed tier: 1. mysql2 ships in the originate runtime image, per both rows' own reachability text.

AFTER #1030 MERGES
- Merge develop in (never rebase).
- Regenerate the root lock from develop's blob (both PRs touch it), with `npm update mysql2`, and re-prove resolution.
- Re-measure the gates, including the negative control, at 31 -> 29.
- Suites, then the full in-hook preflight, then push.
- PR body carries Kam's 18:31:30 ruling verbatim and your 11:07:34Z ANSWER under the two-row removal.
- Facts comments on KS-763 and KS-751. KS-751's says mysql2 only; its two browserslist advisories are untouched; no state change.
- READY tier 1.

Seat B

