# Deploy blockers — conditions Kam set that must be met BEFORE a named deployment

**Why this file exists:** a note on a ruled card ("keep a note that this needs to change before deployment") reaches the next deploy seat only if something carries it. A card's text is read once; a deploy brief is written fresh each time. Every deploy brief (kintsugi or demo) Wednesday writes MUST read this file and carry each open row for the deployment it names. A row is closed only by Kam's word or by the artefact he named; never by inference.

| id | blocks | condition (Kam's words, verbatim) | source | scope reading (Wednesday's, correctable) | status |
|---|---|---|---|---|---|
| ks1533-admin-bounded | the KS-695 part (ii) ERASURE deployment (PR 1497 and its successors) to kintsugi and demo | *"Decision secuura-ks1533-admin-role-unbounded-by-org-arm-1013: a — Leave ADMIN unbounded for now \| note: keep a note that this needs to be changed before deployment"* | live board, 2026-10-13 09:53:40 view=wednesday; card ruled `a` | Narrowest reading that fits the card text: the tenant-level ADMIN role can still mint keys for any organisation in its tenant; with live erasure that is the cross-organisation hazard the round-4/5 gates found; so the ERASURE deploy waits until ADMIN is organisation-bounded (or Kam rules otherwise). Other deploys are NOT blocked by this row because the unbounded ADMIN is already on kintsugi today. Wednesday asked Kam on the panel (09:5x) to say if he meant every deploy. | OPEN. Ticket for the change: filed by V 6th (mail sent); id to be recorded here. |

## When a row closes
1. Kam's word or the named artefact (the ticket Done and deployed and live-checked).
2. Move the row below a `## Closed` heading with the date and the evidence; never delete.
