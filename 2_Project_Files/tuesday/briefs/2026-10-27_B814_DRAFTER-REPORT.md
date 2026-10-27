STARTABLE: YES (stamp when you want it; read D1-D4 and Q1-Q4 first. Branch head, main, PR state and the guarded paths were all re-measured at 11:18-11:21 and match the kit; the one thing that moved since your handover is PR #222's head, which does not touch this lane)

# B814 drafter report (SEAT-H45, Datasec / HPSM-POC, FIX ROUND on PR #233, class "the reader strips Unicode white space as space", gate after = tier 2 round 2 of 2) -- drafted Tue 27 Oct 2026 from 11:18 AEDT

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B814_SEAT-H45_hpsmpoc-233-fix-round.md` (123 lines, 8 four-underscore slots by `/usr/bin/grep -c -E '_''_''_''_'`, 7 slot lines plus the last line; at-slot pattern count 0; no person's name by `grep -c -i -E 'kam|kreiser'` = 0). Template: the B800 builder kit (shape, partition, standing lines, HP-tools line, STATUS channel). Gate method read whole: B805 STATUS (221 lines) and the first 60 lines of the B805 gate kit.

## BLUF
- One builder, Sonnet, one commit, one path, a plain fast-forward push to the SAME ref. The fix is confined to the 24-line file-level section of the new method (head lines 829-852): locate each step by `step_identity` equality with the pinned triple, edit the step's own key line (matched with the same pattern `step_keys` uses), and run the 11 existing rows over five layouts (as-is, F1, F2, F4, F6). The two strip sites, the docstring, the 126 unit rows and the 34 old tests are held byte-equal to `adcd0fd`; this is what keeps round 2 narrow.
- The red-proof uses the gate's own anchors (P1-P6, C-zwsp, C-inner, the legitimate set, the 64-plant sweep, F1/F2/F4/F6/F7/F9), with the head method as the column that must fail where the gate saw it fail.
- Model: Sonnet (row C2 line 92, row C1 line 91 counter "one fix round on the same seat model"), launch line carries `BRIEF_SEAT_LEVEL=sonnet`.
- Notes: one IN (the gate's own regression test, which is how B805-1 is proven closed), nine carried as NARROWING.

## Facts re-measured (instrument, control)
| Fact | Value | Instrument | Control |
|---|---|---|---|
| Branch head | `adcd0fd67fee9eab3707974d676bdfb560760821` | `git --no-optional-locks ls-remote origin refs/heads/b800*` and `gh api -X GET pulls/233` (both) | `refs/heads/main` and `b709*` print lines |
| `b814*` on origin | none | `ls-remote origin 'refs/heads/b81*'` printed no b81x line | control: the same call printed `b800*`, `b709*` |
| main | `bf4a7bddf37e42675c263518ac218a08eb1dd607` (moved from `d415a3fe` by the #232 squash) | `ls-remote`, `compare d415a3fe...bf4a7bd` | 5 paths (api Auth x2, api test, web config, web test); `grep -c -x -F infra/tests/test_ci_workflow.py` over them = 0; control `compare 4c067e4f...d415a3fe` = 1 |
| PR #233 | open, +70 -2, 1 file, `mergeable_state` `clean`, base sha `d415a3fe` | `pulls/233`, `pulls/233/files` | the file list reads the one path |
| Open PRs | #233, #222 | `pulls?state=open` | - |
| #222 | head **`595b0b59a44ca032d5c5f75bc55d01667d298532`** (your handover and the B800 kit say `7b3f3c76`: it moved, presumably the bring-up-to-main builder), 1 path `RequestTimingLogTests.cs`, shared with the reader 0 | `pulls/222/files` | `printf` of the reader path through the same grep = 1 |
| Head file | 891 lines, 54565 bytes, blob `f9f9477a6eef071ff21ae1261e4ec295da9821ea`, 0 non-ASCII bytes (20 tab lines, which `[^ -~]` counts) | raw `contents?ref=adcd0fd6` read into scratch, `git hash-object` | the same call at `d415a3fe` hashes to `7a1563a6...` (the known blob) |
| Method lines | `test_the_shard_job_has_exactly_the_pinned_steps_in_order` 763; new method 789; file-level comment 829; next method 854 | `grep -n` on the scratch copy (case-sensitive; patterns found hits, so not a false zero) | - |
| Shard job in `ci.yml` (blob `0176b491...`, equal to `d415a3fe`'s) | start step line 197, Api build line 237, shard checkout line 188; the identical checkout line occurs at 11 lines of the file (45, 188, 381, 460, 498, 549, 589, 638, 671 and two more by count) | raw `contents?ref=bf4a7bd`, `grep -n` | `git hash-object` of the raw read = `0176b491...` |
| CI predicate | `ci.yml:576` job name, `:581` `BICEP_VERSION: v0.47.16`, `:623` step, `:627` `bash infra/scripts/validate.sh`; `validate.sh` line 7 `set -euo pipefail`, line 21 `BICEP="$BICEP" python3 tests/test_security_baseline.py`; `on:` lines 14-18 | `sed -n` on the raw reads | `validate.sh` raw hash `d6fd1317...` = the gate's blob |
| Ruleset | `deletion,non_fast_forward,code_scanning,required_status_checks` | `rules/branches/main` | - |
| Landing text | one hit `CLARIFICATIONS.md:138` (squash, head-pinned, one precedent). No rule requires squash. | `/usr/bin/grep -n -i -E 'squash|match-head'` over project `CLAUDE.md` and `CLARIFICATIONS.md` | the hit itself |
| Checks on the head / alerts | `check-runs` read returned a count (gate: 20 rows all success at 11:06); `code-scanning/alerts?...&state=open` length 0 | `gh api -X GET` | not re-controlled by me (the gate's control: analyses on main return rows) |
| Ports 8980-8989 | free, `lsof` rc 1 | `lsof -nP -iTCP:8980-8989 -sTCP:LISTEN` | I bound and listened on 8985 from `python3 -I`, `lsof` listed it, freed it, rc 1 again |
| 898x in SEAT kits | 0 files | word-boundary scan `(^|[^0-9a-f])898[0-9]([^0-9a-f]|$)` over the 108 non-`.pre-` SEAT kits of 2026-10-26 and 2026-10-27 | `x 8981 y` = 1, `x 18981 y` = 0. Frame: those two dates only; older kits (2026-10-23/24, MPS) do name 898x, outside the frame |
| Panes (11:20) | `tuesday`, `Security-Composer-R60`, `MPS-R59`, `HPSM-POC-G171`, `Security-Composer-J25`, `NexusAI-M20`, `HPSM-POC-D37`, `fleet-monitor` | `tmux list-panes -a -F '#{@cockpit_name}'` | Note: R60 is new since your 11:14 read (another repo); `H45`/`B814` names: 0 in `.tools/` |
| Local clone | has `adcd0fd` (`cat-file -t` = `commit`); does NOT have `bf4a7bd` (`fatal`, rc 128) | `git --no-optional-locks cat-file -t` | the kit says no fetch is needed |
| Partitions | G171: ports 8950-8959, `.tools/b809`, `.tools/wt-b809-*`; D37: ports 8900-8909, `.tools/b804`; D38/B810 kit drafted, not live (`.tools/b810`) | `grep -o` over the B809/B804/B810 kits | - |
| Model | row C2 line 92 (S55 "1st"), C1 line 91 counter, G2 line 109, G-cap line 111; `levels.sonnet.model_id` `claude-sonnet-5-5` | `sed -n 80,112p` of `model-routing.md`, `sed -n 18,28p` of `models_latest.json` | row numbers match the B800 kit's L6 85 / C2 92 / G2 109 |

Landing rule confirmed: the kit says the squash is Tuesday's, head-pinned, through CodeQL, on the strength of one precedent (`CLARIFICATIONS.md:138`) and no merge-method rule. The builder pushes a fast-forward of the existing ref, never force; a squash of the PR lands both commits as one on main.

## What was decided from the B805 findings
- **B805-1 shape.** The gate's anchors that fail are exactly the text-literal ones: `api`/`start` line literals, `re.search(r"uses: actions/checkout@\S+", text)` and `text.count(old) == 1`. The kit removes all three and adds a program check that none of `"- run: `, `"- name: `, `uses: actions/checkout@` or `text.count(`/`text.replace(` remains in the section.
- **Layout scope.** F1, F2, F4, F6 are IN (valid YAML, green at base, red at head, per the gate). F3, F5, F8, F10 are red at BASE already (other tests) and excluded. The space/tab before the `@` is invalid for GitHub: reported, not required.
- **Why 5 variants x the same 11 rows rather than new rows:** it keeps every existing row's meaning (the four differ rows and seven same rows) and gives the gate's requested regression test (pinned list equal on F1/F2/F6, and the section runs to its end) as a counter assertion.

## D-decisions
- **D1. Notes N1-N10 disposition** (property: in only if required to close B805-1 or a one-line pin the gate asked for). IN: the gate's regression test only. OUT, carried as NARROWING: N1 (11 strip characters without a row, input to the ticket's line-break ruling), N3 (docstring wording; would edit the held docstring), N4 (message pin on the `run: |` + U+00A0 cell, not asked by the gate), N5 (sibling strip sites), N6 (3.9 base failure), N7 (mkdtemp leak), N10 (green-by-construction rows). N2, N8, N9 need nothing.
- **D2. Everything outside the section stays byte-equal to `adcd0fd`** (strips, docstring, unit rows, 34 old tests), proved by `git diff adcd0fd..HEAD` ranges and an AST check. Reason: round 2 is the cap; a smaller diff is a smaller gate surface.
- **D3. Helper shape is "spelled out" but subordinate to the property.** The kit lets the builder deviate with a reason in Design (STANDING LINE 10). The expected row counts (about 181 total, 117 red on the old strip) are arithmetic from the gate's 137/101 and are flagged as estimates.
- **D4. Mutants.** Strip mutants m1-m6 are re-run on the new method (the `rstrip` survivor is the gate's proved-equivalent one, optional); four new mutants n1-n4 target the layout code (no-op layout, edit on the first line instead of the key's line, off-by-one locator, counter off by one). These are what stop the layout rows being a check that cannot fail.
- **D5. Timing suggestion for the stamp:** target READY 70 minutes after launch, hard stop 120.

## Q-questions for Tuesday (each with a default)
- **Q1.** Is the round-2 gate's wording "NO GO 1 of 2 on class 'the reader strips Unicode white space as space', B805 first line" right for the stamp? Default: yes (read from the B805 first line: "round 1 of 2 ... NO GO"; the 83-file loop was the gate's, not re-run by me).
- **Q2.** Do you rule F1/F2/F4/F6 as legitimate edits the reader must keep green (the gate's own question; its default was yes)? Default: yes, as the kit assumes. If you rule no, B805-1 becomes a Note and there is nothing for this builder to do: do not launch.
- **Q3.** Pull N4 (a message pin on the `run: |` + U+00A0 `assertRaises`) into this round? Default: no (not asked by the gate; it is a one-line pin but outside the property).
- **Q4.** Should the builder also merge main into the branch? Default: no (the PR stays 1 path, mergeable `clean`; the squash is Tuesday's; a merge commit would add risk to the cap round).

## UNMEASURED
- Nobody has run the fixed shape: no worktree, no test, no plant by me. The gate's F1/F2/F4/F6 numbers (6, 1, 6, 4 rows red) are RELAYED; the builder reproduces them at Step 4 before editing.
- Python 3.9-safety of the helper shape as written; row counts of the fixed method; whether `bf4a7bd` matters (not in the clone; blobs equal per the gate).
- The whole-infra run (needs the Bicep binary; not run), the runner's Python, GitHub's own YAML parse of the layouts (the gate used a YAML 1.1 parser).
- The check-run state on the head was read once (a count and the gate's 11:06 figure); I did not re-control the code-scanning zero.
- The 108-kit scan frame is 26/27 Oct only; 898x appears in older kits (out of frame).

## Outside-the-fences disclosure
- I wrote exactly two files: the kit and this report. No `decision_queue.sh`, no card, no `briefs_staged`, no scoreboard, no ledger, no WEDNESDAY/FRIDAY tree, no Artifact/Docs/mail tool.
- Git in the project repo: only `cat-file -t` (two calls, one expected fatal for `bf4a7bd`) and `ls-remote`. `git hash-object` ran on scratchpad copies only. No fetch, no merge-tree.
- `gh` calls were all `-X GET` under the project's `GH_CONFIG_DIR`, exported inline in each shell: pulls/233, pulls/222 files, open pulls, branches list, contents (raw) of the reader at two refs, `ci.yml` and `validate.sh` at `bf4a7bd`, compare (two), rules, check-runs, code-scanning alerts, commits of pulls/233. No Jira call.
- Raw reads written to my scratchpad (`/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/5763a99f-d3dc-49d0-84f9-4fe29e51ff2d/scratchpad/`): `head.py`, `ci.yml`, `p222.txt`, `cmp.txt`. One local `python3 -I` socket bind/listen on 127.0.0.1:8985 for the lsof control, closed in the same command; no HTTP to any host.
- Read the HPSM-POC project `CLAUDE.md` and `CLARIFICATIONS.md` only through a squash/match-head `grep`; read B805 and B800 STATUS files under the project's `Briefs/` as claims (allowed by the rules); read the B809/B804/B810/B801 kits only through `grep -o` for ports and tree names. One shell line used `grep -P` (not supported on macOS) and failed; no effect on any number above.
