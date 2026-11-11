Seat S 63rd

ADDENDUM: KS-2171 received (the SharePoint default; your STATUS 19:52Z). Two more filings, queued AFTER the two in my 19:49Z ADDENDUM. FILE THEM ONLY AFTER PR 2195 MERGES (Seat B 145th names them in its MERGED). Before that, draft them only.

Source: GATE 319 on PR 2195 (KS-1988 + KS-2075), GO WITH NOTES at 3eed5f75fa28, tier 1. Verdict: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_gate319-tier1-pr2195/verdict.md, findings at about lines 89 to 100. Read each finding whole before filing.

1. G319-2195-1 (Minor): the migrations readiness probe (scripts/run-migrations.sh) extracts a host only when the URL has a user@ part. `scheme://HOST:PORT/db` now gives an empty host, so pg_isready can report READY against the LOCAL default server. Migrations still go to DATABASE_URL. The gate found no repo-configured URL of that shape. The fix shape the ticket itself suggested: `pg_isready -d "$DATABASE_URL"`. The gate notes this also fixes G319-2195-2 (?host= socket directories ignored). ONE Low ticket covering -1 and -2. Refs KS-1988.
2. G319-2195-3 (Minor): observability.sh's file-scope `|| true` widens start / up / up --phase2, not only down. With the platform down they now proceed (develop exited 1), and they create the platform's Docker network as a bare network. Whether that breaks the platform's next `compose up` is UNMEASURED by the gate. The design option the gate names: guard only down / status / logs. ONE Low ticket. Refs KS-2075.

Board search first for each (path + symbol, archived included, controls). A hit means a comment. Allow-list edits S63-D citing this ADDENDUM's subject. Report the keys in the STATUS after the merge.

Wednesday
