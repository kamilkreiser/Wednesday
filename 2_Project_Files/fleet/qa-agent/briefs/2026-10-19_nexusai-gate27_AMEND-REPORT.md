# Gate 27 (RD-778) — AMENDMENT 1 report, for Tuesday

Drafted 2026-10-19 from 04:53:50 AEDT by a read-only drafting agent (Opus 5.5). This agent only read and measured. It wrote the four files below, plus the `.pre-amend` copy. Nothing was launched.

## 0. BLUF

- **M0 is confirmed: `888203c8c50e13938ca557e8aa0f1faf2101ff31`.** `git ls-remote origin` read it at 04:53:50 AEDT, `gh api` read it at 04:53:58, and the launcher's own `ls-remote` read it again during `--check`. All three agree, so there is no STOP.
- **One premise in the commission is wrong: the landing chain is NOT main's first-parent chain.** Both landing merges are forward merges that put the branch first:
  - `888203c`'s parents are `2facd7c` then `5eb80a7`.
  - `5eb80a7`'s parents are `537741c` then `36a0dc0`.
  - So `git log --first-parent 888203c` runs `888203c → 2facd7c (tree e2bb3ac) → cd171f9 → …` and never reaches `36a0dc0` or `5eb80a7`.
  - A "first-parent chain contains tree fb8197a" check would therefore refuse forever.
  - What I did instead: the kit and the launcher check the chain by **ancestry** (`merge-base --is-ancestor` c7ca0ed→36a0dc0→5eb80a7→888203c), plus each commit's tree and its exact parents, plus "main's ancestry carries tree fb8197a at exactly 36a0dc0".
  - GitHub's push log confirms the three lands were fast-forwards (see §2).
- **Prediction (arithmetic only): 4676 tests / 292 suites.** That is 4660/291 from `888203c`'s counts blob `f3f387b`, plus 16 tests in 1 suite from RD-778.
- **The conflict set against `888203c` is the counts file only** (§2, item 7).
- **Launcher:** `bash -n` passes (rc 0). `--check` passes every guard, then refuses with exit 40 (32S + 40), as intended (§4).

## 1. What changed (diff summary)

### 1a. The kit

File: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-18_nexusai-gate27-rd778-xss.md`

- Before: 241 lines (the numbering below follows `diff`'s count of 242 for the pre-amend file), sha256 `8596111b3ea915ea55b82a34c0e44d47947538e1659b6e9ff084fdc199a6da8c`.
- After: 242 lines, sha256 `b5216da1888b2537e424afa02baea10c276cd108cc5cf69183845266fdb97534`.
- Pre-amend copy, made with `cp -p` and identical hash: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-18_nexusai-gate27-rd778-xss.md.pre-amend`.
- `diff` shows 15 hunks and 41 changed lines. Line numbers are pre-amend → post-amend:

| hunk | what changed |
|---|---|
| 3a4 (new) | **AMENDMENT 1** paragraph: the measured chain, the push log, `e2bb3ac` vs `428f042`, C-170 not landed, the TOPOLOGY NOTE, and the list of amended places. |
| 6c7 | The READY sentence: the body is now copied, with its sha256 re-measured. |
| 11-12c12-13 | PIN-HEADS filled: MAIN `888203c…`, RD778 `3047ae9…`, commits `1`. |
| 14c15 | A sentence appended to the drafting-pins note, giving the sources of the fill. |
| 19c20 | MERGE-PINS row M778 filled: `3047ae9… \| 888203c… \| none \| REBUILT \| REGENERATED \| 4676 \| 292`. |
| 22c23 | The launcher paragraph now states the new refusal conditions and says 4676/292 is arithmetic. |
| 37-39c38-40 | **WRONG 1** gets the new condition, with each id measured. **WRONG 2** is re-measured against `888203c`. **WRONG 3** is recomputed to 4676/292 and labelled arithmetic. |
| 41c42 | **WRONG 5**: I added only the evidence-class words "(MEASURED at drafting, `gh` READ;". Without them the derived launcher's "every WRONG item is marked" guard refuses on item 5, which was the only unmarked item. |
| 54c55 | **T0's default (a)**: the condition is now "main exactly `888203c`" with the chain by ancestry, and the prediction is 4676/292. The `RULED:` slot is untouched. |
| 131c132 | r1's predicted-by column now reads "MEASURED against M0 `888203c`". |
| 136c137 | r5's expected value is now 4676/292 (arithmetic). |
| 165c166 | §3 Q1's T0 landing-check wording is updated. |
| 213c214 | The §11 verdict line's RE-PIN clause now reads `M0 <m0-7> = 888203c carrying 36a0dc0 (fb8197a)→5eb80a7 (2d2caa3)→888203c (428f042) by ancestry <yes\|no>`. |
| 234-236c235-237 | FILL AT STAMP for T0 now says the tables are filled and Tuesday re-reads main. The T-slot and SELF-CHECK lines are **re-worded to name the slots without their at-signs** (see §3). |
| 238-239c239-240 | FILL AT STAMP for the READY and the launcher: both marked done (✓). |

- Nothing else changed. Every T-slot, the SELF-CHECK slots, rows r0–r10/b1/b2, §2b, §2c, §3a, §9–§11 and PROVENANCE are verbatim.
- WRONG 4 and 6–14 are verbatim. Their drafting-time numbers (114 objects, the 434,634-byte clarifications file) are now historical; the current readings are in §2.

### 1b. The new launcher

File: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate27.sh`

- 761 lines, sha256 `b32498b27ecc0764d9c9d3ebd69bb3d64beec3f9833c75e7c9bf635068127895`.
- **Derived from gate 26's launcher**, with gate 25's read whole for the multi-row parser. The structure is unchanged:
  - the embedded prompt and `--check` mode;
  - the PIN parser (guard 40);
  - the C-192 `lsr` retry;
  - the lock-tool, runner and C-133 pins (90/91);
  - the carried-rulings greps (70);
  - the MODEL RULE (82);
  - the H-rule fragment guards (76–79);
  - the live 38R negative-control derivation;
  - guard 86;
  - the stamp and route guards last;
  - SESSION_SECRET unset, NEXUSAI_LOCK_BASE exported, and the notifier switch, before `exec claude`.
- **What it refuses on:**
  - **(40)** PIN-HEADS must hold exactly MAIN `888203c…` and RD778 `3047ae9…` (base `c7ca0ed`, 1 commit). The M778 row must equal `none / REBUILT / REGENERATED / 4676 / 292`.
  - **(18M, new: T0's landing check)**
    - the MAIN pin is not `c7ca0ed`;
    - its tree is `428f042`, with parents `2facd7c` + `5eb80a7`;
    - `2facd7c` is tree `e2bb3ac` with parents `cd171f9` + `36a0dc0`;
    - `5eb80a7` is tree `2d2caa3` with parents `537741c` + `36a0dc0`;
    - `36a0dc0` is tree `fb8197a` with parents `7f1881e` + `c7ca0ed`;
    - **main's ancestry carries tree `fb8197a` at exactly `36a0dc0`**;
    - the is-ancestor chain c7ca0ed→36a0dc0→5eb80a7→888203c holds;
    - `diff --name-only e2bb3ac 428f042` = the three paths;
    - RD-775's two blobs at `888203c` equal `5eb80a7`'s;
    - `be0fe37` (C-170) is not an ancestor, and `arm-ttk.yml` is absent.
    - A `--first-parent` walk is used **only as a NOTE**: it should read 0, and it does today.
  - **(18T)** The T9 must not be mounted.
  - **(18)** `ls-remote` (C-192): origin main ≠ `c7ca0ed` and **= the MAIN pin exactly**, and the branch = `3047ae9`. `refs/pull/94/head` is a NOTE only.
  - **(22)** 7 gated paths; the both-sides set vs `888203c` is the counts file only; 25 main paths changed; 0 main `static/` paths.
  - **(93)** Lock / package / deploy-demo blobs at c7ca0ed, the head and main. proxy-addr 2.0.8, playwright and playwright-core 1.62.1, jsdom 20.0.3. The deploy-demo `if:` lines. Counts 4559/287, 4575/288, 4660/291, with the blobs pinned. **The prediction recomputed in-guard** as main + 16/1. The census 341/342/347. settings.js declares `escapeHtml` twice and the other three files once each. The WeakMap. The two builder payloads. The CDN tags.
  - **(96, new)** Google Chrome must be present. Its version 155.x and the Playwright cache are NOTEs.
  - **(31)** Requires these to be present:
    - the READY copy, with its **sha256 = `d652bdb9…b201`** and the strings `READY FOR QA`, PRIOR WORK, NOT TESTED and the verify line;
    - the s101 rd778 evidence;
    - gate 24's and gate 25's instruments (by name), and gates 24/25/26 reports at `STATUS: COMPLETE`;
    - gates 21–26 §3a;
    - the census row for #28.
  - **(32S, new, last)** **0 at-sign SLOT placeholders anywhere in the kit.** The SELF-CHECK line must also be in the fleet's form (`SELF-CHECK: re-read end-to-end for contradictions | …`, as gate 26's kit line 25). This replaces gate 26's `@STAMP@` token.
  - **(40)** The route line must exist.
- **Derived as instructed:**
  - pane and route name `QA/NexusAI-gate27`;
  - the model read at runtime from `/Volumes/Laptop-DEV/TUESDAY/0_Brain/dashboard/data/models_latest.json` `levels.opus.model_id`, which must equal `claude-opus-5-5` (exit 9 otherwise);
  - the brief path;
  - report path `/Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-10-18-gate27-rd778/report.md` (kit T8);
  - `READY_778` override env for `--check` only.
- **The embedded prompt was rewritten for gate 27** (the browser leg, ruling (u), DOM-PLANTED/STUBBED captions, C-209's "0 NEW"). It carries the kit's NOT TESTED line verbatim, does not name the server entry path, and contains no placeholders.
- **Disclosed:** I ran `chmod +x` on it to match gate 25/26's mode (`-rwxr-xr-x`). It is launched via `bash '…'`, so the bit is cosmetic. That is the one change I made outside the Write/Edit tools.

### 1c. The READY copy

File: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-18_nexusai-rd778-READY-mail.txt`

- **Source:** AgentMail GET of `tuesday-agent@agentmail.to`, made inside `python3 -I`. The key was read by name and never printed.
  - Message `<010001a14e84d2df-…@email.amazonses.com>`, from `CoAgent <coagent@agentmail.to>`, timestamp `2026-10-18T10:18:10.000Z`.
  - Subject: `[Datasec/NexusAI-O -> Tuesday] READY FOR QA: RD-778 js/xss-through-dom x8 — rd-778-xss-through-dom-s101o @ 3047ae92b4179adf5ae1bf6e1b60825af2e296e3`.
- **Field `text`** (6444 chars, 6452 bytes, 55 lines) has sha256 **`d652bdb96311429f67fde188043fcd5256327f27257209279a937dccb992b201` = the kit's line 6**. The `extracted_text` field differs (`45f1d2eb…`) and was not used.
- **How it was written:** staged in the scratchpad, written with the Write tool, then re-hashed on disk. The result matches exactly (6452 bytes).

## 2. What I measured, with sources

All NexusAI reads used `git --no-optional-locks` with read verbs only, plus the legacy stdout-only `merge-tree`. All `gh` calls were GETs, with `GH_CONFIG_DIR='/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/4_Credentials/.gh-config'` on repo `datasecau/Reporting_Dashboard_Au`.

1. **Heads**
   - `ls-remote origin` at 04:53:50 AEDT (rc 0, 1 attempt): main `888203c8c50e13938ca557e8aa0f1faf2101ff31`; `rd-778-xss-through-dom-s101o` and `refs/pull/94/head` both `3047ae92b4179adf5ae1bf6e1b60825af2e296e3`.
   - `gh` at 04:53:58: the same two refs; PR #94 head `3047ae9…`, base `c7ca0ed…`, draft, open.
   - The launcher's `--check` (§4) read main `888203c` and branch `3047ae9` again, in 1 attempt.
2. **Commit count:** `rev-list --count c7ca0ed..3047ae9` = **1**, with no merges. `merge-base(888203c, 3047ae9)` = `c7ca0ed`. `--left-right --count 888203c...3047ae9` = `31 1`. The head's tree is `932a907…` (matches kit §A).
3. **Landing chain** (`cat-file -t` = commit for every id; trees by `rev-parse <c>^{tree}`; parents by `log -1 --format=%P`):
   - `36a0dc0eb801e5eb52a00be7c0d3de360eb1952d`: tree `fb8197a78a94806a2bc7b7ec00ff6e8758788a12`; parents `7f1881e…`, `c7ca0ed…`.
   - `5eb80a7a0ee896d8189c85f9103c9f5df01e0112`: tree `2d2caa3f610626ac5f5219aad401590739c2fcfe`; parents `537741ce…`, `36a0dc0…`.
   - `888203c8c50e13938ca557e8aa0f1faf2101ff31`: tree `428f042b34fb1729d8fd45a112a1220af0fdae6a`; parents **`2facd7c…` (first)**, `5eb80a7…`.
   - `2facd7c0645755de400770fe4f2db641f46ba42e`: tree `e2bb3ac…`; parents `cd171f9…`, `36a0dc0…`.
   - `merge-base --is-ancestor` c7ca0ed→36a0dc0→5eb80a7→888203c: rc 0 at every step.
   - **Push order**, from `gh api repos/…/activity?ref=refs/heads/main` (04:56:22 AEDT), each `push` by `kamilDatasec`:
     - `c7ca0ed→36a0dc0` at 2026-10-18T10:43:23Z
     - `36a0dc0→5eb80a7` at 13:06:37Z
     - `5eb80a7→888203c` at 15:32:32Z
4. **First-parent vs ancestry, for trees:**
   - `fb8197a`: in a first-parent walk, none; in full ancestry, `36a0dc0`.
   - `e2bb3ac`: first-parent `2facd7c`; ancestry `2facd7c`.
   - `2d2caa3`: in a first-parent walk, none; in full ancestry, `5eb80a7`.
5. **`428f042` vs `e2bb3ac`:** `diff --name-status` gives:
   - `A __tests__/rd775-readiness-key-no-hash.test.js`
   - `M backend/services/aiReadiness.js`
   - `M scripts/verify-expected-counts.json`

   The RD-775 blobs at `888203c` equal `5eb80a7`'s: `578e7e7967152efd832e21e70644f15eaec1eb44` and `0cca0e04ee6e81ccd237d6907cb56a608d16bfda`. This matches ANSWER-18's own *"compare 2facd7c...888203c = exactly counts + aiReadiness.js + rd775 test"*.
6. **Counts** (`git show <c>:scripts/verify-expected-counts.json` → tests suites):

   | commit | counts blob | tests / suites |
   |---|---|---|
   | c7ca0ed | `fadda68` | 4559/287 |
   | 36a0dc0 | `6a55f68` | 4646/289 |
   | 5eb80a7 | `937927d` | 4651/290 |
   | 2facd7c | `a11d7ec` | 4655/290 |
   | **888203c** | **`f3f387bf989629f938e193927eb6599245471d0a`** | **4660/291** (`_updated` 2026-10-18T14:24:37.292Z) |
   | 3047ae9 | `2d803d7` | 4575/288 (= 4559/287 + 16/1) |

   **Prediction: 4660+16 = 4676, 291+1 = 292.** This is arithmetic only, not measured.
7. **WRONG 2 re-measure against `888203c`** (04:54:58 AEDT, git 2.54.0):
   - `diff --name-only c7ca0ed 888203c` = 25 paths; the intersection with RD-778's 7 is `scripts/verify-expected-counts.json` alone; main changed 0 `static/` paths.
   - The legacy `git merge-tree c7ca0ed 888203c 3047ae9` (rc 0, 520 lines) has exactly three kinds of section:
     - one `changed in both`: counts, with base `fadda68`, our `f3f387b`, their `2d803d7`;
     - one `added in remote`: `__tests__/rd778-dom-text-stays-text.test.js` `da3248b`;
     - five one-sided `merged` entries, one per static/js file. Each `result` equals `3047ae9`'s blob: `28eb133`, `9118081`, `a3bf04d`, `59aca9d`, `adaa340`.
   - Headers counted case-insensitively = 2.
   - The no-write check was taken on the correct git dir (`rev-parse --absolute-git-dir` = `…/NexusAI/2_Project_Files/.git`): `.git/objects` held 35 files before and after, and the newest mtime did not change.
8. **Other premises:**
   - Lock `19477a9` and package `384805d` at c7ca0ed, 3047ae9 and 888203c. The lock resolves proxy-addr 2.0.8, playwright and playwright-core 1.62.1, and jsdom 20.0.3.
   - deploy-demo is `953b2a2` at all three, with 2 `vars.CI_DEPLOY_ENABLED == 'true'` lines (:53, :91), 1 `branches: [main]` and 1 `paths-ignore:`.
   - `__tests__` file count: 341 / 342 / 347.
   - `escapeHtml` declarations at 3047ae9: settings.js :89 and :2436; chart-details :533; first-run-setup :2933; index :109. The WeakMap is at index.js :643.
   - C-170 is not landed: `be0fe37` is not an ancestor of `888203c`, and `arm-ttk.yml` is absent there.
   - Machine: `/Volumes` = Laptop-DEV, Macintosh HD, Recovery (**T9 unmounted**); Chrome 155.0.8059.84; node v26.8.1; gitleaks 8.30.1; load 4.71.
   - `models_latest.json` `levels.opus.model_id` = `claude-opus-5-5`.
   - Gates 25 and 26 reports read `STATUS: COMPLETE`.
9. **Quotes the launcher greps** were each confirmed present in both the source and the kit. This covers 19 CLARIFICATIONS quotes, the two driver-ruling quotes, the four READY lines, and ANSWER-1/12/16/18/19 and ADDENDUM-1.

**Observations for Tuesday (not amended — outside (a)–(d)):**
- **Payload line numbers.** The kit's THE MODEL RULE paragraph cites the builder's payloads at *"test :38-:39"*. At `3047ae9` they are at **:39 and :40** (`grep -n`). The launcher checks the strings, not the line numbers.
- **Object count.** NexusAI `.git/objects` now holds 35 files; the drafter saw 114 at 21:39. Something packed objects since. The kit's §7 still says "114 at drafting", and that is now historical.
- **Jest lock.** During `--check`, the Laptop-DEV jest lock was **held by `s101o-c170d-verify`**: S101O is running the C-170 delta verify (ANSWER-19 item 2).
- **Sequencing wording.** ANSWER-18 says *"Hold their re-pins until your MERGED mail"* and *"After C-170: Tuesday stamps and launches gate 27"*. ANSWER-19 then holds C-170 behind gate 28. This amendment re-pins gate 27 to `888203c` on the commission's instruction ("C-170 … will NOT land before this gate"). If C-170 does land before gate 27 launches, the launcher refuses at guard 18 ("main MOVED"), and both the kit tables and the launcher pins must be re-pinned.

## 3. Still open for Tuesday (12 at-sign SLOT placeholders remain)

- **10 × `RULED: @SLOT@`:** T0 (the re-pin mode; default (a) is the filled one), T1, T2, T3, T4, T5 (read twice: CDN), T6, T7, T8, T9.
- **`SELF-CHECK: @SLOT-SELF-CHECK@`** (kit line 25) and **`Self-check note: @SLOT-SELF-CHECK-NOTE@`** (line 26). Fill them LAST, by hand. The SELF-CHECK line must start `SELF-CHECK: re-read end-to-end for contradictions | `, the fleet form the launcher greps (gate 26 line 25).
- **Re-wording I did so the launcher's zero-placeholder rule can be met:** FILL AT STAMP used to name the slots with their at-signs, which would have counted as unfilled placeholders forever. Those lines now say "each `RULED:` slot" and "the `SLOT-SELF-CHECK` and `SLOT-SELF-CHECK-NOTE` slots".
- If T0 (b) is ruled, or main or the branch moves, re-pin **both** the kit tables and the launcher's pin block (`MAIN_SHA`, `H778`, `PRED_TESTS/SUITES`, and guard 18M's chain). Never `sed` a sha blindly.
- **Route line**, which Tuesday adds; this file has not been edited. Add this exact line:

  ```
  QA/NexusAI-gate27|tuesday-agent@agentmail.to|no
  ```

  It goes in `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/inbox_routing.conf` directly after gate 26's line. That line is at **:232**, the file's last line (232 lines); gate 25's is at :231 and gate 24's at :227. So the new line becomes :233.

## 4. Launcher verification (quoted)

`bash -n /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate27.sh` gives rc 0.

**First `--check`** refused at guard 81 on my own premise word `'exits 71'`; the kit says `(exit 71)`. I corrected it and ran again. **Second `--check`**, with the kit still slotted (`/bin/bash … --check`, exit 40):

```
NOTE: the Laptop-DEV jest lock is held now by 's101o-c170d-verify' (FIFO; the gate waits behind it)
NOTE: /Users/kamil/Library/Caches/ms-playwright exists (1 entr(y/ies)) — read its path + mtime before and after (ruling u)
NOTE: no tmux pane named 'Datasec/NexusAI-M' — not a negative control this launch
NOTE: no tmux pane named 'Datasec/NexusAI-N' — not a negative control this launch
NOTE: no tmux pane named 'Datasec/NexusAI-P' — not a negative control this launch
NOTE: no tmux pane named 'Datasec/NexusAI-R' — not a negative control this launch
NOTE: fleet-monitor has no single live claude — not a negative control
guards pass (9 MODEL 40 6 7 8 18M 18T 18 90 91 22 93 96 70 70N 31 39 10 17 11 12 13 14 15 20 41 82 19 24 53 71 76 77 78 79 81 38R 86); stamp, route and/or READY NOT complete.
  ls-remote attempts this run: 1 (C-192); origin main 888203c (landing chain 36a0dc0/fb8197a -> 5eb80a7/2d2caa3 -> 888203c/428f042 by ancestry); RD-778 3047ae9; pull/94 3047ae9; lock tool 3c33f5ae58e1…; c57 1ae84a108334…; c133 6f938bfcf255…; Chrome 155.0.8059.84; model claude-opus-5-5
  NEG seats (38R, derived live; coordinator pane 'tuesday'): `78171` (Datasec/NexusAI-O); `53331` (tuesday);
REFUSING (32S): 12 at-sign SLOT placeholder(s) remain in the brief (the RULED: slots T0-T9, the SELF-CHECK line and the Self-check note), or the SELF-CHECK line is not in the fleet's form — the coordinator re-reads end-to-end and stamps them before launch
REFUSING (40): no 'QA/NexusAI-gate27|tuesday-agent@agentmail.to|no' line in /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/inbox_routing.conf — answers to the gate would have no route; Tuesday adds it at stamp (this launcher never writes it)
EXIT=40
```

Every content guard passed against the amended kit and live origin. The script refused only on the stamp and the route, and no claude was started.

## 5. Hard limits kept

- NexusAI repo: read verbs only, with `--no-optional-locks`; no fetch, worktree or `--write-tree`.
- `gh`: GETs only.
- AgentMail: one GET listing plus one GET message; the key was never printed.
- No HTTP to any live or hosted host.
- Datasec only. I read only the files named by the commission or by the kit and launchers; I did not glob any shared folder for other clients' material.
- Nothing was launched or mailed, and `inbox_routing.conf` was not edited.
