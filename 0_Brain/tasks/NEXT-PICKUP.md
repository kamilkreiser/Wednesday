---
date: 2026-09-08
type: pickup
scope: SECUURA ONLY on this machine — Kam, panel 07:08:23: "only secuura projects on this machine until further notice". Datasec is the LAPTOP's; read its mail by SUBJECT only.
source: replaced WHOLESALE at 10:5x by the s151 seat
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — 10:5x Tuesday. ONE card on Kam's desk. s149 live on %170 and working.

## 🔴 FIRST, IN THIS ORDER
1. `2_Project_Files/tools/kam_rulings_today.sh` — **and settle its stale warning by PULLING and re-running.**
   "He said nothing" and "this copy has not caught up" are different facts.
2. `2_Project_Files/tools/sync_kam_rulings.sh --dry-run` then `--apply`. **His panel rulings still do not
   write themselves into `decisions.json`** (w=93). The tool bridges it; dry-run is the default. It refuses
   a key not among that card's options and will NOT rule a card he only left a NOTE on.
3. `0_Brain/fleet/claims/` — read the OTHER seat's file before starting anything; write only `claims_studio.md`.
4. `2_Project_Files/tools/fleet_ack.sh list` — **NEW today.** Fleet activity items now clear once answered;
   ack a mail only after its ANSWER is verified at the destination.

## THE ONE CARD ON KAM'S DESK
- **`secuura-platform-s-count-was-wrong-when-you-ruled`** — he ruled `archive` on "fifteen" Platform S
  tickets; the board says **18 in Done, 11 in the 770-784 range**, and the wrong figure was Wednesday's,
  in the card's TITLE. Options: all18 (rec) · range11 · none. **Default HOLD — nothing on Stuart's board
  moves on silence.** Nothing there has been touched.

## RULINGS OF KAM'S THAT ARE LIVE AND NOT IN ANY ARTEFACT AN AGENT LANDS ON
- `secuura-archive-fifteen-platform-s-tickets` → **`archive`** (10:35:09) — superseded in its NUMBER by the
  card above, not in its direction.
- `secuura-793-…-already-expired` → **`add-dead`** (10:35:15) — the four expired advisories as-is, plus the
  three expiry corrections and develop's corrected `q8mj`, in **ONE write** of the preserved built file, plus
  **ONE** re-triage ticket. **Not yet executed.**
- `secuura-archive-tested-not-deployed` → **`hold`** — TND stays visible until deployed. **Not superseded by
  his 10:14 archive word:** a TND ticket is neither closed nor deployed. s149 has confirmed TND ∩ Done = ∅.
- `secuura-archive-uat-tickets-vs-peters-test-list` → **`archive-all-33`** — Deployed-to-UAT is archivable.

## 🔴 THE FINDING OF THE MORNING — `issueArchive` CASCADES TO SUB-ISSUES
Archiving 23 UAT tickets silently archived **KS-918 (Backlog) and KS-920 (In Progress)** — live work, never
targeted. **Caught ONLY by the full census delta (−25 against an expected −23).** Stopped, both restored,
accounting reconciles at 35 (33 intended + 2 collateral).
- **The parent side of the query is BLIND:** once children are archived, `parent.children` returns 0. The
  only detectors are (a) a full census delta and (b) a child→parent lookup after the fact.
- **MANDATORY on every remaining archive:** child→parent children count BEFORE, full paged census AFTER,
  and `expected delta = |targets| + |children found|`. Stop the class on any mismatch.
- **97 archived tickets board-wide sit in NON-TERMINAL states; 95 predate today.** Ticket + measurement owed
  (does each one's parent carry a millisecond-identical `archivedAt`?). **Do not unarchive anything** — a
  restoration is as much a board change as an archive, and 83 tickets reappearing in Backlog is Kam's call.

## STATE
    origin/develop   986c592d5      demo VM   400517aaf      unarchived issues  370
    #903 (KS-991) · #904 (KS-992) · #905 (the schema trap)   open, unmerged
    #793             built file PRESERVED, UNWRITTEN — Kam ruled add-dead; write it ONCE
    #896 / #899 / #900   UNAPPROVED, deliberately. ~18,600 lines of harness code the seat
                         refused to approve unreviewed and Wednesday upheld. Do not let a later
                         seat stamp them. #900's base is #899's branch, not develop.
    KS-968           moved Done -> In Progress at 00:28:26Z by another hand — out of archive
                     scope by its own state. The ciphertext trap is committed at c38040bd1 on
                     `kamilkreiser/ks-968-schema-trap-literal-comparison`, NOT yet on develop.
    archived today   33 (reversal list is in s149's 00:44Z mail, one place)

## 🔴 PROJECT TRAP — third occurrence across two seats
**ANY probe of `users.email` by literal comparison is VOID BY CONSTRUCTION** — it is AES-GCM ciphertext, so
`WHERE email = '…'` returns no rows regardless of the address. It does not error; it answers a different
question and looks like evidence. Resolve via `email_lookup_hash`. **A hash comparison is decisive on a
MATCH only.** The warning now lives in the schema file itself — but on a branch, not on develop.

## WED ITEMS STILL OWED
- **Chat panel option to separate/merge Datasec and Secuura views** (Kam's 07:09 note). **Not started.**
- **Route PS #783** to Platform S. Not started.
- The ticket for the 95 pre-existing non-terminal archived tickets.
- The vault reconciliation is the **LAPTOP'S** card — do not both write the shared vault.

## WHAT s151 GOT WRONG — all filed, none reached a cost
1. **Red-proofed an anti-junk-tap guard by sending junk taps to the LIVE agent**, costing s149 a turn.
   *On a side-effecting system a positive control IS an action; in a guard's red-proof the dangerous half
   is the branch that is supposed to PASS.*
2. **A count entered a card's TITLE with no provenance clause and Kam ruled on it.** The classification was
   labelled "unverified"; the number was not.
3. **Two false absences from Wednesday's own harnesses in ten minutes** — an `awk` range, and measuring
   `generate.py`'s stdout instead of the file it writes. Both self-caught by a control.

## THE BOOT NUMBER, CORRECTED — the predecessor's premise was wrong
The 05:35 handover said the two mandatory reads are "~158 K tokens against a **200 K** window" and
recommended changing Kam's ledger cadence on that basis. **Measured at this seat across a ~100 K-token
delta: 1% of the statusline ≈ 7 K tokens, so the window is ~700 K.** The full brain load (digest whole +
this seat's ledger whole) took the statusline from 7% to **21%**. **No cadence change is needed; rule 3c
stands as Kam ruled it at 07:07 ("leave your cadence alone").** Do not re-raise it.
