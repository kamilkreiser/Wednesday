# B647 DRAFTER REPORT (gate kit for NexusAI PR #112, round 1 of 2, tier 1, SEAT-G108)

Drafted 2026-10-25 08:53-08:59 AEDT (clock from `date`) by the read-only gate-kit drafter (Sonnet 5.5). Nothing was built, run, cloned, fetched, mutated or bound; nothing was written in any project. Two files under `tuesday/briefs/`. No `.pre-stamp` copy was made: `cp` the kit to `.pre-stamp` before stamping.

## Startable
**Yes, once Tuesday stamps.** Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-25_B647_SEAT-G108_nexusai-112-gate-tier1.md`, 92 lines. Four-underscore slot lines: 8 (seven slots at lines 68-74, last line 92); `/usr/bin/grep -c -E '_''_''_''_'` = 8 at 08:58:48, control scratch line reads 1. `@[A-Z_]+@` count 0. Non-ASCII lines 0. The repo is `datasecau/Reporting_Dashboard_Au`.

## Facts re-measured (MEASURED-BY-DRAFTER, `date` in brackets)
- `ls-remote` [08:53:08]: main `6e076b29`; branch = `refs/pull/112/head` = `412c784b`; `refs/pull/112/merge` = `37fe97de` (parents `6e076b29`, `412c784b`; tree `dadbc3e7`); `refs/pull/67/head` = `94b288cc`. `pulls/112`: open, not draft, mergeable true, state blocked, 3 commits, +190 -14, 3 files (164/0, 23/11, 3/3). Open PRs #112 and #67. `cat-file -t 412c784b` fails in the shared (stale) repo.
- Check-runs [08:53:18]: 8; `Analyze (actions)` and `(python)` success (analyses on the PR ref 0 results each), `scan`, `audit-production-deps` x2 success; `build` and `Analyze (javascript-typescript)` in progress; `CodeQL` neutral. Open alerts on the PR ref 0 so far.
- Alerts [08:53:22]: #83 (`:173`), #84 (`:179`), #43 (`:209`), #136 (`:243`) all open on main, high, rule severity warning. Ruleset 24139430 `rules/branches/main` [08:53:18]: code_scanning alerts_threshold errors, security_alerts_threshold high_or_higher, required checks empty.
- Head `validators.js` read raw [08:53]: 315 lines, git blob `33067668...` = the builder's claim; lines `:168`, `:169-177`, `:188`, `:194-198`, `:226`, `:255` quoted in the kit. Finding of reading: `validateInput` tests the ORIGINAL `value`, not the sanitised string (cross-stage assembly, the kit's Check 3b i-iii). Body limits in the stale `server.js`: json 5mb (`:20919`), urlencoded 50mb (`:1171`).
- Main's Build 40130530831 [08:54:13]: `in_progress` (Tuesday's re-run). Deploy demo last 5 on main all `skipped`. #67 open, head `94b288cc`, dirty.
- Ports [08:53-08:54]: `lsof` 9980-9989 rc 1; word-boundary scan `998[0-9]` over `*SEAT*` briefs 24-25 Oct: 0 files; control `985[0-9]` = 7 lines in the B635 kit. Panes: tuesday, Composer J12/J13/G98, HPSM-POC-G106, MPS-G105, fleet-monitor (no NexusAI pane). `worktrees/b647*`, `session-tools/b647`, `refs/heads/b647*` absent. Lock hash equal; `queue-jest/` empty; load1 20.18 [08:53:22].
- CLARIFICATIONS lines read: C-190 `:2062`, `:2067`, C-68 `:665`, C-209 `:2270` and amendment `:2276-2280`, C-115 `:1182`.

## Decisions I made (D)
- **D1 Tier 1 Opus, row G1, `BRIEF_SEAT_LEVEL=opus`, pane `Datasec/NexusAI-G108`, suffix G108, findings `B647-n`, ports 9980-9989.** Accept.
- **D2 A second tree `worktrees/b647-mut`** (`cp -R` of the gate's own clone after `npm ci`) for mutants: the cells `require` `../backend/validators`, so mutants need a tree; only `backend/validators.js` changes there, restored by `cp` and proven by sha256. Needs Q-1.
- **D3 Mutant matrix M1-M23** with predictions written before the run; survivors classified EQUIVALENT / TEST GAP / DEFECT; M7 (drop `g`) predicted an equivalent survivor, M9 the in-run control, M12 (strip before removals) the likely test gap.
- **D4 Bypass hunt is classified A/B/C** (executable in context / not reachable / out of the ruled scope), with the cross-stage assembly cases run end to end through the middleware. Escape-on-output and allow-list requests are Notes for the product owner, never defects (ruling recorded in the test header).
- **D5 ReDoS timed**, including the fixed-point worst case (nested `java`xk + `script:`xk, quadratic by reading), sized to the 5 MB JSON limit; grading by time at the limit.
- **D6 The gate does not run the whole verify;** it reads the PR `Build` verify line (5044/306) and checks the counts delta by program. Fallback stated if `Build` cannot finish.
- **D7 #136 appearing open on the PR ref is a Blocker candidate** per the C-209 amendment (`:2276-2280`); the verdict line carries the reasoning and Tuesday decides the landing.
- **D8 The 13 non-ASCII bytes in the byte-equal test file are a Note** unless a repo rule against them is found (then Major).
- **D9 Hard stop:** target verdict 2 h, HARD STOP 3.5 h after Step-0 `date`, never later than 13:00 AEDT. No fixed rule beat this; Check 3 is the long one (about 25 single-file jest runs under the lock).
- **D10 Known fact B4** carried as a Note: rerun alone 3x if red, never grade the PR on it.

## Questions for Tuesday (Q)
- **Q-1:** is the second tree `worktrees/b647-mut` (a `cp -R` of the gate's own clone, own `node_modules`) approved for mutants? Without it Check 3a cannot run; the alternative is mutating the single clone's file with sha256 restore, which I judged riskier.
- **Q-2:** confirm the 13 em dashes in the byte-equal test file stay a Note (the builder kept byte-equality over a "0 non-ASCII added" line in its own brief).
- **Q-3:** if #136 appears open on the PR ref, do you want NO GO (my reading of the amendment) or GO WITH FINDINGS plus your own decision? The kit leaves the call to the gate's reasoning in the verdict line.
- **Q-4:** launch timing: load1 was 20.18 at 08:53; one waiter, launch_when_cool, as the sibling kits say. No port conflict with the live seats.

## Not done / UNMEASURED
Every clone, fetch, npm, jest, mutant, probe and timing; CodeQL on the javascript-typescript leg (in progress); `Build` result; whether #136 surfaces on the PR ref; whether any bypass candidate is executable (the kit tells the gate to read the sinks); the realistic route set that mounts `validateInput` (stale `server.js` only); whether a repo rule forbids non-ASCII in tests; the PR body beyond its first 20 lines.

## Fences kept
`git --no-optional-locks` read verbs only (`ls-remote`, `cat-file`, `hash-object` on a scratch copy); `gh api -X GET` only, under the project `GH_CONFIG_DIR`; no fetch, clone, worktree, checkout or merge-tree; no HTTP to any hosted host; no Jira; no `decision_queue.sh`; did not read `briefs_staged/`; no Artifact, Docs, mail, chat or publish tool; no person's name or decision-card id in either file. Scratch copy of the head `validators.js` in the session scratchpad only.
