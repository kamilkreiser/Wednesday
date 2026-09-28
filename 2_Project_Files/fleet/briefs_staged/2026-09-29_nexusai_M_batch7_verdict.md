BLUF: BATCH 7 VERDICT (05:58 AEST; report `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-29-gate-batch7/report.md`, read whole by Tuesday). RD-628 GO WITH FINDINGS, RD-652 GO, RD-646+647 GO WITH FINDINGS: RELEASED to merge AFTER your 5a/5b sequence (RD-594 last there), in this order: RD-628 (a5799f3) -> RD-652 (09e2e6a) -> RD-646+647 (608a1cd), one at a time under C-184/C-186. RD-618 is NO GO: fix round 2 of 2 (tier 1), below. RD-686 is P's and goes to Kam.

MERGES (the per-merge pattern of the 5a/5b RELEASE; the forward merge onto today's main is counts-only per the gate):
- C-57: ruling (h) / C-187 covers the image-content-exposure pair only; any other missing id is a STOP.
- C-179 note to Kam: DONE (live board, 2026-09-29 ~06:0x, HTTP 201): the Redis-down boot change, the Docker unhealthy-not-restart consequence, and the Marketplace being unaffected. RD-646+647 may merge in its turn.
- STANDING RE-RUNS BY NAME: CENSUS-B/M at every later lane-1 merge that changes the server source (and K2 once RD-594 is on main); rd646 AND rd618 on the tree that first holds both; rd628's G2 when rd-424 (2ce26eb) merges.
- 7e4cd2e must never reach main on its own. RD-618 arrives only as its fixed head.

RD-618 FIX ROUND (round 2 of 2 for its class; tier 1; a NO GO after this goes to Kam):
- A-F1 (MAJOR): one anonymous Reporting-API request stores 319 ring entries (was 1); two replace the ring. Cap entries per request in buildCspEntries (a small N), or count each entry against the CSP limiter. Red-first cell: "one array of 300 reports stores <= N entries and <= N log lines" (red at 4334b96).
- A-F2 (Minor): userinfo kept when `new URL` throws (report §4.2 s3: port 99999, a space or %zz in the host). Fix the fallback; add those three shapes to S1.
- A-F3 (Minor): charset.unsupported / encoding.unsupported now reach the global handler, which logs the attacker's header value. Log only type/status for non-entity parser errors (keep the named 503 pass-on the cross cell proved).
- New READY: red-first per item, the cross-change cell x1/x2 re-run (with RD-646+647 if it is on main by then, else a scratch merge), PRIOR WORK, NOT TESTED.

TICKETS TO FILE (Jira, BLUF-first, search first): D-F1 + D-F2 (the rd646 census checks the NAME of every 503; the "down at boot" server must not share the proxy's port), one ticket, tier 2. B-F1 (the rd628 cell scrubs MACHINE_ID, WEBSITE_SITE_NAME, LEGACY_MACHINE_IDS), tier 2. Polish A-N1/B-N1/D-N2/D-N3 inside the nearest ticket.

-- Tuesday
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-29 05:48
