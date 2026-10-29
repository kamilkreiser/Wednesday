# Spark operator 13 report, 2026-10-30 (Secuura / Blockchain only)

Saved by Wednesday from the operator's returned text. Condensed. Specs, runners and logs sit beside this file.

## BLUF
- Three briefs, each lint ok, `--dry-run` ok and `--control` PASS 7/7 with the golden byte-identical.
- All at develop `203734468019feaf44428975b10cf5f799483187` (ls-remote re-read at the end, unchanged).
- Two are real candidates: KS-1840 and KS-1823. `ks_1840_p1_stale_citation_loose` is a rung-4 calibration twin of the tight KS-1840 brief.
- Nothing was queued by the operator.

| Brief dir (local-model/night/briefs/) | Ticket | Mode | Files | Control | A4 reds | Overlap |
|---|---|---|---|---|---|---|
| ks_1840_p1_stale_citation | KS-1840 | code_patch2, vitest | anchoring/src/index.ts (one 3-line comment hunk :983-985) + NEW ks1840-stale-gateway-citation-is-gone.test.ts | PASS 7/7, 126 s | 2 of 5 | 0 vs 22 open PRs; shares index.ts with the HELD KS-1454 P2 readback pass (:42, :956-963), disjoint hunks |
| ks_1840_p1_stale_citation_loose | KS-1840 (rung 4) | code_patch2 loose | same | PASS 7/7, 87 s | 2 of 5 | same |
| ks_1823_p1_dockerfile | KS-1823 | code_patch2, vitest | api-gateway/Dockerfile (+2 lines above "# Relax strict ...") + NEW ks1823-dockerfile-drops-spec-backups.test.ts | PASS 7/7, 70 s | 3 of 8 | 0 |

## Refused
- **KS-1831..KS-1835:** originate documents.ts, which #1814 owns. KS-1831 and KS-1833 are also decision-shaped.
- **KS-1836:** decision-shaped (every record carries userId 'user-id'), and next to the mint money path.
- **KS-1837:** the mintNFT money path; needs a service-token design. If ever spelled out, it gets a tier-1 gate.
- **KS-1838:** the mint money path.
- **KS-1839:** a question, and needs a Schemathesis report or a box.
- **KS-1824:** needs a live DB and a concurrency design.
- **KS-1825:** wallet / UTxO.
- **KS-1826:** a 1.1 MB generated spec; check:openapi unrun.
- **KS-1840 DEVELOPMENT.md:121:** the builder refuses a second service, so this stays as a doc-only follow-up on KS-1840.
- **First KS-1823 draft (.dockerignore):** refused, because the builder needs a product under one service. Quarantined at night/briefs/_quarantine_2026-10-30/ks_1823_p1_dockerignore/; logs in quarantine/ here.

## Unmeasured (operator)
- No docker build was run for KS-1823.
- The unmatched-glob `rm -f` behaviour is the operator's reading of sh.
- Whether any current caller treats a 404 as no anchor.
- Other docs that paraphrase the retired claim.
- Whether the deploy rsync uses --delete.

## Wednesday's disposition (2026-10-30 03:5x)
- Read both golden.diff files WHOLE.
- Premises re-read at source in her own clone at 203734468019:
  - makeFetchDocFromAnchorStore: 1 hit (the comment), removed by 78cb3c393 "KS-1628 (2 of 2)".
  - Tracked docs/openapi: 3 files, 0 matching the rm globs.
- QUEUED ks_1840_p1_stale_citation_loose (rung 4; the tight brief is the one rebrief) and ks_1823_p1_dockerfile.
- Raise notes:
  - KS-1823's PR gets a TIER-1 gate (deploy surface).
  - The KS-1840 describe title overclaims ("no comment or doc row" while reading index.ts only); the raise seat retitles it.
