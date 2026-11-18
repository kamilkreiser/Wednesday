# SWEEP-2305: Datasec tickets agents can build now, in lanes (read-only sweep, 2026-11-18 late evening)

Written by a read-only sweep drafter. Clock from `date`: 23:03:22 AEDT at start, 23:07:42 AEDT after the file was written. Form and instruments copied from `2026-11-18_SWEEP-0630_datasec-actionable-lanes.md` (read whole first): `jqdump.py`, `jdesc.py`, `jcom.py`, `rg.sh`, `bc.sh` copied into `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s291/sweep2305/` (each read before use; all GET-only). Fences kept: no Jira write, no GitHub write (`gh api -X GET` only), no git write, no mail, no `az`, no deploy, no `cd`, no token printed, `decision_queue.sh` used for `show` only, nothing under Secuura, WEDNESDAY or FRIDAY read. NexusAI is excluded tonight (a build seat holds `backend/server.js` and the jest lock): census line only.

## BLUF

**2 buildable keys in 2 lanes on 2 projects: HPSM-POC 1 key (HPSMPOC-510), MPS Calculator 1 key (MPSCALC-414), Security Composer 0, NexusAI not swept for lanes (census only).** Both keys are one-comment or two-docstring corrections, size S, with the ticket's own proposed default and no ruling needed. Predicate for "buildable": open (statusCategory != Done), not on any held or ruled-against line in the pickup or today's note (grep, section Excluded), ticket text says what to change, no new customer words, no client human's question, no deploy, no HP-tool integration. The morning sweep's MPS lane M-D4 (MPSCALC-364) is **landed**: MPSCALC-364 is Done (in `MPSCALC_done.tsv`; it left the open list since 06:30). MPSCALC-316 step 2 is still not built and is not buildable (its refusal sentence is customer words: the daily note of today, line 41, says "words are Kam's").

**No merge is blocked by the picomatch advisory any more.** Card `nexusai-picomatch-advisory-audit-1118` is ruled a and delivered; HPSM's own dev-tooling exception landed as HPSM #334 (main `deef2d76` shows its `web build (audit, ...)` check `success`); MPS's audit step (#214) is production-only and its main `51ed36eb` is green (8 of 8 check-runs listed `success`, 4 CodeQL analyses). Both Dependabot alerts, one on each of HPSM and MPS, are the same picomatch alert GHSA-fc5q-39xc-vjpf (high, scope development, no fix).

Recommended order (at most three, two exist):
1. **H-F: HPSMPOC-510** (two docstrings, one repository, size S, G3 with G2 fallback, can merge).
2. **M-E: MPSCALC-414** (one comment line, plus an optional one-cell doc wording, size S, G3, or G2 if the doc cell is touched; can merge after gate and CodeQL).
They are in different repositories and share no file: they can run side by side under the machine-load rule. A third lane does not exist: nothing else qualified.

## Board census

All counts are `board_count.sh jira` through `bc.sh`, JQL `project = <KEY> AND ( ... )`; every line printed `limit was 5001, so this is a real count and not a cap`. The same sets were dumped with `jqdump.py` (`rows` = `unique` in all twelve dumps).

| project | open now (statusCategory != Done) | Done (dump) | created since 2000 (count) | control: open + Done = created | open at SWEEP-0630 | change by `comm` of key lists | buildable keys | lanes |
|---|---|---|---|---|---|---|---|---|
| HPSM-POC (HPSMPOC) | 146 | 364 | 510 | 146 + 364 = 510 holds | 146 | gone HPSMPOC-356 (Done); new HPSMPOC-510 | 1 | 1 |
| MPS Calculator (MPSCALC) | 163 | 251 | 414 | 163 + 251 = 414 holds | 165 | gone MPSCALC-207, 364, 410 (all Done); new MPSCALC-414 | 1 | 1 |
| Security Composer (PCOMP) | 78 | 51 | 129 | 78 + 51 = 129 holds | 81 | gone PCOMP-74, 80, 81 (Done); none new | 0 | 0 |
| NexusAI (RD), census only | 871 | 130 | 1001 | 871 + 130 = 1001 holds | 870 | gone RD-1003 (Done); new RD-1004, RD-1005 (both To Do, label `records-pass-1118`, `security`) | not swept | 0 |

A control that can fail: the key-list arithmetic. HPSM 146 - 1 + 1 = 146 and MPS 165 - 3 + 1 = 163 and Composer 81 - 3 = 78 and NexusAI 870 - 1 + 2 = 871 each equal the measured open count (a miss of one key in any list would break one of them). Positive control for the Done lists: `RD-1003` is 0 hits in `RD_open.tsv` and 1 hit in `RD_done.tsv`; `HPSMPOC-356` is 1 hit in `HPSMPOC_done.tsv`. Updated since 06:00 today (dump): HPSM 4 rows, MPS 8, Composer 3, NexusAI 10; each was read by key (the Done moves above, the new keys, and MPSCALC-195, which got comment 41374 at 10:38).

Origin state today (all `gh api -X GET` under each project's own `GH_CONFIG_DIR`; `gh api user` login contained 'datasec': count 1 for each of the three): HPSM-POC main `deef2d76` (#335, merged 2026-11-18T01:05:53Z), 0 open PRs; MPS main `51ed36eb` (#215, merged 2026-11-18T01:01:38Z), 0 open PRs; Composer main `b4681297` (#130, unchanged since 11-15), 1 open: draft #85 `b330/sm316-content-catalogue` (HELD). Open Dependabot alerts: HPSM 1, MPS 1 (the picomatch alert above), Composer 0. Open code-scanning alerts: HPSM 0, MPS 0, Composer 0. Controls: `state=closed` printed each repository's last three merges (HPSM #335, #334, #333; MPS #215, #214, #213; Composer #130, #129, #128); the same Dependabot call form returned 1 for two repositories, so a 0 for Composer is not a silent failure of the call form. NexusAI new keys are census only (not read).

## Lanes

| lane | project | keys | owns (paths, line numbers printed at origin main today) | model row | gate | size | merge |
|---|---|---|---|---|---|---|---|
| H-F | HPSM-POC | HPSMPOC-510 | `scripts/deploy-package.py` (536 to 537 the `live_check` docstring; the summary lines at 566 to 570 are read, not edited); `infra/tests/test_deploy_hpsmpoc208.py` (460 the `plant` docstring) | L3 (`model-routing.md` line 82: two-file fix, spelled out), run on Sonnet (the "esc" column; Spark is not this seat's); C2 (line 92) if the builder finds it needs more | G3 (line 110: comment corrections, the builder's own red-proof plus a before-and-after test-id comparison); G2 (line 109) if Tuesday prefers a gate for a change in a deploy tool's file | S | yes: HPSM main is green with the dated exception; 0 open PRs |
| M-E | MPS | MPSCALC-414 | `tests/MpsCalc.Import.Tests/PanelOptionImportTests.cs` (12, the class comment); optional: `docs/IMPORTER.md` (17, one table cell) | L1 (line 80: one file, one hunk, spelled out), run on Sonnet; C1/C2 are not needed | G3 (line 110) for the comment alone; G2 (line 109) if the optional doc cell is touched (docs) | S | yes, after gate and CodeQL (MPS rule); 0 open PRs, 0 code-scanning alerts |

Model-routing line numbers printed today by `awk NR` over `fleet/specs/model-routing.md`: L1 line 80, L3 line 82, C2 line 92, G2 line 109, G3 line 110.

### H-F: HPSMPOC-510 (two docstrings in the deploy tooling)

Ticket scope, quoted: "Nothing behaves wrongly: both are words in docstrings. Recommendation: Correct both docstrings and change nothing else." The ticket adds "Fix shape (a proposal; the builder decides)", "No test row is needed", "Proposed default if nobody chooses: that change. Alternative: accept both as they stand". The default is the build, so no ruling is needed; only "accept as they stand" is the alternative.

Printed today at main `deef2d76` (rg.sh, `gh api` contents):
- `scripts/deploy-package.py:536` to `:537`: `"""Every file of the package's zip must be on the site with the same sha256; nothing else may be (Oryx's two aside).` and `Returns (summary line, [difference lines]); no difference = the site holds exactly this package."""` Still the old text.
- The code the docstring must now describe: `:83` to `:84` (`FAVICON_ROUTE_CACHE` and `SITE_ONLY_PATTERNS = {"web": (...), "api": ()}`), `:561` to `:562` (`visit` taken out of the differences), `:569` to `:570` (the second summary line, only when above 0).
- `infra/tests/test_deploy_hpsmpoc208.py:460`: `"""Add site-only files (a page visit's route-cache files) to the site, with a site time no package holds."""` Still without "not tested".
- Red-first for a docstring change: before and after, `git diff` over the three named files shows docstring lines only, and the whole infra suite compared by test id reads lost 0, added 0, changed 0 (the ticket's own proof); a before and after count of the old phrase `nothing else may be` (1 expected before, 0 after, with the unedited file as positive control).
- Standing line for every HPSM kit: this phase builds no integration with HP tools; nothing deploys. This lane edits the wording of a tool that runs at deploy time; it does not run it.
- Size S. Owns the two files only. Nothing else in HPSM-POC is open for a lane (section Excluded).

### M-E: MPSCALC-414 (one stale class comment)

Ticket scope, quoted: "Change the comment so that it says what the proof does with the colour panels (it counts the section's SKUs per sheet, checks the owed device and SKU pairs, and does not compare the records with the approved workbook or re-read the book); read each word against src/MpsCalc.Import/Parity/ParityProof.cs before it is used; no identifier, attribute, assertion or test row changes." Whether it is developer-only: the ticket cites entry C-109 (developer-only sentences are corrected from what the code does without the product owner's word review) and reads a code comment as developer-only; I read the same (the comment is in a test file; "no code or test reads its words").

Printed today at main `51ed36eb`:
- `tests/MpsCalc.Import.Tests/PanelOptionImportTests.cs:12`: `/// has to be typed in as an "Other" manual line. They are outside the approved workbook: the parity proof counts them only.` (the stale sentence; lines 9 to 13 are the summary block it sits in).
- What the code does: `src/MpsCalc.Import/Parity/ParityProof.cs:193` to `:201` (the owed (device, SKU) list and the `SequenceEqual` against the store's records, with the refusal at 201); the sentence already corrected by MPS #215 is `src/MpsCalc.Import/PriceBookImporter.cs:150` (read: it says the proof "counts the section's SKUs per sheet against the store and checks that the store holds exactly the owed (device, SKU) pairs, each once, but does not compare the panel records with the approved workbook and does not re-read the book"). The builder may reuse that sentence's shape.
- Optional in the same change, the ticket's own words: `docs/IMPORTER.md:17`, the last cell reads "They are not in the approved workbook, so `prove` counts them and compares the governed options only." (printed; the ticket calls it "narrower than the proof but not false" and "the only documentation byte this ticket may touch"). Default for the builder: do the comment only; touch the cell only if Tuesday says so (it moves the gate to G2 and the file is shared with no other open lane).
- Red-first for a comment change: count of the old phrase `counts them only` over the test file before and after (1 expected before, 0 after; positive control on the unedited file), the project's own build (0 warnings as errors) and the Import tests unchanged (198 of 198 per the 11:41 note, a number relayed, not re-run here).
- Size S. Owns one line in one test file (and optionally one table cell).

## Excluded

Each key was checked against both files by `/usr/bin/grep -i -n` (pickup and today's note); every DROPPED or HELD line was read (the greps printed 20 lines from the pickup and 12 from today's note: HELD cards for NexusAI audit-entry limits, RD-1003, RD-1000, HPSMPOC-356, the MPS 410/195 card, the HPSM picomatch exception card and the NexusAI one; the cards that touch a key below are named). Cards read by `decision_queue.sh show` only: `nexusai-picomatch-advisory-audit-1118` (status ruled a, delivered 14:13 by NexusAI #221) and `mps-410-openapi-195-wording-1117` (status ruled a, delivered 10:42).

| key | reason | source |
|---|---|---|
| MPSCALC-364, 410, 207, 411 | Done (landed): MPS #213 and #212 and records C-180; 364 is the morning's lane M-D4, now closed | `MPSCALC_done.tsv`; card `mps-410-openapi-195-wording-1117` delivered_artefact |
| MPSCALC-316 (step 2) | the refusal sentence in `QuoteEndpoints.cs` is customer-visible words; "words are Kam's"; not built | daily note 2026-11-18 line 41; pickup line 185 |
| MPSCALC-195 | now a records move, not a build: comment 41374 reads all seven clauses MET on the 11-18 ruling and leaves the ticket open only for "the coordinator's reading" of the engine-target sentence's placement (its words are not on the ticket: new words) | comment 41374 (read whole); pickup lines 148, 161, 167 |
| MPSCALC-120 | the accepted fix is a new short section in `docs/API.md` for the version practice: "queued with its own review" and is contract wording for API readers, not developer-only; no word of it is drafted | comment 41091 (read); 0 hits in pickup and daily |
| MPSCALC-200 | its table is already restated at `docs/IMPORTER.md:115` to `:116` (the A3 8-of-23 and A4 22-of-25 reads explained, 262 explained at 127); the ticket stays open on measurement and records, not a build I can name; 0 hits for "294" in the file (control: the 262 line printed) | `docs/IMPORTER.md` at main; comment of 2026-11-10 |
| MPSCALC-407 | items 1 and 2 landed in MPS #206; item 3 (contract wording) is the product owner's | comment of 2026-11-17 01:00 |
| MPSCALC-402 | its fixes change words of the roll-forward stop pack the product owner approved as written on 11-15 | comment of 2026-11-15 15:11 |
| MPSCALC-333 | clauses 1 to 3 landed (#110, #172); the remainder is a records reading | comments of 11-10 and 11-15 |
| MPSCALC-372 | landed as MPS #204; open until a deploy proves it (a deploy item) | comment of 2026-11-16 21:31 |
| MPSCALC lane-v keys (47 open with a `lane-v*` label), 233, 288, 368, 237, 314, 310, 315, 251, 135 and the rest of the MPS list | as the morning sweep: new words, decisions, designs or larger builds; none changed since 06:30 (the only new key is 414) | `MPSCALC_open.tsv`; SWEEP-0630 section 3 and 7 |
| MPSCALC-69 to 85 (`question-for-kam`, 10 keys listed) | Kam's questions | labels in `mps_nonv.txt` |
| HPSMPOC-509 | Done (HPSM #335) | `HPSMPOC_done.tsv` |
| HPSMPOC-356 | Done (left the open list since 06:30) | `HPSMPOC_done.tsv` |
| HPSMPOC HTML-phase keys (21) | "Once we agree what is in which phase, we will ticket"; carried from `hpsm_html_all.tsv` | SWEEP-0630 section 1 |
| HPSMPOC-470, 408, 431, 357, 246, 228, 207, 343, 503 | as the morning: a choice, product-owner words, hosted measurement or deploy | SWEEP-0630 section 1 (not re-read; no change in the 06:00 updated dump) |
| HPSMPOC In Progress 87, 90, 91 (Kam-owned C-30) | Kam | SWEEP-0630 |
| any HP-tool integration (Security Manager API, Fleet Threat, firmware, SIEM) | HPSM builds only this phase, no integration | commission |
| PCOMP-74, 80, 81 | Done (records pass C-153) | `PCOMP_done.tsv` |
| PCOMP-12 | landed in Composer #119 (a records move) | comment of 2026-11-10 20:12 |
| PCOMP-75, 79, 84 to 92, 76, 73, 72, 71, 70, 69, 68, 20, 19 | `held` label, or Guided: "No Guided work until you turn it back on" (PCOMP-75's comment says HELD) | `pcomp_list.txt`; comment of 2026-11-15 18:19 |
| PCOMP-66, 67 | test-only but on the held PR #85's branch (files not on main) and ruled "carried", struck from round 3 | tickets PCOMP-66 and 67 (read) |
| PCOMP-9, 10, 11, 13, 16, 18, 25, 28, 93 | a design call, a deploy or environment item, or contract words (PCOMP-11 needs "two new words" and a contract change) | tickets PCOMP-9, 11, 93 (read); morning for the rest |
| PCOMP-23, 123, 65, 78, 128, 129, 46, 94, 29 to 61 | unchanged from the morning: held PR #85 overlap, words, `needs-kam`, sample-policy content | SWEEP-0630 section 2 |
| Composer draft PR #85 | held | pickup |
| RD-1004, RD-1005 (new), and all other RD keys | NexusAI is excluded tonight (build seat holds `backend/server.js` and the jest lock); census only | commission |
| Vision, myPKI, CypherKey, Lead_Bot | skipped | commission |

## Questions for Tuesday

1. **MPSCALC-414: touch `docs/IMPORTER.md:17` too?** Default: no; do the comment only (G3), and file the doc cell as a later key. It would raise the gate to G2 and the ticket calls the cell "not false".
2. **HPSMPOC-510 gate:** G3 (the builder's red-proof plus the test-id comparison) or G2? Default: G3, because it is two docstrings and the proof "lost 0, added 0, changed 0" is measurable; raise to G2 if you want a gate on any edit in the deploy tooling.
3. **MPSCALC-195's last owed item (placing the engine-target sentence in the docs):** the words are not on the ticket; default is a records reading, not a build. Do you want a words card?
4. **MPSCALC-120 (the version-practice section):** default: not built until its words are drafted and approved.

## How measured

**FOUND.** 2 buildable keys (HPSMPOC-510, MPSCALC-414); 0 in Composer; the morning's M-D4 (MPSCALC-364) is Done. Counts and arithmetic in the census table. Merge state: no picomatch block on HPSM or MPS (cards and checks above).

**TESTED.** (a) Four project counts: `bc.sh` (wrapper of `board_count.sh jira`) for open and created-since-2000; Done from `jqdump.py` `statusCategory = Done` dumps; control open + Done = created in all four (510, 414, 129, 1001). (b) Key-list differences by `comm` of today's `*_open.tsv` against `s288/sweep0630/*_open.tsv`; the control is the arithmetic in the census. (c) Ticket text and comments for HPSMPOC-510; MPSCALC-414, 316, 195, 120, 200, 333, 372, 402, 407; PCOMP-93, 12, 11, 9, 67, 66, 75 by `jdesc.py` and `jcom.py` (descriptions capped at 1,100 to 2,200 characters, so tail text of some tickets is unread; comment 41374 of MPSCALC-195 read whole). (d) Lines at main by `rg.sh` (`gh api -X GET repos/<repo>/contents/<path>` at `main`); the HPSM line numbers named in the ticket (`:83` to `:84`, `:561` to `:562`, `:569` to `:570`) match main, a positive control that the ticket's reading is current. (e) `gh api -X GET` for commits, pulls, Dependabot and code-scanning alerts and check-runs on `deef2d76` and `51ed36eb`; `gh api user` count 1 on each. (f) `/usr/bin/grep -i -n` over the pickup and today's note for the keys and every DROPPED or HELD line (two greps first failed: a regex repeat count over 255 and a harness output cap; both were rerun narrower and printed into files in scratch). (g) `decision_queue.sh show` for the two cards.
**NOT tested:** the 36 other MPS `lane-v` keys, PCOMP keys beyond those read (the morning's reads are carried, not redone), the other 70-odd NexusAI keys, whether HPSM's infra suite compares as the ticket says (not run; the ticket's number is relayed), whether the MPS Import tests are 198 of 198 (relayed from the 11:41 note), whether a PR on either repository would pass the audit check (not opened; only main's green checks were read), the live feedback stores (fenced as in the morning; this is not "0 items"), Vision. `decision_queue.sh prior --help` printed `ERROR: prior: unknown or incomplete flag: --help` (it takes `--id`, `--title`, `--client-project`), so `prior` was not used; only `show` was.

**HOW.** Instruments: `jqdump.py`, `bc.sh`, `jdesc.py`, `jcom.py`, `rg.sh`, `gh api -X GET`, `/usr/bin/grep`, `awk`, `comm`; scratch (dumps, ticket reads, card prints) in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s291/sweep2305/`. Errors met: two hook refusals (a `cd`, a `==` word and a `set -- $var` split; each rewritten under `bash <<'EOF'`), one `LC_ALL` sort failure on a multibyte character (rerun with `LC_ALL=C awk`), the grep and output-cap errors above. No data harmed; nothing written to any board, repository or host. Clocks from `date`.

READ-WHOLE-BY-TUESDAY: ____
