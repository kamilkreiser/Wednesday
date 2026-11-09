STARTABLE: YES

# B1451 / B1452 DRAFTER REPORT (seats G375 and G376, HPSM-POC gates of the L1 web UI builder's two branches)

Kits:
- `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_B1451_SEAT-G375_hpsmpoc-web-ui-gate.md`: 75 lines. Tier 1, Opus. Branch `b1392/hpsmpoc-web-ui` @ `121ee236`.
- `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_B1452_SEAT-G376_hpsmpoc-walkthrough-caveat-gate.md`: 76 lines. Tier 2, Sonnet. Branch `b1392/hpsmpoc-web-ui-d` @ `aca2290c`.

Checks on both kits, each with a control that fired:
- Four-underscore lines: 5 each (S1-S4 and READ-WHOLE).
- `@VAR@`: 0.
- Non-ASCII lines: 0. The B1451 count only reached 0 after a fix, see the disclosure.
- Underscore-aware person-name scan: 0. Control `_by_<name>_` counted 1.
- Card ids: 0.

Drafted 04:2x-04:37 AEDT 2026-11-10. Refs were re-read at 04:36:54 and were unchanged: main `884fd72b`, the two heads as above, 0 open PRs.

## BLUF
- **Both kits are startable.** The two branches share no paths (0 of 5 vs 2) and no parent directories (0).
- **Landing order assumed: B1452 (d) first, then B1451.** (d) is main plus one commit, so its squash is exactly the tree its gate judges.
- **B1451 also judges M2**, the merge of the two heads. M2 is the tree after both land, in either order. B1452 computes the same M2 tree sha as a cross-check, so neither landing order needs a re-gate.
- **I found a real issue for B1452 to grade.** The new step 10 caveat tells the presenter to "score the assessment and approve the narrative before you show it". That contradicts `steps.ts:6-7`, the file's own rule ("No step asks the presenter to save anything ... the review copy's sample data is shared by every reviewer and cannot be reset there"), and step 6's cue "View only: do not save an answer" (`:93`).
  - The panel shows caveats in both mock and UAT modes (`WalkthroughPanel.tsx:36`).
  - The pin `steps.test.ts:64` ("no step that asks to save anything") cannot catch it: it bans `/Answer just one/i` and names only.
  - Gate B1390-1's own suggested fix contained the same kind of sentence.
  - The kit grades it: Major if it is shown in UAT mode and the words do not confine it to a copy that resets; Minor if the words confine it.
- **Branch 1 adds two test-file lines holding a LITERAL U+202E** (right-to-left override). The three main test files I checked for this class use escapes (8 and 17 lines) and hold 0 literals. The kit makes this Minor if main holds none, and Major if a CI step refuses it.

## FACTS RE-MEASURED (instrument and control)

**Refs and PRs**
- Measured with `gh api -X GET git/ref`, at 04:23:39 and again at 04:36:54: main `884fd72b238ec8dc0d566b0e9c18b5362f920a2b`; `b1392/hpsmpoc-web-ui` `121ee236fb4da33f13fcd8a7364e049f4039abbe`; `-d` `aca2290ca280d1b7e60a99dbe4b32a1668008752`.
- Open PRs: 0. Control: the closed list showed 297 to 293. `pulls/99999` rc 1.

**Compares (`compare/...` JSON)**
- `fa401da9...121ee236`: ahead 2, 5 files, +191 -17.
- `884fd72b...121ee236`: diverged, ahead 2, behind 1, base `fa401da9`.
- `884fd72b...aca2290c`: ahead 1, 2 files, +11 -1.
- `fa401da9...884fd72b`: 16 files.
- Commit `121ee236` has 0 files and the same tree `423f6244` as `7f41b900`. So 7f41b90 carries all 5 files. This matches the builder's disclosure.

**Overlap (`comm -12` over sorted path lists)**
- Branch 1 vs branch 2: 0.
- Branch 1 vs main's 16: 0.
- Parent directories shared by the two branches: 0.
- Control: branch 2 vs main's 16 counts 2.
- Coupling that is not in the paths (DERIVED): `steps.ts:220` links "Overview" to `{ customer: "" }`, which is EngagementOverview. Both kits therefore run the walkthrough shards on M2.

**Messages and added lines**
- Non-ASCII lines in messages: 0 and 0 (control: a planted U+200B counted 1).
- `B<digits>` in messages: 0 and 0.
- Opus 5.5 trailer: 2 of 2 and 1 of 1.
- Added lines in branch 1: 191, of which 2 are non-ASCII (the literal U+202E pair) and 6 carry `B<digits>` (comments in main's style).
- Added lines in branch 2: 11, with 0 non-ASCII and 0 `B<digits>`.

**Branch 2's change**
- `steps.ts` has 249 lines at both shas. With line 130 removed from each, `diff` prints nothing.
- `steps.test.ts` goes from 11 to 12 `it(` rows; the new row is at `:99`.

**Screen sources (`awk NR==n` at `884fd72`)**
- `ReportScreen.tsx:175` and `:187` are the two NeedsResult paths; `:188` and `:192` are "Approve the narrative first".
- `NeedsResult.tsx:11` is the title `No ${what} yet`; `:15` is "completed and scored".

**Mock vs API (sources at main)**
- `api.ts:201,204` and `customer-detail.ts:57,82,85` are the mock's guard.
- `Requests.cs:141,146-148,149,153` are the API's list.
- `client.ts:322` reads the first code.

**CLOSED lines**
- 10 lines (`grep -c '^CLOSED-WITH-EVIDENCE '`, control: `-i` gives the same 10). Each has 3 `|` (4 fields), 10 of 10.
- Every cited line re-printed at `884fd72` lands on the claimed construct. I did not grade the claims.

**Round-count loops (173 `GATE VERDICT` first lines)**
- Branch 1 pattern: 1 hit, B1147. It matched only on "two rhythms" and belongs to the other class.
- Branch 2 pattern: 2 hits, B1384 and B1389 ("caveat wording", the readiness class).
- Controls: "customer-page text-link 44 px" hit B1072, B1127 (NO GO) and B1147; "a new sign-in entry point" hit B1385 and B1390.

**Tier precedent (`grep -o -i 'tier...'` over the earlier kits)**
- B1072 and B1147 (the parent class of 439) were tier 1 because the work was "handed to client testers".
- B478 (the hidden-character guard plus the web mock's mirror) was tier 1.
- B959 and B963 (restyles) were tier 2.

**Routing and model ids**
- `model-routing.md:108` G1, `:109` G2, `:111` cap.
- `models_latest.json:17` `claude-opus-5-5`; `:23` `claude-sonnet-5-5`.

**CI (`ci.yml` at main, 682 lines, `grep -n`)**
- The line numbers as written in both kits.
- `e2e.mjs:53-61` (the shards). `playwright.config.ts:4,21,22,25` (ports) and `:26-29` (`CHOOSER_ENV`, the UAT mode with the mock API).

**Landing rule**
- `CLARIFICATIONS.md:3617` (analysis repo, now 5799 lines): "The landing form is a head-pinned squash".

**Ports**
- B1451 gets 9680-9689; B1452 gets 9690-9699.
- `lsof -nP -iTCP:9680-9699 -sTCP:LISTEN`: 0 rows at 04:2x and 0 at 04:36. Control: all listeners, 15.
- Kits scanned: 53 non-`.pre-` SEAT kits of 9 and 10 Nov (95 files of those dates in total). Word-boundary scans for `968[0-9]` and `969[0-9]` found 0 kits.
- Range scan `9[5-7][0-9]{2}(-9[5-9][0-9]{2})?`: no range spans 9680-9699.
- Controls: `967[0-9]` hit 7 kits; `99[4-8][0-9]` hit 5 kits (B1391, B1440-B1442, B1450).
- Live panes: %0, %1, %11-%20 (G374 is %20).

**Other**
- Neither `.tools/b1451` nor `.tools/b1452` exists (`ls`; control: `.tools/b1392` and `.tools/b1450` exist).
- Neither B1451 nor B1452 has a file in `briefs/` other than mine.
- Disk: 1374 GiB available. Load 18.15 / 26.92 / 30.48 at 04:30.

## D-DECISIONS (mine)
- **D1. Tier.**
  - B1451 is tier 1 (G1 `:108`): the link is on the customer page given to client testers (B1072/B1147 precedent), and the mock mirrors the hidden-character input guard (B478 precedent).
  - HPSMPOC-408 does NOT make branch 1 tier 1. Its evidence refusal is not in the diff (closed at main by `d0eff4c`); it is only re-verified as a CLOSED line.
  - B1452 is tier 2 (G2 `:109`, "follow-ups whose mechanism a prior gate already measured"): one string and one test row. G2's escalation to G1 is written into the kit.
- **D2. Landing order and how the overlap is handled.**
  - Paths do not overlap, so neither kit has to wait for the other to land.
  - Both kits judge main `884fd72`. B1451 also judges M1 (with main) and M2 (with the sibling); B1452 judges head (which is its own merge) and M2.
  - Assumed order: (d) first.
  - REFUSE: if main moves, the seat stops for a re-stamp. If the move is exactly the sibling's squash, the re-stamp turns M2 into "the merge with main".
- **D3. Class names (both new).** "one row rhythm in Recent activity and the mock's customer text problems in one 400 list" and "the Demo Walkthrough step 10 presenter caveat". Each kit names its parent class, that class's NO GO count, and leaves S1 free to rule otherwise.
- **D4. B1452 must not follow the caveat in UAT mode** (that would write data). It follows it only in mock mode, counts the writes, and proves the laptop copy resets on restart.
- **D5. B1451 runs all 8 e2e shards at main and at M1.** The builder found 3 reds at fa401da9 (T06/T09), and the mock serves every non-hosted project. At M2 it runs only the walkthrough shards plus the shards holding specs that render EngagementOverview or call create/rename.
- **D6. Name scans are underscore-aware** (the new DRAFTER_RULES line). The ban list comes from the project's CLAUDE.md and JIRA.md; STATUS records only its count and sha256.
- **D7. Landing-file trailer for B1452:** the one its head commit carries (`Claude Opus 5.5`), even though the gate seat itself is Sonnet.
- **D8. HARD STOPs:** B1451 at Step 0 + 180 (heavier e2e scope than B1450); B1452 at Step 0 + 120.

## Q-QUESTIONS FOR TUESDAY (each with a default)
- **Q1. Should the (d) words go to the product owner before landing, not just before a UAT deploy?**
  - Context: the B1392 kit allowed builder wording for (d) and stopped 408 item 2 as his words. The product owner's 2026-11-10 UAT-words ruling (card `hpsmpoc-uat-words-readiness-1110`, D-8 in B1391) makes new walkthrough strings his closed list for any UAT deploy.
  - Default: land on a GO without him. The kit writes a "whose words" Note quoting the string, so it is on his list before any UAT deploy carries PR 297 plus (d).
- **Q2. How severe is the "score the assessment and approve the narrative" instruction?**
  - Default: as the kit states (Major if shown in UAT and not confined by its words; Minor if confined). Since the words say "On the laptop sample", I expect Minor plus a Minor for the `:64` pin.
  - If you rule writes on the laptop copy acceptable, put it in S1.
- **Q3. Is 439 round 1 of a new class, or round 3 of "customer-page text-link 44 px targets" (NO GO 1 of 2: B1127; closed by B1147)?** The same question applies to (d) against the walkthrough class (NO GO 1 of 2: B1385). Default: new classes, round 1 of 2.
- **Q4. Should B1452 run on Opus because the walkthrough reaches client testers on UAT?** Default: no, Sonnet (G2). Its words reach UAT only through the deploy seat's words gate, and the escalation clause covers any security-shaped finding.
- **Q5. Literal U+202E in `customer-shape.test.ts`.** Default: Minor if main holds no literals in source; Major only if a CI step refuses it. CodeQL's reaction on the PR is not known (UNMEASURED).
- **Q6. Launch order of the two waiters (`launch_when_cool.sh` allows only one at a time).** Default: B1452 first (smaller, Sonnet, lands first), then B1451 after the first launch is verified.

## UNMEASURED
- Whether M1 and M2 are clean. I expect clean from 0 overlap. The builder RELAYED `merge-tree 884fd72b 121ee236` rc 0; I did not run it (fence 3).
- The current main's unit and e2e counts. The builder's are RELAYED: 283 files, 4142 passed.
- Which halves hold the walkthrough specs.
- Whether any tracked source file at main holds a literal hidden character. I checked only 3 test files.
- Whether the laptop mock resets on restart, and which role can "Reset demo".
- Whether the hosted UAT sample is already scored (that would change what the caveat means on UAT).
- Whether axe-core is in `node_modules`.
- The full-shard runtimes under the current load.

## OUTSIDE-THE-FENCES DISCLOSURE
- I wrote only my three files.
- **One self-correction.** My first Write of the B1451 kit turned the text `\u202E` / `\u200B` into 3 LITERAL hidden characters (U+202E x2, U+200B x1). My own non-ASCII check caught them, and I replaced them with ASCII escape text using python on my own kit. The file now has 0 non-ASCII lines.
- All reads were read-only:
  - `gh api -X GET` under the HPSM-POC GH_CONFIG_DIR. No token was printed.
  - Raw files fetched into my session scratchpad. The scratchpad also held earlier files (`cl/m_*` from another drafter of this session id). I did not use them, apart from overwriting the ones I re-fetched.
  - Finished project Briefs STATUS files: B1390, B1392, B1385, B1388 by grep, and the first lines of `*STATUS.md`.
  - Tuesday kits in `briefs/` (B1391 for D-8; older kits for tier lines and ports).
  - `lsof`, `tmux list-panes`, `df`, `sysctl`, `ls` of `.tools/`.
  - The header of `launch_when_cool.sh`, via `sed -n 1,40p`.
- I made no git call in a project repo and no Jira call. I did not run decision_queue. I used no `cd`. I made no recursive grep of `0_Brain/learnings/` and did not read `_ledger.md`. I did not read anything inside `.tools/b1392/`.
- `DRAFTER_RULES.md` changed on disk while I was drafting (the underscore-aware name-scan rule was added). I re-read it and applied the change.
