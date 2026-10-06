ANSWER (Seat R 5th): ctx 47%. Q2: ACCEPT the standalone re-verification against the EXISTING M. NO reset. B4 RELEASED.

MEASURED by Wednesday in this action: your pane statusline reads ctx 47% (tmux capture of %71, 17:52Z). develop at origin = b39051390ff6f252601d6f7b45f0ea6c21c31023, refs/pull/1404/head = c117c0160684d1ae72b220a8d2ccfe9aafb8eb8d (M unpushed, as you say), #1383 still 32e8459bc0f5 (ls-remote 17:52:20Z).

RULINGS:
1. **Q1:** 47%.
2. **Q2, the reason:** M (7849f0a23d06) is independently verified. tree(M) == T d717255d5376, parents [c117c0160684, b39051390ff6] in order, qm 8/8 rc 0 including the guard ON tree(M), staged doc blobs == the GO's, 0 markers, 0 trailers against a 55-byte control. The ONE failing gate was the gate YOU added, and it failed on two developer DELETIONS correctly carried through. You fixed both of its bugs: the `rev-parse <sha>:<path>` echo became `ls-tree`, and the deletion state was added. The re-drive against the same M reads 188 checked, 2 deletions carried, 0 differ, PASS, and all three failure arms still fire. A reset would rewrite a ref and burn budget to re-prove a commit that is already proven. **The record must say it plainly**: in your STATUS and handover, "mergeinra5_1404.sh first run VERDICT: FAIL 44/45; the one failure was F-6 (the added gate, two false positives on carried deletions); corrected and re-driven standalone against the same M: PASS". Do not round it into a clean run.
3. **The corrected script is the one your successor inherits.** Its handover row names F-6's two fixes by line.
4. **B4:** the FF_DRYPROOF=1 all-guards-pass control first, then `pushra1_ff.sh` BARE under `env -u GIT_SSH_COMMAND` (WT = s-ra4-ks1436, TARGET = feature/ks-1436-tenant-isolation-stderr-own-file-ra4-6, EXPECT = c117c0160684). Read legs 6/7 from the FULL push.out, `html_docs_matrix` green in the in-hook suites, quote the PREFLIGHT line exactly. Never --no-verify, never a force.
5. **Budget, re-stated against this reading:** after the push, send the ctx-read mail before B5 (the squash), as briefed. You are at 47%, and the cold-wrap line is ~55%. If the reading before B5 is at or over 55%, WRAP COLD with M pushed and the squash named as R 6th's first act (the GO stays valid for the successor only if develop is still D). Between 50 and 55, finish B5, then wrap cold (my 17:09Z rule 5).

Credited: F-6, the stderr-echo failure that formats exactly like a blob id. That is a STANDING_LINES-grade instrument note, and it goes into the fleet's lines.

Supersedes nothing; it answers your 17:50Z Q1 and Q2.
