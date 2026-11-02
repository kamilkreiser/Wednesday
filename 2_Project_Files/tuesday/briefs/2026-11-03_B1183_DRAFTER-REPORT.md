STARTABLE: YES (after Tuesday stamps the 9 four-underscore lines and answers Q-1 to Q-3; no pane, ref, worktree or session-tools directory named N93/b1183; origin main `2567293f` read at 06:11 and 06:17 AEDT; open PRs 0; no NexusAI seat live, so launch_when_cool waits only for load1 below 7, which read 5.63 4.92 4.53 at 06:12)

# B1183 DRAFTER REPORT (kit `2026-11-03_B1183_SEAT-N93_nexusai-rd917-streamexport-destroyed-and-vanished.md`, 37.5 KB, this report beside it)

## BLUF
One Sonnet C2 builder (row C2, `model-routing.md:92`), ONE commit on `b1183/nexusai-rd917-streamexport-destroyed-and-vanished` from main `2567293f`: `streamExport` rejects when its destination closes with no `finish`, a vanished (ENOENT) file leaves `manifest.json` and `filesIncluded`, three cells in one new test file (+3 tests, +1 suite: 5294/314 to 5297/315, one `--update-counts`). Ends at READY FOR QA; gate G2 (`:109`), round 1 of 2, escalating to G1 on a STOP, an unbitten mutant or the size bound. **Seat label: N91 and N92 were both taken (B1148 = N91, B1167 = N92); N93 is the next free number** (scan of the 2-3 Nov non-`.pre` SEAT kits for `N93`/`NexusAI-N93`/`b1183`: 0 files; control `NexusAI-N92`: 4 files).
**The finding that matters:** the ticket's "10 to 15 lines" will probably not hold. `manifest.json` is serialised at `dataExport.js:377` on the same synchronous pass that queues the files, but the archiver judges a missing file later and asynchronously (archiver 7.0.1: `core.js:121` queues the stat, `:435` emits the warning). Dropping the row on the warning would leave the ZIP's `manifest.json` still naming the file. The kit says so, makes the builder prove the manifest INSIDE the ZIP, and sets a 60 added-line bound after which it stops (Q-3).

## Facts re-measured (instrument; control)
- Clock: `date` 06:10:49 at the first measurement, 06:17:04 at the last.
- Main: `gh api -X GET git/ref/heads/main` = `2567293f8211d2431f6be3d2df3c45585c9029d0` twice (06:11, 06:17). Tarball of that sha extracted in the scratchpad (`.../scratchpad/b1183/x`); blobs by `git hash-object`: `backend/dataExport.js` `2a4ba545` (404 lines by `wc -l`), `verify-expected-counts.json` `b384e09b` (`cat -n`: tests 5294 `:4`, suites 314 `:5`, `_updated` `:3`), rd913 file `4a47b115`, deploy-demo `597b3487`, build.yml `e4e5c095`, verify-suite.sh `eb9731f5`. The first three blobs are of the three-file set the sweep named; the sweep's counts pair matches.
- Every `streamExport` pointer in the kit (`:212 :217 :218 :221 :223-:226 :224 :225 :227 :234 :305 :350 :361 :370 :377 :379-:382 :383-:389 :391 :397`) was printed by `awk NR==`/`grep -n` over the raw file at the pinned sha; `server.js:18901 :18911 :18912 :18913-:18919 :18918` by `awk` over the same tree; rd638 `:45 :57 :58 :60 :110` and helper `rd525-live-store.js:146 :198` by `grep -n`; `package.json:51 :97-:125` by `sed`; deploy-demo `:26-:32 :53 :91 :95` and build.yml `:3-:9 :29 :83-:84` and verify-suite `:258 :343 :349 :354 :360 :366` by `awk`; C-190 `:2062`, item 2 `:2067`, addendum `:2076-:2081`, C-224 `:2412`, C-231 `:2467` by `grep -n` over CLARIFICATIONS (2472 lines by `wc -l`). Depth-1 `__tests__/*.test.js` = 314 = counts `suites` (control that agree); `rd917*` in `__tests__`: 0.
- Absence of a close handler: `grep` for `on('close'` in dataExport.js 0, control `on('finish'` 1 (stale-checkout `git log -S"destStream.on('close'"` prints nothing, control `-S"destStream.on('finish'"` prints `798f020`; the stale checkout ends 2026-09-08, the builder repeats on full history).
- Archiver: `package-lock.json` at main = 8.0.0 (python read of the lock), `package.json:51` `^8.0.0`. The only archiver source I could read is 7.0.1 in the stale shared checkout (`core.js:121`, `:435`); archiver 8 is UNMEASURED and the kit tells the builder to read it at Step 2.
- Jira (project `b774lib.py` in-process, `python3 -I`, GET only, token never printed): RD-917 To Do, Low, 4 labels, 1 comment read whole (the 00:21 decision). Control `RD-99999999` 404. Searches: `streamExport` 7 issues (RD-917, 826, 791, 640, 638, 617, 616), `dataExport` 18, control `zzqxnonexist` 0. Statuses read: RD-913 Testing, RD-638 and RD-791 Release Ready, RD-826 To Do, RD-640 Testing (its comments edit `dataErasure.js`), RD-902 and RD-916 To Do.
- Branches: six branches name the export; `compare main...<b>` ahead 0 on all, behind 328-628, none touches `backend/dataExport.js` (control b1167 ahead 0 behind 1). `matching-refs` for `b1183` 0 and `b118` 0; `b1167` 1 (landed branch). Open PRs 0; control `pulls/99999` 404.
- Deploy: repo variables total 0; environments `["dev"]`; the four newest push runs of deploy-demo (`2567293f c8f361aa 91d0d6e9 a91753cd`) all `skipped`; control variable `zzqxnonexist` 404. Org variables: 403 (UNMEASURED).
- Routing: lines 92 (C2), 94 (C4), 108 (G1), 109 (G2) printed by `grep -n`; model id `claude-sonnet-5-5` from `models_latest.json` `levels.sonnet.model_id`.
- Ports/seats: `lsof -nP -iTCP:8500-8599 -sTCP:LISTEN` printed nothing; `tmux list-panes -a`: `tuesday`, `Datasec/Security-Composer-G308`, `Datasec/MPS-M85`, `Datasec/MPS-G307`, `fleet-monitor`.
- Slots: `grep -o -E '_{4}'` on the kit prints 9 matches (`grep -c` 9 lines; same as B1167's `.pre-stamp`). No person's name, no `@...@` token, no `06:1x`-style placeholder (grepped).
- C-190: the entry says "land the SAME commit. Never squash, never rebase"; the phrase "head-pinned" is not in the entry (the kit says so and says "a merge commit of the gated head").

## D-decisions (mine, overrule at the stamp)
- D1: seat N93, pane `Datasec/NexusAI-N93`, branch `b1183/nexusai-rd917-streamexport-destroyed-and-vanished`, worktree `worktrees/b1183-n93`, hard stop 150/210 as B1167 (two verifies plus waits).
- D2: the decision's three "cells" are mapped to D (destroyed destination), V (vanished file, a loop over the four `archive.file` sites inside the one body so the closed list is a property), W (the non-ENOENT warning branch at `:225`). W is a characterisation cell: green at main, proved by mutant MC (precedent: RD-640 T1, relayed from that ticket's comment). So "red first" is D red, V red, W green-by-design; the kit says so and predicts it.
- D3: wording rule applied: "Under the product owner's delegation (C-231) the coordinator decided ... open to his veto"; no "he ruled".
- D4: 60 added-line bound on `backend/dataExport.js`; beyond it STOP. The mechanism is left to the builder (property plus the hazard stated), because I could not read archiver 8.
- D5: the finalize catch (`:379-:382`) is a finding (Step 6, 20 minutes), not a fourth cell, because three cells were decided; reaching it ends in a question about a fourth cell (+1 test).
- D6: G2 round 1 of 2 with escalation to G1 (the file is the data-rights export).
- D7: partition names RD-902 then RD-916 as queued behind this lane for the counts file; RD-826 (same file, near `:279`) named as a separate lane and HOLD 4.

## Q-questions for Tuesday (each with a default)
- Q-1 gate tier. Default G2 (Sonnet) with the escalations written in the kit. Alternative G1 because the export is the data-rights artefact.
- Q-2 cell count. Default as drafted: exactly three cells (D, V, W) and Step 6 reports the finalize catch without a fourth cell. Alternative: a fourth cell for the finalize catch now (counts +4/+1).
- Q-3 size bound. Default 60 added lines in `dataExport.js`, STOP above it. The ticket's 10-15 is relayed and, by my reading of `:377`, probably too low.
- Q-4 (not blocking) a non-ENOENT warning (for example a directory named like a rotated log) may leave the same manifest overstatement; the kit reports it as a finding (HOLD 2) and does not fix it. Default: report only.

## UNMEASURED
- Archiver 8's source (stat queue and warning emission, and the codes for a directory or link). The cell W provocation (a directory named like a rotated log) is my reading of archiver 7, not run.
- That the `fs.statSync` spy approach for cell V is deterministic under jest and Node 26; offered as a suggestion, the builder may choose another.
- That D red / V red / W green at main (predicted from source, no jest run by a drafter).
- Whether the diff fits 60 lines; whether the ZIP entry order matters to any cell.
- Organisation variables of the repo (403); CodeQL and the hosted Build on the eventual PR; the hosted node version.
- The ticket's size "10 to 15 lines" (relayed).

## Outside-the-fences disclosure
- Writes: the two named files, plus scratch in `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/b6404be7-7dc9-4eec-9a83-b75139a48267/scratchpad/b1183/` (the tarball and its extraction, three small Jira read scripts `jira.py`, `j2.py`, `j3.py`).
- Reads/GET: `gh api -X GET` under the NexusAI `GH_CONFIG_DIR` (ref, pulls, branches, compare, matching-refs, tarball, variables, environments, workflow runs; organisation variables answered 403, the pulls/99999 and variable controls answered 404); Jira GETs via `b774lib.py` in-process (`issue`, `comments`, `search`; no write verb); `git --no-optional-locks log -S` on the stale shared checkout; `tmux list-panes -a`; `lsof`; reads of CLARIFICATIONS, briefs, specs and the stale checkout's `node_modules/archiver/lib/core.js` and `package.json`.
- Not done: no `decision_queue.sh` verb, no card read; no `fleet/briefs_staged`, scoreboard, `_ledger.md`, WEDNESDAY/FRIDAY tree or non-Datasec project; no `cd`; no docker/az/ssh; no HTTP to any hosted host; no Artifact/Docs/mail tool; `stamp_paths_check.py` and `brief_seat.sh` read by header only, not invoked; I read the large `brief-standing-lines.md` and `BRIEF_SKELETON.md` only by their first lines (the output was truncated), taking the standing lines from the B1167 kit as the template.
- Near-misses: three tool calls drew hook advisories (a `cd`-containing first call was refused and rerun; a `====` separator was refused by the zsh hook; several case-sensitive greps drew advisories, each used with a positive control or on a file I had printed).
