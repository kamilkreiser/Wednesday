BLUF: (Seat L4) #1218 KS-897 + KS-896 = NO GO in the tier-2 gate (QA 05:33:03Z, report sha256 55cfc49a…, verified by Wednesday), round 1 of 2 under the cap. KS-896 is MET exactly. **KS-897 is NOT met (blocking, FIXTURE-LASTCMD):** `( … ) >"$WORK/build.log" 2>&1 || { …; exit 2; }` tests only the subshell's LAST command, so a MID-build failure (the gate's T897b) still gives rc 1, 9 passed / 19 failed, all 28 cells run, and no named abort. Your T897 aborts only because `mkdir -p "$root"` (:76) sits outside the subshell. **And a SAFETY defect rides on it (FIXTURE-GITENV):** when the fixture root fails and the caller's cwd is inside a git repo, the remaining git verbs rewrite THAT repo, including `git push -q origin main develop` against its real origin. It happened in the gate's own clone; the gate verified nothing reached origin.

## Fix shape (the gate's, measured on bash 3.2.57)
- `( set -e; … ) >"$WORK/build.log" 2>&1; rc=$?; [ "$rc" -eq 0 ] || { echo "FIXTURE BUILD FAILED …" >&2; sed … >&2; exit 2; }`. Do NOT use `( set -e; … ) || {…}`: bash 3.2 ignores errexit inside a `||`-tested subshell (the gate's evidence/97).
- Move `rm -rf`/`mkdir -p "$root"` INSIDE the subshell, or guard it. The fixture must never run a git verb outside its own root: `cd "$root" || exit 2` inside, and prefer `git -C "$root"` on every verb.
- Two regression cells: (1) T897b-shaped mid-build failure → rc 2 + the named line + 0 cells; (2) T897 run from a cwd INSIDE a scratch git repo → rc 2 AND that repo's HEAD, refs and config byte-identical (hash them before and after). Neither cell may ever reach a real remote: point the scratch repo's origin at a local bare repo or `no-push://`.
- Subject for round 2 (the gate's, ≤92 chars): `KS-897 FIXTUREABORT + KS-896 CONTROLEXISTS: pre-push base suite aborts on an unbuilt fixture`. Keep `Refs` only.

## Until it merges
Never run `pre_push_hook_base.test.sh` or `run-shell-suites.sh` from a cwd inside a git repo. The same fleet warning has gone to the other seats.
READY again as round 2; it joins the next tier-2 batch. PR 2 (tier 1) continues as queued. #1227 and #1229 stay queued for the next tier-2 batch.
