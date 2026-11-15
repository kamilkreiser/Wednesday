# notes: drafter for Seat D 64th, k28, 2026-11-15 22:4x-22:5x AEDT

- Grant: NOT lapsed. EXPIRING-GRANTS.md row with "keep the grant alive until further notice" is now line 38 (was 37 in earlier briefs; file shifted). It reads "this grant NO LONGER ends Sat 31 Oct; it stands until Kam changes it." Brief cites by text.
- develop 7b452b1bbb96 (22:22:25 +1100, PR 2224), equal to Wednesday's 22:38 read. 17 first-parent merges since 4e4347818772 (2224, 2079, 2234, 2223, 2098, 2236, 2222, 2221, 2233, 2238, 2235, 2230, 2229, 2220, 2232, 2231, 2140). 2081 and 2237+ not merged.
- Predicted REBUILD 7: auth, api-gateway, originate, kyc, vc-issuer, billing (if running), admin-frontend (if running). UNCHANGED 26, NOIMAGE 3.
- Differences from Wednesday's expected list: PR 2230 is merged (anchoring changed, EXCLUDED by default); 2098 is comments-only in auth; 2079 and 2234 and 2236 reach no image; governance/tokenisation/mcp-server drop back to UNCHANGED.
- Migrations: none new; 058 last; PR 2099 OPEN (8967de8b1755); 2195, 2067, 2225, 2081, 2239, 2237 OPEN.
- Anchoring: PR 2081 not merged; gate 248 F1 and card 1107 bluf say 2081 is NOT the empty-reply fix; no empty-reply fix in develop (confirmation.ts last 2026-11-03).
- Free disk carried 60,117 MB; 117 MB above the 60,000 QUESTION line (W5).
- Drafter slips: first clone attempt failed (no deploy key); retried with the repo-local core.sshCommand key path via GIT_SSH_COMMAND (no key content printed). A blobless clone needed the same env for blob fetches.

UNMEASURED: the box (all of it, including whether billing and admin-frontend containers run); Linear ticket states; gate verdicts for the 17 merges; Kam's 2230 "deploy when ready and tested" at source; security's shared-delta import analysis; compiled literals; the _d64 kit dry run.
