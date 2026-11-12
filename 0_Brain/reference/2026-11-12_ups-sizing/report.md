# UPS sizing for Mac mini + Mac Studio(s) (AU) - 2026-11-12

## BLUF
- Kam's reference unit (CyberPower Value line, B084WX3GRL) could NOT be verified: Amazon AU returned HTTP 503. The AU "Value Pro 1600VA" is VP1600ELCD: 960 W, SIMULATED sine on battery, 4 AU outlets (3 battery-backed). A cheap, fine fit for ONE Studio + mini on load, but not pure sine.
- Pick now (mini + one Studio): CyberPower PFC Sinewave CP1500EPFCLCDa-AU (1500 VA / 900 W, pure sine, 6 AU outlets), AU$400-525. Worst-case load ~440 W = ~49% of 900 W.
- Pick later (two M3 Ultra): do not rely on one 1500 VA. Worst case ~705 W (78% of 900 W). Two separate pure-sine 1500 VA units (one Studio each, mini on either), or a 2-3 kVA unit. Two units is my judgement: independent failure, and each Studio only needs one.
- Pure sine for Apple Silicon: no Apple requirement found. CyberPower states active-PFC gear "requires Pure Sine Wave" (vendor claim); forum evidence is anecdotal and mixed. Treat as conservative judgement.
- Note: Apple never made an M3 Mac mini (only M1/M2/M4 per Apple's tables). Kam's mini is probably M2 or M4; check About This Mac.

## 1. Apple power figures (SOURCED, wall power incl. losses)
| Model | Idle | Max | Source |
|---|---|---|---|
| Mac Studio 2025 M3 Ultra | 9 W | 270 W | https://support.apple.com/en-us/102027 |
| Mac Studio 2025 M4 Max | 6 W | 145 W | https://support.apple.com/en-us/102027 |
| Mac Studio 2023 M2 Ultra | 10 W | 295 W | https://support.apple.com/en-us/102027 |
| Mac mini 2024 M4 (16GB) | 4 W | 65 W | https://support.apple.com/103253 |
| Mac mini 2024 M4 Pro | 5 W | 140 W | https://support.apple.com/103253 |
| Mac mini 2023 M2 / M2 Pro | 7 / 7 W | 50 / 100 W | https://support.apple.com/103253 |
Max = compute-intensive test app (same page). Apple tech-specs "maximum continuous power" for Mac mini 2024 is 155 W (M4 and M4 Pro not separated): https://support.apple.com/121555 . I did not find the Studio's equivalent spec-page number; I use the wall figures above.

## 2. Sizing (JUDGEMENT on SOURCED inputs)
Rules: size so worst-case load <= ~60-70% of the UPS WATT rating (battery ageing, surge headroom). VA needed = W / UPS power factor (these units: 0.6 = 900 W/1500 VA, 960 W/1600 VA). External NVMe assumed 10 W, monitor 40 W (Kam's figure; estimates, not measured).
| Scenario | Worst-case W (all at max) | Min UPS W at 70% | at 60% |
|---|---|---|---|
| (a) mini (155 W spec) + 1 Studio M3 Ultra (270) + SSD (10) | 435 W | 620 W | 725 W |
| (a) + 40 W monitor | 475 W | 680 W | 790 W |
| (b) mini + 2 M3 Ultra + SSD | 705 W | 1010 W | 1175 W |
| (b) + monitor | 745 W | 1065 W | 1240 W |
Real draw will be far below worst case (idle total ~25 W), so (a) fits 900-960 W comfortably. (b) exceeds a 900 W unit's 70% line, so needs ~1.5 kW class or a split.
Runtime (vendor charts, SOURCED): VP1600ELCD 11 min at half load (~480 W), 2 min at full: https://www.cyberpower.com/au/en/product/sku/VP1600ELCD . CP1600EPFCLCD (1000 W) 9.7 min half / 2.6 min full: https://store.area9.com.au/products/cyberpower-pfc-sinewave-series-1600va-1000w-2101054 . So at ~435 W expect roughly 10 min; at real idle loads much longer, but no vendor figure for that. Enough for a clean shutdown, not for riding out outages.

## 3. Kam's reference: CyberPower Value / VP1600ELCD
Amazon AU B084WX3GRL: fetch failed (503); could not confirm the ASIN maps to this model or its Amazon price. Search found no match either. Manufacturer AU page (https://www.cyberpower.com/au/en/product/sku/VP1600ELCD): VP1600ELCD, 1600 VA / 960 W, simulated sine on battery, 4 AU outlets (3 battery+surge, 1 surge only), AVR boost+buck, 1 HID-compliant USB port. Price not on that page. Search-snippet prices (not live-fetched; read 2026-11-12): PB Tech ~AU$316.69, The Tech Geeks AU$315.70, Computer Alliance $289, Officeworks $419 (see search listing https://officeworks.com.au/shop/officeworks/p/cyberpower-value-pro-ups-tower-1600va-960w-vp1600elcd).

## 4. Alternatives (AU$ from search snippets 2026-11-12, inc GST unless noted; confirm before buying)
| Model | VA/W | Waveform | Outlets | USB HID/macOS | Price | URL |
|---|---|---|---|---|---|---|
| CyberPower CP1500EPFCLCDa-AU | 1500/900 | Pure sine | 6 AU | USB present; macOS not verified by me | $400-$576 (Austin $469, Spotit $400, Acquireit $576) | https://austin.net.au/products/cyberpower-pfc-sinewave-series-1500va-900w-10a-tower-ups-with-lcd |
| CyberPower CP1600EPFCLCD (area9 page) | 1600/1000 | Pure sine | page says "2 x UK, 4 x C13" (not AU sockets, needs adaptors) | USB-A + USB-C | $509.30 | https://store.area9.com.au/products/cyberpower-pfc-sinewave-series-1600va-1000w-2101054 |
| APC BR1600MI | 1600/960 | Stepped approx. sine | 8 x C13 (IEC leads) | USB, not verified | $692-$781 | https://www.pbtech.com/au/product/UPSAPC1600/APC-Back-UPS-Pro-BR-1600VA--960W-8-Outlets-AVR-LCD |
| APC BR1500MS2 (Newegg AU, ships from Canada) | 1500/900 | Sine | not stated | not verified | $685.30 | https://www.newegg.com/global/au-en/apc-br1500ms2/p/N82E16842301736 |
| Eaton 5S 1600 (5S1600AU) | 1600/960 | Not pure sine per my sources | 6 AU | not verified | $467.93+GST / $514.72 PB Tech; $529 Techbuy | https://www.pbtech.com/au/product/UPSPWR62674/Eaton-5S-1600VA1000W-Line-Interactive-Tower-UPS |
| APC BX1600MI-AZ (cheaper) | 1600/900 | Stepped approx. | AU | not verified | $314 DeviceDeal | https://www.devicedeal.com.au/apc-bx1600mi-az-back-ups-1600va-230v-ups |
| CyberPower VP1600ELCD (cheap) | see 3 | Simulated | 4 AU | HID | ~$289-$419 | see 3 |
Gaps: I could not open most retailer pages (403/429), so USB HID/macOS status for APC and Eaton is not verified here (CyberPower VP1600ELCD HID is manufacturer-stated). APC and Eaton units are generally Mac-compatible via macOS's built-in UPS support, but that is my general knowledge, not sourced here.
Pure sine claim: CyberPower: "The equipment with active power factor correction (PFC) design requires Pure Sine Wave source." https://www.cyberpower.com/eu/en/product/series/pfc_sinewave_gen._1 (vendor marketing). Apple has no stated requirement; AppleCare reportedly defers to the UPS maker: https://discussions.apple.com/thread/253120221 . Forum reports of simulated-sine units working fine for short outages exist (e.g. https://forums.macrumors.com/threads/does-mac-studio-require-a-pure-sine-wave-ups.2344458, not fetchable by me; seen only in search summary). Whether the Apple Silicon PSUs are active PFC is unsourced.

## 5. Recommendation (JUDGEMENT)
- Now: CP1500EPFCLCDa-AU. Pure sine removes the open question, AU sockets, ~49% worst-case load. Put the Studio, mini and NVMe on battery outlets; monitor on the surge-only/second outlet or skip it (monitors dumping load shortens runtime). Cheaper fallback: VP1600ELCD at ~$300 if Kam accepts simulated sine.
- Later (two Studios): two CP1500EPFCLCDa-AU, one per Studio (mini on the lighter side). Each unit then sees <=~425 W worst case. A single 1500 VA at 705 W+ is too tight; one 2-3 kVA unit costs more and is a single point of failure (and I did not price one).
- Also: the NVMe dropping out may be cable/enclosure/power-budget, not mains; a UPS does not fix a flaky USB-C link. Plug in the UPS USB cable and enable macOS Battery > UPS shutdown settings.
