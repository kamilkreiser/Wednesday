STARTABLE: YES (once stamped; the four Q-questions below each have a default that keeps it startable)

# B1050 drafter report: SEAT-G259, NexusAI RD-913 tier-2 gate of branch b1045/nexusai-rd913-audit-highs @ 79dc9f59

## BLUF
- **Kit:** `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1050_SEAT-G259_nexusai-rd913-gate-tier2.md`.
  - 113 lines, sha256 `1e40b5df404952810fb350bbc6e8e7ae9bcd1a917c4db08fdbc0cdfd065e3b1f`.
  - Slot lines: 8 (7 slots and the last line).
  - `@X@` tokens: 0 (control: 1).
  - Non-ASCII bytes: 0 (`python3 -I` byte count; control: a planted e-acute reads 2).
  - Owner, staff and reviewer names: 0 by a word-bounded grep (control: Tuesday's `CLAUDE.md` reads 31).
  - I did not create a `.pre-stamp` copy. Tuesday makes it before stamping.
- **Shape:** copied from the B1023 gate kit: REFUSE, THE WORK as C1-C13, MAIN-MOVED, GRADING G-1..G-4, ROUND COUNT, LOAD, HOLDS, STANDING LINES, PARTITION, VERDICT, LANDING, Stamp. The checks follow B392's lock-only method (EQ with a second instrument, registry integrity, base audit by `--package-lock-only`, canary-first gitleaks).
- **Subject:** a branch with no PR, re-pinned at 14:30:46.
  - Branch `79dc9f59` sits on main `89375808`: ahead 1, behind 0.
  - The diff touches only `package-lock.json` (+6 -6).
  - Tree `f633f244`, whose parent is main. So the merge tree must equal the head tree.
- **My own packages-map diff of the two locks (raw GETs) agrees with the builder:**
  - Exactly 2 changed keys, each changing only version, resolved and integrity: follow-redirects 1.16.1 -> 1.16.2, joi 18.2.9 -> 18.3.1.
  - 0 keys added, 0 removed, 691 keys on both sides.
  - Neither entry is dev. Root `packages[""]` is unchanged.
- **The branch's hosted npm-audit is red, which is expected:**
  - Run 41269219163, job 124738325576.
  - Log by GET: moderate 12, high 0, total 12.
  - follow-redirects and joi appear on 0 lines each (control: archiver 4).
- **Port block 9730-9739:**
  - `lsof` empty (rc 1; control: the unrestricted listing has 24 lines).
  - `973[0-9]` hits 0 of the 81 non-`.pre-` SEAT kits for 10-31 and 11-01 (control: `97[0-9][0-9]` hits 14, including B1044's 9720-9729).
  - It is neither 8470-8479 nor 9720-9729.
- **Seat G259:** 0 hits word-bounded in `tuesday/briefs` and the NexusAI Briefs (control: G253 hits 19 files).
- **Deploy:** a merge STARTS a Deploy demo run, because `package-lock.json` is not in `paths-ignore`. Both jobs skip while `CI_DEPLOY_ENABLED` is unset.
  - Repo variables 0, organization variables 0, environments `[dev]`.
  - The last 5 runs all skipped.
  - Main `89375808` was a HISTORY-only push and started no run: the positive control for `paths-ignore`.
- **The PR body is required to say:** "The audit-production-deps check stays red after this merge: 12 moderate rows remain ... RD-913 stays open for the product owner's ruling on them". `merge-body.txt` carries the same point. The gate checks both by program.
- **Live state at drafting:**
  - B1044 (`Datasec/NexusAI-M62`) HOLDS the jest lock (`tag=b1044-build-nbafter`, since 03:30:34Z).
  - load1 was 22.35 at 14:32.
  - The kit tells the gate to wait in the FIFO and never pre-empt. `launch_when_cool` holds the launch below load1 7.

## Facts re-measured (instrument, control)
- Pins: `git ls-remote` of the shared checkout's origin returned main `8937580841a39123f32955c3df067af01544418e` and branch `79dc9f59b573b5a6fbf006a93cbf7d5a5473dfce`. `refs/heads/b1050*` none.
- `compare` via `gh api -X GET` under the project GH_CONFIG_DIR:
  - ahead 1, behind 0, the single file above.
  - Head lock blob `2e64988d`.
  - Commit message read whole (graded in the kit's C10).
- PRs: 0 open (control: `pulls/99999` 404).
- Blobs at the head by raw GET plus `git hash-object`: package.json `3908a828` (104 lines), counts `7680a3ff` = 5267/311, `npm-audit.yml` `61a6804d` (51), `build.yml` `e4e5c095` (84), `deploy-demo.yml` `597b3487` (182), `verify-suite.sh` `eb9731f5` (367).
- Lock at main: `050c1a2a`, 8912 lines.
- CI predicate lines, quoted in the kit:
  - `npm-audit.yml` lines 34, 42 and 49.
  - `build.yml` lines 3-9 and 83-84.
  - `verify-suite.sh` lines 343, 354 and 366.
  - `deploy-demo.yml` lines 26, 28, 29, 53, 91 and 95.
- Advisories by GET (control: `GHSA-zzzz-zzzz-zzzz` 404):
  - mrwp: high, `>=1.16.0 <=1.16.1`, patched 1.16.2, CWE-201, the `sensitiveHeaders` option.
  - 4528: high, `>=18.0.0 <18.3.1`, patched 18.3.1, CWE-1333, `string().email({ multiple: true })`.
- Main's npm-audit runs: `89375808` failure, `88144175` failure, `a4a227dc` success (2026-10-30T01:11Z, before the advisories were published on 10-30 at 22:59Z and 23:10Z).
- Rule types on main: deletion, non_fast_forward, code_scanning, required_status_checks. That the status-check list is empty is RELAYED from B1045/B1023; I did not re-read the list's contents.
- Lock tool sha256 `cf01bafb...4971f` equals B1045's stamp. `queue-jest/` is empty, and the lock is held by B1044 (owner file read).
- Model: `models_latest.json:23` `claude-sonnet-5-5`. `model-routing.md` rows: G2 at line 109, G1 at 108, G-cap at 111 (C2 92 and C3 93, as B1045 cites them). `brief_seat.sh:24` `LEVEL="${BRIEF_SEAT_LEVEL:-opus}"`.
- Landing rule source: `CLARIFICATIONS.md` C-190 at line 2062, item 2 at line 2067 ("Never squash, never rebase"), item 3 at line 2068, the wait rule at line 2073, the addendum at line 2076. C-68 at line 665, C-196 at line 2134, C-224 at line 2412. EXPIRING-GRANTS line 30 holds the merge grant's exclusion.

## D-decisions
- **D1. A new class, round 1 of 2.** Census over the first lines of `Briefs/*_STATUS.md`: 106 files, 36 gate verdicts. NO GO: B592, B647, B667, B906, B912, B926; none is a lock-only subject (control: a scratch NO GO line counts 1).
  - Lock-only precedents: **B392** (RD-879, PR #104, one entry, GO WITH FINDINGS, no round clause) and **B612** (PR #108, a Dependabot multi-package change, GO WITH FINDINGS round 1 of 2).
  - **RD-881 (PR #107) was never gated.** B605 STATUS line 80: "No separate QA gate report exists for this PR; it merged on the coordinator's GO". The commission's premise of "RD-879/RD-881 lock-raise gates" is therefore half true. B1045's kit line 3 also says both were "each gated at tier 2", which is wrong for RD-881.
  - Different tickets, heads and advisories, and 0 NO GO on any lock-only subject, so the new class is round 1 of 2 however it is grouped.
- **D2. Tier: Sonnet G2 (line 109), "follow-ups whose mechanism a prior gate already measured" (B392 measured the lock-only mechanism at tier 2).** G1 (line 108, security surfaces) was considered, because follow-redirects decides credential-header forwarding. I did not take it: the delta is two registry tarball pins with no code. Instead the kit makes a C6 finding of product code that depends on the OLD behaviour (`sensitiveHeaders`, or `email` with `multiple`) an Escalation STOP to tier 1, per G2's own text "a Sonnet G2 that finds a security-shaped issue hands the PR to G1". See Q-1.
- **D3. Mutants for a lock lane (C4):**
  - NOOP.
  - MF and MJ: revert one whole entry to main's. Expected: `--package-lock-only` audit rc 1 naming exactly that package. This is a per-package red-first proof.
  - MS-J and MS-F: plant a version outside its declaring range. Expected: the semver table fails.
  - MC: an extra changed key. Expected: closure.py flags it.
  - MP: a one-byte change to package.json. Expected: the byte check flags it.
  - All run on scratch copies; no worktree file is edited.
- **D4. Second audit instrument.** `--package-lock-only` on scratch copies runs beside the `npm ci` tree audits (B392's base method). The two must agree.
- **D5. B1044 landing first is handled as "EXPECTED BUT RE-VERIFY"** in the MAIN-MOVED RULE. If B1044 lands first, the merge result is no longer the head tree, so the gate builds `worktrees/b1050-merge`, runs `npm ci` there, and runs one more verify against the new counts file. The audits are unchanged.
- **D6. Merge trailer** in `merge-body.txt` is `Co-Authored-By: Claude Opus 5.5`, following B1023, because Tuesday (Opus) performs the merge.
- **D7. Hard stop.** I suggested target 120 and HARD STOP 210 minutes. The verify takes about 25 minutes, the work is lighter than B1023's (no shape boots), and a jest wait behind B1044 is likely.
- **D8. Gitleaks.** The kit adds `gitleaks dir` with `.gitleaks-lockfile.toml` if that file exists. B1045 MEASURED that the range scan does not cover the lock, which sits under the default allowlist. I did not verify that the config exists at the head; the gate says whether it does.

## Q-questions for Tuesday (each with a default)
- **Q-1 Tier.** G2 Sonnet, with C6's Escalation to G1, or G1 Opus outright because follow-redirects is a credential-header library? **Default: G2 Sonnet.** The mechanism was gated at tier 2 in B392, the delta holds no code, and B1045's reachability read found 0 `.email(` in `backend/` (RELAYED; C6 re-measures it).
- **Q-2 Ports.** Is 9730-9739 accepted? **Default: yes** (0 kit hits, `lsof` empty, distinct from 8470-8479 and 9720-9729).
- **Q-3 Order against B1044.** If B1044 reaches READY first, does its gate or this one land first? **Default: this one lands first** (C-196, line 2134: a security fix to shipped dependencies may take the next merge turn by Tuesday's word). The kit covers either order.
- **Q-4 Seat number.** **Default: keep G259** (0 hits; G258 is the latest used).

## UNMEASURED
- The joi and follow-redirects reachability at the head. I relied on B1045's read (0 `.email(` in `backend/`) and did not run a `git grep` at the head (C6 does).
- The contents of the `required_status_checks` list and the CodeQL thresholds (types only, read at 14:31).
- Whether `.gitleaks-lockfile.toml` exists at the head.
- The jobs of each of the last 5 Deploy demo runs. I read only the run-level `conclusion` skipped; C11 reads the jobs.
- Registry integrity of 1.16.2 and 18.3.1 against the lock (C2 does it with `npm view`).
- Whether B1044 has pushed or will land before the gate finishes.

## Outside-the-fences disclosure
- Reads only. I wrote no file other than these two, plus scratch files in my session scratchpad: raw GET copies of locks and workflows, a 21 KB job log, a drafter `closure.py`, `kits.txt`, and two control files.
- Git in the project: only `ls-remote` with `--no-optional-locks`. `gh` was `-X GET` only, under the NexusAI GH_CONFIG_DIR: repo endpoints, `advisories/<id>`, and the job-log GET.
- No Jira call, no decision-queue tool, no scoreboard, no ledger, no WEDNESDAY or FRIDAY tree, and no other client's project.
- I read the lock's `owner` file inside `session-tools/locks-laptop-1017/` (lock state, not a seat tree). I did not open `worktrees/b1044-*`, `session-tools/b1044/` or `session-tools/b1045/`.
- My first port-scan command had a quoting slip: an unquoted multi-line variable passed to grep printed "File name too long" and a file list, but changed nothing. I re-ran the scan correctly through `xargs -0`, and the figures above come from that run.
- One hook refusal: a `====` separator in zsh. I re-ran it with `----`.
