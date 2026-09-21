#!/usr/bin/env python3
"""patch_drafts_seatc_late.py — fold Seat C 16th's READYs 9-13 (#1162 … #1166, read 19:13Z — seatc_late_paths_1.out) into the prompt drafts' Seat C set, so the
gate starts from the twelve Seat C PRs the drafter saw rather than the seven at its first capture. Pre-fix copies beside. Run ONCE, after the controls."""
import subprocess, shutil
G = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-22_gate16B_seatB/'
hhmm = subprocess.run(['date', '+%H%M'], capture_output=True, text=True).stdout.strip()
def patch(f, pairs):
    p = G + f; s = open(p, encoding='utf-8').read(); shutil.copy(p, p + '.pre-' + hhmm + '-seatclate')
    for old, new in pairs:
        assert s.count(old) == 1, (f, old[:60]); s = s.replace(old, new)
    open(p, 'w', encoding='utf-8').write(s); print('patched', f)
patch('prompt_gate16B.DRAFT.part1.txt', [(
 "#1156 KS-1237, #1158 KS-855, #1160 KS-944 at the drafter's capture; #1162 KS-1156 and #1163 KS-1188 landed after it, 18:36:04Z / 18:43:32Z — more may\nland: state the set YOU read and when).",
 "#1156 KS-1237, #1158 KS-855, #1160 KS-944 at the drafter's capture; #1162 KS-1156, #1163 KS-1188, #1164 KS-1193, #1165 KS-1217 and #1166 KS-910 landed\nafter it, 18:36:04Z … 19:08:40Z — TWELVE at Seat C's 19:12Z HOLDING STATUS, its PR 2 KS-1123 HELD; more may land: state the set YOU read and when).")])
patch('prompt_gate16B.DRAFT.part2.txt', [(
 "    gh_seatc_late_1.out). Seat C's PR 2 (KS-1123 F3b) is HELD un-pushed (its TS18046 delta +1 — Wednesday 16:53:40Z); more of its thirteen may land\n    while you work (KS-1193, KS-1217, KS-910 had no PR at 18:49Z): RE-READ its open PRs' files at your open, mid and close and state the set you\n    read and when",
 "    gh_seatc_late_1.out); then #1164 KS-1193 (ba730c6ac; two auth files ks1193-review-read-query-error-is-not-503 + ks1193-verification-reads-codeless-pool-timeout),\n    #1165 KS-1217 (4ecb09cf2; auth ks1050-profile-update-zero-rows-is-not-success +2/-1) and #1166 KS-910 (a08741f51; TWO `.test.sh` under scripts/__tests__/:\n    pre_push_hook_base_leg_comment.test.sh + pre_push_hook_base.test.sh — a BASH lane, Seat C's) by 19:08:40Z — 14 paths over its twelve PRs, ∩ ours ∅ (seatc_late_paths_1.out;\n    Seat C's 19:12Z HOLDING STATUS: twelve READY, GO subject `GO: merge #1148, #1150, #1152, #1154, #1156, #1158, #1160, #1162, #1163, #1164, #1165, #1166 batch`,\n    twelve-PR tree 4817a9c2ea23…). Seat C's PR 2 (KS-1123 F3b) is HELD un-pushed (its TS18046 delta +1 — Wednesday 16:53:40Z): RE-READ its open PRs' files at\n    your open, mid and close and state the set you read and when")])
patch('prompt_gate16B.DRAFT.part3.txt', [(
 "    every open Seat C PR at YOUR read (#1162 KS-1156 and #1163 KS-1188 landed after the capture; more may) — state the SET you read and WHEN, and",
 "    every open Seat C PR at YOUR read (#1162 … #1166 landed after the capture — twelve at 19:12Z; more may) — state the SET you read and WHEN, and")])
