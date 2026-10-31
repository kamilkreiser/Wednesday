STARTABLE: YES

# B998 drafter report (round-3 builder kit, SEAT-H85, PR #266 GET-only), drafted 2026-11-01

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B998_SEAT-H85_hpsmpoc-266-round3-get-only.md` (56 lines, long paragraphs; last line `READ-WHOLE-BY-TUESDAY: ____`).

## BLUF
Startable. Head `7490fb36...`, main `d0eff4ca...` re-measured by `git ls-remote` (unmoved vs the B997 pins). The kit makes the read re-ask and the 30 s limit GET-only; HEAD goes back to main's generic 10 s and one call. Slot count: 8 slot lines plus the last line = 9 lines with the four-underscore pattern (`grep -c` printed 9; the REFUSE line writes the pattern split so it does not count itself). Non-ASCII 0. No person name, no card id in the kit (the words "card id" appear only inside prohibitions).

## Facts re-measured (instrument, control)
- `git --no-optional-locks ls-remote origin` branch `7490fb362edb10b932baf9779a77912b9d7fad77`, main `d0eff4ca637b8959dd205adc0b77e8111b60280a`. Control: both refs printed in one call. I did not re-read `pulls/266` (not needed for a kit; the seat re-measures).
- Source text read at the head by `git show 7490fb36:<path>`: readRetry.ts whole, bff.ts lines 135-215 (READ_TIMEOUT_MS block :141-146, upstreamTimeoutMs :198-206), the HEAD rows: bff.wake.test.ts :129-137 and :191, readRetry.test.ts :54-59, bff.timing.test.ts :51. `bff.test.ts`, `EngagementsList.wake`, `ApiNarrative.readRetry`, `formMeter.test.ts` have no `"HEAD"` literal (grep; the controls were the other files, which printed). Caveat: my first grep was case-insensitive and matched "headers"; the kit tells the seat to run the word-bounded form.
- Main's own `READS` already contained HEAD (B997 C1(d): `READS` byte-equal to main), so at main a HEAD was re-asked once in-process but never over HTTP (body-less 504). See Q-1.
- Model: model-routing.md C2 row is line 92 (sed 90-93 printed it); `models_latest.json` line 23 `"model_id": "claude-sonnet-5-5"`.
- Ports: `lsof -nP -iTCP:9470-9479 -sTCP:LISTEN | wc -l` = 0. Word-boundary scan `-w -E '947[0-9]'` over the `*B99[5-9]*` and `*B100*` kits: 0 hits (rc 1); an earlier wider scan `94[67][0-9]` over today's/yesterday's kits hit only the two B997 files (9460s block), so the instrument answers. Panes: tuesday and fleet-monitor only (no `Datasec/HPSM-POC-H85`). No `b998` trees under `.tools` (0).
- Round count: B997 is NO GO round 2 of 2 on the class; this kit is the product owner's extra last round (cited as "the product owner's 2026-11-01 round-cap ruling").

## D-decisions
- D-1 HEAD limit = main's generic 10 s (drop HEAD from the `if` entirely; it falls to `method !== "POST"`). Why: it is closest to main (zero HEAD difference at runtime, one call), the edit is the smallest (one line, `bff.ts` net +6 -0 vs main), and keeping 30 s would add a limit no read path uses.
- D-2 `readRetry.ts`: `READS` becomes `new Set(["GET"])`; the write guard line stays byte-equal and now also covers HEAD (one call). Alternative (leave `readRetry.ts` alone) would leave a dead HEAD re-ask in code and comments; the product owner asked for words to match.
- D-3 The new HEAD wake row models HTTP by stripping the body (`new Response(null, {...})`), the regression shape the gate named.
- D-4 Socket rows reuse the gate's stub, client and schedule from `.tools/b997/` as READ-AND-COPY prior work (HPSM-POC project tree, not forbidden); ports 9470-9479 (stub 9470, BFF 9471, control 9479).
- D-5 Target READY 75 / HARD STOP 110 minutes (one small edit, one suite, 90 s socket rows).
- D-6 Fence on option (b): the kit forbids any header on the BFF's 504 this round.

## Q-questions for Tuesday (each with a default)
- Q-1 Main's `READS` had HEAD, so in-process a HEAD at main was asked twice; GET-only makes it one call in-process too (over HTTP it was always one). Default: accept (the dead path is removed; HTTP behaviour equals main).
- Q-2 `bff.test.ts:154` row title says "everything else keeps 10 s" while its GET row expects 30_000 (B997 N-7), and `bff.ts:177` "Every other read keeps 10 s." (N-4) is stale. Default: leave both (the ruling said no other change); Tuesday may add them to the gate's Notes.
- Q-3 The PR body and the 136265f9 message still say "GET or HEAD" and the round-1 text. Default: Tuesday corrects the body at landing; the squash subject/body must say GET only (the new commit's message does not rewrite history).

## UNMEASURED
- Whether `.tools/b997/` still holds the scripts the kit names (not listed by me; `stub9460.py` was found by `find`; `client.mjs`, `c4b.sh`, `schedule.json`, `plants.py` come from the B997 STATUS file list).
- Whether the B995 worktree `.tools/wt-b995-fix` still has the branch checked out (the kit uses a new detached worktree, so no conflict either way).
- The exact shape of `world()`/`track()` in bff.wake.test.ts (only lines 125-215 read); the seat reads the file whole.

## Outside-the-fences disclosure
Read-only reads only: `git show`/`ls-remote` in the HPSM-POC repo, `sed`/`grep` of model-routing.md, models_latest.json, the B995 and B997 briefs/reports, the B997 STATUS file; one `tmux list-panes` and `lsof`. A first Bash call was refused by a hook (a `==` echo separator) and re-run. No card read, no `decision_queue.sh`, no mail, no write outside the two files.
