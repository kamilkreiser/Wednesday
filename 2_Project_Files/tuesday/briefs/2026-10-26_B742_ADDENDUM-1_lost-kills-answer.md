# B742 ADDENDUM-1 - Tuesday's answer to your STOPPED question (the 13 + 3 lost cells)

From Tuesday s182 (the Datasec coordinator seat), Datasec / Security Composer. This file answers the question in the last line of `1_Project_Definition/Briefs/2026-10-26_B742_STATUS.md` (STOPPED 17:12:20).

## Answer: it is a STOP for the product owner's card. Do NOT push.
Your kit's THE PROPERTY, clause 2, is binding: "no kill that `eddebf34` flags and bash 5.2 confirms may become unflagged". Clause 4 says a kill lost outside the ticketed list that `99585f7d` and `eddebf34` did not both lose is a regression of this round, and a STOP, because this is the last round. Your 13 cells are lost against HEAD. The 3 cells lost against PREV are outside the ticketed list unless your counterfactual proves them of a ruled shape. Tuesday does not regrade a binding property of a guard. The product owner decides on a card, with your measurement in it.

## What you do now, in this order
1. **Keep your work; push nothing.** Leave your one commit LOCAL in `wt-b742-fix`, never deleted, never amended, so that a "yes" from the product owner can be pushed and gated exactly as it stands. Print its sha and `git diff --stat eddebf34` in STATUS.
2. **Write the cells into STATUS under `## LOST CELLS`,** one row each for the 13 + 3. Each row gives: the input as `U+XXXX`-safe text; the line OLD, PREV, HEAD and NEW flag; the pty transcript line that shows bash failing; and the one-word context that carries the failure across lines (open bracket, dangling quote, exec replay, unclosed `$((`). Also give, in plain words, whether NEW is right about the construct and wrong only about the cross-line context. That is the sentence the card will quote.
3. **Say whether any of the 16 can arise in the real `DEPLOY.md`** (your kit: the real file holds none of the B736-1 texts; check these 16 the same way), and what OLD (main's scanner) answers for each.
4. Write `## PROGRESS and RESUME`, stop every process and container of yours, restore every mutant, release the heavy lock by move, free the port block. End the FILE with `STOPPED: NEEDS TUESDAY continue in a fresh seat from RESUME?`.

Tuesday cards the product owner with these options: accept the 16 as ticketed residue (then your commit is pushed and short-gated); hold #94 unmerged and leave main's scanner as it is; or a further round on his word.
