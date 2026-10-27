STARTABLE: YES

# B876 DRAFTER REPORT - SEAT-J30, Security Composer, PCOMP-106 (round 3 of 3, the last) then PCOMP-107 (fresh round 1 of 2)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-28_B876_SEAT-J30_composer-pcomp106-107-routeb-residue.md` (122 lines; 9 lines with the four-underscore pattern = 8 slots + the last line; 0 non-ASCII bytes, 0 CR; 0 hits for the owner's name or the card id).
Drafted 2026-10-28 07:17-07:4x AEDT by Tuesday's read-only kit drafter (Opus 5.5).

## BLUF
- One seat (J30, Sonnet, row C2) builds **two independent one-commit branches on main `bdcfde7b`**, both touching only `packages/db/test/b778-route-b-script-complete.db.test.ts`. Part A (PCOMP-106) comes first. Part B (PCOMP-107) is built after A is pushed. The two PRs have different gates, so they are **two PRs** (D-PR). Tuesday opens both. The seat opens neither, as the template kits require.
- **Part A**, additions only: two new `it` rows (13 to 15) and two helpers.
  - (1) Each of the six pinned command lines (write, redirect, stop, DROP, cat, apply) must sit on exactly one line inside the fences. The count is by `pinned(line).includes(<whole-line constant>)`. **Equality, the ticket's word, misses `GW-dupredirect-nbsp`**, one of the ticket's own 12 shapes.
  - (2) The first non-blank line after the apply line must be the status echo, followed only by blank lines up to the closing fence.
  - Gate: tier 1 (G1), **round 3 of 3, the last**.
- **Part B** changes one assertion: line 311 compares only the lines from the opening fence to the closing fence. It also adds two in-helper controls. Gate: tier 2 (G2) by default, **round 1 of 2**.
- **Design check (drafter's node script, not the test):** the sketched helpers are empty at main and red on all 66 line copies plus `GW-dupredirect-nbsp`. The fence-only line 311 turns GR-cr-222/230/261 equal and keeps the in-fence CRs unequal. Nothing was run in the project.

## Facts re-measured (instrument; control)
- **Card**: `decision_queue.sh show composer-106-107-routeb-residue-round-1028` into a scratch file (id count 1). Status `ruled`, choice `a`, `ruled_ts=2026-10-28T07:15:22.250275+11:00`. Tuesday's relay said 07:14:52; the store's time is 07:15:22. The kit says "about 07:15 AEDT".
  - Option a label and detail are quoted verbatim in the kit, under "the product owner's 2026-10-28 ruling" (no card id).
- **Main**: `ls-remote` 07:17 gives `bdcfde7b90a5e0022bf50f639de2db85b51e44a3`, the squash of PR #100.
  - `compare/304507b5...bdcfde7b` lists 1 file, the b626 date test, so packages/db is unchanged since PR #99.
  - `b876*` is absent. Controls: `b839*` reads `cca0f6cb` and `b857*` reads `9494afe7`.
- **Blobs at main** (`contents?ref= .sha`; for the two raw copies, `git hash-object` agrees):

  | File | Blob |
  |---|---|
  | test | `954f7c9f` (= PR #99 head; 811 lines, 13 `it(`, 0 non-ASCII, 0 CR, 0 tab) |
  | `DEPLOY.md` | `8359bace` (628 lines) |
  | b616 | `ee282782` |
  | `support.ts` | `13eb5f3e` |
  | `vitest.config.ts` | `d9c74dfd` |
  | `package.json` | `32fea116` |
  | lock | `53305eb4` |
  | `ci.sh` | `4b2d15ce` |
  | `test-db.sh` | `c6aa9c7c` |
  | `.prettierrc.json` | `de753c53` |

- **Tickets** (`jira791.py get`; control `PCOMP-999999` gives 404):
  - PCOMP-106: label `plan-comp-396`, Backlog, 0 comments. PCOMP-107: label `plan-comp-397`, Backlog, 0 comments.
  - The summary, fix shape and Done-when of each are quoted verbatim in the kit.
- **Test anchors** (`grep -n -i -F`): line 311 holds `expect(block.lines).toEqual(routeB(markdown).lines);` (count 1). `groupProblems` is at 238. Line 811 is `});`.
- **DEPLOY.md block**: lines 198-209 (fence, umask, write 200, redirect 201, echo 202, check 203, stop 204, DROP 205, cat 206, apply 207, status 208, fence 209). Printed by `sed`.
- **Gate lineage**:
  - B845: line 1 reads STOPPED (escalation), round 1 of 2. The ruling addendum records NO GO round 1 of 2.
  - B850: line 1 reads NO GO round 2 of 2, tier 1.
  - C-107 (`CLARIFICATIONS.md:1924`) records the landing and leaves the third-round question open.
  - B815 is the PR #97 gate (round 1 of 2 on the paragraph class). I read only its head. It is lineage, not this class.
  - Evidence `mutant-table.tsv` has 591 lines. The 12 ticket ids plus GR-cr-1/263 read GREEN13. GR-cr-222/230/261 read `W,G`.
- **Seat name J30**: a word-boundary scan of 110 non-`.pre-` SEAT kits dated 27-28 Oct gives 0 hits. Controls: J29 gives 7, J28 gives 5. J3x appears in no file dated 26-28.
- **Ports 9910-9919**:
  - The same 110-kit scan gives 0 hits. Control: `985[0-9]` gives 2 (B857, B864).
  - Widened to every file dated 26-28, there are hits only in 26 Oct HPSM-POC files (B730/733/734/735/738: closed seats, no pane).
  - `lsof` printed nothing (rc 1). Control: a `python3 -I` bind on 9919 listed 2 lines, and after it closed `lsof` was back to rc 1.
- **Panes 07:2x**: `%0 tuesday`, `%122 Datasec/HPSM-POC-D40`, `%121 Datasec/NexusAI-R79`, `%1 fleet-monitor`. No Composer pane.
- **Open PRs**: #95 (2 files), #91 (2), #86 (2), #85 (57, draft). Each has 0 overlap with the test path, `DEPLOY.md` and `packages/db/`. Control: the b712 test is found in #95.
- **Live b6-8 branches**: 29. Five touch the test path or DEPLOY.md: b61, b616, b778, b806 and b839. All are diverged, have no PR and no pane, and three of them are the merged #96/#97/#99.
- **Identity**:
  - The last 8 main commits have 1 distinct author pair, all on `users.noreply.github.com`.
  - `localdomain` count: `bdcfde7b` 0, control `dc16530a` 1.
  - `gh auth status`: Datasec 1, Secuura control 0.
  - `core.sshCommand` points at the Composer deploy key.
- **CI**:
  - `ci.sh`: step() at :28, `if "$@"` at :34, node chain at :117, db step at :118.
  - `test-db.sh`: `set -euo pipefail` at :4, never skips (:3), both vitest configs chained with `&&` at :58.
  - `.github/workflows` returns 404.
  - Check-runs on `bdcfde7b`: total 2, both completed success.
- **Routing** (`model-routing.md`):
  - Builder: C2 at :92 (S55 1st) and L6 at :85.
  - Gates: G1 at :108, G2 at :109, G-cap at :111.
  - Model ids from `models_latest.json`: sonnet at lines 23/38, opus at 17/37. `brief_seat.sh:24` defaults to opus, so the level is written inside the quotes.
- **Load**: `uptime` load1 was 5.57 at 07:23.

## D-decisions (the drafter's; Tuesday accepts or strikes at the stamp)
- **D1 Seat and ports.** J30 and 9910-9919, measured as above.
- **D2 Model.** Builder C2 Sonnet (`BRIEF_SEAT_LEVEL=sonnet`). Not C3: this is a test-only pin on operator text, not a design surface.
- **D-PR (shape), default: two branches, two PRs, each ONE commit whose only parent is main `bdcfde7b` (independent, not stacked).**
  - The seat builds A first, pushes it, then builds B in a fresh tree from main.
  - The hunks do not overlap: A adds near :38, :250 and :810, and B changes :311 (maybe :304) and adds controls after it. The seat proves `git apply` of both in `wt-b876-both` (15 of 15). It also proves A's rows are 0 red on every outside-the-fences CR id.
  - Why not one PR with a split gate: A's gate is final with no fix round, while B may need one. One PR would tie a B fix round to a head A's last gate already judged.
  - Why not stacked: if A's round 3 is a NO GO and A is not landed, a stacked B is stuck. Independent B lands either way.
  - Cost: whichever PR lands second has a moved main. Tuesday's squash check then compares against a 3-way merge tree, not the head tree (Q4).
- **D-A (part A design).**
  - Additions only, so the 10 old rows (the ticket's clause) and the 3 PR #99 rows stay byte-equal, and the gate can diff old13 against main's file per mutant. O is not widened, though the ticket's fix shape said to widen it. Two new rows, not one, so each shape is red on a named row.
  - The count uses `includes`, not equality: equality leaves `GW-dupredirect-nbsp` green (design check).
  - The status tail allows blank lines. A blank line after :207 or :208 is a bash equivalent, and refusing it would be a stricter-than-necessary Note in the last round.
- **D-B (part B design): compare from the opening fence to the closing fence, inclusive.**
  - This is the ticket's first fix shape. It turns GR-cr-222/230/261 green.
  - It keeps a CR on :199 (`umask 077`), :202 and :203 (the check line) red. Today line 311 is the only thing that catches those lines, and bash reads them.
  - "Strip one trailing CR everywhere" would turn them green on every row, so it is not taken.
  - Known effect: KT-206-cr stays red on W as well as G. The Done-when requires only G; the ticket's BLUF mentions W as part of the symptom (Q3).
- **D-gates.** A: G1 tier 1, round 3 of 3, the last (the ruling's "top-tier tester"). B: G2 tier 2, round 1 of 2 on its own class (Q2).
- **D-scope.** `DEPLOY.md` is untouched: the ruling says test-only. Part A makes the pin paragraph ("Nothing else in the command is pinned.") understate more. It goes to FOR TUESDAY; row #398 already holds it as O-item (Q1).

## Q-questions for Tuesday (each with a default)
- **Q1 `DEPLOY.md` pin paragraph.** After A, the paragraph does not name the six-lines-once pin or the status-tail pin.
  - Default: accept as a Note under row #398. A words ticket can follow later.
  - Not in this lane: the ruling says test-only, and a DEPLOY.md edit would bring a G1 document-class gate into a last round.
  - Risk: A's tier-1 gate grades it under the PR #97 class ("the test pins what the guide says"). The kit tells the gate it is out of lane, but only Tuesday's stamp makes that binding.
- **Q2 B's gate tier.** Default: tier 2 (G2). The mechanism is a false red that a prior G1 gate (B850-3) already measured. Alternative: one Opus seat gates both PRs as two verdicts.
- **Q3 KT-206-cr on W.** Default: accept that W stays red on it under fence-only. The Done-when names only G, and D-B's reason is the umask and check-line CRs. Alternative: the per-pinned-line shape, which loses those CR pins.
- **Q4 Landing order.** Default: land A first, then B. B's squash tree must equal `merge-tree(main-after-A, B-head)`, and `wt-b876-both` is the seat's proof that it is 15 of 15.
- **Q5 Builder model.** Default: Sonnet, as row C2 says. Opus is not in the table for a test-only build, though A's round is final and two Sonnet builds on this file each drew a NO GO.

## UNMEASURED
- No vitest, container, image, probe or mutant was run against the test.
- The design check copied `routeB`, `exactBlock` and `pinned` into a node script and ran 88 swapped documents. It did not cover `respaced()`, `missedBy`/`planted()` and the rows' full verdicts.
- The group count 39/527 at `bdcfde7b` is RELAYED from B850. It is the same test and document; the drafter did not re-run it.
- The exact text swaps of the regression ids beyond `mutant-table.tsv`'s edit column.
- prettier on the added lines.
- psql's real answers.
- The wall time of the batteries.

## Outside-the-fences disclosure
- The card was read with `show <exact id>` into a scratch file, and the id was counted (1). I then printed the whole scratch file, not only the lines matching the id. It held this card only.
- I read the header and function list of `jira791.py` with `sed`/`grep` (no invocation) and called only `get` from a scratch program.
- The drafter wrote session-scratchpad files only: card.txt, jr.py, scan.sh, scan2.sh, b778.test.ts, DEPLOY.md, ci.sh, test-db.sh, design/d.mjs, d2.mjs and out.txt. It bound port 9919 on 127.0.0.1 for under a second, as the lsof control.
- One command was refused by a hook (an unquoted `=====` separator). Nothing ran; it was re-run with `echo ----`.
- No project file was written. No git write verb, fetch, `merge-tree`, HTTP to a hosted host, mail, card, Jira write, Artifact or launch. No non-Datasec tree was read.
- Two files written: the kit and this report.
