STARTABLE: YES

# B837 drafter report: tier-2 QA gate kit for NexusAI PR #131 (seat Datasec/NexusAI-G181)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B837_SEAT-G181_nexusai-131-risk-level-gate-tier2.md`. Drafted 17:42-17:5x AEDT 2026-10-27 by the Sonnet drafter; read-only apart from the two files named; nothing cloned, fetched, installed or run in the project. Stamp slots: 7 slot lines plus the last line = 8 lines with the four-underscore pattern (control: a scratch line holding four underscores reads 1); at-sign token count 0; non-ASCII 0 (control: a planted two-byte character reads 1).

## BLUF
- STARTABLE YES, with one wait: at 17:42 the head's CI is INCOMPLETE (build and all three Analyze runs in_progress; only the actions analysis row exists; the CodeQL summary run reads neutral). The gate starts on the local work and reads CodeQL LAST after a bounded wait; the kit says a zero alert count is a suspect until every Analyze run is complete and all three language rows exist.
- The kit gates the three-path, +355 -3 PR: one product statement in `backend/server.js`, one new 21-cell test file, the counts file. It adds what you asked for: the uncapped file list, backend numstat 3/0, the 400 and 200 words counted before and after, the gate's own red run at main (new file copied into a main tree, blob-proved) and green at head twice, 12 own mutants, determinism and ports, reader/scheduler reading, red-flag setting untouched, counts diff and the plain verify, CodeQL last.
- The kit's hand-up line is live because this tier-2 PR holds a product byte: a measurement showing the statement lets through a level the check refuses, or changes who may call the route, is a STOP to tier 1 (reading says neither is possible: the statement runs after the check, on the same `toLowerCase()`).

## Facts re-measured (instrument, clock, control)
- Pins, `git ls-remote` at 17:42: main `c8e1a9a1...`; branch and `refs/pull/131/head` `a055bd637b71...`; merge ref `3ec854e4...`; `refs/heads/b837*` absent (control: `b835*` and `b823*` print branches). Main equals the relayed value.
- PR #131 (`gh api -X GET pulls/131`): open, not draft, mergeable true, mergeable_state blocked, 1 commit, 3 files, +355 -3, base `c8e1a9a1`; 0 comments, 0 reviews. `pulls/131/files` (uncapped, `--paginate`): test 349/0, `backend/server.js` 3/0, counts 3/3. `compare c8e1a9a1...a055bd63`: ahead 1, behind 0, three files (control: the `97fac53a...c8e1a9a1` pair lists the counts file).
- Product diff (raw files at main and head saved to the scratchpad, `diff`): the ONLY difference in `server.js` is three inserted lines at head 21237-21239 (comment, statement, blank) between the existing level check and `updateRiskCondition(...)`. The 400 sentence and the 200 message each occur once in the file at main and once at head (`grep -c -F`; the control is in the kit, a sed-changed copy).
- Counts file diff (`diff` of main and head): exactly `_updated`, `tests` 5178 to 5199, `suites` 308 to 309; `_why` untouched. `scripts/verify-suite.sh` blob `eb9731f5...` at main and head (`contents?ref=`). CI predicate read in the main copies: `verify-suite.sh` header (measured below or above expected both FAIL) and `build.yml:83-84` (`npm run verify -- --maxWorkers=2`).
- Readers read at main: `getRiskConditionsByLevel` strict `===` (`jsonStorage.js:3743`), scheduler `riskAlertScheduler.js:114`, by-level route `server.js:21069`, report generator `:10426`; red-flag setting `server.js:20638` and `:20659-20665`, none in the diff.
- New test file (head copy read): 21 cells (P1 1, E1 3, E2 4, E3 3, E4 6, E5 1, E6 1, C1 2), real server as a jest child, all PUTs in one `beforeAll`. `sleep` at lines 37, 137, 151 are readiness and teardown, outside assertions (the kit makes the seat classify, not pattern-flag).
- CI at 17:42 (`commits/<head>/check-runs`): CodeQL completed/neutral, scan success, audit-production-deps success, build in_progress, Analyze python / javascript-typescript / actions in_progress. Analyses on the PR ref: one row (actions, 0 results). Open alerts on `refs/pull/131/head`: 0, NOT evidence yet. Controls: the same query on `refs/pull/130/head` returned 1 open row; `alerts/9999` 404. The Actions runs listing is refused for this account (scope), so the kit reads checks only through `check-runs`.
- Ports 9670-9679: `lsof -nP -iTCP:9670-9679 -sTCP:LISTEN` rc 1 at 17:42. Word-boundary scan over the 132 non-`.pre-` SEAT kits of 10-26 and 10-27: 9670 and 9679 hit B749 and B752 only (closed seats); 9671-9678 hit 0; control `9600` hits B746 B747 B750 B778 B832 B833 B834. Live panes (`tmux list-panes -a`, 17:42): coordinator, `Datasec/HPSM-POC-D39`, `Datasec/NexusAI-M24` (parked builder), `Datasec/NexusAI-M23`, fleet-monitor. No pane named G181 (not tested by launching).
- Model: `model-routing.md:109` row G2, `:111` G-cap; `models_latest.json:23` `claude-sonnet-5-5`. Launch line carries `BRIEF_SEAT_LEVEL=sonnet` inside the inner quotes. Lock tool sha256 `cf01bafb...` and fence `55eaafcb...` (shasum 17:43); `queue-jest/` empty at 17:43. `worktrees/b837-*` and `session-tools/b837` absent (`ls -d` no such file; control `session-tools/b835` listed).
- Round count: STATUS-file grep for the head, `#131`, `b835`, `pull/131` hit B835 (the builder) and two 10-20 STATUS files (B302, B334) whose hits are old CodeQL alert numbers #131/#132 (read the hit lines); control `b816` hit 4 files. No earlier gate verdict on #131: "NO GO 0 of 2 before, round 1 of 2" holds.
- PR #130's branch moved to `9fa41981` at 17:42 (the live builder is pushing); no overlap with the three paths.

## D-decisions made in the kit
- D-1 Tier-2 with a live hand-up line (a product byte exists; defined what counts as security-shaped).
- D-2 Own mutants G-M1..G-M12 instead of copying the builder's MR1-MR8: adds a Turkish-locale mutant (rows with a capital I), a statement-after-store mutant, a single-spelling pair (High-only, HIGH-only), a typeof-guard mutant, and an equivalent mutant.
- D-3 G-M11 (remove the typeof guard) is predicted to SURVIVE: no cell sends a falsy non-string (the builder declared falsy levels out of scope). Graded a Note, with the neighbour suites run once against it.
- D-4 G-M12 (remove the `!== ''` clause) is an equivalent mutant (`''.toLowerCase()` is `''`); reported EQUIVALENT, never as a survivor.
- D-5 Red at main is done in a base tree at main with the head's test file written in (blob-proved equal), not by trusting the builder's logs; three npm installs budgeted (base, gate, mut).
- D-6 CodeQL is C11 and read last; the neutral CodeQL summary run and a single actions row are named as not the set.
- D-7 `session-tools/b835` and the builder clone are not opened; only the STATUS file and commission are read as claims.
- D-8 The kit's G-3 makes "a way to store a level the check refuses" a Blocker and hand-up; "a way to store a mixed-case level" a Major.

## Q-questions for Tuesday (each with a default)
- Q-1 Does the tier stay 2 with a product statement in the diff? Default: yes (your ruling), hand-up line live.
- Q-2 Launch now or after CI completes? Default: launch now; the gate's local work (clone, installs, red/green, mutants, verify) takes longer than the CodeQL wait, and C11 is read last.
- Q-3 Port block 9670-9679? Default: accept (0 listeners; closed-seat kit hits B749 B752 only).
- Q-4 Hard stop: drafter suggests target verdict 150 minutes and hard stop 240 minutes after the gate's own Step-0 date (3 installs, 12 mutants, neighbours twice, verify about 25-30 minutes, lock queue behind the live PR #130 builder). Default: those values.
- Q-5 If PR #130 lands before the gate reaches REFUSE 2, main moves by tests only; the kit says re-pin and continue. Default: that.

## UNMEASURED
- CodeQL result on the head (analyses incomplete at 17:42); `build` result; Linux runner and node 24.
- Whether the builder's 21 cells are red/green as claimed (not run; the gate does it).
- The test file was read at its harness, cells and `beforeAll` (lines 20-34, 194-349) and by pattern for timers (all lines); lines 36-193 (harness body) not read whole by the drafter.
- Whether the child server inherits the fence's `NODE_OPTIONS` (the kit makes the seat read the `spawn` env).
- Other tests that PUT a mixed-case level (the neighbour census is the gate's `git grep`, not run here).
- The `.pre-stamp` copy count and the stamp are Tuesday's.

## Outside-the-fences disclosure
- Wrote only the two named files. Scratch copies of raw files fetched with `gh api -X GET` (counts file, `server.js`, `jsonStorage.js`, scheduler, `verify-suite.sh`, `build.yml`, head test file) were saved in the session scratchpad `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/59f24562-ea21-4839-8efe-6c4a3767c6d2/scratchpad/`.
- Read, not written: the builder STATUS and commission, the B832 template, DRAFTER_RULES, model-routing, models_latest, CLARIFICATIONS (grep lines only), STATUS-file grep (hit lines of B302 and B334 only), the briefs directory listing and kit scans, `queue-jest/` listing, `shasum` of two plumbing files, `tmux list-panes -a`.
- Network: GitHub `gh api -X GET` under the NexusAI `GH_CONFIG_DIR` and `git ls-remote`. One `gh api` call (workflow runs listing) was refused for scope; one deliberate 404 control (`alerts/9999`). No Jira call, no decision-queue call, no mail, no Artifact/Docs tool.
- Two shell slips: one command used an unquoted word starting with `=` and was refused by the hook (nothing ran); one `grep -P` was unsupported on this system (no effect). A non-ASCII scan was re-run with `-E` and read 0 with a control of 1.
- Case-sensitive phrase greps drew the hook advisory three times (counts of fixed strings with `grep -c -F` and a two-file positive result); the 400 and 200 counts are 1 and 1 in both files, which is the positive control.
- No person's name or decision-card id in the kit text (scanned for the owner and the two client names; the phrase "decision-card id" appears only as a rule). RD-893, RD-878, RD-836, RD-892, RD-876 are Jira keys, as in the template.
