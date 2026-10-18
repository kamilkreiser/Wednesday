# Gate 27 kit: DRAFTER REPORT (2026-10-18, from 21:34:00 AEDT; read-only drafter, Opus 5.5)

**BLUF:** The kit for **gate 27** is drafted: routing name `QA/NexusAI-gate27`, tags `qa-g27-*`. It is a TIER-1 gate of RD-778 (`3047ae9`, 8 `js/xss-through-dom` sites) with a **browser leg**, re-pinned onto main AFTER gate 25's lands.
- **Not launchable as written, by design.** At 21:41:46 AEDT main was still `c7ca0ed`, so the MAIN pin and the merge row are `@SLOT@`s. T0 picks the re-pin mode.
- **Four corrections to the commission (details in the next section):**
  - The landing ids `f4ae63b` / `559dcec` are gate 25's store commits. What lands is `36a0dc0` / `2facd7c`, so match them by tree.
  - "Open xss count on the PR head = 0" cannot prove the alerts closed (C-209, measured).
  - The pages load Bootstrap from a CDN, which the 127.0.0.1-only browser rule would block.
  - Four of the eight sources sit in the DOM, not in a form field.
- **No launcher was written.** You asked for exactly two files.

## Files
- Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-18_nexusai-gate27-rd778-xss.md` (241 lines; sha256 `8596111b3ea915ea55b82a34c0e44d47947538e1659b6e9ff084fdc199a6da8c`, taken after the two line-reference corrections; re-hash at stamp).
- This report.
- Scratch only (session scratchpad, not the project): `rd.sh` (a bash `git show` wrapper), the inbox JSON, the two message JSONs, `ready778.txt`, the path lists, and `mt-legacy.txt`.

## What I read (whole unless noted)
- Gate 25 kit (231 lines) and gate 26 kit (233). Gate 26 DRAFTER-REPORT (81). `BRIEF_TEMPLATE.md` (179).
- Gate 21 kit, lines :74, :223, :322 only (the browser driver). `fleet/briefs_staged/2026-10-04_qa_batch13_browser_driver_answer.md` (12).
- Tuesday's `2026-10-18_S101O_ANSWER-16_gate25-landing-stacked.md`.
- From AgentMail (GET of `tuesday-agent@`): the RD-778 READY (2026-10-18T10:18:10Z) and Tuesday's ANSWER-12 (05:31:40Z).
- In the NexusAI repo:
  - commit `3047ae9`: message, full product diff, test file :1-:84 and its cell list;
  - helper and source lines in all five scripts; server.js `/api/chat` (:7121-:7230, filtered);
  - `local-date.js` humanSpan; the five pages' CDN tags; lockfile JSON; deploy-demo lines.
- CLARIFICATIONS head lines: C-02, C-40, C-57, C-63, C-76, C-133, C-190, C-209 (whole), and the C-209..C-217 index.
- S88Q census rows 22-30.
- Gate 25 report: line 3, the last six lines, `classifier-stops.txt`. Gate 26 report: line 3.
- Builder evidence, method only: cells JSON summaries, `rd778-render-identity.out`, `own-install-rd778.out`, the verify log tail.

## Facts, each with its source
| # | fact | source (command / file:line) | when |
|---|---|---|---|
| 1 | main `c7ca0ed7113750b268028f12e8659bf1e3d34282`; branch `3047ae92b4179adf5ae1bf6e1b60825af2e296e3` = `refs/pull/94/head` | `git ls-remote origin` rc 0, first attempt | 21:34:04 and 21:41:46 AEDT |
| 2 | 3047ae9: parent c7ca0ed, tree `932a907…`, ahead 1 / behind 0, 7 files (+350/−28) | `log -1 --format`, `rev-list --left-right --count`, `diff --name-status/--stat` | 21:34 |
| 3 | 3047ae9 is in NexusAI's object store, named by `refs/heads/rd-778-…` and `refs/remotes/origin/rd-778-…` | `cat-file -t`, `for-each-ref --contains` | 21:34 |
| 4 | PR #94: open, **draft**, head 3047ae9, base main @ c7ca0ed, mergeable, `mergeable_state unstable` | `gh api repos/datasecau/Reporting_Dashboard_Au/pulls/94` | ~21:35 |
| 5 | Check runs on the head: CodeQL, Analyze ×3, audit, scan all success; **Build in_progress** (run 39118735119) | `gh api …/commits/<sha>/check-runs`, `…/actions/runs?head_sha=` | 21:35:50 |
| 6 | Analyses on `refs/pull/94/head` for commit 3047ae9: js `1975466586` (results 0, rules 103, tool 2.27.2), python `1975463081`, actions `1975462924` | `gh api …/code-scanning/analyses?ref=refs/pull/94/head` | ~21:36 |
| 7 | Open alerts on the PR head: 0 of any rule. Fixed: 0. #28, #29 and #31 have no instance on the PR ref | `…/code-scanning/alerts?ref=refs/pull/94/head&state=open|fixed`, `…/alerts/{28,29,31}/instances?ref=` | ~21:37 |
| 8 | Open `js/xss-through-dom` on main @ c7ca0ed: #29-#36 at the 8 sites, plus #28 test-import.html:41. Warning / high | `…/alerts?ref=refs/heads/main&state=open` filtered | ~21:36 |
| 9 | Positive control: PR #58's head carries #256-#259 (fixed) | `…/alerts?ref=refs/pull/58/head` | ~21:40 |
| 10 | Main's js analysis `1972429266` on c7ca0ed (results 233) | `…/analyses?ref=refs/heads/main` | ~21:40 |
| 11 | C-209 text (quoted in the kit) | CLARIFICATIONS.md :2270 | ~21:38 |
| 12 | `codeql` CLI not installed | `which codeql` | ~21:38 |
| 13 | `f4ae63b` and `559dcec` are not objects in NexusAI. They are gate 25's own commits, named in its verdict lines | `cat-file -t` → "Not a valid object name"; gate 25 `report.md`, last lines | 21:38 |
| 14 | Seat's landing commits: 36a0dc0 (tree fb8197a) and 2facd7c (tree e2bb3ac). ANSWER-16 says "the tree equality is the check" | `rev-parse <c>^{commit} <c>^{tree}`; ANSWER-16 lines 1, 7 | ~21:39 |
| 15 | RD-778 ∩ `c7ca0ed..2facd7c` (23 paths) = counts file only; M794S touches 0 `static/` paths | `diff --name-only` + `comm -12` | ~21:39 |
| 16 | Legacy merge-tree c7ca0ed / 2facd7c / 3047ae9: one `changed in both` (counts: fadda68 / a11d7ec / 2d803d7) and one `added in remote` | `git merge-tree <base> <a> <b>` (trivial-merge mode, stdout only) | ~21:39 |
| 17 | Builder cells: base 16 tests / 6 pass / 10 fail; branch 16/16; 1 suite | `rd778-cells-{base,new}.json` | ~21:37 |
| 18 | Builder verify: "VERDICT: PASS — 4575/4575 tests passed across 288 suites (jest exit 0)" | `session-tools/s101/verify-rd778.log` :18641 | ~21:38 |
| 19 | The cells lift functions by the first regex match; `settings.js` has `escapeHtml` at :89 and at :2436 (they differ on non-strings) | test :55-:64; `show 3047ae9:static/js/settings.js` :85-:100, :2430-:2446 | ~21:35 |
| 20 | index.js helper :109 (div textContent → innerHTML). New local helpers: first-run-setup :2933, chart-details :533 | `git grep -n 'function escapeHtml'` | ~21:35 |
| 21 | Offline chat: `addMessage(result.response)`. The server's response comes from `displayResponse`. The backend's only `<strong>` literal is an email body (:21754). Main page `formatAIResponse` escapes first | index-offline.js :77-:89, :119; server.js :7169-:7219, :21754; index.js `formatAIResponse` | ~21:36 |
| 22 | No other reader of `data-original-text` | `git grep -n 'original-text\|originalText'` over static, templates, backend, *.html | ~21:35 |
| 23 | Pages ↔ scripts: index-offline.html, chart-details.html, first-run-setup.html, settings.html + admin.html, index.html | `git grep -l <script> 3047ae9 -- '*.html'` | ~21:36 |
| 24 | 4 pages load bootstrap 5.3.0 CSS/JS, bootstrap-icons 1.10.0 and papaparse 5.5.3 from cdn.jsdelivr.net. index-offline loads none. No bootstrap package in lock 19477a9 | `show <page> | grep -o` of `<script>`/`<link>`; lock JSON | ~21:41 |
| 25 | Lock `19477a9` = c7ca0ed's and 3047ae9's; package.json `384805d`; playwright 1.62.1, playwright-core 1.62.1, jsdom 20.0.3, proxy-addr 2.0.8; no pixelmatch, pngjs, sharp or jimp | `rev-parse <rev>:package-lock.json`; lock JSON | ~21:37 |
| 26 | Chrome 155.0.8059.84; node v26.8.1; `~/Library/Caches/ms-playwright` has one entry; gitleaks at /opt/homebrew/bin | `defaults read`, `node -v`, `ls` | ~21:37 |
| 27 | Tool sha256s = gate 25/26 pins (3c33f5ae…, 1ae84a10…, 6f938bfc…) | `shasum -a 256` | 21:37:50 |
| 28 | Floor: T9 unmounted. Load 4.14 / 3.90 / 4.21. Jest lock held by `s101o-rd476r2-verify`; queue-jest empty | `ls /Volumes`, `uptime`, `ls`/`cat` of the lock base | 21:37:50 |
| 29 | Gates 25 and 26: `STATUS: COMPLETE` (~20:55 and ~18:40 AEDT) | each report.md line 3 | ~21:38 |
| 30 | Gate 25 safeguards stop on its hostile-config server probe, 12:29:04 AEDT, then Opus 4.8 | gate 25 `evidence/classifier-stops.txt` | ~21:39 |
| 31 | deploy-demo `953b2a2` at c7ca0ed and 3047ae9. `paths-ignore` is `**.md`, `docs/**`, `tests/**`. `if:` at :53 and :91 | `rev-parse`, `show … deploy-demo.yml` | ~21:41 |
| 32 | NexusAI `.git/objects`: 114 files; count-objects shows 104 loose | `find | wc -l`, `count-objects -v` | ~21:39 |
| 33 | Ticket provenance: census rows 23-30 (#29-#36 → RD-778), row 22 (#28 → RD-790) | `evidence-s88q-codeql-census/census.csv` | ~21:40 |
| 34 | Model: `levels.opus.model_id` = `claude-opus-5-5` | `0_Brain/dashboard/data/models_latest.json` | ~21:40 |
| 35 | Report dir `…/reports/2026-10-18-gate27-rd778/` does not exist yet; its parent and `qa-trees/` do | `ls` | ~21:41 |
| 36 | No `QA/NexusAI-gate27` route line yet (gates 24-26 at :227, :231, :232) | `grep -n` on `fleet/inbox_routing.conf` | ~21:40 |

## Corrections to the commission
1. **"after main moves for gate 25's landings (M761 f4ae63b then M794S 559dcec)".** Those are gate 25's own rebuilt commits (fact 13). ANSWER-16 lands the seat's `36a0dc0` then `2facd7c`, with the same trees (fact 14). T0 checks main by **tree** (`fb8197a` → `e2bb3ac`), never by commit id. ANSWER-16 item 6 also queues C-170 after land 2, so M0 may sit one land further on. M0 is stamped, never predicted.
2. **"open js/xss-through-dom count must be 0, with a control that the analysis ran on that ref".** The analysis ran on the head (fact 6), and the open count is 0. But **C-209 says that zero cannot mean "fixed"**, and the data shows why: no alert has any instance on the PR ref, not even #28, whose file the PR does not touch (fact 7). So r6 reports it as "0 NEW (C-190 met)". The closure is the landing checklist: #29-#36 read by number on main after the land, with #28 still open as the control. A positive control that a PR analysis can report anything at all is PR #58 (fact 9).
3. **"drive … in a real browser … every non-127.0.0.1 request aborted" (gate 21's precedent) conflicts with the visual compare.** Four of the pages need Bootstrap from cdn.jsdelivr.net, and no local copy exists (fact 24). Under a strict abort, the pages render unstyled and the settings modal has no `bootstrap.Modal`. That is **T5**: (a) Chrome may fetch the exact pinned CDN URLs, or (b) keep the precedent and compare unstyled.
4. **"proving payloads are inert".** The four DOM-resident sources (#29, #32, #34-#36) and the server-supplied ones (the errorCode, the chat answer, the validation result) have no typed product path (fact 21; kit WRONG 10). **T2** (DOM plants at the alert's source) and **T3** (stubbed responses) decide whether those browser arms count.

## UNMEASURED (each with why and the instrument that closes it)
- **Which `escapeHtml` settings.js :1701 binds in the browser (:89 or :2436).**
  - Why: a scope read needs a parse, and I ran nothing.
  - Closes it: r2's scope parse (node's own parser on the file) and b1's settings arm.
  - Expected effect: nil for strings, since both escape the same five characters (READ ONLY).
- **The merge result if C-170 lands before the gate.**
  - Why: there is no merged count for M794S + C-170, and I measured no such merge.
  - Closes it: r1 (rebuild in the gate's store) and r5 (verify).
- **Predicted counts 4671/291 for M0 = `2facd7c`.** This is arithmetic only (READ-ONLY-INFERRED). r5 closes it.
- **Whether the legacy merge-tree wrote nothing.**
  - Why: my before/after object count pointed at the WRONG `.git` (TUESDAY's own, from the cwd), so I cite git's documented stdout-only behaviour of that mode, not a measurement.
  - Closes it: anyone re-running it with `find '<NexusAI>/.git/objects' | wc -l` around it. NexusAI's count afterwards was 114 files.
- **Whether `/api/chat` ever returns entity- or tag-bearing text.**
  - Why: I only grepped for literals.
  - Closes it: b2's AI-answer arms (with a stub, T3) and a read of the analyzer's output builders.
- **Screenshot stability (two boots of the same tree giving 0 px).** b2's base-vs-base control closes it.
- **Whether the synthetic feed populates the user filter with a user and offers an empty date window.** b2 closes it. If it does not, the arm is NOT RUN, named.
- **PR #94's Build conclusion.** It was in progress at drafting. r8 closes it.
- **Gate 21's actual browser driver code.** It is on the unmounted T9 (L-B7). The kit re-derives it from the ruling's words.

## Open slots Tuesday must stamp (the launcher must refuse while any remains)
1. **T0 (first):** read origin main and confirm gate 25's two lands by tree. Choose (a) the gate rebuilds the merge, or (b) the builder forward-merges first. Then fill:
   - PIN-HEADS: `@SLOT-M0-FULL-SHA@` (×3), `@SLOT-RD778-HEAD@` (×3), `@SLOT-RD778-COMMITS@`;
   - the M778 row: `@SLOT-SEAT-COMMIT-or-none@`, `@SLOT-TREE-or-REBUILT@`, `@SLOT-COUNTS-BLOB-or-REGENERATED@`, `@SLOT-TESTS@`, `@SLOT-SUITES@`.
2. **T0-T9 `RULED: @SLOT@`**, 10 slots.
   - **T5 is the one to read twice** (CDN contact).
   - T2 and T3 decide whether DOM-planted and stubbed payload arms count.
   - T1 applies only if the merge conflicts.
3. **The SELF-CHECK line and the Self-check note** (`@SLOT-SELF-CHECK@`, `@SLOT-SELF-CHECK-NOTE@`), last and by hand.
4. **The route line** `QA/NexusAI-gate27|tuesday-agent@agentmail.to|no` in `fleet/inbox_routing.conf`.
5. **Copy the READY** to `briefs/2026-10-18_nexusai-rd778-READY-mail.txt` (body sha256 `d652bdb96311429f67fde188043fcd5256327f27257209279a937dccb992b201` as I read it). Its subject says `READY FOR QA`, not `READY FOR GATE`.
6. **The launcher** `launch_qa_nexusai_gate27.sh`: derive it from gate 26's. It needs to add:
   - the T0 refusal: main = `c7ca0ed`, or main's history lacks the two trees;
   - checks that Chrome and Playwright are present;
   - the READY subject change;
   - a `--check` run with its negative controls, as gate 26's drafter did.

## Notes for Tuesday (not findings)
- **The builder's leftovers are a candidate ticket.** Settings `validationResult.suggestion/.message/.suggestions`, first-run-setup `data.message` and the troubleshooting tips, plus `userType`/`userClass` in the user table: all are still written as HTML and none is in these alerts. The kit routes them to N27, never as findings against RD-778.
- **RD-771 is stacked on rd-778** (ANSWER-12). It re-pins after this gate's land.
- **The model leg.** Gate 25's precedent says Opus 5.5 safeguards may stop b1, which composes XSS payloads against a booted server. The kit restricts b1 to the builder's two marker-only payloads and carries Kam's 2026-09-30 ruling (b): switch that one session to Opus 4.8.

## Holds I did not break
- **NexusAI repo:** read verbs only: `ls-remote`, `cat-file`, `rev-parse`, `rev-list`, `log`, `show`, `diff`, `grep`, `for-each-ref`, `merge-base`, `count-objects`, and the legacy stdout-only `merge-tree`. One `worktree list` attempt was refused by the TUESDAY hook before it ran; I replaced it with `ls` of `worktrees/`.
- **Commands I did not run:** fetch, checkout, worktree add, merge-tree `--write-tree`, `hash-object -w`, clone, jest, npm, browser, server boot, lock ticket, az, docker.
- **Network:** `git ls-remote`, read-only `gh api` GETs under NexusAI's `GH_CONFIG_DIR` (`/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/4_Credentials/.gh-config`, account `kamilDatasec`), and AgentMail GETs. No HTTP to any `*.azurewebsites.net` or other live host.
- **Secrets:** none printed. The AgentMail key was sourced from `/Volumes/Laptop-DEV/TUESDAY/4_Credentials/.env` into the environment only.
- **Writes:** only the two files above and scratchpad temp files. I did not touch `inbox_routing.conf`, the launchers, `briefs/` READY copies, gate dirs or any other client's material.
