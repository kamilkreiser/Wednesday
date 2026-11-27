# DRAFTER REPORT: Seat S 132nd In Progress sort brief (drafted 2026-11-27, about 21:30 AEDT)

Brief: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-27_seatS132_inprogress_sort.md (20,567 bytes)

## 1. FIRST: facts in the commission or templates measured as wrong or stale
1. **"212 started" is not In Progress + In Review.** The card text and the commission give 202 + 7 = 209 beside 212. Measured: the team's started-type states are Blocked, In Test, In Review, In Progress; Blocked = 3 (board_count.sh, 21:29:18), so 202 + 7 + 3 = 212. In Test returned an UNVALIDATED ZERO (script refused), so it is not asserted. Source: decision_queue.sh show secuura-board-grant-reask-1127 (bluf line) and the drafter's board_count runs. The brief says the 3 Blocked tickets are outside the pass.
2. **Kintsugi "k45 = 9c1ecde5abd6" is stale** in the S 124th brief, line 14 (and its PROVENANCE line 38, from the D 87th HANDOVER of 2026-11-24). The newer record /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-27_seatD-88th/HANDOVER.md lines 12-13, 43 shows REVISION head k46 = 4764b2cfbc28 for originate (admin-frontend and api-gateway stay 9c1ecde5abd6; auth d4ffc8308249 HELD; next stamp k47). The new brief points to the D 88th record.
3. **The S 124th's counts are stale for a start-from file**: its population was 228 (In Progress 221 + In Review 7), measured 2026-11-25 about 07:30Z (18:30 AEDT) (template line 13, 37; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-25_seatS-124th/HANDOVER.md line 3 of FINAL). Now In Progress is 202 (drafter read 21:28:52). Its 17 A tickets were closed and archived; its second look added KS-1699 as closeable, not written.
4. **S 124th brief lines 12 and 29 ordinal check**: its 'seat s 124th' count is now 1 (taken); 'seat s 132nd' = 0, 'seat s 131st' = 1, 'seat s 130th' = 1 (history.md grep, drafter). No error in the commission; recorded as measured.
5. **Stale checkout**: 2_Project_Files shared checkout was 0e6479d7b6c0 of 2026-11-10 when the 124th read it (P124 HANDOVER, traps list), and the S 131st brief line 38 says the same local tip. The new brief tells the seat to use its own clone, not the checkout.
6. **Row C8 wording**: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/specs/model-routing.md line 98 says "(Agent-tool sub-agent)"; the commission applies it to a launched pane seat. The S 121st brief used C7 for a board seat. Not wrong enough to change; raised as O1.
7. Not stale: the 250 per-request limit in board_count.sh is the linear branch's own (`PAGE=${BOARD_COUNT_PAGE:-250}` in the linear case); 202 is below it, a real count.

## 2. Measured by the drafter this session (read-only)
- Card text, option a detail, ruled_ts (decision_queue.sh show) and the EXPIRING-GRANTS.md line 44 row: quoted in the brief verbatim.
- board_count.sh linear through a python subprocess (key from LINEAR_API_KEY in the project .env, passed in the subprocess environment, never printed; the one printed-error path was masked): In Progress 202, In Review 7 (21:28:52), Blocked 3 (21:29:18). Backlog refused (more pages, not a total). Team states list read by one GraphQL query (names only).
- Ordinals in history.md; top history entry is Seat W 79th's.
- P124 census: re-hashed population.tsv, D.tsv, C_by_person.tsv (the SHA256SUMS agree with the files for D.tsv and population.tsv and C_by_person.tsv); class counts from population.tsv: A 17, B 2, C 23 (21 In Progress + 2 In Review), D 186 (181 + 5), rows 228.
- Row C8 line 98; model-routing C-rows list.
- S 131st tools directory listing (am_s131.py, rekey_s131.py exist).

## 3. Carried without a read by the drafter
- Tool bodies of P124/tools and S 131st/tools (only headers of lin_snapshot_s124.py and am_s124.py seen); the `watch` and send-lock behaviour of am_s13x helpers; the paging behaviour of the 124th's snapshot tool (23 pages of 10, per its HANDOVER).
- Stuart's four merge rules: not used, not read.
- Standing lines, holds and mail shape: read whole from the S 124th and S 131st briefs and adapted; not independently re-tested.

## 4. Could not measure
- Develop's current tip and any ticket's content (the brief gives that to the seat).
- In Test count (unvalidated zero).
- Whether the S 124th's A2.tsv rows are still accurate.

## 5. Questions for Wednesday before sending
Listed as O1 to O7 in the brief's STAMP section. The ones that change the seat's output: O3 (leave In Review 7 and Blocked 3 out of the pass?) and O5 (may a merged-but-not-on-Kintsugi ticket be pile 1?).

## STAMP (Wednesday fills)
(empty)
