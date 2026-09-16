hits: 1
SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA: #1012 KS-745 @e225a49480e16bb77251a5d7cbd16afdf2929550
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TS: 2026-09-16T18:11:24.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}
----
Seat A

## BLUF
- READY FOR QA: https://github.com/Secuura/Distributed_Secuura/pull/1012 at head e225a49480e16bb77251a5d7cbd16afdf2929550 (API = ls-remote, read just now). Base develop d067725ff (unmoved).
- A13 KS-745: the admin audit export fetches the security list route /api/audit (was /api/audit/logs, which matched /api/audit/:id and 404'd) and reads data.data.logs.
- Tier: I propose TIER 2 (an admin-only export's upstream URL and read; no auth change). Your call.
- Links: KS-745 contributes, In Progress (its own PR); "Part of KS-745"; it stays open on merge per 5f. KS-743 / KS-28 are named, not linked, unmoved. Ticket comment 87694669-0818-46f5-b78e-709778059eb9.
- Now at 3 open, the limit: #1010 c3213b04e (tier-1 gate drafting), #1011 0a1f8900c (tier-1 gate drafting), #1012. All heads unmoved. Holding. A14 KS-999 is not started.
- Files disjoint from #1010 / #1011: audit-export.ts + one new test.

## Recommendation (for the gate)
1. The READY's cell could not see the :144 read. With the old read, the export's data is the list's wrapper object, which still contains the entry id, so toContain passed. The cell now parses the body; tamper TR reddens it on "the exported data is the entries array".
2. Residuals the fix exposes, read at source, not measured, not filed; your routing:
   - the security list route (security/src/index.ts:732-777) ignores the export's type param;
   - the list defaults limit to 50 and the export sends none, so an export caps at the 50 newest entries;
   - the list compares createdAt <= new Date(to) with a date-only to, which looks like it excludes the to day.
3. Reach read, not driven: mounted at api-gateway index.ts:801 (/api/admin/audit). Shadowing and the security list's KS-743 tenant gate on the forwarded token: not measured. The ticket's UNMEASURED stands.
4. Seat edits, declared: body assertions (above); a readable URL assertion; the file made to type-check (TS1378 top-level await, TS2741 Server type, TS2554: a stray 10_000 passed as a second argument to new Promise, never a timeout).

## Test Evidence (summary; full block in the PR body)
- Apply: split per file; test + product via git apply --recount. Before the seat edits the diff was exactly the READY lines (+4 -2; test byte-equal).
- Red before green at d067725ff: 2 run, 1 red (the URL), control green, 0 skipped. 2/2 after, with and without the seat edits.
- Tampers: whole api-gateway suite per row (402 cells, 0 skipped), project tsc rc per row, byte restore asserted. All as predicted, every row tsc 0.
  - T0: 0 red.
  - TU (URL back): 1 red.
  - TR (read back): 1 red, the entries-array assertion.
  - TUR (develop's product): 1 red.
  - TI (inert): 0 red.
  - T0 after: 0 red.
- api-gateway at head 48 files / 402 pass (develop 47 / 400). shared 44 / 851 pass. Project tsc rc 0. Including tsc: 0 in the touched files (READY test 3); other files identical (33, 0 new). eslint 0.
- Pre-push preflight in-hook 18:04:37Z -> 18:09:41Z rc 0: "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed." Legs 3/4/8 skipped (no stack); not a pass. Push verify PROTOCOL-CLEAN.
- Skill 4 docs: neither HTML affected (ks745 / audit-export / unit counts 0 hits; control 65), stated in the body. Host line in the body.

## NOT done / NOT covered
- No stack; the export not driven end to end; shadowing, the forwarded token and the residuals not measured.
- Schemathesis / Akto / Playwright / k6 not run (no stack, 0 docker images).

Seat A

