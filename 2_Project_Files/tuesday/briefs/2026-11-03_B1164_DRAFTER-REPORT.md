STARTABLE: YES

# B1164 drafter report (Sonnet drafter, row C8) - kit `2026-11-03_B1164_SEAT-M82_mps-365-quantity-zero-line.md`

## BLUF
MPSCALC-365 is a web-only, two-file lane: one added condition on the counted-device filter at `web/src/screens/bom/quantityAuditModel.ts:100` (plus one clause in the comment at `:99`) and three new rows in `QuantityAudit.severalDevices.test.tsx`. New branch `b1164/mps-365-quantity-zero-device-line` cut from main `b7eebb47f4712d16241b53868f14539dc55a5a2b`. Gate G2 (reason below). Builder C2 `model-routing.md:92`, model id `claude-sonnet-5-5` (`models_latest.json` line 23). No new customer-facing word: `0 per device` comes from the existing template at `QuantityAudit.tsx:77`, the chip is the existing `Not 1 per device`. Partition with M81 (b1146), PRs #120/#121: 0 on every set. Nothing was run (no npm, vitest, lint); the red/green predictions are hand derivations, marked as such in the kit.

## Facts re-measured (instrument; control)
- main = `b7eebb47...` by `gh api git/ref/heads/main` and `git ls-remote`; `compare pin...main` = 0 files; last commit has 1 parent (`git log --format='%h parents=%p'`).
- Jira MPSCALC-365 (own in-process GET, token not printed): Backlog, 1 comment (id 40682, the coordinator's answer), Done-when text quoted in the kit. Also `CLARIFICATIONS.md:2426` (awk NR). Control: the key returned 1 row.
- Raw bytes I read equal the pinned blobs: `git hash-object` of the fetched model and test = `9706104c...` and `856148c3...` = `git rev-parse pin:path`.
- Counting site census (`git grep -n` at pin): `purchaseAudit` read only by `QuantityAudit.tsx:84` and the test file; `mayFlag` only at `quantityAuditModel.ts:104`; other `=== 'device'` sites (`InventoryPicker.tsx:47,97`, `PurchaseBomEditor.tsx:395,521`) do not count audit lines. Control: `perDeviceOf` 2 hits in the model file. This answers the sweep's "second place that counts lines: UNMEASURED" for web: there is one.
- `quantity: 0` in the test file and over `web/src/screens/bom`: 0 hits, rc 1 (control: `quantity: ` prints per-file counts); sweep draws `1 + next(40)` at `:279`.
- Engine pointers `PurchaseCalculator.cs:732`, `:920` printed by awk NR; the ticket's `:692` is stale (the comment on the ticket says so).
- Prior work: `git log -S` on the filter text finds `67bf200` (#86, origin of the audit) and `6e0aa64` (#138 added `mayFlag`); `-S 'quantity > 0'` and `-S "quantity: 0"` and `-S MPSCALC-365` find nothing. Gate B1078 already measured this exact case (HQ7 row, mutant GQ3 red on HQ7 only, `B1078_STATUS.md:61`, `:90`).
- Partition (`grep -c -x -F -f`, planted control prints 1): my 2 paths vs b1146's 12 compare files 0; vs PRs #120/#121 files (2, both `web/package-lock.json`) 0; vs M81's B1162 LANE paths 0. Branch `b1116` is on origin and lists both audit test files, but it landed as #143 (`17fc0db` in the pin's history).
- Ports: none assigned; `lsof` listeners at drafting: 49152, 5000, 59869, 7000, 49166, 49168, 49171, 64703 (none ours). Word-boundary scan of non-`.pre-` SEAT kits dated 11-03 (B1164 excluded) for my two paths: 0 (control: B1162 names `Dtos.cs` 16 times). 11-02 kits that name my paths: 11 finished seats' kits (listed in the kit). Live panes: `tuesday`, `Datasec/MPS-M81`, `Datasec/Security-Composer-G300`, `fleet-monitor`.
- Machine: load1 6.76 (00:55), 8.53 (00:58); `df -g` 257 GiB. gh account active under the project config is the Datasec one.
- REFUSE tests against launch truth: `.tools/b1164` absent (`ls -d` fails; control `.tools/b1125` present), local `b1164*` refs 0, origin `matching-refs/heads/b1164` 0 (control `b1093` 1), main-moved regex prints 1 for each planted path and 0 for `docs/API.md`, `TemplateIsolationTests.cs`, `PurchaseBomEditor.tsx`, pane M82 count 0 (control M81 1), Node 24 binaries print v24.21.0. The slot count is 9 in the kit; the `.pre-stamp` control ("copy reads 9") needs Tuesday to keep an unstamped copy, as for B1162.
- Caught while drafting: the machine's load is above 7 now, so the REFUSE for load would have fired if I had made it a refuse. It is deliberately NOT a refuse (heavy.sh waits; a 60-minute wait writes WAITING; at the hard stop it ends BLOCKED). The kit's "any kit naming my paths" refuse also would have fired on 11 finished 11-02 kits; I narrowed it to 11-03 kits plus live panes and listed the finished ones.

## D-decisions (kit makes; Tuesday stamps)
- D-1 Build the coordinator's recorded answer as written; STOP if a newer comment reverses it.
- D-2 Condition is `> 0` (the ticket's words), which also excludes negatives.
- D-3 Update the one comment at `:99` by one clause (otherwise it states a rule the next line no longer follows). It is developer prose only.
- D-4 Three rows (A rendered per the ticket, C same with zero line first, B model result with literals), all red at the unedited pin. A "every device line is zero" row is NOT built: it is green at the pin and under the fix and no plant of that line turns it red (the ruling at `CLARIFICATIONS.md:2214-2218` forbids committing it).
- D-5 Plants PA (condition removed), PB (flipped to `=== 0`), PC (boundary `> 1`, a measurement only), P0. Plants run on the fixed file in `-mut`, over the folder `src/screens/bom`.
- D-6 No timeout, config or dependency change; `web/package-lock.json` held for #120/#121.
- Gate G2, not G1: advisory staff-facing chip, no quantity or price change, not deployed (card-per-deploy), and the same panel's rule was G2 at B1078 whose gate measured this very case; fits `model-routing.md:109` "follow-ups whose mechanism a prior gate already measured". It becomes G1 if the answer is overruled into something a tester reads as a quote figure, or the change grows past the filter.

## Q-questions for Tuesday (each with a default)
- Q-1 Negative quantity: does the editor let a person type one? UNMEASURED. Default: `> 0` as the ticket words it; report only.
- Q-2 Comment at `:99` updated (D-3)? Default yes. If you want zero non-code bytes in the product file, strike the comment sentence in Step 7 and the "2 lines removed" figure in Step 10(b) becomes 1.
- Q-3 Worktrees at `.tools/b1164/wt-b1164-fix` and `-mut` (inside the seat's own directory, as B1125 did) rather than `.tools/wt-b1164-*` as B1162 does. Default: inside `.tools/b1164`.
- Q-4 Should the launch also wait for M81's heavy lock to clear? Default no: the seat-local lock plus the load1 below 7 gate only, as the template does (M81's `.tools/b1162/heavy.lock` exists now; I only `ls`-ed it).
- Q-5 Gate class name: "web: quantity audit, a zero-quantity device line is not a counted device line", round 1 of 2. Default as written.

## UNMEASURED
- Whether the three rows are red at the pin and green after the edit, and PA/PB/PC outcomes: derived by hand from `quantityAuditModel.ts` and `QuantityAudit.tsx`, not run.
- Whole web suite duration and whether it finishes under load above 7 (M81 is running its own); the baseline red set (MPSCALC-369's five rows may time out).
- Negative-quantity input (Q-1); whether any ticket beyond 300, 262, 365, 366 owns the filter (the seat re-runs the text search).
- `npm ci` and the production build at the pin; hosted CI and CodeQL.
- Local `2_Project_Files` working tree is stale (HEAD differs from the pin); every read was of pinned objects or origin.

## Outside-the-fences disclosure
- Wrote only the two named files plus scratch files in the session scratchpad (`jget.py`, copies of the two pinned files, small lists).
- Jira: one read-only GET (script printed fields to my terminal; token never printed).
- `gh api -X GET` only; git read verbs with `--no-optional-locks`. `tmux list-panes`, `lsof`, `df`, `uptime`, `node --version` on two Node binaries (read-only runs). No fetch, no checkout, no worktree, no `decision_queue.sh`.
- Read `.tools/b1125/{heavy.sh,hb.sh,ci.sh,plant.sh,mutate.py,jira_read.py}`, `.tools/b562/jira.py` (headers/bodies) as templates, and the project's `1_Project_Definition/CLARIFICATIONS.md` lines and `Briefs/` STATUS files for B1078 and B1119 (verdict lines only). Did not read `fleet/briefs_staged/`, the scoreboard, `_ledger.md`, or any Wednesday/Friday tree.
- Two Bash calls were refused by hooks (a `cd` in my first attempt; an unquoted `====`) and re-issued correctly; one zsh `$M:path` modifier mishap returned errors and was redone under `bash`, nothing written.
