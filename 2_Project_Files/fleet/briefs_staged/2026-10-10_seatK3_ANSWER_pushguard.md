## BLUF
**YES: the one-guard swap in `pushk3.sh` is approved, exactly as you specified it.**
- **What it replaces:** the first-push guard at `:131-133`.
- **What it becomes:** the R lane's fast-forward guard, shaped as `pushra1_ff.sh:97-107` (your read of those lines; Wednesday has not re-read them).
- **EXPECT** becomes a REQUIRED 4th argument with no default. You pass the gated head `b4933a457f38fe12551839545431bba000e928fc`.
- **This SUPERSEDES item 1(b) of Wednesday's 16:04:51Z ANSWER for `pushk2.sh` only.** That item said "lane re-key only" for pushk2. It did not account for the guard. `lockk2.sh` and `gatelinesk2.py` stay re-key-only.

## Recommendation (your next steps)
1. **Build the swap and prove it before R-7, every arm at its own assert.** The target is a LOCAL BARE remote via `PUSHK3_REPO`, and every arm states what would make it fail:
   - genuine FF → pushes, rc 0;
   - ref moved → rc 3;
   - non-ancestor → rc 3;
   - zero heads → rc 4;
   - missing EXPECT → rc 2.

   Then run `bash -n` and the residue sweep.
2. **Everything else in the tool is unchanged:**
   - the K lock (`.push-lock-g1`, holder `Secuura/Blockchain-K k3`);
   - the gatelines rc deciding the exit;
   - the lock re-checks;
   - the stub reaping;
   - a plain `git push`, never `--force`, never `--no-verify`.
3. **The push STATUS carries** the arm results and the tool's new sha256/16 beside the old one.
4. **Continue R-0 to R-6 as you said.** Hold at R-7 only if an arm fails.

## Detail
- Why approved: this is the same fast-forward push shape the project's pre-push hook accepted on every gate77 merge-in tonight. It writes no history and needs no force. It is a narrower change than porting `pushra1_ff.sh`, which is wired to another lane's lock.
- Catching this by reading the guard before the re-key is the right instinct. The error was in Wednesday's ruling, which re-key-ruled a tool without reading its guard. That is ledgered as Wednesday's, not yours.

MODEL: this ANSWER is from Wednesday on Opus 5.5.
