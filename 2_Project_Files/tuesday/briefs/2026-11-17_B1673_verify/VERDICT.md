GATE B1673: GO WITH FINDINGS @ 5e9a3d4 on main b81793d

Tier G2, one round, HPSM-POC lane H-D (B1672): `next` 16.4.2 to 16.4.5. Own clone in `fleet/state/s286/g1673/head` (deploy key, repo-local core.sshCommand), node v24.21.0, ports 9912-9915 (inside 9910-9919; 0 listeners before and after), nothing pushed, no PR, no merge, no Jira, no alert dismissed, no deploy. Run 21:00 to 21:12 AEDT 2026-11-17. Logs in `evidence/`.

## Findings
| # | Severity | Finding | Recommendation |
|---|---|---|---|
| 1 | Minor | The builder's pr-body.md ended with the plain text "Generated with Claude Code (https://claude.com/claude-code)", not the required footer. | Use pr-body.md in this folder (footer corrected, nothing else changed). |
| 2 | Info | `next@16.4.6` exists (modified 2026-11-16) and `npm audit` at main names it as the fix target. 16.4.5 is the lowest patched release, audit reads 0 at head, and the two alerts name 16.4.5 as first patched, so the lane's target is right. | None; a later bump is a separate decision. |
| 3 | Minor | I did not re-run main (vitest, shards, build notice at main). The "main" columns in the landing texts (4339 passed / 304 files, 972 passed, notice at main's first build) are the builder's, not re-measured. My head numbers equal the builder's exactly, so the claim "no change" rests on identical counts. | Accept; hosted CI runs main and head. |
| 4 | Minor | CodeQL ran with no planted-flaw control (0 results over 718 files). | Hosted code scanning is the proof; PR lands through it. |
| 5 | Info | Load1 rose to 17 to 23 during shards 3 to 7 (my own run plus the shared machine); every shard still passed, no retry, no timing red. | None. |

## Measured rows
| Check | Result |
|---|---|
| Refs | head 5e9a3d4066007983b81980e04386ba976fd403f0 (fetched by name), main b81793d15f41d133f5c2657329e31aef3ac00322; `rev-list --count main..head` = 1; open PRs 0; origin main still b81793d at the end |
| Diff | exactly 2 paths: `web/package.json` 1/1, `web/package-lock.json` 40/40 (80 lines). package.json diff is only line 20 (`"next": "16.4.2"` to `"16.4.5"`, exact pin) |
| Lock by JSON load | changed `packages` keys = 11 = "", node_modules/next, node_modules/@next/env and the 8 `@next/swc-*` (set equal to the expected set); added 0, removed 0; other top-level keys (name, version, lockfileVersion, requires) equal; root diff only `dependencies`; each non-root entry changed only in resolved/version/integrity (next also dependencies/optionalDependencies); eslint-config-next entry equal, still 16.3.6 |
| Integrity | lock next integrity equals `npm view next@16.4.5 dist.integrity` (sha512-rmdfsWos...CdXbBw==); `deprecated` empty |
| Ranges | no caret or tilde added (0 added lines carrying one) |
| Text | diff non-ASCII 0; commit message non-ASCII 0; no ticket key, brief/seat id or name in the message; the digits-hyphen hits are test counts and the shard names; one trailer (Co-Authored-By: Claude Sonnet 5.5); author = committer (name and email, equal) and equals the project checkout's configured identity (name equal, email equal, length 46) |
| Audit at main | `npm audit --package-lock-only`: `next 16.3.0 - 16.4.4`, 1 moderate (GHSA-mfr8-8qww-v76h) |
| Audit at head | `found 0 vulnerabilities` |
| Planted 16.4.4 lock | prints the 1 moderate again |
| Dependabot | alerts 10 (package.json) and 11 (lock) open, both first patched 16.4.5 |
| Cache-feature grep (unstable_cache, use cache, cacheComponents, cacheLife, cacheTag, revalidateTag) | 0 files (control: `next/server` finds files) |
| npm ci | rc 0; installed next 16.4.5 |
| lint / typecheck | rc 0 / rc 0 |
| vitest whole | 304 files, 4339 passed, 0 failed (builder: 304 / 4339) |
| build | rc 0 on the first try; no security notice (the only "security" text is the app's own /security routes) |
| `--check-shards` | plan OK, every test in exactly one shard |
| e2e, CI=1, all eight shards | journey-and-prototype 198 (2 timed + 182 desktop + 14 hosted); playbook-desktop-1 65; prototype-desktop-2 178; prototype-tablet-1 181; prototype-tablet-2 178; playbook-desktop-2 55; playbook-mobile-1 64; playbook-mobile-2 53. Total 972 passed, 0 failed, 0 flaky, 48 skipped; per shard equal to the builder's |
| CodeQL 2.27.4 | javascript-typescript, javascript-code-scanning.qls (87 rules), 718 of 718 files, 0 results, no control (finding 4) |

## Landing texts (builder's evidence folder checked; approved copies in this folder)
- pr-title.txt (67 chars), squash-subject.txt (67 chars), squash-body.txt: confirmed true against my runs (11 entries, 80 lines, 304/4339, 972/48, audit 1 to 0, two alerts), ASCII, one trailer, no names or keys. Copied unchanged.
- pr-body.md: corrected footer to `🤖 Generated with [Claude Code](https://claude.com/claude-code)` (finding 1). Rest unchanged and true.
- landing.txt: copied unchanged; the `--match-head-commit 5e9a3d4066007983b81980e04386ba976fd403f0` pin equals the head I reviewed. Its quoted landing rule is RELAYED by the builder, not checked by me.

## NOT RUN
- main-side re-measurement (finding 3); `scripts/audit-dev.mjs` and the infra scans (not asked; no code or workflow change by diff); deploy-package (cannot complete on a Mac, builder says identical at main); hosted CI and hosted CodeQL (Tuesday's); CodeQL planted-flaw control.
