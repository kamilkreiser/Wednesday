# A_REPORT: drafter A, B1742 decision pack, JOB A (Tuesday reviews; nothing posted)
Clock: started 16:59 AEDT, finished about 17:12 AEDT, 2026-11-19. Read-only: Jira GET (credentials read in-process by name from each project's own 4_Credentials/.env), gh -X GET under each project's own GH_CONFIG_DIR, git not used, decision_queue.sh list/show/prior only. HPSM-POC: not read, listed or named. Scratch and scripts: fleet/state/s293/d1742/a/.

Result: 3 cards, 1 not-a-card. Files in this folder:
- card_composer-reviewer-round-hold-1119.json (A1)
- NOT-A-CARD_composer-guided-hold-1119.md (A2)
- card_mps-hosted-deploy-main-317bbb14-1119.json (A3, deploy)
- card_mps-seed-secret-renewal-1119.json (A3, secret; the commission's single A3 id was split in two because they are two decisions)

## A1 composer-reviewer-round-hold-1119
Question: has the reviewer's current review round ended? Recommended b (still running, keep holding); default: nothing changes, ask again in a week. Honest reason: nothing in the records says it ended, and a wrong "ended" costs the reviewer's own review engagement.
Verified (2026-11-19): C-92 (line 1682), C-99 (1762, 1771), C-71 COMP-1 (b) (1286) say the owner says when the round ends; no entry C-100 to C-153 records an end (headings read, whole file searched, control fires); Jira PCOMP-19, 20, 92 held, last touched 2026-10-23; PCOMP-94 (five questions) still Backlog, needs-kam, no record of the send; three ruled cards quoted in the card.
Unverified: whether the round ended (only he knows); whether he sent the five questions; the state of the L1 branch; the demo's engagement counts now.
FINDING that changes the sweep: "13 behind the round" is only 3 (PCOMP-19, 20, 92). PCOMP-31 to 35 wait on L0-1 (PCOMP-29, Not started, no hold on it) and PCOMP-36 to 39 on L1; C-92 says they "may be built and merged on branches", the round only times the release. PCOMP-29 itself has no hold. So the L0-1 -> L1 -> L2 chain is buildable on branches today under Tuesday's grant, subject to PCOMP-29's catalogue source (lives on a sibling project's branches; its ticket calls that the coordinator's call). Also PCOMP-42 says it starts after L3-1 (landed as PR #87 per the sweep) and PCOMP-44 is the conditional start the sweep names; I did not re-check them.
Prior ruling: yes, the policy (hold until the round ends) is ruled three times; only the fact is open, so a card is right.

## A2 composer-guided-hold-1119 -> NOT-A-CARD
Reason: C-71 COMP-2 (a), ruled 2026-10-12 20:12:54, "No Guided work until you turn it back on"; C-52 / card composer-guided-view-1006 c (2026-10-06): Guided hidden, reversible. No later entry changes it (searched; control fires). The hold's end is his own switch, not a pending decision. Ten keys read (all Backlog; 9 held label, PCOMP-75 held by comment 41225). Nothing becomes buildable; the ten should not be counted as "waiting on Kam". Oddities: PCOMP-84 is the Expert dashboard, PCOMP-86 is held under COMP-16. Unverified: that Guided is still off on the demo today (relayed only; no host request). An "off for good" card was not drafted; wording is in the NOT-A-CARD file if Tuesday wants it.

## A3 MPS hosted deploy and seed secret (two cards)
The sweep's premise is stale. It relied on CLARIFICATIONS.md line 1708 ("hosted runs e027ebd0, deploy not ruled"). Later entries show: hosted swapped to 0bb3ed12 on 2026-11-12 (C-145) and to 5e800095 on 2026-11-16 11:31 to 11:34 AEDT (C-166), both on his rulings; the secret was found expired at both (C-145, C-165). Everything about the hosted state is relayed, not probed (no az, no host request allowed).
Verified now: main = 317bbb14 (gh GET 17:04:55; control 404), ahead 18 of 5e800095, 27 files, 0 open PRs, CI push runs success. Only one of the 18 commits changes the live site (MPSCALC-372 template path setting plus start warning); the rest are tests, stub, docs. Standing rule (line 324, C-164) that each deploy has its own card. The 1116 card and C-165 say the secret ruling covered one deploy only.
Card 1, deploy (recommended a: deploy without the three seller checks, same rules as 16 Nov; default: nothing deployed). Frees: MPSCALC-372 (needs this deploy); MPSCALC-224 (next host read); MPSCALC-187 only if he allows a hosted brief to ride along.
Card 2, secret renewal (recommended a: he renews it in the Entra portal, his step; default: nothing happens, third ask at next deploy). Frees: MPSCALC-395 after one seller pass.
Unverified: that the hosted site runs 5e800095; that the secret is still expired (last measured 2026-11-16 11:25); the exact portal path and where the new value goes; whether the 18 commits hold any customer word (titles read, diffs not); the three small src/ diffs (Dtos.cs, csproj, PriceBookImporter.cs) not opened.
FINDING: of the sweep's 11 keys, only 372, 224, 187 and 395 genuinely wait on this deploy or the secret. MPSCALC-103, 222, 226: their 2026-11-15 comments say the refusal was built (MPS #192, deployed 2026-11-16 per C-166) and the tickets stay open on other clauses. MPSCALC-135, 251, 297: test tickets that wait on test legs, "nothing is put on a host". MPSCALC-173: its open clause is the seed identity's role. MPSCALC-144 is a lead for Tuesday, not part of the cards: his 2026-10-17 ruling (b) waited for MPSCALC-202 and 203 to be live on the host; both read Done today and #192 reached the host on 2026-11-16 (relayed), so the data step (an Administrator adds three catalogue items on the hosted inventory) may be raised again, as a separate small card.
Prior rulings found: seven MPS deploy cards and the two secret cards, quoted in each card.

## Not done / limits
No diffs of code were read; no Jira write; no mail. A background search of Tuesday's own notes for an "end of round" mention was started and is not part of the cards; the project records are the cited source.
