KS-1147 ks860 loopback guard boundary (R-5, #980 delta gate): a listen call carried as a string fixture in a `"`-literal with an escaped host `\"127.0.0.1\"` is reported as host-less — the mask copies the backslash, `:440` wants a bare quote
state In Progress

## BLUF

A class boundary of the ks860 loopback guard (`Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts`, widened to `packages/` by #976 / KS-876), measured by the tier-2 delta gate on PR #980 (KS-924 + KS-901) at `103c235b4` and recorded as R-5 — not a finding against #980, which ships `app.listen(0, '127.0.0.1')` (single-quoted host, the guard's own `:517` accepted spelling) and reads GREEN: `packages/shared` 813/813 on the merged tree, ks860 23/23. Nothing on develop trips it today; it is the guard's, and #976's gate owns the guard's design. One file, one test pass; the fix shape below is the gate's PROPOSAL, not ratified.

Report: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-13-ks924-901-980-103c235b4-tier2-r2/report.md` — §3 the Tg-B row, §4 the tamper table, §6 Records R-5. Line numbers at M17 `a4ef481c8` (the guard's blob `e0dfadb9c`, unchanged since M15).

## The boundary (MEASURED by the gate, Tg-B)

* A test file that carries a listen call as a string fixture inside a `"`-delimited literal can only spell a double-quoted host as `\"127.0.0.1\"`. Written to disk that body is `app.listen(0, "127.0.0.1");` — exactly the guard's own `:516` accepted spelling (`expect(offendingListenSites('const s = app.listen(0, "127.0.0.1", resolve);')).toEqual([])`). Yet with #980's `:235` rewritten that way the guard's 🔴 cell reads RED naming `:235` (two-file run 51/52), the offender printed with its backslashes.
* Cause: `maskCommentsWithState` preserves string contents by design (docblock `:104-109` — a `//` inside `'http://x'` is data) and copies the backslash into the masked text; the site regex `:433` `/\.listen\(\s*0\s*(,|\))/g` matches, then the host check `:440` `/^\s*(['"])127\.0\.0\.1\1/` requires a bare `'` or `"` as the first non-space character after the comma — a `\` is neither, so the site is reported host-less.
* Blast radius: any test file carrying a listen call as a STRING FIXTURE in a `"`-literal with a double-quoted host. None exists on develop today (the merged tree is green); the natural escape is the single-quoted host, which #980 uses. Sibling boundary noted by the same gate (Tg-D): `listen(3000)` with no host passes `\s*0\s*` — the regex's declared narrowness (port 0 only), recorded, not a defect claim.

## Fix shape (the gate's PROPOSAL)

Let the host check accept an escaped quote: e.g. `/^\s*\\?(['"])127\.0\.0\.1\\?\1/` at `:440`, and add a control cell beside `:516-517` feeding a `"`-literal fixture whose host is `\"127.0.0.1\"` (as a string, i.e. the file's own text carries the backslash-quote), expecting `[]`. Regression instrument: Tg-B on the widened guard → the 🔴 cell GREEN; the T-860 tamper (host removed) must still RED.

## Dedupe (searched before filing)

By symbol over the KS board, title + description, includeArchived (s211 ITEM 0 for L): `offendingListenSites` 5 (KS-895, KS-894, KS-891, KS-874, KS-873 — all archived; the mask-desync / announcement-row classes, none the escaped-host boundary) · `SELF_EXCLUDED` 0 · `maskCommentsWithState` 1 (KS-891, archived — the re-synchronising desync) · `mask preserves` 0 · `ks860` 7 (KS-876/875/879/891/893/894/895, all archived; none this boundary) · `listen(` 11 (KS-860 the parent — 55 listeners binding all interfaces; KS-845 the nine bare sites; the rest other subjects). No home; filed new. KS-873 / KS-874 / KS-891 are the guard's mask-class neighbours (archived; named, not related).
