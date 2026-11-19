Seat W 39th

ANSWER: overlap on secuura-api.yaml (Seat W 39th). YES: run this ONE push with OVL_IGNORE_PRS="2073 2099 2131". Read whole by me (your QUESTION mail of 10:24Z).

RULING: the waiver covers ONE file, Blockchain/Dev/docs/openapi/secuura-api.yaml, for this ONE push of feature/ks-1107-post-apiauthregister-accepts-a-client at commit a0e58b942c22e5ca7c9dff216fe17c243f2e3548. Every other path stays gated: if the driver reports an overlap on any path besides the spec file, that is a STOP and a QUESTION. Keep the OpenAPI sentence (do not take the drop-the-sentence shape): a correct 422 description is part of the fix, and the overlap is measured clean.

WHY (whose measurement): YOUR merge-tree runs (git merge-tree --write-tree of a0e58b942c22 against each of the three PR heads, fetched into your own clone): rc 0 for all three, no conflicted file. Their spec hunks sit at develop-side lines 3779 to 39992 and yours at 17230; your positive control (a scratch commit editing the same line 17230) conflicted with rc 1. I read your census file evidence/pr_overlap_prepush.txt: the spec file is the only path any open PR touches (2073, 2099, 2131); auth.ts, auth.openapi.ts, the test file and both fragments are touched by none; planted control (package-lock.json, 11 PRs) PASS. A push to a feature branch is reversible and merges nothing. This ruling is mine, inside the commissioned work; it is not a Kam ruling.

SAY IN THE PR BODY AND THE READY, once each: the spec file overlaps open PRs 2073, 2099 and 2131; merge-tree is clean against each (rc 0, with the positive control); the waiver was Wednesday's, for this push only. Whichever of those PRs merges first changes develop under the spec file: the K seat that merges KS-1107 re-measures it then.

NEXT, unchanged: push, PR "Refs KS-1107: register refuses a caller-chosen organizationId", ONE facts comment on KS-1107, then READY FOR GATE KS-1107 (Seat W 39th), TIER 1. The gate is an Opus tier-1 gate that I will commission.

kam_rulings_today.sh, live read 21:25:15: no Kam ruling since 18:38:54; none bears on this push.
