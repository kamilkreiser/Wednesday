KS-1379 PR #1339's standalone locks were re-resolved from bare manifests: ~1,000 non-target moves, incl. runtime bullmq/msgpackr 2 and @azure/identity/msal-node 6
state Backlog

Raised from **gate41's finding N-1339-2** (Major, non-blocking) on PR #1339 (KS-1378, the four-package advisory bump). Wednesday ruled this a ticket rather than a fold-in for round 2, because the only mechanism the gate's own fix-shape offers is `npm install --package-lock-only`, and host npm 11.5.1 dies with `Cannot read properties of null (reading 'edgesOut')` on this machine — measured by Seat B 43rd even on a bare `package.json` in an empty temp dir, so it is the host npm build and not the workspace layout.

## What happened

#1339's 13 standalone `package-lock.json` files were regenerated **from their bare manifests** rather than from their committed locks. That resolved every dependency afresh, so about **1,000 versions moved that the bump did not target**. All are inside their declared ranges, so nothing is a range violation — but nothing exercises them either: the suites run from the **root** lock, which moved **0** non-target versions.

## The moves that matter (gate-measured)

* `services/queue`: **bullmq 5.76.2 → 5.81.5**, pulling **msgpackr 1 → 2** — runtime.
* `services/m365-integration` and `packages/shared`: **@azure/identity 4.13.1 → 4.13.3**, pulling **@azure/msal-node 5 → 6** — runtime.
* `services/originate`: minimatch 3 → 10, plus dev-only eslint-cache majors.

## Fix-shape, quoted verbatim from gate41's report

> Fix-shape: regenerate each standalone lock FROM its committed lock (`npm install <pkg>@<ver> --package-lock-only`), or declare the drift and add a standalone-install smoke (build + boot) per service.

## The condition attached to #1339 merging without this

Wednesday's ANSWER to Seat B 44th, 2026-09-29T03:54:40Z: the two runtime moves above **get a clean standalone** `npm ci` **plus that service's own suite in the next gate**, so what ships untested by the root-lock suites is tested once. **Merged is not deployed:** no deploy carries these until this ticket is done or Kam says otherwise.

## Blocked on, and why it is not just "run the command"

`npm install` in any form is unavailable on this host. Seat B 43rd's workaround for #1339 was `node:24-alpine` (npm 11.19.0), mounted at `/src` — **never** `/dev`, which clobbers the container's `/dev/null` and dies rc 127 before starting. Whoever takes this needs either that container route explicitly permitted, or a working host npm.

## Neighbours (cross-reference only)

KS-1290 (an npm command inside a workspace member moves platform discriminators silently) and KS-1154 (the root lock carries only the darwin rollup binary) are the same family — lockfile regeneration doing more than it was asked to — but neither covers this drift.

Discovered 2026-09-29 by gate41 on PR #1339; ticketed by the Platform K build seat under Wednesday's ruling.
