STARTABLE: YES (engine half, purchase only, no input member, reconciler untouched. Tuesday answers Q-2 to Q-7 at the stamp, and each has a default. Q-6 is the one that matters most: one existing test pins the limit this lane removes and goes red by construction.)

# B1043 drafter report (SEAT-M61, MPS MPSCALC-256 purchase half: the purchase recurring projection), 2026-11-01

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1043_SEAT-M61_mps-256-purchase-annual-projection.md`, 110 lines, sha256 `ad406e0d509a6bdecd8f00b1ad41d3849c8efb408f478d859129836b969572e3` at 13:52:55. The four-underscore count is 8 (7 slots plus the last line), by `/usr/bin/grep -c -E '_''_''_''_'`. Non-ASCII bytes: 0. The last line is `READ-WHOLE-BY-TUESDAY: ____`. **I did not write a `.pre-stamp` copy**, because the task allows exactly two files. The kit's REFUSE line therefore names "Tuesday's unstamped copy, if kept" as the control. Tuesday makes that copy before stamping, if wanted.

## BLUF
- **The lane:** one new branch, `b1043/mps-256-purchase-recurring-projection`, off main `5c64a442` (re-read from origin, see Facts). It adds one result member, `PurchaseResult.Projection`, which reuses the rental `RecurringProjection`/`ProjectionFigures` types unchanged. The member has six measures, each Monthly, Annual (= monthly x `WorkbookRules.MonthsPerYear`, exactly) and Contract. It reads only figures the result already holds and writes none. There is no input member, so all 40 input hashes stay equal by construction. Register row **X-39**. One commit (two at most), one push, no PR. Gate after: ONE tier-1 gate, round 1 of 2 on the new class "V4 engine: purchase recurring projection".
- **Where the line is (scope):** engine only. OUT, each with its reason:
  - The web table is MPSCALC-267 (T-V5-7), and the ticket itself names it.
  - The Api, DTO and openapi members are not ruled. CLARIFICATIONS:1774 7(a) leaves the owner of the V4 Api half open for -252/-258/-259, and :1907 7(a) does the same for the fee ("none does"). The rental projection never reached the Api either (measured).
  - The list's per-year GP is MPSCALC-315.
  
  The acceptance names no Api clause. This lane closes clause **1b** (comment 40383: "1b NOT MET: the purchase result carries no projection") and makes clauses 2, 3 and 4 true for purchase.
- **Prior work found (guard):** `Briefs/2026-10-31_B974_ADDENDUM-1_purchase-projection-scope_ruling.md` is Tuesday's own earlier ruling (b). It said: no purchase projection member until MPSCALC-255 lands, because "two null measures beside four real ones is a half-filled shape". MPSCALC-255 has now landed (MPS #135, Done). With no fee stated, the two fee measures are 0 by X-38's own rule ("no default"; an unset fee adds nothing), so no measure is null. The kit cites ADDENDUM-1 as the reason the existing pin exists and why it now gives way.
- **The one red-by-construction test:** `RecurringProjectionTests.R30_a_purchase_result_carries_no_projection` (:177-192 at `5c64a442`) asserts by reflection that `PurchaseResult` has no `RecurringProjection` property. It is B974's row U, pinning ADDENDUM-1. Q-6 lets the builder replace exactly that method, plus the class summary sentence on :13, with a precise shape: the fixture and the runtime assertions are kept, `Purchase.Projection` null is added, and the reflection loop is kept for the three sub-results. Names lost: exactly 1.
- **Model:** C3 Opus (`model-routing.md:93`, re-checked by `sed -n`; C2 is :92, G1 :108, G-cap :111). Id `claude-opus-5-5` (`models_latest.json:37`, checked_at_local 2026-11-01 13:27:30). `BRIEF_SEAT_LEVEL=opus` is written inside the launch quotes. Pane `Datasec/MPS-M61`. No ports needed; block **9640-9649** reserved.

## Facts re-measured (instrument; control)
- **Origin main** (`gh api -X GET repos/datasecau/MPS-Commercial-Calculator/git/ref/heads/main`, under the project's `GH_CONFIG_DIR`, 13:41:47): `5c64a44226614523031a7b2d67cb9bfb477a380e`. Its commit: 1 parent `edac7431`, committed 2026-10-31T19:57:37Z, subject "MPSCALC-255 ENGINE HALF: purchase managed-service fee per device per month on a section". This equals the RELAYED value.
- **Open PRs:** #121 `6931286b` and #120 `85aafb7f`, both dependabot. Their files, from `pulls/<n>/files`: `web/package-lock.json` only. Control: `pulls/99999` returns HTTP 404.
- **Branches:** `matching-refs/heads/b1043` 0 (control `heads/b10` 59). There are 158 heads. Only `b974/mps-254-256-v4-volume-basis-annual` matches `256|projection|annual`, and that is the merged PR #133 branch.
- **Jira** (my own urllib GET in the scratchpad; it reads `4_Credentials/.env` in process; no token printed; control `MPSCALC-99999` HTTP 404):
  - MPSCALC-256: Backlog; labels `calc-register lane-v4 mpscalc-b308 plan-b308-t-v4-5 tier-1`; 0 links; 1 comment (40383, records pass B1004, 01:54); updated 01:54:55. The description, acceptance and comment are quoted in the kit.
  - Scope edges: MPSCALC-267 (T-V5-7, web table, tier 2, 0 comments), MPSCALC-315 (list GP, Api + web, 0 comments), MPSCALC-253 and -257 (same engine files, serialise after this lane).
- **Rulings and records at source** (`CLARIFICATIONS.md`, 1929 lines):
  - C-79 at :1712, the Done rule.
  - The -256 record at :1731 ("1b NOT MET").
  - The -252/-258/-259 section item 7 at :1774 ((a) Api half not ruled; (f) -256 not judged).
  - The -255 section items 1-7 at :1895-1907, with 7(a) "none does" and 7(e) "MPSCALC-256's purchase half ... this pass did not touch it".
  - The landing rule at :758 and :774.
  - D-05 and D-06 at :673-674, MPS-4 at :331, C-38 at :543.
  - No ruling gates T-V4-5. The ticket says "no ruling needed", and the plan at :276 agrees.
- **Source at `5c64a442`** (raw `gh api` GET into the scratchpad; tree `truncated=false`, 664 blob paths):
  - Line counts: PurchaseResult.cs 276, PurchaseCalculator.cs 961, PurchaseInput.cs 144, CalculationResult.cs 282, QuoteCalculator.cs 685, RecurringProjectionTests.cs 193, ManagedServiceFeeTests.cs 282, ENGINE.md 206, PurchaseRecomputation.cs 260, ci.yml 123.
  - Anchor counts (`/usr/bin/grep -c -i -F`; control `zzz-no-such-string-7f3a` 0): `projection` 0 and `annual` 0 in both purchase files. The positive anchors each read 1: `Usage` and `ContractManagedServiceSell` declarations, `ContractManagedServiceSell = contractFeeSell,`, both `SuppliesProfit =` lines, `RecurringProjection(`, `ProjectionFigures(...)`, the "Rental only" summary, the rental `Of` line, `MethodOf(`.
  - ENGINE.md: `| X-38 |` 1, `| X-39 |` 0, "a purchase result carries no projection" 1.
  - ci.yml: `:31` job name, `:42` build, `:43` test (sed).
- **Correction to the sweep:** `PurchaseCatalogue.cs` IS in the tree, at `src/MpsCalc.Engine/Reference/PurchaseCatalogue.cs`. B1015's report found the same; the sweep repeated the wrong path. The sweep's "747 paths" is a different frame from my 664 blob paths (the sweep's tree file probably includes tree entries). This is not material.
- **Who reads `Projection`** (local `git grep -w -i` at `edac7431`; the local checkout lacks `5c64a442`, and #135 changed 5 paths, none of them a reader):
  - Engine: `QuoteCalculator.cs` 3, `CalculationResult.cs` 4, `RecurringProjectionTests.cs` 7, ENGINE.md 1.
  - Api `Proposal.cs` 12 and 4 Api test files, but every Api hit is the customer-safe "proposal projection", a different concept (read line by line).
  - `openapi.json` 2, both the proposal.
  - The Api maps purchase results by hand (`PurchaseMapping.ToDto(PurchaseResult p, bool internalMetrics)` :144, `WhatChanged` :327-358 field by field). So an engine-only member cannot reach a response. The store keeps the engine `CalculationResult` (`QuoteStore.cs:26`), so the key will appear in new stored snapshots that have a source (the kit makes any Api/Import test red from this a STOP).
- **Engine design facts the kit depends on** (read at `5c64a442`):
  - Section-rate supplies figures are PER DEVICE. `ClicksOf` builds `monthlyMono = AmpvPerDevice * (1 - ColourShare)` and contract figures from it, and `SuppliesProfit = net * model.DeviceQuantity` (:775). `model.DeviceQuantity` is an input of the supplies model, independent of the section's `DeviceQuantity`.
  - Deal-usage figures are WHOLE DEAL (`SuppliesProfit = net` :935).
  - Revenue exists only where a supplies model exists. Both functions return before any P&L when there is no model.
  - `DealProfit - HardwareProfit = SuppliesProfit (+ contract fee sell - cost when stated)` (:231-246). This identity gives the contract recurring GP.
- **Harness frame (RELAYED):** B1015 and B1020 saw 25 caller files, 80 sites and 35,614 records at `edac7431`, and 35,641 at `687c6d1`. `687c6d1`'s tree equals main's (CLARIFICATIONS:1895). Local CI at that tree: 493/193/3165.
- **Gate class census:** first lines of `1_Project_Definition/Briefs/*_STATUS.md` that start "GATE VERDICT": 69. Of those, 0 name `purchase recurring projection|b1043`. Controls: `rental projection` 2, `managed-service fee` 1.
- **Ports** (DRAFTER_RULES port check):
  - Block 9640-9649. `-w -E '964[0-9]'` over the 74 non-`.pre-` SEAT kits of 10-31 and 11-01 found 0 files.
  - Controls on the same set: `962[0-9]` 2 (B1020, B1022), `963[0-9]` 2 (B1025, B1027), `961[0-9]` 3, `948[0-9]` 5, `967[0-9]` 2 (B1037, B1038).
  - `lsof -nP -iTCP:9640-9679 -sTCP:LISTEN`: 0 rows (control: the unrestricted listing printed 14 lines).
  - Live pane list: no port-holding MPS seat.
- **Seat name and panes:**
  - `-w 'M61'` over ALL `briefs/*.md`: 0 files (control `M60`: files listed). Over the 74 SEAT kits: 0.
  - Panes at 13:44: `%0 tuesday`, `%158 Datasec/ATTIO-R113`, `%157 Datasec/Security-Composer-R112`, `%1 fleet-monitor`. No MPS seat is live.
  - `.tools` filtered `b1043|m61`: 0 (control `b1015` 3). `.tools/.git-lock` is absent, and no heavy slot exists.
- **Local repo state** (read verbs only): code HEAD branch `b03/api`, `origin/main` = `edac7431`, `cat-file 5c64a442` fails. `core.sshCommand` is the deploy-key command (key elided). Root HEAD is `76f1806c` and root `git status --short` has 849 lines. `gh auth status` shows the project account as active.
- **Load:** load1 2.83 at 13:44.

## What went well and badly on the -255 template (B1015 STATUS, B1020 gate), and what the kit does about it
- **Well:** READY in about 35 minutes. The gate found 0 Blockers and 0 Majors. Byte-equality held on 25 files under three serializers, 40/40 hashes, a sweep of 400 (gate 600) with 0 differences, and 12/12 mutants. The kit keeps that shape: three serializers, mask-then-sort, CALLED `InputHash.Compute`, the c0 pair, and ApiJson's CurrencyTests limit.
- **Badly, fenced:**
  - B1020-6: the builder's rows left 4 gate mutants alive. The kit adds edge rows (a) k differs from the section devices, (f) a stated zero, and (h) a non-terminating CPP.
  - B1020-4/-5: X-38 was silent or short on edge cases. The kit lists every clause X-39 must state.
  - B1020-1/-2: a stated zero rewrote DealProfit's bytes. Here the projection writes no existing member, which property check (b) and the stripped compare prove.
  - B1020-11 (process slips):
    - The `cd` and the files outside the seat tmp: standing line 6 is now explicit.
    - `git add -N`: forbidden, and `git add` of Yours is listed.
    - The mutant tree left at base with copied files: Step 6 now runs mutants AFTER commit 1, in `wt-mut` detached at commit 1, so porcelain is 0. A surviving mutant's cell goes into commit 2 (D2).
  - B1020-3: the rule tag. Not applicable, because no issue is added and check (g) requires 0 new literals in `src/`.

## D-decisions (drafter; Tuesday overrides at the stamp)
D1 Opus C3. D2 One commit, plus at most one forward commit. D3 X-39, plus the R-30 sentence under Q-7. D4 Reuse the rental types; no new type. D5 Deal level only. D6 Purchase only; reconciler untouched (proved). D7 Engine names lost exactly 1 (under Q-6); Import and Api unchanged. D8 `Datasec/MPS-M61`; ports 9640-9649 reserved. D9 Push once. D10 Message rules. D11 3 h / 5 h. D12 No input member.

## Q-questions for Tuesday (each with a default)
- **Q-1** Engine half, purchase only. Api/DTO/openapi/web stay OUT (MPSCALC-267 owns the table; the Api half is unowned under the CLARIFICATIONS 7(a) items). **Default YES.**
- **Q-2 Presence.** `Projection` is set only when the quote is priced AND has at least one recurring source:
  - S1: a section with a supplies model.
  - S2: a deal usage with a supplies model.
  - S3: a stated fee.
  
  Otherwise it is null and omitted, so hardware-only quotes stay byte-equal. Alternative: set it on every priced purchase result (all zeros when there is no source). That changes every purchase result's bytes. **Default: source-only.**
- **Q-3** A rate or deal usage WITHOUT a supplies model is not a source. Its pages and revenue are not projected, because the result holds no cost for them and projecting revenue would show a profit with no cost. ADDENDUM-1 raised the same half-filled-shape concern. **Default YES.**
- **Q-4 Contract column** = the result's own contract figures:
  - Section figures x the supplies model's device quantity; deal figures as they are; the X-38 contract fee figures.
  - Contract recurring GP = `SuppliesProfit` + contract fee sell - cost = `DealProfit - HardwareProfit`, so it carries the replacement shortfall.
  
  The builder MEASURES how often contract differs from monthly x term (decimal CPPs from non-terminating divisions) and states it. It is not a failure: the acceptance pins only annual = monthly x 12. Alternative: contract = monthly x term everywhere. That breaks the exact tie to DealProfit and the existing supplies totals. **Default: the existing figures.**
- **Q-5 Monthly recurring GP** = monthly click revenue - click cost + fee sell - fee cost, with no shortfall. The shortfall is a contract-end figure with no monthly reading, so monthly x term differs from contract GP by exactly the shortfall, and X-39 states this. Alternative: monthly = contract / term (a division, so a repeating decimal). **Default: no shortfall in monthly.**
- **Q-6** May the builder replace exactly one existing test method, `RecurringProjectionTests.R30_a_purchase_result_carries_no_projection` (:177-192), and the class summary sentence on :13, in the stated shape? Names lost: exactly 1. If NO, the lane cannot be built (STOP at Step 4). **Default YES.** Precedent for a coordinator permitting a single existing-test change: CLARIFICATIONS:772 (the B352 ANSWER-1).
- **Q-7** May the builder rewrite two sentences that become false? They are R-30's last sentence (`ENGINE.md:41`, "Rental only: a purchase result carries no projection ...") and the `RecurringProjection` summary sentence (`CalculationResult.cs:242`, doc comment only). The gate grades sentences, and leaving them would leave false statements at the head. **Default YES.**
- **Q-8** Keep the seat name `Datasec/MPS-M61`. **Default YES.**

## UNMEASURED
- No build, test, compile or mutant was run.
- Whether any Api or Import test pins stored purchase JSON that the new key turns red (the kit makes this a STOP).
- The exact caller-file count at main (25 or 26).
- How many existing harness records carry a source and so gain the key.
- Whether decimal contract figures equal monthly x term with a 28-digit CPP.
- Whether `ReconciliationTests`' source-walker reacts. It did not for X-38 (RELAYED).
- The cost of the sweep.
- The hosted state of anything (fenced).
- The two live seats (`Datasec/ATTIO-R113`, `Datasec/Security-Composer-R112`) belong to other projects. I did not read their kits beyond the port and name scans.

## Outside the fences: disclosure
- **Writes:** exactly the two files above (Write/Edit tools). I also wrote scratch files only in my session scratchpad `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/f8947a38-04ac-46b8-96f3-ceebf0948b77/scratchpad/b1043/`: a Jira reader `issue.py`, the Jira bodies `256.txt` and `rel.txt` (no token), raw source copies under `src/`, `tree.txt`, `heads.txt` and `kits.txt`. I wrote nothing in any project or tree.
- **Network:** Jira GET only (5 issues + the 404 control), with JQL never used. `gh api -X GET` only, under the MPS project's `GH_CONFIG_DIR` (one search/code call returned 404; nothing else). No HTTP to any app host, and no az, ssh or docker.
- **Git in the project repo:** `--no-optional-locks` read verbs only (`grep`, `show`, `config --get`, `rev-parse`, `cat-file -t`, `status --short` on the root). No fetch.
- **Not read:**
  - The decision store (no `decision_queue.sh` in any form).
  - `fleet/briefs_staged/`, `scoreboard.md`, `0_Brain/learnings/_ledger.md`, and any WEDNESDAY or FRIDAY tree.
  - Any `.tools/*` tree of another seat (I only listed `.tools` names).
- **Hooks:** two of my commands were refused before running. One used an unquoted `======` separator; the other a `$D/..` redirect. Neither had any effect, and both were re-run in a compliant form.
- **Template divergence:** DRAFTER_RULES' launch-line paragraph names `cockpit.sh add`, while the template kit (B1015) uses `launch_when_cool.sh` and says "never a `cockpit.sh add` inside the string". I followed the template kit. `BRIEF_SEAT_LEVEL=opus` is inside the quotes either way, and `brief_seat.sh:24` defaults to Opus, so the level matches the row regardless.
