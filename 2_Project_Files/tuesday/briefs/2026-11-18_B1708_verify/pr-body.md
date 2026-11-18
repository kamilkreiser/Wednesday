## Summary

`deploy-package.py live-check` stops reporting the favicon route-cache pair as a stale or foreign file on the **web** site. The pair appears on the web site between a deploy and the live check, and today it turns a healthy deploy into exit 3 NOT PROVEN (HPSMPOC-509). The deploy records read it as left by a page visit; that cause is not tested. This is the ticket's proposed default, approved by the coordinator.

## What changes

- `scripts/deploy-package.py`: live-check allows exactly `.next/server/route-cache/APP_ROUTE/<64 lowercase hex>/$/favicon.ico.body` and `.meta` as site-only names, on the web site only, matched whole-name (`fullmatch`: no prefix, no suffix, no trailing newline). Each name is judged on its own. A second output line counts them, only when the count is above 0; the first output line is byte-identical to before.
- `infra/tests/test_deploy_hpsmpoc208.py`: seven new rows in `LiveCheck` (one helper, three constants); no existing row is edited.
- `infra/README.md`: names the allowed site-only names.

The allowance is the two names and nothing more. What the 64-hex folder name comes from, and whether any other route can leave a route-cache file, are not established, so any other route-cache file is still SITE-ONLY, red, and exit 3.

## What does not change

The API is unchanged and strict (the same two names on the API are still reported). The Oryx allowance, every other site-only name, `live_files`, `package_files`, `make`, `verify` and `deploy-from-ci.sh` are untouched.

## Evidence (red first, run counts)

- Against the unchanged script the 4 allowing rows fail (5 failure records, of 29 `LiveCheck` rows); with the change all 29 pass. 10 planted over-allowing copies of the script (wider hex, `match`/`search` for `fullmatch`, allowance on the API, an open-ended tail, upper-case hex, any folder for `$`, always-print count, an unescaped dot, any route type) each turn at least one row red; the unmutated copy passes.
- `test_deploy_hpsmpoc208`: 35 tests before, 42 after, on python 3.14 and on 3.9.
- Infra suite: 325 before, 332 after; by test id lost 0, added 7, changed 0. `validate.sh` rc 0 at the change, `ResourceWarnings: 0`, `Files still open: 0`. `test_deploy_package`: 44 at both.
- The diff is exactly three files.

Nothing deployed; no integration with HP tools (Security Manager API, Fleet Threat Assessment, firmware tools, SIEM). The first deploy after this lands is the real proof.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
