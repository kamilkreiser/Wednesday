# QA_CHANGES — pass 7 (s15, round 6 second half)

**Branch:** `rd-136-nga-defaults-s12`
**Surface head:** the SHA named in the `QA SURFACE UP (pass 7)` mail and printed by
`qa-surface-up.sh` — named by reference, not written here, because a SHA written into
this file is stale the moment the file is committed (the ee3c4c1 lesson).
**Surface:** local run on **port 3016**, from the worktree for that SHA, auth OPEN by design.
**Previous surface:** `ca98a55` on `:3015` — **retired** (process stopped; worktree and
its `qa-data` kept, as always).
**Range under review:** `f48ea5f..HEAD` — the four commits of round 6's second half.
`QA_DIFF.patch` carries it. **This pass is a DELTA** over pass 6.
**The demo is untouched.** Revision `--0000092` = `ca98a55`. Nothing in this round is live,
and nothing here asks for a deploy.

---

## WARNING 1 — which stylesheets each page links, and in what order

All three dark-mode pages now link, in this order:

```
<page>-styles.css → inline-styles-extracted.css → feedback-widget.css → dark-mode.css  (LAST)
```

`dark-mode.css` **moved to last** in this round (RD-158). Two things about that:

- **It is inert in a browser.** All 175 selectors in `dark-mode.css` are
  `.dark-mode`-scoped, and no other stylesheet in the product defines a
  `.dark-mode` rule. Both halves are pinned as tests with negative controls that
  sabotage a copy in memory. In a browser those rules already out-specified
  everything they now also follow in source order.
- **It was made so the harness resolves the same winner a browser does — not to
  change what a user sees.** If pass 7 finds a *rendered* difference attributable
  to the move alone, that contradicts the invariant and is worth reporting loudly.

The other **eleven** shipped pages link no dark stylesheet at all (RD-167), so
they render light whatever the user's setting. `chart-details.html` is the one
that matters most here: it is a drill-down from the dashboard.

## WARNING 2 — whose claim is whose

| Mine (jsdom) | The tester's (real engine) |
|---|---|
| the colour arithmetic | whether the page actually reads correctly |
| which of *our* rules apply | anything Bootstrap paints |
| that light did not regress | `!important`, `var()`, colour inheritance |
| that a rule exists and matches | every button with a `btn-*` class |

**A pass in my suite means "our own stylesheets no longer fail this node."** It
does not mean the page renders correctly.

---

## The counts, and what they are not

| page | dark before | dark after | light before | light after |
|---|---|---|---|---|
| first-run-setup | 267 | **30** | 169 | **169** |
| index | 99 | **29** | 91 | **91** |
| settings | 7 | 7 | 7 | 7 |

**267, 328 and 30 are three different wrong cascades, and none of them is a
product count.** Before RD-158 the harness read the sheets in an order no engine
uses and reported 267; with `dark-mode.css` loaded last but before the fix it
reported 328; it now reports 30. The differences between those numbers are the
instrument, not the page.

The reason is **RD-163**, found this round: **jsdom resolves the CSS cascade by
source order and ignores selector specificity entirely.** Four isolated probes,
pinned in `__tests__/jsdom-cascade-limit.test.js` — the less specific rule wins
when declared last, the answer flips when the order flips, it behaves identically
for shorthand and longhand, and both single-rule controls discriminate.

So: **enumerate with these numbers, decide with yours.** The real-engine table is
the only thing pass 7 should judge by. The same caveat retires the 267/99/7 in
the s15 handover.

Light is pinned **exactly** at 169 / 91 / 7 — one more or one fewer fails the
build, so a colour leaking into light mode cannot pass unnoticed.

---

## MEASURE THIS FIRST

The tightest pair in the entire round is **muted `#9090a0` on the warning tint
`#332a12` at 4.51:1** — it clears AA by 0.01. If any single pair is going to
disagree between engines, it is that one.

---

## What changed, one row per item

| id | ticket | what | where |
|---|---|---|---|
| R6-2 | RD-158 | 51 extracted `.s-xxxxxxxx` classes on first-run-setup painted light surfaces with no dark counterpart. Grouped by the value each paints, reusing round 4's palette: white→`#1e1e3f`, `#f8f9fa`→`#252550`, `#e7f3ff`/`#cce5ff`→`#16263f`, `#fff3cd`→`#332a12`, `#d4edda`→`#14301f`, `#f8d7da`→`#3a1a1e`, plus matching foregrounds. | `dark-mode.css`, `a8c8162` |
| R6-2 | RD-158 | `dark-mode.css` linked LAST on all three pages, with an invariant test and a link-order test, both with negative controls. | 3 pages, `a8c8162` |
| — | RD-163 | The jsdom cascade defect, pinned. | `jsdom-cascade-limit.test.js` |
| R6-3 | RD-159 | `div.controls` and `div.ai-assistant-section` (and `.data-table`, `.info-card`, `.import-section`, `.file-drop-zone`, `.risk-conditions-summary`) darkened. The **eight filter labels** the tester measured at 1.23:1 now clear AA via the surface. | `dark-mode.css`, `f822839` |
| R6-3 | RD-159 | `body.dark-mode th` — the dashboard tables are not Bootstrap `.table`s, so a bare `th { background:#f8f9fa }` head was never darkened. | `f822839` |
| R6-3 | RD-159 | Sort chevrons `#6a6a7a`→`#a8a8bc`; `.risk-category-title` `#e74c3c`→`#ff9c9c` (was 4.46, under AA by 0.04). | `f822839` |
| R6-3 | RD-147 | The **sixteen** `.table-title` headings — one rule, one counterpart. | `0c4ea07` |
| R6-3 | RD-159 | The **quick-question chips**: six colour objects became six variant classes, because an inline style at 1,0,0,0 cannot be themed by any stylesheet without `!important`. | `index.js`, both sheets, `4ab4182` |

---

## Known unverifiable from my seat — stated, not glossed

- **`.list-group-item`** on first-run-setup is **latent**: it is hidden until
  "Detect Columns & Validate" is pressed. It is styled, and it is
  **unverifiable in a render until that step is reached.**
- **The `.example-prompt` chips** are created by `index.js`, so they are absent
  from the static markup the page sweep walks. They are covered instead by a test
  that builds a chip on the real stylesheets inside the card it lives in. That
  measurement *is* mine to make — these buttons carry no Bootstrap class, so the
  missing Bootstrap does not distort it — but it is not a page render.
- **The load overlay** (RD-166) reads white-on-white at **1.00:1 in BOTH modes**
  to my harness, which strips scripts. A browser removes the overlay after load,
  which is why the pass-6 sweep never reported it. **Severity needs a real
  browser on a throttled connection** before anyone ranks it.
- **Every `btn-*` button.** jsdom gives them the UA button face (`#efefef`), a
  browser gives them Bootstrap's. Those rows in my residue are noise; yours are
  the real reading. This is R6-1's lesson and it has not changed.

## Deliberately not touched

- **Brand chrome on `#0096d6`** — RD-160, Kam's card. Measurements added, nothing
  changed. Note it fails in **light** mode too, at the same 3.32, so it is a
  brand-palette decision rather than a dark-mode bug. `.step-title` 2.71 and
  `.step-desc` 1.89 are **newly visible, not newly created**: their dark rules
  pre-date this branch and already out-specified the extracted ones in a browser.
- **Light mode** — 169 / 91 / 7 pre-existing, ruled off-delta. Not fixed, not
  regressed, pinned exactly.
- **RD-155**, **SCIM** — untouched, per the standing holds.

## Filed this round

RD-163 (High, instrument) · RD-164 (border contrast, pre-existing) ·
RD-165 (hash-keyed counterparts are regeneration-fragile — a guard now fails the
build if a probed hash is renamed) · RD-166 (load overlay) ·
RD-167 (**High** — dark mode is a three-page feature; eleven pages never link the
stylesheet) · RD-168 (**High** — `npm run verify` went 88s → 10m33s this session;
I introduced it, and the fix is deliberately deferred because it means changing
the instrument every number here was measured with).

**Suite: VERDICT PASS — 930/930 across 42 suites.**
