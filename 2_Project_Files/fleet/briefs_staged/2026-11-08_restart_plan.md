# Restart plan, Secuura/Blockchain fleet, drafted 2026-11-08 (drafter, read-only; Wednesday to confirm)

Sources: P = /Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/NEXT-PICKUP.md (11-07 UPDATE blocks win). V/<gate> = /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/<folder>/verdict.md. M = /private/tmp/wed_newmail/batch_20261108T092844Z.txt (Secuura rows only). LR = `git -C .../Blockchain/2_Project_Files ls-remote origin` (read 2026-11-08, no fetch). Q = `decision_queue.sh show <id>`.

## BLUF
1. develop is now a65ae7ed1d60 by LR (PR 2054 squash, M row 1, B 97th, 2026-11-07T00:14:33Z). Every gate verdict was written against b27f5fb30f4a (or earlier); B must recompute tree/pin per PR. Every open PR head (2058-2090, 2052) equals its verdict head by LR; none has moved.
2. Queue now (GO / GO WITH NOTES, no open card): 2062, 2065, 2063 (already B's next three per M), then 2060, 2066, 2077, 2072, 2082, 2083, 2084, 2086, 2069, 2074, 2068, 2070, 2078, 2071, plus conditional ones (body edits first): 2067, 2080, 2085, 2087, 2076, 2081, 2059, 2073(after round 2).
3. HELD on an OPEN Kam card: 2061 (ks1536), 2075 (ks2083), 2079 (ks657). NO GO: 2052, 2058, 2064 (round 2 gate 253 owed). Gates owed: 252 (2088, 2089, 2090) and 253 (2064 r2).
4. Kam's seven rulings (all a, ruled 2026-11-08 20:28:02-20:28:23 per Q) fund: pre-run third round (X), KS-2059 + KS-2060 builds (U), KS-1231 read-only fields (R), KS-1081 production guard (J), disk deletion of merged gate clones. TWO MORE cards were ruled a at 20:31 (ks1152, anchoring) that the task brief did not list: see C.8.
5. Mail: Agent Mail daily cap reset was 11-07 11:00 AEDT (P line 62); current state UNMEASURED today. All seats and gate subagents are dead; P says gates die with the seat and re-launch from commission.md unless verdict.md exists. All 24 gate folders 230-251 have a verdict; only 252 and 253 do not.

## A. MERGE QUEUE for B 98th (proposed order; B reads GOs by mail, one at a time; no mail to B between a GO and MERGED, P line 52)
Merged by LR (merge ref absent) and NOT to queue: 2040-2051, 2053, 2054, 2055, 2056, 2057 (B's own list, M row 1, agrees: ...2049, 2050, 2051, 2053, 2055, 2056, 2057 and 2054 merged).

A1. Already told to B (ADDENDUM 00:01:58Z, M row 1): in order 2062, 2065, 2063. B's last mail said it would want each READY then a GO.
| # | PR | Ticket | Head (verdict) | Verdict | Verdict path | Condition before queuing |
|---|---|---|---|---|---|---|
| 1 | 2062 | KS-864 | 71566cce6101 | GO | V/2026-11-07_gate249-tier2-batch | none. Gate notes an older PR 2032 overlap (merged since by LR). |
| 2 | 2065 | KS-709 | 9eb86dfdaa20 | GO | V/2026-11-07_gate243-tier2-batch | none |
| 3 | 2063 | KS-1503 follow-up | 3e94297ec9a8 | GO | V/2026-11-07_gate243-tier2-batch | none |
A2. Next, proposed order (mine, drafter's reasoning: 2060 first because T's PR 8 and V's 2086/2087 overlap grants name its branch, P lines 30, 44, 46; 3a before 3b per Y):
| # | PR | Ticket | Head | Verdict | Path | Condition |
|---|---|---|---|---|---|---|
| 4 | 2060 | KS-1536 3a | 796ea55fb8eb | GWN | V/2026-11-07_gate244-tier1-ks1536 | P line 32: "2060 may queue". Notes to rule at queue: F1, F2, F3, F4, F5, F7, F8 (wording). Commission fault (rm line vs QA no-rm) to reconcile. |
| 5 | 2066 | KS-2032 | baf577c78e7f | GWN | V/2026-11-07_gate245-tier1-y-auth | none; its comment F1 to tell Y (P line 33). F3 role-constructor ticket later. |
| 6 | 2077 | KS-2081 | b387a6ef1c02 | GWN | V/2026-11-07_gate240-tier1-pr2077-ks2081 | P line 25: queue it. After merge a filing seat owes F1, F2, F3, N2, N5 tickets (one per test pass, verdict path in full). N1 (reads) told Kam, no ruling. |
| 7 | 2072 | KS-1448 | 14f402572f1a | GWN | V/2026-11-07_gate246-tier1-services | P line 34: "may queue"; 72-1 cross-tenant minor to be filed by a board seat. No body correction named for 2072. |
| 8 | 2082 | KS-1534 | 75c1282a64dc | GWN | V/2026-11-07_gate249-tier2-batch | none; file F-1 (P line 37) |
| 9 | 2083 | KS-1505 | 72182689bace | GWN | same | none; file F-1 |
| 10 | 2084 | KS-1858 | 223499281cb9 | GWN | same | none; file F-1 (Google toLowerCase, GitHub /user/emails unpinned) |
| 11 | 2086 | KS-736 | c70f8182f43d | GWN | same | queue AFTER 2060 (overlap grant at 796ea55fb8eb; P line 37 "Merged 2086 with 2060 not run" is ambiguous, see Contradictions). File 2086 F-1 (K cells ask specRouteMap). |
| 12 | 2069 | KS-1613 | 3f4ca578d3e3 | GWN | V/2026-11-07_gate247-tier1-tests-tooling | verdict says tier 2 would do. Edits scripts/preflight/preflight.sh. |
| 13 | 2074 | KS-1728 b2 | e8c950ecb30d | GWN | same | F74-1 conditional Major (check-package-format.sh:730 may exit 0 silently under GNU grep): "ticket and measure before relying" (P line 36); queue is Wednesday's call. |
| 14 | 2068 | KS-2080 | 1be849a4fc94 | GWN | V/2026-11-07_gate243-tier2-batch | none |
| 15 | 2070 | KS-2079 | 0ae8aa98046c | GWN | same | F-2070-1/-2 can refuse a legitimate shape in a push guard: "follow-up round or tickets, my call at the queue" (P line 29) |
| 16 | 2078 | KS-1560 | e702127f3790 | GWN | same | F-2078-1 (refuse legit) and F-2078-2 (pass bad): same call as 2070 |
| 17 | 2071 | KS-1370 | 697226c8395d | GWN (nine cells never ran in gate) | same | P line 35: decided; G 29th's own run (evidence/next/tampers/baseline.json, develop d00221c38e12) is the record, not independent; say so in the GO. |
A3. Conditional (body or word edits first):
| PR | Ticket | Head | Verdict / path | Condition |
|---|---|---|---|---|
| 2067 | KS-2071 | 0d08681c616d | GWN, V/gate246 | body corrections 67-1, 67-2, 67-4 first (P line 34); 67-3 filed. C 36th wrapped: a board seat edits. |
| 2080 | KS-1670/1641 | 83ee8509c985 | GWN, V/gate246 | body correction 80-3 first; file 80-1, 80-2 |
| 2085 | KS-2074 | 4d4726ca41d9 | GWN, V/gate248 | body lines false (G1 line 11, G2 line 27, G3, G4): correct before queuing; G2's 404 on mid-life DB fault contradicts Wednesday's ruling: ticket it; Wednesday's rulings there are wider than KS-888: tell Kam (P line 38). G 29th wrapped: a successor makes the body edits. |
| 2087 | KS-1600 item 3 | 954af815c7b7 | GWN, V/gate251 | may queue after a successor fixes F3 stale DRAFT header if taken as a round; F1 null mints ['read'] narrower than Kam's "matching": told on panel, default stands; F4 ticket. After 2060 (overlap grant on its branch). |
| 2076 | KS-2058 follow-up | 8ce56b0f9a86 | GWN, V/gate242 | decide first: H2 ("my driver", unmeasured "vanishingly rare") words only: one small round by F 35th then compare, OR ticket with H1, H3, H4, H5 (P line 28). Must merge BEFORE U's KS-2060 push (P: Kam "no push before F's follow-up merges"). Also before Z's KS-1733 (waits 2072, 2073, 2077 per P line 44). |
| 2081 | KS-1171 8k | 17c453253d68 | GWN, V/gate248 | body fixes F3, F4. Card secuura-anchoring-second-fee-on-empty-reply-1107 RULED a (Q, 20:31:42): merge, two tickets (High empty reply, Medium mint), build seat fixes empty reply next under tier 1; anchoring deploy stays held for Kam's word. |
| 2059 | KS-1410/1214 r2 | 5d8969b36a24 | GWN round 2, V/gate250 | BEFORE its GO: R2-1, three false client-read sentences: Z 5th edits the PR body AND EDITS comments 4eb82d57 and e997f1d3, moving no head. Ticket R2-2 to R2-7 (incl. Jenkins recipe exit 0 on subdir / spaces). |
| 2073 | KS-1152 | 9709acff5c5f | GWN, V/gate245 | Card ks1152-rotated-true-on-count-zero-1107 RULED a (Q, 20:31:45): include count-0 fix, ROUND 2 of 2 on PR 2073; the head will move, so it needs a new gate. NOT queueable at 9709acff5c5f. |
HELD on an open Kam card (Q shows status open, no ruling, as of 2026-11-08):
- 2061 (KS-1536 3b, edcb42e7ae99, GWN V/gate244): card secuura-ks1536-bare-admin-loses-all-tenants-1107, default unmerged. Also 3a before 3b, 3b forward-move is doc-only only if KS-2083 not first on users.ts.
- 2075 (KS-2083, d2245bf37fe0, GWN V/gate245): card secuura-ks2083-session-end-race-in-flight-1107, default unmerged; "closes" wording must be corrected.
- 2079 (KS-657, 0fffdfba0f95, GWN code only V/gate241): card secuura-ks657-redis-security-store-delete-1107, default unmerged.
NO GO: 2052 (KS-1081, 0e5b29380ddc, V/2026-11-06_gate233-tier2-pr2052-ks1081; card ks1081 now ruled a, J builds round 2, new gate needed); 2058 (KS-1231, 93bf64e29276, V/2026-11-06_gate236-tier1-pr2058-ks1231; R builds round 2); 2064 (KS-1205, round 1 head 836e21a79d9e NO GO V/gate247; round 2 head 6c8856baf102 awaits gate 253).

## B. GATES OWED
- Gate 252, tier 2 batch, Sonnet, STAGED: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate252-tier2-batch/commission.md. PRs 2088 (KS-1797, 0f0933afd24b), 2089 (KS-1493, 3796e4b90c6a, comment in a test file), 2090 (KS-692, 4c4f696f7699, docs fragments, no preflight ran). Heads equal LR.
- Gate 253, tier 1 round 2 of 2, STAGED: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate253-tier1-pr2064-r2/commission.md. PR 2064 head 6c8856baf102 (equals LR). Must read comment 195d740a posted before any gate (M, T 14th READY). A further NO GO ships what is closed and tickets the rest. NOTE: commissions say leave clone at /private/tmp/gNNN (no-rm wins).
- READYs in M with no verdict covering them: NONE found. Every Secuura READY in M maps to a verdict: Y (2075, 2073, 2066, 2060, 2061), K (2074, 2063), W (2077), E (2072, 2065), V (2087, 2086), J (2070, 2069, 2078, 2068), T (2090, 2083, 2064 r2, 2088, 2082, 2084, 2062, 2089), C (2067).
- Also owed (not in M): V 26th's/Z's READYs seen only through P (2059 r2 gated at 250). Gate for 2073 round 2 (after J/Y round) and for any U/R/J/X round-2 heads.
- Gate 241-251 commissions each say: do not relaunch (verdict exists).

## C. BUILD WORK FROM KAM'S SEVEN RULINGS (Q, all `ruling: choice='a'`, ruled_ts 2026-11-08T20:28:02-20:28:23+11:00)
1. secuura-prerun-push-third-round-1106, a = "One narrow third round (recommended)": "One seat fixes the blocker and the Majors only, one tier 1 gate on the changes, then the side-by-side and one real push. A NO GO ends it for good." Owner: lane X (X 7th wrapped; successor X 8th owed). Read first: gate 237 verdict /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-06_gate237-tier1-x7-prerun-driver/verdict.md (blocker: a failing git status reads clean, line 6) and X 7th's HANDOVER (path UNMEASURED: pickup names none; try !CODING/Secuura/Blockchain/5_Project_History/2026-11-0*_seatX-7th/HANDOVER.md). STANDING_LINES.md:96 amended only after a GO (P line 51). KS-2047 parked. Note P line 50: "on a third round a: one seat, blocker and Majors only, tier 1 gate."
2. secuura-ks2059-design-tenant-scope-named-route-1106, a = "Take the package, one global DAO (recommended)": "U 17th builds it after KS-2060, migration included, under a tier 1 gate." Owner U (U 17th wrapped; successor owed). Read first: U 17th HANDOVER, FINAL block first (M, U wrap: REC/HANDOVER.md under U 17th's record folder; exact path UNMEASURED, pickup names seat U 17th only). Local state: KS-2059 failing cells commit 29c2dda8403f on feature/ks-2059-governance-an-admin-in-one-tenant-can-set in worktrees/s-u17-work (X1, X2 red on purpose; do not push until fix is on it).
3. secuura-ks2060-address-in-history-dpia-1106, a = "Remove it from governance history (recommended)": "Votes, proposer and delegation addresses blanked on erasure; tallies kept. Data-destroying path, tier 1 gate. The DPIA's tables updated after you rule." Owner U. DPIA edit follows the ruling (whose hands: UNMEASURED).
4. secuura-ks2060-clear-wallet-null-migration-1106, a = "NULL, with migration 059 (recommended)": "U 17th builds it under the tier 1 gate, spec line and refusals included; goes through Kintsugi first." Owner U. Merging a migration is close to applying it; demo frozen. KS-2060 local commit a35d4c0d06372b3a3d647757e8ac971b40ade2f3 (worktrees/s-u17-work, 13 files, on develop 90b500e19883, NOT pushed). Push needs exact-name OVL grant on heads of 575, 649, 1360 and must wait for PR 2076 (F's follow-up) to merge (M, U update 18:3xZ; P line 54). Push cap: drivers MAXTURN 20000 (P line 56).
5. secuura-ks1231-nine-fields-share-integrations-key-1106, a = "Show the nine fields read-only for now, with a note (recommended)": "The page cannot write them while the key is shared. An admin cannot edit those nine from this page until KS-2035 decides their home. No gateway change." Owner: lane R (R 87th wrapped; R 88th owed; r88_waiter.sh at fleet/state/r88_waiter.sh was NOT launched, 429 at 23:19, P line 65). Work = PR 2058 round 2 of 2 (head 93bf64e29276 NO GO gate 236). Read first: R 87th HANDOVER (path UNMEASURED; pickup: "PR 2058 round 2 from its HANDOVER, KS-528 driver pid 69770 and its PR chain, row C2 Sonnet") and brief /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-06_seatR87_ks528.md (the file did not appear in my 40-line listing: UNMEASURED if it exists). PID 69770 is dead (reboot). KS-528 at 258e049aaf75 was to queue (P line 55); no KS-528 PR visible in LR 2040-2090, UNMEASURED which PR number.
6. wed-disk-25gib-delete-merged-gate-clones-1106, a = "Delete merged gate clones once": "I read each PR merged at origin, delete those clone folders only, keep verdicts and evidence, report df before and after; the no-delete guard stays as it is otherwise." Owner Wednesday herself. See E.
7. secuura-ks1081-template-flips-secrets-production-path-1106, a = "Keep the template's values, and make production refuse them (recommended)": "Local stacks stay as they are. The production guard refuses the published values, demo-service is refused or left out on the production overlay, the rate limit, log level and network become must-set rows, and a test proves none reaches production unedited. A little more build, tier 1 gate." Owner: lane J (J 20th wrapped; J 21st owed, P line 46). Read first: J 20th HANDOVER FINAL block (5_Project_History/2026-11-06_seatJ-20th/HANDOVER.md, M J wrap). KS-1081 round 2 committed b80833a5b67c on 0e5b29380ddc, NOT pushed, proved locally (118 passed; docker half 23 assertions not run); push steps (A) merge develop in (one shared path check-stack-safety.sh). Plus gate 233 findings F2, F6, F7, F8, F10 and now F1, F3, F4, F5 "per option" (P line 97). Credential check fix is separate. New gate needed.
8. Not in the seven but ruled a at 20:31 (Q): secuura-ks1152-rotated-true-on-count-zero-1107 (round 2 of 2 on PR 2073, Y lane) and secuura-anchoring-second-fee-on-empty-reply-1107 (merge 2081; two tickets; build seat for the empty reply, tier 1). Y 6th wrapped? UNMEASURED (Y's last mail 00:15Z, no wrap in M).

## D. OTHER SEATS OWED (P; all dead after reboot, launch order is Wednesday's)
- V 27th: KS-1090 (yes, one exact-name grant PR 945's branch at head 264098fce62b; PR 945 merge ref present by LR 945 => open), plus fix rounds for 2086/2087; HANDOVER FINAL block first (P lines 24, 40). KS-1090 NOT started.
- S 35th: items D and E of S 34th; keys KS-2095 to KS-2100 read at source; gate 235 F3 vs PR 2057 body; C 36th's five filing candidates; SDK type on KS-1733 + README from gate 240; ks488 TS2300 (originate); the post-merge ticket filings listed in A (G235 F2/F4/F5/F8, G240 F1/F2/F3/N2/N5, 72-1, 2086 F-1, 2084 F-1, etc.); W1 High (originate events.ts:143-145 empty catch). (P lines 45, 53)
- Z 5th: PR 2059 round 2 PR body + comment edits (R2-1); KS-1733 item 4 (local head 57cfcc0f23d1, NOT pushed, waits 2072, 2073, 2077; forward-move then queue once) (P lines 30, 44, 39).
- T 14th successor: round 2 PR 2064 gate 253; PR 8 KS-1462 (adminConfig.ts, head f637b59288f0) on hold until PR 2060 merges; KS-1788 item 2 / KS-1545 step 2 not built (T wrap in M).
- B 98th: merge seat; B 97th estimated under 70% context (P line 70); reads GO by mail subject in 12-hex shape: 'GO: merge PR N at <12hex head> on develop <12hex pin> (Seat B 98th)' (M, B QUESTION: its go_gate refused a 40-hex subject).
- R 88th (C.5), J 21st (C.7), U successor (C.2-4), X successor (C.1), Y successor (2073 r2, KS-2063 waits on KS-2032 which is 2066), W successor (KS-2081 deploy etc.), E (Akto re-run when ~6 seats, load1<7), K (batch 2 fix rounds in worktrees s-k18-ks1728b2, s-k17-ks1503c), C (staking image at next Kintsugi), AA 5th (anchoring, deploy held), G, F 35th (2076 small round if chosen), D (Kintsugi, KS-2073), S/others per P.
- Wednesday's own: send_brief error body + daily send counter warning near 800 (P line 26); Agent Mail plan card wed-agentmail-daily-limit-upgrade-1106 (money, Kam).

## E. DISK CARD (Q wed-disk, ruled a): "read each PR merged at origin, delete those clone folders only, keep verdicts and evidence". Do NOT delete in this plan.
df /Volumes/DevMASTER now: 25Gi free, 99% (measured this run).
Pickup-named boot-volume clones: g245 (PRs 2066, 2073, 2075), g246 (2067, 2072, 2080), g248 (2081, 2085), g249 (2062, 2082, 2083, 2084, 2086, 2086). Locations are /private/tmp/gNNN on the BOOT volume (V/gate245 line 166; V/gate249 line 56; V/gate246 line 272; V/gate248 line 188), not DevMASTER. `ls /private/tmp` now shows 19 entries and NONE of g240-g253: gone (reboot or cleanup, UNMEASURED which). None of those PRs is merged by LR (all have refs/pull/N/merge present, see A), so NONE qualify under the card anyway. Deleting boot-volume clones would not free DevMASTER either.
Other /private/tmp clones named in gates: g242 (PR 2076, open), g245 etc: also absent.
Gate folders on DevMASTER that contain a `clone` dir (found by ls) and PR merge state by LR (merge ref absent => merged or closed, not overclaimed):
| folder under 0_Brain/reference | PR | LR |
|---|---|---|
| 2026-11-06_gate217-tier1-pr2032-2036/clone | 2032, 2036 | merge ref absent (B list says merged) |
| 2026-11-06_gate218-tier2-pr2037-2038/clone | 2037, 2038 | absent (B list: merged) |
| 2026-11-06_gate219-ks1951-pr2039/clone | 2039 | absent (B list: merged) |
| 2026-11-06_gate220-ks1613-pr2040/clone | 2040 | absent (B list: merged) |
| 2026-11-06_gate221-ks1136-pr2041/clone | 2041 | absent (B list: merged) |
| 2026-11-06_gate229-tier1-pr2048-ks2038/clone | 2048 | absent (B list: merged) |
| 2026-11-06_gate231-tier2-pr2050-ks1707/clone | 2050 | absent (B list: merged) |
| 2026-11-06_gate232-tier1-pr2051-ks2058/clone | 2051 | absent (B list: merged; P line 99: 44ee04cba478) |
| 2026-11-06_gate234-tier1-pr2053-ks957/clone | 2053 | absent (B list: merged) |
| 2026-11-05_gate199, 199r2 (PR 2009), 200 (2010), 201 (2011), 202 (2012) /clone | 2009-2012 | absent; B's list names 2009 merged; 2010-2012 not in B's list: merged-or-closed UNMEASURED, do not delete under "merged" without a check |
| 2026-11-03_gate155-ks1868-pr1972/clone | 1972 | refs/pull/1972 not seen in my range: UNMEASURED |
Also `repo`, `wt`, `base` dirs exist in gates 209-216 (not listed per PR). Per the card only merged ones qualify; only deleting `clone` folders is authorised; sizes UNMEASURED (no du run). Verdict/evidence files kept.

## Contradictions and gaps between sources
1. Task brief says gate clones g245/g246/g248/g249 exist; the folders are absent from /private/tmp (the only place gates and P place them) and none of their PRs is merged.
2. P line 33/62 names merge order but P line 37 "Merged 2086 with 2060 not run" is unclear: it may mean gate 249 did not run 2086 together with 2060, not that 2086 merged. I read it as the former.
3. P line 16 (11-07 11:0x) says B ADDENDUM queue 2062, 2065, 2063 after 2054; M row 1 confirms; but B's "READY for 2062 follows" and the later GOs are not in M (batch ends 00:17Z). State after 11-07 00:17Z is UNMEASURED (only LR shows develop a65ae7ed1d60 = 2054; no later merge visible).
4. P's gates all pinned develop b27f5fb30f4a; develop is now a65ae7ed1d60. Verdicts remain valid per SHA of heads but need a merge-tree recompute (B does it).
5. P line 25 says 2077 "may queue at the reset"; brief says Kam card ks657 etc. are open; these three cards (ks1536, ks2083, ks657) and wed-secuura-usage-89pct are still `open` in Q even though Kam has logged in.
6. The brief lists seven rulings; Q shows two additional rulings at 20:31 (ks1152, anchoring) that change 2073 (round 2, head will move) and 2081.
7. KS-528 PR number and R 87th/X 7th/U 17th HANDOVER paths are not in P; I did not find them. PR 2052 ls-remote head equals gate 233 head, so J's b80833a5b67c is still unpushed (consistent with P).
8. P line 12 says "NONE OPEN WITH HIM (ten ruled 21:04)" while later P lines list open cards (ks657, ks1536, ks1152, ks2083, anchoring, disk, ks1081 etc.). The later lines win by the 11-07 UPDATE rule.
