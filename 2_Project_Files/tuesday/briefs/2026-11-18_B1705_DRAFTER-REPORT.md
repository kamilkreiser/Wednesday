STARTABLE: YES (the kit is complete and stamp_check exits 0; two Tuesday rulings are asked below, each with a default that lets the seat start; the lane builds and pushes only, landing is held)

# Drafter report B1705 | SEAT-H182 | HPSM-POC | live-check allows the favicon route-cache pair (HPSMPOC-509)
Drafted 2026-11-18, `date` printed 10:43:42 at the first read and 11:06:52 at the last check. Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-18_B1705_SEAT-H182_hpsmpoc-lane-live-check-favicon-pair.md` (342 lines, 0 non-ASCII bytes, 7 four-underscore runs = the 7 Stamp slots, 0 `@TOKEN@`). Sidecar beside it. `stamp_check.py <kit>` rc 0: 50 claims, 50 measured. Rules read whole first: `DRAFTER_RULES.md` (its paths say `/Volumes/Laptop-DEV`; this machine's drive is `/Volumes/Datasec_DEV`, so every path in the kit uses the latter).

## BLUF
- The ticket's proposed default, approved by the coordinator (never written as the product owner's ruling): one compiled pattern for exactly `.next/server/route-cache/APP_ROUTE/<64 lowercase hex>/$/favicon.ico.body|meta`, used with `fullmatch`, on the WEB only; the API gets none; the first stdout line is unchanged and a SECOND line counts the allowed pair, only when above 0. Three files: `scripts/deploy-package.py`, `infra/tests/test_deploy_hpsmpoc208.py`, `infra/README.md`.
- The frozen patch is IN the kit as a printed unified diff (16/3, 112/0, 6/3 lines) produced from my scratch run; the seat applies it with Edit hunk by hunk.
- Measured in my own scratch copy of main (never the project folder): red first, green, ten planted over-allowing copies each red, the whole infra suite, `validate.sh`, both Pythons.
- Landing is HELD: the CI dev-tools audit fails on any new PR until `b1695/hpsmpoc-picomatch-dev-audit-exception` lands. The kit says so in the title, in a "Landing waits" paragraph, in Step 6 and in `landing.txt`'s first line. The lane builds and pushes only.
- Gate tier: G1 argued (Opus, one gate), a G2 reading is available; Q-2.

## Facts re-measured with instruments (sidecar ids in brackets)
- origin main `36c557ad9255125793bfeb99abdea3b0b4d988e2` at 10:43 and 11:01 (`gh api -X GET commits/main`); open PRs 0; `b1705` refs 0 (control `b1639` 2); 349 branches; the kit's pattern hits one old branch `b123/ci-deploy-package` [S02, S03].
- Blob shas of the three owned files at main equal `git hash-object` of the tarball copy [S05]. Every pointer of the ticket holds at main: `SITE_ONLY_ALLOWED` :75, `allowed` :541, `extra` :551, summary :555-557, the two rows :385 and :438, docstring :25-30; the README paragraph ends at 186 (ticket said 185) [S06].
- Other branch from both sides: `b1695/hpsmpoc-picomatch-dev-audit-exception` is `dc688f765fb2da0eec8a8a6d2aada9c2ce1d3a57`, ahead 1 of main, files `.github/workflows/ci.yml`, `web/scripts/audit-dev.mjs`, `web/src/audit-dev.test.ts` (compare API); this lane's three paths share none; the kit's PARTITION prints both sides [S02].
- Red first (final test file, main's script, Python 3.14.10): `python3 -B -m unittest -v test_deploy_hpsmpoc208.LiveCheck` -> `Ran 29 tests`, `FAILED (failures=5)`: four rows (the pair allowed and counted; pair plus Oryx; pair beside a sibling; each name on its own, which fails once per name). The other three new rows are GUARDS that pass at main (API red, siblings red, clean tree one line); they are proven able to fail by the mutants.
- Green with the patch: the 208 file `Ran 42 tests` `OK` on 3.14.10 AND `/usr/bin/python3` 3.9.6 (main: `Ran 35` `OK` both). `LiveCheck` 22 -> 29. Whole infra suite (git-initialised scratch copy, `BICEP` set): main `Ran 325` `OK`, patched `Ran 332` `OK`; by test id lost 0, added 7, changed 0 (control: drop one -> lost 1). `bash infra/scripts/validate.sh`: rc 0 at main and patched (`ResourceWarnings: 0`, `Files still open: 0`). The system python's whole-suite red is the known base red; not measured here because the kit names 3.14 for the suite.
- Ten planted copies of the patched script (mutants.log): M1 hex `{63,65}`; M2 `match`; M3 API gets the pattern; M4 trailing `.*`; M5 upper-case hex; M6 `$` any char; M7 count line always printed; M8 `search`; M9 dot any char; M10 route type any: all ten red, in the rows the kit's table names; the unmutated control `OK`. (The first mutant run left M9 alive; I added three siblings "a character where a dot is" and re-ran: that is why the sibling list has 19 names.)
- Summary-line census by program: `deploy-from-ci.sh` parses no text (line 96 runs it, line 104 turns non-zero into exit 3); rows pinning the first stdout line are 371, 383, 428, 453, 462, 473, 482, 490 (+452/498 NotIn, 564/584/600); four rows pin `stdout == ""` on a REFUSED path (520, 554, 620, 638); `test_deploy_package.py` 485/737/750/778 pin script text and stderr, not the summary. Nothing under `web/` or `api/` reads `deploy-package` (control: ci.yml 6 lines). The rule in the kit: first line byte-identical, count as a second line only when above 0; the existing rows pass unchanged (they are in the 325 -> 332 run, 0 changed).
- CI pass predicate read at source: ci.yml `infra (Bicep validate)` job (:578-579) runs `validate.sh` (:630) -> line 21 `python3 tests/test_security_baseline.py` -> its `main` loads every `infra/tests/test_*.py` (:2857-2859) and needs `ResourceWarnings: 0` and `Files still open: 0` (:2873-2874). The web jobs do not read these files.
- Routing: row L3 (`model-routing.md:82`) Sonnet 1st, gate "as L1" (:80, tier-1 only for auth/security), C3 (:93) not applicable (decision made, edits spelled out); G1 (:108) "anything deploying", G2 (:109) tooling. Model id `claude-sonnet-5-5` at `models_latest.json:23`. `BRIEF_SEAT_LEVEL=sonnet` is inside the launch quotes.
- Ports: none needed; `lsof 9900-9929` 0 rows (control :5000 3 rows); live panes `fleet-monitor`, `tuesday` only. Load1 5.65 at 10:54.

## D-decisions (mine)
- D-1: `fullmatch` on a compiled pattern, not `re.match` with `$` (measured: `re.match(pattern + "$", name + "\n")` is True; `fullmatch` False).
- D-2: the count is a second stdout line, printed only when above 0 (the ticket's "after the existing summary line ... only when the count is above 0"); no signature change to `live_check`.
- D-3: the output wording says "(the favicon route-cache pair)" and every comment says the page-visit cause is the deploy record's reading, DERIVED, not tested (ticket Detail).
- D-4: HPSMPOC-509 and the existing HPSMPOC-215 sentence may appear in added lines (project convention; counts 5 and 2 by program); no brief number, seat, card id or person's name. The ticket's C-390 record id is not written anywhere in the kit text.
- D-5: the infra suite is run in a git work tree (it scans `git ls-files`); my tarball copy without `.git` produced 4 errors + 4 failures at main (BICEP unset, no git): not a finding, recorded so the seat does not copy that setup.
- D-6: Step 3.3 of my draft ("a real-shape run") was removed: the rows already build a package, deploy it through `zipdeploy_model` and run the real live-check as a subprocess.

## Q-questions for Tuesday (each with a default)
- Q-1: each name of the pair is judged on its own (a lone `.body` or `.meta` is allowed and counted 1; a row pins it) or both-or-neither? Default: on its own (the ticket says "a name of the form ... and no other").
- Q-2: gate G1 (Opus, default; the change relaxes the deploy's own proof) or G2 (Sonnet; the narrowness is checkable by program)? Default G1.
- Q-3: the count as a second stdout line (default) or appended to the first line (would change the first line; the existing rows use `assertIn` so they would still pass, but the first line would no longer be byte-identical).
- Q-4: push only, landing waits for the picomatch branch (default). If you would rather land this first, the PR's CI dev-tools audit step fails regardless of this change.

## UNMEASURED
- The hosted live check after landing, and whether a page visit creates the pair (the ticket's own DERIVED); whether any other route leaves a route-cache file; the 64-hex folder's origin. The kit says the first deploy after landing is the real proof.
- Hosted CI's python version on the `infra` job (the rows pass on 3.9.6 and 3.14.10).
- The seat's typing of the patch hunks by Edit (the kit says a fixture detail that does not run is fixed at its source, never an expectation).
- That the picomatch branch's CI failure on new PRs still holds today: RELAYED from the B1695 kit and STATUS, not re-run (no npm in this lane).

## Inputs table (rule 4: every input exists at BASE or is made by an earlier step)
Step 0 makes `.tools/b1705/**`, the clone `head`, `main-tree`. Step 1 reads GitHub only. Step 2 reads `main-tree` (Step 0). Step 3.1 applies the test hunks to `head` (Step 0); 3.2 the script hunks (needs 3.1's file only for the run); 3.4 copies `head` after 3.2 to `scratch/mut`; 3.5 applies the README hunk. Step 4 reads `out/base-infra-v.log` (Step 2). Step 5(a) runs on the working tree before the commit and again after it. `env.sh` and `compare.py` exist at `.tools/b1695/scripts/` (checked).

## Outside-the-fences disclosure
- Wrote the kit, its `.measured` sidecar and this report (the Write tool), plus scratch only under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s289/d1705/` (a tarball of main, a patched copy, two git-initialised scratch copies `g/base` and `g/head` with local scratch commits, `mut/`, scripts, logs). `git init`/`add`/`commit` ran only inside `g/base` (inside the allowed scratch folder, literal path; the first attempt with a `$VAR` path was refused by the hook and nothing ran). No project folder, no repo, no ref touched.
- Jira: one GET of HPSMPOC-509 through my own GET-only helper (creds read in process from the project `.env`, never printed). No JQL search, no write. `gh api -X GET` only (commits, compare, contents, branches, pulls, matching-refs, tarball). No mail, no board, no az, no hosted HTTP, no decision-queue read. `tmux list-panes` and `lsof` read-only.
- I did not read `fleet/briefs_staged/`, `scoreboard.md`, `_ledger.md` or any WEDNESDAY/FRIDAY tree.
