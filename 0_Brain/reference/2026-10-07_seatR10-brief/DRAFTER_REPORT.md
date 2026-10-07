# DRAFTER REPORT — Seat R 10th brief (gate73 merge seat, then raise)

**Drafted 2026-10-07 06:3xZ-06:5xZ (≈17:3x-17:5x AEDT) by a Wednesday brief-drafting subagent. Staged only: NOT sent, NOT launched.**

## BLUF
- **Built:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-07_seatR10_merge_gate73_raise_pr5_spark3.md`. 205 lines, 51,737 B, sha256/16 `6681b19616f19236` (measured after the last edit, 06:49Z).
- **Shape.** It mirrors R 7th's merge shape and R 9th's raise shape:
  - BLUF; the FIRST THREE THINGS; the partition from both sides; a bounded ITEM 0;
  - QUEUE M: four squashes, each on its own GO, in order 1407 -> 1409 -> 1408 -> 1410, with merge-ins built from the composed docs VERBATIM plus `qm`;
  - QUEUE 5D: the owed tier-3 comment follow-up;
  - QUEUE R: PR 5 (KS-1164) plus the Spark passes KS-1274 and KS-1410 x2;
  - PR BODIES, TOOLS, HOLDS, THE GO;
  - RULED BY KAM NOT YET IN AN ARTEFACT, and RULED BY WEDNESDAY STILL OPERATIVE;
  - QUESTIONS, MAIL FORMATS, UNMEASURED, and PROVENANCE P1-P13.
- **The finding that most changes the seat's plan:** the merge set has to be re-keyed before any merge can happen.
  - R 9th copied none of it. It lives in R 8th's `raise/` folder.
  - Its addendum builder is narrow to gate71's GO-mail shape: `build_addendumra8_1398.py:72-78`, `:92`, `:94`.
  - So **Wednesday's gate73 GO and ADDENDUM mails need a defined shape** (Q-GO73, Q-ADD73).
  - So do the four squash body files (Q-BODY73). Nothing in the kit holds them.
- **New hazard, not in any earlier brief:** R 10th is the first two-digit R ordinal.
  - `namecheckra1.py`'s argv-tag list carries `-ra1` and is SUBSTRING-matched by its own comment (`:140`). Its ref-namespace list carries `seatra1`.
  - Both are substrings of `-ra10-` and `seatra10`.
  - The segment verdict at `:1021` compares whole segments, so it is not exposed.
  - **I read this. I did not run it.** The brief tells the seat to drive planted arms.
- **Budget, stated plainly in the brief.**
  - Precedent: R 6th read 52% after ONE merge, and R 9th read 49% after two raises.
  - So the brief tells R 10th to expect to finish the four merges plus the §5d follow-up and hand the raise track to R 11th.
  - It says to wrap cold at about 50% with a RESUME block.

## Every fact and its source

### Develop and refs
- **develop `147ae442074c7f3b5be9ce7ccc4452c8dae34b4f`**
  - Each of the four heads equals its `refs/pull/<n>/head`, and equals its branch.
  - #1383 head is `32e8459bc0f5`.
  - 2,115 lines; highest `refs/pull` is 1410.
  - 0 `-ra10-` and 0 `-e11-` branches. Control: 2 `-ra9-` branches read.
  - Source: `env -u GIT_SSH_COMMAND git -C ".../2_Project_Files" ls-remote origin`, **06:39:44Z-06:39:49Z** (from `date -u`), rc 0, output saved to my scratchpad as `lsr_r10.out`. An earlier narrow read at 06:39:31Z-06:39:37Z agreed.

### Gate73 state
- **gate73 is launched and running. There is no verdict yet.**
  - Pane `QA/Secuura-gate73` is %84 (`launch_063526.cockpit_add.out`).
  - `launch_063526.launcher_check.out` reads "all guards pass … merge seat Seat R 10th".
  - The report dir holds only `NOT-TESTED.written-first.md` (17:36) and `evidence/`. There is no `report.md`, read at 06:38:04Z.
  - Gate prompt `:41` carries the four GO strings, each to be the VERBATIM subject of its own mail. Prompt `:23` defines `qm`.
- **Kit files and hashes (sha256/16):**
  - `KIT_REPORT.md` `4ecae42acc6bfb15`
  - `RULINGS_wednesday.md` `041ddcdda1450fac` (includes "RULED AT LAUNCH")
  - `kit.json` `dfc3b34353f4a6f4`
  - In `kit.json`: `merge_seat` = "Seat R 10th"; `squash_max` = 92; `trailer_control` = `bf277eead268`, 55 raw bytes.
- **Predicted trees** (KIT_REPORT §0.3, which matches `composed_2026-10-07/MANIFEST.txt`):

  | step | PR | predicted tree |
  |---|---|---|
  | 1 | #1407 | `e1d3f4a6…` |
  | 2 | #1409 | `2a0a7203…` |
  | 3 | #1408 | `640d33dd…` |
  | 4 | #1410 | `54c2c6dd…` |

- **Composed docs:** `git hash-object` on all 8 composed docs matches their MANIFEST blobs, 8/8 (my run).
  - #1407's own head doc blobs equal the step-1 composed blobs, and its head tree is `e1d3f4a6` (my `ls-tree` and `rev-parse`).

### Merge-set tool reads (my file:line reads)
- **`mergera1.py`** (sha256/16 `aaf230e7d1975213`, 604 lines):
  - `:127-136`: `--addendum --go-ts --gate --scratch --seat` are REQUIRED. `--expect-develop` is OPTIONAL (`:129`).
  - `:261`: the PR's files must equal the addendum's target paths.
  - `:376-415`: MG-11. It refuses a missing subject, `(#n)$`, any `(#`, more than 92 characters, and non-ASCII. It appends nothing.
- **`build_addendumra8_1398.py`** (`51b293d05a762cf5`, 232 lines):
  - `:28-29`: 13 required env vars.
  - `:72-78`: the GO-text regexes.
  - `:92`: the GO clause `GO (Seat R 8th): merge {PR} on gate71`, plus `qm Q2 STRICT` and `qm green`.
  - `:94`: `ACTIONS VERDICT (Wednesday):` and `0 new failures`.
  - `:176`: the predecessor loop.
  - `:211`: writes `addendum-gate71.json`.
  - 46 `RA8_` occurrences, counted with `grep -o`.
- **`mergeinra7_1398.sh`** (`38040091a9cf4b52`, 286 lines):
  - `:31`: `REPO=` is hardcoded.
  - `:43-58`: the arguments.
  - `:79`: refuses unless the lock seat is on lane R.
  - `:98`: the log name. `:196`: `merge --no-ff --no-commit`. `:282`: the summary print.
- **`pushra1_ff.sh`** (`dd8b1083a37fb82d`):
  - `:82`: LOCK_SEAT is required.
  - `:84`: positional arguments `WT TARGET EXPECT`.
  - `:100`, `:103`, `:106`: exits 4 and 3.
  - `:108`: DRYPROOF.
  - I found no branch-name gate in `:82-118`. That is a read, not a proof; the brief says the tool wins.

### Raise-set tool reads
- Hashes as listed in the brief's TOOLS section (`shasum -a 256`).
- `lockra1.sh:217-226`: lock name guard. `:505-509`: a foreign holder exits 12, by exact string compare.
- `inbox_matchra1.py`:
  - `:102` MINE is "r 9th".
  - `:236`: **OTHER_SEATS already carries "r 10th"/"seat r 10th"** (R 9th's forward-add). R 10th must REMOVE them.
  - `:113`: the matcher is word-boundary anchored.
- `twolockra1.sh:41`: LOCK_SEAT is `ra9`.
- `restraisera9.py:32`: User-Agent is `secuura-seat-ra9`.
- `namecheckra1.py` declaration lines are as cited in the brief. Grep counts: 15 lines carry `ra9`, 14 carry `r 9th`.

### Shared store and worktrees (read verbs only)
- `rev-parse --all`: 1,618 lines, `6c02ca445cad9fed`, identical before and after my `clone --shared`.
- All four batch worktrees are ATTACHED to their branches, with 0 modified files:
  - `s-ra9-ks998` at `3be1a5317735`
  - `s-ra9-ks1313` at `c8899a95dc44`
  - `s-e9-ks1435` at `ce33ec8b3eae`
  - `s-e10-ks591c` at `c976c9f72ba0`
- Locks: 0 `.push-lock-*` at maxdepth 2, while a planted scratch dir read 1 by the same `find` (06:44:43Z).
- `df -m`: 677,849 MiB available.

### Payloads, applied in a temp index at `147ae442`, in my scratch clone
`check`, `apply` and `write-tree` all returned rc 0.

| payload | bytes | sha256/16 | tree |
|---|---|---|---|
| KS-1164, ruled variant | 4,643 | `5c5e586406ebe4b1` | `4a0a1ad20ba6` |
| KS-1164, other variant | 4,886 | `bca34d1f0e9857fa` | `4a0a1ad20ba6` (same) |
| KS-1274 | 5,023 | `138b5cef4f3e4ded` | `67316d99d353` |
| KS-1410 notifications | 10,086 | `59f20b6bc1af75ba` | `e3cb026fb558` |
| KS-1410 batch + audit-export | 10,835 | `417c112c7be043da` | `765218138c71` |

- The two KS-1410 payloads stacked give `64aefb896ae6` in both orders.
- Control: applying notifications a second time fails with rc 1 at `notifications.ts:13`.
- Modes: `04-container-trivy.sh` is **100755**. The rest are 100644.
- The KS-1164 payload adds ONE test file (+102/-0) and no product line.

### §5d sites
- Hunk headers from `git diff -U0 147ae442..<head>`:
  - #1407 `@@ -180 +180`
  - #1408 `@@ -411,0 +412`
  - #1410 `@@ -1630 +1630`
- Own-key count in each whole file: 0, 0 and 0.
- Text-search trap: `signature: z.string().optional(),` appears at `:403` AND `:412` in #1408's `index.ts`.
- Control: the sibling KS-518 comment count is 1.

### Other PRs
- #1383 changes 4 paths (`git diff --name-only 147ae442...32e8459b`): migration 049, its test, and both platform docs. Its code is disjoint from every payload and every batch PR.

### Seat-history sources
- R 9th's handover: **re-hashed `ff849038744e45ba`**, which matches the expected first 16. 166 lines, 13,197 B.
- E 10th's handover: `e7bb132c8848d3a7`, 248 lines, 17,688 B.
- R 9th READY/WRAP, E 10th WRAP, and the R 7th, R 8th and R 9th briefs: read whole. The cited line numbers were re-checked by grep, and six were corrected after the first write.

### Rules
- Project rules:
  - `CLAUDE.md:185` is the notify rule (Peter/Stuart, tickets only, batched at wrap).
  - SKILL blob `b59b74a592e9` at `147ae442`: §4 `:360-363`, §5d `:507-516`, §5f `:540-552`.
- STANDING_LINES:
  - `:76-99`: holds and test blocks.
  - `:269-270`: the canonical `live sweep owed`.
  - `:272`: quote only the gate lines that push printed.
  - `:339`: the "next up" rule.
  - `:395`: `$TMUX_PANE`.
  - `:396`: no force push.
  - `:397`: fresh-worktree build.
- Routing tokens: `fleet/send_brief.sh:136-151` (stop / hold / hand over now / checkpoint outside the leading position).

### Decision cards
- Source: `decision_queue.sh list ruled | grep -i secuura | tail -40`.
- Touching this seat:
  - `secuura-capped-prs-1245-1278-disposal-1005 = a`: #1245's pointer comment is now due when #1409 squashes.
  - `secuura-ks1404-anchors-before-049-merge-order-1005 = a`: #1383 is held.
- The "RULED BY KAM NOT YET IN AN ARTEFACT" section is present and lists these.

## OPEN QUESTIONS for Wednesday (each with my recommendation)
1. **Q-GO73: what the GO body must carry.** The builder parses labelled lines (`:72-78`) and requires the `qm Q2 STRICT` / `qm green` clauses (`:92`). **Rec:** use R 8th's labels verbatim in each gate73 GO. The seat re-aims only `:92`'s GO-subject clause to `GO (Seat R 10th): merge {PR} on gate73`.
2. **Q-ADD73: should there be an ADDENDUM for every GO, including #1407?** #1407 has no merge-in, and the gate already classified its head. The builder's `:94` cannot pass without one, and the seat must not re-point it. **Rec:** yes, all four. #1407's ADDENDUM cites the gate's classification; the other three follow the Actions on each merge-in M.
3. **Q-BODY73: who writes the four squash body files, and where do they live?** **Rec:** Wednesday composes them from the gate report into `gatesets/2026-10-07_gate73/squash_bodies/<pr>_squash_body.txt`, with the sha256 in each GO. The seat re-hashes and never edits. #1408's body states Q-NULL.
4. **Q-ADOPT10: the merge-in pushes write to three branches the seat did not author** (`…-ra9-4`, `…-e10-1`, `…-e10-2`), and all four worktrees are attached. **Rec (a):**
   - Adopt the three branch NAMES only: ADOPTIONS = 3, EXPECTED = 3.
   - `ADOPTED_WORKTREE = []`.
   - Cut fresh detached `s-ra10-m<pr>` worktrees at each head.
   - Hold any E successor off those two E branches until #1410 squashes.
5. **Q-RA10-PREFIX: how should the ra10/ra1 substring collision in the namecheck forms be resolved?** **Rec:**
   - The seat drives planted arms at ITEM 0 and reports.
   - If a scanner reads its own `-ra10-` as R 1st's, it proposes a change: drop `-ra1`/`seatra1` from the substring lists, keeping the segment-matched `ra1` in FOREIGN, which already covers R 1st. You rule.
6. **Q-5D-PATH: how does the comment-only follow-up land?** **Rec:**
   - Branch `feature/skill5d-why-comments-gate73-ra10-1`, with no ticket key in the name.
   - KS 998, KS 1435 and KS 591 de-hyphenated in the title, body and commit, and no hyphenated key.
   - GO subject `GO (Seat R 10th): merge <pr> on tier3`.
   - No §4 doc block. §4's own words say "test change" (SKILL `:362`).
7. **Q-N10: flow numbers for KS-1274 and KS-1410.** **Rec:** `35.` and `36.` (plus `37.` if two KS-1410 PRs). E keeps `32.-34.` for E3-E5.
8. **Q-1410: one PR or two?** Q-BUNDLE says one PR per ticket. Your commission said "three … as PRs". **Rec:** ONE PR for KS-1410. The stacked tree was measured equal in both orders. Your call, because it deviates from the commission wording.
9. **Q-1245: #1245's pointer comment after #1409 squashes** (Kam card a). It is a GitHub comment that a human can see. **Rec:** you supply the text in an ANSWER; the seat posts once and reads it back. Otherwise it waits.
10. **Q-NOTIFY10: the §5f `live sweep owed` comment on KS-1435 after #1408**, and any Peter/Stuart test block. **Rec:** the KS-1435 comment goes out only with your text in #1408's ADDENDUM. No Peter/Stuart comment from this seat; you batch the test block with the next kintsugi deploy.
11. **Q-TIMING: when to launch.** **Rec:** launch R 10th when gate73's verdict mail lands, not now. An early launch spends ITEM 0 context and then idles for hours on a gate it cannot act on. If you launch now, the brief's ITEM 0 still holds it until GOs arrive.
12. **Q-BASE10R** (RAISE_BASE = develop at the start of QUEUE R, accepted by name), and **Q-1383** (if #1383 lands, STOP and re-predict). **Rec:** as written.

## UNMEASURED (and why)
- **gate73's verdict, the GO lines, the declared subjects and the bodies.** The gate was still running when I read it (06:38Z).
- **Linear states and assignees for all eight tickets.** I made no Linear read, to stay lean. The brief puts it at ITEM 0 (f).
- **Whether the ra10 substring hazard actually fires.** I did not import or run namecheck; the seat's planted arms close it.
- **`mergera1.py` beyond the lines I cited.** I did not read the whole 604 lines, and its `0 lines` for `gate71|1398|ra7|ra8` is a four-pattern grep, not a sweep. The brief says so.
- **Real post-squash develop shas and doc tails.** Only the trees are predicted. Tails `31` / `KS-591` come from KIT_REPORT §0.3.
- **The current R pane id.** Not read; R 9th was %81.
- **Payload applies at the post-merge develop.** Measured only at `147ae442`; disjointness from the gate73 and #1383 paths makes a clean apply expected, not proven.
- **`STANDING_LINES` "routing tokens not in subjects".** There is no standing line by that name. I grounded it in `send_brief.sh:136-151` and ledger rows, and named that source in the brief.

## Writes I made
- The brief and this report.
- In my scratchpad only:
  - `r10clone` (a `clone --shared --no-checkout`) and temp index files `idx_*`;
  - `lsr_r10.out`, `SKILL_147ae.md`, `sapply_r10.sh`, `stack_r10.sh`, `stack_ctrl.err`;
  - a `lockctl/.push-lock-zz` planted control.
- No mail, tmux, push, Linear or GitHub write.
- No write verb in the Secuura `.git`. The shared `rev-parse --all` was byte-identical before and after.
