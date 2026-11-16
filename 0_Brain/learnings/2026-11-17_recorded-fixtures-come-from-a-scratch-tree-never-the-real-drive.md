---
date: 2026-11-17
type: lesson
source: Friday, self-found through a pre-publication sweep she commissioned (no harm: the repository was still private)
status: live
tier: M
---

# A recorded test fixture is made from a scratch tree the seat builds, never from the real drive: raw tool output carries whatever the drive holds, and a repository's history keeps it

**The lesson:** A build seat that records real tool output as a fixture (a search, a directory listing, a debug log, a session stream) copies into the repository whatever that tool happened to walk: other projects' names, the user name, the drive's folder layout, memory paths. Once committed it is in the history, and removing the file later does not remove it. In a repository that will be opened, or that belongs to a different client from what the tool walked, that is a leak waiting for one click.

**The case (2026-11-17, General project, repository private at the time).** Kam ruled the repository "open from the first commit". Before handing him the link, Friday commissioned a read-only sweep of every branch and all 79 commits. It found no secret, and it found recorded spike logs holding two project names of one of his clients (one file), his Mac user name (7 files) and the drive layout (115 files on main), present in almost every commit. Friday confirmed the counts at source with `git grep`. The spike seat had recorded real search output from the workspace; its brief said nothing about where recorded output may come from. Kam was told not to make it public and carded with three ways forward.

**How to apply:**
1. Every build brief that allows recorded output says: fixtures are generated from a scratch tree the seat creates for the purpose (invented names, a scratch home), and a recording made against the real drive is never committed. Paths in committed output are relative or scrubbed.
2. Before any repository changes visibility, or is handed to anyone outside the project, a sweep of EVERY branch and the WHOLE history runs first (secrets, personal data, other clients' and projects' names, internal layout, commit identities), with a positive control for every search that returns nothing. The sweep's main findings are confirmed at source by the coordinator before they reach Kam.
3. The link to a visibility setting is given to Kam only with the sweep result beside it.
4. A finding in history is fixed by a fresh repository from a cleaned copy or by a history rewrite; both are Kam's decision (the rewrite is irreversible).

**Related:** [[2026-08-03_role-beyond-code-three-priorities]] (no bleed between clients) · [[2026-08-13_shared-bus-tag-filter-or-leak]] · [[2026-09-08_when-a-check-returns-nothing-the-instrument-is-the-first-suspect]]
