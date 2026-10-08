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

## 🔴 16:4x 2026-10-08 — LIVE STATE (read first; supersedes the 14:3x block)
- **Kam /login 14:3x → new account, "use as much as you like; push and merge what you can, test as much as possible"** (`learnings/2026-10-08_new-account-push-merge-test-as-much-as-possible.md`; EXPIRING-GRANTS row; EVENT = renewal ~Fri 9 Oct morning). Launch with `WED_USAGE_STOP=100` naming it.
- **RAISE ROUND** (report `0_Brain/reference/2026-10-08_raise-round-after-ks1450/REPORT.md`): **R 18th LIVE %95 · G 4th LIVE %96** (`…_seatG4_raise_originate_ks593_ks1171.md`, amended + launched 16:5x; owed: its plan ANSWER, and Q-READ593: Wednesday reads the built `routes/documents.ts` diff before G-A's push) · (`fleet/briefs_staged/2026-10-08_seatR18_raise_r2_r5_ks1450done.md`; it closes KS-1450 → Done first). **NOT YET LAUNCHED, each READ WHOLE + amended before send (the G 4th amendment is the template):** `…_seatE11_raise_openapi_ks591_ks1364_ks1449.md`, `…_seatF5_raise_scripts_ks808_ks1355_ks1328.md`. On launch, mail R 18th and G 4th the new pane id. The send gate needs every ticket named in the QUEUE in PROVENANCE, including tail keys like KS-1164, and refuses any placeholder token quoted in prose. Their open questions (REPORT §Open questions): E's doc-key tool (until ruled, E builds only the KS-1449 pair); E regenerates the YAML; missing READY files for analytics-r4, billing-credits-r4, adminconfig-r2, share-cp2, KS-1171 (hold them first, or the seat raises from review + patch and says so); share-cp2 and KS-808 diffs Wednesday reads before the push; F borrows E 10th's raise tools re-keyed to f5. Linear reads done 05:40Z (in the R 18th amendment; KS-1328 unassigned = ours). Mail each live seat the new pane ids when they launch.
- **R 18th, owed by Wednesday:** plan confirmation → read through NEEDED-BY → pane ctx → ANSWER; then the KS-1450 Done write; RAISE_BASE acceptance BY NAME; ctx reads before every build and push.
- **oMLX TEST TONIGHT** (Kam 16:12): report `0_Brain/reference/2026-10-08_omlx-flash-next/REPORT.md`; drive-local install DONE; **106 GB download RUNNING** (log `2_Project_Files/tools/omlx/setup.log`, script `local-model/omlx_setup_and_download.sh`). Tonight: quiet the Mac (Ornith down, browsers closed), serve on 47780, bench.py; fallback gpt-oss:120b. Kam's open questions are in the report (ask one at a time).
- Laptop-DEV → DevMASTER Datasec copy: DONE and reported twice.
- Stash hazard: `stash@{0}` (16:08, wed_claim autostash) is KEPT; state was verified equal. After any `wed_claim.sh` call, run `git stash list` and `git status`.

## 🔴 14:3x 2026-10-08 — LIVE STATE (read first; supersedes the 13:3x block)
- **KS-1450 round CLOSED.** #1426 merged → develop **0a6177ea5482227e83d5045b68b8577a56326ffc** (verified at source by Wednesday); the KS-1450 comment cea25ad0 was read back by id (Peter told). R 17th scored 0.97 and wrapped (handover `HANDOVER-seatR17-2026-10-08.md` 9933eea0319606c9, "FOR R 18th"). **No agent live.**
- **Card OPEN:** `secuura-raise-backlog-at-99pct-1008` (a: Kam /login; default b: hold new Claude seats to the Sun 11 Oct renewal). On a: brief R 18th+ raise seats from the census, partitioned by file (shared-file pairs stacked in one seat), each under the 09:17 grant (or the new account's gauge); R 18th's traps are in R 17th's handover.
- OWED to the next Secuura seat: **KS-1450 → Done** (board write); KS-1451's change must anchor the path, bound membership by position, correct the doc clauses and its own description.
- OWED Wednesday tooling: gate75's repin must export WED_USAGE_STOP for its own `cockpit.sh add`; gate kits should check the merge seat's inherited builder against the head's real shape (trailers).

## 🔴 13:3x 2026-10-08 — LIVE STATE (read first; supersedes the 12:3x block)
- **gate75 = GO for #1426** (scored 1.0, pane closed). **R 17th LIVE (%94 `Secuura/Blockchain-R`)**, brief `fleet/briefs_staged/2026-10-08_seatR17_merge1426.md` (SEND AMENDMENT at top). Owed to it, in order: plan confirmation → read through NEEDED-BY → pane ctx → ANSWER; then its builder arms → **GO** (subject `[Wednesday -> Secuura/Blockchain-R] GO (Seat R 17th): merge 1426 on gate75`, every M1 line once; body file `gatesets/2026-10-08_gate75/merge_inputs/1426.squash_body.GATE75_CORRECTED.txt` 10735 B cf71406f…; comment file `…/KS-1450_comment.GATE75_CORRECTED.md` c9da667f…; report sha ff94ef79…) + **ADDENDUM** (Wednesday's own Actions read: 0 new failures, per gate75 class rules). Test the GO against R 17th's NEW builder regexes before sending. Then verify the squash at source → its KS-1450 comment → WRAP → score → pane_close.
- After the merge: develop green on leg 14 → raise backlog (census `0_Brain/reference/2026-10-08_spark-hold-census/CENSUS.md`), file-partitioned raise seats under the 09:17 grant. KS-1451's change must also: anchor the path, bound membership by position (gate arms A4v/N4v/O1 must red), correct the doc clauses, and correct its own description's "all five guards".
- **Datasec copy Laptop-DEV → DevMASTER DONE** (Kam 12:34; verified, Tuesday told). Nothing owed.
- OWED tooling: gate75's repin must export `WED_USAGE_STOP` for its own `cockpit.sh add` (it refused once at 90%).

## 🔴 12:3x 2026-10-08 — MIDDAY SEAT STATE (read first)
- **R 16th WRAPPED + scored 0.96, pane closed.** No agent live. #1426 head dd31aa0c998c / develop ddea005553bf (Wednesday's `git -C <Secuura checkout> ls-remote origin`, 12:2x).
- **gate75 kit drafter RUNNING** (background sub-agent) → `fleet/qa-agent/gatesets/2026-10-08_gate75/` + `fleet/briefs_staged/2026-10-08_seatR17_merge1426_DRAFT.md`. A rotation kills it: re-commission from the 12:27 note line. NEXT: read KIT_REPORT whole → rule its questions in `RULINGS_wednesday.md` → dry run → launch with `WED_USAGE_STOP=100` (Kam 09:17 grant, gate class) → verdict → R 17th merge → KS-1450 comment → raise backlog.
- Usage 95%: Spark re-screen (a drafter) waits for the renewal; everything held is blocked behind #1426 anyway.

## 🔴 12:0x 2026-10-08 — ROTATION HANDOVER (morning seat, ctx ~79%) — READ THIS FIRST
- **#1426 = the KS-1450 fix, READY FOR QA** (R 16th, `fleet/briefs_staged/2026-10-08_seatR16_READY.txt`, 99 lines): https://github.com/Secuura/Distributed_Secuura/pull/1426 · head **dd31aa0c998ca43291c975dccb906a42e55c73c2** (Wednesday's `ls-remote` 12:0x) on develop ddea005553bf. Guard 8/1 at develop → 11/0 at head; arms A1-A4 RED (A4 caught only by the jq membership cell), A5 = the ruled named limitation; full preflight 71/0, 12/15 legs (3 stack legs SKIPPED), in-hook on the push too. Both docs carry one parity clause (D1 :1268, D2 :2169). KS-1451 filed (five-guard bare-marker gap). The DRAFT KS-1450 comment is in its READY mail, NOT posted.
- **FIRST ACTS for the successor:**
  1. R 16th's WRAP (expected next; ends at READY) → re-hash its handover, score, `pane_close.sh %92`.
  2. **Commission the gate75 kit** (one PR, #1426, TIER 2: a guard change; red-proof is the heart of it — every arm re-driven by the gate, especially A1/A4, plus a planted literal in a NEW harness file). Shape: `fleet/qa-agent/gatesets/2026-10-08_gate74/` (copy, re-key). Usage 94%: a gate is inside Kam's 09:17 grant → `WED_USAGE_STOP=100` naming it.
  3. On GO: a merge seat (R 17th; its traps are in R 16th's handover) lands #1426; verify at source; THEN the KS-1450 comment goes on the ticket (tell Peter, don't ask; text = R 16th's draft, re-read against the head).
  4. Once develop is green on leg 14: the raise backlog (10 held READYs + KS-1274 + R3-R5), partitioned by file, raise seats under the 09:17 grant.
  5. Still owed from Kam's 09:18 rulings: the demo-disk pricing D seat (card the monthly figure before any resize); kintsugi's one-time cache prune at the next kintsugi deploy.
- Kam's standing rule today: we fix our own problems; Peter only sporadically (`learnings/2026-10-08_fix-our-own-problems-involve-peter-sporadically.md`).

## 🔴 10:5x — KS-1450 BEING FIXED BY US (read first)
- **Kam 10:45: KS-1450 = a (fix it now)** + STANDING RULE: we fix our own problems and tickets, Peter only sporadically (`learnings/2026-10-08_fix-our-own-problems-involve-peter-sporadically.md`).
- **FLOOR: %0 wednesday · %92 Seat R 16th** (brief `fleet/briefs_staged/2026-10-08_seatR16_fix_ks1450_leg14.md`; rung 5 verified) · %1 monitor.
- **NEXT from R 16th:** plan confirmation → read WHOLE → pane ctx → ANSWER (check its fix design keeps a planted literal in ANOTHER baseline key failing). Then its ctx QUESTION before the push → READY FOR QA with the draft KS-1450 comment → a tier-2 QA gate (batch nothing; it unblocks everything) → merge seat → THEN post the KS-1450 comment (tell Peter, don't ask) → the raise backlog unblocks.
- **USAGE 94%.** Only raise/gate/merge (≤ 2 deploy) seats may launch, with `WED_USAGE_STOP=100` naming the 09:17 grant. The demo-disk pricing seat is a deploy-class seat: allowed under the same grant, but only one deploy seat at a time.

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
