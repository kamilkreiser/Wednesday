GATE B1557: GO WITH FINDINGS @ 881f8dc on main 0bb3ed1

Gate G1, ROUND 2 OF 2 (the cap), 2026-11-15 07:59-08:17 AEDT. MPS Calculator, branch b1554/mps-lane-mo-deploy-script-rulings @ 881f8dc49e046d48f67e2c165dec95ca490f0c20 (Part A 98b9fed MPSCALC-202, Part B 355fe9e MPSCALC-222/103/226, round-2 fix 881f8dc) on main 0bb3ed12808d72d3187c51d56852b7ecd2174666.
Findings: Blocker 0, Major 0, Minor 1 (R1), Note 5 (R2-R6). Both round-1 Majors are CLOSED, measured: F1 (token in a traced deploy) and F2 (PRE1_TIME). F3 is listed and every reason is true of the code. F8 is 22.
Tier: G1, security-shaped surface (the Kudu token). No security issue remains: the token is in 0 trace lines and on 0 faked argv lists, in every mode tried.

## Refs, scope, merge (measured)
- `git ls-remote origin` (08:00 and again at 08:12): branch = 881f8dc49e046d48f67e2c165dec95ca490f0c20, main = 0bb3ed12808d72d3187c51d56852b7ecd2174666. `refs/heads/b1554*`: 1 ref. Open PRs: 0 (`gh api -X GET pulls?state=open` length 0). `rev-list --left-right --count main...head`: 0 3. The parent of 881f8dc is 355fe9e8 (a fast-forward).
- `git merge-tree --write-tree main head`: tree 1c5b4745, equal to the head's tree.
- Round-2 paths (355fe9e8..881f8dc): 4 of 4 allowed (scripts/deploy-from-ci.sh, scripts/deploy-package.py, scripts/tests/overlay_forms.json, scripts/tests/test_scripts.py). Outside the list: 0 (a planted src/x.cs counts 1). Cumulative main..head: 8 paths, all under scripts/ (round 1's 7 plus test_scripts.py). `.github` versus main: unchanged (`git diff --quiet` rc 0).
- The line property holds. Hunks: deploy-from-ci.sh -195 +195-196 (the `rf_token=""` line, now two comment lines), -198-199 +199-201 (inside `kudu_get`), -206-207 (the two token lines in `rollforward_hosted`); deploy-package.py :448 only; overlay_forms.json +5-14, inserted after `"forms": [`; test_scripts.py +471-495, inside `test_xtrace_never_prints_the_token` (:464), after its last line.
- Removed lines, printed whole: the 5 rf_token and old kudu_get token lines, and the one PRE1_TIME line. 0 removed lines in overlay_forms.json and test_scripts.py. That is what the kit allows.
- Identity: `881f8dc kamil.kreiser@datasec.com.au | kamil.kreiser@datasec.com.au` (the repo's own, as in rounds A and B).

## F1: CLOSED (measured)
- **The round-1 probe** (`probe_xtrace.py` copied unchanged; `bash -x` plus SHELLOPTS=xtrace; the repo's Sandbox with fake az and fake curl; PATH=/usr/bin:/bin; Python 3.9.6): at 355fe9e8 (control), `rc 0 token lines 2` and `rc 1 token lines 2` (`+ rf_token=<TOKEN>`, `+ [[ -n <TOKEN> ]]`). At head, `rc 0 token lines 0 []` and `rc 1 token lines 0 []`.
- **My probe** (`probe_xtrace_g1557.py`) runs each mode on its own: `bash -x` alone, `SHELLOPTS=xtrace` with plain `bash`, both together, and no tracing as a control. Each runs at count 0 and count 1. At base, every traced mode prints 2 token lines (6 of 6 cases); the untraced control prints 0. At head, all 8 cases print 0 token lines. Faked argv lists holding the token (the fake az and fake curl log every argv): 0 at base and 0 at head. Every traced head case shows the Kudu calls in its trace (2 `kudu_get` lines at count 0, 3 at count 1), so the traced path ran. Count 1 ends rc 1 with "git answered 128" (the synthetic sha is not a commit). That stop comes after all three Kudu reads, at base and at head alike.
- **The token-line table, by program** (`f1_table.py`): for every line holding `get-access-token`, I find the nearest function header above it. The line passes only if that header is `name() (` and the next line is `{ set +x; } 2> /dev/null`, with no close of the function in between. Base: :111 read_overlay PASS, **:206 rollforward_hosted FAIL**, :283 download_wwwroot PASS. Head: :111 PASS, :199 kudu_get PASS, :283 PASS; 0 failing. Control: a token line planted in the `{ }` function pre1_hosted reads FAIL (1 failing). The token reaches curl on stdin by `printf` (a builtin) and `--config -`, never on a command line. The new kudu_get token lines (:199-201) are byte-identical to read_overlay's (:111-113). `rf_token`: 0 lines at head. (scripts/lib/kudu.sh:19 also takes a token, but it is outside this branch and unchanged.)
- **The extended test is real, not vacuous.** I ran `DeployAndLiveCheck.test_xtrace_never_prints_the_token` over head's tests with 7 script variants. Head: OK. Base's scripts: FAIL in 2 sub-cases (token found). Mutant `set +x` in rollforward_hosted (tracing off): FAIL 2 (no kudu_get line). Mutant roll-forward returns early with the count-0 line: FAIL 2 (no kudu_get line). Mutant `echo "debug $token" >&2` in kudu_get: FAIL 2 (token found). Mutant with kudu_get's `set +x` line removed: FAIL 2 (token found). Mutant that skips each file read: FAIL 1 (count 1 not reached). It cannot pass on a run that stopped early or was not traced.

## F2: CLOSED (measured)
- deploy-package.py:448 is now `^([0-9]{4})-...(Z|[+-][0-9]{2}:[0-9]{2})?)?\Z`: 9 `\d` became `[0-9]` and `$` became `\Z`; `.match` at :541 is unchanged. No other regex or string in the file changed: the multiset of quoted strings differs only in this one pattern, and the diff shows one line.
- **The C# oracle, mine.** Class ZzG1557Oracle (from the round-1 file, renamed) in a third worktree of my clone at the head (src/ and tests/ equal at base and head: `git diff --quiet` rc 0). It records `CatalogueOverlayStore.Open` (DevStub, a synthetic git repo) and `OpenHosted`. Toolchain: SDK 10.0.404 (`dotnet --version` printed first; DOTNET_ROOT = the project's .tools/dotnet-10.0.404). Restore came from `~/.nuget/packages` only (0 log lines naming nuget.org, GET or Downloading). One build (0 errors), then two `dotnet test --filter ZzG1557Oracle` runs, each Passed 1.
  - HEAVY: `.heavy-lock-1` was taken by atomic mkdir 08:06:48 and released 08:07:09 (holder moved to out/). The load gate read load1 4.37 at 08:04:46 and 3.50 at 08:06:48 (122 s apart; not independent). Node reuse was off. No dotnet, MSBuild or compiler process was left (ps). The oracle file was moved to _quarantine; the worktree has 0 porcelain lines and `git diff --quiet` rc 0.
  - Forms: the 10 new fixture forms, built with the head fixture's own `form_bytes`. Their bytes equal the round-1 gate's 242/244/271/280/341/345-349.bin, 10 of 10. Plus 4 controls and 18 time probes of my own (950-967).
  - Result: two runs, sha256 f09c3f7e... both, byte-identical. Open = OpenHosted on 32 of 32. Controls: good OPENED, writer-shaped good OPENED, one open brace REFUSED, empty author REFUSED. **345-349 (F2) REFUSED; 242, 244, 271, 280, 341 (F3) OPENED.** These equal the round-1 rows and the builder's.
  - **Fixture `refusedByApp` equals my oracle: 14 of 14** (the 10 new forms plus the 4 controls).
- **Head PRE-1 against the oracle: 32 of 32 agree** (stop exactly where the app refuses, or where the fixture lists a knownDifference). Each refusal is one count line (`{'at not a real time': 1}`), rc 1.
  - Valid shapes still pass at head: `2026-10-16`, `T00:00Z`, `T23:59` (no zone), `+14:00`, a 7-digit fraction, a 16-digit fraction, the writer form `.1234567+00:00`. The app OPENS all of them.
  - My probes also stop at head, and the app REFUSES them: Unicode digits in the month, hour, fraction and offset, and a fullwidth leading digit (952-955, 967; base PRE-1 PASSED all five); trailing `\r`, trailing space, leading newline, lowercase `z`, two trailing newlines, a fullwidth Z, and `\r\n` after a date.
- **Both halves of the fix are pinned.** Head with only `\Z` reverted passes 347 and 348. Head with only `[0-9]` reverted passes 345, 346 and 349. Either revert turns test_deploy_pre1_forms.py red.
- **Red first, reproduced.** Head tests and fixture over base's two scripts (a `git archive` copy with src/). test_deploy_pre1_forms.py: Ran 16, FAILED (failures=2), the two property rows only, whose lists name exactly the 5 F2 forms (`rc 0, wanted 1`). test_scripts.py: Ran 56, FAILED (failures=2), the two new xtrace sub-cases only.

## F3: the 5 knownDifference reasons, each read against its line (true)
1. unitCost 7.91e28 and 2. the decimal maximum: `pre1_number` stops at `abs(v) < PRE1_DECIMAL_LIMIT` false (deploy-package.py:536; limit 7.9e28 at :444), so both stop ("at or above 7.9e28": true). The oracle OPENS both. "The app's writer refuses a price above 1000000": true, `Money(errors, "unitCost", ...)` at InventoryEndpoints.cs:90 and :169 checks `value > QuoteEndpoints.MaxMoney` (:381; MaxMoney = 1_000_000m at QuoteEndpoints.cs:34).
3. `0001-01-01T00:00:00.0000001Z`: the pattern does not capture the fraction and `pre1_time_ok` builds the instant without it (:543-552), then returns `when != datetime(1, 1, 1)`, which is false. So it stops. The oracle OPENS it. "The writer takes the audit time from the clock": true, `var now = clock.GetUtcNow()` at InventoryEndpoints.cs:97 and :186, used in the audit entries at :111 and :219.
4. `2026-10-16T00:00:00.Z`: the pattern needs `\.[0-9]{1,16}` (:448), so it stops. The oracle OPENS it. "The writer writes digits after any fraction mark": DERIVED (System.Text.Json's DateTimeOffset writer leaves out a zero fraction and writes digits otherwise). The fixture's writer-shaped form `.1234567+00:00` is consistent with that.
5. `itemClass "service, staging"`: PRE-1 asks for the exact name and stops it ("itemClass undefined"). The oracle OPENS it. "Reads a comma list as flags": true, the reader inserts `JsonStringEnumConverter(namingPolicy: null, allowIntegerValues: false)` (CatalogueOverlayStore.cs:481). It is the same reason as the three existing entries. See R4 for what that reading gives.

## Behaviour preserved (measured)
- Operator words: every `echo "..."` and `stop "..."` string in deploy-from-ci.sh is identical as a multiset (52 at base, 52 at head; diff empty). The word pack is unchanged and still pending the product owner. The order of pre1_hosted, reread_overlay and rollforward_hosted (:236-238) is unchanged. probe and check are untouched (no hunk outside :195-207).
- Run outputs, base vs head (`behave.py`, untraced): count 0 is identical apart from the temp path (rc 0, 1 `az webapp deploy` at both). Count 1 (undecided, git 128) is identical. Token failure injected at the roll-forward's first token call: see R1 (rc 1 and 0 deploys at both).
- The CI python loop (`tools/demo/test/test_*.py infra/tests/test_*.py scripts/tests/test_*.py`, each `python3 -I -v` with cwd at the tree; env -i, PATH=/usr/bin:/bin; Python 3.9.6, bash 3.2.57) at 355fe9e8 and at head: **all 15 files have the same rc and the same `Ran N` (the diff of the two summaries is empty).** test_ci_workflow 8, test_deploy_pre1 44, test_deploy_pre1_forms 16, test_deploy_rollforward 22, test_scripts 56, all rc 0.
  - Red at both, for the environmental causes round 1 named, outside the lane: test_run_demo.py (no node or lsof on that PATH; failures=9, errors=23) and test_infra.py (no Bicep compiler, Ran 0). Hosted CI has both.
  - Test names: 288 and 288, sha256 equal; `comm -23` 0 and `comm -13` 0 (a planted name makes it 1). The round adds no method.
  - The real az is unreachable: `command -v az` under /usr/bin:/bin finds nothing; under the tests' PATH it names scripts/tests/fakes/az; under my own PATH it names /opt/homebrew/bin/az, which the tests never see.
- `bash -n scripts/deploy-from-ci.sh` rc 0.
- Repeats at head: test_scripts, test_deploy_pre1_forms, test_deploy_rollforward and test_deploy_pre1, 2 more runs each, 8 of 8 rc 0 (out/reps.txt).
- Other readers of the changed paths (grep over the head tree): infra/README.md (text), scripts/package.sh and ci.yml (the package job via make, which does not use PRE-1 or the roll-forward), and the four test files above, all run.

## Scans (measured, each with a planted control that fired)
- ASCII: 41 added lines and the 12-line commit message hold 0 non-ASCII characters (a planted U+200B = 1). The fixture writes the digits as `\u` escapes.
- Names, underscore-aware `(?<![A-Za-z])name(?![a-z])`, case-insensitive, over added lines and the message. List: Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite, Tuesday, Wednesday, Friday, Anupam, Philip. Hits: 0. The `_by_<name>_` control fired 14 of 14.
- B-number, finding id ([FN]digit), card or decision id, seat id, GUID, `.local`, and the synthetic token literal: 0 each (9 of 9 controls fired). Host pattern: 2 benign hits, the synthetic test host already in `Sandbox.setUp` and the attribution line.
- gitleaks 8.30.1: a random `ghp_` canary rc 1 first. Then 355fe9e8..881f8dc: 1 commit, no leaks. Then main..head: 3 commits, no leaks.
- CodeQL Python pre-scan over the added lines, test lines included: eval, exec, pickle, shell=True, os.system, subprocess, chmod, makedirs mode, os.open, S_IRGRP/S_IROTH, octal modes, regex from input, skip, expectedFailure, noqa: 0 (controls `eval(x)` and `os.chmod(p, 0o755)` = 2). The test's `os.makedirs` calls pass no mode. JS and C#: none changed.

## Findings
| # | Sev | Where | What | How measured |
|---|---|---|---|---|
| R1 | Minor (words; the builder named it as RESIDUE 1) | deploy-from-ci.sh:200 with :209-210 and :214-215 | When az fails to give a token during the roll-forward, the run now prints 3 lines before the final stop, where base printed 1: the token line, then `newtype count: STOP: the read gave no HTTP answer`, then the listing stop (or the file stop, if the failure comes at a later read). "The read gave no HTTP answer" is said although no read was made. Every line is an existing string; rc 1 and 0 deploys at both. This is the shape the kit spelled out ("the callers stay as they are"). For the word pack, not a code change now. | `behave.py`: a wrapper az fails the Nth token call (N = 3, 4, 5), base vs head. |
| R2 | Note (builder RESIDUE 2) | deploy-from-ci.sh:199 | Each Kudu read calls `az account get-access-token`: 2 plus one per hosted quote or snapshot file. With the real az the cost is UNMEASURED. A token failure in the middle of the loop stops the deploy (the safe side). | Fake az log: 5 token calls per deploy at head versus 3-4 at base. |
| R3 | Note | overlay_forms.json | The fixture pins other-script digits only in the year, day and seconds. Month, hour, fraction and offset digits, and a fullwidth leading digit, were also passed by base PRE-1. They are stopped at head, and the app refuses all five, so the same `[0-9]` change closes them. They are not pinned. Optional: add them in a later pass. | Oracle rows 952-955 and 967 REFUSED; base PRE-1 rc 0, head rc 1. |
| R4 | Note (records) | Dtos.cs:681-691; CatalogueOverlayStore.cs:481 | The app OPENS `itemClass "service, staging"`, and the comma list reads as a bitwise OR of positions: Service (4) OR Staging (7) = 7, which is Staging. So the app would see a staging row. PRE-1 stops this form, so no deploy goes through with it. It matters for the MPSCALC-216 reading of comma lists. | DERIVED from the enum order and the converter; the class read was not run through the app. |
| R5 | Note (builder FOR TUESDAY) | deploy-package.py:50 (`SHA`), :671-672 (`NEWTYPE_FILES`) | Same class as F2: `$` also matches before a trailing newline. `SHA.match(<40 hex> + "\n")` is True (a 39-hex string is False). Low risk: the sha comes from the checkout, and the shell re-checks file names with its own anchored `=~` (:213). | python3 -c. |
| R6 | Note | commit 881f8dc trailer | The commit's attribution line names "Claude Sonnet 5.5". The squash body replaces it. The author name is the repo's own identity (as in commits A and B). | git log. |

## STATUS claims graded
True: the head is a fast-forward and the read-back; files are exactly the 4; the F1 probe numbers (base 2 and 2, head 0 and 0); red-first (2 property rows naming exactly the 5 F2 forms; 2 xtrace sub-cases); the F1 table (:111, :206 FAIL, :283 at base; :111, :199, :283 at head); the 10 oracle rows and the controls; the bytes equal the round-1 bins (10 of 10); the fixture equals the oracle; the F2 forms rc 1 with one count line; the valid shapes still pass; F8 = 22 (the round-1 log ends `FAILED (failures=20, errors=2)`, and `^(FAIL|ERROR):` counts 22); the loop rc and Ran identical; comm 0 and 0; the removed lines; words unchanged; gitleaks; the scans; RESIDUE 1, 2 and 3; FOR TUESDAY item (1).
Not re-measured: the Jira reads (outside my fences); the builder's names-file sha256 (fdcbcf...) differs from mine (cfc40d...) only because our runners print differently, and both lists are 288 names with comm 0 against their own base.
False: none found.

## Anything NEW this round
Nothing defective. The changes are the token move (it removes a leak and adds no word), one regex that only narrows what PRE-1 accepts (it cannot create a new pass of a form the app refuses), 10 fixture entries, and one extended test. R1 and R2 are the side effects of the token move, both safe.

## NOT TESTED
- Hosted CI and hosted CodeQL.
- Any run against a real host, the real az or real Kudu (the real token cost per read, the real listing format).
- test_run_demo.py and test_infra.py to green (no node, no Bicep).
- The runner's own Python and bash versions.
- The app's class reading of a comma list (R4 is derived).
- Time forms beyond the 32 I tried and the 252 in the fixture.
- The roll-forward count against real stored documents.

## FOR TUESDAY
- **Round 2 of 2 closes both Majors.** GO WITH FINDINGS: R1 is words only, R2-R6 are notes. Landing files are in this folder (head-pinned squash at 881f8dc49e046d48f67e2c165dec95ca490f0c20). Nothing is deployed, and a merge deploys nothing (MPS hosted is a card per deploy).
- **Round-1 Minors left to the MPS records pass, restated (all still present at head, untouched by this round):**
  - F4: `rollforward_hosted` runs after `reread_overlay` (deploy-from-ci.sh:237-238), so 2+N Kudu reads now sit between the re-read and `az webapp deploy`. Suggest roll-forward first, re-read last.
  - F5: on a shallow checkout that holds the floor object, `merge-base --is-ancestor` answers 1, and the "older" stop (:225, word line 3) can be false. Suggest treating `git rev-parse --is-shallow-repository` = true as undecided.
  - F6: "N care-pack or staging row(s)" counts JSON objects, and one line can count up to 3 times (draft, result lines, snapshot). Suggest "entries".
  - F7: `|| return 1` at :213 prints nothing before the final "the line above says why"; an overlay-count failure (:156-157) ends with "PRE-1 did not pass" although PRE-1 passed. Both look unreachable in practice.
  - Add R1 (the extra "the read gave no HTTP answer" line after a token failure) and R5 (the `$` at :50 and :671-672) to the same pass. R3 and R4 are optional records items.
- **The word pack, my reading (WORDS still PENDING the product owner; byte-identical to round 1, so the round-1 line-by-line reading stands):**
  - Line 1 (count 0) is accurate.
  - Line 2 (at the floor) is accurate, but "rows" overstates (F6).
  - Line 3 (older) is plain and true on a full checkout and can be false on a contrived shallow one (F5). "A package whose commit contains <floor12>" is more exact than "at or after".
  - Line 4 (undecided) is accurate; "git answered G" is operator jargon.
  - Lines 5-6 (listing, file) are accurate. After this round they also follow a token failure, preceded by the token line and "the read gave no HTTP answer" (R1); suggest the pack say "could not be read" there, or add a token preflight.
  - Line 7 (overlay count failed) is unreachable in practice (F7).
  - Line 8 (final stop) is accurate.
  - The counter reasons are fixed strings with no values.
  - Nothing in the pack prints a store value or a token.
- Evidence (my gate folder /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s275/g1557/):
  - out/probe-xtrace.txt, out/mutants.txt and out/mut-*.log, out/oracle-1.tsv and out/oracle-2.tsv, out/compare.txt, out/pre1-forms.txt, out/behave-compare.txt, out/{base,head}.loop.txt and their names files, out/red-*.log, out/reps.txt.
  - scripts/{probe_xtrace_g1557.py, f1_table.py, gen_g1557.py, oracle_g1557.sh, behave.py, scan_g1557.py, pyloop.py}.
  - The oracle source is in _quarantine/oracle/. The worktrees base/, head/ and otree/ are clean, detached, and never pushed (the push URL is set invalid).
