STARTABLE: YES (P1 406-4, P2 465, P3 462 diagnose-then-build and P4 356 closure run without a ruling; P5 (356 B734-6) waits for the RELEASED slot, see Q-1)

# B1503 DRAFTER REPORT: SEAT-H158, HPSM-POC lanes H-B and H-D (HPSMPOC-406 item 4, 465, 462; 356; 399 and 405 dropped or held)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-11_B1503_SEAT-H158_hpsmpoc-lane-hb-hd-shell-buttons-infra.md` (141 lines). Written 2026-11-11 15:36-15:46 AEDT. I wrote only the kit and this report.

## BLUF
- **The sweep's lane was half stale again.** Of the seven items (462, 405, 465, 399, 406 items 4-5, 356) the kit builds three (406-4, 465, 462 if its defect is in an owned file), closes one with evidence (356 B734-9), holds three (405, 406-5, and 462's review half) and drops one (399).
- **399 dropped: nothing left.** All four clauses are built at main. H157 (branch `b1497/hpsmpoc-customer-look-a11y`) wrote `CLOSED-WITH-EVIDENCE` lines for B908-7 and B908-4 with mutation controls (its STATUS lines 44 and 46). The sweep's "put the 6 px letter-spacing clause in H-A" is superseded: H157 built nothing for it (the clause was already built by PR 244), it only closed it with evidence. H-B's 399 remainder is empty, so there is no file-disjointness question.
- **356 dropped to one open sub-item.** B734-9 was built by PR 301 (squash 7d4e3142c3bb996e1113e4659945e2e027a11884, merged 2026-11-09T19:30:13Z = 2026-11-10 06:30 AEDT). The ticket's last comment (10-27) and the sweep still call it "untouched". Only B734-6 (unread `with:` inputs, image strings, retry-log path) is open; P5 is a bounded build of it behind the RELEASED slot.
- **405 held, not drafted as a build.** The ticket says the fix is "a scope call that is not made here"; the records (2-3 Nov) say the residual cells are neither fixed nor recorded as declined. A fixed pill always covers something at scroll 0; the clean fix is the product owner's (move the pill, or accept the cover). It needs a card.
- **406 item 5 held:** the gate's hand-off says "second link to /training after a ruling"; no ruling is recorded. The Home page no longer contains a `/training` href at all (0 hits), and the link in question is `home-next-actions.ts:11` -> `/playbook/phase-1`.
- **No ruling of the 14:15 "accept all 18" pass touches these keys.** B1498's 23 keys exclude all six of mine.

## What I dropped and why (with the instrument)
| key | decision | why | instrument |
|---|---|---|---|
| HPSMPOC-399 | DROPPED | all four clauses built at main; the last two already closed by H157 with controls | B1497 STATUS lines 44 and 46 read by `grep -n`; the 11-04 Jira comment (clauses by number) read by REST GET |
| HPSMPOC-405 | HELD | scope call open; no ruling; every fix either moves the pill (product owner's earlier ruling) or only helps at full scroll | Jira description and comment read whole; records entries read (see Q-3) |
| HPSMPOC-406 item 5 | HELD | ruling owed, none recorded | B947 STATUS line 150 and 159 (hand-offs), Jira description item 5 |
| HPSMPOC-406 items 2, 3 | not in kit | layout calls; the sweep said build 4 and 5 only | Jira description |
| HPSMPOC-356 B734-9 | CLOSURE not build | built by PR 301 | `gh api commits/7d4e3142`, `commits/7d4e3142/pulls` (301), `compare 7d4e3142...009421a2` ahead 8 behind 0; raw `test_ci_workflow.py` lines 34/42/50/981/990 |
| HPSMPOC-462 review half | HELD | "UX/UI review asked for" is to be scoped as its own ticket; Jira writes are not the seat's | Jira text |

## Facts re-measured (instrument; control)
- **Jira** (Python REST GET `/rest/api/3/search/jql`, `project = HPSMPOC AND ( key in (...) )`, credentials read in-process from the project `.env`, never printed; control `key in (HPSMPOC-99999)` returned 0 rows), 15:36 AEDT. All six are **Backlog**; last update and comment count: 356: 10-27 19:50, 2; 399: 11-04 09:46, 5; 405: 11-02 10:26, 1; 406: 11-04 09:46, 1; 462: 11-10 11:40, 0; 465: 11-10 11:40, 0. Also 357: 11-01, 3; 439: 11-03, 0 (read in passing, not in this kit).
- **Register pass (Kam's "accept all 18" and B1498):** `/usr/bin/grep -o -E "HPSMPOC-<k>([^0-9]|$)"` over `1_Project_Definition/Briefs/2026-11-11_B1498_STATUS.md`: 0 each for 356, 399, 405, 406, 462, 465; control 14: 6 hits. Count over B1498's kit file: 0. B1498's keys moved to Done at 14:56 (STATUS line 9): 14, 109, 180, 224, 226, 242, 257, 271, 318, 322, 352; entries C-341 to C-358 (merged as 49eebb284bb48c60ff0869cfb6521e52bce00a48 at 14:54:32). None is in this kit, so nothing is dropped for being Done. Where a ruling governs a key here, it is older than the register pass: 406 item 1: C-271 (approved three phrases, trimmed the fourth; built by PR 282, C-291); 399 ring/radius: C-272; 405: C-240 (filing) and C-42 (pill's place, quoted in the ticket); 462 and 465: C-329 (filing only, no ruling).
- **Code main:** `009421a28616c8b31dde86b59d4c4ca674c288fa` (`gh api -X GET repos/datasecau/HPSM-POC/branches/main`, 15:36), committed 2026-11-10T07:10:19Z, unchanged since the morning; open PRs 0 (`pulls?state=open` length 0; control `pulls/99999` 404). Tree 1803 paths (control: contains `infra/tests/test_ci_workflow.py`). Records repository main `49eebb28...` (the B1498 landing).
- **H157 branch:** head `4f084fb302a44b004e7efee8b666952120889011` (`branches/b1497/hpsmpoc-customer-look-a11y`); `compare 009421a2...<branch>`: ahead 5, behind 0, 11 files (listed in the kit's PARTITION). The set difference with this kit's OWNS set is empty by inspection (no `partner/`, `ui/Button*`, `globals.css`, `TrainingScreen*`, `infra/` path in the 11). Note the 11, not "8+3": the 3 are the extra test lines Tuesday authorised.
- **Pointers** (raw files fetched by `gh api -X GET contents/<path>?ref=009421a2`, `grep -n` at 15:3x-15:4x): `parts.tsx:48` MoreLink; `TrainingScreen.tsx:24` badge, `:29` main, `:31` steps list, `:39` pathway list; `Button.tsx:9` `rounded-[9px]`; `globals.css:103-106` focus rule, `:125` revert-layer; `FeedbackPill.module.css:25-27`; `test_ci_workflow.py:34/42/50/273/329/488/502-504/981/990`; ci.yml `:184-185` images, `:188-191`, `:246`, `:345-349`, `:371/450/483/578` jobs, `:390-426` web-build steps, `:478`, `:494`, `:518`, `:602`, `:630`.
- **Mechanisms (DERIVED, not run):**
  - 465: the steps are non-interactive `<li>` (no link, no button) sharing the pathway rows' badge.
  - 462: the unlayered `:focus-visible { border-radius: 4px }` beats the layered `rounded-[9px]`. The sidebar and the Feedback pill already carry workarounds for the same snap. Whether this is what the feedback saw is UNMEASURED (attachment unopened); the kit makes the seat measure it first.
  - 406-4: `MoreLink` has no min-height; the gate measured 20 px at both trees (B947 STATUS line 147, `grep -n`).
- **Test route for 356:** `infra/scripts/validate.sh:21` runs `python3 tests/test_security_baseline.py`; its runner (from line 2835) loads every `test_*.py` in the folder and demands ResourceWarnings 0 and no open files. So hosted CI runs `test_ci_workflow.py` and `test_hidden_characters.py` through it (PR 301's message: "Ran 316 to 317"). `bicep` on this machine: UNMEASURED; the kit gives a fallback.
- **Ports 9670-9679:** `lsof -nP -iTCP:9670-9679 -sTCP:LISTEN` 0 rows at 15:40 (control: 10 distinct listening addresses). Python word-boundary/range scan of the 71 non-`.pre-` SEAT kits of 10 and 11 Nov: bare hits only in B1391, B1398, B1454, B1460, B1466 (yesterday's seats; their blocks, not live) and wide lists in B1455, B1494, B1496, B1497. Control: the same scan finds 9650-9659 in B1497 and 9630-9639 in B1495. Live pane list (`tmux list-panes -a`): `tuesday`, `fleet-monitor`, `Datasec/NexusAI-N122` and unnamed keep-alives; no HPSM pane. A concurrent drafter (B1502, working in the same scratchpad) may take a block unknown to me; Tuesday's assignment governs.
- **Model:** model-routing.md line 92, row C2 (`grep -n`); id `claude-sonnet-5-5` at models_latest.json lines 23 and 38.
- **Kit self-checks (python, `-I -B`):** four-underscore count 7 (six Stamp slots plus the last line); `@TOKEN@` 0; non-ASCII 0 (after a repair, see Outside the fences); decision-card ids `C-nnn` 0 (control fired); name scan (Kam, Kamil, Kreiser, Paul, Philip, Anupam, Friday, Wednesday) underscore-aware 0, control `x_by_<name>_y` fired for every name; last line `READ-WHOLE-BY-TUESDAY: ____`.

## D-decisions (drafter's; Tuesday may overturn)
- **D-1: 399 is dropped, not carried as a closure.** H157 already closes both open clauses; repeating them here would duplicate the measurements and leave two seats writing closure lines for one ticket.
- **D-2: 462 is diagnose-first with a stated property**, because the element is unknown. The fix has two allowed shapes (one class in `Button.tsx`; or one rule in `globals.css` below the focus rule) and a census requirement for the second, since `globals.css` is global.
- **D-3: 465 keeps the digits and all words** and varies shape, fill and a separator only, so the existing "three numbered items" row stays and no word needs the product owner. Look is the seat's choice within existing tokens and listed contrast pairs; screenshots before/after are saved for Tuesday to show the product owner.
- **D-4: 406-4 uses `min-h-11`** (the 44 px convention used elsewhere in the same file), not a 24 px floor. Tile heights may grow; the probe prints it.
- **D-5: P5 (B734-6) is the gate's own candidate, reduced to three pins** (with-key sets, image repository path, retry-log coupling). Tags, digests, SHAs stay unpinned so Dependabot-style bumps are not noise. It is behind the RELEASED slot because the ticket's done-when says "commissioned or recorded as not wanted", and commissioning is Tuesday's act.
- **D-6: ports 9670-9679** as instructed; e2e ports 9674-9676 follow H157's pattern.

## Q-questions for Tuesday (each with a default)
- **Q-1: the RELEASED slot: `B734-6` or `none`?** Default: **`B734-6`**. The pins are test-only, one file, bounded, and the done-when accepts "commissioned". Without it H-D is a closure only.
- **Q-2: does the product owner want to see the Training look before it lands?** Default: yes, show the saved PNGs from `.tools/b1503/shots/`; the kit builds regardless since it is the product owner's own UAT idea and adds no word.
- **Q-3: 405, a card to the product owner?** Options for the card: (a) accept the cover at scroll 0 and record 405 as declined (no code); (b) move the Feedback pill (his earlier ruling on its place). Default: carry (a) as the recommendation. I did not read the C-42 entry itself (cited in the ticket text).
- **Q-4: 406 item 5**: does the product owner want the Home's "Build assessment competency" action re-pointed to `/training`? It would change a target, not a word, but the hand-off said it waits for a ruling. Default: leave held; put it on the same card as 405.
- **Q-5: merge order with H157.** Default: either order; the OWNS sets are disjoint and the kit's "moved main" rule handles it. If H157 lands first, H158's rebase is not needed (the kit forbids rebasing; it pushes on a non-overlapping moved main).
- **Q-6: records follow-ups** (relay at the next records pass; the seat writes them under `## FOR THE RECORDS SEAT`): 356's comment is stale about B734-9; 399 can be moved after H157 lands; 462's review half needs its own ticket.

## UNMEASURED
- Every number the seat will produce: MoreLink heights, the Training look, the 462 element and radius table, the plant counts for P4 and P5.
- Whether 462 is the focus-radius snap at all (attachment unopened).
- Whether the product owner's earlier ruling on the pill's place permits any 405 change (not read at the entry).
- `bicep` availability on the seat's machine.
- Whether any test other than `TrainingScreen.test.tsx` reads `TrainingScreen.tsx` as text (vitest whole covers it; its own file reads `SRC` and `PAGE` for held words).
- Whether `MoreLink` has users outside `partner/` (the seat prints `git grep`).
- B1502's port block.

## Outside the fences (disclosure)
- **Shared scratchpad collision.** Another drafter (B1502) works in the same session scratchpad directory and overwrote some of my generic scratch names (`tree.txt`, `jq.py`, among others) mid-run; one tree listing came back as a different repository's, which I caught because a control grep returned 0. I moved to a private subfolder (`.../scratchpad/b1503/`) and re-fetched. Facts above come from the re-fetched files. Nothing in a project folder was written.
- **Scratch only:** raw files fetched by `gh api -X GET`, the 2 MB `CLARIFICATIONS.md` (analysis repository, main 49eebb28), the B947 STATUS (analysis repository), Jira text dumps, a ports scan. All under the scratchpad; the Jira reader loaded credentials in-process and printed no token.
- **Reads beyond the template:** B1498's STATUS and its SEAT kit (to check the register pass), B1496's kit (partition), B1497's STATUS, report and addenda. No `decision_queue.sh`, no `briefs_staged/`, no scoreboard, no `_ledger.md`, no WEDNESDAY/FRIDAY tree.
- **Repair:** my Write tool turned the escapes `\u2028\u2029` in the kit's line 56 into the two raw characters (the exact hazard `OTHER_LINE_BREAKS` guards); I replaced them with the backslash-u text by python and re-scanned: non-ASCII 0.
- Two hook advisories on case-sensitive greps; the counts that matter were taken with `/usr/bin/grep` and controls or by python.
- `git ls-remote` over SSH failed from here (no key under my control); I used `gh api` for refs. No git verb touched a project repo.
- The rules file names `/Volumes/Laptop-DEV`; I wrote only under `/Volumes/Datasec_DEV/TUESDAY/`.
