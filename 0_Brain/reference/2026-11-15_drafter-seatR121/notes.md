# Drafter notes, Seat R 121st (PR 2239 fix round), 2026-11-15 22:3x

Output: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-15_seatR121_pr2239_fixround.md

## Choices and defaults set (for Wednesday)
- G4 (D2 pin) defaulted IN, with an out clause the seat must justify in the plan QUESTION. Commission said "consider".
- G8 port: the PR's test file uses direct mode (req.tenantId set by callerTenant); G8 needs the real resolver. Brief tells the seat to port the minimum switch, or use a new test file if cleaner (partition allows both).
- Comment draft Fix 1 defaults to DROP the "as revoke already refuses it" clause (alternative: name /api/keys revoke precisely).
- Overlap grant: the brief states Wednesday re-grants the same exact names for this one push by stamping the brief. That is a grant written into a brief Wednesday must consciously stamp; if she does not want to pre-grant, strike that sentence and make it QUESTION-based.
- PR body edit permission unknown; brief allows a PR comment fallback.
- Item 3: kept the "do not post" rule (10:48Z ruling) and requires a --dry only.
- Product change limited to the comment sentence at :159-160; the gate's proposed sentence quoted verbatim.

## Facts the drafter checked this run
- PR 2239 head f1ac5fec9b67 open, 2160 head b02bd2716cc2 open, develop 7b452b1bbb96, KS-1699 In Progress / 4 comments / newest 05:33:05.910Z, ordinals 0 and 1, push queue empty, load1 7.74.
- Line numbers at head: comment :159, function :162, new helper :199.

## UNMEASURED
- Linear state and newest-comment time for KS-1197 and KS-2017 (the drafter queried KS-1699 only); they are named in PROVENANCE as unread.
- Whether the gate's plant.py entry for claim_defaults_to_default_tenant applies to the branch file; I did not open plant.py.
- Share and recertify check line numbers at the head (:1388 and :1503) are taken from the gate verdict, not re-read in the file.
- Whether the harness port leaves the existing 54 cells untouched.
- Wednesday's intent on pre-granting the overlap exception in the brief.
- Brief size (under 35 KB by construction, not measured with wc).
