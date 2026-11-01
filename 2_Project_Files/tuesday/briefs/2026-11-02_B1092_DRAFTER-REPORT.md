STARTABLE: YES

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-02_B1092_SEAT-R127_mps-records-b1086-b1078.md` (seat `Datasec/MPS-R127`, Sonnet, no ports, template B1082). Unstamped it reads 6 lines with the four-underscore pattern (5 slots + last line); non-ASCII 0. Drafted 04:28 to 04:37 AEDT 2026-11-02.

## BLUF
1. MPS #139 landed (squash b7cf1ad0, merged 04:05:16 AEDT, 8/8 checks, ci attempt 1 success). MPSCALC-312: Backlog, 0 comments; both Done-when clauses read MET at code main (blob of contract = blob of snapshot = 6adc6e0f; five refusal phrases 0, control 6). Slot default MOVE-TO-DONE. STATUS lines 137-138 are the right pointers.
2. Corrections to the commissioning: (a) the GP-column sentences are only PARTLY stale: code fills 3 of 4 columns for a purchase (oneOffGp, tcv, totalGp), tcv for a rental, annualRecurringGp never (MPSCALC-315 open); line pointers moved after the sync (openapi.json:1409, snapshot:1409, schema.ts:1430, API.md:367-368). (b) MPSCALC-195 item 6 (generated headers) recorded NOT MET by B1082 is probably answered by #139: BACKLOG row only, no second comment. (c) B1078 is the gate of MPS #138 (MPSCALC-300), not of 312.
3. B1078-4/-5/-6 all still hold at b7cf1ad0 (quantityAuditModel.ts:100,101,104). No duplicate in Jira (dump 362 keys, controls fire). Plan: T1 guard gap (lane-v0), T2 GP sentences word-pack ticket (lane-v2), T3 zero-quantity decision, T4 one tests-only ticket for -5 and -6 (one-ticket-per-test-pass rule).
4. Scope addition (04:35) folded in: MPSCALC-300 (PR #138, squash 6e0aa641, 02:45:01 AEDT, Backlog, 0 comments re-read). Lean COMMENT-ONLY: clause 1 says "the ruled reading" but the gate says the rule is the coordinator's reading, not a product-owner ruling (B1078_STATUS.md:170; C-79 :1716). Move only if the seat finds a ruling at source.

## Facts re-measured (instruments in the kit)
Root main cdfa19f6, C-79 highest at 1712, B1082 section at 2065, 2098 lines, records newest b1082, no lock, remote 0. Jira 362 keys, Done 127, Backlog 235, 655 comments, highest MPSCALC-362 (B1082 created 358-362). Panes at 04:31: M71 live, no MPS-R pane; anchored `^Datasec/MPS-R[0-9]+$` 0 now (1 after launch), unanchored would fire (1 now, 2 with G274). Ports none; seat names R127/B1092 free (controls R126, b1087 fire). Hosted: compare to e027ebd0 reads `behind`.

## D-decisions
D1 Sonnet. D2 target 60 / hard stop 120 minutes. D3 up to 9 writes (7 expected). D4 no ticket for B1078-1/-2/-3 (BACKLOG rows). D5 no sentence drafted for the GP wording. D6 tickets carry no gate mutant ids.

## Q-questions for Tuesday (default in brackets)
- Q-1 T3 and T4 as two tickets, or one (all three findings)? [two: -4 needs a decision first]
- Q-2 DONE-300: COMMENT-ONLY or MOVE-TO-DONE? [COMMENT-ONLY, see BLUF 4]
- Q-3 MPSCALC-195 item 6: BACKLOG row only, no comment? [yes]
- Q-4 Lanes/tiers for T1 (lane-v0 t2), T2 (lane-v2 t2), T3/T4 (lane-v5 t2)? [as written]
- Q-5 T2 as a new ticket, or a comment on MPSCALC-315 (shares the unfilled fourth column)? [new ticket, Related 315]
- Q-6 model-routing.md:98 (C8) does not name records seats (only grep "records" hit is line 117); earlier records kits cited it anyway. Keep C8/Sonnet? [yes]

## UNMEASURED
No request run for the GP columns; B1083 builder STATUS not read; PurchaseCalculator.cs zero-line claim not re-read; rental fleet-line counts of existing rows only from call shapes; hosted state relayed.

## Outside-the-fences disclosure
Writes: the kit and this report only; scratch (Jira dump script and JSON, code-main tarball) in the session scratchpad. Jira GET only via my own scratch reader (.env in process, no token printed); gh only `-X GET` under the project GH_CONFIG_DIR; git read verbs only. Two of my own Bash calls were refused by hooks (a stray `cd`, an unquoted `=`-word); no effect. Not read: briefs_staged, scoreboard, ledger, decision cards, WEDNESDAY/FRIDAY trees. I read the sweep only as directed by the coordinator's mid-task message (section 4 lines 83-90).
