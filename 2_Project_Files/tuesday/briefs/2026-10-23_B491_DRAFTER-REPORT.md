# B491 drafter report (2026-10-23 about 00:55-01:05 AEDT, read-only)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-23_B491_SEAT-G48_hpsmpoc-b489-and-pr184-gate-tier2.md` (about 50 KB). Seat `Datasec/HPSM-POC-G48` (J1 is the only HPSM-POC pane live; G48 free), Sonnet `claude-sonnet-5-5` row G2, tier 2, ports **8380-8389**, B-number B491, round 1 of 2 for both subjects. No `.pre-stamp` copy was made (fence: two files only); Tuesday can `cp` it before stamping.

## Measured by me (GitHub GET, ls-remote, lsof, tmux)
- main `4e77cf1d` (#187), B489 head `fd54671a` (compare: ahead 1, **behind 1** now, one file +25 -23, #187's 11 files disjoint), `refs/pull/184/head` `ff8339a4`, PR #184 open, ahead 1 behind 2, merge base `1d1fa462`, `mergeable` null.
- #184 lock patch read hunk by hunk: 11 changed (vitest, @vitest/mocker, @vitest/spy, chai, obug 2->3, std-env, tinybench, tinyexec, why-is-node-running 2->3 with engines `>=20.11`, two nested magic-string), 2 removed (siginfo, stackback), **6 added `inBundle` entries without resolved/integrity** under `@tailwindcss/oxide-wasm32-wasi`; 11 `+resolved`, 11 `+integrity`, 0 other hosts, 0 `hasInstallScript`.
- Open Dependabot alerts: #4 and #3 medium `@vitest/mocker` (< 5.0.3, patched 5.0.3), #1 high `braces` (<= 3.0.3, no patch). #184 appears to clear #3/#4 and not touch #1 (read from patch and alert metadata; the gate measures with `npm audit`).
- Check-runs on #184 head: 16, 15 success, CodeQL neutral; code-scanning alerts for `refs/pull/184/head` 0, repo open 0; five required contexts.
- **New fact:** `b429/telemetry-224` (ahead 29, behind 6, no PR) changes `web/package.json` +5 and `web/package-lock.json` +359 -4: the same two files as #184. b49 does not. I turned this into a Check 7 measurement (legacy merge-tree) and softened "overlap > 0" to "overlap that conflicts" for B.
- Ports: `lsof` 8300-8399 empty; 8380-8389 is named only by finished 2026-10-20/21 seats (B317-B421), not live.

## Relayed, not re-measured
All builder figures for A (21 rows, 11 at-risk, 5-minute skew, 1826/13/0, repeats, mutants), RELAYED CI figures, and that b429 is not live (no PR; gates B431/B436 exist).

## UNMEASURED (and why)
No npm or dotnet run (fence): `npm audit`, `npm ci`, the registry integrity match, whether the six bundled entries are a regeneration artefact, whether alerts close on merge, why CodeQL is neutral, whether a lock hunk conflicts with b429, the vitest release-note behaviour changes, A's whole Api count on current main.

## Departures from the templates
- Two subjects with different kinds (A uses the B488 batched shape; B has no builder STATUS and no ticket, so B's verdict is "mergeable / rebase / not safe" and the last line names #184 not a ticket).
- A3 requires the gate's OWN instrument, different from the builder's in at least one stated respect, plus a direct mint-stamp route (Property P read without waiting); the builder's scripts are read-only claims, never run.
- Trees: `-base` is current main (not a fork sha) for both subjects; builds only where needed.
- Mutants MA1-MA8 chosen to differ from the builder's (other rows, token never applied, ADDED-18 sign flip as the no-weakening proof, Names() missing a key); MA3/MA7 allowed to survive as Notes.
- Registry GETs limited to `npm view <name>@<version> dist.integrity` of the changed packages.

## `____` slots (8 lines)
Stamp time; stamped by; launch authority; hard stop; main at launch; both heads at launch; model receipt + load1; last line `READ-WHOLE-BY-TUESDAY: ____`.
