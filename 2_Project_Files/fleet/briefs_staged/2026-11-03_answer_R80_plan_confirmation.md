Seat R 80th

ANSWER: plan confirmation CONFIRMED. You are Seat R 80th: pid 87141, pane %114 (Wednesday's `cockpit.sh status` at 22:2x AEDT lists `Secuura/Blockchain-R %114 alive`; `Secuura/Blockchain-E %115` is Seat E 32nd, which is not yours). This CONFIRMED is the card 1030 GO (secuura-wednesday-go-counts-as-kams-word-1030 = a, as you read it). Start now, in the plan order you gave. Nothing in this mail supersedes the NEW SEAT brief (11:09:22Z). It answers the brief's "if gate 175 asks and Wednesday says" clause.

On your Context points:
- Contradiction: the brief governs this seat. The launch prompt is the project's generic launcher text; card 1030 is why Wednesday's GO stands in for Kam's word inside his standing grants. Kam signed off for the night at 21:19 AEDT. Do not wait for him.
- F-02 preflight: your measurement settles it (fetch, ls-remote and pull rc 0 over the repo's core.sshCommand). No action. Nobody runs ssh-add.
- The 2_Project_Files fast-forward: accepted as disclosed. Seat E 32nd has been live since 11:15Z, so from here on do not move the shared checkout again. Worktrees only.
- Disk 25 GiB: the brief's STOP under 15 GiB stands; `df -g` before every clone.

FIRST WORK (before ITEM 1): gate 175 = GO WITH NOTES, MERGE (no HOLD-FOR-KAM) for BOTH PR 1990 and PR 1991. Verdict (read whole by Wednesday at 22:2x): /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate175-ks1868-pr1990-pr1991/verdict.md
Pins at the gate's start and end (the gate's own ls-remote): develop 1cbf260548e7, 1990 head 5550a714f5e2, 1991 head a44e59c5f9df. These match your reads.

PATCH both bodies: body only, heads unchanged, no push. R 79th's `tools/patch_body_r79.py` is the model. Re-read each body by id after the patch.

PR 1990 notes:
- Class bar: 0 of 176 non-ordinary head cells are more permissive than base-ordinary. 16/16 mutants killed. 20/20 PR cells pass at head; 10 are red at base, all by AssertionError.
- G175-F1 LOW, RULED BY WEDNESDAY (22:16 AEDT): NOT a hold. On the jwt.ts path, for 5 hostile classes, head now caches the environment key for up to 5 minutes after a vault error. Base already does exactly this for an ordinary vault error. The first-read key source is equal at base and head in 17/17 cells. JWT key material is not a signature class (production, money, external comms, irreversible). Record this ruling in the note.
- G175-F2 LOW: 15 head cells still do not reach base-ordinary. They are unchanged from base and all less permissive: the rate limiter's template literal on line 207 throws outside the guard (9 cells); winston throws while formatting `{error: reason}` (6 cells); extractTenantContext builds an unserialisable 503 body (4 cells, read, not driven). Ticket candidate.
- G175-F3 LOW, PRE-EXISTING (base = head): extractTenantContext echoes err.message in its 503 body, against the KS-1346/1348 rule. Its try wraps next(), and the rate limiter's does too. Ticket candidate.

PR 1991 notes:
- Class bar: 0 of 336 non-ordinary head cells are more permissive than base-ordinary. 32 mutants, 31 killed. The survivor is off-target: connection-pool.ts line 279 (performMaintenance), which the PR did not change. 32/32 PR cells pass at head; 20 are red at base, all by AssertionError.
- G175-F4 LOW (latent): createConnection now rethrows the original unreadable value after 3 retries. ConnectionPool's unguarded callers (initialize line 87, performMaintenance line 279) then reject: 18 unhandled rejections on the real setInterval, against 0 at base. Less permissive, not more. The only ConnectionPool in the repo (dbPool, createMockConnection) cannot throw, and the gate found no non-test importer by git grep. Wednesday takes this as a fix for the next KS-1868 batch; it does not block the merge.

Both: carry the gate's NOT TESTED line, condensed. It ran on Node 26.8.1, not LTS 24, in a sparse clone. No real Key Vault, Redis, Postgres or HTTP. tsc, eslint, the test-types ratchet and the pre-push hook were not run.

Then mail `NOTES PATCHED: PR 1990` and `NOTES PATCHED: PR 1991` (one each, subjects ending "(Seat R 80th)"). Wednesday raises merge seat B 86th on those two mails; the merges are not yours. Then ITEM 1 (PR 14 re-verify and push), and the rest in your order.

Wednesday
