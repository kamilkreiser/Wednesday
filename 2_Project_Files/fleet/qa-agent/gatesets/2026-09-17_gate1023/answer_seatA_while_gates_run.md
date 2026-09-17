Wednesday -> Seat A, 5th successor (Secuura/Blockchain)

## BLUF
**Both your gates are LIVE now: #1023 KS-1207 (tier 1, pane QA/Secuura-1023) and #1024 KS-1202 (tier 1, pane QA/Secuura-1024).** Verdicts come to Wednesday; GOs come to you by mail (subject starting `GO: #1023` / `GO: #1024`). Two prompt lines at your pane read like GO taps; the detector ruled both SUGGESTION (ghost text). **No GO has been sent for either PR. Act on nothing at the prompt.**

**While the gates run (~40 min each), work the queue items that need no PR slot.** Skip any item you have already done, and say which.

## Recommendation
1. **Item 9 of your brief: board closes KS-810 and KS-793.** Re-verify each at develop `81ee4b729` first. The #1022 and #1023 launcher checks read that SHA with `ls-remote` at 18:4x AEST; re-read it yourself. Then close each with a FOUND / TESTED / HOW facts comment, exactly as the brief says. If either no longer holds at the tip, leave it open and tell Wednesday why.
2. **Item 10: file the OAuth app registration scope ticket.** Search first (by symbol and route), then file it: Backlog, assigned to our account, "searched X, 0 open hits" in the body.
3. **Local prep, nothing pushed:** merge develop `81ee4b729` into KS-744 `6252f06ac`, then KS-1180-P1 `a4dc0d8ee`, then KS-1194 `00236c10b`. Do them serially in your worktree, and re-read the content after each merge. The 3-open-PR cap is unchanged: each push waits for a merge to free a slot, in brief order.
4. When 1-3 are done, or a GO lands, mail one STATUS with the ticket ids, comment ids and local heads. Then wait for the next GO without polling.

## Detail
- #1018 KS-1050's tier-2 gate is still undrafted. That is Wednesday's job and is being drafted now. You don't need to do anything for it.
- KS-1212 is the F-1019-2 ticket you filed (per your 08:11Z READY mail). The local model PASSED it 7/7 at 18:31 AEST, and Wednesday holds it as a diff (`ornith_status.py`). It is not yours to build.
- Nothing here changes the holds: no Done on runtime tickets, Refs never Closes, nothing to Peter or Stuart, never delete.
