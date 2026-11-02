Seat S 13th

ANSWER: PR 3 acceptance: three places zod 4 refuses input zod 3 accepted = (a).
- KEEP datetime (class 1): one helper in packages/shared on z.stringFormat('datetime', ...) with zod 3.25.76's own datetime regex and its offset/precision options, issue rendered as zod 3's ("Invalid datetime"), at all 14 `.datetime(` request-schema sites (the shared isoDateTimeSchema included, its custom message kept). Golden cells for "2026-11-02T10:00Z" (no seconds) and the offset / precision variants: zod 3's accept/refuse set reproduced exactly. The published spec keeps format: date-time. A timestamp without seconds is a plausible real client input, so refusing it would tighten validation, which this upgrade must not do.
- ACCEPT classes 2 (`.int()` beyond the safe-integer range) and 3 (coerce.number on Infinity / -Infinity / 1e400) as LISTED tightenings: they refuse only values JSON cannot carry faithfully (precision already lost before any schema; Infinity serialises to null), so no legitimate request changes. Conditions: (1) the PR body lists both with the exact inputs measured, their site counts (37 `.int`, 12 coerce) with the grep's positive control, and why; (2) one PINNING cell each (2^53 and "Infinity" refused with today's 400 envelope and a zod-3-shaped first issue), so the behaviour is deliberate and visible.
- Your "no record schema has an enum key" finding with its control: state it in the body.

Wednesday
