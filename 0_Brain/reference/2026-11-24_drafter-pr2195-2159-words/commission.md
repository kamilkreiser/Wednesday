# COMMISSION (Wednesday, 2026-11-24): what "Wednesday's words" PRs 2195 and 2159 need — read-only research, Sonnet

## Goal
Two open Secuura PRs have been carried for ~2 weeks as "need Wednesday's words before any READY":
- PR 2195 (Secuura/Distributed_Secuura) "Refs KS-1988, KS-2075: the migration readiness probe parses a URL with no port or host, and observability down survives an absent redis container" — OPEN, MERGEABLE, head 3eed5f75fa28, updated 2026-11-11T19:27:59Z (gh read by Wednesday 2026-11-24).
- PR 2159 "Refs KS-2111: the settings PUT and the Settings page refuse a category named __proto__, constructor or prototype" — OPEN, MERGEABLE, head 7b54e7cbb6f0, updated 2026-11-10T00:45:53Z. Notes say "held on gate 301" and "2159-only waiver".
Find out EXACTLY what decision is pending on each, who owns it (Wednesday's own ruling under her grants, or Kam's), and draft the ruling text.

## Where to read (read-only; never write outside this folder)
- Wednesday's gate folders: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/ — list it (do NOT grep it recursively); open the folders whose names or verdicts concern PR 2159 or 2195 (start with 2026-11-10_gate301, then gates whose commission.md names 2159 or 2195; you may grep ONE named file at a time).
- Daily notes /Volumes/DevMASTER/WEDNESDAY/0_Brain/daily/2026-11-10.md, 2026-11-11.md, 2026-11-12.md, 2026-11-20.md (grep -i for 2159 / 2195 in each named file).
- GitHub, read-only: export GH_CONFIG_DIR='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.gh-config' then `gh pr view <n> -R Secuura/Distributed_Secuura --json body,comments,reviews,files,headRefOid` (read text bodies containing backslash-u sequences via `gh api` piped to python only if needed; report which transport you used).
- Kam's rulings: bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list all (read-only listing; read its usage line first) — search for cards naming 2159, 2195, KS-2111, KS-1988, KS-2075.
- Current develop: b69addc39652 (Wednesday, 13:28). Whether each PR still merges cleanly on it: `gh pr view` mergeable field only; NO git fetch, NO worktree, NO write into any project checkout.

## Output (write ONLY this file)
/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-24_drafter-pr2195-2159-words/findings.md, BLUF-first. Per PR:
1. What is held and why (quote the gate verdict line / note line with its path).
2. Whose decision it is: Wednesday (cite the grant or rule) or Kam (signature class or no grant).
3. Any Kam card already ruled on it (card id + ruling verbatim) or "none found (searched: <terms>)".
4. Recommended ruling text, ready to paste into a K drafter commission, and whether the PR then needs a re-gate (tier) or a rebase measure.
5. What you could not establish ("not measured").
Three fields for every claim: found, tested, how. No ticket writes, no PR comments, no mail, no edits anywhere else. Stop and say so if anything would need a write.
