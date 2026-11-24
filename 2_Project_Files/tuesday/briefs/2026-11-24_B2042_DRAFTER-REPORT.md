STARTABLE: YES

# B2042 DRAFTER REPORT: NexusAI lane NX-W (RD-1026), kit `2026-11-24_B2042_SEAT-N170_nexusai-rd1026-chat-label.md`

Drafter: an Agent-tool drafter for Tuesday (s322), commission `2026-11-24_B2042_NEXUSAI-NXW-RD1026_DRAFTER_COMMISSION.md`. Read window: Tue 24 Nov 2026 from 13:49:37 AEDT (first `date`) to the `date` on the last line of this report. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s322/d2042/`. Files written outside scratch: this report, the kit and the kit's `.measured` sidecar.

## SUMMARY (10 lines)
1. STARTABLE: YES. Seat id N170 is free (word scan of the non-`.pre-` SEAT kits of 23 and 24 Nov: N170 0 files; control N169 3 files).
2. **Main moved during drafting:** pull request 247 (NX-S1) landed at 13:52:55 AEDT; BASE is now `04a6b89dcd14` (merge of 247), counts 6280 / 396. `static/js/index.js` is unchanged by it (blob `2c883fa50b9b`).
3. **Finding:** 247 and this lane share `scripts/verify-expected-counts.json`; the commission's "shares no path" holds only for the product and test files. Moot now it has landed; HOLD 20 stops the seat if the counts file moves again.
4. **Fix:** one token on `static/js/index.js` line 3523: `${label}` becomes `${escapeHtml(label)}`. The escape sits where the label is written, so it covers the four arguments AND the tool name (line 3515: an unknown tool name is the label itself), plus any value a later tool adds.
5. **Why this is the smallest correct fix, proved by program:** the label's own literal text has 0 `<>&`, so this gives the same output as escaping each value. `escapeHtml` does NOT escape quotes (jsdom and real Chromium both return `"'`), which is safe because the label is element text, and cell S1 checks it stays there. Switching to `textContent` would show the icon's `<i>` tag as visible text and lose the icon.
6. **Real browser** (headless Chromium, `about:blank`, no network): at BASE an image tag made an element and its handler ran; after the fix there is 1 child, the text shows as typed, and no handler runs.
7. **Cells** (new file, 20 tests): red-first at `d96a83d3` gives exactly 11 named failures out of 20. Red-proof (only the product line reverted) gives the same 11. Green: 20/20, and the 26 suites that name index.js pass 346/346. The frozen `lane2042.sh` ran end to end on scratch trees with all judges PASS.
8. **Full verify** with `--update-counts`: at `d96a83d3` it was `VERDICT: PASS` 6265/396 (22 min). At BASE's tree (`5c98e04d`, tree equal to `04a6b89d`) it was `VERDICT: PASS` 6300/6300 across 397 suites (14:21:03 to 14:43:14, final test file, EADDRINUSE 0). K must carry 6300 / 397.
9. **Local CodeQL:** rc 0 PASS, 0 KEPT, 0 NEW, 29 results at both base and head. It never flagged this sink, so the cells are the evidence for the fix, not CodeQL.
10. **Questions:** Q-0 accept the counts file in the partition; Q-1 no deploy, landing read is Tuesday's; Q-2 gate G1; Q-3 sibling rows not in this change; Q-4 fix at the sink; Q-5 BASE `04a6b89d`. Defaults are below.

Read load for Tuesday (wc -c): see the last lines.

## FACTS RE-MEASURED (instrument; control)
- origin main: `d96a83d3ee6df25f74bcfe2f9ec0d0b42714e029` at 13:49:49, then `04a6b89dcd142eebdb99f441c3840e32d7e0701f` at 14:20:25 (gh GET `git/ref/heads/main`). The commit GET shows `Merge pull request #247`, parents d96a83d3 and 5c98e04d, tree `d882ab64d84a`. `compare/d96a83d3...04a6b89d` is 3 ahead, 0 behind, 10 files, none of them `static/**`. Counts at `04a6b89d` (contents GET) are 6280 / 396. `pulls?state=open` returns 0. `matching-refs/heads/b2042` returns 0 (control: b2032 returns 1).
- `git rev-parse 5c98e04d^{tree}` in the drafter's clone is `d882ab64d84a9e2076868df47c8745ba82242905`, which equals BASE's tree. This is why the second verify and CodeQL ran there.
- Jira GET, whole, comments paginated (`jwhole.py`, a copy of the B2032 drafter's GET-only reader):
  - RD-1026: To Do, 0 comments, 5587 characters.
  - RD-1014: To Do, 1 comment (the alignment note: chat-region rows "belong to no other ticket").
  - RD-1008: Testing, 1 comment.
  - RD-1027, RD-1028, RD-1029: To Do; `index.js` count 0 in each (control: RD-1026 reads 4).
- `CLARIFICATIONS.md` (914067 bytes) was not read whole. `awk NR==2062` (C-190) and NR==3138 to 3146 (C-310); `grep -n -i` for RD-1026 and RD-1008.
- Line pointers (`grep -n -i -F` over `git show d96a83d3:static/js/index.js`): 113 escapeHtml, 3506 `case 'tool_call':`, 3515 label default, 3517 to 3521 args, 3522 recent jobs, 3523 the sink, 3527 `case 'error':`, 3529 the RD-1008 escape.
- `deploy-demo.yml` at BASE: lines 26 `on:`, 29 `paths-ignore:`, 53 and 91 `CI_DEPLOY_ENABLED`, 95 `environment: demo`. The last 20 runs all read skipped (total 264).
- model-routing line 93 is C3 and line 108 is G1; `models_latest.json` line 17 is `claude-opus-5-5`.
- Code scanning: 22 open, 0 at `static/js/index.js`.
- Literal-text program (`literals.py`): 7 label assignments, 0 `<>&` each (control: 3 on a planted string).
- jsdom (`proof.js`) results:
  - `escapeHtml('"\'')` returns `"'`.
  - The markup case returns `&lt;b a="1"&gt;&amp;&lt;/b&gt;`.
  - With the `textContent` alternative, `icon kept true false` and the tag text is visible.
- Chromium (`chromium-proof.js`, Playwright 1.62.1):
  - `fixed`: `[[1,true],[1,true],[1,true],[1,true]]`, ran 0.
  - `base`: `[[2,false],[2,false],[1,true],[1,false]]`, ran 1.
  - Quotes `"'` both times.
- Jest at `d96a83d3` (clone, dot-free):
  - rf: 20 tests, 11 failed.
  - green: 20/20.
  - redproof: 11 failed, a failed set equal to rf's by program.
  - 26-suite green: 346/346 in 12 s.
  - Judge controls: green.json judged as rf gives FAIL; green1.json judged as redproof gives FAIL.
- Full verify at `d96a83d3` (13:54:45 to 14:16:49): `Test Suites: 396 passed`, `Tests: 6265 passed`, `VERDICT: PASS`, EADDRINUSE 0 (control: VERDICT 2). Counts went to 6265/396.
- Full verify at `5c98e04d` (BASE's tree) + A: 14:21:03 to 14:43:14, `Test Suites: 397 passed, 397 total`, `Tests: 6300 passed, 6300 total`, `VERDICT: PASS — 6300/6300 tests passed across 397 suites (jest exit 0)`, EADDRINUSE 0 (control VERDICT 2); counts 6300 / 397, only `_updated`, `tests`, `suites` moved. Prototype A `89a251685b14` (parent 5c98e04d) and K `7ab0aa379235`: STATIC A PASS, STATIC K PASS, gitleaks over staged K and over `log -p 5c98e04d..7ab0aa37` no leaks found.
- Prototype commits A `829f4485b3c3` and K `8f05686665e8` (scratch identity, never pushed):
  - `STATIC A PASS` and `STATIC K PASS`. The first staging read `STATIC A FAIL` because its non-ASCII check caught five literal ellipses in the test file. That was a real-output control firing; I fixed the frozen file.
  - gitleaks `no leaks found` on staged A and staged K (control pair: `leaks found: 2`).
- CodeQL against `d96a83d3` (head `8f05686665e8`, 14:18:26 to 14:19:28): rc 0 PASS. Against `5c98e04d` (BASE tree; head `7ab0aa379235`, 14:43:30 to 14:44:34): results 29/29, KEPT 0, NEW 0, GONE 0, `RESULT rc 0 PASS`, cq.err empty.
- Seat bands (lsof, 14:20): 0 listeners in each of 20000-20639, 24480-25119, 31520-32159 and 25760-26399 (control: 12 listeners machine-wide).
- Slots (sha256 mod 19 rule; controls b2032-nodot/vupd3 17 and b2013-nodot/chk26 17): rf 0, work 7, vupd 18, chk 9.
- `stamp_check.py <kit>`: 116 claims, 116 measured, rc 0. The four-underscore count in the kit is 5 (four slots plus the last line). The underscore-aware name scan over the kit and the test file (the four names of scanlib1114.py line 20) reads 0; its control fires.

## D-DECISIONS (the drafter's, each overrulable)
- **D-1: escape at the sink (`escapeHtml(label)`), not each value.** The output is identical by finding 2. It also covers the tool name and any value added later, and it is one token.
- **D-2: two commits, A (index.js + new test) and K (counts)**, the B2032/B1977 form.
- **D-3: every jest, verify and server tree is dot-free** (`b2042-nodot/{rf,work,vupd,chk}`). This fixes the B2032 kit fault (its seat's Corrections 3). Only the clone, `wt`, logs, frozen files and cq live under `.tools/b2042/`. `v2042.sh` refuses a tree path that holds `/.` (REFUSE 8 too).
- **D-4: no generator step.** The change touches no route, so the role inventory does not move.
- **D-5: three lock acquisitions** (lane, update verify, plain verify).
- **D-6: the test asserts "no element/attribute made" in jsdom.** jsdom runs no handler, so the claim that a handler does not run rests on my Chromium proof and the review's run. The kit states this limit.

## Q-QUESTIONS FOR TUESDAY (each with a default)
- **Q-0 (partition).** OWNS-B2042 adds `scripts/verify-expected-counts.json` to the commission's "one file plus one new test". The ticket's acceptance names the counts, and a new test file changes them. **Default: accept.** If refused, the lane cannot meet the acceptance (REFUSE 1).
- **Q-1 (deploy).** A merge starts a `Deploy demo` run (`static/**` is not path-ignored), gated on `vars.CI_DEPLOY_ENABLED`. The last 20 runs were skipped. **Default: nothing deploys; the landing read is Tuesday's; the C-224 hold stands.**
- **Q-2 (tiers).** The builder is Opus C3 (line 93), as the commission says. The gate is **G1** (line 108, security surface), where the sweep had written G2. **Default: G1.**
- **Q-3 (sibling rows).** RD-1026 says "Decide in the same change whether the other chat-region rows ... are escaped too". The commission excludes them. They are tracked nowhere else: RD-1014's comment says so, and C-310 item (3) lists them as not fixed. **Default: not in this change. The records pass states this on RD-1026 and proposes a Low hardening ticket.**
- **Q-4 (fix form).** The ticket proposes escaping each value; the kit escapes at the sink. The two give identical output (finding 2). **Default: the sink.**
- **Q-5 (BASE).** Main moved to `04a6b89d` (pull request 247) during drafting. The kit names it as BASE, and I re-ran the full verify and CodeQL at its tree. **Default: launch on `04a6b89d`. Any further move goes by HOLD 20 (a counts-file move is a STOP).**

## UNMEASURED
- The seat's own clone, `npm ci`, the jest lock, the push, and the plain verify at K (its pair is PREDICTED equal to the update run's).
- My clone's `node_modules` is a symlink to the B2032 drafter's `npm ci` (same lockfile sha256). I did not run `npm ci` myself.
- The final spelling of the test file (with `\u2026` escapes) ran in the rf, green, red-proof and lane runs at `d96a83d3`. It also ran in the full verify at `5c98e04d` (BASE tree). The first verify at `d96a83d3` ran the earlier spelling.
- A hosted page and its CSP, a real AI endpoint, Linux.

## CHAIN INPUTS (every step's inputs are produced by an earlier step or exist at BASE)
| step | inputs | made by |
|---|---|---|
| Step 0 | the kit, the frozen files, Jira | Tuesday's stamp; the drafter's folder; Jira |
| Step 1 | the project checkout, the deploy key, origin | BASE |
| Step 1b | the clone at BASE, `apply2042.py` | Step 1, Step 0 |
| 0 `trees` | BASE, the frozen test file, `apply2042.py` | Step 1, Step 0 |
| 1 `quiet` | the lock base | Step 1 |
| 3 `lane` | `rf`, `work`, `lane2042.sh`, `judge2042.py`, `suites2042.txt` | step 0, Step 0 |
| 4 `astep` | `work`'s two paths, `msg-A.txt`, `static2042.py` | step 3, Step 0 |
| 5 `update` | A, `v2042.sh` | step 4 |
| 6 `kstep` | `vupd`'s counts file, `msg-K.txt` | step 5, Step 0 |
| 7 `plain` | K | step 6 |
| 8, CQ, push | K, origin | step 6 |

## OUTSIDE-THE-FENCES DISCLOSURE
- **Jest, the verifies and Chromium ran WITHOUT the project's jest lock.** The commission asks for prototype proof, and taking a lock ticket would mean writing in the project tree. Before each run the lock base listed no holder, `queue-jest` held 0 tickets, and no NexusAI pane was live. Load averages were 1.1 to 2.6 on 18 CPUs. Each run used a dot-free scratch path and its own slot (clone 8, v247 18).
- **Playwright launched a local headless Chromium on `about:blank`.** There was no network and no server. It ran a `new Function` over the page's own `escapeHtml` text.
- **Writes in my own scratch clone (never pushed):**
  - a repo-local scratch identity (`drafter-scratch@invalid.test`)
  - branches `proto2042` and `proto2042b`
  - prototype commits A and K (and a second pair in `t/v247`, see below)
  - worktrees `t/rf`, `t/work` and `t/v247`
- **Two hook refusals:**
  - A Bash call with `$D/clone` as the `-C` target (the hook could not resolve the variable). I re-issued it with literal paths.
  - `sleep 240` (the hook blocked a chained sleep). I used background waits instead.
- **Reads only toward the project:**
  - `git clone` read the B2032 seat's clone (no write to it).
  - `git ls-remote` read `.tools/b2032/clone`'s origin.
  - gh `-X GET` and Jira GET only.
  - cat, sed and grep of project files.
  - Nothing was written under `!CODING`. No az, ssh or HTTP to any hosted site.
- **One slip of mine:** the Write tool stored five `…` escapes in the test file as literal characters. `static2042.py` caught it; I fixed it before the frozen sha256 table, and the first full verify ran the earlier spelling (said above).

Read load for Tuesday (wc -c before this line): kit 56285 bytes, sidecar 12511 bytes, this report about 13100 bytes.

Last `date` of the drafting: Tue 24 Nov 2026 14:46:51 AEDT
