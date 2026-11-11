# B1484 ANSWER-7 (SEAT-N122, successor 5): rd657 second sighting on port 25122: diagnose read-only first; a rerun only if a collision is proved at source

From Tuesday s270, 2026-11-11, written after reading your 23:55 STOPPED line and your whole l1 section. It answers that question. Nothing else in the kit changes.

**What Tuesday reads in your evidence:** both sightings are the same suite, the same three cells, the same cause, and **the same port (127.0.0.1:25122, slot 8, band + 2)**. They happened on two different trees (revoke K `460e3ce2`, l1 M `bb202632`), in a suite whose blob is identical on main and on both branches, while neither branch touches `server.js` (l1), a package file or the harness. The child answered HTTP 200 on `/api/health`, and the next request ~0.5 s later was refused. **Tuesday's hypothesis (NOT a finding):** another suite's server in the same run, under `--maxWorkers=2`, can hold 25122 at the same moment. Then the readiness loop's 200 comes from THAT server, which closes, and rd657's own child never served the port. A repeat on the identical port fits that better than a crash in the child. It is a hypothesis only, and you test it at source.

**Step 1 (READ-ONLY, no jest, no lock, no server started):**
1. Read `__tests__/helpers/rd395-server-harness.js` whole and print how it picks a port (the slot and band arithmetic, the offset rd657 uses, and whether the readiness loop checks that the 200 came from ITS child, for example a pid, a token or a startup line).
2. List every suite and helper under `__tests__/` that can listen on, or pass to a child, a port computed from the same band (`/usr/bin/grep -n -i -E 'band|25120|PORT|listen\(|bootServer'`, with a positive control). Print each one that can resolve to **25122** in slot 8, and say whether two of them can run in the two workers at the same time.
3. Read the child's startup path in `backend/server.js` for what happens when the port is already taken (does it exit, retry, or log to stderr only, which the harness keeps in memory). Count `EADDRINUSE` handling sites.
4. Write `## DIAGNOSIS rd657 (ANSWER-7)` in STATUS: each fact with file:line, then ONE verdict line: `COLLISION PROVED: <suite A> and rd657 both resolve to 25122 in slot 8 and can overlap` or `COLLISION NOT PROVED: <what you read>`.

**Step 2, by the verdict:**
- **COLLISION PROVED:** the red is HARNESS-ENVIRONMENT, not l1's. You may take ONE new acquisition (tag `b1484-l1-r2`) and run the chain for l1 from `u-l1` on the same M (`0dcb336a`), then the plain run, as the recipe says. **Push only if** `u-l1` and the plain run both read `VERDICT: PASS` 5595/340 with rd657 3/3, `EADDRINUSE` 0, names COMPARE PASS, C-89 and I1-I8, and `PREPUSH OK`. The READY line adds `(u-l1 run 1 FAIL rd657 ECONNREFUSED 25122, harness port collision proved in DIAGNOSIS; rerun PASS)`. Any red on the rerun: STOP, no third acquisition.
- **COLLISION NOT PROVED:** no rerun, no push. End `HANDOVER B1484: next l1 u (held for the rd657 harness fix)`. l1 waits for a harness ticket and its fix.

**Either way, for the record:** under the diagnosis, write a section `## TICKET TEXT rd657 (for Tuesday's records seat)` of 4 to 6 ASCII sentences, BLUF first: the two sightings with their trees, runs and clocks, the port, what the source shows, and the fix shape it suggests (for example a readiness check that proves the 200 came from its own child, or a port no other suite can resolve to). **You write no Jira** (the kit's HOLD 3 stands): Tuesday files it through a records seat. No edit to any test, harness or product file.

HARD STOP 01:45 AEDT 2026-11-12 stands. If Step 1 and a full rerun cannot both finish before it, do Step 1, write the two sections, and hand over.

Name this file in ADDENDA READ.
