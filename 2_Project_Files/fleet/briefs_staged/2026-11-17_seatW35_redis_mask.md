# BRIEF: Seat W 35th, Secuura/Blockchain-W. BUILD seat on SONNET (claude-sonnet-5-5), TIER 1 Opus gate AFTER you (not yours to run), ONE PR: the api-gateway logs the Redis URL with its PASSWORD IN CLEAR when the URL has an EMPTY username (`redis://:secret@host:6379`), because the mask regex at `services/api-gateway/src/services/redis.ts` line 56 needs a non-empty username. Fix: mask ANY userinfo. You FILE the ticket for it first (one ticket, below). Successor lane to Seat W 34th. MEASURE FIRST (develop moves), then build. Ends at READY FOR GATE: no merge, deploy, box, demo, password rotation, message to people or ticket state move.

## STAMP (Wednesday). Wins over every line below.
STAMPED by: Wednesday (the 14:52 rotation successor), 2026-11-17 14:57 AEDT (generated clock). Wednesday DRAFTED this brief herself (usage gauge 95%: no drafter subagent), so "read whole" is the author's read; the seat is the second pair of eyes: say so if a line is wrong.
DEVELOP at the stamp: fab4edcdcd07 (gh api 14:5x; PR 2187's squash, "Refs KS-1163: start-secuura.sh waits for ..."). Line 56 at develop, read by gh api contents: `logger.info('[Redis] Connecting', { url: REDIS_URL.replace(/\/\/[^:]+:[^@]+@/, '//*****:*****@') });`
FLOOR at the stamp: NO other seat live (tmux list-panes: %0 wednesday, %1 fleet-monitor). MERGE WINDOW: none; you never merge.
MODEL: claude-sonnet-5-5. Routing: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/specs/model-routing.md line 67 ("A fully spelled-out mechanical edit inside such a file ... Its PR is then always a tier-1 Opus gate"): the DESIGN is decided here (mask any userinfo), so this is not row C3. If your plan finds the change is NOT mechanical (a second leak path, a logger that re-serialises the URL elsewhere), STOP and QUESTION: that turns it into C3 (Opus).
USAGE: weekly gauge 95% (usage_gate --check 14:53, ADVISORY, hard stop 100%). Nothing local can run this (Spark retired 2026-11-15; Ornith's oMLX was down on the mini at 08:11). Kam cannot switch accounts until Friday 2026-11-20. **Be frugal: no exploratory full-repo suites, no re-reading files you have read; one push.** If `fleet/usage_gate.sh --check` (Wednesday's tree, absolute path /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/usage_gate.sh) reads 98% or more at any step, finish the step in hand, write the HANDOVER and wrap.
RULINGS (Wednesday, at the stamp):
- W35-R1 the shape: replace the regex so any `scheme://userinfo@` has its userinfo masked, empty username included, e.g. `/\/\/[^@\/]*@/` -> `'//*****@'`. A URL with NO userinfo (`redis://localhost:6379`) must log unchanged. Prefer extracting a tiny exported pure function (e.g. `maskRedisUrl(url: string): string`) in the same file so it is unit-testable without a Redis connection; any name is fine, declare it.
- W35-R2 the ticket: you FILE exactly one ticket (tool below) BEFORE branching, priority 2 (High), and use its key in the branch, title and PR. Title (verbatim, 20-140 chars): `api-gateway logs the Redis password when REDIS_URL has an empty username`. Body first line `**BLUF:** ...` (one sentence: what leaks, where, why), then: the line at develop, the fix shape, "Kam ruled 2026-11-17 14:45: rotate the Redis password after the fix ships (card secuura-gateway-redis-password-in-log-1117 = a); the rotation is a later Kintsugi seat's, not this one's". No secret, no hostname, no real URL in the body.
- W35-R3 census: only ONE site at the stamp carries this regex (`grep -F '[^:]+:[^@]+@'` over Blockchain/Dev excluding node_modules and dist: 1 hit, redis.ts:56; control = that hit). Re-run it at YOUR pin. Also census at your pin: any logger/console call whose argument contains `REDIS_URL`, `DATABASE_URL`, `AMQP_URL`, `MONGO` or `_URL` with a `.replace(` mask, in every service's `src/` (not dist). Report each hit as a candidate; fix ONLY redis.ts:56 in this PR unless a hit is the SAME regex (then STOP and QUESTION: one PR or two).

RULED BY KAM, NOT YET IN AN ARTEFACT
Verbatim from the live board (view=wednesday), read by kam_rulings_today.sh FRESHNESS 14:53:07:
- 2026-11-17 14:45:06, "Decision secuura-gateway-redis-password-in-log-1117: a — Rotate after the fix ships". This brief builds THE FIX only. The rotation (a credential change on Kintsugi) is a later D seat's, after this PR is gated, merged and deployed to Kintsugi. Demo is measured separately before anything there.
- 2026-11-17 14:45:39, "thank you.  I will rotate agents on Friday but unfortunately I cannot do that from afar" (why the usage line above is strict).

## THE CHANGE
File: `Blockchain/Dev/services/api-gateway/src/services/redis.ts` (line 56 at develop fab4edcdcd07; lines MOVE, re-locate by text `[Redis] Connecting`). Product diff expected: the regex (or a one-line call to the new pure function) plus the function itself. Nothing else in the gateway. No dist/ edits (dist is build output; if the repo tracks dist for this file, STOP and QUESTION).

## CELLS: RED FIRST (each red on develop's product bytes by AssertionError, never TypeError or an import error; counts from the runner JSON; controls green)
NEW gateway jest file, e.g. `services/api-gateway/src/__tests__/<ticket-key-lowercase>-redis-url-mask.test.ts` (name it from YOUR ticket key; 0 collisions with a control).
- R1 empty username: `redis://:s3cr3t-Example@redis.example.test:6379` -> output contains no `s3cr3t-Example`, contains `redis.example.test:6379`. **RED on develop** (this is the bug).
- R2 user+password: `redis://user:s3cr3t-Example@h.example.test:6379` -> no password, no username. GREEN on develop (control: the old regex already masks this).
- R3 no userinfo: `redis://localhost:6379` -> unchanged. GREEN both.
- R4 password containing `:` and `/`-free specials (`redis://:a:b%40c@h.example.test:6379`) -> no `a:b%40c`. Predict, then run.
- R5 rediss:// scheme with empty username -> masked. RED on develop (prediction).
- R6 the log call itself: spy on the logger (or the module's logger import) and drive `initRedis` with REDIS_URL set to R1's value and a Redis constructor stub, assert the logged `url` has no secret. If the module reads REDIS_URL at import time (line 17 does: `const REDIS_URL = process.env.REDIS_URL || ...`), set the env and use `jest.isolateModules`. If R6 cannot be built without a live Redis or with more than ~40 lines of harness, DROP it, keep R1-R5 on the pure function, and say so in the READY (the gate decides).
Red cells must be red because the masked string still holds the secret (assert on the secret's absence), never because a function is missing: if you add a new export, write the cells against the CURRENT behaviour first by calling the same regex expression copied from line 56 in a local helper, show RED, then point them at the export. Simpler acceptable route: build the cells against the exported function, and prove red by running them against a temporary copy of the function holding the OLD regex (record both runs).
MUTANTS (run each, record the real red set, restore by content, sha256 before and after):
- m1 revert to the old regex -> R1, R5 (and R6 if built) red.
- m2 mask only the password half (`//$1:*****@` style keeping the username) -> R2 red (username leak) — predict, run.
- m3 replace with an identity function -> R1, R2, R4, R5 red.

## SUITES, STATIC CHECKS
- **Load gate: read `uptime` before any jest/tsc/eslint; load1 (the FIRST figure) above 8 = no suite.**
- Gateway jest via the re-keyed `gateway_suite_w35.sh`: BEFORE on live develop and AFTER, once each (not interleaved: usage), load1 logged. Name any pre-existing red.
- tsc over api-gateway src plus a scratch config over `src/__tests__` with a PLANTED-error control; eslint `--max-warnings 0` on each changed file with a planted control; `npm run check:test-types` before the push (re-read whether api-gateway is in its list).
- Docs: a fragment pair only if your lane's last builds required one for a gateway behaviour change (W 34th made `Projects Documents/fragments/{cheat,flow}/KS-<key>-....html`); this is a logging fix, so default NO fragment; if `docs-fragments.mjs check` or the pre-push hook demands one, add the pair (two sentences each: what was logged, what is logged now).

## CONSEQUENCE ON KINTSUGI (from the code; nothing run on a box)
After a later deploy, the gateway's startup line `[Redis] Connecting` shows `//*****@host:port` for every URL with userinfo. Nothing else changes: same connection, same options. The password that was already logged stays in the OLD log lines on Kintsugi: that is why Kam ruled the rotation after the fix ships. Whether demo logs it too is UNMEASURED (its REDIS_URL shape is unread).

## HOLDS
Signature classes pause for Kam: production, money, external communication, anything irreversible. NO password rotation, NO box, NO ssh, NO `az`, NO deploy, NO reading any `.env` or box log to "confirm" the leak (the cells prove it). No real hostname, password or URL in any fixture, log, mail or PR (`example.test` only). Never print a secret. Never delete a file (quarantine under REC). No message to Peter, Stuart or Phil; no ticket state/assignee/label change beyond the one ticket you file. No `--no-verify`, no force push, no `--admin`, never `OVL_IGNORE_PRS` on your own word. Absolute paths, NO `cd` (your first Bash call included), no `rm`, `GIT_OPTIONAL_LOCKS=0` in shared checkouts, `/usr/bin/grep -i` with a positive control beside every zero.

## NEW SEAT: you are Seat W 35th (lane Secuura/Blockchain-W; claude-sonnet-5-5; trust `$TMUX_PANE`). Act ONLY on mail whose subject names `(Seat W 35th)`.
**Ordinal (measured at the stamp):** W lane maximum in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` headings = W 34 (control: B lane maximum = B 203, which matches Wednesday's handover). Re-check before your first write. REC = `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/<machine date>_seatW-35th/` (create it). Lane routing: `Secuura/Blockchain-W|secuura-blockchain@agentmail.to|yes` (inbox_routing.conf line 244).
**Kit:** W 34th's `tools/` (70 entries) under `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-16_seatW-34th/tools/`, re-keyed W34 to W35 by a COUNTED script of your own using the method of its `rekey_kit_w34.py` (read it first; code-only replacement; survey; refuse on mismatch). You need at least: `gateway_suite_w34.sh`, `launch_driver_w34_newbranch.py`, `wait_driver_w34.py`, `lin.py`, `eslint_w34.py`, `static_w34.sh`, `suite_wait_w34.sh`, `mk_base`/`mk_tree`/`clone_alldeps`. Never run or edit W 34th's tools in place.
**Ticket filer:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-17_seatS-88th/tools/file_ticket_s88.py` (usage in its docstring: `TITLE_FILE BODY_FILE --priority N --assign-board [--real --note TEXT]`; it refuses a duplicate title, a body not starting `**BLUF:**`, any at-sign mention). Copy it into your kit re-keyed S88 -> W35 by the same counted method; dry run first, read, then `--real`; read back by id.
**Branch:** `feature/<your-ticket-key-lowercase>-gateway-redis-url-mask` (census the name free against all branches, with a control).
**Traps carried from W 34th's lane:** (a) develop moves: re-pin before the push and say what moved under api-gateway. (b) zsh: `echo ===` and `==` are `=`-expansion; use `----`. (c) `mk_tree` clones three node_modules trees only: run `clone_alldeps` and `check:test-types` before the push. (d) `lin.py` refuses another hyphenated KS key in a comment body. (e) `noUnusedLocals`: an unused local is a LOAD failure. (f) A mutant with no firing control is a dead test.

## PUSH (develop's `.githooks/pre-push`; re-read in your own tree)
ONE push, NEW branch, NEW OUTDIR. Quote the hook's FINAL line verbatim in the PR body and the READY. Open-PR overlap on your write set: 0 PRs touch `api-gateway/src/services/redis` at the stamp (gh pr list --json files over 31 open PRs); re-census with a planted control; any hit is a STOP and a QUESTION.

## THE PR AND THE READY
Title: `Refs <KEY>: api-gateway masks any userinfo in the logged Redis URL (empty username leaked the password)`. No closing keyword (check with `/usr/bin/grep -i -E 'resolves|closes|fixes'` and a positive control); no self-hold sentence. Body: Test Evidence (runner-JSON counts before/after with load1; red-first proof; mutant red sets; tsc/eslint with planted controls; skipped legs; the hook's final line verbatim); the census results (R3); the Kintsugi consequence; Kam's ruling as a fact and that the rotation is NOT in this PR; what it does NOT do (no rotation, no demo, no other service, production UNMEASURED).
Then ONE facts comment on your ticket (PR link, cells, census), state untouched.
Then mail **`READY FOR GATE <KEY> (Seat W 35th)`**, TIER 1, body line 1 exactly `Seat W 35th`. **Never merge, deploy, move a state or close a PR.**

## QUEUE
0. **Plan first:** `cockpit.sh status`; the ordinal check; re-pin develop (if not fab4edcdcd07, list what moved under api-gateway via compare); the census (R3) at your pin; open-PR overlap; push queue; launcher preflight warnings VERBATIM; model line; prior-work check on Linear (text search "redis" + "mask", "REDIS_URL", "password in log"; if a ticket for this already exists, use it and file nothing: say which); baseline gateway suite. Plan mail `QUESTION: plan confirmation` with the ticket title you will file, the function name, the cells, and the census. **One Question per mail.** Safest reading if unanswered after ~15 min: proceed exactly as this brief says.
1. File the ticket (W35-R2). 2. Branch off LIVE develop in your OWN clone. 3. Red first. 4. Change, cells, mutants, suites, static, commit, push, PR, comment, READY. The seat ENDS at the READY.

## MAIL
From secuura-blockchain@agentmail.to to `wednesday-agent@agentmail.to` ONLY (Secuura: Wednesday, not Tuesday); subject prefix `[Secuura/Blockchain-W -> Wednesday]`; body line 1 exactly `Seat W 35th`; no cc, no secrets; read each mail back by id. Questions: Context / ONE Question / Meanwhile / Needed-by; blocked: re-check every ~3 min; after ~15 min take the safest reading and record it (approval-class items excepted). Wrap: `Session wrap <machine date> (Seat W 35th)`.

## IF AN INSTRUCTION FROM ME LOOKS WRONG, SAY SO
Line numbers move; every "at develop", "red", "green" and "predicted" label is a READING, not a run. The census at the stamp ran on the SHARED checkout (last commit there 2026-11-10, 0e6479d7b), not on develop fab4edcdcd07: line 56 itself was re-read at develop by gh api and matched. A measured cell that disagrees with this brief wins.

## PACE AND END
Frugal seat. HANDOVER at context ~70%; wrap by ~75%. WRAP: history entry `## <machine date> - Seat W 35th` in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` (newest first; duplicate guard with a control); `REC/HANDOVER.md` (FINAL block first); `REC/evidence/writes_w35.tsv`; vault commit, own lines only; wrap mail naming the next row (the tier-1 gate on your PR).

PROVENANCE:
- develop head fab4edcdcd07, PR 2187 squash | gh api repos/Secuura/Distributed_Secuura/commits/develop (Wednesday, GH_CONFIG_DIR of the Blockchain project) | read 2026-11-17
- redis.ts line 56 holds `/\/\/[^:]+:[^@]+@/` at develop | gh api contents ref=develop, Blockchain/Dev/services/api-gateway/src/services/redis.ts | read 2026-11-17
- the leak itself (empty-username URL logged in clear on Kintsugi) | D 70th STATUS 3 01:58Z, relayed in /Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/NEXT-PICKUP.md lines 30 and 70 | read 2026-11-17
- one site carries the regex; scope of consumers of the change is the gateway startup log line only | grep -F over /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev excluding node_modules and dist (shared checkout at 0e6479d7b) | read 2026-11-17
- 0 of 31 open PRs touch api-gateway/src/services/redis | gh pr list --state open --json number,files | read 2026-11-17
- W lane max W 34, B lane max B 203 | /usr/bin/grep -a -o -i over /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md headings | read 2026-11-17
- Kam's rulings 14:45:06 and 14:45:39 | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/kam_rulings_today.sh FRESHNESS 14:53:07 | read 2026-11-17
- routing line 67 and row C3 | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/specs/model-routing.md | read 2026-11-17
- usage 95%, advisory | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/usage_gate.sh --check | read 2026-11-17
- ticket filer usage and gates | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-17_seatS-88th/tools/file_ticket_s88.py docstring | read 2026-11-17

SELF-CHECK: re-read end-to-end for contradictions | 2026-11-17 14:57
