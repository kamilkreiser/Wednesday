STARTABLE: YES (after Tuesday stamps: 8 four-underscore lines, Q-1 to Q-4 to answer)

# B1003 drafter report (SEAT-G245, HPSM-POC tier-2 gate, UAT keep-awake template)

## BLUF
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1003_SEAT-G245_hpsmpoc-uat-keep-awake-gate-tier2.md`. Shaped on B982 (tier-2 gate). Row G2, `model-routing.md` line 109 (G1 line 108, G-cap line 111); `BRIEF_SEAT_LEVEL=sonnet` inside the launch quotes; model `claude-sonnet-5-5`, `models_latest.json` line 23. It judges seven checks: compile equality, the CI predicate, the 10 rows against base, 12 own plants, cost re-measure, Learn claims, commit message truth. Ports: none (no listener). Azure acceptance in place is stated NOT TESTABLE and is the first FOR TUESDAY item.

## Facts re-measured (Sun 1 Nov 2026 00:47-00:5x AEDT)
- `git ls-remote origin`: branch `b999/hpsmpoc-uat-db-keep-awake-template` = 930cb5b5d163d2d19d9da8890bccfe68c8ce07aa; main = d0eff4ca637b8959dd205adc0b77e8111b60280a (also `commits/main`). Control: both match the task text.
- `gh api -X GET compare d0eff4ca...930cb5b5`: ahead 1, behind 0; files `infra/env/uat.bicepparam +7 -3`, `infra/main.bicep +4 -0`, `infra/modules/sql.bicep +6 -3`, `infra/tests/test_security_baseline.py +143 -5` (matches the task). Removed lines 3+0+3+5 = 11, matching the builder's 11.
- PRs for the branch (`pulls?state=all&head=...`): 0. Open PRs: only #266 (`b992/hpsmpoc-wake-tolerant-reads`).
- Round count: loop over `Briefs/*_STATUS.md` first lines `GATE VERDICT` filtered `b999|keep-awake|uat-db`: 0 hits. Weakness: I did not run the positive control for this exact filter in this session (I ran a broader filter whose output was huge); the kit tells the gate to run it with the B982 control.
- ci.yml at origin/main: job `infra` line 575 (`infra (Bicep validate)`), `WHATIF: "0"` line 583, shell-scripts step lines 599-606, validate step 623-627 (`bash infra/scripts/validate.sh`). Grep was case-insensitive on retry: the first attempt got the advisory only.
- Commit message read in full via `gh api commits/930cb5b5 --jq .commit.message`; the kit asks the gate to judge each sentence.
- Tools present: `.tools/bicep/bicep`, `.tools/b198/lock.sh`, `.tools/b267/waitload.sh`, `launch_when_cool.sh`, `cockpit.sh`, `brief_seat.sh`. `.tools/b1003*` and `.tools/wt-b1003*` do not exist.
- Panes (tmux): `Datasec/HPSM-POC-H85`, `Datasec/MPS-M53`, `Datasec/MPS-R97`, `fleet-monitor`, `tuesday`. No G245 pane. No B1002 kit exists yet (`ls | grep -c B1002` = 0).
- Kit self-checks: four-underscore lines 8 (7 slots + last line); non-ASCII 0; `@X@` tokens 0; no `localdomain`; B-numbers present are B982 (control), B991 (source finding), B999 (builder); no person names, no card ids.

## D-decisions
- D-1: no PR exists, so no check-runs are in the kit; the hosted predicate is judged locally by running `validate.sh` as ci.yml does. The kit also tells the gate to handle a PR appearing in the meantime (read its checks, do not stop).
- D-2: the gate is allowed two public read-only GETs (Azure Retail Prices API, Microsoft Learn), because checks 5 and 6 cannot be done otherwise. This is a stretch of the "no HTTP to hosted hosts" fence (those fences are for hosted, demo, prod); it is listed as Q-2.
- D-3: added a check beyond the task list: does merging main deploy anything (workflow triggers, `deploy-from-ci.sh`)? The tier rests on "nothing is deployed". It is a Blocker-class fact if wrong.
- D-4: plants are 12 gate-own mutants M1-M12 (uat flags, a nonsense 0 delay, dev/demo drift, main default, literal pass-through, module literal with param still used, module default, condition flip, two test-side loosenings), plus an equivalent mutant.
- D-5: the builder's commit-message claim "the rest are mutation rows red under their plants" is checked row by row; a new row green against base and under every plant is vacuous (Major).
- D-6: the builder's own arithmetic has a possible one-cent rounding (322.84 - 2.78 = 320.06, builder prints 320.07); the kit sets one cent as Note.
- D-7: the builder's `cd` slip is repeated as a fence ("not even a subshell").

## Q-questions for Tuesday (each with a default)
- Q-1: if the plant table exceeds 12, may the gate run extra? Default: NO; cap 12 stands.
- Q-2: may the gate GET the two public pages (prices.azure.com, learn.microsoft.com)? Default: YES, read-only, only those two.
- Q-3: tier 2 stands given the deploy is a separate tier-1 act? Default: YES, with auto-escalation on any byte outside the four paths.
- Q-4: should a merge-triggered deploy finding escalate or just flag? Default: flag as Blocker-class and STOP for Tuesday.

## UNMEASURED by the drafter
- The Learn page wording and the Retail Prices figures: relayed from the builder STATUS only (I made no HTTP calls). The 91.5 % / 8.47 % / "about a minute" resume figures are in the B991 STATUS, which I did not open. The B999 builder brief was not re-read beyond the STATUS; the dev/demo effective values and the 6-red/4-green split are the builder's claims.
- Whether `launch_when_cool.sh` accepts the template's exact arguments (not invoked, per the rules).
- Port occupancy: `lsof -nP -iTCP:9400-9599 -sTCP:LISTEN` printed nothing (no control run; the output was swamped by a word-boundary scan that showed many overlapping decades in older kits). The gate binds none, so no decade was reserved.

## Outside-the-fences disclosure
Read-only: ls-remote and `gh api -X GET` under the project `GH_CONFIG_DIR`; ci.yml read via `git show origin/main:`; the B982 template, DRAFTER_RULES, tier learning, routing table, models_latest.json, B999 STATUS, tail of the B999 brief and head of its drafter report, tmux pane list, lsof. Never opened: `fleet/briefs_staged/`, `scoreboard.md`, `_ledger.md`, `HP Reporting and Docs/`, SOWs, `Source_Documents/`, `inbound/`, decision cards, Jira, WEDNESDAY/FRIDAY trees. One tool-use slip: the first `ls` of non-existent `wt-b1003*` globs errored harmlessly in zsh. No file written besides the two outputs.
