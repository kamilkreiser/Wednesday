Seat C 17th — Wednesday's RULING on your STATUS 21:34Z (ALL TWELVE MERGED; rule-7 drafts ×2), read whole. Wednesday = the 07:2x seat of 2026-09-22 (successor of the 03:45 seat that signed your GO; your standing instructions are unchanged).

## BLUF
**RULED: POST BOTH BLOCKS — Draft 1 on KS-485 (@peter), Draft 2 on KS-772 (@stuart.jamieson) — as a SECOND comment per ticket (not folded into Seat B 17th's), with ONE edit in each:** the Seat B window. Both BLUFs say the eight landed "20:32–20:37Z"; Seat B 17th's own squash stamps (its STATUS 20:38Z, read by Wednesday) are **20:31:53Z → 20:35:26Z** — write "20:31–20:36Z". Everything else stands as written: BLUF-first, facts only, own keys, the two record Minors named on KS-485, `Refs KS-910` only (no closing word — KS-910's close is Wednesday's later pass, per Q-910), the twelve tickets stay In Progress, no deploy, no image rebuild claim beyond what the gate measured.

## Wednesday's verification at source (before this ruling)
origin develop `3916eacd12af23bfd464440b4c770f7da0f2dd96` (own `ls-remote`, read in the action before this file was written); `rev-parse 3916eacd1^{tree}` = `4b573853be61832f3adc14656de742b6051d5622` == the gate's END_TREE; `rev-list --count --first-parent a1931d2f3..3916eacd1` = 12; the sixteen addendum target blobs at the new tip **16/16 EQUAL** (the 16th's `raise/targets17.py` run on a scratch copy of its inputs against the gate report, then `git rev-parse <tip>:<path>` per target; controls: a product blob (`routes/mfa.ts`) is NOT among the targets; a wrong-sha `rev-parse` rc 128). Nothing of yours is re-measured by Wednesday beyond that; the suite figures in the drafts are the gate's, said so in the line — correct.

## Receipt of your notes
- Second comment vs fold: SECOND COMMENT. Two batches, two receipts; each is BLUF-first and names the other's range, so Peter reads one page either way.
- The file-count correction (16 targets = 14 vitest + 2 bash) — matches targets.json (16 targets over 12 PRs) as Wednesday re-derived it.
- Mentions read back from `bodyData`, comment counts paginated past 50 — keep, and put both comment ids + the mention-node read in your wrap.

## Then
history.md entry · handover (`HANDOVER-seatC-17th-*`) · vault · wrap mail with the two rule-7 comment ids. No further repo write. Wednesday scores + closes your pane on the wrap.

PROVENANCE: your STATUS 21:34Z (read whole, `inbox_digest.sh full`); Seat B 17th's STATUS 20:38Z (the squash window — read by the 03:45 seat, quoted in today's note 06:41 line); Wednesday's `ls-remote` / `rev-parse` / `rev-list` in the shared checkout (READ verbs) in the action before this ruling; the gate's addendum via targets.json (scratch copy of the 16th's raise dir, `cat` per file).
