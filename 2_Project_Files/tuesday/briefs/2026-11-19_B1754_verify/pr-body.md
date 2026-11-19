## What the settings file did before

`infra/modules/showcase.bicep` replaces every app setting of the showcase site on each apply. It did not hold
`MpsCalc__Feedback__Path`, which was set on the site by hand, so the next apply would have removed it and turned
feedback off (every submission would answer 503). Both client id parameters defaulted to empty, and the parameter file
fell back to empty when the id variables were unset, so an apply without them would have blanked four sign-in
settings. The budget start date defaulted to the first day of the month of each apply, so each apply moved it.

## What it does now

- The file sets `MpsCalc__Feedback__Path` to `/home/data/feedback/`, the value the site was given by hand.
- The two client id parameters have no default and a length of 36. The parameter file reads `MPSCALC_API_CLIENT_ID`
  and `MPSCALC_SPA_CLIENT_ID` with no fallback: when either is unset the compile stops (BCP427), and an empty or
  wrong-length value is refused (BCP333 / BCP332). The two ids must be supplied or the step stops. The rule is a
  length rule: any 36-character value passes, so the right ids are still the deploy's to check.
- The budget start date is the literal `2026-10-01`, the existing budget's start.
- A committed list `infra/env/showcase.app-setting-names.txt` holds the 18 setting names (names only), and
  `infra/tests/test_infra.py` fails when the file's names and the list differ. New rows also pin the feedback path,
  the budget date and the id parameters' shape.
- `infra/README.md` and the hosted configuration section of `docs/API.md` say what the file does.

## Measured difference against the names saved on 16 November

The names in the file were compared with the 17 setting names saved from the site on 16 November (names only):

| | Names in the file | Added | Removed |
|---|---|---|---|
| main | 17 | `MpsCalc__Templates__Path` | `MpsCalc__Feedback__Path` |
| this change | 18 | `MpsCalc__Templates__Path` | none |

The literal values the file shares with the saved set are equal, and the sign-in settings are equal when the same ids
are supplied. The live site is NOT read by this change: whether it still holds exactly those names and values today is
for the next deploy to measure.

## What the new test can and cannot see

It sees the compiled template: the setting names against the committed list, the feedback path, the budget default and
the id parameters' shape. It cannot see the hosted site (a setting put there by hand is invisible to it), a changed
value of the expression settings, or whether the ids supplied at deploy are the right ones.

## What the next deploy must prove before any write

- The live setting names equal the committed list minus `MpsCalc__Templates__Path`, and the live feedback path equals
  `/home/data/feedback/` (by hash).
- The supplied client ids equal the live ones (by hash), so the four sign-in settings do not change.
- The what-if shows only the added templates setting on the app settings and no change to the budget start date.
- Run once without the id variables, the step stops at the parameter file before any request.

Nothing is applied and nothing is deployed by this change. Tests run locally: `infra/tests/test_infra.py` 35 OK,
`infra/tests/test_validate_script.py` 6 OK, `scripts/tests/test_deploy_pre1.py` 44 OK.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
