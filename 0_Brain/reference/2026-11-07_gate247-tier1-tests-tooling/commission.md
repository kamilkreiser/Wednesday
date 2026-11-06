# Gate 247, tier 1 asked, round 1 of 2: PRs 2062, 2064, 2074, 2069

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md, read whole first. Clone: /private/tmp/g247. Tier reason: seats asked tier 1 on content (a security pin, comments in product code, the push path). Mass is small. You may say a PR's tier was too high; say so, it does not change this round.

- PR 2062, KS-864, head 71566cce6101 [H/2026-11-06_seatT-14th/mail/out_12_ready_ks864_body.txt]. Test only, one file.
- PR 2064, KS-1205, head 836e21a79d9e [H/2026-11-06_seatT-14th/mail/out_14_ready_ks1205_body.txt]. Six comment lines in product code: confirm by your own diff that no code line changed, and that each comment is true.
- PR 2074, KS-1728 batch 2, head e8c950ecb30d [H/2026-11-06_seatK-18th/mail/out_READY_ks1728b2.txt]. Its section F3 raises systemTest/scripts/check-package-format.sh:585, printf into awk with exit under pipefail in a push gate: say what the gate returns today and whether it can lie.
- PR 2069, KS-1613 follow-up, head 3f4ca578d3e3 [H/2026-11-06_seatJ-20th/drafts/ready_ks1613fur.final.md]. It edits preflight.sh, the push path; words and cells by the seat's statement. Could it let a bad push through, or refuse a good one?
