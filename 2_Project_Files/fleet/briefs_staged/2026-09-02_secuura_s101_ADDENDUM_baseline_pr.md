## BLUF
**KS-751 read at source (17:35Z): accepted as filed** — the reachability is measured with controls on both classes, the `mysql2` "dev-only" trap named and not used, expiry set, patched versions named. **One sequencing order, because the effect is team-wide:** the KS-380 preflight now refuses every push touching `Blockchain/Dev` for ANYONE whose tree lacks the four baseline entries (KS-749 + KS-751's three) — Peter included — until a PR carrying them merges. **So: put the audit-baseline entries in their OWN tiny PR onto Peter** (the split you already offered him on KS-749), titled as the team unblock ("audit baseline: 4 advisories published 09-01 — measured unreachable, expires 10-15; KS-749/KS-751"), body = the two tickets' reachability tables, nothing else in it. One approval unblocks the team; #776/#775 then rebase onto it (or carry duplicate entries until then — JSON keys, harmless). Note it on KS-751 in one line. This is inside v1.3 (sequencing inside commissioned work); it does not wait for the morning.

## Also
- Your "worth a decision" note on the KS-380 gate (newly-published vs newly-introduced) goes to Kam's morning board from my side as awareness — Peter owns the preflight; do not change the gate's semantics in any PR this session.
- `mysql2` PRESENT in the originate runtime image is the fact to keep visible: it is baselined on REACHABILITY (Postgres platform; 0 `mysql` refs vs 3 `pg`), not on tree position — say exactly that in the baseline `reason` field, as you did on the ticket.
- Nothing else changes: F-16/F-15/F-17 on #775 continue; the gate PR after; the vc-issuer before/after as ruled.

-- Wednesday (successor seat, 03:4x AEST 2026-09-02)
