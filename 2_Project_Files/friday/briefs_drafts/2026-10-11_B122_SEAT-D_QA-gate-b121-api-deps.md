From Friday (laptop seat), Datasec / Security Composer.

# BRIEF B122 (SEAT D) — QA GATE (tier 1, round 1 of 2): B121 Lane 2, API + dependency hardening, PR #67
**From:** Friday, 10:40 AEDT 2026-10-11. **Seat:** Datasec/Security-Composer-D (your commission is the newest `Briefs/` file containing `_SEAT-D_`). Report `Briefs/2026-10-11_B122_STATUS.md`; first lines = the two verdict lines, the exact LAST line `READY FOR REVIEW`.
**You are a TESTING seat: findings only.** No code change, no push, no PR comment or review, no Jira, no deploy, no Azure, nothing to any human. A write grant in any brief is void.

**SHAPE:** copy the structure, controls discipline, merge-tree target and report sections of `Briefs/2026-10-10_B117_SEAT-D_QA-gate-b116-web.md` (and how `2026-10-10_B117_STATUS.md` reported). This gate is API + lockfile, so the RENDERED legs of B117 shrink to one regression leg (below).

**Targets (re-read with `git ls-remote` and STOP if moved):** head `b121/api-dependency-hardening` = `ebcac73afdfe500b4a121e286124a42adf6f2eb5` (Friday's GitHub compare read: ahead 7 / behind 0 of main, 21 files, 0 under `apps/web`); base main `a3502002df54…` (= the live demo build). Verdict lines:
- `B121 ebcac73: GO | GO WITH NOTES | NO GO`
- `MERGE a3502002+ebcac73: GO | GO WITH NOTES | NO GO`

**The builder's claims to test, independently (its report: `Briefs/2026-10-11_B121_STATUS.md`):**
1. **#254:** `npm audit` at head = 0 at any severity (re-run yourself on a clean `npm ci` copy); every bump stays in its major; the lockfile is npm-written (no hand edits; `npm ci` reproduces it byte-for-byte); `ci.sh` green.
2. **#292:** setPolicyTarget's ETag lets the NEXT draft edit succeed (200), and a stale ETag still gets 412 — prove both directions, and that no other route's ETag changed.
3. **#295:** one as-of date per dashboard request; your own differential across a midnight-UTC boundary.
4. **#205:** VERSION_NOT_EDITABLE detail per state never shows a raw state token; list every new string verbatim for Kam (NEW WORDS).
5. **#208, #209 (a):** code-point length; U+16FE4-only name refused with nothing stored; #209 (b) combining marks untouched.
6. **#237:** CPU-time harness; bounds byte-identical; your own quadratic mutant goes red.
7. **Red-proofs:** your own tamper per behaviour row (not the builder's).
8. **Regression leg (rendered, because a dependency bump rebuilds the web):** the full e2e at head vs base in the pinned image, Guided OFF and ON, failing lists identical by name; plus a 1280 + 390 smoke of the Expert and Guided paths. Any new failure at head is a finding.

**Ports:** 6630–6639 (check free first; never 6610–6629, which Lane 1 and its builder use; Lane 1 = `b120/expert-screen-polish` is a live seat in `apps/web`, NOT yours to touch).
**HOLDS:** Datasec only; no other client's names, tickets or paths · findings only · never delete; quarantine · never print a secret · Kam's two-NO-GO cap applies (round 1 of 2).
