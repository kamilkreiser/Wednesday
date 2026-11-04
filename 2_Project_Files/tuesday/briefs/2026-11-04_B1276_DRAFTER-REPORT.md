STARTABLE: YES (after the stamp). One caution: the machine load1 read 12.86 at 13:58 AEDT, but the kit runs no heavy job (no npm, no node), so it is a wait for nothing.

# B1276 drafter report (SEAT-M93, MPS lockfile re-push of the undici and zod bumps)
Drafted 2026-11-04 13:54 to 14:00 AEDT (clocks from `date`). Files: kit `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-04_B1276_SEAT-M93_mps-deps-undici-zod-repush.md` (116 lines, 9 slot lines incl. the last; `grep -c` of four underscores prints 9, control: the Step-0 refuse line quotes them split and is not counted), `.../2026-11-04_B1276_slots.json` (9 keys, drafter's measured facts only plus `@NOW@` and `@SEAT@`), this report. M-number: `ls` of the briefs folder filtered by `/usr/bin/grep -i 'SEAT-M93'` printed nothing (control: the same filter on `SEAT-M92` printed two files), so M93 is free as asked; B1276 also unused.

## BLUF
- Main is still `60ac2e5b214c9e9f3a6c2da329bbb0c5996f4822`; both PRs unchanged (#120 head `80f336a6...`, #121 head `19893df0...`, clean, 1 commit and 1 file each). No `b1276` ref exists.
- The kit commissions ONE commit on `b1276/mps-deps-undici-zod` carrying both bumps; the deciding property is the lockfile blob `7c7d4608f669a19e4b52c963cdb4debb81d6f879` and a one-path diff.
- I re-derived that blob independently: from the three raw blobs (base `4e20034b`, #120 `84043c1a`, #121 `6c4123d1`, each re-hashed equal to its sha) `git merge-file -p` exits 0 and hashes to `7c7d4608f669a19e4b52c963cdb4debb81d6f879`. Control: base/base/#121 hashes to `6c4123d1`.
- Model: Sonnet 5.5, row C2 (`model-routing.md:92`), id `models_latest.json:23`, `BRIEF_SEAT_LEVEL=sonnet` inside the quotes.
- Trap found: both Dependabot commits have parent `511e6c03`, not main `60ac2e5b`; the cherry-picks are three-way applies, which the kit says. The local `2_Project_Files` checkout lacks all three commits (`cat-file -t` fails), so the kit has the seat do ONE fetch.

## FACTS (instrument; control)
1. Main sha: `gh api -X GET .../branches/main --jq .commit.sha` and `git ls-remote ... refs/heads/main` both print `60ac2e5b...` (control: ls-remote also answered for `refs/heads/b1276*` with nothing).
2. `compare 511e6c03...60ac2e5b` files: one, `tests/MpsCalc.Engine.Tests/ComponentQuantityRuleTests.cs` (nothing under `web/`).
3. Lockfile blobs by the contents API: main `4e20034b53b6f28684370b2c75f2fea579f60beb`, #120 head `84043c1a2faf51108cf62e30d1e2542d9c9f175b`, #121 head `6c4123d1183f2c7ba35cc4c6c2af2cabd4dc2035` (equal to the gate's values; each also re-hashed locally by `git hash-object`).
4. Dependabot commit parents, read in the gate's clone with `rev-parse <sha>^` (read verb, no write): both `511e6c037ce029835c94b2400930bb6755009a30`.
5. Open PRs by `pulls?state=open`: 121 and 120 only. `matching-refs/heads/b1276` 0, `b1270` 0, control `b1255` 1.
6. Workflow triggers (`ci.yml` at `60ac2e5b`, `awk NR` 10-14): `push` to main only, `pull_request`, `workflow_dispatch`: a branch push alone starts no run; stated in the kit so the seat does not read the 0 runs as a failure.
7. PR bodies read by `gh api -X GET pulls/<n> --jq .body`: #120 7472 bytes, 5 distinct GHSA and 5 CVE ids (`grep -o -E`); #121 4581 bytes, 0 ids, carries the upstream maintainers' disclosure. The kit's PR text relays these as RELAYED and tells the seat to re-check each id against the live #120 body and drop any it cannot find.
8. Landing rule at source (`awk NR`): `CLARIFICATIONS.md:758` and `:774` (squash, head pinned, MPS convention); quoted in the kit.
9. Model row: `model-routing.md:92` is C2 (builder, Sonnet 1st); `:108`-`:109` G1/G2 not needed (no gate commissioned). `models_latest.json:23` `"model_id": "claude-sonnet-5-5"`; `brief_seat.sh:24` `LEVEL="${BRIEF_SEAT_LEVEL:-opus}"`.
10. Live panes `tmux list-panes -a -F '#{pane_id} #{@cockpit_name}'`: `tuesday`, `fleet-monitor`, `Datasec/HPSM-POC-D49`, `Datasec/NexusAI-R171`, `Datasec/HPSM-POC-H117`; no `Datasec/MPS-*`. `.tools` of the project: `b1255`, `b1262`, `b1270` exist, `b1276` does not (control `b1270` found); no `heavy.lock`, `light.lock` or `.tools/.git-lock` (glob/ls reported no match; the glob control is `b1270` existing). Ports: `lsof -nP -iTCP -sTCP:LISTEN` shows 49152, 5000, 59869, 7000, 8770, 49166, 49168, 49171, 9711, 9714; the kit binds none. Word scan of the non-`.pre-` SEAT kits of 11-03 and 11-04 for `M93|B1276`: 0 hits (control: `M92` in the B1255 kit is found by the earlier filter).
11. Repo identity: `2_Project_Files` `remote.origin.url` is `git@github.com:datasecau/MPS-Commercial-Calculator.git`; `core.sshCommand` carries the project deploy key (key path hidden); `gh auth status` under the project `.gh-config` shows account `kamilDatasec`.
12. gitleaks `/opt/homebrew/bin/gitleaks` exists (`which`); the gate used 8.30.1 with the same canary method.

## D-decisions (the drafter's)
- D-1 One commit by `cherry-pick --no-commit` of both, own plain message (not the two bots' messages, which carry release-note text). The fallback for a git refusal makes two commits; the TREE property still decides.
- D-2 Base is origin main as re-read, not forced to `60ac2e5b`, but only if the move touches nothing under `web/` and not `ci.yml`, and the base lockfile blob is still `4e20034b` (the brief's wording).
- D-3 No `npm` run by the seat (the brief says the gate already ran the identical lockfile); the PR body says tests were not re-run on the branch and that the PR's CI is that check.
- D-4 The PR body is written in the kit as a literal block the seat copies after checks (ids re-grepped against live #120), so Tuesday reads the exact public text at the stamp.
- D-5 The kit says #120 and #121 are closed unmerged by Tuesday after landing; the seat does not touch them (no `@dependabot` command either).
- D-6 No gate commissioned in the kit (none asked); the tree equals a blob the gate measured, and CodeQL plus `ci` on the PR are the remaining checks.

## Q-questions for Tuesday (each with a default)
- Q-1 Should a tier-2 gate follow? Default NO: the blob is the gate's own; Tuesday reads the PR's `ci` and CodeQL runs.
- Q-2 Wording of the PR body: it quotes five GHSA/CVE ids and the zod maintainers' disclosure as RELAYED. Default: keep (public, from the Dependabot text).
- Q-3 Keep `git config` identity (the repo-local user, which prints as the project owner's name in the commit author)? Default yes; the kit makes the seat print it, not change it. If the commit must not name a person, say so before launch.
- Q-4 GATE-ROUND slot: default "no round counted".
- Q-5 Launch form: the kit uses `fleet/cockpit/cockpit.sh add` as the rules file shows; the B1255 precedent used `launch_when_cool.sh`. Default: either, level inside the quotes.

## UNMEASURED
- That `git cherry-pick --no-commit` of the second pick applies cleanly onto main with the first staged, at the seat's git version: the gate did it (rc, no conflict) and my `merge-file` result matches, but I ran no `cherry-pick` (forbidden). The blob check at Step 4 decides.
- `git diff --numstat` of `6 6` through `git diff` (the gate's `6 6` came from `--no-index`); the kit says a different count is reported, the blob decides.
- Whether the CodeQL `dynamic` run starts on a PR opened by Tuesday on this head: RELAYED from the earlier #157 evidence (head `c313bb47`, actor `kamilDatasec`) and the gate's landing note; I did not re-query code-scanning analyses (not asked) and did not run `git worktree list` (forbidden verb), so old worktrees under `2_Project_Files/.tools/wt-*` are unexamined (none is a `b1276` name).
- Machine-wide load at launch (12.86 at 13:58, the sample is mine; it fell from a peak shared with other seats).

## Outside the fences
None. Reads only: the briefs folder, the gate's STATUS and evidence (project-side, read), the project's CLARIFICATIONS lines, the PR/commit/contents/blob/compare/matching-refs/branches endpoints by `gh api -X GET` under the project `.gh-config`, `git ls-remote`, `git cat-file`/`rev-parse`/`log` (read verbs, with `--no-optional-locks`), `tmux list-panes`, `lsof`, `uptime`, `df`. Three blobs and two PR bodies were written to the session scratchpad (`.../scratchpad/b1276/`) for the `merge-file` check, outside any git tree; `git merge-file` and `git hash-object` ran on those scratch files only. The gate's clone `.tools/b1270/clone` was read by `git log`/`rev-parse` only (a read of another seat's tree, for the two commit parents); no write anywhere but my three files.
