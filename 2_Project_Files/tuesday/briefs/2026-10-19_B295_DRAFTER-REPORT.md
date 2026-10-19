# B295 drafter report (2026-10-19 20:47-20:55 AEDT)

Brief: `2026-10-19_B295_SEAT-D2_composer-demo-offbox-copy-and-pin.md` (pane `Datasec/Security-Composer-D2`, model by slot, Opus, routing C6). It is B292's Phases 1b and 2 with Kam's option a authorised: B292's structure, standing lines, STOP RULE, STATUS protocol and last-line formats, plus Phase 0 (re-measure, since B292's A3 never ran) and Phase 1 (the five creates). Every sha, path and id in it was pasted from a read I made.

**Tools I used:** Read, Write (two files) and two `Edit` calls on my own brief file (a slot-count correction and adding `az vm get-instance-view` to the allowed reads). Read-only shell: `cat/sed/ls/grep/date/uptime`, git `rev-parse/show/branch/log/merge-base --is-ancestor/check-ignore`, `az` reads under the Composer `AZURE_CONFIG_DIR`, one `python3 -I` read of the decision store, and two GETs to the public Azure retail price API. **No** Azure write verb, no VM contact, no HTTP to the demo, no git write, no Artifact/Docs/mail/chat/card, no `decision_queue.sh` run (I read `decisions.json` directly).

## Verified at source (MEASURED)
- **Ruling 2:** `decisions.json` card `composer-demo-image-offbox-route-1019`: `status ruled`, `ruled_choice a`, `ruled_ts 2026-10-19T20:46:22.188584+11:00`; option a label "New storage account + one container in HPSM-DEV-RG (recommended)" and its detail (quoted verbatim in the brief). The board time 20:45:50 is from your commission (RELAYED); the store time is 32 s later. Both are quoted, not reconciled, as C-79 and C-81 did.
- **Ruling 1:** C-81 on `records/b292` (`git show records/b292:1_Project_Definition/CLARIFICATIONS.md`) and B292 `runs/D1-card-…txt`: `choice='b' ruled_ts=2026-10-19T20:19:50.283820+11:00`.
- **Refs (20:47):** `main` `b57b607114ccd6686b2cf9110c58eeb92a3f1ded`, `records/b292` `62c3403159f8d837138384a3101569ea7c6413de`, `records/b287` `a9787105c0863214de7c3377aa38a5aeba8b1de0`; remotes 0; `merge-base --is-ancestor records/b292 main` → **exit 1** (B294 not yet folded). There is no B294 STATUS and no `.tools/b294`; `.tools` holds `b290`, `b292`, `wt-b290-*`. No `B295` file in either briefs folder.
- **Azure (Composer config, 20:48):** identity `kreiser.org@me.com` / tenant `d500ebad-cf53-4f2a-a501-f831289e67fc` / sub `0c57ab37-349c-47ae-a10f-e284a380bbb9` (`Azure subscription 1`), equal to B292's. Signed-in user object id `c38fcea6-ff23-40c3-a875-e84e324910cf`, UPN `kreiser.org_me.com#EXT#@kreiserorgme.onmicrosoft.com` (external, so the brief assigns by object id). The user holds **Owner at subscription scope**, so it can create role assignments. `Microsoft.Storage` is `Registered`. `HPSM-DEV-RG` storage-account count **0**. VM `identity==null` **true**, `Standard_B2s`, australiaeast, `ubuntu-24_04-lts`/`server`.
- **az CLI 2.90.0** has `--allow-shared-key-access`, `--allow-blob-public-access`, `--min-tls-version`, `container-rm create --public-access`, and `vm identity assign --role/--scope` (the brief forbids both flags because they would make an extra assignment).
- **Prices (retail API, 20:48, USD, australiaeast):** Hot LRS Data Stored 0.02 per GB-month (first tier); Hot LRS Write Ops 0.055/10K; Hot Read Ops 0.0044/10K; LRS List and Create Container 0.055/10K; internet egress 0.0 for the first 100 GB, then 0.12/GB (MGN routing). So one 0.241 GB blob costs about **USD 0.005 a month**; the one download is within the free 100 GB (worst case about USD 0.03). The identity and role assignments have no meter in the API. The seat re-measures and STOPs before creating if the storage price is more than 10× this.
- **B287 pin plan:** `proposed/apply-and-rollback.md` read whole. No restart and no `up` are needed ("There is no `docker compose up`, `restart`, `pull`, `rm`, `prune`…"). Hashes are `263e6199…cdbe1` → `387bb7ee…04bd73`. The backup suffix in the draft is `.pre-b287-`, and the brief makes it `.pre-b295-` (the one deviation, disclosed).
- **Local:** G-DRIVE not mounted (`ls /Volumes`: Laptop-DEV, Macintosh HD, Recovery, 20:50). `.tools/` is gitignored (`.gitignore:29`). Mail key count 0 (control `COMPOSER_DEMO_URL` 1). Load 4.08.
- **Slots in the brief:** 2 lines, 5 tokens, 4 distinct (STAMP_TIME ×2, B_NUMBER_CONFIRM, ROOT_MAIN_SHA, MODEL), all in the TUESDAY STAMP section. The REFUSE grep uses the split pattern, so it does not match itself.

## Not verified (UNMEASURED, stated in the brief)
- The VM since B287's 07:29:53Z read: digest, overlay hash, disk, `/opt/hpsm/backups`, curl/openssl versions, IMDS. Phase 0 A3 re-measures all of it before anything is created.
- Whether `dscomposerdemobk1019` is available. `check-name` is a POST, so I left it to the seat.
- That `az vm identity assign` never restarts the guest. The brief compares the guest's `uptime` before and after.
- How long RBAC propagation takes. The brief allows bounded waits.
- Whether `curl -H @-` works on the VM's curl (it needs ≥ 7.55; A3 prints the version).
- Whether a demo container can reach IMDS.
- `docker save` layout and `docker load` on the arm64 Mac.

## Design choices you should know about
1. **The container is created on the management plane** (`container-rm create`). With shared-key access off, the data-plane `container create` would try a key.
2. **The token never touches argv or disk.** It goes `printf … | curl -H @-` (printf is an sh builtin). The run-command script holds no secret, and no SAS exists.
3. **The phase order is re-measure, create, copy, pin.** If the image or overlay changed, the seat stops before any resource exists.
4. **A partial stop leaves the resources as reported residue.** Nothing is ever deleted. A copy without a pin ends STOPPED, never DONE.
5. **Public network access on the account stays at its default.** Option a has no network rule, and a firewall would be a network change. Access is Entra-only (shared key off, public blob off).
6. **Removing the VM's Contributor role after the copy** goes to Kam in FOR TUESDAY. The seat does not do it.

## R-D2 questions (recommended default first)
- **R-D2-1 Launch gate:** stamp only after B294's fold has landed (`records/b292` in `main`)? **Recommend YES.** The brief REFUSES otherwise. Without the fold, a branch cut from `main` lacks C-79..C-81 and #319, and its next C-number would collide (C-79). The alternative is to cut `records/b295` from `records/b292` and launch now. That works too, but it adds a third unfolded records branch for the next fold.
- **R-D2-2 G-DRIVE:** also place a copy on G-DRIVE when it is mounted? **Recommend OWED, recorded, not blocking.** Card b's detail named G-DRIVE. Option a's route already puts two copies off the VM (the blob and this Mac's `.tools/b295/offbox-copy/`). G-DRIVE is not mounted now. If it is mounted at launch, the brief has the seat `cp -p` and hash it.
- **R-D2-3 Tags** `project=datasec-security-composer`, `purpose=demo-image-offbox-copy`, `created-by=B295` on the account at create? **Recommend YES.** They are part of the one create, not a new resource, and they make ownership visible in the portal.
- **R-D2-4 Names:** account `dscomposerdemobk1019` (the seat may append one letter, up to 3 tries, if taken), container `composer-demo-backups`, prefix `2026-10-19_demo-minio-image/`? **Recommend YES.**
- **R-D2-5 No curl (or curl < 7.55) on the VM is a STOP, with no python fallback?** **Recommend YES.** It keeps the token handling to one reviewed path. Ubuntu 24.04 normally ships curl 8.x (UNMEASURED).
- **R-D2-6 Bounded RBAC waits** (10 × 60 s on the VM's HEAD preflight and on the Mac download) before a 403 counts as a STOP? **Recommend YES.** Fresh role assignments commonly take minutes, and without a wait a correct setup would STOP spuriously.
- **R-D2-7 Live seats at stamp:** confirm B290 (G9) is finished or fenced, and that B294 (W7) has ended `RECORDS DONE`. **Tuesday confirms.**

## Things that did not match the commission
- The commission says "C-82 (or next number re-derived)". C-82 is right only after B294 folds. On today's `main` the next number would be C-79, hence R-D2-1.
- The commission names "a BACKLOG #319 dated line". After B294, #319 also carries B294's cross-reference line, and the same risk lives in renumbered row 325. The brief appends to #319 only and names 325 in FOR TUESDAY.
- I used `Edit` twice on my own brief file, beyond "Write tool only". These were corrections to the file I had just written. No other file was touched.
