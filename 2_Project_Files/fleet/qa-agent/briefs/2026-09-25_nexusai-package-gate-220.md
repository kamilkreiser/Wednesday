# QA Agent Invocation Brief — Datasec/NexusAI, PACKAGE GATE 2.2.0 (TIER 1): the resubmission zip, one verdict

**Drafted for Tuesday 2026-09-25 11:15-11:55 AEST by a read-only drafting agent. Tuesday fills the placeholders, stamps
and launches.** This is **THE ONE PACKAGE GATE** named in `HANDOVER-S78G.md` §★ ("set the digest -> the anonymous-pull
read-back -> the non-draft build -> **the ONE package gate** -> Tuesday emails the zip"). **Your verdict decides whether the
2.2.0 resubmission zip is emailed to Kam as ready for him to upload to Partner Center.** Nothing after you checks it.

**Commissioned on:** the READY FOR PACKAGE GATE mail from seat NexusAI-J (S81J), sent copy at `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-25_nexusai-pkg220-READY-mail.txt`, and the
builder's mails `mail-01` … `mail-12` in `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/s81j/`.
**The package head is `c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47`** on branch **`mkt-release-2.2.0-s81j`**. At drafting (11:39 AEST) that branch existed ONLY
locally, at `6f4945bf825dbe1928ef781613c94b5ee7cfdf8b`, and was **not on origin**; the step-4 commit did not exist yet (its
`--update-counts` run was in progress). The launcher refuses while the HEAD placeholder is unsubstituted and re-reads
`git ls-remote origin refs/heads/mkt-release-2.2.0-s81j` at launch; it refuses if origin does not hold exactly `c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47`.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-25 12:25
Self-check note: stamped by Tuesday at READY; the one-commit/six-file framing is superseded in part by the ADDENDUM AT READY (package commit 3464dd8 + three doc-only commits to c5da4d4); counts 4121/241 confirmed by the READY; read-only az demo read-back kept.

## ⚠ ADDENDUM AT READY (Tuesday, filled from the READY mail — read BEFORE §1; it narrows Q1, Q7, Q8)
- **The gated branch head is `c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47`, but it is NOT the single step-4 commit this brief was drafted around.** The chain on top of `6f4945b` (merge) is: **`3464dd8`** (THE PACKAGE COMMIT: the digest plus the re-anchors; the zips are built from it) → `28e1949` → `482bdf7` → `c5da4d4`. `28e1949` is a MERGE of `resubmission-handover-s78g` @ `dfbd55b`. The last three are documentation only (the handover doc `docs/resubmission/2026-09-22_resubmission-handover-for-kam.md`, folded and filled).
- **Q1 is therefore run in TWO halves:** (i) `git diff --name-only 6f4945b 3464dd8` = exactly the six files (four product/test files, the README, and the counts file, per the drafter's correction that the SIX includes counts). Plus the test file `marketplace-single-build-path.test.js`, which the builder was ruled to add, so compare against the builder's own stated list and report the set EXACTLY. (ii) `git diff --name-only 3464dd8 c5da4d4` = ONLY the handover doc. Anything else there is a NO GO finding.
- **Build and zip (Q7/Q8): rebuild at `3464dd8`**, the commit the zips were built from (`NexusAI_plan-managed-ai_2.2.0_3464dd8.zip`, sha256 `18155587c6cb0141b35d082b25fcccae9f3b8683189208dac3cf701790eef21c`; listing `NexusAI_listing-assets_2.2.0_3464dd8.zip`, sha256 `c333f95c328c1a0dceb19b9a47ec16721d05742b597d6659446c25159da7ecbe`). Then confirm the SHIPPED files (`azure-marketplace/**`, `scripts/**`) are byte-identical at `c5da4d4`, so either head produces the same package.
- **Verify numbers from the READY (confirm or contradict):** `3464dd8` 4121/4121 (241) PASS; `c5da4d4` full verify 4121/4121 (241) PASS; arm-ttk on `3464dd8` 49/49. The predicted counts `4121/241` HOLD.
- **The builder's four red-proof arms** (R1, R2 on package-build 7 red each; Q1, Q2 on single-build-path 2 red each) are in the READY. Re-run them INDEPENDENTLY as §Q3 says.
- **C-58 1b demo (the builder re-read it at 02:07Z):** `nexusaidev-app--s81j-220-fdda330`, sole active, `/api/health` build `b6f4bfddadcd4055`. The read-only `az` clause in §9 is KEPT by Tuesday.
- **The branch reaches origin by the builder's push** (GO sent 02:2xZ). The launcher's ls-remote guard compares against `c5da4d4`.

## Charter
Read `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an
independent tester. You did not build this package and you owe the builder nothing. **Every line below that reports what a
builder says is a CLAIM, never evidence.** Rule 1: state the FAIL condition before each test. Rule 2: what you did NOT test
is first-class output.

**ONE gate, ONE target, ONE verdict: TIER 1.** The target is the package branch head `c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47` AND the non-draft package
(two zips and a manifest) the builder produced from it, AND the release image the package points at. Verdict: **GO**,
**GO WITH FINDINGS** or **NO GO FOR UPLOAD**, stated about `c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47` and the release digest only.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- **None new.** The rulings that apply are in `1_Project_Definition/CLARIFICATIONS.md` (C-149 is the authority for the build
  and the zip; C-58 item 1 the release-image condition; C-72 the image is built from MAIN; C-131 and C-133 the re-anchor and
  accounting rules; C-124 and C-20 the residuals Kam keeps).
- **Kam's words for this whole chain (C-149, signed mail 2026-09-23T23:04:37Z, spf/dkim/dmarc pass, re-verified at source by
  S81J):** *"Please build the zip or send me instructions on what to do. Don't forget I am away for 1 more day and can't
  access your machine."* **He cannot reach this machine; he reads the zip by email.** Anything that would need him to act
  on this machine is a finding, not an instruction to him.
- **Tuesday's rulings the builder acted on, RELAYED by the builder (the drafter did not read Tuesday's ANSWER mails at
  source; Tuesday confirms at stamping):** 2026-09-24T23:37:38Z GO step 2, IMAGE_SOURCE deliberately NOT passed (no private
  repo URL in a customer image) · 23:45:22Z GO the demo redeploy (C-58 item 1b, under C-127) · 23:47:02Z GO step 4 as
  re-anchors (sites a, b, c1/c2, d) · 2026-09-25T00:51:41Z rd495 CTRL-1 ACCOUNTED on the A side under C-133 on blobs ·
  01:30:21Z the placeholder-pin census, then step 4b (the RD-506 re-anchor in a sixth file).

## PRIOR ROUND
- **This package line has NO prior QA gate at any head.** Searched 2026-09-25: no `report.md` under
  `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/*/` names `df70a96`, `5b6a24f` or
  `mkt-release-gate-s78g` (positive control: the same search finds `7aa5aaf` in its own report). S78G sent READY FOR QA
  for `5b6a24f` and READY FOR DIGEST for `df70a96`; neither was gated. **So this is round 1 for the 2.2.0 package line, and
  every lane-C fold inside `df70a96` reaches a gate for the first time here, through its package-facing effects.**
- **The most recent package gate with a report on disk:** round 4 on `s51-marketplace-remediation` @ `7aa5aaf`, verdict
  **GO WITH FINDINGS** (B2, the wizard's dev-registry image default, reserved to Kam — since REMOVED by RD-460: the image is
  now a template variable, C-58). Report, read it for method and for the package checks you should repeat:
  `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-12-mktpkg-7aa5aaf-tier1r4/report.md`
- Two later package-related folders exist with **evidence but NO `report.md`**: `2026-09-15-mkt-template-hygiene-981d120-tier1`
  and `2026-09-16-mkt-release-1470e18-tier1` (its `evidence/` holds `package-build/`, `ttk/`, `image/`, `verify/`). Reuse their
  instruments BY COPY if useful; cite nothing from them as a verdict.

## 1. Target — pinned at drafting from the object store (read-only), except `c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47`
**Repo:** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files` (object store only; see §7).

| what | sha / value | how read |
|---|---|---|
| package head (GATED) | **`c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47`** on `mkt-release-2.2.0-s81j` | the READY; the launcher re-pins by `ls-remote` |
| step-3 forward merge (the head's ONLY parent) | `6f4945bf825dbe1928ef781613c94b5ee7cfdf8b`, parents `df70a96145c5887a762b86f081436bd8befdf329` + `0677388ab031ffaf569a52f6c0301af48f44aece`, tree `9ec70f87b3976bdf7ec2154465b3d85652afd843`, committed 2026-09-25T10:52:12+10:00 | `git log -1 --format='%H %T %P'` |
| package line before the merge | `mkt-release-gate-s78g` @ `df70a96145c5887a762b86f081436bd8befdf329` (on origin) | `ls-remote`, 11:39 AEST |
| image commit = origin `main` at drafting | `0677388ab031ffaf569a52f6c0301af48f44aece` (CI Build 35811343989, 3974/3974, 234 suites, RELAYED) | `ls-remote`, 11:39 AEST |
| merge base of the forward merge | `c0788b1017a20ea5d2d0b9c0e5837ee233830696` | `git merge-base df70a96 0677388` |
| counts | `6f4945b` **4120/241**; `c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47` **predicted 4121/241** (`step4-hold-run2.log`: 4121 total after the c1/c2 split; step 4b adds no cell) | `git show <sha>:scripts/verify-expected-counts.json` |
| `package-lock.json` | blob `906476350431e2ecb3c21070a25c64b1702c1aa8` at `34f11f4`, `0677388`, `df70a96`, `6f4945b` — gate 8's `node_modules` serves (confirm at `c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47`) | `git rev-parse <sha>:package-lock.json` |

**The release image (C-149, C-58 item 1):**
`nexusaireleaseacr.azurecr.io/nexusai@sha256:fdda33098c36a484b50a9a761660bb69bc53f5ed238ffceeb1bd038c8eb77f66` —
tag `2.2.0`, built from `0677388` by `az acr build`, **ACR run `cr1`** (log `session-tools/s81j/acr-build-2.2.0.log`),
linux/amd64, labels (claimed) `revision=0677388ab031…`, `version=2.2.0`, **`source=""` deliberately** (Tuesday's ruling).
**`/api/health` `build` must equal `sha256("0677388ab031ffaf569a52f6c0301af48f44aece")[:16]` = `b6f4bfddadcd4055`** (the 40-hex
string, no newline — drafter recomputed it; the same formula gives `0d58cb8b3a02cfd3` for `34f11f4`, the demo's previous
value, which is the builder's own control). **`/api/health` reports `"version":"2.0.1"`** — known residual **RD-657**
(hard-coded in the server entry point at `0677388` line 18199; `package.json` says 1.3.0). **Not a failure; list it.**

**The step-4 commit (`6f4945b..3464dd8`, ONE commit — SUPERSEDED IN PART by the ADDENDUM AT READY: the branch head c5da4d4 adds three doc-only commits) changes EXACTLY SIX files** (the builder's commit hold stops on any other
staged set, `step4b-hold.sh:34`):
1. `azure-marketplace/combined/mainTemplate.json` — `variables.containerImage` (line 106) from
   `nexusaireleaseacr.azurecr.io/nexusai@sha256:RD-460-DIGEST-NOT-SET` to the release reference above. Nothing else.
2. `azure-marketplace/plans/README.md` — the `containerImage` sentence. **The commission said line 40; the placeholder
   prose is lines 40-42 at `6f4945b` and the builder's diffstat is `6 ++--` (three lines), so expect 40-42.**
3. `azure-marketplace/release-policy.json` — `imageTagExceptions` gains exactly `{"2.2.0": {"image": <the release ref>,
   "reason": …}}`; **`imagePlaceholder` is KEPT** (line 4) as the refusal rule; nothing else changes.
4. `__tests__/marketplace-package-build.test.js` — four re-anchored sites: **a** `realFixture()` asserts the shipped image
   is EXACTLY the committed release reference before substituting; **b** REAL POLICY keeps the placeholder AND the template
   equals the exception image; **c** split into **c1** (placeholder put back into the REAL files: exit 1, registry never
   contacted) and **c2** (REAL files as shipped: exit 0, no FAIL, probe called exactly once with the shipped digest);
   **d** the real file still holds the shipped digest after the fixture ran.
5. `__tests__/marketplace-single-build-path.test.js` — the RD-506 cells run through `shippedRepo({ placeholderBack: true })`,
   which asserts the shipped image equals the exception, then writes the placeholder into the COPY only; describe renamed
   "the placeholder put back into the shipped files"; assertions claimed byte-unchanged.
6. `scripts/verify-expected-counts.json` — regenerated.

## 2. Why tier 1, and who is waiting
The zip is the artefact Kam uploads to Partner Center himself, from an email, while he cannot reach this machine. A wrong
digest, a secret, a draft or failed build, or a package that refuses nothing ships to every Marketplace customer. Tuesday
emails it on your GO; there is no further check. **Kam's deadline, RELAYED (mail-12): "well inside Kam's 3pm"** — treat
15:00 AEST 2026-09-25 as the target, and never trade a check for it: a NO GO with its evidence is on time.

## 2a. LEGITIMATE SHAPES — the checker in this gate is `scripts/marketplace-package-build.sh` (template §2a)
The re-anchored cells are the checker's tests. Every ordinary shape it will see, put through the rule:

| shape — its ordinary form | expected verdict | the rule clause that yields it | predicted-by |
|---|---|---|---|
| non-draft build of the SHIPPED files at `c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47` (release digest + the `2.2.0` exception, anonymous pull 200) | exit 0, `MANIFEST COMPLETE: N checks, 0 failed`, two zips + manifest | tag check: tag differs from version but `imageTagExceptions["2.2.0"].image` equals the image exactly | drafter (from the script at `6f4945b` + mail-11) |
| `--draft` build of the same files | exit 0, outputs named `DRAFT-…` | registry/pull checks become WARN; the placeholder check is not softened | drafter |
| the placeholder put back into a COPY of the real template (real policy) | exit 1, no zip, `still the RD-460 placeholder`, registry never contacted | `imagePlaceholder` refusal (kept in the policy) | drafter / builder c1 |
| exception image one hex character off (real template) | exit 1, "no exception for exactly this image" | tag check, exact-match exception | builder R2 |
| exception keyed `"2.2.1"` instead of `"2.2.0"` | exit 1 | exception must be keyed by the package VERSION | drafter — **nobody has run this; you do** |
| a leftover zip in the out-dir | exit 2, nothing written | RD-527 leftover rule | S78G (RD-527) |
| an out-dir that is not empty of zips but holds other files | build proceeds | RD-527 counts `*.zip` only | drafter — measure |
| anonymous pull probe answers 401 (registry flips to private) | exit 1 non-draft, WARN draft | C-58 item 4 probe kept | drafter |

A row whose verdict and clause disagree is a finding against this brief — report it as such.

## 3. THE BUILDER'S CLAIMS — verify each, relay none
From mails 04-12 and the READY (`/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-25_nexusai-pkg220-READY-mail.txt`, read it whole; where the READY and this list disagree, the READY's
measurement is the claim and the disagreement is a finding):
1. **Image:** built from a clean detached worktree at `0677388` (0 lines of `status --porcelain --ignored`), tag did not
   exist before, digest `sha256:fdda3309…7f66`, the registry holds exactly one repository, one tag, one manifest.
2. **C-58 item 1(a):** anonymous token + HEAD manifest by digest = 200 with matching `Docker-Content-Digest`; no-token 401;
   the dev registry `nexusaidevacrfa39` refuses an anonymous token 401; `docker pull` by digest with a fresh `DOCKER_CONFIG`
   holding `{}` rc 0 (**run 1's PASS was VOID** — its empty-config pull failed on the missing Docker Desktop context and the
   script never read the exit code; run 2 pinned `DOCKER_HOST` and required rc 0). Smoke boot: health 200 in ~6 s,
   build `b6f4bfddadcd4055`.
3. **C-58 item 1(b):** revision **`nexusaidev-app--s81j-220-fdda330`** is the SOLE active revision at 100%, image
   `nexusaireleaseacr.azurecr.io/nexusai@sha256:fdda3309…7f66`, **no registry credential added**; anchor
   `nexusaidev-app--s80i-34f11f4-b2` Stopped; env 22/22, volume, scale 1/1, identity unchanged; demo health build
   `b6f4bfddadcd4055`. Before/after JSON: `session-tools/s81j/demo-anchor-before.json`, `demo-after-5b.json`.
4. **Step 3 (6f4945b):** only the counts file conflicted; A1 `--update-counts` 4120/4120, 241 suites, SESSION_SECRET unset;
   C-57 runs A 3974 · B 4070 · merged 4120, missing 21, new 0; C-133 accounted 20 by script + 1 by Tuesday's ruling;
   C-112 283 files, 270 = A blob, 13 = B blob, neither 0, absent 0; plain verify 4120/4120; named 341/341 across 26 files;
   C-89 clean.
5. **Step 4 red-proofs** (predictions written BEFORE the arms, `expect-step4.txt`, `expect-step4b.txt`):
   package-build file **R1** (placeholder put back into the shipped template, exception kept) and **R2** (exception image
   one hex char off) each redden EXACTLY 7 cells (48/55); clean 55/55. Single-build-path file **Q1** (`placeholderBack`
   forced false) and **Q2** (exception one hex off) each redden EXACTLY the 2 RD-506 rows (15/17); clean 17/17.
   **Correction the builder recorded itself:** c1 also reddens under R1 (it goes through `realFixture`'s pre-substitution
   assertion), so "the refusal-on-placeholder property" is proven by c1 on the CLEAN tree, not by R1.
6. **Census:** no pin of the pre-digest state outside the six files (`census-table.md`, `census-raw.txt`); one STALE
   COMMENT flagged, not edited: `scripts/marketplace-package-build.sh:37-38`.
7. **Build + zip:** `scripts/marketplace-package-build.sh <repo> c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47 2.2.0 <empty-out> azure-marketplace/listing-assets.txt`,
   non-draft, outputs at `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/marketplace-submission-2026-09-25-2.2.0`: `NexusAI_plan-managed-ai_2.2.0_3464dd8.zip`, `NexusAI_listing-assets_2.2.0_3464dd8.zip`,
   `MANIFEST-2.2.0_3464dd8.txt`; arm-ttk on the head (S78G's runner; `df70a96` was 49/49).
8. **Handover doc for Kam** (goes in the same email as the zip): `session-tools/s81j/doc/handover.md` (outside git; its git
   ancestor is `resubmission-handover-s78g` @ `dfbd55b`), every `<filled at build>` value "filled from a measurement".

## 4. WHAT TO ATTACK, in order. Answer each with a measurement.

**Q0 — the frame.** Re-pin at start, mid and end: `c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47` on `mkt-release-2.2.0-s81j`, `df70a96` on
`mkt-release-gate-s78g`, and `main` (three timestamped readings, branch name beside each sha). Confirm `c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47`'s ONLY
parent is `6f4945b`, `6f4945b`'s parents are `df70a96` + `0677388` in that order, its tree is `9ec70f87…`, and
`git merge-base df70a96 0677388` = `c0788b1`. **If `main` has moved past `0677388`, that is NOT a refusal** — C-149 pins the
image commit — but report it, and say whether any commit on main after `0677388` touches `azure-marketplace/**`, the build
script, or anything the image serves (C-68).

**Q1 — the step-4 delta, exactly.** `git diff --name-only 6f4945b c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47` = the six files of §1, no more, no fewer. Then:
parse both templates and prove they are identical except `variables.containerImage`; parse both policies and prove they are
identical except `imageTagExceptions`, that `imagePlaceholder` is byte-unchanged, that `imageTagExceptions` has exactly one
key, `"2.2.0"`, whose `image` equals the release reference character for character; read the README hunk (expect 40-42) and
say whether any sentence still claims "every build fails" or "placeholder until the release image is pushed".

**Q2 — every re-anchor is STRICTLY STRONGER, nothing deleted (C-131 shape, C-98).** For both test files, list every test
id at `6f4945b` and at `c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47` (same runner) and account for each: unchanged, renamed (old -> new), split (c -> c1 + c2), or
missing (a missing id with no successor is a **Major**). For sites a, b, c1, c2, d and the RD-506 pair, write old assertion ->
new assertion side by side and say whether the new one implies the old on the files it now reads. **Specifically prove
the refusal-on-placeholder property is still proven ON THE REAL FILES:** c1 and RD-506 copy the REAL template and policy
and put the placeholder back; confirm by reading that they do not build their own policy or template, and that
`placeholderBack` writes into the COPY only (the real files' blob ids must be identical before and after a run — measure).
**The mirror risk:** a re-anchor that asserts "shipped == exception" and "exception == shipped" proves consistency, not
correctness. Say which cell, if any, would stay GREEN if BOTH the template and the exception were changed to the same WRONG
digest — then run that arm (both files set to one well-formed but wrong digest on the release registry). If nothing in the
suite reddens, that is a finding (the digest's correctness then rests only on the build's anonymous-pull probe and on this
gate); state its evidence class.

**Q3 — the red-proof arms, re-run INDEPENDENTLY.** **POSITIVE CONTROL FIRST:** the clean files at `c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47` green (55/55 and
17/17). Then YOUR OWN mutants, built by you (not the builder's `step4-apply.py` / `step4b-apply.py`): **R1**, **R2** on
`__tests__/marketplace-package-build.test.js` (predicted exactly 7 red each, named in `expect-step4.txt`) and **Q1**,
**Q2** on `__tests__/marketplace-single-build-path.test.js` (predicted exactly the 2 RD-506 rows each, `expect-step4b.txt`).
**A red arm counts only if the mutant still parses:** `node --check` every mutated `.js`, `JSON.parse` every mutated `.json`,
quote the exit codes. A red from a mutant that does not parse or load is a **VOID** arm. Report the exact red set per arm
against the prediction; a mis-prediction is reported, not smoothed. Add the drafter's arm: exception keyed `"2.2.1"`.

**Q4 — the census, re-run.** At `c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47`, find every place that reads the shipped `containerImage`, the placeholder text,
or the RD-460 FAILURE MESSAGE (`still the RD-460 placeholder`) — `__tests__/**` including helpers
(`__tests__/helpers/shipped-plan-build.js` feeds rd471/rd472), `scripts/**`, `.github/**`. The builder's first grep missed
the RD-506 site because it matched the literal and the cell matched the message; do not repeat the frame. Classify each
(pins the old state / value-agnostic / stronger / unrelated) and confirm rd471 and rd472 still redden on THEIR OWN mutation
now that the shipped build no longer exits 1 for everyone (they were unable to fail by construction before the digest).

**Q5 — C-57 / C-133 / C-112 on `6f4945b`, re-derived by BLOB, not by commit list.** Read `session-tools/s81j/pkgmerge-A-accounting.txt`
and the table in `6f4945b`'s commit message. For **all 21** missing ids (not only the one Tuesday ruled), check C-133's two
conditions on blob ids: merged blob == one parent's blob, AND the other parent's blob == the base blob (`c0788b1`). The one
ruled id: **rd495 CTRL-1** in `__tests__/rd495-admin-routes-behind-the-gate.test.js` — drafter measured blobs **base
`c0788b1` = `76bbbf3c4ec1…`, A `0677388` = `9ffe71a215c5…`, B `df70a96` = `76bbbf3c4ec1…`, merged `6f4945b` = `9ffe71a215c5…`**;
A-side change `5366193` (RD-497); the script's STOP came from `5b6a24f` on the B side, whose blob equals base (RD-658 filed
for the script's commit-based test). Reproduce the blobs, then read `5366193`'s change to CTRL-1 and say whether it is strictly
stronger (plant above the gate must be found, plant below must not). **Also re-check the rd503-r2 id** the script accounted to
the B side `5b6a24f` — the builder's own `rd-new-c133.txt` says that one was right "only because the blob test and the commit
test happened to agree". C-112: 283 merged `__tests__` files each byte-identical to a parent, 0 neither, 0 absent — reproduce.
**C-133's standing addition (Tuesday's, in C-133 itself):** *"the package QA gate after this release gate reads the 23-id
table and confirms class (a) against RD-460's commits"* — that table is `session-tools/s78g/c57-accounting.txt` (merge
`5b6a24f`, base `784b831`). Nobody has discharged it (no gate ran on `5b6a24f`/`df70a96`). Do it: for the 18 RD-463
wizard-image/acrLoginServer ids, confirm the removing commits (`9eee3ff`, `c7f62f2`) are RD-460's and that the property each
pinned is either retired with the feature or re-asserted elsewhere.

**Q6 — C-58 item 1, the release image.** (a) **Re-verify anonymous pull YOURSELF, without touching the shared Docker image
store:** anonymous token from `https://nexusaireleaseacr.azurecr.io/oauth2/token?service=nexusaireleaseacr.azurecr.io&scope=repository:nexusai:pull`
with NO credentials; GET the manifest by digest with that token; **the sha256 of the manifest bytes you received must equal
`fdda33098c36a484b50a9a761660bb69bc53f5ed238ffceeb1bd038c8eb77f66`**; GET the config blob and at least one layer by digest
anonymously and hash them. From the config blob read the labels (`org.opencontainers.image.revision` = `0677388ab031…`,
`version` = `2.2.0`, `source` = empty — deliberate) and `BUILD_COMMIT_SHA`. NEGATIVE CONTROLS in the same window: the same
manifest GET with no token = 401; an anonymous token request to `nexusaidevacrfa39.azurecr.io` refused. **Never `docker rmi`
the release image** (it is in the shared store and is the builder's evidence). If you also `docker pull`, use a fresh
`DOCKER_CONFIG` holding `{}`, pin `DOCKER_HOST` to the Desktop socket, and read the pull's exit code (run 1's lesson) — and
note that a pull of an image already present proves nothing about the registry. Optional, under the docker lock: smoke-boot
the image locally (`docker run --pull never`, loopback port, random `SESSION_SECRET` never printed) and read `/api/health`:
`build` must be `b6f4bfddadcd4055`; `version` `2.0.1` is RD-657. (b) **Read the demo back, READ-ONLY:** at most three
`GET /api/health` requests to `https://nexusaidev-app.politeforest-b008d469.australiaeast.azurecontainerapps.io/api/health`
(client timeout 20 s): `build` must equal `b6f4bfddadcd4055`. Then, only if §9's read-only az clause stands at launch,
`az account show` (must be tenant `d500ebad-cf53-4f2a-a501-f831289e67fc`, subscription `0c57ab37-349c-47ae-a10f-e284a380bbb9`)
and `az containerapp revision list -n nexusaidev-app -g nexusai-dev-rg`: the sole active revision must be
`nexusaidev-app--s81j-220-fdda330`, its image the release reference, and `configuration.registries` must NOT name
`nexusaireleaseacr` (no credential was added — that is the "anonymously" in C-58). If az is not available or refused, the
digest-on-the-demo half is READ ONLY from the builder's JSON — say so.

**Q7 — the image came from MAIN (C-72).** `0677388` was origin `main` when the image was built (READY / mail-03 claim;
reflog of `refs/remotes/origin/main` is readable, do not fetch). The image's `revision` label and health `build` both name
`0677388`. The package head is NOT the image commit — confirm nothing in `0677388..c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47` that the IMAGE serves would differ
from `0677388` (the package branch's own product-code changes are not in the image: list them, and say whether any of them is
something a customer would reasonably expect the 2.2.0 image to contain; the builder's claim is that `df70a96` = `c0788b1` +
lane C, and lane C is package/tests/docs/scripts).

**Q8 — REBUILD the package yourself and compare with the builder's zip.** From your own project, into a NEW empty out-dir:
`bash <a git-archive extract of c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47>/scripts/marketplace-package-build.sh /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47 2.2.0 <your-empty-out> azure-marketplace/listing-assets.txt`
(the script reads the repo only through `git archive` / `rev-parse`, which are read-only; its anonymous-pull probe contacts
`nexusaireleaseacr.azurecr.io` — that host only). **Predict first, then measure:** the LISTING zip's whole-file sha256 should
EQUAL the builder's (entries come from `git archive`, whose mtimes are the commit time, zipped with `zip -X -D`); the PLAN
zip's whole-file sha256 will probably DIFFER, because the script `cp`s the three plan files into a stage directory WITHOUT
`-p` (script lines ~104-109 at `6f4945b`), so each entry's DOS timestamp is the build time. **A plan-zip whole-file mismatch is
therefore NOT a finding on its own — the binding comparison is per ENTRY:** every entry in both zips, yours and the builder's,
must have sha256 == `git show c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47:<source path>` (plan: `mainTemplate.json` <- `azure-marketplace/combined/mainTemplate.json`,
`createUiDefinition.json` <- `azure-marketplace/plans/managed-ai/createUiDefinition.json`, `viewDefinition.json` <-
`azure-marketplace/combined/viewDefinition.json`; listing: the 7 paths in `azure-marketplace/listing-assets.txt` at `6f4945b`,
re-count at `c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47`). Entry counts: 3 and the listing count. Both manifests must end `MANIFEST COMPLETE: <N> checks, 0 failed`;
`diff` the two manifests and explain every differing line (expected: the build date and the plan-zip sha/bytes line only).
**The digest in the ZIPPED `mainTemplate.json` `variables.containerImage` must equal the release reference exactly.**
No `DRAFT-` or `FAILED-` file anywhere in `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/marketplace-submission-2026-09-25-2.2.0`; no other zip there. If the whole-file plan sha DOES match, say how.

**Q9 — arm-ttk.** Run `bash /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/s78g/armttk.sh /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47 pkg220`
(set `TMPDIR` to a directory in YOUR project first: the runner `mktemp`s under it) and quote `TOTAL N/M PASS`; `df70a96`
was 49/49 (HANDOVER-S78G). Then its two controls, `hideconf` (the wizard's credential-confirmation test must drop) and
`hardloc` (the template location tests must fail) — **a 49/49 without a control that fired is not reportable.** Also run
arm-ttk on the three files UNPACKED FROM THE BUILDER'S PLAN ZIP (copy the runner's `Test-AzTemplate` call; do not edit the
runner) — they should be byte-identical to `c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47`'s, so the result must be the same.

**Q10 — no secrets in what Kam receives.** gitleaks over the UNPACKED contents of BOTH zips, the manifest, and the handover
doc `session-tools/s81j/doc/handover.md` (copy each into your own dir first): once with the repo's `.gitleaks.toml` at `c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47`
and once with gitleaks' default rules. **POSITIVE CONTROL FIRST:** plant a canary the ruleset TARGETS (C-103: a canary the rules
do not target is not a control) into a copy of one unpacked file; it must fire in the same run; then run the clean copies.
Report the gitleaks version and how it ran (the Homebrew binary or the `zricethezav/gitleaks` image — both were present at
drafting). Also read the handover doc against your measurements: the digest, `c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47`, `0677388`, the zip sha256s it quotes,
the counts, the arm-ttk result — any `<filled at build>` left, or any value that disagrees with what you measured, is a
finding (it goes to Kam in the same email). The doc must say what the package does NOT prove (C-124 first).

**Q11 — the full verify at `c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47`.** Under the jest lock, `env -u SESSION_SECRET` (print SET/UNSET as the hold's first
line, the NAME only), `npm run verify -- --maxWorkers=2` (C-81: the `--` form is the only one that reaches jest) on a tree
you built from `c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47`. Predicted **4121/4121, 241 suites** — confirm or contradict against `scripts/verify-expected-counts.json`
at `c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47`. Then the two step-4 files and the named package suites (`marketplace-*`, `rd461-*`, `rd471-*`, `rd472-*`,
`rd503-*`, `dev-scripts-template-parameters*`) once more by name. **C-131's lesson: a clean merge-tree and a counts-only
conflict do not show the checks agree — the full verify on the merged head is the evidence.** C-89: `c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47`'s counts file
equals what `--update-counts` would write (measure on your own copy; never write into the NexusAI repo).

## 5. KNOWN RESIDUALS — list them in the verdict, do NOT fail on them
- **RD-657** — `/api/health` reports `"version":"2.0.1"` on the 2.2.0 image (hard-coded; `package.json` 1.3.0). The image is
  fixed at `0677388` by C-149; changing it means a new build and digest. **Not a failure.**
- **Stale comment** at `scripts/marketplace-package-build.sh:37-38`: *"mainTemplate variables.containerImage carries a
  placeholder digest until the release image is pushed, so every build fails today. That is the intended state"* — false
  once the digest is set. The script does not ship in the zip. Ticket, post-resubmission.
- **C-124** — the Key Vault SUCCESS path has never been executed by anyone; everything known about it is a code claim. A GO
  must not read as "the Key Vault feature works".
- **C-20** — the template has never been validated or deployed against real Azure (the validate script is an `az` write and
  is NOT RUN; the deploy SP lacks roleAssignments/write). Kam's call.

## 6. KNOWN — do NOT report as new
RD-658 (the C-133 accounting script's commit-based test; not edited) · RD-656 (the NexusAI launcher's `git fetch` contradicts
C-28; S81J ran it once at boot, measured harmless) · RD-580 (preflight gitleaks warning) · RD-642 (`README.md:382` wording) ·
the dev-scripts residuals S78G listed (`deploy-dev.sh` unexecuted; `--password` visible to `ps`; H-2 flip uses
`identityref:system` while the template's app identity is user-assigned; `.gitleaks.toml:171-173` comment cites old lines) ·
RD-644 (feedback notifies Tuesday, post-resubmission, C-144) · the NexusAI `2_Project_Files` checkout is a stale snapshot with
a dirty tree (C-28) · CI has not run at `c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47` (§10) · the image's `source` label is empty BY RULING.

## 7. Trees, and where you may write
- **Build your own trees INSIDE YOUR OWN PROJECT** (Testing Agent MAIN), from the object store:
  `git -C <repo> archive c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47 | tar -x -C <a fresh mktemp -d under projects/nexusai/qa-trees/pkg220.XXXXXX/>`, git-indexed
  from the object store where a full verify needs a git tree. `node_modules`: an APFS clone (`cp -c -R`) of gate 8's
  (`qa-trees/gate8.*`); `package-lock.json` blob `9064763` must hold at `c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47` — confirm.
- **Each tree is EXCLUSIVE to this gate and to ONE purpose**: a fresh `mktemp -d` per arm; never reuse a mutant tree for a
  clean arm; `pkg220`-prefixed directories only. Gate 8's trees are that gate's evidence — copy from, never run in.
- **NexusAI repo: read verbs only** (`show`, `log`, `diff`, `ls-remote`, `rev-parse`, `ls-tree`, `cat-file`, `grep`,
  `merge-base`, `archive`). **Never `fetch`, `pull`, `push`, `checkout`, `worktree`, `commit`, `stash`, `gc`, `clean`, or
  `merge-tree --write-tree` against it** (C-28, C-67), and never work in its `2_Project_Files` checkout, its `worktrees/`
  (including the builder's `worktrees/s81j-pkg`), `session-tools/` or `1_Project_Definition/`. Count
  `find <repo>/.git/objects -type f` before and after your run and account for any delta by mtime (the live NexusAI-J seat
  commits into the same object store).
- **Never write into `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/marketplace-submission-2026-09-25-2.2.0`** — copy the builder's zips into your own dir before unzipping; hash them at start and end.
- **NEVER `rm`** — quarantine (template §5).

## 8. Floor discipline — THE FOUR CLAUSES, plus THE DEADLINE RULE
1. **Every jest run goes through `session-tools/nexusai-lock.sh jest <tag> …`, tagged `qa-pkg220-…`** (C-141 + addendum:
   gate-class tickets; C-110: no other queue jumping). **QUEUE, NEVER TAKE OVER:** never kill, signal, move or edit another
   seat's process, lock directory, owner file or ticket. Any docker leg goes through the **docker** lock the same way.
2. **Hold the lock ONCE per multi-run measurement,** as a TRACKED CHILD of your seat — never detached (`nohup … &`).
3. **Record the foreign server count beside every result, the RD-606 form anchored on YOUR OWN claude pid** (argv from the
   kernel; `basename(argv[0]) == node` AND the server entry point anywhere in the remaining argv; "ours" = the ancestor chain
   CONTAINS your claude pid). **NEGATIVE controls, read at drafting 11:40 AEST from `tmux list-panes -a` + `ps`:** NexusAI-J
   claude **`11382`** (pane `%2`, launcher `11380`) and Tuesday's claude **`2679`** (pane `%0`). Re-read them at start; a
   hold with NO live negative control aborts. Reuse gate 7 round 1's instrument BY COPY with YOUR pid as `ROOT`:
   `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-22-gate7-rd645/evidence/qa-floorcount.py`
   and `…/qa-floorlib.sh` (its first line names gate 7's pid — correct it).
4. **A zero is reportable only beside a control that fired in the same window** — the floor count, gitleaks' zero, the
   "registry never contacted" of c1/RD-506, and "no other zip" in the out-dir all included.

**5. THE DEADLINE RULE:** every real-server probe and every network request has a per-step **DEADLINE** and a client timeout
(boot 60 s, request 30 s, registry call 30 s, exit 20 s); every server you start is killed in a **`finally`** (SIGTERM, then
SIGKILL after a grace) and the reap confirmed by your counter; log a **HEARTBEAT** line (timestamp, step, pid, elapsed) at
least every **2 minutes** during any hold; a step with no heartbeat for **5 minutes** is aborted and reported. Never wait
out a lock window.

## 9. Drivable surface, network and identity
- Product probes run on **127.0.0.1** against servers YOU boot (or the release image you boot locally).
- **External hosts you MAY contact, and nothing else:** `nexusaireleaseacr.azurecr.io` (anonymous token + manifest/blob GETs,
  and the build script's own probe) and `nexusaidevacrfa39.azurecr.io` (ONE anonymous token request, the negative control);
  the demo's `GET /api/health`, at most three times (Q6b). No login, no POST, no rendered page on the demo (RD-76, C-84).
- **Azure: READ-ONLY az only, and only if Tuesday leaves this clause standing at stamping** — `az account show`,
  `az containerapp show`, `az containerapp revision list|show`, under NexusAI's own `AZURE_CONFIG_DIR` (the launcher exports
  it). Any other az verb, any write, any `az login` or tenant switch: HELD. An authorization error is the boundary working —
  report it, never work around it.
- If a response is cut off by a safety check, record it and continue with the next item; this is authorised defensive QA of
  Datasec's own product and release artefacts.

## 10. CI (C-142) and HELD
- **CI NOT RUN at `c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47`** (no PR; Build runs on pull_request and on push to main). CI on the image commit `0677388`:
  Build 35811343989 green, RELAYED — `gh`, if used at all, is READ-ONLY; confirm it and quote the run.
- **HELD:** no push, no merge, no tag, no registry change (no image push, delete, re-tag, anonymous-pull setting), no demo
  change, no Partner Center, no production, no money, no external comms, no mail to any human. No `az` beyond §9.
  **Findings-only:** no commits, no tickets, no edits anywhere in NexusAI. The gate fixes nothing and rebuilds nothing that
  ships — your rebuild in Q8 is evidence in your own directory, never a replacement zip.

## 11. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-25-pkg-gate-220/report.md`

**Questions:** your routing name is **`QA/NexusAI-pkg220`**. If you must ask, mail `tuesday-agent@agentmail.to`, subject
`[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>` (Context / one Question / Meanwhile / Needed-by), and **proceed on the
safest reading** without waiting. Tuesday's answer arrives in `tuesday-agent@agentmail.to` with a subject beginning
`[Tuesday -> QA/NexusAI-pkg220] ANSWER` — read it with the AgentMail key below. If two answers differ, STOP that item and ask
which stands. Approval-class items (anything touching the demo, the registry, Partner Center, money, or a human) never
proceed on a safe reading — they are NOT RUN and named. Record every question, the reading you took and any answer.

**MAIL YOUR VERDICT** to `tuesday-agent@agentmail.to`, subject beginning exactly:
`[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — package gate 2.2.0: ` followed by `GO`, `GO WITH FINDINGS` or
`NO GO FOR UPLOAD`, then ` @ ` and the first 7 characters of the pinned head. **Never `wednesday-agent@`.**

AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env` (absolute path: the QA project
has none). Never put the key, or any secret, in a mail or the report.

**Verdict format** (lead with it; one sentence first: *is the zip at `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/marketplace-submission-2026-09-25-2.2.0` ready for Tuesday to email to Kam, and if not,
what stops it*):
- the frame (Q0) with three timestamped head readings, branch names beside each sha;
- the step-4 delta (Q1) and the strictly-stronger table (Q2), including the both-files-wrong arm;
- the red-proof arms R1, R2, Q1, Q2 and the `"2.2.1"` arm (Q3), each with its `node --check` / parse exit code;
- the census (Q4); the C-133 re-derivation for all 21 ids plus the 23-id class (a) check (Q5);
- C-58 item 1(a) measured by you, and 1(b) read back (Q6), with the evidence class of the digest-on-the-demo half; C-72 (Q7);
- the rebuild comparison per entry and per whole file, with the timestamp prediction confirmed or refuted (Q8);
- arm-ttk N/M with both controls (Q9); gitleaks with its canary, and the handover doc check (Q10); the full verify (Q11);
- §5's residuals listed by name; every action recommendation labelled **MEASURED AT RUNTIME**, **PROBED** or **READ ONLY**.
- **Rule 2: a NOT TESTED section.** It MUST carry this line, verbatim:

  Real Azure: not deployed through Partner Center, not validated against real Azure (C-20), and the Key Vault success path never executed (C-124); the jest suites are not network-sandboxed (C-58).

- **Run long commands in the FOREGROUND; never end a turn waiting on a background notice** — you have no inbox that wakes you.

## WRONG AT SOURCE — what this brief found when it checked the commission against the repo
1. **The branch was not on origin at drafting.** `mkt-release-2.2.0-s81j` exists only locally (at `6f4945b`); `ls-remote`
   showed no such ref. C-113: a branch a gate must read has to be at origin before launch — the launcher enforces it.
2. **"Step 4 changed SIX files … plus the regenerated counts file"** reads as seven. It is **six INCLUDING the counts file**
   (five content files + counts), which is what the builder's commit guard enforces (`step4b-hold.sh:34`). The builder's own
   mail-12 says "the six files plus counts", the same ambiguity; the hold script is the authority.
3. **"README.md:40"** — the placeholder prose is **lines 40-42**; the builder's diffstat for it is three lines.
4. **"re-run the two red-proof arms"** — there are **four** builder arms: R1/R2 on the package-build file and Q1/Q2 on the
   single-build-path file. All four are in Q3.
5. **"compares sha256 with NexusAI-J's zip"** — a whole-file sha comparison of the PLAN zip will very probably fail for a
   benign reason (entries staged by `cp` without `-p`, so entry timestamps are the build time). The binding comparison is
   per entry against git; whole-file equality is predicted for the LISTING zip only. READ ONLY prediction — Q8 measures it.
6. **C-133's own text carries an undischarged package-gate duty** the commission did not name: Tuesday's addition that
   "the package QA gate after this release gate reads the 23-id table and confirms class (a) against RD-460's commits". No
   gate ran on `5b6a24f` or `df70a96`, so it falls here (Q5).
7. **C-58 (the 2026-09-17 07:31 addition) says "The jest suites in package gates are not network-sandboxed. That limit
   carries into the release gate's NOT TESTED list."** Carried in the NOT TESTED line.
8. **"The gate re-verifies (a) itself"** — re-running the builder's method needs `docker rmi` of the release image from the
   SHARED store (the builder deleted its copy first). This brief replaces it with registry-API pulls by digest that hash the
   bytes, which prove anonymous pullability without mutating the store (Q6).
9. **"reads (b) back read-only"** — the running image of a Container App revision cannot be read without `az` (the health
   `build` names the commit, not the digest). The brief permits READ-ONLY az verbs under NexusAI's own identity; **this is a
   decision for Tuesday at stamping** (§9). Without it, the digest-on-the-demo half is READ ONLY from the builder's JSON.
10. **C-149 is filed under the heading "## 25. Added 2026-09-22 (S79H …)"** in CLARIFICATIONS (line 1545), while S81J's
    mail-01 says "CLARIFICATIONS §27". Cosmetic; cite C-149 by number.
11. **The newest package gate is not quite the one the commission named:** `7aa5aaf` (2026-09-12) is the newest package gate
    WITH a report; `2026-09-16-mkt-release-1470e18-tier1` and `2026-09-15-mkt-template-hygiene-981d120-tier1` are newer and
    hold evidence only, no `report.md`.
12. **The routing name `QA/NexusAI-pkg220` has no line in `fleet/inbox_routing.conf`** at drafting (gate 7 and 7r2 have
    `QA/NexusAI-gate7…|tuesday-agent@agentmail.to|no`). The launcher refuses until Tuesday adds it. The ANSWER subject prefix
    `[Tuesday -> …]` is the drafter's reading of the Datasec convention; the Vision gate 7 brief used `[Wednesday -> …]` —
    Tuesday confirms which her send tool emits.
13. **Convention departure, by the commission's own limit (two files):** there is no `.prompt.txt` beside this brief; the
    gate's prompt is a heredoc inside the launcher, and the launcher applies every prompt guard to that text.

## PROVENANCE (drafter, 2026-09-25 11:15-11:55 AEST, read-only)
- origin: `main` `0677388ab031…`, `mkt-release-gate-s78g` `df70a96145c5…`, `resubmission-handover-s78g` `dfbd55b7cdc9…`;
  NO `mkt-release-2.2.0-s81j` on origin | `git ls-remote origin <refs>` | read 11:39
- local `refs/heads/mkt-release-2.2.0-s81j` = `6f4945bf825d…`; parents `df70a96` + `0677388`; tree `9ec70f87…`; commit
  message carries the C-57/C-133/C-112 table and Tuesday's 00:51:41Z citation | `git rev-parse`, `git log -1 --format` | read 11:40
- merge-base `df70a96`/`0677388` = `c0788b1017a2…` | `git merge-base` | read 11:41
- rd495 file blobs `c0788b1`/`df70a96` `76bbbf3c4ec1aa1cee6269d4ac2331b75d4c5ad0`, `0677388`/`6f4945b`
  `9ffe71a215c55eb15a641e93b7114922675f29b0`; `c0788b1..0677388 -- <file>` = `5366193`; `c0788b1..df70a96 -- <file>` = `5b6a24f` |
  `git rev-parse <sha>:<file>`, `git log` | read 11:41
- health formula: `sha256("0677388ab031ffaf569a52f6c0301af48f44aece")[:16]` = `b6f4bfddadcd4055`; for `34f11f4…` = `0d58cb8b3a02cfd3` |
  `shasum -a 256` | read 11:41
- `6f4945b`: `mainTemplate.json:106` = the placeholder; `plans/README.md:40-42` placeholder prose; `release-policy.json`
  `imagePlaceholder` kept, `imageTagExceptions` `{}`; `scripts/marketplace-package-build.sh:37-38` the stale comment; plan
  files staged with `cp` (no `-p`) and zipped `zip -X`; listing zipped from the archive extract `zip -X -D`; the server entry
  point line 18199 `version: '2.0.1'` at `0677388`; counts 4120/241; `listing-assets.txt` 7 paths | `git show`, `git grep -n` | read 11:43-11:48
- the step-4 edits UNCOMMITTED in the builder's worktree `worktrees/s81j-pkg` (HEAD `6f4945b`): 5 files, +63/−18; template
  line 106 only; README lines 40-42 (it still names the placeholder once, as the thing the build refuses); policy
  `imageTagExceptions` gains `"2.2.0": {image, reason}` and nothing else changes | `git --no-optional-locks -C <worktree> diff`
  (read-only) | read 11:58 — **a pre-commit reading; the launcher re-checks the committed head**
- `package-lock.json` blob `9064763…` at `34f11f4`, `0677388`, `df70a96`, `6f4945b` | `git rev-parse` | read 11:47
- builder claims: mails 01-12, `c-rd450-*.txt`, `expect-step4.txt`, `expect-step4b.txt`, `rd-new-*.txt`, `step4-hold-run2.log`
  (R1/R2 7 red each, 48/55; `--update-counts` 4119/4121 FAIL on the RD-506 pair), `step4b-hold.log` (Q1/Q2 2 red each, clean
  17/17 and 55/55), `step4b-hold.sh:32-34` (the six-file commit guard) | `cat` of `session-tools/s81j/` | read 11:20-11:45
- HANDOVER-S78G §★ (the ONE package gate; digest at `mainTemplate.json:106`, README:40, `release-policy.json:4`), §1 item 8, §2,
  §5 | `cat` | read 11:22
- CLARIFICATIONS: C-20 :117, C-28 :153, C-30 :164, C-57 :410, C-58 :433, C-62 :573, C-68 :657, C-72 :695, C-89 :827,
  C-112 :1141, C-113 :1156, C-124 :1307, C-127 :1349, C-131 :1406, C-133 :1425, C-141 :1478, C-142 :1488, C-149 :1545 |
  `grep -n` | read 11:30
- prior package gate report `2026-09-12-mktpkg-7aa5aaf-tier1r4/report.md` (GO WITH FINDINGS); no report naming
  `df70a96`/`5b6a24f`/`mkt-release-gate-s78g` (control: `7aa5aaf` found) | `grep -il` over `reports/*/report.md` | read 11:36
- seats: pane `%2` -> launcher `11380` -> claude `11382` (NexusAI-J); Tuesday claude `2679` (pane `%0`) | `tmux list-panes -a`, `ps` | read 11:40
- local tools: `gitleaks` at `/opt/homebrew/bin/gitleaks`; image `zricethezav/gitleaks:latest`; the release image present in the
  local store; S78G's `armttk.sh`, `pwsh-v7.6.6.bYFB`, `arm-ttk-20260213.TjXW` present | `which`, `docker image ls`, `ls` | read 11:37
- demo fqdn `nexusaidev-app.politeforest-b008d469.australiaeast.azurecontainerapps.io`, latest revision
  `nexusaidev-app--s81j-220-fdda330` | `session-tools/s81j/demo-after-5b.json` (a builder artefact, not read from Azure) | read 11:44
- `fleet/inbox_routing.conf`: no `QA/NexusAI-pkg220` line | `grep` | read 11:50

## FILL AT READY — Tuesday, before stamping (the launcher refuses until each is done)
- the HEAD placeholder (the token HEAD between two @ signs) -> the full 40-hex step-4 commit, in THIS brief and in the launcher (`sed` both; the gate's PROMPT is embedded in
  the launcher, not a separate `.prompt.txt`, because this commission allowed two files only; the launcher's placeholder
  comparands are built by concatenation so the `sed` cannot reach them).
- the ZIPDIR placeholder -> the absolute directory holding the builder's non-draft zips and manifest.
- the READY_MAIL placeholder -> the absolute path of S81J's READY FOR PACKAGE GATE sent copy in `session-tools/s81j/`.
- The launcher's `EXP_COUNTS` if the READY's counts differ from the predicted `4121 241`.
- The routing line `QA/NexusAI-pkg220|tuesday-agent@agentmail.to|no` in `fleet/inbox_routing.conf`, and the ANSWER prefix.
- §9's read-only az clause: keep it or strike it.
- The negative-control seats in §8 if either pid has exited.
- Both STAMP placeholders (the SELF-CHECK line and the Self-check note) — LAST. Stamp them by hand, not with a global `sed`,
  and write no placeholder token into the note.
