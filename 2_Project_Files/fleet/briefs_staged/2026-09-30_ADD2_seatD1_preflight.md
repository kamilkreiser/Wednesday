# ADDENDUM 2 (Seat D 1st): before your ONE push, run npm ci AND build packages/shared INSIDE the pushing worktree (leg 14 refused B 49th's push without it)

**Measured by Seat B 49th at 05:39Z, not by Wednesday:** the pre-push hook runs INSIDE the pushing worktree, and its leg 14 (`ks949_main_seed_idempotence.test.sh`) FAILS when `packages/shared/dist/index.js` is missing there. B 49th's 1a push was refused on exactly that (60/61), and its suite is 27/27 green at the merged develop once shared is built.
**So, in the worktree you push Direction B from, and BEFORE the push:** `npm ci --ignore-scripts`, then build `packages/shared`. Keep your IMAGE-BUILD trees pristine as before; this is the push tree only. If leg 14 or any other leg still fails, STOP and mail; never `--no-verify`.
Nothing else in ADDENDUM 1 changes. `.push-lock-45` was released by B 49th at 05:36:48Z; it may take it again for its re-push, so wait if it is held.

PROVENANCE:
- leg-14 cause and control | Seat B 49th's status item1a preflight mail (05:39Z), relayed; not re-run by Wednesday | read 2026-09-30 15:40
