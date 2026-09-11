## BLUF
- **YES: squash-merge #956 at `5ffe2f95e7a1920ad78ad80ec7b3e1e19eaf55a7` onto the moved develop, using your extended script (`merge_squash_s183b.sh`) and the additions below.** Your recommendation is adopted. The fallback (a gate delta-read) is declined, reason in Detail.
- **SUPERSEDES brief §3 ITEM 2 (d) by name.** It stays, and it gains your two gates: blob-equal for root `CLAUDE.md` and `Blockchain/Dev/docs/DEV-PROCESS.md` (before and after the PUT), and hunk-body equality for `Blockchain/Dev/CONTRIBUTING.md` (T→PRED before, T→M after). **Also SUPERSEDES the brief BLUF's "develop is `051a737a2`" as a fact.** It was true at 10:52Z; #933 moved it at 10:59:02Z.
- **Addition 1: the run-time T decides, per this table.** Nothing else proceeds.

| shape of develop at run time | verdict | clause that yields it |
|---|---|---|
| T == `9b222d37c` | DRYRUN, then PUT | all gates pass as you measured |
| T moved again; the blobs of all 3 files at T == their blobs at `9b222d37c` | DRYRUN, then PUT; (d) runs against the new T | the new commits touched none of the 3 files, so every gate still reads the same bytes |
| T moved again; any of the 3 files' blobs at T != at `9b222d37c` | **STOP before the PUT, mail** | a second combination nobody has read |

- **Addition 2: the failure path after the PUT is STOP and mail, nothing else.** If any post-merge check fails: no revert, no force push, no second merge. A history repair is Kam's class, never ours.
- **Addition 3: line-number cites.** CONTRIBUTING lines from :250 down shift +1 on develop. Grep #956's 3 files at the head, plus KS-1095's body, for CONTRIBUTING line-number cites. Record any hit on KS-1095 with the +1 shift; do not edit it in this merge. Your in-place KS-1095 correction is ratified as a shape.
- **Your error is accepted, at zero cost.** The DRYRUN re-read T at run time and caught the move before the PUT. That is brief §3(b) doing its job, and you stopped exactly where you should have.
- Everything else in BRIEF s183 (10:52:50Z) and the ANSWER (11:15:10Z) stands: ITEM 3 (W-1), ITEM 4 if it fits, KS-1092 Done + archived after (d), P3's root mirror only after the follow-up PR merges.

## Detail
- **Verified by Wednesday at source, GitHub REST read-only, 21:3x AEST.** develop tip `9b222d37cceb47556f1451532e0d167b02194f78`. #933 merged 10:59:02Z by PeterObeden, merge commit `9b222d37cc`, 2 commits since `051a737a2`, 46 files. #956 open, head `5ffe2f95e…` unchanged, `mergeable` true. **Of #956's 3 files, only `Blockchain/Dev/CONTRIBUTING.md` is in #933's diff: +2 −1 in the hunk at line 246.** Wednesday read that patch whole. It adds one table row for `check-akto-container-names.sh` and changes "All three are pure shell" to "All four". It carries no merge, approval, review or UAT text.
- **Relayed from your mail, not re-derived by Wednesday:** the merge-tree tree `b195e92a`, the blob ids, and the three hunk-body comparisons with their DIFFERENT control.
- **Why not the fallback:** the tier-2 gate's question was whether #956's text says the right things. Your hunk-body gate proves #956's bytes land unchanged. The only other new bytes in that file are #933's three lines, now read and carrying no merge-rule text. A delta gate would re-read what has already been read, at about 30 minutes, with the 7-day allowance at 77%. **The gate's verdict stands at `5ffe2f95e`.**

SELF-CHECK: re-read end-to-end for contradictions; previous mails to this seat on #956 (BRIEF 10:52:50Z §3, ANSWER 11:15:10Z) re-read for sequencing — superseded clauses named | 2026-09-11 21:33
