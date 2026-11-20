# CodeQL and the pull request of the logging lane (datasecau/OXPd_2, head 2c231b4)

Read 2026-11-20 18:55 AEDT by `gh api -X GET` under the project's own login. Nothing was changed; no pull request was opened.

## The answer, in four lines

1. **Code scanning will run on this lane's pull request, for the first time on any pull request of this repository.** Since
   the first merge the organisation's default setup lists `csharp` and `python` (it listed nothing before), with the EXTENDED
   query suite. The first pull request ran before that and carried no code-scanning row.
2. **Expected result: 0 alerts from this change, test code included.** That is a reading of the query sources, not a run:
   the C# extractor cannot run on this machine. Only the hosted check on the pull request proves it.
3. The rule on `main` blocks a merge on a CodeQL alert of severity error, or a security alert of high or above. If the hosted
   check reports one, it is fixed in the code by a new commit and gated again. It is never dismissed and the rule is never
   bypassed (the ruleset has no bypass actor).
4. What is still UNMEASURED: which rows the pull request shows and what `mergeable_state` reads. `landing.txt`, line 1, holds
   the two calls that read them.

## Why 0 alerts is expected (the hand rows; query pack `csharp-queries` 1.11.0, library `csharp-all` 7.4.2, read on this machine)

The question the commission asks: does test code that hands values NAMED like credentials to a logger draw a clear-text
alert at high or above?

- The query is `cs/cleartext-storage-of-sensitive-information` (security severity 7.5, in the suite). Its sinks include every
  argument of a call on a type that extends something named `ILogger` (so every `Log.Information(...)` argument of these
  tests IS a sink) and file writes. Its sources are "sensitive expressions": a read of a VARIABLE whose name matches
  `password`, `passwd`, `account...id`, `account...key`, `licen[cs]e...key`, `voucher...code` or `trusted`; a call to a METHOD so
  named; or any method call that has an ARGUMENT whose constant text matches. **The words `token`, `secret`, `pwd`, `card` and
  `handle` are not in that list for C#.**
- In the 1908 added lines the pattern matches on 8 code lines. None gives a path:
  - no variable, parameter, field or method of the change is named with a matching word (the test values are `Class1Value`
    to `Class6Value`, `value`, `marker`; the builder named them neutrally on purpose);
  - the calls that carry a matching constant (`AssertRemoved(..., "password")`, `Assert.Contains("...Password...")`,
    `log.Information("Class six {Password}", ...)`) all return nothing, so no value flows out of them;
  - the property `Password` of the anonymous objects in L04 is only written, never read by the code;
  - the constant `Class6Value` holds the word `password` in its TEXT; it would make a call a source only if that call
    returned a value that reached a sink; the one method call that takes it (`AssertRemoved`) returns nothing, and its
    other uses are an attribute argument, an array element and the member of the anonymous object.
- `cs/hardcoded-credentials` (9.8): its sinks are arguments of LIBRARY parameters and LIBRARY property setters named like a
  password, user name or certificate, and comparisons against such a variable. The change calls none and compares none.
- The other queries of the suite need a remote source (a web request); the change has none. The scanner holds no regular
  expression, so the two regular-expression queries have nothing to read.

**A trap for the lanes that follow, to put in their kits:** a C# variable, parameter, field or method whose NAME holds
`password` or `passwd` (also `accountid`, `accountkey`, `licensekey`, `trusted`), passed to any logger method, to a file write
or to a trace call, is an alert at 7.5, in test code too, however fake the value. Name the thing for what it is
(`fakeValue`, `class6Value`); never dismiss.

## The API facts: changed or unchanged against the earlier rounds' table

| Call | Earlier rounds (last read 16:54) | Now (18:55) | |
|---|---|---|---|
| `rules/branches/main` | 4 rules from ruleset `24139430`: `deletion`, `non_fast_forward`, `code_scanning` (CodeQL, alerts `errors`, security alerts `high_or_higher`), `required_status_checks` with an empty list | the same 4, the same parameters | unchanged |
| `rulesets/24139430` | "Security scan rule", organisation, `active`, `bypass_actors` `[]`, `current_user_can_bypass` `never`, updated 2026-10-09 | the same | unchanged |
| `code-scanning/default-setup` | `configured`, `languages` `[]`, `query_suite` `extended`, `schedule` null, `updated_at` null | `configured`, **`languages` `["csharp","python"]`**, `query_suite` `extended`, `schedule` `weekly`, `updated_at` 2026-11-20T06:06:25Z (two minutes after the first merge), threat model `remote` | **changed** |
| `code-scanning/analyses` | 404, no analysis | 2 on `refs/heads/main` at `7bf37526`: `/language:csharp` (63 rules, 0 results) and `/language:python` (50 rules, 0 results), CodeQL 2.27.4 | **changed** |
| `code-scanning/alerts` | 404 | 0 open, 0 of any state | **changed** (the list exists and is empty) |
| `languages` | `{}` | Python 44873, C# 744, Dockerfile 360 (bytes, of `main`) | **changed** |
| check runs on `main`'s commit | 0 | 7: `linux`, `windows`, `secret-scan`, `rules`, `Analyze (csharp)`, `Analyze (python)` each success; `Adjust Configuration` skipped; all GitHub Actions | **changed** |
| check runs on the lane head | 4 on the first lane's head | 4 on `2c231b44` (`linux`, `windows`, `secret-scan`, `rules`), each completed success; none from code scanning (a lane branch push starts none) | the head only |
| the first pull request (number 1, merged) | did not exist | its head carried 8 rows: the four jobs from the push event and the four from the pull_request event; 0 code-scanning rows | new fact |
| workflows | 1: `ci` | 2: `ci`, and the dynamic `CodeQL` (`dynamic/github-code-scanning/codeql`), active | **changed** |
| workflow runs | 3 | 7: four pushes of the first lane, its pull_request run `44684936169`, the push to `main` `44685196570`, the dynamic `CodeQL Setup` on `main` `44685211085`, and this lane's push `44695261723`; each success | more runs |
| `branches/main/protection` | "Branch not protected" | the same | unchanged |
| the repository | private; squash, merge-commit and rebase merges allowed; default squash title the commit's or the pull request's title, default message the list of commit messages; the branch is not deleted on merge; secret scanning and push protection disabled | the same; `code_security` reads enabled | unchanged |
| the login's rights | `admin: true`, `push: true` | the same | unchanged |
| refs, pull requests, tags | 2 refs, 0 pull requests, 0 tags | 3 refs (`main` `7bf37526`, the first lane's branch `6e2629bc`, this lane's `2c231b44`); 1 pull request, closed and merged; 0 open; 0 tags | changed as expected |

## The local passes at this head

CLI 2.27.4, the extended suite (the suite the default setup names), databases under the gate's own folder.

| Language | Queries | Results at `2c231b4` | Proof the suite can fire |
|---|---|---|---|
| Python (unchanged by this lane, byte-equal to `main`) | 50 | 0 | a planted world-writable `chmod` in a copy: 1 result, `py/overly-permissive-file` |
| C# (the whole of this lane) | **NOT RUN** | - | the extractor does not run on this machine ("Bad CPU type in executable", 1 line in the create log; create rc 2). The hand rows above are the floor; **hosted CodeQL is the only C# proof** |
| The workflow language | not run this round | - | the default setup does not list it, and this lane changes no workflow file |
