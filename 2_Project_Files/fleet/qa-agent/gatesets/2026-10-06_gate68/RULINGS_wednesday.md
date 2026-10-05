# gate68 — OPEN QUESTIONS for Wednesday (the drafter rules none)

Q1. **Merge seat.** Seat B 65th (the author) says it is "wrapping cold" in its new-head addendum. The kit therefore forbids 63rd, 64th and 65th in the GO; the repin script refuses rc 9 on those seats. Which B seat merges? Pass it as `--merge-seat <NNth>`.

Q2. **The merge-in target tree on develop 3f9ff4e1e1b9.** The two KEY-ANCHORED cheat rules now disagree:
- `last` (the gate66/67 rule) gives `1711f2b944a8`, with KS-1278 after KS-938.
- `after-pred` (gate65 D7's "OURS above THEIRS") gives `5dab555016b7`, with KS-1278 directly after KS-1005 and before KS-938.

git merge-tree conflicts on the cheat and auto-merges the flow MIS-ORDERED, so it is a DIVERGENCE either way. Which tree does Q-M M1 hold the merger to?

Q3. **X9, real PostgreSQL.** Does the gate get a named exception to run `c3b_pgprobe_gate68.py`?
- What it uses: homebrew PostgreSQL 18.3 on the host, initdb in the gate's scratch, 127.0.0.1 only. No Docker, not repo infra.
- Why it matters: the repo's own Postgres is docker compose, which the hold forbids, so without X9 the C3-REAL-POSTGRES row is NOT RUN.
- What the drafter measured on b5adaba751d8 (a prediction, not evidence): 9/9 PASS, with two concurrent sessions at 1/0 and the control (develop's unguarded statement) at 1/1. Its planted arms U1, T1, T5b and K1 each FAIL as intended.

Q4. **Batching.** #1394 (gate67) is the other open PR that edits both docs. If it lands first, does KS-1278 go after KS-723 (`last`: `0b4c3a265454`) or after KS-1005 (`after-pred`: `a395bd88579b`)? gate67's own figure `e23888941fda` was keyed to 22b2 and is now void; on 3f9f its predict gives `6884601a03dc`.

Q5. **Is a measured assertion-strength gap GO-blocking at round 2 of 2?** This covers T5 if it is still uncaught at launch, and the gate's own T5b. T5b appends ` OR TRUE` after the exact clause text. It is predicted BLIND to b5adaba's R2, which uses a substring match plus slice(-2). On a real database T5b updates every row of every tenant. The prompt asks the gate to rule; Wednesday may pre-rule.

Q6. **Squash subject.** The PR title is still round 1's: "KS-1278: revoke decides already-revoked in the UPDATE, not only on the read" (75 chars). The commit subjects are those of 97ce2f (84 chars) and b5adaba (79 chars). Which one is the squash subject? The gate declares what is TRUE of the diff.

Q7. **KS-TICKET placeholder.** documentRepo.ts:583 says "tracked separately -- see KS-TICKET." at both 97ce2f and b5adaba. Is that ticketed residue, or a fix-before-merge?

Q8. **Routing.** The line in `ROUTING_LINE.txt` has not been added to `inbox_routing.conf`. The real launch refuses rc 1 until it is.

---
## RULED BY WEDNESDAY (2026-10-06, before launch). Each ruling is final for this gate unless the gate measures it wrong; if it does, say so in the verdict.
- **Q1 merge seat: Seat B 67th.** The B lane's next seat. B 66th is on #1394 now. GO string: `GO (Seat B 67th): merge 1393 on gate68`.
- **Q2 target: the TAIL rule, the same as gate66/67.** A new cheat section goes LAST in merge order: on 3f9ff4e1e1b9, KS-1278 after KS-938 → **`1711f2b944a8`**. gate65's "after KS-1005" reading is superseded. The gate's qm checks decide; merge-tree's divergence is reported, not followed.
- **Q3 Postgres: named exception GRANTED** for `c3b_pgprobe_gate68.py` on the HOST's homebrew PostgreSQL only, in a scratch database the gate creates and names `gate68_*`. No docker, no project config change, no other database touched. The database is reported in the verdict and left in place (never dropped by the gate; Wednesday disposes of it). If the host PG is not running, X9 is NOT RUN with the reason.
- **Q4 batching:** if #1394 lands first, the same TAIL rule applies (KS-1278 after KS-723: `last` = `0b4c3a265454`), RE-PREDICTED at the GO on whatever develop then is.
- **Q5 assertion-strength gaps at round 2 of 2: NOT GO-blocking on their own** when the PRODUCT behaviour is proven correct (X9 on real PG + N1/K1). The gate reports T5 and T5b as measured (caught / not caught). An uncaught one is RESIDUE: the merger files ONE ticket on the board account (search first by symbol), and the verdict names it. A PRODUCT defect remains blocking.
- **Q6 squash subject:** `KS-1278: key the guarded revoke UPDATE on the row the read resolved, not external_id` (84 chars; 92 with ` (#1393)`). The gate states whether it is TRUE of the whole diff; if not, it proposes one ≤92.
- **Q7 KS-TICKET placeholder (documentRepo.ts:583): ticketed residue, not fix-before-merge.** A comment-only change would move the head and void the gate. The merger adds one facts-only line about it to KS-1424's tracking (on Wednesday's relay).
- **Q8 routing:** added by Wednesday before launch.
- **Author-claim defects 1-3 and 5** (the flow-doc :2293 "at the branch base" sentence, N2's 22P02 claim, the placeholder, T5b): the gate classifies each. A FALSE sentence in a platform doc is reported with its severity; Wednesday decides whether it rides in the merge-in or becomes a follow-up.
