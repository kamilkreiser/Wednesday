# CodeQL and the pull request of the logging lane (datasecau/OXPd_2, head 6bcd02e): ONE HIGH ALERT, MEASURED LOCALLY

Read and run 2026-11-20, 20:17 to 20:36 AEDT. Nothing was changed on GitHub; no pull request was opened; no alert exists to dismiss.

## The answer, in five lines

1. **At this head the C# security suite reports 1 result: `cs/cleartext-storage-of-sensitive-information`, security severity
   7.5 (high), at `tests/Datasec.Suite.Logging.Tests/KeyValueShapeTests.cs` line 126.** Run by this gate on this machine with
   the CodeQL CLI 2.27.4 (the version the hosted analysis of `main` names) and the suite `csharp-security-extended.qls` (the
   suite the default setup names): 63 rules, 1 result.
2. The rule on `main` refuses a merge with a security alert of high severity or above. So the hosted check on a pull request
   of this head is expected to block the merge. The hosted check is the authority; this is a local run of the same queries.
3. It is test code and the value is synthetic. It is still never dismissed and the rule is never bypassed: it is fixed in the
   code by a new commit.
4. **The fix is one line** (two, to be safe), measured: with the key word of two test makers changed from `Password` to
   `Passphrase` (another listed name of the same class), the same run reports 0 results and the solution's 192 tests pass.
5. The first review could not run the C# extractor on this machine and read the queries by hand; its hand reading (0 alerts)
   was right for the first commit. The fix commit added the line that fires.

## The result, as the run printed it

| Tree | Rules run | Results | Detail |
|---|---|---|---|
| the head `6bcd02e` | 63 | **1** | `cs/cleartext-storage-of-sensitive-information`, 7.5; sink `KeyValueShapeTests.cs:126` (`harness.Log.Information(..., made)`); path `:90` -> `:125` -> `:125` -> `:126`; message: "This stores sensitive data returned by call to method Create ... as clear text." |
| the head with the two key words changed (a copy in the gate's scratch) | 63 | **0** | the control that the result comes from those lines, and the proof of the fix |
| `main` `7bf3752` | 63 | **0** | equals the hosted analysis of `main` (`/language:csharp`, 63 rules, 0 results, CodeQL 2.27.4, read by GET at 20:17): the local method gives the hosted number where a hosted number exists |

## Why it fires (the query's own source, read on this machine: `csharp-all` 7.4.2, `csharp-queries` 1.11.0)

- A source is any METHOD CALL that has an argument whose constant text holds `password` (`SensitiveMethodAccess`: "to pick up
  methods with an argument like password, which may indicate a lookup"). The call's RESULT is the sensitive value.
- A sink is any argument of a call on a type that has a base type named `ILogger`.
- Line 90 of the new test file is `case 17: return Tuple.Create("Password", s);`. The tuple is returned by `Make`, stored in
  `made` (line 125) and passed to `harness.Log.Information(...)` (line 126). Source to sink with no library step between.
- Every other maker of that cell builds its object with a constructor or an initialiser (not a method call), or with a
  non-constant argument, or with a method that returns nothing; line 76 (`ImmutableDictionary...Add("Password", s).Add(...)`)
  is a source by the same rule but the run reports no path from it. The first commit's calls that carry such a constant all
  return nothing (the first review's reading: confirmed by this run, which reports nothing else).

## The fix shape (a new commit on the branch; never a dismissal, never a suppression comment)

In `tests/Datasec.Suite.Logging.Tests/KeyValueShapeTests.cs`:

- line 90: `case 17: return Tuple.Create("Passphrase", s);`
- line 76 (not reported; changed so that a later version of the query cannot find the same shape):
  `case 10: return ImmutableDictionary<string, string>.Empty.Add("Passphrase", s).Add("Kept", Kept);`

`Passphrase` is a listed name of the class `password`, as `Password` is, so the cell tests what it tested: a value beside a
listed name in a tuple and in an immutable dictionary. Measured in the gate's work tree: build `0 Warning(s)`, `0 Error(s)`;
`total: 192`, `failed: 0`; the change undone and proved (`git diff --quiet` rc 0). This is a truthful name for a value that is
not sensitive, not a hidden literal: the query's list of words does not hold `passphrase`, and nothing is rebuilt at run time
to escape it. No number of any text changes (192 tests, 191 cells, 46 files).

**A rule for every later lane, to put in the kits beside the first review's rule:** in C#, test code included, a method call
with a constant argument that holds `password` or `passwd` (also `account...id`, `account...key`, `licen[cs]e...key`,
`voucher...code`, `trusted`) and whose RESULT reaches a logger call, a file write or a trace call is an alert at 7.5. Calls
that return nothing are safe; constructors and initialisers are safe; an argument that holds `invalid`, `crypt`, `hashed` or
`encrypted` is not counted.

## How the run was made (a correction for the gate standard)

The standard says the C# extractor cannot run on this arm64 machine (its launcher is an x86_64 program: confirmed again,
`Bad CPU type in executable`). **Its managed program can.** The gate copied the 42 managed files of the extractor that are
not part of the .NET runtime into its scratch, wrote a run-time settings file that names the shared runtime, and ran
`Semmle.Extraction.CSharp.Standalone.dll` with the project's own `dotnet` (10.0.404, arm64) inside
`codeql database trace-command --no-tracing` on a database made with `--build-mode=none`; then `database finalize` and
`database analyze`. 33 source files found, 333 references resolved, 0 unresolved, "Failed to resolve 2 types"; the references
came from the built outputs in the source copy (the extractor's own restore was refused by the closed local proxy the gate
runs every job under: its requests to the package source were refused at that local port and none left the machine). Programs and logs:
`/private/tmp/b1804-gate/codeql/` and `/private/tmp/b1804-gate/logs/cq-*.log`.

Residual, said plainly: a local approximation. The hosted analysis extracts with its own restore and may resolve types this
run did not; it can report MORE, not less, on these lines. Python: not re-run; `build/**` and the workflow file are byte-equal
to the first commit (the first review: 0 results of 50 queries, with a planted control).

## The API facts: changed or unchanged against the first review's table (read by GET, 20:17)

| Call | First review (18:55) | Now | |
|---|---|---|---|
| `rules/branches/main` | 4 rules from the organisation ruleset: `deletion`, `non_fast_forward`, `code_scanning` (CodeQL, alerts `errors`, security alerts `high_or_higher`), `required_status_checks` | the same 4 | unchanged |
| `code-scanning/default-setup` | `configured`, `["csharp","python"]`, `extended`, `weekly`, threat model `remote` | the same | unchanged |
| `code-scanning/analyses` | 2 on `main` at `7bf37526`: csharp 63 rules 0 results, python 50 rules 0 results, CodeQL 2.27.4 | the same 2 | unchanged |
| `code-scanning/alerts` | 0 open | 0 open | unchanged |
| check runs on the lane head | 4 on `2c231b44`, each success | 4 on `6bcd02ed` (`linux`, `windows`, `secret-scan`, `rules`), each success; none from code scanning (a branch push starts none) | the head only |
| refs | 3 | 6: `main` `7bf37526`, this lane `6bcd02ed`, the first lane's old branch, and three other lanes' branches | more branches |
| pull requests | 1 closed (merged), 0 open | the same | unchanged |

Not read again: the ruleset by its id, the workflow list, the repository's merge settings (no reason to think they moved; a
landing reads `mergeable_state` in any case: `landing.txt`, line 1).
