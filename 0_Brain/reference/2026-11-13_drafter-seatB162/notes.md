# Drafter notes: Seat B 162nd brief (for Wednesday, at the stamp)

Drafted 2026-11-13 00:3x to 00:5x AEDT. Output: `brief_B162.md` (about 48 KB: above the ~45 KB target by about 3 KB; B 161st's stamped brief was 52.5 KB). STAMP block left blank, no SELF-CHECK line. Nothing written outside this folder except the drafter's own session scratchpad (`rc` scratch clone, scripts).

## 1. Meter readings (kit meter, 1M window; from B 161st's HANDOVER and wrap, B 160th's from its brief)
| seat | first read | PLAN | SET-UP CLOSED | READY | MERGED build | after MERGED send | wrap start |
|---|---|---|---|---|---|---|---|
| B 161st (2216) | 19.5 | 30.2 | 39.3 (+9.1; tripwire waived to 43.0) | 46.5 (+7.2; facts read 43.6) | 50.4 | 51.4 | 54.2 |
| B 160th (2214) | 19.3 | 23.3 | 35.6 (+12.3) | 42.0 (+6.4) | 47.6 | 49.2 (as wrap start) | 49.2 |
| B 159th (2215) | 20.8 | 22.4 | 34.7 (+12.3) | 51.3 (+16.6) | about 57.9 | | |

Eleven first MERGED readings: ten from the B 161st brief (sum 555.1) plus 51.4 = 606.5, mean 55.1; one of eleven at or under 50. Ambiguity for Wednesday to rule: B 160th's 49.2 was read at wrap start (after the MERGED send); B 161st's equivalent point is 51.4 (the 54.2 wrap-start reading is later because a STATUS and its ANSWER came in between). I used 51.4.

## 2. Second-row rule
Carried unchanged (r at or under 48: next row alone; above 48 to 54: STATUS first; above 54: wrap). B 161st's figures do not argue for a change: r = 51.4 (middle band), its own forecast for a second row (60.2 to 68.0) was past the pace line, and Wednesday ruled WRAP with no line waived. 2219 has 2216's shape, so the best prior for B 162nd is: MERGED build 41 to 50, r 42 to 52 (an ESTIMATE from PLAN 22 to 25 plus the measured deltas; not a measurement).

## 3. Proposed tripwire for a seat that RE-KEYS the kit (brief COST AND PACE (a2); for Wednesday to rule)
B 161st's SET-UP delta was +9.1, the smallest of three; its PLAN (30.2) carried the overspend because it wrote six new scripts, a 15 KB template and long working-out. Proposal: (1) a PLAN reading above 26.0 means new scripts were written: the plan names them and the seat stops writing them; (2) SET-UP CLOSED above `min(38.0, PLAN + 12.3)` is a STATUS and a stop (12.3 = the largest measured delta; a re-keying seat should read PLAN + 9 to 12). The 38.0 and 58 tripwires, pace 60 and ceiling 66 are carried; B 161st's waiver to 43.0 is stated as for that seat only.

## 4. Which gate verdict covers PR 2178
None. Instrument: `head -1` of every `verdict.md` under `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/*/` (601 files) tested for 'PR 2178': no hit. A body grep for `2178|KS-2149` hits two files, both incidental (gate 6 names `adminConfig.ts:2178` and a hunk header `-2178,4`; gate 312's text lists PR 2178 in a file-census line, not as a verdict). So 2178 stays HYGIENE by Wednesday's ruling (B 160th's line 99, carried) and its GO names the hygiene ruling in place of a verdict.

## 5. Things measured that change the picture (read these)
- **PR 2219's live body has NO `## Notes for the gate` section** (REST body, 5,891 bytes; no heading matching at any level; its line 1 is `Refs KS-2174`). B 161st's carried rule says the stock notes sentences are TRUE only for a body that has one. The brief says: NO-NOTES ruling stands for 2219 but the stock sentences must not be carried. 2217, 2218, 2178 do have one (lines 43, 42, 42).
- **check-runs are readable through the project gh config** (HTTP 200, 19 runs) where B 161st declared a 403 for 'the project token' (different instrument; not chased). 2219's and 2217's heads each show 11 failure and 8 skipped; PR 2216's merged head showed the same 11 and 8; develop's tip `621275a89677` and `43d7eae7a5f8` show 3 failure and 4 skipped. GraphQL mergeStateStatus is UNSTABLE on 2219, 2217, 2218, 2178. Consistent with UNSTABLE being the CI state; cause not diagnosed (UNMEASURED, carried as a declared non-blocker). The brief changes the check-runs line in the accepted NOT-covered list accordingly.
- **Planted-conflict controls for 2219 (ADDENDUM 1)**: develop-side plants at develop lines 1766 and 1775 (the PR's own two lines, shifted by 2216's added lines) rc 1; PR-side plants at 2216 hunk lines 1754 and 1798 rc 1; untouched line 200 rc 0. My FIRST develop-side attempt at line 1764 (the PR's old numbering) read rc 0 because develop's numbering had shifted: the line number must be taken from develop, which the brief says. Expected trees on develop `621275a89677` all rc 0 both orders; 2219 `61f2f53343fe` equals gate 343's 2219+2216 tree; 2219 vs 2052 `35c88b3ce7eb` and 2218 vs 2099 `825f70fefb78` equal their gates' trees.
- Develop's first-parent distance and moved-path counts for 2217 and 2218 are higher than B 161st's (4 and 3 commits; 21 and 19 paths) because 2216's squash and the earlier moves are counted from the old merge-bases.
- B 161st's HANDOVER re-key paragraph trails off mid-sentence about the source set for 162 ('... i.e. produced = ... own161 = ...'); the brief tells B 162nd to read `rekey_b161.py`'s own sets and say which of the 16 own-authored scripts it carries. Worth asking B 161st's lineage to fix at its source if the next HANDOVER is edited.
- History ordinals: 158: 2, 159: 2, 160: 2, 161: 1, 162: 0 (1,124 headings). Note B 160th reads 2 now (its heading plus B 161st's naming it).
- Kit by program: two tools differ from v3 (`merged_build_b161.py`, `run_merge_b161.sh`), baselines v1/v2/v3 prefixes equal the HANDOVER's.
- Floor: tmux at 00:38 AEDT lists only %0 (wednesday) and %1 (fleet-monitor); the shells %157 and %158 named in the commission did not list (re-list at the stamp).

## 6. What I could not measure / did not do
- Any install, suite, tsc leg, or planted control for 2178, 2208, 2207, 2184 (not planted).
- Gates 330 and 328 (not read); PR 2099 or 2052 mail/GO status beyond their PR state (I read only the B161 files in briefs_staged, as commissioned).
- The inbox, launcher preflight, pane owners, `git worktree list`, the cause of UNSTABLE and of the eleven CI failures, and why 'the project token' read 403 where the gh config reads 200.
- The model-routing row C5 (carried, not re-read). Linear: ten keys read (all In Progress except KS-1964 Backlog); keys KS-2166, KS-1053 and the extra-keys of the PR bodies are no longer named in the brief except KS-966 (PR 2219's extra key, from gate 343).
- Cuts to reach the size: the brief drops B 161st's builder-hand-change prose (points at the HANDOVER's seven items) and its per-row gate-measurement detail beyond what a GO must name.

## 7. Method notes
Scratch clone: `git clone --shared --no-checkout` of REC161's clone into the session scratchpad; PR 2219's and PR 2052's heads fetched into it over the project's own repo-local ssh command (read use; push URL dead); all merge-trees, plants (temp index + `commit-tree`) and synthetic squashes there. Project trees: only `ls-remote` (GIT_OPTIONAL_LOCKS=0), `config --get`, `cat-file`, `ls`. No credential printed; the Linear key was read inside python only. One slip: a first Bash call contained a `cd` and was refused by the hook (nothing ran); no other counted slips.
