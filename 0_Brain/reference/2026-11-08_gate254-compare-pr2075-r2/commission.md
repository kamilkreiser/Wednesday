# Gate 254: COMPARE, PR 2075 round 2 (KS-2083), wording only. Tier 2 (already-gated follow-up, docs fragments), Sonnet.

Commissioned by Wednesday 2026-11-08 ~21:0x AEDT. Kam's card secuura-ks2083-session-end-race-in-flight-1107 = a: "Merge with the wording corrected, and ticket the race High"; detail "A fix round on the wording only moves the head, so a compare follows."

Pins (Wednesday's git ls-remote origin on /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files, just before this file): PR 2075 head 32aa0d06bc0aceccb790443bbf16384ff0c8e930; previous gated head d2245bf37fe0c9a096dd8e90fb006035d454e753 (gate 245); develop a65ae7ed1d6083bde60c4198a60a528129277c40.

Read first: the seat's READY /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-08_seatY-7th/pr/sessend/ready_r2.txt (whole) and gate 245's verdict /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate245-tier1-y-auth/verdict.md (the 2075 section, F1 to F5).

Questions, each answered by your own measurement in a fresh clone of yours (by sha; no fetch into anyone else's checkout):
1. Is d2245bf37fe0..32aa0d06bc0a exactly the two KS-2083 fragment files, with 0 product or test bytes changed? Prove with --stat and a planted control.
2. Does every sentence the round changed match the code AT 32aa0d06bc0a and gate 245's measurements? Check each citation the new words make (session.ts:286 read-then-write; session.ts:332 returning 0; routes/users.ts:844 and :846; the fail-closed 401/500 line). A cited line that does not say what the sentence says is a finding.
3. Does the wording still say anywhere, without the serial-request qualifier, that the change closes the walk-around? Search both fragments and quote any hit.
4. docs-fragments check at the head: rc and last line, plus a planted defect that makes it fail.
5. Merge tree of 32aa0d06bc0a on a65ae7ed1d60: rc and tree id.
Out of scope: the auth code itself (unchanged, gated by 245), the PR body and the ticket comment (staged by the seat, posted after this verdict).

Write verdict.md here, line 1 = GO, GO WITH NOTES or NO GO, then findings, then what you did NOT test. Findings only: never edit the PR, push, comment or touch a ticket. No `cd`; no rm (leave your clone, state its path and size); nothing to any human.
