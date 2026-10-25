STARTABLE: YES

# B713 DRAFTER REPORT (SEAT-M14, NexusAI lane N-FLAKE, RD-867)
Drafter: Sonnet, 2026-10-26 07:52-08:0x AEDT (clock from `date`). Kit: `2026-10-26_B713_SEAT-M14_nexusai-867-logger-live-flake.md` (155 lines).

## BLUF
- Startable now: one test file, no path shared with any open PR (0 open) or with B703 (its 5 test paths plus the counts file); main `8ae0a87f`, file blob `c00b8d8a` (hash recomputed over the raw bytes), 322 lines, 10 cells.
- The kit makes the seat MEASURE FIRST: a node mechanism probe with a planted-failure control, then N runs of the unmodified file (S arm shipped, A arm amplified by in-cell repetition on a scratch copy) with a stop rule, then the change, then an interleaved A/B at N >= max(N_base, 3 N_base / k), a revert, and two router mutants under both files. No base failure in the campaign = PARTIAL, nothing pushed.
- Drafter finding that changes the ticket's story: the one preserved failing report shows the failed cell took **11 ms** (suite 319 ms). That cannot include a 5 s idle keep-alive timeout, so the ticket's literal cause (H1) does not fit; a stale pooled socket on a REUSED ephemeral port across stands (H2) does. Correlation from one report only; the kit ranks H1/H2/H3 by measurement.
- `undici` is not a dependency, so the ticket's "per-request dispatcher" recipe would add a new import: the kit forbids it. Sibling stands already call `server.closeAllConnections()` before `close` (precedent, 3 files read plus 5 more in the index).
- Landing rule quoted: C-190 item 2 at `1_Project_Definition/CLARIFICATIONS.md:2067`, "Merge path: open a PR from the gated branch, wait for CodeQL ... then land the SAME commit. Never squash, never rebase ([[C-68]])." = a MERGE commit; `:2068` no dismissals; `:2073` every `Analyze (<language>)` run completed; addendum `:2076` second threshold; C-218 (`:2362`) records the one slip.

## Facts re-measured (instrument, control)
| Fact | Reading | Instrument | Control that could fail |
|---|---|---|---|
| origin main | `8ae0a87f564b72fc1f9082cd89013740e7162d58` | `git ls-remote` | same sha as the sweep and the B703 kit |
| open PRs | 0 | `gh api -X GET pulls state=open` | `compare/19b7106b...6e076b29` lists 6 files (the compare call works) |
| remote branches vs main | b617, b632, b642, b658, b689, records/b362, b605, b656, b681 all ahead 0, 0 files | `compare/main...<branch>` | the 6-file control above |
| b703, b713 refs | none on origin | `ls-remote 'refs/heads/b6*' 'b7*' 'records/*'` | b689 and records/* lines printed |
| test file | blob `c00b8d8ac7bbecf9d5df71b510301fd03233cdf8`, 15835 bytes, 322 lines | raw contents + `printf 'blob 15835\0' | cat - f | shasum -a 1` | recomputed hash equals the API's blob sha |
| file history | one commit on main, `b4464361` (2026-09-05) | `commits?path=` | the router file's log returned 3 commits |
| cells | 10 (3 + 2 + 3 + 2) | read the file; and the preserved report lists the same 10 | two independent sources agree |
| preserved failure | 4683 tests, 1 failed, failed cell #8 of 10, **11 ms**, suite 319 ms, message `TypeError: fetch failed`; sibling cells 153 and 92 ms | `python3 -I` over `session-tools/s101/flake-rd338-qaf2/verify-report-fail.json` | other nine cells printed `passed` with durations |
| undici in deps | absent; express ^5.1.0, jest ^29.7.0 | `package.json` at main parsed by `python3 -I` | jest and express keys found by the same filter |
| node | local v26.8.1, npm 11.19.0; CI `node-version: '24'` (`build.yml:29`) | `node -v`, grep of `build.yml` | the grep also found `runs-on` and the verify line |
| sibling stands | `closeAllConnections` at `rd395-server-harness.js:67`, `rd516-ai-test-ssrf.test.js:206`, `aoai-stand-in.js:143`; `keepAliveTimeout` 0 hits | raw contents grep; `search/code` | nonsense token returned 0 (search is an index, not a census; the kit makes the seat re-count) |
| prior work | none: JQL `sustainability-logger-live` = 7 tickets (RD-867 + context), `keepAlive` = 0, no STATUS file under `Briefs/` names RD-867 | Jira GET via the HPSM-POC helper; `grep -l` over `*STATUS*.md` | JQL control `zzz-no-such-string-7f3a` = 0; B703's STATUS found by `RD-882`-style control |
| counts | blob `a8085c1d64f92427a95fbda0fd3db6000f97cf61` (pair 5102/306 RELAYED from B703's read at the same sha); depth-1 `*.test.js` census = 306 | `contents` GET; `git/trees` recursive filter | census equals `suites` |
| pane name | `Datasec/NexusAI-M14` (M5 to M13 used; M99 is a control) | word-boundary scan over 98 non-`.pre-` SEAT kits of 10-25 and 10-26; `tmux list-panes -a` (live: tuesday, NexusAI-M13, Security-Composer-G133, fleet-monitor) | scratch line `x NexusAI-M99 y` matches once |
| ports 9800-9809 | free | `lsof -nP -iTCP:9800-9809 -sTCP:LISTEN` rc 1; word-boundary scan hits B630 (finished MPS seat), B687 (no port needed), B634/B643/B692 (prose naming B630's block), B650 (`9806 ms` timing) | scratch line `x 9800 y` matches once; the kit orders a bind-and-see control at launch |
| lock tool | sha256 `cf01bafbc51f555ca0f14d1711f01885bcec5bc6293b177fe24702226bb4971f`; base `locks-laptop-1017`; held now by B703 tag `b703-build-final` pid 16993, queue-jest empty | `shasum -a 256`; `ls`; `cat owner` | matches the value in the task and the B703 stamp |
| load | load1 7.63 at 07:55 (above 7: heavy runs wait) | `uptime` | n/a |
| model | `claude-sonnet-5-5`, C2 at `model-routing.md:92`, G2 at `:109`, id at `models_latest.json:23` | `grep -n` | the grep also matched opus (line 17) and the other rows |

## D-decisions (mine; Tuesday accepts or overrides in the stamp)
- **D1 unit and N.** A UNIT is one full `driveToCap` (one stand, 45 requests, one close). Arm S = 300+ separate jest runs of the shipped file (900+ units); arm A = a scratch copy (outside `__tests__/`, never staged) whose three QA-F2 bodies loop T times, stopping at 5 failures or 20000 units. The after arm is interleaved with base blocks and sized at max(N_base, 3 N_base / k) so a null result has a 5 percent false-comfort bound. Reason: the field rate is 1 in 4683 cells, so a short loop would read 0 at base and "fix" nothing.
- **D2 the measurement is the fix's precondition.** BASE must fail at least once in the SAME interleaved campaign, else PARTIAL (no push). This is the task's "a fix the seat cannot show is not a fix", made mechanical.
- **D3 mechanism probe is a node script, not jest, outside the lock** (one light process; P0 planted stale socket must produce the exact ticket error or the instrument cannot see the failure and the seat STOPS). H1/H2/H3 each have an amplifier; the probe uses ports 9800/9801 only.
- **D4 allowed fixes are ranked by evidence, not by the ticket**: `connection: close` in `hit()` (proved honoured by a connection-event count), `closeAllConnections()` in the stand's close (sibling precedent), keep-alive setting only if H1 is proven; NO undici import, NO retry/skip/catch, NO assertion change.
- **D5 non-weakening proof**: two temporary router mutants (old cap wording; cap no longer bounds) run under BOTH the base and changed file; a cell green under the changed file but red under base is a STOP.
- **D6 PARTIAL pushes nothing** (a hardening that cannot be shown is exactly what the ticket forbids); the measurement and the exact diff are the deliverable. New last-line marker `PARTIAL:` (template had READY / STOPPED / BLOCKED).
- **D7 whole verify at the head** as in B689/B703: the pinned pair is the CI predicate; arithmetic is the plan, the run is the proof.
- **D8 count-neutral by construction**: the cap-hit scratch copy is never under `__tests__/`; 10 titles identical by program; `git status --porcelain` clean before the verify.

## Q-questions for Tuesday (each with a default)
- **Q-1** Gate tier: tier 2 (G2, Sonnet) or tier 1? Default: tier 2, test-only, one file, no product byte.
- **Q-2** On a PARTIAL (base never failed in the campaign), push nothing and hand Tuesday the measurement plus the diff? Default: yes, push nothing.
- **Q-3** Campaign cost: arm S 300 runs plus arm A up to 20000 units, each loop held under the jest lock at most 40 minutes per ticket. The lock is shared with B703's final verify and any gate. Default: accept; raise the stop rule only if base shows 0 after the first ceiling and Tuesday asks.
- **Q-4** Ticket priority: Jira says Medium, the sweep row says Low. Default: no effect on the lane.
- **Q-5** Brief mentions `node` v26.8.1 locally vs 24 on CI; if the failure only reproduces on 26, should the PR still land? Default: yes if the mechanism is a stale-socket reuse, which is node-version independent; the gate states the version in its note.

## UNMEASURED
No npm, jest, clone, fetch, worktree, node probe, browser, CodeQL or workflow run was made by me. Not measured: the base failure rate under any loop; which of H1/H2/H3 holds (H2 rests on ONE report's 11 ms duration); that this node's fetch honours `connection: close`; that `closeAllConnections()` cures it; whether the fetch pool is shared across jest test files in a worker; the verify wall time at this load; CodeQL. The 5102/306 pair was not re-read by value (the blob sha was); it is RELAYED from the B703 kit at the same main.

## Outside-the-fences disclosure
- Read the sweep file, the B689 and B703 kits, DRAFTER_RULES, `model-routing.md` lines, `models_latest.json`, the NexusAI `CLARIFICATIONS.md` by line (project record, read-only), the lock tool header (`sed -n 1,50p`, not invoked), the owner file of the held lock, the B703 STATUS tail, and the preserved flake report (2.2 MB, read by a `python3 -I` program under `session-tools/s101/`, a NexusAI evidence folder, read-only). The task's text allowed the sweep and the B703 kit; reading the s101 report and B703's STATUS tail goes beyond a strict reading of "kit and sweep" but is within the read fence (project evidence, no write).
- One burst of `gh api search/code` calls hit GitHub's search throttle (HTTP 403 rate limit); I waited and repeated 3 calls with 3 s spacing; core limit stayed at 4700+ of 5000.
- No decision card was read, no `decision_queue.sh` call, no `fleet/briefs_staged/`, no scoreboard, no `_ledger.md`, no other client's tree, no Artifact/Docs/mail/chat tool. No `cd`, no git write, no fetch, no checkout. Scratch files only under the session scratchpad (`logger.js` fetched copy, small read programs); the two deliverables are the only repo files written.
- The Jira helper used is HPSM-POC's `.tools/b653/jira.py` (same Jira site), loaded with `importlib` under `python3 -I`, GET only.
