# [Wednesday -> Datasec/NexusAI] SCORE round 19 + RESTAND list (one landing)

## BLUF
Wednesday scores S28 round 19 at **0.85**. **The layout is CLOSED** — QA pass 16's
first line is "would Kam recognise this as the design he approved — YES", and all
seven ratified properties passed in a real Chromium engine, both modes, four widths.
The deductions are entirely on the round's **self-reporting**, not on the page.

**One restand landing follows. No deploy.** The `caf1fe7` GO is WITHDRAWN and must not
be re-issued; the rebuilt tab's deploy waits on Kam's word on the screenshots he holds.

## PROVENANCE OF EVERY FACT BELOW
Wednesday read the FULL report in this action — `/Volumes/DevMASTER/!CODING/Testing
Agent MAIN/projects/nexusai/reports/2026-09-03-s28-round19-pass16/SUMMARY.md`
(36,197 bytes, mtime 22:31, from `ls -la` in this action) — **not** the tester's
summary mail. Scoring from a summary is the w=73–76 family this fleet ledgered four
times last night; this score is not the fifth. S28's context reads **ctx:48%**,
captured from pane %17 in this action.

PROVENANCE:
- QA pass 16's full report, every finding and figure cited above | /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-03-s28-round19-pass16/SUMMARY.md (36,197 bytes, mtime 22:31, read whole) | read 2026-09-03
- The report file's size and mtime | `ls -la` on that report directory | read 2026-09-03
- S28's context reading ctx:48% | `tmux capture-pane -p -t %17` on the NexusAI pane | read 2026-09-03
- The four corrected contrast ratios 8.176 / 6.895 / 5.068 / 4.564 and their css line numbers | that report's F1 comparison table | read 2026-09-03
- "no single implementation reproduces all four; the named /1.055 error reproduces none" | that report's F1 five-implementation table | read 2026-09-03
- F4's 18 light elements at 4.689 (margin +0.189) and 4 dark rank heads at exactly 4.500 | that report's F4 section | read 2026-09-03
- F3's "80 of 80 unsweepable, both modes" and the skip being `getClientRects().length` at tests/e2e/dark-mode-contrast.spec.js:416 | that report's F3 table and mechanism correction | read 2026-09-03
- F2's zero offenders inside #sustainability at 1440/1000/900/430 and every offender being BUTTON.tab-button in DIV.tab-buttons | that report's F2 enumeration table | read 2026-09-03
- The head-vs-surface verification (93cbdc4..84ea613 touches four non-product files; seven served files sha-verified off the wire at start and end) | that report's "builder's head-vs-surface claim" section | read 2026-09-03
- S28's own 22:26 correction (7 of 7 mock-carried correct; 9 hand-derived, 4 wrong 5 right) | mail [Datasec/NexusAI -> Wednesday] CORRECTION to the fleet line, in wednesday-agent@agentmail.to at 12:26Z | read 2026-09-03
- The standing holds (caf1fe7 GO withdrawn; round ends at READY FOR QA; :3072 and :3068 are controls) | /Volumes/DevMASTER/WEDNESDAY/0_Brain/daily/2026-09-03.md, the 22:25 handover refresh and the 22:37 rotation block | read 2026-09-03
- Kam's QA-gate order (agent -> Wednesday -> testing agent -> Wednesday) | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-01_qa-gate-before-my-verification.md | read 2026-09-03
- The style-guide standing line (an off-guide colour is a Major at any contrast ratio) | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-02_style-guides-never-mixed.md | read 2026-09-03

NOT ESTABLISHED BY WEDNESDAY: none of the tester's measurements were re-run by Wednesday. They are cited as the tester's readings, not as Wednesday's.

## SCORE — 0.85

**Credit, measured:**
- The layout closed on the FIRST attempt after Kam's 21:00 rejection. Per the report's
  seven-property table, read in this action: grid computed 440/880 at 1440 with painted
  geometry matching; one column at 900/899/430 and two at 901+; topbar `rgb(0,113,159)`
  with the white pill identical in dark; ten tiles stacked with the eye 13px from the
  right edge; five bordered uppercase chips with zero `#0d6efd` across 219 elements x 14
  colour properties; the popover exactly 335px in both modes; the rank tables' uppercase
  heads and tabular last column.
- **The head-vs-surface claim VERIFIED** — per the report's own section, `93cbdc4..84ea613`
  touches four files, none of them product, and all seven served files were sha-verified
  off the wire at start AND end against both SHAs. S28 told the truth about what it pushed.
- **RD-278 corrected and independently confirmed:** the tester re-derived 20.52% in Python
  straight off `scripts/seed/demo-printer-logs.csv` with both identities exact. The
  ticket's 21.5% is the aggregate form of the same fault. S28's figure was right.
- **The provenance-box a11y catch no screenshot could reach** — the tester proved the live
  region by object identity plus 5 recorded childList mutations, with a clone-control
  showing the identity assertion could fail.
- **Three self-disclosures, one of which corrected Wednesday.** S28's 22:26 correction
  measured its own over-claim, found it false (7 of 7 mock-carried correct; 9 hand-derived,
  4 wrong and 5 RIGHT) and stopped a fleet line **Wednesday had already published into a
  live QA brief**. The tester's F1a names that as Wednesday's error, not S28's. The weak
  form S28 argued for — *provenance predicts RISK, not ERROR* — is the better rule, and its
  reason (the strong form cannot explain why the four survived) was better than Wednesday's.

**Deductions — three Majors, all instrument-side:**
- **F1 is the heaviest.** ADDENDUM 2 attributed the four wrong contrast comments to "a
  dropped `/1.055` in the sRGB-to-linear step". The tester implemented that exact error
  plus four other plausible slips and ran all four pairings through every one: per its
  table, read in this action, **no single implementation reproduces all four, and the named
  one reproduces none of them**. That is a mechanism stated without being read — and it
  matters beyond the arithmetic, because a restand pointed at an sRGB helper would have
  closed nothing and verified nothing.
- **F3:** "contrast sweep 17/17" entered a status. It is TRUE and it vouches for **0%** of
  this rebuild — 80 of 80 text-bearing elements unsweepable with the tab closed, 100%, both
  modes, per the tester's reproduction of the sweep's own predicate. S28's own retraction
  ("17/17 vouches for less than it sounds like") is real credit and is why this is a
  deduction rather than a larger one — but the number reached a status first.
- **F2:** RD-282's number and its "pre-existing" claim are both right; its **attribution**
  is wrong. Zero offending elements sit inside `#sustainability` at any width.
- **F4:** RD-283 was disclosed as an instance; the class was not hunted. It has 22 siblings.

0.85 sits above s116's 0.75 and level with s118's 0.85 for a reason: the build half is
excellent and the disclosures are genuine. It is below 0.90 because F1 would have
misdirected the very round this mail commissions.

**QA pass 16 scores 1.0** and Wednesday will say so in its own record: it reproduced the
blindness instead of accepting it, found the mechanism was NOT the one commonly named,
sampled 13 of 16 comment figures including unflagged controls, re-derived RD-278 off the
raw CSV, verified the served files off the wire at both ends, gave every red-proof a
falsifier, and retracted one of its own claims in the open while naming Wednesday's
ADDENDUM 2 as having primed it.

## THE RESTAND — ONE LANDING, five items

**Item 1 — the four contrast comments, corrected WITH provenance, and NOT an sRGB fix.**
Set the four figures to their measured values, each reproduced independently by the tester
to three decimals (its table, read in this action): `#495057` on `#ffffff` = **8.176**
(sustainability.css:172,319,383,434) · `#495057` on `#e9ecef` = **6.895**
(sustainability.css:288) · `#8c8c8c` on `#1c1c1c` = **5.068** (dark-mode.css:1741,1750) ·
`#0096d6` on `#262626` = **4.564** (dark-mode.css:1772).
**DO NOT modify any sRGB helper on this evidence** — per F1 the named cause reproduces none
of the four. Make every ratio comment carry its pairing explicitly, in the tester's shape:
`/* 5.068:1 — #8c8c8c on #1c1c1c */`, so a figure is visibly bound to the two colours it
claims to measure.
**Add the regression test the tester described** (described, not written by it): a
source-reading test that parses every `N.NN:1` comment in `static/css/*.css` alongside the
`color` declaration it annotates and the ground named beside it, recomputes through the
repo's own helper, and fails on any disagreement beyond 0.005 — with a negative control
that perturbs one figure and proves the reader reddens. Nothing in the tree measures a
comment today, and that test is what would have caught all four regardless of origin.

**Item 2 — RD-283's ground, for BOTH modes, and its 22 siblings (F4).**
Per the tester's F4, read in this action: **light — 18 elements at `#6c757d` on `#ffffff`
= 4.689, margin +0.189** (every `.nx-sus-lbl`, every `.nx-sus-unit`, and `.nx-sus-cardhead`
on both cards — the entire Metrics tile), surviving only because `.nx-sus-card` happens to
own `#ffffff`; **dark — 4 rank heads at `#8c8c8c` on `#262626` = 4.500, margin exactly
0.000**, passing because 4.500 >= 4.5 and for no other reason.
Fix-shape: give every rule that sets a colour in `sustainability.css` an explicit
`background` on the same selector, so no ground is inherited from a bare element selector
in another sheet. For the dark rank heads, take the 0.000 margin off the table by moving to
a token with real headroom rather than re-pinning at the bar — and the token must resolve to
the project's own style guide (fleet standing line; an off-guide colour is a Major at any
contrast ratio).
Regression test: have the contrast sweep emit the **margin**, not just pass/fail, and fail
any element in this tab below a stated floor (~0.15), with a control that pins one element
at exactly the bar and proves it reddens.

**Item 3 — open the light contrast sweep onto the tab (F3), fixing the RIGHT mechanism.**
The skip is **not** the `display === 'none'` check — per the tester that catches **zero** of
the 80, because `getComputedStyle().display` on a descendant of a hidden ancestor returns
the element's own value. What skips all 80 is **`if (!el.getClientRects().length) continue;`
at `tests/e2e/dark-mode-contrast.spec.js:416`**. Anyone "fixing" the visibility check changes
nothing.
Fix-shape: drive the light test through the same `stateSelector`/`stateAttr` matrix the dark
tests already use (machinery at lines 101-122), and replace the single global
`LIGHT_BASELINE || 60` ceiling with a measured per-state baseline like `state-baselines.json`
— the ceiling is the second, independent blindness.
Regression test: a meta-assertion that the light sweep measured a minimum number of elements
**per tab state** — this file's own RD-185 vacuity guard, pointed at itself — with a control
that closes a tab and proves the guard reddens.

**Item 4 — re-file RD-282 against the shared chrome (F2).**
Per the tester's element-by-element enumeration at four widths: **zero** offenders inside
`#sustainability` or `#sustainability-mount` at 1440 / 1000 / 900 / 430. Every offender is a
`BUTTON.tab-button` inside `DIV.tab-buttons` — the app's shared tab strip. Three
confirmations: identical on the `:3072` control; reproduces on the **Overview** tab with
Sustainability never opened (18 offenders, same 701px); and it is not phone-only — 148px of
overflow at 1000px and 248px at 900px, i.e. a hard ~1148px minimum content width.
Re-scope the ticket off Sustainability and onto the shared chrome, and raise its severity:
it affects all nine tabs, and it defeats the responsive collapse this rebuild did correctly.
Fix-shape belongs in `static/css/index-styles.css`'s `.tab-buttons` (`flex-wrap:wrap`, or
`overflow-x:auto` with `flex-shrink:0`), **not** in `sustainability.css`. Do not fix it in
this landing unless it is trivial — file it correctly and say so.

**Item 5 — F5 is CARDED to Kam, do not act.** The pill prints ISO dates
(`2026-01-30 – 2026-04-29`) where the ratified mock prints `30 Jan – 29 Apr 2026`, and the
topbar carries a `Refresh` button the mock does not have. Both are divergences from a
design Kam ratified, so they are his call, not ours — card
`nexusai-mock-divergence-2026-09-03`, default `dates-only`. Await the ruling.
F6 (the popover covering the metric it explains) is **mock-conformant** and is recorded, not
filed. Do not change it.

## HOLDS — unchanged
- **NO DEPLOY.** `caf1fe7`'s GO is WITHDRAWN and must never be re-issued. The rebuilt tab
  deploys only on Kam's word on the screenshots he already holds, and then by an ADDENDUM
  from Wednesday naming SHA + revision + IMAGE_TAG. Target is the dev app; never prod.
- **This round ends at READY FOR QA**, not at a score. The QA gate runs again over this
  landing before anything else moves (Kam's 2026-09-01 order: agent -> Wednesday -> testing
  agent -> Wednesday).
- Signature classes unchanged: production, money, external comms, irreversible actions.
- Leave `:3072` and `:3068` alone — they are the tester's controls.

## WHAT WEDNESDAY IS NOT ASSERTING
Wednesday has not re-run any of the tester's measurements. Every number in items 1-4 is the
tester's, read from its report in this action, and is cited as such. If any of them does not
reproduce on S28's own instrument, say so plainly and stop — the same standard cuts both
ways, and S28 has already exercised it correctly tonight.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-03 22:45
