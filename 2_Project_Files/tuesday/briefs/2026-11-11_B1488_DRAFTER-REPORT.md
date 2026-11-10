# B1488 DRAFTER REPORT: SEAT-R208 MPS records kit (11 Nov)

## BLUF
- **Kit:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-11_B1488_SEAT-R208_mps-records-1111.md`, 102 lines. The `.pre-stamp` copy beside it is identical (`cmp` equal, sha256 `ef9a8af00b5e9f02...` both). It has 16 four-underscore slot lines and 0 non-ASCII bytes.
- **The list has 7 keys.** Five can move: 205, 221, 178, 225 and 254. Two are comment-only: 195 and 124. Each of R204's other keys is left out with a one-word reason, per your 10 Nov ledger rule.
- **205:** every clause reads MET at code main `54ed7627`. Its files are unchanged since #169. **Recommend: name it.** One caveat, not a blocker: review finding 4 says no one ran the real `dotnet build -c Release`, then package. Reading (l) covers that, and comment 40920 already says it.
- **221:** both clauses MET. The only hold is the backlog row `[B873-B866-9]`, a scanner false positive in a *different* file (`SourceLifecycleTests.GateB41.cs:85-86`) that 221's Acceptance does not name. **Recommend: ROW-RESIDUAL-221 = YES, and name it.**
- **records/b1406 has a new problem: it can no longer fast-forward.** R204's C-100 commit moved root main to `f4d126fb` after the branch was cut from `13db4d11`, so it is now a sibling of main. R204 was told NO only because you had not verified the row. I have now read it: one line, names only, and every pointer still holds at code main. The kit's slot is **LAND-1406 = PICK or NO**. PICK means a `cherry-pick -x 1af6c445` onto `records/b1488`, with a blob assert, landed by the seat's one ff-only. **Recommend: PICK, and name 225.**
- **#175 (B1471 docs, now code main `54ed7627`) is the only landing since R204.**
  - 178: clause 2 is now corrected at `docs/API.md:441-444`, and its table should read 4 of 4. **Recommend: name it.**
  - 195: item 6 is closed, but clause 3, the "(whole seconds, at least 1)" text at `:744`, still holds it. Comment only.
  - 124: clause 5 is closed, but clause 4 and the Retry-After residual still hold it. Comment only.
- **Suggested MOVE-KEYS: `MPSCALC-205, MPSCALC-221, MPSCALC-178, MPSCALC-225, MPSCALC-254`.** Each still moves only if the seat's own table reads MET throughout. 254 moves only if the seat finds and reads #134's review record.

## Facts measured (instrument, clock)
All reads only. `date` printed 07:24:01, 07:24:33, 07:25:08 and 07:29 (`uptime`) AEDT, 2026-11-11. GitHub reads used `gh api -X GET` under the MPS `GH_CONFIG_DIR`. Jira reads went through a GET-only python helper in my scratchpad that read the credentials from `.env` by name, in-process, and never printed them.

**Code repo**
- Code main is `54ed76273cf5e7eb804315635c413034f28b3372`. Open PRs: 0. Control: `pulls/99999` answers 404.
- **#175:**
  - Merged `2026-11-10T05:20:42Z` (16:20:42 AEDT). Squash = main. One parent, `dad90244`. Head `79c2a09b`.
  - 3 files: `docs/API.md` +12 -6, plus one line each in `SOURCE.txt` and `schema.ts`.
  - 12 of 12 check-runs success. `ci` push and `Push on main` both succeeded on attempt 1.
  - Per-file blobs of the reviewed head equal the squash for all 3 files. Control: each differs at the parent.
  - Review `2026-11-10_B1471_verify/VERDICT.md:1`: GO WITH FINDINGS (3 Minors, no Major).
- No `b1472` ref exists on origin. Control: `heads/b14` lists `b1471/...`.
- Code-scanning alerts: open 0 and fixed 0. **This zero has no control that fires.** The kit forbids writing "no alerts".
- No changes since the reviews on 205's or 221's files:
  - `compare 8d665e3f...main`: 0 `scripts/` files. Control: 2 `docs/` files.
  - `compare 94b24e8b...main`: 0 `CareKeyPattern` files. Control: 1 for API.md.
- `scripts/package.sh:43-44` at main holds the 205 guard (`awk`).
- `GateB41.cs:85-86` at main still holds the case-id list (`awk`).
- `docs/API.md`, read at main:
  - `:441-444` is the new lifecycleEvents sentence.
  - `:739-746` is the rate-limit sentence. `:744` still holds "(whole seconds, at least 1)".
  - `:768-771` is the lock-order sentence.

**Jira**
- Census: 386 issues, 167 Done, 219 open.
- `text ~ "B1488"` returns 0. Control: `text ~ "B1196"` returns 6.
- Read whole, all Backlog: 205, 221, 178, 195, 124, 225, 254 and 157. I also read their comments 40920, 40102, 40527, 40915, 40913, 40942, 40927, 40945, 40955 and 40956.
- Transition 41 (Done) is listed for 205, 221, 178 and 195.

**Root records repo**
- HEAD = main = `f4d126fb`. 1,118 status lines, 3 tracked files modified. `SETUP_RUNBOOK.md` is clean.
- `records/b1406` = `1af6c445` with parent `13db4d11`.
- Ancestry (`merge-base --is-ancestor`):
  - main into b1406: rc 1. b1406 into main: rc 1. So no fast-forward either way.
  - Control: 13db4d11 into main returns rc 0.
- `13db4d11..main` changes only `CLARIFICATIONS.md`.
- `SETUP_RUNBOOK.md` blob: `be440632` at main and at 13db4d11; `2b7032f1` at b1406.
- The runbook row's pointers still hold at code main:
  - `DEMO.md:165` still names `MPSCALC_API_CLIENT_ID`.
  - `seed.py` names it 5 times and `MPSCALC_HOSTED_HOST` 7 times; the bicepparam names the client id once.
  - `compare 31234f5f...main` touches none of those files.
- `.env` holds neither name (anchored counts 0 and 0; control `JIRA_EMAIL` 1; no value was read).
- Absent: `.tools/.git-lock`, `.tools/b1488` and `.tools/wt-b1488-records`.

**Floor**
- No `Datasec/MPS-` pane (3 panes in all).
- Seat id R208 is free: 0 `SEAT-R208` files (control R204: 2).
- No listener on ports 9400-9439 (`lsof` rc 1).
- load1 8.68. Free disk: 1324 GiB.

**Tools**
- `status_watch.sh:56` matches `"READY B"[0-9]*`, `STOPPED:*` and `BLOCKED:*`, so the kit's last lines fire. `WORKING:` does not fire.
- `model-routing.md:98` is row C8 and `:110` is row G3.
- `brief_seat.sh:24` defaults to opus, so the kit puts `BRIEF_SEAT_LEVEL=sonnet` inside the launch quotes.

## What I could NOT measure
- **254:** the review record of MPS #134 (not opened). R204 also relayed it without reading it. The kit makes the seat find it and test blob equality, or leave 254 unmoved.
- **205:** whether a real-SDK `dotnet build -c Release` leaves a `.pdb` in `obj/Release`. No one has run that chain.
- Whether the cherry-pick applies cleanly. I derived that it will, since the only path main changed is `CLARIFICATIONS.md`, and the kit makes the seat abort and treat the slot as NO on any conflict.
- The project's total comment count: I read only the 7 keys.
- Any hosted site, and the alert list (the zero above has no control).

## Open decisions for Tuesday (each with my recommendation)
1. **MOVE-KEYS.** Recommend `MPSCALC-205, MPSCALC-221, MPSCALC-178, MPSCALC-225, MPSCALC-254`. The table gates each one, so naming 254 costs nothing if its review cannot be found.
2. **ROW-RESIDUAL-221.** Recommend **YES**. The row is about a different file that 221's Acceptance does not name, which is the same logic as reading (d). The row stays open and untouched. The question of whether that second file's false positive gets its own ticket stays open (`CLARIFICATIONS.md:1669` item 7(d)).
3. **LAND-1406.** Recommend **PICK**. A straight fast-forward is impossible now. A non-fast-forward merge commit would be the first in this records repo, and the fences forbid it. PICK keeps the line byte-identical (blob asserted) and records where it came from (the `-x` trailer). `records/b1406` itself is kept.
4. **Q-R208-3, reading (w) for 225.** Recommend **yes**. Reading (w) says a ticket whose only Where is a root records file is met when root main holds the change. R204's own comment 40945 already said the merge would release it. The kit records it as the coordinator's reading, not the product owner's.
5. **Q-R208-2, 205 with the real chain unrun.** Recommend **move**. The review's program probe and red-first rows are independent measurements, so this is not a builder's say-so (reading q does not bite). Reading (l) is the precedent, and the comment will say "read, not run".
6. **Q-R208-1, 157.** Recommend **leave it out**. The `needs-ruling` label stands, PR #50 has no independent review line, and the Acceptance says "Per the ruling (K-15)".
7. **COMMENTS = FILE, REC-CLAR = FILE.** Same as R204's stamp.

## Observations (not in scope; for you)
- **Your ledger row of 10 Nov** (`_ledger_laptop_datasec.md:20`) says 205 "sat in the body-only column of #168's row". The source says #169: B1470 kit `:23` lists 205 in #169's body-only column, and comment 40920 cites PR #169. The rule itself is unaffected.
- **178 / [B36-K6]:** #175's body asks for "the ticket text" to be corrected. 178's Jira description names no route; the stale route list (duplicate described as body-less) is only in BACKLOG `[B36-K6]`. The kit has the seat append a pointer row rather than edit anything.
- **B1472 M112** (MPSCALC-203, the production deploy script) is still unstamped and has no branch. It is left off this list (reason: lane).
- R204 left more keys that are blocked only on your readings or on the product owner. They are not in this kit:
  - **CAP-READING** (cap NO GO): 302, 207, 325, 338, 339, 331, 333.
  - **The product owner:** 380 (guard shape) and 381.
  - **A ticket create:** 119 (the infra follow-up).
