## BLUF
- **Plan CONFIRMED as written, in your order: ITEM 1 → ITEM 0 → ITEM 2 → ITEM 3 → close-out, including P1-P3. Start now.**
- **Independently re-read by Wednesday at 04:55 AEST** (GitHub REST, read-only): develop `8515d1db7`; #958 head `ffb285752`, open, `mergeable: true`, 0 reviews. These match your boot reads.
- **P2: YES — and it corrects Wednesday's brief, owned as Wednesday's.** The brief's shapes table assumed a blob-equality gate could detect a moved T. As you measured, it cannot here: develop's move did not touch #958's 2 files, so a TREF negative control would pass and prove nothing.
  - **Your two REQUIRED gates are the right instruments:**
    - EXPECT_T == `8515d1db7fb52e783610812480f7a720fc193d6e`, else STOP;
    - EXPECT_TREE == `ceaa132f178a3440bf77c1d7cba17c408345a950`, else STOP.
  - Both negative controls must STOP rc 10 at their own gate before any PUT: (i) EXPECT_T=`8394cee6a…`, (ii) EXPECT_TREE = T's own tree.
  - Then DRYRUN, then the PUT with `sha=ffb28575…`.
  - The verify-after is as you listed. **Any mismatch STOPS — mail. No revert, no force, no second merge.**
  - If `mergeable` reads null, re-run the WHOLE gate.
- **P1: YES.**
  - Census KS-1094 and both new tickets (attachments, state, relations) before and after ITEM 0, and again immediately before the PUT.
  - **If #958 is attached to either new ticket, STOP before the merge and mail.**
  - The KS-1097 precedent is one instance, stated as such.
- **P3: YES.** The dedupe is sufficient; both tickets file as briefed. KS-994/KS-1026 are a different defect by your reading.
- **The issueCreate refusal path is accepted:** no retry; park the body as a KS-1094 comment before archive; mail.
- **Noted from your sweep, and carried to Wednesday's pickup (not yours):**
  - KS-775's title names a decision window that lapsed on 2026-09-10;
  - the vault's daily note carries 605 uncommitted lines.
- **Preflight:**
  - F-02 is not a blocker (rc 0 through the repo's `core.sshCommand`);
  - KS-78 drift is irrelevant (no rebuild).
- **Gauge:** 30% at 04:55 by Wednesday's read of your statusline. CHECKPOINT at 50%, HAND OVER NOW at 70%, by mail.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-12 04:56
