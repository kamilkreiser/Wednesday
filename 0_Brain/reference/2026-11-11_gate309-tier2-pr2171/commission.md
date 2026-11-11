# Gate 309, TIER 2 (Sonnet, config): R 96th round 0 = PR 2171 (KS-2164), the GHSA-chp3-j5qr-2vfr audit-baseline entry. ONE PR, one verdict. Commissioned 2026-11-11 ~17:1x AEDT by the Mac mini Wednesday seat (16:0x rotation seat). PRIORITY: every Blockchain/Dev push is blocked until this merges.

Common rules: the tier-2 shape of /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-10_gate306-tier2-pr2166-2169/commission.md (read whole; its common-rules pointer and Constraints apply unchanged). Calibration: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-11_gate307-tier2-pr2170/verdict.md.

Pins (Wednesday's ls-remote 17:1x AEDT; RE-READ at start and end, say whether each moved):
- develop 6911aa643db13ad1d09b37dd69c38df01cb029a4
- PR 2171 head be5d7b6057cd00f85cc4978bf29fd6b3fe7071ee

AUTHORITY (not yours to re-decide): Kam ruled card secuura-ghsa-chp3-effect-platform-shipped-1111 = a, live board 2026-11-11 16:29:47 AEDT, verbatim "Accept it in the audit baseline until the shared re-triage date, and ticket the override". Your job is whether the PR does exactly that, correctly, and nothing else.
READY (read whole; reproduce, do not trust): /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-11_gate309-tier2-pr2171/ready_r96_round0.txt. The seat's brief: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-11_seatR96_raise.md (stamp block + ROW 0 section).

Questions:
1. File set: exactly ONE file, Blockchain/Dev/scripts/audit/audit-baseline.json, additions only (PR files API + a diff read; planted difference control).
2. The entry: ONE new key GHSA-chp3-j5qr-2vfr under `accepted` with package "@effect/platform", reason, ticket "KS-2164", decidedAt "2026-11-11", expires "2027-02-28"; the four existing keys byte-equal to develop's; the JSON parses; the schema check in scripts/audit/baseline-contract.mjs accepts it (run `npm run audit:contract` from Blockchain/Dev in YOUR scratch copy; count its cases).
3. The reason's facts match R 95th's measurement (REC95 = /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-11_seatR-95th/mail/out_status_advisory.txt): moderate, makeCookie unreferenced (with its control), 0.97.1 outside lucid's ranges, shipped via lucid -> provider; no claim wider than measured.
4. RED-FIRST ON THE LEGS: in your own copy, `npm run audit:gate` and `npm run audit:locks` from Blockchain/Dev FAIL naming GHSA-chp3-j5qr-2vfr WITHOUT the entry (develop) and PASS WITH it (the head); a planted past-expiry copy makes both refuse. If a DIFFERENT new advisory now fails either leg, report it as a finding (not this PR's fault, but the merge will not unblock pushes).
5. The PR body: Kam's ruling verbatim with 16:29:47, zero product bytes, KS-2164 stays open, the KS-1981 second-fuse sentence (2027-01-01), what was not run. Title 'Refs KS-2164:'; no closing word in closing form in title, body, commit or comments.
6. Merge tree onto today's develop: clean, with a planted conflict control. No open PR touches the file.
Constraints: read-only on the Secuura checkout (ls-remote, show, log, diff, ls-tree, cat-file, grep only; fetch/clone into YOUR scratchpad only); no push, no merge, no board/Linear/GitHub writes, no mail; never print secrets; no cd; quoted heredocs; whole-suite legs only at load1 < 8.
OUTPUT: verdict.md in this folder: GO / GO WITH NOTES / NO GO at the head sha, findings numbered G309-2171-N with severity, what you ran (commands + rc), what you did NOT run. Return it in full.
