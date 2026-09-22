# READY — KS-1097 PART A of four (`docs/DEV-PROCESS.md`: QA-957-4 line 65 — "a second seat signs it off — the QA gate verdict at head plus Wednesday's GO — never the seat that built it"; QA-957-1 line 262 — the v4 footer glosses TESTED by reference "(as defined in `CONTRIBUTING.md`, step 6 of Adopted merge flow) and Wednesday's GO, naming the head SHA, is the approval"; the `(16:56):` prefix byte-identical so CONTRIBUTING:455 stays a prefix)
# Source read by me (Wednesday): both `+` lines are the ticket's ruled sentences verbatim (QA-957-4 whole-sentence per Wednesday's 13:04:26Z ruling; QA-957-1 the gate's proposal, "Adopted merge flow" unstarred inside the italic footer on purpose). D0–D6 PASS, D2 REANCHORED (the model dropped the blank context line 263 in hunk 2; the applied text keeps it). Run: runs/2026-09-15_ks1097-ornith35b-night. First sample, ~20 s.
# PR NOTES: ONE docs PR for all four parts (A here; B + C = CONTRIBUTING.md; D = CLAUDE.md), tier-2 docs gate at head, Wednesday's GO. NOT in the PR: `.github/workflows/`, CONTRIBUTING:531-532 and DEV-PROCESS:26 (Kam's 2026-08-27 red-pen lines). The project-root untracked `CLAUDE.md` mirror is done by hand after merge (ticket's note).

```diff
--- a/Blockchain/Dev/docs/DEV-PROCESS.md
+++ b/Blockchain/Dev/docs/DEV-PROCESS.md
@@ -62,7 +62,7 @@
 
 - **Review isn't testing.** Untested PRs turn the reviewer into the bottleneck and stall the automation work Peter owns.
-- **Separate the ticket from the review.** The author tests, but a second pair of eyes signs it off — never the same person on both.
+- **Separate the ticket from the review.** The author tests, but a second seat signs it off — the QA gate verdict at head plus Wednesday's GO — never the seat that built it.
 - **Merging doesn't wait on the reviewer.** Approval is the gate, not availability. `develop` keeps moving when someone is off.
 - **Manual deploys, no billed minutes.** The reason the last stage is by hand rather than a pipeline.
@@ -259,7 +259,7 @@
 ---
 
-*v4 · 11 September 2026 — Kam ruled that we approve our own work (16:56): a PR merges once it is TESTED — a QA gate verdict at its current head, a Test Evidence block and our own suites — and Wednesday's GO is the approval. Peter runs periodic formal test passes, and demo (UAT) waits for his nod. Merge-signal sentences updated; the 2026-08-27 measurements kept, with dated superseded notes (KS-1092).*
+*v4 · 11 September 2026 — Kam ruled that we approve our own work (16:56): a PR merges once it is TESTED (as defined in `CONTRIBUTING.md`, step 6 of Adopted merge flow) and Wednesday's GO, naming the head SHA, is the approval. Peter runs periodic formal test passes, and demo (UAT) waits for his nod. Merge-signal sentences updated; the 2026-08-27 measurements kept, with dated superseded notes (KS-1092).*
 *v3 · 27 August 2026 — Kam ruled the four platform suites are the author's final check before handover, and that GitHub Actions will not be restored. Adds the four suite lines to the Test Evidence block, the manual CI-gate equivalents map KS-685 commissioned, and the branch-protection setting that now blocks every merge until it is unticked. Replaces v2's "suspended, not retired" framing throughout.*
 
 *v2 · 26 August 2026 — updated from v1 after the first day under the flow (zero approvals on 16 PRs; the branch-naming trap; `clean` ≠ tested; CI-outage gate). Repo copy: [`CONTRIBUTING.md`](../CONTRIBUTING.md), merged as PR #733; process ticket KS-685.*
```

# SUPERSEDED-BY (feed11 drafter, 2026-09-22 12:57:28 AEST): re-briefed at develop 8c2f7b3fd as night/briefs/KS-1097-R16B-DEVPROCESS.md (golden PASS through the real checker in the feed11 precheck clone; Wednesday queues). This READY is STALE - do not raise it.
