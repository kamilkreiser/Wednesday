# Vision gate 17 (QuickQuote quality round, PR #6 @ d030674): drafter's report

Drafted 2026-10-13, 10:16 to 10:40 AEDT, by a read-only drafter for Tuesday.
Outputs:
- `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-13_vision-gate17-qq-quality-round.md`
- `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_vision_gate17.sh`

Nothing was written outside these three files, apart from scratch copies in the session scratchpad. No push, no merge, no `az`, no mail, and the launcher was not run except with `--check`.

## WRONG, or not verifiable as the commission or the READY states it

1. **The CodeQL proof cannot fail (brief WRONG (a)).** The READY says `alerts/N/instances?ref=refs/pull/6/merge` is empty for every alert. That same query also returns **0 for `refs/pull/3/head` and `refs/pull/3/merge`**. PR #3's head `1270b71` has tree `e4c688c`, the same tree as main `108bbb4`, which still carries all 14 open alerts. The query also returns 0 for **`refs/pull/999/merge`, a ref that does not exist**. Other reads point the same way:
   - The PR analyses are filed under `refs/pull/6/head`, not the merge ref.
   - The PR SARIF has 0 results for both PR #3 and PR #6. Main's SARIF has 9 + 5.
   - Both PRs show the same CodeQL check text: "No new alerts in code changed by this pull request".
   So **R4 cannot be measured before the merge.** Decision D2 asks Tuesday how to word the verdict. Vision's root BACKLOG.md:32 already records this unproven claim as "BUILT".
   Instrument: `gh api` GET calls with Vision's gh-config, plus `rev-parse ^{tree}`.
2. **R8 asks for Azure reads that R2 forbids (WRONG (b)).** The gate therefore relays the builder's ACR and webapp reads, and re-reads only the GitHub side. That is decision D3.
3. **GitHub access is undecided (D1).** The repo is private, so R4 and R8 need an authenticated token. Gate 16 pointed `GH_CONFIG_DIR` at an empty directory and said "no gh". Gate 16's NOT TESTED line "gh not authenticated" is out of date: Vision's gh-config is logged in with a token that can write. The brief's `GH-API-LEG` is set to TUESDAY-DECIDES, and the launcher refuses until Tuesday sets it. If it is set to READ-ONLY-VISION-TOKEN, the launcher puts a shim in front of `gh` that allows only GET calls.
4. **R3 needs the npm registry, which gate 16 banned (WRONG (c)).** The brief makes one exception: `curl` from the gate's own shell, nothing else.
5. **The R5 evidence covers only AUD and a wide sans font, but the price is set in `--mono` (WRONG (d)).** The first choice in `--mono` is Consolas, a Windows font, and the tests never use it. The brief adds a wide monospace font, CAD, the currency with the widest prices, and a 1 px width sweep.
6. **The change in which malformed emails are refused is wider than the READY lists (WRONG (f)).** The new pattern also refuses `a@b@c.io`, `a@b.io.` and any address with an empty domain label. Instrument: reading the two regexes. The gate measures this.
7. **A comment is now stale (WRONG (g)).** `stage3/lib/sendFailure.js:7` still says "junk@@x.example passes the route's shape check". That address now gets a 400.
8. **The base is not what gate 16 approved.** Gate 16 gave GO WITH FINDINGS at `9bd21c0`. PR #3 then merged `b102b56` + `1270b71` (strip.js now writes its outputs atomically) without a gate of their own, and v2.34 went live from `108bbb4`. Gate 17's base is `108bbb4`.
9. Smaller points:
   - `1e1d78d` says "No visible change", but the version string changes.
   - The READY's "BACKLOG.md marked BUILT" refers to Vision's root BACKLOG, not QuickQuote's. QuickQuote's BACKLOG has the same blob before and after.
   - `HANDOVER/02:316` still describes a `validate()` email check that was removed in v2.17. That predates this round.
   - The rate limiter lives in memory per container. It does not cover `/api/quote/:qnum` or `GET /api/feedback`.
   - The 10-minute window reset is not tested by any cell.
   - `d030674` changes behaviour without its own version bump, inside the same unreleased v2.35. That is a version-discipline question for Tuesday.

## What I verified, and how

- **Heads.** `ls-remote origin` at 10:16:14, plus a cross-check over HTTPS: `fix/qq-quality-round-2026-10-13` = `d030674694279be3159d67de4a10f220ea6b8335`, main = `108bbb443647e0f1c8ec2f426e9f33c15585eaa2`, `refs/pull/6/head` = d030674, `refs/pull/6/merge` = `f1a10662…`.
- **Commit chain and file sets.** Six commits, each with a single parent. There are no merges, the branch is 0 behind main, and `108bbb4`'s parents are `e408904` and `1270b71`. Per-commit and whole-diff file sets, numstat, the unchanged blobs, and the `test(` counts (server suite 101 → 106, so npm test 127 → 132). Instruments: `log`, `diff`, `diff-tree`, `rev-parse`.
- **Local main.** Local main is `8b29136`, which has the same tree as `108bbb4`. The worktree HEADs match the READY's HOLDS. Instrument: reading `.git/worktrees`.
- **PR #6.** Open, mergeable_state clean.
- **CI.** Runs 38320719480 and 38320741967 passed with all 5 jobs green. The last earlier green run was 31385330061 on 2026-08-10T11:51Z.
- **Alerts.** All 14 are open, and none has been dismissed or fixed.
- **GitHub deploy surface.** Hooks [], environments 0, deployments 0, no secrets. Workflows: tests, Dependabot, CodeQL. One ruleset, and no branch protection. Instrument for this and the three items above: `gh api` GET calls.
- **express-rate-limit 8.7.0.** Published 2026-08-29T00:49:51.601Z, 45 days before 2026-10-13. 8.7.1 was published 2026-10-06. The registry integrity and dependencies match the lockfile. debug 4.4.3 is clean. Instrument: `curl registry.npmjs.org`.
- **npm cache.** The three new tarballs are in the user's npm cache index. Instrument: grep of the index.
- **Builder's screenshots.** Of the 16 before/after pairs, 14 are identical and 2 differ. Instrument: sha1. These are the builder's claims, not evidence.
- **Current seats.** Tuesday 3983 (%0), Vision 39098 (%12), NexusAI 84103 (%11). Gate 16's negative-control seats have all exited. Load was 2.98. Instruments: `ps`, `tmux`, `lsof`.
- **Local environment.** Docker is down. `codeql` is not installed. Chrome is present.

## What I could not verify

- Whether CodeQL will mark #1-#14 as fixed after the merge, especially whether it treats `esc()` as a sanitiser and recognises `rateLimit()`. Pre-merge this can only be read from the code.
- Any Azure state. I did not run `az`.
- Every runtime claim, including timings, the 429 behaviour, byte identity and rendering. I did not run a product process or a browser.
- debug@4.4.2 as the compromised 2025 release is my recollection only. The registry document holds no dist for it.
- The en-US currency prefix widths (DKK/SGD/CA$) are my expectation, not measured.
- The shim limits `gh` only through PATH. The agent could still call the real gh binary directly, so the rest is held only by the brief's rules.

## Launcher changes compared with gate 16

Every gate-16 guard number is kept. Changes:
- **New guard 46** checks the `GH-API-LEG` setting.
- **Guard 23** now checks the exact `index.html` change by sha256 of the added and deleted lines, plus the numstat and a check for any new colour or token. Gate 16's literal-line style regex would have refused this round's legitimate CSS lines.
- **Guard 18** also re-reads `refs/pull/6/head`.
- **Guard 38** uses the new negative-control seats.
- **Guard 31** also checks R1-R10 as ruling lines, C-17, and gate 16's report and tools.
- **Guards 46, 41 and 32** are the coordinator's to-do checks. They are now reported together.
- **Exit 11** gives the gate an empty `GH_CONFIG_DIR` unless D1 allows reads, in which case it gets the GET-only shim.

Tests on scratch copies of the brief and launcher:
- Fully stamped brief, GH set to NOT-RUN, route present: rc 0 ("all guards pass").
- Wrong head: rc 40.
- One NOT TESTED line changed: rc 31.
- R7 removed: rc 31.
- GH setting "YES": rc 46.
- GH set to READ-ONLY-VISION-TOKEN: rc 0.
- The shim refused `pr view`, `-X`, `--method=`, `-f`, `-F…`, `graphql`, `--input` and `--raw-field=`, and passed a GET.
- `bash -n` printed SYNTAX-OK.

## `--check` output on the real files, verbatim (2026-10-13 10:3x AEDT)

```
REFUSING: the brief's GH-API-LEG line is still TUESDAY-DECIDES — Tuesday sets READ-ONLY-VISION-TOKEN or NOT-RUN (decision D1) before launch
REFUSING: no 'QA/Vision-gate17|tuesday-agent@agentmail.to|…' line in /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/inbox_routing.conf — answers to the gate would have no route. Add it (pattern: the QA/Vision-gate16 line) before launch.
REFUSING: the brief still carries @STAMP@ (Self-check line and note, or the RULED lines of D1-D4) — the coordinator re-reads end-to-end and stamps all of them before launch
guards pass (40 6 9 7 8 18 22 23 74 63 31 39 10 17 12 78 13 14 15 20 70 82 19 24 53 60 61 62 64 69 75 38 45 44); coordinator to-do pending (46 41 32 as listed above); exiting 46.
rc=46
```

Nothing was launched. To launch, Tuesday needs to:
1. Set `GH-API-LEG`.
2. Stamp the SELF-CHECK line, the note, and D1-D4.
3. Add the routing line `QA/Vision-gate17|tuesday-agent@agentmail.to|no`.
4. Run the launcher in a tmux pane.
