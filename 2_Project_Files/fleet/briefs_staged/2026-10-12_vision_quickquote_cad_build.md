# BLUF — Datasec/Vision_Sales_Portal: BUILD QuickQuote v2.34, CAD currency. Kam ruled the card quickquote-cad-currency-1012 = (a) on the live board at 2026-10-12 14:31:35, verbatim: "Decision quickquote-cad-currency-1012: a — Add CAD, priced like the other non-regional currencies". Build it red-first, run your own verify, then send READY FOR QA (tier 1: customer-shown pricing). Nothing is published or deployed: publishing is a separate Kam decision, and he sees screenshots first. Send a PLAN CONFIRMATION before any edit.

## WHAT (a) MEANS, as the card stated it (option a's detail, verbatim)
"Live FX as now. Offline fallback seed 1.42 CAD per USD (ECB 9 Oct). Professional services = USD rate card × live FX. Built as v2.34 with red-first cells, through the QA gate. Publishing comes back to you."

## READ FIRST (Vision_Sales_Portal folder)
1. Your previous seat's plan mail and wrap (this inbox, 2026-10-12 02:13Z and 02:18Z, read WHOLE). They hold the exact files and the five proposed cells.
2. `1_Project_Definition/CLARIFICATIONS.md` C-13. Record this ruling as the next C-number, and mail it back.
3. QuickQuote `CLAUDE.md`, `HANDOVER/02-business-rules.md` (Currency and FX), and `index.html` around :1261-1268 and :1571-1579 (the two selects), :1803 (CONFIG.fxSeeds), :1921-1936 (psRatesFor) and :1724 (toolVersion). These are your predecessor's line reads, so re-read them at the tip.

## MEASURED (relayed from your predecessor; re-read before relying)
- QuickQuote main e408904, toolVersion "2.33", clean, 0/0 against origin.
- CAD is absent from both selects and from fxSeeds. HANDOVER/02:31 lists seven currencies.
- ECB 2026-10-09: USD->CAD 1.4226 (api.frankfurter.dev). The seed per Kam's (a) is 1.42.
- Branch backlog/qq-aud-seed-2026-10-12 @ e1a865c (the AUD-seed BACKLOG entry) is pushed and NOT merged. Leave it out of this build.

## BUILD (as your predecessor proposed, now ruled)
- Files: one CAD <option> in each of the two selects; a CAD 1.42 entry in fxSeeds; the currency line in HANDOVER/02; toolVersion "2.34" in the same commit. The pricing engine is untouched.
- Red-first cells (red on e408904, green after):
  1. CAD is offered in both selects and has a seed.
  2. A CAD quote's every figure equals USD × rate at a fixed hand-worked rate.
  3. FX falls back to the CAD seed when every provider is stubbed to fail.
  4. A stored quote saved in CAD reopens in CAD.
  5. test:print and test:xlsx on a CAD shape.
- At least one mutant per cell family must bite. Run your own full verify and quote its VERDICT line.
- Screenshots: the currency select open, and one CAD quote in simple mode, light and dark. These go to Kam before any publish.
- READY FOR QA with PRIOR WORK, NOT TESTED, the branch + head (ls-remote) and the screenshot paths.

## HOLDS
- PRODUCTION: no publish, no deploy, no Azure change, no production write. No merge to QuickQuote main until Tuesday's GO after the gate. Before the GO, state whether a merge to QuickQuote main triggers any deploy workflow, and how you know.
- No reply to John Spears or any author. Kam tells him.
- Style: QuickQuote's own tokens only. PRIOR-WORK CHECK. Never delete. Every factual sentence names its instrument, or says "unmeasured".
- The portal, ATTIO and the rest of the backlog stay paused (C-13).

## RULED BY KAM, NOT YET IN AN ARTEFACT
- quickquote-cad-currency-1012 = (a), 2026-10-12 14:31:35 (verbatim above). Record it as a C-number and mail the number back.

## RULED BY TUESDAY FOR THIS PROJECT, STILL OPERATIVE
- The 2026-09-29 pause stands except for QuickQuote feedback work (C-13). Tier 1 for this build.

PROVENANCE:
- Kam's ruling | live board via /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/tools/kam_rulings_today.sh (14:31 row) | read 2026-10-12
- option (a) text | /Volumes/KK_T9_External_HDD/TUESDAY/0_Brain/dashboard/data/decisions.json card quickquote-cad-currency-1012 (written by Tuesday) | read 2026-10-12
- file and line reads, e408904, ECB rate | the previous Vision seat's plan mail, datasec-vision@ / tuesday-agent@ 2026-10-12T02:13Z (relayed, not re-derived) | read 2026-10-12

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-12 14:35

## PLAN CONFIRMATION
Mail `[Datasec/Vision_Sales_Portal -> Tuesday] QUESTION: plan confirmation` with your seat identity (pane id, cockpit name, claude pid), what you read, the files and cells at the tip, the deploy-on-merge answer, and any launcher preflight warnings VERBATIM. Then wait. Your wake is Tuesday's mail plus a tap.
-- Tuesday
