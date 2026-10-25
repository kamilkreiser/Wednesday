STARTABLE: YES (after your stamp; re-check at the stamp: main still `8ae0a87f`, the lock-tool hash, and whether the B702 branch exists, which would join the path-intersection print)

# B703 drafter report (NexusAI lane N-COUNTS), drafted 2026-10-25 23:2x-23:5x AEDT

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-25_B703_SEAT-M13_nexusai-counts-882-850-854-843.md` (140 lines). Seat `Datasec/NexusAI-M13`, ports 9690-9699, model C2 Sonnet `claude-sonnet-5-5`, launch carries `BRIEF_SEAT_LEVEL=sonnet` and `WED_USAGE_STOP=100`. Gate after: G2 tier 2 (Q-1).

## BLUF
- All six tickets are in (RD-882, RD-850, RD-851, RD-852, RD-854, RD-843): each is `To Do` by Jira GET, still unfixed in the file at main `8ae0a87f` by reading the code, test/test-helper only, no word on any screen, no production touch, no ruling needed. None dropped. Two carry a conditional rule inside the kit (RD-854 drops itself if the packer's list cannot be re-read at source; RD-851 prefers the opaque-token fix and falls back to narrowing the wording only under a stated rule).
- Shape: ONE branch, SEVEN commits (six tickets in the sweep's order, then the counts file as its own last commit, regenerated once by `--update-counts` on the final tree, never hand-edited). This follows the project's own prior art (B642 and B650 regenerated last; C-57, C-89). Intermediate commits are not verify-green by design; CI judges the head and the landing is one merge commit.
- The cells ADD tests, so `tests` moves from 5102 (suites stay 306; a new test file is forbidden). The seat measures per-file deltas and must show the regenerated figure equals 5102 plus the deltas, or STOP.
- Landing rule quoted with source: `CLARIFICATIONS.md:2067` (merge path, "Never squash, never rebase"), `:2068`, `:2073`, `:2076`, C-68 `:665`, C-209 `:2270`; counts rules C-57 `:418` and C-89 `:835`.

## Facts re-measured (instrument, control)
| Fact | Reading | Instrument | Control |
|---|---|---|---|
| main | `8ae0a87f564b72fc1f9082cd89013740e7162d58` (PR #116 merge commit, 2 parents) | `git ls-remote` + `pulls/116` (`merged` true, `merge_commit_sha` = main) | same call lists the branches compared |
| open PRs | 0 | `pulls?state=open` length | `pulls/112/files` lists the 3 files incl. the counts file |
| branches vs main | b617, b632, b642, b658, b689, records/b362, b605, b656, b681 all ahead 0, 0 files; no `b703*` | `compare/main...<branch>` | `19b7106b...6e076b29` lists 6 files |
| path moves since the B689 draft | `dbbf5881...8ae0a87f` = HISTORY.md (via #115) + the rd490 test + the guard (via #116); the counts file NOT moved | `compare` files | 3 files listed, nonzero |
| counts file | blob `a8085c1d`, tests 5102, suites 306, `_updated` 2026-10-25T00:11:44Z | contents GET raw | same blob the B689 kit recorded |
| suites census | 306 depth-1 `__tests__/*.test.js` files = the file's `suites` | tree GET with a regex | equals 306, so the arithmetic that a new file moves `suites` is grounded |
| six path blobs | rd777 `2b3a0602`, helper `c2ac36fd` (13497 B), rd848 `685656c2`, rd618 `10d3a6be`, validators `37ff4001`, readers `Dockerfile f0367f12`, `.dockerignore 3e45ec51`, `image-manifest 2040ca2e`, `rd395 harness c826c1ea`, `cspReport 0c5657d4` | tree GET | the helper's blob recomputed over the fetched bytes (`printf 'blob n\0' ... shasum -a 1`) = `c2ac36fd` |
| tickets | all six `To Do`, 0 comments each | Jira GET via the HPSM-POC read helper (read whole first) | `project = RD AND ( text ~ "zzz-no-such-7f3a" )` = 0 |
| each still open in code | rd777 has no TAB/LF/CR row, no two-whitespace-after-`<` row, `nest(k)` NESTED family starts at 3; helper `:214` keys chown as text; no cell for `:101-106`, `:125`, `:133`; rd618 `:191` filter present; live Dockerfile has 0 `COPY --chown` | file reads by line | pattern fires on a scratch `COPY --chown=1:1 a b` (1) |
| RD-882 product lines | `validators.js:175`, `:219`, `:251` match the three mutant diffs M35, M36, M39 (exist in `B667_evidence/mutants/`) | file reads | diffs read and compared by eye to the lines |
| RD-854 packer list | `common_vcs_ignore_list = {'.git', '.gitignore', '.bzr', 'bzrignore', '.hg', '.hgignore', '.svn'}` by basename, `_archive_utils.py:67,74`; `.venv` dirs separate (`:70`) | one `gh api -X GET` of the public file at tag `azure-cli-2.90.0` | the tag ref resolves; code search for the name finds this file and its containerapp sibling only |
| verify predicate | `build.yml:83-84` `npm run verify -- --maxWorkers=2`; `verify-suite.sh:87-92`, `:358-360` fail in either direction | file reads at main | B642/B650/B667 STATUS record the same pair printed |
| Deploy demo | main's own push run `skipped`; variables `total_count` 0 | `actions/runs?head_sha=` (query in the URL; a `-f` form returned an error, noted), `actions/variables` | other runs in the same list show real conclusions |
| names | highest real NexusAI builder is M11 (B689); `M99` occurs only as a control sentence; M12 reserved for B702 | scan over the 10-24/10-25 non-`.pre-` SEAT kits | scratch `x NexusAI-M99 y` matches once |
| panes | live: tuesday, Datasec/MPS-G131, Datasec/Security-Composer-G130, fleet-monitor; no NexusAI | `tmux list-panes -a` | n/a |
| ports 9690-9699 | `lsof` rc 1 (nothing); kit-text hits are range prose ending `9699` or scan sentences (B607, B608, B609, B612, B619, B667, B673), none an assignment | `lsof` (PATH one; `/usr/bin/lsof` absent), word-boundary scan | python listener on 9691 listed, then freed; scratch `x 9690 y` matches once |
| lock tool | sha256 `3c33f5ae...a792` (same as B689), `queue-jest/` empty | `shasum`, `ls -la` | the kit makes the Stamp's value govern (B702 may change it) |
| load | 3.16 at 23:50 | `uptime` | n/a |
| model | row C2 `model-routing.md:92`; C3 `:93` explicitly considered and NOT applicable; G2 `:109`; id `claude-sonnet-5-5` (`models_latest.json` sonnet level) | file reads | n/a |

## D-decisions (drafter)
- D1 One branch, seven commits, counts last. Alternative (six PRs or a counts commit per ticket) rejected: the counts file would conflict on every PR after the first (C-57), and a per-commit regeneration costs about 25-30 min of verify each. Cost accepted: intermediate commits are verify-red; mitigated by per-file jest proof per commit and by the head verify.
- D2 Counts figure is proved by arithmetic (5102 plus per-file deltas) AND by the regenerating run; a mismatch is a STOP naming the file that moved. Plain verify at the committed head follows, with C-89 checks.
- D3 RD-850: normalise-and-resolve with a THROW on any unresolvable owner (ticket's fix shape), `node` = 1000 flagged an assumption; `--chmod` left keyed as text (the ticket's cells ask for ownership only).
- D4 RD-851: prefer the opaque-token form, with the existing precondition cell (`rd848:52-66`) as the hard constraint; fallback to the narrowed wording only if red-first cannot satisfy both.
- D5 RD-852 needs a temporary git repo for HM-7: the kit pins the construction (mkdtemp, literal execFileSync args, finally-cleanup) and names the CodeQL rules to pre-scan.
- D6 RD-854: the kit makes the seat re-read the packer line and DROPS the ticket if it cannot, rather than guessing; `.venv` left out.
- D7 RD-882 validators mutants are applied to the clone's `backend/validators.js` TEMPORARILY and restored by `git show HEAD:<path>` plus hash (the standing rule forbids `checkout --`); `backend/**` must be byte-identical at the commit. No product edit.
- D8 If jest is not startable, no counts commit is written (an unmeasured figure is never committed).
- D9 Time guidance: target READY 5 h, HARD STOP 8 h from the Step-0 date (about 14 lock tickets and two full verifies); Tuesday may tighten.

## Q-questions for Tuesday (each with a default)
- Q-1 Gate tier: G2 tier 2 (Sonnet) is the default (tests-only; the validators mechanism was measured by an earlier tier-1 gate). Because the RD-882 cells sit on a security filter, you may stamp tier 1. Default: tier 2.
- Q-2 The kit allows ONE GET of the public azure-cli source (RD-854 only) beyond STANDING LINE 2's usual outbound list, via the project's gh config. Default: allowed.
- Q-3 Order against B702 (N-LOCK, NexusAI-M12): disjoint paths, so they may run together; if B702 lands first and changes `nexusai-lock.sh`, the Stamp's lock hash governs (the kit says so). Default: run in parallel.
- Q-4 N-LOGSAFE (RD-849) waits for this lane to LAND (counts file). Default: launch it only after this PR merges.

## UNMEASURED
No npm, jest, clone, fetch, worktree, browser, CodeQL or workflow was run. The rd848 and rd618 per-file test counts (so the final `tests` figure) are the seat's to measure; the helper and cspReport mutants are described, not run; whether the opaque-token form keeps the precondition cell true; the `node` = 1000 assumption; the main `Build` run at `8ae0a87f` was still in progress at 23:5x; the `Deploy demo` `paths-ignore` reading for this change.

## Outside-the-fences disclosure
Read-only everywhere except the two output files. Two `Write`s (kit, report) and one `Edit` of the kit. One scratch directory under the session scratchpad holds fetched copies of main's files and the Jira dump (outside the project). Port control: a 4-second python listener on 127.0.0.1:9691, freed. One `gh api -X GET` of the public file `Azure/azure-cli` at tag `azure-cli-2.90.0` (third-party public source, GET only, under NexusAI's gh config). Jira reads through the HPSM-POC helper (credentials read in-process, never printed; two JQL, both with parentheses). A first `lsof` call used `/usr/bin/lsof`, which does not exist (rc 127), then the PATH `lsof`. No `cd`, no `decision_queue.sh`, no Wednesday/Friday trees, no briefs_staged, no scoreboard, no `_ledger.md`, no hosted-host HTTP, no mail/chat/Artifact/Docs tool. The kit text carries no person's name and no decision-card id (checked by grep; `kam`, `wednesday`, `friday` 0 hits; the 9-line slot count reads 9).
