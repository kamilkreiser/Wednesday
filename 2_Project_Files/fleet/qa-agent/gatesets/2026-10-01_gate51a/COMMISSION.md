# gate51a COMMISSION — ONE Secuura PR: #1365 KS-1364 (T2, round 1); author and merger Seat B 52nd, round 51a

Filled by fill_gate51a.py at 2026-10-01T02:31:09Z from pins_gate51a.json (measured 2026-10-01T02:26:18Z). This restates Wednesday's commission to the drafter (2026-10-01), requirement by requirement. The gate prompt carries each requirement by name, and the launcher refuses a prompt that is missing any of the 28 keywords (each matched as a token).

## The PR
| PR | ticket | tier | head | parent | merge-base | ahead / behind | files (+/-) | subject declared -> lands |
|---|---|---|---|---|---|---|---|---|
| #1365 | KS-1364 | T2 | `bf277eead26897bb648c801f92308681dbdaffdc` | `c56dd7c32edf` | `c56dd7c32edf` | 1 / 0 | 11 (+316/-6) | 81 -> 89 |

- develop `c56dd7c32edf203177ade6c4d0c9040e624681b8` (tree `90fe6bbb79eb487023eda4ab8cb237a29f924f8b`) = #1364's merge. 0 behind. END_TREE `da849aa1d5c3d60f62b49b7f625fca01e3d59059` (`11 files changed, 316 insertions(+), 6 deletions(-)`). Three instruments agree on it (end_tree_crosscheck_1.out): merge-tree + commit-tree over develop, the head's own tree (parent == develop), and GitHub's `refs/pull/1365/merge` tree; develop's own tree 90fe6bbb79eb is the control that differs.
- MODES (git ls-tree): all 11 PR paths 100644 at head / alone / END; control `Blockchain/Dev/scripts/run-migrations.sh` 100755 at develop / head / END.
- IDENTICAL at develop / head / END: `pre-push` ffc25ebc37d4, `preflight.sh` 270b8913c009, `generate-openapi.ts` e84acdc9e1be, `check-spec-examples.mjs` e9c14a4dedf1, `package.json` d22c14e6c370.
- Merger: Seat B 52nd (the author). Pane: `QA/Secuura-batch1365`. Report dir: `2026-10-01-batch1365-g51a`.

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
The GO string, as the GO mail's SUBJECT: `GO (Seat B 52nd): merge 1365 on gate51a`. Seat B 52nd merges #1365. Verdict mail subject: `[QA -> Wednesday] GATE51A #1365 (Seat B52 author and merger, round 51a; T2 OpenAPI: eleven request bodies marked required, 6 new spec-rendering tests, the generated yaml)`.

## The drafter's predictions (the gate re-derives each and never adopts one)
- pin_gate51a.py -> pin_1.out: END_TREE `da849aa1d5c3d60f62b49b7f625fca01e3d59059`. The measured numstat is +316/-6 over 11 files; the seat claimed +316/-6.
- specdiff_gate51a.py -> specdiff_1.out: SPECDIFF PASS: 0 FAIL of 7 checks | base c56dd7c32edf | head bf277eead268
- handlers_gate51a.py -> handlers_1.out: HANDLERS PASS: 11 of 11 operations REJECTS-EMPTY at bf277eead268 | control TENANT-CTL OK | 0 FAIL
- keyscan_gate51a.py -> keyscan_1.out: KEYSCAN PASS: 6 checks over 1 PR, 0 FAIL, 0 FLAG line(s) (live surfaces; the gate rules them)
- gh_read_gate51a.py -> gh_read_1.out: CENSUS 22 other open PR(s) read | 0 touch a kit path or carry a census key ['KS-1364'] | client-human PRs named: ['1360', '1362'] (the launch action re-reads it, rc 15 on any hit outside kit.json reported_overlaps)
