# Spark operator 27 - report (2026-10-30, base develop 85cd24d81cb9, clone .../2026-10-30_spark-operator27/clone)

## BLUF
Rung 4 (loose brief + dictated hunk headers + per-hunk skeleton wording) did NOT break between 6 and 9 hunks: 7, 8 and 9 hunks all PASS 7/7 on the ORIGINAL brief (no rebrief used, counters unspent). The earlier 9-hunk failure (ks_1410_p5, twice, A2) was therefore the brief wording, not the count: ks_1410_p5 and ks_1410_p5_rebrief contain NO per-hunk skeleton (grep -i count 0; positive controls p5a and cal9 = 1). This corrects operator 26, who wrote that p5 already carries per-hunk skeletons. I added a 9-hunk run (not asked) because it closed the bracket. Task 2: nothing briefable. Held: 0 (calibration only, as instructed). Drainer 97411 alive, I started none; Spark idle again after cal9.

## Rounds (all hand-run round.sh, 3 Spark rounds; lint 0, dry OK, control PASS byte-identical beforehand for each)
| brief | hunks | result | round | model | tokens | golden |
|---|---|---|---|---|---|---|
| night/briefs/ks_1410_cal7_mcp_http_500_no_echo | 7 (p5a's 5 + /workflow/:id, /connector) | PASS 7/7 | 93 s | 58.8 s | 16404+2504 | BYTE-IDENTICAL |
| night/briefs/ks_1410_cal8_mcp_http_500_no_echo | 8 (+ /policy) | PASS 7/7 | 178 s | 59.8 s | 16866+2511 | TREE-IDENTICAL |
| night/briefs/ks_1410_cal9_mcp_http_500_no_echo | 9 (+ /generate-package, the `if (!res.headersSent)` site) | PASS 7/7 | 109 s | 64.2 s | 17416+2766 | BYTE-IDENTICAL |
Failure cause per hunk-count: none failed. Output speed ~43 tok/s end to end; 2.5-2.8 K output tokens even at 9 hunks (limit not approached).
Base check: origin develop 85cd24d81cb9 (ls-remote; one transient github:22 timeout on the first ls-remote, repeat returned the same sha). `git diff --stat 40c0608..85cd24d -- services/mcp-server` is empty and the ten `.status(500).json(` lines are still at :62 :77 :111 :135 :170 :183 :193 :203 :213 :267, so p5a/p5b's lines are unchanged. Briefs generated with GEN_BRIEFS explicit -> 2_Project_Files/local-model/night/briefs/ (not 0_Brain/night/).
Caveat: this is one sample per hunk count (n=1 each, original brief), same file, same shape of hunk. It shows the 9-hunk shape is solvable with the skeleton wording; it does not show the model is reliable (cal7-9 each passed once). Heterogeneous hunks (different shapes per hunk) were not tested.

## Task 2 (KS board, read-only, key transient, paginated)
KS-1840..KS-1856 (17 tickets, filed since 2026-10-29T16:02Z). Excluded per the list: 1845/1850/1851, 1848/1849, 1847/1842/1853 (docs/spec), 1852, 1844, 1840 (anchoring service). Remaining, none briefable: KS-1841 (api-gateway Dockerfile glob: F1 fix is an allow-list vs .dockerignore design choice, Dockerfile not a Spark tier), KS-1843 (nft-certificate trim asymmetry: behaviour/design choice, Low), KS-1854 (reset limiter mount + billing route order: ticket says "Kam decides which side moves"), KS-1855 (gateway stand-ins: removal/guard decision), KS-1856 (analytics exports authz: security behaviour, no spelled-out fix). Nothing queued, no O27-P<n> notes. Screen output: ks_screen.json (titles/descriptions; no key).

## Held notes
None. Calibration only; cal7/8/9 patches deliberately NOT held (overlap held p5a/p5b).

## Faults
1. Hooks: a `cd`, and a `$VAR` in `git -C $VAR <write verb>`, refuse the call; `timeout` does not exist on this Mac. Re-issued with literal paths.
2. A hand-run round.sh does not append to done.md; I appended the 3 rows manually (also IMPROVEMENTS.md: 2 rows; backup IMPROVEMENTS.md.pre-1030-op27).
3. Operator 26's premise about p5 was wrong (above); reading the brief files, not the report, is what exposed it.
4. mk22.py's SRC default points at a dead scratchpad path; GEN_SRC=<clone> was set (reads the checked-out tree, which is the tip).

## Next
1. Re-brief the original ks_1410_p5 (9 hunks) is unnecessary: cal9 IS the 9-hunk single brief and its golden equals the union of p5a+p5b. If Wednesday prefers one raise over two, cal9's patch could replace the held p5a+p5b pair (same golden content; verify the diff and the POST /verify response-shape note) - her decision, I held nothing.
2. To find where rung 4 does break: heterogeneous hunks (different shapes per hunk), multi-file, or a count above 9 in a file with more sites; http-server.ts has no more sites.
3. Fix the grep case discipline: positive-control count when comparing briefs.
4. Prune: clone (dir above, ~small), run dirs spark_secuura_2026-10-30_ks_1410_cal{7,8,9}_...{,-control}.

## Left behind
tools/ (copies of op23 generator + spec_n.py, CAL_N=7|8|9), prep.sh, linear_screen.py, ks_screen.json, lint/dry/control/lsremote logs and round_cal{7,8,9}.log, lsremote_cal7_FIRST_TIMEOUT.txt.
