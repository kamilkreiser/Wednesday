# Gate 251, tier 1, round 1 of 2: PR 2087, KS-1600 item 3

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md, read whole first; one correction: the QA template's no-rm rule wins, leave the clone at /private/tmp/g251 and name its size. Never cd, even in a subshell. Tier reason: behaviour change on originate's admin API-key mint.

- PR 2087, head 954af815c7b71497485c71fd3321f015650ef512 [H/2026-11-06_seatV-26th/mail/out_06_ready_item2.txt]. Card secuura-ks1600-originate-malformed-permissions-1106 = a; the card requires callers measured first.

Specific asks:
1. The seat says originate reads `permissions` and security reads `scopes`, that 'matching' means the same validity rule, and that a body with only `scopes` is still ignored to ['read']. Does the gateway rename it? It did not measure that. Read it. Can anything mint wider than asked?
2. Two differences remain by Wednesday's answer: absent, null and [] become ['read'] at originate; security stores [] and refuses null. Read the card: inside Kam's words?
3. Callers: are 0 production senders of a malformed value right, by your own search? State the frame.
4. The refusal runs where, against what has already been read or written? The seat says RED showed 201 with one INSERT: confirm no insert on the refused path.
5. Overlap with PR 2060 on adminConfig.ts is granted: merge the two heads and run the file's cells on the merged tree.
