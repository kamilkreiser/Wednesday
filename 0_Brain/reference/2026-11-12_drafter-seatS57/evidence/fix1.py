import re
p='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_drafter-seatS57/brief_S57_body.md'
t=open(p).read()
R=[
("`gl.sh lines SHA PATH A B` or `gh_lines`","`gl.sh lines` (arguments in order: the sha, the path, the first and last line) or `gh_lines`"),
("it only wakes you for item 3d's QUESTION","it only wakes you for item 3b's QUESTION"),
("PR 2169 `3521d7889c93` (item 3d's question)","PR 2169 `3521d7889c93` (item 3b's question)"),
("PR 2169 `3521d7889c93` (item 3b's question)","PR 2169 `3521d7889c93` (item 3b's question)"),
("the PR 2124 residue (3f) is MEDIUM (3)","the PR 2124 residue (item 3d) is MEDIUM (3)"),
("`Delivered: PR N (SHA12) is merged to develop and is in the running Kintsugi build (REASON). Closing as done.`","`Delivered:` then the PR number, its 12-hex squash and the reason in a parenthesis, then 'is merged to develop and is in the running Kintsugi build', then 'Closing as done.'"),
("`bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show ID`","`bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show` followed by the card id"),
("the body names the search ('searched <the terms you ran>, N open hits, none covering')","the body names the search (a sentence 'searched' plus the terms you ran, the number of open hits and that none covers the four)"),
("a declared `S57-D<n>` edit adds KS-1845","a declared S57-D edit (S57-D1 and up) adds KS-1845"),
("gains a key ONLY by a declared `S57-D<n>` edit","gains a key ONLY by a declared S57-D edit (S57-D1 and up)"),
("A write needs its key on the allow-list by a declared `S57-D<n>` edit","A write needs its key on the allow-list by a declared S57-D edit"),
("(nine directories; line numbers below are S 53rd's, carried by S 56th's brief, NOT re-opened by this drafter)","(nine directories; the line numbers below are S 53rd's, carried by S 56th's brief, NOT re-opened by this drafter)"),
("the drafter did NOT open any of these seven)","the drafter did NOT open any of these nine)"),
(", the drafter's `ls | grep -i S56` found `2026-11-11_S56_answer_plan.md` only, positive control: that file matched",", the drafter's listing of that folder filtered by name for S56 shows `2026-11-11_S56_answer_plan.md` as the only answer file naming S 56th, positive control: the same filter matched that file and S 56th's brief"),
("completing with conclusion failure and one skipped; the repo total_count read 20542)","five runs: 'PR — Lockfiles (path-skip twin)', 'pr', 'pr-premerge-ack' and 'PR Security Gates' concluded failure and 'Dependabot standalone locks' was skipped; the repo total_count read 20542)"),
("five runs named 'PR — Lockfiles (path-skip twin)', 'pr', 'pr-premerge-ack', 'PR Security Gates (KS-168)'","five runs: 'PR — Lockfiles (path-skip twin)', 'pr', 'pr-premerge-ack' and 'PR Security Gates'"),
("(KS-1846, KS-1703 whole, KS-1511, KS-1327, KS-1015, KS-565)","(KS-1703 whole, KS-1511, KS-1327, KS-1015, KS-565)"),
("(KS-1846, KS-1703 whole, KS-1511, KS-1327, KS-1015, KS-565: read each whole)","(KS-1703 whole, KS-1511, KS-1327, KS-1015, KS-565: read each whole)"),
("the brace spellings `kyc/user/{` 0 hits and `kyc/{id}` hits KS-1853","the brace spelling `kyc/user/{` 0 hits (its control: the brace spelling `kyc/{id}` is searchable and) `kyc/{id}` hits KS-1853"),
]
for a,b in R:
    if a in t: t=t.replace(a,b)
    else: print('MISS',a[:70])
open(p,'w').write(t)
