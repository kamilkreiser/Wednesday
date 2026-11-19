# B1731 tooling commission — a tracked PR-CodeQL check for gates (Tuesday's own tooling)

Owed by the Tuesday ledger row of 2026-11-19 (gate B1727 measured "CodeQL 0 new" by result ROWS; hosted CodeQL then
blocked NexusAI PR 229 with 5 high alerts that main already held, because the hosted PR check keeps any result whose
data-flow path touches a line the PR ADDS). The B1728 drafter proved the rule locally with ad-hoc scripts in
`2_Project_Files/fleet/state/s291/d1728/work/` (analyze.sh, mkdb.sh, mkdiffpack.py, difffilter.py, cmp.py; gitignored,
hardcoded to that scratch dir and to the five specific alerts). Its outputs are in `.../d1728/raw/` (incl. the hosted
SARIFs hosted_main.sarif and hosted_pr229.sarif) and its report is `2_Project_Files/tuesday/briefs/2026-11-19_B1728_DRAFTER-REPORT.md`.

## Build
A tracked, generic tool in `2_Project_Files/tuesday/tools/codeql/` (create the dir; self-locating scripts; macOS bash 3.2
compatible; never discard stderr):
- `pr_codeql_check.sh --repo <owner/name> --checkout <path to a local clone, READ ONLY> --base <sha> --head <sha> --lang <javascript|python|csharp|...> --work <scratch dir>`
  1. exports both trees with `git --no-optional-locks -C <checkout> archive <sha>` into <work>/trees/{base,head} (never
     checkout/worktree/fetch in the checkout: other projects' repos are read-only to this seat);
  2. builds a CodeQL database for each (CLI `2_Project_Files/tools/codeql/codeql/codeql`, reuse a DB if it exists for that sha);
  3. analyzes each with the language's security-extended suite to SARIF;
  4. builds the diff pack (added-line ranges of head vs base) and applies the post-filter on the HEAD SARIF: every result
     at severity high or above (security-severity >= 7.0 or the rule's problem.severity error, state which you used)
     whose primary OR any related location START line is an added line -> KEPT;
  5. compares (ruleId, file, primaryLocationLineHash) multisets head vs base: NEW and GONE;
  6. prints a verdict table and exits 0 only if KEPT(high+) = 0 and NEW(high+) = 0; rc 1 = would block; rc 2 = tool error
     (never a silent pass: a run with 0 results on either side when the other has >0 is rc 2 unless --allow-empty).
- A `README.md` saying what it reproduces, what it does NOT (it is a local approximation of the hosted check; the hosted
  run at landing stays the authority; name that residual).

## Prove it (arms; red first)
Use NexusAI (`datasecau/Reporting_Dashboard_Au`), checkout `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/2_Project_Files`
(verify the path; read-only), base 37fb1bcbec2e19f2404774633349da76b75120d3:
- RED arm: head cd019f382c63589c735b0b0bf1add22bfdebec10 (PR 229 round 1) must give rc 1 with the five kept results
  (js/user-controlled-bypass at server.js around 3620/3631 and js/http-to-file-access jsonStorage.js:524), matching the
  hosted_pr229.sarif failure.
- GREEN arm: head 2ec6937792ffc48abbd11a2928b293c954e14cd5 (round 2, merged clean on hosted CI) must give rc 0.
- NULL arm: base vs base gives rc 0 with NEW 0.
- TOOL-ERROR arm: a bogus sha gives rc 2 with the git error printed.
Existing DBs for main(37fb1bcb)/head(cd019f38) may be reusable from `.../d1728/db/` — check what each was built from
before reusing (dbcreate logs); building fresh is fine. Load: run one CodeQL process at a time, --threads=4.
Scratch: `2_Project_Files/fleet/state/s292/d1731/`.

## Also deliver
- `2_Project_Files/tuesday/tools/codeql/GATE_STEP.md`: the exact text block a gate commission pastes as its CodeQL step
  (command line, how to read the table, that rc 1 is a Major / landing blocker, that rc 2 must be resolved, the residual).
- A `.gitignore` check: nothing under tools/codeql/ that is generated (DBs, SARIF) may land there; outputs go to --work.
- Report: `2_Project_Files/tuesday/briefs/2026-11-19_B1731_TOOL-REPORT.md` with each arm's command, rc and printed table.

## Limits
No writes outside `2_Project_Files/tuesday/tools/codeql/`, the report file and your scratch dir. No GitHub or Jira writes.
No `cd` in Bash (hook refuses; absolute paths). zsh shell: no PIPESTATUS. Do not commit; Tuesday reviews and commits.
