# No objection to lane-w-e2e. C12 accepted. Before anything is built for C11, MEASURE release with one synthetic device group, because the live stacks' tenants have one

**BLUF.** **For session 42 (seat hpsm-3e04).**

1. **`s42/lane-w-e2e` (`apps/web/e2e/**` only: the F1 fixture fix and the F7 guard, merged right after lane R): no objection.** Your default applies, and so does the known-RED classification rule until it lands.
2. **Lane R round 1: accepted as reported.**
   - The draft footer *"Unreleased draft. Not generated from an approved policy manifest."* is accepted. No source defines one (A-38 and screens-MEASURED define only the watermark).
   - Also accepted: UTC on Last Modified, "Framework lineage", no header wraps, device group names via the renderer.
   - Round 2 (posture, and item 10's "confirmed as supported on every device group in scope" with zero groups) goes ahead as planned.
3. **Lane C12 FINAL `7e324c5`: accepted as reported.**
   - Release was reached through the product's own workflow on `pc-s42-c12`, with nothing written into content or fixtures.
   - One SYNTHETIC adapter row, `SYNTHETIC-DEMO-1`, citing Kam's ruling and "not HP's HPSM support matrix".
   - `release-draft` is unchanged (`79364073…`); the demo `CONTENT_HASH` is `fd7db6b8…`.
   - Both released PDFs show "SYNTHETIC CONTENT | NOT SIGNED".
4. **NEW: measure the device-group case before any C11 work.**
   - **Why:** S40 seeded both LIVE stacks' synthetic tenants with **one synthetic device group** (its 04:08:07Z report: *"scope E8 2023 ML3 + one synthetic device group"*). Your release proof used **zero** groups. Your note that C11 rows are needed with a group is inferred, not measured. **If it is right, Kam's demo cannot release on the stacks he will open.**
   - **Do:** on `pc-s42-c12`, repeat the product-workflow release with ONE synthetic device group in scope, nothing else changed. Report the exact blockers and exactly which C11 rows (`baseline_values`, `device_capabilities`) they need.
   - **Do NOT build C11 mapping or synthetic capability rows yet.** Extending the synthetic fence to device capabilities is a content decision beyond Kam's `build-c12` wording. **If it blocks, Tuesday puts it to Kam as a card, with the measured row list.**
   - If it does NOT block, say so; nothing further is needed.
5. **Q-merge rollback plan: accepted as written:** (a) the objects pre-step, (b) `redeploy.sh <previous sha>`, (c) the ~10 min check, proven on `pc-s42-merge` with an induced bucket failure.
   - Add to the Azure read-only MinIO check: **if Azure's `latest` MinIO fails the conditional-PUT round trip, S40 rolls back and stops.** Pinning Azure's image is then a separate upgrade step, named in the next message, not improvised.
6. **F3 routing** (`RenderInput.device_group_names`, wired by lane Q from `input_snapshot`, manifest unchanged, no hash impact): accepted.

## Unchanged
- Merge order R → lane-w-e2e → C12 → Q → W. No push. A combined tier-1 gate is due before any push. **Its targets now also include:**
  - the released synthetic PDFs;
  - the device-group release measurement;
  - the Azure MinIO version.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-13 14:38

Tuesday
