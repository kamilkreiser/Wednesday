# Commission: QA GATE 386, TIER 1 (Opus), PR 2263 (KS-2280), 2026-11-20 ~07:5x AEDT (written by Wednesday, the 06:0x morning seat)

SHAPE: as /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-20_gate385-tier2-pr2262-ks2276/commission.md and the gate 384 / 383 commissions it names (read all WHOLE: method, hard limits, verdict format). Line 1 of your verdict = `PR 2263: <GO | GO WITH NOTES | NO GO> (at head <40-hex>; tier 1)`. Findings-only: you fix nothing. Write /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-20_gate386-tier1-ks2280-db-role-guard/verdict.md.

TIER 1, ON OPUS, AND WHY: a security surface (row-level security depends on the runtime database role) and a boot path that can stop a deploy.

THE CHANGE (Wednesday read at source 07:50:21: git ls-remote + PR files API): PR 2263 (https://github.com/Secuura/Distributed_Secuura/pull/2263) "Refs KS-2280: the gateway reads the database role it connected as, first in its DB boot work", head 2e8b9fffd91fa21b1a079b65d09aa014b9525544, base develop 718b15bbeb2004afe562ae097f3bb1246458cbdf, 7 files +378 -1:
- added Blockchain/Dev/packages/shared/src/db/runtime-role-guard.ts (+59)
- modified Blockchain/Dev/packages/shared/src/index.ts (+3)
- added Blockchain/Dev/packages/shared/src/__tests__/ks2280-runtime-role-guard.test.ts (+97)
- modified Blockchain/Dev/services/api-gateway/src/index.ts (+34 -1)
- added Blockchain/Dev/services/api-gateway/src/__tests__/ks2280-db-role-guard-at-boot.test.ts (+148)
- added two KS-2280 fragments (cheat +21, flow +16)
The builder's READY is saved beside this file as ready_w45.txt; its record is /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-20_seatW-45th/. Its claims are the builder's: reproduce, do not cite. The released design is in /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-20_W45_answer_plan.md (read WHOLE: it is the spec this PR must meet).

THE SPEC TO CHECK (Wednesday's ANSWER = option (iii)): WARN by default; REFUSE (process.exit(1), called by the guard path itself, not a throw: db.ts runDbReadyHook 102-117 swallows throws) ONLY when DB_ROLE_GUARD=refuse; unset or any other value warns. The check runs FIRST in runDbBootTasks, BEFORE loadFromDb, and therefore also on the KS-377 recovery path (db.ts ~144). Query unavailable or zero rows = warn and carry on (degraded mode unchanged). rolsuper and rolbypassrls are OR'd (a real superuser reads rolbypassrls false). Logs: the two booleans and a fixed hint ONLY; never the URL, user, password or role name (Kam's card secuura-ks1346-logging-thrown-objects-leaks-secrets = a, "Type and field names only"). runDbBootTasks becomes a named export; startServer still does not run under vitest.

QUESTIONS (your own measurement, in your own clone/worktree under this folder's _work; never in another seat's tree):
Q1 Does the PR meet every clause of THE SPEC above? Name any clause it misses, with the line.
Q2 Reproduce at least M1 (drop rolsuper), M3 (swallow the refusal), M4 (refuse when unavailable) and M5 (refusal on by default) yourself and show each fails a named cell; is there a mutant the cells miss (e.g. DB_ROLE_GUARD compared case-insensitively or by prefix, session_user for current_user, the check moved after loadFromDb, the recovery path skipping it)?
Q3 Can any value of DATABASE_URL, the role name or a thrown error reach the log through the new lines (including an error object's message from the query)? Plant a marked URL and role and grep the captured output.
Q4 Both suites whole on the merged state (develop + PR) vs develop, failure-name sets compared (packages/shared carries five known reds on develop: KS-1727 + KS-2281's four; anything else is a finding); tsc; eslint; the test-types ratchet; docs-fragments.
Q5 What would boot differently TODAY with this merged and no flag set? (Expected: nothing stops; a warning line on a box whose role is unsafe.) The PGlite cell: does it use only the existing hoist (no package.json or lockfile edit)?
Q6 The PR body and the KS-2280 facts comment: does any factual sentence not hold (including the demo correction: demo's gateway role and NODE_ENV are UNMEASURED; deploy-demo.yml targets the deleted Container Apps demo)?

HARD LIMITS: read-only on GitHub and Linear (no comment, review, label or merge); no write in any !CODING path (your own clone under _work); no fetch, pull or worktree add in another seat's checkout; no database server, no container, no box (in-process PGlite through the existing hoist is allowed); no mail, no send tool, no launch; no cd; no rm (move to _work/_quarantine); never kill a process by name; /usr/bin/grep -i with a positive control beside every zero; never read long lines through `cut -c`; never write a secret to any file.
RETURN: verdict line 1, then a 10-line summary (findings by severity with ids G386-2263-N, what you ran, what you did not).
