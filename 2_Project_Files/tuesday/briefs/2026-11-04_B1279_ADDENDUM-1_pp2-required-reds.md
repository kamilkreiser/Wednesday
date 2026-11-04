# B1279 ADDENDUM-1 | SEAT-G339 | Step 2(d): the required reds of plant PP2 (a correction to the kit)

From Tuesday (Datasec coordinator seat), Datasec / HPSM-POC. Read whole at your next safe boundary. It corrects ONE sentence of your kit, Step 2(d). Nothing else changes.

**The kit said:** PP2 (`print:min-h-0` put back, anchor exactly 1) turns "the unit pin, the new floor row (`:504`) and the print spec ALL red".

**Corrected:** the plant's SHAPE decides which rows it can reach, so judge each shape by its own required reds.
- **PP2 = the `print:min-h-0` token ADDED to the current row class at `AppShell.tsx:166`, with `min-h-0` kept:** required red = the unit class pin and `playbook-print.spec.ts:122` (0 of 6), with the `@media print` block count above main's. **The floor row (`:504`) staying GREEN is correct here and is NOT a survivor.** With `min-h-0` present, the computed `min-height` is still `0px` below 1024 px and in print, so the floor row has nothing to see.
- **PP2-old = the WHOLE round-1 class put back** (`lg:min-h-[calc(100dvh-48px)] print:min-h-0`, no base `min-h-0`): required red = the unit pin, the print spec AND the floor row (at 1023 px it reads `auto`, not `0px`). This is the shape the fix round ran (`Briefs/2026-11-04_B1275_STATUS.md:63` and `:101`, a CLAIM).
- Run both shapes, inside your plant cap (they count as two). A required red that stays green IS a Major, per its own shape above.

**Why:** the kit copied the fix round's PP2 result without its plant shape. That was Tuesday's error. A live seat (H117) hit the same mismatch on the token-only shape at 16:30 today.
