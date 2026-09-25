#1259 KS-906 CASE6CWD: drop the inert cd, and pin that the leg ignores the caller's cwd
head 8a2a28f50eb3453db7284da0f098f6a819d40145

## BLUF

CASE 6 of the KS-859 suite did `cd /tmp` to simulate "outside a work tree", but the leg resolves its root with `git -C "$DEV_DIR"`, so **the process's cwd never reached the answer.** The case passed for a different reason than the one its name gave, and a reader copying the cell would copy an inert precondition.

**Measured at `6e2a00bfe`, both halves of the premise:** the harness invokes the leg by absolute path (`bash "$DEVDIR/scripts/preflight/…"`), and the leg derives `DEV_DIR` from `"$0"` at `:83` then asks `git -C "$DEV_DIR" rev-parse` at `:123`.

## The ticket asks three things, and the first is already done

It asks to *"make the precondition explicit … rather than relying on `cd`, and rename the case to say so. Drop the `cd`."* **The explicit precondition already exists at `:200-211`**, added by KS-916 F-02 (the ancestor walk for a `.git`). So what remained was to drop the inert `cd` and rename the case to name the real mechanism — that `$DEVDIR` itself is outside any repository.

## And one cell, because otherwise this change has no red proof

Dropping an inert line cannot go red. **CASE 6b pins the property the `cd` was gesturing at without testing:** the leg's answer is independent of the caller's cwd. It asks the same leg, about the same `$DEVDIR`, from two different working directories and requires byte-identical answers. That is the **KS-853 / KS-1034 class this repo has been bitten by twice**, so it is worth a standing guard rather than a deleted line.

**⚠ My first version of that cell could not fail.** It compared `/tmp` with `$WORK/c6` — **both outside any repository** — so a cwd-dependent leg would have answered identically from both. It now uses `/tmp` and `$HERE`, which is inside this checkout.

## Test Evidence

**Touched:** `Blockchain/Dev/scripts/__tests__/no_tracked_credentials_root.test.sh` (1 file, +31 / −3).

**Ran — the in-hook gate on this push:**
- `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` · `legs 3 4 8 — local stack not up`. **Quoted as INCOMPLETE, not as a pass.**
- **`no_tracked_credentials_root` 16 passed, 0 failed** — the declared figure (15 before).
- `pre_push_hook_base` **28/0** · fixture guard **6/0** · `run_shell_suites` **49/0** · **shell suites 60 passed, 0 failed, 0 skipped (of 60)** — unchanged by this PR.

**Ran — RED / GREEN:**
- **GREEN 16/0**, with CASE 6b passing.
- **RED against a cwd-dependent copy of the leg** (`-C "$DEV_DIR"` removed, tamper verified applied): **7 passed, 9 failed**, and **CASE 6b is among the failures** with the right diagnostic — from `/tmp` it says *"not inside a git work tree — nothing to check"*, from inside the checkout it scans the real repository and says *"OK — no tracked credential files"*.
- That arm reds 9 cells because a cwd-dependent leg is fundamentally broken; the breakdown is reported rather than the number. CASE 6b being in the set is what makes the new cell falsifiable.
- `bash -n` rc 0. The inert `res=$(cd /tmp && run_check)` call: **0 remaining**. CASE 6b's two deliberate differing-cwd calls: **2**.

**NOT run / NOT covered:**
- **Legs 3, 4, 8 did not run** (no local stack). 12/15.
- **CASE 6b compares two cwds, not all of them.** It proves the answer does not vary between one directory inside a repository and one outside; it does not enumerate every cwd.
- **Nothing about the leg's behaviour changed** — this is a test-harness change only, so there is no product behaviour to verify either way.
- **No measurement on Linux.** macOS `/bin/bash` 3.2.57 only.

**Migrations + config:** none. Test-harness only.

`Refs KS-906`; does not close it. Parent `ks859` written un-hyphenated so no attachment lands on it.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

