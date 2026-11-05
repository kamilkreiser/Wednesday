STARTABLE: YES, after 10:08 today (all 21 on-disk objects already outside the 3-day line at the drafter's reads); five images and `/tmp/x_never` are unmeasured by the drafter's fences.
BLUF: Kit B1300 (69 lines, seat R175, Sonnet) removes 27 named regenerable leftovers (B1123 Step 6's 18 plus B1085 and B1096 from B1108 STATUS :180), about 1.97 GiB on disk plus 5 images; the 09-29 ruling authorises REMOVAL for this class (not quarantine), so the kit removes these and quarantines anything else; the newest object `.tools/b1101` is 2026-11-02 09:59:48, outside by 7 min at the 10:07 read.

## Facts re-measured (all clocks from `date`)
- Thu 5 Nov 2026 10:06:34 AEDT: B1123/B1108 kits and both STATUS files located (`Briefs/2026-11-02_B1123_STATUS.md`, `..._B1108_STATUS.md`, 208 lines; the "REMOVAL STILL OWED" paragraph is `:180`, found by `grep -n`).
- Thu 5 Nov 2026 10:07:01 AEDT, `stat -f '%Sm'` of every path (the tools live at the project ROOT `.tools/`, not `2_Project_Files/.tools`: my first stat there printed ABSENT x29, a control for the second run that found them):
  - wt-b1084-base 2026-11-02 02:40:10, -fix 02:40:10, -mut 02:40:11
  - wt-b1101-main / -head / -mut all 2026-11-02 08:02:09
  - wt-b1047-base / -fix / -mut all 2026-11-01 21:41:10
  - b1084 2026-11-02 05:57:59; **b1101 2026-11-02 09:59:48**; b1047 2026-11-02 02:15:17
  - b1085 2026-11-02 04:35:41; b1096 2026-11-02 08:10:26
  - wt-b1085-main / -head / -mut 03:12:11, -merge 03:12:17; wt-b1096-main / -fix 06:29:16, -mut 06:29:17
  - Not in the kit, printed for the partition: b1108 12:00:46, b1123 13:42:14, wt-b1108-main/-head 10:14:10, -mut 10:30:06, -merge 10:26:25, wt-b1123-rec 13:56:05
  - /tmp/x_never: 10240 bytes, 1 Nov 21:39 (ls -la).
- 10:07:09 to 10:07:11: `find <path> -newermt '2026-11-02 10:08:00' -print -quit` printed nothing for all 21 objects; controls: `-newermt` earlier cutoffs on b1101 and b1047 each printed a file. Directory mtime alone is not clause 3's test, so the kit tests the newest file inside.
- 10:07:40: `du -sk` as in the kit (A trees+dirs 1,029,780 KB; B 1,033,228 KB). `df -k` at 10:07:01: avail 158,172,336 KB, 92% used.
- Worktree registrations: `ls .../2_Project_Files/.git/worktrees` shows 15 of 16 trees registered with gitdir files naming `.tools/`; `wt-b1085-merge` is NOT registered (my `git worktree list` was barred by fence 3, so this is a directory listing, not a git verb).
- Open PRs on datasecau/Datasec-Security-Composer (`gh api -X GET`, Composer `.gh-config`, 10:07:32): #91, #86, #85 only, none a target lane; control: state=closed prints #118, #117, #116. (My first call used `{owner}/{repo}` placeholders from the wrong cwd and returned `[]`; discarded, redone with the explicit repo.) #110 merged 2026-11-01T23:07:28Z, #111 merged 2026-11-02T01:50:47Z.
- Panes at 10:08:00: `%0 tuesday`, `%1 fleet-monitor` only. Kit scan of non-`.pre-` SEAT kits of 11-04/11-05 for target names: no hit (control: B1123 kit hits `x_never`). `lsof -nP -- /tmp/x_never`: empty, no control run (UNMEASURED-strength).
- Ruling quoted from `0_Brain/learnings/2026-09-29_regenerable-build-leftovers-are-not-kept.md:17-20` and `:26` (`cat -n`). The ledger copy of the 11-02 clause-3 catch is `_ledger_laptop_datasec.md:83` (named in the file listing by grep, not read as a source for the kit). Quarantine rule: `2026-08-26_never-delete-cleanup-means-quarantine.md` (narrowed by the ruling for this class only); the 10-07 archive-to-G-DRIVE rule covers bulky NON-regenerable items and does not apply to regenerable ones.
- Launch-line prefix `Datasec/Security-Composer-<seat>` from the B1173/B1181/B1197 launch lines; model id `claude-sonnet-5-5`; routing row C8 `model-routing.md:98`, no removal row exists.
- Kit checks: `/usr/bin/grep -c '____'` = 8 (7 slots + last line); `@[A-Z_]+@` = 0; ASCII only (no output from the non-ASCII scan after the first grep -P failed on macOS; re-ran with [:print:]).

## D-decisions
- D1: the ruling's method is removal by the project's own seat with `df` as proof; so the kit REMOVES the class and quarantines everything else. B1123's `worktree remove` / `rm -r` / `docker image rm` method is reused, no `--force`.
- D2: clause 3 is tested on the newest file inside each object (and its mtime), cutoff taken at the removal command.
- D3: B1123's never-delete list named b1085 and b1096; this commission overrides that for those two lanes only, explicitly stated in the kit.
- D4: `wt-b1085-merge` (unregistered) is moved to `.tools/b1300/quarantine/` unless S6 says YES.
- D5: hard stop Step 0 + 45 min; heartbeat and seat-local lock `.tools/b1300/removal.lock` kept from B1123.
- D6: B1108's own trees and directory and B1123's are excluded.

## Q for Tuesday (each with a default)
- Q-1: Sonnet or Opus? Default Sonnet (C8 by the B1123 precedent; not row C4, nothing here is product data).
- Q-2: include B1108's own `.tools/b1108` (889,508 KB) and `wt-b1108-*`? Default NO: the commission names only b1085, b1096 and "their trees"; B1108 STATUS labels them "mine, for review"; their newest mtime is 2026-11-02 12:00:46 (a later dated kit can take them).
- Q-3: `wt-b1085-merge` is unregistered: remove or move? Default move (S6 = NO).
- Q-4: confirm the 3-day test on the newest file inside rather than directory mtime. Default yes.
- Q-5: the images of List A are unmeasured (docker is outside my fences); B1108 `:180` says b1085 and b1096 images are gone. Default: the seat records ABSENT or HOLD per the kit.

## UNMEASURED
Docker images and containers; `git worktree list` and each tree's cleanliness; process list; `lsof` control; load1; whether `wt-b1085-merge` contains a `.git` file; whether any of the five tags is in use by a container.

## Outside the fences
None crossed. I printed the clock of a first `cd /dev/null` attempt that the hook refused (nothing ran). I read the B1293 and B1294 kits (templates), `model-routing.md` lines, `launch_when_cool.sh` header, and the project `.git/config` remote line and `.git/worktrees` listing (file reads). No card read, no `decision_queue.sh`, no docker, no az, no git write verb.
