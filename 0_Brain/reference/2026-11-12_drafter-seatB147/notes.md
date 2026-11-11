# Notes: drafter of brief_B147.md (re-commission), 2026-11-12 ~10:0x-10:07 AEDT

## develop readings (git ls-remote, read-only, GIT_OPTIONAL_LOCKS=0, no fetch)
- START 10:03:52 AEDT: develop `d35f75875275158ce3b20b636b4198a4c8834968`, 2,118 lines.
- END 10:06:42 AEDT: identical (develop and every queued, watch-list and 2199 head diffed against the first read: SAME).
- develop did NOT move past d35f75875275. No queue-fact adjustment needed beyond the pin change from the 2186 merge.

## Heads vs gate pins (program: 12-hex of refs/pull/N/head grepped in the gate verdict; planted control 000000000000 read 0)
All 20 queued heads equal their gate pin (hit counts 1 to 5 each): 2189, 2184, 2185, 2187, 2188, 2190, 2192, 2191, 2193, 2194, 2195, 2196, 2197 (2f10c9750a90), 2198 (5064d0e99dd8), 2177, 2176, 2169, 2170, 2123. 2178 has no gate (hygiene). Watch-list 2100 and 2094 unmoved. 2199 reads 4a0a166b95a1 (gate 322 not read; not queued).

## What changed vs B 146th's brief
- 2186 struck (merged, squash d35f7587..., tree 1ffbf153...). 2189 is now row 1.
- 2197 and 2198 (KS-1868, tier 1, gate 321 GWN each) inserted after 2196, GO-name sentences verbatim from the commission; filings G321-2198-1 (Minor) and -3 (Note) added to the S-lane table; G321-PRE-1 stated as filed by S 64th (note: services/auth rc is not a pass signal).
- Fragment-gap ticket trigger now seven rows (2186 already merged).
- Added: DRIVE-DROP DISCIPLINE section, OWED pin-table edit section (from HANDOVER), B 146th's six traps and measured costs (23.5 -> 36.3 -> 50.0 -> 54.9; +13.7 set-up to READY use 12), kit source switched to REC146, ordinal check 2,2,0,1.
- RULED BY KAM section copied verbatim from B 146th's brief. STAMP block left blank.

## Measured at draft time (re-measure by the seat)
- REC146: tools 37, evidence 171 (HANDOVER said 170), drafts 28 (said 26), mail 16 (said 15). Baseline v2 31 lines. No manifest diff or fsck run by me.
- history.md ordinals (^## .*Seat B 14N): 145=2, 146=2, 147=0, 144=1 (B 146th's entry at line 12, completed B 145th record at line 23). Positive controls: counts above zero from the same file.
- B 146th's watcher pid 14528 (watch_current.pid): not running by ps.
- Push lock EXISTS: holder = Seat R 104th pid 64679 (10:01 AEDT), not B's; noted, untouched.
- Shared checkout HEAD 0e6479d7b6c0, 18 status lines. Mini up 2:15, load 6.19; DevMASTER 2,378 GiB free.

## Not done / caveats
- Linear, PR API, live PR bodies, gate 322, merge trees on the new pin: UNREAD.
- KS-2170 provenance cites the commission (no verdict read). KS-1988, KS-2075, KS-2125, KS-2163, KS-1927, KS-2149, KS-907 are carried from B 146th's brief; I cited the gate verdict paths for 1988/2075/2125 (head matched by grep, findings not re-read) and the predecessor brief for the rest.
- Brief names no lesson files. Provenance check: every KS key named has exactly one PROVENANCE line (program).
- Never cd; heredocs not used; writes only in this folder (plus scratchpad lsr1/lsr2 for ls-remote output).

## Output
brief_B147.md: 141 lines, 43,413 bytes (under 55 KB).
