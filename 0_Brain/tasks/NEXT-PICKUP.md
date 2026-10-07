---
date: 2026-10-08
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE 2026-10-08 05:3x by the overnight seat (booted 02:4x) at the 05:30 shift-change wrap, ctx ~61%. Previous copy in that session's scratchpad (NEXT-PICKUP.pre-0530.md). Replace wholesale again; never stack.
---

# NEXT PICKUP

## 🔴 FIRST ACTS — the 06:00 MORNING seat
0. `kam_rulings_today.sh` + `reconcile_rulings.py`. Kam silent since 10-07 13:02. **USAGE 89% at 05:51 → at 90% nothing new launches.** Card `secuura-usage-89pct-raise-backlog-1008` (rec a: 100% for raise/gate/merge seats; default c: hold to Sun 11 Oct renewal) is the first thing in the morning brief. Other open cards (both default nothing): `secuura-demo-disk-too-small-to-rebuild-1007`, `secuura-standing-build-cache-prune-1007`.
1. `inbox_digest.sh --inbound` WHOLE + `--all` for `[QUESTION]` rows in the last 12 h, each matched to a later ANSWER. Save bodies with `inbox_digest.sh full <inbox> <id>` into `fleet/briefs_staged/`. **Read every seat mail through to NEEDED-BY.**
2. **R 15th is LIVE (%91 `Secuura/Blockchain-R`)** — see FLOOR. Its plan confirmation is the first thing owed.
3. **Morning brief LEADS with (value first):** gate74 GO (#1423), R 15th merging #1422 + #1423, the Spark census (24 unraised passes found, 10 now held), and the BLOCKER: **develop red on pre-push leg 14 → KS-1450** (Peter's #1424) blocks every push touching `Blockchain/Dev/`. Give Kam a 1-2 line WhatsApp text pointing at https://linear.app/secuura/issue/KS-1450 in case Peter has not seen it (Kam sends; nobody else messages Peter).

## 🔴 09:2x — KAM RULED (read first)
- **Usage = a:** 100% for raise/gate/merge (≤ 2 deploy) seats until the renewal / account switch → `learnings/2026-10-08_use-to-100pct-raise-gate-merge-seats-only.md`, EXPIRING-GRANTS row. Launch past 90% with `WED_USAGE_STOP=100` naming it.
- **Demo disk = a (grow)**, after Wednesday answered his G-drive question (measured: Azure VM ~170 ms away; G-DRIVE a USB HDD; not viable). **OWED: brief a D seat** (`Secuura/Blockchain-D`) to READ the demo disk's SKU, current size, a ~128 GiB target and the monthly price in the Secuura subscription, then Wednesday CARDS Kam the exact figure. **No resize before his tap on that price card (money).** Then demo deploy resumes from D 16th's handover (3 images built).
- **Build cache = b:** the NEXT kintsugi deploy seat prunes kintsugi's build cache ONCE (build cache only), reporting free space before/after.
- **New card OPEN:** `secuura-ks1450-leg14-who-fixes-1008` (rec c nudge-then-fix-at-18:00; default b wait). Until it or Peter resolves KS-1450, every `Blockchain/Dev/` push is refused, so the raise backlog cannot move.

## FLOOR (06:2x)
%0 wednesday · %1 monitor. **No agent live.** R 15th WRAPPED (0.94, pane closed; handover `HANDOVER-seatR15-2026-10-07.md` da495708b0364f65). **The gate74 round is DONE: #1422 → 4afefcbfb064, #1423 → develop ddea005553bf65ffc284a9124a02ad53c5f88019, both verified at source.** Next R seat = R 16th (its handover's first three things). Nothing launches until Kam rules the usage card or the allowance renews.

## R 15th — what Wednesday owes it, in order
1. ~~plan confirmation~~ **DONE 05:3x** (ANSWER 18:34Z: confirmed, ctx 23%, no pull; c4 to be re-run with `--expect-tree`). **NEXT from it: `QUESTION: ctx read (Seat R 15th)`** after its step 1 (builder + m7_squash + m1_go_complete + provenance_ra15, all arms), carrying the c4 11/0 + wrong-tree numbers → pane ctx → ANSWER → GO 1422.
2. ~~GO 1422~~ **SENT 05:50** (`fleet/briefs_staged/2026-10-08_seatR15_GO_1422.md` + `…_ADDENDUM_1422.md`, 0 new failures; 13/13 builder parsers; values verified in Wednesday's clone). R 15th ctx 32% at 18:49Z.
3. ~~#1422~~ **MERGED → develop 4afefcbfb06445f0f9a8a7c1f3e29e414b2909d3, verified at source by Wednesday (06:0x).**
4. ~~GO 1423~~ **SENT 06:09** (`…_seatR15_GO_1423.md` + `…_ADDENDUM_1423.md`; T' d6ee60d9 on 4afefcbf; Actions vs base 0 new). **#1423 MERGED → develop ddea005553bf, verified at source by Wednesday 06:1x. NEXT: its WRAP** (tree == d6ee60d91e2f, one parent == 4afefcbfb064, subject 73, 3 paths, 0 trailers, PR `merged` field) → its WRAP → score, `pane_close.sh %91`.
5. R 15th then wraps; its handover carries R 16th's traps.

## 🔴 THE BLOCKER — develop red on pre-push leg 14 (KS-1450)
`systemTest/__tests__/no_hardcoded_slot_literals.test.sh` fails at develop on 8 `slot2` lines in `systemTest/schemathesis/config/schemathesis-baseline.json` (Peter's 89dff83aa / #1424). Two of the lines are run-id strings in a JSON array that cannot carry the guard's marker → **Peter's call** (guard KS-1386 and baseline are his). Root: the hook runs the full preflight only on `^Blockchain/Dev/` changes, so systemTest-only merges skip leg 14. **Nothing of ours edits his guard or baseline; never `--no-verify`.** Watch KS-1450 for his answer and `ls-remote` develop for a fix.

## RAISE BACKLOG (all blocked behind leg 14, except nothing) — census `0_Brain/reference/2026-10-08_spark-hold-census/CENSUS.md`
- **R2 KS-1274** built + committed, NOT pushed (`feature/ks-1274-trivy-bare-object-guard-ra14-1` 32e263890b69, worktree `s-ra14-ks1274`; R 14th's handover e748ea224a1b360d). Re-cut on the fixed develop. R3+R4 KS-1410 and R5 KS-1139 unbuilt (READYs in `night/`).
- **Held 2026-10-08 (READY files in `local-model/night/`, `_spark-dsv4flash_`, dated 2026-10-08):** KS-591 MINTUPLOADFEE + KS-1364 IPFSPINUNPIN (nft pair, ONE seat, stacked, `Refs KS-1449`), KS-1364 ORIGINATESHARESYSTEMERRO, KS-1364 TEAMSWEBHOOKNOTIFY, KS-591 ANCHORSPOSTTHREADMINT, KS-591 BILLINGCUSTOMERSBUNDLE, KS-591 PLATFORMTENANTSCREATESTA, KS-591 STAKECOMPLETEUNSTAKE, KS-591 TRANSFERDELEGATIONPOSTS, KS-808 APPLIEDCOUNTSSKIPS. Held 10-06, never raised: KS-1328, KS-1355 stack-guard, KS-1364 apigw-batch, KS-593 signatories.
- **Still to hold** (each its own handling): KS-1171 b1-boundary-pin (checker not code_patch mode), KS-1364 analytics-exports-r4 + billing-credits-use-r4, KS-593 adminconfig-negative-offset-r2 + share-null-recipient-cp2 (brief dirs named differently from run dirs).
- **Need a REVIEW first:** KS-865-r2, KS-948-r3, KS-1355 dev-reload-r2, KS-1432, KS-591 platform-tenant-id-uuid.
- **Shared-file pairs → one seat each, stacked:** billing.openapi.ts, nft-certificate.openapi.ts, tenant-provisioning.openapi.ts. Otherwise file-disjoint: partition into SEVERAL raise seats when green (as-many-agents rule). Biggest throughput lever of the day.

## Spark
Queue EMPTY with a why-line (03:00 screen `0_Brain/reference/2026-10-08_spark-screen/SCREEN_0300.md`: 13-ticket delta, 0 new briefable). Re-screen when develop moves or new KS tickets land. KS-1448 = security → Claude. **KS-1447** (Peter-created, UNASSIGNED; systemTest guard implementing Kam's KS-592 2026-08-26 ruling): owner question — read it at source; the 09-06 rule makes unassigned Platform K tickets ours.

## OWED (Wednesday tooling)
- gate-kit ADDENDUM provenance check in the template (STANDING_LINES :437).
- `cockpit.sh say %<id>` prints nothing and does nothing: tap by pane NAME until fixed.
- `pane_close.sh` should stop a seat's detached `inbox_watch*` by record-folder path.
- The announced-step STALL watcher leg; `safe_push.sh:108` / `wed_claim.sh:54` internal `--autostash`.
- A REVIEW verdict of HOLD must write the READY in the same action (ledger 10-08): put that line in the Spark review-commission template.

## STANDING NOTES
- Pathspec-only commits; pull with `tools/safe_pull.sh`. decisions.json and the chat stores are STATE.
- A seat CANNOT read its own context: gates are mail handshakes; Wednesday reads the pane.
- Receipts quoting a send's output are written AFTER the output is visible. Quoted heredocs only.
- Before any GO, copy the seat's GO shape from its brief and run the seat's builder regexes against it.
- Write verbs only in your own scratch clone; the hook needs LITERAL paths in `git -C` (it cannot resolve `$VAR`).
- Grants live: October deploy (to Sat 31 Oct), week instruction (to Sun 11 Oct), TESTED merge grant (open-ended).
