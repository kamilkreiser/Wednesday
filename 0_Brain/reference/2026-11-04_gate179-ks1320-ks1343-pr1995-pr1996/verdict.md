NO GO (G179-F1) for PR 1995 | PR 1996: GO WITH NOTES — MERGE (no HOLD-FOR-KAM)

# QA Gate 179 (Tier 2, round 1): PR 1995 / KS-1320 and PR 1996 / KS-1343 (PARTIAL), Secuura/Distributed_Secuura, documentation only

## Per-PR verdict lines
- **PR 1995 (KS-1320): NO GO (G179-F1)**
- **PR 1996 (KS-1343, PARTIAL): GO WITH NOTES — MERGE (no HOLD-FOR-KAM)**

## Subject block
| | start (22:42:33Z) | end (22:47:15Z) |
|---|---|---|
| develop | `ee1e1b83211504f96ebccba325d1ef7139bc83cc` | same |
| refs/pull/1995/head | `15c32a6ef6b6d37b812dfc2b7329e12c87202b03` | same |
| refs/pull/1996/head | `6ccdccb07199e8260f675ad2dd851ea42025a4bc` | same |

Both PR parents = `ea5134d6b98c470615c59fca5d3ec30356adfbd7`, one commit each. Nothing moved. Host: git 2.54.0 (Apple), Node v26.8.1 (not used; no tests apply to a docs gate). Run on macOS only.

Method: shared clone in `repo/` (no checkout), PR refs fetched into it, base/head read with `git show`/`git grep` at the PR head refs (every file named below was read at head, not from a working tree). Merge tests via `merge-tree --write-tree` in my clone only. The project checkout was touched only with `ls-remote`, `config` reads and `git clone --shared`. PR title/body and the KS-1343 comment live on GitHub/Linear and could not be read (the repo is private and no `gh` login is available in this shell; I did not use the project's stored token): the commit message and commit subject stand in for title/body.

## Findings

### G179-F1 — HIGH — FIX-BEFORE-MERGE (PR 1995): CONTRIBUTING.md states two things the repository does not show: that "the merge gate finds" an over-long squash subject, and that the subject must be "ASCII only"
**FOUND.** The added text (CONTRIBUTING.md:107-109 at head) says the squash subject "must be 92 characters or fewer and ASCII only", and that "nothing rejects a longer title when the PR is opened; the merge gate finds it, and a replacement subject then has to be written".
- Nothing in the repository enforces 92: `git grep -w 92` over `*.sh *.md *.yml *.yaml *.py *.js *.mjs *.ts` and `.githooks` returned only the new CONTRIBUTING lines plus unrelated hits (pricing text, minified JS, a test-report row). The one `.githooks` file (`pre-push`) and the 20 `.github` files hold no PR-title or commit-subject check (grep for `pull_request.title`, `PR_TITLE`, `commit-msg`: 0 hits; Actions are retired anyway).
- The only enforcer I found is outside the repo: the seat tool `5_Project_History/2026-11-02_seatV-17th/tools/subject_check_ks_v17.sh` (lines 11-14: `wc -c` over 92 refuses, rc 1; must start `Refs <KS-key>: `; no `(#n)` suffix). It counts BYTES, not characters, and has no ASCII test (`grep -c -i ascii` over it, create_pr_v17.py and check_body_ks_v17.py = 0 each). Seat Handover E 24th (HANDOVER.md:11) states the same 92 as a seat convention.
- The merge tool does not check it: `5_Project_History/merge-protocol/merge_squash_v3.sh` PUTs `{"merge_method":"squash","sha":...}` only (line 336), sends no commit_title, and the only subject lines are `say` logs (223, 380). The three `run_merge.sh` copies (s211, s220, s228) have no hit for subject/92/ascii/commit_title. So "the merge gate finds it" is not shown by any merge code I could open; GitHub's default squash title is then the PR title, unchecked.
- So: "92 or fewer" is true as a fleet convention enforced at PR creation by a seat-side tool outside the repo (not by a merge gate); "ASCII only" has no enforcer at all in anything I read; "the merge gate finds it" is unsupported. A repo doc that tells authors a gate exists, when none was found, claims more than the repository shows.
**TESTED.** Read the 3 enforcement candidates above and grepped the repo at head. Did NOT test: the merge seat's live practice (a human or a tool I did not find might check the title at merge), GitHub branch-protection or ruleset settings (not readable), ticket KS-1320's own evidence (R 81st may hold it).
**HOW.** `git grep` at refs/pr/1995 with controls: `MULTI_TENANCY_ENABLED`-style positive fire seen on the same repo (24 hits in docker-compose.yml, so the grep reaches yml); `-w 92` fired on the new CONTRIBUTING lines themselves. Suggested fix (finding only): reword to what is shown ("a seat-side guard refuses a subject over 92 bytes at PR creation; nothing in this repository or the squash PUT checks it"), drop "ASCII only" or cite its enforcer, and drop or cite "the merge gate finds it".

### G179-F2 — LOW — NOTE (PR 1996, PRE-EXISTING, base = head): line-number citations beside the changed sentence are stale
**FOUND.** The changed bullet (MULTI-TENANCY.md:54-57) and RLS-FAIL-CLOSED-PLAN.md:50-51 cite `tenant-pool-manager.ts:151/152`, `tenant-provisioning/src/index.ts:245` (also MULTI-TENANCY.md:176 `:245-274`, "INSERT at `:271`") and `services.bicep:798`. At head: MULTI_TENANCY_ENABLED is read at tenant-pool-manager.ts:**153**, PROVISION_PER_TENANT_DB at **154**; the flag read in tenant-provisioning/src/index.ts is at **275** (245 is inside the INSERT block start region; the INSERT text is at ~246-247); the bicep setting is at services.bicep:**818**. `env.dev.json:7` and `env.demo.json:7` are correct. The PR did not touch these citations; the source files are unchanged between base and head. The facts cited are true; only the line numbers drifted. Not a NO GO (does not claim more; a reader still finds the flag by name).
**TESTED.** Opened each cited line at both base and head (same). **HOW.** `git show <ref>:<file> | grep -n process.env` etc.

### G179-F3 — LOW — NOTE (PR 1996): the new RLS wording is narrower, true, but the pair of docs still says "database-level" without defining it
**FOUND.** "the only database-level tenant isolation that exists" (RLS-FAIL-CLOSED-PLAN.md:55) is true by what I could see: the per-tenant-database path is gated by `perTenantDbEnabled` (tenant-pool-manager.ts:235, set only from the option or the env flag; no caller passes `perTenantDbEnabled: true`; 0 hits in tests); migrations hold 18 files with `CREATE POLICY` and 35 `FORCE ROW LEVEL SECURITY` lines; the only other roles/DB-level mechanisms are the `secuura_auth_lookup` role and SECURITY DEFINER lookups, which are exceptions to isolation, not isolation. Unclear to a reader: the doc does not say what non-database isolation (application tenant filters) does exist. True and not misleading ("database-level" is the narrowing), so NOTE only. Whether RLS actually binds the live app role (BYPASSRLS / owner) was not checked and is not claimed in this sentence.
**TESTED.** Static grep of migrations and pool-manager; no database driven. **HOW.** `git grep` at refs/pr/1996.

### G179-F4 — INFO (my instrument): my close-word scan hit "FAIL-CLOSED" in PR 1996's commit message (RLS-FAIL-CLOSED-PLAN.md filename). Not a ticket-closing phrase. Commit message only; the GitHub PR body was not read.

## What passed (measured)

**Q1 truth (PR 1996), every changed sentence, quoted:**
1. MULTI-TENANCY.md:53 "they are in different states" (dropped clause "a distinction the first version of this correction got wrong" removed: removes a statement, adds nothing). OK.
2. MULTI-TENANCY.md:54-57 "`PROVISION_PER_TENANT_DB` ... is set in no configuration file in the repository ... in the repository it is off everywhere; live app settings were not checked": whole-repo `git grep -I PROVISION_PER_TENANT_DB` at head, excluding `*.md` and `*.ts`: 3 hits, all `Projects Documents/fragments/*.html` prose about the flag (no value set); `.ts` hits: tenant-pool-manager.ts:52,154,228 (flag read/comments), tenant-provisioning/src/index.ts:268,275,597 (flag read/comments) and tests that save/restore it. 0 config, compose, bicep, `.env.example`, `env.example` or JSON sets it. Control from the same action: the identical grep for `MULTI_TENANCY_ENABLED` returns 17 files (.env.example, env.dev/demo.json, services.bicep:818, docker-compose.yml 24 hits), so the grep reaches those file types. Read-off code defaults to false: tenant-pool-manager.ts:154 `=== 'true'`; index.ts:275 `=== 'true'`. TRUE as written, and the limit (live app settings not checked) is in the sentence itself.
3. MULTI-TENANCY.md:58-61 unchanged context: `env.dev.json:7`, `env.demo.json:7` "true" (read), `services.bicep:818` `{ name: 'MULTI_TENANCY_ENABLED', value: 'true' }` (cited as :798, F2).
4. RLS-FAIL-CLOSED-PLAN.md:55 see F3. TRUE.
**Q1 (PR 1995):** 92 limit: see G179-F1. The adjacent sentence "Feature PRs into `develop` stay squash" is old text.
**Q2 what was not checked:** PR 1996: the live-settings limit is IN the doc text (MULTI-TENANCY.md:56-57). The RLS sentence makes no live-settings claim, so none needed. PR 1995: the text states what nothing rejects but not that the merge-gate claim was not verified (F1).
**Q3 scope:** `git diff --stat` PR 1995 = 1 file `Blockchain/Dev/CONTRIBUTING.md`, +3/-1; PR 1996 = `Blockchain/Dev/docs/MULTI-TENANCY.md` +3/-2 and `Blockchain/Dev/docs/RLS-FAIL-CLOSED-PLAN.md` +1/-1; one commit each on `ea5134d6b98c`; 0 code/test/config/fragment paths. PR 1996 commit message says "They cover notes N-1286-4, N-1286-7 and N-1286-8 only, so the ticket stays open": no claim that -3/-5/-6/-9/-10 are done. NOT read: PR body on GitHub and KS-1343 comment `fa23c3ab-...` (access), so "PARTIAL stated in body/comment" is NOT confirmed by me; it is in the commit message and R 82nd's READY mail.
**Q4 merge (my clone, full 40-hex):**
- 1995 onto develop `ee1e1b83...`: rc 0, tree `2aa2a0686f94ddc8af24e72d5c266ebadbb9e938`.
- 1996 onto develop `ee1e1b83...`: rc 0, tree `f4418c5659bb5b30d8d417bae0c36d509fb43bf6`.
- 1996 onto develop-plus-1995: rc 0, tree `fc097335f63e416838e03435d28f97801a2e3db0`; the other order (1995 onto develop-plus-1996) gives the same tree `fc097335f63e416838e03435d28f97801a2e3db0`, rc 0. Develop's own tree `ce7a5d0d1a99a2f734011df3799b0d597ff4df11`.
- Expected squash trees for the merge seat: 1995 first = `2aa2a068...e938`; then 1996 = `fc097335...3fc0`; if 1996 goes first, `f4418c56...bf6` then `fc097335...3fc0`. (A squash tree equals the merge-tree tree here since each PR is one commit on a parent that is an ancestor of develop and there is no change the merge reorders.)
- Shared paths 1995 vs 1996: 0. Controls in the same action: the same compare of 1995 against itself = 1 shared path; a planted conflicting edit of the same CONTRIBUTING line on the shared parent merged with 1995: rc 1 with stages 1 and 2 listed (so merge-tree can fail).
- Whole `git diff --stat develop..merged(both)` = 3 files, +7/-4, only the three named docs.
**Q5 hygiene (commit message as proxy; PR title/body on GitHub NOT read):** subjects start `Refs KS-1320: ` / `Refs KS-1343: `, 84 and 87 bytes (= chars), both <= 92, 0 non-ASCII. Added lines 3 and 4, 0 non-ASCII characters (control: one planted non-ASCII char counts 1). Close-words: 0 in 1995, 1 hit in 1996 = "FAIL-CLOSED" file name (F4; control `This fixes KS-1` = 1). `@`: only the `noreply@anthropic.com` Co-Authored-By email (an address, not a mention); control `cc @bob` = 1. Secret-shaped strings (ghp_/AKIA/PEM/40+ hex/JWT): 0 in both; control `ghp_...` = 1. Test Evidence block: NOT checked on GitHub (body unreadable).
**Q6 (PR 1995):** answered in F1. 92 is a seat-side convention (byte count) at PR creation; nothing in the repo and no merge script I read enforces it; nothing enforces ASCII-only.

## NOT tested
- PR title and body as they stand on GitHub (Test Evidence block, "Refs" title, close-words in the body) and KS-1343 comment `fa23c3ab-...`: unreachable (private repo, no login). Checked only commit subject/message.
- Whether the live apps (dev, demo, production) set `PROVISION_PER_TENANT_DB` or `MULTI_TENANCY_ENABLED`: not checked, and PR 1996's text says so.
- Whether RLS binds the live application database role.
- The merge seat's real practice at merge time and any GitHub ruleset/branch-protection that might check a subject; only the scripts named in F1.
- Markdown link validity; rendering; any test or suite (none exist for these paths); Spark shadow (not run, per commission); the pre-push hook run recorded in the READY mail (relayed, not re-run); containment against the held READY files (relayed from R 81st/82nd).
- Reachability/exposure words: I do not claim any. "Off everywhere" is "in the repository" only.

## Plain answer for Kam
PR 1996 is safe to merge as it stands: it only makes two sentences in the multi-tenancy docs more careful, saying a setting is off "in the repository" (not that the live apps were checked) and that row-level security is the only "database-level" isolation. Every fact in those sentences checks out against the code and config; a few line numbers beside them are out of date, and that was already so before the PR. PR 1995 should not merge yet. It tells contributors that the merge gate will catch a squash subject over 92 characters and that it must be plain ASCII, but I could not find any merge gate, hook or workflow that does either check; the only check I found is a seat-side tool that refuses over 92 bytes when a PR is created. Reword it to what is actually checked, or point to the real gate, and it is a clean docs change. Neither PR changes any behaviour for users; both touch documentation only, and the two do not collide with each other or with develop.
