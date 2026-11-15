# Drafter notes, Seat C 42nd brief (KS-1600 null permissions), 2026-11-16 ~06:50 AEDT

Output: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-16_seatC42_ks1600_null_permissions.md (34183 bytes, STAMP block blank).

Measured
- develop cf87f40fc145 (06:32:15 AEDT), read 06:35:57; ordinals C 42nd 0, C 41st 1.
- originate mint condition (adminConfig.ts lines 1024-1027) carves out null with `&& d.permissions !== null`; one commit (94c8a05d, PR 2087) introduced it (git log -S, two strings).
- security service: schema `scopes: z.array(z.string()).default(['read'])` (index.ts:718), parse at 1268, ZodError -> 400 at 1549-1552. Schema line run through safeParse on zod 3.25.76 and 4.4.3: omitted ok ['read'], null FAIL, [] ok stored [], string FAIL.
- Design: null -> 400 same message/shape as other malformed values; omitted and [] unchanged.
- No open PR (65, 346 file rows) touches adminConfig.ts; PR 2158 already merged as the tip.
- Existing cell pinning null -> 201: ks1600-malformed-permissions-refused-at-the-admin-mint.test.ts line 110 (the only one in nine mint-related test files). Forced edit (W-1).

Traps seen while drafting
- A whole-originate `git grep -E` with `\s` returned empty although the known cell contains the text: a FALSE ZERO; left UNMEASURED in the brief, task stopped.
- The scratch blobless clone needed a repo-local credential helper (`gh auth git-credential`) for lazy blob fetches; clone is under _work/ only.

W-items: W-1 forced cell edit, W-2 docs (stale flow fragment sentence), W-3 falsy rows, W-4 message text, W-5 [] difference.

UNMEASURED
