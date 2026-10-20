# B342 drafter report (Sonnet drafter, 2026-10-20 ~20:10-20:35 AEDT)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-20_B342_SEAT-D6_composer-demo-deploy-eaff2b7.md` (~38 KB; over the ~25 KB aim because it carries B147's runbook delta, the 10 verbatim words and the 0022 way back). Two slots only, both on one line: `@SLOT:STAMP_TIME@`, `@SLOT:MAIN_SHA@` (pre-stamp slot-line count 1, MEASURED with the brief's own Step 0 grep). Seat SEAT-D6, pane `Datasec/Security-Composer-D6`, Opus. Launch line uses `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh` (the path exists; `tools/cockpit.sh` does not).

## BLUF for Tuesday
**Do not expect this deploy to go today. The brief is built to STOP at Step 3, before any VM write, and the drafter's reads say Step 3 fails:**
1. **PR #83's 10 new words have no Kam approval.** B322 listed them ("NEW WORDS (listed, not shipped; per K9 nothing reaches a customer before Kam's word card)", `B322_STATUS.md:177`), B331 verified the list (10 of 10), B335 r8 "I approve no word" (`:365`). `decisions.json` has no Composer card for them. They reach the demo through the API (two 422 details, contract descriptions in the served `/api/openapi.json`).
2. **Card `composer-l05-setup-card-too-1014` is still `open`** (`decisions.json`, read 20:2x). #79 (`230f9fab`) carries L05, which also changes the Expert set-up card. The card says that screen "comes to you before any demo deploy" and its default is "nothing goes to the demo (it stays on ef916ce2) until you tap". #79 cannot be left out: the delta is a straight line of 6 commits.
3. **K1-K10 ruling (`composer-sro-vic-gap-10-decisions-1020` = a)** says "Lanes start in waves; nothing is deployed without your card." #83 is lane L3-a. The grant (2026-10-16) does not mention it; I treated the sentence as binding in the brief (Step 3 last bullet) and flag it below.

Everything else in READY is green or expected green (CodeQL, B335 GO, no content release, no dependency change, one migration).

## Sources read (whole unless noted)
- Grant: `0_Brain/learnings/2026-10-16_tuesday-inherits-push-to-demo-hpsmpoc-unfrozen-account-controls-datasec.md` and `.../2026-10-06_push-to-demo-when-ready-no-card.md` (both whole; quoted in the brief with READY and NOT COVERED).
- Template: `Briefs/2026-10-13_B147_SEAT-F_demo-deploy-ef916ce.md` (whole; Friday-era, last Composer demo code deploy), its STATUS (BLUF, lines 100-150, 349) and evidence listing; B299 brief (whole, Tuesday-era form for fences, refuse-at-once, last-line format); B341 brief (lines 1-14, slot-check convention). B295 STATUS (selected lines), B299 STATUS last line.
- `DEPLOY.md` @eaff2b74 via `gh api contents` (358 lines, sha256 `29baaf30…5792`, saved in the scratchpad): lines 1-58 (backup procedure), 60-111 (Route A/B pattern), 153-222 (0021 section, for the Route B function-drop pattern), 241-296 (0022 section, quoted/paraphrased).
- B322, B331, B335 STATUS (selected sections: NEW WORDS table, r8, verdict lines). `decisions.json` (all Composer cards since 10-12 listed; two cards read whole). `NEXT-PICKUP-TUESDAY.md` grep for demo state and the L05 card.

## Measurements (instrument, time)
- `gh api` GETs under the project's `.gh-config` (account `kamilDatasec`), 2026-10-20T09:15-09:30Z (20:15-20:30 AEDT):
  - `git/ref/heads/main` and `commits/main` at 09:18:31Z: `eaff2b7442d8cc28e536d41a46cec701266024b1`, tree `610ec59bf07acc5c8caaa718254a6f704ba1fd97`, parent `318df1767035e92a55f633824927ce01b9986293`, committed 09:13:29Z. PR #83 merged 09:13:30Z, head `8e062d94549ee027c5ed66924bce45f33904e9e0` (2646 add, 41 del, 19 files). #81 merge `d8d2a2c7…`, #82 merge `318df176…`. One open PR: #84.
  - **CodeQL on `eaff2b74`:** at 09:15:27Z the JS/TS analysis was `in_progress` (csharp success 09:15:14Z); at 09:18:31Z both `completed success` (JS 09:17:20Z); analyses on main for `eaff2b74`: JS 09:17:05Z results 0, csharp 09:15:03Z results 0; open alerts on `refs/heads/main` = 0. So **READY item "CodeQL 0 new alerts" is satisfied as of 09:18:31Z**; the brief makes the seat re-read it.
  - `compare/ef916ce2...eaff2b74`: `ahead`, ahead_by 6, behind 0, 6 commits (#78, #79, #80, #81, #82, #83), 77 files, 36 non-test paths (listed in the brief).
  - Migration `0022_exception_review_and_scope.sql` at `eaff2b74` via contents API raw: sha256 **`8195ecb7307b54001260d396a5f38b2b9f3331fa6dfe4d5e4a1ded0d4b539717`** = the pin. Down-recipe sha256 `c4d94cbeaf0fa97e57119a97908a785daef08c46eb9902e2c3c63dc731fa5d0f`. `CONTRACT_VERSION = "0.34.0"` at `document.ts:98`. Tree: 934 blobs, 22 migration files. `openapi.json` `info.version` 0.34.0; `listExceptions` = `GET /policy-versions/{policyVersionId}/exceptions`.
  - Delta paths by class: `content/` 0 non-test paths; `package.json`/lock 0; `docker/`, `.github/` 0; renderers 0; web screens and styles many (the bundle WILL change; B147's "bundle unchanged" control is dropped, replaced by markers).
- Local reads: B335 last line `VERDICT: B335 pr83 ... @ 8e062d9 on main 318df17: GO`; B297 GO WITH FINDINGS; B320 GO WITH FINDINGS; B281 NO GO (one pre-existing finding, Tuesday ruled and merged #80); last-line scan of every `*_STATUS.md` in the project's `Briefs/`: the newest `DEPLOYED:` is B147 `ef916ce28989fa4bd3db0bfdf61d314598f279b9`. `uptime` 20:18: load 2.85/4.49/4.82; `pc-b341*` containers: 0 running at that moment (so B341 had not started its stack yet).

## The deployed sha and how it was read
**Not measured by me.** The demo's version endpoint (`/api/healthz`, `/api/openapi.json`) is behind Basic auth (B147 `live_checks`), and reports a contract version, not a sha. The project's own records name no unauthenticated version endpoint, so per the fences I sent nothing to the demo. **Deployed sha = `ef916ce2` by record only** (B147 last line + Tuesday's NEXT-PICKUP "Demo stays on ef916ce2" + no later `DEPLOYED:` line). The brief makes the seat measure it read-only (one `az vm run-command` read: manifest of `/opt/hpsm/composer` against the archive, ledger, overlay hash; no SSH, no NSG) before the words check, and STOP if it is not `ef916ce2` with ledger 21. Caveat: Tuesday's pickup says L05 card holds a deploy of `230f9fab`, so nothing between B147 and today should have reached the demo.

## New-words finding (the stop)
| Reaching demo | Approval | State |
|---|---|---|
| #78 B149 words (16 wordings) and looks (11) | `composer-words-comp19-b149-1013` = a (2026-10-14T06:58:19), `composer-look-comp18-b149-1013` = a (06:58:17) | ruled |
| #79 B152 "12 words, L05, L06" | same cards by the commit message (not matched item by item: B152 STATUS lists W07 etc.; the seat must match) | words ruled; **L05 on the set-up card: card open** |
| #80, #81, #82 | none needed | confirm by program |
| **#83 B322: 10 items** | **none** | **unapproved**; verbatim in the brief |
The drafter did NOT build the by-program table of all added strings across #78-#79 (that is the seat's Step 3), so a #78/#79 string outside the ruled lists is possible and UNMEASURED.

## Deliberate choices
- **STOP order:** READY, then measure deployed sha (read-only), then words/looks, all before temp access opens. If Step 3 fails there is nothing to clean up.
- **Backup:** `pg_dump -Fc` + `pg_restore -l` count + sha256 (B147/DEPLOY.md), plus a required throwaway-database restore test (`b342_restoretest`, dropped by name, proved absent) when disk allows, else schema-only restore. This is stronger than B147 and touches only a new DB name in the demo's Postgres. Say if you want it dropped to readability only.
- **No off-box copy:** B299 removed the VM's write role on the backup container; the brief forbids re-granting. The dump stays on the VM only.
- **Rollback:** Route A (DEPLOY.md 0022 section) written as text, not run; previous build = measured deployed build (`ef916ce2`, `composer.prev`). Route B marked UNMEASURED for 0022 per DEPLOY.md.
- **#80 compose change:** `${PC_OBJECTS_IMAGE:-<old pin>}`; demo overlay is pinned since B295 (`387bb7ee…`). The seat renders `docker compose config` before the swap and proves the objects container is not recreated.
- No heavy local work (B341 is docker-heavy): no npm build, no docker, no ci.sh; one light headless browser run gated on load.

## Open questions with recommended answers
1. **Does the K1-K10 sentence "nothing is deployed without your card" override the standing grant for #83?** Recommend: yes, treat it as binding for L3-a (it is later than the grant and Kam's own ruled wording), and file ONE Kam card now: *"Composer: approve the 10 new exception wordings (API messages, none on a screen) and the L05 look on the Expert set-up card, then Tuesday deploys 0022 to the demo under the grant."* Launch B342 only after it is ruled; set `composer-l05-setup-card-too-1014` aside by folding it into that card (do not re-card it, per the pickup note; reference its id).
2. **Stamp now or wait?** Recommend wait: if stamped today the seat runs Steps 0-3 and STOPs with the listed words (a useful, cheap, read-only artefact), but it will occupy an Opus seat. Alternative: stamp only after the card is ruled.
3. **Throwaway-database restore test OK?** Recommend yes (see above); it is a write to the demo DB cluster (a new database), small and reversible. If you read it as a data change beyond the deploy, remove the (a) branch.
4. **Gate files B150/B153** (#78/#79) are not in the project's `Briefs/`; the brief tells the seat to find them or record UNMEASURED. Recommend Tuesday names their path at stamp if known.
5. **Deployed sha of the demo** is by record, not by measurement (above). Recommend leaving it to the seat's Step 2.

## Fence notes
Wrote only the two files named, with Write; after creating the brief I made three small corrections with Edit on the same brief file (cockpit.sh path, slot-line count, one wording). No Artifact/Docs/mail/chat tool, no az call, no HTTP to the demo, git read verbs and `gh api` GET only, one scratchpad copy each of DEPLOY.md and openapi.json at `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/ceec922c-2944-48a5-bc00-14ba876a7b55/scratchpad/`. No secret printed. The hook-blocked `cd` and a `=====` echo were rejected and re-issued without them.
