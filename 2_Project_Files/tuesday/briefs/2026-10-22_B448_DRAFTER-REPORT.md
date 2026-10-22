# B448 drafter report (read-only drafter for Tuesday), 2026-10-22 ~12:00 AEDT

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B448_SEAT-D2_mps-hosted-deploy-f5b6f5a.md` (cloned from B268; read whole: the B268 brief, the B268 STATUS, the project `CLAUDE.md`, `CLARIFICATIONS.md` C-43/C-45 and the tail sections). Fences held: git read verbs, `gh api` GETs under the project's `GH_CONFIG_DIR`, `decision_queue.sh show <one exact id>`, no az, no HTTP to any hosted site. One local `ls-remote` network read of the project origin. Writes: the brief and this report only (plus scratch files in the session scratchpad).

## BLUF: TWO STOPS ARE LIKELY BEFORE ANY DEPLOY. Decide before you launch.
1. **CI on `f5b6f5a7` is RED and there is NO deploy package.** Run `39514401396` (`ci`, push, attempt 1) `completed/failure`; job `dotnet` failed on ONE test of 1828 (`FeedbackTicketTests.A_timeout_then_a_search_that_finds_the_label_records_that_key_and_never_creates_a_duplicate`, "ticket never reached the expected state", Api 1827 passed / 1 failed; Engine 394/394; Import 156/156); job `package` was SKIPPED; run artifacts = 0; no `deploy-mpscalc-f5b6f5a7…` artifact in the repo's list. The test and `src/MpsCalc.Api/Feedback` are untouched by the 11 PRs (`git diff --quiet` rc 0). It is the known timing test (BACKLOG `[B100-1]`, `[B340-B318-C1]`, `[B406-MAIN-RED]`). `CLARIFICATIONS.md` (B406 process note 4, item 3c) says expressly: **whether to re-run the failed job is NOT ruled.** The brief's stamp slot R-2 is where you rule it (default written: no re-run, seat stops). B268 rule R-6 stands: no local package. A re-run is a GitHub write the B268 seat never made; the script's own error text says "re-run CI on main, then fetch again".
2. **Words: the card did not approve any, and a large unruled set is merged.** Details below. Expect `STOPPED: NEEDS TUESDAY words: <n> new` with n in the hundreds.

Everything else I could read is clean (below). Main is still `f5b6f5a710258a4a36ffbcab92787a2434962500` (`ls-remote`, 11:5x), one parent `1eccbc8b`, tree `450c793ef848f214f87eaa8cfd712ccc88fb090d`.

## Facts pinned (all in the brief)
- `e6f92a5f` is an ancestor of `f5b6f5a7` (rc 0); 11 commits, first-parent = 11: #83, #84, #87, #85, #88, #86, #89, #90, #91, #92, #93; 142 files, +12,022 / −300 (92 A, 50 M).
- `diff --name-status e6f92a5f f5b6f5a7 -- infra .github scripts tools`: **empty** (deploy tooling byte-identical to B268's). `appsettings*` in range 0; `migrat` in src 0 both ends; `MpsCalc:` keys 13 = 13 (wide 14 = 14), narrow lists diff-equal. No new setting.
- Stores: `QuoteFileStore.cs`, `ApiJson.cs` rc 0 unchanged; `CatalogueOverlayStore.cs`, `FeedbackStore.cs` present and untouched (no `*Store*` file in the 17 changed `src` files). BUT `Contracts/Dtos.cs` adds persisted draft members (`AccountManager`, `DeliverySite`, `OpportunityNotes`, `OpportunityDeviceCount`) and `QuoteEvents.cs` adds the event `accepted`. With `Disallow` on read, a quote saved by `f5b6f5a7` with an opportunity field is REFUSED by `e6f92a5f` after a rollback. I added a new pre-swap count 3e and a matching rollback condition for this (not in B268).
- Rollback target is `e6f92a5f`, not B268's `12f8e566`: package `.tools/wt-B268-release/.local/deploy-packages/e6f92a5f7568b2f2d72f454524b8e09406357957/mpscalc.zip`, sha256 `f5165caa23722048b7d8ad69313508c2fab43b2098bdaacfedb16b7602d61c63`, 3,149,736 B, `.RUN` 39009325479. Drafter re-hashed it: equal; worktree HEAD `e6f92a5f…`, porcelain 0. The seat must re-prove it (`verify`, `bash -n`). Its artifact `12092282044` expires 2026-10-24T06:22:53Z; the local zip does not expire. B166's `12f8e566` zip also still present (sha `cdfe793e…1d00`, 3,142,810 B).
- Hosted target (stated in the brief; B268 never calls it demo or production): site `app-mpscalc-showcase-u6agl3edszqvs`, RG `mpscalc-showcase-rg`, sub `a6b8fe11-…`, tenant `ec01829b-…` (the datasec-rd tenant, C-06a). Treated as live with real user data. For Tuesday: workspace CLAUDE.md names tenant #5 as `d500ebad-…`; this project's hosting is a different tenant by C-06a, and B268 ran against `ec01829b`. I carried B268's classification unchanged; R-4 in the stamp lets you overrule.
- Authority text is quoted verbatim; store `show` read: `ruled`, choice `a`, `ruled_ts 2026-10-22T11:51:21.297836+11:00`. Option a's detail contains no words clause (earlier cards C-26, C-36, C-43 did).
- Partition: `.tools/heavy-slot-1` (holder file inside), `.tools/b444`, `wt-b444-base/fix/mut` exist; the brief forbids touching or reading inside them. Load at 11:52 AEDT was 8.8 (rule: launch under 7).

## Words check, as far as git read verbs allow (the seat repeats it with controls)
Method used: for each of the 11 first-parent commits, `git diff -U0` over production paths only (`web/src` not tests/qa/generated, `src`, `docs` .md), extract added quoted strings with a space and letters, plus added docs sentences. Script and output in the session scratchpad (`words448.py`, `words448.tsv`), not in the project.

| PR | prod files | candidate strings (noisy count) | declared NEW WORDS (builder/gate) |
|---|---|---|---|
| #83 | 1 | 1 | 1 sentence (the CARE-PACKS rule text, staff-only; old `Item class: service (default K-05, until MPSCALC-142).`, new `Item class: carePack ("Care pack", MPSCALC-142); it totals under Services with service and staging (X-31).`) |
| #84 | 4 | 23 | 11 (B303, staff-only importer/prove) |
| #87 | 9 | 85 | 36 (B312, readiness/reconciliation) |
| #85 | 8 | 73 | 22 (B309; the gate B318-3 says the list missed `-COPY` and 2 contract descriptions + API.md:415) |
| #88 | 8 | 35 | 28 declared / 20 rows (B310) |
| #86 | 11 | 49 | 81 per-component / 47 strict (B313); round 2 B326 says 43 |
| #89 | 5 | 14 | 12 (B311) |
| #90 | 12 | 29 | 33 (B345) |
| #91 | 4 | 4 | 0 (B354) |
| #92 | 0 | 0 | 0 (B365; tests only) |
| #93 | 2 | 1 | 0 (B388; one docs sentence in `docs/API.md`) |
| **Total** | | **314 lines / 307 distinct** (includes some non-word literals, comments excluded) | **declared ~181 strict (11+22+20+36+47+12+33) up to ~223** |

- Examples confirmed as screen text, not in `CLARIFICATIONS.md` as ruled words: `Finance rate (p.a.)`, `Annual escalation`, `Target GP` (#88, `QuoteScreen.tsx`); `Go to section` (#88); `One-off GP (AUD ex GST)`, `Annual recurring GP (AUD ex GST)` (#89, `QuoteList.columns.tsx`); `Devices in the opportunity must be a whole number from 0 to …` (#90). `Ready to Export` has one hit in CLARIFICATIONS.md (not checked as a word ruling) and 3 in the unruled register.
- Rulings search: `CLARIFICATIONS.md` has word approvals only up to C-43 (W2 list). **There is no ruled word pack for #83–#93.** The register `Registers/2026-10-20_v13-wave1-new-words.md` (421 lines, sha256 `f0b719dc12ff652df1199136dafb2840a140270c50b7519aa10b5d932909797a`) says in its own words that it was "collected for the product owner's next hosted-deploy words card. This seat approves nothing." Its sources B303/B309/B310/B312/B313 add 178 to 183 declared strings (11+22+20+36+47..81), plus B311 12 and B345 33. The standing rule (K-02; C-45 option a detail): every new word goes to the product owner as a pack before it ships. I found no card id for such a pack and did not enumerate cards (`list` forbidden). **Verdict for you: a STOP `words: <n> new` is near certain; I put n at roughly 180 to 310 depending on the counting rule, and most are customer/screen-visible (v13 workspace), a minority staff-only (#83, #84 = 12).** If you prefer to avoid a wasted seat, send the register as a word-pack card first and launch only after it is ruled (then R-1 names the card id).
- Not counted as unruled: W2 words (`Deals won`, care-pack classes, below-0 sentences) are in `e6f92a5f` and already live.

## CI, other
- The newest deploy artifact in the repo is for `1eccbc8b` (#92, id `12287910362`, expires 2026-10-27T17:58:42Z). It is not the card's sha and the brief forbids deploying it. Say so if you want a different card (e.g. deploy #92 only, which still carries the same unruled words from #84–#90).
- Open code-scanning alerts on main: not read (the seat measures).

## Per-PR live probes (brief step 6)
Read-only: one new GET route exists (`GET /api/v1/quotes/{quoteId}/versions/{n}/diff?against=`, no write, auth first, then 400 on bad input, then 404). Probes use a random quote id (404), `against` equal to the version (400, no data read), no token (401), and the absence of the staff keys on the Seller list. Everything else (new workspace, opportunity panel, autosave, readiness, Ready to Export, duplicate, approve-blocking) is static-string or UNMEASURED by design; listed in NOT TESTED. Staff list columns need an internal-metrics persona to see them; the seed account is a Seller (UNMEASURED positive case).

## Open questions for you (the stamp slots)
1. R-2: may the seat re-run the failed job once (`gh run rerun 39514401396 --failed`, the only GitHub write), then wait 30 minutes? Default written: no.
2. R-1/R-3: send the register as a word pack first, or let the seat measure and stop? Do staff-only words (12) count in n?
3. R-4: confirm the hosted-target sentence (datasec-rd tenant `ec01829b`, "showcase", live with user data).
4. Deviation to confirm: rollback also conditions on 0 new-member files (3e), which B268 did not have.
5. Time: it is ~12:00; hard stop 14:30; a re-run plus 30-minute wait plus the deploy fits only if the words STOP does not fire.

## Stamp
- Drafter self-check: four-underscore slots exist only in the brief's `## Stamp` section and its last line (9 lines, all in the stamp); no person's name used (account id `kamilDatasec` appears once as the gh account, as in B268).
- Read whole by Tuesday: ____

READ-WHOLE-BY-TUESDAY: ____
