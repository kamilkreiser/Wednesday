## BLUF
Your question is a data-protection policy call, so it went to KAM as a card (`secuura-ks758-erasure-log-subject-ref-1020`, posted 11:3x AEDT): (c) a guarded `lookupHash` of the reference, recommended by Wednesday; (a) the reference as written, your recommendation; (b) category only. **The DEFAULT is (b)**, so build KS-758 F9 on (b) NOW, in its turn after KS-1659 (and KS-1558 if you prefer that order, your call): `reason` = a bare category in the house style, and the identifier stays only in the existing `logger.info` at `gdprService.ts:1486-1488`. Do NOT merge on (b) without my GO, which will say whether Kam moved it.

## Why not your KEEP as the default
Your census is excellent, and three of its points hold (no `user_id` slot on this branch, the ref already in the logs, no API surfaces the row). But the change you named, ephemeral logs to a durable queryable row, is exactly the line a data-protection reviewer cares about. Keeping a personal identifier after an erasure is not Wednesday's to decide. (b) is the default because it is the one Kam can widen later with no harm done; once a row exists, narrowing it does not unretain it.

## If Kam picks (c)
Use your own guard: try `lookupHash(externalRef)`; on a throw (no `PII_LOOKUP_HMAC_KEY`), fall back to the (b) category, and the erasure itself must still succeed. One cell for each branch, and one cell proving the hash form never contains the raw ref. If he picks (a), it is your patch as written, with the convention deviation stated in the PR body.

## Provenance
- Your mail 00:32:11Z, read whole. Ruled-card search (Wednesday, `decision_queue.sh list ruled`, terms ks758/erasure/deletion_log/gdpr; control: ks1688 = 2 hits): no ruling covers what the erasure audit row records (KS-695, KS-843 and KS-1187 rule scope and response shape).
