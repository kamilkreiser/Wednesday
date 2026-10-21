# Spark candidate: KS-1622 (api-gateway platform audit-log: an upstream error status on a LATER paging window is not logged)

Written by the Wednesday morning seat 2026-10-21 (shell date at write). A CANDIDATE, not a brief: nothing was run. Read at origin/develop 32964477fe88 (cache clone, read-only git verbs).

- Product: `Blockchain/Dev/services/api-gateway/src/routes/platform.ts`, inside the paging loop that starts `while (collected.length < overfetch)` (about line 480). The guard line (about 491) reads, byte for byte: `          if (!r.ok && collected.length === 0) logger.warn('GET /api/platform/audit-log upstream answered an error status', { status: r.status, windowsRead });`
- The ticket (Kam's own 2026-10-19 comment on KS-1622) says the natural fix is to drop the `collected.length === 0` half so the warn fires at any window; whether a later error status should also DISCARD the platform half is a separate product decision and is NOT part of this candidate.
- Existing test beside it: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1622-platform-audit-log-logs-an-upstream-error-status.test.ts` (137 lines at the tip; read it for the mocking shape before writing a cell) and `ks1545-platform-audit-log-logs-the-dropped-platform-half.test.ts`.
- Rung: code_patch (one product line edited in place, one new cell or a new test file), model brief = `local-model/night/briefs/ks_1689_p1/KS-1689.md` (the test is given whole, run by hand before the brief is written; golden.diff + spark.pins; `round.sh --dry-run` then `--control`, then queue).
- Cell needed: a SECOND window that answers HTTP 500 with a body still carrying an `entries` array must log one warn (status 500, windowsRead 1) and the caller still gets its rows. RED at the tip (no warn), green after.
- UNMEASURED: whether the existing ks1622 test already has a two-window fixture; whether a live lane touches platform.ts (open PRs not checked); the whole api-gateway suite.
- Not taken tonight because the brief format is heavy (about 25K tokens including the by-hand run) and this seat was at ~74% context; a fresh seat should take it first when it feeds the Spark.
