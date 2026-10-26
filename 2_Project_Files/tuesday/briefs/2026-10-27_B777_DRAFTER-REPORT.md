STARTABLE: YES

# B777 drafter report (Sonnet drafter, 2026-10-27 02:3x-02:5x AEDT)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B777_SEAT-M17_nexusai-878-risk-level-type-check.md` (154 lines). Shape copied from B746 and its STATUS.

## BLUF
RD-878 is completable now, in one commit, on one new branch, and adds NO new word: the existing 400 sentence is on the line after the throwing line and a `typeof` test in the same `if` returns it unchanged. The kit is stamp-ready (9 slot lines read, 0 at-tokens, no person name, no card id). One thing you must rule on before launch: the falsy values (0, false, null, "") skip the check today and reach the store; the kit leaves them alone and asks the seat to probe and report (Q-1).

## Facts re-measured (instrument; control)
- RD-878 at source: Jira GET via the HPSM-POC helper loaded by importlib, whole (summary, status, description, links, comments). To Do, Bug, Low, 0 comments, links Relates RD-774 and RD-836. JQL `project = RD AND ( key in (RD-878, RD-870) )` = 2 rows; control `key in (RD-zzz)` = 0.
- Main = `f4efe10f184ef99e8e8e8d1a93f29e52e2d4bb5b` (ls-remote and `commits/main` agree). It moved from the sweep's `e553d340` by #118; `compare e553d340...f4efe10f` = ahead 2, behind 0, one file (`__tests__/sustainability-logger-live.test.js`); control compare `19b7106b...6e076b29` = 6 files. `server.js` is still 22351 lines, 1107905 bytes, blob `4d12ac0d9be1`, 0 CR bytes, so the sweep's line numbers hold: PUT handler `:21220`, the throwing line `:21233`, the 400 sentence `:21234`, store write `:21237`, catch 500 `:21249`, allow-list `:20940`. The raw file was saved and read with `grep -n -F 'updates.risk_level'` = exactly line 21233 (once). The sentence "Invalid risk level" occurs twice: `:21062` (different sentence, GET route) and `:21234`.
- NO NEW WORD claim: verified at source. Reusing `:21234` adds zero characters to any customer-facing text. The kit also carries a program check (Step 5.4) that the added and removed string-literal sets differ only by the type name `'string'`, and a STOP-shaped rule if any word would appear.
- Falsy values: read only. `jsonStorage.js:3721` spreads `updates` into the stored record, so 0/false/null/"" would be stored (the guard `updates.risk_level &&` skips them). UNMEASURED by running.
- UI caller: `static/js/settings.js:1351` sends `risk_level` from a form control value (always a string); the new 400 is not reachable from the shipped UI.
- Counts: `scripts/verify-expected-counts.json` blob `b0fa5295d89c`, tests 5162, suites 306 (the post-#120 pair). Depth-1 census of main's recursive tree = 306 (tree `truncated: false`, 1017 entries). A new `__tests__/rd878-...test.js` is therefore +1 suite: expected pair after = 5162+N tests, 307 suites (N about 6-9, UNMEASURED). This differs from B746 ("a new file is a STOP"); the kit says one new file is mandated and any other movement is a STOP. `rd878-risk-condition-put-risk-level-type.test.js` answers 404 at main; no tree path contains `rd878`.
- CI predicate: `build.yml:83-84` `npm run verify -- --maxWorkers=2`, `node-version: '24'` at `:29`; `verify-suite.sh` header: measured below or above expected FAILS. Written into the kit.
- Landing rule: `CLARIFICATIONS.md` (project folder, 2408 lines, not in the repo: `contents/CLARIFICATIONS.md` is 404) `:2067` merge path, `:2068` never dismiss, `:2073` wait on every `Analyze (<language>)`. Quoted in the kit; the records seat is editing that file, so the kit says re-find by text.
- Model: row C2 at `model-routing.md:92` (Sonnet 1st, ruled 2026-10-10 09:06:47); C3 at `:93`; gate rows G1 `:108`, G2 `:109`. Id `claude-sonnet-5-5` from `models_latest.json` (`levels.sonnet.model_id`); launch line carries `BRIEF_SEAT_LEVEL=sonnet`.
- Panes (tmux list-panes at 02:34): HPSM-POC-G159, MPS-G158, MPS-G160, NexusAI-R51, fleet-monitor, tuesday. No `NexusAI-M17`, and no `NexusAI-G161` yet. Name scan of 71 non-`.pre-` SEAT kits dated 10-26/10-27 (python3 -I, `NexusAI-M[0-9]+\b`): highest real name M16 (M99 appears as a planted control and fires); M17 named by no kit.
- Ports 8710-8719: `lsof -nP -iTCP:8710-8719 -sTCP:LISTEN` empty (rc 1); positive control (python listener on 8715) listed, then freed (rc 1). Word-boundary scan over the 71 kits: 0 hits (control `x 8715 y` matches, `x a8715 y` does not).
- Branches and PRs: open PRs = none. Remote heads b595, b703, b713, b746, records/b362, b605, b656, b681, b727 are ahead 0; `b770/nexusai-873-codeql-tests` @ `4558a53a` is ahead 1, behind 2, files = exactly the two `__tests__` files you named, both existing at main (so it adds no suite and does not move the counts file; its STATUS line 25 agrees). `refs/heads/b777*` empty (control b770* prints a line). Intersection with the kit's three paths: EMPTY.
- Lock tool sha256 `cf01bafbc51f555ca0f14d1711f01885bcec5bc6293b177fe24702226bb4971f` (same as B746). `queue-jest/` empty. load1 5.36 at 02:34.
- Kit self-checks (grep): slot lines with four underscores = 9 (8 slots + last line), `@[A-Z_]+@` = 0, no person name and no card id.

## D-decisions (mine, for you to overrule)
- D1 Change shape: add `typeof updates.risk_level !== 'string' ||` inside the SAME `if`, keeping the `updates.risk_level &&` guard first. Smallest edit; falsy behaviour stays byte-for-byte as on main.
- D2 Cells: `test.each` over 7, ["high"], {}, true (ticket's three plus `true`), each expecting 400, the full existing sentence, and the store file unchanged by one read each side; three controls (valid 'medium' 200 and stored; 'urgent' 400 same sentence; no risk_level 200). Red-first: four 500s printed against unmodified main. Three mutants (undo, too-wide typeof, typeof after toLowerCase).
- D3 Harness: one server, one planted condition. Open first-run window first, configured admin as fallback, decided by measurement (an anonymous PUT is UNMEASURED). No helper file, no edit of rd774.
- D4 Gate default: tier 1 (Opus), because it is a backend handler behind the admin gate and its merge starts the deploy workflow. Sonnet builder because the edit is spelled out (C2).
- D5 Time: target READY 3 h, hard stop 5 h after Step 0 (two verifies of 25-30 min plus red/green/mutant runs). I set no wall-clock ceiling; that is yours at the stamp.

## Questions for Tuesday (each with a default)
- Q-1 Falsy values (0, false, null, ""): they reach the store today (a second, different defect). Default: this commit does not change them and pins nothing; the seat probes once each and reports; you file a follow-up if you agree. Alternative (not drafted): widen the check to `'risk_level' in updates` so null/0/false/"" also answer 400, which changes behaviour for `""` and `null` and is arguably beyond the ticket.
- Q-2 Gate tier. Default tier 1 (Opus). Tier 2 (G2) is defensible if you read the edit as a validation-only follow-up.
- Q-3 Launch timing: the CodeQL-test gate (G161) will take the jest lock for a verify; this seat will queue behind it. Default: launch now; the lock is FIFO and the kit says wait, never refuse.
- Q-4 The kit tells the seat the counts pair ends at suites 307. If any other branch adds a suite before this one lands, the counts file will conflict: default is that whichever lands second regenerates once (a new head, a new gate). Nothing else open adds a suite today.

## UNMEASURED
Whether the 500 reproduces live; the falsy-values effect; whether an anonymous PUT is accepted in the open window; N; other test files that drive the PUT over HTTP (code search is an index, not a census; "Invalid risk level" search returned 0 despite the sentence being in server.js); API callers outside the UI; wall times; CodeQL on the new head; whether CI is running or paused at push; whether `Deploy demo` is still skipped by the variable (carried from B746, not re-read).

## Outside-the-fences disclosure
- Wrote only the two files above. No Artifact/Docs/mail tool used. No `cd`; absolute paths. No `decision_queue.sh`, no briefs_staged, no scoreboard, no `_ledger.md`, no WEDNESDAY/FRIDAY tree read.
- I wrote scratch files into the session scratchpad directory shared with Tuesday's own session (it already held files). My `server.js`, `jsonStorage.js`, `simpleDb.js` downloads (main f4efe10f) there overwrote same-named files if they existed (the listing showed `server.js` 1107905 bytes at 02:33, mine; I did not check whether a prior copy existed), plus a `b777/` subfolder and `j.py`. Nothing else in the repo or project folders was written.
- I read the finished B746 STATUS and B770's STATUS (lines 1-3, 25, 86-99, 137) from the NexusAI Briefs folder and listed `Briefs/`, `worktrees/` and `session-tools/` names (listing only, no tree opened). All other reads were git/gh GETs: one `search/code` x6 (throttle respected), compares, contents, one recursive tree.
- One positive-control listener was bound on 127.0.0.1:8715 for 6 seconds and released (lsof confirmed free). Jira: GETs and two search POSTs only. No hosted host contacted.
