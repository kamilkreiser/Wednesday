# CodeQL and the first pull request of datasecau/OXPd_2: the plain answer

Read 2026-11-20 13:54 AEDT by `gh api -X GET` under the project's own login. Nothing was changed; no pull request was opened.
Marks: MEASURED = printed by the gate today; DOCUMENTED = GitHub's documented behaviour as the gate knows it (the documentation was
NOT re-read today: no host but the API was allowed); RELAYED = from the kit; UNMEASURED = nobody has seen it on this repository.

## The answer in four lines

1. **No CodeQL analysis will run on the first pull request.** The default setup lists no language, and it only analyses the
   languages it lists. (MEASURED state; DOCUMENTED behaviour; RELAYED: the same happened on the organisation's other repository.)
2. **Whether the ruleset then BLOCKS the merge is UNMEASURED.** The gate expects "blocked, waiting for CodeQL results" and the
   coordinator should plan for it. It is read in one call after the pull request is opened (below).
3. **Once the commit is on `main`, the default setup is expected to pick up C#, Python and the workflow language by itself** and
   analyse `main` within minutes; later pull requests then carry CodeQL results. (DOCUMENTED; RELAYED precedent; UNMEASURED here.)
4. **No seat and no file in the repository can change any of this.** The default setup is ENFORCED from above the repository
   (MEASURED), and the ruleset has no bypass (MEASURED). If the merge is blocked, the way through is one owner's ruling.

## What the API shows today (MEASURED)

| Call | Reading |
|---|---|
| `rules/branches/main` and `rulesets/24139430` | one ruleset, "Security scan rule", from the organisation, `active`; 4 rules: `deletion`, `non_fast_forward`, `code_scanning` (tool CodeQL, alerts threshold `errors`, security alerts threshold `high_or_higher`), `required_status_checks` with an EMPTY list; `bypass_actors` `[]`; `current_user_can_bypass` `never` |
| `code-scanning/default-setup` | `state` `configured`, `languages` `[]`, `query_suite` `extended`, `schedule` null, `updated_at` null |
| `code-security-configuration` | configuration "SecurityPolicyConfiguration", target type `enterprise`, status `enforced`, `code_scanning_default_setup` `enabled`, secret scanning and push protection `disabled` |
| `code-scanning/analyses`, `code-scanning/alerts` | 404 "no analysis found": no analysis has ever been uploaded |
| `languages` | `{}` (the default branch holds a README and a `.gitignore`) |
| check runs on the head `a0f9bdcc` | 4, all from GitHub Actions (`linux`, `windows`, `secret-scan`, `rules`); none from CodeQL |
| check runs on the first commit of `main` | 0 |
| `branches/main/protection` | "Branch not protected" (the ruleset is the only rule) |
| the login's rights on the repository | `admin: true` (so the account CAN reach repository settings; a setting is still not a seat's or a gate's to change) |
| the first push to `main` | accepted under this ruleset (the STATUS quotes the output; `main` reads the commit): the `code_scanning` rule did not refuse a branch-creating push with no analysis |

## What is expected when the pull request is opened

- The `ci` workflow runs on the `pull_request` event: 4 more check runs on the same head commit. (DOCUMENTED; UNMEASURED here.)
- No "CodeQL" or "Analyze (<language>)" check appears. (Expected from the empty language list.)
- The merge box either lets the merge through or reads that code scanning is waiting for results from CodeQL.
  **Read it, do not guess:**
  `gh api -X GET repos/datasecau/OXPd_2/pulls/<n> --jq '[.mergeable, .mergeable_state] | @tsv'`
  `clean` = mergeable; `blocked` = a rule holds it. Because the ruleset names no status check and no review, the ONLY rule that can
  hold a green pull request here is `code_scanning`, so `blocked` on a pull request whose checks are green IS the CodeQL answer.
  (`unstable` = a check is not green; `unknown` = ask again in a few seconds.)
- Why the gate expects `blocked`: DOCUMENTED, the rule needs results from the named tool for the commit and for the branch it
  targets, and a pull request whose tool never ran is held as "waiting"; RELAYED, on the organisation's other repository the first
  pull request showed no CodeQL check and its one unscanned merge needed the product owner's ruling. Against it: MEASURED, the same
  rule let the first push through with no analysis. So: UNMEASURED until read.

## If it reads `clean`

Merge by the landing line. Then, within about ten minutes, read and record:
`gh api -X GET repos/datasecau/OXPd_2/code-scanning/default-setup` (languages no longer empty: expected `actions`, `csharp`,
`python`), `gh api -X GET 'repos/datasecau/OXPd_2/code-scanning/analyses?ref=refs/heads/main'` (at least one analysis per language)
and `gh api -X GET 'repos/datasecau/OXPd_2/code-scanning/alerts?state=open'` (expected 0; any alert is fixed forward by a lane, never
dismissed). If the languages stay empty after an hour, that is a question for an organisation owner, not a seat.

## If it reads `blocked`: the smallest correct way, and who does each step

The knot: the default setup lists a language only after code in that language is on `main`; code reaches `main` only by a merge;
the rule holds the merge until CodeQL has results. Nothing inside the repository unties it.

| Step | Who | What |
|---|---|---|
| 1 | the coordinator | Take it to the product owner as ONE question with the facts above. Change nothing meanwhile; do not close the pull request |
| 2 | an organisation owner (the product owner's click, or the administrator he names) | For this ONE merge, let the ruleset through: set the organisation ruleset "Security scan rule" to evaluate mode (or add one bypass actor, or exclude this repository), nothing else. This is the same one unscanned merge the organisation already ruled once for its other repository (RELAYED) |
| 3 | the coordinator | Merge by the landing line (squash, head pinned) while step 2 holds |
| 4 | the same owner | Put the ruleset back exactly as it was (active, no bypass). The coordinator reads `rulesets/24139430` and compares it with the table above |
| 5 | the coordinator | The three reads of "If it reads clean". From then on every pull request carries CodeQL results and the rule works as meant |

What the gate can offer the product owner in place of the missing hosted result, for that one merge (MEASURED today, local CodeQL
CLI 2.27.4, the `security-extended` suite, which is the suite the default setup names):

| Language | Queries run | Results at the head | Proof the suite can fire |
|---|---|---|---|
| Python (the two build scripts and their two test files) | 50 | 0 | a planted world-writable `chmod` in a copy: 1 result, `py/overly-permissive-file` |
| The workflow (`actions`) | 23 | 0 | a planted injection in a copy: 1 result, `actions/code-injection/medium` |
| C# (3 files, 30 lines in all) | NOT RUN | - | the C# extractor does not run on this machine ("Bad CPU type in executable"); read by hand: no input, no file access, no process, no query |

## The ways that are NOT the smallest, and why

- **An advanced-setup workflow (`codeql.yml`) in the repository.** The default setup is enforced by an enterprise-level
  configuration (MEASURED: status `enforced`); DOCUMENTED, a repository cannot switch to advanced setup while that holds, and an
  advanced workflow beside an active default setup is refused. It needs a larger owner's change than step 2, and `main` would still
  have no analysis to compare with.
- **Choosing the languages by hand in the default setup.** DOCUMENTED, the setup offers only languages found on the default
  branch; today that is none. UNMEASURED whether an owner can force one.
- **Putting the code on `main` another way** (a direct push, a second "first commit"). Forbidden by the project's rules; the gate
  names it only to say no.
- **Uploading a result file made by a local run.** A write to the repository's security data by a seat, with no C# result in it.
  Not a seat's, and not honest as "CodeQL green".

## What stays true whatever the reading

- Exit point E0.4 names CodeQL. Until an analysis exists on `main`, that clause of WP0.3 is OPEN.
- The four `ci` checks are not required by any rule (the list is empty). A green CodeQL result does not make them required.
