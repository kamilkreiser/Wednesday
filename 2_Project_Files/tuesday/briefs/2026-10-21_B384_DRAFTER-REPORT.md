# B384 drafter report (2026-10-21 ~07:51 AEDT)

Brief: `2026-10-21_B384_SEAT-D16_hpsmpoc-lane5-ci-e2e.md` (139 lines). Shape copied from B372 plus the skeleton's PROVENANCE / SELF-CHECK lines. Read-only drafter: `gh api` GETs, `git ls-remote`, Jira GET; no dotnet, npm, Playwright, no Jira write, no HTTP to hosted.

## Stamp slots
Two, both in the Stamp paragraph: `@MAIN@` (main sha) and `@STAMP@` (stamp time, launch authority, answered questions below). Stamped copy must read 0 by `grep -o -E '@[A-Z_]+@' | wc -l`. The drafter made no `.pre-stamp` copy (fence): Tuesday copies the file before stamping (control reads 2; MEASURED on the brief now: 2).

## What changed the lane (the plan assumed five builds; two are already built)
- **-155 is built.** ci.yml at main `54fbceac` has `api-sqlserver-shard` (:163-333) and `api-sqlserver` (:337-349); Jira -216 is Done and "extends -155". The brief turns -155 into evidence plus an OPTIONAL separate-branch shard split.
- **-109 O-2 is built and merged** (PR #105, `infra` job, pinned shellcheck; `test_ci_workflow.py` `ShellScripts`). Brief: evidence only; ticket stays open for O-1 (Kam's).
- **Main CI at `54fbceac` is RED** in the SQL Server shard on `RequestTimingLogTests` (window 900-1250 ms, actual 1384). Not Lane 5's file (Lane 1 family). Put in FOR TUESDAY.
- **-297 is readable in code**: `showcase.sh:70` gives the dev user `Partner,Demo`; `ReportingEndpoints.cs:412-418` re-renders an issued report by alias for Demo, so a different sha is by design. A reading, not a measurement; the brief makes the seat measure with a discriminating arm (Partner only) and STOP if the sha still differs.
- **No live-API spec runs in CI**; so -296's "runner" is a new LOCAL runner. CI wiring is out of scope.

## Measurements (instrument + control)
| What | Instrument | Result | Control |
|---|---|---|---|
| Main sha | `git ls-remote origin refs/heads/main`, 07:47:55 | `54fbceac12393f503fae8c5810af9609bac44548` | local `origin/main` read `6818896b`, i.e. the local ref is stale; all code read through `gh api ?ref=` |
| ci.yml | `gh api` raw at main | 664 lines, sha256 `32c18bd9d3df...` | read whole; line cites above are from that copy |
| CI wall clock, newest 8 main pushes | actions runs, `updated_at - run_started_at` | 988, 980, 974, 924, 900, 892, 835, 834 s; 5 of 8 at or over 900 s; median 912 | run 39488366465: latest job end minus earliest job start = 976 s vs run 980 s |
| Critical path | actions run jobs, `completed_at - started_at` | `api on SQL Server (api-other-and-feedback)` 980 and 969 s; `(api-assessment)` 903 and 843 s; `api` 891 and 563 s | same cross-check; step list of the 980 s job: Api non-Assessment tests 10 m 1 s, then Feedback tests 3 m 46 s (226 s) in sequence |
| Red on main | job log of job 118866460991, ANSI stripped | 1 failed / 642 (RequestTimingLogTests, `Assert.InRange` 900-1250, actual 1384); Feedback 302/302 passed | other 7 of the last 8 main runs: success |
| Open PRs | `gh pr list --state open`; `pulls?state=open --jq length` | empty; 0 | merged-list control NOT run (listed in the brief for the seat) |
| Tracked shell scripts | git tree at main | 6 `.sh`; executable blobs outside `.tools/` also 6 | not cross-checked at another ref (seat does it) |
| Tickets | Jira GET | -271 / -296 / -297 / -109 / -155 all Backlog; -271 2 comments, -109 2 comments, -155 2 links (both Done) | `jira.py`, `post.py`, `read.py` present in `.tools/b300` |
| Load | `uptime` 07:47:55 | 10.53, 11.07, 8.63 (over the 8 line) | none |
| Ports 7440-7449 | `lsof` | no listener | no positive control run |

Not measured: any CI run time after a change (cannot be done locally), the -297 arms, whether the API exposes showcase mode or a fresh-seed marker (decides -296 clause b), the 900 s line's written source.

## Proposed model row and checks
**Sonnet 5.5, row C2** (`model-routing.md:92`), launch with `BRIEF_SEAT_LEVEL=sonnet`. **P1: the pin's owner is authority that would originate with the coordinator, so it needs Kam's card** (see Q1). P2/P3 are Tuesday's gauge check. P4: no local tier for Datasec. **Gate tier 2 (G2, config/CI/tests)**, tier 1 and STOP if any `api/src` path, any `permissions`/`secrets`/`uses` change in ci.yml, or -297 reaches Reporting.

## Questions for Tuesday (recommended answers)
1. **Q1. Who owns the Pkcs pin, and on what cadence?** Recommend: raise a card to Kam now (P1). Default text: owner role = the Datasec coordinator seat; cadence = on each .NET servicing release (second Tuesday of the month, 10 Nov next; derived from the calendar, not from a Microsoft source) plus whenever the early-warning test turns main red. Quote the ruling in `@STAMP@`. If no ruling by launch, the brief already makes -271 skipped and starts at -296.
2. **Q2. Accept that -155 and -109 O-2 become evidence, not builds?** Recommend YES (finding 1, 2 in the brief). The brief tells the seat to refute them at source in PRIOR WORK before it relies on them.
3. **Q3. The optional -155 step (a third SQL Server part for the Feedback tests, parallel, separate branch)?** Recommend: leave it OPTIONAL and last. It is the only change in this lane that could bring CI under 900 s (about 226 s off the slowest shard on paper), but it cannot be proven locally and it edits a required-adjacent workflow. Land it only after its own PR CI shows the time.
4. **Q4. Who deals with the red `RequestTimingLogTests` on main?** Recommend: rerun the failed job once (your call, I did not), and if it recurs, a ticket for the Lane 1 seat to widen or de-clock the window. Not this lane; the brief fences the file.
5. **Q5. Is the 900 s line a hard line?** Recommend: tell the seat the true number. Five of the last eight runs are already at or over 900 s on main with nothing added, so "fit inside 900 s" is only meaningful as "do not add to the critical path". The brief says that.
6. **Q6. Tier 2 for the PR, or tier 1 for the workflow edit?** Recommend tier 2 for commits 1-3 (comments, a runner, a spec), your choice of tier 1 for the optional shard-split branch.
7. **Q7. Five Jira comments allowed (one per ticket, after push read-back, no transitions)?** Recommend YES, as B372 allowed one. The -109 and -155 comments only state what is already on main.
8. **Q8. May the seat download the pinned shellcheck (sha256-checked, into its own folder)?** Recommend YES: shellcheck is not on the laptop's PATH (MEASURED) and a new runner script would be checked by CI's `infra` job; a Python runner avoids the question and the seat may choose it.

## Could not verify
- Whether the seat can read the mode or the user from a read-only API surface: depends on code the drafter did not open (`/api/v1/me`, health).
- Whether `.tools/actionlint` runs (a tarball and a directory exist).
- Panes live, `AGENTMAIL_API_KEY` presence (relayed from B378), the `B150-B153` STATUS file names (listed "if present").
- Whether the earlier -271 clause "early-warning test" is still green at main (RELAYED from the 2026-10-19 comment).
