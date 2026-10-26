From Tuesday, Datasec / HPSM-POC, to seat Datasec/HPSM-POC-H38 (brief B759). ADDENDUM-1. It CHANGES D-1 and widens your lane by ONE file. Everything else in your brief stands.

**What changed:** the product owner made HP's digital design system available to Tuesday after your launch. Tuesday read its colour primitives and measured HP's own design-system site in a browser: its primary links and primary button background are `#024AD8`, its body text `#1A1A1A`, its page `#F5F5F5`. The HP design-system material is access-controlled: you receive only the values below. Never search for, fetch or quote it; no HP design-system name, URL or token name goes into code, comments, tests or the commit message. Say "the HP brand palette" if you need to name it.

**Your lane gains exactly one file: `web/src/styles/brand.css`** (its header says it is the ONE file to swap when branding is decided). Change ONLY these values; every other line, the comment block excepted, stays byte-equal:

| Variable | Now | New |
|---|---|---|
| `--brand-primary` | `#1d4f91` | `#024ad8` |
| `--brand-primary-hover` | `#163d71` | `#103fb2` |
| `--brand-primary-subtle` | `#e8eff9` | `#e4eefa` |
| `--brand-on-primary` | `#ffffff` | `#ffffff` (unchanged) |
| `--brand-accent` | `#0f766e` | `#356373` |

Comment: replace "Branding is UNDECIDED ... neutral, professional placeholder theme" with plain words saying the brand colours now follow the HP brand palette (primary blue, its hover and subtle tints, and a blue-grey accent), that the fonts are unchanged on purpose (a brand web font would be a new download), and that the neutral tokens in tokens.css are unchanged. No person's name, no id.

**NOT changed (hold):** `--brand-name`, `--brand-font-sans`, `--brand-font-mono`, everything in `tokens.css`, any font, any component class. No new variable.

**Tests:** `src/design/contrast.test.ts` must stay green with NO edit to its thresholds or pairs. If it fails, print the failing pair and its ratio and STOP with that as the question; never pick another colour yourself. A test that pins the OLD brand hex values may be updated (class (c) of your lane): list each assertion old/new in STATUS. Add one unit row that pins the five new values as read from `brand.css` (RED at the base, green after) and one mutant (m10: `--brand-primary` back to `#1d4f91`, the row turns red).

**Performance:** the hex values are the same length, so CSS bytes must be EQUAL to the base. Your existing CSS predicate (delta <= 0) applies unchanged.

**Screenshots:** your existing set now shows both changes. In STATUS, say per page whether any text or control looks wrong in the new blue, and quote the contrast test's printed ratios for the primary pairs.

**Commit:** still ONE commit if you can. The message also says the brand colours now follow the HP brand palette, with no font change. The words "no colour changed" in your brief's commit text no longer apply; "no font, word, proxy or dependency changed" still does.

**Order:** do this inside THE WORK 6, after the logo. Clock unchanged: target READY 23:30, hard stop 01:30. If the colour change alone would make you miss 23:30, finish the logo first and ask, last line `STOPPED: NEEDS TUESDAY logo READY without the colours, or wait?`.

Record this addendum under Corrections (one line) and continue.
