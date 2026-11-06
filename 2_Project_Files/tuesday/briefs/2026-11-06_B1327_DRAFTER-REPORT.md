STARTABLE: NO as MPSCALC-118 is filed (its fix shape asks for a copy of the server's rules, and its purchase half is a presentation ruling). YES only as the NARROWED rental-only lane this kit drafts, and only if Tuesday answers Q-1 yes in S4 (the kit refuses to run otherwise). No MPS pane live, no b1327 ref, 132 GiB available, load1 4.74 at 13:10.

# B1327 drafter report: SEAT-M95, MPSCALC-118 (the stub's breakdown fields)

Kit: /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-06_B1327_SEAT-M95_mps-118-stub-breakdown-fields.md (12 four-underscore runs = 11 slots plus the last line; 0 non-ASCII bytes by `LC_ALL=C grep -c '[^ -~]'` after one fix). Slots: 2026-11-06_B1327_slots.json (12 keys, no angle-bracket placeholder). Shape copied from the B1315 kit. Clocks (date, AEDT): 13:07:46 start, 13:11:03 last read. Nothing in the kit is later.

## BLUF
- As filed it fails the test: "the stub emits the fields from the same rules the server uses" means putting the server's cumulative rounding (R-28) into TypeScript in the stub, a second implementation that can drift, and the purchase half (class subtotals on a calculation the stub marks "STUB: not priced") means choosing between a zero-valued block and the existing note, which is a presentation call, not a test rule.
- The rental half is small and clean: ONE fixed object (`stubApi.ts:34` `stubProposal`, returned at `:408`) gets eight literal strings (four `ExTax` parts, four `InCentsExTax` parts), derived by hand from the object's own fields as 1, 0, 1, 0 (sum 2 = `monthlyChargeExTax`). No function, no arithmetic in the stub; the arithmetic lives in the test.
- Hosted product: no change (the stub is excluded from the production bundle by `check-bundle.mjs`, run at `ci.yml:66`); stub mode only. New words: none (the block uses the existing `RENTAL_PART_LABELS`). Rules: not changed, not duplicated.
- The test holds the literals to the server's stated invariants (R-27 sum; cents sum = charge rounded to 0.01; at most 2 decimals; within one cent; zero stays zero), with a plant for each. It does NOT hold the stub equal to the engine for arbitrary inputs, because the stub computes nothing and the fixture is integers, so rounding is never exercised.
- Tier C2 Sonnet (`model-routing.md:92`), gate G2 with a doubt (Q-3). Not a Done under C-79: no Done-when exists, and this lane leaves the ticket's own fix shape unmet.

## The questions the commission asked
1. Does it change what a user sees in the hosted product? No (DERIVED; the hosted site is not read, no HTTP): `check-bundle.mjs:1` states a production bundle holds no stub code and `:29` lists the marker `STUB-PROPOSAL`; CI runs it at `ci.yml:66`. What flags the hosted showcase was actually built with: UNMEASURED. In stub mode (VITE_MPSCALC_API_STUB=1) the stub proposal screen changes from NO breakdown block to the four-row block.
2. Customer-facing words? None added. The labels are `RENTAL_PART_LABELS` (`PriceBreakdown.tsx:57`), already shipped. Showing "Software / month $0.00" and "Colour print / month $0.00" rows is the existing component's behaviour (`rentalRows` always lists four). So it is a build, not a word pack, in the narrowed form.
3. Pricing rules changed or duplicated? Not in the narrowed form: literals only, a checked NO in the kit (property: no function, no arithmetic in added `stubApi.ts` lines, with a counted control). In the ticket's form, yes: duplicated.
4. The test that holds it equal, and its plant: R-2 in `stubApi.test.ts` asserts the server's invariants (quoted from `RentalPartsInCentsTests.cs:10`); plants P-M (a cents literal moved), P-Z (a zero part made non-zero), P-F (a field deleted), P-D (the charge changed) each turn named rows red; PC0 runs the new file on the unchanged stub. All DERIVED, none run.
5. "No new word, no ruling, no production touch": the narrowed lane passes all three; the ticket as filed does not (rules copy; purchase zero-block). Hence NO, with the narrowed YES behind Q-1.

## Corrections to the commission text (what was wrong or loose)
- C-1 "Ranks 10 to 13, M4": the sweep line about 118 is line 92 of `2026-11-06_SWEEP-1006_delta-on-0600.md` (M4); I did not map "Ranks 10 to 13" to a line, only the M4 text. Its counts are right: 428 and 216 lines, 0 matches each, re-measured with controls (`monthlyChargeExTax` 1 in stubApi.ts, `notPriced` 2 in purchaseQuotes.ts).
- C-2 The sweep names `stubApi.ts` and `purchaseQuotes.ts` as the fix paths. Only `stubApi.ts` carries a rental figure at all (`stubProposal`); there is NO stub rental `Calculation` (rental quotes go to the real API, `stubApi.ts:1-4`). `purchaseQuotes.ts` is the purchase half only.
- C-3 The ticket says stub mode "shows the note". For the rental proposal it shows no block and no note (`ProposalPage.tsx:88` `parts &&` renders nothing when parts are absent; DERIVED, not rendered). The note belongs to the purchase calculation (DERIVED).
- C-4 The sweep says size "3 files, 100 to 300 lines"; the narrowed lane is 2 files and about 60 to 150 lines (GUESS).
- C-5 M94's two `b1315/*` branches are not "awaiting a gate" in a way that blocks anything: both are ahead 1 behind 0 and READY FOR QA per the B1315 STATUS last line; their file lists are `summaryCensus.test.tsx` (census) and `cssColourGuard.ts` plus `cssColourGuard.test.ts` (guard). The partition with M95: 0 common paths (neither touches `web/src/api/stub/**` or `PriceBreakdown.tsx`). The M94 kit explicitly dropped 118 for the same reasons as above (its D-1).

## D-decisions
- D-1 Write the narrowed kit but gate it behind Q-1 in the REFUSE list, rather than force a rules copy or silently drop the rental half.
- D-2 Literals, not rules; the test, not the stub, does the arithmetic (test files are outside the browser-pricing guard, `noBrowserPricing.ts:30`).
- D-3 Literals follow the object's own fields: base 1 x 1 = 1, software 0 (`softwareMonthlySell` `'0'`), colour 0 (`appliedColourClick` `'0'`), mono 2 - 1 = 1 (implies 1000 pages at 0.001, not carried by the object; said in the kit).
- D-4 Purchase half out of the lane (`purchaseQuotes.ts` listed NOT yours).
- D-5 No port block (jsdom, ephemeral loopback only); `lsof` printed no seat conflict; the word-boundary scan of 34 non-`.pre-` SEAT kits of 5 and 6 Nov printed 0 files for `B1327` and `M95` (control: `B1315` finds 1).
- D-6 READY 60 and HARD STOP 100 minutes (one commit, one push, five plants).
- D-7 The ticket stays open after landing; the kit says so in FACTS 12 (C-79 quoted, `CLARIFICATIONS.md:1714` and `:1716`).

## Facts re-measured (instrument; control)
- Main `3b1ec832879cf59f1997f50a0914beb4c4685912` by `gh api -X GET git/ref/heads/main` (13:07:57 and 13:11:03). Open PRs 0; control `pulls?state=all&per_page=3` lists #158, #157, #156. `matching-refs/heads/b1327` 0; control `heads/b1315` 2 rows.
- Blobs by contents API `.sha`: stubApi.ts `6ec508fe...`, stubApi.test.ts `16478a97...`, purchaseQuotes.ts `7537bc60...`, PriceBreakdown.tsx `f1da8a50...`, ProposalPage.tsx `d7494e88...`, schema.ts `af3e92ee...`.
- Jira (copy of the b1255 reader with its output re-pointed to this session's scratchpad; GET only; JQL `project = MPSCALC AND ( key in (MPSCALC-118, MPSCALC-361) )`): MPSCALC-118 Backlog, 0 comments, updated 2026-10-13T22:44:07, description 986 characters, quoted in the kit; control MPSCALC-361 Done, 1 comment. Done-when count not run by me beyond reading the description whole (no such line in it).
- Pointers printed by `grep -n` over raw copies at main: stubApi.ts `:33 :34 :52 :53 :54 :55 :61 :65 :408`; purchaseQuotes.ts `:5 :127 :147 :159 :206`; noBrowserPricing.ts `:30 :33`; PriceBreakdown.tsx `:3 :57 :74 :95 :119 :150`; ProposalPage.tsx `:17 :36 :88`; check-bundle.mjs `:1 :29`; ci.yml `:66`; proposal-stub-mode.spec.ts `:25 :28`; schema.ts `:1593 :1617 :1625 :1633`; RentalPartsInCentsTests.cs `:10 :14`; stubApi.test.ts `:5 :47`. `model-routing.md:92 :93 :109` and `models_latest.json:23` and `brief_seat.sh:24` printed by `awk NR`. `CLARIFICATIONS.md:774 :1712 :1714 :1716 :2218` printed by `awk NR`.
- C-79 quoted: "Done means merged to main, the same as Composer" (`:1714`).
- B1315 STATUS (project root, local): 380 lines, first line `PROGRESS B1315: M1 DONE M2 DONE`, last line READY FOR QA with both heads and whole-suite 1399/0/0 and 1415/0/0 (baseline 1398/0/0); heads equal the two origin refs I read.
- Ports: `lsof -nP -iTCP -sTCP:LISTEN` at 13:10 printed `*:7000 *:5000 *:49156 *:59869 127.0.0.1:49221 :49223 :49226`; panes 10, 0 matching `mps`.

## Q-questions for Tuesday (each with a default)
- Q-1 Run the NARROWED lane (rental stub proposal literals plus invariants test; purchase half and rules half not built) at all? Default: NO, hold the kit; the value is "stub fidelity for the demo", ranked lowest of four in the sweep, and the rules half has no safe test-only form. Say yes in S4 to run it.
- Q-2 The purchase half (zero class subtotals vs the existing note on a not-priced calculation): leave open on the ticket as a product-owner call? Default: yes, a decision card is Tuesday's to open, not the builder's.
- Q-3 Gate G2 or G1? The change is in a non-test source file but is excluded from the production bundle and is synthetic. Default: G2 (`model-routing.md:109`, "config/CI, tooling"), with the bundle check as part of the CI line; raise to G1 if Tuesday reads the stub as a "handed to a client tester" surface (demo use, UNMEASURED).
- Q-4 After landing, does MPSCALC-118 stay open? Default: yes (no Done-when exists and the fix shape is unmet; C-79 requires the clauses met).
- Q-5 Accept literals 1, 0, 1, 0 (integers, so rounding is not exercised)? Default: yes; a rounding-exercising set would need a computing helper, which NO 2 forbids.
- Q-6 READY 60 and HARD STOP 100 minutes? Default: yes.

## UNMEASURED
- Whether the stub proposal screen really shows no block today, and what it shows after (kit Step 5 prints both).
- Whether `ProposalView` can be mounted from `stubApi.test.ts` without a heavier helper (the kit allows a `proposalRentalRows` fallback).
- Every plant's red (all DERIVED). The whole-suite baseline at this base (RELAYED 1398 from B1315).
- Whether the hosted showcase or any demo uses the stub (no HTTP allowed); `tools/demo/test/stub_api.py` is a separate Python stub, not read.
- The product owner's words since the ticket was filed; any decision card for this ticket (none read, per the rules); gate verdict history for the class.
- Hosted CI, CodeQL, the dotnet and python jobs, the e2e specs.

## Outside the fences
Wrote only the kit, the slots file and this report (Write tool); one `python3 -I -B` edit of my own just-written kit (two phrase fixes, one U+03A3 replaced by words). Reads: DRAFTER_RULES.md, the B1315 kit, slots and report (`.pre-stamp` and `.pre-tuesday` copies), the sweep line, `model-routing.md` rows by `awk`, `models_latest.json:23`, `brief_seat.sh:24`, `CLARIFICATIONS.md` lines by `awk`, MPS Jira via a scratchpad copy of the b1255 reader (GET; no token printed), `gh api -X GET` under the MPS `GH_CONFIG_DIR` (ref, pulls, matching-refs, compare, trees, contents), local `ls` and `head`/`tail` of the B1315 STATUS and `ls` of `.tools/b1270` and `.tools/b1315` (no file inside read except the STATUS), `tmux list-panes`, `lsof`, `df`, `uptime`. Raw copies and the Jira output under /private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/f5b86e85-0127-40a5-a736-8e33c71346ec/scratchpad. No decision_queue.sh, no briefs_staged, no scoreboard.md, no _ledger.md, no WEDNESDAY or FRIDAY tree. Hook refusals (a `cd` once, an unquoted `==` once) stopped before running and were re-issued. No fetch, no ref write, no mail, no Artifact or Docs tool.
