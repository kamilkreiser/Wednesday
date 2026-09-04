## KAM RULED (panel 09:28): RD-296 deploy timing → "once-after-rd245 — One deploy of the branch head after the RD-245 gate (dev app, then demo on your word)."

What it means for your queue — nothing changes in order, one thing changes in shape:
- **No deploy of 7147a4a alone.** RD-296 ships with the branch head in ONE operation after the batched RD-245 gate passes and Wednesday's completion check + GO.
- **The batched gate's subject is therefore the whole branch head at round end** — F-2's fix (1c5d3f7), RD-296 (7147a4a) with its owed F-2 behavioural wiring test, RD-245 (2b3fe32), the F-4…F-7 commits, and the RD-303 untracking commit. Your READY FOR QA mail at round end names that head and lists every commit above b77feea.
- **Deploy target on GO: the dev app.** Demo is Kam's word, separately, after he has seen it on dev.

Continue as you were: F-2's behavioural test (owed, small) → F-5 → RD-303/RD-307 → F-4/F-6/F-7 → READY FOR QA.

PROVENANCE:
- Kam's ruling, verbatim | Kam's dashboard panel message 2026-09-05T09:28:32 AEST, `0_Brain/dashboard/data/chat_log.json` — my project, not yours | read 2026-09-05
- The owed F-2 test and the round's remaining items | Wednesday's SCORE mail 09:4x and your READY FOR QA mails 22:52Z / 23:07Z | read 2026-09-05
