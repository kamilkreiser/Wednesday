# Drafter report: B526-B532 (HPSM-POC H6, MPS M5-M8, Composer C1 and R24)

Drafted 2026-10-23 13:05-14:20 AEDT by Tuesday's brief drafter (Sonnet 5.5, row C8). Wrote only the 14 brief files below and this report. Nothing stamped, launched, sent, posted or merged; no Jira write; no HTTP to any app or hosted host (Jira GETs and `gh api -X GET` only). No other drafter had taken B526-B532 (free numbers confirmed at 13:10 and 14:15; the folder holds B489-B525 only), so the numbers are as asked.

## BLUF

Seven briefs, each with a byte-identical `.pre-stamp` (verified with `cmp`). All 36 REFUSE fact-check strings were run against the repos at the stamped shas: each counts exactly as the brief says (one deliberate exception: the HPSM `e.status === 400` string reads 0 on purpose, it is the "PR #197 merged" gate; and one string I had wrong in B531 and fixed). The intersection program (below) prints **0 shared** for every new brief against every live seat, every open PR, and the new briefs against each other, including the two partition updates received at 13:5x (B522 ADDENDUM-1's `B103DealUsageCountedLineTests.cs`, B520 ADDENDUM-1's `SourceDocumentChecks.cs`, which was already in B520's list). Four things Tuesday should know first:

1. **B526 is not what the dispatch assumed.** The API already refuses U+FEFF/U+2028/U+2029 (and U+000B/U+000C) as sent, for the customer name and the feedback comment (HPSMPOC-177/-178 are on main). The gap is in the WEB: it calls `trim()` first, and JS `trim` silently drops those five characters. So B526 is a web-only brief (7 paths, no `api/**` file, no new word): stop trimming the five, and the API's existing sentence answers. It must **launch after PR #197 merges** (the customer-name 400 shows its message only through B513's `describeFailure` fix); the brief has a mechanical REFUSE check for that.
2. **PCOMP-36..39 are not "blocked" in Jira and not ready either.** The PCOMP workflow has only Backlog / Selected for Development / In Progress / Done; no blocked status exists. All four issues' State text names TWO waits: L0-3 approved (cleared by the owner's 13:35 words) and **L1 (the content loader, not built; code PR #85 open under hold K6)**. B532 therefore carries a Stamp slot `PCOMP-36..39 TRANSITION` (RULE default = move none while L1 is unbuilt; ALL = the coordinator's words literally; NONE). Decision-shaped, see below.
3. **The owner's card was withdrawn, not ruled.** `composer-baseline-template-draft-review-1023`: status `withdrawn` 13:37:07, `choice=None`, his words are the withdrawal reason. B532 records exactly that and does not write "ruled a/b".
4. **MPS heavy slots:** slot 1 holds a dead B483 (B522 ADDENDUM-2 now orders its quarantine); slots 2 and 3 are held by B520 and B518 (read 13:40). With four more MPS seats, stagger the launches (load1 read 10.23).

## The briefs

| Brief file | Seat (pane) | Branch | Model row, gate | Ports | Lines | Open stamp lines (`grep -c '____'`) |
|---|---|---|---|---|---|---|
| `2026-10-23_B526_SEAT-H6_hpsmpoc-edge-characters-refused.md` | `Datasec/HPSM-POC-H6` | `b526/hpsmpoc-edge-characters-refused` | Sonnet `claude-sonnet-5-5`, C2; G2 Sonnet tier 2 | 8700-8709 | 116 | 8 (7 slots + last) |
| `2026-10-23_B527_SEAT-M5_mps-bom-fleet-identity-class-labels.md` | `Datasec/MPS-M5` | `b527/mps-bom-fleet-identity-class-labels` | Sonnet, C2; G2 Sonnet tier 2 | 8710-8719 | 124 | 8 |
| `2026-10-23_B528_SEAT-M6_mps-reconciliation-hardening.md` | `Datasec/MPS-M6` | `b528/mps-reconciliation-hardening` | **Opus** `claude-opus-5-5`, C3 (money verifier design), `BRIEF_SEAT_LEVEL=opus`; G1 Opus tier 1 | 8720-8729 | 123 | 8 |
| `2026-10-23_B529_SEAT-M7_mps-importer-panel-parity.md` | `Datasec/MPS-M7` | `b529/mps-importer-panel-parity` | Sonnet, C2; G1 Opus tier 1 (importer) | 8730-8739 | 122 | 8 |
| `2026-10-23_B530_SEAT-M8_mps-feedback-server-hardening.md` | `Datasec/MPS-M8` | `b530/mps-feedback-server-hardening` | Sonnet, C2; G1 Opus tier 1 (download headers) | 8740-8749 | 122 | 8 |
| `2026-10-23_B531_SEAT-C1_composer-flaky-verify-test-split-comment.md` | `Datasec/Security-Composer-C1` | `b531/composer-verify-test-wait-split-comment` (code repo) | Sonnet, C2; G2 Sonnet tier 2 | 7660-7669 (reserve) | 105 | 8 |
| `2026-10-23_B532_SEAT-R24_composer-records-fold-approval.md` | `Datasec/Security-Composer-R24` | no code branch; local `records/b532` in the root repo | Sonnet, C8 (records/fold, as B428); no gate | none | 106 | **9** (8 slots + last: the extra slot is `PCOMP-36..39 TRANSITION`) |

Model line in each: `model: <id> -- <row> -- P1-P4 none -- gauge 95% (Tuesday no-90% grant)`; ids from `models_latest.json` (checked 2026-10-23 13:26: sonnet `claude-sonnet-5-5`, opus `claude-opus-5-5`). Stamp slots are one per line ending in `____` (stamp_brief.py label matching); the B532 extra slot is a labelled line like B513's B478-4 slot. Drafter suggestions for hard stop / target READY: B526 4h/2h, B527 8h/5h, B528 7h/4h, B529 5h/3h, B530 7h/4h, B531 3h/2h, B532 3h/90min. Main at drafting: HPSM-POC `4db192b025732a35e6070a7d235ba93f26b8e23a` (stale: expected to be later at B526 launch), MPS `e027ebd09640cad95d5b18716c6e6fb8e870835e`, Composer code repo `308b7aa60cd8d2a8576b29e0422538cbaf140f24`, Composer root `main` `12a8bfad7d786939897556f71421576e94e312cf` (all read by `ls-remote` or `rev-parse`; the local `origin/main` refs in HPSM-POC and MPS equal the remote).

## Per-ticket: keep / narrow / drop (file:line at the stamped sha)

**B526 (HPSMPOC-323, item B478-5 only).** KEEP, REDIRECTED. API refuses as sent: `Requests.cs:146-148`, `FeedbackEndpoints.cs:233,243`, set `FollowUpModels.cs:195-198`. Web drops them: `CustomerManagement.tsx:106`, `customer/api.ts:50` (a second trim the lane screen did not list), `FeedbackButton.tsx:31,130`. The class, computed by `node -e` over the repo's own table: JS `trim` removes 25 scalars, **5 are refused: U+000B, U+000C, U+FEFF, U+2028, U+2029** (the ticket names three; VT/FF are the same class). Authority: `hpsmpoc-refuse-more-invisible-characters` = a (2026-10-01), extended to name and comment by `hpsmpoc-class-c-wording-six-tickets-1022` = a (2026-10-22), which the dispatch did not cite; both quoted. Keep-list rows (ZWJ, ZWNJ, NBSP, SHY) are in the brief. Not built (listed, with file:line): other `trim()` sites (contact name, message, narrative, partner calculator name, snapshot name).

**B527 (M5), 5 tickets.** -198 KEEP, REFRAMED: `FleetGrid.tsx:84` is `key={i}` (index), not a line-number key as the ticket says, so the first job is a measure (pin or product defect); 14 `it(` lines vs the ticket's 17. -199 KEEP: `bomModel.ts:105-118` by number; the ticket's `:86-99` is stale; existing by-number functions kept (existing rows call them), new by-position functions added. -208 KEEP: `PurchaseBomEditor.tsx:405` (ticket's `:341` is stale); eight labels exist in `InventoryScreen.tsx:16-25`, no new word. -301 KEEP with a stop clause: `consolidatedBomModel.ts:39`; if the result line lacks the inputs and a caller outside Yours is needed, narrow. -220 KEEP: `InventoryPicker.tsx:51` groups options only; inventory screen's "Fits <SKU>" is not Yours.

**B528 (M6), 3 tickets.** -291 KEEP: `PurchaseRecomputation.cs:85` (cost has no contract-scale twin; revenue/margin twins at `:88-89`); design constraint: no tenth measure, no type change (`ReconciliationTypes.cs` not Yours), tolerance stays one cent inclusive (D-13 a, CLARIFICATIONS.md:681). -292 KEEP: `ReconciliationTests.cs:457-476`, augment with a reflection guard, keep the old test. -294 KEEP, split: docs half certain (`RECONCILIATION.md:14-16`, `QuoteReconciler.cs:10-12`), cross-check half only if it fits existing `Figure` outcomes (`PurchaseRecomputation.cs:120`).

**B529 (M7), 2 tickets.** -302 KEEP: `ParityProof.cs:189-190` count-only comparison; may need a staff-only sentence (WORDS-DRAFT). -303 KEEP, WIDER FILE SET: `SynnexBook.cs:309,334-336`; the only caller of `PanelRows` is `PriceBookImporter.cs:659`, so that file is **added to Yours** (screen's list lacked it); the existing Warning (`:672-676`) is reused byte for byte; ticket's second option (fixed heading list) not built (real book unmeasurable: `.local/` is confidential).

**B530 (M8), 5 tickets.** All cites in the tickets are from old mains; re-measured: -122 `FeedbackEndpoints.cs:303-333` (refusals `:307,:311,:317,:323`, headers `:327-330`) KEEP; -124 `FeedbackStore.cs:398,417-422` KEEP (deterministic interleaving instead of a wall-clock row); -125 `FeedbackStore.cs:254-255` KEEP; -102 `FeedbackEndpoints.cs:277,286` vs `FeedbackTickets.cs:293` KEEP (atomic store transition, deterministic seam); -97 NARROWED to MEASURE FIRST: the overlay's fix helpers are private in `CatalogueOverlayStore.cs` (not Yours), CI is Linux (NFD/NFC rows must ask the filesystem), likely outcome "not reproduced, rows kept as pins". `FeedbackTickets.cs` added to Yours (screen's list lacked it) for -102's seam.

**B531 (C1), rows 363 and 364.** Both KEEP, both reproduce at `308b7aa6`: `b116-s10-verify-dom.test.tsx:88-90` (five `setTimeout(0)` turns) and `:120`; comment `s47-crf2-linear-detector.test.ts:245-254`, `SINGLE_SPLIT_BOUND` `:255`. Red proof is a slowed-mock variant (deterministic), not only the hog. Comment-only proved by program.

**B532 (R24).** Fold KEEP: `records/b511` then `records/b521` (`--no-ff`, the B428/B344 precedent; the verb is not written in `CLAUDE.md`, it is the merge history). Collision set measured: 7 added paths, **4 exist in the root** (3 byte-equal, the B521 STATUS root copy is append-only, 27,058 vs 29,546 bytes), 3 absent; 3 modified paths clean. Added by the coordinator at 13:4x and built in: approval record C-100 (next free, on no branch), template status taken off by keeping the path and changing the status inside (a rename would break the references in BACKLOG, history, CLARIFICATIONS, the B328 and B339 files; C-40 is the precedent), BACKLOG State appends on #330 and #336-#339, `records/b532` folded as a third merge, PCOMP-30 comment + owner-wait label removal, PCOMP-36..39 comments. **Stale PCOMP epic descriptions: NOT IN THIS BRIEF.** B521's STATUS (FOR TUESDAY item 4) says only that PCOMP-1..-3 are stale by #329, #290 and #236 and that editing an existing description was outside its fence; it gives no way to update them, and B532's Jira fence forbids description edits.

## Corrections to the lane screen (all measured)

- H2/B478-5 and the API: the API half of B478-5 is already built; the work is web-only (above). Open PRs are now HPSM-POC #196, #197, #198; MPS #98 (the screen said 0 and 0).
- M5: `FleetGrid.tsx:84` key is the index; `:82` and `:86-99`, `:341` cites stale; three new test files added so new rows have a home.
- M7: `PriceBookImporter.cs` added. M8: `FeedbackTickets.cs` added; "FeedbackStore.cs is frozen" (B65) is obsolete.
- M6: tests list gains a new-file glob `ReconciliationB528*.cs`.
- Composer: the code repo `datasecau/HPSM-light` is now `datasecau/Datasec-Security-Composer`; the local clone's `main` is stale (`0b2fca43`), only `origin/main` is current. The root repo is a separate records repo with no remote.
- M16 (B522) is outside the screen's intersection check: checked here, 0 shared.
- Heavy slots: slot 1 orphaned B483, slots 2 and 3 busy (B520, B518).

## The intersection program (output, run 13:55-14:15; Python over `git ls-tree` at the stamped shas, globs expanded against the trees, live seat lists copied from the live briefs, PR files from `gh api`)

```
repo-lane intersection (new brief Yours x every live seat/PR path):
  B526 HPSM  ( 7 paths) vs H3 B514   ( 1): shared 0
  B526 HPSM  ( 7 paths) vs H4 B515   ( 7): shared 0
  B526 HPSM  ( 7 paths) vs H5 B516   ( 3): shared 0
  B526 HPSM  ( 7 paths) vs B513 nominal Yours (H2, branch pushed) ( 5): shared 2 ['web/src/components/customer/CustomerManagement.tsx', 'web/src/components/feedback/FeedbackButton.tsx']
  B526 HPSM  ( 7 paths) vs PR196 B510 ( 4): shared 0
  B526 HPSM  ( 7 paths) vs PR197 B513 actual ( 2): shared 0
  B526 HPSM  ( 7 paths) vs PR198 B512 ( 3): shared 0
  B526 HPSM  ( 7 paths) vs b501 parked ( 3): shared 0
  B527..B530 (13, 6, 5, 5 paths) vs M1 PR98 live files / M1 nominal / M2 B518 / M3 B519 / M4 B520 (+ADDENDUM-1) / M16 B522 (+ADDENDUM-1, 4 paths): shared 0 in all 24 pairs
  B531 C1    ( 2 paths) vs PR85 b330 (57 files): shared 0 ; vs PR86 dependabot (2 files): shared 0
  B532 R24   ( 7 paths in the root repo) vs live Composer seats: none live; shared 0
among the seven new briefs (same-repo pairs): B527xB528, B527xB529, B527xB530, B528xB529, B528xB530, B529xB530: shared 0 each
control (planted docs/ENGINE.md vs M1): ['docs/ENGINE.md']
control (planted B103DealUsageCountedLineTests.cs vs M16): ['tests/MpsCalc.Api.Tests/B103DealUsageCountedLineTests.cs']
TOTAL shared, excluding the B513 nominal read-only lines: 0
```

The only non-zero line is B513's own brief listing `FeedbackButton.tsx` and `CustomerManagement.tsx` as READ-ONLY paths in its Yours; B513's actual diff (PR #197, `compare` = 2 files) does not contain them. B526 says so from both sides and sequences itself after PR #197 anyway (functional dependency). B532's dependency on B531 is none (different repos/trees).

Open ports: HPSM and MPS blocks 8700-8749 and Composer 7660-7669 all `lsof` empty at 13:4x; the gate briefs hold 8670-8699, so the new blocks begin at 8700.

## Decision-shaped for Kam (card candidates, not carded)

1. **PCOMP-36..39 after the template approval.** Question: the four tickets are in Backlog with two stated waits; one (approval) is cleared, the other (L1 loader, PR #85 on hold K6) is not. Options: (a) RULE: comment only, move none until L1 is built; (b) ALL: move all four to Selected for Development now (the building of data files on branches is already permitted by C-92); (c) NONE. **Default: (a)**, because (b) would mark as ready what its own text calls unbuilt-dependent; (b) is a one-word change in B532's stamp slot if the coordinator prefers it.
2. **Does "approved" cover the words?** C-89/C-95 keep the why and customisation texts as the sample's source wording until a words card (L2-3). The owner's 13:35 words approve the template. Options: (a) values approved, words still go to the L2-3 words card (what B532 records); (b) he also waives the L2-3 rewording. **Default: (a).**
3. **PCOMP-30 to Done?** After the approval its job is finished. Default: leave it for the coordinator (B532 removes the owner-wait label only).

## Lane candidate for PCOMP-36..39 (not drafted, as asked)

One Composer build lane ("L2 baselines") on one seat, since all four tickets say "a new `content/baselines/` data file (+ README)": L2-1 (PCOMP-36, row #336) the per-item class/target/severity/remediation/unsupported values from the approved template; L2-2 (PCOMP-37, #337) the 28 CONDITIONAL/MANUAL rows with `variable` and the Composer question or control decision (C-54); L2-3 (PCOMP-38, #338) Datasec's own why/customisation texts and the 8 section owner lines (WORDS-DRAFT: the words gate first, K9/C-95); L2-4 (PCOMP-39, #339) solution-compatibility dependencies (gap D36, 7 rows). Files (all new): `content/baselines/**` in the code repo (no such directory at `308b7aa6`). Read-only input: the approved records folder in the project root (`1_Project_Definition/Content/2026-10-20_hpsm-baseline-template-DRAFT/`). Dependency: L1 (the loader, `packages/content`, code PR #85, 57 files, HOLD K6): the ticket text says the data files stay disjoint from the loader, so it can be built on a branch (C-92) but not released. Disjoint from PR #85 (touches `content/release-*`, `content/sources`, `packages/content`) and from lane C2 of the screen (migration 0023, `apps/api/src/**`, `packages/api-contract/src/**`, renderers). Plan tier 1 on all four, so a G1 Opus gate; build Sonnet C2 for L2-1/-2/-4, L2-3 held for the words gate. The records lag: B532 must have landed first.

## UNMEASURED (and what would close it)

- Any behaviour: I ran no build, test, install or probe. For each ticket the briefs list the red proof the seat must produce. Notably unmeasured: whether the -198 test is green or red at main; whether -301's result line carries the inputs; whether the -302/-303 synthetic books can be built as described; whether reflection over the reconciler's IL works in CI (-292); the real API's answer end to end for a name starting with U+FEFF (B526); the hosted pipeline's headers (-122). Instrument: the seats' red-first runs.
- Whether the owner's discussion with the reviewer changed any template row (his words say only "changes unlikely in the future"): B532 records "none reported" and marks it UNMEASURED.
- Live Jira counts after B521's STATUS (94 issues, 19 held, 3 owner-wait): RELAYED, B532 re-counts at start. Instrument: the REFUSE 7 check.
- The root repo's dirt count and processes beyond one `tmux` and one `git status` read; Composer BUILDER seats may be live by launch.
- `.env` contents (not opened except to list key names for HPSM-POC at the start; no value read or printed by me beyond in-process Jira auth).
- Load: load1 10.23 at 13:40; heavy runs by the seats will queue.
- The drafter did not run `usage_gate.sh`; the gauge in each model line is the dispatch's 95%.

## Fences I touched (all inside the allowance; disclosed for completeness)

Read-only git verbs with `--no-optional-locks` in the three project repos and the Composer root repo (`ls-remote`, `show`, `grep`, `ls-tree`, `rev-parse`, `rev-list`, `merge-base`, `diff`, `cat-file`, `status --short`, `for-each-ref`, `worktree list`, `log`); `gh api -X GET` under each project's own `GH_CONFIG_DIR` (pulls, compare, branches); Jira GETs with each project's own `.env` read in-process (HPSMPOC-323, -134; MPSCALC-198, -199, -208, -301, -220, -291, -292, -294, -302, -303, -122, -124, -125, -97, -102; PCOMP-30, -36..-39 with transitions); `decision_queue.sh show` of exactly three ids (`hpsmpoc-refuse-more-invisible-characters`, `hpsmpoc-class-c-wording-six-tickets-1022`, `composer-baseline-template-draft-review-1023`); one `node -e` fed from `git show` (no file written); `lsof`, `tmux list-panes`, `uptime`, `ps`. No `decision_queue.sh list`; no `fleet/briefs_staged/`, scoreboard or other client's material seen. Two tool calls were refused by Tuesday's own hooks (a `cd`, an unquoted `=====`) and re-issued correctly. The harness itself saved two large tool outputs under its own tool-results folder (not a file I wrote or read as a deliverable). I did not Edit/Write anything outside the 14 briefs and this report (the four MPS briefs were edited once more after the partition update; the `.pre-stamp` copies were made last, so every pair is byte-equal). No file in any project tree was created.

SELF-CHECK: all seven briefs re-counted for stamp lines (8, 8, 8, 8, 8, 8, 9) and `cmp`-equal to their `.pre-stamp`; fact strings run; intersection re-run after the partition update; no person name is asked of any seat in code or Jira text; the ruling quotations carry the owner's words verbatim as the brief's own text.
