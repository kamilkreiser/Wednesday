# B433 drafter report (HPSM-POC UAT budget alert, card hpsmpoc-uat-budget-alert-1021)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B433_SEAT-B1_hpsmpoc-uat-budget-alert.md` (about 70 lines, slots: the Stamp paragraph and the final line, both `@STAMP@`; the REFUSE rule counts `@[A-Z_]+@` and so reads 0 once stamped).

## Route: CLI, not template (MEASURED + RELAYED)
- MEASURED: `git grep` on origin/main `infra` finds a budget only in `infra/showcase-ai.bicep:91` (the showcase group). None in `main.bicep` or its modules, none named `budget-hpsmpoc-demo`.
- RELAYED: the demo budget was made by az CLI/REST (B98 D-7 "az CLI or the portal"; `B102_STATUS.md:52,72` with its `az rest delete` rollback). So a CLI create + read-back is consistent; a template PR would make UAT unlike the demo. Recommendation: CLI.
- Caveat, UNMEASURED: whether a UAT template deploy leaves an unnamed budget alone (incremental mode). `git grep` for `--mode|deploymentMode` printed 0 lines, no positive control. Closing instrument: a `budget list` after the next UAT template deploy (in FOR TUESDAY).

## Facts the brief rests on
- Subscription `a6b8fe11-...`, tenant `ec01829b-...`, "Azure subscription 1": RELAYED, `B410_STATUS.md` Step 0. The project CLAUDE.md names none (grep 0).
- Demo budget (RELAYED, `B410_STATUS.md:65,116`): A$401 now (150 at creation; a user write on 19 Oct, B316 FOUND-2, C-124), 3 forecast alerts 50/80/100 %, group scope. The brief copies thresholds and recipients (read at runtime, masked to count + domain) and NOT the amount, which is the card's A$150.
- `budget-hpsm-poc-sm` has a different shape (actual 50/80/100 + forecast 100). The card says "same as the demo's", so the demo's wins; the seat says if the live read differs.
- B410 stood up UAT and created no budget (its Open item 2): no prior work to duplicate. A budget on the UAT group does not exist as of B410; the seat re-checks.

## Decisions for Tuesday
1. **Model: Opus 5.5.** Routing row C6 (Azure-writing seat) is the nearest row; it names Opus 1st and Sonnet "no (unmeasured)". No row names a budget-only write. Sonnet is probably adequate for one reversible create, but the table does not support it; override is yours.
2. **Authority line** is left for the Stamp to fill: the card's timed default (09:00 22 Oct) or Kam's tap. The brief voids itself if the card was ruled b or c.
3. **Forecast alerts on a brand-new group** need usage history, so none may fire for days (written under NOT TESTED). If you want an Actual alert too, that is a changed brief, not this one.

## UNMEASURED
- Spend of a budget (nil): from Microsoft's documentation, recalled, not fetched. Closing instrument: no budget meter in the Cost lines after a day, plus the before/after resource lists.
- The live demo budget's current thresholds and recipients (the seat reads them).
- Whether `az consumption budget` works under the project's CLI version (preview group; the brief gives the `az rest` fallback B410 used).
- Weekly gauge (P2/P3): your launch check.

## Fences kept
Read-only. Only local file reads, `decision_queue.sh show hpsmpoc-uat-budget-alert-1021`, and `git --no-optional-locks grep`; no az, HTTP, mail or card writes. Two files written, plus one hook refusal of a `cd` (retried without it).

Launch line (Tuesday, after stamping):
`WED_USAGE_STOP=100 bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/HPSM-POC-B1 "BRIEF_SEAT_LEVEL=opus bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B433_SEAT-B1_hpsmpoc-uat-budget-alert.md'"`

Files:
- /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B433_SEAT-B1_hpsmpoc-uat-budget-alert.md
- /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B433_DRAFTER-REPORT.md
