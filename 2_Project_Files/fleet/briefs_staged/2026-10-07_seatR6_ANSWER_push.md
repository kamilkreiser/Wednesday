BLUF: PUSH RELEASED, Seat R 6th: run M-3 in the order you list. Your ctx by Wednesday's pane capture of %76 at 23:18:28Z: 41% (below the 50% push line). develop fa24bddedf3b and pull/1404/head c117c0160684 by ls-remote at 23:18:28Z (unmoved). After the push: Actions on M' by the pre-existing-failure rule, then M-4 squash under this same GO, then STATUS. Your next handshake is the ctx read after the merge.

RULINGS:
1. The :180 re-expression is ACCEPTED (same inherited defect class as :145; its intent "my run has not moved $BR" is now "$BR == M"; arm driven both ways). Reporting it before the push, rather than pausing, was the right call. Name both gate changes in your handover for R 7th.
2. The M-2 record is ACCEPTED exactly as you wrote it: first run 43 of 45 -> wrong --dev-paths (the two docs passed where only develop's five locks belong) -> corrected property re-verified STANDALONE (docs == kit blobs, 5 locks == develop, a differing negative control). Not rounded, no reset, no re-run.
3. The wrong --base caught by the tool's pre-gate is accepted; note the tool's message prints the CLAIMED base, not the computed merge-base, as a tool defect for your handover.
4. qm 8/8 on M' (run in your vclone after the tool refused the shared checkout: correct) and M-0 (16-object pack, rev-parse --all byte-identical, no ref written) ACCEPTED.

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-07 10:18
