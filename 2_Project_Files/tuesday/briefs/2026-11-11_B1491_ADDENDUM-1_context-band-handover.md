# B1491 ADDENDUM-1 (SEAT-U4): a context band and a clean handover, so the guide survives more than one window

From Tuesday, 2026-11-11 11:39 AEDT. Binds you as part of your commission; name it in STATUS.

**Why:** your pane read ctx 51% at 11:38 with the inventory crawl done and capture, inspection, writing, the PDF and VERIFY still ahead. That will not fit one window. Nothing you have done is wrong; this only adds the rule for handing over.

1. **Band.** At about **70%** context, start no new part. At about **75%**, finish the step in hand at a safe boundary (a file fully written, no browser or server running, ports 9530-9539 free, every started process stopped by pid), then write the handover below and end. Never let a part die half-written.
2. **Handover file** `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-11-11_B1491_HANDOVER.md` (append-only if it exists): what is DONE (parts, file paths, counts, hashes of finished outputs), what is IN HAND (exactly where it stopped), what is NEXT (the next part and its first step), the fence totals so far, sign-ins used so far, every process and port you left (expected none), and any decision you made that a successor must keep (figure numbering, section order, naming). The successor reads your STATUS, this file and the kit; write so that is enough.
3. **Last line** of STATUS when you hand over, exactly: `HANDOVER B1491: next <part> <step> | done <parts>` (the watcher fires on it).
4. **Spend context on what only you can do.** Inspect each raw screenshot with the Read tool as the kit requires, but read each image ONCE; keep notes in files, not in your head; do not re-read large files you have already summarised to a file.
5. Nothing else changes: the fence, the holds, PDF-ONLY, the VERIFY section, the HARD STOP.
