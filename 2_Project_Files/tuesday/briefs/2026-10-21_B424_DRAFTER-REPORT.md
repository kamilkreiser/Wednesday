BLUF: B424 tier-2 gate kit drafted (SEAT-G30, the B423 delta `e969ad38..85105729` only). Read-only: nothing fetched, pushed or run in a container. Seven questions for you below, each with a recommendation; none blocks stamping except Q1 and Q5 if you disagree.

# B424 drafter report · 2026-10-21 ~22:30 AEDT

## Files
1. Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-21_B424_SEAT-G30_composer-pr85-gate-tier2-round3.md` (129 lines). One slot, `@STAMP_TIME@`, on 2 lines (the Model line and the Stamp line). `grep -c -F` of the slot prints 2; the split-quote REFUSE-1 form prints 2 on the unstamped file, so the `.pre-stamp` control should print 2. Last line `READ-WHOLE-BY-TUESDAY: PENDING`.
2. This report.

## Read, in order
B423 STATUS (whole), B423 brief (whole, with its stamp rulings), B358 STATUS (whole, 551 lines), B358 brief (whole), the charter (whole), `BRIEF_TEMPLATE.md` (whole, for 2a), `model-routing.md` rows G1-G3 (grep), the gate-33 launcher's pane census lines (grep + `:683-740`). Not read: the B358 kit's scripts (listed only), the builder's kit or evidence, `.env` beyond a name count.

## Measured (read verbs only)
| fact | value | instrument, time |
|---|---|---|
| branch / `refs/pull/85/head` / main | `851057291ffb019baee6c3c51a50d7b8833f5b3a` / same / `308b7aa60cd8d2a8576b29e0422538cbaf140f24` | `git --no-optional-locks ls-remote origin …`, 22:24:23 |
| PR | open, draft, `mergeable_state` clean, 14 commits, 57 files, +38887/-3186, base `308b7aa6…` | `gh api …/pulls/85` (GET, project `GH_CONFIG_DIR`), 22:24 |
| delta | exactly 2 paths: qgate test +32/-2, label-run test +48/-0; 2 commits `48414956`, `85105729`, author `kamilDatasec`, one Sonnet trailer each | `git diff --numstat`, `git log`, 22:24 |
| PR-level arithmetic | 38809 + 80 - 2 = 38887; deletions 3186 unchanged. It holds, and the kit makes it an R0 check | arithmetic on the two `pulls/85` readings (B358's and mine) |
| byte-equal | `secrets.ts` blob `88b77292…`, `content` tree `0c11b6f5…`, `package-lock.json` blob `53305eb4…`, `renderers/src` tree `83d4c7756f…`, all equal at `e969ad38` and `85105729` | `git rev-parse <c>:<path>`, 22:24; plus `git diff --quiet` rc 0 for secrets.ts and for `content package-lock.json packages/renderers apps` |
| 57-path set | equal at `e969ad38` and the head | `diff <(git diff --name-only …)` printed `same57` |
| released hashes | draft `5679855b…`, demo `5db37614…` (full values in the kit) | `git show 85105729:content/release-*/CONTENT_HASH` |
| CodeQL | 3 check-runs success; JS/TS analysis `1995918281` and csharp `1995908872` at `85105729`, 0 results; open alerts on the PR ref 0; main `fixed` 20 | `gh api` check-runs, analyses, alerts, 22:2x. So the head is already fully scanned; R5 is a re-read, not a wait |
| test-title lines | qgate 8 -> 10, label-run 12 -> 15; qgate removed lines 2 | `grep -c` on `git show`, `git diff -U0` |
| ancestry | `e969ad38` is an ancestor of the head (rc 0), reverse rc 1; ahead 14, behind 0 | `merge-base --is-ancestor`, `rev-list --left-right --count` |
| origin refs | `b424*`, `b423*`, `b358*`: none | `ls-remote`, 22:24 |
| load / ports | 2.19 2.47 2.54; `lsof` 7660-7669 rc 1; 0 briefs name `766x` (control `771x` finds 11 in `briefs/2026-10-2*`) | `uptime`, `/usr/sbin/lsof`, `/usr/bin/grep -l -w` |
| model | `levels.sonnet.model_id` = `claude-sonnet-5-5` | `models_latest.json`, 22:20:22 |
| `.env` | `AGENTMAIL_API_KEY` count 0, control 1 | `/usr/bin/grep -c -i`, 22:24:38 |
| Briefs folder | B424 files 0 (control B423: 3) | `ls \| grep -c` |

## What the kit does (so you can check it against Kam's option a)
- Gates only the delta plus boundary proofs (R0 byte-equal tree/blob ids with controls, hashes, 57-path set, merge prediction, K6). B358-2 is a Note, never re-raised, none of its mutants run.
- R1 B358-1: the gate's own fragment-built scan extended by the two bare patterns; a second instrument (`git grep -i -c` with names assembled in the shell) over EVERY distinctive local name, at main, round-1 tip, `e969ad38`, head; mutants T1b-A, T1b-B, T1c (the old line-68 form back), T1, T3, and T1x (one per distinctive local name and prefix). Names are never spelled; labels and counts only.
- R2 B358-4: static pair-list identity (15 = 15), T4b and T4a RED, plus T4d, T4e, T4g and the Note-only T4c.
- R3 B358-3: the gate recomputes the strict set from main's `secrets.ts` compiled verbatim, N2 RED with the failing test names, no-op control 0.
- R4 suites in the gate's own image (318 / 3,213 / 1 / 0 vs the B358 baseline 318 / 3,203 / 1 / 0, +10); a two-file baseline by overlay instead of a second image build. db suites NOT RUN by design (argued).
- R5 CodeQL four legs; R6 messages graded sentence by sentence, prior work, names; R7 gitleaks with a canary.
- LOAD rule: heavy only at load1 < 8 (two reads 4 s apart), one heavy job at a time, never beside the other gate, 20-minute wait then `NOT TESTED: load` and a conditional verdict, 120-minute time-box.

## Questions for Tuesday (each with my recommendation)
1. **Q1 Model row.** The kit says Sonnet, row G2 (`model-routing.md:109`: tier 2, tests-only follow-up whose mechanism a prior gate measured). The two tests guard a credential detector, which is a G1-class surface by subject, and the G2 row has a "1st if the follow-up's mechanism sits on a G1 surface" cell that I read but did not resolve to a column header. **Recommend Sonnet as your task says**: the delta is test-only, the mechanism was measured by an Opus G1 gate (B358), and the heavy work is instrument-driven. If you want Opus 5.5 for the T1x and N2 reading, change `BRIEF_SEAT_LEVEL` and the Model line; nothing else in the kit depends on it.
2. **Q2 Severity of a T1x survivor.** The kit scores "a distinctive local name (0 files on main, not one of the four generic words) that stays GREEN when spelled whole in a comment of the qgate test" as a **Major** (the class B358-1 named: "add the bare local names"). Kam's option a says a gate "checks only that change", and the builder claims only two bare names were needed. **Recommend keep Major**: it is the Blocker's own class, the probe is cheap, and the result is either "0 survivors" (closing the claim by measurement) or a real hole. If you prefer Minor, edit the Major list in the kit's floor.
3. **Q3 T4c (a 16th pair for a file that really hits).** I predict it passes (the new test proves a pair hits, not that main has it), and the kit scores it a Note, never a finding, because B358-4's own fix-shape allowed "each pair asserted to hit its own file". **Recommend Note**; ask Kam only if you want the frozen-manifest form.
4. **Q4 Last-line form on a refusal.** You said the last line begins `VERDICT:`. B358 used `STOPPED: NEEDS TUESDAY` as a separate last line. The kit makes the refusal `VERDICT: B424 STOPPED: NEEDS TUESDAY <ONE question>` so a single `^VERDICT:` grep works. **Recommend keep**, unless some tool of yours greps `^STOPPED:` for B-numbers (UNMEASURED by me).
5. **Q5 Pane label and the other gate.** The gate-33 launcher (`launch_qa_nexusai_gate33_repin2.sh:710`) derives its negative-control seats from a fixed candidate list that names `Datasec/Security-Composer-W13` and `Datasec/Security-Composer-G22`, not `-G29` and not `-G30`; a missing candidate is a NOTE, never a refusal, and an unlisted pane is not counted. So `-G30` cannot make that launcher refuse. I did NOT read whether gate 33's floor census (the foreign-process counts in its prompt) counts every live claude, and I did not touch panes. **Recommend:** launch G30 after gate 33 has launched (its negative-control seats are derived once at its launch, so a later pane is just another seat) and keep the kit's LOAD rule. If gate 33 is mid-floor-measurement when you stamp, wait or ask its owner. Also the finished builder pane `-W13` is in that candidate list as a negative control; the kit lets an IDLE `-W13` stay open (REFUSE 6) so closing it is not required.
6. **Q6 Time-box and the load wait.** I set 120 minutes and a 20-minute wait before `NOT TESTED: load` with a conditional verdict. B358 took about 85 minutes wall-clock at tier 1 with several load waits. **Recommend keep 120**; shorten to 90 if you want the verdict before a given card.
7. **Q7 The false-positive cost of bare pattern B.** Its two fragments joined are a plausible camel-case identifier; the builder measured 0 files on main and at the head, so nothing trips today, but a future `valueType`-style variable would turn the test RED until someone adds an allow-list pair (the same cost `copy|right` already carries). The kit scores that cost a **Note** and measures main and the head with `git grep -i -c`. **Recommend Note, not a finding**; if you want it gone, that is a later pass, not this round.

## UNKNOWN, with why and what closes each
- **Whether gate 33 (or any other gate) is live right now.** The task says one is; I did not touch panes or `ps` for it. Closing it: the kit's own REFUSE 6 and LOAD `ps` check at launch.
- **Whether the 72-string grid includes the gate's two strings.** I read only the added lines of the qgate file and the commit messages, not the label-run test file's added lines in full. The builder's STATUS lists the two gate strings as a separate test AND says they are among the 72; R3a/R6a make the gate settle it. A mismatch is a Note on `85105729`'s sentence.
- **The exact count of red tests under T1c and N2.** Builder claims 4 of 10 and 2 of 51; the kit records the gate's counts, and a difference by one with a true claim is a Note.
- **Names, the 13 local names and 2 prefixes.** I did not extract them (that needs `git show` of the round-1 tip, which the kit has the seat do into an ignored folder, masked). I read the added lines of the qgate diff, which hold only fragments; the kit refers to bare patterns A and B and to "the middle alternative" and spells nothing whole. `grep` of the kit for the fragment names and for the other schema words printed no line.
- **`.tools/b358/kit/` script contents.** Listed only (MEASURED 22:2x: 39 files incl. `qgate358.py`, `names358.py`, `mutants358.py`, `heavy.sh`, `treeproof.sh`, `classhunt.sh`). The brief makes the seat read each copy whole before running it. If a script hard-codes old paths, the seat fixes its copy and says so.
- **The L05 card and the `eaff2b74` deploy.** Not read (`decision_queue.sh list` is forbidden and no id was given). The kit repeats the hold and does not touch the demo.
- **Weekly gauge.** Not read; the routing receipt is yours.

## Slips and self-corrections
- My first PR/ref measurement bundle was refused by the Bash zsh-wordsplit hook (an unquoted multi-word `$G`); I reran it under `bash <<'EOF'`. Nothing ran in the refused call.
- The B423 builder's STATUS gives its kit location as `2_Project_Files/.tools/b423/`; the project-root `.tools/b423` does not exist (MEASURED `ls` rc 2). The kit therefore says "never open the builder's kit or tree" by name, not by one path.
- Every figure in the kit labelled MEASURED was re-read by me today; the builder-only figures (e.g. 4 red / 6 pins, `6cc548cc…`, 36 patterns, 949 files) are marked claims in the kit.
