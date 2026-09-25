#1214 KS-528 DOMPATCH: react-router-dom 6.30.6 in four locks, GHSA-jjmj row removed
head 6fce4d0b188655a520e97447d3bfb1749d22a435

## BLUF

The baseline row says of these advisories that the remedy lands in v7 only, a semver-MAJOR v6->v7 migration. For **this** row that is stale: `GHSA-jjmj-jmhj-qwj2` patches `react-router-dom` at **6.30.6** (affected `>= 6.30.2, <= 6.30.5`), a patch move inside v6. Read from the GitHub advisory API, read-only, 2026-09-25.

So the pin moves 6.30.4 -> **6.30.6** in the three portal locks and the workspace root, with the shared `remix-run/router` 1.23.3 -> **1.23.4**. **No manifest change** — the declared range is already `^6.30.4`.

**And the baseline row comes out, on the repo's own verdict rather than a judgement.** With the four locks updated and the row still present, `audit-gate` printed:

```
CLEANUP (advisory): 1 baseline entry is no longer reported - remove:
  - GHSA-jjmj-jmhj-qwj2 (react-router-dom, KS-528)
```

Only then was the row deleted — **0 insertions / 7 deletions**, that one member.

*(npm scope sigils are omitted so the symbols stay searchable.)*

## This ticket still has work, which is why this is Refs only

The **other two** `react-router` rows are untouched and still needed. `GHSA-wrjc-x8rr-h8h6` (`react-router >= 6.0.0, < 7.18.0`) and `GHSA-337j-9hxr-rhxg` (`react-router >= 6.4.0, < 7.18.0`) are both **patched only at 7.18.0**, which no v6 release reaches. They expire **2026-10-02**, five days after the row this PR removes. The v7 migration this ticket is named for is unaffected by this change.

## Test Evidence

**Touched**
- `Blockchain/Dev/frontend/admin/package-lock.json` (+12/-12)
- `Blockchain/Dev/frontend/issuer/package-lock.json` (+12/-12)
- `Blockchain/Dev/frontend/verifier/package-lock.json` (+12/-12)
- `Blockchain/Dev/package-lock.json` (+12/-6)
- `Blockchain/Dev/scripts/audit/audit-baseline.json` (+0/-7)

No source file, no test file, no spec, no migration, no `package.json`.

**Scope, per lock: added 0 / removed 0 / version-changed 3** — the two router packages plus their shared `remix-run/router`. Platform discriminators unchanged everywhere: issuer `libc 13->13`, root `os 112->112, cpu 110->110, devOptional 84->84`, admin and verifier `os 26->26, cpu 26->26`.

**Ran, by me, at this PR's head `6fce4d0b188655a520e97447d3bfb1749d22a435`**
- `audit-gate` bare: **rc 0, 25 distinct advisories reported, 25 baselined, no CLEANUP line** — so the row and the advisory went away together, which is the removal's whole justification.
- `audit-gate` with the clock frozen at 2026-09-30T00:00Z: `GHSA-jjmj-jmhj-qwj2` is **absent from the lapse list**; the two rows that remain belong to other PRs. `audit-locks` frozen: advisory matches **24 -> 23**.
- **`npm run audit:contract` — the validator both gates import — 59 pass, 0 fail, rc 0.** The edited baseline still satisfies every field rule.
- The two rows expiring 2026-10-02 verified **still present by name** after the edit.
- **The in-hook push preflight, 12 of 15 legs:** leg 2 lockfile clean-room — **all 35 standalone locks pass `npm ci --dry-run`**, with all three frontend locks in the covered list; leg 5 audit-contract **59 cases pass**; leg 6 npm-audit gate **25 reported / 25 baselined, OK**; leg 7 standalone-lock advisories **23 match, 23 baselined, OK**; legs 1, 9, 10, 11, 12, 13, 14, 15 all OK. **Zero FAIL-shaped lines in the run.**
- Each spliced lock proved self-consistent: an isolated resolution pass over it moves 0 versions.

**NOT run — say it plainly**
- The preflight's own verdict is **`PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.`**, and it prints `This is NOT a pass. Do not quote it as one — say which legs ran.` The three are **leg 3** (spec-auth conformance), **leg 4** (path resolvability) and **leg 8** (served-spec consistency), each `SKIP — local stack not up on http://localhost:6882`.
- **No frontend was built and no browser was driven.** This is the important gap: `react-router-dom` is client-runtime code in all three portals, and nothing here proves the portals still route correctly on 6.30.6. A vite build plus a real-browser pass on the issuer, admin and verifier is the check this PR does not carry.
- The three portals' unit suites were not run — no source or test file changed, so there is nothing new for them to cover, but that is a reason rather than a result.
- The four platform suites (Schemathesis, Akto, Playwright, k6) were not run: no service source, spec or route changed.
- The advisory's own vulnerability — an open redirect leading to XSS — was not reproduced before or after. The evidence is the published affected range and the pin, not a proof of exploitability.

**Migrations + config**
None. No `.sql`, no env template, no compose file. One baseline row removed from `Blockchain/Dev/scripts/audit/audit-baseline.json`.

## What this does NOT clear

- The two `react-router` rows expiring **2026-10-02** — they need react-router **7.18.0**, i.e. this ticket's v7 migration.
- Nothing about the other two rows expiring 2026-09-30; each has its own change.

## Merge exposure

Merging this makes dependabot **#572, #575, #635, #639, #649, #945, #946, #947, #948** and **#949** dirty — all ten touch `Blockchain/Dev/package-lock.json`.

Refs KS-528

🤖 Generated with [Claude Code](https://claude.com/claude-code)

