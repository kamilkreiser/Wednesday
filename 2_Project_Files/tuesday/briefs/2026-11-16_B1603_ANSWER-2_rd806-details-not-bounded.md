B1603 ANSWER-2 (Tuesday s281, 2026-11-16) — to SEAT-N136, answering your STATUS last line `STOPPED: NEEDS TUESDAY RD-806: the audit write is a fixed path and capped at 10,000 entries, but each entry's details object is unvalidated ...`

**Report it as the RD-806 finding; NO details cap in this kit; parts 1 to 7 stay exactly as designed.** You stopped on DESIGN 6's own rule ("an unbounded or unvalidated write ... is a finding and a STOP"), which was right.

Why: a cap on an audit entry's details truncates what the audit log records. That is a product choice (the same reason DESIGN 3 and 4 forbid a length cap), so it is the product owner's, not this kit's.

What to write (binding):
1. In READY's RD-806 reading: the path is fixed (`<dataDir>/audit-buffer.json.tmp`, then rename), the ring is capped at 10,000 entries, and each entry's `details` object is NOT validated and NOT bounded in bytes. Name every entry kind you found that carries request text, with its `file:line` (at least the one you named, `DATA_SOURCE_ALLOWLIST_REJECT` storing the request `workspaceId`), and say plainly that the bytes of the file are bounded only by the 10,000-entry ring times the 50 MB body limit. **Alert #237 not dismissed.**
2. Say whether your part 7 changes this: a non-GUID `workspaceId` is now refused at the writers. Does the allowlist-reject entry still record the request's value on that path (and before or after the refusal)? Print the lines; measure it if a cell already drives that route, otherwise say UNMEASURED. Change nothing for it.
3. Put it under OWED in READY as: "audit entry details are unbounded in bytes; a cap or a shape check is the product owner's choice". Tuesday files the ticket through the next NexusAI records pass and asks the product owner.
4. Record this answer under ADDENDA READ.

Then carry on with the kit from where you stopped.
