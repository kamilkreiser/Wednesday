# gate52 COMMISSION — TWO Secuura PRs, merged A then B: #{{PA}} KS-1015 and #{{PB}} KS-1364 (both T2, round 1); author and merger {{MERGE_SEAT}}, round 52

Filled by fill_gate52.py at {{FILLED_AT}} from pins_gate52.json (measured {{MEASURED_AT}}). This restates Wednesday's commission to the drafter (2026-10-01), requirement by requirement. The gate prompt carries each requirement by name, and the launcher refuses a prompt that is missing any of the {{N_KW}} keywords (each matched as a token).

## The PRs
{{PIN_TABLE}}

- develop `{{DEVELOP}}` (tree `{{DEVELOP_TREE}}`) = #1365's merge. Both 0 behind, siblings.
- END_TREE_A `{{END_TREE_A}}` (`{{SHORTSTAT_A}}`). END_TREE_B `{{END_TREE_B}}` (`{{SHORTSTAT_B}}`) = the seat's PREDICTED tree. {{END_XCHECK}}
- {{CHAIN_LINE}}
- {{MODE_LINE}}
- {{HOOK_LINE}}
- Merger: {{MERGE_SEAT}} (the author of both). Pane: `QA/Secuura-batch{{PA}}`. Report dir: `{{REPORT}}`.

## The claim (the ONE READY)
- #{{PA}}: 3 files, +127/-2; `referral.openapi.ts` +21/-1 (the GET 200 envelope); 1 new test +76; yaml +30/-1, sha256 `43c71cf6d5f213b6`, 39889 lines.
- #{{PB}}: 5 files, +98/-0; two `*.openapi.ts` +1/-0 each; 2 new tests +48 / +46; yaml +2/-0, sha256 `39f027b63d4aa804`, 39862 lines, `required: true` 71 -> 73.
- The A+B union yaml: sha256 `e761a0b3c1eac6a5`, 39891 lines, blob `1ffd687b8a9d…`, `check:openapi` rc 0 on it.
- `generate-openapi --check` rc 0 per PR, control rc 1 with the yaml reverted; `check:openapi` rc 0, 405 example blocks.
- Red-first by assertion: A 3 failed | 3 passed (6); B 1 | 3 (4) per file. Suites: referral 28 -> 34; tenant-provisioning 13 -> 17; originate 1058 -> 1062 (89 -> 90 suites). tsc rc 0.
- Trailers: both commit messages empty, control `bf277eead268` carries Co-Authored-By (53 bytes).

## What the gate must rule (by name)
1. **#{{PA}}: the declared GET /api/referrals/{code} envelope == what the handler returns**, on 200 and on every error status the spec lists (file:line). A spec that disagrees with its handler is a Major. (ENVELOPE-MATCHES-HANDLER, ERROR-CODES-MATCH)
2. **#{{PB}}: each handler refuses an absent body** — tenants PATCH by the "No fields to update" 400 (`tenant-provisioning/src/index.ts:455-457`), v2 verify by the `:452-456` 400 after the four-alias coalesce (`verificationV2.ts:450-451`); body-parser's `req.body || {}` cited from the installed package. (HANDLER-REJECTS-ABSENT, BODY-PARSER-DEFAULT, ALIASES-COVERED)
3. **#{{PB}}'s body claim: POST /api/referrals/generate is NOT marked required because its handler accepts `{}`** (`referrals.ts` generateCodeSchema `:16-21`, `.parse` `:61`), verified from source. (GENERATE-NOT-REQUIRED)
4. **Goldens byte for byte; the yaml == generator output** (`--check` rc 0, control rc 1); the three YAML shas. (GOLDENS-BYTE-EQUAL, GENERATOR-REPRODUCES, CHECK-OPENAPI-RC, YAML-SHAS)
5. **Red-first per new test by assertion, then green; referral + tenant-provisioning (vitest) and originate (JEST), 0 new reds.** (RED-FIRST, CONTROLS-GREEN, SUITES-BASE-HEAD, TSC-NO-REGRESSION)
6. **The sequencing: B after A lands exactly on {{END_TREE_B}}; no textual conflict; both stay mergeable.** (SEQUENCE-A-THEN-B, CLEAN-MERGE, END-TREE, BOTH-MERGEABLE, MODES)
7. **The PR-text key scan: only the own hyphenated key, no closing keyword, NO Co-Authored-By trailer** (control `bf277eead268`). (KEYSCAN-OWN-KEY, NO-CLOSING-KEYWORD, NO-TRAILER, SUBJECT-LANDS-AT, SUBJECT-TRUE-OF-DIFF, PR-BODY-CLAIMS, NO-RUNTIME-CHANGE)
8. **The census** of other open PRs touching the 7 paths; Peter's #1360 / #1362 reported only. (COLLISION-CENSUS)
9. **NOT TESTED, explicit.** (NOT-TESTED-LIST) Plus TIERING, DISK-ENOSPC, **REPORT-HASH-LAST**; the `## MERGE ADDENDUM` goes LAST. The pass is proportionate (usage {{USAGE}}, Kam's 17:40:22 grant).
- NOT in scope: a live server, Schemathesis, any deploy, any DB, any request to a handler.

## GO
The GO string, as the GO mail's SUBJECT: `{{GO}}`. {{MERGE_SEAT}} merges #{{PA}} then #{{PB}}. Verdict mail subject: `{{VERDICT_SUBJECT}}`.

## The drafter's predictions (the gate re-derives each and never adopts one)
- pin_gate52.py -> pin_1.out: END_TREE_A `{{END_TREE_A}}`, END_TREE_B `{{END_TREE_B}}`. {{NUMSTAT}}
- specdiff_gate52.py -> specdiff_1.out: {{SPECDIFF}}
- handlers_gate52.py -> handlers_1.out: {{HANDLERS}}
- keyscan_gate52.py -> keyscan_1.out: {{KEYSCAN}}
- gh_read_gate52.py -> gh_read_1.out: {{CENSUS_LINE}}
