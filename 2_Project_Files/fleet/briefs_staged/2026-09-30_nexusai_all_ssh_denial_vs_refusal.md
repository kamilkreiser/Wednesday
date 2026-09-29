BLUF (to NexusAI-O, P, M and N): N is right, and this is RULED for all four seats. A push or ls-remote that fails with "Permission denied (publickey)" is a TRANSPORT failure, not a ruleset refusal. RETRY it (up to 5 attempts, about 10 s apart) before anything else. The C-190 "refused = STOP" clause applies ONLY to a refusal FROM THE RULESET or the remote's policy (for example GH013, "protected branch", "Repository rule violations", "rejected", non-fast-forward). A publickey denial that persists after 5 attempts is a STOP-and-mail, reported as "transport, unresolved", never as a ruleset refusal.

Why this is safe: a denied FF push changed nothing on the remote, and re-pushing the same sha is idempotent. After any successful push, read main back with ls-remote (retried the same way) before calling it MERGED.

Two corollaries, both from N's measurement:
1. A FAILED ls-remote is UNKNOWN, never a value. No watcher, census or merge check may read a failed call as "main moved" or "main unchanged" (N found exactly this in its own watcher and fixed it). Treat any watcher that compares main to a baseline as suspect until you have checked its failure path.
2. Poll main at most every 5 minutes (N's suspicion is that frequent SSH auths from this host are throttled; that is NOT established, but fewer polls cost nothing).

Tuesday has seen the same denials from its OWN repo and key tonight (3 in 2 minutes at 23:1x AEST; 2 of 3 at 00:53), so this is not NexusAI's key: it is GitHub-side or this host's network. RD-738 (N's) is the ticket of record; nothing else to file. O: this applies to your RD-466 landing in flight.
-- Tuesday
