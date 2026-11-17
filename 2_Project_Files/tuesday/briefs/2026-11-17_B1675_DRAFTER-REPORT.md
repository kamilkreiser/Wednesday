STARTABLE: YES, after the Stamp; nothing waits on an answer (Q-1 to Q-3 have defaults). Main, the function, the anchor row and the expected result were re-measured at origin main 6c1aa32e; the one thing not run is the row inside vitest (no npm ci by the drafter, load about 8).

# B1675 drafter report (lane H-T, SEAT-H180, HPSMPOC-507), 2026-11-17

Clocks (`date`): start 21:49:20, port check 21:50:17, last 21:54:33 AEDT. Files: the kit (142 lines, longest line 1774 characters), the `.measured` sidecar (31 claims plus S01-S09), this report. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s287/d1675/` (Jira dump, GET helpers copied from the s286 sweep scratch, shallow clone at 6c1aa32e, `rowcheck.js`, branch list, kit list).

## Measured
- Origin main is `6c1aa32e` (#332, the `next` bump); open PRs 0; `b1675` refs 0. #332 touched only `web/package.json` and the lock, so the sweep's `b81793d1` lines still hold: block at test file line 454 to 569, `startingOwner` at `remediation-store.ts:58-72`, compare at :68, `OWNER_MAX` :18, `checkEntry` length check :45 (S02, S03, S05).
- The result, run under the project's own node24 (`v24.21.0`, ICU 78.3) on a copy of lines 58-72: 99 letters + U+D83D + `b` gives 100 units, last unit d83d, `b` not added, the file's `lone` regex TRUE; the opposite expectation (99 letters) is false, a length-99 expectation false; `checkEntry`'s length rule passes it (S04). This closes the ticket's "not run on the pinned Node version" for the function; the row itself is the seat's Step 3.
- The row: inserted before the row titled `starts empty when the first character alone is longer than the limit...` (occurs once, line 542); uses the block's own `lone`, `ownerOk`, `letters`, `longer`; ASCII, escape `\uD83D`; the decision is in the title ("pinned as it is"). Expected diff: 10 added lines, 0 deleted. The test file has 0 non-ASCII bytes and no row mentions "surrogate" (control: "grapheme" counts 2).
- e2e: 0 files in `web/e2e` import `remediation-store` (control: `browser-store` also 0, so the instrument is not blind to imports); the store is imported by `RoadmapScreen.tsx:19` and `SecurityRoadmap.tsx:5` only. Five e2e files mention the register by words and drive it through the page. A `*.test.ts` row changes nothing the build or a browser loads, so the kit runs no build and no shard; typecheck (`tsc --noEmit`) still reads the new row (S06, S07).
- Ports: reserved block 9910-9919, 0 listeners (control 5000 prints rows), 0 mentions in 59 non-`.pre-` SEAT kits of 16-17 Nov (control 997x: 3 files). The lane starts no server; block 9900-9909 is B1672's (S09).
- Live panes at 21:5x: `Datasec/HPSM-POC-R261` (records seat, owns the analysis repo CLARIFICATIONS entry and two Jira writes, no code-repository path) and `Datasec/NexusAI-N145`. No path shared.

## Model and gate
Sonnet, `model-routing.md:85` row L6 (test-only pin), id `claude-sonnet-5-5` at `models_latest.json:23`; gate G2 at `model-routing.md:109`. Launch line carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes.

## Chain inputs (rule 4)
| Step | Inputs | Produced by |
|---|---|---|
| 0 | the kit, the deploy key, the project 2_Project_Files identity | exist at BASE |
| 1 | clone `head`, the gh helper | Step 0 item 4 |
| 2 | `main-tree` clone, `npm ci` in it | Step 0 item 5, then Step 2 first command |
| 3 | `head`, `npm ci` in `head/web`, `base-unit.json` path | Step 0 item 4; Step 3 first command; Step 2 |
| 4 | the committed-to-be edit in `head`, `base-unit.json` | Step 3 |
| 5 | `d1-test.diff`, base and head vitest json | Step 3, Step 4 |
| 6 | Steps 3-5 green | Steps 3-5 |
| 7 | all logs, the pushed sha | Steps 2-6 |
Note: the row's node-side re-measurement (Step 3 item 4) needs only `remediation-store.ts` from `head` and node24: exists at BASE.

## D-decisions
- D-1: the row asserts six things (the exact value, length 100, last unit 0xd83d, not ending in `b`, `lone.test` TRUE, `ownerOk` TRUE). TRUE on `lone` is deliberate: it pins that the half stays, and the neighbouring rows assert FALSE on their own inputs.
- D-2: red-first by two plants (the opposite value; a length of 99) in `head` before the true row, as the brief asked; one failure each expected.
- D-3: the lone LOW surrogate and any other input are held, named only in FOR TUESDAY.
- D-4: `landing.txt` repeats the HPSM head-pinned squash form with the CLARIFICATIONS line 3617 citation marked RELAYED (not re-read).

## Q-questions (defaults)
- Q-1: keep and pin, the row as written (title carries "pinned as it is")? Default yes (the ticket's own default, the sweep's card candidate 6).
- Q-2: gate G2 or G1? Default G2 (tests only).
- Q-3: no build and no e2e? Default no (measured import count 0; typecheck and lint cover the row).

## UNMEASURED
The row inside vitest (the seat runs it); the whole-suite counts at 6c1aa32e (B1659's 304 files and 4339 passed are an older main, RELAYED); whether `npm run lint` has a rule that reacts to a lone-surrogate escape in a string (the seat's lint run); the infra scan counts at this main (RELAYED from B1659: 14 and 325); wall time of `npm ci`; the CLARIFICATIONS landing line.

## Disclosures (outside the fences, none broken)
- Read: DRAFTER_RULES, the sweep file, the B1672 kit, sidecar and report (form), B1659 kit excerpts, STATUS and evidence landing files (form), the B1674 kit's ownership lines, `model-routing.md`, `models_latest.json`, `ci.yml`, the project `.tools/b1659/scripts/env.sh` (read-only).
- Network: HPSMPOC-507 description and comments by the GET-only `jdesc.py` and `jcom.py` copied from the sweep scratch (credentials in-process, never printed; no Jira write); `gh api -X GET` under the project's own GH_CONFIG_DIR; one shallow `git clone` with the `github_deploy_rw` key into my scratch (as B1672's drafter did); no hosted host, no az, no `npm`.
- One careless command printed the whole #332 file list (a `--jq '.files // empty'` over the commit) to the terminal; it is public diff text, no secret.
- Writes: the three files in the briefs folder and the scratch folder only. No `cd`. The B1672 kit text was NOT blanket-renamed: every B1672/H179 reference was rewritten by hand; a program scan of the new kit for `B1672|H179|b1672` should show only the line naming block 9900-9909 as B1672's (the stamp-day check Tuesday runs).
- stamp_check: 31 claims, 31 measured, 0 not measured; exit 0. Several sidecar lines are marked "instruction to the seat" where the literal is an instruction, not an observed output; stated in each line.

DRAFTED B1675: kit 142 lines, sidecar 31 claims measured, questions 3
