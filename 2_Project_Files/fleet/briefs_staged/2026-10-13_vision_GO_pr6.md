GO to the Vision_Sales_Portal seat (%12): merge QuickQuote PR #6. Gate 17 = GO WITH FINDINGS, CONDITIONAL (D2) on main's first post-merge CodeQL analysis.

The gate's report (Testing Agent MAIN/projects/vision/reports/2026-10-13-vision-gate17-qq-quality-round/report.md, read by Tuesday) re-measured your claims: every suite passes as a set at d030674; the ReDoS input ~20 s at base -> 2.5-18 ms; the 301st request on each limited route gets 429, /healthz is never limited; the quote document is byte-identical to v2.34 except the version (32/32); at 481 px the price is visible with a wide font and nothing else moved (0 box changes in 220 widths). No FAIL fired.

MERGE (merge authority: the open-ended TESTED grant + Kam's C-17 round; this GO is Tuesday's):
1. Re-read main and the head (ls-remote): main must still be 108bbb4 and refs/pull/6/head d030674. If either moved, STOP and mail.
2. Merge PR #6 through GitHub with a merge commit, --match-head-commit d030674694279be3159d67de4a10f220ea6b8335.
3. Read main back (ls-remote, parents).
4. THE CONDITION (D2): wait for main's first CodeQL analysis on the merge commit. Each of #1-#14 must read `fixed`, none `dismissed`, and no new alert number may appear. If ANY of the 14 is still open, or a new alert appears, STOP and mail Tuesday with the alert list; do NOT try a fix on main. Also read tests.yml's five jobs on main.
5. MERGED mail with: the merge sha, the 14 alert states read after the analysis (with its id), the tests.yml run id and result, and confirmation that nothing deployed (the live image is still v0.6.2-tool2.34-108bbb4).

RULED on the gate's points:
- Version: d030674 shares the unreleased v2.35 with 1e1d78d. Accepted (one release, one number). Note it in history.md.
- G17-F1/F2/F3 (test strength: the #6 cell's second input is not pathological; margin-left:auto unpinned; layout cells AUD-only, so add DKK, the widest currency, and a price-right-edge assertion) and G17-P1/P2/P3 (the READY's malformed-email list; the stale sendFailure.js:7 comment; the inert xForwardedForHeader option): ONE entry in QuickQuote's BACKLOG as a test-strength follow-up round, with the gate's fix-shapes. NOT built now.

NO PUBLISH. The live site changes only on Kam's publish card, which Tuesday raises after your MERGED, with the gate's screenshots (evidence/browser/n7/shots/) and yours (v235-evidence/).
-- Tuesday
