STARTABLE: YES

# B1440 to B1444 drafter report: HPSM-POC, the product owner's 10 Nov card rulings (drafted 2026-11-10 03:3x AEDT)

## BLUF
- Five kits, B1440 to B1444. Three builders (L1 web follow-on, L3 API follow-on, a separate retention and ledger-audit kit because it is L), one Sonnet drafting kit for the expert content, and one records kit (seat R201). **No L2 follow-on kit:** none of the ruled items needs `web/src/server`, `web/src/lib`, `web/src/api` or `web/src/data`. The one candidate, the page data of HPSMPOC-410 that carries the full name, is not covered by the ruling. B1440 writes `NEEDS-SHARED` if it meets that.
- **B1443 (drafts) can launch now.** The others each say what they wait for at the top. B1440 waits on B1392 landed and PR 297 merged. B1441 waits on B1394. B1442 waits on B1394 and B1395. B1444 waits on B1397 finished and landed.
- **Ports: 9740-9799 has no free block of 10.** The MPS kits B1400 to B1405 hold 9740-9799 in six blocks. 9800-9939 is held by MPS, Composer and NexusAI kits. I wrote **9940-9949 / 9950-9959 / 9960-9969** into the three builders (0 listeners, 0 kit hits). They are outside your range, so Q1.
- **Records: no key overlaps R197**, but both seats append to `CLARIFICATIONS.md` and each reads its next numbers when it writes. So B1444 is sequenced after R197 has finished and landed. Expect C-315 onward.
- **One card was not ruled.** `facts-only-kam-1110` reads `status: open`, `choice=None`. Kam's note text is RELAYED from your commission only: it is not on the card. The card's summary cites it as "your 03:18 note".
- **Ruling times differ from the commission.** The commission says 03:25-03:27. `ruled_ts` reads 03:25:53 and 03:25:57 (sme-content, small-wording), then 03:29:16 to 03:29:35 (the other six). The kits carry the measured times.

| Kit | Seat | Tickets | Waits on (launch line) | Size | Model (routing row) | Ports |
|---|---|---|---|---|---|---|
| B1440 `2026-11-10_B1440_SEAT-H150_hpsmpoc-web-ui-rulings.md` | H150 | 417, 410, 438 (slot), 324 web mock mirror, 392 read-only check | B1392 READY and landed, and PR 297 merged (AppShell.tsx) | S-M | Sonnet (line 92, C2) | 9940-9949 (proposed) |
| B1441 `2026-11-10_B1441_SEAT-H151_hpsmpoc-api-hidden-characters.md` | H151 | 324, 257 | B1394 READY and landed | S-M | Sonnet (line 92, C2) | 9950-9959 (proposed) |
| B1442 `2026-11-10_B1442_SEAT-H152_hpsmpoc-retention-ledger-audit.md` | H152 | 100, 117 (180 excluded) | B1394 and B1395 READY and landed | L | Opus (line 94, C4) | 9960-9969 (proposed) |
| B1443 `2026-11-10_B1443_SEAT-H153_hpsmpoc-sme-content-drafts.md` | H153 | 31, 37, 44, 46, 55, 87, 393, 394, 395, plus 390 role definitions | none (launch now) | L | Sonnet (B1396's routing; line 98, C8, nearest row) | none |
| B1444 `2026-11-10_B1444_SEAT-R201_hpsmpoc-records-rulings-1110.md` | R201 | 25 keys: 6, 31, 37, 44, 46, 51, 55, 87, 91, 100, 117, 180, 203, 257, 324, 390, 391, 392, 393, 394, 395, 401, 410, 417, 438 | B1397 finished and landed; no live Jira or CLARIFICATIONS writer | M | Sonnet (line 97, C7) | none |

Records-only rulings (no build): 401 (accept the 4.5 px), 91 (download and preview only), 203 (keep as is), 391 and 392 (as stated), 6 and 51 (facts), 180 (not named by the ruling).

## Facts re-measured (instrument; control)
- **Cards.** `bash .../tools/decision_queue.sh show <id>`, once per exact id, each into its own scratch file. Nine files, each holds its id exactly once (`grep -c -F`). `list` was never run. Choices: sme b, small-wording a, layout a, hidden a, design a, defer b, product-sends a, keep a, facts-only open.
- **Code main** = `fa401da9f7bdab21c46ad9717c964433a2d22650` at 03:36:13 AEDT, by `gh api -X GET .../branches/main`. Tree: 1491 blobs, `truncated` False. This matches lanes.md's count.
- **PR 297** is open, not merged, head `e9a36f7e`. lanes.md read `60639d15`, so H147 has pushed since. It has 16 files, one of them `web/src/components/shell/AppShell.tsx` (`pulls/297/files`).
- **Analysis main** = `6670d18d` (03:38). `CLARIFICATIONS.md` has 5769 lines. The highest heading is `### C-311` at :5762; the control `### C-263` is found once. There are 0 open analysis PRs.
- The landing-form line is at `CLARIFICATIONS.md:3617` ("The landing form is a head-pinned squash"), by `grep -n -i`.
- **File pointers at fa401da9**, each from `grep -n` or `awk NR` over the raw file fetched by `gh api ... contents?ref=fa401da9`:
  - `RoadmapScreen.tsx:86` holds the rule line. The ticket's `:75` was read at an older main.
  - `AppShell.tsx:165-166` holds the logo `Link` and the `HpLogo` with `h-7 sm:h-10`.
  - `PartnerDashboard.tsx:184` holds Upcoming activity.
  - `useCustomerShownAs.ts` has 41 lines.
  - `GlobalNav.tsx:51` holds `label: "Revenue"`, the control for the 392 check.
  - `CustomerEndpoints.cs:79,198` hold `customer.name-blank` / "name is blank.". The ticket's `:77,196` were read at an older main.
  - `FeedbackFiles.cs:136-139` holds `DeviceStems` and the FormKC fold. `:125` declares `Reserved`, with the superscript 1-3 entries at `:129`. `:198` is the invisible-only test.
- **Migrations at fa401da9:** Assessment has 35 SqlServer and 37 Sqlite tracked files (tree `grep -c`).
- **Jira, 25 keys by REST GET** through my own read-only reader in scratch, which reads the token in-process and never prints it. Control: `/myself` 200, `HPSMPOC-99999` 404. All 25 are Backlog except 87 and 91, which are In Progress. None has a resolution.
  - HPSMPOC-6 comment 39918 (2026-10-23) records "there is no deputy". Kam's new note supersedes it. E9 records that and edits nothing.
- **Ports.**
  - `lsof -nP -iTCP:9740-9799 -sTCP:LISTEN` printed 0 rows, but the kits hold the range.
  - `lsof` for 9940-9969 printed 0 rows, and for 9680-9699 printed 0 rows. Control: 15 listeners machine-wide.
  - Word-boundary scan of the **47 non-`.pre-` SEAT kits of 9 and 10 Nov**:
    - `9[67]xx`: MPS B1400-B1405 hold 9740-9799.
    - `9[89]xx`: MPS B1406-B1410 hold 9800-9849, Composer B1420-B1424 hold 9850-9899, NexusAI B1430-B1434 hold 9900-9939, and B1391 names 9970-9979.
    - `99[4-6]x` and `96[89]x`: 0 files. Control: `9939` is found in 2 files.
  - Live panes (`tmux list-panes -a`): %0 tuesday, %1 fleet-monitor, %11 H147, %12 D56, %13 H142, %14 H143, %15 H144, %16 H145, %17 H146. There is no R197 pane yet.
- **Seat and B-numbers.** No `SEAT-H148`..`H159` or `SEAT-R199`..`R209` kit exists, and no `2026-11-10_B144*` file existed before mine (`ls | grep`). Control: 8 `SEAT-H14[0-7]` files.
- **Stamp slots, unstamped** (`grep -c` for four underscores): B1440 has 7, B1441 6, B1442 9, B1443 6, B1444 9. Each REFUSE 1 states its count. `@MAIN@` appears 4 times in each of B1440, B1441 and B1442 and nowhere else.
- **Model ids** come from `models_latest.json` (checked 03:28:26): opus `claude-opus-5-5`, sonnet `claude-sonnet-5-5`. `brief_seat.sh:24` defaults to opus. Every launch line writes its level inside the quotes.

## D-decisions (mine)
- **D1 Draft location.** The drafts go to the analysis folder `1_Project_Definition/Architecture/content/2026-11-10_sme-drafts/`, not `web/src/content`. The ruled detail says "never loaded until you approve", and `web/src/content` is loaded by the product and owned by L1. The project's earlier `_DRAFT-FOR-KAM` drafts sit in `Architecture/content/`. L5's glob `Architecture/2026-11-10_*` does not cover that sub-folder, so it can launch now.
- **D2 The 390 role definitions go into B1443.** The design ruling's item (1) asks for a written definition. That is drafting, not a build.
- **D3 HPSMPOC-438 is gated by a B1440 slot.** The ruled detail says the sentence is posted on the ticket for review before it is built. So B1444 posts 438 first, and B1440's `438 BUILD` slot defaults to HOLD.
- **D4 324 reuses the existing problem code and words** (`customer.name-blank`, "name is blank."), so no product word is invented. The web mock mirror goes in B1440, and its test is a new file because `customer-name.test.ts` is L4's.
- **D5 257 builds the ruled words literally.** A width fold keeps `CON`+U+FF0E refused, although the ticket lists it as an over-refusal. B1441 pins that row and reports it for the records.
- **D6 HPSMPOC-180 is excluded.** The chosen option (b) names "retention and ledger audit" only. B1444 records that 180 is not settled by the ruling.
- **D7 B1442 puts the risky choices behind slots, each defaulting to HOLD or NONE.**
  - MIGRATION: the ruled detail itself says "Needs a migration; migrations are frozen.".
  - RETENTION PERIOD: "12 months proposed" appears only in the card's summary.
  - ERASE: the value `client (erased)` is the ticket's, not the card's.
- **D8 The comments cite their entry.** B1444 allows `entry C-<n>` for its own nine numbers only, as an exception to B1397's ban. The commission asks for the citation, and earlier comments cite entries this way (40288). The ban stays for every other C-number.
- **D9 The `DRAFT-FOR-KAM` marker.** B1443 uses it in file names and first lines, verbatim from the ruled detail. Its name scan allows that one token and nothing else. Commit messages do not carry it.
- **D10 Names in the records.** E9 quotes Kam's note verbatim, including the deputy's name, in `CLARIFICATIONS.md` only. The file already carries names (the C-30 heading). No name goes into a Jira text. Card-option details that name "Tuesday" are paraphrased and marked, because B1397's closing check bans that word in added lines.
- **D11 Moves.** Only 401, 203, 391 and 392 may move, under `MOVE=CLOSE-IF-MET`, which defaults to COMMENT-ONLY. Every other key is comment-only.
- **D12 Builder models.** B1440 and B1441 are routed Sonnet (C2) even though lanes L1 and L3 ran Opus. B1442 is Opus (C4, a data-destroying path).

## Q-questions for Tuesday (each with a default)
- **Q1 Ports.** 9740-9799 is fully held by the MPS kits. Use 9940-9949, 9950-9959 and 9960-9969? *Default: yes.* All three read 0 listeners and 0 kit hits. 9680-9699 is the fallback, also 0 and 0.
- **Q2 B1442 MIGRATION.** `ALLOWED` or `HOLD`? *Default HOLD as written.* I recommend ALLOWED: the chosen option's own detail says it needs a migration.
- **Q3 B1442 RETENTION PERIOD.** `12 months` or `NONE`? *Default NONE*, which builds the purge and leaves it idle. ERASE is *default HOLD*.
- **Q4 B1444 MOVE.** Do the decision-only moves (401, 203, 391, 392) fit C-263's "merged to main" Done rule? *Default COMMENT-ONLY.*
- **Q5 B1440 builder model.** Sonnet (C2), or Opus to match L1? *Default Sonnet.* 410 is a display-privacy change; if you read it as a security surface, use Opus.
- **Q6 HPSMPOC-410 page data.** Do you want an L2 or L3 follow-on for the full name in the customer page's data? *Default: no.* It is not ruled.
- **Q7 facts-only card.** It is still open. Its 10:00 default covers "baseline as not supplied". *Default:* B1444 records the note and the "not supplied" fact without a ruling. If you rule the card first, nothing in the kit changes.

## UNMEASURED
- Which file holds the customer profile's "Customer name" field (410). B1440 finds it by `git grep`.
- Whether the web mock refuses a whitespace-only name today. B1440 checks first and STOPs that item if it does not.
- Whether CI's SQL Server image supports ledger tables. B1442 Step 1.2 checks, and STOPs if not.
- Whether any product path updates or deletes audit rows. B1442 Step 1.1 checks, and STOPs if one does.
- Whether the analysis deploy key can push a new branch for B1443. I took the path from B1396:84 and did not test it.
- What B1392, B1394, B1395 and B1397 will change before these launch. Each kit re-reads main in Step 0.
- The Composer `bundle.json` that B1443 might cite is not tracked in the analysis tree. If present, it is local only. Not checked.
- I did not read the project `CLAUDE.md`. The kits tell each seat to read it.

## Outside the fences (disclosure)
- I wrote six files, five kits and this report. DRAFTER_RULES says "ONE brief file". The commission asked for five kits, and I followed the commission.
- In my session scratchpad (not the project) I wrote a read-only Jira reader. It sends GET only and refuses any JQL not of the form `project = HPSMPOC AND ( ... )`; I used issue GETs and `/myself` only. I also wrote the card, Jira and file reads to scratch.
- `gh api -X GET search/code` ran 11 queries. The 11th answered **403, search rate limit**. I stopped searching and made no retry. No other GitHub endpoint failed. Core remaining was 4714 at 03:38.
- No `cd`, no git write verb, no mail, board, Artifact or Docs. No token was printed: the reader prints only status, keys and text.
- The template B1392 shows as modified in `git status` (Tuesday stamped it). I only read it.
