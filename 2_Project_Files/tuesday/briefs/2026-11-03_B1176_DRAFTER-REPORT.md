STARTABLE: YES (after Tuesday's stamp; see Q-1 to Q-4 and the main-moved check at stamp time)

# B1176 drafter report (SEAT-M84, MPSCALC-374), drafted 04:21 to 04:28 AEDT 2026-11-03 by `date`

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-03_B1176_SEAT-M84_mps-374-contract-sync-advice.md` (9 slot lines of four underscores, the template's count; 0 non-ASCII bytes; last line `READ-WHOLE-BY-TUESDAY: ____`).

## BLUF
One file, `web/src/api/contract.sync.test.ts`: the `HOW_TO_SYNC` constant (`:19-22`) gets a condition on its first advice and two added sentences (unchanged contract: sync at `HEAD`; missing install: `npm ci`), plus one new text-pinning row. Model C2 `:92`, gate G2 `:109`, launch `BRIEF_SEAT_LEVEL=sonnet`, pane `Datasec/MPS-M84`, branch `b1176/mps-374-contract-sync-advice` from main `314b53f6`. Tuesday's word ruling is stated in the kit as the coordinator's, with the project's own property for it (`CLARIFICATIONS.md:959-960`) and a STOP if the text would reach any user or operator surface.

## Facts re-measured (instrument; control)
- Main = `314b53f6ddaaa9005e1015479882ff35e33b631e` at 04:21 (`gh api -X GET git/ref/heads/main` and `ls-remote` agree; one parent). Open PRs 120, 121, each `web/package-lock.json` only (`pulls/<n>/files`).
- The pin's object is NOT in the local `2_Project_Files` (`cat-file -t` fails; HEAD `7f6ca4c`, 2026-10-01); `b7eebb47` is. The kit therefore has the seat do ONE fetch of main by URL under `.tools/.git-lock` (the template's own fallback).
- Test file blob `a6d8e137...` = `git hash-object` of the raw bytes fetched = the API `.sha`; 76 lines; `HOW_TO_SYNC` `:19-22`, used `:33`, `:41`, `:64`; rows `:47`, `:56`. `grep -c -F HOW_TO_SYNC` prints 4 (decl plus three uses), `npm ci` 0, `how-to-fix` 0 (positive control is the 4). Script blob `18be1ecc...` (38 lines; `:17-19` reads a committed ref, `:31` runs npx). `ci.yml` blob `212b0da1...`: `:46`, `:58`, `:61-63`, `:66`. `package.json` blob `f74032cf...`: `:12`, `:14`, `:16-18`, `:42` pins openapi-typescript 7.13.0.
- The new constant text was run through node against the four row strings: 4 of 4 contain-checks true (control: the pin's text has none of the new pieces).
- Code search (`gh api -X GET search/code`) for the phrase and for `HOW_TO_SYNC`: total_count 1 each, only the test file. The index can lag; the kit has the seat run `git grep` at Step 4a.
- 12 origin heads match `^b1(0[89]|1)[0-9]` of 174 heads; compare against the pin for the sync/generated filter: b1083, b1093, b1146 (generated copies, old), b1125 (`contract.sync.test.ts`, landed as #147, squash `80203089`, diverged ahead 1 behind 5); b1164, b1169 and the rest empty. Origin `heads/b1176` length 0 (control `heads/b1093` 1); local `b1176*` 0; `.tools/b1176` absent (control `.tools/b1125` exists).
- Panes: `tuesday`, `Datasec/Security-Composer-G304`, `Datasec/MPS-G305`, `Datasec/NexusAI-G303`, `fleet-monitor`; no MPS-M84. Today's SEAT kits naming `contract.sync.test.ts`: B1162 (`:64`), B1165 (`:53`, `:57`), finished seats.
- Ports: none needed (vitest binds ephemeral loopback); `lsof` listeners `*:49152 *:5000 *:59869 *:7000 127.0.0.1:49166/:49168/:49171`, none ours. Word-boundary scan of today's SEAT kits for a port block: none assigned, none to scan.
- Machine 04:22-04:23: load1 5.56 then 3.89; `df -g` 249 GiB free; `.tools/*/heavy.lock` and `light.lock`: no match. Node 24: `.tools/b1125/node24` and `.tools/b1146/node24` both v24.21.0. `gh auth status` under the project's config: `kamilDatasec` active.
- Jira (own reader copy in the session scratchpad, output redirected there, in-process credentials): MPSCALC-374 Backlog, 0 comments, desc 2064 chars, updated 2026-11-02T22:43 AEDT; control MPSCALC-363 Done, comments=1.
- Round: B1143 (neighbour class "web: generated contract copies equal the contract") GO WITH FINDINGS round 1 of 2, NO GO 0; this class is new, ROUND 1 OF 2, NO GO 0 before.

## D-decisions (in the kit)
D-1 one shared constant with three conditioned pieces (not per-row texts). D-2 `HEAD` as the ref for an unchanged contract (the script reads a committed ref; Step 4c measures that following the advice turns the contract tests green, STOP otherwise). D-3 the existing first piece is edited by its first words (`To fix:` becomes `If <contract> changed,`), so the diff removes 2 lines, not add-only. D-4 the committed row pins text; real-failure proof (S1 contract changed, S2 generator output differs, S3 module moved aside) is scratch-only before and after. D-5 gate G2. D-6 no timeout, config or lockfile change.

## Q for Tuesday (each with a default)
- Q-1 Wording: the three pieces are my draft of the ticket's done-when, written verbatim into the kit so the seat does not freelance. Default: accept as written (seat STOPs if Step 4c shows the `HEAD` advice leaves the contract tests red). Alternative: Tuesday rewrites them before stamp.
- Q-2 Heavy slot: the kit adds to the template's seat-local lock a condition that no other seat's `heavy.lock` or `light.lock` exists (the rule G305's kit B1174 uses), so the web seat and the dotnet gate never run heavy together. Default: keep. Cost: either side can wait; nothing deadlocks because neither holds a lock while waiting.
- Q-3 Hard stop: the template capped the hard stop at 06:00 on its own launch day; this kit has no calendar cap (target READY = Step 0 + 120 minutes, HARD STOP = + 240). Default: no cap; Tuesday may write one in the Stamp slot.
- Q-4 Row choice: the committed row asserts the text only. Default: yes (counts as red-first by C-83, `CLARIFICATIONS.md:2214-2218`). A committed row that really breaks `node_modules` or the snapshot was rejected as unsafe for a shared suite.
- Q-5 Conflicting open work: main is allowed to move on `package-lock.json` (PRs #120/#121 landing) without a STOP; any move on the test file, the script, `package.json`, `generated/` or `ci.yml` is a STOP. Default: keep.

## UNMEASURED
- Whether the sync at `HEAD` leaves only header lines changed in the generated copies and keeps `contract.test.ts` green (read from `sync-contract.mjs:17-37` and `contract.test.ts:13-14`, not run; the kit makes it Step 4c).
- Whether `npm run lint` accepts the longer string lines (the file already has a 157-character line at `:33`; no line-length rule was read).
- Any other ticket owning this text beyond the ticket's own search list; the code-search index lag for other files carrying the advice.
- The edit's exact added-line count (kit says 15 added, 2 removed, by the drafter's count of the planned text, not by a diff).
- Hosted CI and CodeQL: NOT RUN by the seat. Whether the whole web suite is green at the pin under load (MPSCALC-369 class): Step 3.

## Outside-the-fences disclosure
- Wrote the two files only, plus scratch files in the session scratchpad (a copy of the Jira reader with its output path re-pointed, fetched raw copies of the test file, script, package.json and ci.yml at the pin, a node check). A scratchpad file named `ci.yml` already existed there from earlier and held different content (679 lines, blob `0176b491...`); I measured `ci.yml` again into `ci2.yml` (blob `212b0da1...` = the API sha) and used that.
- Read `CLARIFICATIONS.md` and the B1143 STATUS in the project's own `1_Project_Definition/`, and the B1174, B1162, B1165 kits (readable claims). Did not run `decision_queue.sh`; read no card, no staged brief, no scoreboard, no ledger, no WEDNESDAY/FRIDAY tree. Read `.tools/b1125/heavy.sh` and `jira_read.py` (named copy sources) and listed `.tools` for lock files and node24 versions. No git write, fetch, checkout or worktree in any project repo; `gh api -X GET` only, under the project's `GH_CONFIG_DIR`; no HTTP to a hosted or production host. No `cd`.
- One zsh slip while drafting: `$M:web/...` parsed as a modifier, so a first `git show` failed harmlessly; the later reads use the API raw contents.
