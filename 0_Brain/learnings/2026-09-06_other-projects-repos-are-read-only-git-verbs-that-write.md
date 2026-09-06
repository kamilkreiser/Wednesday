---
date: 2026-09-06
type: correction
source: ledger w=2 — 10:28 `git fetch` in the NexusAI checkout (self-caught), 15:2x `git merge-tree --write-tree` ×2 in the Secuura checkout (self-caught one call late)
status: live
tier: W
---

# Another project's checkout is READ-ONLY for git too — `fetch`, `merge-tree --write-tree` and `worktree add` WRITE into its `.git`; predict a merge by naming the seat that runs it, never by running it there

**The operative case, so the headline matches it:** Wednesday is about to run a `git` command with `-C <another project's checkout>` to verify a merge, predict a merge-tree oid, or bring a commit into view. **Ask: does this verb write to `.git`?** `diff`, `diff --numstat`, `merge-base`, `rev-list`, `show`, `cat-file`, `ls-tree`, `ls-remote`, `log`, `grep` — READ. `fetch`, `pull`, `push`, `merge-tree --write-tree`, `worktree add/prune`, `checkout`, `reset`, `stash`, `commit`, `tag`, `gc` — WRITE. A write into an agent's checkout from Wednesday's hands is hard rule 1 broken (stay in the project folder; manage, don't do), however harmless the objects are, and it happened twice in one day because the two verb classes look identical at the prompt and no headline named the line.

**The two cases (2026-09-06).** (1) 10:28: to verify S41's merge, `git fetch origin <branch>` was run inside the NexusAI agent's live checkout because the merge commit was not yet in the local objects — `FETCH_HEAD` and objects written. (2) 15:2x: to predict the #854 and #855 merge oids for two gate briefs, `git merge-tree --write-tree <develop> <head>` was run twice inside the Secuura agent's checkout — two tree objects written. In both cases no ref moved and no working tree changed; in both cases the pickup file's standing note ("a `merge-tree --write-tree` also writes objects — cite the seat that ran it, have the tester re-derive") and the 10:28 ledger row were in context. The rule existed as a row and a note; it had no handle.

**How to apply:**
1. **Verify a merge from the agent's own receipt** (parents + tree oid + stat, DKIM-verified) plus `ls-remote` from Wednesday's seat. When origin holds a commit the local objects lack, the merge fact is the agent's to re-derive on request — or Wednesday clones by SHA into its OWN scratchpad (`git clone --shared` from the checkout is itself read-only on the source) and runs the write verbs there.
2. **A merge-tree prediction in a brief names the instrument and the seat:** "predicted by the tester in its own copy" or "the builder's merge-tree in its worktree, quoted". Wednesday's own prediction, if ever needed, is made in Wednesday's clone.
3. **Before any `git -C <path>` where `<path>` is outside `/Volumes/DevMASTER/WEDNESDAY`:** read the verb against the WRITE list above. If it is on it, stop.
4. **Enforcement candidate (w=3 promotes it):** the pretooluse hook that refuses `cd` gains a clause refusing `git -C <path outside WEDNESDAY>` followed by a write verb, and `git fetch|pull|push|merge-tree --write-tree|worktree` with the tool's cwd outside WEDNESDAY.
5. **When it has already happened:** disclose it in the artefact the objects were written for (the brief's provenance line: "run by Wednesday IN THE BUILDER'S CHECKOUT — a write; re-derive it, do not trust it"), record the row, and tell the seat whose repo it is if anything could be observed (`FETCH_HEAD` moved; dangling objects — nothing an agent's workflow reads).

**Family:** [[2026-07-31_manage-dont-do]] (rule 2: editing that project's files from Wednesday's hands is not allowed — `.git` is its files) · [[2026-08-15_a-gui-open-is-a-write]] (an action classified as reading that writes) · [[2026-08-13_headline-must-match-the-operative-case]] (a rule without a headline does not fire) · [[2026-08-09_an-enforcement-you-must-arm-is-not-one]] (the w=3 clause).
