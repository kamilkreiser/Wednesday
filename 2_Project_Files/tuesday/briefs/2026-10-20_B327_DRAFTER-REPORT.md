# B327 DRAFTER REPORT — gate 31 kit + launcher (NexusAI RD-863 / PR #99 @ 172d321)

Drafted 2026-10-20 from 14:01 AEDT (first `date` 14:01:26) by a read-only drafting sub-agent. Nothing was run, launched, mailed, committed or chmod'ed.

## Outputs
- Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-20_B327_SEAT-G19_nexusai-gate31-pr99.md` (184 lines; slots ONLY `MAIN_SHA` x2 and `LAUNCH_TIME` x1; last line `READ-WHOLE-BY-TUESDAY: PENDING`).
- Launcher: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate31.sh` (derived from gate 30's; NOT chmod'ed, NOT run, NOT even `bash -n`'d).
- Static cross-check (not a run of the launcher): a scratch python checker extracted the launcher's embedded prompt and replayed its declaration lists (guards 10, 12, 14, 19, 24, 53, 71, 76-82, the T-slot form, the rows, the WRONG markers, the 10 CLARIFICATIONS quotes) against the kit: **0 misses**; negative control (a scratch kit with `M863-c` renamed) → flagged. The MAIN-STAMP and READ-WHOLE refusals were not exercised.

## What I measured (14:01-14:10 AEDT)
- **Pins:** `ls-remote` main = `39653db4`, branch = `refs/pull/99/head` = `172d321f…` (rc 0, 1 attempt). Head tree `a5bee805…`, parent `39653db4`, ahead 1 / behind 0. PR #99 draft, mergeable `clean`, 3 files +144/−6.
- **Diff:** A `__tests__/rd863-group-nouns-not-users.test.js` (blob `2a17826c`), M `backend/server.js` (2 hunks, `8193f799`→`624abb25`), M counts file (4880/302 → 4934/303). Lockfile, package.json, deploy-demo, seed CSV, intentRouter, RD-395 harness and preload: same blobs at base and head.
- **CodeQL / CI:** analyses js/ts `1985610931`, python `1985603966`, actions `1985603725`, all results 0; 0 open and 0 fixed on `refs/pull/99/head`; control PR #96 = 6 fixed. 8/8 check runs success (build 02:56:43Z).
- **16 seeded users:** seed CSV has 1445 rows and 16 distinct names. A static scan of their 32 words against the 21 nouns (±s/es) and the prototype names found 0 hits. Control: `guests` hit.
- **Corpus:** FOUND. See the next section.
- **Port block `7620-7629`:** no listener (`lsof` rc 1). Unfiltered control: 11 listeners. No 2026-10 brief or launcher names 762x (grep 0 files; control `7330-7339` matched 9).
- **Floor (14:03):** lock tool sha256 `3c33f5ae…` = pin. Jest lock HELD by `qa-g30-H1b` (pid 20764, since 02:55:16Z). queue-jest empty. load 11.95. T9 unmounted. Node v26.8.1, gitleaks 8.30.1. NexusAI `.git/objects` 268 before and 268 after my one legacy merge-tree read.
- **PR overlap:** #97 (head now `278afc2`) touches `server.js` + counts. Legacy merge-tree against #99: server.js has no conflict marker, the counts file CONFLICTS. #98, #100: 0 overlap. #67: counts only.

## The corpus (the mandatory item)
- **Path:** `/Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-10-19-gate28-batch-rd476-rd856-rd857/evidence/r6/corpus.json`
- **sha256:** `6f5c40314bd437dc91997c3ab7967c50973fc396c4f4f90c278890294545fdf5`. Gate 28's report prints `6f5c4031…`.
- **Count:** 173 entries with 173 distinct ids.
- **Generator:** `evidence/inst/qa-corpus28.py`.
- **How to tell it is the same corpus:** the sha256, the count and the ids, plus a byte-equal regeneration from the generator. The launcher refuses on any mismatch, and it also pins gate 28's five instruments.
- Gate 28's kit names "your own corpus" but gives no path. The path came from gate 28's report §r6(C). The AMEND-REPORT does not mention the corpus.

## Things the kit flags that Tuesday should know
1. **gate 28's slice cannot run the head as-is (READ-ONLY-INFERRED).** RD-863 puts `OBJECT_PROTOTYPE_NAMES_LOWER` at top level, outside `checkForCurrentUserQuery`, and `qa-slice28.js` only extracts the function. On the head it would throw `ReferenceError`. The kit tells the gate to extract that line too, with a control showing the unpatched slice throws.
2. **A real-surname collision: `Guest` (READ-ONLY-INFERRED).** `guest` is one of the 21 nouns, and one rejected word rejects the whole capture. So a roster user named "Sarah Guest" would stop reaching the handler. No seeded user is affected. The kit adds a planted-roster leg (r4S) and leaves the rating to the gate (drafter's lean: Minor).
3. **The drafter's prior for r4 (READ-ONLY-INFERRED, from gate 28's `diff2-mbc.json`, not from 39653db):** 15 INTENDED flips from not-found to the stand-in, 0 UNINTENDED. 11 questions stay not-found, including executives and teachers (neither word is on the list).
4. **The `+es` arm cannot be killed by any RD-863 cell,** because no group noun takes -es. The kit marks it as an expected survivor so it is not read as a Major.
5. **Possible gate-30 hygiene issue (observation only, not in this kit):** the jest lock owner file shows `qa-g30-H1b` with `cwd=…/2026-10-18-gate27-rd778/evidence/inst`. Gate 30 may be running from inside gate 27's evidence directory, and its H-33 forbids writing there. Worth a look.

## Tier / model
**Tier 2, Sonnet `claude-sonnet-5-5`.** The basis is routing v1.0 §4c row G2: "follow-ups whose mechanism a prior gate already measured". RD-863 fixes gate 28's own finding in the same function. The change is OR-only and used only under negation, so fewer questions reach the handler and none newly does. It touches no auth, secret, deploy or package surface. This agrees with Tuesday's prior.

The model id is RELAYED from gate 30's stamped self-check (`models_latest.json` is outside my fence). Launcher guard 9 re-reads the file.

## Open questions (each with a recommended answer)
- **Q1. Accept the kit's corpus identification (gate 28 `r6/corpus.json`, sha256 `6f5c4031…fdf5`, 173)?** Recommend: YES. It is MEASURED and pinned by the launcher.
- **Q2. Tier 2 Sonnet, or Opus because this is a product-server change and gate 28 ran on Opus?** Recommend: Sonnet (row G2). Routing row G2's own escalation covers a security-shaped surprise: the PR goes to G1.
- **Q3. Pre-rule `guest`, or let the gate measure it?** Recommend: let the gate measure and rate it (r4S). Then decide between keep, drop, or accept-and-document. If the word is dropped, the head moves, which means a round 2 / delta gate.
- **Q4. Landing order with PR #97.** Both PRs change the counts file, so the second to land needs a counts-only TURN, which is a new head. Recommend: land whichever gets its GO first. Gate the second as a delta whose only allowed difference is the counts file (prove it with `git diff`) plus its new CodeQL run, rather than a full re-gate.
- **Q5. Stamp design.** The T0-T5 rulings are filled with the drafter's defaults instead of slots, and gate 30's SELF-CHECK lines are replaced by the `READ-WHOLE-BY-TUESDAY` last line, which the launcher refuses while it reads PENDING. Recommend: accept. It is what the brief asked for: slots only for the launch time and main's sha.
- **Q6. Gate 30's launcher deferred on a gate-29 HOLD (33L). I dropped that and kept FIFO, so gate 31 can launch while gate 30 holds the lock.** Recommend: accept. FIFO already serialises the holds, and only a qa-g31 ticket or holder refuses.
- **Q7. T1 default (a): no full verify** (the PR Build ran 4934/303 on Node 24). Recommend: accept (a).
- **Q8. Unverified by me:** `fleet/briefs_staged/2026-10-05_qa_b14_sqlite3_ANSWER.md`, `…_qa_gate16_notifier_ANSWER.md`, `inbox_routing.conf`, `models_latest.json` and BRIEF_TEMPLATE are outside my fence. The launcher keeps gate 30's checks on them unchanged. Recommend: run `bash -n` and then `--check` before stamping. Expected refusal: 32S (slots and PENDING), plus 40 until the routing line `QA/NexusAI-gate31|tuesday-agent@agentmail.to|no` is added.
- **Q9. Fence disclosure:** I read gate 28's and gate 27's report directories under `Testing Agent MAIN` (read-only). The task named the gate-28 report, so I read it there. Recommend: no action.
