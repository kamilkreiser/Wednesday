# B169 DRAFTER REPORT: Kam's 17 Oct MPS builds (lanes D/E) + records seat R2
Drafted 2026-10-17 14:2x AEDT (`date` 14:26:16) by a Tuesday drafter. Datasec / MPS Calculator only. Nothing launched, tapped, mailed, posted or written outside Tuesday's `briefs/` folder. Jira and GitHub were read with GET only.

## Files
1. `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B103_ADDENDUM-10_kam-1017-builds.md` (lane D: A negative headline, D proposal rates)
2. `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B104_ADDENDUM-8_kam-1017-builds.md` (lane E: B feedback 401, C overlay-copy retention)
3. `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B169_SEAT-R2_mps-records-1017.md` (records seat)
4. this report

## What I measured (each read taken by me)
- **Main:** `git ls-remote origin refs/heads/main` = `725b4ef550a10a7c6f022521438d321846dd4646` (14:26) = the expected sha = PR #75's merge commit. **It is NOT in the local object store** (`cat-file` fails; local `origin/main` = `0217044`). I did not fetch. I ran `git grep` at **`ef8146c`** (#77's head, local). #75 changed only `web/src/screens/QuoteList.tsx` and `Home.test.tsx` (gh `pulls/75/files`), none of the four items' files, so `ef8146c` equals main for every file cited.
- **PRs (gh GET, project GH_CONFIG_DIR):** #74 `ed72606…` 2026-10-16T23:15:10Z (MPSCALC-140) · #76 `0217044…` 02:27:05Z (MPSCALC-142, -155) · #77 `422b87b…` 02:53:01Z (MPSCALC-158) · #75 `725b4ef…` 02:59:02Z (no ticket; card). #73 `12f8e566…` 2026-10-16T21:13:08Z (MPSCALC-150, -158). Jira text search for each of the five merge shas: 0 (control `798fe98…` → 1, MPSCALC-183). **No ticket carries a merge comment for #73-#77.**
- **Rulings (`decisions.json`, `ruled_ts` AEDT):** panel 09:22:38 · negative 09:23:27 · large-format 09:23:31 · hosted deploy 09:23:34 · feedback 09:23:50 · E877 09:23:54 · overlay copy 09:23:57 · deal-usage 09:24:14 · rental caption 09:32:22 · Deals won 10:34:04. All `status: ruled`, with the choices the commission gave.
- **Jira (GET, own client; secrets read by name inside python, never printed):** `created >= "2026-10-17"` → 24 (MPSCALC-189…212, all B164); highest key 212; `text ~ "PRE-1"` → 8; `text ~ "zzqxvbw"` → 0.
- **Ticket keys for the four builds:** (A) negative headline: **NONE** (`"technical limits"` 0, `ErrorBox` 0; MPSCALC-105 is the merged refusal, related). (B) feedback 401: **MPSCALC-194** (B164 R06, lane-h tier-2). (C) overlay retention: **MPSCALC-203** (B164 R15, lane-j tier-1; "Retention waits for the product owner"). (D) deal-usage proposal rates: **NONE** (`usageRates` 2 = 150, 139, neither names the proposal; `"usage charge"` 0). The records seat files A and D first, as T01/T02.
- **Code (at `ef8146c`):** (A) `QuoteEndpoints.cs:1160` the one headline, `InRange` `:1096-1161`, `NotNegative` `:1129`, the five fleet calls `:1139-1143`; `ErrorBox.tsx:35-53`; `FleetGrid.tsx:55-68` column headers; `git grep "technical limits"` (json excluded) = 1 hit, so no test pins it. (B) `FeedbackPill.tsx:37`, `:44-46`, `:56`; `FeedbackDialog.tsx:221-225`. (C) `deploy-from-ci.sh:96-99` (comment), `:108-119` (`pre1_hosted`), copy name `:112` at one-second resolution; harness `scripts/tests/test_deploy_pre1.py` (235 lines, `Pre1InTheDeploy` sandbox `:162-224`); CI python loop `ci.yml:80-88`. (D) `Proposal.cs:513` `CopyPurchase`, rates from `p.Clicks` only `:517-532`, allow-list `:148-156` (deal applied clicks = N, "not on the proposal until Tuesday's word"), `:328` sources; `Dtos.cs:1012-1019` `DeviceClass` required.
- **Lane file lists:** lane D's own (`B103_LANE-D` `:9`): engine, six `Quotes/*.cs` files, `Dtos.cs`, the contract files, `ENGINE.md`; lane E's (`B104_LANE-E` `:9`): importer, `Engine/Reference`, `InventoryEndpoints.cs`, `web/src/screens/inventory/**`, `IMPORTER.md`. **None of the four builds' files is on either list**, so each addendum grants its files by name (as ADDENDUM-6 did for `QuoteList.tsx`).
- **Records:** `CLARIFICATIONS.md` last heading `### C-32` (`:466`), file clean in `git status`; the project ROOT is its own git repo (branch main, no remote), records commits titled `Records: …` (`0cd5eab`, `12554b7`); `history.md` +115, `BACKLOG.md` +225, `JIRA.md` +19 uncommitted (other seats, incl. B164).
- **Gate sources:** B165 370 lines (findings `:287-293`), B166 265 ("For the records seat" `:203-213`), B167 384 (findings `:293-304`). **B168 STATUS: absent at 14:20** (evidence dir only).
- **Cockpit:** `cockpit.sh status`: panes tuesday, MPS-V4, HPSM-POC-G3, Vision-gate22, NexusAI-O, MPS-LE, MPS-LD, Vision_Sales_Portal, fleet-monitor. **`Datasec/MPS-R2` is free.**

## The lane split, and why
| Build | Lane | Branch | Files (disjoint) | Tier |
|---|---|---|---|---|
| A negative headline | **D** | `b103/mpscalc-<T01>-negative-headline` | `QuoteEndpoints.cs` (headline only), `ErrorBox.tsx`, 2 new test files, `docs/API.md` | 2: screen words, no figure, no printed document |
| D proposal rates | **D** | `b103/mpscalc-<T02>-deal-usage-proposal-rates` | `Proposal.cs`, a new API test, contract files via `sync-contract.mjs` | 1: changes the printed customer proposal and prints a price figure |
| B feedback 401 | **E** | `b104/mpscalc-194-feedback-401-words` | `web/src/feedback/{FeedbackPill,FeedbackDialog}.tsx`, `words.ts`, a new test | 2: one sentence, no figure |
| C overlay retention | **E** | `b104/mpscalc-203-overlay-copy-retention` | `scripts/deploy-from-ci.sh`, `scripts/tests/test_deploy_pre1.py` | 1: removes a cost-bearing file on the deploy path (203 is tier-1 already) |
Why: lane D built the contract/API and the deal-usage DTOs (`Proposal.cs:148-156` comments name lane D), so both server-side customer/API changes go there; A also needs the API's headline. Lane E has done a web change for Kam today (#75) and has no API file in these builds, so it takes the web-only feedback fix and the script-only deploy change. **No file is touched by both lanes.** Lane D's two branches may both touch `docs/API.md`; they are sequential in one lane. Neither lane touches B168's files (`PurchaseCatalogue.cs`, `CarePackImportTests.cs`, `B104CarePackApiTests.cs`, `GateB41.cs`).

## Records seat B169: what it does
10 C-entries (C-33…C-42, one path-limited commit of `CLARIFICATIONS.md`), 2 history entries (B166's verbatim line + its own), 13 tickets (T01, T02 for the builds, filed FIRST with a `BUILD KEYS:` line; G01-G11 from B165-2/-3/-5/-7, B167-2/-3/-4/-6/-8/-9/-10/-11, B166 candidates 1/4/6), 6 finding/ruling comments (202 ← B167-5; 208 ← B167-12; 195 ← B165-4/-6; 203, 194, 144 ← Kam's rulings), 5 merge comments (140, 142, 155, 158, 150), 13 BACKLOG rows, a JIRA.md section. Expected last line `DONE: B169 10 C-entries, 13 tickets, 11 comments`.

## UNMEASURED
- Main `725b4ef`'s tree by `git grep` (not in the local store; covered by `ef8146c` + #75's two-file list).
- Which device classes the engine charges the deal's mono/colour clicks on, and whether `p.Clicks` is empty under deal usage (only B158-11's `usageRates: []` says so). Lane D measures both before choosing rows.
- Whether ink should print (the ruling names mono and colour only).
- Whether `'Your session has ended. Sign in again.'` stays reachable once the 401 fix lands.
- How the deploy should behave when the removal itself fails (I wrote: one stderr line, deploy continues). That is my choice, not Kam's.
- B168's verdict, and so B167-1 / B167-7.
- Whether a calculation-register row was written for the Care pack / Staging classes (MC-2 asks the seat to read it).
- Whether MPSCALC-144's text names the E877 supply costs (CMT-6 is conditional).
- Heavy-slot occupancy and load now. No `holder` read, by design: the lanes read them.
- PR #73's clearance wording. The seat quotes the PR body.

## Traps
1. **The tap times are not the `ruled_ts` times.** The commission's times are Kam's board taps. `decisions.json` holds the queue times: the rental caption was tapped ~09:22 but ruled 09:32:22; Deals won was tapped 10:33:19 but ruled 10:34:04; the hosted deploy was tapped 09:22:56 (B166) but ruled 09:23:34; deal-usage was ruled 09:24:14, not 09:23. The C-entries use `ruled_ts` and add the tap time where a record holds one.
2. **One Problem carries both kinds of refusal.** The negatives and the magnitude limits share the headline at `:1160`. "Some values are below 0." would be false for a mixed refusal, so the mixed case keeps today's headline. That way no new words are needed.
3. **`ErrorBox` is shared by every screen.** The column mapping is limited to `INPUT_OUT_OF_RANGE` lines that match the five fleet fields. The filled form `Line {n}, {column}` is NEW WORDS FOR KAM, and the merge waits for Kam's yes at the words gate (the card's default says this).
4. **`DeviceClass` is required on a usage row.** A deal-level rate has no single class. The lane must measure the engine before it emits rows, and it must flip ONLY the two applied-click fields in the allow-list (a leak guard).
5. **Overlay copy:** decide "clean" by the HTTP code and the PRE-1 rc, never by size (B166's 54 B vs B161's 21-27 B). The script removes only the path THIS run created: no glob, and not B166's existing copy. With a one-second copy name, two runs can share a path, so a unique name is part of the branch. **The agent deletes nothing itself.** Tests run inside the harness's tmp sandbox.
6. **No ticket exists for A or D.** Launch B169 BEFORE tapping lane D, or lane D works on placeholder branch names and renames them before pushing (ADDENDUM-10 says this).
7. **MPSCALC-194 has two halves.** Kam's words cover only the sentence. The B157-6 half (unsent text is lost) stays open, and the READY line says "partly".
8. **#73 was never merge-commented.** It falls between B164's window (#45-#72) and today's #74-#77, so I added it as optional lines (MC-4, MC-5). Strike them before you stamp if you don't want them. Also, the 36 tickets B164 commented "not deployed" are now deployed (B166 put `12f8e566` live). A deploy-comment pass is your call. It is not in this brief.
9. **The 16 Oct card rulings have no C-entries either.** `grep` for "1016" in `CLARIFICATIONS.md` returns 0, yet the cards draft cites K-06/K-20/MPS-6 rulings of 16 Oct. That gap is outside this brief.
10. **Labels with a person's name exist on the board.** MPSCALC-142/-150/-155/-158 carry a `<reviewer-name>-review-2026-10-16` label. The seat must not reuse that label family. Its labels are `mpscalc-b169` / `plan-b169-*` only.
11. **Records commit.** Only `CLARIFICATIONS.md` is clean. The other three records files hold other seats' uncommitted edits, so the commit is path-limited to the one file. The brief STOPs if `CLARIFICATIONS.md` is dirty at run time.
12. **Jira text search splits underscore names into tokens.** `MPSCALC_HOSTED_HOST` unquoted returned 20 unrelated hits, so the brief uses the quoted phrase only.
13. **B168 is still running.** Lane E's addendum forbids touching `b104/mpscalc-140-care-packs`, and the records seat files B168 items only if a `VERDICT:` exists. If B168 ends NO GO, CP does not ship this round (the cap). That is for you, not the seat.
14. **G10 vs MPSCALC-188.** Both say "F-1 residual", but they look like different findings. The seat reads 188 and comments on it instead of filing if they are the same.

## Launch command (pane name checked free)
```
bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/MPS-R2 "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B169_SEAT-R2_mps-records-1017.md'"
```
Order: stamp and launch B169 → tap lane E with ADDENDUM-8 (its keys exist) → tap lane D with ADDENDUM-10 (its keys come from B169's `BUILD KEYS:` line).
