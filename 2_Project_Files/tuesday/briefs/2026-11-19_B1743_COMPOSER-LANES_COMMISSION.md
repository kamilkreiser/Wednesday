# B1743 commission — Security Composer: which content tickets may be BUILT ON BRANCHES now (read-only lane sweep)
Commissioned by Tuesday (s293), 2026-11-19. Model: Sonnet (routing row C8). You write ONE document; you change nothing.

WHY: SWEEP-1630 classed 13 Composer tickets as waiting on the reviewer-round hold. Drafter A of the decision pack
(`2026-11-19_B1742_decision_pack/A_REPORT.md` and `card_composer-reviewer-round-hold-1119.json`: read both whole) found
that only PCOMP-19, 20 and 92 hold on the round; that PCOMP-31 to 39 wait on unbuilt lanes and that entry C-92 of the
project's CLARIFICATIONS.md lets them be BUILT ON BRANCHES (the content RELEASE waits for the round, not the build); and
that PCOMP-29 has no hold at all. If true, there is buildable Composer work today. Tuesday has NOT verified this.

Output: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-19_B1743_composer-buildable-on-branches.md`.
Project: '/Volumes/Datasec_DEV/!CODING/Datasec/Datasec Security Composer' (Jira PCOMP; verify the folder by listing the
parent; find the repo name from its git remote with a read verb).

DO:
1. Quote, word for word with line numbers, every sentence of CLARIFICATIONS.md that decides what may be built, merged,
   released or deployed while the reviewer's round runs (C-92 with its K-rows, C-99, C-71, line 1764, and anything
   later). State exactly what is allowed: build on a branch? merge to main? release? deploy? Check BOTH directions: is
   the allowance narrower or wider than drafter A wrote? The Guided hold (C-71 COMP-2) and the held PR #85 are HOLDS:
   list which of the keys below either one touches; those are out.
2. Read PCOMP-29 and PCOMP-31 to 39 whole (description, every comment, status, links). For each: what it asks, the
   unbuilt lane or predecessor it waits on (name it and its state at main), whether the ticket says WHAT to change
   precisely enough to build, whether it needs customer-facing or reviewer-facing words that nobody has approved (then it
   is NOT buildable: words are the product owner's), and whether its content source exists in the repo or the project
   folder (print the path).
3. Propose lanes in dependency order (the first lane must have no unbuilt predecessor): keys, files touched (read at
   main, print the sha), size, gate tier guess, what would STOP it, and where the work rests when done (a branch that is
   NOT merged? a merge to main that is not released?) with the sentence of step 1 that permits it.
4. Say plainly if the answer is "nothing is buildable" and why.

RULES: read-only everywhere except the output file and scratch
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s293/d1743/`. Jira GET only (credentials by name in-process
from the project's `4_Credentials/.env`; discover the key names without printing values); gh `-X GET` only under the
project's own GH_CONFIG_DIR; git read verbs only (`--no-optional-locks`). Nothing of HPSM-POC is read or named. No az,
no request to any app host, no mail, no test run, no server; `decision_queue.sh` only with `show`, `prior`, `list`.
No `cd`; no unquoted word starting with `=`; zsh; absolute paths; never delete; clocks from `date`; every zero with a
positive control. ASCII; built whole, temp file, os.replace. Sections FOUND / TESTED (and NOT tested) / HOW at the end.
First line of your reply: `COMPOSER: <n> buildable keys in <m> lanes` or `COMPOSER: nothing buildable - <why>`.
