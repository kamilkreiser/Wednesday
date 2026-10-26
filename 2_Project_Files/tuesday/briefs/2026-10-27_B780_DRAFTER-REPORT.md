STARTABLE: YES (launch when cool: load1 3.07 at 04:10; the jest lock queue was empty at 04:06; ports 8710-8719 free; one live NexusAI gate, G161, shares the lock and the gate queues FIFO behind it)

# B780 drafter report (kit: `2026-10-27_B780_SEAT-G163_nexusai-878-risk-level-gate-tier1.md`, 85 lines, Opus, tier 1, round 1 of 2)

## BLUF
One tier-1 gate kit for `b777/nexusai-878-risk-level-type` @ `58234bd8e8323da9d953066e8a6b3474bff0c0b9` (RD-878). Delta re-measured at source: ONE product line changed (`backend/server.js:21233`, the `typeof updates.risk_level !== 'string' ||` clause), plus one new 211-line test file and the counts file 5162/306 -> 5170/307. Main is now `209446c0` (HISTORY.md only, 2 ahead of the builder's base), so the kit judges the merge tree against current main. The kit's heart is Check 3 (the handler under every JSON and urlencoded shape, the other fields, middleware order, and the CONFIGURED deployment, because the builder's 8 cells only drive the open first-run window), Check 4 (falsy values and their stored state followed to the readers) and Check 5 (nine guard mutants with written predictions, including a wrong-field mutant the shipped cells probably cannot see). Stamp slots left as four underscores (8 lines with the pattern, last line `READ-WHOLE-BY-TUESDAY: ____`).

## Facts re-measured (instrument; control)
- Refs 04:06: main `209446c082c2be1f78ee4511296c1d265186878a`, branch `58234bd8...` (`git ls-remote`; control: `b770*` prints its one line). `b780*`/`b779*` none.
- `compare f4efe10f...58234bd8`: ahead 1 behind 0, 3 files, +211/-0, +1/-1, +3/-3, parent `f4efe10f`, `verification.reason` `unsigned` (`gh api -X GET`; control: the 6-file pair). `compare 209446c0...58234bd8`: ahead 1 behind 2. `compare f4efe10f...209446c0`: ahead 2, `HISTORY.md` only.
- Product diff: `diff` of the two raw `server.js` reads (22351 lines each; 1107905 and 1107949 bytes): exactly line 21233 differs; the handler region `:21218-21252` read whole; `requireRiskConditionAdmin, refuseSqlText` order is on the unchanged `:21220` (control: the saved file against itself prints nothing).
- Counts file raw at both shas: 5162/306 -> 5170/307; depth-1 `__tests__/*.test.js` census by `git/trees?recursive=1`: 306 -> 307 (control: the two reads differ by the one new file). The tree `truncated` flag was NOT read (UNMEASURED; the kit asks the gate to read it).
- Test file read whole (211 lines): 1 precondition + 4 `test.each` rows + 3 controls; all PUTs run in one `beforeAll` in a fixed order; only the OPEN first-run window is driven (no admin, no viewer).
- CI at the head: `actions/runs?head_sha=` = one `npm-audit` success; `code-scanning/analyses` for the branch ref = 0 (control: main returns 2); no open PRs (control: closed list #121 #120 #119). Ruleset read: code_scanning CodeQL `errors` + `high_or_higher`, required_status_checks empty.
- Open main alerts in `backend/server.js`: 79 (paged fully, `state=open`), 0 in lines 21150-21320, 2 in 20000-22351 (control that the filter fires). None in rd774/rd777 files, open or fixed (control: alert 95 in the fixed list).
- Deploy workflow at `209446c0`: push to main, `paths-ignore` `**.md`, `docs/**`, `tests/**` (lines 29-32), jobs gated on `vars.CI_DEPLOY_ENABLED` (lines 53, 91); last three push runs `skipped`. A merge of `backend/**` starts a run, expected `skipped`.
- Landing rule lines found by text: C-190 `:2062`, merge path `:2067`, never-dismiss `:2068`, wait `:2073`, C-68 `:665`, C-209 `:2270`, C-218 `:2362` (CLARIFICATIONS.md is 2417 lines now).
- Routing: `sed -n 108p` of model-routing.md prints the G1 row (G2 `:109`, G-cap `:111`); `levels.opus.model_id` = `claude-opus-5-5` (line 17; `checked_at_local` 2026-10-27 03:06:40).
- Ports 8710-8719: `lsof` empty at 04:06 and 04:10; control: a python3 -I listener on 8715 listed (2 lines with header) then freed (0). Word-boundary scan over 74 non-`.pre-` SEAT kits of 10-26/10-27: 1 hit, the finished builder B777 (pane closed). Live panes: `tuesday`, `Datasec/NexusAI-G161`, `fleet-monitor`. `NexusAI-G163` named by no kit. Lock tool sha256 `cf01bafb...971f` (equal to B750/B776/B777), `queue-jest/` empty.
- Sibling census (server.js at head, grep, frame: `.toLowerCase()` in lines 20900-21420 and routes whose path holds `risk-condition`): 8 routes plus the settings sync route; `.toLowerCase()` at `:20992` (receiver from Joi: `riskLevel: Joi.string().valid('low','medium','high').required()` read at `validators.js:49-`), `:21061/21067/21069` (route param), `:21233`. Prediction written in the kit: no other unvalidated body `.toLowerCase()`. `jsonStorage.updateRiskCondition` (`:3721`) spreads whatever it gets, so the other PUT fields are type-unchecked (a prediction for the gate to confirm).

## D-decisions (mine, for Tuesday to accept or strike)
- D1 Class name: "a request-validation guard whose evidence pins less than it claims". New class for this branch; B750's class on another branch (verdict GO WITH FINDINGS round 1, since landed) is cited and does not carry over.
- D2 The in-clone fetch destination is `refs/remotes/origin/g163-head`, not `origin/b777`: B776's STATUS records a ref-name clash and five wasted retries on that shape.
- D3 The plain verify runs at the BRANCH HEAD (the gated commit, C-68), not on a merge; the merge prediction is by clone-local `merge-tree` plus path intersection.
- D4 Check 3(d): probe the configured, admin-gated deployment (anonymous, viewer, admin), because the builder's cells prove the 400 only in the open window. NOT TESTED past 30 minutes of harness work.
- D5 Added shapes the builder did not run: urlencoded arrays/objects (`risk_level[]=high` reaches the handler as an array), duplicate JSON key, a valid `condition_text` sent with the bad `risk_level`, a 1 MB string, unicode lookalikes, `[]`/`{}`/nested.
- D6 Q2 (type test on the wrong field) is predicted to leave the four non-string rows GREEN (400 for the wrong reason) and kill only the valid-level control, because every shipped cell sends `risk_level` alone; the gate adds its own cell to show it. Graded Minor unless the gate argues otherwise.
- D7 Falsy values: gate drives them, follows a stored falsy level to GET list, GET :level, execute and stats, reads RD-878 words, grades as Note/Minor-for-follow-up, never as a request to change the guard (the commission's D-FALSY stands).
- D8 Jira read helper: the project's own `scripts/jira-query.sh` (existence, positive/negative control inside) and `jira issue view` (JIRA.md says `view` works), not the HPSM-POC helper the builder commission used.
- D9 Verify ticket cap 40 minutes (builder 1287-1445 s), other jest tickets 20; severity table puts an admin-gate bypass in "STOP, security-shaped".

## Q-questions for Tuesday (each with a default)
- Q-1 Tier: G1 Opus (default, as the builder commission said) or G2 Sonnet? Default G1 (route behind the admin gate, merge starts the deploy workflow).
- Q-2 Clone-local `git merge-tree --write-tree` (object write in the gate's own clone only, no ref)? Default YES (B750 precedent).
- Q-3 The configured-deployment probe (Check 3d) and one scratch probe server on a port of 8710-8719? Default YES, NOT TESTED if the harness needs more than 30 minutes.
- Q-4 Read-only Jira GETs through the project's helper? Default YES, NOT TESTED after five minutes.
- Q-5 Falsy values: Note/Minor-for-follow-up, not a NO GO reason? Default YES.
- Q-6 G161 holds or queues the jest lock (its STATUS last written 02:57, queue empty at 04:06): launch now and queue FIFO? Default YES; the kit forbids breaking, `--after` or `--replace` on its ticket.
- Q-7 Hard stop: 4 hours after Step 0 and not later than 09:30 AEDT 27 Oct? Default as written; Tuesday may set another.
- Q-8 Ports 8710-8719 kept (only the finished B777 names them)? Default YES.
- Q-9 Should the gate also run the plain verify at the merge tree (main + the three paths)? Default NO (C-68 head; the delta is HISTORY.md-only on main).

## UNMEASURED by me
No clone, fetch, npm, jest, node probe, server boot, workflow, CodeQL or Jira call was made. The Jira words are RELAYED from the builder commission; `scripts/jira-query.sh` was read, not run (needs the project token in the launcher's environment). All mutant predictions (Q1-Q9), the urlencoded array prediction, the configured-deployment predictions and the sibling-field storage prediction are reasoning from the code, not runs. Whether G161 is making progress. The `truncated` flag of the tree reads. The Linux runner and node 24. CodeQL on the head.

## Outside-the-fences disclosure
- Bound one loopback listener on 127.0.0.1:8715 for 6 seconds (python3 -I) as the lsof positive control, then freed it (verified 0 listeners).
- Wrote scratch files only in the session scratchpad (`server_base.js`, `server_head.js`, `rd878.js`, `deploy.yml`, `alerts.tsv`) from `gh api -X GET` raw reads; no file written in any project tree except my two files. Rewrote non-ASCII characters in the kit to `\uXXXX` text escapes after a non-ASCII check found 7.
- Read, not invoked: headers/bodies of `scripts/jira-query.sh` (lines 1-140, past the header), `scripts/jira-adf.py` header, `JIRA.md` by grep, `nexusai-lock.sh` header (lines 1-40). Read the live gate G161's STATUS first 900 bytes and last line (the file it uses as its channel) for the round-count text and the fetch slip; read the finished B750 STATUS first/last lines. Listed names (no content) in the NexusAI `session-tools/`, `worktrees/` and project root.
- Two hooks fired advisories on case-sensitive multi-word greps (results still read; the kit's own greps carry `-i` and controls) and one refused an `echo` of a `=` word (re-run with `---`); one `cut` hit a multibyte string (no effect). No `decision_queue.sh`, no Artifact/Docs/mail/chat tool, no git write, no gh write, no HTTP to hosted hosts, no az/ssh/docker, no `cd`.
