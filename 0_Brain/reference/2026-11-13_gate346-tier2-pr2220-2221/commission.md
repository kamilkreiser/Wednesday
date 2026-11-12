# Commission: QA GATE 346, TIER 2, on PRs 2220 (KS-1105) and 2221 (KS-1913), Secuura/Blockchain, 2026-11-13 07:2x AEDT

Commissioned by Wednesday (06:00 morning seat). Findings only: nothing fixed, posted, mailed, pushed, merged or written to Linear. Work only in `scratch/` of THIS folder (gitignored); write `verdict.md` here.

## Copy-and-change
Template: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_gate344-tier2-pr2184/commission.md` (read WHOLE; method, scratch-clone rules, fences, red-proof requirements and verdict format apply). Notes from gate 345 (`/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_gate345-pr2079/tier.md`, last paragraph): set `core.sshCommand` in your scratch clone from the project's `2_Project_Files` repo config or blob fetches fail; `gh repo clone` over https returns Repository not found.

## Subjects (pins by Wednesday's ls-remote 07:23:07 AEDT)
- develop 1dd6299bccd61b884d5c31eda3f43e85ebbc72ff
- PR 2220 (KS-1105) head ab5a7e119cc8ef3740750504f8631d4031c5f9dd: frontend/admin src/pages/Login.tsx (+1 -1, placeholder string) + new src/__tests__/ks1105-admin-login-email-placeholder-is-neutral.test.tsx (+39). Parent 410feda1a85e (one commit behind develop's move by PR 2198: 3 auth files, no overlap claimed by the author).
- PR 2221 (KS-1913) head 32a9bf0fb2d329453e417a76d92af6ab429f3148: frontend/admin src/pages/platform/PlatformAuditLog.tsx (+3 -0, two badge entries) + new ks1913-platform-audit-log-archive-actions-are-styled.test.tsx (+56).
- The author's READY FOR GATE (Seat R 116th, 20:21:42Z) is the claim under test; its text is in the batch `/private/tmp/wed_newmail/batch_20261112T202300Z.txt` (read it; quote nothing you did not re-measure).
- Re-pin all three refs before your first measurement and again before the verdict.

## Tier
Tier 2 (Wednesday's STAMP for Seat R 116th, item 5): a placeholder string and two style-map entries. If you find anything that changes an auth decision, a request, stored data or a security surface, STOP and write `tier.md` (Wednesday relaunches on Opus).

## Questions
1. Does each PR do exactly what its ticket asks (read KS-1105 and KS-1913 at Linear, read-only, Blockchain project key; quote each scope sentence)? KS-1105: is the new placeholder neutral and is the old company-address string gone from every rendered login surface (grep frontend/admin for the old string at the head)? KS-1913: do the two new action names match what the server writes (names in services/tenant-provisioning; the author measured by name only)?
2. frontend/admin has NO test runner in the repo. Reproduce each cell's red-first (the cell alone against develop's unchanged file RED; with the change GREEN) under the author's external config `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/tiers/vitest_configs/frontend-admin.config.mjs` (read-only; do not write in the Spark store), in your scratch. If you cannot run it, say NOT RUN and why.
3. Colour: KS-1913 adds orange-500 and reuses the tenant_deleted red classes. Every class must already exist in the admin palette (grep the admin src at develop for each class string; positive control a class you know exists). An off-palette class is a finding (the style-guide rule).
4. tsc --noEmit on frontend/admin at each head and develop; eslint with the repo's root flat config on the changed files.
5. merge-tree of each PR against develop 1dd6299bccd6 (each side's own merge-base), both orders, rc and tree; a planted develop-side conflict must refuse; then the pair 2220 x 2221 (they touch different files: confirm 0 shared paths and a clean chain).
6. docs-fragments check: the author chose NO-PAIR on '244 new, unchanged': reproduce.

Verdict format: line 1 `PR 2220: <GO | GO WITH NOTES | NO GO> (at head <full sha>; tier 2)`, line 2 the same for PR 2221; then FOUND / TESTED / HOW / NOT TESTED; findings G346-<pr>-N. Model: Sonnet (tier 2). Return a 10-line summary.
