# QA GATE BRIEF — Secuura/Blockchain PR #951 (KS-1041 Step 2) — TIER 1, ROUND 2 OF 2

**Charter — read first, in full:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`

PRIOR ROUND: round 1 gated `dd0a0c934a58d9293cfe54f6e6daca49191bf6f9`, verdict **NO GO**.
ITS REPORT IS ON DISK AT: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-11-ks1041-951-dd0a0c934-tier1/` (`report.md` + `evidence/`)
Findings carried forward and their disposition: **F1** fixed on `02a22f4bb` · **F2** fixed on `02a22f4bb` (three new wiring test files) · **F3 + F4** NOT in the PR by Wednesday's scope ruling — one follow-up ticket, being filed by the builder; the PR body now opens with an inert-until-provisioned, gateway-first warning · **F5** recorded in the PR body as latent, not fixed · **F6** corrected in the PR body and the bicep comment.

## WHY THERE IS A ROUND 2 — AND WHY IT IS THE LAST

Round 1's deciding finding: the gateway minted `x-gateway-vouch` onto every proxied request, so 15 non-originate upstreams could replay it to originate. **Round 2 is the builder's fix.** **This is round 2 of 2 under the cap: a NO GO here does not open a round 3 without Kam.** Be exact about which findings, if any, would decide a NO GO.

## TARGET

- **PR #951** — branch `kamilkreiser/ks-1041-gateway-provenance-middleware`, head **`02a22f4bbc46a66983c3752a5a12394ff5b1afaf`** (parent `dd0a0c934`), 2 commits, 15 files, +1245 −18.
- **Merge-base `0f8fb33c3416eaa5a79b980402deb845312b20ae`**; `develop` is now `2d864ae9220c57ddcd8dc77af1b80fbd8001d530`, **17 commits past it** (12 squash merges this morning). **Diff against the MERGE-BASE for the PR; diff `dd0a0c934..02a22f4bb` for what round 2 changed** (7 files: `proxy.ts`, `gatewayProvenance.ts`, `services.bicep`, `ENVIRONMENT-VARIABLES.md`, and three new test files `ks1041-vouch-mint-scope`, `ks1041-edge-strip-wiring`, `ks1041-provenance-mount-wiring`).
- **Re-derive whether any of develop's 17 commits touches any of #951's 15 files** (the builder measured 0 at `2d864ae92`; do not inherit it).
- Repo READ-ONLY: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`. **Three seats are working in that `.git` today. Clone by SHA into your own scratch** — never `worktree add`, `fetch` or `checkout` there.

## WHAT ROUND 2 MUST ESTABLISH

1. **F1 is closed IN FLIGHT, not just at the mint line.** The builder gates the mint on `VOUCH_RECIPIENTS = new Set(['originate'])`. **Drive the real `createProxyRoutes` and show no non-originate upstream receives the vouch** — round 1 measured analytics and auth and READ the other 13 from the factory; **measure more than two this time** (as many of the 15 service keys as your harness can mount cheaply), and **show originate still receives it on every originate-bound mount** (the builder names `/originate/` and `/api/system-errors`). **Quote the recipient set you enumerated and where you read it.**
2. **F2 — the three new files bite, and bite on the right thing.** Re-run the builder's tampers yourself: C1 (originate mount removed), C2 (mint line removed), C3 (strip call removed), F1-revert (gate back to secret-only). **Cells run quoted on every row; each red on an ASSERTION, never a load or compile failure; red sets pairwise disjoint.** The builder reports its syntax control reddens with no assertion message and classifies that as a load failure, not a red-proof — **confirm your classifier agrees.** Note it used `void x;` tampers because `noUnusedLocals` turns a deleted import into a compile failure — **check that this tamper shape still removes the behaviour.**
3. **F6 — the corrected claims are now true:** `commonSecrets` reaches 20 apps and `verifierFrontend` is not one of them; declarations went 20 → 2. **Re-count from the bicep source at the head.**
4. **Regression — round 1's "TESTED — held" still holds at the new head:** env carriers exactly api-gateway + originate (verifier-frontend control); the edge strip; no deploy order opening a forgery window.
5. **NEW — MEASURE the builder's READ ONLY flag. This does NOT decide F1; it decides whether PROVISIONING the control is safe.** The gateway's own handlers forward identity to originate by `http.request`, with no vouch:
   - `routes/verification.ts:879` `router.post('/api/documents', …)` → forward at `:1020-1045` (`http.request` at `:1044`) carrying `x-user-id`, `authorization`, `x-tenant-id`, `x-tenant-slug`.
   - `routes/verification.ts:700` workflow-approve → forward at `:771-786` (`http.request` at `:785`) carrying `x-user-id`.
   - Wednesday verified at `02a22f4bb`: those lines exist and `verification.ts` contains **zero** occurrences of `vouch` (1,226 lines).
   **The open question the builder named: with a (synthetic) secret SET, originate strips those headers — does originate's `authenticate()` recover the tenant from the forwarded JWT?** Drive it in-process. **Report it as its own verdict line — `PROVISIONING SAFETY: SAFE / UNSAFE / NOT ESTABLISHED` — separate from the GO/NO GO on the PR.**

## NOT COMMISSIONED — said before running

- **The live-stack toggle** — needs containers rebuilt/restarted; the machine runs one build at a time and you have no inbox. Report NOT RE-RUN.
- **No platform suite** (Schemathesis · Akto · Playwright · k6). Unit suites in your own clone are fine.
- **Never use `127.0.0.1:6882`, kintsugi, demo or any running container as evidence** — none contains `02a22f4bb`.

## SECRETS

**Never read, print or quote any secret value.** Use a synthetic secret in-process. `docker compose config` resolves values — extract key names only. The gitignored `Blockchain/Dev/.env` on this machine holds a generated `GATEWAY_VOUCH_SECRET`; never open its value.

## KNOWN-FRAGILE / KNOWN-CHANGED

- `mergeable_state` is inverted on this repo — ignore it.
- CI reds are repo-wide on most PRs; a red check on #951 is evidence about #951 only if attributed at STEP level with a cross-branch control.
- `api-gateway` tsconfig excluded `__tests__` on an earlier gate; the builder reports `tsc --noEmit` rc 0 on both services with a planted-type-error control — **establish whether that tsc saw the new test files.**
- Originate full suite has 2 pre-existing reds (KS-444 webhooks, tracked on KS-927) — the builder's red SET is identical to baseline; **confirm the set, not the count.**

## BOUNDS

Findings only — no fix, commit, push, merge, deploy, comment or ticket. No contact with Peter or Stuart. No `--no-verify`. Never delete — quarantine, a fresh `mktemp -d` per attempt. Quote the Secuura checkout's `git status --porcelain` at start and end.

## REPORT

FOUND / TESTED / HOW with controls; every action-recommending finding carries its evidence class (**MEASURED AT RUNTIME / PROBED / READ ONLY**). NOT TESTED at the same prominence. Head readings start / mid / end with timestamps and branch. **If a claim in this brief is false, that is Wednesday's error — report it as one.** Write to your own `projects/secuura/reports/` and name the absolute path in the mail.

**Verdict:** GO · GO WITH FINDINGS · NO GO — **plus the separate `PROVISIONING SAFETY` line.**

## VERDICT DESTINATION

**Mail your verdict to `wednesday-agent@agentmail.to`**, subject
`[QA -> Wednesday] TIER 1 GATE #951 ROUND 2 (KS-1041 Step 2) 02a22f4bb — GO / GO WITH FINDINGS / NO GO`,
with a CLOSING section naming anything you want acted on. **Your pane has no scrollback and you cannot receive mail: the verdict mail is the only thing that survives your session.**

PROVENANCE:
- #951 head 02a22f4bbc46a66983c3752a5a12394ff5b1afaf, parent dd0a0c934, 2 commits, 15 files, merge-base 0f8fb33c3, develop 2d864ae92 17 ahead, round-2 delta 7 files | https://api.github.com/repos/Secuura/Distributed_Secuura/pulls/951, /commits/02a22f4bb, /compare/develop...02a22f4bb, /compare/dd0a0c934...02a22f4bb | read 2026-09-11
- verification.ts:879 router.post /api/documents, :700 workflow approve, http.request at 785 and 1044, zero vouch mentions | https://api.github.com/repos/Secuura/Distributed_Secuura/contents/Blockchain/Dev/services/api-gateway/src/routes/verification.ts?ref=02a22f4bb | read 2026-09-11
- round-2 dispositions, bite matrix, suites, READ ONLY flag, open JWT question | s174 READY FOR QA mail 2026-09-10T22:48:50Z, DKIM/SPF/DMARC pass | read 2026-09-11
- round 1 NO GO and its findings | /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-11-ks1041-951-dd0a0c934-tier1/report.md | read 2026-09-11
