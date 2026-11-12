# B1542 ANSWER-1 (Tuesday s273, 2026-11-12, to SEAT-D62): the 31 staff-only words are RULED; resume at Step 0C/target asserts and carry on to the deploy

**Your question (STATUS last line, 17:13):** may the 31 staff-only strings ship as written, or go to the product owner as one card?

**Answer: they went to him as one card and he approved them as written.** Card `mpscalc-staff-words-31-deploy-1112` (the full verbatim table of your `## Words pack for the product owner` attached in his file drawer), read by Tuesday with `decision_queue.sh show` at 18:20:36: `status: ruled`, `choice='a'`, `ruled_ts=2026-11-12T18:20:36.133272+11:00`. His tap on the live board, 18:20:03, verbatim: *"Decision mpscalc-staff-words-31-deploy-1112: a — Approve all 31 as written; deploy now (recommended)"*. (Cite it in STATUS as "the product owner's 18:20 ruling on the 31 staff-only strings"; do not copy the card id into anything but STATUS.)

**So:**
1. Step 0W is CLEARED: mark the 31 rows `ruled` with that citation; customer-visible unruled 0 (your census). Any string you find that is NOT one of those 31 and not ruled still STOPS (strict, as stamped).
2. Re-run Step 0 items 3 (the first card, still `ruled a`) and 4, then continue in order: Step 0C, target asserts (your first `fetch` attempt read rc 128: read why before re-trying; the kit allows ONE fetch: if that one was spent with nothing fetched, a second attempt is allowed once, recorded), step 0 C-2, 1 (pre-read), 2 (backup), 3 (3a-3f), 4 (package), 5 (swap), 6, 7. Everything else in the kit is unchanged.
3. **S9 is REPLACED (this answer supersedes the stamp's S9):** latest swap START **19:45 AEDT**; absolute hard stop **20:45 AEDT** 2026-11-12. Swap not started at 19:45: `STOPPED: hard stop; NEEDS TUESDAY: relaunch`. Swap under way: finish `check` and the rollback decision, then report. Reason: the ruling arrived at 18:20, after your stop; the stamp's 18:45 would not fit the backup and 3f counts.
4. Load: another deploy seat (`Datasec/HPSM-POC-D61`) is running on a DIFFERENT resource group (`hpsm-poc-uat-rg`); no path or resource of yours; do not touch it.
