# gate51a COMMISSION — ONE Secuura PR: #{{PR}} KS-1364 (T2, round 1); author and merger {{MERGE_SEAT}}, round 51a

Filled by fill_gate51a.py at {{FILLED_AT}} from pins_gate51a.json (measured {{MEASURED_AT}}). This restates Wednesday's commission to the drafter (2026-10-01), requirement by requirement. The gate prompt carries each requirement by name, and the launcher refuses a prompt that is missing any of the {{N_KW}} keywords (each matched as a token).

## The PR
{{PIN_TABLE}}

- develop `{{DEVELOP}}` (tree `{{DEVELOP_TREE}}`) = #1364's merge. 0 behind. END_TREE `{{END_TREE}}` (`{{SHORTSTAT}}`). {{END_XCHECK}}
- {{MODE_LINE}}
- {{HOOK_LINE}}
- Merger: {{MERGE_SEAT}} (the author). Pane: `QA/Secuura-batch{{PR}}`. Report dir: `{{REPORT}}`.

## The claim (the READY + its CORRECTION)
- 11 files, +316/-6.
- 4 `*.openapi.ts` files, +11/-6: `required: true` on 11 request bodies.
- 6 new tests, +294.
- yaml +11/-0, generator `--check` rc 0, with a base-yaml control rc 1.
- `check:openapi` rc 0, 405 example blocks.
- suites 38->48, 28->32, 93->98, 47->57, 0 failed.
- red-first: 11 RED, 0 controls.
- tsc 0 errors (base not captured).
- Fuse 189.7 h at 02:19:54Z, 3 rows (from the correction mail).

## What the gate must rule (by name)
1. **The 11 paths exactly**, every changed product line only adding `required: true` to a `request.body`, the yaml +11/-0 all `required: true`, and each product hunk byte-for-byte against the Spark's held goldens. (PATHS-ELEVEN, REQUIRED-ONLY, YAML-ELEVEN, GOLDENS-BYTE-EQUAL)
2. **The yaml is the generator's output**: `generate-openapi --check` at head (plus a control), and `check:openapi` rc at head and at base. (GENERATOR-REPRODUCES, CHECK-OPENAPI-RC)
3. **The runtime truth, per operation, by reading each handler at head (file:line)**: a handler that ACCEPTS an absent body is a Major. (HANDLER-REJECTS-ABSENT, NO-RUNTIME-CHANGE)
4. **Red-first**: each new test fails at base on its RED cells by assertion, and passes at head; the controls pass both ways. (RED-FIRST, CONTROLS-GREEN)
5. **The 4 suites at base vs head**, with 0 NEW reds; tsc as a no-regression reading only. (SUITES-BASE-HEAD, TSC-NO-REGRESSION)
6. **The PR text**: title, body, `Refs KS-1364` only, the other keys de-hyphenated, no closing keyword, the six remaining operations named with reasons, and NOT COVERED honest. (SUBJECT-KEY-SCAN, SUBJECT-LANDS-AT, SUBJECT-TRUE-OF-DIFF, REFS-OWN-KEY, NO-CLOSING-KEYWORD, DEHYPHENATED-KEYS, SIX-REMAINING-NAMED, NOT-COVERED-HONEST, PR-BODY-CLAIMS)
7. CLEAN-MERGE, END-TREE, MODES, COLLISION-CENSUS; TIERING, DISK-ENOSPC, **REPORT-HASH-LAST**; the `## MERGE ADDENDUM` goes LAST. The change is SMALL, so the pass is proportionate (usage 87%, hard stop 90%).
- NOT in scope: a live server, Schemathesis, any deploy, any DB.

## GO
The GO string, as the GO mail's SUBJECT: `{{GO}}`. {{MERGE_SEAT}} merges #{{PR}}. Verdict mail subject: `{{VERDICT_SUBJECT}}`.

## The drafter's predictions (the gate re-derives each and never adopts one)
- pin_gate51a.py -> pin_1.out: END_TREE `{{END_TREE}}`. {{NUMSTAT}}
- specdiff_gate51a.py -> specdiff_1.out: {{SPECDIFF}}
- handlers_gate51a.py -> handlers_1.out: {{HANDLERS}}
- keyscan_gate51a.py -> keyscan_1.out: {{KEYSCAN}}
- gh_read_gate51a.py -> gh_read_1.out: {{CENSUS_LINE}}
