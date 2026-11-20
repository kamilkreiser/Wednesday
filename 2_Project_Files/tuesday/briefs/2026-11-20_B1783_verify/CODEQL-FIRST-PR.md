# CodeQL and the first pull request of datasecau/OXPd_2: round 3, changed or unchanged

Read 2026-11-20 16:54 AEDT by `gh api -X GET` under the project's own login. Nothing was changed; no pull request was opened.
**The round-1 answer stands whole** (`2026-11-20_B1772_verify/CODEQL-FIRST-PR.md`: its four lines, its steps and who does each),
and so does round 2's table (`2026-11-20_B1778_verify/CODEQL-FIRST-PR.md`). Nothing GitHub shows has changed except the head
the checks sit on and one more workflow run. This file is the re-read and the re-run.

## The answer, unchanged, in four lines

1. No CodeQL analysis will run on the first pull request: the default setup still lists no language.
2. Whether the ruleset then BLOCKS the merge is still UNMEASURED; expect "blocked", read it in one call after the pull request
   is opened (`pulls/<n>`: `mergeable_state`), and take `blocked` on a green pull request to the product owner as ONE question.
3. Once the code is on `main`, the default setup is expected to pick up C#, Python and the workflow language by itself.
4. No seat and no file in the repository can change any of this: the setup is enforced from above the repository and the
   ruleset has no bypass.

## The API facts, re-read

| Call | Round 2 | Now | |
|---|---|---|---|
| `rules/branches/main` | 4 rules from ruleset `24139430`: `deletion`, `non_fast_forward`, `code_scanning` (CodeQL, alerts `errors`, security alerts `high_or_higher`), `required_status_checks` with an empty list | the same 4, the same parameters | unchanged |
| `rulesets/24139430` | "Security scan rule", organisation, `active`, `bypass_actors` `[]`, `current_user_can_bypass` `never`, the default branch, last updated 2026-10-09 | the same | unchanged |
| `rulesets?includes_parents=true` | 1 ruleset | 1 ruleset, that one | unchanged |
| `code-scanning/default-setup` | `configured`, `languages` `[]`, `query_suite` `extended`, `schedule` null, `updated_at` null | the same | unchanged |
| `code-security-configuration` | "SecurityPolicyConfiguration", `enterprise`, `enforced`, default setup `enabled`, secret scanning and push protection `disabled` | the same | unchanged |
| `code-scanning/analyses`, `code-scanning/alerts` | 404 "no analysis found", both | 404 "no analysis found", both | unchanged |
| `languages` | `{}` | `{}` | unchanged |
| check runs on the lane head | 4 on `e0ddd0dc`, all success, all GitHub Actions | 4 on `6e2629bc` (`linux`, `windows`, `secret-scan`, `rules`), all completed success, all GitHub Actions; none from CodeQL | **changed: the head only** |
| check suites on the lane head | `github-actions` completed success with 4 runs; `xcode-cloud` queued with 0 runs | the same two on the new head | unchanged (wait on check RUNS, never on suites) |
| check runs on `main`'s commit | 0 | 0 | unchanged |
| `branches/main/protection` | "Branch not protected" | the same | unchanged |
| the login's rights | `admin: true`, `push: true` | the same | unchanged |
| the repository | private; squash, merge-commit and rebase merges all allowed; secret scanning and push protection `disabled` | the same. Read for the first time: the default squash title is the commit's or the pull request's title, the default squash message is the list of commit messages; the branch is NOT deleted on merge | unchanged; two new observations (see `landing.txt`, line 2) |
| refs and pull requests | 2 refs (`main` `7e1a01cf`, the lane branch `e0ddd0dc`), 0 pull requests, 0 tags | 2 refs (`main` `7e1a01cf`, the lane branch `6e2629bc`), 0 pull requests of any state, 0 tags | **changed: the lane head only** |
| workflow runs | 2 | 3: `44661506229` on `a0f9bdc`, `44671776263` on `e0ddd0d`, `44680821033` on `6e2629b`, each `push`, each success | one more run |
| workflows | (not listed) | 1: `ci`, `.github/workflows/ci.yml`, active | no CodeQL workflow exists |

## The local CodeQL passes, re-run at the new head

CLI 2.27.4, the `security-extended` suite (the suite the default setup names), databases under the gate's own folder.

| Language | Queries run | Results at `6e2629b` | Proof the suite can fire |
|---|---|---|---|
| Python (the two build scripts and their three test files) | 50 | 0 | a planted world-writable `chmod` in a copy: 1 result, `py/overly-permissive-file` |
| The workflow (`actions`), with the new step | 23 | 0 | a planted injection in a copy: 1 result, `actions/code-injection/medium` |
| C# (unchanged in round 3) | NOT RUN | - | the extractor does not run on this machine ("Bad CPU type in executable", 1 line in the create log); hosted CodeQL is the only C# proof |

## What round 3 adds to the picture

- The third commit changes one workflow step, one test file and two README lines. It brings no local CodeQL result. Nothing in
  it makes the first pull request more or less likely to be blocked.
- The pull-request event will start a second run of the same four jobs. Its `secret-scan` job checks out the pull request's
  merge commit; by the pinned checkout action's source it fetches the branches, the tags and that one merge commit, and the
  second scan reads all of it (VERDICT.md, finding 1: DERIVED and modelled; UNMEASURED on a hosted pull-request run).
- After the squash the commit on `main` carries the message of `squash-subject.txt` and `squash-body.txt`, and from this change
  on that message is scanned by every run. It was scanned through the workflow's own function first: rc 0.
- Exit point E0.4 names CodeQL. Until an analysis exists on `main`, that clause of WP0.3 is OPEN.
