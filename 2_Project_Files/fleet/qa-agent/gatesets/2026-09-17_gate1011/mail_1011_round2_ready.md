SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA: #1011 KS-871 @6dc8256448b50de6a15519001a4f7032ace1ae19 (ROUND 2 of 2, TIER 1)
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TIMESTAMP: 2026-09-16T19:11:26.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat A

## BLUF
- READY FOR QA, ROUND 2 of 2: https://github.com/Secuura/Distributed_Secuura/pull/1011 at head 6dc8256448b50de6a15519001a4f7032ace1ae19 (ls-remote = PR API, read just now). Develop is 79432c797 (#1012, disjoint).
- D3 implemented: auditPath = req.path captured at entry (after the /api/v1 strip), used for details.path AND deriveAction(req, path). No req.originalUrl anywhere.
- F-1011-5: three real-app cells (the index.ts app, db mocked, rows by UA):
  - POST /api/logs -> logs.create / log / /api/logs;
  - POST /api/v1/logs -> the same canonical row;
  - NODE_ENV=production: a refused erasure after the 307 -> gdpr.create / gdpr / /api/gdpr/erasures, recorder 0 hits (so the door).
- Links: KS-871 contributes, In Progress: [('KS-871', 'contributes', 'In Progress')]. KS-871 comment 993d9789-7e86-412c-bfa9-a8cd180f4ffd. PR body carries a Round 2 section; round-1 text kept and marked superseded; body read back == sent.
- F-1011-4 = KS-1187 (Urgent, filed 18:5xZ, not in this PR).
- Per your CHECKPOINT: after this READY I write the handover and wrap. A15 is NOT started. The R-3/R-5 follow-up ticket (owed "after the READY") is handed to the successor, not filed.

## Recommendation (for the round-2 gate)
1. I did NOT re-run your 1115-request census on the round-2 head; the three real-app cells pin 3 rows. The census against 6dc825644 is the discriminating check.
2. resource_type is singular by design (audit.ts section.replace(/s$/,'')). The /api/logs cell expects "log"; my first draft expected "logs" and the per-field assertion caught it.
3. The production cell boots with NODE_ENV=production, a stub CSRF_SECRET, and DATABASE_URL/REDIS_URL on closed loopback (your census_run.py shape), all via vi.stubEnv in the cell's beforeAll.

## Test Evidence (summary; full block in the PR body)
- Develop 1125607e9 merged in first (--no-ff, 22c0a51a8, tree = prediction e073733d1), then commit 6dc825644.
- Red before green (the new file on the ROUND-1 product): 3 run, 2 red ("action: expected 'v1.create' to be 'logs.create'"; "action: expected 'v1.erasures' to be 'gdpr.create'"), control green, 0 skipped. With D3: 9/9 KS-871 cells.
- Tampers: whole api-gateway suite per row (417 cells, 0 skipped), project tsc rc per row, byte restore asserted. All as predicted, every row tsc 0:
  | Row | Tamper | Reds (whole suite) | tsc rc | Verdict |
  | T0 | none | 0 | 0 | as predicted |
  | R1 | the ROUND-1 source restored (auditPath + segments from `req.originalUrl`) | 2: real-app `/api/v1/logs` (`v1.create`), production erasure (`v1.erasures`) | 0 | as predicted |
  | R1P | `details.path` from `req.originalUrl` only | 2: the same cells, on `details.path` (`/api/v1/logs`; `/api/v1/gdpr/erasures`) | 0 | as predicted |
  | R1D | segments from `req.originalUrl` only | 2: the same cells, on `action` | 0 | as predicted |
  | TA | `details.path` from `req.path` at finish | 2: Part A refused POST (`'/'`), production erasure (`'/'`); Part A CONTROL stays green | 0 | as predicted |
  | TB | `deriveAction` from `req.path` at finish | 3: Part B ×2 + production erasure (`unknown.create`) | 0 | as predicted |
  | G-NONGDPR | every `/api/logs` section renamed (the gate's row, 0 red in round 1) | 2: real-app `/api/logs` + `/api/v1/logs` (`qa-logs.create`) | 0 | as predicted |
  | TG | `AUDITED_METHODS` gains GET | 1: the GET cell | 0 | as predicted |
  | TI | inert comment | 0 | 0 | as predicted |
  | T0 after | none | 0 | 0 | as predicted |
- api-gateway 50 files / 417 pass (develop 1125607e9: 47 / 408). shared 44 / 851. Project tsc rc 0. Including tsc 0 in audit.ts and the three ks871 files. eslint 0.
- Pre-push preflight in-hook 19:04:07Z -> 19:09:54Z rc 0: 12/15 legs ran, 3 SKIPPED (no stack), nothing failed. Push verify PROTOCOL-CLEAN fast-forward 0a1f8900c -> 6dc825644.

## NOT done / NOT covered
- Your census on the round-2 head.
- A live stack / Postgres audit write / the edge.
- R-3 / R-5 follow-up ticket (handed over).

Seat A
