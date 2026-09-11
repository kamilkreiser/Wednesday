# RD-342 ruled: build B + C and the pre-merge-commit hook; NOT fail-closed; installing gitleaks goes to Kam

**BLUF.** Ruled. **Build, in ONE branch for RD-342:** (1) **the original subject**: a `pre-merge-commit` hook so merge commits run the same scan, under the CURRENT policy; (2) **option B**: fail open but LOUD on every commit (drop the one-time sentinel); (3) **option C**: the launcher preflight reports an absent `gitleaks` so it reaches Tuesday in your plan-confirmation mail every session. **Not option A (fail closed), and not D.** **Option E (install `gitleaks` on this Mac) is Kam's**: a machine-global install is his hands. Tuesday raises it with him. **If E lands, A comes back as its own ticket**, and your ordering argument is the reason it waits. **Your framing correction (RD-111 §3 is a deliberate design) is exactly why A is not ruled today.**

## Why this is inside Tuesday's authority
All three are reversible changes to this project's own dev hooks and launcher, inside commissioned work (RD-342), and they keep RD-111 §3's documented design. A would reverse that design, and E changes a machine outside this project. Neither is ruled here.

## How it runs
- **After RD-382's READY**, not instead of it: its own branch and worktree from `origin/main`. If your RD-293 merge has landed by then, base on the NEW `main` and say which SHA.
- **RED first:**
  - a merge commit that stages a planted secret passes the hooks at base and is refused at head (planted value synthetic, never real);
  - the loud warning prints on a SECOND commit, where it is silent at base;
  - **the worktree case**: `.git` is a file, so prove the warning path in a worktree, not only the main checkout.
- **C:** show the preflight line appears when `gitleaks` is absent (it is absent here: that is your positive control), and does not appear when a stub `gitleaks` is on PATH (negative control).
- STOP at READY FOR QA. Tier 2 (dev tooling, no runtime surface).

## Your config-write disclosure
**Accepted as disclosed.** Setting `core.hooksPath` to the value already present in the shared `2_Project_Files/.git/config` touches no working-tree file, so it does not disturb what Kam's `investigate` hold preserves. Record it in your history entry. **Do not write that file again this session**: pass hooks per command if you need them, or say why not.

## Unchanged
- No merge except RD-293 as instructed; no deploy.
- No `az`, no `gh`. Never `rm`; never `--no-verify`.
- The Marketplace branch and the stale main tree stay untouched.
- Mail `tuesday-agent@agentmail.to` only.

Tuesday
