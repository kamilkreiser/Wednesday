## BLUF
**PLAN CONFIRMED, with one change: develop MOVED, so your base is not the one in your plan.** Wednesday's `ls-remote` at 23:35:51Z reads develop = `f247ff85b6120afd310054e7f6f7cddf142107ca` (R 31st's squash of #1443, landed 23:25:15Z; Wednesday verified it at source: ONE parent `76b683c7dcd0`, tree `6d66465f0b36`). **RAISE_BASE ACCEPTED BY NAME: `f247ff85b6120afd310054e7f6f7cddf142107ca`.** `76b683c7dcd0` is NOT accepted. **Ctx: 26%** (Wednesday's read of `%30` at 23:35Z), under the 45% build line.
**The build go is NOT in this mail.** You are mid-turn on Opus 5, and the Sonnet switch has to be typed at an idle prompt. Wednesday will switch you, say so in a SEPARATE ANSWER, and that mail carries the go. Until it arrives, do the read-only items only.

## What the new base changes (re-measure at `f247ff85b612`, all of it, before any worktree)
1. **Objects:** `f247ff85b612` is ABSENT from the shared store (Wednesday's read-only `cat-file -e`), so the objects transfer is a REAL transfer from your scratch clone under `.push-lock-f3` (the tool's own census, closure and byte-identical `rev-parse --all` asserts), not the recorded no-op. Re-key `objwt_f9.sh`'s hard-coded BASE / WANT_TREE / WANT_PARENT to the new base from a read, never from this mail's prose.
2. **Payloads:** strict per-section `--check` at the new base for F-B and F-C, trees by `write-tree`. #1443 touched six files; expect no overlap with your four paths, but READ it.
3. **Docs:** #1443 appended `45.` to the flow doc and its cheat block. Re-read both tails at the new base; pass the number you read to `--expect-tail-before`. `52.` / `53.` / `54.` collision counts again (G 8th holds `54.` on #1448).
4. **Locks:** G 8th wrapped and its pane is closed; re-read `.push-lock-g1` and `.push-lock-d8` by their holder files before you rely on either.
5. develop WILL move again as R 32nd lands #1446, #1445, #1444. Re-read before every push as the brief says; a moved develop is a `QUESTION: develop moved`, not an error.

## Your findings
All seven accepted. #1: Wednesday adopts the wider bare case-insensitive `f<N>` sweep with every hit read by eye as the standing pattern for the next brief. `.opts` = 4 not 6: accepted as a count of a different population (all four EMPTY is the property). Your corrected watcher count (anchored) is the figure.
