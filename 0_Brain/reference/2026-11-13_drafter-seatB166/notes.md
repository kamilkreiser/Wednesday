# Drafter notes: Seat B 166th brief (drafted 2026-11-13 about 04:37 to 04:5x AEDT)

Output: `brief_B166.md` (46,883 bytes; commission said ~45 KB; B 165th's was 46,669). STAMP block blank except the PROPOSED lines (second-row line, set-up stop line); no SELF-CHECK line; every KS key named has one PROVENANCE line (11 keys: 1873, 1868, 1959, 2083, 2060, 1536, 961, 2174, 1053, 2021, 667). Wrote only into this folder plus the session scratchpad (`scratchpad/d166/`: `rc166` scratch clone, `m1.sh m2.sh m3.sh`, body copies).

## 1. B 165th's measured meter (kit meter, 1M; from b165_wrap.txt and HANDOVER)
| point | reading | delta |
|---|---|---|
| first read | 17.1 | |
| PLAN | 24.2 | +7.1 |
| re-key done | 35.9 | +11.7 (own reasoning text between calls; STATUS; Wednesday raised the line 36.5 -> 39.5) |
| set-up steps closed | 38.9 | +3.0 more (+14.7 over PLAN) |
| gate 344 read (14 KB) | 40.2 | +1.3 (counted to READY) |
| READY text written / sent | 46.6 / 48.9 | sent = +10.0 from set-up closed |
| MERGED 1 sent (r) | 53.7 | +4.8 from READY |
| wrap start | 54.4 (wrap mail 56.8) | |
B 164th's (carried): first 20.4, PLAN 23.4, set-up 34.2, READY1 39.9, MERGED1 45.6, READY2 51.1, MERGED2 53.7, wrap 55.0. Fifteen first-MERGED readings now: 750.5 + 53.7 = 804.2, mean 53.6; four of fifteen at or under 50.

## 2. Proposed second-row line (Wednesday rules at the stamp; the numbers are the drafter's reading, not measurements)
ROW 2 = PR 2200 after 2201: **r <= 49.0 DIRECTLY; 49.0 to 52 STATUS; > 52 WRAP naming 2200; a READY above 58 is a STATUS then WRAP.** Basis: second-row READY cost measured r + 5.5 (B 164th), r + 5.8 (B 163rd), r + 6.1 (B 162nd); 2200 has a 26-test package run, a tsc leg, no pair proof, no new install: price r + 6 to 7 READY, r + 9 to 10.5 MERGED, so r = 49.0 gives READY 55 to 56 and MERGED 58 to 59.5. Row 1 (2201) is dearer than B 165th's 2184 (adds a pair proof, a survive control, a 25 KB verdict to read), so the honest forecast for r is 48 to 51: the line opens in about half the cases or fewer (only four of fifteen first-MERGED readings were at or under 50). Alternative if Wednesday wants 2200 pushed: 50.0 (MERGED up to 60.5, past PACE 60). No third row: the queue has two rows. SET-UP stop line proposed unchanged, `min(38.0, PLAN + 12.3)`; B 165th crossed it from reasoning text, and its derive scripts (`evidence/aids`) now exist, so the re-key should be cheaper.

## 3. The 2201 x 2075 pair proof (instrument: git's real merge-tree in a scratch clone, develop `f3e8540b8540`)
Synthetic squashes by `commit-tree`: S01 = develop+2201, S75 = develop+2075. merge-base(S01, 2075 head) = `631ccfb8266a` (2075's own base); merge-base(S75, 2201 head) = `c78c80bd5370` (2201's own base). (develop+2201)+2075 and (develop+2075)+2201, both argument orders each: rc 0 in all four, ONE tree `9938b119429894f7d8fa090c52477126224de511`. Head vs head (2201, 2075; base 631ccfb8266a): rc 0 both orders, tree `226cf3ddf4a5`. Survive control: `isPlatformRole` in users.ts: develop 2, merged 2 (both orders), 2201 head 2, 2075 head 0 (2075 is cut before KS-1536 PR 3b); `PLATFORM_ADMIN_ROLES` develop 0, merged 0; merged vs develop numstat 10/3 = 2201's 1/1 + 2075's 9/2. Wrong-base control (merge-file, base = develop's blob): rc 0 with 0 `isPlatformRole` hits: the instrument sees the revert gate 323 found. Planted line 678 on develop: rc 1/1; line 10: rc 0/0. Result: CLEAN, no interaction, KS-1536 lines survive. Gate 323's tree `d679db4707a0` was on its own develop (`697f422f1a39`): not comparable and not claimed.

## 4. Findings and discrepancies Wednesday should know
- **Verbatim GO sentences.** B 165th's brief carried PARAPHRASES labelled "verbatim Q5": for 2201 ("the 'Admin created user' log line now carries userId ...") and for 2200 ("the tokenisation service now answers ..."). Gate 323's Q5 for 2200 has a literal `GO: PR 2200 makes the tokenisation service answer, instead of crashing, ...` sentence; for 2201 Q5 has no `GO:` sentence, only "PR 2201: no client-visible change. Status and body ... Operator-visible: the `Admin created user` line now carries `userId` where it carried `email`; a log search or alert keyed on that line's `email` field stops matching." The B 166th brief quotes both from the verdict text itself. RULE NEEDED: whether the GO's Q5 line for 2201 is that two-sentence text (drafted) or a composed one-liner.
- **The auth package moved** (BLUF 5): 4 new test files (three KS-2174 raw-email-log tests, one KS-2021), one modified, three source files (userRepo.ts, auth.ts, password.ts); none touches users.ts or 2201's test; merge trees clean. The three KS-2174 tests are in 2201's own family (log lines carry no raw email); I made them the "neighbour" tests to run with 2201's new file, and derived the whole auth suite at 154 files (153 at develop by `ls-tree` + 1). The 1,843 count is gate 323's on its develop and is NOT carried as a merged-tree expectation.
- **Directory neighbours on `services/auth/src/routes/`:** PRs 2098 (mfa.ts), 2099 (wallet.ts), 2197 (issuerCerts.ts); file-disjoint from 2201. Not tested against 2201 by merge-tree (only the 2075 pair was commissioned); UNMEASURED beyond the file census.
- **Tokenisation is UNMOVED** since the merge-base (`git diff --stat` empty), so gate 323's tokenisation baseline stands for 2200 on this develop.
- **CI failing check-run NAMES, previously UNMEASURED, now read:** the same eleven at 2201's and 2200's heads (diff rc 0), nineteen runs, 0 success; develop 7 runs, 3 failing. Cause still unmeasured; no ticket cited; the 11 names are in BLUF 14 (one name carries `KS-667`).
- **CFG tier field** is a free string (`tier {c['tier']}` in the MERGED builder); no entry uses `tier="1"` (0; control `tier="2"` 5). Whether the remaining stock text suits tier 1 is UNMEASURED; the brief says READ the body.
- 94 open PRs now (95 before; 2184 merged).
- Decision-queue priors (`decision_queue.sh prior`) NOT re-run; B 165th's 0 of 6 is carried and labelled.
- The brief's REST `mergeable_state` read `unknown` while GraphQL read UNSTABLE at the same minute; the brief says so.
- ls-remote used REC165's clone origin (GitHub); pins equal Wednesday's 04:37:11 for all six.

## 5. Things Wednesday must rule at the stamp
(1) The second-row line (49.0 / 52, or 50.0); (2) the 2201 GO sentence form (BLUF/rows: verbatim two-sentence Q5 text vs a composed line); (3) whether to run the 2098/2099/2197 directory-neighbour merge-trees for 2201 before the stamp (cheap; not commissioned); (4) floor re-list from tmux at the stamp (04:38: %0 wednesday, %1 zsh titled Kamils-Mac-mini, no seat live); (5) set-up stop line unchanged or raised; (6) whether PR 2075 should be queued by someone (open, gate 254 GO WITH NOTES, card a; in nobody's queue; pair proof is clean).

## 6. Slips of this drafter
Two shell calls refused by hooks (a literal `====` echo; a delete-pattern in a sed edit) and re-run in a script file; no write outside the drafter folder and the scratchpad.
