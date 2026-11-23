GATE B1975: GO WITH FINDINGS @ d37db35 on main 3c3be15

Independent review, tier G2 (one Sonnet reader), round 1 of 2, no rendered leg. Lane NX-SR, kit B1966, seat N165.
Branch `b1966/nexusai-signal-read-race`, head `d37db35c9bb99cf39136448a05f1a39ef214313e` (one commit, parent = main
`3c3be156e8ea36ad297fdadd3055c6e00252ba38`, tree `d25569e8...` equal to GitHub's). Main unmoved at 10:32 and 10:34 AEDT
2026-11-23. Clocks from `date`. Jest lock: ONE acquisition (`g1975-gate`, 10:33:59 to 10:39:42, acquired after 0 s).
Trees: `git clone --no-hardlinks --no-checkout` of the seat's clone (read verbs only, push URL `invalid://no-push`) in
scratch; worktrees b1 (BASE + planted slow writer), h1 (head), p1 (head + planted slow writer), n1 (head + planted
never writer); Node v24.22.2, `--maxWorkers=2`, NODE_OPTIONS unset, lockfile blob 2d7dbece2ecd at BASE = head = seat clone.

Blocker 0 | Major 0 | Minor 0 | Info 4

## Findings
| Severity | Finding | Recommendation |
|---|---|---|
| Info | I-1. rd711's `waitFor` re-calls its condition after the loop to compute its return, so with the new condition the signal file is read twice back to back; if a second preload `mark` truncated the file in that instant, `windowOpen` would read false. Marks recur only after a SIGTERM the test sends later (or the 60 s-later interval flush), so no path reaches it. | None; in FOR-RECORDS.md. |
| Info | I-2. rd711 `given.what` would throw TypeError on a file whose JSON is `null`; the preload never writes that. | None. |
| Info | I-3. The commit message carries a `Co-Authored-By: Claude Sonnet 5.5` trailer after the frozen text (message == kit msg-A + trailer, by program; control: without the trailer reads unequal). | None (session attribution rule). |
| Info | I-4. The hosted rate of the race stays unmeasured; the planted writer makes the gap certain, not likely. | Named in NOT TESTED. |

## WHAT WAS MEASURED
### Scope and text (item 1)
- `gh api -X GET compare main...b1966/...`: ahead 1, behind 0, merge base = main, exactly 2 files (rd615 +8 -2, rd711 +8 -2).
- Preload blob at head = at main = `a686b105331b` (hashed both; full a686b105331be8648103a2fb74b67e84ef061300);
  `scripts/verify-expected-counts.json` blob `32146fe9377e` at both. The head diff's 20 +/- lines equal the kit's diff
  block line for line (control: altered line reads unequal); message equals the kit's msg-A plus the trailer.
- Scans over the 16 added lines and the message (`progs/textscan.py`, every pattern with a control that fires): owner
  attribution 0, ticket key 0, B-number/seat id 0, decision-queue/card 0, `existsSync` 0 (3 removed), `new RegExp(`/eval/
  `new Function(` 0, child_process/network 0, timers 0, `.only(`/`.skip(` 0, secret shapes 0, non-ASCII 0, bidi 0; catch
  bindings `_e` and `_e`.

### Attack (item 2)
- **Bounded, both readers.** rd711: `waitFor(signalGiven, waitMs)`, deadline loop (waitMs 120000 for INTERVAL, 15000 for
  TWO-SIGNAL), 100 ms poll; a throw is swallowed by design and only by the condition, so the loop ends at the deadline and
  `windowOpen` is false: the CTRL and TWO-SIGNAL cells then fail BY VALUE (`windowOpen: false`). rd615: `while (step === null
  && Date.now() < by)` with `by` = now + 15000, a final read after the last sleep; `slowStep` null fails the cells by value.
  No infinite loop; a parse error never turns a real failure green: it can only delay until the bound.
- **Plant: never-valid file** (writer creates the file empty and never writes it) at the head: 6 of 8 red, 0 of the red by
  a throw, both files ended at their bounds (138 s wall for both files; no hang). Red cells: rd615 all four (W1 and W2,
  CONTROL and after exit), rd711 CTRL and TWO-SIGNAL; rd711 INTERVAL and SOURCE stay green (they do not assert the signal),
  exactly the kit's M4 row. A missing or corrupt signal file cannot pass.
- **Third reader.** `progs/census.py` over 976 text files of the head tree (not node_modules/.git): 3 files name
  `RD615_SIGNAL_FILE|RD615_SLOW|rd615-slow-audit-flush-preload|slow-step.json`: the two tests and the preload. No reader in
  `scripts/` or elsewhere. Positive control: the three known files are the 3 found; the pattern fires on a planted reader
  line and not on neutral text.
- **Assertions unchanged.** The diff touches only the read lines (rd711 :68-69 -> :68-75; rd615 :87-88 -> :87-94); every
  `expect`/`toEqual` is outside the hunks. In rd615 `.what || null` additionally treats an empty `what` as not yet given
  (the preload always writes `write` or `rename`).

### Jest (item 3; colours from the JSON `assertionResults`; `progs/chain.py`; EADDRINUSE 0 every run; the tree's band had 0 listeners before and after)
| run | tree | cells | result |
|---|---|---|---|
| BASE readers + planted 700 ms writer | b1 | 8 (4 + 4) | **8 of 8 RED**, all `SyntaxError: Unexpected end of JSON input` (66 s) |
| head readers + the same planted writer | p1 | 8 | **8 of 8 GREEN** (70 s) |
| head, real preload | h1 | 8 | **8 of 8 GREEN** (69 s) |
| head + never-valid file | n1 | 8 | 6 RED by value, bound held (138 s) |
Preload blobs after: h1 `a686b105331b` (b1/p1/n1 are scratch trees with the plant, never the project). A full verify was NOT
run by the gate; the seat's plain verify at this head (`VERDICT: PASS 6235/6235, 394 suites`, 22 min 25 s) is RELAYED
from its STATUS.

### CodeQL (item 4)
`pr_codeql_check.sh --repo datasecau/Reporting_Dashboard_Au --checkout <scratch clone> --base 3c3be156... --head d37db35c... --lang javascript --work <scratch>/cq/run1 --threads 4`, one CodeQL process, after the lock: **rc=0** (CLI 2.27.4)
```
VERDICT TABLE (severity rule: security-severity >= 7.0, else problem.severity == error)
  results   head 29   base 29
  KEPT      total 0   high+ 0   (post-filter: primary or any related location START line is an added line)
  NEW       total 0   high+ 0   (rule,file,primaryLocationLineHash multiset, head minus base)
  GONE      total 0
  RESULT    rc 0 PASS (KEPT high+ 0, NEW high+ 0)
```
Open code-scanning alerts on main: 22 (13 backend/server.js, 2 each incidents.js, jsonStorage.js,
routes/entraProvisioning.js, services/emailService.js, 1 tests/uat-run.js), none under `__tests__/`. A local
approximation; the hosted check is the authority.

## LANDING TEXTS (item 5)
`landing.txt` (head-pinned MERGE COMMIT, C-190; `pr_checks_wait.sh --min-checks 7`, 7 names / 8 runs read from PR 242's head;
hosted counts 6235 / 394; no new alert against main's 22; Deploy demo run both jobs skipped: `deploy-demo.yml:29-32`
ignores only `**.md`, `docs/**`, `tests/**`, jobs gated at :53 and :91, last four runs on main skipped, newest jobs
`build skipped`, `deploy skipped`), `merge-subject.txt` (`(#PRNUM)`), `merge-body.txt`, `pr-title.txt`, `pr-body.md`,
`FOR-RECORDS.md` (the new ticket text with measured numbers, relation to RD-711 / RD-615). Who decided: the coordinator;
the product owner only through his dated 2026-11-16 answer, named from rd711's header in FOR-RECORDS.md and in no
committed text.

## NOT TESTED
A full verify (relayed from the seat); the hosted Build and CodeQL on the PR and merge commit; Linux; the real race on a
loaded hosted runner; the Deploy demo run a landing starts; Jira (not read; "no ticket" relayed from B1965 and the seat).
HOW: read the commission, B1964's form, the kit (383 lines, two pages), the seat's STATUS and ANSWER-1 and the diagnosis
whole; GitHub GET only under the NexusAI `GH_CONFIG_DIR`; nothing pushed, opened, merged, re-run or deployed; nothing
sent to any human; nothing deleted. Scratch: `fleet/state/s315/g1975/`.
