# Drafter notes: Seat B 178th brief (2026-11-15 17:37 to 17:45 AEDT)

Brief: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-15_seatB178_merge.md (46.4 KB; heading `## RULED BY KAM, NOT YET IN AN ARTEFACT` x1; one at-sign, in the shared mailbox address; STAMP block left blank with six W items).

## Facts verified
- develop = ce35818d50ae (tree c4143be5ba25, ONE parent 4e4347818772), unchanged since B 177th's READY (06:17Z). All eight queued heads equal B 177th's pins; none moved.
- Merge trees on ce35818d50ae: eight rows and 2230 rc 0/0, same tree both orders. Row 1 (2220) tree 43cf796733bd = the figure in B 177th's READY (independent reproduction). Planted 4 of 4 rc 1/1, negatives 4 of 4 rc 0/0.
- **2081 vs 2230 CHANGED since B 177th's brief:** 2230 is now head 220df650550a (3 commits, 7 files +509 -6). It shares exactly ONE path with 2081: services/anchoring/src/cardano/provider.ts (hunks ~130 to 220 lines apart, no same-line edit). Head-vs-head merge-tree rc 0/0 tree 7e591ac6a60b (AA 6th's mail quotes the same); stacked on develop either order rc 0, tree 746f0d92f497. Semantic coupling found by reading: 2081's test imports ViewUtxo (walletView) and payloadDigest (walletSpend), both edited by 2230. Not run.
- Census of 90 open PRs: only 2230 shares a path with a queued row; 0 shared with K's rows or 2229, 2231 to 2236.
- B 177th: HANDOVER_notes.txt only (no FINAL, no MERGED, no history entry, no wrap manifest). Last state: SET-UP CLOSED 32.4, legs 9 of 9, READY 06:17Z at 49.8, no GO. Watcher last tick 06:20:02Z, process absent. history.md has NO B 177th heading (B 178th 0, B 177th 0, B 176th 1, B 175th 2).
- Check runs by the drafter's token: 2220 19/11/8/0, 2081 22/14/8/0, 2230 22/14/8/0 (200). B 177th's READY says both 403 and 19 runs; DECLARED in the brief.
- Matcher for 178: 722 entries (B 177th's file), B 177th absent (add), B 178th present (out), six new controls absent; n = 728, self-test 737 by arithmetic.
- Kit: 38 files in REC177/tools = 31 manifested + 7 not; two changed since v3 (ready_build2_b177.py, run_merge_b177.sh). v3 first 16 hex 1d25067e79c938d4 (31 lines).
- External vitest config sha b3fe391097a8486e and deps store versions equal B 177th's READY; W-1 = YES carried from B 177th's STAMP.
- Floor: only %0 and %1 alive. Push queue 0. Load 26.64 / 13.00 / 8.09. Gates 358 (2230) and 359 (2236) now commissioned (no verdicts).

## Wednesday must rule (brief's STAMP block, W-1 to W-6)
W-1 which seat merges 2230 and when versus 2081 (shared provider.ts). W-2 load rule. W-3 GO only after this seat's own READY, naming Seat B 178th (B 177th's READY and K 19th's GO are for dead seats). W-4 no B 177th history heading: 178th writes its own, no stub. W-5 B 177th's scratch left untouched. W-6 kit baseline = REC177/tools as found.

## Deviations from B 177th's brief shape
- New BLUF 2 (recovery: four duties), BLUF 6 rewritten, BLUF 13 (floor and gates), FIRST ACTIONS block, and an instruction to write a short HANDOVER state block after SET-UP CLOSED and each READY (the reason this seat exists).
- overlap.py's trailing locks loop raised KeyError (2225 not fetched); output up to that line kept; lock facts come from the census.

## UNMEASURED
- Every install, suite, tsc, eslint, vitest, cell run; whether B 177th's fe_legs_b177.py and glue still run; the matcher self-test (737 is arithmetic); semantic coupling of 2081 and 2230 beyond the two imports; the check-run counts of the six other B-lineage heads (carried 19); why B 177th's READY says both 403 and 19 runs; Linear automation on merge; inbox since 06:32Z beyond the newest batch and staged GO files; decision_queue; launcher preflight; tmux pane contents; K 20th's brief, matcher and queue (not written yet); gate verdict contents beyond line 1, table lines and hex presence; PR body box text; cause of the tmux death.
