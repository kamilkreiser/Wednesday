# B571 DRAFTER REPORT (2026-10-24, Sonnet drafter, read-only)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-24_B571_SEAT-H10_hpsmpoc-zod-audit-and-braces-exception.md` (84 lines, long ones). Unstamped copy `.pre-stamp` reads **9** lines with `/usr/bin/grep -c -E '_''_''_''_'` (8 slot lines at 73-80 + the last line 84), matching the Stamp text. Template: B564 brief (stamped and .pre-stamp), shape cloned.

## Read
- CI log lines 184-200 of job 120690275703 (gh api GET, ANSI stripped): FAIL zod GHSA-mrhx-c7xc-m3w5 (high) <4.6.6, NOTE braces GHSA-vfj7 no longer reported, counts total 1, "dev-tooling audit FAILED". Quoted in the brief.
- At main 08af828b (gh api raw): `web/scripts/audit-dev.mjs` (whole), `web/package.json` (whole), `ci.yml` (grep + 385-395), `package-lock.json` (zod, braces, eslint-plugin-react-hooks blocks), `web/src/audit-dev.test.ts` (grep).
- main = 08af828b (ls-remote 09:38), `b571*` absent; ports 9200-9209: lsof empty; word-boundary grep of 23/24 Oct briefs for 920x = 0 matches (file-level `grep -l`, rc 1; no positive control run for this scan).

## Findings that change the commission (check first)
1. **ci.yml does NOT hold the braces exception.** It holds only comment lines 389-392 and the step name at 393 ("one dated exception, C-44"); `run:` is `node scripts/audit-dev.mjs`. The exception data is `EXCEPTIONS` in audit-dev.mjs:14-16. The brief limits the ci.yml edit to those comment lines plus the `name:`.
2. **A fifth path is needed.** `web/src/audit-dev.test.ts` asserts exactly one braces exception (lines 35-37, 40-44, 110 and more), so removing the entry turns it red. I added it as PROPOSED in YOURS, with a rewrite design (inject a synthetic exception via `evaluate`'s third parameter). Tuesday strikes or accepts at the stamp; striking it means the exception cannot be removed in this round (zod alone fixes CI; the braces NOTE is a note, not a failure).
3. **zod is transitive, dev-only, no overrides anywhere.** `eslint-plugin-react-hooks` 7.1.1 depends on `zod ^3.25.0 || ^4.0.0`; lock has 4.6.5. Expected fix is lock-only; package.json should stay untouched. I told the seat to STOP-ask before adding the project's first `overrides` entry.
4. braces is still 3.0.3 in the lock; why npm stopped reporting GHSA-vfj7 is UNMEASURED (seat prints it).
5. C-44/C-99 text: grep of `1_Project_Definition/CLARIFICATIONS.md` printed nothing; quoted only from the audit-dev.mjs header. Marked UNMEASURED; seat to find it.
6. Branch name fixed `b571/hpsmpoc-zod-audit-braces` (no ticket key); TICKET-KEY slot allows "none, branch fixed".
7. Workflow edit: comment and step-name only, no `run:`/job name; a WORDS-free BLUF line is in the brief's FOR TUESDAY. Whether it needs the product owner is Tuesday's call.

## UNMEASURED
No npm/audit/vitest; registry has zod >= 4.6.6 in range (assumed); whether other packages move with the bump; extra braces-dependent rows in audit-dev.test.ts beyond grep; ci.yml working-directory/node setup beyond lines 385-395; the brief runs ~4 lines over the ~80 target.
