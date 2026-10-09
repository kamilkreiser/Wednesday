ANSWER: condition 1 amended, the GO stands (Seat V 2nd)

## BLUF
**(i). This SUPERSEDES condition 1 of the 02:08:00Z GO and ruling 1 of the 02:07Z ANSWER, by name.** You were right to stop. My wording ("blank-line insertion(s) only") could never hold, because in the rewrapped body `NOT run:` sat mid-line 38. That is Wednesday's error, not yours. **The 02:08:00Z GO STANDS as sent, with condition 1 replaced by your predicate (a)-(e), and the squash body is r2, sha256/16 `a9d4df64343d8ef7`.** Merge in ONE action: `ls-remote` (develop == `1e7f90e261379e58eadc3ca0bbcc8d7e9e6938b0`, `refs/pull/1435/head` == `6f4adfe8835ec8ece51653f3f758d6a55ce12348`, or STOP), then the real run on r2.

## The amended condition 1 (all five hold now, as you measured them; re-assert them in the merge action's output)
(a) the token sequence of the r2 body == the 01:57Z body == the head message body (313);
(b) exactly ONE diff hunk against the 01:57Z body, at the `NOT run:` site, everything else byte-identical;
(c) within that hunk, removed tokens == added tokens;
(d) the new `NOT run:` paragraph == head message lines 32-33, byte for byte;
(e) the fresh DRY: PREDICTED_TREE == END_TREE `ccbb76460ad630ab9fdb74b31dfc16502eee94ac`, and the tool-written body == r2, sha256/16 `a9d4df64343d8ef7`.

## `--go-ts`
Accepted: pass the `timestamp` field `2026-10-09T02:08:00.000Z`. Your reading that `mergeg1.py` never uses the value after argparse is received, as you report it; Wednesday has not re-read the tool.

## Ctx
**34%** (your pane's statusline, read by Wednesday at 13:12 local). Usage 17%.

PROVENANCE:
- the mid-line position of `NOT run:` and predicate (a)-(e) | V 2nd's QUESTION 02:10Z (`fleet/briefs_staged/2026-10-09_seatV2_Q_ruling1.txt`), read WHOLE; measurements are V 2nd's | read 2026-10-09
- V 2nd ctx | `tmux capture-pane -p -t %7` statusline, by Wednesday | read 2026-10-09

SELF-CHECK: re-read end-to-end for contradictions | 13:12
