# QA GATE — TIER 1 — Datasec/NexusAI, RD-369 round 3

**Head under test:** `rd-369-round3-s49` @ `7cd0907724d1313b4f64950f5f8600dde3acb448`, based on `cd2b543`.
**Repo:** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files`
**Diff:** 3 files, +210/−37 — `__tests__/helpers/image-manifest.js`, `__tests__/image-content-exposure.test.js`, `scripts/verify-expected-counts.json`.

## WHY TIER 1, stated here so this brief and the launcher cannot drift apart

**Every file in this change is a test or a config, which on Kam's 2026-09-05 tiering reads "through-code only." That classification is wrong here and I am overriding it deliberately.** The tier is set by what the change *is*, not by where it lives: **this IS the security control.** It is the guard that decides whether internal tenant correspondence, subscription GUIDs and a named staging-user roster are detected inside the customer container image. If the guard is wrong, the exposure ships and nothing reports it.

Classifying it "tests" because the files sit under `__tests__/` would be using a convenient classification to reduce scrutiny — the exact failure `learnings/2026-08-16_classification-is-the-field-that-grants-authority` names.

## WHAT KAM AUTHORISED, AND THE TWO EDGES

*"Authorise ONE round 3, narrow — the window and the certifying cell only. Remove the window from BOTH paths and make the certifying cell able to fail."*

- **In scope: DETECTION.** The window on both paths; the certifying cell's ability to fail.
- 🔴 **OUT OF SCOPE: removing the RD-385 files from the image.** Kam was offered that option (`wider`) and **declined it.** No file is removed. If the builder removed one, that is a finding.
- 🔴 **THE CAP IS REAL: no round 4 without Kam.** A NO GO here does not open another round — the closed instances ship and the residue is ticketed. **So grade findings by whether they must block, not by whether they could be fixed.**

## THE BUILDER'S OWN CLAIMS — verify each, do not relay any

1. The round-2 docblock said *"there is no window"*. Builder says that was **true of the roster path and false of the labelled path three lines below**, which carried a 24-character single-line gap between the noun and `id`, plus a per-line scan.
2. A **purely cosmetic reflow** (break the line after a trailing `ID:`, every value preserved) flipped **three** detected carriers to CLEAN at round 2: `TEST_SETUP_README.md`, `docs/SECURITY_AUDIT_AND_RECOMMENDATIONS.md`, `docs/SYSADMIN-LAW-TENANT-ACCESS-REQUEST.md`. Builder says the set is now identical before and after that reflow **and after a 3-line scatter**.
3. **The old certifying cell was vacuous:** `expect(found.length).toBeGreaterThan(0)` over two paths stays green when one path dies. Now pinned **per path: 13 by label, 5 by roster, 16 union.**
4. **Mutation matrix, green baseline either side of each:** baseline 27 passed · `byLabel := false` → 5 FAILED/22 · restore 27 · `byRoster := false` → 4 FAILED/23 · restore 27 · round-2 window reintroduced → 4 FAILED including the reflow cell.
5. **Image-level:** tracked 685 · derived-to-ship 284 · present-in-image 288 · **0 false positives, 0 false negatives**; the 288−284 is `docs/test-files/` copied to a second path by `Dockerfile:67`. All 16 carriers confirmed **from files extracted from the image**, per-path verdicts identical to the derivation.
6. **Suite: 2282/2282 across 117 suites, jest exit 0.** Count expectation moved 2278 → 2282 (+4 net: one cell removed, five added) and `scripts/verify-expected-counts.json` is committed in the same change.

## 🔴 WHAT TO ATTACK FIRST — the builder named its own weak point and invited this

**The carrier set widens 9 → 16 and the builder did not tune it back.** It says every added file does present a GUID as an identifier, but **two present WELL-KNOWN PUBLIC Azure GUIDs**: `docs/AUDIT-DEFERRED-ITEMS-PLAN.md` (a built-in role definition) and `backend/marketplaceJwt.js` (a Marketplace audience). It left them **detected on purpose**, arguing that suppressing them needs an allowlist of "safe" GUIDs and *"an allowlist is instrument-narrowing in a different coat — the exact move this ticket exists to stop."*

**Is that call right?** It is a real disagreement if you think otherwise, and the builder explicitly asked to have it before a merge rather than after. **Consider both failure directions:** a guard that cries wolf on public constants gets discounted wholesale (`learnings/2026-08-16_an-overstated-record-gets-discounted-wholesale`), and an allowlist is the narrowing this whole ticket exists to prevent.

**The strongest control the builder offers, and the one to re-run rather than believe:** the real shipped `scripts/seed/demo-printer-logs.csv` — **over a thousand unlabelled GUIDs, genuinely in the image** — is asserted **NOT** a carrier. That is the file the widening had to survive. **If that assertion is weak, the widening is unbounded.**

## HOW TO DRIVE IT — and the honest limit

**There is no rendered surface in this change.** No route, no page, no product behaviour moves. **Do not manufacture screenshots and do not report their absence as a gap** — the builder was right not to fake them. This gate is **through-code plus re-running the evidence**, and the evidence is built to be re-run:

    git fetch origin && git checkout 7cd0907724d1313b4f64950f5f8600dde3acb448
    npm ci && npm run verify          # read the VERDICT line, not the exit code
    docker build --target production -t <yourtag> .

**Docker IS up on this machine (29.7.2), measured.** Work in your own clone or worktree — **`2_Project_Files/` in that repo is a known stale snapshot** (33 tracked files off `cd2b543`, `+248/−1230`, mechanism unexplained, card open). **Do not touch it, do not "fix" it, read verbs only if you go near it.**

## WHAT WOULD MAKE THIS A NO GO

- The reflow/scatter invariance does not reproduce, or reproduces only on the cases the builder chose.
- A mutation that kills a detection path leaves the suite GREEN (the vacuity is not actually closed).
- The image-level 0/0 does not reproduce, or the 288−284 gap has a second unexplained member.
- `demo-printer-logs.csv` is asserted not-a-carrier by something that would also miss a real carrier.
- Any RD-385 file was removed from the image (out of scope, Kam declined it).

## CONTROLS THIS GATE OWES ITSELF

**Every zero gets a control that would have produced a non-zero, run in the same action.** A green from a check that could not fail is worse than no check. If an instrument cannot reach the case it names, **say so and mark that cell NOT TESTED** rather than reporting a pass.

## YOU ARE FINDINGS-ONLY

**Never fix.** Report. Grade Blocker / Major / Minor. **Qualify your own greens** — a qualified green is worth more than a confident one.

## 🔴 MAIL YOUR VERDICT

**Send it to `tuesday-agent@agentmail.to`**, subject `[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-369 round 3 @ 7cd0907 (tier 1)`.
**NOT `wednesday-agent@`.** Datasec's coordinator is **Tuesday**; Wednesday is the Secuura seat and Datasec mail in her inbox is a cross-client leak.
**Your pane has ~19 lines and no scrollback and you have no inbox — an unmailed verdict is lost at the pane close.**
