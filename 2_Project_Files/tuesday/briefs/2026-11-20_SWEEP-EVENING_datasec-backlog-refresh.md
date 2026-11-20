SWEEP-EVENING: 6 buildable keys, 5 decisions still open, 51 built-but-open

# SWEEP-EVENING: Datasec backlog refresh, MPS Calculator and Security Composer (read-only, 2026-11-20 evening)

Written by a read-only sweep analyst for Tuesday (s299). Clock from `date`: 17:42:18 AEDT at start, 17:52:07 AEDT at the write of this file. Form: SWEEP-1630 (commission, document, answers file read whole). Instruments copied from `fleet/state/s293/sweep1630/` into `fleet/state/s299/sweep_evening/` (bc.sh, rg.sh, jqdump.py, jdesc.py, jcom.py, lastc.py, each read before use; GET only) plus two GET-only scripts I added (lread.py, prcheck.sh). Fences kept: no Jira, GitHub or git write; no mail, az, deploy, app-host request, test, build or server; no `cd`; no token printed; `gh api -X GET` under each project's own `GH_CONFIG_DIR`; MPS root read with `git --no-optional-locks log/status` only (no lock taken); `decision_queue.sh` used for `list`, `show` and `prior` only.

## BLUF

1. **HPSM-POC was EXCLUDED, as commissioned (the product owner's hold to the end of 2026-12-10): its Jira board, repository and project folder were not swept, counted, read or listed.** NexusAI and OXPd 2 are out of scope by the commission. Frame of every "all tickets" claim below: Jira projects MPSCALC and PCOMP, `statusCategory != Done`, counted by `board_count.sh` through `bc.sh` at 17:42 and again at 17:49 (identical both times: MPS 171, Composer 78).
2. **6 buildable keys, all MPS, none Composer:** MPSCALC-314 (Tuesday's ruling, never started), MPSCALC-418, 422, 423 (test-only follow-ups) and MPSCALC-417, 420 (developer-docs words, buildable only on the C-109 option (b) reading). **Four file-disjoint lanes** (Job 2).
3. **Yesterday's lane M-G is gone, and it did not land as planned.** MPSCALC-316's C# sentence landed (MPS #218, 2026-11-19 18:39 AEDT) but 316 stays open on an unruled question; MPSCALC-195 is NOT buildable: its accepted engine-target sentence is on no record a seat may read (kit B1741 FACT 2). **PCOMP-44 is not "conditional": the product owner ruled HOLD on 2026-11-01** (card `composer-pcomp44-refusal-words-or-hold-1101`, option a).
4. **MPS main moved from 317bbb14 to debb5e28** (five pull requests #218 to #222 merged since 16:30 yesterday). MPSCALC-426 (part codes) is built by #222 and still open; the records seat for #222 (B1781) had written nothing visible at 17:49 (no C-187, board counts unchanged). Composer main is unchanged (b4681297, 2026-11-15), nothing merged, no ticket touched since 2026-11-16.
5. **Of the six candidate decisions, one is already decided and one is mis-framed.** The MPS hosted deploy is ruled and done three times (11-12, 11-16, 11-20); the "words pack" premise is false for the lanes built so far (words are ruled per lane after the build, before the deploy). 0 decision cards are open on the board now. Still open and undecided: the MPS question sheet, the Composer reviewer-round hold, the Composer Guided hold, the Composer seven calls, and (Tuesday's, not the product owner's) whether to build more v13.4.1 lanes on pending words.
6. **51 tickets are built on main but still open** (MPS 47, Composer 4); none is proposed for closing here.

## Census (counts through `board_count.sh`; each line printed "limit was 5001, so this is a real count and not a cap")

| project | open now (statusCategory != Done) | Done (dump) | created since 2000 | control: open + Done = created | open at SWEEP-1630 (16:30) | change by `comm` of key lists | buildable keys |
|---|---|---|---|---|---|---|---|
| MPS Calculator (MPSCALC) | 171 (17:42 and 17:49) | 255 | 426 | 171 + 255 = 426 holds | 162 | gone MPSCALC-267 (Done, #219); new MPSCALC-417 to 426 (10); MPSCALC-416 created and Done | 6 |
| Security Composer (PCOMP) | 78 | 51 | 129 | 78 + 51 = 129 holds | 78 | none gone, none new | 0 |
| HPSM-POC | EXCLUDED | | | | | | |

Controls that can fail: key arithmetic MPS 162 - 1 + 10 = 171 equals the measured 171; Composer 78 = 78. Positive controls for the Done lists: `MPSCALC-415` 0 hits in `MPSCALC_open.tsv`, 1 in `MPSCALC_done.tsv`; `MPSCALC-267` 0 open, 1 Done (updated 2026-11-20T10:19); `MPSCALC-416` 1 Done. Dumps: `rows` = `unique` in all four (171, 255, 78, 51); all 171 MPS and all 78 Composer open tickets read status Backlog. **Staleness control for the carried readings:** 159 of the 171 MPS open tickets have an `updated` stamp earlier than 2026-11-19T16:30 (so their text and last comment are what SWEEP-1630 read); the 12 that moved are MPSCALC-278, 316, 417 to 426 (2 + 10 = 12; 159 + 12 = 171). The newest `updated` stamp in Composer is 2026-11-16T15:13: **no Composer ticket changed since SWEEP-1630**.

Open by reason class today (SWEEP-1630's closed list; a ticket gets one class; B buildable, L landed on main and open, W words, R ruling or answer owed, H hold, C client human, D deploy or an Azure step, X outside tool or data, P planned build or unbuilt predecessor, S stale or umbrella or answered, O other):

| class | MPS | Composer |
|---|---|---|
| B | 6 | 0 |
| L | 48 | 4 |
| W | 34 | 5 |
| R | 13 | 7 |
| H | 0 | 25 |
| C | 1 | 3 |
| D | 12 | 6 |
| X | 4 | 0 |
| P | 8 | 17 |
| S | 21 | 9 |
| O | 24 | 2 |
| sum | 171 (open 171: holds) | 78 (open 78: holds) |

MPS arithmetic: 6 + 48 + 34 + 13 + 1 + 12 + 4 + 8 + 21 + 24 = 171. Composer: 0 + 4 + 5 + 7 + 25 + 3 + 6 + 0 + 17 + 9 + 2 = 78. How the MPS table moved from SWEEP-1630 (162): -267 (W, now Done); 278 W to L (two of three clauses met); 316 B to R; 195 B to W; 314 R to B; new 417, 418, 420, 422, 423 B; 419 D; 421 O; 424 R; 425 R; 426 L. Composer: PCOMP-44 moved from "conditional" to H (ruled hold), nothing else. The other classes are SWEEP-1630's readings, carried because the staleness control above shows those tickets unchanged; **I did not re-read their texts** (see NOT tested).

## JOB 1: what landed since SWEEP-1630 (measured at source, 2026-11-20 17:42 to 17:49)

**Code main now.** MPS `debb5e28f7bbd4e0f641a829eb353ac356afdd81` ("Print the part code before each description in the unpriced purchase documents (MPSCALC-278) (#222)", 2026-11-20T04:55:53Z = 15:55 AEDT; `gh api -X GET .../commits/main`, read again at 17:49: same sha). Composer `b4681297` (2026-11-15T05:56:15Z, PR #130, unchanged since SWEEP-1630). Open pull requests: MPS 0; Composer 1, draft #85 `b330/sm316-content-catalogue` "HOLD K6" (unchanged).

**MPS pull requests merged since 2026-11-19 16:30 AEDT (= 05:30Z)** (`gh api -X GET pulls?state=closed`, merged_at filter; control: the same call returned 40 merged rows back to #183, so the filter reads; the keys are those in the pull request title or body):

| PR | merged (UTC) | merge sha | title | keys named |
|---|---|---|---|---|
| #218 | 2026-11-19 07:39:37Z (18:39 AEDT) | e036c966 | Say the unit of the quote reference limit in the 400 refusal message | MPSCALC-316 |
| #219 | 2026-11-19 08:26:38Z | 73eef991 | Show the server's recurring projection table on the purchase result to callers who receive it | MPSCALC-267 (Done) |
| #220 | 2026-11-19 09:14:32Z | 50d2a471 | Showcase infra keeps the hosted feedback path, refuses empty sign-in ids, pins the budget start and checks setting names | none in title (record ticket MPSCALC-416, Done) |
| #221 | 2026-11-20 01:10:05Z | 565ba142 | Add a priced or unpriced option to the full proposal and the short form | MPSCALC-278 |
| #222 | 2026-11-20 04:55:54Z | debb5e28 | Print the part code before each description in the unpriced purchase documents | MPSCALC-278 in the title; the ticket it builds is MPSCALC-426 |

(#217, merged 2026-11-19T00:48Z, is before the cut.) **Composer: 0 pull requests merged since the cut** (newest merged #130 on 2026-11-15; control: the list returned 40 merged rows back to #92).

**Newest clarification entry of each project's records (heading line, read from the working file; both repos' last commit read with `git --no-optional-locks log -1`).** MPS: `1_Project_Definition/CLARIFICATIONS.md:3544`, "### C-186 -- Did MPS #221 (the priced or unpriced option on the full proposal and the short form) land on main ..." (commit dbc559a, 2026-11-20 13:32:39 +1100). No C-187 exists yet (`grep -c -i '^### C-18[7-9]'` = 0 at 17:49, control: `^### C-186` = 1 in the same file); #222 is unrecorded. The root working tree shows `BACKLOG.md`, `JIRA.md` and `5_Project_History/history.md` modified, so a records pass is mid-write; I counted board numbers at 17:42 and 17:49 and they did not move. Composer: `1_Project_Definition/CLARIFICATIONS.md:2872`, "### C-153 -- Composer PR #125 (the white as one named style value, --pc-on-primary ...) landed on main 2026-11-11 20:13 AEDT and is on the demo since 2026-11-16 ..." (file position newest; C-152 at 2853 records the 2026-11-16 demo deploy of main b4681297).

**What SWEEP-1630 called buildable, one by one:**

| key or lane | status now | the line that shows it |
|---|---|---|
| lane M-G, MPSCALC-316 | PART landed: the C# refusal sentence and its test line (#218, kit B1741, seat M163); the ticket stays open | `QuoteEndpoints.cs:1436` now reads "quoteRef is at most 100 UTF-16 code units (an emoji counts as two) and customer at most 200" (C-184, comment 41400); remaining: `docs/api/openapi.json:988` and `:1036` still `maxLength: 100` (printed at debb5e28, control: same file prints other `quoteRef` lines at 369, 1081, 1490, 1590) and "whether C-64 reaches the schema maxLength" is NOT RULED (C-184, "Work owed") |
| lane M-G, MPSCALC-195 | NOT started and NOT buildable | kit B1741 FACT 2: "THE ENGINE-TARGET SENTENCE OF MPSCALC-195 IS NOT FOUND, so 195 is NOT in this lane"; Q1 default "195 stays open; Tuesday asks the product owner for the sentence's words (the register that carried it is outside the repository)". `docs/API.md:588` and `docs/ENGINE.md` still carry "a what-if only" text for the target. No branch or kit exists for it |
| MPSCALC-314 (Tuesday's ruling) | NOT started | no kit names it (`grep -l` over the 2026-11-18-and-later seat kits in `tuesday/briefs`: 0 hits for MPSCALC-314; control: 12 files hit for MPSCALC-195); no `b17xx` branch other than the merged #218 to #222 branches exists on the origin; `autosave.ts:9` still `export const AUTOSAVE_QUIET_MS = 2000;` |
| PCOMP-44 (conditional) | NOT started; and RULED HOLD | `document.ts` at b4681297 has 0 lines with `sm_policy` (control: `hpsm_policy_id` at 1272); card `composer-pcomp44-refusal-words-or-hold-1101`, ruled option a, `Hold PCOMP-44 until the renderers exist`, 2026-11-01T10:05:08+11:00 (printed with `decision_queue.sh show`). The Composer `CLARIFICATIONS.md` has no entry for that ruling (PCOMP-44 appears only at lines 2068, 2069, 2074, "untouched") and the ticket carries no comment of it |

## JOB 2: the buildable keys now

**Predicate, quoted from SWEEP-1630 (it quotes SWEEP-1115):** "open (statusCategory != Done), status To Do or Backlog, not named on a held, dropped or ruled-against line, the ticket says what to change, no new customer words, no client human's open question, no deploy, no Partner Center, no HP-tool integration, and still true at main"; plus "Developer documents are not word-reviewed (C-109 option b, applied by Tuesday to MPSCALC-415)". Re-run on all 171 MPS and 78 Composer open tickets (the 12 moved MPS tickets re-read; the 159 unmoved carried from SWEEP-1630's classes with the staleness control; Composer carried whole).

**Zero for Composer, with controls:** (a) the predicate fires on MPS in the same run (6 keys); (b) PCOMP-44 passes every structural clause (open, Backlog, says what to change, no deploy) and is stopped by exactly the clause "not named on a ruled-against line", so the clause reads real data; (c) the key list and every `updated` stamp are unchanged since SWEEP-1630. A zero is therefore "nothing new, and the one conditional is a ruled hold".

Blob shas printed at MPS code main debb5e28 (git tree, `mps_tree.txt`): docs/ENGINE.md 3b5ffc81; infra/README.md 55171ec9; infra/tests/test_infra.py 34ebbeda; web/src/screens/quote/autosave.ts dd4ae636; web/src/screens/QuoteScreen.tsx 9e18e29e; web/src/proposal/unpriced.test.tsx eb3f7e7b; OnePager.tsx 9d02239f; ProposalDocument.tsx df4b6bb9; OnePager.test.tsx 558ee1f8; ProposalDocument.test.tsx dcbfa29f; pricedUnchanged.test.tsx 9f2aa36e.

**Proposed lanes (file-disjoint: no path in two lanes; checked against the file lists below, and `test_infra.py` contains 0 mentions of `README` while it contains `bicep` 21 times, so lanes C and D do not read each other's file):**

| lane | keys | scope sentence quoted from the ticket | files it would touch | size | gate guess | what would STOP it |
|---|---|---|---|---|---|---|
| M-1 | MPSCALC-314 | "Autosave writes a history event and a revision per typing pause (22 per minute of paused typing)"; ruling (answers file): "a MINIMUM GAP between saves, in the web autosave only ... 10 seconds as the default ... a named constant beside AUTOSAVE_QUIET_MS"; acceptance: "A counting fake fails above one save request per quiet interval" | `web/src/screens/quote/autosave.ts` (9: the constant), `web/src/screens/QuoteScreen.tsx` (imports it at 24; autosave at 256, leave-save at 94), tests `autosave.test.ts`, `autosave.b456.test.ts`, `QuoteScreen.autosave.test.tsx` (lines 57 to 80 pin one save per quiet interval) | S to M | G2 | (1) the screen shows a "saved" mark while a change is pending in the gap (Tuesday's own STOP: no new customer word); (2) existing cells that pin one save per quiet interval need a changed expectation (QuoteScreen.autosave.test.tsx 60, 74, 80); (3) a trailing save on blur, unload, leave and explicit save is part of the ruling, so any of the four missing is a stop |
| M-2 | MPSCALC-422, 423 | 422: "the committed check for a price in the unpriced documents reads text only, so an amount in an attribute or a whole-dollar fragment without a dollar sign stays green"; 423: "the no-new-word cell admits any part of a priced text, and no committed check sees a priced markup change beyond the column heads" | `web/src/proposal/unpriced.test.tsx` (now eb3f7e7b, after #222's +692 -25), and for 423's committed priced-markup check `pricedUnchanged.test.tsx` or `OnePager.test.tsx` / `ProposalDocument.test.tsx` (the ticket names them, the builder picks); no product byte, no customer word (both tickets say so) | M | G2 | the "stated rule for which integer parts count" and for when a deliberate priced change updates a committed capture are builder design choices the tickets leave open; if the builder wants a rule that bans ordinary counts, that is a judgement for Tuesday; the file was rewritten by #222 so the kit must be cut on debb5e28 not 565ba142 |
| M-3 | MPSCALC-418 | "infra/tests/test_infra.py cannot see the value of an expression setting or an unpinned literal: a changed audience, scope, instance, tenant, allowed hosts or sign-in id expression stays green" | `infra/tests/test_infra.py` only (494 lines; compiles `main.bicep` with `bicep` on PATH or `$BICEP`, every test FAILS rather than skips if none) | M | G2 | needs a working standalone `bicep` in the builder's seat (the file says CI has it; az is never called); each new row must be shown red by a planted change; no real id may be written |
| M-4 | MPSCALC-417, 420 | 420: "docs/ENGINE.md:166 (the X-39 row) still says the contract and the screens do not carry the purchase recurring projection; since MPS #174 the contract does and since MPS #219 a screen does" (change only the first clause); 417: "One words change in infra/README.md" (steps 2 and 3, the pinned budget start, the known what-if noise) | `docs/ENGINE.md` (line 166; the phrase "the contract and the screens do not carry it" is on exactly 1 line, control: line 166 prints), `infra/README.md` (46, 49 to 51, 63) | XS (420), S (417) | G2 (docs read against code) | **conditional on Tuesday reading both as developer-only under C-109 option (b)** ("developer-only documentation sentences are corrected from what the code does without the product owner's word review"; both tickets say that reading is the coordinator's to make); 417's sentence that the pinned budget start blocks a first create after October 2026 rests on "the budget service's published rule (relayed, not fetched)": the builder must not write what it cannot measure |

**Shared files between buildable keys:** none across lanes. 422 and 423 share one file (one lane). 420 touches `docs/ENGINE.md`, which MPSCALC-195 would also touch, but 195 is not buildable.

**Not counted, and why (each read at the source named):**
- MPSCALC-195: the sentence is missing (above). Under C-109 (b) a seat could draft a NEW engine-target sentence from what the code does and skip the product owner's review, but the accepted sentence is "the drafted sentence" of 2026-11-11; whether a fresh sentence is the accepted one is Tuesday's call (question 2).
- MPSCALC-316 remainder: needs the C-64 reach ruling for the schema `maxLength`, and the two sibling messages at `QuoteEndpoints.cs:1450` and `:1454` have no ticket (C-184 "Work owed").
- MPSCALC-419: needs `az` against the showcase subscription and "the coordinator's go and the project's own login" (its own text).
- MPSCALC-421: not a build: read the alert again, close or leave (its own recommendation); a records action. Alert 11 re-read by the records seat at 13:31 today: open, advisory withdrawn 2026-11-18, no patched release.
- MPSCALC-424: "First settle what recorded should mean ... as a question with a default for the product owner"; builds nothing.
- MPSCALC-425: "WAITS for his word; it is not to be started".
- MPSCALC-426: already built (#222); open for its records move.
- MPSCALC-360: Tuesday owes a confirmation after a read-only analyst lays out the reading with two worked examples (answers file); not a build.
- **Words-pending lanes (not counted by the predicate; Tuesday's call, question 3):** MPSCALC-272 [T-V7-1] "Review summary tiles (staff-only)": ticket text "Start: now, no ruling needed (plan section 4). ... Depends on: nothing"; "New words go to the product owner's words gate before any deploy"; files `web/src/screens/Lifecycle.tsx` (bec2c494) and new `web/src/screens/review/**`; acceptance "a caller without internal-metrics sees none and the response carries none". It has the same shape as #219 (built on PENDING words, merged). Whether the server already sends all six figures was not read. MPSCALC-283 (field-help catalogue, "Lane V9 depends on D-15 (words) and nothing else") also reads as words-gated at deploy, not at build; not read to lane shape. MPSCALC-274 is NOT such a lane: it needs a contract field and "Every contract change" waits for the exact name (C-116).

## JOB 3: the candidate decisions of SWEEP-1630, one by one

`decision_queue.sh list open` at 17:43: "0 decision(s) [open]" (so no card is open for any of them; control: `list all` printed 1,573 cards and 295 matched mps or composer). `prior` run on each subject (five calls): only an unrelated card or old chat lines matched; none answers any of them (the matches are listed in `dq_prior.txt`).

| # | decision | ruled already? | card open? | frees today (keys re-counted today) |
|---|---|---|---|---|
| M1 | MPS words pack for the v13.4.1 lanes | PARTLY, and the premise is wrong (below) | no | 33 open W keys + 278 (now part-built); startable-without-predecessor read on 4 of them |
| M2 | MPS hosted deploy of main, and the seed identity's expired secret | DEPLOY: ruled and done (cards 11-12, 11-16, 11-20 = a; entry C-185). SECRET: "renew separately" was ruled each time, never given an owner | no | 2 keys certain (395; 372's restart check), not 11 |
| M3 | MPS open Questions for Kam as one sheet | NO (D-10 a and D-14 c answer parts of Q-10 and Q-03 as defaults) | no | 9 keys now (69 75 76 79 80 82 83 110 288), 314 is no longer waiting (Tuesday ruled it), 360 is Tuesday's owed reading |
| C1 | Composer reviewer-round hold | NO end named | no | 13 keys (19 20 29 31 32 33 34 35 36 37 38 39 92), all 13 present in today's open list; and 17 behind them (42 45 46 47 48 49 50 51 53 54 55 56 57 58 59 60 61; 17 of 17 present) |
| C2 | Composer Guided hold | NO end named | no | 10 keys (68 69 72 75 84 85 86 87 88 90; 10 of 10 present) |
| C3 | Composer seven owner's calls | NO | no | 7 keys (9 70 71 73 76 91 123; 7 of 7 present) |

**Holds relied on (line that sets each, date, whether it names an end):**

| hold | line quoted | date | end? |
|---|---|---|---|
| HPSM (excluded) | "no more HPSM work for the next 3 weeks or until I request something new" and "keep working on other outstanding tickets and the backlog" (live board 16:25:45 and 16:26:43; from the commission and SWEEP-1630) | 2026-11-19 | yes, 2026-12-10 |
| Composer Guided hold | Composer `CLARIFICATIONS.md` line 1298 (the COMP-2 row of C-71), answer "(a) Hold them all." Why: "No Guided work until you turn it back on." Applied on PCOMP-75 (comment 41225): "not to be built while the Guided hold stands" | row dated 2026-10-12 (date as given by SWEEP-1630; not re-derived); applied 2026-11-15 | no |
| Composer reviewer-round hold | line 1297 (COMP-1 row of C-71): "(b) After Paul's current review round." and "a deploy card comes to you when his round ends"; C-99 line 1764: "The owner holds the review until the reviewer's current review round ends ... lane 3a stays blocked until then"; line 1771 "Not settled here: when the round ends (C-92 and C-71 COMP-1 (b) still say the owner says so)". Card `composer-e8-mapping-review-1023` ruled b, 2026-10-23T11:32:53 | 2026-10-12, 2026-10-23 | no: "when his round ends", the owner says so |
| Composer PCOMP-44 hold | card `composer-pcomp44-refusal-words-or-hold-1101`, option a "Hold PCOMP-44 until the renderers exist", detail "Nothing new is built on Composer tonight; no new words" | 2026-11-01 10:05 | a condition, not a date: until the renderers exist (the renderers lane L7 itself waits behind the reviewer-round hold) |
| Composer held PR #85 | label `held`, draft, title "HOLD K6: L1 SM 3.16 content catalogue (release built, not cut)" (read from the pulls list today) | 2026-10-21 | no |
| MPS hosted deploy | SWEEP-1630 quoted `CLARIFICATIONS.md` line 1708, "A hosted deploy of code main 5d96a3dc ... not ruled". **That line is a 2026-11-01 "Open, not ruled" note (batch 4b records) about main 5d96a3dc; it is not a hold and it is superseded:** three deploys are ruled and done since | 2026-11-01 (the line); 2026-11-12, 11-16, 11-20 (the rulings) | n/a |
| "No hosted site change without his card" | C-45 (line 654) and C-186: "putting any later main on the site needs a decision card" | standing since 2026-10-20 | no |

### M1: the words pack for the v13.4.1 lanes (reframed; Tuesday's call)

Already decided? **Not as one pack, and not needed as one.** Quoted: C-186, "the three words ... went to the product owner on a decision card, and he ruled on it on 2026-11-20 (12:52:39, option a)"; C-184, the ten table words of #219 "approved as written by the tap above" (card `mps-hosted-deploy-main-50d2a471-1119`, ruled a, 2026-11-20 09:11:53). Both lanes were BUILT AND MERGED on pending words: #219's body says "Words: PENDING the product owner's word pack ... They are not shown on any hosted site until the pack is ruled"; #221's says "The three new words: PENDING the product owner's word pack". The tickets say the same: 272 "New words go to the product owner's words gate before any deploy". C-45 (the product owner's 2026-10-20 acceptance of the plan): "every new customer-facing word still comes to the product owner as a word pack before it ships". So the gate is the DEPLOY, and SWEEP-1630's class W ("needs customer-facing words ... a builder may not use them") is stricter than what Tuesday has done twice. The matter for the product owner is not "approve a pack so builders may use it". If it is asked at all, the ONE sentence is: "For the remaining v13.4.1 screens, may I build each on pending words and bring you that lane's words on its own deploy card, as I did for the projection table and the priced or unpriced option?" Default if he does not answer: yes, per lane, nothing deployed (this is what has been done, and it is Tuesday's under the 11-06 backlog grant). Tickets it frees today: the 33 open W keys (121 129 130 139 154 156 161 169 194 233 237 243 246 264 265 268 270 271 272 273 274 275 276 277 279 280 281 282 283 286 287 368 402, 33 of 33 present in today's open list) plus 278. **Most are not startable anyway:** most of the 33 list a predecessor ticket (for example 246 depends on 237, 268 on 257, 270 and 271 on 269), and 169, 368 and 274 need a contract field whose exact name is held by C-116 ("holds every contract change until you approve the exact name"). I read their first 700 characters and last comment only; I did not count the predecessors, and whether each is built was not checked. Premises, each with its source: (1) words are gated at deploy: C-45 line 654, #219 and #221 bodies, tickets 272 to 283 text. (2) V7 "Start: now": MPSCALC-272 text. (3) contract names held: C-116 line 2779 and MPSCALC-169, 368 last comments. (4) hosted deploys need a card: C-186 "Not on the hosted site".

### M2: hosted deploy and the seed identity's secret (decided; one owed action)

Already decided? **Yes, the deploy.** Card `mps-hosted-deploy-main-50d2a471-1119` printed with `show`: ruled a, 2026-11-20T09:11:53+11:00, "Deploy now, words approved as written, seller checks skipped again", delivered 09:40:17 "DEPLOYED 50d2a47195957a8b0c914ab2972d0dc703f9bee3" (entry C-185). Earlier: `mpscalc-deploy-seed-secret-expired-1112` ruled a, 2026-11-12T18:36:55 ("Deploy now; skip the 3 Seller checks"), `mpscalc-deploy-seed-secret-again-1116` ruled a, 2026-11-16T10:25:36 ("Deploy without the three seller checks again; renew the secret separately"). **The renewal was named as a separate task and nobody owns it**: MPSCALC-395 (comment 2026-11-16) "the seed identity's client secret is still expired ... nothing has renewed it"; its own text calls it "an Entra write for the product owner or a holder of that grant". It is an action, not a ruling. If it must be asked: "Will you (or Datasec IT) renew the seed test login's secret, or shall the three seller checks stay skipped for good?" Default: stay skipped, record each deploy as "not measured". Tickets freed today: 395 and 372 (C-185: "MPSCALC-372's acceptance ... stays NOT MET as a measurement") = 2 certain; SWEEP-1630's 11 was the whole deploy-class list (103 135 173 187 222 224 226 251 297 372 395); the rest wait on records re-reads of the 2026-11-16 and 2026-11-20 hosted state (224's last comment 2026-11-16 says the host read was "made in part"), on smoke-test repairs (135, 251, 297) or on an approval-class hosted restart (187), not on this decision. Not on the board: no card open.

### M3: the MPS question sheet (undecided; low yield)

Already decided? No. The nearest rulings are defaults inside C-45's D-rows: D-10 a (line 678: "Review warnings at those values" ... the row text itself says "Q-10 open"), D-14 c (line 682: "a setting per quote ... (Q-03 open)"), D-09. MPSCALC-76 and 69 carry no note saying they were answered. The ONE sentence: "Please answer, in one sheet, Q-03 (the brand a customer sees as seller), Q-09 (pricing owner and approvers), Q-10 (approval thresholds), Q-13 (service costs), Q-14 (device recommendation data), Q-16 (retention and audit periods) and Q-17 (fleet size)." Frees today: MPSCALC-69, 75, 76, 79, 80, 82, 83 (the seven seed question tickets, label `question-for-kam`) and 110 (one-pager caps; design rule) and 288 (callerCan.approve vs reject; ruled 2026-10-25 keep listing, a separate reject rule owed): 9 keys, each present today; **not builds**, they close or unblock records, not code. MPSCALC-314 left this list (Tuesday ruled it). Default if no answer: leave them, the build proceeds on the D-ruling defaults. Premises: C-45 lines 678 and 682; the 11 seed texts unchanged (stamps before 2026-11-19).

### C1: the reviewer-round hold (undecided, no end)

Already decided? No end is named by any line (table above). K1, K3 to K10 are ruled (C-86 to C-96); only the timing is open. The ONE sentence: "Has the reviewer's current review round ended, so the new content release (L1 and L2), lane 3a and the Essential Eight mapping review may start?" Frees today: 13 keys (19 20 29 31 32 33 34 35 36 37 38 39 92) and, behind them, 17 (the L3 to L9 chain: 42 45 to 51 53 to 61), 13 of 13 and 17 of 17 present today. Default Tuesday may take if he does not answer: keep holding; no Composer build starts; Tuesday asks again at the next dated checkpoint. Premises with sources: C-71 line 1297 (COMP-1 (b), "After Paul's current review round"); C-92 line 1682 (the content release waits until the round ends); C-99 line 1764 and 1771 (lane 3a blocked; "when the round ends ... the owner says so"); the round's state is not readable here.

### C2: the Guided hold (undecided, no end)

Already decided? No. Line 1298 sets it ("No Guided work until you turn it back on"), dated 2026-10-12. The ONE sentence: "Guided mode is switched off on the Composer demo: switch it back on (and when), or confirm it stays off for good?" Frees today: 10 keys (68 69 72 75 84 85 86 87 88 90), 10 of 10 present. Default: it stays off, the ten stay held (what is happening). Premises: line 1298 (the row text "Guided mode is switched off on the demo", dated 2026-10-12; whether it is still off on the demo today was not read, no host reads); PCOMP-75 comment 41225 (2026-11-15) applies the hold.

### C3: seven owner's calls (undecided)

Already decided? C-71 ruled COMP-1 to COMP-17 on 2026-10-12; none of these seven are in it. Keys present today 7 of 7: 9 (migration tolerance design call), 70 (PDF fonts for CJK, Arabic, emoji), 71 (DEL and C1 characters), 73 (Guided UX review decisions), 76 (hide or build unbuilt controls), 91 (engagements read-only on a content release), 123 (footer sizing, "a measurement"). Not read again by me beyond the titles (SWEEP-1630 read them). One question each; not a single sentence; Tuesday may keep them as separate small cards. Default: leave all seven.

## JOB 4: tickets built on main but still open

**Re-count today: MPS 47, Composer 4** (SWEEP-1630: 46 and 4). MPS: the 46 carried (all 46 present in today's open list, none with an `updated` stamp after 2026-11-19T16:30: staleness control above) plus **MPSCALC-426**, built by #222 (merged 2026-11-20T04:55:54Z, "the ticket it builds" per its own text and the #222 title) with no record yet. Part-built and NOT counted: MPSCALC-278 (#221 and #222; clause 3 "the choice is recorded" is NOT MET, C-186) and MPSCALC-316 (#218; schema clause not met). **Who opened them:** every one of the 50 tickets I read for this has Jira reporter and creator "Kamil Kreiser" (the records seats' single API account), so Jira cannot tell a client human's ticket from a seat's. The only signal is the description's source line: **MPSCALC-140, 155, 157, 158** cite a PR-xx item of the 16 October review transcript (the reviewer's and product owner's words) and 155, 157, 248 name "the reviewer"; none of the 46 cites an in-app feedback id (`FB-nn`: 0 hits in the 46 descriptions; the regexp was checked on MPSCALC-161, which the ticket reads "FB-03" but is class W, not L). Those five are the ones to leave for the client to close; the other 41 read as seat-opened. This is a reading of a text marker, not a Jira field.

Landing evidence (the pull request named in the ticket's last note; **the 49 distinct pull-request numbers my regexp extracted from the 50 notes were checked with `gh api -X GET pulls/N`: 49 of 49 `merged`**; MPSCALC-124's #171 and #175 and the Composer numbers are from the note text, not checked):

| key | pull request(s) named | key | pull request(s) named |
|---|---|---|---|
| 26 | 7, 12, 88, 90 | 140 | 74, 78 (client source) |
| 27 | 90, 91 | 155 | 76 (client source) |
| 28 | 89 | 157 | 50 (client source) |
| 32 | 7 | 158 | 73, 77 (client source) |
| 33 | 15, 16, 26 | 162 | 59, 63, 68 |
| 34 | 88, 89, 90 | 170 | 64, 196 |
| 35 | 6, 137 | 177 | 44 |
| 36 | 7, 16 | 189 | 100, 184 |
| 40 | 7, 88 | 236 | 85 |
| 41 | 7 | 244 | 89 |
| 42 | 7 | 245 | 89, 91 |
| 45 | 5, 7, 11, 12, 25 | 248 | 87 (names the reviewer) |
| 46 | 5, 25 | 258 | 134 |
| 47 | 6, 15, 26 | 269 | 145 |
| 48 | 6, 7, 18, 20 | 306 | 91 |
| 49 | 18, 20, 26 | 310 | 115 |
| 50 | 27 | 359 | 155 |
| 51 | 3 | 369 | 178, 205 |
| 53 | 15, 16, 27 | 407 | 206 |
| 54 | 11, 25 | 124 | 171 (3a7a8048), 175 (54ed7627) |
| 55 | 27 | 426 | 222 (debb5e28), no record yet |
| 57 | 6, 11, 15, 18, 20, 178, 195 | | |
| 62, 64, 65, 74 | 10; 7, 8, 10; 8, 10; 2, 15 | | |

Not read: whether each of those pull requests built every clause of its ticket. The tickets' own last notes say "Recorded; not moved" and the reading of the clauses is the coordinator's (C-79); the 25 seed tasks (26 to 65 range) say the ticket "stays open" for a clause that is a reading or a words item (SWEEP-1630). **Composer 4** (PCOMP-12, 23, 41, 52): PCOMP-12 built by PR #119 (squash 411400f7, merged 2026-11-10); PCOMP-23 by PR #120 (squash 61b3a0c2, merged 2026-11-10; half of PCOMP-23 per C-132); PCOMP-41 by PR #87 (squash e019ac3a, merged 2026-10-24, migration 0024); PCOMP-52: the word "Contents" approved 2026-11-11 and the table of contents present at main per SWEEP-1630 (`policy-document.ts:53 to 60`), the pull request not named on the ticket (not re-read by me). Same reporter finding (all five Composer tickets read: Kamil Kreiser). Proposed to close: nothing. Tuesday's answer 6 stands ("one records seat per project"; "MPS first, AFTER lane M-G is drafted"): note that M-G is now moot (part landed, part dead), so the MPS records pass has no remaining reason to wait.

## EXCLUDED and why

- **HPSM-POC (HPSMPOC board, HPSM-POC repository, project folder): excluded by the product owner's hold to 2026-12-10 and by the commission; nothing of it was swept, counted, read or listed.** One incident to disclose: the decision store is one file for every project. `decision_queue.sh prior` returned, on the word "sweep", the title of an HPSM-POC card (`hpsm39-azure-region-sweep`), and my `list all` greps for "paul|reviewer" printed the one-line titles of several HPSM-POC cards (about ten, some naming MPS as well, e.g. `hpsmpoc-showcase-notes-1023`). I did not open any of them with `show`, did not use them in this document and did not touch the HPSM board, repository or folder. The scratch file `dq_all.txt` holds the whole store's one-line list (all projects) for the same reason; delete or keep as Tuesday decides.
- NexusAI and OXPd 2: out of scope by the commission.
- Anything needing a deploy, a host read or an `az` step (MPSCALC-419; the hosted state of anything).
- The live records seat B1781 (MPS #222): not disturbed; no lock taken; I read the root files by `git --no-optional-locks` verbs and plain reads only. The commission said that seat files "up to two new tickets and two comments (MPSCALC-426, MPSCALC-278)": **those writes were already made at 13:27 to 13:31 today by the previous seat (B1766, entry C-186)**; the seat live now (B1781) is recording #222 and had written nothing visible by 17:49.

## QUESTIONS for Tuesday (each with my default)

1. **MPS lane list.** Run M-1, M-2, M-3 now, and M-4 only if you read 417 and 420 as developer-only under C-109 (b)? Default: M-1, M-2, M-3 yes; M-4 yes, since you applied C-109 (b) to MPSCALC-415 the same way.
2. **MPSCALC-195.** Draft a new engine-target sentence from what the code does under C-109 (b), or ask the product owner for the accepted words (the register that carried them is outside the repository)? Default: ask, via the next card, with the sentence the code supports quoted beside it; do not draft ahead.
3. **Pending-words pattern.** Is MPSCALC-272 (T-V7-1, "Depends on: nothing") a lane for the next free MPS slot on pending words, as #219 was? Default: yes, one lane, after M-1 to M-4 are cut; I did not read whether the six figures already exist in the result.
4. **PCOMP-44 hold.** Add the 2026-11-01 ruling to the Composer records (no entry, no ticket comment) when the next Composer records pass runs? Default: yes; a records seat does it, you decide the wording.
5. **Records pass for MPS.** Launch the MPS records seat for the 47 built-but-open tickets now that M-G is moot? Default: yes, after B1781 returns (same board, same root files; two seats at once would collide).
6. **Seed secret.** Does anyone own renewing MPSCALC-395's secret? Default: leave it, note it on the next deploy card as "not measured".
7. **Stale premise in SWEEP-1630.** `CLARIFICATIONS.md` line 1708's "not ruled" was cited as a hold in SWEEP-1630 and in the MPS decision M2; it is a 2026-11-01 note superseded by three deploys. Default: treat as not a hold; correct SWEEP-1630's table only if you reuse it.

## FOUND / TESTED / HOW

**FOUND.** 6 buildable keys in 4 file-disjoint lanes (MPS only). Contradictions with yesterday's sweep, said plainly: (a) MPSCALC-195 is not buildable (sentence not on any record; SWEEP-1630 said "the builder takes it from the B102 and B163 status files; if it cannot be found the key drops out": it could not, and kit B1741 recorded that); (b) MPSCALC-316's C# half landed (#218), its remainder is an unruled question; lane M-G no longer exists; (c) PCOMP-44 is a ruled hold since 2026-11-01, not a conditional start; (d) the MPS "hosted deploy not ruled" line was stale and the deploy decision (M2) is already made three times; (e) the M1 premise "builders need the words pack" is contradicted by #219 and #221; (f) the commission's own sentence about the live seat is out of date (its two tickets and two comments were written at 13:27 to 13:31). 51 built-but-open tickets. 0 decision cards are open.

**TESTED.** (a) Counts: `board_count.sh` through `bc.sh`, open and created-since-2000, for MPSCALC and PCOMP at 17:42 and 17:49; open and Done dumps by `jqdump.py` (`rows` = `unique`); key-list `comm` against the 16:30 lists; arithmetic controls; positive controls named above. (b) Origin: `gh api -X GET` for main, open pulls, closed pulls (40 each), the five MPS pull request bodies and file lists (#218 to #222), 49 pull requests of the built-but-open set, `git/trees/debb5e28?recursive=1` (734 blobs, for blob shas), `contents` reads at debb5e28 of `docs/ENGINE.md`, `docs/API.md`, `docs/api/openapi.json`, `autosave.ts`, `QuoteScreen.tsx`, `QuoteScreen.autosave.test.tsx`, `infra/tests/test_infra.py`; Composer `document.ts` at b4681297. (c) Tickets: `jdesc.py` for MPSCALC-195, 316, 314, 272 and the ten new tickets 417 to 426 (descriptions to 1,800 characters, three newest comments); `lastc.py` for 33 W keys, 11 D keys, 12 keys with 700 or 650 characters; `lread.py` for the 46 L keys plus 278, 426, 316, 267 and five PCOMP keys. (d) Records: `CLARIFICATIONS.md` of both projects (headings, C-184 to C-186 whole, C-109, Composer lines 1296 to 1300 and 1762 to 1766, grep for PCOMP-44); the s299 daily note lines and kit B1741 FACT 2; kit file lists in `tuesday/briefs`. (e) Decision store: `list open`, `list all`, `show` on six cards, `prior` five times.
**NOT tested:** the text of the 159 unmoved MPS tickets and all 78 Composer tickets (carried by the `updated`-stamp control, not re-read; a comment that does not change `updated` would be missed, but Jira updates that stamp on a comment, which is why the 12 moved tickets are exactly the ones the records seat touched); whether the 33 MPS words keys have built predecessors; whether MPSCALC-272's six figures exist in the server result; the 18 MPS seed tasks with no comment; whether each of the 49 pull requests built every clause of its ticket (only that each is merged); the reviewer's round status; whether Guided is off on the demo today; hosted state of anything; any test, build or server; the PR #222 diff itself (only its body and file list); MPSCALC-195's B102 and B163 status files (I relied on kit B1741's FACT 2 and the ticket's own last note); alert and CodeQL counts. A grep piped into `cut -c` was NOT used to claim any absence: absences are counted on full text with controls (`C-187` 0 / `C-186` 1; `sm_policy` 0 / `hpsm_policy_id` present; `README` in `test_infra.py` 0 / `bicep` 21).
**HOW.** Instruments and dumps in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s299/sweep_evening/`: `bc.sh rg.sh jqdump.py jdesc.py jcom.py lastc.py dgrep.py flags.py` (copied, read first), `lread.py prcheck.sh runL.sh` (mine), `MPSCALC_open.tsv MPSCALC_done.tsv PCOMP_open.tsv PCOMP_done.tsv`, `mps_prs.txt mps_new.txt mps_lane_tickets.txt mps_W_lc.txt mps_L.tsv mps_L_prs.tsv pc_L.tsv mps_tree.txt test_infra_main.py`, `dq_open.txt dq_all.txt dq_show.txt dq_prior.txt`. Clocks from `date`. Instrument errors: (1) zsh does not split an unquoted `$KEYS` variable, so my first `lread.py` run got one malformed key (`InvalidURL`); rewritten as a `bash` script (`runL.sh`) and re-run: 50 of 50 read. (2) My first `lread.py` regexp for pull requests matched only "MPS #n" and missed "PR #n" in MPSCALC-124 and the Composer notes: filled by hand from the notes (124: #171, #175). (3) `rg.sh` caps results at 14 to 30 lines; the `README` absence in `test_infra.py` was therefore re-checked on the whole fetched file (494 lines, `grep -c` 0). (4) An unquoted `======` separator was refused by the shell hook and re-run quoted. No data harmed; nothing written to any board, repository or host; the only files written are in my scratch folder and this document (built whole, temp file beside the target, then `os.replace`).

READ-WHOLE-BY-TUESDAY: ____
