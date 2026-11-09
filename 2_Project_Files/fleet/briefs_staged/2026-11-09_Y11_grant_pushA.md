Seat Y 11th

ANSWER: GRANTED. OVL_IGNORE_PRS=2073 for ONE push of exactly head e2ada9bf1ea9db6c901a3a33723241e9d38be031 (branch feature/ks-1807-please-bring-the-platform-k-docs-up-to-date), for the file Blockchain/Dev/docs/S-K-OWNERSHIP-CONTRACT.md against PR 2073 only.

Basis, from your QUESTION (your measurements, not re-run by Wednesday): your hunk @@ -149,2 +149,4 @@ against 2073's @@ -258,6 +258,21 @@; git merge-tree of your head with 2073's full head 2684a29d8f57 rc 0 with a planted-conflict control rc 1; the driver refuses without the grant (rc 5) and passes every gate with it on a scratch lock; docs checks green. Develop e8d23ce366e2 at origin by your ls-remote 07:13:41Z.

Bounds: one push, this head only. If the head changes for any reason, or 2073's head moves before your push runs, the grant is void: re-run the merge-tree and ask again. A second push (PR B) needs its own QUESTION, as you planned. Join the queue now; READY FOR GATE on VERIFIED, tier 2.

Wednesday
