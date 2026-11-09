# Spark o126 report (operator's message, saved by Wednesday; the operator did not attempt the Write, WED-158)
Rounds: 0 briefed, 0 PASS, 0 FAIL. Both targets STOPPED at the screen; no counter round spent. develop d0b4825cc244 (ls-remote start and end). Open PRs 69 / 329 files at start and end; control fired (api-gateway/src/index.ts in PR 2125). Tunnel UP at start, DOWN (TimeoutError) at end.

## KS-1372 (card = a, retire the gateway lockout): STOPPED
Census: git grep -i -E "bruteForce|brute.force|BRUTE_FORCE" at develop (control: finds createBruteForceProtection in middleware/security.ts and its index.ts use).
Edit points far over 3: src/index.ts import 38, construction 454, app.use 459; src/middleware/security.ts function ~144-292, config type field 31, header comment 8; src/config/services.ts bruteForce block 63; src/services/redis.ts get/set/deleteBruteForceData + in-memory fallback + TTL (orphaned; card silent); tests: ks1461-brute-force-guard-folds-case, ks1868-brute-force-redis-catch-unreadable-throw, ks1961-brute-force-guard-fails-closed (guard-only files), security.test.ts describe at 220, ks1461-case-variants-keep-the-gateway-checks.test.ts; docs WORKFLOWS.md 238, S-K-OWNERSHIP-CONTRACT.md 350; outside the gateway: frontend/admin/Settings.tsx toggle, nginx-demo.conf mention (scope UNMEASURED).
Held by open PRs: index.ts (PR 2125), ks1461-case-variants test (PR 2132), WORKFLOWS.md (PR 2136), S-K-OWNERSHIP-CONTRACT.md (PRs 2136, 2135, 2073).
Route: a Claude seat after PR 2125 merges, with a multi-file removal brief deciding the orphaned redis.ts functions and the three guard-only test files.

## KS-1785 (card = a, secret-guard hook, local-only exemption): STOPPED
Source: ticket text from the o120 folder's tickets_priority12.json (local copy, not a live read). Needs: new Python hook under .claude/hooks/; new .claude/settings.json (none at develop); .gitignore rule for .env.*; contract test via python3; CLAUDE.md + systemTest/CLAUDE.md docs; a comment per systemTest .env.example. 5-8 edit points; the hook body IS the product (security surface, tier 1 gate). Files free of open PRs except .env.example in PRs 2067 and 2052. Not under .github/workflows.
Route: a Claude tier-1 build seat (files are free now). UNMEASURED: platform-s block_secret_reads.py, PS-1387 state, whether Peter's setup is bound, .env.* vs tracked .example templates.
