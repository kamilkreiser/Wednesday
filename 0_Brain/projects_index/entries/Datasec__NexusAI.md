---
client: Datasec
project: NexusAI
path: /Volumes/DevMASTER/!CODING/Datasec/NexusAI
status: active
updated: 2026-09-03
---

# Datasec / NexusAI

**🔴 DEPLOY HOLD (Kam, 2026-09-02 07:3x — brand): the dark theme (rounds 6–8, head `6b78315`/`451dfba`) is an INVENTED navy/indigo palette (`#1a1a2e`/`#1e1e3f`/`#252550`/`#16213e` — measured from my seat) and the repo has NO style guide / brand-token file. Kam saw it as another client's aesthetic. Rounds 6–8 do NOT deploy on any pass-9 contrast verdict — deploy = a Kam-approved palette first. s17 item 0 = write `docs/STYLE_GUIDE.md` + a brand-token file from the product's existing HP tokens (`#0096d6` family in the light theme), derive the dark palette from it, PROPOSE to Kam as rendered screenshots both modes, then re-theme; a guard that every dark-mode colour resolves to a token. Pass 9 carries a brand-conformance leg (ADDENDUM 2). Lesson: learnings/2026-09-02_style-guides-never-mixed.**

**s12 (2026-09-01 17:3x→19:37, 0.85) + s13 LIVE (19:45→):** Kam's round-2 commission (17:25): Settings icon (bi-tree) · 27 NGA-2025-sourced deployment-default factors with references · Sustainability tab root-caused + fixed · SCIM F-1/F-4 tests-first (fb3b11e) · the fleet QA GATE's first live run (Kam 17:55): pass 1 = 18 findings on a 1.0-scored build → fix round (14/17 held) → pass 2 = PASS with findings, six dashboard Major rows + two SCIM Majors remain → **item 5 'fully functional' NOT MET** (PAPER COST $0 on the empty default view) → s13 = refine round 2 on branch `rd-136-nga-defaults-s12` (head cca9fb014). Nothing deployed since --0000091; SCIM OFF. RD-141/143/144/145/146 filed.

**Open / next (refreshed 2026-09-03 06:57 — S21 WRAPPED 20:00:51Z READY FOR QA at `2bc7ef7` (verified on origin by ls-remote): ten fixes / eleven commits / seven new tickets; RD-237 built (a second limiter on `/api/setup/*` with no env override — now `SETUP_RATE_LIMIT_MAX`); jest 1160/1160 at `fc8e779`; the full gate at `2bc7ef7` NOT RUN and the e2e set NOT MEASURABLE (the Studio's Docker VM wedge — Kam's card); PASS 13 = THROUGH-CODE leg LAUNCHED (pane %27, brief qa-agent/briefs/2026-09-03_nexusai-s21-round13-pass13-through-code.md); NO deploy):**
- **Pass 13 through-code → my completion check (delivered vs the S21 brief + the seven ANSWERs) → SCORE s21 (rec ~0.90–0.95) → S22 brief.** Pass 13b (the BROWSER leg: e2e at `2bc7ef7`, hover across the product, the acceptance sweep, the brand leg on rendered pairings, the screenshots Kam sees) runs only after Kam restarts Docker. Deploy GO needs 13 + 13b + completion + Kam's palette word on record.
- **Surfaces:** `:3053` UP (pid 95059, `RATE_LIMIT_MAX=20000`, sess 0 / tty ??, at `fc8e779`) · **`:3052` DOWN — my act 06:5x** (died with S21's pane close; ledger w=2, lesson 2026-09-03_a-pane-close-is-a-session-kill) → S22 re-stands the DEFAULT-limiter subject at `2bc7ef7` (from a script file, detached) before pass 13b. 18 idle QA listeners on `:3023–:3053` untouched.
- **Kam's morning:** RD-236 (the settings encryption key derives from a file in his HOME — product decision) · RD-233 (the Jira transition rename — until then that transition is never invoked by name: the first match lands in Declined) · `~/data` written by the pass-12 tester (card, default leave) · the six NexusAI cards (rd196 B · rd198 B · rd202 HOLD · brand-chrome-dark-token leave · primary-action-blue leave · costs-header-green-gradient C).
- **Not done, named by the builder:** hover unmeasured across the product (a 13b leg) · RD-224 filed not fixed · RD-234/235 filed not built · three deliberate `listen(0)` prose lines remain.
- Scores: s20 0.85 · QA pass 12 1.0 · s21 pending.

**Open / next (refreshed 2026-09-03 02:06 — PASS 12 = PASS with findings (all four fixes FIXED; render matches Kam's approval); s20 SCORED 0.85, QA 1.0; S21 LAUNCHED (pane %23) on P12-02 → P12-01 → P12-03 → the round's instruments → RD-203 rollout → RD-223 sweep → pass 13; DEPLOY HELD on P12-02 (DATA_DIR loses to $HOME/data) + P12-01 (overlay CTA invisible in dark)):**
- **Kam's morning (NEW):** the pass-12 tester's run wrote to `~/data/settings.json` on the Studio via P12-02 — card `nexusai-home-data-mutated` (rec restore from `~/data/backups`; default LEAVE; nobody in the fleet touches `~/data`).

**Open / next (refreshed 2026-09-03 01:10 — S20 WRAPPED READY FOR QA at `79dc30a` (code head `e952f3b`, docs-only delta); PASS 12 RUNNING (pane %20) on `:3042`; NO deploy):**
- **Pass 12 → my completion check → SCORE s20 (−0.05 candidate: the 00:47 turn-end stall) → S21 brief** (RD-203's 7 files / 18 sites · the RD-223 class sweep · whatever pass 12 finds). Deploy of the repaint needs pass 12 + completion + GO; the palette word is on record (20:14, card A).
- **Landed this round:** RD-217 `5f3b0bf` (far stops → `#106ebe`) · RD-216 `badff5f` (dark selected step; the chip's lost circle = Kam's eye) · RD-195 `6339847` (allowance with a real-server control) · RD-223 `e76c734` (the midnight red, pinned) · RD-211 `4835d59` (Appearance preview, dark branch) · RD-218 `4e0ada2` (the `--*-rgb` reader, three holes) · RD-203 `e952f3b` (one file). Ticket-only: RD-180 (its own `#0d1b2a` FAILS; only `#000000` clears — needs-decision) · RD-162 (five dead blocks = one) · RD-61 (resolved by SUBSTITUTION; RD-118 confirmed in prod logs; no `az` write) · RD-148 sized.
- **Surfaces:** `:3042` (e952f3b, DEFAULT limiter — the pass-12 subject, pid 28105) · `:3040` (raised, pid 26107) · controls `:3029` (2b014bc) + `:3024` (463f03d); `:3036 :3038 :3039` intermediate. Demo `--0000092` = `ca98a55` untouched.
- **Kam's cards:** rd196 (B) · rd198 (B) · rd202 (HOLD) · brand-chrome-dark-token (leave) · primary-action-blue (leave) · costs-header-green-gradient (C, RD-215 ticketed) · NEW for the morning: the wizard chip circle (a dark token = brand) · RD-180's options A–D · RD-61 close-by-substitution + a real-ingest health-check ticket (rec).

**Open / next (refreshed 2026-09-02 23:08 — PASS 11 = PASS with findings: P10-01 FIXED against the control; 3 Majors (P11-03 on the round's own repaint) → s19 SCORED 0.90, QA 1.0; NO deploy; S20 = round 12, brief staged):**
- **S20 queue:** P11-03 far stops → `#106ebe` (ruled value, no new token) → P11-01 the Costs header PAIRING (the ruled gradient's stops never move) → P11-02 the dark active wizard step from existing tokens → RD-195 (three conditions) → RD-211 both branches → P11-05 → items 7–9 → RD-203 → pass-12 surface → wrap READY FOR QA → pass 12 → my completion check → deploy GO.
- **Kam's cards:** rd196 (B) · rd198 (B) · rd202 (HOLD) · brand-chrome-dark-token (leave) · **NEW nexusai-primary-action-blue** (P11-06: Bootstrap `#0d6efd` on the primary buttons beside the HP chrome; rec A repaint to the chrome pair; default B leave). The palette he approved is what rendered (tester's (f), screenshots in the pass-11 evidence/).
- **Surfaces:** `:3029` (2b014bc, default limiter, the subject) · `:3030` (raised) · `:3024` (463f03d, the P10-01 control) · `:3023`, `:3025`–`:3028`. Demo `--0000092` = `ca98a55` untouched.
- **Debt located, not this round's:** 30 unexcused off-guide dark values (27 on index.html per BRAND.md §2) in RD-206's ratchet; 66 light = the product's own pre-existing palettes.

**Open / next (refreshed 2026-09-02 22:29 — s19 WRAPPED 12:15Z READY FOR QA at `2b014bc` (+docs `de6e51b`); PASS 11 RUNNING (pane %14) on `:3029`; NO deploy):**
- **Pass 11 → my completion check → SCORE s19 → S20** (RD-195 first, then RD-211, items 7–9, RD-203's remedy). Deploy of the repaint needs pass 11 + my GO; Kam's palette word is on record (20:14, card A incl. gradient chrome).
- **Surfaces:** `:3029` (2b014bc, default limiter — the subject, pid 57380) · `:3030` (2b014bc, RATE_LIMIT_MAX=20000, pid 57512) · controls `:3023` (29ea1c0) · `:3024` (463f03d); `:3025–:3028` up. Demo `--0000092` = `ca98a55` untouched.
- **Kam's cards:** rd196 (default B) · rd198 (default B) · rd202 (default HOLD) · brand-chrome-dark-token (default leave).

**Open / next (refreshed 2026-09-02 22:13 — s19 ROUND 11: items 0–4 DONE, head `2b014bc` verified on origin; wrapping after item 5; NO deploy):**
- **Landed:** RD-205 `db0d1d6` · RD-209 `9449cdb` · RD-206 `7bd442e` · RD-207/208/214 `2b014bc` (23 chrome sites repainted on Kam's approved palette A; 12/13 gradient signatures; the Bootstrap-success gradient stays by ruling). Jest 1103/1103; Playwright 21/21 in ONE run at RATE_LIMIT_MAX=20000 (disclosed — RD-195 option-B evidence, not settled).
- **s19 → wrap:** item 5 (RD-210 docs) → pass-11 surface at the final head → WRAP with SETS + S20 handover (item 6 RD-211 + the brief's items 5–8 first; RD-195 fix = S20's first infra item). Then: pass-11 QA brief (tester re-derives the gradient population; RD-206 corpus resolves -rgb; the FOUR unverified sheets admin/legal/testing/feedback-admin as a brand-leg set) → completion check → SCORE s19 (note: 70df9fd committed on a red verify, self-disclosed) → S20.
- **Surfaces:** :3023–:3027 (default limiter) + :3028 at 70df9fd (raised limiter), all daemonised + pidfiled. Demo `--0000092` = `ca98a55` untouched. SCIM OFF.
- **Kam's cards:** rd196 (default B) · rd198 (default B) · rd202 (default HOLD) · brand-chrome-dark-token (default leave). Palette approved 20:14 (card A) incl. gradient chrome.

**Open / next (refreshed 2026-09-02 19:45 — PASS 10 FAIL on P10-01 (the re-theme's own blocker) → s18 SCORED 0.85, QA 1.0; s19 ROUND 11 LIVE since 19:20: item 0 done (RD-205..213 filed), item 1 RD-205 CLOSED at `db0d1d6` (1.00 → 5.14 dark, light byte-identical); NO deploy):**
- **Palette:** the tester's judgement = the neutral re-theme reads as THIS product ("the largest single improvement of the campaign"); the pass-10 screenshots are on Kam's device as the PROPOSAL — **his word is the deploy gate**. Remaining foreign notes = the Bootstrap CONTROLS (Apply Filters `#0d6efd`, Settings `#198754`, FAB `#106ebe`, the Flat-UI consumable bars).
- **s19 queue (round 11):** P10-01 ✅ → P10-04 (RD-209: gradient awareness IN `ground()` — the repo sweep never read `background-image`, a FALSE PASS not an exclusion) → P10-02 (RD-206: the brand gate on rendered PAIRINGS across all sheets + JS; must resolve `-rgb` triples — RD-213) → P10-03/03b (RD-207/208) → P10-05 (RD-210) → P10-06 (RD-211) → items 5 (RD-162/176/178/180) · 6 (RD-61 measure-and-plan) · 7 (SCIM sizing) → pass-11 surface daemonised at the final head → wrap 65–70%.
- **Surfaces:** `:3023` (29ea1c0, round-9 control) · `:3024` (463f03d, pass-10) · `:3025` (db0d1d6, item-1 verification) — all daemonised (os.setsid), PID files under /tmp/nexusai-qa/. Demo `--0000092` = `ca98a55` untouched. SCIM OFF.
- **Kam's cards open:** rd196 (dashboard default window; default B stands) · rd198 (border token naming; default B) · rd202 (light active tab indigo; default HOLD). None blocks the round.

**Open / next (refreshed 2026-09-02 08:0x — PASS 9 read: s16 round 8 SCORED 0.90; contrast the strongest round yet; BRAND leg FAILS → NO deploy; round 9 = s17, style guide FIRST):**
- **Pass 9 (real browser, `:3018` @ `6b78315`):** every P8 id CLOSED with controls — settings dark 21→9 (all RD-160 chrome), wizard 19/19 RD-160, dashboard 18→6 groups; RD-179 closed with the allow-list out; RD-171/161 closed; RD-172 determinism re-proved non-vacuously; four guards RED under sabotage. **Residual dark-only Major: P9-04** `a.btn.btn-success` (header Settings button ×9) 4.53 light / 2.18 dark, hidden by an allow-list reason written for another element. **Instrument: P9-03** the sweep measures the dashboard on the EMPTY default window; P9-05 empty determinism subject; P9-06 `#aiQuery` white input outside the guard's population.
- 🔴 **P9-01/P9-02 (Kam's 07:3x observation, measured): 59 of 62 dark values (95%) resolve to nothing in the product's own palette; `#0096d6` 71× light / 1× dark; the brand-blue metric values repainted grey; NO style guide/token file in the repo. NOT on s16's score (coordinator's gap). Rounds 6–8 deploy HELD on a Kam-approved palette.**
- **s17 queue (round 9):** (0) `static/css/tokens.css` + `docs/BRAND.md` from the product's OWN light tokens, dark counterparts by a STATED rule, a resolves-to-token check that FAILS by name → **rendered PROPOSAL to Kam (dashboard + wizard, both modes) BEFORE any re-theme** · (1) P9-04 split the allow-list + fix + the "every 'identical in light' excusal asserted both modes" test · (2) P9-03 data dimension in the MATRIX + count bands from the seed · (3) P9-05 · (4) P9-06 form controls into the guard · (5) P9-07 → tickets (three `/api/normalized/*` 503s per load; CSP `style-src-attr` self-violations on the wizard; the null `disabled` TypeError) · RD-162/176/178/180 as sized. `:3018` stays up as the control until s17 stands its own. `:3017` RETIRED 08:0x (pass 8's surface, planned).
- **Kam's:** the PALETTE (nothing themed ships without his word) · RD-167 (3 of 14 pages) · RD-160 (brand chrome; now 19/19 of the wizard's dark residue) · RD-155 High · SCIM A/B (A) · energy KPIs (dark).

**Open / next (refreshed 2026-09-02 05:0x — PASS 8 read: s15 round 7 SCORED 0.85; leg 3 NOT MET → NO deploy; ROUND 8 = s16):**
- **Pass-8 verdict (real browser, whole page, both modes + the load-time render):** P7-01 CLOSED (1.07→12.39; `.warning` 11.58) · P7-03 CLOSED (1.35→7.27, state machine proven by a click) · both P6-01 residues CLOSED · P7-04 guard exact 142/142 · **the wizard's 19 remaining dark lines are ALL RD-160 brand chrome (Kam's card) — the first clean page of the campaign** · light unregressed, zero round-7 values leak. 🔴 **P8-01 (Major, pre-existing, newly swept):** `.bg-light`/white cards keep light grounds under `body.dark-mode` (1.14–1.23, three settings panels; `dark-mode.css` has ZERO `.bg-*` counterparts — Bootstrap's carries `!important`) · 🔴 **P8-02 (Major, ROUND-7 REGRESSION):** the `.btn-outline-secondary` rule lightens text onto those light grounds (same button 4.45 light vs 1.66 dark) · 🔴 **P8-A:** the P7-02 flash SURVIVES the link fix — mechanism is `dark-mode.js` (class only at DOMContentLoaded; 0 `[data-theme]` selectors), normal case <81 ms · P8-03/P8-04: the in-repo sweep's numbers are physically impossible (mid-fade continuum) AND it ships aimed at retired `:3016`, wrong localStorage key, pages-as-loaded (cannot see P7-01) · P8-05/06 guard blind spots (classList.add evades; drift guard one-directional; memo stale on DOM mutation) · P8-07 `consumable-text` 1.19 both modes (designer's text-shadow mitigation named).
- **Round 8 (s16, briefed from `S16_ROUND7_HANDOVER.md` at `9b4e829` + the SCORE mail):** (1) P8-01+P8-02 TOGETHER (`.bg-*` counterparts with `!important` + the luminance guard) · (2) P8-A mechanism (`html[data-theme]` top-level grounds; timing regression test, not position) · (3) the sweep usable = RD-172 done once (state-based settle + navigation matrix + run-twice-same-sets + live port + the product's own `darkMode` key) · (4) P8-05/P8-06 hardening · (5) RD-171 → RD-161/162 · file P8-01 (High) / P8-02 (High) / P8-07 tickets → `QA SURFACE UP (pass 9)` → completion check → SCORE → deploy GO by digest only then.
- **Deployed state unchanged:** demo `--0000092` = `ca98a55` (verified untouched: zero non-GET all session; `$HOME/data/settings.json` byte-identical). `:3017` now PID 7242 (the tester's, left up). SCIM OFF. Kam's cards: RD-160 (now 19/19 of the wizard's residue + 18 dashboard lines) · RD-167 (3 of 14 pages) · SCIM A/B (A) · energy KPIs (dark).

**Open / next (refreshed 2026-09-02 02:48 — PASS 7 read: s15 SCORED 0.90; NO deploy from `4ab4182`; ROUND 7 on the delta → pass 8):**
- **Pass 7 verdict (real browser, whole page, both modes):** P6-01 FIXED at the root · P6-03 FIXED (9/9 filter labels, 98 `th`, chevrons 6.16, chips 6/6/6) · RD-147 FIXED (16/16 at 13.06) · Settings → Sustainability 0/0 dark AND light · light-leak check 0 · completion legs 1+2 UNREGRESSED (PAPER COST unavailable-with-reason; four honest period windows). **Leg 3 NOT MET:** 🔴 **P7-01** `.result-box.info` (`first-run-setup-styles.css:1427`, `#e7f1ff`) has NO dark counterpart — two boxes visible on first load of Advanced Setup at 1.07 (`p`) / 2.91 (`h6`); `.result-box.warning` defined in neither sheet · 🔴 **P7-02** the link move out of `<head>` to the end of `<body>` renders every page fully in LIGHT during load for every dark-mode user (steady state inert: 1,816 elements / 0 diffs; during load NOT — `dark-mode.js:11-14`'s own "no flash of light content" contract falsified; verified from my seat by curl of the served pages: `</head>` at line 27/20/19, the link at 1057/819/2305 — the tester's "22 → 1057" etc. are the link's OLD and NEW lines) · P7-03 pre-existing (`.btn-outline-primary.active` 1.35, the worst pair on the dashboard, byte-identical across three commits; the suite's declared blind spot) · P7-04 the RD-165 guard covers 15 of 142 hash-keyed classes. Wizard dark 87 → 25 (19 = RD-160 Kam's · 4 = P7-01 · 2 = P6-01 residue at 3.16/3.53).
- **Round 7 (s15 in-seat under its 50% rule, else s16) — ruled 02:5x:** (0) RD-168 memoisation FIRST with before/after proof no count moves (the tester's `first-run-dark-surfaces` timed out at 2 min — the cost is measured now) · (1) P7-02: link back into `<head>` on all three pages; give the HARNESS the ordering (RD-163 is jsdom's defect — the product does not carry its workaround); invert the link-order test + a general "no `<link rel=stylesheet>` in `<body>` on any shipped page" assertion · (2) P7-01: `.result-box.info` + `.warning` counterparts; guard = every `.result-box` variant present in the HTML has a `body.dark-mode` counterpart, derived from the HTML not a palette · (3) P7-03 on-delta this round (the whole page is the acceptance): `:not(.active)` scoping or an active-state dark rule · (4) the two P6-01 residues · (5) P7-04: 142 generated assertions, not 15 probes (RD-165 comment) · (6) **move the real-engine sweep into the repo as a Playwright check the owner runs** · tickets: P7-02 its own RD (High, this round's regression); P7-03 RD (Medium, pre-existing); RD-158 → In Progress; RD-157/159/147 stay Testing (engine-confirmed, comment) → `QA SURFACE UP (pass 8)` → completion check → SCORE → deploy GO by digest only then.
- **Deployed state unchanged:** demo `--0000092` = `ca98a55` (rollback `--0000091` sha256:055ea791…). SCIM OFF. Kam's cards: RD-160 brand chrome (19 of the wizard's 25) · RD-167 (3 of 14 pages; `chart-details` confirmed white) · SCIM A/B (A) · energy KPIs (dark).

**Open / next (refreshed 2026-09-02 01:26 — s15 LIVE %67 on round 6's second half):**
- **R6-2 / RD-158 DONE at `a8c8162`** (verified on origin): the wizard's dark SURFACES (51 light-only `.s-xxxx` classes) given dark counterparts, 267 → 30 in the harness (the 30 = RD-160 chrome / RD-145 Bootstrap / native option, each named), light pinned at 169, 886/886. **`dark-mode.css` now linked LAST on all three pages** (ruled 01:08 — jsdom cascades by SOURCE ORDER, ignoring specificity → **RD-163 High**, the harness; invariant + link-order tests sabotaged both ways). RD-157 + RD-158 → Testing. RD-164 (Medium, card border 1.47:1, pre-existing) filed.
- **R6-3 / RD-159 IN PROGRESS** (index.html `div.controls` + `.ai-assistant-section` as a new dark surface) **+ RD-147's `.table-title` folded in as its own commit** (16 headings at 1.55, one rule) → minors if they fit → `QA SURFACE UP (pass 7)` on :3016 → retire :3015 (PID 24637) → HOLD → pass-7 brief (whole page, all five wizard sections, both modes, the 4.51 pair first, the link move verified in the real engine) → completion check → SCORE s15 → any deploy = a fresh GO by digest.
- **RD-160 (Kam's card `nexusai-rd160-brand-chrome-contrast`, default HOLD) now carries the whole brand-chrome set:** white on #0096d6 3.32 · `.step-title` 2.71 · `.step-desc` 1.89 · `tab-button.active` 3.34 · `btn-success` 2.18 — **none mode-specific (fails in light too): a brand-palette decision, not a dark-mode bug.**

**Open / next (refreshed 2026-09-02 00:37 — 🎉 ca98a55 DEPLOYED to demo as --0000092; s14 WRAPPING on my word; s15 = round 6's second half):**
- **Deployed (verified from my seat 00:2x):** rev `--0000092`, image `1.23.0-rd136-s12-ca98a55`, digest sha256:c589bccc…; rollback `--0000091` sha256:055ea791… (re-read live before the swap); range 1d0b9c6..ca98a55 (rounds 2–5), 837/837; (a)/(e) preconditions SUBSTITUTED behind the SSO wall (platform-log line + the presence-discriminating `/css/dark-mode.css`, sha-identical, 404 control) — accepted; doc corrected. RD-136/137/138 **Release Ready**. For Kam: default view shows 'Unavailable' tiles by design (pick All Time); `POST /api/settings/costs` now 400s on invalid values.
- **Round 6 (s14 checkpoint 00:33):** R6-1 RD-157 DONE at `449af60` (the HTML's three typo classes fixed, not the CSS — 3 vs 11 uses, no sheet defined the typo; its flattering jsdom assertion deleted) · R6-4 RD-160 measured, NOTHING changed → **Kam card `nexusai-rd160-brand-chrome-contrast`** (rec #00719f on text-bearing chrome; default HOLD) · **R6-2 RD-158 + R6-3 RD-159 (High) → s15** from `docs/sustainability/S15_ROUND6_HANDOVER.md` at `3f180d6` (sweepPage ENUMERATES — 267/99/7 are over-counts, Bootstrap unpainted in jsdom; the real engine DECIDES — the tester's 87; settings clean) → QA SURFACE UP (pass 7, new port) → whole-page acceptance sweep → completion check → SCORE → any deploy = a fresh GO by digest. `:3015` stays up at ca98a55 as the live control until pass 7's surface stands. s14 SCORE at its wrap (rec 0.85–0.90: two rounds delivered in the engine; three own regressions across rounds 4–5, all gate-caught; exemplary disclosure; QA report ids pass 5 + pass 6).
- **Residual tickets (To Do):** RD-157 In Progress · RD-158 Med · RD-159 High · RD-160/161/162 Low · **RD-155 High PRE-EXISTING** (numeric-only settings.json abandons DATA_DIR — Kam's priority call) · RD-148 + auth-enforced P2-07 re-verify before any SCIM flip (card `nexusai-scim-deploy-live-ab` default A) · `nexusai-energy-kpis-tec` default dark.

**Open / next (refreshed 2026-09-01 23:26 — s14 round 5 briefed; NO deploy from 1f41edc):**
- **s14 (live, holding→round 5):** pass 5 = PASS WITH FINDINGS; my completion check FAILS leg 3 (first-run-setup dark 41/67 lines fail AA) → round 5: R5-1 cost `pattern` does not compile in Chrome (escape the dash; test compiles with the `v` flag) · R5-2 six `.text-*-emphasis` rules need `!important` · R5-3 dark counterparts for first-run-setup's own surfaces (light untouched) · R5-4 real `JsonStorage` in the cache test · R5-5 → RD ticket (a cost cannot be un-set through the product) → QA SURFACE UP (pass 6, new port) → my completion check → SCORE s14 → deploy GO by digest. :3013 retired on this ruling; :3014 until pass 6's surface.
- **Round 4 delivered at `1f41edc` (on origin):** P4-01 blocker dead in a real engine; 8/11 P4 ids fixed; 815/815; RD-152 (three Bootstrap versions) · RD-153 fixed · RD-154 open · **RD-155 High — numeric-only settings.json abandons DATA_DIR → `$HOME/data`; PRE-EXISTING (8eb94ce, 2026-04-18) → not deploy-gating; Kam's morning board: priority call.**
- **Demo:** still rev `--0000091` (s11's build); nothing deployed since. SCIM OFF (card `nexusai-scim-deploy-live-ab` default A; RD-148 + auth-enforced P2-07 re-verify first). Card `nexusai-energy-kpis-tec` default dark.
- **QA gate this project:** passes 1–5 all scored 1.0; the pattern across passes 3–5 — the stand-in agrees with the code and disagrees with the browser — is now the standing acceptance (one real-engine sweep per UI round).

**Open / next (refreshed 2026-09-01 19:4x):**
- [ ] s13: P2-01..08 fixes (tests at the CLASS, RED first) → QA SURFACE UP (pass 3, delta) → Wednesday's completion check → deploy to demo on GO (rollback by DIGEST sha256:055ea791…; Kam: default view shows 'Unavailable' by design — select All Time) → paper KPIs (Q1) as a new round.
- [ ] SCIM: P2-06 (revoke UI) + P2-07 (role check) BEFORE any flip; Kam's A/B open (default A after).
- [ ] Kam cards: `nexusai-energy-kpis-tec` (default dark) · SCIM A/B (prose, default A).

**Completed (moved off the dashboard 2026-09-01, verified at source):** s11 deploy --0000091 · RD-135 both Entra routes · Sustainability MVP · s12's four delivered items.

**Last sessions (2026-08-24, s1+s2+s3 — all 1.0):** Kam's feedback commission
live on demo in <40 min (RD-116, attachments with full untrusted-upload
standards). Data-provenance report answered his tenant question (dashboard data
= synthetic by design; the address he saw = LAW workspace in tenant bf504a5d,
outside our incomplete recorded set — naming it is his). His link double-check
answered with a fresh LAW-credential probe: workspace ACTIVE and ingesting;
printers stale since 1 June. Isolation audit falsified RD-118's own severity
(AI tools returned real ROW DATA; guarded 1 of 11 sites) → RD-118/120/119
shipped to demo (rev 88, SESSION_SECRET on secretRef); 3h post-fix window:
ZERO real-workspace SP tokens vs 374/30d baseline. RD-107 closed on Kam's
sample-data-stays ruling. HEAD 695aa98 == origin/main (verified).

**s4 (2026-08-25, 1.0):** RD-121 fixed at root cause — discovery now reads the
workspace METADATA endpoint (what exists in schema: 682 tables, relevance
filter → exactly the 3 HpamPrinterLogs_* tables, pinned by a test), full-
retention scan as a warn-logged fallback, `slice(0,50)` gone with a canary;
metadata path asserted inside the RD-118 guard with a non-vacuous control.
Deployed rev 0000089 under the reworded Single-mode condition (rollback tag
named + digest-chained before). ACR: Basic SKU, nothing prunes; **RD-124
found** (soft-delete DISABLED while its policy reads 7 days). RD-122 Done on
Wednesday's ruling; RD-123 filed for the residual. origin/main 458cdfb.

**s9 (2026-08-27 06:10–06:44, 1.0):** Session-Start check repointed to the Container App `/api/health` (CLAUDE.md; the launcher never curled the VM — Wednesday's premise, corrected); **RD-128 / RD-125 / RD-129 → Testing, deployed as `nexusai:1.21.0-rd128-rd125-9cdd5ca` → revision `--rd128125`** (rollback 1.20.0-rd121-e151431 digest-verified first; --0000089 deprovisioned = Single mode observed). Retention sweep now logs `feedback before:2 removed:0` on demo (was a false 0 for the feature's life). Third unfiltered export copy fixed in the same PR; `scripts/jira-query.sh` refuses with SEARCH BLIND on a dead token. 🔴 **RD-130 filed: the hourly health sweeper still probes the dead VM (DEFAULT_URLS[0], HEALTH_SWEEP_URLS unset) → ~2,300 false P1s feeding the SLA + morning-digest reports since 05-22.** RD-131 (Fleet Health CSV omits Drum Status). RD-93: transition to Testing is named "In Review" (id 31) — table in JIRA.md. main b376055. Board 62.

**s10 (2026-08-27 12:45–13:08, 1.0):** RD-130 both halves live — `HEALTH_SWEEP_URLS` set on demo (rev --0000090, same image, one URL by ruling, rollback = unset) and the 03:00Z run observed clean (p1 0 vs three P1s the hours before); `DEFAULT_URLS` loses the dead VM (red-first tests + a control against emptying the list), main 63ba114 / HISTORY fdce1ed, 279/279. 🔴 **Ticket corrected: 683 false-P1 audit entries EXIST (30-day retention pruned the rest), not ~2,300 — rec LEAVE, self-expiring; no Kam decision needed.** RD-131 proposal (shape 1; omission in two functions + a false-negative alert). **Filed: RD-132** (docs still name the dead VM as the live demo) · **RD-133** (readRecent line-cap used as a time window; SLA report fails optimistically) · **RD-134** (no scheduler tests; jest/ESM uuid trap, stub proven). Board 65.

**Open / next (refreshed 2026-08-27 13:1x):**
- [ ] RD-132 / RD-133 / RD-134 — next commission when Kam wants one (none launched by default; RD-133 is the one that mis-reports customer downtime).
- [ ] RD-131 — design call on the ticket (proposal posted), when commissioned.
- [ ] RD-128/125/129/130 in Testing — the browser click path still behind RD-76.
- [ ] RD-76/RD-116 browser eyeball on demo (Kam or my browser seat).
- [ ] 18+ tickets in Testing awaiting review / promotion — only if commissioned.
- [ ] PT-002 / PT-011 secret liveness — needs Datasec dev-tenant admin.

**Completed (moved off the dashboard 2026-08-27, verified at source):** RD-130 both halves (s10) · stale VM Session-Start check repointed (s9) · RD-125 · RD-128 · RD-129 (all Testing, deployed).

**s8 (2026-08-26 17:1x, micro, 1.0):** Kam's ruling (sweep + report only) LIVE: `scripts/feedback-sweep.sh` read-only, wired into CLAUDE.md Session Start + launcher FIRST ACTIONS step 6 (both machine-local — outside the repo; HISTORY says so). First live output: 2 items / 0 unreferenced, controls both ways. **RD-129 filed (Medium): a dead Jira token reads as an EMPTY BOARD, not an error** — `jira issue list` exits 0 with "No result", REST returns 200 `[]`; a negative control alone cannot detect a blind search. Boot is guarded by the /myself probe; mid-session token death + JIRA.md recipes are not. RD-125 comment 36707 (does NOT fix RD-125). main fc3bf0d. Board 60. Next session first: REPOINT the stale `curl https://4.198.168.215` Session-Start check (VM wound down 05-22) at the Container Apps health endpoint (ruled).

**s7 (2026-08-26, micro):** Kam's "ticket both feedback items" → agent HELD: both were delivered by
Kam on 2026-05-08 (91dab1bc, deployed) → recorded as **RD-126 (Bug) / RD-127 (Story), both Done**
for the trail; **RD-128 (Bug, Medium, To Do)** new: Export CSV → Job History ignores Copy/Fax
filters (one of two sites updated in May); other nine export functions not audited. HISTORY
823ff43. Board 59. Feedback→Jira has no mechanism either way → card for Kam.

**s6 (2026-08-26, micro, read-only — Kam's feedback-portal question):** store holds 2 human
items (both 2026-05-07, open, no attachments), none since; corroborates Kam's own look.
**RD-125 filed (Medium):** the retention sweep is a permanent no-op for feedback — the route
file exports no getter, both sweep sites bind `() => []`, the RETENTION_SWEEP audit line
records a false `before:0`; 365-day TTL first due ~May 2027. Portal unaffected. HISTORY
0af9b96. Missing feedback #1: Kam — "skip".

**s5 (2026-08-25 09:2x, 1.0):** Kam ruled RD-124 → ACR soft-delete ENABLED on
nexusaidevacrfa39 (7-day recovery proved with an isolated probe; NOT retroactive —
deletes before 2026-08-24T23:25:12Z stay gone; preview feature) and RD-123 → Single
stays (recorded, no infra change). Both Done. Board 57. origin/main e590b35.

**Open / next (as of 2026-08-26 — superseded above):**
- [ ] Repoint the stale Session-Start reachability check (dead VM → Container Apps health) — ruled 08-26.
- [ ] RD-129 dead-token-reads-empty (Medium) — fix when commissioned (mid-session + JIRA.md recipes).
- [ ] RD-128 CSV export ignores Copy/Fax filters (Medium) — one-line fix + audit the other nine export functions, when commissioned.
- [ ] RD-125 retention-sweep no-op (Medium) — fix when commissioned.
- [ ] Feedback→Jira mechanism — Kam's card (nexusai-feedback-loop-mechanism).
- [ ] RD-121 in Testing — promote once a customer-shaped workspace exercises
      the metadata path (demo blocks it by design under SYNTHETIC_DEMO_FEED).
- [ ] RD-76/RD-116 browser eyeball on demo (Kam or my browser seat) — the one
      remaining independent leg on the feedback widget + AI-path fixes.
- [ ] 18+ tickets in Testing awaiting review / promotion — only if
      commissioned.
- [ ] PT-002 / PT-011 secret liveness still unverified — needs Datasec
      dev-tenant admin (same blocker as RD-54/55).

**Completed (moved off the dashboard 2026-08-25, verified by my Jira read):** RD-123 Done ·
RD-124 Done · ACR tag-pruning check done (s4: nothing prunes at Basic SKU).

**Completed (moved off the dashboard 2026-08-24, verified at source):**
RD-107 Done (Kam's ruling, comment 36681) · key-sprawl card ruled RECORD ONLY
by Kam 10:54 (RD-111 annotated — "not a licence for a later session to tidy") ·
restore-path card ruled status-quo (synthetic is the standing state BY RULING).

**Blockers:** none agent-side.

**Notes for Wednesday:** Deploy condition for this app (Single revision mode):
rollback = redeploy by image tag, named BEFORE deploy, tag verified in ACR —
"previous revision retained" is unsatisfiable here (RD-122). The
`storage/` key-sprawl set is recorded, never touched, per Kam's record-only
ruling. Jira gotcha: their JIRA_SITE env var is scheme-less — prefix https://
or CloudFront 301s. tools.js executor logging (AC-3) closes history forward
only — nothing can establish whether the AI tools ever reached the real
workspace before 2026-08-24.
