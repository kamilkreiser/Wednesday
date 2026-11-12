# Drafter notes: Seat R 115th brief (2026-11-12 ~23:2x AEDT)

Output: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_drafter-seatR115/brief_R115.md` (about 42.4 KB, about 2 KB over the ~40 KB target: the overlap measurement and the two orderings are the over-run). STAMP block left blank; no SELF-CHECK line; PROVENANCE line for every KS key named. Nothing written under `!CODING/`; writes are this folder and the drafter's scratchpad (blob copies, merge-file inputs, census.json, patch texts). No mail, tmux tap, board write, launch, fetch or git write verb. Reads: `ls-remote` (GIT_OPTIONAL_LOCKS=0), GitHub REST (`gh`, kksecura confirmed by `gh auth status`) pulls/files/compare/contents, `gh pr list --json files`, Linear GraphQL (key read inside python, never printed), `git cat-file -t`/`rev-parse`/`status --porcelain`/`hash-object`, `git merge-file -p` on scratchpad copies. `DRAFTER_RULES.md` does not exist at `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/` (ls error), so nothing extra obeyed.

## Queue as drafted
1. Row 50 = KS-2174 part 2, tier 2, ONE PR, Refs KS-2174 only: `userRepo.ts` the two hint arms (call lines 1764 and 1773, the raw-email VALUE lines 1765 and 1774 at develop 203585d73269; `email: account.email` -> `userId: account.id` with why-and-ticket comments), the two ks949 F2 reads (develop lines 408 and 435), a NEW vitest cell file `ks2174-demo-seeder-hint-arms-carry-no-raw-email.test.ts`, a NEW fragment pair `KS-2174-demo-seeder-hint-arms-carry-no-raw-email.html` (flow and cheat). Product and test edit are atomic (the F2 cells go red the moment the arms drop `email`), so one PR.
2. NOT this seat: KS-2173 part 2, any PR 2218 fix round (gate 342 GO WITH NOTES, no Major/Minor), KS-2101, KS-2116.
3. No second row proposed. One measured candidate described but NOT queued: `services/auth/src/services/email.ts` console lines (7 print `options.to`; census [] at 23:17; no ticket; gate 340's G340-2216-3 leaves it to the board).

## THE OVERLAP ANALYSIS (the main item; instrument: `git merge-file -p`, symmetric 3-way, scratchpad copies; NOT merge-tree)
Base blobs verified exact: userRepo.ts blob `97729fbe571b` is identical at `eab5ac6bff8d` (2216's parent and merge base), `13e62febfba8` and develop `203585d73269`, so ours/base/theirs = fix / develop / PR 2216's head is the true 3-way. ks949: merge base with 2052 is `cfb6c1573ba9` (blob `03b3ba97c6fd`, 699 lines), develop `6332a927d7b4` (704), 2052 `ca06b0b170ff` (701).

**(a) PR 2216 (head b12dd042761d, same file userRepo.ts).** 2216 changes develop lines 1754, 1796, 1842, 1865, 1867 (hunks at 1751, 1793, 1839, 1862). Part 2's lines 1765 and 1774 sit in the gap between hunks 1 and 2.
- Merge with the two swaps: rc 0, 0 conflict markers; `userId: account.id` 7 times in the merged file (2216's five plus the two). Real shape (a comment line plus the swap at each site): rc 0, 0 markers, comment present twice.
- Planted sweep, one `//x` on one develop line, 1735 to 1830 (96 lines): conflict set {1753, 1754, 1755, 1795, 1796, 1797}; everything else merges clean, including both sites.
- Distances: site 1 (1765) is 10 lines after the nearest conflicting line (1755), 11 after 2216's changed line 1754; site 2 (1774) is 21 lines before the nearest conflicting line (1795), 22 before changed line 1796.

**(b) PR 2052 (head b61674e7b763, ks949 test file).** 2052 changes base lines 533 and 573-574 (+5 -3; hunks `@@ -530,7 +530,8 @@`, `@@ -570,8 +571,9 @@`). Develop's own changes from PR 2215 are at base 28, 148, 347, 362, 547, 564.
- Baseline develop + 2052 (no part 2): rc 0, 0 markers. With the part-2 edit at 408 and 435 (token swap, and a real-shape 3-line edit): rc 0, 0 markers.
- Whole-file sweep, every develop line 1 to 704: conflict set {537, 538, 539, 577, 578, 579, 580}; nothing else.
- Distances: edit lines 408 and 435 are 129 and 102 lines before the nearest conflicting line (537); 142 lines before the second hunk's 577 from 435.

**(c) Nobody else:** census at 23:17 (`gh pr list --state open --limit 300 --json number,headRefOid,files`: 102 PRs, 457 rows, max 32 files; controls `.env.example` [2052], absent path [], test-helpers.ts [2217]): userRepo.ts [2216], the ks949 file [2052], services/auth prefix 13 PRs but none on these two paths, the new cell and fragment names [], `services/auth/src/services/email.ts` [].

**The two orderings**
- **A (recommended): cut on develop 203585d73269 now; conditional one-push grant naming BOTH PRs** (`OVL_IGNORE_PRS="2216,2052"` + `CENSUS_ACCEPT` for the two paths; conditions per R 114th's STAMP 1: merge-tree rc 0 both orders and equal trees per PR head as it stands, line-multiset survival, planted rc 1 in 2216's and 2052's hunks both orders (plant 1754 and 1796; 538 and 578), twins rc 0; any head moved: STOP and QUESTION). Needs the existing gate retargeted (it is single-target and governance-hard-wired: `PATH`, `H1/H2/TWINS`, `CALL_OLD/NEW`, the `KS-2060 round 2` check), red-proofed per target; a new cell file (2216's file is held, so its ~60-line harness is copied); two heads to re-pin. Forecast +14 to +19 (READY about 49 to 54 from a PLAN near 35).
- **B: wait for PR 2216 to merge, then cut.** One overlap (2052, the far one), one grant, gate reused as is, cells can extend 2216's SITES table (smaller PR, no copied harness): +10 to +14, READY about 45 to 49. But 2216 is queued behind B 160th's PR 2214 and no merge seat is running for it, so B can leave the seat with no row.
- **Recommendation: A**, because the measured geometry is clean (rc 0 both, nearest conflict 10 lines from site 1 and 102 lines from the F2 edit), the row is small, and waiting depends on a merge that is not scheduled. Pace arithmetic from three meters: R 112th +19.0 (first product row), R 113th +12.6 (test-only), R 114th +15.7 (34.6 -> 50.3, including a brand-new gate); 55/60 lines kept.

## Where Wednesday must rule at the stamp (numbered; the brief's STAMP block is blank)
0. PINS: develop `203585d73269`, PR 2216 head `b12dd042761d`, PR 2052 head `b61674e7b763`, PR 2099 head `8967de8b1755` (not used by this row), PR 2218 head `210e396d7cb8`; re-measure.
1. **Ordering A or B** (above). If A: the conditional one-push overlap GRANT naming two PRs as worded in the brief, re-pinned to the two heads.
2. **The gate.** Accept that the seat generalises or copies `merge_gate_r114.{sh,py}` into `merge_gate_r115` (two targets, red-proofed for each BEFORE use), or hand it a ready one. Also: R 114th's scratch bare store lives in its own `_scratch/gate_store.git`; ANSWER item 3 (alternates to `s-r90-base`) was one-seat: renew for R 115th's own record folder?
3. **Fetches.** Develop `203585d73269` is NOT in `s-r90-base` or `s-r114-ks2173` (cat-file fatal); the heads of 2216, 2052, 2218, 2099 and the bases `eab5ac6bff8d`, `cfb6c1573ba9`, `bba80c3c8e24` ARE. Rule: the URL-form develop fetch into `s-r90-base` again (objects only). Probably no PR-ref fetch needed (heads present).
4. **Pace:** accept the A or B forecast and the 55/60 lines; optional "QUESTION if the PLAN reads over 40".
5. **Fragment pair:** brief says YES (a new flow and cheat pair with distinct names; PR 2216 carried one). Confirm.
6. **Second row / email.ts:** leave `email.ts` console lines to the board, or hand it as a second row only after a ticket exists and row 50 is READY under 55 (brief says: not queued).
7. **Carried READY list** (2194, 2195, 2197, 2198, 2200, 2201): whether PRs 2216, 2217, 2218 join. Gate 340 GO WITH NOTES, 341 GO, 342 GO WITH NOTES.
8. **Protected trees:** `s-r114-ks2173` (PR 2218 open) newly protected; `s-r101-ks1053` (PR 2215 merged) and `s-r110-ks1923` (PR 2212 merged) protection ended or not (brief: not yours either way); `s-a28-ks2182` stays the read-only clone source after the seat's own root-pair proof (still matches develop's pair; defect (i) symlink still present, dated 12 Nov 16:04); `s-t24-l1` is the old pair.
9. **Kit source:** brief says shift from REC114's `tools/` as they stand (maker 22:28, `round_gate_launch_r114.sh` 22:29, `merge_gate_r114.py` 22:42 edited after the maker), not from `orig_r113`, declared. Confirm.
10. **Gate 342** verdict file mtime 23:16 (could still be written); its mail goes to R 114th's suffix, which R 115th's watcher also reads. Whether R 115th acts on an ADDENDUM naming findings (it would need a NEW governance grant against 2099).
11. **Floor:** tmux at 23:19: `%0`, `%147` (B 160th, PR 2214 only), `%1`, `%148`, `%149` (bash, untapped). Re-list at the stamp.
12. **KS-2174 closure wording:** part 2 completes the ticket's eight sites with PR 2216; the brief says Refs only, no close word, and does not claim the ninth site (routes/users.ts 678, PR 2201) or `email.ts`. Confirm.

## Established (instrument, time)
- develop `203585d73269`, 2052 `b61674e7b763`, 2099 `8967de8b1755`, 2201 `50c32501e60c`, 2214 `eb7315988de5`, 2215 `ba847c2ef9f9`, 2216 `b12dd042761d`, 2218 `210e396d7cb8`: ls-remote 23:16:16.
- userRepo.ts: raw contents + `git hash-object` + contents-API `.sha` `97729fbe571b` at eab5ac6bff8d, 13e62febfba8, develop; 2008 lines; sites at 1764/1765 and 1773/1774; last develop change 2026-11-06 (commit 581fdc8a9c71). At 2216's head the pairs read 1765/1766 and 1774/1775 (2013 lines, blob `48d8a66888e1`).
- ks949: lines 408 and 435 read by `meta['email']` (only two hits in the file; same two at 2052's head and base, lines 403 and 430 there); F2 describe lines 394 to 439.
- Part 1's cell file read whole at 2216's head (99 lines; harness, SITES table, oracle, C1; header says hint arms not covered); part 1's fragments read; 2216's PR body read; gate 340 and 342 verdicts read (first lines, notes G340-2216-3, G342-2218-1 to -6).
- PR 2215 MERGED as 203585d73269; compare `13e62febfba8...203585d73269` = 5 files; PR 2216 compare vs develop: diverged, merge base eab5ac6bff8d.
- Linear (23:1x): KS-2174 In Progress Low (PR 2216 attached; 1 comment 10:18:25Z); KS-2173 In Progress Low (updated 12:04:44Z); KS-1081 In Progress High (2026-11-08); KS-2060 In Progress Medium; KS-1053 In Progress Medium (PR merged, ticket open); KS-949 and KS-966 Done; KS-1873 In Progress Low; KS-2029 In Progress Low.
- Root pair at develop `c5649b43817c`/`11f32889c6d5`; equal in s-a28-ks2182, s-r112-ks2174, s-r113-ks2029, s-r114-ks2173; s-t24-l1 old pair. auth package.json `de3e8948b45d`, lock `cddd2274a99d` equal s-a28's; `s-a28` auth node_modules 8 entries.
- Machine 23:19: load 2.67/3.42/3.28, 2.2 TiB free, `.push-lock` absent (control `lock-holder.json` present). History guard 111th 1, 112th 1, 113th 1, 114th 1, 115th 0.
- Trees: all clean (status 0) except s-r90-base (5854 lines, stale, not touched).

## Could not establish (and what would close it)
- The real `git merge-tree --write-tree` of the row against 2216 and 2052 in both orders (the drafter may not run it): the seat's gate. merge-file is a symmetric proxy; ort can differ at the margin.
- Whether the seat's tree can run the auth vitest suite from the cloned node_modules, and the exact reach states for the two hint arms: the seat's set-up and a read of source 1695 to 1779.
- 2052's and 2216's near-term behaviour (about to merge or move): KS-1081's board state, a merge seat's plan; both unmeasured.
- Whether F2's edit shape (find by `userId`, by message, by `hint`) keeps the cells meaningful: the seat's call, said in the PLAN.
- Gate 342's verdict beyond lines read, and whether a verdict mail already exists in R 114th's mail folder: R 115th reads its mail.
- The push queue; Node 24; `%148`, `%149`.
- Slips: none that touched a write; my first sweep lines used 1-based indexing against 0-based lists and were cross-checked against the raw line prints (1765 and 1774 carry `email: account.email`; both asserted in code before replacing).
