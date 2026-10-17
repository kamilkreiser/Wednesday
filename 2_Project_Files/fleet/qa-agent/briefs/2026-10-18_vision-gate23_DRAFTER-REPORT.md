# Vision gate 23 (QuickQuote PR #8 @ 4d6ed6e, puppeteer-core 25.0.2 + node:22; C-19): drafter's report

Drafted 2026-10-18, 06:09 to ~06:35 AEDT, by a read-only drafting sub-agent for Tuesday (Opus 5.5).

Outputs:
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-18_vision-gate23-qq-pr8-puppeteer25-node22.md` (the kit)
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_vision_qq_gate23.sh` (chmod +x, `bash -n` clean)
- this report

Nothing else was written outside the session scratchpad. The scratchpad holds a tree-hash script, a stamped copy of the brief, a copy of the routing conf and two launcher copies, all used only to test the launcher. There was no launch, mail, tap, routing edit, push, merge, fetch, `az`, npm, browser or product process. The QuickQuote repo was read only with `git --no-optional-locks` read verbs. `gh` was used for GETs only, with Vision's GH_CONFIG_DIR, and that directory's file mtimes are unchanged (12 Oct 18:09). **One disclosure:** while checking host tools I ran a single read-only `docker version --format '{{.Server.Version}}'` (it returned 29.7.2). I ran no other docker command.

## The four facts that shape this gate

1. **PR #8 is 4 commits behind main.** Its head `4d6ed6e` was last forward-merged onto `e4ce536` (2026-10-16 12:49). Main then took the email guard (PR #9, `5f08fe0` / `9d1c5ab`) and v2.36 (PR #11, `818a019` / `437ab4b`). Everything the builder measured (69/132/170/6, the arm64 images, the audit) was against `e4ce536`.
2. **What would land is GitHub's test merge `7378a4e`, with tree `8077fdc`.** I reproduced that tree read-only: I took main's tree and swapped in PR #8's five blobs, with the merged package.json computed as blob `f0df06f`. The same method gives back `c71780c` and `01bdc92` exactly, which are its two controls. `7378a4e` is not in the local object store, and **no CI has ever run on it** (0 runs for that head_sha). The launcher recomputes this tree before every launch (guard 25).
3. **The only file PR #8 and main share is `stage3/package.json`, and the hunks don't overlap** (PR #8 at line 21, puppeteer-core; main at line 11, test:print). The same is true for PR #8 against PR #10. The GitHub compare API agrees: `f31720e...4d6ed6e` and `4d6ed6e...f31720e` both have merge-base `e4ce536`, and package.json is their only common file. Merged in either order, main + #8 + #10 should give the same tree, `d809de1` (my prediction; the gate proves it).
4. **The host has only Node 26.8.1.** There is no Node 20 or 22 installed. A gate without docker therefore never runs Node 22 itself. The repo records App Service as running a container, so in production Node comes from the image's floating `FROM node:22-bookworm-slim`. The repo has no NODE| stack setting and no WEBSITE_NODE_DEFAULT_VERSION. Tuesday's AZ-PRE-READ, with its `DOCKER|` prefix, is the live confirmation.

## Pins, each with when I read it (AEDT, 2026-10-18)

| what | value | how / when |
|---|---|---|
| main | `437ab4bc412bc74d8da3b66a6ac5c71d7335c5d6` (= HEAD; LIVE v2.36 expected) | `ls-remote` 06:09:46 |
| PR #8 head | `4d6ed6ef403ef8962ded8211b76c3c6809bbb8c3` = `refs/pull/8/head` | `ls-remote` 06:09:46; launcher re-read 06:29:53 |
| `refs/pull/8/merge` | `7378a4e1206afb6c2429ca9a9c74c30b52d40c39`: parents 437ab4b + 4d6ed6e, tree `8077fdc`, created 2026-10-16T19:13:21Z | `ls-remote` 06:09:46; commits API 06:10:25 |
| PR #10 head | `f31720ee677dbe2deb53dcb7991f1683a1b03ce1` (tree `ee51fa7`) | `ls-remote` 06:09:46 |
| merge-base / counts | `e4ce536`; 3 ahead, **4 behind** | rev-list 06:10:02 |
| PR #8 API | open, not draft, mergeable, `clean`; base.sha still `e4ce536`; 5 files, +85/−522; updated 2026-10-16T01:53:57Z | GET 06:10:17 |
| PR #8 body | read whole: C-19, the "Verified" list, and the not-tested list (amd64, prod-settings boot, live site) | GET 06:10:25 |
| CI on 4d6ed6e | 38837565972 push, 38837589895 pull_request, 38837588311 "PR #8" dynamic CodeQL: all completed success; 13 check runs, all success; CodeQL "No new alerts in code changed by this pull request" | GET 06:11:24 |
| CI on 7378a4e | 0 runs | GET 06:11:24 |
| Dependabot | #1 GHSA-jmr9-qjv8-65gv and #4 GHSA-7pqw-9j4j-h8q3: extract-zip, high, `<= 2.0.1`, **no patched version**, open. #2, #3, #5-#16 fixed | GET 06:11:24 |
| dependency review | `437ab4b...4d6ed6e` and `437ab4b...7378a4e`: 57 entries (14 added, 43 removed); extract-zip@2.0.1 removed carrying both GHSAs; 0 vulnerabilities on the added entries | GET 06:11:42 / 06:13:56 |
| advisory DB | puppeteer-core@25.0.2 → 0; positive control extract-zip@2.0.1 → both GHSAs | GET 06:13:5x |
| code scanning open | main 0, refs/pull/8/head 0, refs/pull/8/merge 0 | GET 06:11:4x |
| repo merge settings | merge, squash and rebase all allowed (the Vision CLAUDE.md says "merge commit") | GET 06:11:45 |
| merged package.json | `f0df06f` (M8), `23cc8c9` (M8P10) | python blob hash 06:11 |
| trees | M8 `8077fdc65d39be92d27aba11ebed33586b00440a` (= GitHub); M8P10 `d809de1dd44bd7a0624fcf17dd50636f1acfcb79` (predicted) | read-only python over ls-tree 06:2x |
| lockfiles | head: 247 entries, puppeteer-core 25.0.2 and @puppeteer/browsers 3.0.2 both `>=22.12.0`, chromium-bidi 16.0.1, no extract-zip. main: 286 entries, extract-zip 2.0.1 (+ nested debug/ms) | python over `git show` 06:1x |
| READY on disk | sha256 `201da80e…`, 6,738 B, 40 lines, written against e4ce536 | shasum 06:1x |
| gate 22 report | sha256 `56356c76…`, 455 lines; its §12 lists what to re-run "If PR #8 merges first" | 06:1x |
| host | load 1.55; Chrome 155.0.8059.84; gitleaks 8.30.1; ports 47310-47319 free; tmux panes `tuesday` and `fleet-monitor` only (no Vision builder pane); routing conf ends at QA/Vision-gate22, line 229 | 06:12 |

## What I copied, and from where

- **Gate 22's kit and launcher (read whole)** gave the section shape, the PIN parser, the guard numbering and pattern, the pending-guard ordering, the GET-only gh shim, THE MODEL RULE, the floor and egress and deadline text, the question and verdict routes, and `--check`. I diffed gate 21's launcher against gate 22's; the shape is identical, and the differences are in content.
- **Gate 18's kit (read whole; drafted for this same PR, never launched)** gave the PR-#8 traps: the image ships `stage3/test/`, the stub-identity problem and its G-M1/M2 mutants (renamed G23-M1/M2), `require(esm)` warnings, the entry point needing Azure, and the whole image method. The new kit cites gate 18's §N2-§N5 and §13.5 for the image leg instead of copying them, which keeps it shorter.
- **New in this kit:** the M8 / M8P10 merge-result model and its tree proofs; the fixed synthetic quote set S1-S16 with a byte-or-semantic equality rule and a BASE-vs-BASE determinism control; the interaction column with PR #10 (gate 22's 12 cells under puppeteer 25); the Node-22-as-recorded section (§N5); dependency-review and advisory-DB reads standing in for npm audit; gitleaks with a planted positive control; and the merge-order table in §12.
- **Launcher changes from gate 22:** guard 25 (the merge model), guard 49 (IMAGE-LEG; docker checks only for an image leg), guard 50 (NPM-AUDIT), and guard 48 (now TARGET-MODE; FORWARD-MERGE-FIRST is a hard refusal). In 38R the builder pane is now optional, since none is live. Guard 44 adds gitleaks. Guard 74 now checks the lockfiles and confirms `lib/cjs` appears only in the two files PR #8 rewrites.

## Launcher test (in the scratchpad, never against the real brief's stamps)

- Run on the real kit, `--check` passes every content guard and stops on the six coordinator to-dos (47, 48, 49, 50, 41, 32). Exit code 47. Output at 06:29:53.
- On a scratch copy with every stamp filled (MERGE-TREE / NONE / NOT-RUN) and a scratch routing conf, it reports **"all guards pass"** and exits 0.
- A scratch copy with a wrong M8 tree constant fails at guard 25. A copy set to FORWARD-MERGE-FIRST is refused at 48.
- **The image-leg branch (ARM64-NATIVE / AMD64) was not exercised.** Testing it would have meant running more docker commands. It is shaped after gate 18's guard 45D.

## What Tuesday must stamp before launch

1. **SELF-CHECK** line and note.
2. **AZ-PRE-READ.** Tuesday's own `az webapp config show` of linuxFxVersion, using Vision's AZURE_CONFIG_DIR. The `DOCKER|` prefix matters for §N5.4. I expect v0.6.4-tool2.36-437ab4b.
3. **TARGET-MODE (D6).** My reading is MERGE-TREE. The alternative is FORWARD-MERGE-FIRST, which follows C-19's scope wording literally and gets CI on the real tree, at the cost of a builder round.
4. **IMAGE-LEG (D7).** My reading is NONE, because the commission scopes Node 22 as a read. Weigh that against C-19's own evidence list ("the container image built LOCALLY … with the PDF path run inside it") and gate 18's R2 (amd64). Under NONE, no gate will have run Node 22 + Debian Chromium before a publish. ARM64-NATIVE is the cheap way to cover the Node half; the load is low now (1.55).
5. **NPM-AUDIT (D8).** My reading is NOT-RUN; the GitHub advisory reads cover it with no new egress.
6. **D4 RULED line.** Round 1. A NO GO goes back to the builder. A GO releases a merge only while main is still 437ab4b and in the order Tuesday rules. It never releases a publish.
7. **Routing.** Add `QA/Vision-gate23|tuesday-agent@agentmail.to|no` to inbox_routing.conf (after line 229) and stamp ROUTING-LINE.
8. Re-run `--check`. Launch through `cockpit.sh add 'QA/Vision-gate23' …` (the exact command is in the launcher header).

## Open doubts (for Tuesday)

- **Merge order is a coordinator decision with a Kam-shaped consequence.** If PR #8 merges first, a v2.39 publish built from that main also ships Node 22 + puppeteer 25. C-20 says PR #8 needs Kam's own word, and his open card `quickquote-v239-custom-price-fix-publish-1017` doesn't mention the runtime. There is precedent for asking him: `quickquote-guard-publish-includes-pr7-deps-1016`. The cleanest order looks like PR #10 merged and published first, then PR #8. That is my reading, not a ruling. §12 has the gate measure both orders.
- **Whether GitHub will accept the merge without fresh CodeQL on the new merge ref is UNVERIFIED** (Vision CLAUDE.md: "Main only takes a PR that CodeQL has scanned"). The PR-side CodeQL result is for the old test merge over e4ce536. The ruleset read may need permissions the token lacks.
- **Byte equality of the PDFs.** I expect BASE and M8 to differ only in Chrome's date and ID tokens, since it is the same Chrome binary and the same page code. A changed `page.pdf` default between puppeteer 23 and 25 (for example tagged PDF) could change bytes without changing meaning. The kit counts that as EQUAL with an observation. Anything that changes text, pages, fonts or pixels is a FAIL. I didn't read the defaults of either version; that is the gate's §N4.3.
- **The count mismatch is expected.** The dependency-review compare's 14 added / 43 removed and the READY's 40 removed / 1 added / 13 changed count different things. The gate reconciles them by name@version.
- **The builder's amd64 STATUS mail is not on disk.** Only Tuesday's 10-16 14:09 summary of it exists: 169/170 vs 168/170, all timeouts under emulation at load ~200. The kit treats it as a relayed claim.
- **Gate 4's report is on the T9 only.** The kit reads it only if the T9 is mounted.
- **The `fleet-monitor` pane has no live claude,** so the only negative control this run is the `tuesday` seat (pid 68690 at 06:30). Guard 38R accepts that, but it is one control, not several.
- **The backlog branch name is misleading.** `backlog/qq-extract-zip-2026-10-16` now carries the G21 tickets. `88ad5e8`, the READY's extract-zip ticket, is still an ancestor of its tip `01c8d7f`, and BACKLOG.md there still holds the extract-zip item. Someone should close it after the merge, once #1 and #4 read fixed.
