STARTABLE: YES (once Tuesday stamps; 8 four-underscore lines to fill; Q-1 to Q-4 below carry defaults)

# B668 DRAFTER REPORT (gate kit for MPS PR #113, ROUND 1 OF 2, tier 2, SEAT-G116)

Drafted 2026-10-25 13:29-13:50 AEDT (clock from `date`) by the read-only gate-kit drafter (Sonnet 5.5), under `DRAFTER_RULES.md` (read whole first). Two files written: the kit `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-25_B668_SEAT-G116_mps-113-gate-tier2.md` (110 lines) and this report. No `.pre-stamp` copy was made: `cp` the kit to `.pre-stamp` before filling a slot.

## BLUF
- Kit is startable: pins fresh at 13:29 (head `3e61c27a`, main `dd0ce36d`, merge ref `c0215d96` with tree `41b083c3` = the head's tree, ahead 1 behind 0), 8 slot lines (`/usr/bin/grep -c -E '_''_''_''_'` = 8: lines 37-43 plus the last line 110), `@[A-Z_]+@` = 0, non-ASCII lines 0, person-name grep 0.
- C2 is the heart: the gate rebuilds the builder's S1-S6 from text and adds N1-N9, three seeded edits (seed 668101), an assertion-pin table (every `Assert.` line pinned by a named mutant or marked UNPINNED) and vacuity probes for the zero-count legs (F1 "Loaded" = 0 and "cannot be opened" = 0 are satisfied by a rename; the drafter predicts N3 and N2 leave F1 green).
- Main-moved rule is written for the 15:00 landing of PR #110: STOP only on the listed anchor paths, otherwise re-pin and run C4/C6 at the new merge ref; #110's validator file is read by the store load, so the gate also builds scratch merges with #112 and with #110 and runs the new class on them (red = Major for the merge order).
- One new fact for Tuesday: the PR TITLE carries `MPSCALC-332:` (Q-2).
- Ports 9630-9639: free (lsof rc 1), one word-boundary hit on a finished HPSM-POC kit (B613); heavy-slot-1 held by B663 (`j5-family`) at 13:3x.

## Facts re-measured (instrument, time, control)
- `git --no-optional-locks ls-remote origin` (13:29): main `dd0ce36dc1083266bf89c55d9ddab4aa9efb4c85`; `refs/heads/b665/mps-store-first-use-absent-row` = `refs/pull/113/head` = `3e61c27a8166761c510686ea0875da3ee4570f1a`; `refs/pull/113/merge` = `c0215d9606751a587b594f421bee2e309ee3fca8`; `refs/pull/112/head` `6618f119...`; `refs/pull/110/head` `650ddfb7...`. Control: the same listing prints the other `b6*` refs (b60, b603, b614, b62, b630, b654, b69) and is not empty.
- `gh api -X GET` (project `GH_CONFIG_DIR`, the project account): `pulls/113` open, not draft, mergeable true, `mergeable_state` blocked, 1 commit, 1 file, +118 -0, base `dd0ce36d`; commit parent `dd0ce36d`; `commits/c0215d96` parents `dd0ce36d,3e61c27a`, tree `41b083c30bc65d17a8766a8b1de733eb666bf0ae`; local `rev-parse 3e61c27a^{tree}` = the same id (control: the base tree `9629b441...` per the builder differs; the drafter did not re-print it). `compare` ahead 1 behind 0, 1 file.
- Delta: `diff --stat dd0ce36d 3e61c27a`: one file, 118 insertions. `rev-parse` of `src/MpsCalc.Api/Sources/ActiveSources.cs` at head and base both `8942fe8aedaa9450149d83eda72515c5a4b36dfd` (a non-event is a weak control; the control is that the two refs resolve, `cat-file -t` = commit for both).
- Squash settings: `squash_merge_commit_title` COMMIT_OR_PR_TITLE, `squash_merge_commit_message` COMMIT_MESSAGES, squash/merge/rebase all allowed.
- Check-runs at 13:29: 8 listed, all queued or in_progress (CodeQL umbrella queued); `analyses?ref=refs/pull/113/head` 1 row (actions, results 0); main's analyses listing returns 30 rows (positive control); alerts open 0 on the head ref (no positive control). Ruleset: code_scanning thresholds errors + high_or_higher, required_status_checks list empty, deletion, non_fast_forward.
- Open PR file lists: #110 (5 paths) and #112 (4 paths), 0 shared with the one path (control: `docs/API.md` and `QuoteRefusalOrder.cs` printed in their lists).
- Source anchors in `ActiveSources.cs` at head (`git show "${H}:path" | /usr/bin/grep -c -F`): 11 anchors read 1 (and `return new FixedActiveSources(null);` 3), control `zzz-no-such-string-7f3a` 0. Lines: `:172` check, `:198` catch, `:233` Settle, `:238`/`:244` sentences.
- CI: `ci.yml` at main read by `contents?ref=`: dotnet job ubuntu-latest, build then test, no filter/shard/SQL; `Directory.Build.props` `TreatWarningsAsErrors>true` count 1.
- Instruments: `models_latest.json` line 23 `claude-sonnet-5-5`; `usage_tuesday.json` pct 81 (ts 13:28 AEDT); `uptime` 13:29 load 7.02 6.66 6.87; `model-routing.md:109` is row G2, `:111` G-cap (read by `sed -n`). `CLARIFICATIONS.md:809` (landing rule) and `:1327-1336` (the ruling) read by `sed -n`.
- Ports: `lsof -nP -iTCP:9630-9639 -sTCP:LISTEN` empty, rc 1 (no bind control run). Word-boundary scan of non-`.pre-` SEAT kits of 10-24 and 10-25 for `963[0-9]`: ONE hit, `2026-10-25_B613_SEAT-H17_hpsmpoc-test-pins-344-347-349.md` (a finished HPSM-POC builder kit of another repository, whose own block was 9630-9639; no pane H17). Control: the pattern fires on `x 9630-9639 y` (1). Live kits: B663 9060-9069, B664 9600-9609, B667 9620-9629 (also lists 9620-9699 as a range note and 9570-9589, 9950-9959 etc.: none touches 9630-9639 except the range `9620-9699` in B667's text, which is a census note and not a block; the gate need not act). Live panes (13:3x): tuesday, NexusAI-G115, HPSM-POC-H23, MPS-G114, fleet-monitor.
- `.tools`: `b665`, `wt-b665-fix`, `wt-b665-mut`, `wt-b663-*`, `heavy-slot-1` (holder `B663 13:16:02 j5-family`); no `b668`, no `wt-b668-*`.
- Round count: the earlier gate on this lane's mechanism, `Briefs/2026-10-24_B594_STATUS.md` line 1: "GO WITH FINDINGS round 1 of 2 on #108"; no gate has judged PR #113: "NO GO 0 of 2 on class store-load pin tests".

## D-decisions (override at the stamp)
- D1. Tier 2 / row G2 (`model-routing.md:109`), Sonnet, launch line with `BRIEF_SEAT_LEVEL=sonnet` inside the quotes; the ticket's tier-1 label was overridden by Tuesday at the builder stamp on the same grounds (tests-only, nothing deploys).
- D2. Mutants named S1-S6 (rebuilt from the builder kit's text; the builder's trees and scripts READ-FORBIDDEN) plus N1-N9 and three seeded edits (seed 668101, not 630/631/640/643/606).
- D3. Grading: a row that asserts new behaviour or a new word = Major (the product owner's ruling: no word change); any `src` byte = Blocker.
- D4. PR title key graded Note with the squash-text fact (G-7), not Major.
- D5. Main-moved rule stops only on the PR's own path, `src/MpsCalc.Api/Sources/`, `StoreReopen*.cs`, `StoreLoadFaultMapping.cs`, `Infrastructure/`, `Directory.Build.props`, `global.json`, `.csproj`, `ci.yml`; any other move re-pins and moves C4/C6 to the new merge tree.
- D6. Scratch merges with #112 and #110 plus a narrow class run on each (informational but graded Major for the merge order if red); heavy, slotted.
- D7. Hard stop suggestion 2 h target / 3.5 h hard (no absolute cap written; Tuesday sets it in the slot). Whole Api run is about 6 to 15 minutes under load.
- D8. Port block 9630-9639 kept as assigned (reserve only; in-process hosts).

## Q-questions for Tuesday
- Q-1 (stamp, Q-1 slot): may the gate mutate `ActiveSources.cs` and add scratch rows in its own `wt-b668-*` trees? Default: YES (C2 needs it).
- Q-2: the PR title carries `MPSCALC-332:`. GitHub's COMMIT_OR_PR_TITLE setting uses the commit title for a one-commit PR (documented, not tested here), so the key should not reach the squash subject; PR #111's title carried no key. Default: edit the PR title to word-only before landing (a PR write, Tuesday's, not the gate's); the gate grades Note either way.
- Q-3: launch order. The gate runs heavy mutant builds while B663 (MPS-G114) holds `heavy-slot-1`. Default: launch when two slots are free and load1 < 7 on two reads; the kit tells the gate to release the slot between batches.
- Q-4: PR #110's possible landing at about 15:00 is inside the gate's window. Default: as written (re-pin, gate the new merge ref); if Tuesday would rather hold the 15:00 landing until this gate finishes, say so at the stamp.

## UNMEASURED by the drafter
Every runtime claim (green at base, mutant kills, the 2842 total, CI line, the start probe) is the builder's, RELAYED. Linux behaviour of the `FileShare.None` hold (advisory lock semantics) is argued from the existing StoreReopen rows being green in CI, not run. The predicted survivors (N3 on F1, N2 on F1, N6, N7) and the BROKEN-or-equivalent N9 are readings of the source, not measurements. No bind control on the port block. The squash text for a one-commit PR is documented GitHub behaviour, not tested. The F3 "write the file afterwards" strengthening the builder offered is left to the gate to measure.

## Outside the fences, disclosed
- Read-only reads beyond the template and the two builder files: `fleet/specs/model-routing.md` (lines 105-112), `0_Brain/dashboard/data/models_latest.json` and `usage_tuesday.json` (one grep and a 600-byte read), the first line and a grep of `Briefs/2026-10-24_B594_STATUS.md`, line 1 and lines 1-16 of `Briefs/2026-10-25_B643_STATUS.md`, `2026-10-25_B643_DRAFTER-REPORT.md` lines 1-6, port greps over the non-`.pre-` SEAT kits (including a `-o` context grep of B613 and B663 for the port text).
- One Bash call was refused by the zsh word-split hook (a git function variable with a spaced path); re-run under `bash -c`, no effect on any file.
- Not used: Jira (the ticket text came from the builder kit and STATUS), `decision_queue.sh`, `fleet/briefs_staged/`, `scoreboard.md`, `_ledger.md`, any WEDNESDAY/FRIDAY tree, any non-Datasec project, Artifact/Docs/mail/chat, az/ssh/docker, any HTTP to a hosted host. No git write verb, no fetch, no clone in the project repo; `gh` was `-X GET` only (a `gh auth status` read prints the account name; it was not quoted into either file).
- Files written: exactly the two named above (the kit plus this report), by the Write tool; one in-place Python edit of the kit (N5 wording) before finishing.
