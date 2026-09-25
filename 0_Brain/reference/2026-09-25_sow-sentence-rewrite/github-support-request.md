# GitHub Support request: purge sensitive data after a history rewrite (datasecau)

**Where to send it:** https://support.github.com/contact. Sign in as an OWNER of the `datasecau` organisation, pick "Removing sensitive data" (or the closest category), and paste the text below. Drafted by Friday on 2026-09-25 per Kam's card `composer-github-support-purge: a`. It contains no sensitive text itself.

---

**Subject:** Remove cached commits and pull-request refs after a sensitive-data history rewrite (datasecau/HPSM-light, datasecau/HPSM-analysis)

Hello,

We removed third-party contractual text that should not have been committed from the history of two PRIVATE repositories in the `datasecau` organisation. The work was done on 2026-09-25 with `git filter-repo --replace-text`. Every branch was force-pushed, and we have verified that no branch now contains the text.

Please:
1. Remove the cached views of the old commits listed below, and run garbage collection on the unreferenced objects in both repositories.
2. For datasecau/HPSM-light: dereference or remove the pull-request refs that still point at old commits containing the text: PRs **#1, #2, #3 and #4**. `refs/pull/{1,2,3,4}/head` currently point at `c918594`, `888c59a`, `1c30cf9` and `98c16f5`. The pull requests themselves are closed/merged, and we do not need their refs kept.

**datasecau/HPSM-light.** Old commits where the text was introduced or removed (every old commit between them also contains it):
- 5fd5870c740bd8fa88fa3e69ea89577d36dbb757
- 9d5152c94537fd5c09917342f695c390dae1c0ea
- ba67540d78db1212315b9efb92b4fd4253c07871
- edf5cfe564fc549925761d80fc49d292553a9389

The new default-branch head is `7855f10a1fdd47f6e7899097c81430f88a59d698`.

**datasecau/HPSM-analysis.** Old commits where the text was introduced or removed:
- af65839310d66a391250d07e8c6884555cb0061a
- dd35f74bbb49a28cbb6c4c50de060bae7c67058d
- bb9a4952f1f093e87a2ecff16038c5fe0657fd31

The new heads are `main` `80cb5b4b06857679fd7953ddda17e3f61c5d1c82` and `s50/toolkit-r2` `12ffb44cd4cd24e68ff509b3e840f526c14251e6`. This repository has no pull requests.

Neither repository has a fork (GitHub API, forks_count = 0, read 2026-09-25).

Thank you,
Kam Kreiser, Datasec
