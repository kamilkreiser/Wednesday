# B407 drafter report (C8 Sonnet), 2026-10-21 14:45-15:00 AEDT

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-21_B407_SEAT-D21_hpsmpoc-word-pack-b.md` (105 lines, 2 unfilled slots: `@STAMP_TIME@`, `@LAUNCH_AUTH@`; no `.pre-stamp` made). Structure copied from B386 (`.pre-stamp` copy, whole) and B398 (whole). The word-pack note was read whole (42 lines).

## Measured facts (instrument)
- Main = `ec0a62a1ac107e26d859b5eebd220153a0cf691c`, commit time 2026-10-21T01:18:04Z: `git ls-remote origin refs/heads/main` and `gh api repos/datasecau/HPSM-POC/commits/main` agree (14:45). Object present locally (`git cat-file -t` = commit), so every grep below ran at that sha, no fetch.
- Open PRs: one, #171 (`b383/sqlite-rebuild-atomic-292`, api test-only): `gh pr list --state open`. No overlap with the census files.
- Ports 7930-7939: `lsof -nP -iTCP:7930-7939 -sTCP:LISTEN` 0 lines (no control run; the brief tells the seat to run one).
- Records `CLARIFICATIONS.md` from origin (`gh api` raw, 2126 lines): C-105 at `:1235` (the push-to-demo grant) and its line `:1240` "every word a customer will see is Kam's"; C-130 `:2051` (HP review this week); latest C-132 `:2094`. The B386 brief's phrase "Kam's C-105: every customer-facing word is Kam's" is correct in substance. The project `CLAUDE.md` (51 lines) has no restricted-docs or wording text (grep `-i` returned nothing for restrict/word); the hold is carried from B386's HOLDS section (verbatim) instead.
- Tests/checks commands: `web/package.json` at `ec0a62a1`: `test` = `vitest run`, `typecheck` = `next typegen && tsc --noEmit`, `lint` = `eslint --max-warnings=0`, `build` = `node scripts/build.mjs`, `test:e2e` = `node scripts/e2e.mjs`. B398 STATUS `:70-71`: base 1898, after 1919 (older main).

## Preliminary census (git grep at `ec0a62a1`; the seat's own census governs)
Command shape: `git --no-optional-locks -C .../2_Project_Files grep -I -h -o -e '<pat>' ec0a62a1 -- . <pathspecs> | wc -l`. Controls fired: `-i datasec` = 2,196 lines; `preferred_username` found in 3 files.

| Variant | Count | Where |
|---|---|---|
| `-i 'security services playbook'`, whole tree | 394 matches | 358 in `web/src/content/**` + `api/.../SeedContent/**` (HP-supplied), 36 outside |
| outside content: exact `HP Security Services Playbook` | 12 | already correct |
| outside content: `Security Services Playbook` without `HP ` | 24 (sub-counts 15 web/src non-test + 3 web/src tests + 7 e2e = 25; lookbehind difference, unexplained, seat must reconcile) | 11 person-read component files, layout.tsx, phase-flow.ts, 2 unit tests, 6 e2e specs |
| outside content: `HP Print Security Services Playbook` | 0 | lives only in packages |
| `DataSec` exact | 8 | all in `web/src/components/home/` (phase-flow.ts :4 comment, :22, :23, :65, :66; PhaseFlow.test.tsx :16, :46, :48) |
| `DATASEC` / `-i 'data[ -]sec'` | 0 / 0 | the on-screen "DATASEC IMPLEMENTATION PATH" is source "Datasec implementation path" (`phase-flow.ts:19`) uppercased by CSS `PageHeader.tsx:21`: no edit |
| `-i datasec` lines | 2,196 | identifiers, org, hosts, e-mail domain (group-classified) |

Findings beyond the word-pack table: the unprefixed name appears in about 11 more screens than the note listed (PackView, DocumentGeneration, ReportScreen print covers, ClientShell, PlaybookHome/Shell, HomeScreen x2, PartnerDashboard, DesignSystemScreen eyebrow). No product-name hit in `api/` outside SeedContent, contract and comments; no manifest in `web/src/app` (favicon only). `brand.css:11 --brand-name` has no consumer.

## Questions, with recommended answers (the brief already applies the recommendation as a default; Tuesday may veto before the deploy)
1. Does "one name everywhere" reach the 11 extra screens the note did not list (print/report covers, follow-up header, Playbook pages, Home)? Recommend YES (the ruling says everywhere a person reads it); applied.
2. Browser-tab default (`layout.tsx:8`): the card gave only the template. Recommend default = `HP Security Services Playbook` (drop the internal code name "HPSM-POC —"); applied, flagged for veto.
3. `phase-flow.ts:66` "DataSec Security Services Playbook Web Platform": recommend `Datasec HP Security Services Playbook Web Platform` (insert `HP `, fix spelling, no other word). `:65` "DataSec-HP Playbook Platform Enabler": spelling only (`Datasec-HP ...`). Applied, flagged.
4. Bare "Playbook" (phone header span `AppShell.tsx:148`, "The Playbook", menu nouns): recommend LEAVE (a section noun, and changing the phone header changes layout); listed in STATUS as LEFT.
5. Contract titles (`openapi.yaml`, already "HP Security Services Playbook ...") and `brand.css --brand-name`: recommend leave, list. Content packages and SeedContent: leave entirely (HP-supplied; web/api copies are parity-tested).
6. Timing (my proposal, not measured against a clock owner): READY by 16:30, hard stop 17:30, gate tier 2 (from the note's timing line). Veto if the deploy plan differs.
7. Header width: the desktop header span gets longer with the fix; the seat reports (renders at 1280/375 if load allows) but does not fix.

## Not done / UNMEASURED
No npm, vitest, next or Jira call. Whether a unit test pins `layout.tsx` metadata; the 7 e2e hits' completeness; the e2e specs cannot be run by the seat (listed for Tuesday). The attribution in B386 of the word pack is unchanged by this brief. "Kam" is deliberately absent from the brief except one instruction quoting the word to avoid in Jira texts.
