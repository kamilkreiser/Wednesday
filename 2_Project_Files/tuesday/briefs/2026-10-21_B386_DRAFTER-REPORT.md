Brief: `2026-10-21_B386_SEAT-D17_hpsmpoc-lane6-reviewer-path-fixes.md` (137 lines). Shape copied from B381 (read whole). Inputs read whole: B377 STATUS (481 lines), readiness note sections 3-4, `model-routing.md` v1.0 decision table. Code read through `gh api` at main `54fbceac12393f503fae8c5810af9609bac44548` (`ls-remote` 08:03 confirmed). Drafted 2026-10-21 08:02-08:15 AEDT. No npm, vitest, next, Jira call or HTTP to any hosted host was run.

## Stamp slots
Two, the main sha and the stamp line, both in the Stamp paragraph. Control: `grep -o -E '@[A-Z_]+@'` on the draft prints each slot name once (2 total). The stamped copy must print 0. Tuesday keeps the `.pre-stamp` copy (I wrote none, per the fence).

## Included / excluded
- Included (7 commits, 8 findings): B377-5, -11, -10, -18/-19 (heading structure only), -6, -3, -2. Order easy to hard; the two auth commits (-3, -2) are last so a drop leaves five clean commits.
- Excluded, word pack = 8 findings (-4, -12, -13, -15, -16, -17, -18 text, -19 text), each with the exact current string and file:line, section "WORD PACK FOR TUESDAY".
- Excluded other: -1, -9 (data), -7 (tenant), -8 (by design).
- **-13 is NOT word-free** (a time zone adds text to every time shown). **-14 is excluded**: the three chart hexes map to no token (grep read 0 over `tokens.css` and `brand.css`, control `1d4f91` found).

## Model and gate
Proposed row C3, Opus 5.5 (`claude-opus-5-5`), single seat; gate tier 1 (G1). Why: commits 6-7 are sign-in/sign-out design decisions (what a return path may be, which claim may be a logout hint), and the routing rule is set by the surface. Alternative offered in the brief: split commits 6-7 to a second Opus seat and run 1-5 as C2 Sonnet pilot (disjoint files), or gate 1-5 at tier 2 and 6-7 at tier 1 from the same branch.

## Findings worth your eyes
1. **B377-2 may be inert on hosted.** The only non-token, non-UPN hint is the ID token's `login_hint` optional claim; the local stand-in (`web/e2e/stubs/entra-stub.mjs`, Lane 5's tree, read only) issues none (grep 0), and whether the hosted app registration emits it, or has `post_logout_redirect_uri` registered, is UNMEASURED. The brief forbids a `preferred_username` fallback by default. A real end-to-end proof needs a hosted re-walk after deploy.
2. **B377-6 hazard list**: status must stay 404 (proxy comment says a layout `notFound()` can only send 200); `PrototypeBanner` already carries the demo notice, so the page's own `DemoNoticeBanner` must go (C-27 b); on the laptop a signed-out visitor is now bounced to `/` by `AppShell`.
3. **B377-5**: `motion-reduce:transition-none` would NOT fix B377's probe (it leaves computed duration 0.15 s); the brief specifies `motion-reduce:duration-0`.
4. **B377-11** moves the note from full width above the tabs into `<main>` (a visible layout shift, no word change).
5. B380 explicitly leaves `web/src/server/auth/*` and `entra.ts` `bearerFor` (HPSMPOC-228 N-5) unowned; the brief takes only the Tx/Session/begin/complete/signOut hunks and forbids `bearerFor`.
6. Expected CodeQL class on commit 6: unvalidated URL redirection; the four-check validator is the answer.

## Questions for Tuesday (recommended answer)
1. Single Opus seat (C3) or split auth to a second seat? [single, auth last]
2. B377-2 hint source: `login_hint` claim only, no email fallback? [yes; Kam or the tenant admin enables the claim]
3. Accept the B377-11 layout shift? [yes]
4. B377-10 loading state: blank panel body (no words) rather than reusing "Loading the customer…"? [blank]
5. Accept the laptop behaviour change on the 404 page (commit 5)? [yes]
6. Let the builder create up to eight Jira tickets (one per finding, search first)? [yes; else comments only]
7. Who re-walks hosted -2/-3/-6 after deploy (a B377-style seat; the builder cannot)? [Tuesday schedules it before the freeze]

## Not read (UNMEASURED)
Jira (no existing ticket search), the web test baseline, `web/src/lib` date formatter, `playbook-placeholder.v0.5.0.json:11`, the source of "DATASEC IMPLEMENTATION PATH", weekly gauge, live panes, load.
