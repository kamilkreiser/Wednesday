STARTABLE: YES

# B1560 DRAFTER REPORT (SEAT-M134, MPS codeql test-marker rename)

Drafted 2026-11-15 08:34 to 08:45 AEDT (`date` printed 08:34:03 first, 08:44:30 last). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-15_B1560_SEAT-M134_mps-codeql-test-marker-rename.md` (74 lines, 12 `____` slots as the template's S0-S10 plus the last line). Sidecar `.md.measured`: 72 claims, `stamp_check.py <kit>` rc 0 (run twice, the second after the last kit edit). Work folder `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s275/d_mps3/` (files named `b1560_*`).

## BLUF
Your ruling holds on the evidence, so the kit is startable. The alert's only source is the string literal assigned at `scripts/tests/test_deploy_pre1_forms.py:37` (`SECRET = "SYN-DO-NOT-PRINT-7f3a"`), and the query library keys a source on the NAME the expression is assigned to. The fix is one identifier renamed in one file: `SECRET` to `SYNTHETIC_MARKER`, 28 uses on 19 lines. No other file reads the constant. The kit asks for no alert action and no suppression comment, and its proofs are programs: the diff mapped back equals the removed lines (P4), a syntax-tree comparison after the rename (SAME), an identical CI python loop, and a name pre-scan with planted controls. Size S, Sonnet, READY Step 0 + 40, HARD STOP Step 0 + 60. Hosted CodeQL at the new head is YOUR read; the seat does not wait for it.

## Facts re-measured with instruments (each is in the sidecar with its command)
- **Refs (08:42:27):** branch `881f8dc4...` (matches the head you gave), main `0bb3ed12...`, PR 192 open with that head, open PRs 1, `compare` ahead 3 behind 0 with 8 files.
- **The alert:** `alerts/14`, rule `py/clear-text-storage-sensitive-data`, `refs/pull/192/head` @ `881f8dc4`, line 163 cols 26-80 (`fh.write(raw if ...)` in `run_doc`). Analyses at that sha: python 1 result, csharp, js/ts and actions 0. Main has 0 open alerts (control: the PR-head call printed 1 row).
- **The source (SARIF of analysis 2168753667):** one result, 4 code flows, all four start at line 37 col 10 (the literal) then line 37 col 1 (`SECRET`). Distinct starts by program: 1. Control, one flow's start edited in a copy: 2.
- **Why that is the name (the library, not memory):** I read the query library at the tag the SARIF names (`github/codeql` ref `codeql-cli/v2.27.4`, saved with sha256 in the sidecar). `SensitiveDataSources.qll:250-272` `SensitiveVariableAssignment`: the source is the expression assigned to a variable whose NAME matches (`:255`), and the library's own note (`:246`) says so. The `secret` name regex is `SensitiveDataHeuristics.qll:60`. A Python port of the regex families (the drafter's, lookbehinds split) says: `SECRET` matches the `secret` family; `SYNTHETIC_MARKER`, `MARKER` and the literal text match none. **So the ruling's STOP condition (source other than the name) does not fire.** The port is my translation; the hosted run at the new head is the final test.
- **Other uses of the constant:** over the 22 files of `scripts/` at head, `SECRET` as a whole word is in the forms file only (28 occurrences, 19 lines; `grep -o -F` also 28, so a plain replace touches nothing else). The same value sits in `scripts/tests/test_deploy_pre1.py:39` as `SECRET_LOOKING`: a different name, NOT touched, and it raises no alert (no flow to a clear-text sink). The forms module is loaded by path, never imported (the mentions under `scripts/`: a comment in `deploy-package.py:428` and its own line 1).
- **My dry run of the rename:** word-bounded replace over the raw file: 28 replaced, diff 19 added / 19 removed, ASCII, Python parse ok, the line-37 comment untouched. The pre-scan over that diff: P1 to P5 PASS; five planted controls each exit 1 (a `secret_value =` line, `password =`, `oauth =`, `mfa =`, `_by_password_`, one changed character). The AST check printed `renamed Name nodes in the old tree: 28` and `SAME`; a planted change of the value prints `DIFFERENT`, rc 1.
- **CI predicate:** `ci.yml` at head, job python (`:84`), loop `:102-104`, `exit $rc` `:107`; gate's loop (RELAYED, VERDICT :43): 15 files equal base and head, five green files `Ran 8/44/16/22/56`; two reds are environmental. The kit asks for EQUALITY at base and head, not those numbers.
- **Ports 9760-9769:** 0 listeners (control 13). **One hit** in the word-boundary scan: the earlier MPS kit `...B1557_SEAT-M133...md` (same block, "none needed", finished). No MPS pane (0 of 7).
- **Model:** `model-routing.md:81` row L2 (one file, multi-hunk) names the shape; its S55 column says "esc; raises" and local workers never push (row C1 `:91`), so a Sonnet seat does the edit and push; nearest Sonnet-first row C2 `:92`; not a C3 design surface (`:93`, `:67`). Model id `claude-sonnet-5-5` at `models_latest.json:23`; the launch line carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes.

## Chain inputs (rule 4)
| Step | Input | Made by |
|---|---|---|
| 0 | the three programs in `d_mps3/` (`b1560_prescan.py`, `b1560_astcheck.py`, `b1560_heur_port.py`) | exist now; sha256 in the sidecar (SRC-13); keep that folder until the seat has copied them |
| 1 | clone at base, `out/base-python-loop.txt`, `out/base-names.txt` | Step 1 itself |
| 1 | SARIF of the PR-head python analysis | `gh api -X GET` (read) |
| 2 | the base file | the clone at base |
| 3 | head loop vs `out/base-names.txt`; the base copy of the file for the AST check (`git show <base>:path` into `out/`) | Step 1; the clone |
| 4 | `out/diff.txt` (working tree against base, before the commit; against HEAD again after) | the edit of Step 2; the commit of Step 5 |
| 6 | the commit, the ref | Step 5 |

## D-decisions (mine, for Tuesday to reverse)
- **D-1:** the new name is `SYNTHETIC_MARKER` (truthful; `grep -i marker` printed nothing in the file before, so no collision).
- **D-2:** `secret_doc`, `"b-pre1-secret-"` and the test names that hold `secret` or `token` are NOT renamed. Reason: the SARIF shows no flow starting at them (one source, one result), and a rename of test methods changes the test-name list your loop equality guards. They stay in the kit's FOR TUESDAY so you can see them if the hosted run names one.
- **D-3:** no red-first row (a rename cannot fail a test); the kit says so and uses three programs instead of a red.
- **D-4:** the pre-scan's word list is a superset of what the query matches. The query's families are secret/trusted/confidential, account-like, password-like (password, passwd, passcode, passphrase, auth+key, oauth, api key/tok, mfa), certificate and a private-data list; `key` and `token` ALONE are not among them (checked by the port). The program judges "no new sensitive word on added lines beyond what the removed lines held" plus "nothing assigned or defined under such a name", so the inherited `key=` and "token" words (2 and 2) do not read as hits.
- **D-5:** the seat does not poll hosted CI or CodeQL. One optional read of `alerts/14` after the push, printed as found, never acted on.
- **D-6:** no Jira read in this kit (nothing in it depends on a ticket state), and no gate row is imposed; the stamp slot S8 is yours.

## Q-questions for Tuesday
- **Q-1 (level):** Sonnet (default). Opus only if you want the C3 reading applied to a test constant in a security-flavoured file. Default: Sonnet.
- **Q-2 (also rename `secret_doc`?):** the SARIF says it is not a source today, but it carries the same word. Default: leave it; if hosted CodeQL then reports a NEW alert naming it (or the `"b-pre1-secret-"` string), that is a second one-line kit.
- **Q-3 (the same value as `SECRET_LOOKING` in `test_deploy_pre1.py:39`):** no alert on it; the name matches the same `secret` family but nothing reaches a clear-text sink. Default: leave it untouched (it is outside this kit's lane and on main already, where 0 alerts are open).
- **Q-4 (a gate after):** the diff is one identifier in a test file. Default: no gate; you re-run the kit's own property programs and read hosted CI and CodeQL at the new head. If you want one, row G2 (`model-routing.md:109`, tests-only).
- **Q-5 (landing read):** the check that can fail here is alert 14 on `refs/pull/192/head` at the NEW head reading fixed while python results there read 0 and no new alert appears (the PR head carries alerts today: 1; main carries 0). I could not run CodeQL (no CLI on this machine: `command -v codeql` printed nothing), so this is your read after the push.

## UNMEASURED
- Whether the python tests actually pass after the rename on the seat's machine (the drafter did not run them: the repo layout and fakes are the seat's; the AST comparison and P4 prove the only change is the identifier).
- The count of 4 code flows being CodeQL's cap on paths per result.
- The seat's `git diff`, `git show`, gitleaks range run and push read-back (command shapes only; gitleaks `dir` with a canary read rc 1, the renamed copy rc 0).
- The whole-clone `SECRET` search (the drafter's census covers `scripts/`; `src/`, `tests/`, `web/` and `infra/` were not searched; the kit has the seat judge any hit by one question and touch none that is not this constant).
- Hosted CodeQL at the new head.

## Outside-the-fences disclosure
- Read-only `gh api -X GET` under the MPS project's `GH_CONFIG_DIR`: this repo's alert, instances, analyses, SARIF, refs, PR, compare, tree, raw files (22 files of `scripts/` and `ci.yml` at head); and two raw files of the PUBLIC `github/codeql` repo (the query library at `codeql-cli/v2.27.4`). That second read is outside "this Datasec repo"; it is a public read-only file fetch through the same authenticated client, and no token was printed.
- Read the template kit, `DRAFTER_RULES.md`, `model-routing.md`, `models_latest.json`, `brief_seat.sh`, the round-2 gate's `VERDICT.md` and the kit folder; local read-only `git config` (identity) and `ls` in the MPS project (`2_Project_Files`, `.tools`), `lsof`, `tmux list-panes`, `command -v`.
- Writes: the kit, its sidecar, this report, and scratch files under `d_mps3/` (`b1560_*`, including a `b1560_sim/` folder of scratch copies and a `gl/` canary folder). One `sed -i ''` was run on MY OWN kit file (a pointer correction), not on any project file. No git write verb, no Jira, no alert action, no WEDNESDAY, FRIDAY, Secuura or non-Datasec tree opened.
