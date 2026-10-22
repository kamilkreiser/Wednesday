# B496 DRAFTER-REPORT (2026-10-23, drafted 04:55-05:10 AEDT)

Brief: `2026-10-23_B496_SEAT-L4_hpsmpoc-next-advisory-bump.md` (124 lines, seat L4, model row C2, ports 8440-8449). Nothing was built, installed, fetched or run in the project; only reads.

## Stamp slots (line numbers in the brief; `grep -c '____'` reads 8)
- 104 Stamp time
- 105 Stamped by
- 106 Launch authority
- 107 Hard stop and target READY (drafter suggests READY 06:15, stop 07:30)
- 108 Main at launch
- 109 npm advisory state at launch (replaces the Jira-state slot used in B490/B493; there is no ticket)
- 110 Model receipt line and load1
- 124 `READ-WHOLE-BY-TUESDAY: ____`

## What I measured (command -> result)
- `gh api advisories/GHSA-2464-fhr4-w9xw` and `.../GHSA-p3m5-59mp-jv5r` -> critical / high; both `>= 16.0.0, <= 16.4.0`, first patched 16.4.1; published 15:52:53Z and 15:50:34Z. Both also list a 15.x range (patched 15.5.28), which is irrelevant here.
- `git ls-remote origin refs/heads/main 'refs/heads/b4*'` (04:57) -> main `4daa4054...`; no `b496*`; b490 `6708ac6b`, b493 `52b6b26a`.
- `gh api pulls?state=open` -> only #189 (b490). `pulls/184/files` -> exactly `web/package.json`, `web/package-lock.json`.
- `gh api contents?ref=4daa4054` of `web/package.json`, `web/next.config.ts`, `web/package-lock.json` (parsed with Python), `.github/workflows/ci.yml`, `web/scripts/package-standalone.mjs`; git tree listing of `web/`.
- `lsof -nP -iTCP:8440-8449 -sTCP:LISTEN` -> empty rc 1; `tmux list-panes` -> tuesday, K1, J2, G51, fleet-monitor (no L4); `.tools/b496`, `.tools/wt-b496-*` absent; `.tools/b198/lock.sh`, `.tools/b267/waitload.sh`, `.tools/node24/bin` present; load1 6.64 at 04:58.
- `npm view next versions --json` (public npm registry GET, the only non-GitHub network read; I judged it not a "hosted production host") -> 16.4 line = 16.4.0, 16.4.1, 16.4.2 plus canaries.

## Where your facts and the source differ or were extended
- No disagreement with any figure you gave (16.3.8 exact pin, sharp 0.35.5, @img/sharp-linux-x64 0.35.5, standalone output, advisory ranges and patched version).
- Additions you did not state, all now in the brief:
  1. `eslint-config-next` is an exact devDependency `16.3.6` and `@next/eslint-plugin-next` is 16.3.6 in the lockfile, already different from next 16.3.8. The brief says leave both untouched and STOP to ask if npm wants to move them. `@next/env` and the eight `@next/swc-*` entries are next's own dependencies (16.3.8) and are allowed to move with next; the brief defines an allowed closure (keys of the new `node_modules/next` entry's dependencies and optionalDependencies) and STOPs on anything outside it.
  2. The web has NO `public/` folder (package-standalone.mjs says so; the only image-like file is `web/src/app/favicon.ico`). So "an image the app ships" does not exist. The brief has the builder create a scratch PNG (and a scratch SVG for the advisory's SVG surface) inside `.next/standalone/public/` only (git-ignored build output), with negative controls (absent file, bad width, missing quality).
  3. CI has TWO audit steps: `npm audit --omit=dev --audit-level=high` and then `node scripts/audit-dev.mjs` (full audit, dated C-44 braces exception, lapses after 2026-10-31). The brief requires both results recorded, C-44 named and not touched.
  4. `deploy-package.py web --standalone` runs after the build in CI and refuses non-Linux natives; on a Mac build it may refuse. The brief says record it as expected-if-only-for-that-reason, not work around it, and list Linux as NOT TESTED.
  5. next 16.3.8's lockfile entry lists `sharp ^0.35.4` as an optionalDependency, so sharp's resolved version after the bump is recorded and must stay >= 0.35.5.

## Assumptions
- Candidate version 16.4.2 is the newest stable 16.x (from `npm view`); the builder re-reads and picks by measurement, falling back to older stable >= 16.4.1 if the audit rejects it.
- Required env for the standalone server on a Mac is unknown (src/proxy.ts and root layout not read); the brief allows dummy env only and a documented login redirect instead of 200.
- Chosen image URL parameters (w=64, q=75) are in Next's default allowed sizes and quality list; the 400 controls rely on that.
- The 15.x ranges in the advisories were ignored. Jira treated as read-only and optional; no ticket is known, framing left to Tuesday.
- `web/AGENTS.md` and `web/CLAUDE.md` exist and the brief tells the builder to read them; I did not.
- Hard stop 07:30 as instructed; READY target 06:15 is my suggestion in the slot.
- The apiq.sh rule is included verbatim in the FIXED form but marked conditional ("you should need no dotnet"), since this brief runs no Api tests.
- The brief contains the middle-dot character only in the final-line formats, as the sibling briefs do; otherwise ASCII.
- ADDENDUM files from 2026-10-22/23: I read B490 ADDENDUM-1 and -2 whole and skimmed the first ~450 characters of the rest for rules (only the B466 lock rule was relevant and is in standing line 9).
