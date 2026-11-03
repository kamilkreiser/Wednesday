# Drafter report: PR landing text, Composer branch b1170/composer-pcomp115-116-db-typecheck-awk

Drafted 2026-11-03. Files in this folder: pr-title.txt, pr-body.txt, squash-subject.txt, squash-body.txt, counts.txt, this file.

## What I read
- DRAFTER_RULES.md (whole); PR-MPS375 landing pr-body.txt and squash-body.txt (form).
- Composer 1_Project_Definition/Briefs: B1197_STATUS.md whole (the final review, round 3) and B1197_evidence/residue.md whole; first 16 lines of B1173_STATUS.md and B1181_STATUS.md (what rounds 1 and 2 fixed); first 30 lines of B1170_STATUS.md (builder).
- CLARIFICATIONS.md lines 1799, 2032, 2161 (landing rule and PCOMP-116 ticket).
- GitHub (GET only, project GH_CONFIG_DIR): git/matching-refs for the branch (sha ce523783bc2f9e2be99083a5bb34ef02becdf0db) and main (f5f33e189f34d36fa374c0ac1d6fa38d003df8ec); compare f5f33e18...ce523783 (3 commits, ahead 3, behind 1, merge base 01bc16e4, files DEPLOY.md +1 -1, one test file +345 -4); compare 643c389e...ce523783 (test file +88 -0 only); the three commit messages; pulls/113 title and body.

## Landing convention (quoted)
CLARIFICATIONS.md:1799: "[the coordinator] squash-merges PR #88 pinned to head 2da99cab after re-reading CodeQL and the checks. Nothing is deployed (Composer deploys only on your card)." Authority line :2032.

## Points to check
1. TICKETS: the branch covers PCOMP-116 only. Its first commit says "PCOMP-115 (the typecheck of packages/db/test) is not in this commit" and the review (B1197_STATUS.md:121) says the typecheck does not read packages/db/test. So the title and subject name PCOMP-116 once; PCOMP-115 appears once in each body, as NOT in this change. The branch NAME says 115; the content does not. If you want both keys in the title, that would be wrong on the facts.
2. DEPLOY.md: it IS changed, by one line (203, the awk check), one hunk, in the first commit of the branch (63fe0b9e); the later two commits do not touch it (643c389e..ce523783 lists only the test file). The review's "equals 643c389e" means the head's DEPLOY.md is byte-equal to the second commit's, not to main. The bodies say exactly that.
3. EXTENSIONS beyond your list (all sourced, say if you want them cut): (a) x--y is named as a fifth cell of the first shape, because the same mutant accepts it (residue.md:10); (b) the two fail-safe survivors (a -- line ending in CR; refuse side) are mentioned and folded into "to be ticketed"; the ruling says "ticket the four shapes", so ticketing those two is my extension; (c) the "83 edits: 20 / 57 / 6" split is my arithmetic from B1197_STATUS.md:101-102 (not one printed cell); (d) test totals and engine versions.
4. "Of 83 single edits ... 6 leave every row green" counts the review's own mutant set (50 + 33); the review says that set is not exhaustive and more survivors of the same kind are likely (B1197_STATUS.md:158). The bodies do not say that second part. Add it if you want the limit stated as open-ended.
5. Hosted CI and CodeQL: the review ran before any PR existed (NOT RUN, B1197_STATUS.md:61). The bodies make no claim about them beyond "are read before landing".
6. Attribution: pr-body ends with the "Generated with Claude Code" line per the session attribution reminder (PR #113 does the same); no Co-Authored-By in it. squash-body ends with exactly one Co-Authored-By line (Opus 5.5) per your instruction. The review noted the author of the three commits is a local-host address; the squash sets the author (N3).
7. Squash subject is identical to the title (93 chars). GitHub will append " (#N)" itself if the merge is done through the UI default; with the API, pass the subject as is.

## Could not source
- Whether the two fail-safe items (point 3b) are within the product owner's ticketing ruling: only the four shapes are named in the quoted ruling. Nothing else unsourced; every other sentence is mapped in counts.txt.
- The ruling text itself I rely on as given in the task message; I did not read the live board (fences).

## Checks run
ASCII-only (grep for bytes outside space..tilde: none). Forbidden-word scan (gate, seat, brief, lane, round, B-numbers, C-numbers, names, Tuesday, Wednesday): none in the five .txt files. Line counts: pr-body 19, squash-body 17. Co-Authored-By count: pr-body 0, squash-body 1 (last line).
