# QA Agent Invocation Brief — Datasec/NexusAI, PACKAGE GATE 2.2.1 (TIER 1): the RD-665 resubmission zip, one verdict

**Drafted for Tuesday 2026-09-25 ~18:20-18:50 AEST by a read-only drafting agent, adapted from the 2.2.0 package gate
brief (`2026-09-25_nexusai-package-gate-220.md`). Tuesday fills the placeholders, stamps and launches.** This is the
package gate named in C-158's path ("the fix on a branch off the submitted package source → READY FOR QA → Tuesday
commissions the package gate → on GO, the package is built from the fixed branch head and gated → Tuesday emails Kam the
zip → **Kam resubmits in Partner Center; agents never touch it**"). **Your verdict decides whether the 2.2.1 zip is emailed to
Kam as ready for him to upload.** Nothing after you checks it.

**Commissioned on:** the READY FOR PACKAGE GATE mail from the NexusAI seat (S83L), sent copy at `@READY_MAIL@`, plus
`HANDOVER-S83L.md` and the create-time evidence in `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/evidence-s83l-customer-test/`.
**The gated head is `@HEAD@`** on branch **`rd-665-standard-webtest-s83l`**. The launcher refuses while the HEAD placeholder
is unsubstituted, re-reads `git ls-remote origin refs/heads/rd-665-standard-webtest-s83l` at launch, and refuses if origin
does not hold exactly `@HEAD@`. The PACKAGE COMMIT (the commit the zips are named after) is read by the launcher from the
first line of the manifest in the zip directory; it must be the head or an ancestor of it, and anything between it and the
head may touch `docs/resubmission/` only.

SELF-CHECK: re-read end-to-end for contradictions | @STAMP@
Self-check note: @STAMP@

## Charter
Read `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an
independent tester. You did not build this package and you owe the builder nothing. **Every line below that reports what a
builder says is a CLAIM, never evidence.** Rule 1: state the FAIL condition before each test. Rule 2: what you did NOT test
is first-class output.

**ONE gate, ONE target, ONE verdict: TIER 1.** The target is the gated head `@HEAD@`, the non-draft 2.2.1 package (two zips
and a manifest) the builder produced from its package commit, and the release image the package points at (UNCHANGED from
2.2.0). Verdict: **GO**, **GO WITH FINDINGS** or **NO GO FOR UPLOAD**, stated about `@HEAD@` and the release digest only.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- **None new.** The rulings that apply are in `1_Project_Definition/CLARIFICATIONS.md`: **C-158** (fix RD-665 now and
  resubmit; Kam resubmits, agents never touch Partner Center, C-23), **C-157** (the customer test lives ONLY in the empty
  sponsorship subscription `73e9b141-f0ed-4b92-962b-86a2be888ec7`, labelled "not a clean tenant"), **C-156** (`a6b8fe11`,
  `hpsm-poc-rg`, `hpsm-poc-deploy` are Friday's: never read or touch), **C-149** / **C-58 item 1** / **C-72** (the release
  image, unchanged), **C-124** (Key Vault success path; UPDATED 2026-09-25, see §5), **C-20**.
- **The version 2.2.1 was ruled by Tuesday, RELAYED** (release-policy reason text: "Version ruled by Tuesday (ANSWER
  2026-09-25T08:10:12Z): Partner Center needs a new version for a plan package update"). Tuesday confirms at stamping.
- **Tuesday's GO for the create-time proof in `rg-nexusai-customer-test`, RELAYED** (HANDOVER-S83L: "Pending Tuesday GO: real
  create of the Standard test in rg-nexusai-customer-test"). The drafter did not read that GO at source.

## PRIOR ROUND
- **Package gate 2.2.0** on `mkt-release-2.2.0-s81j` @ `c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47`, verdict **GO WITH FINDINGS**
  (2026-09-25 12:27-13:05 AEST). Report, read it WHOLE before you start — it is the baseline this gate diffs against:
  `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-25-pkg-gate-220/report.md`
  Its findings that bear on this gate:
  - **F-1 (Major, email only):** the brief named the UNFILLED `session-tools/s81j/doc/handover.md`; the filled doc was the
    COMMITTED `docs/resubmission/2026-09-22_resubmission-handover-for-kam.md`. **For 2.2.1 the handover doc is `@KAM_DOC@`**;
    confirm it is FILLED FOR 2.2.1 (not the 2.2.0 values) — see Q10.
  - **F-3 (the mirror risk):** no jest cell catches a CONSISTENT wrong digest; correctness rests on the real anonymous-pull
    probe and on this gate. Unchanged by 2.2.1; now also applies to the `"2.2.1"` exception (Q3).
  - **F-6:** the build script reads the listing-list argument as a FILESYSTEM path relative to the cwd, not a git path. Run
    your Q8 rebuild with the cwd set to your own archive extract of the package commit.
  - F-2, F-4, F-5 are carried as KNOWN (§6).
- **Everything the 2.2.0 gate proved on the 2.2.0 chain (Q0-Q5: the forward merge, the step-4 re-anchors, the four red-proof
  arms, the census, C-133 by blob for all 21 ids plus the 23-id class (a) duty) is NOT re-run** — the files it proved it on
  are byte-identical between `c5da4d4` and this head except the four files in §1. Prove THAT (Q1) and cite the 2.2.0 report
  for the rest. If Q1 finds any other file changed, the 2.2.0 proofs no longer cover it and that is a finding.

## 1. Target — pinned at drafting from the object store (read-only), except `@HEAD@`
**Repo:** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files` (object store only; see §7).

| what | sha / value | how read |
|---|---|---|
| gated head | **`@HEAD@`** on `rd-665-standard-webtest-s83l` | the READY; the launcher re-pins by `ls-remote` |
| the RD-665 fix commit | `d14a975e6a325b0b246fbb85287b7831f22e5f33`, ONLY parent `c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47`, committed 2026-09-25T18:08:39+10:00, "RD-665: availability test is a Standard test, not a classic URL ping test" | `git log -1 --format='%H %P %ci %s'` |
| the submitted 2.2.0 line | `mkt-release-2.2.0-s81j` @ `c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47` (on origin; the 2.2.0 gate's head) | `ls-remote`, 18:2x AEST |
| the 2.2.0 package commit | `3464dd80854c108063facfb0355ce1a4eed5fff8` (the 2.2.0 zips were built from it; `c5da4d4` adds handover-doc commits only) | 2.2.0 brief ADDENDUM |
| image commit | `0677388ab031ffaf569a52f6c0301af48f44aece` = origin `main` at drafting | `ls-remote` |
| counts | `c5da4d4` **4121/241**; `d14a975` **4125/242** (the new suite: 4 tests) | `git show <sha>:scripts/verify-expected-counts.json` |
| `package-lock.json` | blob `906476350431e2ecb3c21070a25c64b1702c1aa8` at `c5da4d4` and at the drafter's reading of the package commit — the 2.2.0 gate's `node_modules` serves (confirm at `@HEAD@`) | `git rev-parse <sha>:package-lock.json` |
| builder's zip dir | `@ZIPDIR@` | the READY |

**The release image — UNCHANGED from 2.2.0 (no rebuild, no push):**
`nexusaireleaseacr.azurecr.io/nexusai@sha256:fdda33098c36a484b50a9a761660bb69bc53f5ed238ffceeb1bd038c8eb77f66` —
tag `2.2.0`, built from `0677388` by ACR run `cr1`. **`/api/health` `build` = `sha256("0677388ab031ffaf569a52f6c0301af48f44aece")[:16]`
= `b6f4bfddadcd4055`**; `version` `2.0.1` is RD-657 (not a failure).

**The 2.2.1 delta from the submitted 2.2.0 source (`c5da4d4..<package commit>`) is EXACTLY FOUR files:**
1. `azure-marketplace/combined/mainTemplate.json` — the ONE `Microsoft.Insights/webtests` resource (name
   `[concat(parameters('siteName'), '-availability-test')]`, unchanged): `properties.Kind` `"ping"` -> `"standard"`;
   `properties.Configuration` (the classic `WebTest` XML) REMOVED; `properties.Request` ADDED (`RequestUrl` =
   `[uri(concat('https://', <container app ingress fqdn>), '/api/health')]`, `HttpVerb` GET, `ParseDependentRequests` false,
   `FollowRedirects` true); `properties.ValidationRules` ADDED (`ExpectedHttpStatusCode` 200, `IgnoreHttpStatusCode` false,
   `SSLCheck` false); the resource's `comments` rewritten. **Nothing else** — the availability metric alert's `webTestId` and
   `scopes` still name the same resource id, so the alert is unchanged. `contentVersion` stays `1.3.0.0`.
2. `__tests__/rd665-standard-availability-test.test.js` — NEW, 4 cells (the shipped template passes the rule; the Standard
   test keeps the ping test's behaviour; CONTROL: the rule rejects an alert pointing at another webtest; CONTROL: the rule
   rejects the classic ping test).
3. `scripts/verify-expected-counts.json` — 4121/241 -> 4125/242.
4. `azure-marketplace/release-policy.json` — in the PACKAGE commit (after `d14a975`): `imageTagExceptions` gains exactly
   `"2.2.1": {"image": <the SAME release reference>, "reason": …}`; the `"2.2.0"` entry and `imagePlaceholder` byte-unchanged.

**Where "2.2.1" must appear, and where it CANNOT:** the version is the build script's `<version>` argument. It appears in the
two zip FILE NAMES, the manifest file name and its first line ("version 2.2.1, commit <sha>"), the manifest's tag-exception
check line, and the `release-policy.json` exception key. **It appears in NO file inside either zip** — `mainTemplate.json`
and `viewDefinition.json` carry `contentVersion` `1.3.0.0` and `createUiDefinition.json` `version` `0.1.2-preview`, all
unchanged since 2.2.0. The Partner Center version is typed by Kam at upload.

## 2. Why tier 1, and who is waiting
The zip is the artefact Kam uploads to Partner Center himself to replace the LIVE 2.2.0 plan package. **RD-665 (Highest):**
on the live 2.2.0 listing, telemetry "Enabled" fails the customer deployment because Azure refuses to create new classic
URL ping tests (BadRequest "Value cannot be null. Parameter name: format"), and Microsoft retires URL ping tests on
2026-09-30. A 2.2.1 that is wrong in any other way ships to every Marketplace customer. Tuesday emails it on your GO; there is
no further check. A NO GO with its evidence is on time.

## 2a. LEGITIMATE SHAPES — the checkers in this gate are `scripts/marketplace-package-build.sh` and the new RD-665 rule
| shape — its ordinary form | expected verdict | the rule clause that yields it | predicted-by |
|---|---|---|---|
| non-draft build of the SHIPPED files at the package commit, version `2.2.1` | exit 0, `MANIFEST COMPLETE: N checks, 0 failed` (builder: 32), two zips + manifest | tag check: tag differs from version but `imageTagExceptions["2.2.1"].image` equals the image exactly | drafter (read the builder's manifest) |
| same files, version argument `2.2.0` | exit 0 (the `"2.2.0"` exception is still present) | same clause, other key | drafter — measure |
| same files with the `"2.2.1"` key REMOVED, version `2.2.1` | exit 1, "no exception for exactly this image" | exact-match exception keyed by VERSION | drafter — **nobody has run this; you do** |
| `"2.2.1"` image one hex character off, version `2.2.1` | exit 1 | exact-match exception | drafter — you do |
| the shipped template | the RD-665 rule passes (the new suite green) | the rule in `rd665-standard-availability-test.test.js` | builder |
| the webtest put back to the `c5da4d4` ping block (a COPY) | the RD-665 rule FAILS (`Kind is "ping"`) | same rule | builder CONTROL; you re-run independently |
| a leftover zip in the out-dir | exit 2, nothing written | RD-527 | S78G |
| anonymous pull probe answers 401 | exit 1 non-draft, WARN draft | C-58 item 4 | drafter |

A row whose verdict and clause disagree is a finding against this brief — report it as such.

## 3. THE BUILDER'S CLAIMS — verify each, relay none
From the READY (`@READY_MAIL@`, read it whole; where the READY and this list disagree, the READY's measurement is the claim
and the disagreement is a finding) and `HANDOVER-S83L.md`:
1. **Fix:** `rd-665-standard-webtest-s83l` @ `d14a975`, off `c5da4d4`, 3 files; verify 4125/4125, 242 suites; arm-ttk 49/49;
   the RD-665 cell red-proofed.
2. **Create-time proof (customer-test sub `73e9b141`, tenant `ec01829b`, `rg-nexusai-customer-test`):** the deployment
   Succeeded; the webtest read back `Kind` `standard`; the availability alert's `webTestId` points at it; 6/6 availability runs
   Passed; the test then DISABLED. On disk: `evidence-s83l-customer-test/RD665-webtest-readback.json`,
   `RD665-alert-readback.json`, `RD665-availability-results.json`.
3. **Package:** version `2.2.1`, image digest unchanged, `release-policy.json` gains `imageTagExceptions["2.2.1"]` with the
   same image; built non-draft into `@ZIPDIR@`; arm-ttk on the package commit (`session-tools/s83l/armttk-<sha7>.txt`).

## 4. WHAT TO ATTACK, in order. Answer each with a measurement.

**Q0 — the frame.** Re-pin at start, mid and end: `@HEAD@` on `rd-665-standard-webtest-s83l`, `c5da4d4` on
`mkt-release-2.2.0-s81j`, and `main` (three timestamped readings, branch name beside each sha). Confirm `d14a975`'s ONLY
parent is `c5da4d4`, the package commit's ONLY parent is `d14a975` (or state the chain exactly), and the head descends from
the package commit with ONLY `docs/resubmission/` between them. `main` moving past `0677388` is NOT a refusal (C-149 pins the
image) — report what moved.

**Q1 — the delta, exactly, and the 2.2.0 proofs still cover everything else.** `git diff --name-only c5da4d4 <package commit>`
= the four files of §1, no more, no fewer; `git diff --name-only 3464dd8 c5da4d4` = only the 2.2.0 handover doc (the
baseline the 2.2.0 zips were built from). Parse both templates and prove they are identical except the webtest resource's
`comments`, `properties.Kind`, `properties.Configuration` (removed), `properties.Request` and `properties.ValidationRules`
(added). Prove `variables.containerImage` is the release reference at both. Prove the metric alert whose criteria are
`WebtestLocationAvailabilityCriteria` is byte-identical and its `webTestId` resolves to the webtest's own resource id. Parse
both policies: identical except `imageTagExceptions`, which gains exactly `"2.2.1"`; `"2.2.1".image` == `"2.2.0".image` ==
the release reference, character for character; `imagePlaceholder` byte-unchanged.

**Q2 — (a) the RD-665 fix in the PACKAGED template, not only in git.** From YOUR COPY of the builder's plan zip: the zipped
`mainTemplate.json` has exactly ONE `Microsoft.Insights/webtests` resource; `properties.Kind` == `"standard"`; no
`properties.Configuration`; no `<WebTest` string anywhere in the file; `properties.Request.RequestUrl` targets `/api/health`
on the Container App ingress fqdn, `HttpVerb` GET; `ValidationRules.ExpectedHttpStatusCode` 200; `Frequency` 300, `Timeout`
30, `RetryEnabled` true, the same three `Locations` as the ping test at `c5da4d4`; `condition` still
`[parameters('enableTelemetry')]`; `apiVersion` `2022-06-15` accepts the Standard shape (READ ONLY against Microsoft's
published schema, cite it). **The "no ping" check is SCOPED, not a text search:** the zipped file contains the substring
"ping" legitimately — the webtest's own `comments` explain the ping-to-standard conversion, the Azure OpenAI setup check sends
the word `'ping'` as a 1-token prompt, and identifiers such as `kvWrappingKeyName`/"mapping" contain it (the drafter counted
18 case-insensitive hits). The binding checks: no JSON key or value under ANY webtest resource's `properties` equals or
contains "ping" (case-insensitive), no `"Kind": "ping"` anywhere, no `<WebTest` anywhere. List every remaining "ping" hit
with its JSON path and classify it. Then, on a COPY: put the `c5da4d4` ping block back into the webtest and run the RD-665
suite — it must redden (the builder's CONTROL, re-run by you with your own mutant); point the alert's `webTestId` at another
name — must redden. `node --check` / `JSON.parse` every mutant, quote exit codes; a red from a mutant that does not parse is
**VOID**. Census (READ ONLY, scoped `git grep` on `__tests__ scripts azure-marketplace bicep deployment` at the head): is any
other file still carrying a classic ping test or pinning `Kind` `ping`? (Drafter: only the new test file, as its CONTROL.)

**Q3 — (b) the version, everywhere it must appear, and the red-proof arms.** Measure: both zip file names and the manifest
file name carry `2.2.1` and the package commit's sha7; the manifest's first line reads `version 2.2.1, commit <the full
package commit sha>`; its tag-exception check line names version 2.2.1 and quotes the `"2.2.1"` reason; `release-policy.json`
has the `"2.2.1"` key. Confirm NO zipped file needed a version bump (contentVersion `1.3.0.0` and createUiDefinition `version`
unchanged vs 2.2.0 — say whether that is right for a Partner Center plan update, READ ONLY). **POSITIVE CONTROL FIRST:** the
clean files at the package commit green (the RD-665 suite 4/4, and the two 2.2.0 package suites 55/55 and 17/17). Then YOUR
OWN arms, each on a fresh copy, through the REAL build script with a stub anonymous-pull probe answering 200 where the
registry must not decide the result: **V1** the `"2.2.1"` key removed, version 2.2.1 → predicted exit 1; **V2** the `"2.2.1"`
image one hex off → predicted exit 1; **V3** version argument `2.2.0` on the shipped files → predicted exit 0. **The jest
coverage gap, predicted by the drafter:** every package cell builds with version `'2.2.0'` (`SHIPPED_VERSION = '2.2.0'` in
`__tests__/marketplace-package-build.test.js:45`, and `'2.2.0'` hard-coded in `marketplace-single-build-path.test.js:166,185`
and `__tests__/helpers/shipped-plan-build.js:35`), so **NO jest cell reads the `"2.2.1"` exception** — run V2 through the named
package suites and report whether anything reddens. If nothing does, that is a finding (the `"2.2.1"` exception is guarded only
by the real build's check and by this gate); state its evidence class.

**Q4 — (c) the image is unchanged and still anonymously pullable.** The zipped `variables.containerImage` equals, character
for character, the 2.2.0 zip's (`NexusAI_plan-managed-ai_2.2.0_3464dd8.zip`) and the release reference. **Re-verify anonymous
pull YOURSELF, without touching the shared Docker image store:** anonymous token from
`https://nexusaireleaseacr.azurecr.io/oauth2/token?service=nexusaireleaseacr.azurecr.io&scope=repository:nexusai:pull` with
NO credentials; GET the manifest by digest with that token; **the sha256 of the manifest bytes must equal
`fdda33098c36a484b50a9a761660bb69bc53f5ed238ffceeb1bd038c8eb77f66`**; GET the config blob and one layer by digest and hash them;
labels `revision` = `0677388ab031…`, `version` = `2.2.0` (the IMAGE version; 2.2.1 is a template-only release), `source` empty
by ruling. NEGATIVE CONTROLS in the same window: the manifest GET with no token = 401; an anonymous token request to
`nexusaidevacrfa39.azurecr.io` refused. **Never `docker rmi` the release image.** If you `docker pull`, use a fresh
`DOCKER_CONFIG` holding `{}`, pin `DOCKER_HOST`, read the exit code. Optional smoke boot under the docker lock: health `build`
`b6f4bfddadcd4055`. The demo read-back (C-58 item 1b) was done by the 2.2.0 gate and the image has not changed: at most ONE
`GET /api/health` to `https://nexusaidev-app.politeforest-b008d469.australiaeast.azurecontainerapps.io/api/health` (client
timeout 20 s), `build` must be `b6f4bfddadcd4055`; the revision read-back by `az` is kept only if §9's clause stands.

**Q5 — (d) the 2.2.1 zips against the 2.2.0 zips, entry by entry.** Copy the four zips (both versions, from
`/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/marketplace-submission-2026-09-25-2.2.0` and `@ZIPDIR@`) into your own
dir and hash them at start and end (2.2.0: plan `18155587c6cb0141b35d082b25fcccae9f3b8683189208dac3cf701790eef21c`, listing
`c333f95c328c1a0dceb19b9a47ec16721d05742b597d6659446c25159da7ecbe` — these are the zips live in Partner Center; if either
changed on disk, that is a finding). **Rule: the entry-name sets must be identical, and the ONLY entry whose bytes may differ
is `mainTemplate.json`, and inside it ONLY the webtest resource (its `comments`, `Kind`, `Configuration` -> `Request` +
`ValidationRules`).** `createUiDefinition.json`, `viewDefinition.json` and all 7 listing entries must be byte-identical to
2.2.0's. The version fields, `release-policy.json` and the handover doc are NOT zip entries — their differences are checked in
Q1/Q3/Q10, and one appearing INSIDE a zip is itself a finding. Any other difference = finding. Whole-file zip shas WILL
differ (entry timestamps: the listing entries carry the commit time via `git archive`, the plan entries the build time via
`cp` without `-p`) — not a finding on its own. Drafter's READ ONLY pre-reading of the builder's zips agrees with the rule;
you measure it.

**Q6 — REBUILD the package yourself and compare with the builder's zip.** With the cwd inside your own `git archive`
extract of the package commit (2.2.0 gate F-6), into a NEW empty out-dir:
`bash scripts/marketplace-package-build.sh /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files <package commit> 2.2.1 <your-empty-out> azure-marketplace/listing-assets.txt`
(the script reads the repo through `git archive` / `rev-parse` only; its probe contacts `nexusaireleaseacr.azurecr.io` only).
**Predict first:** the listing zip's whole-file sha256 should EQUAL the builder's; the plan zip's probably will NOT (cp
without -p). **The binding comparison is PER ENTRY:** every entry in both zips, yours and the builder's, == `git show <package
commit>:<source path>` (plan: `mainTemplate.json` <- `azure-marketplace/combined/mainTemplate.json`,
`createUiDefinition.json` <- `azure-marketplace/plans/managed-ai/createUiDefinition.json`, `viewDefinition.json` <-
`azure-marketplace/combined/viewDefinition.json`; listing: the paths in `azure-marketplace/listing-assets.txt`). Both
manifests end `MANIFEST COMPLETE: <N> checks, 0 failed`; `diff` them and explain every differing line. No `DRAFT-` or
`FAILED-` file and no other zip in `@ZIPDIR@`.

**Q7 — arm-ttk.** `bash /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/s78g/armttk.sh /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files <package commit> pkg221`
(`TMPDIR` set inside your own project first); quote `TOTAL N/M PASS` (builder claims 49/49; 2.2.0 was 49/49). Both controls,
`hideconf` and `hardloc`, must fire — **a 49/49 without a control that fired is not reportable.** Then the same `Test-AzTemplate`
call on the three files unpacked from the builder's plan zip. Say whether arm-ttk has any test that inspects webtests at all
(if not, its 49/49 says nothing about RD-665).

**Q8 — (e) the create-time proof: RELAYED, not re-tested.** Read the three `evidence-s83l-customer-test/RD665-*.json` files
and report what they show and what they do NOT: (i) the webtest read-back — `properties.Kind` `standard`,
`provisioningState` `Succeeded`, `Request` and `ValidationRules` in the shape above, **`Enabled: true` at read-back**; (ii) the
alert read-back — `criteria.webTestId` equals the webtest's id; (iii) 6 availability rows `Passed` from 3 locations. Then say
plainly: **there is no deployment-operation record on disk for "deployment Succeeded"** (only the webtest's own
`provisioningState`), **no artefact showing which template (git blob) was deployed**, and **no artefact showing the test was
later DISABLED** (the read-back says `Enabled: true`) — each is a CLAIM from the READY, evidence class RELAYED. **This gate does
NOT use Azure in the customer-test tenant:** §9 permits read-only `az` under NexusAI's OWN identity in the dev environment only;
`session-tools/s83l/ct-az.sh` pins a DIFFERENT identity (`4_Credentials/.azure-customer-test`, tenant `ec01829b`), and a
what-if is a POST to Resource Manager, not one of §9's read verbs. So the create-time behaviour of the 2.2.1 template is **NOT
RE-TESTED** by this gate — list it under NOT TESTED. If Tuesday grants a what-if at stamping, it appears as a signed line in
§9; absent that line, it is HELD.

**Q9 — no secrets in what Kam receives.** gitleaks over the UNPACKED contents of BOTH 2.2.1 zips, the manifest, and the
handover doc `@KAM_DOC@` (copies in your own dir): once with the repo's `.gitleaks.toml` at the head and once with the default
rules. **POSITIVE CONTROL FIRST:** a canary the ruleset TARGETS (C-103) planted in a copy must fire in the same run. Report the
gitleaks version and how it ran.

**Q10 — the handover doc for 2.2.1.** `@KAM_DOC@` is what goes to Kam with the zip. The committed doc at `c5da4d4`
(`docs/resubmission/2026-09-22_resubmission-handover-for-kam.md`) names the 2.2.0 zips, `3464dd8` and 4121/241; the drafter
found it UNCHANGED at the builder's package commit. Read `@KAM_DOC@` against YOUR measurements: version 2.2.1, the package
commit, both zip file names and sha256s, the manifest's last line, the digest (unchanged), the counts 4125/242, the arm-ttk
result, and a plain sentence that 2.2.1 replaces 2.2.0 BECAUSE OF RD-665 (telemetry Enabled fails at deploy) with the image
unchanged. Any `<filled at build>` or `@@…@@` left, any 2.2.0 value presented as 2.2.1's, or any value that disagrees with
your measurement is a finding (it goes to Kam in the same email). It must also say what the package does NOT prove (§5).

**Q11 — the full verify at the head.** Under the jest lock, `env -u SESSION_SECRET` (print SET/UNSET as the hold's first
line, the NAME only), `npm run verify -- --maxWorkers=2` (C-81) on a tree you built from `@HEAD@`. Predicted **4125/4125, 242
suites** — confirm or contradict against the counts file at the head. Then the RD-665 suite and the named package suites
(`marketplace-*`, `rd461-*`, `rd471-*`, `rd472-*`, `rd503-*`, `dev-scripts-template-parameters*`) once more by name. C-89: the
head's counts file equals what `--update-counts` would write (measure on your own copy; never write into the NexusAI repo).
Q2 (strictly stronger, nothing deleted): list every test id at `c5da4d4` and at the head (same runner) — the ONLY change
allowed is the 4 new RD-665 ids; any missing id is a **Major**.

## 5. KNOWN RESIDUALS — list them in the verdict, do NOT fail on them
- **RD-657** — `/api/health` reports `"version":"2.0.1"` on the (unchanged) 2.2.0 image. **Not a failure.**
- **Stale comment** at `scripts/marketplace-package-build.sh:37-38` ("every build fails today"). Does not ship.
- **C-124 — UPDATED 2026-09-25 (S83L):** the Key Vault success path has now been OBSERVED AT LOG LEVEL on the 2.2.0
  customer test in `73e9b141` ("DEK unwrapped via KV … using user-assigned managed identity", `T4-restart-log.json`); the
  `/api/admin/health` fields (`keyVaultStatus: configured`, `encryptionKeyMode: kv-wrapped`) are still NOT measured. Report
  it in exactly those terms: a GO must not read as "the Key Vault feature works" beyond that log line.
- **C-20** — this gate does not validate or deploy the template against real Azure. The builder's customer-test deployments
  in `73e9b141` (2.2.0, and the 2.2.1 create-time proof) are RELAYED evidence, labelled "not a clean tenant" (C-157).
- **2.2.0 gate F-3** — no jest cell catches a consistent wrong digest; now joined by the Q3 gap for `"2.2.1"` if measured.

## 6. KNOWN — do NOT report as new
2.2.0 gate F-2 (the image ships main's `DEPLOYMENT_GUIDE.md`/`README.md`), F-4 (the renamed describe covering the RD-527
cells), F-5 ("Status: DRAFT." in the 2.2.0 handover doc) · RD-658 · RD-656 · RD-580 · RD-642 · RD-644 · RD-666, RD-667, RD-668
(filed by S83L) · the dev-scripts residuals S78G listed · the NexusAI `2_Project_Files` checkout is a stale snapshot with a
dirty tree (C-28) · CI has not run at `@HEAD@` (§10) · the image's `source` label is empty BY RULING.

## 7. Trees, and where you may write
- **Build your own trees INSIDE YOUR OWN PROJECT** (Testing Agent MAIN), from the object store:
  `git -C <repo> archive <sha> | tar -x -C <a fresh mktemp -d under projects/nexusai/qa-trees/pkg221.XXXXXX/>`.
  `node_modules`: an APFS clone (`cp -c -R`) of the 2.2.0 gate's or gate 8's; `package-lock.json` blob `9064763` must hold at
  `@HEAD@` — confirm.
- **Each tree is EXCLUSIVE to this gate and to ONE purpose**: a fresh `mktemp -d` per arm; never reuse a mutant tree for a
  clean arm; `pkg221`-prefixed directories only. Earlier gates' trees are their evidence — copy from, never run in.
- **NexusAI repo: read verbs only** (`show`, `log`, `diff`, `ls-remote`, `rev-parse`, `ls-tree`, `cat-file`, `grep`,
  `merge-base`, `archive`). **Never `fetch`, `pull`, `push`, `checkout`, `worktree`, `commit`, `stash`, `gc`, `clean`, or
  `merge-tree --write-tree` against it** (C-28, C-67), and never work in its `2_Project_Files` checkout, its `worktrees/`,
  `session-tools/`, `evidence-s83l-customer-test/` (read only) or `1_Project_Definition/`. Count
  `find <repo>/.git/objects -type f` before and after and account for any delta by mtime (the live NexusAI seat commits into
  the same object store).
- **Never write into `@ZIPDIR@` or `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/marketplace-submission-2026-09-25-2.2.0`**
  — copy before unzipping; hash at start and end.
- **NEVER `rm`** — quarantine (template §5).

## 8. Floor discipline — THE FOUR CLAUSES, plus THE DEADLINE RULE
1. **Every jest run goes through `session-tools/nexusai-lock.sh jest <tag> …`, tagged `qa-pkg221-…`** (C-141; C-110).
   **QUEUE, NEVER TAKE OVER:** never kill, signal, move or edit another seat's process, lock directory, owner file or ticket.
   Any docker leg goes through the **docker** lock the same way.
2. **Hold the lock ONCE per multi-run measurement,** as a TRACKED CHILD of your seat — never detached (`nohup … &`).
3. **Record the foreign server count beside every result, the RD-606 form anchored on YOUR OWN claude pid.** NEGATIVE
   controls, read at drafting ~18:30 AEST from `tmux list-panes -a` + `ps`: NexusAI seat claude **`29171`** (pane `%8`) and
   Tuesday's claude **`60235`** (pane `%0`, launcher `59586`). Re-read them at start; a hold with NO live negative control
   aborts. Reuse the instrument BY COPY with YOUR pid as `ROOT`:
   `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-22-gate7-rd645/evidence/qa-floorcount.py`
   and `…/qa-floorlib.sh` (its first line names gate 7's pid — correct it).
4. **A zero is reportable only beside a control that fired in the same window** — the floor count, gitleaks' zero, the
   scoped "no ping" check (Q2's re-inserted ping block is its control), and "no other zip" in the out-dir all included.

**5. THE DEADLINE RULE:** every real-server probe and every network request has a per-step **DEADLINE** and a client timeout
(boot 60 s, request 30 s, registry call 30 s, exit 20 s); every server you start is killed in a **`finally`** (SIGTERM, then
SIGKILL after a grace) and the reap confirmed by your counter; log a **HEARTBEAT** line (timestamp, step, pid, elapsed) at
least every **2 minutes** during any hold; a step with no heartbeat for **5 minutes** is aborted and reported. Never wait
out a lock window.

## 9. Drivable surface, network and identity
- Product probes run on **127.0.0.1** against servers YOU boot (or the release image you boot locally).
- **External hosts you MAY contact, and nothing else:** `nexusaireleaseacr.azurecr.io` (anonymous token + manifest/blob GETs,
  and the build script's own probe), `nexusaidevacrfa39.azurecr.io` (ONE anonymous token request, the negative control), the
  demo's `GET /api/health` at most once (Q4). No login, no POST, no rendered page on the demo (RD-76, C-84). **Nothing in the
  customer-test deployment** (`nxcusttest-*`, tenant `ec01829b`) — not even a GET; its evidence is read from disk.
- **Azure: READ-ONLY az only, and only if Tuesday leaves this clause standing at stamping** — `az account show`,
  `az containerapp show`, `az containerapp revision list|show`, under NexusAI's own `AZURE_CONFIG_DIR` (the launcher exports
  it; tenant `d500ebad-cf53-4f2a-a501-f831289e67fc`, subscription `0c57ab37-349c-47ae-a10f-e284a380bbb9`). Any other az verb,
  any write, any what-if, any `az login` or tenant switch, and **any use of `session-tools/s83l/ct-az.sh` or
  `4_Credentials/.azure-customer-test`: HELD**. An authorization error is the boundary working — report it, never work around it.
- If a response is cut off by a safety check, record it and continue; this is authorised defensive QA of Datasec's own
  product and release artefacts.

## 10. CI (C-142) and HELD
- **CI NOT RUN at `@HEAD@`** (no PR). CI on the image commit `0677388`: Build 35811343989 green, RELAYED — `gh`, if used at
  all, is READ-ONLY.
- **HELD:** no push, no merge, no tag, no registry change, no demo change, nothing in the customer-test tenant, **no Partner
  Center (C-23: Kam resubmits himself)**, no production, no money, no external comms, no mail to any human. **Never merge**
  `rd-665-standard-webtest-s83l` anywhere (C-158: main stays untouched unless Kam rules otherwise). **Findings-only:** no
  commits, no tickets, no edits anywhere in NexusAI. Your Q6 rebuild is evidence in your own directory, never a replacement
  zip.
- **Prior-work check (standing):** before calling anything missing, wrong or new, search what was built before and why — the
  2.2.0 report, `HANDOVER-S83L.md`, CLARIFICATIONS, the ticket named in the code comment — and cite it.

## 11. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-25-pkg-gate-221/report.md`

**Questions:** your routing name is **`QA/NexusAI-pkg221`**. If you must ask, mail `tuesday-agent@agentmail.to`, subject
`[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>` (Context / one Question / Meanwhile / Needed-by), and **proceed on the
safest reading** without waiting. Tuesday's answer arrives in `tuesday-agent@agentmail.to` with a subject beginning
`[Tuesday -> QA/NexusAI-pkg221] ANSWER` — read it with the AgentMail key below. If two answers differ, STOP that item and ask
which stands. Approval-class items (anything touching the demo, the registry, Azure beyond §9, Partner Center, money, or a
human) never proceed on a safe reading — they are NOT RUN and named.

**MAIL YOUR VERDICT** to `tuesday-agent@agentmail.to`, subject beginning exactly:
`[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — package gate 2.2.1: ` followed by `GO`, `GO WITH FINDINGS` or
`NO GO FOR UPLOAD`, then ` @ ` and the first 7 characters of the pinned head. **Never `wednesday-agent@`.**

AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env` (absolute path: the QA project
has none). Never put the key, or any secret, in a mail or the report.

**Verdict format** (lead with it; one sentence first: *is the zip at `@ZIPDIR@` ready for Tuesday to email to Kam, and if
not, what stops it*):
- the frame (Q0) with three timestamped head readings, branch names beside each sha;
- the delta (Q1); the RD-665 fix in the PACKAGED template with the scoped no-ping check and its control (Q2);
- the version sites and arms V1-V3 plus the jest coverage gap (Q3), each with its `node --check` / parse exit code;
- the image unchanged and pulled anonymously by you (Q4); the 2.2.0-vs-2.2.1 entry diff (Q5); the rebuild per entry and per
  whole file (Q6); arm-ttk N/M with both controls (Q7);
- the create-time proof, RELAYED, with what its evidence does and does not show (Q8); gitleaks with its canary (Q9); the
  handover doc check (Q10); the full verify and the test-id account (Q11);
- §5's residuals listed by name; every action recommendation labelled **MEASURED AT RUNTIME**, **PROBED** or **READ ONLY**.
- **Rule 2: a NOT TESTED section.** It MUST carry this line, verbatim:

  Real Azure: not deployed through Partner Center; the 2.2.1 template was not deployed, validated or what-if'd against real Azure by this gate (the builder's create-time proof in 73e9b141 is RELAYED, not re-tested); the Key Vault success path is observed at log level only (C-124 update), its admin-health fields never measured; the jest suites are not network-sandboxed (C-58).

- **Run long commands in the FOREGROUND; never end a turn waiting on a background notice** — you have no inbox that wakes you.

## WRONG AT SOURCE — what this brief found when it checked the commission against the repo
1. **"The package head SHA is not known yet" — it existed at drafting, locally.** `refs/heads/rd-665-standard-webtest-s83l`
   = `3f79e9cb8ed8834e08a1744af8bbbd5823d4303a` ("2.2.1 package commit: release-policy imageTagExceptions["2.2.1"] = the 2.2.0
   image", parent `d14a975`, 18:15:42 +1000); **origin still held `d14a975`**. The builder's zips were ALREADY built from it:
   `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/marketplace-submission-2026-09-25-2.2.1/` holds
   `NexusAI_plan-managed-ai_2.2.1_3f79e9c.zip` (sha256 `5fb54789…72dd`), `NexusAI_listing-assets_2.2.1_3f79e9c.zip`
   (`ba29c189…a7e7`), `MANIFEST-2.2.1_3f79e9c.txt` ending `MANIFEST COMPLETE: 32 checks, 0 failed`. The placeholders are kept
   as commissioned; C-113 still requires the branch at origin before launch, and the launcher enforces it.
2. **"no 'ping' anywhere in the zipped template" cannot hold as a text rule.** The shipped template has 18 case-insensitive
   hits: the RD-665 comment itself, the Azure OpenAI check's `'content': 'ping'`, and `kvWrappingKeyName`/"mapping". Q2 scopes
   it to the webtest resources' `properties` plus `"Kind": "ping"` and `<WebTest`.
3. **"the version field 2.2.1 everywhere it must appear" — no shipped file carries a version.** `contentVersion` is `1.3.0.0`
   and createUiDefinition `version` `0.1.2-preview`, both unchanged; 2.2.1 lives in file names, the manifest and the policy key.
4. **"only differences allowed: the template webtest, the version fields, and release-policy/handover docs" — the last two are
   not zip entries.** The plan zip is three files and the listing zip seven images; Q5 allows ONE differing entry
   (`mainTemplate.json`, webtest only). Drafter's pre-reading of the builder's zips: exactly that.
5. **"test then disabled" — no artefact on disk shows it.** `RD665-webtest-readback.json` reads `Enabled: true`; no later
   read-back or deployment-operation record exists in `evidence-s83l-customer-test/`. "Deployment Succeeded" is likewise
   supported only by the webtest's `provisioningState`. RELAYED (Q8).
6. **"the gate may re-run a what-if through ct-az.sh ONLY if the template allows a gate to use Azure" — it does not.** The 2.2.0
   brief §9 allows read-only `az` under NexusAI's OWN config in the dev tenant; ct-az.sh uses the customer-test config in
   tenant `ec01829b`, and what-if is not a read verb. Stated as NOT RE-TESTED.
7. **The 2.2.0 standing NOT TESTED line is partly FALSE now.** "the Key Vault success path never executed (C-124)" is
   superseded by C-124's 2026-09-25 update (observed at log level); "not validated against real Azure (C-20)" is superseded
   for the builder (2.2.0 deployed in `73e9b141`, C-157). The line is REWORDED for this gate (§11); the launcher checks the new
   wording.
8. **No jest cell reads the `"2.2.1"` exception** (every package cell builds version `'2.2.0'`). A wrong `"2.2.1"` image would
   stay green in the suite. Q3 measures it.
9. **The handover doc for 2.2.1 did not exist at drafting.** The committed doc is unchanged between `c5da4d4` and `3f79e9c`
   and describes 2.2.0. `@KAM_DOC@` is a new placeholder (the 2.2.0 gate's F-1 shows why the path must be named exactly).
10. **The 2.2.0 negative-control pids `11382` and `2679` have exited;** re-read as `29171` (NexusAI, `%8`) and `60235`
    (Tuesday, `%0`).
11. **The routing name `QA/NexusAI-pkg221` has no line in `fleet/inbox_routing.conf`** (only `QA/NexusAI-pkg220`, line 86).
    The launcher refuses until Tuesday adds `QA/NexusAI-pkg221|tuesday-agent@agentmail.to|no`.

## PROVENANCE (drafter, 2026-09-25 ~18:20-18:50 AEST, read-only)
- origin: `main` `0677388ab031…`, `mkt-release-2.2.0-s81j` `c5da4d4d77b7…`, `rd-665-standard-webtest-s83l` `d14a975e6a32…`,
  `s83l-customer-test-plan` `549bb7885b8b…` | `git ls-remote origin <refs>`
- local `refs/heads/rd-665-standard-webtest-s83l` = `3f79e9cb8ed8…`; `d14a975` parent `c5da4d4`; `3f79e9c` parent `d14a975` |
  `git rev-parse`, `git log --format='%H %P %ci %s'`
- `git diff --stat c5da4d4 d14a975` = 3 files (template 16 +/-, new test 80 +, counts 6 +/-); `git diff d14a975 3f79e9c` = policy
  +4 lines (the `"2.2.1"` entry only) | `git diff`
- counts `c5da4d4` 4121/241, `d14a975` and `3f79e9c` 4125/242 | `git show <sha>:scripts/verify-expected-counts.json`
- template blob `006dc5c…` at `c5da4d4` and `3464dd8`; `93ecbca…` at `3f79e9c` (sha256 `f91ee8f1…8e18`, which the builder's
  manifest quotes) | `git rev-parse`, `shasum`
- `package-lock.json` blob `9064763…` at `c5da4d4` and `3f79e9c` | `git rev-parse`
- the zipped 2.2.1 template vs the zipped 2.2.0 one: structural diff = `resources[3]` (the webtest) `comments`, `Kind`,
  `Configuration` removed, `Request` + `ValidationRules` added; `createUiDefinition.json`, `viewDefinition.json` and all 7
  listing entries byte-identical | python `zipfile` in memory (no file written)
- scoped census: `git grep` for webtests / ping kind / `<WebTest` on `__tests__ scripts azure-marketplace bicep deployment` at
  `3f79e9c` → only `__tests__/rd665-standard-availability-test.test.js` (its CONTROL) and the template | `git grep`
- version use: `marketplace-package-build.sh` lines 2-7, 52-59, 294, 332-335, 409 at `3f79e9c`; `SHIPPED_VERSION = '2.2.0'`
  and `'2.2.0'` literals in the package tests | `git show`, `git grep`
- 2.2.0 zips on disk: plan `18155587…021c`, listing `c333f95c…ecbe` (= the 2.2.0 brief's values) | `shasum -a 256`
- `session-tools/s83l/ct-az.sh` (customer-test config, forbidden-tenant refusal list), `armttk-3f79e9c.txt` ("TOTAL 49/49 PASS")
  | `cat`
- `evidence-s83l-customer-test/RD665-{webtest,alert}-readback.json`, `RD665-availability-results.json` (6 rows Passed, 3
  locations, 08:11:38Z-08:13:17Z) | `cat`
- CLARIFICATIONS C-124 :1307 (+ UPDATE :1318), C-156, C-157 :1612, C-158 :1619, C-159 :1625; HANDOVER-S83L lines 36-49 |
  `grep -n`, `sed -n`
- 2.2.0 gate report `2026-09-25-pkg-gate-220/report.md`: GO WITH FINDINGS @ `c5da4d4`, F-1..F-6 | `head`
- seats: pane `%8` -> claude `29171`; Tuesday claude `60235` (parent `59586`, pane `%0`) | `tmux list-panes -a`, `ps`
- `fleet/inbox_routing.conf`: `QA/NexusAI-pkg220` at line 86, no `pkg221` | `grep`

## FILL AT READY — Tuesday, before stamping (the launcher refuses until each is done)
- the HEAD placeholder (the token HEAD between two @ signs) -> the full 40-hex gated head, in THIS brief and in the launcher
  (`sed` both; the placeholder comparands in the launcher are built by concatenation so the `sed` cannot reach them).
  The branch must be at origin at exactly that sha.
- the ZIPDIR placeholder -> the absolute directory holding the builder's non-draft 2.2.1 zips and manifest.
- the READY_MAIL placeholder -> the absolute path of the builder's READY FOR PACKAGE GATE sent copy.
- the KAM_DOC placeholder -> the absolute path of the handover doc that will go to Kam WITH the 2.2.1 zip (a committed doc may
  be named as a path under the repo only if the launcher can read it; otherwise a file copy in the builder's session-tools).
- The routing line `QA/NexusAI-pkg221|tuesday-agent@agentmail.to|no` in `fleet/inbox_routing.conf`, and the ANSWER prefix.
- §9's read-only az clause: keep it or strike it. A what-if in `73e9b141` is HELD unless you add a signed line here saying so.
- The negative-control seats in §8 if either pid has exited.
- Both STAMP placeholders (the SELF-CHECK line and the Self-check note) — LAST. Stamp them by hand, not with a global `sed`,
  and write no placeholder token into the note.
