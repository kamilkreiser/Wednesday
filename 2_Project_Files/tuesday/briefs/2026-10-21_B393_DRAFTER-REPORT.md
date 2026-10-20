# B393 drafter report (2026-10-21 09:45 AEDT)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-21_B393_SEAT-G20_hpsmpoc-b386-gate-tier1.md` (97 lines, ~41 KB, exactly 3 slots: `@STAMP_HEADS@`, `@STAMP_TIME@`, `@LAUNCH_AUTH@`; the grep count reads 3 now and must read 0 after stamping). `READ-WHOLE-BY-TUESDAY: PENDING`. Pane `Datasec/HPSM-POC-G20`, ports 7520-7529, B-number B393, round 1 of 2.

## Read whole
B389 brief (shape), B386 builder brief (137 lines), B386 STATUS (304 lines), B386 ADDENDUM-1, B377 STATUS (481 lines).

## Measurements (read verbs only; `GH_CONFIG_DIR` = HPSM-POC `.gh-config`; no npm, node, vitest, HTTP to hosted)
All via `gh api repos/datasecau/HPSM-POC/...` GETs at 09:42-09:43:
- Branch head: `branches/b386%2Freviewer-path-fixes-b377 --jq .commit.sha` = `687246aa1b84a02ae2bc3f902781b09245bf0f34` (matches the task; the e2e commit was not yet pushed).
- `compare/main...b386%2Freviewer-path-fixes-b377`: status ahead, ahead_by 6, behind_by 0, total_commits 6, 21 files (list with +/- in the brief's PINS). Commit subjects in order: 701147e, a668c01, 52dc771, f6f3624, e5a5c21, 687246a.
- Main: `git/ref/heads/main` = `54fbceac12393f503fae8c5810af9609bac44548`.
- `commits/687246a.../check-runs --jq .total_count` = 0 (no PR yet, so no CI evidence at that sha).
- Open PRs (`pulls`): #168 (b382), #169 (b381), #170 (b380), #171 (b383). No B386 PR yet.
- `git/matching-refs/heads/b390`: empty (the b390 branch is not on origin at 09:42; B386 saw it only as a remote-tracking ref).
- `code-scanning/alerts?state=open&ref=refs/heads/main` length = 0.
- `contents/web/src/server/auth/returnPath.ts?ref=687246a` and `contents/web/src/proxy.ts?ref=687246a` (lines 85-110) read: the validator is a strict allow-list (`/^[A-Za-z0-9._~/-]+$/`, leading `/`, no `//`, no dot segments, first segment in a 15-entry list, max 300). The proxy builds `new URL("/?"+URLSearchParams({next}), request.url)` only when `safeReturnPath(path)` is non-null.
- `uptime` 09:43: load averages 20.46 14.95 12.49 (heavy; the brief carries the load rule and puts priorities).
- Not measured: `entra.ts`, `page.tsx`, `SignInScreen.tsx`, the old e2e spec lines (all RELAYED from B386 STATUS), and the 1845-at-`e5a5c21` figure.

## Design choices in the brief
- Source of the open-redirect attack surface is wider than the four points in the task: B386 STATUS says `completeSignIn` redirects 303 to `/?next=<path>` (a deviation from its brief) and `SignInScreen.tsx:112` does `router.replace(next)` client-side. So the brief lists proxy, page, `beginSignIn`, `completeSignIn`, `router.replace` and the link `href` (T-b, r3), and asks the gate to judge the deviation.
- Fuzz (T-a/r2): seeded, >= 10,000 inputs, an independent oracle, `new URL(out, origin).origin` and a `URLSearchParams` round trip, one and two decodes, three planted weakeners plus a wrong oracle as controls.
- The gate's own mutants only (never the builder's); builder's files named as CLAIMS-only.
- Cut order and the B377-6-absent check are in the brief (Blocker if `not-found.tsx` or `hosted.test.tsx` appear).
- CodeQL: open alerts fixed in code, never dismissed; the gate reports whether the validator is recognised as a sanitiser.
- Expected-and-not-blamed: the `npm audit` vite advisory red leg (from B389's brief, RELAYED) and the tracked timing flake.

## Questions for Tuesday, with recommended answers
1. The stamp's head will include the e2e commit; should the brief say the gate also runs `hosted-entra.spec.ts` locally? Recommended: no, read-only plus CI evidence (the brief says run only if Playwright and the stand-in run at load < 8, else NOT RUN), because load is 20 and the shared Playwright state is another seat's.
2. Should the `login_hint` claim choice (no Microsoft page may be read) block a GO? Recommended: no, record it as Minor "inert until the tenant claim" and a Tuesday/Kam tenant setting (as the brief says).
3. The brief tells the gate to judge the `/?next=` redirect deviation and the client-side `router.replace`. Recommended: keep; if you prefer the gate not to second-guess a design Tuesday already accepted, delete the "Judge the deviation" sentence in THE CLAIMS.
4. Launch timing: load1 was 20.46 at 09:43. Recommended: launch behind the HOLD at load1 < 7, as for B389, after the PR is open and the e2e commit is pushed (the Stamp needs the final head and the PR number).
5. The B389 brief said the PR would be opened before launch; B386's PR and CI will take time. Recommended: stamp only after the first `check-runs` list is non-empty, so r9 has something to read; else launch with the conditional suffix.
