**BLUF:** words in two docstrings only; no behaviour change. This is the ticket's proposed default, approved by the coordinator (HPSMPOC-510).

## What changes
- `scripts/deploy-package.py`, `live_check` docstring (+5 -2): names every site-only name the web site accepts (the Oryx archive found there, `oryx-manifest.toml`, and the favicon route-cache pair), says the API site is allowed none, and says the summary is one line plus a second line counting the pair only when the count is above 0. It no longer says "nothing else may be".
- `infra/tests/test_deploy_hpsmpoc208.py`, `plant` docstring (+2 -1): carries the "not tested" qualifier the other three places carry (a page visit leaving the route-cache files is the deploy records' reading, not tested here).

## What does not change
No code, comment, constant, identifier, test row, assertion or README.

## Proof
- A program (`docdiff.py`) shows exactly one hunk per file, every changed line inside those two docstrings, and the ASTs equal with the two docstrings blanked: `DOCDIFF OK`. Its control (one code character changed in a copy) reads `DOCDIFF FAIL`, rc 1.
- Infra suite, compared with main by test id: 332 tests on each side, lost 0, added 0, changed 0 (control: a dropped row reads lost 1).
- `bash infra/scripts/validate.sh` at head: rc 0, ResourceWarnings 0, files still open 0.
- The edited test file alone: 42 tests OK under Python 3.14 and under Python 3.9; with `test_deploy_package`: 86 tests OK.

| Run | Tests | Result | load1 start/end | Wall |
|---|---|---|---|---|
| infra suite at main | 332 | OK | 5.38 / 5.85 | 47 s |
| infra suite at head | 332 | OK | 5.76 / 5.72 | 46 s |
| validate.sh at head | 332 | OK, rc 0 | 5.74 / 5.57 | 50 s |

Nothing deployed; no integration with HP tools.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
