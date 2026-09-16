hits: 1
SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA: #1011 KS-871 @0a1f8900c7094fbdaed1099799c029e351296b39
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TS: 2026-09-16T18:01:07.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}
----
Seat A

## BLUF
- READY FOR QA: https://github.com/Secuura/Distributed_Secuura/pull/1011 at head 0a1f8900c7094fbdaed1099799c029e351296b39 (API = ls-remote, read just now). Base develop d067725ff (unmoved).
- A12 KS-871: a refused POST /api/gdpr/erasures is now audited with details.path /api/gdpr/erasures and gdpr.create / gdpr, where it read "/" and unknown.create / unknown. Admitted requests unchanged.
- Tier: I propose TIER 2 (an audit-row content change, no HTTP response change, no auth change). Your call.
- Links: KS-871 contributes, In Progress (walked by its own PR); "Part of KS-871", no closing phrase; it stays open on merge per 5f. KS-843 / KS-858 are named in the body, not linked, unmoved. Ticket comment 23a68884-71a7-4a22-a918-7f2d3be20955.
- Open PRs of mine awaiting GO: 2 (#1010 tier-1 gate being drafted, #1011).
- Files disjoint from #1010: audit.ts + two new ks871 tests vs verification.ts + ks1087.

## Recommendation (for the gate)
1. The acceptance's GET clause cannot be met through the audit log. AUDITED_METHODS (audit.ts:58) has no GET, so a refused GET /api/gdpr/erasures/:ref writes no row. A new cell pins that; tamper TG reddens exactly that cell.
2. Out of scope, unchanged, NOT measured: the other inside-finish req.path reads, i.e. the login special case, the H29 attemptedEmail capture (the same comparison) and the warning log's path. For a proxied /api/auth/login they may see a trimmed path. The brief named only one of them (":274"); at source there are three, and all three are named in the PR.
3. Latent or live stays UNMEASURED (isDbAvailable), per the ticket.
4. Seat edits beyond the READY lines, all declared in the PR:
   - accurate KS-871 comments (the READY said express trims req.path "after the response is sent"; the ticket measured a responding router.use gate);
   - Part A's red cell restores the env flag in finally;
   - the GET cell;
   - a typed query mock (12 including-tsc errors in the READY test files -> 0).

## Test Evidence (summary; full block in the PR body)
- Apply per HOW TO APPLY:
  - Part A: 5 fake meta lines stripped; product + test applied with git apply --recount (offsets 203->210, 277->280).
  - Part B: 2 indented headers de-indented; test applied; product :108 applied BY HAND from its -/+ pair.
  - Before the seat edits the diff was exactly the READY lines: product 5+/2-, and both test files byte-equal to the READY + lines (112 / 134).
- Red before green at d067725ff: 5 run, 3 red ("expected '/' to be '/api/gdpr/erasures'"; "expected 'unknown.create' to be 'gdpr.create'" x2), 2 controls green, 0 skipped. READY product lines 5/5; after the seat edits 6/6.
- Tampers: whole api-gateway suite per row (406 cells, 0 skipped), project tsc rc per row, byte restore asserted by sha256 + git diff --quiet HEAD. All as predicted, every row tsc 0.
  - T0: 0 red.
  - TA (details.path reads req.path again): 1 red.
  - TB (deriveAction reads req.path again): 2 red.
  - TAB (both): 3 red.
  - TG (GET audited): 1 red, the GET cell only.
  - TE (auditPath = req.path at entry): 0 red; the timing is the fix.
  - TI (inert): 0 red.
  - T0 after: 0 red.
- api-gateway at head: 49 files / 406 pass (develop 47 / 400). shared 44 / 851 pass. Project tsc rc 0. Including tsc: 0 errors in the 3 touched files; every other file's error set identical (33, 0 new). eslint 0 problems.
- Pre-push preflight in-hook 17:53:57Z -> 17:59:46Z rc 0: "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed." Legs 3/4/8 skipped (no stack); not a pass of those legs. Push verify PROTOCOL-CLEAN.
- Skill 4: neither Projects Documents HTML is affected (ks871 / audit.ts / unit counts 0 hits; control Schemathesis 65), stated in the body. Skill 2 host line in the body.

## NOT done / NOT covered
- No stack, no Postgres audit_logs write, no nginx; in-process only.
- isDbAvailable live-ness not measured.
- Schemathesis / Akto / Playwright / k6 not run (no HTTP response change; no stack, 0 docker images).
- The three other req.path reads (Recommendation 2).

## Next
A13 KS-745 (routes/audit-export.ts) from origin/develop into slot 3 of 3. It is file-disjoint from #1010 and #1011. I start it unless you say otherwise.

Seat A

