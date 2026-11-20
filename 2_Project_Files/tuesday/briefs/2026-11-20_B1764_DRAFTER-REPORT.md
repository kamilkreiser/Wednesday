STARTABLE: NO - the project has no .NET SDK (`<project>/.tools/dotnet` is absent and the machine has no `dotnet` on PATH), so the kit refuses at once until Tuesday places SDK 10.0.404 there; after that one placement and the stamp it is startable.

# B1764 DRAFTER REPORT | Datasec / OXPd_2: the first build kit (bootstrap and WP0.3) and the lane plan

Drafter: read-only, Fable, for Tuesday (s296). Window 2026-11-20 11:59:36 to 12:21 AEDT (clocks by `date`; the read clocks are in the kit's first line and the sidecar's first line). `<project>` = `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2`.

## Files
| File | What | Checked by program |
|---|---|---|
| `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_B1764_SEAT-X1_oxpd2-bootstrap-and-wp03.md` | the kit, 407 lines (`wc -l`) | `stamp_check.py` rc 0 (204 claims, 204 with a sidecar line); 59 of 59 quoted design sentences hold at their `file:line`; 9 four-underscore lines; the launcher block re-extracted: 137 lines, 7521 bytes, sha256 `ef365371...aefd16`, `/bin/bash -n` rc 0; ban-list name scan 0 hits (control fires); 0 decision-card ids |
| `...2026-11-20_B1764_SEAT-X1_oxpd2-bootstrap-and-wp03.md.measured` | the sidecar, 204 lines | 93 lines carry a run and its output; 7 are `file:line` pointers proven by the pointer check; 20 are frozen Jira text (their row citations checked against the plan's rows, 15 of 15 true); 1 is launcher text; 83 are instructions or names the seat writes, said so |
| `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_B1764_LANE-PLAN.md` | the lane plan, 66 lines | 45 of 45 quoted sentences hold at their `file:line`; 13 work-package rows, 8 difference rows, 5 wave rows, 6 flagged rows (each recounted by program) |
| `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_B1764_DRAFTER-REPORT.md` | this report | |
Scratch (not deliverables): `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s296/d1764/` (the launcher draft, the pointer check, the GET-only Jira reader, the saved text of `OXPD2-1` and `OXPD2-2`, the sibling workflow as fetched, two gitleaks logs, the claim lists).

## BLUF
1. **The design defines WP0.3 in one table row and one exit criterion and names no layout at all.** `03:136` and `03:69` are quoted whole in the kit. Neither `02` nor `03` names a folder layout, a CI product, a runner, a secret scanner, an SDK version or a test framework (word counts with a control in the sidecar). So thirteen things the kit needs are Tuesday defaults (D1 to D13), each a Question, none written as the design's word or the product owner's.
2. **The ruleset names NO required check.** `required_status_checks` reads `[]`. What it does require is CodeQL results, and CodeQL on this repository is the organisation's default setup with `languages` reading `[]`. So there is no workflow file a seat could write that "produces exactly those": the kit writes ONE workflow (`ci`, four jobs) and no CodeQL file.
3. **The first pull request may not be able to go green, and no kit can fix that.** On the sibling repository the first pull request ran 0 checks, CodeQL first analysed `main` two minutes after it merged, and the record says the product owner ruled that one merge unscanned and that the default setup is "controlled by organization administrators". The ruleset was last updated nine days after the sibling's first commit, has no bypass actor, and reads `current_user_can_bypass: never`. Whether it blocks an unscanned first pull request today is UNMEASURED. This is Q1 and it is the open point of the whole bootstrap.
4. **Whether the first commit to `main` is accepted is UNMEASURED too.** The only precedent (sibling, 2026-09-30, accepted, no GH013) predates the ruleset's last update (2026-10-09). The kit pushes once, reads the result, and on a refusal stops that step with the exact text and still does the launcher, the runbook, Jira and the records.
5. **Two clauses of WP0.3 are NOT built by this kit and the kit says so first in its READY:** "SPU in CI" with "a test bundle with the SPU" (HP's tool; no decision on how a runner gets it), and the real development-CA fingerprint (the certificate is not where report B3 says it is in the NAS copy: that folder lists 2 files and neither certificate). WP0.3 and E0.4 stay open on both.
6. **A security fact Tuesday should know:** the organisation's Actions secrets are visible to this repository's workflows by name, and the list starts `AZURE_CREDS`, `AZURE_CREDS_PROD`. The kit forbids any `secrets.` reference, `pull_request_target` and unpinned actions, and makes that a checked rule (R3, R4) with planted controls.
7. **The lane plan:** 13 rows (three are documents), five waves, critical path WP0.3 then WP1.1 then WP1.5 then WP1.4; six rows flagged for the pending correction pass; four questions that belong on `OXPD2-1` before their kits are written.

## Facts re-measured, with instruments
| Fact | Instrument (all GET or local reads) | Result |
|---|---|---|
| Repository state | `gh api -X GET repos/datasecau/OXPd_2`, `/branches`, `/git/refs`, `/pulls?state=all`, `/keys` under the project `GH_CONFIG_DIR` | private, size 0, `branches` `[]`, refs 409 "Git Repository is empty.", 0 pull requests, 1 deploy key (`read_only` false, `verified` true), created 2026-11-19T23:47:53Z |
| Ruleset | `/rules/branches/main`, `/rulesets/24139430` | 4 rules as the commission says; `required_status_checks` `[]`; `do_not_enforce_on_create` false; `bypass_actors` `[]`; `current_user_can_bypass` `never`; updated 2026-10-09T06:53:46.474+11:00 |
| Code scanning | `/code-scanning/default-setup` | `state` `configured`, `languages` `[]`, `query_suite` `extended` |
| Sibling precedent | sibling `Briefs/2026-09-30_B01_ADDENDUM-1...`, `2026-09-30_B01_STATUS.md:51-56`, `2026-10-01_B02_ADDENDUM-2...`; `gh api -X GET` on the sibling's pulls 1 and 2, check runs and analyses | first commit accepted 2026-09-30, "no GH013 refusal"; pull request 1: 0 check runs, merged; first analyses on `main` 22:04:38Z and 22:05:25Z, after the merge at 22:03:24Z |
| Actions settings | `/actions/permissions`, `/actions/permissions/workflow`, `/actions/runners`, `/actions/organization-secrets` (names), `/actions/secrets` | enabled, `allowed_actions` `all`, default permission `read`, 0 self-hosted runners, organisation secrets visible by name, 0 repository secrets |
| Action pins | `gh api -X GET repos/actions/checkout/git/ref/tags/v7.0.1`, `.../setup-dotnet/git/ref/tags/v6.0.0` | the two 40-hex shas the sibling workflow uses, equal |
| Toolchain | `command -v`, `--version` | no `dotnet`; `gitleaks` 8.30.1; `git` 2.54.0; the sibling's SDK folder prints 10.0.404 (arm64, 654M) |
| Secret-scan control | `gitleaks dir` on two scratch folders | planted token: rc 1, "leaks found: 1", token absent from the log; clean folder: rc 0, "no leaks found" |
| Jira | project, create screens, search (GET) | classic, 5 issue types, an Epic needs no epic-name field, a Task takes `parent`; **2 issues, `OXPD2-1` and `OXPD2-2`** |
| Project folder | `ls`, `awk`, `find` | `2_Project_Files`, `.tools`, `Briefs`, `Registers` empty; `<project>` is not a git repository; no launcher, no BACKLOG, no runbook; `Source_Documents` 1657 files |
| Design quotes | `ptr_check.py` (scratch) | 59 of 59 for the kit, 45 of 45 for the lane plan |

## Inputs of each chain step (each produced by an earlier step, or present before launch)
| Step | Needs | Produced by |
|---|---|---|
| 0 | the stamped kit; the project folder | Tuesday; exists |
| 1 | `gh` login, Jira login, `<project>/.tools/dotnet` | exist; **Tuesday's placement (not present today)** |
| 2 | the deploy key; the sibling's two config values; texts T1 and T2 | exists; the two named reads; the kit |
| 3 | `main` at origin | Step 2 (or already there: then no first commit) |
| 4 | the branch; the SDK; NuGet | Step 3; Step 1; the named registry |
| 5 | the tree of Step 4; `Source_Documents` (for R5's hash half) | Step 4; exists |
| 6 | the commit of Step 5; Actions enabled | Step 5; measured enabled |
| 7 | the launcher block in the Step-0 copy | Step 0 |
| 8 | the Jira login; texts T5 and T6 | exists; the kit |
| 9 | the results of Steps 2 to 8 | those steps |

## D-decisions the drafter took (all are Tuesday defaults in the kit, each with its Question)
D1 one repository | D2 prefix `Datasec.Suite` (from `02:255`) | D3 the layout: `src/`, `tests/`, `build/`, `packaging/`, one project per component of `02:330-348`, 22 paths now, 23 reserved names | D4 SDK pin 10.0.404 | D5 the SDK is placed by Tuesday | D6 GitHub-hosted `ubuntu-latest` and `windows-latest` | D7 the workflow also runs on lane-branch pushes | D8 no CodeQL workflow | D9 gitleaks 8.30.1 as a checksum-verified binary, no licence secret | D10 guard scripts in Python 3 standard library | D11 the SPU clauses not built | D12 the development-CA fingerprint owed | D13 xUnit. Also: twelve Jira Tasks (one per row of `05:155-166`) under five Epics; the launcher's text frozen in the kit so that the seat never reads the sibling's; READY = Step 0 + 300 min.

## Questions for Tuesday, each with its default and its source line
| Q | Question | Default | Source |
|---|---|---|---|
| Q1 | The first pull request and CodeQL: what if it shows no CodeQL result and the rule blocks it? | the seat does nothing; Tuesday reads the rule on the pull request and takes a block to the product owner. Alternative: put `ci.yml` in the first commit (three files) so `main` holds a language | ruleset and default setup (measured); sibling `B02_ADDENDUM-2:3-4`; project `CLAUDE.md:56-57` |
| Q2 | "repos" in the plan: one repository or more? | one | `03:136`; `CLARIFICATIONS.md:274` ("a private repository") |
| Q3 | Where does the amended deployment utility live? | no folder in this lane; the correction pass says | `CLARIFICATIONS.md:282` |
| Q4 | The folder and assembly prefix | `Datasec.Suite` | `02:255` |
| Q5 | The SDK: which version, and who brings it? | 10.0.404, placed by Tuesday at `<project>/.tools/dotnet` (`brief_seat.sh:41` looks exactly there) | sibling `global.json` (measured); `brief_seat.sh:41` |
| Q6 | Hosted runners and "no spend" | both hosted runners; billing UNMEASURED | `CLARIFICATIONS.md:274` ("no spend"); `03:69` ("both packagings") |
| Q7 | May the workflow run on a lane-branch push? | yes | `03:136` ("pipeline red/green on planted secret and planted dev CA") |
| Q8 | The SPU in CI | not built; WP0.3 stays open on it | `03:136`, `03:69`, `03:34` |
| Q9 | The development-CA fingerprint | owed; mechanism and file-name rule ship | `02:599`; report B3 line 118; the NAS listing |
| Q10 | The guard's language | Python 3 standard library | no design line (open choice) |
| Q11 | Twelve Tasks or fourteen? | twelve | `05:155-166` (12 rows, 14 numbers) |
| Q12 | The gate tier | G1 | `model-routing.md:108`, `:109` |
| Q13 | Squash or merge commit for this repository | Tuesday decides before the first merge | written nowhere (the repository allows all three) |
| Q14 | The git identity: two reads of the sibling's config, or a file Tuesday places? | the two reads, as the commission says | project `CLAUDE.md:46-47` against the commission's step 1 |
| Q15 | The pane name | `Datasec/OXPd2-X1` | the launcher's seat rule |

## Corrections to the commission
1. **"holding one issue, OXPD2-1":** the project holds TWO, `OXPD2-1` and `OXPD2-2` ("Phase 0 kit: what is in hand, and the set-up steps for each item"), read at 12:02:33.
2. **"read WHICH checks the ruleset names":** it names none (`required_status_checks` is `[]`). And the code-scanning requirement cannot be met by a workflow file while the organisation's default setup is on (DERIVED from GitHub's rule on advanced configurations; the sibling repository carries no CodeQL workflow either: its only workflow file is `ci.yml`, MEASURED).
3. **"so that the first pull request can go green":** not in a kit's power (BLUF 3).
4. **"the other eleven":** the list that follows names thirteen work-package numbers; `05` has 12 rows carrying 14 numbers. The plan has 13 rows; Jira gets 12 Tasks by default (Q11).
5. **The sibling's "one-time initial README commit" record:** found (`2026-09-30_B01_ADDENDUM-1_github-repo-and-key.md` and `2026-09-30_B01_STATUS.md:51-56`). It is a precedent from before the ruleset's last update, so it proves nothing about today.
6. **The toolchain is missing from the "what exists" list:** no `dotnet` anywhere the seat may use. The kit cannot be run until an SDK is placed.
7. **"no hosted call beyond GitHub and the package registries the build needs":** the hosted run itself pulls a base image from Microsoft's container registry (the Dockerfile) and the gitleaks binary from a GitHub release; the seat's own machine calls only GitHub, NuGet and Jira. Said in the kit.
8. **`DRAFTER_RULES.md` says a drafter writes two files; this commission says four.** The commission was followed. The rules file also still names `/Volumes/Laptop-DEV` (the commission already says so) and has no rule for a kit whose repository does not exist yet (no base sha, no tarball): the kit's S2 slot says so.
9. **`model-routing.md:39` still says Fable is not a worker tier**, and the table has no Fable column: the kit cites the project rule (`CLAUDE.md:7`) for the model instead of a routing row.

## Corrections to the project `CLAUDE.md` (Tuesday's file; the drafter changed nothing)
1. **`:54-55` "required status checks":** true as a rule type, but the list is empty; and "merges once the checks and CodeQL are green" (`:55-56`) may be unmeetable on the first pull request (BLUF 3). Worth one sentence.
2. **`:46-47` "Never read or write a sibling project"** contradicts the commission's own step 1 (the identity is read from the sibling's config). The kit grants ONE named exception of two reads and offers Q14 to remove it.
3. **`:50-51` "Nothing under `Source_Documents/` is ever committed or copied into `2_Project_Files/`" contradicts the plan in one place:** `03:184` seeds the languages "from the Workpath string resources", and the SharePoint strings are under `Source_Documents/`. A rule the design contradicts; it bites at WP3.12, not in this kit.
4. **`:35` "A9 and A10 follow":** A9 is already in `Analysis/` (and differs from the copy in Tuesday's tree from line 7); A10 is not there.
5. **`:42` Jira:** `OXPD2-2` exists and is not mentioned.
6. **`:63` "Phase 0 first"** against the word to build, which starts packages of phases 1, 3, 4 and 6 now. The plan itself has the same tension: `03:266` says "Parallel tracks once phase 0 exits", and decision D3 (`02:815`) is "Firm after spike S2", so code written now for the older printers rests on a choice a printer test may overturn.
7. **Not said anywhere and now needed:** the landing rule (squash or merge commit), the toolchain path (`.tools/dotnet`), and that the organisation's Actions secrets are visible to this repository.
8. **A stale path in the design, for the correction pass:** `03:43` says the SharePoint source is kept under a `2_Project_Files/fleet/state/` folder, which is a path of Tuesday's tree; in the project it is under `Source_Documents/`.

## UNMEASURED (nobody has run it)
1. Whether GitHub accepts a branch-creating push to `main` under today's ruleset, and the exact refusal text if not.
2. Whether the first pull request gets any CodeQL result, whether the rule blocks it without one, and whether the default setup picks up `csharp`, `actions` and `python` by itself once `main` holds them.
3. Every hosted run: nobody has run a workflow in this repository; the Windows leg, the container build and the gitleaks download have never run. Whether hosted minutes are a spend.
4. `gitleaks git` (the history form): the drafter may make no repository; only `gitleaks dir` was run.
5. `git ls-remote` and `ssh` with the deploy key: a drafter may not; RELAYED from the commission that the key is verified.
6. Any `dotnet` command for this layout: no build, restore, test or publish was run; the package versions; whether SDK 10.0.404 is still the newest 10.0 patch; whether cross-publishing `win-x64` and `linux-x64` from the Mac works as written.
7. The Jira create call's accepted body (GET only).
8. Whether a pane name `Datasec/OXPd2-X1` suits the cockpit; live panes (a drafter does not read them).
9. The real development-CA certificate: where it is. The SPU: how a runner could get it.
10. The size of each lane in the plan; whether the hosted run can host the two databases WP1.1 needs.
11. The sibling's test framework and solution style beyond its `global.json` (not read: not needed).

## Outside the fences (disclosed)
- **Read in a sibling project, as the commission told me:** its `CLAUDE.md` (2 lines by search), its `Launch_Claude.command` (whole), four files of its `Briefs/` folder (two whole, two by search), its `.tools` listing, the byte lengths and the masked domain of its local git identity. **Also ran one binary there: `<sibling>/.tools/dotnet-10.0.404/dotnet --version`** (prints a version; writes nothing). No other read of that project.
- **GitHub GET beyond the two repositories named:** `orgs/datasecau/repos` (8 names, to look for a precedent newer than the ruleset: none), `orgs/datasecau` (plan name), the tag refs of three `actions/*` repositories, the `gitleaks` release. One GET was refused (the organisation ruleset history: 404, needs `admin:org`); not retried.
- **Organisation secret NAMES were printed** by a GET that returns names only. No value was read or printed. The Jira login was used in-process by a GET-only reader; `/myself` was read for a liveness check and its id not printed.
- **The NAS library:** one `ls` of the one folder report B3 cites. Nothing searched, nothing opened.
- **Wrote with a program as well as with the Write tool:** the launcher block was inserted into the kit, eleven wording fixes were applied and the sidecar was filled by short Python programs (temp file, then `os.replace`), so that the bytes and counts are exact.
- **Ran:** `gitleaks dir` on two scratch folders, `/bin/bash -n` on the scratch launcher, `stamp_check.py`, my own pointer and count checks. No test, no build, no git write, no `cd` (one command was refused by the `=` hook and rewritten).
- **Read in Tuesday's tree beyond the commission's list:** the `.pre-stamp` copy of the form kit (for the unstamped Stamp form), the headers of `stamp_check.py`, `stamp_brief.py`, `launch_when_cool.sh`, and reports A9 and A10 under `0_Brain/reference/2026-11-18_datasec-oxpd/analysis/` (for the lane plan's flags).
- **No person's name and no decision-card id is in the kit or the lane plan** (scanned). This report names none either.
