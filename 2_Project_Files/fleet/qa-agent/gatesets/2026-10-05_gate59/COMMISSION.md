# gate59 — the commission (Wednesday -> kit drafter, 2026-10-05 ~16:40 AEDT), as received

QA gate KIT DRAFTER for Wednesday. Client Secuura / Blockchain. Build the kit folder `fleet/qa-agent/gatesets/2026-10-05_gate59/`
(README.md first, with the exact launch command at its end; kit.json; checker scripts; prompt template; `repin_and_launch_gate59.sh` with
`--dry-run`). Write ONLY inside that folder and the drafter's scratch `…/scratchpad/g59/`. Never write under `/Volumes/DevMASTER/!CODING`
(read verbs only; any fetch / merge-tree only in the drafter's own `git clone --shared` scratch clone, fetching from
`git@github.com:Secuura/Distributed_Secuura.git` with the checkout's `core.sshCommand`). Refusal-arm tests use scratch paths only. Do not
launch the gate; do not edit `fleet/inbox_routing.conf` (the routing line goes in the README for Wednesday).

SHAPE: copy the newest T1 kits — gate57 (merge-in / Q-M handling) and gate58 (T1, frozen proofs) — and the gate charter
(QA_AGENT_CHARTER + BRIEF_TEMPLATE). Every checker gets a positive control and a must-fail tamper arm, both run.

THE CHANGE: READY `fleet/briefs_staged/2026-10-05_seatE2_READY_1382.txt`. PR #1382 (KS-1005: change-password reads the hash it verifies),
author + merger Seat E 2nd, pane `Secuura/Blockchain-E`, GO string `GO (Seat E 2nd): merge 1382 on gate59`. Head 80bafc849a54 (a MERGE-IN:
parents 4346bc7fbdf8 built commit + develop 46c3e20cfbd2), END_TREE ada5b278269e, develop 46c3e20cfbd2. Tier T1 (auth surface:
services/auth/src/routes/users.ts change-password). Brief: `fleet/briefs_staged/2026-10-05_seatE2_successor.md` (row 1) + Wednesday's ITEM 0
ruling (row 1 merge-in folded before first push; Q-M = M1-M4).

The gate must: C1 pin (head/develop by ls-remote + PULLS API, exactly 4 paths differ from develop: ks1005 test, routes/users.ts, two
platform-k docs; 2 parents; 0 trailers); C2 the users.ts hunk only (read against the KS-1005 ticket's claim: change-password must read the
same hash it verifies; 404 kept for passwordless accounts per Q-1005); C3 red-first BY ASSERTION at develop vs head for the 6 cells, the
auth suite before/after (0 new reds; name the ks949 timeout class if it recurs), tsc with a positive control; C3b a security probe: wrong
current password -> refused, right -> accepted, passwordless -> 404 at head, plus a timing/enumeration note if measurable; C4 docs §4 (block
19. in NUMBER order after 12., stated-timings rule, no other block edited) and the merge-in resolution (remerge-diff touches only the two
docs); C5 PR text (Refs KS-1005, ticket URL, NOT COVERED incl. session revocation on password change and §5f live sweep owed); C6 NOT COVERED
list; plus the census of other open PRs touching users.ts. Squash subject to declare: the built commit's subject "KS-1005: change-password
reads the hash it verifies" (verify <= 92 as it lands, no (#n)).

Reply with: kit path, every checker's control + tamper result, the routing line, the launch command, and every doubt for the gate to rule.
