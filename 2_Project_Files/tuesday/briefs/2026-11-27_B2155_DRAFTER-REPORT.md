STARTABLE: YES

# B2155 DRAFTER REPORT: OXPd lane OX-D, kit 1 (seat X83)

Drafter: in-session read-only agent (Opus) for Tuesday s333, commission `2026-11-27_B2154_OXPD-WORKING-COPY-CRITICAL-PATH_COMMISSION.md`, section "B2155 (lane D)". First `date`: Fri 27 Nov 2026 16:58:32 AEDT; kit written 17:2x; this report after `date` printed 17:23:06 AEDT. Files written: the kit `2026-11-27_B2155_SEAT-X83_oxpd2-lane-d-kit1.md` (240 lines, sha256 `8a6f847b...`), its sidecar `.measured` (121 claims, 0 TODO; `stamp_check.py <kit>` exits 0), this report. Scratch only under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s333/d2155/` (the seat tools in `seat-tools/`).

## BLUF
- **The OX-D block, item by item, against main `760e1a64` and the four records passes since 11-26 (B2124, B2132, B2140, B2146: none names an OX-D item, measured by program over each kit's owed-item numbers; control: each names lane C items):**
  - **DROPPED as closed on main:** owed 19 (`README.md:78`-`:79` now name the pull request's merge commit; changed by PR 16, squash `185b9eef`: README at `7bf37526` held "fetches branches and tags only" at `:73`); owed 22 (R6 line rules and `BASH_ENV`, R7 NUL, R8 LFS filter, whole-file workflow fingerprint, README `:81` on a job added after `rules`; PRs 16 and 19); OXPD2-25's code (owed 51 is ticked: PR 19).
  - **IN KIT 1:** owed 129 (the release guard's JSON-escaped tab), the buildable remainder of 12 (refuse anchors/aliases/tags at a node start, document markers and directives; refuse a scanner line ending in a backslash), the pin half of 27 (`actions/setup-dotnet` `a98b5685` = `v6.0.0` to `0f4a354d` = `v6.1.0`, release 2026-11-03).
  - **Kit 2 (buildable, deferred):** owed 11 (open gzip, bzip2, xz and tar members); it changes the landed cell `test_g3_archive_formats_the_guard_does_not_open_fire`.
  - **Not buildable without a ruling or a heavy job:** 16 (the item calls the rest "a decision"), 17 (hash half needs the supplied source on a runner), 20 (script exists; NOT DECIDED 3 of OXPD2-21 left), 23 (compressed single-file host needs a `dotnet publish`; NOT DECIDED 1), 27's `.pdb`/`web.config` half (NOT DECIDED 2). 21's checks are built (PR 16); its speed clause measured 12 s for 2079 stored objects on main: a records note (Q4).
- **Lane OX-D is pure Python, so the drafter RAN the whole local proof** (no dotnet, no wave lock; the lock folder was absent at every look): red-first (5 red ids exactly, `FAILED (failures=17)`), green (`Ran 121 tests`, `OK`), `RULES: clean (679 files)`, the workflow's own `planted controls` step (`UNIT-TEST FLOOR: ran 121, floor 121`), six mutants `6 of 6 MATCH, 6 of 6 undone equal`, `checks_d1.py` 8 of 8 (control 4 of 8 on BASE's index), `words.py` clean, `gitleaks` clean (control fired), the neutral-scan step `25 of 25` on a scratch commit, the head tree `60ed7217...` when BASE is `760e1a64`. Only the hosted run of the head is PREDICTED.
- **For the plan (lane P):** this seat runs NO heavy job, so it can run beside an OXPd dotnet seat (Q3); landings stay serial by the rebase rule. Size: S-M; READY at Step 0 + 75 minutes.

## FACTS RE-MEASURED (instrument, then value)
- `gh api -X GET repos/datasecau/OXPd_2/branches/main` -> `760e1a644ce9a419cf1b9132d0776e9e5eac1cac`; `git/commits/<it>` tree `8e3985c1...`; `pulls?state=open` 0; `matching-refs/heads/b2155` 0; `.private` true, `.permissions.push` true.
- `gh api -X GET .../tarball/760e1a64` -> 679 files; `git write-tree` in a scratch repository -> `8e3985c15262e5198ffa2fc8b4bf4285f9d82a0c` (equal: control that the scratch tree is main's).
- `hosted3.py 760e1a64 --total 2431 --rules 679 --skipped-linux 4 --skipped-windows 21 --unit 117 --floor 117 --hardened-scan --guard-linux 14 --guard-windows 15` -> `HOSTED ...: PASS`; control `--total 2432` -> `FAIL 4`. Head carries `Analyze (actions)` too (owed 24's subject: code scanning now lists the workflow language; a records point).
- BASE local: `python3 -I -B -m unittest discover -s build/tests` -> `Ran 117 tests`, `OK`; `repo_rules.py` -> `RULES: clean (679 files)`; indented `def test_` 7+43+54+13 = 117 = `FLOOR` (after: 7+44+57+13 = 121).
- `gh api -X GET repos/actions/setup-dotnet/git/matching-refs/tags/v6` -> `v6.0.0` `a98b5685...`, `v6.1.0` and `v6` `0f4a354d...`; releases: `v6.1.0` published 2026-11-03T02:51:23Z, not prerelease.
- `gh api -X GET .../actions/jobs/140249646080` (main's `secret-scan`): neutral step 01:04:44Z to 01:04:56Z; `NEUTRAL-SCAN: stored objects 2079`.
- `<project>/BACKLOG.md` sha256 `74800003...` (1212 lines; 89 open, 71 ticked by `grep -c -E '^[0-9]+\. - \[ \]'` and its `[x]` twin); items 129, 12, 27 each 1 open line by `startswith`; `CLARIFICATIONS.md`: 'release guard' 0, 'repository rules' 0 (control 'C-92' 1): no product-owner word on lane D.
- Seat id X83: 0 of 200 non-`.pre-` SEAT kits of 2026-11-2x (control X81 in 4). `<project>/.tools/b2155` absent.
- Probe at the head (drafter's own program, not a cell): a tab written as backslash u0009 and a tab escape with no line end stay unseen (now named in the frozen Limits); a real LF followed by a tab escape is seen.

## D-DECISIONS (all Tuesday's defaults as coordinator; detail in the kit)
D1 scope = 129 + 12's remainder + 27's pin (11 is kit 2). D2 every byte frozen, cells included (the drafter ran them). D3 no dotnet job, no wave lock. D4 129 by the escape in the join and the joiner, plus two named limits. D5 12 by refusals in R6 and R1; Limits keep "a plain scalar continued on the next line" and "a scanner command built from shell variables or a command substitution". D6 the `v6.1.0` pin; `.pdb` half untouched. D7 the new value line of the landed constant `REVIEWED_WORKFLOW` is the one line excused from the words scan (its landed name holds "review"); `checks_d1.py` proves exactly 1 line is left out. D8 one G1 gate.

## Q-QUESTIONS FOR TUESDAY (each with its default; the kit assumes the defaults)
- Q1 (STOP-CLASS) scope of kit 1. Default a: 129, 12's remainder, 27's pin; 11 in kit 2.
- Q2 (STOP-CLASS) who writes what. Default a: every byte frozen in `edits_d1.json`, applied only by `apply_d1.py`.
- Q3 may this seat run beside an OXPd dotnet seat. Default: yes, beside one named seat whose kit touches none of the seven paths (B2153's lane C part 2 by its commission); landings serial. Alternative: one OXPd seat at a time.
- Q4 owed 21's speed clause. Default: a records note (12 s for 2079 objects), no build.
- Q5 to Q7: the escape (129), refusals (12), the pin (27). Q8: one G1 gate, Opus, 75/60 minutes, pane `Datasec/OXPd2-X83`.
- (Not a kit question) The records pass should tick 19 and 22 on the lines named in THE DROPPED AND THE LEFT, and may close 12 and 21.

## PARTITION (both sides)
- Kit B2155 owns `.github/workflows/ci.yml`, `README.md` (root), `build/release_guard.py`, `build/repo_rules.py`, `build/tests/test_pipeline_controls.py`, `build/tests/test_release_guard.py`, `build/tests/test_repo_rules.py`, and `<project>/.tools/b2155/`.
- B2153 (its kit not yet written at this drafting; read from its commission): owed 137 `tests/Datasec.Suite.Server.Tests/**` and owed 121's README line in three module READMEs under `src/`. No path under `build/`, `.github/` or the root README; the workflow pins no dotnet total. **Shared path: none.** If B2153's kit names any of the seven paths above, that is a STOP for one of the two.
- B2146 (records, R339): `CLARIFICATIONS.md`, `BACKLOG.md`, `history.md`, one Jira comment, `.tools/b2146/`; none in the code repository. **Shared path: none.**

## CHAIN INPUTS (MEASURED LITERALS rule 4)
| Step | Inputs | Produced by or present at |
|---|---|---|
| 0 | kit, Stamp S2/S3/S4 | Tuesday's stamp |
| 1 | `<src>` (10 files), `<repo>` local values, origin BASE, BASE's push run, live BACKLOG | drafter scratch (exists), `<repo>` (exists), GitHub (exists) |
| 2 | BASE files, `edits_d1.json` | Step 1 |
| 3 | group `cells`, BASE clone | Step 1 |
| 4 | red-first tree, groups `product`/`pipeline`, `run_step.py`, mutants files | Step 3, Step 1 |
| 5 | green tree (mutants undone), `checks_d1.py`, `words.py`, commit message | Step 4, Step 1 |
| 6 | staged tree, `origin/main`, `run_step.py`, `hosted3.py` | Step 5, fetch, Step 1 |

## WHAT WAS RUN, WHERE, AT WHAT LOAD (DRAFTER_RULES 2026-11-19)
Python unit tests, `repo_rules.py`, the mutants and the workflow's `planted controls` and neutral-scan steps ran ONLY on copies of main's tree under my scratch, never in the project folder; no dotnet job; the OXPd wave lock folder was absent at about 17:00 and at 17:23 (`ls -d`; no lane held it); load1 1.70 at 17:03, 0.82 at 17:12, 1.22 at 17:23.

## UNMEASURED
- The hosted run of a head of this lane (the pin's effect on the two build legs; GitHub's own YAML reading of the refused shapes).
- Whether `0f4a354d` (setup-dotnet v6.1.0) changes any build-leg output line hosted3 reads (PREDICTED no).
- Jira OXPD2-20 to 25 statuses (no Jira call by this drafter; the records lane's).
- B2153's kit paths (not yet written).

## OUTSIDE-THE-FENCES DISCLOSURE
- `gh` ran under `GH_CONFIG_DIR=<project>/4_Credentials/.gh-config` as the commission mandates (gh reads its own login there; I opened no file in `4_Credentials/`). One `gh api -X GET` series read the PUBLIC repository `actions/setup-dotnet` (tags and releases) under that login.
- Git write verbs (`init`, `add`, `commit` with a scratch-only `-c user.name/user.email`) ran ONLY in scratch repositories under my scratch folder, never in a project repository.
- Two commands were refused by hooks before running: a `git -C $S/base init` (variable path) and an `rm -rf` of a scratch path that did not exist. Nothing was deleted; the two gitleaks control files were moved to `<d>/_quarantine/`.
- I read B2138's seat tools (copied four of them byte for byte), the B2146, B2140, B2132, B2124 kits (owed-item numbers by program), BACKLOG/CLAUDE.md whole items, CLARIFICATIONS and SETUP_RUNBOOK by count only. No `Source_Documents/`, no key folder, no `.env`, no card store, no Jira, no write to any project, GitHub, Jira, card or mail.
