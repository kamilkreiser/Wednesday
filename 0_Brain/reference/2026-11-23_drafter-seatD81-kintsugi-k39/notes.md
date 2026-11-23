# Drafter notes: Seat D 81st, Kintsugi k39 (written 2026-11-23 15:05 AEDT)

Output: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-23_seatD81_kintsugi_k39.md (44,927 bytes). Scratch: `_work/` here (own clone, reach_d81.py, fixstr_d81.py and outputs, compose_pin.yml).

## STOP-class finding (top of the reply)
"Card 1006" is not a card id (`decision_queue.sh show 1006` = no such id). It is `secuura-kintsugi-build-cache-prune-if-disk-guard-1006` (ruled a, 2026-10-06 23:06, one-off for Seat D 12th, delivered 10-07). Kam's standing-rule card `secuura-standing-build-cache-prune-1007` says it was a one-off and was ruled **b = "prune once now only, later rounds ask again"**. Each later Kintsugi prune had its own once-only card. D 65th (11-15) logged a prune as "card 1006 = a": drift. **No ruling authorises a cache clear for k39.** Needs a new Kam card, raised by Wednesday.
Measured arithmetic: free 66,559 MB (carried) vs gate 60,000: the build passes WITHOUT a clear (margin 6,559); estimate 3 to 8 GB, ends 58,500-63,500; the clear matters for k40, not k39. The brief makes the GO carry Wednesday's disk line (W1) and forbids any prune under "card 1006".

## Draft card (for Wednesday to raise; the drafter wrote to no queue)
id suggestion: secuura-kintsugi-build-cache-prune-k40-1123
Title: Kintsugi will drop under its 60,000 MB build gate after this round: may the deploy seat clear the Docker build cache once before the next round?
BLUF: Kintsugi has 66,559 MB free after the last deploy; the next two deploys cost 3 to 10 GB each, so the build gate (60,000 MB) will block the round after this one. Build cache is regenerable (about 88 GB held, about 43 GB reclaimable); clearing it deletes no image, rollback tag or volume. Your 2026-10-08 ruling on the standing rule was "once now only, later rounds ask again", so this is a new ask.
Options: [a] one `docker builder prune` (cache only; no image, tag or volume; before/after figures reported; no --all) by the deploy seat of that round; [b] hold: the round stops at the gate and Wednesday re-plans; [c] standing rule for every round (Kam's 10-08 answer was b to this; re-asking is his call).
Default: nothing pruned.

## Other findings for Wednesday
- **Auth hold:** page part discharged (issuer serves the three pages: 7 files, was 0). Second part of gate 389 (mail delivery) is UNMEASURED: the brief makes `mail_transport_configured` an ITEM 0 boolean and a STOP (R3) for the originate and auth swaps if false. KS-2275 with no mail transport locks unverified recipients out with no way back.
- **NEW trap found in code:** auth at NODE_ENV=development with no mail transport logs the full verify/reset/claim URL (with token) at INFO (auth.ts 205, 352, 911). The brief tells the seat to count, never print, those lines.
- **PR 2285 fix round:** gated head 7c5b2f7d184d, merged head f99294c7629a; delta measured by the drafter (4 files, +119 -7; every non-test line a comment). Pin rule satisfied by content, with a re-run filter in the brief.
- **Gateway:** real code this round (PR 2276); served yaml unchanged (78e3783c2bb6105d), so binds all SAME (k38 had one DIFFERENT); D80-W2 is moot.
- **Deploy-reserving cards:** KS-2272 and KS-2275 cards both say "deploy stays yours". The brief asks Wednesday (W2, W4) to state her reading of Kam's 10:14 word for them (D 80th's brief carried the same reading).
- Carried, not measured: everything on the box (free disk, REVISION, ids). The drafter ran no test suite; packages/shared is byte-equal (0 changed paths) to the tree D 80th and gate 409 ran (1743 / 1742 / 1 failed KS-278, Node 26.8.1).
- develop unmoved at 15:05 (`git ls-remote` in the drafter's clone: b8470f5fd331...).
- Hook noise: one recursive grep refused at first (scope hook), one hung `ls-remote` in the shared checkout (stopped by task id); neither wrote anything.

## Faults declared
- First clone attempt used a variable path for a write verb; the hook refused it, nothing ran; re-issued with a literal path.
- One call piped grep into `cut -c` (advisory fired); no absence was claimed from it.
- A `git -C 2_Project_Files ls-remote` against the shared checkout hung 120 s; stopped by task id. No ref written.
