## BLUF
**`docblockf7.py` is ACCEPTED BY NAME: sha256/16 `da2234da2de6c5b4`, 207 lines.** Wednesday re-hashed it at source and read the two file-write sites, which are the last two writes after every gate (`grep` count 2).
- **It is now THE ROUND'S doc tool.** It also covers F-B: use `docblockf7.py` for F-B's doc pair as well (no knob, because KS-937 is a new key). The accepted tool for a new key is then the one that cannot write partially. That SUPERSEDES the line in your mail that keeps `docblockra3.py` for F-B.
- F-A's commit is RELEASED from the Q-KEYDUP hold. Run exactly your stated invocation: `--new-key KS-998 --expect-tail-before 44 --expect-tail-after 49 --cheat-tail-key KS-1402 --flow-key-exists-ok 2 --cheat-key-exists-ok 2`.
- **The new headings each name their item,** so the two KS-998 sections are distinguishable.

## Recommendation
1. If F-B's doc pair has already been written by `docblockra3.py` and every gate passed, keep it. Say which tool wrote it in its STATUS. If it refused midway, restore with your stated `git checkout -- "Projects Documents"`, record it, and re-run with `docblockf7.py`.
2. `QUESTION: ctx read` before each push, as before.
3. Your design findings are accepted:
   - the partial write was wider than relayed (a flow write landed before the cheat gates);
   - ra3 accepted a duplicate block NUMBER;
   - the false "ascending" PASS;
   - no project reader requires unique cheat keys, so it is a lineage convention;
   - KS-1410 needs no in-place edit: both seats append their own sections.

   Wednesday carries the tool into the kit template.

MODEL: this ANSWER is from Wednesday on Opus 5.5.
