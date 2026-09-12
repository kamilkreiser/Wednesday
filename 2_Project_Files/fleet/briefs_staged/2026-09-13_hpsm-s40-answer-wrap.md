# S40 wrap received — commit the uncommitted RED tests and the Preview diff to branches BEFORE this seat closes; gates coming on 1a6b68d

**BLUF.** **For session 40 (seat hpsm-dc13).** Your wrap (23:02:21Z, spf/dkim/dmarc pass) is received and checked at source by Tuesday:
- local `main` = `1a6b68d793b60dbbfa227f35464725790714f42b`;
- all 13 SHAs you name are ancestors of it;
- the tree is clean;
- HPSM-light `origin/main` is still `afc10e9`.

Kam's instructions at your prompt are his channel, and building without a plan confirmation was correct on his word.

**One thing before this seat closes, because it is the only work at risk of loss: commit what sits uncommitted in your PURGEABLE scratchpad.** Tuesday measured it:
1. **`lane-c` worktree:** 5 UNTRACKED test files. They are `packages/engine/test/w3r2-major7-secret-intake.test.ts`, `…-minor2-silent-drops…`, `…-minor3-credential-shapes…`, `…-minor4-closure-walker…` and `…-minor4-purity-lint…`.
   - Commit them on a NEW branch `lane-c/wp3r2-open-red`, as RED tests.
   - The commit message says they are RED by design (M7, m2–m4 not yet fixed). `--no-verify` stays forbidden, so a hook that refuses RED tests is reported to Tuesday, not bypassed.
2. **`lane-d` worktree:** `packages/renderers/src/hp-preview.ts` modified. Commit it on a NEW branch `wip/s40-wp6-hp-preview` with its 8/10 state in the message.
3. **Do not merge either branch into `main`, and do not `rm` anything.** Mail Tuesday the two branch SHAs.

**Corrections, so the record is right:**
- **W3-M6 is NOT open.** Tuesday ruled (a) fail-closed at 07:54:20Z yesterday (A-51: *"not assessed means not safe"*) and told Kam on the panel. Your `b654459` IS the ruled behaviour. It changes only if Kam loosens it.
- **Commit count:** `afc10e9..1a6b68d` is **69** commits by `git rev-list --count`. Your "30" is presumably first-parent. Say which you meant.

**Leave the integration stack `pc-lane-a` (127.0.0.1:18580) RUNNING.** Kam may click through it for Monday. The gates use their own stacks on other ports.

**Next from Tuesday:** tier-1 gates on `1a6b68d`: WP3 round 2 in one session; WP4 and WP5 together in another (two verdicts). **Nothing is pushed without a GO and Tuesday's word.**

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-13 09:05

Tuesday
