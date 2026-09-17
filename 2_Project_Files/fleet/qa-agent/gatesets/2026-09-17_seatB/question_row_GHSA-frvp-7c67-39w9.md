SUBJECT: [Secuura/Blockchain -> Wednesday] QUESTION: audit row GHSA-frvp-7c67-39w9 @hono/node-server (Seat B)
TS: 2026-09-17T07:27:03.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat B

CONTEXT
Row 14 of 15: GHSA-frvp-7c67-39w9, @hono/node-server (KS-530). expires 2026-09-30, which lapses Wed 30 Sep 10:00 AEST.
- [G] medium: path traversal in serve-static on Windows. Fixed in 1.19.15 on the v1 line (<1.19.15), or 2.0.5 on v2. The row's "fix is >=2.0.5 only, semver-MAJOR" is wrong: a v1 patch exists.
- services/mcp-server: 1.19.14 (prod, via @modelcontextprotocol/sdk ^1.19.9). The move to 1.19.17 is in range.
- services/originate + root: 1.19.11 (devOptional), pinned EXACT by @prisma/dev 0.24.3, which prisma 7.8.0 pins.
  - [V] prisma 7.9.0 / 7.9.1 / 7.10.0 pin @prisma/dev 0.24.14 / 0.24.17 / 0.24.17. Those declare NO @hono/node-server (control: 0.24.3 declares it at 1.19.11 exact).
  - So a prisma lock move inside originate's own ^7.8.0 removes this copy entirely.
- [V] prisma 7.8.0 -> 7.10.0 changes only @prisma/config, @prisma/dev, @prisma/engines and @prisma/studio-core. @prisma/client 7.8.0 -> 7.10.0 changes only @prisma/client-runtime-utils. mysql2 stays 3.15.3 (row 3 is unaffected).
- The prisma client is generated at image build (originate/Dockerfile:38), and your brief's HOLD puts a prisma bump that needs generate behind a question.
- OVERLAP: open Dependabot PR #949 moves prisma to 7.10.0 (root lock + originate/package.json). I will not touch #949.

QUESTION
Which does Kam choose for row 14?
(a) FIX IN RANGE (recommended). One PR:
  - the mcp-server patch (@hono/node-server 1.19.17);
  - a lock-only move of prisma, @prisma/client and @prisma/adapter-pg to 7.10.0 in originate + root (0 manifests; all inside ^7.8.0);
  - originate's unit suites, plus a `prisma generate` smoke in the bounded container (no image build).
  Tier 1. #949 then becomes redundant, and closing it is not mine.
(b) Override @hono/node-server to 1.19.17 under @prisma/dev (contradicts its exact pin, and keeps prisma 7.8.0).
(c) A dated decision. Not mine.

MEANWHILE
Continuing with PR-1 (hono) and PR-2 (colord).

NEEDED-BY
Fri 25 Sep to you. The row lapses Wed 30 Sep 10:00 AEST; (a) needs one tier-1 gate before then.

Seat B
