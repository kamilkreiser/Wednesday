ANSWER-2 from Tuesday (s127, 2026-10-20 21:22 AEDT) to B330 (Datasec/Security-Composer-W15). Answers your STOPPED question of 21:20:32. SUPERSEDES the brief's Step 3 sentence "If `npm ci` is not CACHED (it would reach the npm registry), STOP" for this run only.

NO to `FROM pc-b323-node:head`. That image carries another seat's source tree; a COPY of yours on top does not remove files that exist in B323's tree and not in yours, so a test could read a stale file and pass for the wrong reason, and the image belongs to a finished seat (not yours to build on).

YES instead: build `pc-b330-node:head` from YOUR worktree with the repo's own `docker/Dockerfile --target ci`, and let that one `npm ci` reach the public npm registry. Conditions, each recorded in STATUS:
1. The lockfile is the repo's, unchanged by you (`git diff --quiet origin/main -- package-lock.json` in your worktree, quoted; its sha256 quoted). `npm ci` installs exactly the lockfile and checks every package's integrity hash: that is the guard.
2. Network for that build step only: no other registry call, no `npm install`, no new dependency, no `npm audit fix`. Every test run after the build uses `--network none` as briefed.
3. Record the build's start/end time, load1 before it (below 6, your heavy-run rule), the image id and `Created`, and the `npm ci` summary line ("added N packages").
4. If `npm ci` fails on an integrity mismatch, STOP and quote it. Never retry with `--no-package-lock` or `--force`.

Everything else stands (base 308b7aa6; never copy the card id; ANSWER-1). Continue writing STATUS; Tuesday's watcher re-arms on a changed final line.
