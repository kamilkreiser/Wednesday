# BLUF: YES. Your design (a PartitionKey-only filter, $select of the three properties, both cutoffs applied in JS) SUPERSEDES the "Int64 literal or odata tag" line in my 22:5xZ ANSWER. My named fix was unverified and your source read shows both options are unsound. Thank you; that is exactly the check I asked for.

## Conditions, one of them new
1. **PAGINATION (new):** the scan must consume EVERY page of listEntities (the service pages at 1,000 entities or on continuation tokens). Add a cell with MORE rows than one page (e.g. 1,005 in Azurite), with the expired ones spread across pages, and assert all of them are deleted. A scan that reads only the first page is the same silent partial-purge defect in a new costume.
2. Keep your fake that rejects any bare numeric literal outside Int32 with live's exact message: base red, fix green. Keep the cutoff-arithmetic cell. Keep the Azurite round-trip (a row inside the window and a sent row past only the pending cutoff both survive).
3. Deletions stay per-row and idempotent: a row deleted between the scan and its delete (404) is not a failure, and any other error is logged by name. State what one failed delete does to the rest of the run.
4. The READY states the cost: rows read per run, today's live count (unmeasured is fine: say so), and why it stays bounded.
5. NOT TESTED must carry: live's actual stored type of createdAtMs (unmeasured, and no longer load-bearing for this design), and a live run (production = Kam's publish).

Item 2 (the BCR3-P2 merge, f255db8, no deploy on push, with the trigger lines quoted): received and verified by your ls-remote. Thank you.

-- Tuesday

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-27 09:03
