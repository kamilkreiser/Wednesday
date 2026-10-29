STARTABLE: YES (pins hold: main c00e28284e9acacf16462ea3c2b533936b3db210, 0 open PRs, no b886 ref, no pane H52, ports 9720-9729 unlistened; the local clone's hold on c00e2828 is unmeasured, the seat fetches if absent)

# B886 DRAFTER REPORT (builder kit for Datasec/HPSM-POC-H52: HPSMPOC-363 README line 232, HPSMPOC-364 binding rules)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-29_B886_SEAT-H52_hpsmpoc-363-364-infra-readme-and-binding-rules.md` (147 lines). Shape: the stamped B858 and B859 kits. Read-only: scratchpad runs only, no git verb in the project tree.

## Facts re-derived against main (not copied from the sweep)
- README: 241 lines, line 232 holds `Each of the two has its own key:` once (148 chars, ASCII). Only `test_deploy_package.py` reads the README (lines 474, 520, 686; 8 mentions); `test_env_value.py` has one comment mention; no test reads the "two locks" paragraph.
- Test file: 2244 lines, rule at 1067, `RULES` 1088-1094 (24 entries), `class Baseline` 1097, `mutate_main_variable` 1401 (already exists: kit says reuse), `SHOWCASE_RULES` 2097, 107 test methods.
- Plants g1, g2, g3a, g3b, g4, g4b (plus two deleted-binding shapes) all read 0 red under the 24 rules on the compiled template; control `allowBlobPublicAccess` reads `rule_storage` red.
- b885 branch: 3 `web/` files, 0 under `infra/`.

## Corrections to the sweep
- "23 rules" in the ticket is now 24 (the 358 rule landed): kit uses 24 and 25.
- Sweep said the README coupling was not re-fetched: now measured (see above).
- Sweep gave the test file as 2244 lines and the rule at 1067: both confirmed. Ticket says plants g1..g4; the gate evidence and BLUF also name g4b: kit includes it.

## Q-questions for Tuesday at stamp (default in brackets)
- Q-1 Gate round [NO GO 0 of 2, tier 2, round 1 of 2].
- Q-2 Additive new rule, existing rule untouched [yes].
- Q-3 g4b in scope (needs per-environment evaluation; a text reader cannot see it) [yes, ticket Done-when names it].
- Q-4 One PR, two commits, squash [yes].
- Q-5 No Jira write by the seat [yes].

## Unmeasured
Whole-infra run and test count at c00e2828; runner Python; whether the clone holds the base; a built rule (the g4 structural and g4b masked-evaluation readings are measured on inputs only); the step-7 README control row.
