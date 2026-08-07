---
date: 2026-08-07
type: action-plan
for: Kam
status: awaiting-approval
subject: Datasec / Vision — Quoting Tool (Phase 1) sub-project
sources_read:
  - "Meeting transcript 2026-08-06 15:07 (32 min, audio) — read in full"
  - "Meeting recording 2026-08-06 15:39 (56 min, screen walkthrough) — transcribed locally, in progress at time of writing"
  - "Will's handover email (PDF), 2026-08-06 19:09"
  - "HANDOVER/00–05 docs + READ-THIS-FIRST + CLAUDE.md + README (tool v2.06)"
  - "Vision Sales Portal package.json + 5_Project_History/history.md (newest entry 2026-08-04)"
---

# Vision Quoting Tool — Phase 1 action plan (proposed)

## BLUF

**The maths is not broken in the way it looks. The pricing engine is sound; the
defect is a currency-labelling bug that Will's own dev already diagnosed
(WIL-155, High) with a recommended fix.** The bigger and less obvious problem is
that the tool's professional-services model **does not implement the rule Will
describes as the one he wants** — and that gap, not the currency bug, is why the
channel cannot use it on the deal driving the deadline.

**Phase 1 is genuinely small.** Everything Kam described in the meeting —
OTP login, live-calculating quote, emailed immutable PDF — is achievable by
reusing infrastructure the Vision Sales Portal already has in production.

**My primary recommendation: build it as its OWN app in its OWN resource group,
not inside the live portal.** Reasons in §4.

## Recommendation — six decisions needed from Kam

1. **Hosting shape:** separate App Service in a new resource group, same
   subscription. **Recommended** over adding a route to the live portal.
2. **The PS model:** resolve the contradiction between the tool's tiering and
   Will's stated rule (§2). **Recommended:** adopt Will's per-device rule with
   the tier table as the floor, and get Will to confirm the thresholds.
3. **PS and currency:** confirm PS rates stay OUT of FX conversion (§3). This
   contradicts "make currency conversion always live" if read literally.
4. **"No Pro Services" checkbox in base view:** this reverses a deliberate
   decision (some markets mandate PS). **Recommended:** implement as asked, but
   keep the market-dependent warning text.
5. **Offline dies.** The single-file offline architecture is the reason for most
   of Will's design. A hosted, login-gated tool cannot be offline.
   **Recommended:** accept, and tell Will explicitly rather than let him discover it.
6. **Deadline:** ABT's Rio Tinto extension lands ~**18 August**. Confirm whether
   Phase 1 is meant to serve that deal, because it changes sequencing.

---

## 0. ADDED AFTER THE CODE REVIEW — the defect nobody had found

**Professional services are FX-converted TWICE.** This is not WIL-155, is not in
any handover document, and is larger than the bug Will's dev found. **Verified
by me directly in the source, not taken from the review.**

The chain, three lines from three different places:

1. `applyPsvRates()` (L2155-2172) writes **local currency** into the price field:
   `basic = CONFIG.services.basic.defaultPrice * rate` → `$("price-basic").value`.
2. `calc()` (L1261) reads that field **as USD** into `svcTotal`.
3. `render()` (L1324-1326) prints `fmt(c.svcTotal)`, and `fmt()` multiplies by
   the rate **again**.

Net: `PS = USD × rate × rate`. The grand total is worse still —
`fmt(licenceTotal + svcTotal)` **adds a USD number to a local-currency number**
and converts the sum.

| Currency | rate | Basic tier shows | should show | error |
|---|---|---|---|---|
| AUD | 1.55 | 3,363.50 | 2,170.00 | **+1,193.50** |
| NZD | 1.67 | 3,904.46 | 2,338.00 | +1,566.46 |
| SGD | 1.35 | 2,551.50 | 1,890.00 | +661.50 |
| **EUR** | 0.93 | 1,210.86 | 1,302.00 | **−91.14 (under-charged)** |
| **GBP** | 0.79 | 873.74 | 1,106.00 | **−232.26 (under-charged)** |
| **DKK** | 6.93 | 67,234.86 | 9,702.00 | **+57,532.86** |

**Two things make this urgent rather than merely wrong:**

1. **It defeats the feature it was built for.** Regional PS rates exist
   *precisely* so service pricing does not track FX (Will: *"1.4181 on $280 an
   hour ain't going to fly in Australia"*). An AM who saves a genuine A$2,500
   rate gets **A$3,875** on the quote.
2. **EUR and GBP are UNDER-stated.** Every euro or sterling quote has
   under-charged professional services by 7–21%. That is margin already given
   away if any such quote has been issued.

**It is a regression, with evidence:** the shipped reference PDF
`tool/docs/…AUD.pdf` (June build, before `applyPsvRates` existed) shows PS Basic
at A$2,325 = US$1,500 × 1.55 — a single, correct conversion. The double
conversion arrived with the regional-rates feature.

**Commercial action, not a code action:** someone needs to establish which
non-USD quotes have been issued since that feature shipped. I cannot determine
that — nothing is persisted, quotes exist only as emailed PDFs.

**Root cause, and why it matters for the rebuild:** PS pricing does not live in
`calc()`. It lives **in the DOM**, written by three functions that disagree about
units — `applyPsvRates()` writes local currency, `applyServiceRule()` (L2007)
writes raw USD, and `applyPoc()` rewrites quantities. One input, three owners,
three unit conventions. Seven of the nine confirmed defects are symptoms of the
same design: *the input element is the state store.*

### Other confirmed defects from the code review

- **PoC charges nothing when the tier was manually overridden** (L1968-1976):
  `applyPoc()` keys off device count, not the selected radio. Choose Advanced at
  8 devices with PoC on → the second engagement is silently not charged,
  **US$2,100 missing**.
- **Editing device count or WorkPath-Ready silently resets PS quantities to 1**
  (L1977-1982) — a deliberately-set quantity of 3 reverts with no warning.
- **Device count overrides a deliberate PS selection** (L1996-1997): choose "No
  professional services", then touch the device field, and PS silently
  reappears in the total.
- **Saving PS rates does not refresh the grand total** — setting `.value` in JS
  fires no event, so `render()` never runs; line items change, total goes stale.
- **PS converts at the seed rate while licences use the live rate** — the live
  fetch calls `render()` but never `applyPsvRates()`.
- **"Both" print mode emits two different quote numbers**, contradicting the
  documented rule that the pages share one.
- **The printed quote never states the FX rate** — `fxLine` is computed at L1448
  and never interpolated, though the UI promises "the printed quote records the
  rate used". A regression: the June PDF carried it.
- **166 lines of dead code** (`buildQuote()`, L1592-1757) that has already
  drifted from the live renderer. Anyone fixing the maths is even money to fix
  the dead copy.

**This changes stage 1 of the plan below:** the currency work is no longer a
one-bug fix. The honest scope is *extract pricing out of the DOM into a single
pure function that takes state and returns a priced quote in one explicit
currency* — which is the only way a unit error becomes a testable assertion
rather than a screen-reading exercise. There are currently **no tests at all**.

---

## 1. The maths defect Will's dev found (WIL-155), precisely

**WIL-155 (High, open).** The Custom Pricing Override fields hold **USD** but are
**labelled with the selected currency**. `cpState` is USD; `cpSyncFrom()` reads
and writes the four spinners as raw USD; `renderCustom()` labels the group with
the selected currency and pushes the totals through `fmt()`, which multiplies by
the FX rate. So the fields say AUD, hold USD, and the totals below are converted
from a number the user believes is already converted.

Documented reproduction (1 device, 3-year term, Mix & Match + 3 add-ons, AUD):

| Field | Shows | Should be |
|---|---|---|
| Annual charge | A$341.62 | A$240.90 |
| 3-year total | A$1,024.86 | A$722.70 |

The ratio is the AUD rate in force (~1.418). Will's recommendation is **Option B
— make the maths honour the label** (convert on input, convert back on write,
keep `cpState` USD internally), rather than relabelling the fields to USD. His
handover explicitly warns: **do not half-fix it.**

**WIL-54** is the same class: the per-app price chips are written with a
hardcoded `"$"` and bypass `fmt()` entirely, so they stay USD in every currency.
Will wants both fixed together under one rule — *every monetary figure on screen
states or implies its currency, and that statement is true.*

**One further defect I derived that no document lists:** the /device/year spinner
appears to be computed from the **rounded** day figure (0.66 × 365 = 240.90)
while the annual charge is computed from the unrounded monthly (20.08 × 12 =
240.96). Fixing the currency bug alone leaves a ~6c/device/year mismatch between
the spinner chain and the totals. Whoever takes this needs a stated rounding
policy — there is none anywhere in the codebase or the docs.

**What this means commercially:** the list prices, the SKU matrix and the licence
formula are not implicated. If Kam tells Will "the maths is wrong", the honest
version is "**the currency presentation is wrong, and the PS model is
incomplete**".

---

## 2. The real gap — professional services

The tool today, from `applyServiceRule()`:

| Devices | Behaviour |
|---|---|
| 1–10 | Basic (4 hr) auto-selected |
| 11–100 | Advanced (8 hr) auto-selected, Basic disabled |
| **>100** | **POA — price cleared and locked, quote prints "POA"** |

What Will describes in the meeting as the rule he actually wants:

- **0.1 hour (6 minutes) per device** as the scoping unit. His words: *"over 350
  devices, it's actually 35 hours."*
- Applied **beyond a threshold** — he says *"especially if it's over 100
  machines"* and separately *"after you go beyond, say, 50 devices"*. **The
  threshold is unsettled in his own telling and must be confirmed.**
- **Rounded up to whole days.** His worked example: 374 devices → 37.4 hours →
  *"that's 4.74 days. We're rounded up to the day, which is five days."*
  (His 4.74 is a slip — 37.4/8 = 4.675 — but both round to 5. The spec should be
  `days = ceil(hours / 8)`.)
- Below that, the existing floor stands: *"if it's less than 10 machines, we
  charge half a day."*

**The contradiction that matters:** the tool prints **POA** above 100 devices —
exactly the range of the 374-device ABT deal — while Will's method produces a
concrete five days. He says it himself: *"my tool doesn't really do that because
it asks them too many questions that they don't know the answers to."* This is
the single highest-value fix in Phase 1 and it is a **rules** change, not a bug.

**PoC.** Currently: a second unit of the PS SKU (not more hours) — deliberate,
because a PoC is a separate engagement — plus 1 hour of WorkPath onboarding,
suppressed if the customer supplies their own onboarded devices; disabled below
5 devices. In the meeting Will frames it as *"you're going to pay for the
installation twice"* — same intent, so keep the existing behaviour.

**WorkPath onboarding.** `nonReady = devices − workpathReady`;
`hours = ceil(nonReady × 0.1)`. Note this already uses the 0.1/device unit — the
same number Will wants applied to installation generally.

---

## 3. Currency — the answer to "can you do auto conversion?"

**Yes, and it already exists.** Live lookup against three key-less providers
(frankfurter.dev, frankfurter.app, open.er-api.com), 6-second timeout each,
falling back to a built-in seed table, with the rate always hand-editable and a
provenance note (`anchor` / `live` / `seed` / `manual`). Seven currencies: USD,
AUD, EUR, GBP, NZD, SGD, DKK. A manual rate is never overwritten by a background
fetch — deliberate, for an AM holding a finance-issued contract rate.

So the work is **moving the selector under the pricing tile and making live the
default**, not building conversion.

**The trap in "make it always live":** professional-services rates are
deliberately **excluded** from FX conversion. Will, in the meeting: *"1.4181 on
$280 an hour ain't going to fly in Australia"* — service delivery is locally
resourced, so an AUD PS rate is a real rate, not a converted one. Per-currency PS
rates are stored in settings and override conversion. Reading "always live" as
"convert everything" would silently reverse that, and the handover warns this
area *"took four attempts to settle"* and *"broke four different ways"*.

Related known quirk: the settings panel shows un-overridden PS defaults at the
**seed** rate while the quote converts at the in-force rate, so the two can
disagree. Not currently ticketed; worth folding into the currency pass.

---

## 4. Hosting — recommendation and reasoning

Kam's instruction: hosted on the `kreiser.org@me.com` subscription. That is the
agent-controllable tenant `d500ebad-…`, which also contains **Vision Sales
Portal's live production site, database and key vault** in
`datasec-sales-portal-rg`.

**Recommended: a new App Service in a NEW resource group, not the prod one.**

- **The auth models are incompatible in risk terms.** The portal has real sales
  accounts (bcrypt + sessions). The quoting tool is deliberately open — *"anyone
  off the street can log in, couldn't care less."* Adding a public passwordless
  path into the app that holds the portal's accounts widens its blast radius for
  no benefit.
- **Deploy cadence.** The portal deploys manually by zip and is production;
  Phase 1 will iterate daily with Will. Coupling them means every quoting-tool
  tweak is a production deploy.
- **Never-touch-prod applies in full** inside this subscription — that resource
  group is production despite the tenant being agent-workable.

**But reuse the portal's proven pieces**, which is where the real time saving is.
It already runs, in production, on Node 20:

| Need | Already in the portal |
|---|---|
| Send OTP emails, email the quote | `@azure/communication-email` |
| Generate the immutable quote PDF | `pdfkit` |
| Sessions | `express-session` + `connect-pg-simple` |
| Storage for quote records + real quote numbers | `pg` (Postgres) |
| Rate-limit the OTP endpoint | `express-rate-limit` |
| Collateral for "Extranet Lite" | `seed:collateral` script exists |

**Quote numbering should become authoritative.** Today it is `DSQ-YYYYMMDD-NNN`
with NNN a **random 100–999**, regenerated on every print, never registered —
roughly a 1-in-900 same-day collision chance. The moment we email a quote as a
binding artefact, that has to become a database sequence.

---

## 5. Simplification — Kam's list against what the tool does

| Kam's ask | Current state | Note |
|---|---|---|
| Remove email, phone, unnecessary fields | Salesperson **name, email and phone are mandatory** — print is blocked without them | Consistent with the meeting: we already know the user's email from OTP login, so we can email the quote without asking |
| Client name obviously optional | **Mandatory** today | Meeting: default it to "Client X" |
| First section = devices + term, PoC with WorkPath under it | Devices, WorkPath Ready and PoC exist but are laid out differently | Mostly re-layout, low risk |
| Currency selector under pricing tile, always live | Exists, in its own panel, live-on-change | Move + default; see §3 caveat |
| Keep application selection tile as is | — | No change |
| Hide full PS tile under pro view; base view calculates from rules | PS panel is always visible and manual | Depends on §2 being settled first |
| "Custom PS Rates" button from settings | Exists in the settings drawer | Surface it, don't rebuild |
| "No Pro Services" checkbox + charged-as-above message | Exists but is **settings-gated** because some markets mandate PS | Decision 4 |

---

## 6. Proposed sequence

**Stage 0 — settle the rules with Will (blocking, ~1 session).** The PS model
(§2), the threshold, POA-above-100, and confirmation that PS stays out of FX.
Nothing should be built before this; the whole complaint is that the rules are
wrong, and building against unsettled rules just moves the error.

**Stage 1 — fix the maths in the existing single file.** WIL-155 Option B and
WIL-54 together, plus a stated rounding policy. This is small, self-contained,
and immediately useful to Will **even if nothing else ships** — it makes his
current tool correct. Deliver it as the same single HTML file he uses today.

**Stage 2 — implement the corrected PS model** in the same file, with a small
regression pack of worked examples (10, 15, 50, 100, 374 devices; with and
without PoC; with and without WorkPath-ready) checked against Will's own numbers.

**Stage 3 — the hosted Phase 1 app:** new resource group, OTP login, the tool as
a page, live pricing panel, emailed immutable PDF quote, authoritative quote
numbers, and "Extranet Lite" as a collateral list.

**Stage 4 — Phase 2** (Kam's framing): fine-tuning and the main Vision sales tool.

Stages 1 and 2 deliberately land **before** the hosting work, so the deal-facing
value arrives first and the ABT deadline is not gated on infrastructure.

---

## 7. Open questions for Will (not for Kam)

1. The PS threshold: 50 devices or 100?
2. Above 100 devices — keep POA, or produce the computed day count? His method
   yields a number; his tool refuses to.
3. Is the 8-hour day the right divisor for the round-up-to-days rule?
4. Does the half-day floor below 10 devices survive the per-device rule?
5. Hourly rate must exceed day-rate ÷ 8 (his lunch-break point) — should the tool
   enforce that when custom PS rates are entered?
6. Does offline still matter at all once login is mandatory?

## 8. Things a rebuild must not accidentally reverse

- The internal margin note must **never** reach a customer document.
- "% from standard" never compounds.
- PoC = a second unit of the SKU, not more hours.
- WorkPath Ready = compatible **and** enabled **and** onboarded to Command Center.
- Per-currency PS rates override FX conversion.
- A manual FX rate is never overwritten by a background fetch.
- Page 2 sections stay a modular array.

## 9. Provenance note

There is **no commit history before v1.81** — the tool was built in Claude Chat
sessions and imported to git at that point. The derivation of the base prices
(5.00 / 3.50 / 20.00 per device per month) is not in any tracked history and is
explained only as "HP commercial policy". If the complaint ever turns out to be
about list price rather than currency or PS, **there is no audit trail to fall
back on** and it will have to be re-derived with Will.
