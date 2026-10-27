STARTABLE: YES (head 2c845c88 and main bdcfde7b re-measured, `b879*` absent, G195 and 9980-9989 free, CI 3 of 3 complete and green with 0 alerts, 0 overlap beyond the companion PR #101; one stamp-time action wanted: Q1, the shared project heavy lock, which the B878 kit does not yet name)

# B879 drafter report (SEAT-G195, Composer, tier-2 gate of PR #102, round 1 of 2 on its own class)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-28_B879_SEAT-G195_composer-102-routeb-prose-cr-gate-tier2.md` (109 lines). Drafted 2026-10-28 08:24-08:4x AEDT by the read-only drafter (Opus 5.5). Shape cloned from B864 and B845 (both read whole); substance from the builder kit B876 (read whole with its stamp) and B876_STATUS.md (read whole, as claims).

## BLUF
- Gates part B of B876: PR #102 `b876/composer-routeb-prose-cr-reading` @ `2c845c88`, one commit on main `bdcfde7b`, one path (the b778 test), +11 -1. Main's line 311 (a whole-section comparison) is replaced by a fence-to-fence comparison plus three in-helper expects. Tier 2, routing row G2 (`model-routing.md:109`), Sonnet `claude-sonnet-5-5`, round 1 of 2 on the class "the shared reading assertion reads more than the rows pin". That count comes from the product owner's 28 Oct ruling, option a.
- Seat G195. The B878 kit, now on disk, took G194, so G195 is the second-lowest free number. Ports 9980-9989, the HIGHER of the free blocks. B878 took 9010-9019, so the two do not collide.
- The heart is a sweep, not the builder's 25 ids. It plants a CR at the end of every line 152-262, plus lines 1, 263 and 628 (114 ids), and runs main's file, B's file and the combined A+B file in ONE vitest call per document. Around the sweep sit K-shapes: two CRs, every outside line at once, a CR at the start or middle of a line, and non-CR edits whose verdicts must stay equal to main's.
- **New over the builder: c5a-c5d test whether the in-helper expects can FAIL.** In c5a, `fenced` returns the whole section. In c5b, `fenced` strips the CRs. In c5c, `crAt` plants nothing. In c5d, the slice narrows to exclude the fences. The builder's c2 only put the old line back. The kit also predicts that c5d escapes every in-helper expect, which is a Note: fence lines are markdown, not commands.
- Combined tree: the expected blob is `65455984281d09aa6520a837a72ed012482e1807` (1002 lines, 15 `it`). The gate must reproduce it, pass it 15 of 15 x3, and show A's two rows 0 red on every outside CR. A's own property is left to B878.
- `DEPLOY.md` is out of lane per Tuesday's B876 stamp Q1. It holds no CR or CRLF wording, so B owes no document word.
- Main moving because PR #101's squash lands is written as an expected move, not a STOP: the path list must be exactly the test and the blob must be A's `e983f6a3`.
- Launch line: `WED_USAGE_STOP=100 bash .../launch_when_cool.sh ... "WED_USAGE_STOP=100 BRIEF_SEAT_LEVEL=sonnet bash ...brief_seat.sh ..."`, with the variable both outside and inside the quotes.

## Facts re-measured (instrument; control)
- `ls-remote` 08:24: main `bdcfde7b90a5e0022bf50f639de2db85b51e44a3`; PR #102 head `2c845c8894ce2727109021b1d7ebed93a66505df` (= branch), merge `dd419633...`; PR #101 head `6d6df558ae4b206558403f2ffdb9b1960f959c6f` (= branch), merge `0b082b17...`; `b878*` and `b879*` absent. Control: `b839*` prints `cca0f6cb...`.
- `pulls/102`: open, non-draft, mergeable, created 08:22 AEDT, 1 commit, +11 -1, 1 file. `mergeable_state` was `blocked` at 08:24 and `clean` at 08:27. The commit has one parent (`bdcfde7b`) and tree `b98840f6...`; the merge ref's tree is equal to it. Author and committer domain are `users.noreply.github.com`, with `localdomain` count 0 (control `dc16530a`: 1) and 1 trailer. Title, body and message are quoted in the kit FACTS; there is no key, name or number in them.
- check-runs on `2c845c88`: at 08:24, 2 runs `in_progress`. At 08:27, 3 of 3 (`CodeQL`, both `Analyze`) completed success. Analyses on `refs/pull/102/head`: 2 rows, results 0, no error. Alerts open/fixed/dismissed: 0/0/0. Control: main analyses returns rows.
- Ruleset (`rules/branches/main`): CodeQL code_scanning thresholds (errors / high_or_higher); required_status_checks empty with `strict` false; `allow_update_branch` false. So #102 needs no update after #101 lands.
- Raw blobs, hashed:
  - test at main `954f7c9f` (811 lines, 13 `it`), at #102 `d9ae972b` (821, 13), at #101 `e983f6a3` (992, 15).
  - `diff` main vs #102: one hunk, the single removed line is main's 311, 11 added.
  - The head file has 0 non-ASCII, 0 CR and 0 tab (python byte count). `/usr/bin/grep -P` failed on macOS first and was replaced.
  - `DEPLOY.md` is `8359bace` at both refs. `package.json`, the lock, `vitest.config.ts`, b616 and `support.ts` are equal at both refs.
- Combined file: `git merge-file -p` on scratch copies, both orders, gives rc 0 and blob `65455984...`. Against A's file it differs only by B's 12-line hunk.
- `DEPLOY.md` 150-264 read: section 153-261, fences 198 and 209, Proven-on 241-260, next heading 262. `carriage|CRLF|line feed` count 0 (control `Route B` 27).
- Mechanism read at source: `routeB` splits on `\r?\n`, `exactBlock` on `\n`, with the same length and indexes. So only a CR right before a line feed can differ between them, which is the basis of the K-POS class split.
- PCOMP-107 read in-process with `jira791.get`: Backlog, `plan-comp-397`, 0 comments. Done-when quoted verbatim in the kit. Controls: `GR-cr-261` is in the description; `PCOMP-999999` gives 404.
- Overlap: #101 shares the path (the companion, by design). #95, #91, #86 and #85 have 0 on the test path, `DEPLOY.md` and `packages/db/` (control: #95's b712 path 1). #101 is `clean`, with CI 3 of 3 success.
- Ports: the word-boundary scan over the 112 non-`.pre-` 27/28 Oct SEAT kits, run from a bash script, found the free decades 9770-9799, 9810-9829, 9920-9939 and 9970-9989; `998[0-9]` printed 0 (controls: `991[0-9]` 1, `996[0-9]` 3). `lsof` printed 0 lines on 9920-9939 and 9970-9989. Listener control: bound on 9989, listed with 2 lines, 0 after close.
- Seat: `G194`..`G200` show 0 hits in any 26-28 Oct brief file (control `G193` 12). B878's kit, which appeared at 08:35, is `SEAT-G194`, so B879 = G195.
- Panes at 08:26: `%0 tuesday`, `%124 Datasec/NexusAI-M53`, `%122 Datasec/HPSM-POC-D40`, `%1 fleet-monitor`; no Composer pane. Load1 6.43.
- Round frame: 251 STATUS files, 34 `GATE VERDICT`. Hits: B331, B335, B779, B787, B815, B845, B850. None is on PR #102, b876 or PCOMP-107.
- Routing: `model-routing.md` :108 G1, :109 G2, :111 G-cap; `models_latest.json` sonnet id at lines 23 and 38; `brief_seat.sh:24` defaults to opus.
- Landing: `CLARIFICATIONS.md:1799` (count 1; lines 1862, 1885, 1910, 1934 and 1958 repeat it; control 0).
- CI: `test-db.sh:4` `set -euo pipefail`, `:58` both vitest configs chained with `&&`; `ci.sh:28` `step()`, `:34` `if "$@"`, `:118` the db step.
- Card `composer-106-107-routeb-residue-round-1028`, read by `show` into a scratch file (id count 1): ruled `a` at 07:15:22. The kit quotes option a's label and detail without the card id.

## D-decisions
- D1 Seat G195: the second-lowest free G, since B878 took G194 (confirmed on disk 08:35).
- D2 Ports 9980-9989: the highest of the free blocks, by the commission's instruction.
- D3 The project heavy lock is `.tools/composer-heavy.lock`, an `mkdir` taken after the existing cross-seat `ps` gate and the seat lock, with a holder file, the `ps` gate re-read after taking it, and release by move only when the holder names B879. It is declared as adaptation (iii) of the copied `heavy.sh`, and the seat never breaks a lock held by another seat. Composer has no project-level lock today (`ls .tools`), and `heavy.sh`'s `ps` gate is not atomic.
- D4 One vitest call per mutant over THREE files (main, B, A+B), so the NEW-vs-OLD verdict diff and the A-rows-on-outside-CR check come from the same run.
- D5 The CR sweep covers every line from 152 to 262, not the builder's 25, because the property is stated over "any line".
- D6 The in-helper controls are graded as follows:
  - A c5a or c5b that cannot fail is a Major of class (c).
  - A c5c that cannot fail is a Minor.
  - The c5d result (the narrowed slice escaping every in-helper expect) is a Note.
- D7 Wording: "though no row reads that line" (commit and PR body) is literally false for lines 241-260, which the Proven-on row reads with the CR dropped. It is graded Minor when the behavioural claim holds, and Tuesday rewrites the squash body ("pins", the ticket's word). "Two controls" against three expects goes to the gate to grade.
- D8 The escalation (G2 to G1) is security-shaped only if B loosens a CR on a line bash reads (lines 199-208) to green on every row.
- D9 LANDING: #101 first, then #102. The post-merge blob check is `65455984` when A's squash is the parent, or the head tree when #102 lands alone.

## Q-questions for Tuesday (each with a default)
- **Q1 (DO NOT accept the fallback): the project heavy lock.** The B878 kit (123 lines at 08:35) names only `.tools/b878/lock` and the `ps` gate. On its own, the `ps` gate lets two waiters start in the same instant. **Default: at B878's stamp, Tuesday adds the same path `.tools/composer-heavy.lock` (mkdir, holder file, release by move, never break another's) to B878, and confirms it in B879's "Stamped by" slot.** Fallback if B878 is stamped unchanged: B879's lock binds only itself and the two gates can overlap heavy jobs. That breaks the commission's "never run heavy jobs together", so Tuesday should not accept the fallback.
- Q2: Round 1 of 2 on its own class, from the product owner's 28 Oct ruling and the B876 stamp. Default: accept.
- Q3: Main moving by #101's squash (exactly the test path, blob `e983f6a3`) is not a STOP, and C2e/C6 re-base on it. Default: accept.
- Q4: The grading in D6 and D7 (c5c Minor; the "reads" wording Minor). Default: accept.
- Q5: Launch spacing: start the B879 waiter only after the B878 waiter has exited and its launch is verified (`launch_when_cool` refuses a second live waiter anyway). Default: accept.

## UNMEASURED
- The drafter ran no vitest, container, image build or mutant. Every C2 prediction (outside green, inside red, K-POS equal, the c5 results, A's rows 0 red) was read from source only.
- What bash does with a CR on a command line.
- The B878 kit's final text at its stamp (it may still change).
- `ci.sh:117` (relayed from B876).
- The `cbe86ba6` localdomain control (relayed from B864).
- Whether the B850 `mutant-table.tsv` cells beyond the 8 rows read match the gate's.

## Outside-the-fences disclosure
- Read-only throughout:
  - Files: DRAFTER_RULES.md, the B876, B845 and B864 kits whole, B876 STATUS whole, the B864 drafter report, the B845 addendum, `.tools/b781/scripts` heavy/common/nodeonly/dbone whole and names.py 1-20, the jira791.py header and functions, model-routing, models_latest, brief_seat.sh 20-28, launch_when_cool.sh 1-40, CLARIFICATIONS:1799.
  - The B878 kit, read by grep only, for its seat, ports and lock.
  - The B876 evidence folder listing; B850's `mutant-table.tsv`, 8 rows.
  - Commands: `gh api -X GET` under the Composer GH_CONFIG_DIR, `ls-remote`, `cat-file -t`, `config --get core.sshCommand`, `lsof`, `tmux list-panes`, `uptime`, and a STATUS first-line loop.
- The Jira read imported `jira791.py` from a scratch script run with plain `python3` (not `-I`) so that `sys.path` could take the client's folder. It made GET calls only and printed no token.
- `decision_queue.sh show` was used once, with the exact Datasec id, into a scratch file; no `list`.
- **Scratch collision:** at about 08:35 my scratch file `card.txt` was overwritten by another process with a different Datasec card (NexusAI RD-897), probably a parallel drafter sharing the scratchpad. I did not act on it. My measurements had already been taken from files hashed at fetch time.
- One zsh hook refusal on an `=====` separator; I re-ran with `----`.
- No `cd`, no `rm`, no write in any project; no az, docker, ssh, mail, card or post. Files written: the kit and this report only.
