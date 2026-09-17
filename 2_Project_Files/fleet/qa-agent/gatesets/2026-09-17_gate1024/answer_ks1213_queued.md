Wednesday -> Seat A, 5th successor (Secuura/Blockchain)

## BLUF
**#1024 MERGED is VERIFIED at source, 13 of 13 checks** (GitHub + Linear read by Wednesday, script `gatesets/2026-09-17_gate1024/merged_verify.py`, control KS-999999): squash 79933c798, one parent 81ee4b729, tree ccd3f2819, two originate files, both blobs, no closing phrase, KS-1202 In Progress, comment be343842, KS-1213 exists, KS-1203 comment 81a9546a. **Develop has since moved ONE commit past your squash: `ee40d3099`, Seat B's #1022 hono merge** (compare API: ahead 1, behind 0). The PRE-STEP of your #1023 GO judges develop by content, so re-read it.
**KS-1213 is QUEUED to you. Build it LOCALLY now, between merges; it needs no PR slot to build.**

## Recommendation
1. **Order is unchanged:** merge #1023 (its GO, with develop re-read) → KS-839 takes the freed slot → then KS-744, KS-1180-P1 and KS-1194 as slots free. KS-1194's merge still waits for Kam's tap and for #1018.
2. **KS-1213 build, local only:**
   - **Shape: WRITE-SIDE REFUSE**, the same rule as KS-1202's create guard. Every derived writer that takes `metadata.documentType` (`/:id/version`, `sign-cert`, `sign-wallet`, `certifications/issue` with `parentDocumentId`) refuses a value that differs from the source document's stored type with 400.
   - **Why this shape (Wednesday's sequencing call):** Kam ruled KS-1202 as "Build it" on the refuse shape, and this carries that ruling to the sibling writers. The read-side alternative changes what already-stored legacy rows serve, and it turns the create cells red. That is a different product decision, not this ticket.
   - **Cells:** measure each of the three read-only writers at runtime before fixing it. If a writer turns out not to relabel, record it and leave it untouched. Add N-B's four regression cells. Red-proof on develop; tampers per writer.
   - **Linking:** `Refs KS-1213`, tier 1. KS-1213 stays In Progress on merge (§5f).
   - **If the shape does not fit a writer** (for example, a legitimate caller relies on changing a type), stop and ask. Do not choose silently.
3. When it is built and red-proofed, mail STATUS with its head. It pushes when a slot frees, in the order above.

## Detail
- The GO for #1023 (09:07:27Z) stands. Nothing in this mail supersedes it.
- Holds unchanged: nothing to Peter or Stuart, no deploy, never Done on a runtime ticket, Refs never Closes, never delete.
