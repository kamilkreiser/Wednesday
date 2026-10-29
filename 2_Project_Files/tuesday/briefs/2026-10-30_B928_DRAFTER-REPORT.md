STARTABLE: YES (after your stamp; rank 1 of wave 1. Three facts differ from the sweep's seed and the ticket, all handled in the kit, none blocks: the app has 4 client questions not 16, the API summary has no findings count, and an e2e spec pins the rail's first `p` as the customer line)

# B928 drafter report (Fri 2026-10-30 about 10:23 to 10:55 AEDT)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-30_B928_SEAT-H59_hpsmpoc-374-customer-frame.md` (150 lines; 9 four-underscore lines = 8 slots + the last line; at-sign slots 0; non-ASCII lines 0, control: a scratch file with one raw byte reads 1). Seat `Datasec/HPSM-POC-H59`, ports 9600-9609, branch `b928/hpsmpoc-374-customer-frame`, ticket HPSMPOC-374. Shape copied from B885 (shell) with the restyle rules of B891 (primitives). Read-only everywhere; gh `-X GET` under the project `.gh-config`; Jira only through `.tools/b649/jira.py` (GET); no `cd`, no hosted HTTP, no ref written. No file written in the project's Briefs folder.

## BLUF
HPSMPOC-374 is the customer frame only: a header card over the six tabs, a sticky rail card without Overview, "Back to customers", rail collapse moved from `lg` to `xl`. All 13 lane files exist at `e21d8044` and the only shared thing is that the frame renders `StagePill` and `Breadcrumbs` from `customer/parts.tsx` (H3's file). The kit forbids editing it and has a D-6 sync rule for H3's landing: base on the new main if H3 lands before Step 3, otherwise a single `merge --no-ff` on Tuesday's ADDENDUM. No rebase and no force in either case. No e2e file is edited: the four dependent specs must pass unchanged, and a red one is a STOP.

## Facts measured (instrument; control)
- Main `e21d80442980fb61ad9fb11aaf393c0b20c0ad2d` (`commits/main`); open PRs 0; `matching-refs/heads/b928` 0 (control `heads/b92` lists 2 old refs); panes `%0 tuesday`, `%1 fleet-monitor`; `lsof` 9600-9609 0 lines; 96xx in 10-28..10-30 SEAT kits: only 9660-9669 (B919, B922 gates); load1 2.88 at 10:23.
- Jira HPSMPOC-374: Backlog, `design-v12`, 0 comments, Depends 368 and 371 (both in main). Its AC is the Done-when; quoted verbatim in the kit.
- Frame at main (tarball): `CustomerShell.tsx` 254 lines. Line numbers in the kit: Breadcrumbs import 15, frameLabel 60-65, early returns 118-131, the select 156-175, tabs nav 176-191, rail 194-237 (`lg:w-64`), main 240. Rail lists map all 10 `JOURNEY` entries.
- Dependents: `customer-frame-alias.spec.ts` lines 50 and 81 read the rail's first `p` at 1440 (Partner gets name and industry, Demo gets the no-run words). `frameText` reads `nav[aria-label=Breadcrumb].parentElement.innerText` with `#main` hidden. `customer-headings-alias.spec.ts:40` takes the eyebrow as the `p` before `#main h1`. `CustomerShell.b59.test.tsx` 84-97 pins ONE main and has the axe `region` history.
- Data: `AssessmentSummary.completion{answered,required}` exists and there is no findings count. The client ruleset holds 4 questions. `openQuestionCount` is in `lib/status.ts:16`, and `stageFromApi`/`stageFromPrototype` are in `directory.ts` 42/52.
- Layout: the AppShell content column has no overflow (line 166), and `Sidebar.tsx` is `lg:sticky` 228 px, so a sticky rail should work. Not seen in a browser.
- Model: routing lines 92 C2, 108 G1, 109 G2, 111 G-cap; `models_latest.json:23` = `claude-sonnet-5-5`.
- Design sha256 `fb799db8...feaa` re-measured; `.journey` 226 px / gap 16, `.journey-nav` sticky top 15, the card's name is an `h2`, its chips read `N / 16 captured`, `K draft findings`, stage.

## Sweep pointers found WRONG or incomplete
1. "questions captured of 16": the app has 4 client questions. The kit shows the app's own numbers (D-3).
2. "draft-finding count": the API has no count, and fetching one would add a request on every customer page. So the chip appears only for the prototype-held customer (D-3).
3. The seed's "no Overview entry" does not cover the phone `select`. The kit keeps that select unchanged (both alias specs use it).
4. The seed lists screenshots at 1024/1180/1280/1440 and the standing line lists 390/768/1024/1280/1440. The kit does both.
5. The seed does not say the rail's first `p` is pinned by an e2e spec. The kit keeps it.

## D-decisions (in the kit)
D-1 one branch, C1 rail, C2 card, C3 optional, push after C1. D-2 card is `section aria-label="Customer engagement"`, name in a `p`, tabs inside the card. D-3 the app's own numbers, no new request. D-4 `xl` breakpoint, Overview dropped from both rail lists, select kept. D-5 Back goes to `/customers`. D-6 the H3 sync rule above. D-7 Sonnet C2, gate G2, 240/360 minutes.

## Q-questions for Tuesday (recommended default first)
- Q-1 Gate tier: **tier 2 (G2), round 1 of 2 on the new class "customer frame restyle"**. The sweep defaults to this. Lift it to tier 1 if you count the Demo alias surface (a name leak to Demo is a confidentiality miss in front of HP) as client-tester-facing.
- Q-2 Card name element: **`p`** (keeps the page `h1` first and focus behaviour). The alternative is the design's `h2`.
- Q-3 Chips: **app numbers, no new request** (D-3). The alternative fetches findings in the shell; that moves the request pins.
- Q-4 Breakpoint: **xl** (1280). This is the ticket's own word, and the screenshots confirm it.
- Q-5 H3 sync: **D-6 as written** (base on the new main, or one merge on your ADDENDUM). The alternative is to hold H6's launch until H3 lands. Not recommended: H6 is rank 1.
- Q-6 Times: **target READY 240, hard stop 360** minutes.

## Reasons not to launch now
None blocking. Launch H6 and H3 close together so H3's landing comes before H6's gate. Load was 2.88.
