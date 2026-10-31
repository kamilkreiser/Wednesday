STARTABLE: YES

# B1033 drafter report (SEAT-R109, HPSM-POC records for PR #269, security preview part B)
Drafter: Agent-tool sub-agent for Tuesday, 2026-11-01 10:26 to about 10:50 AEDT. Kit: `briefs/2026-11-01_B1033_SEAT-R109_hpsmpoc-records-269-security-preview-part-b.md` (81 lines; 13 stamp slots plus the last line = **14** four-underscore lines, measured by `/usr/bin/grep -c -E '_''_''_''_'`; `@[A-Z_]+@` 0; non-ASCII 0). `.pre-stamp` made with `cp -n`, `cmp` equal, sha256 both `5c43dd5d567b1c9d52892768b2fa515f2122eeb0aa5b8b3b57fe1f42d5854278`. Template: the B1014 kit, report and STATUS (read whole); cap-landing precedent records C-245 (part A).

## BLUF
- #269 is as you said: squash `1f4bf7bc` merged 10:24:35 AEDT, one parent `77c3132e`, 31 files +1072 -39, tree `670120e9` = the tree of gated head `7f0d832d`; code main still `1f4bf7bc` (10:26). The squash message equals B1027's two data files byte for byte (mutant control unequal). **Post-merge CI was still running at 10:3x:** `ci` 41252413621 in_progress, 6 of 17 check-runs in_progress; the kit has the seat write it AS READ.
- Next free C-number **C-259** (records main `06e8d8f9`, highest heading C-258 at line 5018). One entry.
- Done rule: `CLARIFICATIONS.md:1904` on records main (merged, gated and deployed). #269 is not deployed, so HPSMPOC-388 gets ONE comment and no transition. HPSMPOC-388 has 0 comments now, Backlog.
- The residue ticket for B1027-1 (default FILE) follows part A's cap precedent (C-245 ticketed its residue; HPSMPOC-414's shape). No B1027-1 ticket exists (searches 0). The next key is expected to be HPSMPOC-427 (`key = HPSMPOC-427` 0).
- The ruling: card read with `decision_queue.sh show`: ruled, choice a, 10:04:36 AEDT. The card text names no veto, so the kit records the five items as accepted as built (slot VETO-RULING confirms it).
- **Correction to the brief and the gate's fix-shape:** "red under g18 and g18b" cannot hold for the new row. With two scored runs the newest is both `runs[0]` and `top`, so g18 gives the head's answer. The kit forbids writing "red under g18" in any record or ticket. KIT 2 measures it.

## Facts re-measured (instrument; control)
- PR #269 (`gh api -X GET pulls/269`): merged true, `merged_at` 2026-10-31T23:24:35Z, head `7f0d832d`, base `77c3132e`, 4 commits, 31 files, `merge_commit_sha` `1f4bf7bc`. Commit: 1 parent, verification valid, 31 files, tree `670120e9` (= `commits/7f0d832d` tree). Compare `1f4bf7bc...main` identical. Open PRs 0 on both repos.
- Squash message: 18 lines, 3671 bytes, non-ASCII 0, `localdomain` 0, one `Co-Authored-By` (last line), `B###` 0. It equals subject + blank + body of B1027's files (True; mutant False). Line 14 states what is NOT pinned.
- Records: main `06e8d8f9` (PR #161); `records/b1033` 0 (control `records/b1014` 1). CLARIFICATIONS 5035 lines, 258 headings. The C-259 boundary pattern gives 0/0/0 (control C-258 1/13/1). `B1033`, `B1027`, `HPSMPOC-388`, `PR #269`, `1f4bf7bc` all 0 in the three files (control `PR #253` 6). The tree lacks all four chain STATUS files (control: B953/B965/B1003/B1010 present 4).
- STATUS files (sha256 prefix / lines / bytes / mtime / last line): B1016 `55a2d119100724db` 165 37773 06:33:39 READY FOR QA; B1022 `5ab70f50a86ffa17` 236 55246 07:27:11 VERDICT NO GO (1 of 2); B1025 `78559bdcd66169a4` 134 23867 08:00:18 READY FOR QA; B1027 `a4b52fc661116ec2` 255 51841 08:37:59 VERDICT NO GO (2 of 2).
- Catch-up scans (python byte program and greps; login held as a shell variable from `gh api user`, never printed, control 3 hits in SETUP_RUNBOOK; planted high-byte control 2): logins 0 in all four. E-mail shapes: B1025:92 and B1027:208 `noreply@anthropic.com`, B1027:39 `git@github.com`. No copied STATUS on records main carries either address (B953, B965, B1003, B1010: 0 each). `HP Reporting` B1022:233 and B1027:252 are not-opened statements. non-ASCII, tabs, "main is green" and `HP Restricted` are 0 in all four.
- Jira (`.tools/b1014/read.py`, `search.py`, `desc1014.py` in place; GET only): HPSMPOC-388 Backlog (new), 0 comments, label design-v12. HPSMPOC-387 has 2 comments (40306 landing, 40334 deploy) and is still Backlog. HPSMPOC-414 is part A's residue form. Newest key 426. `created >= "2026-11-01 00:00"` lists only 426. Controls: `HPSMPOC-268` 1, `qxv9k2zzprobe` 0. `B1027|g18b|B1022` 0; `B1016|B1025` 0.
- D43: kit line 4 pins `S` = `77c3132e`; its STATUS reads `DEPLOY B1031: PENDING` / `CHECKPOINT CI green | ... 10:30 AEDT`. Kit lines 45, 105 and 110: no Jira and no records writes.
- Seat and number: `R109` 0 kits in `tuesday/briefs/` and 0 in today's project STATUS files, word-bounded (control `R108` 2 kits, `R103` 4 STATUS). `B1033` 0 names in both folders. No R109 pane. `.tools/b1033` and `.tools/wt-b1033` absent (control `.tools/b1031` present).
- Model: `model-routing.md:98` C8, `:97` C7; `models_latest.json:23` `claude-sonnet-5-5`; `brief_seat.sh:24` defaults to opus, so the launch line carries `BRIEF_SEAT_LEVEL=sonnet`.
- Fixed Jira texts scanned by program (ASCII; no backtick; no HP word, phase, day words, plant ids, finding ids, `A$`, `localdomain`, seat names or the companion brief number; B-numbers only B1016/B1022/B1025/B1027/B1033; planted controls fire): 0 hits. `<TW-SUMMARY>` is 231 characters. Card id in the kit: 0. Person names: 0 (control fires).

## D-decisions
- D-1: one C-entry (C-259) in C-245's cap-landing form. The g18 correction goes in as a records note, never as a gate finding.
- D-2: Jira texts carry base B-numbers only, following B1014. Part A's residue summary used `[B965-1]`; this kit uses `[B1027]`.
- D-3: no priority is set on the new ticket (`create.py` sets none). Part A's residue was filed at High by its seat.
- D-4: the sixth gate veto item (12 px hint, B1022-10) was not on the card. It is rowed as having no ruling: neither accepted nor vetoed.
- D-5: the gate script needs B1022 and B1027 in `BRANCH_PR`, because their file names would misparse as PR 388. A gate kit for the `b1034/...` branch maps to "no PR" (ignored), so the companion lane cannot block Step 8.
- D-6: D43's live deploy is not a stop, because it is pinned to `77c3132e` and holds none of #269. REFUSE 8 fires only on a target that holds #269.
- D-7: KIT 1 and KIT 2 share no path, repository or Jira write (records repo + Jira vs code repo). They may run at the same time; the only shared object is the `.tools/.git-lock` wait.

## Q-questions for Tuesday (each with a default)
- Q-1 TICKET-WRAP: default **FILE** (cap rule plus ruling "ticket the missing test"; C-245 precedent). NONE leaves a BACKLOG row only.
- Q-2 CARRIER: should the records say a test-only lane was commissioned for the fix-shape? Default **LANE**, which means file the ticket AND build it with B1034. Jira text names no lane either way.
- Q-3 CATCHUP-LIST: default **B1016, B1022**. B1025 and B1027 are HELD by the e-mail rule unless you allow `noreply@anthropic.com` and `git@github.com` in the slot. B1027 is the verdict file and is worth allowing.
- Q-4 VETO-RULING: default **NONE-ACCEPTED-AS-BUILT**. Change it only if the product owner's reply did veto an item; the seat then STOPs.
- Q-5 DONE-SLOT: **COMMENT-ONLY** (the only value).
- Q-6 DEPLOY-STATE: write D43's first and last line and its target at stamp. If D43 has moved to a sha holding #269, do not launch.

## UNMEASURED
- The push of `records/b1033` (not run). The hosted state of UAT (D43 running).
- The final state of the post-merge `ci` run on `1f4bf7bc`.
- That the landing was head-pinned and its hosted checks (relayed from your brief).
- The C-scan over every records ref (main only).
- Whether the product owner said anything beyond option a: the card's `ruling` field holds only the choice and its time.

## Outside the fences (disclosure)
- Read-only throughout. I wrote only these kit files, their `.pre-stamp` copies and this report.
- `decision_queue.sh show` was run once, as instructed.
- I ran `.tools/b1014/read.py`, `search.py` and `desc1014.py` in place (Jira GET only; `read.py` printed comment bodies, not authors). `gh api -X GET` only; the login was read with `gh api user` into a variable and never printed. A python read of the shared repo's `.git/config` tested the key path, which was not printed.
- Scratch copies (records blobs, squash message, PR body) are in the session scratchpad only.
- One background grep across every Datasec project's Briefs folder timed out and was stopped with TaskStop (read-only). The narrower scans above replaced it.
