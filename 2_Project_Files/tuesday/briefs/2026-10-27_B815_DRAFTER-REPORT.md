STARTABLE: YES (after you resolve D-1/Q1 below, which is a stamp decision and not a blocker, and after the builder pane J25 is closed or the 10-minute wait in REFUSE 3 runs out)

# B815 drafter report: gate kit for PR #97 (Composer, Route B pins), seat G172, tier 1

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B815_SEAT-G172_composer-97-routeb-pins-gate-tier1.md` (89 lines). Drafted 11:27-11:4x AEDT.

## BLUF
- The kit gates PR #97 head `6f75c2d196c433154cfcc92721bf3d89c855c05b` on main `422ecf373e866728348a76d5854d864f591dd35d`, Opus, tier 1 (row G1 `model-routing.md:108`), round 1 of 2, ports 9020-9029, pane `Datasec/Security-Composer-G172`. Four-underscore line count in the kit: 9 (eight slots plus the last line), 0 non-ASCII, 0 at-sign tokens, no person's name, no card id.
- Three things you should know before stamping. (1) **The PR title and body overclaim**: the title says the change will "pin the write command's protective words" and the body says rows E and P make a guide that "drops or reorders the write command's protective words" turn red. Rows E and P pin the stop line and the Proven-on words; the write/drop/apply text was already pinned by row R1 before this PR (the three constants and R1 are byte-equal in the diff). The squash subject will be this title. C7 grades it, and the kit tells the gate to quote suggested words (the commit title). (2) **The pins are `line.includes(text)` substring matches** (test lines 17-19, 64, 84-85) and the builder's census only deletes lines or swaps a word for `XQX`, so an appended override such as ` -v ON_ERROR_STOP=0` after `-q`, or `|| true`, or a duplicate first match, is outside its census; the kit's C2(b) adversarial set A1-A12 measures them. (3) **The round count is 0 of 2 only by your ruling (b)**: grep finds two NO GO gates (B779, B787) on the old branch, and B787's class text ("... or says more than a run shows") overlaps this class. The kit states that openly (Q-4 in the Stamp).
- CodeQL is already done on the head: three check runs completed success, two analyses with results_count 0, 0 alerts. The gate re-reads them three times.

## Facts re-measured, with instruments (all by me, read-only, 11:28-11:32 AEDT)
| Fact | Instrument | Control / note |
|---|---|---|
| main = `422ecf37...`; head = `refs/pull/97/head` = `6f75c2d1...`; merge ref `c3c42b04...`; `b806*` present, `b815*` absent | `git --no-optional-locks ls-remote` | `b778*` and `b806*` print their branches |
| PR #97 open, non-draft, mergeable true, state `blocked` at 11:28 then `clean` at 11:32; title differs from the commit title | `gh api -X GET pulls/97` | state flipped as checks completed |
| compare: ahead 1, behind 0; DEPLOY.md +14 -6; test +124 -0 | `compare/422ecf37...6f75c2d1` | matches builder |
| merge ref parents = `422ecf37`, `6f75c2d1`; merge tree = head tree = `49e93d1a...` | `commits/<sha>` `.commit.tree.sha` x2 | the squash tree will equal the head tree while main is unmoved |
| check runs: CodeQL, Analyze (javascript-typescript), Analyze (csharp) all completed/success; analyses 2 rows results_count 0 error empty; open alerts 0; all-state alerts 0; merge ref analyses 0 and no runs | `check-runs`, `code-scanning/analyses`, `alerts` | `analyses?ref=refs/heads/main` length 30 (control returns rows) |
| DEPLOY.md head 628 lines blob `8359bace...`; main 620 lines `8c5a3fc3...`; diff is exactly `223,227c223,235` and `250c258` | raw contents + `diff` + `git hash-object` | main blob equals the builder commission's blob |
| test head 542 lines blob `ef544f90...`; main 418 `314f0ba1...`; diff 4 insert hunks 6+65+10+43 = 124, zero removed | same | |
| six "Nothing pins Route B's command." at head 310, 351, 397, 451, 511, 559 (main +8 shift) | `/usr/bin/grep -n -i -F`, `-c` head 6 main 6 | `zzz-no-such-string-7f3a` 0 |
| `completeness check` 5 at head / 2 at main; `tail -n 6` 3 / 2; `one-step command of 0019` 1 / 0; `Route B with the command above it` 0 / 1 | `/usr/bin/grep -c -i -F` | the builder commission's "2" is the sub-section's count; the document-wide count rose to 5. The kit's REFUSE 6 carries the corrected numbers |
| added lines non-ASCII: 0 in DEPLOY.md, 0 in test | `diff | LC_ALL=C /usr/bin/grep -c '[^ -~]'` | I ran no planted-byte control (UNMEASURED control; the kit asks the gate for one) |
| 0019 section heading at head line 60; the one-step command at lines 101-102; the refusal text at 190-193; `### Proven on` at 233 | `sed -n` / `grep -n '^## '` of the raw head file | row 250's claim reads consistent with lines 190-193 |
| round count: 237 STATUS files, 29 with `GATE VERDICT` first line, 4 match the class regex (B331, B335, B779, B787), none on b806 | shell loop over first lines | control: B779 first line matches. The B724 file used as control in older kits is not in this folder |
| ports 9020-9029: `lsof` rc 1; word-boundary scan of 110 non-`.pre-` SEAT kits of 26/27 Oct: 0 hits | `lsof -nP -iTCP:... -sTCP:LISTEN`; `/usr/bin/grep -l -w -E` | the same scan for `8920-8929` lists the B806 kit; no listener control run |
| panes 11:29: tuesday, NexusAI-R61, HPSM-POC-H45, Security-Composer-R60, MPS-R59, HPSM-POC-G171, Security-Composer-J25, HPSM-POC-D37, fleet-monitor | `tmux list-panes -a` | |
| no `.tools/b815`, no `wt-b815-*`, no `pc-b815-*` image; builder images `pc-b806-node:head/final` exist | `ls -d`, `docker images --format` | `ls -d .tools/b626` lists |
| plumbing `.tools/b781/scripts/` 7 files (21/74/13/42/49/10/31 lines); `dbone.sh` line 10 already mounts DEPLOY.md | `wc -l`, `grep -n` | |
| model: G1 `:108`, G-cap `:111`, `claude-opus-5-5` at `models_latest.json` lines 17 and 37; `brief_seat.sh` line 24 defaults to opus | `sed -n`, `grep -n -F` | |
| landing source `CLARIFICATIONS.md` line 1799 holds the squash/pinned-to-head sentence | `sed -n 1799p | grep -c -i -F` = 1 | |
| load averages 4.05 4.77 5.79 at 11:32 | `uptime` | |

## Design of the kit (how it differs from B779/B787)
- THE CLASS is stated as a property with six limbs (a)-(f), including PR/commit text and the "Nothing else" sentence.
- C2 is the heart: the gate writes its own census (about 90 variants, check and stop lines included as controls) and compares it with the builder's 31 red / 62 green, then an adversarial set A1-A12 aimed at the substring-match construction (appended overrides, duplicate first match, inserted lines between the stop line and the DROP line, container name, grouping, implied-by-other-words sentences in the Proven-on text, a full stop inside the scoping text). Grading is by what the paragraph and the commit actually claim (a substring pin is Minor with ticket text; Major if any sentence says the flags are protected).
- C3 re-runs the PCOMP-100 variants against the old and new test (M30, M30b, M30c, M33, M35, M35b, M37), the full B787 regression list as the gate's own plain swaps, and the round-1 lazy-check variants. It records that M30b is already red at the old test (builder's correction L1) and that row E's in-row controls run on literals.
- C4 is the row 250 words and width; C5 the scanner scratch (the block holds its own `psql`, so the old "no psql block throws" control changed); C6 suites and names; C7 words, PR text, merge tree equal to head tree, overlap, CodeQL, claims.
- Because the check line is byte-equal to main's, the round-1 behaviour matrix is not repeated (NOT TESTED BY DESIGN), with a one-row smoke in C3.
- The launch line carries `BRIEF_SEAT_LEVEL=opus` inside the quotes.

## D-decisions (mine, made in drafting; strike any at the stamp)
- D-1: ROUND COUNT states "0 of 2" with the overlap disclosure and cites your ruling (b) instead of silently asserting 0. This is the honest reading of the grep.
- D-2: The PR title/body overclaim is made a gate cell (C7) with a two-level grade (Minor; Major only if the title survives as the squash subject), and the kit says the fix is Tuesday's title edit, not a code change, so it cannot by itself send the branch back.
- D-3: The gate may not run `git add`/`commit`/`stash`/`clean` in the root repo, because its untracked STATUS and evidence sit in the root repo that the records seat R60 commits to. The partition names it from both sides, but R60's side is a request to you (see Q3).
- D-4: Plumbing is copied from `.tools/b781/scripts/` (as the B806 builder did) because `dbone.sh` there already mounts DEPLOY.md; the kit therefore declares fewer adaptations than B779.
- D-5: REFUSE 3 treats a live J25 pane as "wait up to 10 minutes", not an immediate refuse, because you told me it is being closed; a second commit by J25 is a moved head (REFUSE 2).
- D-6: Docker fence: only `pc-b815-*` objects; no prune of any kind; the builder's `pc-b806-*` images are named as not the gate's.
- D-7: Budget about 20 container starts; no behaviour matrix of the check line; no `apps/api` group.
- D-8: Verdict first-line template drops the old C2 "cut points" cells and replaces them with census/adversarial/ticket-variant cells.

## Q-questions for Tuesday (each with a default)
- Q1: Do you keep the PR title as is, or edit it before the gate reads it? Default: leave it; the gate grades it and you decide at landing (a Tuesday edit of title and body is not a code change and does not need a round).
- Q2: Unit step SOW text bind mount (stamp Q-2 in the kit). Default: YES (read-only, `--network none`, never opened), as in B779.
- Q3: Tell R60 (records seat) to stage by explicit path only, so the untracked B815 STATUS/evidence in the root repo is not swept into a records commit. Default: yes, one line in its pane.
- Q4: Accept the round-count reading "round 1 of 2 under ruling (b), with the B787 overlap disclosed". Default: accept.
- Q5: Close J25 before launch, or let the gate wait 10 minutes. Default: close it; the wait is the backstop.
- Q6: Hard stop. Default: target verdict 150 minutes and hard stop 240 minutes after the seat's own Step 0.

## UNMEASURED
- Not run by me: any build, test, container, mutant, census, the check line itself, `psql` override behaviour (A2), prettier on row 250, the `b616` scanner on the new head, gitleaks, `packages/db` group counts, `unit.sh ci`. All builder numbers (10 of 10, 39/524, 55 of 55, 93 variants, 311 files / 3106 tests, 86-character cell) are RELAYED.
- The substring-pin concern (L8, A1/A2/A4/A5/A6) is a reading of the test source (`line.includes`), not a run. The `psql` last-`-v`-wins claim is from knowledge, not measured; the kit tells the gate to measure it.
- No positive control was run for: the non-ASCII count on added lines, the port `lsof`, and the `docker images` count; the kit asks the gate for controls on each.
- Open-PR file lists for #95, #91, #86, #85 not listed by me (the builder reports 0 shared paths, RELAYED). Live `b8*` branches were listed by name only.
- The `mergeable_state` flip from `blocked` to `clean` is observed, not explained; it may be the checks, or a required-review rule that I did not read.
- The B806 STATUS first line still reads `STATUS B806: PENDING` (last line is READY FOR QA); harmless to the watcher, noted as L7.

## Outside-the-fences disclosure
- I stayed inside the fences: read-only outside my two files; no `decision_queue.sh`; no `fleet/briefs_staged/`, scoreboard, ledger or Wednesday/Friday tree; every `gh` call was `-X GET` under the Composer `GH_CONFIG_DIR`; git in the project repo was `ls-remote` and `config --get` only; no HTTP to any hosted or demo host; no Artifact/Docs/mail tool; no az/ssh/docker run (`docker images --format` only lists local image names, which is a read of the local daemon, not a run).
- Two slips, both harmless: (1) my first Bash call contained a `cd` and the hook refused it, nothing ran; (2) I wrote the raw file copies and a `.py`-free set of scratch outputs into the session scratchpad (`/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/5763a99f-d3dc-49d0-84f9-4fe29e51ff2d/scratchpad/`: `deploy_head.md`, `deploy_main.md`, `test_head.ts`, `test_main.ts`), which already held other drafters' files; I did not read or touch those.
- I read the QA charter path only by `ls` (exists); I did not open it. I read the earlier gate kits, the builder kit and the builder STATUS whole or in part as listed in the kit's SELF-CHECK. The builder's evidence `runs/` text files and the B779/B787 STATUS bodies were not opened beyond first lines and a grep of B787's findings lines.
