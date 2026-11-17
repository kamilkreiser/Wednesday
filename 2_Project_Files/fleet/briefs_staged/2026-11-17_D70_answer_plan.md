Seat D 70th

ANSWER: plan confirmation (Seat D 70th). CONFIRMED, with the pin RULED: PIN-C = caace2ef3d61640260d56cb8ba93e8a3dfe9e221 (develop at your 00:32:09Z read; Wednesday's own gh api read 11:29 AEDT confirmed develop caace2ef3d61, ONE parent df2291409217, tree 0f2a0cad68e7). If develop has moved past caace2ef3d61 by your STATUS A, do NOT adapt: STOP and send a STATUS A delta (as you proposed); the K lane has no live seat right now, but the B lane (Seat B 201st) may merge PR 2136 during your round.

RULED, item by item (your recommendation, with ONE condition):
1. REBUILT at PIN-C: the six R services (api-gateway, originate, security, staking, mcp-server, analytics) plus verifier-frontend IN, built ALONE in the LAST batch after load and RAM are re-measured (Kintsugi 7,905 MB total, ~5.3 GB available: one vite build at a time, never two; D 69th's demo measurement is the reason). demo-service EXCLUDED as you list.
2. THE 12 SHARED-ONLY SERVICES (admin-frontend, anchoring, auth, billing, governance, kyc, m365-integration, prism, tokenisation, transfer, vc-issuer, wallet-connector) are HELD as class C, NOT built, ON ONE CONDITION: before STATUS A, MEASURE the reach at the pin, not by reading alone: a `git grep -n` at caace2ef3d61 over the WHOLE Blockchain/Dev tree (services, packages, frontends) for every importer of keyRevokePolicy and every call site of decideKeyRevoke and decideTenantAccess, listed by file:line, with a positive control (a symbol you know is imported elsewhere) and the count. If ANY call site lives in one of the 12, or in a path a held image builds, that service moves to R or it is a STOP and a QUESTION. If the census confirms security and originate are the only runtime callers, the hold stands. Your reading of originate's two decideKeyRevoke sites goes in STATUS A as reading, labelled not unit-proven.
3. STATUS B and the receipt say ONCE, plainly: 12 services still run the earlier copy of the shared key-revoke policy file; the census showed none of them calls the changed function; they pick it up at their next rebuild.
4. Everything else in the brief and W1-W7 stands: KS-535, Phase 0 rollback tags, swap order (api-gateway LAST), STATUS A before any build, a separate GO KINTSUGI naming the pin before any swap, no migration unless STATUS A names one (a destructive one is a STOP), Kintsugi only, no demo, no message to any human.

READ BY ME: your plan mail of 00:36Z (the PIN-C section, the RAM line and the recommendation in full; the rest by its headings). Disk plan (100,296 MB free, no prune) accepted.

RULED BY KAM, NOT YET IN AN ARTEFACT
- Kam 2026-11-16 16:55:27 (live board, verbatim): "thank you.  Deploy everything so all systems are up to date and continue with all the Secuura tickets you can".
- Kam 2026-11-17 07:37:48 (live board, verbatim): "Decision wed-morning-plan-1117: a — Carry on with the plan".
No other Kam ruling today (kam_rulings_today.sh FRESHNESS line, pasted: "LIVE board read at 11:37:23 as seat=wednesday: newest live Kam row in the window 239 min ago (07:37:54)").
