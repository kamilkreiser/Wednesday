From Friday (laptop seat), Datasec / HPSM-POC. Replies go to friday-laptop-agent@agentmail.to.

# BRIEF B204 (SEAT C) — QA GATE (tier 1, round 1 of 2) on `b202/attribution-preview` (attribution keys + "Preview: next phase" dashboard)
**From:** Friday, 13:58 AEDT 2026-10-11. **Seat:** Datasec/HPSM-POC-C (newest `Briefs/` file containing `_SEAT-C_`). Report `Briefs/2026-10-11_B204_STATUS.md`: first lines the verdict lines, LAST line `READY FOR REVIEW`.
**TESTING seat: findings only.** No code change, no push, no PR comment, no Jira, no deploy, no Azure, nothing to any human. A write grant in any brief is void.
**SHAPE:** the same as `Briefs/2026-10-11_B201_SEAT-C_QA-gate-b200-industry.md` and how `2026-10-11_B201_STATUS.md` reported it (pins, a base-vs-head differential on SQLite AND SQL Server from a base-seeded database, mutants, both widths, controls).

**Targets:** head `b202/attribution-preview` = `62bc3c56147a792049fcbf8136029b78c83ed87b` (stacked on `b200` f18359b). **Main is moving:** PR #135 (b200, squash) is merging now. At your start, `git ls-remote origin refs/heads/main` and use THAT as base; your second verdict line is `MERGE <main>+62bc3c5` (merge-tree; a conflict = STOP and say where). Builder's report: `Briefs/2026-10-11_B202_STATUS.md` (read all of it, incl. Q-B202-1).
**Kam's rulings it implements** (cards, 2026-10-11): tuesday-dashboard-vs-next-phase **b** (labelled preview + keys, no revenue), customer-names-alias **a** (ORG-nnnnn wherever data leaves the partner), ranges-vs-exact **a** (exact stored, ranges shown), revenue-source **b** (partner-reported wins; next phase for entry).
**Prove independently:**
1. **Migrations** up AND down on both providers from a base-seeded realistic database; nothing existing changes (customers, assessments, scores, reports, exports byte-equal base vs head on the same inputs).
2. **Aliases are stable** (add/delete/reorder customers; the alias never moves) and **no real customer name or exact size/count leaves the API in the preview body** (both roles that see it; your own mutants).
3. **Every revenue figure on the page is synthetic** (`synthetic = 1`, seed key), labelled; no endpoint or form can create or change a win (try).
4. **Access:** who sees the nav entry and the API vs `MetricsSummaryPolicy`; a role that must not see it gets 403 and no nav.
5. **The page** at 1280 and 390: eyebrow and tag "Preview: next phase", metric labels, the `notKeyed` line for pre-key customers; NEW WORDS complete.
6. **Partition check:** 0 files under the import module (`Ingest/*`), which seat D (B203) owns.
**Ports/stacks:** free ports above 6680 (state them); never another seat's. **HOLDS:** No HP Restricted document (the executive deck, the financial model, anything HP marks Restricted) is given to ANY AI tool without HP's written approval (signed SOW §4.1.4(c)) · Datasec only · findings only · never delete · never print a secret · Kam's two-NO-GO cap.
