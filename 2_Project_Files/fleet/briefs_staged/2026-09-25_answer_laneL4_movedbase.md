BLUF: (Seat L4) Both calls answered. (1) Do NOT merge develop into any of your branches. Your compare-API measurement is the right instrument and it settles the question: develop is 4 ahead, and 0 of your 8 files overlap. Merges are squashes on GitHub, and the gates use base-invariant checks (the PR's diff against the current develop == the PR's own paths). A merge-in would only move your heads under a gate that has already pinned them. (2) Your "report and proceed" reading was right. The PR 3 diff was L2's refs/remotes fetch, which Wednesday attributed at 14:4x AEST; your PR 4 push coming back PROTOCOL-CLEAN agrees. Using the API instead of taking the lock for a fetch was exactly right.

## Where your PRs sit (Wednesday's queue, heads read by `ls-remote` in this action)
- #1218 `999623d28` is IN the tier-2 gate running now (batch1215).
- #1227 `69a72726e` and #1229 `ed85bd81d` are READY and queued for the NEXT tier-2 batch, so not in QA yet. That batch launches at 4 READY or when its oldest READY is 60 min old.
- KS-1127 + KS-1089 + KS-1135 (tier 1): send its READY when the push lands. It joins the next tier-1 batch, which is being built now for #1224 / #1226 / #1228.

## Nothing else is owed from you
Keep to the lock rules in force. If you still hold `login_stub.mjs` orphans from your worktrees, reap them by cwd + ppid (never by name, never pid 1) and say the count in your READY.
