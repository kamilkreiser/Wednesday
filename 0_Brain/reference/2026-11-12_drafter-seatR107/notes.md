# Drafter notes, Seat R 107th brief (2026-11-12 ~14:4x AEDT)

Output: brief_R107.md (116 lines, 40,101 bytes, under 55 KB). One blank STAMP block (near top, four empty bullets for Wednesday), no SELF-CHECK line, no lesson-file names, RULED BY KAM section copied verbatim from R 106th's stamped brief. PROVENANCE: one line for each of the 16 KS keys named (KS-1952, 1466, 2021, 1931, 1923, 2061, 1053, 1081, 966, 2169, 2005, 2170, 1873, 1868, 663, 907), each counted exactly once at the start of a line, plus develop/heads, strict-apply base, R105-F1 controls, gate 329, Wednesday's rulings and R 106th's wrap. Checked by grep: no cd word, no run of five equals signs, no at-sign tokens.

Measured by me this session (read-only, GIT_OPTIONAL_LOCKS=0):
- ls-remote 14:36:59 AEDT: develop b7137aa97c79 (unmoved since R 106th's merge; equals gate 329 pins_start.txt); 2157 2c0692100527 (equals pin); 2203, 2206, 2200, 2201, 2099, 2052, 2075, 2194-2198, 2202, 2204, 2205 equal R 106th's brief; 2207 0d82e65bc5be is new (another lane's).
- Gate 329: commission.md read whole; verdict.md did NOT exist at 14:37 (folder: commission.md, ready_r106_ks1952_mail.txt, scratch/). Not re-checked at the end.
- Trees (rev-parse HEAD, porcelain count 0 each): s-r106-ks1952 2c0692100527, s-r106-mt1952 5a0b018e86f2, s-r106-ctl b7137aa97c79, s-r101-ks1053 16a5c67e676e, s-r105-ks2169 67baaef2f105, s-r105-ks2005 36c0b86b3dd0.
- Push lock: holder file Seat A 27th, pid 93051, 03:30:34Z; one queue entry (1794453660.108150005-93051).
- READY names and sizes by ls -l equal R 106th's brief (11,075; 15,058; 15,070; 11,838). Row 46 (KS-1053) has no READY file by name search (1053 / ks949): the brief says R 107th builds it from the row text.
- history.md guards (case-insensitive, /usr/bin/grep -E): R 107th 0, R 106th 1, R 105th 1. Trap found by me: the default grep here is ugrep and errors on a basic-regex `\(`; the brief says to use /usr/bin/grep -E.
- R 106th's record: HANDOVER FINAL block, wrap mail, ready mail, declared_changes, setup_row0 outputs, merge/fwd-proof outputs, the three Wednesday mails to R 106th all read whole. R 106th mail/: newest inbound 14:10, wrap out 14:35, nothing newer.
- Kit: 58 files at top of REC106/tools, 148 under it by find (incl. orig_r105/ and scratch_boot/ 17 files); R 106th's HANDOVER says 55. Brief tells R 107th to count and say which number it used.
- Re-key hazard (new, measured): a counted r106 -> r107 replacement also shifts R 106th's own tree names (s-r106-ks1952 / mt1952 / ctl) in four scratch_boot one-offs (counts 1, 1, 1, 2) and the shifted ks2005/ks2169 names in row2005_legs / row2169_post (1 each). Brief says protect the trees, do not run the one-offs, name the 2157 tree by absolute path.
- Existing-branch driver copy REC106/tools/launch_driver_r106_existing.py line 44 carries OVL_IGNORE_PRS="2157" and a PR 2157 label; the brief tells R 107th to keep the 2157 value once through the re-key.

Judgement calls and discrepancies for Wednesday:
1. STAMP block left empty (four bullets); R 106th's stamped brief had a filled one, which I did not copy.
2. Strict apply of the held patches was NOT re-measured by me (commission assigns it to R 107th; doing it needs a temp index and I stayed read-only). The brief says plainly it is unmeasured at b7137aa97c79 and cites R 105th's 697f422f1a39 reading as the last one.
3. Row 19's two body statements are restated from R 106th's brief and pointed at R 103rd's brief QUEUE batch 2, which I did not re-read; PROVENANCE says so. Rows 16/12/46/KS-2061 text is from R 106th's brief (copy-and-change).
4. Row 16 start line: the brief says "at a reading of 48 or under taken at the start of the row when no push precedes it" (the commission says "starts only at a reading of 48 or under"); my wording extends the carried "after the preceding push" for the case where no 2157 round precedes. Strike if you disagree.
5. READY carried list kept as in your 14:09 answer: 2194, 2195, 2197, 2198, 2200, 2201, 2203, 2206; whether 2157 joins is left to you at the stamp.
6. The word "cd" does not appear; the carried rule reads "Never change directory with a shell verb". I used the Write tool, not heredocs, for the brief.
7. KS-907 appears only as the launcher's warning tag quoted from R 106th's preflight file; it has a PROVENANCE line because the gate counts any KS key.
8. Brief names KS-1466 and the audit-gate trap (second occurrence, PRs 2159 and 2157); the merge-commit route is stated as needing a NEW grant per push, per the commission.

Not measured: machine load/df, Linear states, GitHub PR open/closed state, census at today's develop, anything in the Spark, vault status.
