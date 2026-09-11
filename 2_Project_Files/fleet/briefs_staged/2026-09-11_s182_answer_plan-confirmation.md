## BLUF
- **Plan CONFIRMED. Start item 0 now.** Your four measurements are all right, and P1 and P2 correct Wednesday's brief. Rulings below; three brief lines are SUPERSEDED BY NAME.
- **P1 YES** — your tree-and-blob check replaces §1(e) for #936.
- **P2 YES** — MINOR-2 onto KS-1074, MINOR-1 recorded as a measured no-op; no new ticket.
- **P3 YES, amended** — one ticket for R2-2 + R2-3 (R2-4 inside it). **Before KS-1041 is archived, its two comment-only residuals go onto live tickets.**
- **P4 YES** — like-for-like at every site where a human's approval is the merge signal, and YES to `git fetch origin develop:develop` (fast-forward only).
- Preflight: **F-02 is not a blocker** (your fetch returned rc 0 through the repo's `core.sshCommand`). **KS-78 drift:** no rebuild this round, so it is the deploy seat's.

## P1 — SUPERSEDES brief §1(e) for #936 only
- **Wednesday's error:** "T..M changes exactly the PR's files" assumes every PR file still changes develop. #936 carries three lockfile bumps that develop already has (KS-1067 `9d84cf5a`), so a correct squash changes 2 files, not 5.
- **Ruled, as you proposed:** develop's tip == M · M has exactly one parent == T · `M^{tree}` == your prediction · T..M == the prediction's 2 originate files · the 3 systemTest locks blob-equal between T and M. Any mismatch STOPS the lane.
- #951 keeps §1(e) as written (15 predicted == 15 in the PR).

## P2 — SUPERSEDES the "file ONE ticket for both" branch of brief §1(a)
- **MINOR-2 → KS-1074** (Backlog, unassigned — measured by Wednesday 19:2x). One BLUF comment quoting `ed1b5934`'s MINOR-2 and saying the `!= null` guard belongs in that ticket's per-writer cells (one test pass, Kam 2026-09-07 13:23). **Assign KS-1074 to our board account** (Kam, 2026-09-06: unassigned Platform K items are ours). Do not start it.
- **MINOR-1:** recorded in KS-1058's closing comment as a measured no-op at merge, citing KS-1067 `9d84cf5a`.
- **No new ticket.**

## P3 — the R2 ticket, and KS-1041's close — SUPERSEDES brief §2(f)'s "otherwise Done + archived"
- **YES:** before the verdict comment, file ONE ticket for R2-2 + R2-3 with R2-4 recorded inside it — Backlog, board account, related to KS-1041, BLUF-first. The verdict comments on PR #951 and KS-1041 name it.
- **KS-1041's residuals:** "the seven other services that read trust headers" (`116ed2d6`) and "the cross-tenant JWT probe" (`116ed2d6`, `47e0b331`) exist only in comments. **Archiving KS-1041 would strand them** — Kam asked for close-and-archive "so there is no confusion", and a finding on an archived ticket is exactly that confusion.
  - **For each:** search the board by symbol or service name first. If a live ticket already covers it, add one facts-only comment there. If none does, file it: Backlog, board account, related to KS-1041, BLUF stating it was **outside Step 1 and Step 2, is not commissioned and not ruled**, and is recorded so KS-1041 can close.
  - **One ticket or two:** Kam's 13:23 rule decides — one if one test pass would prove both, otherwise two. Say which, and why.
  - **THEN** KS-1041: assigned to our board account, closing BLUF comment naming both merges (#938 → `0f8fb33c3` and #951's M), that the vouch secret stays unset (KS-1083), and the ticket ids the residuals now live on. Done + archived, `archivedAt` quoted.
- **KS-741** (Todo, ours) was held "until Step 2 lands". After #951 verifies, one facts-only comment: the hold condition is met at M. **Do not start it** — its own 2026-09-09 STOP comment names a second consequence that needs its own commission.

## P4 — item 2
- **YES** to your wider site list. Apply the handover's verbatim replacements, plus a like-for-like edit at every site where a reviewer's or a human's approval is the **merge signal**.
- **Leave alone** any sentence that describes Peter's periodic formal test passes or the demo (UAT) nod — those stand under Kam's ruling. Where a site is ambiguous, do NOT edit it.
- **The PR body lists every site:** edited, and not edited with the reason. Kam's words are quoted verbatim wherever the replacement text quotes him.
- **YES to `git fetch origin develop:develop`** before item 2's branch. Record the old and new SHA. If git refuses the fast-forward: STOP and mail.
- Item 2 still stops at READY FOR QA, and only if it fits by your 50% checkpoint.

## Unchanged
Everything else in BRIEF s182 (09:03:34Z) stands: the order, the GO heads, the holds, and #951's GO covering the merge only. Your refusals of the launch prompt's step 7, step 8 and rule 7 lines are correct.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-11 19:26
