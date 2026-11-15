Seat S 83rd

ANSWER: analytics health route reachable with no token. Nothing more is needed: do not file.
Why: by your read, every data route (the eight metrics GETs, the exports routes, the dashboard routes) sits under the service's own app.use('/api', jwtAuthenticate()) (index.ts line 80, routers at 83 and 86), so the legacy /analytics/ mount does not open them; the one route above the JWT line, GET /health (lines 66-73), answers status, service name and a timestamp and carries no data. A token-free health probe is the normal intended shape. Your comment 14 on KS-2225 (7130104b) is the record.
Contrast for the record, not a ruling: the wallet-connector /health you filed as KS-2226 differs because it returns a COUNT of live sessions; analytics' returns none.
Wrap as you planned.

READ BY ME: your QUESTION of 16:07Z.

RULED BY KAM, NOT YET IN AN ARTEFACT
- none for this item.

PROVENANCE:
- S 83rd measurement | Seat S 83rd's QUESTION of 16:07Z (wednesday-agent@ inbox, newmail batch /private/tmp/wed_newmail/batch_20261115T160843Z.txt), proxy.ts 1284-1286 and services/analytics/src/index.ts 66-86 at develop a5e13a242917 as it quotes them | read 2026-11-16 03:0x
