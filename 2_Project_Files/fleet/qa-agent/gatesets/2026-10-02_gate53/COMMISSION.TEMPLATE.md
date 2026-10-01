# gate53 COMMISSION — ONE Secuura PR: #{{PR}} KS-530 (T1, round 1); author and merger {{MERGE_SEAT}}, round 53

Filled by fill_gate53.py at {{FILLED_AT}} from pins_gate53.json (measured {{MEASURED_AT}}). This restates Wednesday's commission to the drafter (2026-10-02), requirement by requirement. The gate prompt carries each requirement by name, and the launcher refuses a prompt that is missing any of the {{N_KW}} keywords (each matched as a token).

## The PR
{{PIN_TABLE}}

- develop `{{DEVELOP}}` (tree `{{DEVELOP_TREE}}`) = #1368's merge. 0 behind.
- END_TREE `{{END_TREE}}` (`{{SHORTSTAT}}`) = the seat's PREDICTED tree. {{END_XCHECK}}
- {{MODE_LINE}}
- {{HOOK_LINE}}
- {{UNCHANGED_LINE}}
- Merger: {{MERGE_SEAT}} (the author). Pane: `QA/Secuura-batch{{PR}}`. Report dir: `{{REPORT}}`.

## The claim (the ONE READY) and the ruling it rests on
- 3 files, +3/-18: `package.json` +3/-0 (the scoped override `"@prisma/dev": { "@hono/node-server": "^1.19.15" }`), `package-lock.json` 0/-11 (the nested `node_modules/@prisma/dev/node_modules/@hono/node-server` 1.19.11 removed), `audit-baseline.json` 0/-7 (the GHSA-frvp-7c67-39w9 row removed).
- The lock was made by a ONE-ENTRY PRUNE then npm validation, because npm's override is inert against a complete lock — approved by Wednesday 2026-10-02 (`fleet/briefs_staged/2026-10-02_answer_seatB54_method.md`, conditions 1-4), superseding the brief's Q2 regen route.
- Lock delta 0 added / 1 removed / 0 changed / 0 flips; `npm ci` rc 0; the ruled `npm install --package-lock-only` in node:24-alpine (npm 11.19.0) leaves it byte-identical (sha256 `1e418a81ce03…`); an independent from-scratch resolve gives the same dedupe.
- Red-first rc 1 naming frvp; at head contract / leg 6 / leg 7 rc 0; leg 6 reported 11 -> 9, baselined 25 -> 24; CLEANUP now names GHSA-92pp (nothing removed).
- Prisma: resolution from `@prisma/dev` returns the hoisted 1.19.17; `prisma --version`, `prisma generate`, `prisma dev --help` rc 0. No server started.
- Suites: originate jest 90 suites / 1062 tests / 0 failed; mcp-server vitest 5 / 0 failed; tsc rc 0. No image reads the root lock. Trailers: 0 (control `bf277eead268`, 55 bytes).

## What the gate must rule (by name)
1. **NO COLLATERAL**: the root locks' `packages` diffed key by key: 1 removed, 0 added, 0 changed, 0 flips; `@prisma/dev` byte-identical; hoisted 1.19.17 unchanged; the other 44 locks untouched; a planted-change control. (NO-COLLATERAL, PRISMA-DEV-BYTE-EQUAL, OTHER-LOCKS-UNTOUCHED)
2. **The lock is self-consistent and reproducible**: `npm ci` from it; the ruled container command leaves it byte-identical (with a control that npm ran); an independent resolve of prisma 7.8.0 + the override dedupes; without the override it gives 1.19.11. (NPM-CI-HEAD, LOCK-IDEMPOTENT, INDEPENDENT-RESOLVE, COUNTERFACTUAL)
3. **A real fix, not a false one**: external specifier, not bundled; resolution from `@prisma/dev`'s own dir returns the hoisted 1.19.17 (main entry + walk up; `/package.json` throws ERR_PACKAGE_PATH_NOT_EXPORTED); `prisma --version`, `prisma generate` (as the Dockerfile runs it), `prisma dev --help` rc 0; which of them loads the module. No server. (EXTERNAL-NOT-BUNDLED, RESOLVES-HOISTED, PRISMA-RUNS)
4. **The value**: 2.x is published, so `>=` would take the major; `^1.19.15` is right. (CARET-NOT-GTE)
5. **The audit**: red-first rc 1 naming frvp; contract / leg 6 / leg 7 rc 0 at head; frvp neither reported nor baselined; **explain the 11 -> 9**; the CLEANUP line verbatim (GHSA-92pp, nothing removed); the row removal by KEY SET; cohort 2026-10-09 -> 2; no `expires` changed. (RED-FIRST, AUDIT-LEGS, REPORTED-11-TO-9, CLEANUP-VERBATIM, ROW-KEYSET, COHORT-TWO)
6. **Images**: no Dockerfile copies the workspace-root lock (every Dockerfile, a control line that must hit); else build that image only. (NO-IMAGE-READS-ROOT-LOCK)
7. **Suites and tsc**: originate (jest), mcp-server (vitest), 0 new reds; tsc no regression. (SUITES-0-NEW-REDS, TSC-NO-REGRESSION)
8. **PR text**: {KS-530} only, no closing keyword, other keys de-hyphenated; the method stated plainly; NO Co-Authored-By trailer (control `bf277eead268`); the subject lands <= 92. (KEYSCAN-OWN-KEY, NO-CLOSING-KEYWORD, METHOD-STATED, NO-TRAILER, SUBJECT-LANDS-AT, SUBJECT-TRUE-OF-DIFF, PR-BODY-CLAIMS)
9. **The census** of other open PRs touching the 3 paths (report; a rebase they may need is not ours); **NOT TESTED, explicit.** (COLLISION-CENSUS, NOT-TESTED-LIST)
10. **The merge**: clean, END_TREE == the prediction, modes. (CLEAN-MERGE, END-TREE, MODES) Plus TIERING, DISK-ENOSPC, **REPORT-HASH-LAST**; the `## MERGE ADDENDUM` goes LAST. The pass is proportionate (usage {{USAGE}}, Kam's 17:40:22 grant).
- NOT in scope: a live server, a `prisma dev` server, Schemathesis, any deploy, any DB, the GHSA-92pp cleanup, any re-date.

## GO
The GO string, as the GO mail's SUBJECT: `{{GO}}`. {{MERGE_SEAT}} merges #{{PR}}. Verdict mail subject: `{{VERDICT_SUBJECT}}`.

## The drafter's predictions (the gate re-derives each and never adopts one)
- pin_gate53.py -> pin_1.out: END_TREE `{{END_TREE}}`. {{NUMSTAT}}
- lockdiff_gate53.py -> lockdiff_1.out: {{LOCKDIFF}}
- auditset_gate53.py -> auditset_1.out: {{AUDITSET}}
- registry_gate53.py -> registry_1.out: {{REGISTRY}}
- images_gate53.py -> images_1.out: {{IMAGES}}
- keyscan_gate53.py -> keyscan_1.out: {{KEYSCAN}}
- gh_read_gate53.py -> gh_read_1.out: {{CENSUS_LINE}}
