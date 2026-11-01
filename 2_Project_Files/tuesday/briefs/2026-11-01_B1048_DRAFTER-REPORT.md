STARTABLE: YES (once Tuesday fills the 12 stamp slots; no blocker found; read Q-1 and Q-2 before stamping)
# B1048 drafter report: SEAT-D44, HPSM-POC review site (UAT): code-only deploy of main a3a06b9a (part B + a test)

**BLUF.** I wrote the kit `2026-11-01_B1048_SEAT-D44_hpsmpoc-uat-deploy-a3a06b9a.md` (120 lines). It pins `S` = `a3a06b9ad334b16a16fd51f7fc23e138f8e58fa2` (main head) and deploys it over `PREV` = `77c3132e`, which B1031 deployed today. `S` = #269's squash `1f4bf7bc` (part B: 14 product paths, all `web/src/`) plus #270's squash `a3a06b9a` (two test files). It ships 0 `api/` and 0 `infra/` paths. CI run `41259135668` at exactly `S` completed with success, and both deploy artifacts are live. The kit follows B1031's shape and safety steps with these changes:
- **Dropped:** the dry run (PHASE W), the database write (PART D) and the wake test.
- **Added in their place:** a read-only check that the review database is still Online, `autoPauseDelay` -1 and not paused, run before and after (D-5).
- **No what-if.** The runbook asks for one only when validating the template (`infra/README.md:3,31-35`). A code deploy is `deploy-from-ci.sh` alone (`:140-157`), and every infra and script blob is byte-equal at `PREV` and `S`.

The way back is `rollback1048uat.sh` to the kept `77c3132e` packages. Model is Opus, row C6. Ports 9740-9749. The demo is held, with no `az` and no HTTP.

## Facts (instrument; control)
- **Card** (`decision_queue.sh show hpsmpoc-uat-deploy-269-270-1101` into `scratchpad/b1048/card.txt`, exact-id filter): it is ruled `a`, "Deploy both to the review site", with `ruled_ts` 2026-11-01T14:04:33 AEDT. The live-board time 14:03:55 is as Tuesday relayed it. The BLUF says "no settings or database change and no new cost", "Part B brings new customer-facing words".
- **Main head** `a3a06b9a`: one parent `1f4bf7bc`, verification valid (`gh api -X GET commits/main`, 14:06, account kamilDatasec active under the project `GH_CONFIG_DIR`). Open PRs: 0 (control: `state=closed` lists #270, #269, #268).
- **`compare 77c3132e...a3a06b9a`:** ahead 2, behind 0 (control: the reversed compare reads behind 2).
  - 31 files, all under `web/src/`.
  - Per commit: `1f4bf7bc` has 31 paths (14 non-test). `a3a06b9a` has 2 paths: `SecurityRoadmap.test.tsx` and `testing/harness.ts`.
  - PR #269: head `7f0d832d`, squash `1f4bf7bc`, base `77c3132e`. PR #270: head `1353d337`, squash `a3a06b9a`, base `1f4bf7bc`.
- **Blobs equal at both refs** (`contents?ref=`): `main.bicep`, `sql.bicep`, `uat.bicepparam`, `deploy-from-ci.sh`, `deploy-package.py`, `infra/README.md`, `lib/customers.ts`, `ci.yml`.
- **CI at `S`:** `ci` push run `41259135668`, `head_sha` = `S`, completed/success, attempt 1.
  - 15 jobs: 14 success, plus dependency review skipped.
  - Artifacts: `deploy-web-<S>` 16,265,442 B and `deploy-api-<S>` 49,644,770 B, not expired, expire 11-08.
  - CodeQL run `41259136132` success. Open alerts on main: 0 (control: fixed returns 1).
  - Control: the same query at `77c3132e` lists run `41218555786`.
- **Way back on disk:** `.tools/b1031/repo/out/deploy-packages/77c3132e.../`.
  - web.zip `2779be3b...`, 16,162,737 B, 2042 files. api.zip `38c5c8a5...`, 49,578,971 B, 121 files.
  - Both MANIFEST commits = `77c3132e`. RUN = `41218555786`. All equal to `B1031_STATUS.md:27`.
- **Last deploy:** the deploy-STATUS listing ends at B1031, whose last line is `DEPLOYED: UAT @ 77c3132e ...`. B1040 (records) says the same and says neither #269 nor #270 is deployed (`B1040_STATUS.md:12`).
- **Gates:**
  - #269: B1022 NO GO (round 1 of 2), then B1027 `@ 7f0d832 NO GO (round 2 of 2)`, the class closed at the cap. It was landed on the product owner's ruling (records C-259, `B1033_STATUS.md:9`, "five wording items accepted as built"). The B1027-1 residue is a test pin.
  - #270: B1036 `@ 1353d33 GO WITH FINDINGS (round 1 of 2)`, head = the merged head.
- **Identity:** `.tools/b1031/identity_pass.sh` (sha256 `a3dd8d43...`) checks subscription `a6b8fe11...`, tenant `ec01829b...`, name "Azure subscription 1" and user `@datasec-rd.com`. B1031 printed exactly that (`:39`).
- **Model:** `model-routing.md` line 96 (C6 Deploy, Opus 1st) and line 145 (Sonnet: no deploy-seat rows). Model id `claude-opus-5-5` from `models_latest.json:17`.
- **Seat and B-number:** `SEAT-D44` / `HPSM-POC-D44` appear in 0 briefs (control: `SEAT-D43` appears in 7). `B1048` appears in 0 (control: `B1031` appears in 18).
- **Ports 9740-9749:** 0 listeners (control: 17 without the range). The word-boundary scan over the non-`.pre-` SEAT kits of 10-31 and 11-01 hits:
  - B971 and B1031: both closed.
  - B985: a control mention.
  - B1033, B1034 and B1036: each names the block as B1031's and not theirs (context read).
  - Scan control `942[0-9]` hits B1006 (7).
- **Panes at 14:0x:** `%0 tuesday`, `%161 MPS-M61`, `%160 NexusAI-M62`, `%159 NexusAI-M63`, `%1 fleet-monitor`. No HPSM-POC pane. `.tools/b1048` is absent.
- **Kit checks:** 12 four-underscore slots (11 + READ-WHOLE). Person names and card ids in the kit: 0 (`kam|kreiser|<card ids>` 0; control: "product owner" 9).

## D-decisions (in the kit)
- D-1: pin `S`.
- D-2: code only. No what-if, no template. B1031's `partD1031.sh`, `d2prop1031.py`, `wi1031.py`, `whatif/` and `db/` are never copied. A grep over `.tools/b1048/` for `sql db update|deployment group (create|what-if)|appsettings set|delete` must list 0 files, with a control. `azr.sh` loses its what-if verb.
- D-3: both packages, by the project script.
- D-4: no setting, vault, firewall, plan, access or database write.
- D-5: the read-only database-awake check, before and after. A pause or any changed value is a STOP, and the seat never writes to `az sql`.
- D-6: the platform-image rule, including the unchanged-image case B1031 recorded.
- D-7: the way back to the `77c3132e` packages.
- D-8: the words are not the seat's to judge. The seat writes a found yes/no table only.
- D-9: one attempt.
- D-10: no records. The keys are HPSMPOC-388 and -427.

## Q-questions for Tuesday (default applies if silent)
- **Q-1 (slot 6, the gate record).** The card's BLUF says "Both passed their checks". CI did pass. But #269's QA gates ended **NO GO at the cap** (B1022, B1027). It landed on the product owner's ruling (C-259), and the B1027-1 residue is now pinned by #270 (B1036 GO WITH FINDINGS). **Default:** stamp slot 6 with that record as written. The product owner ruled the landing and then the deploy, so this is no new decision. If Tuesday thinks the deploy card under-stated it, the alternative is to HOLD (slot 11) and re-ask.
- **Q-2 (identity: the commission and the source disagree).** The commission said "tenant d500ebad" and "service principal as in B1031". B1031 recorded tenant `ec01829b...` and subscription `a6b8fe11...` (`:39`). It used the owner's project `az` login, not a service principal: `infra/README.md:153` names the owner's login for deploys, and the SP `hpsm-poc-deploy` is Contributor on `hpsm-poc-rg` only. **Default:** the kit uses the source values: the project `AZURE_CONFIG_DIR`, ec01829b / a6b8fe11, and no SP. Tenant d500ebad appears nowhere in HPSM-POC's records that I read.
- Q-3 (slot 9): the rollback classes are B1031's, plus three new ones:
  - a new view answering 5xx for the known customer;
  - an unknown id answering 2xx with real content rather than the not-found page (a soft 404 is a STOP);
  - a non-GET `/api/v1` request attempted from a new view.

  **Default: accept.**
- Q-4 (slot 11): the words are covered on UAT by the ruling, and the demo stays held. **Default: `UAT WORDS COVERED BY THE RULING`.**
- Q-5 (slot 3): the run needs about 1.5 h with no waits. Load1 was 10.4 at 14:10. The local pair waits for load1 < 7. **Default:** a hard stop of 16:30 or later.

## UNMEASURED
- Every hosted fact: I ran no `az` and no HTTP. That covers the live build, settings, platform lines, the database state since 12:15 and the activity log.
- Whether the four views render for a known customer on the host, and at which levels the chooser serves customers.
- Which of the 14 strings show with UAT's synthetic data.
- `S`'s web file count and BUILD_ID (read at fetch).
- Whether `azr.sh`'s allow-list text matches my description of the what-if verb. B1031 says it allows `deployment group what-if`, and `grep` finds "deployment group" in it.

## Outside the fences (disclosure)
- I wrote only the two files. All other calls were read-only: `gh api -X GET`, `ls`, `shasum`, `lsof`, `tmux list-panes`, `/usr/bin/grep`, `sed`/`cat` of files, and a Python `zipfile` count.
- **The shared scratchpad:** other drafters use the same session scratchpad. My first `show` wrote `scratchpad/card.txt`, and when I printed it, it held a DIFFERENT Datasec card (`hpsmpoc-428-wake-500-fix-choice-1101`, ruled `a` at 14:04:27). Another drafter had overwritten the file. I saw its title, options and ruling before my id check refused it. I used nothing from it. After that I re-ran `show` into `card2.txt`, checked the exact id line, and copied it to `scratchpad/b1048/card.txt`.
- I read a few files inside B1031's closed tree `.tools/b1031/` (`sec404_1031.cjs`, `identity_pass.sh`, `rollback1031uat.sh`, the kit listing) to write accurate copy instructions. Nothing there was run or changed.
- I fetched `infra/README.md` at `S` raw into `scratchpad/b1048/README.md`.
