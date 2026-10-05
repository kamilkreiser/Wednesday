# KS ticket audit — shared spec for the three read-only auditors (Wednesday, 2026-10-05)

**Kam's words (live board, 13:02-13:03):** "go through all the tickets … I want to know whether these are genuine issues or whether the agents are just adding things that are not genuine problems." · "I need to get to a state where the platform is stable and ready by the end of the month." · "also archive anything that can and should be archived."

**You are READ-ONLY.** Linear (key `LINEAR_API_KEY` sourced transiently from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env`, never printed or copied) and GitHub REST (`GH_TOKEN` the same way, GET only) and read-only git (`show`, `log`, `grep`, `cat-file`, `ls-tree`) in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` at origin develop (`3ce8cd4026a6` at 13:00; if a SHA is absent locally, `git clone --shared` into YOUR scratch dir and fetch there with the checkout's own `core.sshCommand`). NO writes to Linear, GitHub, or anything under `!CODING`. No `rm`. Your ONLY writable places: your output file in this folder, and `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/707ca275-d40c-45a7-8ba2-785b7c4e078a/scratchpad/ksaudit/<your-letter>/`.

**Input snapshot:** `ks_all_2026-10-05T0205Z.json` in this folder (1,396 issues; fields: identifier, title, priority, createdAt, completedAt, canceledAt, archivedAt, state, creator, assignee, labels, parent). Fetch descriptions, comments (`comments(first:50)`, sort client-side — `last:N` returns the OLDEST), attachments and relations per ticket as you need them; keep GraphQL complexity under 10,000 (small pages).

**Classification — one row per ticket, exactly one CLASS:**
- `GENUINE-DEFECT` — a real product defect, reproducible or provable at develop by a cited file:line read NOW.
- `GENUINE-HARDENING` — real but not a defect (defence in depth, a missing guard with no exploit path shown).
- `TEST-OR-TOOLING` — test coverage, harness, CI, docs, process; not product behaviour.
- `ALREADY-FIXED` — the cited code at develop no longer has the problem (cite file:line + the merged PR/commit), or a merged PR closed its scope.
- `MERGED-AWAITING-SWEEP` — its fixing PR is MERGED (GitHub API `merged_at`), the ticket is open only for a live check (skill §5f).
- `DUPLICATE` — same defect/ask as a named survivor (survivor rule: the one with the fixing PR; else the older id; else the one a client human wrote). Overlapping-but-distinct is NOT a duplicate.
- `NOT-GENUINE` — speculative, unreproducible, based on a misread, or an agent's internal process note filed as a ticket. Say WHY in one clause.
- `NEEDS-HUMAN` — needs Kam, Peter or Stuart to decide; name who and what.
- `UNVERIFIED` — you could not establish the class; say what would settle it.

**Every row also carries:** creator · assignee · state · priority · age (days) · on the critical path to "stable and ready by 31 Oct"? (yes/no/unknown, one clause) · ARCHIVE? (`yes` only for: Done/Canceled not archived; DUPLICATE; ALREADY-FIXED with the proving cite; `no` otherwise — and NEVER `yes` for a ticket assigned to or created by Peter or Stuart: those go to `ASK`) · the instrument for the class (the file:line, PR number + merged_at, survivor id, or "title/description only").

**Discipline (these are the ones that bite):** a class from a title alone is a REPRESENTATION — mark the instrument "title only" and do not use `ALREADY-FIXED`/`DUPLICATE`/`NOT-GENUINE` on title alone. Every zero gets a control. A parent ticket's children are listed; archiving a parent cascades to children — say so on the row. Do not trust the board's state names ("Deployed to UAT" describes demo, legacy).

**Output:** `audit_<letter>.tsv` (header row; tab-separated; one row per ticket in your partition, ALL of them — state your count against the partition's expected count) + `audit_<letter>.md` (BLUF: counts per class; the top 10 genuine defects by risk to the 31 Oct goal; what you could not verify; your method incl. controls). Terse.
