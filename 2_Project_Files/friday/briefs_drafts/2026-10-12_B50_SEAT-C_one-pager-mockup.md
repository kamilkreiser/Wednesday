From Friday (laptop seat), Datasec / MPS Commercial Calculator. Replies to friday-laptop-agent@agentmail.to (no mail key in this project: your STATUS file is the wrap).
# BRIEF B50 · SEAT-C: One-pager proposal MOCKUP (design records only, no product code): the "One-pager or Full proposal" choice, a one-page A4 proposal on the same template as the full proposal, side by side with the full proposal's first page, and a PDF pack for Kam
**Written:** 2026-10-12 16:50 AEDT (draft). **Fired:** @NOW@. **Pane:** `Datasec/MPS-C`. Your commission is the newest file in `Briefs/` containing `_SEAT-C_`.
(Launcher check, read by the draft writer, the same check B45/B46/B42 state: `Launch_Claude.command:107` sets `SEAT` from a pane name matching `*MPS*-?`; `:111` says the commission is "the NEWEST brief in 1_Project_Definition/Briefs/ whose file name contains _SEAT-${SEAT}_". At drafting, `ls -t Briefs | grep -i _SEAT-C_` prints `2026-10-11_B33_SEAT-C_hosted-redeploy-db8edfd.md` first, finished: `B33_STATUS.md` last line `DEPLOYED: db8edfd5082e49f9a1a1b3c23feeb02b36834b21 live-check 0`. This file replaces it. Seat C was the hosted-redeploy seat; **this round is design only: no deploy, no Azure.**)
**Seat:** Seat C (Claude design seat). **MOCKUP ONLY.** Static HTML/CSS, its renders, one PDF pack, a tokens list, a words list, your STATUS. Nothing in `2_Project_Files` changes.
**Report:** `1_Project_Definition/Briefs/2026-10-12_B50_STATUS.md`. Its last line is exactly one of:
- `MOCKUP READY: 1_Project_Definition/Design/2026-10-12_one-pager/2026-10-12_MPS-one-pager-mockup_FOR-KAM.pdf` (records main @ `<sha>`);
- `STOPPED: NEEDS FRIDAY` and ONE question.

## AUTHORITY
- **Kam, verbatim**, live board 2026-10-12 14:35:55 (view=friday): *"on the Quick quote tool, when someone generates a quote, they should have a choice to build a 1 pager or full proposal as per the template built based on the sample already provided"*.
- **Kam, verbatim**, terminal ~16:45, answering Friday's which-tool question: *"MPS calculator, one-pager option on the same template"*. (Both relayed from FRIDAY `0_Brain/daily_friday/2026-10-12.md:103`, `:110`.)
- **Reading (Friday's, not Kam's words):** in the MPS calculator, where a proposal is produced, the user chooses **One-pager** or **Full proposal**. The one-pager uses the **same template** as the full proposal: same logo, palette (`--pd-*`), Arial type sizes, running header and footer, DRAFT watermark and footer classification. "Quick quote tool" names the calculator; the word "quick quote" appears **0** times in `web/src src docs` @ `b28c95eb` (case-insensitive), so it is **not** a product word here.
- **This round is the mockup.** Kam approves it before any build. Friday tells Kam "mockup ready" from your STATUS; you tell no human anything.
- **The template ruling this rests on** (records `main:1_Project_Definition/CLARIFICATIONS.md:187-202`, C-13): Kam's 2026-10-10 cards `mpscalc-proposal-template-text-assets-1010` = **b** *"Reuse the generic wording from my example"*, `mpscalc-proposal-customer-footer-1010` = **a** *"Approved quotes print 'Commercial in confidence'"*, `mpscalc-proposal-format-gst-ref-1010` = a. They are coded as constants in `web/src/proposal/settings.ts:1-24` (HTML print-to-PDF `:6-7`, footer `:8-11`, watermark `:13`, logo and hero `:15-17`, **ex GST only** `:18-19`, acknowledgement `:20-21`).

## READ WHOLE FIRST (all inside this project; you read no other project)
- The project `CLAUDE.md`; records `main:1_Project_Definition/CLARIFICATIONS.md` (C-04 AUD `:47`, C-05 internal users `:62`, C-13 `:187-202`).
- **B45's mock and STATUS, for shape and method only:** `Briefs/2026-10-12_B45_SEAT-A_home-dashboard-mockup.md`, `Briefs/2026-10-12_B45_STATUS.md` (renders, checks, records route, `*.pdf` force-add), and `1_Project_Definition/Design/2026-10-12_home-dashboard/checks/render_and_measure.py` (its 390 px iframe method, `B45_STATUS.md:64`).
- On code `origin/main` (`git -C 2_Project_Files show b28c95eb:<path>`, read verbs only; re-pin with `ls-remote origin main` first and say if it moved):
  - `web/src/proposal/ProposalDocument.tsx` (510, whole): the full proposal. Cover `:229-266`; sections 1-11 `:268-507`; running header/footer `@page` rules `:32-50`; the existing cap `detail(x).slice(0, 4)` `:295`.
  - `web/src/proposal/proposal.css` (104, whole): the template's palette `:6-12`, A4 page `:22-31`, print rules `:97-104`.
  - `web/src/proposal/template/cover.ts` (35), `template/sections.ts` (453; titles `:11-23`, straps `:26-40`, subheadings `:42-73`), `settings.ts` (35), `model.ts` (33), `format.ts` (58).
  - `web/src/screens/ProposalPage.tsx` (264, whole): the only "Print / save as PDF" button `:233-235`; **purchase quotes get the template document, rental quotes get the older `ProposalView`** `:224-225`, `:238-260` (B16 C-1); banner rule (gate B20 N-7) `:252-253`.
  - `web/src/screens/Lifecycle.tsx`: the **Proposal** link on the quote screen `:99-101`, the only way into the proposal today. `web/src/app/router.ts` (`#/quotes/{id}/proposal` `:12-13`, `:27-28`; no query strings).
  - `web/src/styles.css` `:1-20` (app tokens, for the choice UI only), buttons `:49-53`.
  - The customer-safe rule (below): `src/MpsCalc.Api/Quotes/Proposal.cs:16-25`, `src/MpsCalc.Api/Contracts/Dtos.cs:391-426`, `src/MpsCalc.Api/Quotes/QuoteEndpoints.cs:569-576`, `docs/API.md:118-120`, `web/src/proposal/ProposalDocument.test.tsx:126-133`.
  - The synthetic fixture `web/src/proposal/fixtures/s4Proposal.ts` (invented customer and prices, `:3`).
- **Kam's sample, in this project:** `1_Project_Definition/Source_Documents/2026-10-10_example-client-quote/` (B16 copy; git-ignored by records `.gitignore:11`; `PROVENANCE.md` says CONFIDENTIAL, real client name and prices). Read `analysis/example-structure.md` (page setup `:18-22`, outline `:34-89`, price conventions `:90-95`) and `analysis/gap-table.md`; open `example-quote.docx` only if those leave a question. **Use it only to decide what a one-pager keeps. Copy nothing from it into the mock: no client name, person, site, count, model or price. Never commit it, never quote it in STATUS.** (Friday's inbound copy outside this project is not yours to read.)
- Spec, layout ideas only: `Source_Documents/2026-09-30_from-Kam_renderings/Developer_Specification_and_SOW_v1.0_TEXT.md` FR-EXP-001…012 `:583-594`, FR-TPL-007/008 `:686-687`.

## STYLE RULE (hard): two palettes, each in its own place, nothing else
- **The one-pager is the customer document**, so it uses **only the template's own look**: `proposal.css` **copied byte-for-byte from `b28c95eb`** (blob `415d35c1dfd51b349802cfbf2cd4d0b0b59ac000`; prove it with `git hash-object` = that blob) plus ONE new file `one-pager.css` with rules scoped to `.pd-one`. Colours in `one-pager.css` come from `--pd-navy #122c45`, `--pd-blue #0067c8`, `--pd-pale #f5f8fc`, `--pd-light #eaf2f8`, `--pd-ink #182c3e`, `--pd-slate #516274`, `--pd-rule #c9d6e3`, `#fff`, the watermark `rgba(164, 38, 44, 0.12)` (`proposal.css:6-12`, `:47`, `:87`). Font Arial, Helvetica (`:15`); body 9.5 pt, tables 8.5 pt (`:16`, `:58`). Logo and hero from `web/public/proposal/` @ `b28c95eb` via `git show` (`hp-solutions-centre-logo.png` blob `046e9f43…`, `proposal-hero.jpg` blob `54850c10…`; Kam's supplied assets, `settings.ts:14-16`).
- **The choice UI is app chrome**, so it uses `styles.css:1-20` tokens only (as B45's `tokens.md` lists them), never `--pd-*`.
- **Write `tokens.md` FIRST** (ITEM 1): every colour and font in the mock → its source line, or NEW (name, value, why). A NEW colour inside the one-pager is a failure, not a NEW token: if you think you need one, STOP: NEEDS FRIDAY.

## WHAT EXISTS TODAY (measured by the draft writer, code main `b28c95eb`)
- **One way in:** quote screen → **Proposal** link (`Lifecycle.tsx:99-101`) → `#/quotes/{id}/proposal` → `GET /api/v1/quotes/{id}/proposal` → one **Print / save as PDF** button that calls `window.print()` (`ProposalPage.tsx:233-235`). Output format is HTML printed to PDF by the browser; **DOCX is not built** (`settings.ts:6-7`). Each successful read records a `proposal-generated` event (`QuoteEndpoints.cs:572-575`).
- **The template is purchase-only.** `ProposalDocument` (cover + 11 numbered A4 sections) renders when `quoteMode` is `purchase` (`model.ts:27-30`, `ProposalPage.tsx:224-225`). A rental quote renders `ProposalView` (`ProposalPage.tsx:16-155`): one header, five totals, per-line base and click rates; it is not on the template.
- **The full proposal's first page** is its cover (`ProposalDocument.tsx:229-266`): running header (customer upper-case + `MANAGED PRINT PROPOSAL`), logo, kicker, title (customer), sub-line, hero image, three navy KPI tiles (devices · upfront package ex GST · term), "Proposal ref … • Issued … • …-price validity", "Prepared by …". Section 1 (Executive Summary with the Commercial snapshot table) starts on page 2.
- **The sample's price convention** (`example-structure.md:93`): upfront package totals per device class; no per-unit price, no per-SKU list, no monthly figure; usage billed per page.
- **B46 (in gate as B48) touches the same screen:** `b46/home-dashboard` `0c74086a` changes `Lifecycle.tsx` (+86) and `router.ts` (+51) and no proposal file (`git diff --stat b28c95eb 0c74086a -- web/src/proposal web/src/screens/ProposalPage.tsx web/src/screens/Lifecycle.tsx web/src/app/router.ts`). The mock draws the quote screen as on `main`; say in STATUS that a build must sit on top of B46.

## CUSTOMER-SAFE FIGURES (cite this rule in the pack; the one-pager adds no field)
- The proposal is built on the server through **one allow-list** (`Proposal.cs:16-25`, `ProposalAllowList`; `Dtos.cs:391-394` "Every field is on `ProposalAllowList.Output`"); it carries no cost, markup, margin, rebate or profit field (`model.ts:4`); same body for every role (B45 brief, reading `docs/api/openapi.json` `getProposal`; `docs/API.md:118-120`; projection by status `QuoteEndpoints.cs:570-576`).
- The document shows **ex GST only** (`settings.ts:18-19`, Kam's #11); `purchaseTotalIncTax` exists and is not shown.
- The guard test forbids `cost|markup|margin|rebate|profit|distributor|MANUAL` in visible text (`ProposalDocument.test.tsx:131-132`); the template says "spend" and "consumables" instead (`sections.ts:6-8`).
- **Rule for the one-pager (Friday's default, D-9):** it reads **only** fields of the same `GET /proposal` response the full proposal reads, and only fields the full proposal already shows. ITEM 4(e) proves the words rule on the mock.

## THE MOCK MUST SHOW
1. **The choice** (app chrome, `styles.css` tokens). Friday's default (D-1, D-2): on the Proposal page, above the document, a two-option switch **Full proposal | One-pager**, **default Full proposal** (today's behaviour unchanged), next to the existing **Print / save as PDF**. Under each option one line saying what it contains and what it leaves out (FR-EXP-005, `…_TEXT.md:587`). The Proposal link on the quote screen stays one link. Draw: (a) purchase quote, Full proposal selected; (b) purchase quote, One-pager selected; (c) **rental quote** (D-3): One-pager shown disabled with its reason. Render at 1440 and at 390 (B45's iframe method), no sideways scroll at 390.
2. **The one-pager**, one A4 portrait page, `@page` size and margins as the template (`ProposalDocument.tsx:44-50`, 25.4 mm, `settings.ts:35`), with synthetic data. Four renders:
   - **typical**: the `s4Proposal.ts` fixture values (2 packages, credit row, optional items, 3 usage rates), approved (`isDraft` false: footer "Commercial in confidence", no watermark);
   - **draft**: the same, `isDraft` true: DRAFT watermark, footer `INTERNAL DRAFT — NOT FOR CUSTOMER RELEASE` (`settings.ts:9`, `:13`), "(Draft)" after the ref;
   - **small**: 1 package, 1 detail line, 2 rates;
   - **overflow**: 9 packages, each with 7 detail lines, 6 usage rates, a 1,400-character executive summary, 8 next steps.
   Every customer, ref, package and price is invented ("Sample Customer A", `Q-SAMPLE-2001`, "Sample A3 colour MFP package"…). Mark the data **SAMPLE** in the frame around each page and in every pack caption (not on the A4 page itself, so the fit test measures the real page).
3. **Side by side**: the one-pager next to **the full proposal's first page** (the cover), both from the same typical data. The cover is a **static replica** of `ProposalDocument.tsx:229-266` using the copied `proposal.css`; label it "replica of the built cover, synthetic data". (Running the app would need `npm install`: not this round.)
4. **The keep / condense / drop table**, one row per part of the full proposal (cover + sections 1-11 + their sub-parts, titles from `sections.ts:11-73`): KEEP / CONDENSE (to what) / DROP, and **a reason each**. Friday's starting point, for you to test against the page and change with a reason:

| Full proposal part | One-pager | Reason |
|---|---|---|
| Running header, footer, page number | KEEP | Same template; footer carries the classification (Kam's card, C-13) |
| Logo, kicker, title, sub-line | KEEP, title smaller | Brand and who it is for |
| Hero image | DROP (D-4) | Takes about a third of the page |
| Cover KPI tiles (devices, upfront package, term) | KEEP | The three numbers a reader wants first |
| Ref · issued · validity · prepared-by lines | KEEP, one line | Validity is the commercial condition |
| 1 Executive summary text | CONDENSE: first paragraph, cut at a sentence end ≤ 600 characters, then "…" (D-6) | The full text stays in the full proposal |
| 1 Intended outcomes cards | CONDENSE: up to 3 one-line bullets (card titles) | Space |
| 1 Commercial snapshot table + total | KEEP (the fit rule applies) | The price |
| 1 Pricing interpretation callout | CONDENSE to one line | The reader must know it is an upfront package |
| 2 Scope / fleet split / lifecycle / principles | DROP | Narrative; covered by the snapshot |
| 3 Office, 4 Large format | DROP | Capability narrative |
| 5 Fleet schedule detail column | CONDENSE: up to 3 detail lines per package, then "+n more" | Mirrors the existing cap at `ProposalDocument.tsx:295` |
| 5 Optional items | DROP; one line "Optional items are listed in the full proposal." when any exist (D-7) | Space |
| 6 Usage rates table | KEEP (up to 6 rows) | Ongoing charges are part of the price |
| 6 Rate method, software reconciliation, boundaries | DROP | Detail |
| 7 Service, 8 Implementation, 9 Governance | DROP; one line "{term}-month device support included" | Narrative |
| 10 Open decisions register | CONDENSE: count only, "n items to confirm before contract" when n > 0 | The reader must know it is not final |
| 11 Commercial summary rows | CONDENSE: validity and term only (price is already in the tiles) | Duplicate |
| 11 Next steps | CONDENSE: first 3 | Space |
| 11 Acknowledgement / signature block | DROP (D-5) | A one-pager is indicative; signing uses the full proposal |
| 11 Proposal basis | KEEP, one line | Names the quote and version (`settings.ts:22-23`) |

5. **The fit rule** (D-6), stated on the pack and proven by the overflow render: one A4 page, never two. Package rows: up to **6**; with more, the top **5 by package total** plus one row **"and n more packages"** carrying their combined total, so the TOTAL row still equals `purchaseTotalExTax`. Detail lines: up to 3 per package then "+n more". Usage rates: up to 6 rows then "and n more rates (see full proposal)". Outcomes 3, next steps 3, summary text ≤ 600 characters. Nothing shrinks below the template's 8.5 pt table size (`proposal.css:58`). If the overflow data still does not fit after these caps, say which part pushed it over and STOP: NEEDS FRIDAY.
6. **NEW WORDS** (`NEW_WORDS.md`): every user-visible string on the choice UI and the one-pager that is not already in the built UI or template (`git grep -i -F` on `web/src` @ `b28c95eb`; a hit read by eye is named). Table: string · where · why. Expected at least: `One-pager`, `Full proposal`, the two one-line descriptions, the rental disabled reason, `and n more packages`, `+n more`, `and n more rates (see full proposal)`, `Optional items are listed in the full proposal.`, `n items to confirm before contract`, the one-pager kicker (Friday's default `MANAGED PRINT PROPOSAL · SUMMARY`, D-8). Mock-only marker words (SAMPLE, captions) in a separate list, not proposed for the product.
7. **Decisions for Kam**, numbered, each with Friday's recommended default, so Kam can answer "approve with all the defaults". Put them on the pack, in this order:
   - **D-1 Where the choice sits:** a switch on the Proposal page (default) · or two buttons on the quote screen.
   - **D-2 Default choice:** Full proposal, every time (default) · or remember the user's last choice.
   - **D-3 Rental quotes:** One-pager for purchase quotes only for now, disabled with a reason on rental, because the template exists only for purchase (default) · or build a rental one-pager on the template too (a bigger job: rental has no template today).
   - **D-4 Hero image on the one-pager:** dropped (default) · or a short band.
   - **D-5 Signature block:** dropped (default) · or kept.
   - **D-6 Fit rule:** as item 5 (default) · or a summary by device class instead of package rows.
   - **D-7 Optional items:** one line pointing to the full proposal (default) · or listed.
   - **D-8 Wording:** switch label "One-pager" (Kam's word) and document kicker `MANAGED PRINT PROPOSAL · SUMMARY` (default) · or Kam's wording.
   - **D-9 Figures:** only what the full proposal already shows, ex GST (default; no choice proposed, stated for the record).
   - **D-10 Record which format was generated** on the `proposal-generated` event (FR-EXP-008, `…_TEXT.md:590`): yes (default). Mark it `needs: a format on the proposal-generated event` in the pack; it is a build item.

## FR OVERRULE LINES (one line each on the pack, for Kam to overrule)
- FR-EXP-010 (`…_TEXT.md:592`) says an unapproved quote disables customer export; the app today shows a draft proposal with a DRAFT watermark and an internal footer (FR-EXP-011 `:593`; `settings.ts:8-13`). **The one-pager follows today's full-proposal behaviour exactly; it adds no new rule.**
- FR-EXP-005 (`:587`): the one line under each option states what it includes and leaves out.
- Spec §16 Template Library / Designer (FR-TPL-001…012, `:673-691`) is not built (RECOMMENDED, `:112`). **The one-pager is a second fixed layout of the built template, not a template-library entry.**
- FR-TPL-008 (`:687`): A4 portrait, met.

## ITEMS
**Records route (measured, as B45 did it):** the records repo is the **project-root** git repo, **0 remotes**: commit only, push nothing. Records `main` = **`d18707ca6c56843e88e74064e997f3a705a00445`** at drafting (B47's fold); tracked status clean (0 lines, `--untracked-files=no`); `1_Project_Definition/Design/2026-10-12_one-pager/` does not exist. Re-read both at launch and use what you read. Work in a worktree: `git -C <root> worktree add .tools/wt-B50-design -b records/b50 main` (`chmod 700`).
1. **`tokens.md`** first (see STYLE RULE). Commit.
2. **Mock files**: `choice.html` + `choice.css` (item 1); `one-pager.html` + `one-pager.css` + the copied `proposal.css` (items 2, 5); `cover-replica.html` (item 3); `assets/` (logo, hero via `git show`). Static: no `<script>`, no form, no external URL, no web font.
3. **Renders** with the installed browser, `file://` only, own profile in your scratchpad, light only (no dark theme exists): `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new …`. The four one-pager variants and the cover replica each `--print-to-pdf --no-pdf-header-footer` to their own PDF (these are the fit proof) and to PNG; the choice states at 1440 and 390. If Chrome fails, **STOP: NEEDS FRIDAY** (install nothing). No port is needed; if one ever is, use 6620-6629 only, `lsof -i :<port>` first, and stop it by PID.
4. **Checks** (scripts and outputs in `checks/`, Python with `-I`), each with a control that fires:
   (a) **one page:** each of the four one-pager PDFs has `/Count 1`; control: the overflow data with the caps switched off gives > 1.
   (b) **same template:** `git hash-object proposal.css` = `415d35c1…`; every colour in `one-pager.css` is in `proposal.css`; control: a planted `#12ab34` fires. Every colour in `choice.css` is in `tokens.md` (B45's method).
   (c) **customer-safe words:** visible text of each one-pager matches none of `\b(cost|markup|margin|rebate|profit|distributor|MANUAL)\b` (`ProposalDocument.test.tsx:132`) and shows no inc-GST figure; control: a planted "cost" fires.
   (d) **totals reconcile:** in the overflow render, the package rows (including "and n more") sum to the TOTAL; control: drop the "and n more" row and it fails.
   (e) **390 px** on the choice states: `scrollWidth ≤ clientWidth`; control: a 600 px element fires.
   (f) **no sample leak:** `grep -i -c` in every committed file for the sample's client name, its people and its sites (take the strings from `example-structure.md`, hold them in your scratchpad only, never write them into a committed file or STATUS) = 0; control on a scratch file containing one. Report the count of strings tested, not the strings.
5. **`NEW_WORDS.md`** (item 6).
6. **The pack** `pack.html` → `2026-10-12_MPS-one-pager-mockup_FOR-KAM.pdf`, as few pages as stays legible (target 2, landscape like B45's): page 1 = the side-by-side (cover replica | one-pager, typical) + the choice states; page 2 = the keep/condense/drop table, the fit rule with the overflow thumbnail, the customer-safe rule with its citations, the decisions D-1…D-10 with defaults, the FR lines, the NEW WORDS count. A ribbon says SAMPLE DATA.
7. **Commit** all files under `1_Project_Definition/Design/2026-10-12_one-pager/` on `records/b50` (message `Design: MPS one-pager proposal mockup for Kam (B50)`). PDFs: root `.gitignore:16` ignores `*.pdf`; force-add (`git add -f`) **only your own renders**, as B45 did (`B45_STATUS.md:89`); leave the ignore rule unchanged. Then fold as B45 did (`B45_STATUS.md:90`): if root tracked status is clean and `main` is an ancestor of `records/b50`, `git -C <root> merge --ff-only records/b50`; otherwise `merge --no-ff -m "Records: fold records/b50 (B50)"`; any conflict: `merge --abort`, **STOP: NEEDS FRIDAY**. Read back `git rev-parse main` and `ls-tree -r main -- 1_Project_Definition/Design/2026-10-12_one-pager/`. **No history entry this round** (unlike B45): leave `5_Project_History/history.md` alone.

## STATUS sections
BLUF · pins read at launch (code main, records main) · prior work as you found it · tokens (count, source per colour) · the keep/condense/drop table as rendered, with every change from Friday's starting point and why · the fit rule as rendered · renders and PDFs (path, size or pages, sha256) · checks (a)–(f) with results and controls · NEW words count · decisions D-1…D-10 as shown · records (branch, commits, fold, `main` before/after) · UNMEASURED · NOT DONE · needs-Friday · processes started/stopped.

## UNMEASURED (by the draft writer)
- Whether the typical data fits one page with the template's 25.4 mm margins at all (not rendered).
- How the browser's print dialog names the saved file (`document.title` is not set by `ProposalPage.tsx`; not checked).
- Whether a rental one-pager can be built from the rental fields alone (`Dtos.cs:407-414`); D-3's default leaves it out.

## HOLDS
- Datasec only; no other client's names or files. **You read nothing outside this project.**
- **No product code:** `2_Project_Files` read verbs only (`ls-remote · log · show · diff · cat-file · ls-tree · rev-parse · grep`; no checkout, branch, commit, push, `npm install`). No deploy, no Azure, no setting change. **P-1 hosted hold unchanged** (records `BACKLOG.md` `## Holds on the hosted site`); the hosted site is not touched.
- **Synthetic data only.** Kam's sample stays where it is: read, never copied into the mock, never committed, never quoted. Never open `4_Credentials/.env`.
- **Nothing to any human; no Jira; no `history.md`.** The launcher prompt tells every seat to write history and Jira: refuse both and say so in STATUS. Push nothing (records repo has no remote).
- Own worktree `.tools/wt-B50-design` only. Never delete; quarantine to `.tools/_quarantine/2026-10-12_B50_<what>/`. Kill only what you started, by PID.

## End
The last line of `Briefs/2026-10-12_B50_STATUS.md` is exactly one of:
- `MOCKUP READY: <pdf path>` (records main @ `<sha>`);
- `STOPPED: NEEDS FRIDAY` and ONE question.
