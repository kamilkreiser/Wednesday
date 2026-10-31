# QA Gate 55 - PR #1865 (KS-1403) - TIER 2 config, findings-only
Head: e1a592d56c25b45fcbb60949b3fe0e207e9bec23 (base dc8c210cb29d; develop ddc644fb4869 merged in a scratch merge, clean, no conflicts)

VERDICT: GO

Findings
1. Diff: 1 file (Blockchain/Dev/scripts/audit/audit-baseline.json), 0 insertions, 7 deletions. Exactly the GHSA-vfj7-8cjw-p6xm row (key, package, reason, ticket, decidedAt, expires). No other row/field touched. JSON valid at merged tree.
2. Merged tree (PR + develop ddc644fb4869): audit:gate rc 0, "10 distinct advisories reported, 10 baselined", no CLEANUP line. audit:locks rc 0, "44 standalone lockfiles ... 8 advisories match, 8 already baselined".
   Control develop ddc644fb4869: audit:gate rc 0 but prints "CLEANUP (advisory): 1 baseline entry is no longer reported - remove: GHSA-vfj7-8cjw-p6xm (braces, KS-1403)" ("10 reported, 11 baselined"). audit:locks rc 0. The PR removes exactly that CLEANUP.
3. GitHub advisory API (unauthenticated): withdrawn_at = 2026-10-23T12:53:02Z. The id appears in no other baseline row (0 hits in audit-baseline.json at merged tree).

UNMEASURED
- Author's READY mail and the card text not re-read (Kam ruling not re-verified by me).
- No CI run observed; local audit scripts only. audit:locks needed semver: installed with npm i --no-save in the throwaway clone (no repo change).
- Reference grep beyond audit-baseline.json (rest of tree) not done.
