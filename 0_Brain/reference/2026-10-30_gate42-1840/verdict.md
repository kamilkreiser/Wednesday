## QA GATE - TIER 1, round 1: GO WITH NOTES
(Filed by the Wednesday seat from gate 42's returned text, 19:4x AEDT. Opus. Probes in `probes/`, copied from the scratchpad.)

**Subject:** PR #1840, KS-1845, head 9fc20b583645 at start and end; develop now a41909b50b44. Spark_gate facts: HEAD 65 pass 0 fail, 5 of 5 files; BASE product 17 pass 48 fail. All five gates exist and work; no legitimate repo caller found broken.

### FIX BEFORE MERGE
- **F1 (Low-Medium, SYSTEM_ADMIN only): own-subject refusal bypassed by UUID case.** kyc/src/index.ts:1088 strict `===` (Wednesday read it at source); schema z.string().uuid() admits upper case; migration 002 user_id TEXT (read; gate names svc_kyc_verifications). Gate cells in the KS-849 harness, in-memory table: same case 403; row UPPER, token lower: 200 approved HIGH; initiate with upper-case UUID: 201, stored verbatim. Fix: fold both sides + a cell.
- **F2 (mechanical):** merge-tree vs a41909b50b44 conflicts in both Projects Documents html; no product file.
- **F3 (Low):** cheat sheet "9 of 14 (each of the other four)" and the ticket comment's "73 cells" are wrong: 17+12+12+12+12 = 65 cells, 9 of 12 red.

### FOLLOW-UP
- F4: POST /api/workflows/escalate (transfer routes/workflows.ts:214, "admin endpoint"; no gate, Wednesday read it) ungated; OWNER 200 at service level; no gateway proxy found by grep (read, not run). Needs a ticket.
- F5: unstated routes: /api/kyc/:id/document, /selfie, /complete, /result; /api/kyc/microsoft/*; GET and DELETE /api/wallets/session/:id. Mock auto-approve via /complete not a prod door IF enforceProductionConfig works as read (index.ts:45), not run.
- F6: docs/security INVENTORY:116-118, RULES:192 go stale on merge (candidate 10). F7: kyc.openapi.ts:467 stale. F8: platform_admin in 6 gateway lists, refused by isPlatformRole; no minter found.
- F9 pre-existing: shared authenticate() does not check `type`: real-RS256 type:'refresh' token with SYSTEM_ADMIN passed direct-to-service (200). Gateway not tested.
- F10: brief line 42 listed lowercase system_admin as refused; the PR admits it; the PR is right (isPlatformRole; super_admin rides JWTs verbatim). D1 is a Wednesday-confirmed default, not Kam's words.

### Answers: Q1 five doors closed; census fired. Q2 not passable: 18 role values 403; real RS256 + spoofed headers refused; admitted controls 200. Q3 no repo caller found; other-repo search thin (first control 0). Q4 gate first in all five handlers. Q5 tests bite: 8 of 8 spot mutants killed; each fixture needed; suites reproduced; seat's 59/59 not re-run.

### NOT TESTED: running stack or gateway; live scheduled jobs outside the repo; real Postgres; four platform suites; Node 24; deploy; hook; real platform-admin login tokens; a fresh install (node_modules linked).
