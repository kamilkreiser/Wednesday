STARTABLE: YES

# B752 DRAFTER REPORT (kit: 2026-10-26_B752_SEAT-G153_mps-176-feedback-triage-gate-tier1.md, 91 lines)

Drafted 2026-10-26 19:0x AEDT by the read-only kit drafter (Sonnet 5.5). Read-only outside the two files; no Artifact, Docs, mail, chat, decision-queue or publish tool; no git write; no fetch; no HTTP to a hosted host.

## BLUF
Kit is complete for a tier-1 Opus gate of `b744/mps-feedback-triage-my-feedback` @ `6896aa43`, round 1 of 2 on its class (no earlier gate verdict exists for MPSCALC-176). B752 and G153 are free. Ports 9440-9449 are free by both instruments. The kit has 8 four-underscore lines (7 stamp slots + last line); no at-sign-capitals pattern; 0 non-ASCII bytes; no person name; no decision-card id.

## Uniqueness checks (B752 / G153)
- Word-boundary scan `(^|[^0-9A-Za-z])(B752|G153)([^0-9A-Za-z]|$)` over all `tuesday/briefs/*.md` and `Briefs/*.md` of the MPS project: 0 files. Control: the same scan for `B748` listed 3 files. (A looser substring scan hit four B562 evidence jsonl files by hash text; not a use of the id.)
- `ls` of `tuesday/briefs` for `B752|G153`: only my two files after writing. No MPS STATUS file `B752_STATUS`.
- Live panes (`tmux list-panes -a -F '#{pane_id} #{@cockpit_name}'` 19:04): tuesday, MPS-R48, NexusAI-G152, HPSM-POC-D32, MPS-G151, Security-Composer-J22, fleet-monitor. No MPS-G153, no MPS-M32.
- `.tools/b752` and `.tools/wt-b752-base`: no such file (control: `.tools/b744` exists).

## Facts re-measured with instruments
- Branch ref: `ls-remote` `b744/mps-feedback-triage-my-feedback` = `6896aa430f37c6f43853d4e1afc3b4f26a6b41fe`; main = `1137f11962c9adbee84c119fe7dd2f545bd4a42a`; `b745/mps-walk-caps` = `d259ae1d...`. `gh compare 2e7f9d8a...6896aa43`: ahead 1, behind 0, 18 files; additions sum 1546, deletions sum 52 (arithmetic by hand from the per-file list; matches the relay). `compare 1137f119...6896aa43`: ahead 1, behind 2, diverged.
- Main's 3 moved paths vs the 18: `comm -12` = 0 (control: the 18 vs themselves = 18). b745's 2 paths vs the 18 = 0. #120/#121 = `web/package-lock.json` only.
- No PR for the branch (`pulls?state=open&head=...` length 0), check-runs total 0, code-scanning analyses length 0. Main's 8 check-runs at `1137f119` all completed success (so the "CI paused" relay is stale; kit tells the gate to state what the runs read, not to rely on a pause).
- ci.yml at `1137f119` read with `cat -n`: dotnet job `:30`, build `:42`, test `:43`; web job `:45`, npm ci/lint/test `:61-63`, build+check-bundle `:66`; python `:68`; package `:93`. Pass predicates written into the kit. `check-bundle.mjs` header read: `--control` exists, used in C6.
- Model: routing rows read with `sed -n 108,112p`: G1 `:108`, G2 `:109`, G-cap `:111` (positive control: the case-insensitive grep printed the same lines). Opus id `claude-opus-5-5` from `models_latest.json`.
- Round count: first lines of 54 `Briefs/*_STATUS.md` containing `GATE VERDICT`; 2 matched `176|b744|triage|my feedback` (B318, B347) and both are digits inside test counts ("1769"), verified by printing the matched fragment; control: B748's first line matches. So NO GO 0 of 2; round 1 of 2.
- Register: path in the builder kit, `ls -l` 10541 bytes, read whole (46 rows).
- Landing source: `CLARIFICATIONS.md:809` and `:854` printed (both contain "squash with the head pinned (`--match-head-commit`, the MPS convention ...)"); `CLAUDE.md:50-52` printed (it names the coordinator as a stale name; kit says so without the name). Repo settings: `squash_merge_commit_title` COMMIT_OR_PR_TITLE, `squash_merge_commit_message` COMMIT_MESSAGES.
- Heavy slots: `heavy-slot-1` holder `B748 18:56:18 j4b`; slots 2 and 3 absent. Load 9.02 8.49 8.50 (heavy).
- Ports scan (instrument: python word-boundary regex over the 142 non-`.pre-` SEAT kits of 2026-10-25 and 2026-10-26, counting kits per decade 9000-9999): zero-claim decades were 9040, 9070, 9110, 9130, 9150, 9180, 9190, 9260, 9280, 9290, 9370, 9380, 9410, 9440-9470, 9490. Chose 9440-9449. `lsof -nP -iTCP:9440-9449 -sTCP:LISTEN` printed nothing rc 1; control: a python socket on 127.0.0.1:9441 was listed, then freed, same lsof printed nothing. Pattern control: `940x` scan fired on 20 briefs. A looser scan over all briefs found `944x` in eight 24 Oct files (finished lanes) and a mention in B742's drafter report saying 9440 had 0 hits. Live blocks avoided: B748 9750-9759, B750 9870-9879, B749 9670-9679, B751 none.
- Diff content read (scratch file, 2085 lines): DTOs, endpoints, store, log, EntraAuthTests, the admin panel, the dialog, words.ts. The two new Api/web test files and `MyFeedbackPanel.tsx`, `api.ts`, `stub.ts` were NOT read in the drafter pass (kit marks them for the gate).

## D-decisions
- D1 Opus at tier 1 (G1) because the diff adds an authenticated surface with a visibility property, and the builder was Sonnet.
- D2 Ten checks (C1-C10), with C2 (words) separate from the technical strings, C3 (auth on every op, role, order) and C4 (My feedback isolation, with the Entra-mode same-display-name plant the builder admitted it did not build) as the top priority.
- D3 Words are graded as class W "FOR THE PRODUCT OWNER": a string outside the register is never fixed by the gate; judgement calls are listed, not graded as defects. NEW TECHNICAL STRINGS are a separate table, Note at most.
- D4 The gate builds its own word extractor before reading the builder's `wordcheck.py`, with controls (planted new word flagged, planted register word not, one-character change flagged, base file set finds only base words).
- D5 Web is in scope for CI (node, `npm ci` into a seat-local cache, lint, test, Entra build + bundle check + `--control` on a stub build). Node is v26.8.1 here vs CI 24 (stated). e2e `b47` may run once on port 9440 with installed Chrome, else NOT TESTED; `b83` NOT TESTED.
- D6 Best verdict token without a PR is GO WITH FOLLOW-UPS conditional (CodeQL NOT SCANNED), as in B748.
- D7 Builder trees `.tools/b744`, `wt-b744-*` and the builder's scripts are read-forbidden for the mutant method, same rule as B748 applied to b745.
- D8 Heavy-slot, load, heartbeat and quarantine rules copied from B748's LOAD section with B752 names.
- D9 Hard stop: 180 min target, 4 h hard, never later than 23:30 AEDT, same as B748; Tuesday sets the window.

## Questions for Tuesday (each with a default)
- Q-1 May the gate add scratch rows, probe classes, weak copies and mutants in `.tools/wt-b752-mut`? Default: YES (C3-C5, C7 depend on it).
- Q-2 Should the docs prose (29 lines in `API.md`, openapi descriptions) go to the product owner as a word pack before the PR lands? Default: the gate lists it apart and takes no position; you decide at the landing (as your B744 stamp said).
- Q-3 Round count: kit states NO GO 0 of 2 (round 1 of 2) from the first-line scan. Default: accept.
- Q-4 Ports 9440-9449 (free by lsof and by the scan). Default: accept; confirm at stamp.
- Q-5 The builder kit's NEW TECHNICAL STRINGS table lists 13 entries; the gate re-extracts its own. Default: Note at most for any difference.
- Q-6 Launch window: MPS-G151 (B748) holds heavy-slot-1 and load is 9. Default: launch_when_cool, one waiter, window to your choice (the gate may need most of 4 hours).
- Q-7 The B751 records kit (live) lists M32 and `heavy-slot-2` as live; both are gone (pane absent, slot absent at 19:04). Default: ignore; it is B751's own stale text.

## UNMEASURED
Nothing was built, run, mutated or probed. Not read by me: `FeedbackTriageTests.cs`, `FeedbackTriage.test.tsx`, `MyFeedback.test.tsx`, `MyFeedbackPanel.tsx`, `api.ts`, `stub.ts`, `CallerResolver.cs`, `Roles`, `QuoteEndpoints.Authorized` beyond its signature lines. Merged-tree test totals (Api 3075 etc.) are arithmetic from the B748 kit's relayed "+51", not measured. GitHub's single-commit squash message behaviour is documented behaviour, not measured here. Whether an Administrator acting as Seller lists the Seller's items on `mine` is unknown (the kit makes the gate measure it). I did not check whether 944x appears in non-SEAT kits written after 19:04.

## Outside-the-fences disclosure
- Wrote scratch files only in the session scratchpad (`b744.diff`, `mine18.txt`, `main3.txt`, `b745.txt`) besides my two outputs.
- Briefly ran a python socket on 127.0.0.1:9441 for 5 s as the lsof positive control (freed).
- Ran `for f in Briefs/*STATUS.md; do head -n 1` loops (read-only) in the MPS project folder.
- Read the other seats' kits only for port and uniqueness scans and the B751 kit's partition/live-seat lines (`B751` is a records kit of the same project; no WEDNESDAY, FRIDAY, ledger, scoreboard, staged briefs, decision queue or non-Datasec tree was read).
- One attempted Bash call containing `cd` was refused by the hook and re-issued without it; the early file-list command that included `ls ../` also listed `tuesday/` contents only.
- Hook advisories about case-sensitive grep appeared; the affected counts were either re-run with `-i` and a control or are not zero-claims.
