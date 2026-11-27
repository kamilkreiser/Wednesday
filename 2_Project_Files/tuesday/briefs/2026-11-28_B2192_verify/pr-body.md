Three commits on `d2aeecf8`, the last a merge of main `826bb7a8`; three paths. `__tests__/rd490-open-access-banner-browser.test.js` gains 22 lines and loses 6. `__tests__/helpers/test-server.js` gains 3 and loses 2, all in one comment. The counts file moves by one test. No product code, workflow or other file is changed, and nothing is deployed.

## RD-1051: the rd490 browser guard takes its ports inside its own worktree's band
- `rd490-open-access-banner-browser.test.js` started its two product servers on ports from a fixed band, 38900-38939: the same numbers in every copy of the repository. Its reservation was a per-process `Set`, so it kept two servers of one run apart and nothing across two runs. Two copies running `npm run verify` at the same time could each probe the same port, see it refused and start a server on it. The file's listener check then failed the whole file (72 tests) in one copy. This was measured with three and with five copies running at once.
- The claim loop now walks this run's own band, `workerBand()` from `__tests__/helpers/test-server.js`: the jest worker's band inside the worktree's slot, the band every other server in the suite already uses. Two copies on different slots never search the same numbers.
- The rest is kept as it was:
  - the reservation is still made before the probe's await;
  - a port is still taken only when it refuses a connection;
  - after boot, the listener on the port is still checked to be the file's own child.
- One new cell asserts that both servers listen inside that band. Planting the old fixed band back makes exactly that cell fail.
- The new band, 20000 to 32159, also sits below Linux's default ephemeral range (from 32768). The old band, 38900, sat inside it.
- The helper's comment that said the slots stay below the rd490 band, and the test file's own header, now say where the ports come from.

The merge of main adds no change of its own beyond the counts file, which the project's own command regenerated on the merged tree: 6655 tests in 421 suites (main's 6654 plus the new cell).

## Choices made by the coordinator, not by the product owner
- One new cell, not a test of two concurrent copies inside the suite. The two-copy run was made outside the suite, as described below.
- The two other test files that still name the old band as a range to keep clear of (`rd591-cross-seat-isolation.test.js` and `rd573-jest-port-band-outside-ephemeral-range.test.js`) are left unchanged. They stay green, and their wording is now out of date.
- The merge commit brings main in. The branch was not rebased.

## Reviewed
An independent review read the whole change. It ran the file in two worktrees on different slots (0 and 11) at the same time, inside one acquisition of the machine's jest lock. Both runs were green, 73 of 73 each. Each pair of servers listened inside its own worktree's band (20000-20001 and 27040-27041), and no port was seen on both sides. The review also ran the full verify once on the head. It searched `__tests__` for any fixed listener in the band range and found none. gitleaks found nothing in the commits, their messages or the merge's diff.

## Named limits (nothing is refused for these)
- Two worktrees whose paths hash to the same slot (1 in 19) still search the same ports. The listener check names the collision as a failure, never as a pass. Keeping two such runs apart is the job of the machine's jest lock, not of this file.
- A tree at any commit before this change still uses the fixed band. Two such trees running at once can still collide as before.
- The hosted `build` job of this pull request is the first run of the moved band on a real Linux machine. A red result on the rd490 file there is a fix round.

## Deploy
None. The merge touches `__tests__/` and `scripts/`, which the Deploy demo workflow does not ignore, so a run starts on the push. Both of its jobs are expected to read skipped because the switch variable is not set.
