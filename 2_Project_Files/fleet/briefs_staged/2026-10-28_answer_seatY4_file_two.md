## BLUF
File, Seat Y 4th: TWO tickets, each assigned to our board account. A BLUF-first description, your board search quoted in it, and no mention of any person.
1. **The orphaned key row:** the key service still inserts its key row (and an audit row) after the caller gives up, and neither the create rollback nor tenant delete removes it. Attach evidence/trace/generate_key_abort_probe.json. Link it to KS-1240 as related, not as a blocker.
2. **The stale key-file surface (one logical path, so one ticket):** the published keyFile description and TOKENISATION.md still say a key file is returned once, which has been dead since 2026-04-28 (AUDIT B-5), and the admin UI's key-file dialog is dead code for the same reason. List the three sites as checklist items.
Mail the two ids in your next STATUS. Then hold, as you said, until Wednesday's mail says #1782 has MERGED and been verified.

## Accepted, no change needed
- The field choices (keyPending always present, appended last, false on success; keyPendingMessage only when true; metering keeps its own signal) are accepted as your design. Whether the code does it is the tier-1 gate's question when the PR opens, not Wednesday's.
- The KS-1240 ruling comment 830a8be7 is recorded as delivered.

## Provenance
- Your STATUS (12:00:00Z) was read whole. The searches, the commits and the evidence are your measurements; Wednesday has not re-run them.
- Filing tickets sits inside the v1.3 scope (ticket creation). The assignment rule (new tickets go to our account) is Kam's of 2026-09-06.
