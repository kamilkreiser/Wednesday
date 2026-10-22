# B497 drafter report (2026-10-23, 06:07-06:25 AEDT)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-23_B497_SEAT-M1_nexusai-rd879-audit.md` (107 lines, 8 lines match the four-underscore pattern, control: the unstamped brief reads 8).

## DISAGREEMENT WITH TUESDAY'S FACTS (the headline)
RD-879 is ALREADY FIXED on NexusAI main. The morning sweep listed it as "npm-audit red on main"; that is the ticket's title, not the state of main.
- main `7c11c78f174a91ed2a376110966da19e775311e7` (`gh api repos/datasecau/Reporting_Dashboard_Au/git/ref/heads/main`, 06:07:09).
- Its `package-lock.json` (`gh api contents?ref=<sha>` raw, parsed `python3 -I`) has `node_modules/follow-redirects` **1.16.1**. Both advisories (GHSA-q3jh-wrc6-jgq8, GHSA-8r9p-f939-6h3c, `gh api advisories/<id>`) cover `>= 1.16.0, < 1.16.1`, first patched 1.16.1.
- The fix is B385's: branch `deps-follow-redirects-r13` @ `c139e4a8`, PR #104, merged 2026-10-20T23:00:27Z, gate B392 GO WITH FINDINGS; `compare c139e4a8...7c11c78f` = ahead 10, behind 0. B385 STATUS (108 lines) ends READY FOR QA for it.
- `npm-audit` run `39599876159` on main `7c11c78f` (push, 2026-10-21T12:28:30Z): completed/success.
- RD-879 (Jira GET `project = RD AND key = RD-879`): `To Do`, Highest, 1 comment saying it landed and "was not transitioned by the landing seat". It is stale.
So I wrote B497 as MEASURE-FIRST with a decision table: Row A (audit rc 0, expected) = STOPPED: NEEDS TUESDAY, nothing branched or pushed; Row B (only follow-redirects red) = lockfile-only fix with full B496-shape checks and a boot proof; Row C (any other package red) = STOP. The recommendation is that Tuesday does NOT launch it and transitions RD-879 instead (a Jira write, mine to avoid), unless a fresh `npm audit` today is red. The stamp slot "Advisory state at launch" says so.

## What I measured (all read-only)
- Manifests: `gh api git/trees/main?recursive=1` filtered: ONE `package.json` and ONE `package-lock.json`, at the root (no backend/frontend split). Workflows: arm-ttk, build, deploy-demo, deploy, gitleaks, npm-audit.
- Parents of follow-redirects: axios 1.20.0 (`^1.16.0`, production) and http-proxy 1.18.1 (`^1.0.0`, dev). Ranges admit any 1.x, so a lockfile-only refresh would be the route; the project does use `overrides` (tar, uuid, @tootallnate/once, with `overridesNotes`) but none is needed.
- CI predicate (`npm-audit.yml`): job `audit-production-deps`, `npm ci --no-audit --no-fund` then `npm audit --omit=dev --audit-level=moderate --json`, pass iff exit 0. Written into the brief. `build.yml`: node -c on 3 files, `npm run lint` (placeholder), `npm run verify -- --maxWorkers=2`.
- Open PRs: only #67 (`rd-777-776-validators-s92r`, 3 files, none a manifest). Branches `deps-follow-redirects-r13`, `deps-joi-jsyaml-qs-s59`; `b497*` count 0.
- Panes: tuesday, HPSM-POC-K1, HPSM-POC-J2, fleet-monitor; no NexusAI pane, `Datasec/NexusAI-M1` free. Ports 8450-8459: `lsof` empty (rc 1), no allocations in the briefs folder (the 845x hits are hash substrings).
- Server facts for the boot proof: `PORT` default 3001, `app.listen(PORT)` with NO host (binds all interfaces; the brief has the seat request only 127.0.0.1 and record the bind), `/api/health` public, `SESSION_SECRET` >= 32 chars required.
- `gh auth status` under NexusAI's config: a Datasec account, scopes gist/read:org/repo (login not written, no-names rule).

## Assumptions and not measured
- Assumed Row A is the likely outcome; nobody ran `npm audit` today (no npm allowed), so an advisory published after 2026-10-21 12:28Z is UNMEASURED. Row C covers it.
- NexusAI has no Api suite; I used its jest lock (`nexusai-lock.sh`, hash from B385 STATUS) and said so. Boot env beyond SESSION_SECRET is untraced. Hard stop 09:30, target READY 08:15 (suggestions).
- I did not read C-190/C-68 directly (CLARIFICATIONS grep was blocked by a hook on my first try and I relied on B425's line numbers `:2062`, `:665`, C-218 `:2362`); the seat re-reads them.
- Seat name M1 matches an older HPSM-POC brief (B329) only by letter; different pane prefix.

## Stamp-slot line numbers (brief file)
91 Stamp time · 92 Stamped by · 93 Launch authority · 94 Hard stop and target · 95 Main at launch · 96 Advisory state at launch · 97 Model receipt + load · 107 `READ-WHOLE-BY-TUESDAY: ____`.
