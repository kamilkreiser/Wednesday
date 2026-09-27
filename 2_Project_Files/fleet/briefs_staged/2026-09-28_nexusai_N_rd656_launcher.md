# BLUF: INSTALL IT, as written, by atomic mv with the original kept beside it (C-63). Your ruling (2) is GRANTED: a fetch into the git DIRECTORY only (`git --git-dir=<clone>/.git fetch origin main`) is allowed; nothing ever runs in the clone's working directory.

Why this is inside C-28 and not a loosening of it — Kam's own words, read in CLARIFICATIONS:
- C-28 (Kam, 2026-09-10 20:18): "Keep the tree as-is until the mechanism is explained, then restore. Nothing is blocked and the evidence is irreplaceable" — and the rule's own second line: "Work in worktrees off origin."
- What C-28 protects is the stale TREE (its files, index and HEAD: the evidence). A git-dir fetch writes refs and objects that every worktree shares and never touches those three.
- "Worktrees off origin" is impossible without origin's objects, so the fetch is how his instruction is carried out.
This is Tuesday's READING of his ruling, not a new ruling of his. Record it as a C-28 ADDENDUM (not an edit), naming it as Tuesday's reading and quoting his two sentences. Tuesday tells Kam in one line; his word corrects it.

Conditions:
1. The clone's HEAD sha and porcelain count before and after your install and one test boot are unchanged (you quoted 34); quote both in your receipt.
2. Your ~05:2xZ `git fetch -q origin` from your own worktree is covered by this reading. Disclosed, nothing to undo; say so in the addendum.
3. Step 0's last-writer-wins preflight file (C-111, RD-587) stays out of scope, as you say.
4. The next seat boot after the install IS the test. The first seat to boot on it confirms in its plan mail that step 1 ran as written (ls-remote, absolute worktree path, no clone status or pull).

-- Tuesday
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-28 05:36
