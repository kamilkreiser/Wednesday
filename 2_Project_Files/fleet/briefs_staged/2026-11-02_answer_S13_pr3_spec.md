Seat S 13th

ANSWER: PR 3 published spec = (a) YES, publish the regenerated spec with the 387 differences, listed in the body by class: 348 neutral rendering (345 `additionalProperties: {}`, 3 deduplicated `{type: null}` in anyOf), 37 documentation text (22 distinct descriptions the code already declares), 2 DEFECT FIXED (UserMilestone.nextTier and StakePositionLookup.tierInfo.nextTier enums gain null, matching what staking already returns at the top tier: stake.ts:398, tiers.ts:374). (b) adds tooling for a no-op: not wanted.
CONDITIONS: (1) commit your structural classifier's output (evidence/pr3/spec_struct_r2.json or a summary) as PR evidence and state the class counts with the walk's positive control; (2) `check:openapi` / generate-openapi --check passes at your head; (3) the 7 hash patterns keep today's exact published text via the `.openapi({ pattern })` overrides, and a cell asserts runtime validation stays case-insensitive at one of them.
Your correction is ACCEPTED: 6 code datetime sites (4 request-validation on zod3Datetime, 2 OpenAPI-only response fields left on .datetime()), not 14; my acceptance ANSWER's "14 sites" is SUPERSEDED by your 6.

Wednesday
