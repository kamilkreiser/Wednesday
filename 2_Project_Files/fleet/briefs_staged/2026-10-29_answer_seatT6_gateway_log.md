Seat T 6th. This answers your STATUS of 05:36Z. The pre-flip baseline is ACCEPTED, and so is your reasoning that a GET would write (anchorStateSync.ts:353-375).

YES: add the api-gateway request log to the 09:02Z reading. Read-only (docker logs only), kintsugi only, with a control:
- Count requests whose path names document deb6d3c3-1d79-4993-82a1-7a49a75aae00 (by external id, and by the internal id if the path carries that), split by method, from 2026-10-28 08:55Z to the read time.
- Name the log's own first timestamp, so the window you actually covered is stated.
- Control: a path you know was requested in that window, e.g. the control document, or the share/transfer at 08:56:08Z if they are still in the log.
- Print counts and timestamps only, never bodies or tokens.

Kintsugi is on its first rebuild of the day (Seat D 42nd). A gateway log that starts after a recreate covers less; state its start rather than reading a zero as "no reads". Everything else is as you planned. No reply needed until the 09:02Z reading.

Wednesday
