STARTABLE: YES, after the Stamp; nothing waits on an answer (Q-1 to Q-4 all have defaults), target 16.4.5 exists and is not deprecated, main and the pin are as the ticket says.

# B1672 drafter report (lane H-D, SEAT-H179, HPSMPOC-508), 2026-11-17

Clocks (`date`): start 20:32:37, mid 20:33:51, last re-check 20:37:12 AEDT. Files: the kit (131 lines, longest line 1825 characters), `.measured` sidecar (S01-S10 plus one line per claim), this report. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s286/d1672/` (Jira dump, registry lists, scratch clone, both scratch lock trees and diffs).

## Measured
- Registry: 16.4.5 (2026-11-03) and 16.4.6 (2026-11-09) both exist; `latest` is 16.4.6; neither shows a deprecated field (no positive control found, said so). Lowest patched = 16.4.5 = the target. Q-1 offers 16.4.6; the kit has a version rule (try 16.4.6 once only if 16.4.5 is red, land nothing at 16.4.6 without Tuesday).
- `next` is an exact pin (`web/package.json:20`). Companion `eslint-config-next` 16.3.6 (line 41) is already one minor behind `next` at main and green; the kit leaves it (Q-2). `@next/env` and eight `@next/swc-*` are `next`'s own and move in the lock only.
- Lock change is confined: `npm install next@16.4.5 --save-exact --package-lock-only` in a scratch clone of main `b81793d1` changed exactly 11 `packages` entries (root, `next`, `@next/env`, 8 swc), 0 added, 0 removed, other top-level keys equal; `package.json` diff one line; 80 changed lock lines of 9225; integrity equals the registry's. 16.4.6 gives the same 11 entries.
- Registry audit on the lock: main `1 moderate` (GHSA-mfr8-8qww-v76h); 16.4.5 and 16.4.6 locks `found 0 vulnerabilities`. This is the lane's property (C). The app does not use the cache feature (grep 0 files, with controls).
- CI audit steps (`ci.yml` 390, 395) gate on high/critical only, so the medium alert does not fail CI and CI will not prove the bump: the seat's proof is `npm audit` itself. Dependabot alerts 10 and 11 still open, both patched at 16.4.5.
- Not measured: any build, vitest or e2e at 16.4.5 (no `npm ci`; load1 was 8.44); whether the build notice (`SecurityFatalError`) disappears at 16.4.5 (a prediction in the kit; the seat records it); the hosted CI result.

## Kit shape
Same form as B1659: ports 9900-9909 (0 listeners, 0 kit mentions; controls fired), pane `Datasec/HPSM-POC-H179`, Sonnet (`claude-sonnet-5-5`, row L3 line 82), gate G2 (Q-3 asks if G1), READY target 240 minutes (all eight e2e shards run locally at main first, then at 16.4.5; vitest whole, lint, typecheck, build, `--check-shards`, both audits, infra scans, standalone package). Red-first stated as not applying; the property is (A) confined diff, (B) everything green as at main, (C) advisory range excluded, plus a planted-wrong audit control. One commit on new branch `b1672/hpsmpoc-next-16-4-5`, one push, no PR, nothing deployed; landing files written for Tuesday.

## Q-questions (defaults)
- Q-1: 16.4.5 or 16.4.6? Default 16.4.5 (lowest patched, ticket text).
- Q-2: move `eslint-config-next` in step? Default no (not this lane; a lint config can add rules).
- Q-3: gate G2 or G1 (a framework runtime bump)? Default G2 as the sweep gave it.
- Q-4: all eight e2e shards locally (long, the drafter estimates 2 to 3 hours serial; unmeasured) or the two B1659-style files only? Default all eight, because the ticket says "end-to-end checks".

## Disclosures
- Read: the sweep file, HPSMPOC-508 (whole, GET-only helper copied from the sweep scratch, token never printed), the B1659 kit, sidecar, report, STATUS and run counts, `model-routing.md`, `models_latest.json`, `ci.yml`, `e2e.mjs`, `audit-dev.mjs`, `playwright.config.ts`.
- Network: npm registry reads (`npm view`, `npm install --package-lock-only`, `npm audit --package-lock-only` over scratch lock copies); `gh api -X GET` under the project's own `GH_CONFIG_DIR`; one shallow `git clone` with the `github_deploy_rw` key (not the analysis key). No hosted host, no Jira write, no `az`.
- Writes: the briefs folder (kit, sidecar, this report) and the scratch folder only. No `cd`, no `rm`.
- Instruction-shaped text met: the B1659 STATUS quotes the Next.js build notice ("ask about `next upgrade`") and `npm audit` prints "npm audit fix --force"; neither was acted on; the kit names both as text, never instructions. The tool hooks printed grep-style advisories; the one count that relied on a cut line was not used as an absence.
- stamp_check: 54 claims, 54 measured, 0 not measured. Many sidecar lines are marked "instruction to the seat" or RELAYED (B1659 build-notice lines) rather than drafter-measured; that is stated in each line.

DRAFTED B1672: kit 131 lines, sidecar 54 claims measured, questions 4
