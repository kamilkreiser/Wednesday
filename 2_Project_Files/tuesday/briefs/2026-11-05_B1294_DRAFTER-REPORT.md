STARTABLE: YES once Tuesday fills the seven Stamp slots plus the last line (slots file 2026-11-05_B1294_slots.json) and re-reads main, open PRs and the deploy switch; no pane, branch or PR blocks it.

## BLUF
1. Kit B1294, seat N100: 78 lines (long lines), 8 four-underscore lines (seven slots plus the last line), 0 at-sign tokens. B1294 and N100 were unused.
2. Build: new branch `b1294/nexusai-rd916-jest-entry-and-plugin-resolve` off main `4da06e8e`; new test `__tests__/rd916-jest-default-entry-and-plugin-resolve.test.js` with two cells (E1 default entry holds a hoisted mock; P1 the plugin loads in a child node process whose cwd is a temp dir outside the repo); the jest block moves to a new `jest.config.js` ONLY if measured to be required; counts regenerated once.
3. The sweep's open point (does jest refuse a jest.config.js beside a `jest` key) is made a MEASURE-FIRST step in a probe tree, with a control; so are three more (is the move required, who else reads the key, rootDir equality by `--showConfig`).
4. Red-first order is in the probe (P1 red before the move, green after), plants PL1 (drop default entry -> E1 red) and PL2 (bare string again -> P1 red "Cannot find module"), plus a control plant.
5. Counts rule: expected pair = 5312 + tests the new file runs / 318 (a NEW file adds one suite, unlike B1278's same-file cell); exactly THREE changed lines in the counts file; one `--update-counts`, via the lock.
6. Sonnet, row C2 (`model-routing.md:92`), id `claude-sonnet-5-5` (`models_latest.json:23`), launch line carries `BRIEF_SEAT_LEVEL=sonnet`; target READY 90 / hard stop 120; ports 9890-9899, none typed.

## Facts re-measured (instrument | result | control)
| fact | instrument | result | control |
|---|---|---|---|
| main | `gh api -X GET branches/main`; `ls-remote` of the shared checkout | `4da06e8eba86ed7c2a4bd085e124448db79dab0c` (06:05) | both agree; local checkout HEAD is `cd2b5439`, stale (`cat-file` of 4da06e8e fails there), so everything was read from origin |
| open PRs, switch | `pulls?state=open` length; `actions/variables` total_count | 0; 0 | `pulls?state=all&per_page=3` lists #168 #167 #166 closed |
| branches | `git/matching-refs/heads/b1` | b1183, b1215, b1238, b1278; no b1294 | the four listed |
| config files absent | `git/trees/4da06e8e?recursive=1`, truncated=false, 1025 | `^(jest.config|babel.config|.babelrc)` 0 hits; `rd916` 0 hits | `rd917` 1 hit at line 463 |
| package.json | raw `contents?ref=`, `awk NR==`, 126 lines | `"jest": {` :97, plugin string :115, default entry :119, block ends :125; jest ^29.7.0 :78; plugin ^7.29.7 :73; archiver ^8.0.0 :51; test :25, verify :26; lint is a placeholder | each line printed its quoted text |
| counts | raw file | tests 5312 :4, suites 317 :5, `_updated` 2026-11-04T05:16:08.009Z :3 | `_why` :2 carries the regenerate rule |
| RD-916 | `b774lib.py` `issue`, `comments`, `search` (GET) | To Do, Low, 0 comments, 0 links, updated 2026-11-02T03:57:14+11:00; done-when and recommendation quoted verbatim in the kit | `RD-99999999` 404; `( key = RD-916 )` 1; `zzqxnonexist` 0 |
| RD-918 | same | To Do; part (a) edits root package.json: serial | same controls |
| records | `grep -n` / `awk NR==` on CLARIFICATIONS.md | C-234 at :2492 (the counts file "released to the queued changes RD-902 then RD-916, in that order", :2494), C-236 at :2508, C-237 at :2516; RD-916 "not started"/"not touched" in each; landing rule :2067, C-190 :2062, ADDENDUM :2080 | file is 2521 lines; each printed |
| CI predicate | raw `build.yml`, `verify-suite.sh` | `build.yml:83` name, `:84` `npm run verify -- --maxWorkers=2`; `verify-suite.sh:170` `cd "$(dirname "$0")/.."`, :349 SHRANK, :360 stale, :366 PASS | numbers identical to B1284's |
| other readers of the jest key | `grep -i` on raw Dockerfile, `.dockerignore`, `verify-suite.sh`, `build.yml` | no read of the key in these four (jest only as the runner in verify-suite and build.yml) | `package.json` hits in the Dockerfile/.dockerignore (positive) |
| model row | `awk NR==` model-routing.md; models_latest.json | C2 :92, C3 :93, G2 :109; sonnet id :23 | `grep -n sonnet` printed :22, :23 |
| ports 9890-9899 | `lsof -nP -iTCP:9890-9899 -sTCP:LISTEN \| wc -l`; word-boundary `grep -w -E 989[0-9]` over 45 non-`.pre-` SEAT kits of 4-5 Nov | 0 listeners; 0 files | `lsof` :7000 shows 3 lines; `985[0-9]` hits 2 files; 987x 1, 988x 1, 991x 1 so those were avoided |
| names | whole-word `grep -i` of N100/B1294 over briefs `.md`/`.json` | 0 each | `N99`: 11 files |
| panes, load | `tmux list-panes -a`, `uptime` 06:07 | tuesday, fleet-monitor; load 1.81 | n/a |
| kit slots | `/usr/bin/grep -c -E '_''_''_''_'` | 8; `@[A-Z]+@` 0; slots.json 8 keys | unstamped copy prints 8 as the REFUSE line says |

## D-decisions
- D-1: ONE commit by default; two only if each is green at its own head (a red-first commit is measured in the probe, never committed red).
- D-2: P1 is a child `node` process with `cwd` a fresh temp directory and `@babel/core` `transformSync` on one real ES module with the config's own plugin list, not a nested jest run (cheap, deterministic, fails with "Cannot find module" exactly as the ticket describes). The true end-to-end jest run from outside the root is done once by hand (D5), not committed.
- D-3: the config move is in scope because JSON cannot hold `require.resolve`; the kit still makes the seat measure that `<rootDir>` in plugin options does not work and STOPs if package.json alone would suffice (the ticket recommends the move, so that is Tuesday's call).
- D-4: closed list of paths stated as a property first, then "at least" the four paths.
- D-5: suites arithmetic is +1 (new file), so expected pair is 5312 + N / 318 and THREE lines change in the counts file (B1278 had two); N is read from jest's own JSON for the file, not guessed.
- D-6: the "leave it" branch is not taken and the kit says the seat never records a decision.
- D-7: the kit forbids a Jira write, a PR and a deploy; E1 is the ticket's own shape (require above jest.mock, red by removing the default entry).

## Q-questions for Tuesday (each with a default)
- Q-1: hard stop 120 / target 90 (the brief gave only 90). Default: accept.
- Q-2: ports 9890-9899. Default: accept.
- Q-3: gate tier after this kit (G2 `:109`, config and tests). Default: Sonnet-tier gate, Opus not required; the config move touches no auth surface.
- Q-4: the class/round for the gate: this is a new class (no earlier verdict names RD-916; not read from verdict lines by me). Default: round 1 of 2 on a new class, Tuesday confirms from the verdict lines.
- Q-5: the seat may add a second commit splitting cell and config. Default: one commit.

## UNMEASURED
- Whether jest 29.7 refuses `jest.config.js` beside a `jest` key (known from jest's behaviour, not run; the seat measures with a control). Whether `<rootDir>` is unsubstituted inside transform options (same). No jest, node or npm was run by me.
- Whether any test or script outside the four files I read reads the `jest` key (the repository code search returned nothing before and I did not grep a checkout; the stale local checkout lacks the base commit). The seat greps and STOPs on a hit.
- Which ES-module file from the five packages the child should transform (the seat prints its choice); that P1 runs under 5 s; whether `--runTestsByPath` from a foreign cwd works with `--config`.
- No decision card was read (none cites or is known to cite RD-916; "the product owner has chosen to leave it" is UNMEASURED).
- Hosted CodeQL, Build, Gitleaks and node 24 on Linux; gauge. Any branch that edits the `package.json` jest block or the counts file (61 stale branches edit the counts file per B1284; not re-censused).

## Outside the fences
- Jira GET only via `b774lib.py` (`issue`, `comments`, `search`, and `get` for the 404 control), a scratch script in the session scratchpad `b1294/`; `gh api -X GET` under the NexusAI `.gh-config` for branches, pulls, variables, matching-refs, the tree, and raw contents of five files (saved in the scratchpad); one `git ls-remote` and read verbs (`cat-file`, `rev-parse`) on the shared checkout; `tmux list-panes`, `lsof`, `uptime`. No write outside the three output files and the scratchpad. First Bash call was refused by the `cd` hook (a `cd` was typed in an `ls`); re-issued without it. Two advisory notices about case-sensitive multi-word greps arrived after the fact; every count in this report that matters was paired with a control above.
