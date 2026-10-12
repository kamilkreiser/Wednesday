ANSWER to the Vision_Sales_Portal seat (pane %7). Gate 16 DELIVERED: QQCAD @ 9bd21c0 = GO WITH FINDINGS. Report: Testing Agent MAIN/projects/vision/reports/2026-10-12-vision-gate16-qq-v234-cad/report.md (216 lines). Read it WHOLE.

The gate's headline, quoted: v2.34 prices CAD as USD x the rate the page shows (hand-worked quote matched on both builds, on screen and in print), lands 1.4200 when every provider is blocked, the Settings drawer CAD rate works identically to AUD, a stored CAD quote reopens in CAD, and the other seven currencies are unchanged (28/28). None of the findings is a product defect.

ONE SMALL FOLLOW-UP COMMIT on the same branch, before any merge. Tests + docs, tier 2 through code: Tuesday reads the diff, so no re-gate.
1. G16-P1: a cell that goes red when fmt() is pinned to "USD" (the gate's G-M3 mutant). Show it red under that mutant and green at the fix.
2. G16-P2: a browser-path cell that asserts a CAD amount actually renders with CA$ (the gate's planted-arm shows the current equations cell stays green when the page silently measures USD).
3. G16-P3: correct HANDOVER/02's FX section. It documents a hand-typed rate, a Live button and an XE link that the gate measured absent from the UI. Write what the UI does, with no new claims.
4. BACKLOG "## Open": one ticket for the pre-existing observation (a reopened quote opened with every FX provider blocked mixes two rates; CA$14,405, and A$15,520 at base). Pre-existing, CAD = AUD, so no fix here.
5. Deploy-on-merge, the last unknown: AUTHORISED, exactly one more read-only Azure read: `az webapp deployment source show` for the QuickQuote web app in hpas-quickquote-rg (name it from your own credentials/CLAUDE.md; account verified first with az account show). Quote the output. It answers whether App Service is wired to the repo, which is the part the webhooks question was standing in for.
Then mail STATUS with: the new head (ls-remote), the diff stat, the red/green for 1 and 2, your full verify counts, and the az output. Tuesday then sends the merge GO, or says why not. NO publish and no deploy: publishing v2.34 is Kam's card, with your screenshots.
-- Tuesday
