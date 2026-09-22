# KS-1097-Db R16B-CLAUDEMD - re-brief at develop 8c2f7b3fd of READY_KS-1097-Db_ornith35b-q4_DOCPATCH-RECOUNT-PASS-7of7_2026-09-15.diff.md - **DOCUMENTATION (repo-root `CLAUDE.md`, no code)** (written 2026-09-22 12:56:58 AEST by Wednesday's feed11 drafter; the hunk is the old READY's applied PASS output re-anchored at the tip - the old `:256`-`:258` site is `:266`-`:268` now (+10); every context and `-` line read from `git show 8c2f7b3fd:CLAUDE.md` byte for byte, header recounted, the `+` line ASCII)

Tip: 8c2f7b3fd4fde915b2a24542bc32259b24e092a0
File: `CLAUDE.md`

## What is wrong (one paragraph)
KS-1097 carries six Polish findings from the tier-2 gate on PR #957 (KS-1095). **This part fixes the ONE site in the repo-root `CLAUDE.md`** (QA-957-2): the `*[NOT APPLIED (2026-09-11, KS-1095): ...]*` annotation at lines 266-268 says "Kam has ruled on the required-approvals setting and that ruling is not yet applied" without naming the ruling. It becomes ONE line that names it: the pending ruling is raise-to-1 (Kam's card `secuura-required-approvals-zero-after-the-untick`; Kam applies it himself; not yet applied), and says plainly "do not turn it on while fleet PRs carry 0 GitHub reviews: it would block every fleet merge". Three lines become one; the sentence before (`:265`, "then (2) add the check names to the develop AND") and after (`:269`, "Environment-based sign-off jobs were removed ...") are untouched context. Nothing else in the file changes. Parts A (`docs/DEV-PROCESS.md`), B and C (`CONTRIBUTING.md`) are briefed separately - ONE docs PR for all parts. The project-root untracked `CLAUDE.md` mirror is done by hand after merge (the ticket's note).

## The exact change - 1 hunk in `CLAUDE.md` (3 `-` line(s), 1 `+` line)
Copy the block below BYTE FOR BYTE as your whole diff: the two file-header lines, the `@@` header, the two context lines (a leading space, copied from `files[product_file]`), the three `-` lines and the one `+` line, in this order. Do not add, drop, re-wrap or reword a line; never write a literal `\n` inside a line. The `+` line is ASCII: the old READY's em-dash before "do not turn it on" is written ` - ` (the standing non-ASCII-0 rule on `+` lines).
**A `-` line is a byte copy of the tip line - exactly the characters the file has, no more.** Today's KS-1097 PRPROCESS round FAILed D2 twice on ONE model byte each time: an extra `*` on a `-` line (deterministic - the same byte both rounds). Here the `-` line at 266 ends `KS-1095): Kam has` (no asterisk at its end) and the `-` line at 268 carries `merge.]* The former` with ONE asterisk after `]`. Count them from `files[product_file]`, not from memory. The header is `@@ -265,5 +265,3 @@`: old side 5 lines (2 context + 3 `-`), new side 3 (2 context + 1 `+`).
```
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ -265,5 +265,3 @@
   so a missing box/ticket fails the check, then (2) add the check names to the develop AND
-  main `require-pr-gates` rulesets and turn on required reviews = 1 (any writer). *[NOT APPLIED (2026-09-11, KS-1095): Kam has
-  ruled on the required-approvals setting and that ruling is not yet applied; turning required reviews on
-  while fleet PRs carry 0 GitHub reviews would block every fleet merge.]* The former
+  main `require-pr-gates` rulesets and turn on required reviews = 1 (any writer). *[NOT APPLIED (2026-09-11, KS-1095): the pending ruling is raise-to-1 (Kam's card `secuura-required-approvals-zero-after-the-untick`; Kam applies it himself; not yet applied) - do not turn it on while fleet PRs carry 0 GitHub reviews: it would block every fleet merge.]* The former
   Environment-based sign-off jobs were removed in favour of this checkbox approach.
```

## Where (every **must change** line must appear as a `-` line in your diff, at its number)
- `:266` - **must change**: `  main `require-pr-gates` rulesets and turn on required reviews = 1 (any writer). *[NOT APPLIED (2026-09-11, KS-1095): Kam has`
- `:267` - **must change**: `  ruled on the required-approvals setting and that ruling is not yet applied; turning required reviews on`
- `:268` - **must change**: `  while fleet PRs carry 0 GitHub reviews would block every fleet merge.]* The former`
- `:265` - (correct) `  so a missing box/ticket fails the check, then (2) add the check names to the develop AND` - stays
- `:269` - (correct) `  Environment-based sign-off jobs were removed in favour of this checkbox approach.` - stays

## Required (the checker's proof - each token ABSENT in the section before, PRESENT after)
- `## Branching` :: the pending ruling is raise-to-1, Kam applies it himself

## Output
Exactly ONE ```diff block, ONE file section `--- a/CLAUDE.md` / `+++ b/CLAUDE.md`, 1 hunk with the header and counts exactly as in `## The exact change`. No prose before or after the block.

## Premises (measured at develop 8c2f7b3fd4fde915b2a24542bc32259b24e092a0 by the feed11 drafter, scratchpad `--shared --no-checkout` clone, 2026-09-22 12:56:58 AEST)
- Repo-root `CLAUDE.md` at the tip (495 lines) carries every context and `-` line of the hunk above BYTE FOR BYTE at the line numbers in `## Where` (read by write_doc_1097Db.py from `git show 8c2f7b3fd:CLAUDE.md`; the hunk's old side matches exactly ONE place in the file - asserted); the old READY's `-` lines are at `:266`-`:268` (the old `:256`-`:258` moved by +10), its `+` line absent (FEED 10 `fresh1097.out`).
- section `## Branching — Git Flow (adopted 2026-05-25, KS-137)` = `:241`-`:325` at the tip (the site lies inside it); both tokens 0 in that range before (asserted here) and in the `+` line above.
- Ticket KS-1097 on the Secuura board at drafting time: In Progress, not archived (`board_states.log`); the same state under which FEED 9's two KS-1097 doc rows were queued and ran today. The repo-root `CLAUDE.md` is on neither live seat's GROUPING list and no held READY touches it.
