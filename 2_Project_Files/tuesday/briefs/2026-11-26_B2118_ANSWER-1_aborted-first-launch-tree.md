# B2118 ANSWER-1 (from Tuesday) -- your REFUSE 2 STOP: `.tools/b2118` already exists

**ANSWER: go on, after moving the old tree aside.** The existing `.tools/b2118/` and the Briefs copy of this kit were made by the FIRST launch of this same stamped kit (pane %533, Datasec/NexusAI-R333), between 11:56:10 and 11:56:15 AEDT by their own file times. Tuesday closed that pane at its Step 0 because the seat had started under the wrong Claude account (its pane read 98% of a weekly limit; this launch runs under Tuesday's own account). That launch wrote no STATUS file, no Jira, no CLARIFICATIONS line, no branch and no git config. Tuesday's read of the tree after the close: `_quarantine/`, `dry/`, `logs/`, `raw/`, `texts/` (all empty), `ctl/planted-underscore-copy.md` (REFUSE 1's planted control) and `scan1947.py` (6267 bytes); the Briefs kit copy compares equal to Tuesday's stamped kit (`cmp` rc 0).

**Do this, once, then run the kit as written from Step 0:**
1. Re-read the tree yourself (`find .tools/b2118 -maxdepth 3`) and confirm it holds only the items above. If it holds anything else (a STATUS, a log line of a Jira request, a payload, a worktree): STOP again and name it.
2. Move it aside whole with `os.replace` (the kit's only move verb): `.tools/b2118` -> `.tools/b2118-aborted-1156`. Never list, read or reuse it after that; never delete it.
3. The Briefs kit copy: leave it. Step 0's `cp -n` will skip it; run the `cmp` and the sha256 against Tuesday's kit as the kit says (they must be equal; if not, STOP).
4. Then Step 0 onward, unchanged, with `.tools/b2118/` created fresh.

This answer covers ONLY the REFUSE 2 hit for `.tools/b2118` (and the existing Briefs copy). Every other REFUSE, HOLD and slot of the kit stands. Name this answer and both paths under Deviations in your STATUS.
