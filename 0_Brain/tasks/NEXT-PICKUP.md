---
date: 2026-10-06
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE 2026-10-06 10:4x by the day seat (booted 09:4x, 66% checkpoint); UPDATED IN PLACE at the 70% checkpoint 10:5x. Replace wholesale again; never stack.
---

# NEXT PICKUP

## 🔴 FIRST ACTS
0. `kam_rulings_today.sh` + `reconcile_rulings.py`. Kam is on the live board. Today's rulings: 09:37 **Spark takes 80% of tasks** (past 70% weekly); 09:57 **KS-1402 = a** (originate resolves the holder with its own tenant-scoped credential); 10:22 **KS-1256 card = a** (fail closed, 503, during a Redis outage).
1. `inbox_digest.sh --inbound` read WHOLE, AND `--all` for every `[QUESTION]` in the last 12 h matched to a later outbound ANSWER (ledger 10-06: a QUESTION was lost across the 09:4x rotation). An unmatched question is answered first.
2. develop = **3f9ff4e1e1b9** (#1385 KS-938 merged by E 6th; VERIFIED at source by Wednesday: tree 2203187daaa2, 1 parent 22b268143a63, 0 trailers). It is ABSENT from the shared store until a seat's objects-only transfer.


## 🔴 STATE AT THE 70% CHECKPOINT (10:5x): this block supersedes the table below where they differ
- **gate68 = GO on #1393 at b5adaba751d8** (saved `fleet/briefs_staged/2026-10-06_mail_g68.txt`; scored 1.0). Merger **Seat B 67th**, launched in the B pane AFTER B 66th wraps. Wednesday signs `GO (Seat B 67th): merge 1393 on gate68` naming the TAIL-rule tree re-predicted on the then-develop (1711f2b944a8 on 3f9f; if #1394 lands first, re-predict). B 67th files the residue: one assertion ticket (anchored R2 for T5b + a 22P02 double for N2 / U1); KS-TICKET → KS 1424; flow follow-ups N-1393-8/-9/-10; the documentRepo.ts:629 comment. The KS-1419 correction text needs gate68's three edits (sentences 1/3/8) before any relay. Then the **KS-1402 build** can launch (brief staged, read it whole first; lock `-g1`).
- **B 66th** (ctx 31%): plan CONFIRMED 23:5xZ (Q-BODY + Q-SQ verbatim). Next: its READY → **commission the T2 TEXT re-check of #1394** (body + declared squash body + develop re-read; NOT a code gate) → `GO (Seat B 66th): merge 1394 on gate67` with the key-anchored tree re-predicted on the then-develop (6884601a03dc on 3f9f).
- **Seat R 1st** (ctx 40%): PR 1 KS-1305 built; ADD C3 ruled (code conjunct). Expect PR 1, maybe PR 2, then ITEM 6 READY → gate69 (kit not yet drafted: commission it when the READY lands).
- **E 7th** (ctx 29%): plan CONFIRMED 23:5xZ; develop already in the store (R's transfer). Expect a READY (T1) → a KS-1256 gate.
- **Spark:** KS-1364 + KS-593 HELD (READY_ files in `local-model/night/`; KS-1364 carries a YAML companion diff, so regenerate if #1394 lands first). Queue empty: next screen. A pre-existing finding for a board seat: the signatory routes do not check org membership (search first).
- **Kam cards OPEN:** `secuura-uuid-revokes-never-wrote-status-history-1006` (default: nothing queried).
- **Git hygiene (ledger 10-06):** commit with explicit pathspecs only; after any rebase recovery, inspect every new autostash. `stash@{0..3}` are kept, NOT dropped (their non-generated content has been restored).

## LIVE FLOOR (verify with `tmux list-panes -t fleet:0`; read ctx by enlarging a pane to 14 rows)
| seat | pane | job | waiting for |
|---|---|---|---|
| **Seat R 1st** (new lane, lock `.push-lock-d8`, token ra1) | `Secuura/Blockchain-R` | raise the 5 held Spark passes (KS-1305, 1136, 998, 1313+KS 1326, 1164) as 5 PRs, ONE READY → **gate69** | its STATUS/READY. Plan confirmed 23:4xZ. MERGES wait for #1394 to land (re-rule in its GO if not). After PR 4 merges: close #1245 with one pointer comment (Kam card a). |
| **Seat B 66th** (lock `-56`) | `Secuura/Blockchain` | #1394 (KS-723) body fix for gate67's TEXT NO GO, then a T2 text re-check (Wednesday commissions it), then merge on `GO (Seat B 66th): merge 1394 on gate67` | its ITEM 0 (pre-ruled). END_TREE predicted on 3f9f = **6884601a03dc** (key-anchored; merge-tree 21c445285cb3 rc 1, DIVERGENCE). KS-723 must STAY OPEN. |
| **gate68** | `QA/Secuura-ks1278-1393r2` | #1393 (KS-1278) round 2 of 2 at **b5adaba751d8**, T1 | its verdict (coagent@ `[QA -> Wednesday] GATE68`). Rulings in `gatesets/2026-10-06_gate68/RULINGS_wednesday.md`: merger **B 67th**, target TAIL `1711f2b944a8`, assertion gaps (T5/T5b) = ticketed residue if the product is proven. KS-1419 correction text HELD until this gate reads it. |
| **Seat E 7th** (lock `-e4`) | `Secuura/Blockchain-E` | finish KS-1256: adopt `s-e6-ks1256` (local commit **e16c3133**), merge develop in (predicted tree 9c6cf0171127, 0 conflicts), docs `21.`, ks1195 title, push, PR, ONE READY (T1) | its ITEM 0 (pre-ruled; must cover `-d8` at push). Kam ruled the card a, so there is no time hold. |
| fleet-monitor | `%1` | — | — |

## HELD (do not launch until its condition)
- **KS-1402 build (Kam ruled a, 09:57)**: brief staged `fleet/briefs_staged/2026-10-06_seatK1402_build.md` (NOT yet read whole by Wednesday). **Launch only after #1393 MERGES**: it shares originate `routes/documents.ts`. Mechanism: originate has NO service token; resolve via originate's OWN tenant-scoped DB read (provenance.ts resolveOnBehalfOf). A service JWT would FAIL OPEN at auth users.ts:306. Risk to measure at ITEM 0: legacy plaintext-email rows would 404. Lock: reuse `.push-lock-g1` (never a new name). Tell Kam the mechanism reading at launch.

## SPARK / ORNITH
- Spark queue: KS-1364 apigw batch certify/delegate + KS-593 signatories 400-not-500, `queue.sh` started 10:1x (log in the session scratchpad). Results → `local-model/spark/done.md`. Read every PASS diff against its brief and HOLD it; FAILs get a classified fix (model/harness/brief). Screen: `0_Brain/reference/2026-10-06_spark-screen/SCREEN.md`.
- Ornith PAUSE to 18:00 (its 2 candidates went to the Spark). Re-screen when a lane wraps.
- **80% share:** Claude launches since 09:37 = 4 (R raise · B 66th merge · gate68 · E 7th raise); Spark tasks 2 run + 5 raised.

## SCORED TODAY
B 65th 0.95 · E 6th 0.95 · gate66/67 1.0 (previous seat).

## OWED (carried)
- DEFECT A (matcher addressee precedence) relayed to B 66th/E 7th + STANDING_LINES. F/G lanes inherit it at their next launch.
- Refresh the shared checkout's origin/develop (KS-1422) via a seat, only with no seat mid-round.
- Orphan watchers: B 65th 31017, E 6th 31713, F 3rd 12127, F 4th 89913. Each lane's next seat stops its own (B 66th rules 31017).
- #1383 (KS-1401): no seat; F 5th rebuilds the merge-in on the live develop (GIT_SSH_COMMAND unset = the rc-141 root cause).
- G lane: KS-1127 leg-14 half: no Spark runner (screen), so a Claude seat later.
- `inbox_digest.sh` withhold filter misses QA-tagged Datasec previews. `cockpit.sh say %NN` prints nothing and delivers nothing: use the cockpit NAME.
- Spark tooling: no tier runs a bash test-only change (blocks N-1387-2, N-1389-3); `round.sh:204-206` doubles a path prefix.
- Kam's 20:06 (10-05) rulings → tickets; ~54 undelivered Secuura cards (board-pass backlog).

## WITH KAM
Nothing waiting. Grants live: October deploy (to 31 Oct), week instruction (to Sun 11 Oct), 80%-Spark (to the allowance renewal).
