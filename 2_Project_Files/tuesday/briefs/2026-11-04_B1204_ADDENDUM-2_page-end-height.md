B1204 ADDENDUM-2 (read at your next step boundary; it ADDS one item to your scope; where it and the kit or ADDENDUM-1 differ, this file wins) -- from Tuesday s241

**Why:** main `a8497578` (pull request 282) went to UAT at 08:47 today. The UAT deploy check (B1258, `1_Project_Definition/Briefs/2026-11-04_B1258_STATUS.md` lines 157, 197 and 264; read them) measured short pages ending **136 px sooner** than yesterday's site `69338b64`: 22 of 56 cells, every `/engagements` cell at 1024, 1280 and 1440 wide by 700 and 800 high, menu open AND collapsed, Partner and Admin. The product owner had accepted 64 px, and that figure was measured against an earlier draft, not the live site. At 2026-11-04 09:33:22 AEDT he ruled **"Keep UAT and fix the height"**. The extra space comes from the menu panel in `web/src/components/shell/Sidebar.tsx` line 68: `lg:h-[calc(100dvh-4.25rem-4px)]` and `lg:-mb-16`. That is YOUR file (your kit and ADDENDUM-1 :23), so the fix is yours. No other seat touches it.

**The added property (binding; test it with a red-first row and a plant):** at 1024 px wide and up, on a page whose content is no taller than the menu (Engagements is the measured case), the page's `document.scrollingElement.scrollHeight` at your head is **no more than 64 px less** than at `69338b64` (yesterday's UAT), in every cell of the B1258 frame: `/engagements` and `/home`, Partner and Admin, 1024/1280/1440 x 700/800, menu open and collapsed. Smaller than 64 px, or equal height, is better. AND what PR 282 fixed must not regress, in the same cells plus 420 high:
- Shift+Tab up the open menu from the page's end moves the page 0 times (B1258 measured 0 of 69 at a8497578);
- the footer text is never under the open menu (0 covered);
- the focus ring of every menu item stays visible and uncut (as the round-4 gate measured);
- the band under the menu at the page's end stays at or below 72 px.

These rows go in YOUR spec (`web/e2e/shell-sidebar.spec.ts` is yours), red at a8497578 for the height row and green at your head. The plant that restores `lg:-mb-16` (or the old height expression) must turn the height row red. The B1258 instrument is `.tools/b1258/kit/ring1258.cjs`: READ it as text for the method, never run it from that folder (copy into `.tools/b1204/` if you use it). It is a finished seat's tree.

**How:** your choice of mechanism, CSS only (no JavaScript for layout), inside the files you already own. If the height cannot meet 64 px without breaking the Shift+Tab property, STOP: `STOPPED: NEEDS TUESDAY page height vs focus ring`, with both measured figures. Do not trade one for the other silently.

**Your existing five re-calibrated expanded-walk rows:** if this change moves their flip points again, re-sweep them. In STATUS, list every EXISTING row whose assertion you changed, with the old value, the new value, why, and the plant that still turns it red. Your gate (tier 1, Opus) will judge each one as a possible weakening.

**Unchanged:** everything else in your kit and ADDENDUM-1. One commit or more on your own branch, plain push, no PR, nothing deployed. Record this addendum by name under Corrections. Your READY line names it.
