## What a wrong value could do unseen before

The infra test read only the NAMES of the seven app settings the template computes (audience, scope, instance, tenant, allowed hosts and the two sign-in ids) and left four literals unread. A changed audience built from the wrong id, a changed login endpoint, or two ids swapped in the module call compiled cleanly and left the whole test file green. Ten of thirteen such one-line changes were invisible to the old file (the other three tripped only the unused-parameter warning test).

## What the test now refuses

- Any of the six computed settings whose compiled expression differs from the committed one, and an allowed-hosts value that is not the site's own default host name (the site API version in it may change).
- Any of the four literals (container start time limit, build-on-deploy flag, app-service storage flag, catalogue overlay path) that differs from its committed value.
- A module call that gives either sign-in id to the parameter of the other name.
- Each of these is proved red by a changed line of the template source compiled again, and by a changed value of the compiled template. The test count goes from 35 to 43.

## What did not change

Only `infra/tests/test_infra.py` changes (145 lines added, none removed). No template, no hosted setting, no name list and no other file changes. Nothing is deployed and nothing in Azure is touched. No id, tenant or host name is written to the file.

## What is left on the ticket

The seven unpinned properties of the site itself (always on, HTTP/2, remote debugging, 32-bit worker, startup command, client affinity, public network access) are a follow-up. The test also cannot see a setting changed by hand on the hosted site.

Tests: the 15 python test files of the CI step all pass at this head (388 tests; 380 at the base).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
