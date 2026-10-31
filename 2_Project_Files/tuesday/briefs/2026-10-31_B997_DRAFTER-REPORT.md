STARTABLE: YES

# B997 drafter report (round-2 tier-1 gate kit, SEAT-G244, PR #266), drafted 2026-10-31 19:3x AEDT

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-31_B997_SEAT-G244_hpsmpoc-266-round2-gate-tier1.md` (48 lines, long paragraphs, in the shape of the B994 gate kit; last line `READ-WHOLE-BY-TUESDAY: ____`).

## BLUF
Startable now. PR #266 is open, head `7490fb36...`, main unmoved at `d0eff4ca...`, `mergeable_state` clean, 20 of 20 check-runs success. The kit has 8 four-underscore slot lines (S1-S7 and the last line), 0 non-ASCII, no person's name, no card id. Slot count 7 plus the last line. Port block 9460-9469. A NO GO here is the cap (model-routing.md:111) and the kit says so in the header, the verdict rules and FOR TUESDAY.

## Facts re-measured (instrument, control)
- `ls-remote` 19:30:07: branch = `refs/pull/266/head` = `7490fb362edb10b932baf9779a77912b9d7fad77`; main `d0eff4ca637b8959dd205adc0b77e8111b60280a`; `refs/pull/266/merge` now `69d62e71ff00300c87bce1dc4e2ec3f775d6817c` (was fec4a5a7 in round 1). Instrument: `git ls-remote`; control: the same call returned all four refs asked for.
- `gh api -X GET pulls/266`: open, draft false, mergeable true, `mergeable_state` clean, commits 3, changed_files 9, +396 -32, title unchanged ("Wait out a database wake: ..."). Sum check by hand from `pulls/266/files`: additions 54+19+2+75+1+26+6+209+4 = 396, deletions 3+13+2+0+1+11+0+0+2 = 32 (agrees; 623-227 = 396 and 34-2 = 32 agree with round 1's 13-path figures).
- `pulls/266/commits`: `136265f9` Web, `a9025f2f` API, `7490fb36` `Revert "API: ..."`. The web commit message was read whole.
- Check-runs of `7490fb36` (`--paginate`, sorted): 20 rows, all completed success, including CodeQL, four Analyze, `api on SQL Server` x3, five e2e, web build, web unit, infra, secrets, dependency review. Not re-run by me; the kit makes the gate read them LAST.
- PR body re-read: it is STILL the round-1 text (Two commits, 13 files +623 -34, "Commit 2, API", "no longer fails", "waits about 101 s", "API 3828 -> 3838"). The kit's C5 hands the gate the job of listing every false sentence; Tuesday corrects the body before landing.
- Open PRs: `pulls?state=open` printed 266 only.
- Model rows: `grep -n` of model-routing.md printed G1 at line 108 and G-cap at line 111; `models_latest.json` line 17 `"model_id": "claude-opus-5-5"` (Opus level).
- Landing rule: `CLARIFICATIONS.md:138` matches `squash-merged head-pinned`; the kit tells the seat to re-grep for the current line.
- Ports: `lsof -nP -iTCP:9460-9469 -sTCP:LISTEN | wc -l` = 0; all-TCP listeners 13 (the instrument answers). Word-boundary scan `\b946[0-9]\b` over the 84 non-`.pre-` SEAT kits dated 30-31 Oct: 0 hits; control `\b944[0-9]\b` printed the B995 kit; earlier control `\b959[0-9]\b` printed the B977 and B994 kits. Other candidates seen with hits: 9510-9580 blocks (B-numbers earlier; not used). Live panes by `tmux list-panes -a`: tuesday, Datasec/Security-Composer-R99, fleet-monitor (no kit claims 9460).
- Round count (read from B994's STATUS line 1, not by re-running the loop): B994 = NO GO round 1 of 2 on this class and PR; B995 STATUS line 1 begins `PROGRESS`, so it is not a verdict. The kit makes the gate run the loop and write "NO GO 1 of 2 ... before this gate (B994); this is round 2 of 2, the cap".

## D-decisions
- D-1 The net change is web-only, so I cut the round-1 BeginTransaction census, idempotency table, SQL Server runtime row and the API suite. They are replaced by the byte-equal `api/` subtree proof and the tree-cancellation proof (`7490fb36^{tree}` = `136265f9^{tree}`), which I added as THE check in C1(b).
- D-2 The EF check is kept, but as the EF DEFAULT read from the loaded 10.0.12 package, with a control (a scratch context at 10 retries / 15 s must print about 101 s), because the key property depends on it.
- D-3 The key property (C4) has its own stub: each API request has its own schedule from arrival, optional `lag` for per-try login cost, rows S1-S9, and three control plants K1-K3. K3 (schedule anchored on the first arrival) is new: it is the plant that removes the "fresh request per re-ask" property itself. K1's expected shape follows what the builder actually measured (500 at about 0 s, 1 arrival, since a 500 is passed through and never re-asked), not the builder kit's mistaken "504 at 90 s" prediction; the kit says to report it and not to fit it.
- D-4 Narrow margin S2: my arithmetic from the builder's schedule (r=1.1 offset 28.6 s after attempt 2 arrives at 30 s = 58.6 s) says lag 2 pushes the answer to 60.6 s, past the BFF's 60 s cut; the third attempt then arrives at 60 s, after the wake, and answers at 60+lag (about 62-63 s for lag 2, 66-67 s for lag 6). These are hypotheses written into the kit as predictions for the gate to test.
- D-5 Shortened target/hard stop: 110 / 160 minutes (round 1 was 150 / 210) because there is no API suite, no transaction census and no SQL Server leg locally.
- D-6 SQL Server evidence for B994-1 is read from CI: the TRX duration of the import fail-path test at the new head (expect about 176 s, main 175.7 s, round 1 310.5 s), plus both parts and the aggregate success.
- D-7 Squash text describes only the web change; the kit's check forbids any mention of the API retry.
- D-8 The kit's "READ-FORBIDDEN" list covers `.tools/b992`, `b994`, `b995` and their worktrees (round-1 precedent for B992 trees); STATUS/evidence text only.

## Q-questions for Tuesday (each with a default)
- Q-1 Port block 9460-9469 (free, scanned). Default: yes.
- Q-2 Target 110 and hard stop 160 minutes after Step 0. Default: yes.
- Q-3 Keep the three e2e specs (cut first under load)? Default: yes, cut-able; they were green x3 in round 1 and the web tree is byte-equal.
- Q-4 Grade of the stale `bff.ts` comment ("Every other read keeps 10 s.", N-4). Default: Note, not edited.
- Q-5 Launch timing: launch_when_cool at load1 below 7; the only live seat beside the gate is Datasec/Security-Composer-R99 (another project, load only). Default: yes.

## UNMEASURED
- Whether the PR body or title changes between this draft and the launch (Tuesday corrects the body before landing; the gate reads it as it stands).
- The kit's predictions (S1-S9 times, 29 of 261 red at the pin, 427 limit rows, 3689 of 252 files) are hypotheses carried from B994/B995, not re-measured by me.
- Whether `.tools/b997*` or `wt-b997-*` exist (not checked: the gate's own REFUSE does it).
- The check-run states were read once at 19:30; CodeQL alerts were not read by me (the gate reads them LAST).
- Hosted close propagation and Kestrel RequestAborted: named as UNMEASURED in the kit.

## Outside-the-fences disclosure
Read-only throughout. Files written: the two B997 files only. Read: DRAFTER_RULES.md, the B994 kit and STATUS, the B995 kit and STATUS, the routing and models files (grep/sed), CLARIFICATIONS.md (grep -n only), other briefs by `ls`/`grep -l` for port scans, `ls-remote` on the project repo, `gh api -X GET` under the project `GH_CONFIG_DIR` (pulls, pulls/266/commits, pulls/266/files, commits/<sha> message, check-runs). No fetch, no git write, no Jira, no decision-queue, no Artifact/Docs/mail, no HTTP to any hosted host, no `cd`. Two Bash calls were refused/failed by hooks or a nonexistent filter (an unquoted `====` separator; a later `ls` grep returned rc 1 with no match) and re-run without the offending words; nothing ran from the refused call.
