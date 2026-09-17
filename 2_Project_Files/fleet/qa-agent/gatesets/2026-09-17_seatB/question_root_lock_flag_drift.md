SUBJECT: [Secuura/Blockchain -> Wednesday] QUESTION: root lock flag drift in PR-1 hono (Seat B)
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat B

CONTEXT
PR-1 (hono x3), lock regen at develop f8c7aaa39, node:24-alpine, npm 11.19.0 (the host has 11.5.1):
- services/mcp-server: hono 4.13.0 -> 4.13.8. Parsed diff: 1 entry moved, 0 other.
- services/originate: hono 4.13.0 -> 4.13.8. 1 entry, 0 other.
- ROOT Blockchain/Dev/package-lock.json (`npm update hono --package-lock-only --ignore-scripts`, rc 0, npm printed "up to date"): hono 4.13.0 -> 4.13.8, plus 12 OTHER entries. All 12 are dev-flag changes; no version moved:
  - 11 x lightningcss-<platform> 1.33.0: `dev: true` -> absent (they stay `optional: true`);
  - magicast 0.5.3: `dev: true` -> `devOptional: true`.
- Your scope rule: I restored the root lock by content and sha256 (8ba0f053e73c5275, and `git diff --quiet` = the HEAD blob).
- CONTROL: a no-op write at the untouched develop tree (`npm install --package-lock-only --ignore-scripts`, "up to date") produces the SAME 12 flag changes and 0 version changes. Restored again, HEAD blob confirmed.
- So this is pre-existing flag drift that any write by this npm reconciles. It is not hono over-resolving.
- Mechanism, read from the lock: lightningcss is `devOptional` (an optional peer of a prod vite 7.3.6 at the root, and a dev dependency of the frontend vites), so its optional platform binaries are not dev-only. magicast is an optional peer of c12, which is devOptional.
- Reach: root lock only. Every image builds from a standalone lock, and both standalone locks here showed 0 flag drift. Host `npm ci` from the root lock includes dev, so nothing installs differently there. Only a hypothetical `npm ci --omit=dev` from the root would now install the lightningcss binary for its platform.
- Your brief names ONE recorded exception, pre-existing packages[""] drift, so I am asking rather than applying it. Every later root-touching PR (PR-3, PR-4, PR-5, PR-6) meets the same 12 unless the first one to land absorbs them.

QUESTION
May PR-1's root lock carry the 12-entry flag reconciliation, stated in the PR body with the no-op control as its proof ("pre-existing flag drift; 12 entries, 0 versions; reproduced by a no-op write at develop")?
(a) YES (recommended): recorded like the packages[""] exception. Later PRs then see 0.
(b) NO, narrow by writing with the npm version that produced the committed flags. That version is unknown. Finding it means fetching older npm CLIs via `npx npm@<v>` inside the container, a registry fetch outside the (b) you authorised; say if you authorise it.
(c) NO, other.

MEANWHILE
- PR-1's two standalone locks stay in my worktree, uncommitted; copies are in records.
- Continuing with PR-2 (colord) in a second worktree of my own (worktrees/raise-0917-b-audit-2), and the row 15 cardano-sdk tarball diff.

NEEDED-BY
Before PR-1 can push. Not urgent against a deadline: PR-1's rows lapse Thu 24 Sep 10:00 AEST.

Seat B
