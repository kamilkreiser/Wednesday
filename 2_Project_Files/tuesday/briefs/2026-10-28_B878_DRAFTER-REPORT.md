STARTABLE: YES (Q-1 and Q-3 want Tuesday's own eye at the stamp; Q-3's default should not be accepted unread)

# B878 drafter report: Composer PR #101 round-3 gate kit (tier 1, Opus, the LAST round on class (a)), seat G194

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-28_B878_SEAT-G194_composer-101-routeb-copies-gate-tier1-round3.md` (123 lines, 9 lines carry the four-underscore pattern: eight Stamp slots plus the last line; control: a piped `x____` line counts 1). Non-ASCII 0 (one U+2026 found by a python scan and reworded), CR 0, tab 0; a person-name scan (`kam|kreiser`) 0 (control: a piped `kam` counts 1); the decision-card id 0. Drafted 2026-10-28 08:23 to 08:3x AEDT, read-only; no vitest, container, image, probe or mutant was run.

## BLUF
- The kit gates PR #101 (`6d6df558`, one commit on main `bdcfde7b`, one path, +181 -0) as **round 3 of 3 on class (a), the last**, under the product owner's 2026-10-28 ruling. It re-runs the builder's whole battery with the gate's own text swaps, two files side by side per vitest call (main's 13-row file and the head's 15-row file): the ticket's 12, the builder's 100 closed-list ids re-derived, the B850 closed list as regression, an OUT-gap census, controls c0-c6 including six in-test stubs.
- One step past the named list (C2g): near-copies at EVERY gap (the builder placed them only right after the real line), copies split by backslash-newline (a duplicate in bash that `includes` cannot count), other invisible characters at the ends of copies, more after-apply shapes, function shadows at the four gaps no row reads, commented copies, fence variants, and the `statusAt` docblock edge.
- Because no fix round follows, the kit requires an **ACCEPTED-RESIDUE TABLE in every verdict** (id, edit, IN/OUT, cells on both files, stub-probe bash effect, grade), written so a records seat can paste it.
- Binding from Tuesday's B876 stamp, written into the kit: `DEPLOY.md` is out of lane; its pin paragraph understating the pins is a FOR TUESDAY note, never a finding. PR #102 is not graded; the combined tree is a one-line Note (C6(e)).

## Facts re-measured (instrument, control)
- `ls-remote` 08:23:56: main `bdcfde7b...`; `b876/composer-routeb-copies-and-status-line` = `refs/pull/101/head` = `6d6df558...`; merge ref `0b082b17...`; `refs/pull/102/head` = `2c845c88...`; `b878*`/`b879*` absent; control `b839*` = `cca0f6cb...`.
- `pulls/101`: open, not draft, mergeable true, `mergeable_state` **blocked** (ruleset `code_scanning` waiting; `rules/branches/main` read: deletion, non_fast_forward, code_scanning CodeQL, empty required checks; no branch protection), 1 commit, +181 -0, 1 file. Merge ref parents `bdcfde7b`+`6d6df558`, tree `302e9579...` = the head commit's tree.
- Raw test blobs hashed (`git hash-object` = `contents .sha`): head `e983f6a3...` 992 lines 15 `it(`; main `954f7c9f...` 811/13; #102 head `d9ae972b...` 821/13. `diff` main->head: 0 removed, 181 added, three insert hunks. Eight other blobs equal at main and head (control: the test's shas differ). Non-ASCII/CR/tab in the head file 0.
- Commit message read whole (domain only printed: `users.noreply.github.com`; `localdomain` 0, control `dc16530a` 1). PR title and body read whole (quoted in FACTS).
- Check-runs 08:24: CodeQL completed/**neutral**, Analyze (csharp) success, Analyze (javascript-typescript) **in_progress** (PR opened 08:22:40). Analyses on the PR ref: 1 (csharp, 0 results). Alerts 0 in every state on PR, merge and branch refs (control: main all states 20).
- Overlap: #95/#91/#86/#85 share 0 with the test path, `DEPLOY.md`, `packages/db/`; #102 shares the test path (control 1), by design.
- Round frame: 251 STATUS, 34 `GATE VERDICT`; hits B331 B335 B779 B787 B845 B850 (control: B815's first line matches, 1).
- Card: `decision_queue.sh show composer-106-107-routeb-residue-round-1028` into a scratch file (id count 1; status ruled, choice a, ruled_ts 07:15:22). `CLARIFICATIONS.md` has no entry for it yet (last C-108, line 1948; 1969 lines). Line 1799 holds the landing sentence (count 1; control 0).
- Ports: word-boundary scan of the 112 non-`.pre-` SEAT kits of 27-28 Oct from a bash script file; free decades include 9000-9009, 9010-9019 and others (controls: `991[0-9]` 1 kit, `946[0-9]` 2, `985[0-9]` 2). `lsof` on 9000-9009 and 9010-9019: nothing (listener control on 9009: 2 lines, then 0). `git grep -w -E '900[0-9]'` at `bdcfde7b` hits `compose.yaml:72,130` (Composer's object store on 9000); `901[0-9]` 0.
- Seat: `G19[4-9]` in the 27-28 Oct kits 0 (control `G193` 12 files). Panes 08:27: `%0 tuesday`, `%124 Datasec/NexusAI-M53`, `%122 Datasec/HPSM-POC-D40`, `%1 fleet-monitor` (no Composer pane). Load1 5.19. `.tools/b878`, `.tools/wt-b878-*` absent (control `.tools/b781/scripts` lists). Plumbing sizes by `wc -l` match B876's.
- Model: `model-routing.md:108` G1 (grep `^\| *(G1|G2|G-cap) `), `:109` G2, `:111` G-cap; `models_latest.json` opus `claude-opus-5-5` lines 17 and 37; `brief_seat.sh:24` defaults to opus.
- **A builder claim contradicted by its own table (not by a run):** STATUS FOR TUESDAY item 1 calls the five `GI-*-nbsp-copy` shapes "green on all 15"; `table-A.tsv` shows four of them red on old rows on both files and only `GI-redirect-nbsp-copy` green on all 15. Put to the gate at C7.

## D-decisions (mine)
- D-1 Seat **G194** (next free G).
- D-2 Ports **9010-9019**. The lowest free block was 9000-9009, but Composer's own compose stack serves its object store on 9000, so a local stack could hold it. 9010-9019 is the lowest free block clear of that. **B879 must take a different block.**
- D-3 Two files side by side (main's 13 and the head's 15), not three: no earlier commit of this branch exists.
- D-4 The IN/OUT rule defines "a copy" as a line whose `pinned()` text holds the whole constant. A near-copy at an OUT gap is OUT but must still be measured and recorded. A copy split by backslash-newline is IN, because bash runs it as the duplicate (B850's G-2 already put "split" and "duplicate" IN).
- D-5 There is no fix round, so the GRADING carries no fix shape, only "what it leaves". The ACCEPTED-RESIDUE TABLE is mandatory whatever the verdict.
- D-6 LANDING (0) asks the gate to split a NO GO into "class (a) survivors only" and "the PR itself is wrong" (b/c/d/e, Blocker, CI). It does not decide landing.
- D-7 The combined A+B tree is a Note only (C6(e)): two CR mutants, and SIX/TAIL must stay 0 red.
- D-8 The section is named FOR TUESDAY, following the B864/B876 convention and the commission's wording, not B850's "FOR THE COORDINATOR".
- D-9 CodeQL `neutral` is never read as green. The gate waits for the javascript-typescript analysis.

## Q-questions for Tuesday
- **Q-1 (check before stamping):** B879 is being drafted in parallel and saw the same G193 maximum, so it may also have taken **G194**. Default: B878 keeps G194 and B879 renumbers. B879 did not exist on disk at 08:35, so I could not check.
- Q-2: ports 9010-9019 (D-2). Default: accept.
- **Q-3 (do NOT accept the default unread):** the ruling says "a NO GO ends it and the remaining shapes are recorded as accepted". It does not say whether PR #101 then lands. The kit only makes the gate split its NO GO cause (LANDING (0)) and leaves land-or-hold to Tuesday. Default: land on a NO GO caused only by class (a) survivors (the G-cap's "ship the closed instances"); hold on anything that makes the PR itself wrong. That reading of the product owner's words is mine, so Tuesday should confirm it against the card at the stamp.
- Q-4: if PR #102 lands before this verdict, REFUSE 2 stops the gate, because main moves on the test path. Default: keep the B876 stamp's order (A lands first, then B), so #102 waits for this verdict.
- Q-5: hard stop 210 minutes, target 150, after Step 0. Default: accept.
- Q-6: the IN classification of split copies (D-4) can produce a class (a) Minor and so a NO GO. Default: keep it. A Minor alone gives GO WITH FOLLOW-UPS; only a Major gives NO GO.

## UNMEASURED
- Whether the head rows are green at the document, and each id red where predicted. The builder claims it; nothing was run.
- What every G-series shape does in bash, and what psql answers.
- The final CodeQL conclusion for javascript-typescript.
- Row durations under load.
- The exact battery size and wall time.
- Whether B879's kit chose G194 or 9010-9019.

## Outside-the-fences disclosure
- Read-only throughout:
  - The Read tool on the drafter rules, the B876/B850/B864 kits, the B876 and B850 STATUS files and the B850 drafter report.
  - `gh api -X GET` under the Composer `GH_CONFIG_DIR`.
  - `git ls-remote`, `git cat-file -t` and `git grep` (read verbs, `--no-optional-locks`) at `bdcfde7b`.
  - `lsof`, with one short-lived `python3 -I` listener on 127.0.0.1:9009 as the control.
  - `tmux list-panes`, `uptime`, `/usr/bin/grep`.
  - `ls` of `.tools/` and of the B876 evidence folder.
  - `decision_queue.sh show` of the one exact Datasec card id into a scratch file. No `list` in any form.
- I listed the names of the files in `.tools/b876/scripts/` to name them as forbidden drivers. I opened none of them.
- Scratch files are in the session scratchpad only: the card, three raw test blobs, `DEPLOY.md`, the port-scan and frame scripts.
- Two Bash calls were affected by hooks:
  - One was refused for a `cd` and re-issued without it.
  - A second got an advisory on case-sensitive greps; the counts it touched had controls.
- I did not read:
  - `briefs_staged`, the scoreboard, the ledger, any WEDNESDAY or FRIDAY tree, or any non-Datasec project.
  - `.env`, `3_Access_Keys/` or any SOW.
- Nothing was written except the kit and this report.
