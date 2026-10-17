# B171 DRAFTER REPORT: records seat R3, MPS merges #79-#82 and gate B170's open items
Drafted 2026-10-18, 05:2x to 05:38 AEDT. Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-18_B171_SEAT-R3_mps-records-1017-merges.md` (150 lines, 25,705 B; sha256 `68b13c76…1e92` before this report was written; Tuesday's stamp will change it).

I wrote nothing under `!CODING/`. Tools used:
- git read verbs with `--no-optional-locks`;
- `gh api` GETs under MPS `GH_CONFIG_DIR` (`kamilDatasec`);
- Jira read-only GETs through a scratch client that reads `JIRA_*` by name and never prints them.

No fetch, no az, no hosted call, no mail, no tap.

## Read
- B169's brief (129 lines) and `B169_STATUS.md` (235 lines), both WHOLE.
- `B170_STATUS.md` WHOLE (160 lines, sha256 `5b6d2319…54fb19`).
- The project `CLAUDE.md` (82) and `JIRA.md` WHOLE (94).
- `CLARIFICATIONS.md`: headings, the `:1-30` format, the `:340-400` coordinator precedent, and `:552-594`.
- The tails of `BACKLOG.md` and `history.md` (`:1-40`).
- PR bodies #79-#82. Tuesday's daily note 2026-10-17, by grep. B170 kit `:313`. W2 `:40-60`.

## Measured (05:35)
- **Main** `e6f92a5f…` (ls-remote). Commits API: #82 → #81 → #80 → #79 → #78 → #75, each with 1 parent. #83: 404. `e6f92a5` is NOT in the local store, so the code lines were read with `gh api contents?ref=e6f92a5`:
  - `PriceBookImporter.cs:140`: confirmed stale ("Item class: service (default K-05, until MPSCALC-142).");
  - `PurchaseCatalogue.cs:148` `ItemClass.CarePack`;
  - `OnePager.tsx:29`;
  - `sections.ts:381-382`;
  - `QuoteEndpoints.cs:1197-1200`;
  - `deploy-from-ci.sh:118`;
  - `Proposal.cs:525-526`;
  - `ENGINE.md:141` (X-25).
- **Jira:** no comment carries any of the four merge shas (0 ×4; control `f1d5641…` → 3). The tickets are all in Backlog: 194 and 203 (each with lane E's pre-merge branch comment, 39576 and 39575), and 213 and 214 (no comments). `created >= 2026-10-18` 0; `labels = mpscalc-b171` 0. Every dedupe clause in the kit was run, and its counts and keys are written in.
- **Decision store:** there are 11 MPS `-1017` cards. 10 are ruled, and all 10 are already C-33…C-42 (delivered 14:51). The e6f92a5 hosted card is open. The 1017 quickquote and hpsmpoc cards are not MPS.

## Corrections to the commission
1. **Item 4: no Kam C-entry is owed.** `mpscalc-quote-list-deals-closed-title-1017` = a is already **C-42** (`CLARIFICATIONS.md:585`, commit `efb2b69`). The kit writes C-43 only if the hosted card is ruled by the time the seat runs.
2. **Records commit mechanics (R1, Tuesday to rule).** The commission says "records branch from fresh origin/main, plain push". But the records files live in the project ROOT repo, which has **no remote**. The code repo's tree at e6f92a5 holds none of them. B169 and B164 committed CLARIFICATIONS path-limited to the root `main`. The kit follows B169 and offers a local `records/b171` branch as the alternative. A push is impossible either way.
3. **`history.md:276`** (the brief B169 cite) is now `:299`. The kit cites `:299`.

## Design choices
- **B170-6/-7/-8 → one comment on MPSCALC-203.** It is the same path, the ticket is still open, and its acceptance names "a unique copy name per run". This follows the one-ticket-per-path rule.
- **B170-3/-4 → MPSCALC-214's merge comment**, referencing the open card. Neither gets a ticket, because the card is their gate (W2 item 6 is B170-4).
- **B170-5, OBS-1 and OBS-2 → 3 tickets labelled `needs-ruling`**, since no existing acceptance covers them. MPSCALC-110/-112 are RELATED to N01 and MPSCALC-171 is RELATED to N03.
- **Tuesday's rulings go in a `### Tuesday's rulings (coordinator, not Kam's; not C-entries)` section**, the form of Friday's `:374` precedent, not as C-numbers. It holds (a) the B170 kit `:313`, 15:45 (carve-out + E-vi Major) and (b) the daily note entry 17:04 (the tier-2 through-code completion check).

## Unmeasured / for Tuesday
- I could not establish from git whether the MPS `history.md` / `BACKLOG.md` / `JIRA.md` uncommitted diffs (+130 / +315 / +36) all belong to B169. I did not run `git diff` content; `--stat` only.
- `cockpit.sh status` printed no MPS row at all. That means `MPS-R3` is not in use, unless the status output simply omits panes.
- Whether the hosted card will be ruled, or a deploy seat run, before launch: the kit makes the seat check both, and stop if a deploy happened.
- `scan()` was not run by me. The seat runs it.
