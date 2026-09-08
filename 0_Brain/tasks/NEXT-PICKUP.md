---
date: 2026-09-08
type: pickup
scope: SECUURA ONLY on this machine — Kam, panel 07:08:23: "only secuura projects on this machine until further notice". Datasec is the LAPTOP's; read its mail by SUBJECT only.
source: replaced WHOLESALE at 09:05 by the 22:26 seat at its 65% checkpoint
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — 10:30 Tuesday, written at the 80% rotation. ONE card on Kam's desk. Seat archiving.

## 🔴 FIRST: RUN THE NEW TOOL, THEN READ HIS PANEL
`2_Project_Files/tools/sync_kam_rulings.sh --dry-run` then `--apply` — **NEW today.** Kam's panel
rulings do NOT write themselves into `decisions.json`; this bridges them. **Dry-run is the default
and --apply is required.** It only touches OPEN cards, takes the key only from his own words, refuses
a key not among that card's options, and will NOT rule a card he only left a NOTE on (the `hpsm-*`
card is open for exactly that reason — do not close it).
**Then `kam_rulings_today.sh` and settle its stale warning by pulling.**

## 🔴 CLAIMS — read the other seat's file BEFORE starting anything
`0_Brain/fleet/claims/` — one file PER SEAT (Kam 2026-09-08 10:17+10:19). Write only your own.
**Update `claims_studio.md` as you take and finish work.** It is eventually-consistent, not a lock.

**Run `2_Project_Files/tools/kam_rulings_today.sh` first — and SETTLE its stale warning by pulling
and re-running before concluding he is quiet.** Mail UTC ≈ AEST−10. **ROTATION BAND 80–90%.**

## ✅ KAM'S DESK IS CLEAR — he ruled both cards at 09:57, both Wednesday's recommendations
- **`secuura-793-security-expiry-two-triages-disagree` → `earlier`**: take the EARLIER expiry
  (2026-09-10) for the three, plus develop's corrected `q8mj` row and #793's 4 new advisories.
  **Relayed with the exact file contents specified and a parse-based verification (35 keys, the 4
  named, and a CONTROL that another advisory still reads 09-24 — proving three rows moved, not the
  field globally). If the count is not 35 the seat stops.**
- **`secuura-ks968-my-decision-table-was-void` → `hashcmp`**: ONE read-only comparison of the stored
  `email_lookup_hash` against `lookupHash('issuer@secuura.com')` under the CURRENT key.
  **THE LIMIT IS PART OF THE RESULT: match → decisive for BENIGN; mismatch → CLOSES NOTHING and must
  NOT be reported as evidence of an incident.** Values never printed. No third query either way.
**Both rulings were written into `decisions.json` BY HAND — the panel still does not do it (w=93).**

## STATE
    origin/develop   512480ef1   #892 MERGED (round 5 closed it, 4 negative controls at zero)
    demo VM          400517aaf   LIVE — deployed 2026-09-08 21:43→22:07Z, verified at the destination
                                 The develop→demo delta is FORMATTING-ONLY: nothing to redeploy for.
                                 It rides with the next real deploy. Stated, not left as drift.
    #892             MERGED at 512480ef1 — five rounds, two NO GOs, closed 2026-09-08 09:34
    #902             e04814afe   tsconfig for systemTest/fixtures, 0 errors, MERGE AUTHORISED, unmerged
    #720/#721        clean, pushed, unmerged
    #793             7e8721107   DIRTY, UNTOUCHED, frozen on Kam's card. Do NOT let a later task
                                 quietly resolve it. Wednesday declined even the mechanical half:
                                 the file is written ONCE or nobody will trust it.
    #891             KAM'S OWN CLICK — https://github.com/Secuura/Distributed_Secuura/pull/891
    rollback         632f16dfe   (not free: 3-image rebuild; does NOT undo a DB change)

## 🔴 KS-968 IS UNMEASURED — do NOT let it be filed as benign
The one statement Kam authorised RAN (`is_superuser=on | hash_null=f | addr_unchanged=f`).
**Wednesday's decision table called that reading BENIGN and the table was WRONG:**
`addr_unchanged` compared a plaintext literal to an **AES-GCM ciphertext column** — it returns false
either way, so the benign row was selectable by a check that cannot fail. **World (c) is excluded;
the INCIDENT world (a) and the benign world (b) remain UNSEPARATED.**
**Card `secuura-ks968-my-decision-table-was-void` is on Kam's desk**, recommending ONE read-only
hash comparison and **stating its limit: one-directional — a match is decisive for benign, a
mismatch closes nothing.** Default HOLD.
**PROJECT TRAP, third occurrence across two seats (s145 filed and retracted the same):
ANY probe of `users.email` by literal comparison is VOID BY CONSTRUCTION.**

## 🔴 s149 ON PANE `%170` — queue DRY, holding
**Round 5 BUILT and PUSHED (`d2aa11fd1`), both fixes red-proofed, now AT A TIER-2 GATE** launched
09:1x via `2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_892_round5.sh` (seven guards,
each exercised to its own rc). **KS-968 run and reported. The queue is dry and the seat is holding.**
Brief: `2_Project_Files/fleet/briefs_staged/2026-09-08_secuura-peter-queue.md` (+ the s149 brief
beside it). **It has corrected Wednesday THREE times today and been right every time** — treat its
pushbacks as measurements, not friction.

## PETER'S 14 — CLOSED OUT except the card and three unapprovables
DONE: #750 closed · #758 closed carrying its three-tree measurement · #720 rebased clean
(`fcc611d29`, preflight passed 50 legs, no `--no-verify`) · #721 done (`62108c579`) · #895's two
findings on KS-682 · #901 opened AND MERGED (the live trunk red) · KS-987/988/989/990/991 filed.
**#793** — Kam's card. **PS #783** — a Platform S PR, NOT in this repo; **still needs routing.**
🔴 **#896 / #899 / #900 REMAIN UNAPPROVED and that is deliberate.** ~18,600 lines of harness code.
The seat refused to approve what it had not reviewed to approval depth and **Wednesday upheld it**.
**Do not let a later seat quietly stamp them.** They carry factual verification records saying
explicitly that they are not approvals. **#900's base is #899's branch, not develop** — merging it
as-is reports success while moving nothing on the trunk; that warning is on the PR.

## WHAT WEDNESDAY GOT WRONG TODAY — all caught by measurement, none reached a cost
1. **"NOTHING has been deployed at all"** — false; s146 shipped on 09-07 and it is in the project's
   own history. Job was 8x smaller than briefed. **An absence claim needs a positive control.** w=92.
2. **"Refresh #758's evidence block, ~10 min"** — the refreshed block could not be made true; the PR
   turns neither gate green and its own fix does not survive its merge.
3. **"`audit-baseline.json` is GENERATED, regenerate it"** — there is no writer. Hand-maintained.
   **Wednesday instructed a command that does not exist.**
4. **The queue never recorded Kam's rulings**, so the panel re-served six cards and he answered five
   twice. Fixed by transcription; **nothing bridges chat_log → decisions.json.** w=93.
5. **Nearly rebuilt the doctor ledger trigger** the laptop had already shipped (`8d906698`).
**The pattern: measure your own claim before stating it. Four of the five are that.**

## 🔴 THE SEAT'S QUEUE (pane %170, ~65%) — in this order
1. **#793** per Kam's `earlier` ruling · 2. **KS-968** the one comparison · 3. **KS-991** (raised to
P2: THREE instances in one session, every gap opened by a merge this seat itself performed — a
defect whose trigger is "you did the right thing") · 4. **KS-992**.
**KS-994 filed (P2)** — `withGeneratedActors()` has NEVER overlaid the generated actors: it iterates
the wrapper, so the k6 harness silently runs on `secrets.yml` credentials while reporting success.
**KS-969's own class, in a file #892 touched.** Fix-shape on the ticket, NOT applied — it is a
behaviour change and needs its own gated round. **Do not let it be fixed under a gate-green ticket.**
**KS-990 re-scoped** and must not be closed by making the error go away. **KS-993 done** — but #902
makes the directory CHECKABLE, not CHECKED: nothing runs the tsconfig yet.

## WED ITEMS STILL OWED
- **Chat panel option to separate/merge Datasec and Secuura views** (Kam's 07:09 note). Not started.
- **Route PS #783** to Platform S.
- **The vault reconciliation is the LAPTOP'S card** — do not both write the shared vault.
- `board_count.sh` excludes ARCHIVED by default; "24" was the visible part of a 29-row state.
