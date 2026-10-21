# B427 drafter report (Sonnet brief-drafter, row C8), 2026-10-22 about 01:00 AEDT

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B427_SEAT-U1_hpsmpoc-user-guide.md` (88 lines). Unstamped slots: 1 line (`grep -c` printed 1). Pane `Datasec/HPSM-POC-U1`. Last line `READ-WHOLE-BY-TUESDAY: PENDING`.

## What I measured (00:59 AEDT)
- UAT start page GET: HTTP 200 (one curl, no other HTTP).
- Project `Deliverables/` holds one folder, `2026-10-08_HP-walkthrough` (docx, pdf, `screens/`, `SOURCES.md`); the brief copies that convention under `2026-10-22_user-guide/`.
- No existing UAT user guide or help text (filename search of `Briefs/` and `Deliverables/`). Prior work the brief points the seat to: the email draft, B410 CHECKS `:515-562`, B409's reach table, B186's walkthrough and builders, B377 (demo; route list only).
- Branding: Kam ruled "b — HP branding", assets to come from HP (`Briefs/B120_ADDENDUM-1...:5-6`); no record in the project says HP's assets arrived; site theme is the neutral placeholder (`brand.css` and `design-system.md`, "Branding is UNDECIDED"). The brief therefore forbids any HP mark and builds the house style only from the product's own tokens (hex list in the brief, re-read at source by the seat). No project style guide existed apart from `Design/design-system.md`, so item 0 has the seat write `STYLE.md`.
- Word for Mac was ABSENT and no LibreOffice on PATH, so B186's PDF route (Word) may not work; the brief gives a fallback (Chromium print-to-PDF of the same content, text-diffed against the DOCX).
- Routing: no row says "documentation deliverable"; cited C2 (pilot) with C8, Sonnet.

## Questions for Tuesday (each with my recommendation)
1. **"Fully branded" with no HP assets.** Kam said fully branded; the project has only a neutral theme and a ruling that waits on HP's assets. Recommendation: go as briefed (product tokens, Arial, text "Datasec" on the cover, no logo) and say in the cover note to Kam that HP marks are held until HP's brand assets arrive, so he can supply a Datasec logo or accept the neutral look. Alternative: ask Kam first for a Datasec logo file; I would not wait, since the seat can re-style in minutes.
2. **Datasec's own brand source.** The brief lets the seat read `/Volumes/Laptop-DEV/Notes (MASTER)/context/` (read-only) for a Datasec logo or colours. That folder is outside the HPSM-POC project and outside my own fences, so I did not read it. Recommendation: allow it (the workspace rules say Datasec sessions skim `context/`); strike item 0.2 if you want the seat confined to the project.
3. **PDF route.** Recommendation: leave the fallback as written; if you would rather have Word-exact output, check where Word lives before launch (`mdfind kMDItemKind == Application`).
4. **Level choice and sign-out are POSTs.** The brief allows exactly those two (cookie only, no data change, B410 `:533`) and aborts every other non-GET with a firing control. Recommendation: keep; the guide cannot show the four levels otherwise.
5. **Steps that change data are "shown, not run".** The seat will not answer questions, generate, approve, issue or submit feedback; it screenshots the page before the step and says so. Recommendation: keep; tell Kam in the cover note that the step-by-step for write actions is described, not demonstrated, on the review copy.
6. **Admin feedback list.** UAT holds one synthetic item ("B410 UAT stand-up check ... Please ignore"). The brief masks or omits row text. Recommendation: keep.
7. **Commit/filing.** B186 committed its deliverable to a records branch; this brief commits nothing (a draft for Kam). Recommendation: file it in records after Kam reviews.
8. **Email size.** I set PDF and DOCX each at or under 8 MB (B186's pair was 2.5 MB and 2.9 MB). I did not check the mail attachment limit. Recommendation: confirm it before the send.
9. **No SOW scan.** B186 ran a 6-word no-quote scan against the SOW; that needs opening the SOW, which the standing hold forbids, so the brief drops it and has the seat quote only the live site and the approved email sentences. Recommendation: keep.
10. **Draft-wording duty.** The brief has the seat list all new wording in STATUS (cover, header, footer, executive summary, limits section) for your cover note to Kam. Recommendation: put those into the cover note verbatim and state that it is a draft for his review.

## Not done by me
No stamp, no launch, no other HTTP, no `.tools` or vault reads, no scoreboard, no decision queue.
