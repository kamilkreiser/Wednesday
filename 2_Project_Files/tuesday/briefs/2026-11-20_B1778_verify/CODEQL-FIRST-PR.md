# CodeQL and the first pull request of datasecau/OXPd_2: round 2, changed or unchanged

Read 2026-11-20 15:30 AEDT by `gh api -X GET` under the project's own login. Nothing was changed; no pull request was opened.
**The round-1 answer stands whole** (`2026-11-20_B1772_verify/CODEQL-FIRST-PR.md`: its four lines, its steps and who does each).
Nothing GitHub shows has changed except the head the checks sit on. This file is the re-read and the re-run.

## The answer, unchanged, in four lines

1. No CodeQL analysis will run on the first pull request: the default setup still lists no language.
2. Whether the ruleset then BLOCKS the merge is still UNMEASURED; expect "blocked", read it in one call after the pull request
   is opened (`pulls/<n>`: `mergeable_state`), and take `blocked` on a green pull request to the product owner as ONE question.
3. Once the code is on `main`, the default setup is expected to pick up C#, Python and the workflow language by itself.
4. No seat and no file in the repository can change any of this: the setup is enforced from above the repository and the
   ruleset has no bypass.

## The API facts of round 1, re-read

| Call | Round 1 | Now | |
|---|---|---|---|
| `rules/branches/main` | 4 rules from ruleset `24139430`: `deletion`, `non_fast_forward`, `code_scanning` (CodeQL, alerts `errors`, security alerts `high_or_higher`), `required_status_checks` with an empty list | the same 4, the same parameters | unchanged |
| `rulesets/24139430` | "Security scan rule", organisation, `active`, `bypass_actors` `[]`, `current_user_can_bypass` `never` | the same; target the default branch; last updated 2026-10-09 | unchanged |
| `rulesets?includes_parents=true` | (not listed) | 1 ruleset, that one | no second ruleset exists |
| `code-scanning/default-setup` | `configured`, `languages` `[]`, `query_suite` `extended`, `schedule` null, `updated_at` null | the same | unchanged |
| `code-security-configuration` | "SecurityPolicyConfiguration", `enterprise`, `enforced`, default setup `enabled`, secret scanning and push protection `disabled` | the same | unchanged |
| `code-scanning/analyses`, `code-scanning/alerts` | 404 "no analysis found" | 404 "no analysis found", both | unchanged |
| `languages` | `{}` | `{}` | unchanged |
| check runs on the lane head | 4 on `a0f9bdcc`, all GitHub Actions | 4 on `e0ddd0dc` (`linux`, `windows`, `secret-scan`, `rules`), all GitHub Actions, all success; none from CodeQL | **changed: the head only** |
| check suites on the lane head | (not listed) | 2: `github-actions` completed success with 4 runs; `xcode-cloud` `queued` with 0 runs (the same on round 1's head) | new observation, not a change: an installed app opens a suite and runs nothing. Wait on check RUNS |
| check runs on `main`'s commit | 0 | 0 | unchanged |
| `branches/main/protection` | "Branch not protected" | the same | unchanged |
| the login's rights | `admin: true` | `admin: true`, `push: true` | unchanged |
| the repository | (not listed) | private; squash, merge-commit and rebase merges all allowed; secret scanning and push protection `disabled` | squash is allowed, which the landing rule needs |
| refs and pull requests | 2 refs, 0 pull requests | 2 refs (`main` `7e1a01cf`, the lane branch `e0ddd0dc`), 0 pull requests of any state, 0 tags | **changed: the lane head only** |
| workflow runs | 1 (`44661506229`) | 2: `44661506229` on `a0f9bdc` and `44671776263` on `e0ddd0d`, both `push`, both success | one more run |

## The local CodeQL passes, re-run at the new head

CLI 2.27.4, the `security-extended` suite (the suite the default setup names), databases under the gate's own folder.

| Language | Queries run | Results at `e0ddd0d` | Proof the suite can fire |
|---|---|---|---|
| Python (the two build scripts and their THREE test files) | 50 | 0 | a planted world-writable `chmod` in a copy: 1 result, `py/overly-permissive-file` |
| The workflow (`actions`), with the new step | 23 | 0 | a planted injection in a copy: 1 result, `actions/code-injection/medium` |
| C# (unchanged in round 2 but for two project files losing four lines each) | NOT RUN | - | the extractor does not run on this machine ("Bad CPU type in executable"); hosted CodeQL is the only C# proof |

## What round 2 adds to the picture

- The new step and the new test file bring no local CodeQL result. Nothing in round 2 makes the first pull request more or
  less likely to be blocked.
- The pull-request event will start a second run of the same four jobs on the same head; the `secret-scan` job of that run
  checks out the merge commit and reads every branch and tag of the origin (UNMEASURED on a pull request; DERIVED from the
  hosted fetch line of the push run and the action's `fetch-depth: 0`).
- Exit point E0.4 names CodeQL. Until an analysis exists on `main`, that clause of WP0.3 is OPEN.
