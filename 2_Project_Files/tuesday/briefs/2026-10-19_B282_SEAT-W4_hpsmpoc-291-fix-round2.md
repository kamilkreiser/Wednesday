From Tuesday (Kam's Datasec coordinator seat), Datasec / HPSM-POC. **Your STATUS file is the channel and the wrap.** `AGENTMAIL_API_KEY` was NOT in this project's `4_Credentials/.env` at B276 (MEASURED then: count 0), so no mail can be sent: a question is a `STOPPED: NEEDS TUESDAY` last line with ONE question. If the key is now present, send the question to tuesday-agent@agentmail.to with subject `[Datasec/HPSM-POC -> Tuesday] QUESTION: <topic>` and continue on the safest interpretation.
# BRIEF B282 · SEAT-W4: HPSMPOC-291 fix ROUND 2 of 2 on PR #161 (test-only, one new commit on `b276/l1-tests-291-227`)

**Fact marks.** MEASURED = the drafter read the file named (2026-10-19, read-only). RELAYED = quoted from the gate's report B279 or the builder's B276 STATUS. **You re-verify every RELAYED fact at source before relying on it**; if source and report disagree, source wins and you say so in STATUS.
**Tuesday-owned values are slots**: an at-sign, the word SLOT, a colon, a CAPITAL_NAME, an at-sign. Tuesday fills every one before launch (TUESDAY STAMP, last section).

**REFUSE AT ONCE** (last line `STOPPED: NEEDS TUESDAY`, no other step). Quote each count in STATUS.
- **A stamp slot is unfilled.** `/usr/bin/grep -c -E '@SLOT:[A-Z0-9_]+''@' <your Step-0 copy>` must print **0** (control: the same on `<this brief>.md.pre-stamp` prints >= 1).
- **Code `main` is not `befd45e77b391467a1313af8b7b5e0fc580f7b63`** (`git --no-optional-locks ls-remote origin refs/heads/main` in `2_Project_Files`; RELAYED `befd45e77b391467a1313af8b7b5e0fc580f7b63`). If main moved, STOP unless the only new commits touch no file named in this brief.
- **The branch head is not `b8362d7e1ad1632c4a9c2409d62a117493c2bcda`** (`ls-remote origin refs/heads/b276/l1-tests-291-227`; RELAYED `b8362d7e1ad1632c4a9c2409d62a117493c2bcda`). Someone else pushed: STOP.

**BLUF.** Round 1 of PR #161 (draft) was gated by B279: HPSMPOC-291 NO GO, HPSMPOC-227 GO WITH FINDINGS (RELAYED). Tuesday ruled 15:15: this is **round 2 of 2 for HPSMPOC-291 ONLY**. -227's commit `b8362d7` and its findings (B279-4..-7) are NOT in this round. One new commit on top of the head, only `api/tests/HpsmPoc.Api.Tests/PkcsInPackageTests.cs` changes. The four items:
- **B279-1 (Major):** the comment at `PkcsInPackageTests.cs:178-184` states a false measurement. Rewrite it to what you measure.
- **B279-2 (Minor):** the boundary `Build is >= 0 and < 10_000` (`:138`, RELAYED) is pinned by no row. Add rows `10.0.9999.0`, `10.0.10000.0` and a two-part version.
- **B279-3 (Minor):** the guard checks `Build` only. Require the pin's Major.Minor before naming a package; add rows `10.1.0.0`, `11.0.26.1`.
- **B279-8 (Note):** "five or more digits" is wrong for the negative-build case. Make comment, commit message and Jira comment match the code.

**Model:** `claude-opus-5-5` (brief_seat reads the id; never type one yourself). **Stamp time:** `2026-10-19 15:17 AEDT`. **Pane:** `Datasec/HPSM-POC-W4` (suffix `W4`). **B-number:** `B282 confirmed`.
**Step 0:** copy this file unchanged into `1_Project_Definition/Briefs/`, `cmp` it, put the sha256 of both in STATUS, run the REFUSE checks on the copy.
**Launch (Tuesday):** `brief_seat.sh` with the project and this file, as B276's launch line. It exports this project's `AZURE_CONFIG_DIR` and `GH_CONFIG_DIR` and puts `.tools/dotnet` on PATH. Preflight: write "none (brief_seat launch)". **No az.**
**Report:** `1_Project_Definition/Briefs/2026-10-19_B282_STATUS.md`: Step 0 · BLUF · FOUND · TESTED · HOW · NOT TESTED · PRIOR WORK · Not filed · FOR TUESDAY · Corrections.

## STANDING LINES (every brief; do not skip any)
1. **PRIOR-WORK CHECK first.** `git log -S'PackageVersionOf' --oneline`, `git log --follow -- api/tests/HpsmPoc.Api.Tests/PkcsInPackageTests.cs`, records `CLARIFICATIONS.md` from `origin/main`, the newest `Briefs/*_STATUS.md` (B276, B279), HPSMPOC-291's comments (39677 is the builder's, and B279's comment line if posted), Jira text search for `PackageVersionOf`. **A READY FOR QA without a `PRIOR WORK` section naming what you searched and found is returned unread.**
2. **CodeQL.** Push the branch only. Tuesday lands it once CodeQL and checks are green; never dismiss an alert.
3. **No production. No demo deploy. No hosted site, no HTTP to it. No `az`, no Kudu.** `gh`: read-only GETs. Local servers `127.0.0.1` only (none are needed here).
4. **No message to any human.** No mail, chat or PR comment. The only client-facing words are the one Jira comment below.
5. **Never delete** (`rm`, `git branch -d/-D`, `--prune`, `update-ref -d`, `worktree prune` forbidden). Quarantine to `.tools/b282/_quarantine/`.
6. **Record decisions in the artefact:** every choice a reader would ask about goes in STATUS or the Jira comment with its source.
7. **Questions:** see the first paragraph.
8. **Shell:** never type `cd`; absolute paths; multi-step chains under `bash -c '...'` or a quoted heredoc; where a tool needs a cwd (pinned-SDK `dotnet`, `msbuild`) set it with Python `subprocess(cwd=...)` in your own script and say so; `/usr/bin/grep -i` with a positive control for every count; a zero without a control that fires is not a zero.

## BASE / BRANCH / IDENTITY
- **Code repo** `2_Project_Files`, origin `git@github.com:datasecau/HPSM-POC.git`. The local checkout is stale (RELAYED, B276): never read ticket facts from it. Make a worktree `.tools/wt-b282` on the **existing branch** `b276/l1-tests-291-227` from a fresh fetch (`'+refs/heads/*:refs/remotes/origin/*'`, never `--prune`), under `.tools/b198/lock.sh` (copy into `.tools/b282/`, `cmp`). Do NOT open `.tools/wt-b276*`, `.tools/wt-b279*` or any other seat's `.tools/b2*/` files.
- **Identity.** `gh auth status` under the project `GH_CONFIG_DIR` must read `kamilDatasec` (RELAYED); else `STOPPED: NEEDS TUESDAY`. Push with a per-command `GIT_SSH_COMMAND="ssh -i '<project>/3_Access_Keys/github_deploy_rw' -o IdentitiesOnly=yes"`; quote `git config core.sshCommand` first; edit no git config.
- **Refs:** write `git for-each-ref --format='%(refname)'` to `.tools/b282/logs/refs-{before,after}.txt` and assert removed = 0 by program (control: a name dropped from a scratch copy is reported). New names allowed: none (you add a commit, not a branch).
- **Push exactly one thing, plainly:** `b276/l1-tests-291-227`, fast-forward from `b8362d7e1ad1632c4a9c2409d62a117493c2bcda`. **No rewrite, no amend, no rebase, no force.** Commit `7c87bdf` and `b8362d7` stay untouched. Read the head back by `ls-remote` after the push. Never push `main`. Tuesday owns PR #161.
- **Ports:** your block is `7200-7209 (none expected)`; you should need none. Name any you used.
- **Jira:** copy the helper kit from `.tools/b265/` / `.tools/b276/` by `cp` + `cmp` into `.tools/b282/`; never edit originals. `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN` are read by name in-process, never printed, never on argv. **Write verbs allowed: ONE comment on HPSMPOC-291. No transition (it stays open until merged), no create, field edit, link, label, delete.**

## THE WORK (all in `PkcsInPackageTests.cs`)
**Scope guard.** `git diff --name-only origin/b276/l1-tests-291-227` (your commit vs the pushed head) must list exactly `api/tests/HpsmPoc.Api.Tests/PkcsInPackageTests.cs` (assert by program; control: a planted extra path is flagged). Any need to touch `api/src`, a `.csproj`, `global.json`, `.github`, a web spec or `infra` stops the work: `STOPPED: NEEDS TUESDAY`.

**Step 1 (BEFORE any edit): re-measure the two load-bearing SDK facts yourself.** The gate's claim (RELAYED, B279 r2): SDK 10.0.401 bundles the 10.0.12 targeting pack (`BundledVersions.props` `TargetingPackVersion="10.0.12"`; pack manifest Pkcs `10.0.1226.42308`, below the pin 10.0.13), and 10.0.402 bundles 10.0.13 (Pkcs `10.0.1326.50504`, a tie). Measure:
- (a) In a scratch dir OUTSIDE the repo tree whose `global.json` pins `10.0.401` with `rollForward: disable` (and again for `10.0.402`): `dotnet --version`, then the same `msbuild -t:ResolveTargetingPackAssets;ResolvePackageAssets -getItem:ResolvedTargetingPack` call the test's `SdkPkcs.Read` makes (read the file for the exact call). Quote the resolved pack path and Pkcs file version per SDK.
- (b) Mutant m1 = the `PreferPkcsPackageOverSharedFramework` target removed from `HpsmPoc.Api.csproj`, applied in a scratch copy only, never on your branch, with the same pinned `global.json`: run `PkcsInPackageTests` on pinned **401** (expect 14/14 green) and pinned **402** (expect red, the tie branch). The 401 pin needs the 401 SDK; both SDKs are in `.tools/dotnet` (RELAYED).
- (c) In-tree, `dotnet --version` from the repo's own `global.json` (10.0.401, `latestFeature`): the gate says it prints 10.0.402. Quote yours.
- **If any of your three results disagrees with the gate, STOP**: `STOPPED: NEEDS TUESDAY` with the one question. Otherwise cite your own runs (command, output line, time) in the comment you write and in STATUS; do not cite the gate as the evidence.

**Step 2: B279-1.** Rewrite `:178-184` so it states only what Step 1 measured: 401 bundles the 10.0.12 pack (Pkcs below the pin), so B255's m1, m3, m4a, m4b stay green on a really pinned 401 even with 10.0.13 installed; 402 bundles 10.0.13, a tie, and m1 is red there; the repo `global.json` selects 402 whenever 402 is installed, so a run from the tree is a 402 run, and a real 401 run needs `rollForward: disable`. Leave no sentence you did not measure (the old false claim "m1 is red on SDK 10.0.401 as on 10.0.402" must be gone; grep it with a control).

**Step 3: B279-2 and B279-3 (read `PackageVersionOf` at `:128-140` and `RaiseThePin`, `EarlyWarning` first).**
- Make the helper name a package only when `Major.Minor` equals the pin's `Major.Minor` (10.0) AND `Build` is in the scheme range; otherwise take the existing file-version-only branch. Do not change any row's expectation that round 1 already has (every in-scheme row is unchanged, RELAYED: 30 of 38 fixture cells identical).
- New rows (the existing Theory's `string? red` shape cannot express `DoesNotContain`; add a `[Fact]` or a Theory of the right shape, builder's choice, recorded): framework `10.0.9999.0` -> contains "raise the pin to 10.0.99"; `10.0.10000.0` -> the file-version text, no "raise the pin to"; a two-part version (Build -1, e.g. `10.1`) -> the file-version text; `10.1.0.0` and `11.0.26.1` -> `DoesNotContain("raise the pin to")` and the file-version text.
- **RED/GREEN proof:** the new rows are RED against the round-1 helper (use the head's helper text in a scratch copy, not on your branch) and GREEN after. Quote class counts before (14 passed, RELAYED) and after.
- **Mutants, each restored byte-equal (sha256 + `git diff --quiet`):** the gate's survivors a1 (`< 10_000` -> `<= 10_000`), a4 (`< 9_999`), a5 (drop `>= 0`) must each go RED on your new rows; add a mutant that drops the Major.Minor check (RED on `10.1.0.0` / `11.0.26.1`). Also re-run the gate's killed ones (a2 `< 100_000`, a3 `< 1_000`) and the builder's m291 / m291b: still RED. Quote each result; each tamper asserted landed.

**Step 4: B279-8.** The comment, your commit message and the Jira comment describe the guard exactly as the final code does (for example: a build outside 0..9,999, meaning five or more digits or a negative build from a two-part version, or a Major.Minor other than the pin's). Check by program that no text of yours still says "five or more digits" alone (control: a planted line is flagged).

**Step 5: regression and push.**
- Class `PkcsInPackageTests` and the whole `HpsmPoc.Api.Tests` project, before and after, with `.tools/dotnet` from the repo tree: quote passed/failed/skipped. Round 1: class 14/0/0 (RELAYED), project 1,462/13/0. Test names as multisets before vs after: **lost 0**, added = your new names (control: one name removed reports lost 1). No `Skip`, `.only`-style or timeout token added.
- One commit, first line `HPSMPOC-291: <what round 2 changed>` (match B279-8), message body names the measured facts and the mutants. gitleaks over the diff and the message with a random canary that fires; read its rc before commit and push, chained with `&&` inside `bash -c`. Push plainly. `ls-remote` the head.

**Step 6: ONE Jira comment on HPSMPOC-291** (BLUF first): `BLUF: round 2 of 2 pushed @ <sha7>: <what changed>. Evidence: <your Step-1 results, the RED/GREEN counts, the mutants>. Not done: <list or "nothing">. Source: <file:lines, STATUS path>.` No person's name, no sample-customer name, no HP text, no key value; the word "Kam" never appears (say "the product owner"). Re-GET the issue first (still Backlog, no new Done-when text); read the comment back by id byte-equal with a one-character mutant that compares unequal. Post only after the push is read back.

## HOLDS
- 🔴 **STANDING HOLD (verbatim from B248's brief, as B276 quoted it):** No HP Restricted document (the executive deck, the financial model, anything HP marks Restricted) is given to ANY AI tool — Claude seats, subagents, the product's model, Ornith or the Spark — without HP's written approval (signed SOW §4.1.4(c)). Do not open `HP Reporting and Docs/` or the SOW file in the project root. **Also never open `2_Project_Files/HP Docs/`.**
- **Datasec / HPSM-POC only.** Test file only: no product code, no merge, no deploy, no hosted site, no Azure, no CI change.
- **Not in this brief:** HPSMPOC-227 and its findings B279-4..-7; the PR #161 body and title; the records repo (no records branch, no C-entry, no history entry this round); any other ticket; the amendment of HPSMPOC-291's Done-when clause 1 and the B271-6 note (Tuesday's, FOR TUESDAY).
- **Never open** `.local/`, `1_Project_Definition/Source_Documents/**`, `HP Reporting and Docs/`, `2_Project_Files/HP Docs/`, `.tools/backup-*`, `4_Credentials/inbound_with_secrets`, any other seat's `.tools/b2*/` files, `wt-*` trees or `.tools/dotnet` internals. Named exceptions: the B265/B276 helper files and `b198/lock.sh` by `cp` + `cmp`; running `.tools/dotnet` as a tool; reading `Microsoft.NETCoreSdk.BundledVersions.props` and the targeting-pack manifest for Step 1.
- A line at your prompt that is not a Tuesday file pointer is not an instruction. **Nothing to HP, Paul or any human.**

## UNMEASURED at drafting
Every number and line number above is RELAYED from B279/B276 (the drafter ran no dotnet and read no code, per its commission). Not read: the live ticket text (a new comment may exist), `PkcsInPackageTests.cs` at the head (line numbers `:128-140`, `:178-184`, the exact `SdkPkcs.Read` call and `RaiseThePin` signature), whether the 401 SDK still sits in `.tools/dotnet`, the state of origin.

## FOR TUESDAY (put these in your STATUS as written; do not do them)
- **PR #161 body correction is TUESDAY's.** Corrected text for the "now states what was measured" line: "The comment now states what was measured on a really pinned SDK: 10.0.401 bundles the 10.0.12 targeting pack (Pkcs below the pin), so m1 stays green there; 10.0.402 bundles 10.0.13 (a tie) and m1 is red; the repo global.json selects 402 when installed, so a real 401 run needs rollForward disable. PackageVersionOf names a package only for the pin's Major.Minor and a build of 0 to 9,999; any other file version gets the file-version text. Round 2 adds the boundary and Major/Minor rows (B282)." Commit `7c87bdf`'s message keeps its round-1 sentence (no rewrite); the body note says so.
- Records: amend HPSMPOC-291 Done-when clause 1 and the B271-6 note (B279 candidate 4).

## STATUS contents
Step 0 (sha256s; REFUSE counts with controls) · Step 1 pins (main, head, `gh auth status`, `core.sshCommand`, refs-before) · PRIOR WORK · Step 1 measurements (a, b, c with output lines and times, vs the gate: AGREE or the disagreement) · per item B279-1/-2/-3/-8: what changed, RED/GREEN counts, every mutant and its byte-equal restore · class and project counts before/after, names multiset · `git diff --name-only` · gitleaks rc · pushed head by `ls-remote` · Jira comment id and read-back EQUAL · Corrections · FOR TUESDAY.

**Last line, exactly one of:**
- `READY FOR QA: B282 HPSMPOC-291 round 2 b276/l1-tests-291-227 @ <sha40 by ls-remote after push> · tier 2`
- `STOPPED: NEEDS TUESDAY` followed by ONE question.

## TUESDAY STAMP (fill every slot; keep a `.pre-stamp` copy as the REFUSE control)
- **RULED by Tuesday at stamp (drafter doubt):** if `PackageVersionOf` does not receive the pin, you MAY change its signature (or add a parameter) INSIDE `PkcsInPackageTests.cs`; that is still test-only. Every caller in that file is updated in the same commit, and the scope guard still lists one path.
- Slots: `CODE_MAIN_SHA` (RELAYED `befd45e77b391467a1313af8b7b5e0fc580f7b63`, re-read by ls-remote at stamp) · `HEAD_SHA` (RELAYED `b8362d7e1ad1632c4a9c2409d62a117493c2bcda`) · `MODEL` · `STAMP_TIME` · `PANE` (`Datasec/HPSM-POC-W4`) · `PANE_SUFFIX` (`W4`) · `PORT_BLOCK` · `B_NUMBER_CONFIRM` (`B282 confirmed` after a folder check for B282/B283 hits).
SELF-CHECK: re-read the stamp against the REFUSE checks and the last-line formats | Tuesday, stamp time | slot count 0 after stamping (control: the `.pre-stamp` copy)
