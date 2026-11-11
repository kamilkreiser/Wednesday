GATE B1512: GO WITH FINDINGS @ 2eba09d on main acd6aec

Why: the five tickets do what they claim at source, all 11 python-job files pass on the head and on the merge with current main, every new row goes red for the right reason under its mutant, and the deploy check fails closed on every unknown answer shape I tried. One Major is a test gap, not a code fault: the new pass-through of az's own exit code is correct at head (gate probe), but no row pins it. If that plumbing broke, a failing `az webapp deploy` could end rc 0.

Tier G1 (Opus). Gate run 2026-11-11 19:09-19:40 AEDT. Own clone and worktrees under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s269/gate1512/` (`repo`, `wt-head`, `wt-merged`, `wt-base`, `wt-mut`). Nothing pushed, no PR, no Jira, nothing deployed, real az never run.

## Pins
- Branch `b1512/mps-lane-l5-ops-tooling` = `2eba09d8efe7e199691eee9706c62e6aa7da35df`, read at source with `gh api -X GET repos/datasecau/MPS-Commercial-Calculator/git/ref/heads/b1512/mps-lane-l5-ops-tooling` (project GH_CONFIG_DIR). The branch is 5 commits on base `5cd6002f`, and `merge-base origin/main 2eba09d8` = `5cd6002f`.
- Main = `acd6aec03e707a2c6fb30ac9adeccb4230b05764` (same `gh api` read of `heads/main`). Main is 1 commit ahead of base (PR #176: `src/` and `tests/` only).
- `git merge-tree --write-tree origin/main 2eba09d8` gives rc 0 (clean), tree `1d584f4c`. I committed that tree locally as `4241e6ab` for the `wt-merged` worktree (never pushed). Lane paths in the merged tree are identical to head (`git diff --quiet 2eba09d8 HEAD -- scripts infra tools .github` rc 0).
- 14 files changed. Every file is under `scripts/`, `infra/` or `tools/demo/`, and `.github` is untouched.

## Findings

| # | Sev | Ticket | Finding | Evidence |
|---|---|---|---|---|
| 1 | Major | MPSCALC-126 | **Nothing pins the new az exit-code pass-through.** `deploy_out="$(az webapp deploy ... -o json ...; printf 'x%s' "$?")"`, then `deploy_rc="${deploy_out##*x}"`, then `if [[ "$deploy_rc" != 0 ]]; then exit "$deploy_rc"; fi` (`scripts/deploy-from-ci.sh:201-205`) is new code. It replaces the old `set -e` behaviour on a bare `az` call. Mutant 126-F (that `if` line replaced by `:`) leaves every row green: test_scripts 51/51 and test_deploy_pre1 37/37. Under that mutant, a deploy call that fails (rc 1, 7 or 130) after printing a RuntimeSuccessful document ends **rc 0**, so the script reports success when Azure did not. At head the behaviour is correct. My probe `test_g126_az_failure_keeps_its_exit_code_and_stops_before_the_check` passes at head (rc equals az's rc, no `== deployed` line, no wwwroot download) and goes red under 126-F (`0 != 1`, `0 != 7`, `0 != 130`). The code is right, so this does not block. **Follow-up: add that row** (the probe can be adopted as is). | `out/mutants-126.txt` (126-F block); `out/probes-head.txt`; probes under mutant printed in the session; `probes/gate_probes.py` |
| 2 | Minor | MPSCALC-126 | `-o json` (builder deviation (a)) is not pinned. Mutant 126-E (`-o json` dropped) leaves test_scripts and test_deploy_pre1 green. If it were lost, an operator with `core.output` set to table or tsv would get exit 3 on every good deploy. My probe `test_g126_az_called_with_o_json` pins it: green at head, ERROR under 126-E. | `out/mutants-126.txt` (126-E) |
| 3 | Minor | MPSCALC-126 | **The operator could misread the end of a run.** The new NOT PROVEN line goes to stderr at the deploy step (`:211-212`). The run then prints the success-shaped lines `== <site> holds exactly the verified package ...`, `== HSTS on ...` and `== /health is not compared ...`, and ends `exit 3` with no line of its own (`:259`). Someone reading only the tail sees success lines and an exit 3. Also, the usage header at `:21` still defines exit 3 only as "the live site differs from its package, or could not be read"; it does not mention an unreported start. Suggest repeating one line at `:259` and adding the meaning at `:21`. | `scripts/deploy-from-ci.sh:21,206-215,242-259` at 2eba09d |
| 4 | Minor | MPSCALC-203 | **The STOP wording contradicts itself on a changed overlay.** `:166` prints "the hosted overlay changed after PRE-1 passed, so nothing was deployed; the new overlay copy is kept: <path>". Then `:175` reuses `stop "PRE-1 did not pass (above); nothing was deployed"`, so the operator reads "PRE-1 passed" and then "PRE-1 did not pass". A failure at the re-read (HTTP code, token) is also labelled `PRE-1:`. Both are safe: rc 1 and nothing deployed. | `scripts/deploy-from-ci.sh:163,166,175` |
| 5 | Minor | MPSCALC-173 | **A dry run does not check `--out-dir`, but the docstring, `--help` and the commit subject say it "checks everything a real run checks".** With `--out-dir` outside a work tree, a real run REFUSES with rc 2 and the dry run says rc 0 "3 would be created". `prepare_out_dir` is skipped wholesale (`tools/demo/seed.py:679`), including its read-only git checks. Either run the read-only part of the checks, or say plainly that the out-dir is not checked. | `out/allexist173.txt` ("bad out-dir [] rc 2" / "['--dry-run'] rc 0") |
| 6 | Minor | MPSCALC-173 | When every chosen scenario already exists, the dry run returns at `seed.py:709` (`if not todo: return 0`) after the "exists, skipped" lines. It never prints its "seed: dry run: ... Nothing was created." line, so the docstring's "The last line says nothing was created" is false on that path and the output does not say it was a dry run. | `out/allexist173.txt` (dry run after a real `--only S1,S2,S3`) |
| 7 | Info | MPSCALC-126 | `numberOfInstancesFailed` is not consulted, so RuntimeSuccessful with 1 up and 2 failed passes. This follows the kit's predicate. Installed az 2.92.0 returns a partial start as `RuntimeFailed` with rc 0 (`custom.py:11286-11292` logs and `break`s), and that case is now refused (exit 3). | `test_g126_partial_failure_with_runtimesuccessful_is_accepted` (green) |
| 8 | Info | MPSCALC-203 | With the retry dropped and a second read added, a transient Kudu blip on either read now STOPs the deploy (rc 1, nothing deployed, copy kept 0600). That is fail-safe, never a false success: the operator re-runs. A clean deploy makes 2 overlay GETs and 2 `az webapp show` calls where it used to make 1 of each. | `test_g203_reread_curl_transport_failure_stops_and_keeps_0600_in_0700`, `test_g203_one_get_per_read_on_the_wire` |
| 9 | Info | MPSCALC-201 | Entra is eventually consistent, so the `GET /groups/<id>` right after the POST can 404 briefly. The run then stops with the generic `az rest failed` text, not the new sentence. A re-run finds the group through `find_all_roles_group` (`entra_apps.py:182`). This is safe (it stops, assigns nothing to the group), but the operator sees a less clear line. | source reading |
| 10 | Info | MPSCALC-119 | The validate.sh stop sentence ends "(this test never calls az)", reused verbatim from `infra/tests/test_infra.py:66` as the kit ordered. Coming from a script, "this test" is slightly odd. The README's what-if runbook steps still use `az deployment ... -f infra/main.bicep` (a login step, not a validate route); that is out of scope. | `infra/scripts/validate.sh:14`; `infra/README.md:36` |
| 11 | Info | MPSCALC-203 | ANSWER-2 allowed "one" added assertion in `test_203_vii`. The builder added a helper line and two assertions (`len(reread) == 1` plus the named line). This only strengthens the test: no existing line changed beyond the three authorised counts. | `git diff 5cd6002f 2eba09d8 -- scripts/tests/test_deploy_pre1.py` |

**Counts: Blocker 0, Major 1, Minor 5, Info 5.**

## What I checked, by the brief's seven points
1. **Fail-closed 126.** I read `scripts/deploy-from-ci.sh` at head whole. My 15 unknown shapes all end exit 3, with the NOT PROVEN line and with the byte and HSTS checks still run: a list, `null`, a Kudu record, bool, float, string, negative or 10^7 instances, a lowercase status, a status at the top level, a renamed field, two documents, text before the JSON, `properties: null`, `status: null`. Byte-exact echo held for answers with a trailing space, a trailing `x` and embedded `x1x2x` (the marker parse is right). If both start and bytes are bad, both lines print. The script runs under `/bin/bash` 3.2.57 (`bash -n` rc 0). I read the installed az 2.92.0 source with sed only: `_poll_deployment_runtime_status` returns the status document (`custom.py:11249-11372`), and a 503 on the status API falls back to the Kudu record (`:11226-11244`, which now gives exit 3). The B268 recorded answer has `numberOfInstancesSuccessful: 1` as an integer (`Briefs/2026-10-18_B268_evidence/05_deploy.txt:28`).
2. **203.** `pre1_seen` is the sha256 of the very copy `deploy-package.py pre1` just passed (`:140-142`). The re-read hashes a new copy (`:156-171`). A re-read failure stops the deploy in every form I tried: second token failure, second `scm_host` failure, curl rc 28, HTTP 503 (gate probes and `test_203_xi_c`). The folder is 0700 and the file 0600 under umask 022, for a fresh and for a pre-existing 0755 folder, on the clean, STOP, re-read-STOP and probe paths. The retry is dropped from the overlay read only (`:111`); the wwwroot download keeps it (`:223`).
3. **201.** The read-back requires `mailEnabled is False` and `securityEnabled is True` on the GET answer (`entra_apps.py:175-178`). `None` or `{}` fails closed. The fake stores a different record than the POST echo, so reusing the POST answer cannot pass (mutant 201-A turns `_a` and `_b` red). The Stop text says "earlier steps of this run already changed things" and never "nothing changed".
4. **173, proven by program.** An audit hook (`sys.addaudithook`: `urllib.Request`, `socket.connect`, `open` with write flags, `os.mkdir/rename/remove/chmod`, `subprocess.Popen`) ran `seed.main --dry-run` against the loopback stub in 7 modes: loopback, loopback+purchase, hosted Seller, hosted both roles+S4, hosted `--reset-demo`, `--client-credentials` with a recording token opener, and `--client-credentials` with the DEFAULT opener. Result: **0 non-GET, 0 main-thread write-opens, 0 fs/process events, connects to 127.0.0.1 only, out dir never created, token opener calls `[]`**. Positive control, the same harness without `--dry-run`: 7-10 non-GET, 3-4 writes, mkdir, git subprocesses (`out/audit173-head.txt`, `out/audit173-control.txt`). All HTTP goes through two sends: `Api.call` (guarded at `seed.py:211-212`) and `client_credentials_token` (unreachable in a dry run, `:683-686`).
5. **119.** `az bicep` appears 0 times in `infra/scripts/validate.sh` and `infra/README.md` at head (`/usr/bin/grep -i -c`; control at base: 2 and 1). In the repo at head, the only `az bicep` left is `ci.yml:78` (the CI install step, not lane) and the new test's own assertion string.
6. **New operator words.** All five groups are ASCII (0 non-ASCII added lines; control 1). They print no host, id or value; the 126 line prints only the parsed status word (letters only, else `?`) and an integer. Paths printed are local `.local/...` copy paths, as at base. Misleading wording: Findings 3 and 4.
7. **Red-first in a throw-away worktree** (`wt-mut`, each mutant restored, `git diff --quiet` rc 0 after each, porcelain empty at the end). Every builder row went red under its mutant except the two plumbing lines of Findings 1 and 2:
   - 126-A `<1`->`<0`: `_ii` red.
   - 126-B status compare removed: `_iii_b` red.
   - 126-C final exit removed: `_i`, `_ii`, `_iii`, `_iii_b` red.
   - 126-D exit before the checks: the same four red.
   - 126-G check also on probe: `_v_a` plus 3 existing rows red.
   - 126-E and 126-F: **no row red**.
   - 203-1a no chmod: `ix_a`, `ix_b`, `ix_c` red.
   - 203-1b no umask on create (M183-3): 9 rows red, including `ix_a`, `ix_b`, `iii_a`, `iv`, `v`, `vi`, `x_b`, `xi_b`.
   - 203-1c no umask, no chmod on the folder: `ix_a`, `ix_b`, `ix_c` red.
   - 203-3 retry back: `x`, `x_b` red.
   - 203-4a no re-read: `ix_a`, `vi`, `vii`, `xi_b`, `xi_c`, `xi_d` and `test_an_absent_overlay_is_0_entries_and_deploys` red. This includes **all three changed counts**, as ANSWER-1 item 3 and ANSWER-2 item 3 require.
   - 203-4b compare always equal: `xi_b` red.
   - 203-4c re-read failure ignored: `xi_b`, `xi_c` red.
   - 203-4d `pre1_seen` not recorded: 7 red.
   - 203-4e changed copy deleted: `xi_b` red.
   - 203-4f re-read hash replaced by the PRE-1 value: `xi_b` red.
   - 119-A az route restored: both rows red.
   - 201-A: `_a`, `_b` red. 201-B: `_b` red.
   - 173-A guard removed: `_e` red.
   - 173-B guard and the `seed_one` branch removed: `_a`, `_b`, `_e`, `_f` red.
   - 173-C out dir made in a dry run: `_a`, `_f`, `_i` red.
   - 173-D client-credentials asks for a token: `_g` red.
   - 173-E `seed_purchase` branch removed: `_i` red.

## Changed expectations (ANSWER-1/2), verified
`git diff -U0 5cd6002f 2eba09d8` over the test files removes exactly three lines, all in `scripts/tests/test_deploy_pre1.py`. Each is replaced by the same assertion with the count plus one and a comment:
- `len(self.overlay_reads())` 1 -> 2
- `len(names)` 2 -> 3
- `len(kept)` 1 -> 2

No other line of any existing test is removed or changed, and no test is renamed (0 names lost). Additions in `test_203_vii` are as in Finding 11.

## What I ran (counts)
- **The python-job loop of `ci.yml:86`** (`python3 -I -B <file> -v` per file, BICEP = the project's standalone 0.48.1, tripwire az first after the tests' own fakes):

| Tree | Files | Tests | Result |
|---|---|---|---|
| head | 11 | 236 | 11/11 rc 0 |
| merged with main | 11 | 236 | 11/11 rc 0 |
| base | 10 | 200 | 10/10 rc 0 |

   test_run_demo was 23/23 on all three trees.
- **Test names:** lost 0, gained 36 (`comm`; control: one line removed shows lost 1). Head and merged name lists are identical.
- **Gate probes:**
  - `probes/gate_probes.py`, 10 rows (~30 subtests): head 10/10 pass; base 21 failures and 1 error, as expected.
  - `probes/audit173.py`: 7 dry-run modes plus 5 control modes.
  - `probes/allexist173.py`.
- **Mutants:** 24 (7 for 126, 10 for 203, 1 for 119, 2 for 201, 5 for 173), plus the gate probes under 126-E and 126-F.
- **Static checks:**
  - `bash -n` on the two shell files under bash 3.2.57: rc 0.
  - `compile()` under Python 3.9.6: 5 files.
  - ASCII scan: 0 non-ASCII added lines (control 1).
  - Secret regex (`ghp_`, `AKIA`, `-----BEGIN`, `eyJ`) over added lines: 0.
  - Name, B-number, seat and card scan over added lines and the 5 commit messages: 0 (control 7).
  - Hosts in added lines: only the synthetic `*.example.test` and `app-mpscalc-showcase-abc123.azurewebsites.net`, plus the all-zero GUID.
  - Digit-dot-digit: only `127.0.0.1`.
  - Commit identities: all 5 are `kamil.kreiser@datasec.com.au` for author and committer. Each commit message names exactly one ticket.
  - Readers of the changed files from `src`, `tests`, `web` and `.github`: one comment line in `ci.yml:3`, no read.
- **Tripwire:** `TRIPWIRE-HIT.log` is absent after every loop, probe and mutant run (control: a direct call created it, then I moved it to `_quarantine/tripwire-control.log`). `command -v az` under the run PATH printed the tripwire; inside the tests it is the fake.
- No dotnet run, so no heavy lock was taken. No listener was started by me; the existing tests' ephemeral loopback ports only.

## NOT RUN
Hosted CI and CodeQL on the PR; any real deploy or any run of `deploy-from-ci.sh` outside the tests; real `az` (not even read by path, only package source files with sed); any Entra run; any hosted seed; shellcheck (not installed); the dotnet, web and package jobs (no file they read changed). The builder's INCIDENT (one stray no-argument `az` start at 18:16) is relayed only. I did not read `4_Credentials/.azure` to check it.

## Corrections to the builder's record (`1_Project_Definition/Briefs/2026-11-11_B1512_STATUS.md`)
- FOR TUESDAY "Seen outside scope" calls the `test_run_demo` C5 reds load-sensitive ("failed ONCE ... at load average above 20"). That contradicts its own BASELINE, which proves the cause was SIGINT ignored in a background-started runner. At the gate, test_run_demo was 23/23 on base, head and merged, so it is not a lane red.
- BLUF and CHECKS say the loop was rc 0 "on all 11 files except test_run_demo". At the gate all 11 were rc 0 on head and on the merged tree.
- Ticket 173 (commit subject, docstring, `--help`, STATUS): "checks everything a real run checks" is not true for `--out-dir` (Finding 5). "The last line says nothing was created" is not true when every scenario exists (Finding 6).
- Ticket 126: "a failing az still ends the run with its own code" is true at head but pinned by no row (Finding 1). `-o json` is also unpinned (Finding 2).
- Kit fact: the head adds 36 rows. STATUS lists them correctly. Its gained-name list matches mine.
