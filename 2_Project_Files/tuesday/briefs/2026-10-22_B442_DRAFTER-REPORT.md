# B442 drafter report (Sonnet brief-drafter, row C8), 2026-10-22 about 10:20 AEDT

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B442_SEAT-U2_hpsmpoc-user-guide-refresh-v02.md`. Pane `Datasec/HPSM-POC-U2`. Unstamped: the `## Stamp` section holds 3 slot lines plus the last line (`sed -n '/^## Stamp/,$p' | grep -c '_''___'` printed 4; the control is the same command on the unstamped file, which fires). Last line `READ-WHOLE-BY-TUESDAY: ____`. No `.pre-stamp` copy was made (the write fence allowed two files only); the brief's REFUSE control falls back to a scratch file.

## What I read (whole)
B427 SEAT-U1 brief, ADDENDUM-1, DRAFTER-REPORT, B427 STATUS, the guide's SOURCES.md and STYLE.md, B437 STATUS, B437 brief (shape and stamp lines), model-routing.md rows P1-P4, C2, C8, models_latest.json (sonnet = claude-sonnet-5-5, checked 09:21 +1100). Also read (read-only) `.tools/b427/content427.py`, `build427.py`, `run_build427.sh`, `email_pdf427.py`, `toc.json`, and grepped the other B427 scripts for hardcoded paths. No HTTP, no other fence touched.

## Measured facts the brief rests on
- The badge sentence is `content427.py:158`, in the `GOOD([...])` list of "Getting started"; step 5 is `:148`; Figure 2.2 caption `:153`. Steps 5 and the caption stay true as they stand (they say "a badge naming your level" / "the level badge").
- Section 5.5 = `Step 4: HP/HPSM recommendation` (`toc.json`: "5.5 Step 4: HP/HPSM recommendation"); Figure 5.7; `content427.py:283-291`.
- The build kit exists ONLY in `.tools/b427/` (not in Deliverables). The brief makes the seat copy with `cmp` into `.tools/b442/` and run only the copies.

## Decisions in the brief that need your eye (each is my default; change at stamp)
1. **HARD TRAP found and written in.** The B427 scripts hardcode `.tools/b427/...` and the v0.1 `screens/` and `screens/raw/` folders (`lib427.cjs:13`, `shots427.cjs:4`, `process427.py:6-7`, `build427.py:6,19`, and others). Run unchanged they would overwrite the v0.1 screenshots. The brief puts the v0.2 captures in a new `screens_v0.2/` and demands a repoint-and-grep plus a before/after sha256 of every v0.1 file. "Same file names" is therefore met inside `screens_v0.2/`.
2. **Version stamp is an addition beyond A and B.** Your item 4 says no other wording change, yet the files are named v0.2 and the cover and document-control table say 0.1. I added (to be confirmed at stamp): cover `Version 0.2`, and a second document-control row `0.2 | 22 October 2026 | Datasec | Screenshots re-taken from the current review copy. Header badge sentence updated. HP/HPSM recommendation note added. The PDF is produced separately from the DOCX and carries the same text.` Listed in STATUS as new wording. Strike it if you want the text frozen.
3. **Alt text / captions** at `content427.py:153, 569, 570` say "a Partner badge", "a Consultant badge", "a Demo badge". They stay unchanged (item 4); the seat lists them for you. They are alt text only, so they do not print, but they will read slightly off against the new badge.
4. **E-mail PDF cap is 4,100,000 bytes, not B427's 4,300,000.** Your "each mail <= ~5.5 MB" with base64 (x 4/3) means 4.1 MB; 4.3 MB would be 5.73 MB (still under the 6 MB API cap, over your target). The v0.1 e-mail PDF is 4,159,989 bytes (5.55 MB request), so the seat will need slightly stronger compression; readability at Figures 4.2, 5.6, 6.6 is the stop test. The DOCX (3.98 MB, 5.31 MB estimated) goes alone.
5. **Placement of the 5.5 sentence:** the seat proposes; I recommended a plain paragraph as the first line of 5.5 (not a call-out) and ruled that no other word may be added. The sentence is quoted byte-exact from your instruction, with a `cmp` check.
6. **Section 5.5 vs "step 5 of section 2 near line ~121":** your numbers (~133, ~121) are rendered or other line counts; the brief gives the true source lines (158, 148) and says the product owner's "~133" counts rendered lines (my inference, UNMEASURED).
7. **Build fingerprint will differ from v0.1's** (new web build; BUILD_ID `OUbyoA1w1fl85Q910Jq59` per B437). The brief says a difference is expected, equality of start/mid/end is the rule.
8. **Page-text diff against v0.1 walk text** added: any non-badge change on the site is reported; a quote that no longer verifies is a STOP (the seat must not edit a quotation).
9. Two REFUSE checks added beyond B427: the badge must read `Partner (review copy)` on the live site (else UAT was rolled back), and the three v0.1 deliverables must match the hashes in B427 STATUS `:122-123` (only the prefix and suffix of the DOCX and PDF hashes are in that record; the e-mail PDF's full hash is).
10. Model: Sonnet, row C2 (pilot) with C8, B427's precedent; no row fits "documentation refresh" better. P1 no (nothing goes to a human from the seat). Gauge from the stamp.

## Not done by me
No stamp, no launch, no HTTP, no `decision_queue.sh`, no fleet store, no vault, no `.pre-stamp` copy, no Artifact/Docs/mail/chat tool. The only two files I wrote are this report and the brief.

## Open questions for Tuesday
(a) Confirm or strike the version-stamp row (decision 2). (b) Confirm the 4,100,000-byte e-mail cap (decision 4). (c) Alt text: leave (default) or add the three strings to the commission (decision 3).
