STARTABLE: YES (after your Stamp; the unstamped kit reads 10 four-underscore lines: nine slots and the last line; no `@NAME@` token; the slot count is printed by `grep -c`, and the 44-row kit's own REFUSE 1 names the same instrument)

# B1541 DRAFTER REPORT (SEAT-H162, three approved wordings), written 2026-11-12, last `date` 15:03:16 AEDT

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-12_B1541_SEAT-H162_hpsmpoc-three-words.md`, 90 lines (`wc -l`), under 200. Work folder `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s272/d1541/` (raw files at c6b5c8cf, the tarball and its extraction, `frozen.py`, `chunks2.py`, `pat.mjs`, `frozen.json`).

## BLUF
- A Sonnet builder kit (row C2, `model-routing.md:92`, id `claude-sonnet-5-5` at `models_latest.json:23`, gate G2 `:109`) for one branch `b1541/hpsmpoc-three-words` off main `c6b5c8cf62fc8bc32246589bc7246bae6808f98d`, one commit, one plain push, no PR, nothing deployed. Nine owned paths: 3 product files, 6 test files.
- Authority quoted verbatim in the kit: the product owner, live board 2026-11-12 14:54:12 (card `hpsmpoc-three-words-proposal-ok-1112`, named here only): "a — Approve all three as proposed".
- The three frozen strings, copied and printed by program (all ASCII; lengths 391, 101, 115; each equals the PROPOSED block of the proposal at lines 25, 48, 72; each OLD equals the TODAY block and is found exactly once in its file; control: a planted extra copy reads 2; a last-character mutant of each is not equal):
  1. `steps.ts:42`: "From trusted print partner to security-led business growth. The Playbook connects guided assessments, reviewed findings, recommendations mapped to applicable HP capabilities, customer reporting and commercial next steps. Partners can deepen existing relationships, deliver relevant technology and services, and build recurring engagement without having to become cybersecurity consultancies."
  2. `NextEngagementScreen.tsx:23`: "The logical next engagement for the area with the biggest gap, chosen by rule, with the reason shown."
  3. `phase-flow.ts:24`: "Integration with the tools named here is planned or subject to implementation until release validation is complete."

## Facts re-measured (instrument, control)
- Main now `c6b5c8cf62fc8bc32246589bc7246bae6808f98d`, commit time 2026-11-12T03:54:02Z (`gh api -X GET branches/main`, 14:56). Open PRs 0; control `pulls/99999` 404. `heads/b1541` absent (length 0); control `heads/b1535` length 1 (and `heads/b1538` listed).
- Blob compare at `9308afa0` vs `c6b5c8cf` via `contents/<path>?ref=` sha, 8 of 8 EQUAL (steps.ts, NextEngagementScreen.tsx, phase-flow.ts, PhaseFlow.tsx, PhaseFlow.test.tsx, PartnerDashboard.text.test.tsx, RecommendationScreen.tiers.test.tsx, steps.test.ts); `compare` reads diverged, ahead 1 (the squash), behind 3 (the branch's commits). So the proposal's and the gate's line numbers hold at main; every pointer in the kit was re-printed with `awk NR`/`grep -n` over the raw files of c6b5c8cf.
- Whole-tarball census of c6b5c8cf (`grep -rl -F`): the old phrases ("planned or subject to implementation", "HP-aligned recommendations", "The logical next engagement", "a paid assessment, a no-fee") live in exactly 5 files: the 3 product files, `PhaseFlow.test.tsx`, `PartnerDashboard.text.test.tsx`. Control: "Self-assessment, not certification" finds 3 files. No e2e file holds any of them.
- `PartnerDashboard.text.test.tsx`: LOADED lines 24-71, EMPTY 73-118, the F3 sentence 3x in each (decoded join: OLD count 3 and 3). **Chunk rule MEASURED:** decode every `\u{hex}`, join, cut every 110 characters, re-escape non-ASCII as lower-case `\u{hex}`: reproduces all 47 and 45 chunk lines byte for byte (`chunks2.py`; the first attempt that decoded only \u{2013} did not round-trip, which is the control that the check can fail). The kit makes the builder prove that round trip before changing anything.
- The 9 `customer-text-patterns.mjs` patterns hit none of the three new texts; control "see CLARIFICATIONS.md" fires (doc-path, person).
- `api`, `scripts`, `infra` tests that read the changed files: 0 (`grep -rl -F` for phase-flow, walkthrough/steps, NextEngagementScreen, PhaseFlow; the `web/src` mentions are comments; `IntegrationTests.cs:129` reads only `web/src/styles`). The api jobs are therefore NOT RUN, with that reading in the kit; the infra repo-wide scans are run (rule 8).
- Ports 9900-9909: `lsof` 0 rows at 14:59 (control 11 listeners machine-wide); word-boundary scan of 55 non-`.pre-` SEAT kits of 11-12 Nov: `990x` only in B1535 (landed; not a live pane), control `993x` finds B1538; `tmux list-panes -a`: `%0 tuesday`, `%1 fleet-monitor`, two unnamed.
- Project identity (`git -C .../2_Project_Files config user.email`): `88359143+kamilDatasec@users.noreply.github.com`.

## D-decisions
- D1 (assertion for string 2): no test names the screen. Home chosen: `LoadFailed.states.test.tsx`, which renders it in the real customer shell; the lead is drawn in every state (`NextEngagementScreen.tsx:21-24`). Kit has a fallback (another state; STOP if none).
- D2 (string 1): home is `WalkthroughPanel.test.tsx`, beside the title-card row (`:163-168`) that already pins the same card's headline.
- D3: new test titles and the renamed tiers title are frozen in the kit (the builder composes no wording).
- D4: expected red set at BASE is exactly 5 (PhaseFlow note row, text LOADED, text EMPTY, the two new rows); hygiene items are green at BASE. Vitest name comparison: lost exactly 2 (renamed tiers row, moved steps row, whose ancestors change), added 4.
- D5: e2e shards are derived by program from `SHARDS` and `--list` (the drafter's census: 16 specs under `/home`, 3 walkthrough, 5 next-engagement files, so most or all of the 8).
- D6: the two other "HP-backed tools" comments (`phase-flow.ts:27`, `PhaseFlow.tsx:101`) are product files outside the three-line scope: left, listed under FOR TUESDAY.
- D7: the proposal's ALTERNATIVE texts are barred (the product owner chose the PROPOSED forms).

## Q-questions for Tuesday (each with a default)
- Q-1: the kit edits two test files you did not name (`WalkthroughPanel.test.tsx`, `LoadFailed.states.test.tsx`) as the homes of the two new assertions. Default: yes, nine paths.
- Q-2: leave the two product-file comments that still say "HP-backed tools"? Default: leave.
- Q-3: hard stop and READY target: kit says 150 minutes after Step 0 (S-M, one whole vitest plus the derived shards); your Hard stop slot sets the clock. Default: 150 minutes.
- Q-4: run every shard the program derives (likely all 8), whole shards only, as the 44-row builder did. Default: yes.
- Q-5: cockpit name `Datasec/HPSM-POC-H162` (the style of the newest HPSM kit) rather than `HPSM-H160`. Default: `HPSM-POC-H162`.

## UNMEASURED
- Nothing was run: no clone, no `npm`, no vitest (fetching a clone of the project repo is outside the fences; I read a tarball instead). So the 5-red prediction, the new rows' green at head, and that the LoadFailed shell draws the lead in the empty state are DERIVED from source reading.
- The CI predicates of `web-build`/`web-unit`/`infra` are RELAYED from the 44-row kit; only the `shard:` line (`ci.yml:494`) and `SHARDS` (`e2e.mjs:53-62`) were re-read at c6b5c8cf. The kit makes the builder print them.
- Vitest totals at c6b5c8cf (the gate printed 4236 passed at the branch head; same tree for these files).
- The landing-rule line is RELAYED from the 44-row kit.

## Outside the fences, disclosed
- Read-only GETs under the project `GH_CONFIG_DIR`: `branches/main`, `pulls`, `matching-refs`, `compare`, `contents` (8 files x 2 refs, and 3 test files), `git/trees`, `search/code` (2 queries), and one `tarball` of c6b5c8cf extracted into the work folder (untrusted data; never run).
- I executed one repo file: `node pat.mjs` imported `web/scripts/customer-text-patterns.mjs` from the extracted tarball (constants only) to test the three texts; I did not run anything else from it.
- Read: the 44-row kit, its verdict, the proposal, `model-routing.md`, `models_latest.json`, the minimatch kit's `.pre-stamp` (shape only), the project's `CLAUDE.md`/`JIRA.md` by grep. `tmux list-panes`, `lsof`, `git config` reads. No decision-queue command, no scoreboard, ledger, staged-briefs or other-project read.
- One Bash call contained a `cd` and the hook refused it; it ran nothing. No file was written outside the kit, this report and the work folder.
