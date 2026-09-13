# Kam's typed line wins: stored per-client outputs = lane H (Q5 a, Q6 a, Q7 a, Q8 name + engagement). SUPERSEDES Q1 (a)

**BLUF.** **For session 41 (seat hpsm-982d).** Kam's line is his own channel. Tuesday verified it at source: a queued command at S40's prompt, 2026-09-13T01:08:16Z, not an accepted suggestion. Verbatim: *"Add an export button to the output so it can generate a PDF.  Also, different reports will need to be generated (and stored) for different clients.  The output will need the client details for which client it was generated and by whom"*.

**This SUPERSEDES Q1 (a) of Tuesday's 01:01:43Z ANSWER ("render on request, no persistence yet").** Kam typed "stored".

## Rulings
- **Q5: (a) YES, persistence now, as lane H, exactly as you designed it:**
  - migration 0014 adds `generated_by`, `generated_at` and the generation snapshot to `release_artifact`, tenant-scoped and append-only, with 0012's rules kept;
  - a generate-and-store action writes to the object store under a tenant-prefixed key and is audited;
  - `listOutputs` lists stored artefacts per client, with short-lived audited links;
  - every output carries the generation block OUTSIDE the manifest hash, with the DRAFT and SYNTHETIC marks kept;
  - Export PDF on S10;
  - the determinism proof becomes "same inputs, including the generation block, give the same bytes".
- **Q6: (a).** The generating user's display name and role are printed; the user id stays in the database and the audit record; **no email on the document.** This is Tuesday's reading of "by whom", told to Kam on his panel. If he wants the email, you get a SUPERSEDES mail.
- **Q7: (a)** S41 builds it as lane H, after lane E phase 2, G and F, then S40's demo branch. No second seat enters renderers, API, web or db.
- **Q8:** the client (tenant) name plus the engagement name, as stored. No support contact and no industry unless Kam asks.

## Unchanged
- **The demo content switch stays OFF on every stack** until Kam taps the card or types it.
- **No push.** A combined tier-1 gate on `1a6b68d` through the lane-H head is due before any push; Tuesday's fresh seat commissions it.
- Tests RED-first with fix-removal mutants. Tenant isolation: another client's artefact is a 404. No real client data.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-13 11:16

Tuesday
