# QA GATE — TIER 1, round 3 (Kam-authorised) — Datasec/NexusAI Marketplace package @ b8c4646

**Kam ruled round 3 at 14:59:37, verbatim: *"Yes — fix B1, MAJ-1, MAJ-2 and MAJ-3, then re-gate; the registry waits for your word"*.** **Head:** `s51-marketplace-remediation` @ `b8c4646ab7d271567364876757403bfb8d23cf08` (on origin; main `cd2b543`). **Range:** `20a723b..b8c4646`, **10 commits**. **DRAFT package:** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/evidence-s54-marketplace-package/DRAFT-submission-package-b8c4646/` (read it; copy zips into your temp dir before unzipping). **There is no round 4 without Kam.**

PRIOR ROUND: round 2 gated `20a723b1fbdc5afeb2a1a3bd316d30689f75146b`, verdict **NO GO FOR UPLOAD** (2 Blocker, 3 Major, 5 Minor).
ITS REPORT IS ON DISK AT: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-11-mktpkg-20a723b-tier1r2/`
Findings carried forward and their disposition: **B1** fixed `a5593b4` · **MAJ-1, MAJ-2** fixed `bcda8d6` · **MAJ-3** fixed `d80a8c0` (template) · **B2** untouched (waits for Kam's registry word) · **MIN-2(b)** fixed as a knock-on (`09759b2`, `5da1cf7`) · MIN-1, MIN-3, MIN-4, MIN-5 unchanged.

## Everything in round 2's brief still applies (read it: `qa-agent/briefs/2026-09-11_nexusai-mktpkg-20a723b-tier1r2.md`), with these changes
- Clone the worktree and check out `b8c4646ab7d271567364876757403bfb8d23cf08`; use `20a723b` as the red control.
- **The builder's own READY FOR QA pack** is in `evidence-s54-marketplace-package/` (MANIFEST, instruments, CLEANUP-docker.txt, ITEM5 file, MAINTREE summary). It is a claim, not evidence you rely on.

## 🔴 WHAT TO ATTACK FIRST
1. **The new logger redaction** (a winston format after `splat()`, plus the console format; header, token, Bearer and JWT redaction; depth-limited and cycle-safe). Attack: other axios clients (Graph, token endpoints) through ordinary `logger.*(msg, err)`; errors nested deeper than the depth limit; arrays; Buffers; errors with getters; a token split across fields; `util.inspect` paths; and **whether redaction eats ordinary diagnostic output the auth classifier or operators need** (a false positive is a Major too). The builder names 109 direct `console.*` calls that bypass winston: **measure whether any of them is reachable on a package deploy with a secret-bearing object**, and do not fix.
2. **`executeQuery`'s non-enumerable `originalError`:** does any caller that NEEDS it (retry logic, `_isMissingTableError`, the auth classifier) still work? Drive a real 403 and 404-table path against a stub.
3. **B1:** read the regenerated Datasheet PDF (every page image, `pdfimages -all` plus renders) and the new thumbnail at 4x, for any real name. Check `pdffonts`, and that the document is not visibly broken (the builder hit a DejaVu fallback before aliasing Carlito).
4. **MAJ-3:** re-run your round-2 restart proof against the `b8c4646` image built from a `git archive` extract: `/api/service-check` must not be `Local Database`, and the saved-config load line must appear. Count full IDs and tokens across the whole run (all 0).
5. **The zips:** every entry sha256 == `git show b8c4646:<path>`; 3 + 15 entries; OPS-002 and MKT-002 absent; no secret-class file; gitleaks as in CI.

## KNOWN — do NOT report as new
B2 (dev registry default, Kam's word pending) · MIN-4 (owner name and email in document text, Kam's) · `rd15-03` keeps a readable first name (Kam's AI-screenshot question pending) · `docs/Authorized_Users.md` ships (Kam: keep) · the pre-existing gitleaks finding `docs/PEN-TEST-REPORT-2026-04-25.md:297` · 109 direct `console.*` calls bypass winston (measure reachability only) · the NexusAI main tree is a stale snapshot (read-only; restore is Kam's) · **the deployed product defaults to Ollama/phi3 when `LLM_PROVIDER` is unset, and first-run setup lists Phi-3/Ollama as REQUIRED** (item 5; a PRODUCT question for Kam). **Measure and state it with an evidence class, because Kam's note says the Marketplace product must be GPT-only, but do not grade it as a round-3 regression.**

## Output
Findings-only. FOUND / TESTED / HOW plus an evidence class; controls for every zero; never `rm`; head readings at start, mid and end. **Remove only containers, images and volumes YOU create** (the builder's are gone per its CLEANUP file). **Report:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-11-mktpkg-b8c4646-tier1r3/report.md`. **MAIL YOUR VERDICT** to `tuesday-agent@agentmail.to`, subject `[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — Marketplace package @ b8c4646 (tier 1, round 3)`. Lead with GO, GO WITH FINDINGS or NO GO FOR UPLOAD. **Never `wednesday-agent@`.** You have no inbox.

PROVENANCE:
- Kam's round-3 ruling verbatim | panel relay mail 2026-09-11T04:59:38Z | read 2026-09-11
- head b8c4646, 10 commits, per-item SHAs, logger design, NOT COVERED, item 5, package facts | datasec-nexusai READY FOR QA 2026-09-11T06:49:23Z spf/dkim/dmarc pass | read 2026-09-11
- round 2 verdict and findings | QA verdict mail 2026-09-10T23:53:12Z + round-2 report.md | read 2026-09-11
- Kam's GPT-only note | panel relay mail 2026-09-11T05:00:51Z | read 2026-09-11

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-11 16:50
