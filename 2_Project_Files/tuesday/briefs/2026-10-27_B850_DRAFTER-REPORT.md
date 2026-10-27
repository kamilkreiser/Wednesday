STARTABLE: YES (with one precondition, Q-1: the builder pane Composer-J28 and its STATUS last line)

# B850 drafter report: Composer PR #99 round-2 gate kit (tier 1, Opus), seat G184

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B850_SEAT-G184_composer-99-round2-gate-tier1.md` (117 lines, 9 lines carry the four-underscore pattern: eight Stamp slots plus the last line; control: a planted scratch line counts 1). Drafted 2026-10-27 21:0x to 21:2x AEDT, read-only; no vitest, container, image or mutant was run.

## BLUF
- The kit re-runs every round-1 cell on head `cca0f6cb` (C1-C7) with three files side by side per mutant (main's blob, round 1's blob `a6416fac`, the new blob `954f7c9f`), verifies the builder's 102-id table (82 named-new / 20 old-red / 0 green) and "old-row verdicts equal main's on every mutant" independently, and adds a tier-1 section C2g of shapes the builder did not write (other control and format characters, astral and lone surrogate, content/target changes inside the DROP text and flags, line-feed and lone-CR splits, CR on prose lines of the section versus outside it, heading and fence variants, duplicate cat/redirect lines with NBSP).
- Round count: this is round 2 of 2 on class (a) of PR #99; a Major of the class is `NO GO round 2 of 2` and a STOP under the G-cap, never a third round. The landing section is B845's, moved to head `cca0f6cb`, with a body written from both commits' messages and one attribution line.

## Facts re-measured (instrument, control)
- `ls-remote` (21:0x): main `cbe86ba6`, branch = `refs/pull/99/head` = `cca0f6cb`, merge ref `7351d8f3`; `b850*` absent; control `b822*` printed `c6246c67`.
- `pulls/99`: open, not draft, `mergeable_state` clean, 2 commits, +269 -0, 1 file; `compare dc16530a...cca0f6cb`: ahead 1, +115 -12, the one path. Merge ref parents `cbe86ba6`+`cca0f6cb`, tree `bb2d5bea...` equals the head commit's tree (both read by `gh api -X GET`).
- Raw contents hashed with `git hash-object`: head test `954f7c9f...` 811 lines 13 `it` (equals the builder's blob); `dc16530a` `a6416fac...` 708/13; main `ef544f90...` 542/10; `DEPLOY.md` at main `8359bace...` (control: the three blobs differ from each other).
- Check-runs on `cca0f6cb`: CodeQL, Analyze (javascript-typescript), Analyze (csharp), all completed/success; open alerts on the PR ref 0; PR-ref analyses 4 rows (2 per commit, results_count 0, no error); control `ref=refs/heads/main` returned 3 rows with `per_page=3`.
- Identity: author/committer domains of the fix commit are the GitHub noreply domain; the round-1 commit's are a `.localdomain` host (count read by program; the name was not printed). Control: `cbe86ba6`'s message holds `localdomain` once (count 1).
- Round frame: loop over `Briefs/*_STATUS.md` first lines: 245 files, 32 with `GATE VERDICT`; hit list B331 B335 B779 B787 B815 B845 (control: B815's first line matches). B845's first line says STOPPED (no verdict); the ruling file records NO GO round 1 of 2.
- Port block: word-boundary scan of the 145 non-`.pre-` SEAT kits of 26-27 Oct (`xargs grep -l -w -E '946[0-9]'`, from a file list; control `892[0-9]` = 2 kits and `941[0-9]` = 2 kits) plus `lsof -nP -iTCP:9400-9999 -sTCP:LISTEN` (nothing listening). **No decade of 9400-9999 is free of kit mentions; 9460-9469 has 1 hit (an old finished Composer gate kit quoting its own lsof line)**, 9450-9459 also 1 (an old finished MPS gate kit). Chosen 9460-9469. A first scan with `mapfile` returned a false zero (the host bash is 3.2: no `mapfile`), caught because the `892[0-9]` control printed 0; the kit's HOLDS now says so.
- Panes: `%96 Datasec/NexusAI-M25`, `%95 Datasec/MPS-G183`, `%94 Datasec/Security-Composer-J28` (builder still open), no G184 pane. Load1 2.41 at 21:04. `.tools/b850` and `.tools/wt-b850-*` absent (control `.tools/b781` lists). G184 unused: word-boundary scan of `briefs/` printed nothing (control `G182` printed 3 files).
- Model: G1 row `model-routing.md:108`, G-cap `:111`; `levels.opus.model_id` = `claude-opus-5-5` (`models_latest.json` lines 17 and 37). The G1 row's "Opus 4.8 only if the session is stopped by 5.5's safeguards: switch THAT session" is carried into REFUSE 7.
- Landing source line `CLARIFICATIONS.md:1799` contains the quoted sentence (count 1).
- Text hygiene of the kit: a Python scan for a person's first name, surname, `for tuesday` (any case), `phase` found 0 after two fixes (it first found 4: a quoted ruling sentence naming the product owner by first name, two "FOR TUESDAY" strings, one "for Tuesday"); control: a planted line with all three terms returned all three. Non-ASCII 0, CR 0, tab 0.

## D-decisions (mine)
- D-1: kit section for the hand-off is named FOR THE COORDINATOR (you banned the old name in any text that may reach a record).
- D-2: the `lostBy` loop in W and G (65,536 code units, twice a row) is a timing risk, so C3 records row durations from the JSON reporter (Note over 1000 ms, Major over the 5000 ms default).
- D-3: the C2c family is the builder's K family restated as a PROPERTY with "at least these" and the gate must count its own ids; C2g is the part the gate must invent.
- D-4: the shared no-CR assertion (W and G red for a CR on any prose line of the 0021 section) is posed as a grading question with two outcomes (Note if a CRLF-saved document is the real case; Minor class (b) if a CR-only prose edit reddens a pin that guards nothing), not decided by the kit.
- D-5: both the builder's and the previous gate's TEXT evidence are readable as claims; their drivers are not. The gate writes its own generator.
- D-6: the hard stop suggestion is 150 minutes target, 210 minutes hard stop, because roughly 400 three-file no-database mutant runs plus the group and unit chain.
- D-7: the squash body uses the head's wording where round 1's sentence changed ("with only runs of spaces and tabs free" instead of "(spacing aside)"), so it stays true; C5 grades it.

## Q-questions for Tuesday
- Q-1: the builder pane J28 is still open and its STATUS last line still holds a template word where the final CodeQL read goes (`SECOND_READ_FINAL`; the STATUS body also has `SECOND_READ_PLACEHOLDER`). Default: launch only after J28 is closed and its last line is final; the kit's REFUSE 3 treats a live J28 as not the gate's and refuses only on a moved head.
- Q-2: ports 9460-9469 have one stale mention in an old finished kit, and no decade is hit-free. Default: accept 9460-9469 (the gate publishes no port anyway).
- Q-3: B845's own STATUS first line reads STOPPED, no verdict; the NO GO round 1 of 2 lives in the ruling file. Default: the gate cites the ruling and prints B845's first line; the round count stays 2 of 2.
- Q-4: the PR title and body still describe the round-1 head (+166, baseline 524 +3, "spacing aside"). Default: the gate grades them Minor and Tuesday edits both before landing; the kit's LANDING section says so.
- Q-5: the squash subject keeps round 1's wording (it is still true of the head). Default: the gate's C5 may offer a different subject; Tuesday settles it at landing.
- Q-6: the round-1 gate never ran C3 (counts), C6(b) (overlap) and C7 (Jira read); the ruling said the round-2 gate owes them. They are in this kit. Default: keep.

## UNMEASURED
Whether the head rows are green at the document and each family id red on its row (builder claims only); the effect of each mutant on bash and on psql; whether `lostBy` is fast enough on a loaded host; whether GitHub's squash with an explicit `--body` suppresses the `Co-authored-by` line for the first commit's author (the post-merge `localdomain` = 0 check is the instrument); the exact count of lines added per category.

## Outside-the-fences disclosure
Read-only throughout: Read tool on the kit files and on the Composer STATUS files named; `gh api -X GET` under the project `GH_CONFIG_DIR` (pulls, commits, compare, check-runs, code-scanning, raw contents saved to the session scratchpad); `git ls-remote`; `lsof`; `tmux list-panes`; `uptime`; `/usr/bin/grep` and a Python scan of my own kit; a loop over STATUS first lines. Scratch files (kit list, scans, three raw contents of the test, `DEPLOY.md` copy) are in the session scratchpad only. Two Bash calls were refused by the no-`cd` hook (my command text held the word); re-issued without it. I read no decision card, no `briefs_staged`, no ledger, no scoreboard, no non-Datasec tree, no `.env`, no SOW; I opened no `.tools` tree and no driver of any kit. Written: the kit and this report only.
