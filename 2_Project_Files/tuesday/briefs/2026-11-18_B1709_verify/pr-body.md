## What

Adds one step to the existing web job in `.github/workflows/ci.yml`, right after `npm ci`:

    npm audit --omit=dev --audit-level=high

It exits 0 only when the production dependency tree of `web/package-lock.json` has no high or critical advisory. Only `.github/workflows/ci.yml` changes (4 lines added, none removed). No job or check name changes, because a step is not a check.

## Why

MPSCALC-413: the web job ran no audit. Agreed by the product owner on 18 November: add a production-only audit step; the development toolchain is updated at the next routine dependency round.

## Checked

- Production audit at the base reads 0 vulnerabilities, exit 0.
- The full audit (development included) still reads 12 high findings, all in development tools. This change leaves them as they are.
- A production advisory planted in a scratch copy makes the step exit 1; the same package planted as a development dependency leaves it at exit 0.
- The three CI text tests pass. The workflow parses, job keys and names are unchanged.
- `web/package.json` and `web/package-lock.json` are unchanged.

## Known behaviour

The step asks the npm registry at CI time. A newly published high or critical advisory on a production dependency will turn the web check red on every PR until the dependency is updated, with no code change here.

## Deploy

Nothing is deployed. This changes CI configuration only.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
