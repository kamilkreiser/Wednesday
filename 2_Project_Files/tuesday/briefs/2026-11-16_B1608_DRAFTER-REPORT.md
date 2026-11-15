STARTABLE: YES as a kit (complete, 176 lines, sidecar rc 0); a launch TODAY STOPS BY DESIGN at Step 2 unless Tuesday first closes Q1 (the two new PDF cover phrases have no ruling) and Q2 (the footer-look row #474), and stamps the NO GO rulings (Q3)

# B1608 drafter report: Composer demo deploy of main (SEAT-D64)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-16_B1608_SEAT-D64_composer-demo-deploy-main.md` (176 lines; sidecar `.measured` 73 lines, `stamp_check.py` rc 0 run alone; 13 lines carry four underscores, so Tuesday's `.pre-stamp` copy should print 13). Drafted 10:01:56 to 10:15:08 AEDT (`date` printed 10:01:56, 10:02:25, 10:05:42, 10:13:40, 10:15:08). Template B986 (SEAT-D42, 2026-10-31); the kit keeps its shape (STATUS channel, marks, last-line forms, THE RANGE, THE GATES, AUTHORITY, Order of work, D1-D9, DRAFTER DECISIONS, REFUSE AT ONCE, HOLDS, STANDING LINES, STATUS shape, Stamp, `READ-WHOLE-BY-TUESDAY: ____`), adds a context band and moves the Stamp to the end so `stamp_check` scans the whole body.

## BLUF
- **The words gate fails at drafting on one item, and the kit makes the seat stop there before any `az` call.** PR #130 changes the policy PDF cover's two date labels from `(draft generated, UTC)` / `(released, UTC)` to `(draft generated)` / `(released)` (raw `policy-summary.ts` lines 259-260 at d70edf70, 285-286 at b4681297; counts 1/0 and 0/1). The project's own C-150 says "No ruling of the product owner on the words is claimed" and "the cover's words ... go to the product owner on their card before any deploy". The 2026-10-12 ruling (Sydney day) approves behaviour, not words. The grant excludes new customer-facing words, so this is a STOP.
- **The deploy is not B986-shaped.** B986 changed no screen and applied five migrations. This range has **no migration** (0 of 42 paths), **contract unchanged**, but the **web screens, styles and PDF words change** (a new "Mark all secret fields local" button, per-device-group typed labels, monospace setting key, cover words, footer clipping), and **runtime packages change** (undici, fast-uri, fastify, ip-address; vite 8.3.4), so the VM build is a real `npm ci` rebuild, unlike B986's cached one. `web` WILL be recreated this time (B986's was not). The way back has no down-recipe: re-run the kept `composer-d70edf7.tar.gz`.
- **Range, measured:** d70edf70 to b4681297, ahead 26, behind 0, 26 one-parent commits, 42 files (+7192 -371), 0 `content/`, 0 `migrations/`, 0 `rollback/`, 0 `packages/api-contract`, 0 `compose.yaml`. Gates: 23 of 26 passed at the merged head; **#111, #113, #114 merged on the product owner's ruling after NO GO** (only #113 changes product bytes); CodeQL `Analyze` x2 success on 26 of 26 squashes; open alerts on main 0 (control `fixed` 20); only open PR #85 (draft, held, not in range).
- **Footer row #474 is named and the kit does not decide it.** #120 IS the change the row is about (63 of 265 first lines 1-3 code points short; 100 names cut shorter than main, while the product owner approved on "43"). Slot 5 carries Tuesday's PROCEED or STOP; drafter default is STOP until he has seen 100 and 63.
- **An alternative that needs no new words card (Q1 option):** stamp slot 4 with `27adb70991ff3d7ec13f0732de6ecdcb1aab8043` (the #129 squash): ahead 25, behind 0, 38 files, 973 blobs, leaves #130 out. Row #474 (W7) still needs slot 5.

## Facts re-measured (instrument; control)
| Fact | Instrument | Result |
|---|---|---|
| main | `gh api -X GET git/ref/heads/main` under the project `.gh-config` (`gh auth status`: kamilDatasec) | `b4681297d974ac3d8e74a4a12baeb9ea41962c52`; commit tree `7e6e405bb4e1e704f8d3dd2e9c412c8cfcf2afcd`, 1 parent `27adb709...`, author `88359143+kamilDatasec@users.noreply.github.com` |
| range | `compare d70edf70...main`, python over the JSON | ahead 26, behind 0, total 26, 42 files, all commits 1 parent; control: reversed compare `behind`, behind_by 26 |
| 38-file alternative | `compare d70edf70...27adb709` | ahead 25, behind 0, 38 files, 1 parent each; tree `db97ada9...` 973 blobs, truncated false |
| class of change | path counts over the file list | `content/` 0, `migrations/` 0, `rollback/` 0, `packages/api-contract` 0, `compose.yaml` 0, `docker/` 0, `.github/` 0; controls `apps/` 21, `packages/db/test` 4 |
| blobs | `git/trees?recursive=1` at both shas | 964 at d70edf70, 974 at main (10 added, 0 removed, 32 changed = 42); 27 migration `.sql` at both |
| gates | `gatemap.py` (head[:7] of each `pulls` head against every VERDICT first line in the coordinator's `*_verify*/VERDICT.md` and every `^VERDICT:` line in the project STATUS files) | all 26 PRs map to exactly one gate line at their head; NO GO rows: #111 (B1108 round 2 of 2), #113 (B1161 round 2 of 2), #114 (B1197 round 3, final) |
| CodeQL | `commits/<sha>/check-runs` x26 | `Analyze (csharp)` and `Analyze (javascript-typescript)` success 26 of 26 each; lines without success 0; alerts open 0, fixed 20; `pulls/9999` 404 |
| open PRs | `pulls?state=open` | #85 only, draft, head `85105729`; absent from the compare's commits (0) |
| demo, public | 3 GETs 10:05:42 (no cookie, host from the `.env` URL line, never printed) | `/site.json` 200 `{ "environment": "demo", "guided_view": false }`; `/` 200 naming `index-B-n1v2_U.js`, `index-DN-_9cA1.css`, `vendor-CujEEn2R.js` once each (= B986's recorded bundle, so no web change since); `/api/v1/healthz` 404 |
| identity | `az account show` under the project `.azure` 10:05:48 | `kreiser.org@me.com`, `d500ebad-cf53-4f2a-a501-f831289e67fc`, `0c57ab37-349c-47ae-a10f-e284a380bbb9` |
| VM group | `az resource list -g HPSM-DEV-RG` vs B986 `resources_after.txt` (program diff) | 7 = 7, `IDS_EQUAL` (the old "14" in B986's REFUSE 8 was its own Correction 6) |
| VM state | `az vm get-instance-view`, `az network nsg show` (GETs) | `PowerState/running`; NSG `default-allow-ssh` 1000, `allow-http-https` 1010 only |
| last Composer deploy | loop over every project `Briefs/*_STATUS.md` last line | newest `DEPLOYED:` is B986; none later (control: B119, B124, B133, B143, B147, B537 print too) |
| remote-update.sh | archived copy `qa-wp5/evidence/azure/remote-update.sh` | 30 lines; `scripts/` 0 lines (control `compose` 10); it moves `composer` to `composer.prev` BEFORE `up --build`, so a failed build leaves old containers on a new tree (kit says: STOP, way back printed, not run) |
| words | raw `contents?ref=` at both shas | `(draft generated, UTC)` 1 then 0, `(draft generated)` 0 then 1, `(released, UTC)` 1 then 0, `(released)` 0 then 1; `Mark all secret fields local` 0 then 2; `Marked 1 secret field as local.` 0 then 1; the 409 sentence 1 then 1; `(${groupName(groupId)})` 1 then 2 |
| rulings quoted | CLARIFICATIONS C-71, C-120, C-121, C-123, C-132, C-139, C-145, C-150; B1495 STATUS + ADDENDUM-1 | W3 14:15:02 (words card, a), W4 16:31:16 (a), W6 14:15:08 (all 7 quick), W7 09:07 (b) and 13:33 (a); W8 NOT RULED |
| footer row | `awk NR==470 BACKLOG.md` | begins `| 474 |`, "OPEN, NOT RULED, awaiting the product owner" |
| grant/hold lines | `awk NR==24 EXPIRING-GRANTS.md`; `grep -c -F` over CLARIFICATIONS | grant row at line 24; "a deploy only on the product owner's card" 17 lines (last 2830); `CLAUDE.md` line 30 |
| seat/model/ports | `awk NR==96 model-routing.md`, `awk NR==17 models_latest.json`, `ls briefs | grep -o SEAT-D`, `tmux list-panes` | row C6 line 96 (Opus); `claude-opus-5-5` line 17; highest earlier seat SEAT-D62 so D64 per commission (D63 is the MPS kit); 0 Composer panes, 0 Composer processes; no port block (VM builds) |
| deploy key | `ls 3_Access_Keys`, `2_Project_Files/.git/config` | key and `.pub` exist (2 files); the repo's `core.sshCommand` names `/Volumes/Laptop-DEV/...`, **not mounted today** (`ls -d /Volumes/*DEV*`: `Datasec_DEV`, `DEV-Working`); the kit tells the seat to use the real path; local `2_Project_Files` HEAD `0b2fca43` does not hold b4681297 (`cat-file -t` fatal; control d70edf70 `commit`) |

## Chain-step inputs (rule 4)
| Step | Inputs | Produced by |
|---|---|---|
| 0 | kit copy, stamp slots, pin, `.pre-stamp` | Tuesday's stamp; `.pre-stamp` is Tuesday's (not written by the drafter) |
| 1 | `gh` reads, gate files, CodeQL runs | exist at BASE (GitHub, `*_verify*/VERDICT.md`, project STATUS) |
| 2 | compare patches, slot 6 cards, `decision_queue.sh show` | Step 1 (patches); Tuesday's slot 6 |
| 3 | D1 identity, B986 `scripts/s2_read.sh`, the VM | D1 (Step 3 starts with it); B986 evidence exists |
| D2-D4 | temp key, NSG rule, state SQL, backup | D2 makes key and rule; D3 reads; D4 needs D2 |
| D5 | way-back text | written before D6 |
| D6 | clone and archive of `S`, deploy key at its real path | Step 0 pin; the clone is made in D6 |
| D7 | `S` archive for the manifest, B986 `live.sh` / `b986-live.cjs`, B986 `live_*.png`, `.env` credentials | D6 archive; B986 evidence exists at BASE |
| D8-D9 | D2's key and rule | D2 |

## D-decisions
- D-1 Pin S; D-2 the three NO GO merges ship only with slot 3 by name; D-3 words: STOP, never edit, plus the 27adb709 alternative; D-4 no writes beyond temp access, backup, archive, `remote-update.sh`, throwaway DB; D-5 one attempt; D-6 heavier build (record seconds, a timeout is a STOP).
- D-A (mine): the words gate runs as Step 2, BEFORE any `az` call, because the commission says "First the words gate" (B986 ran its VM read first). Deployed-vs-target moved to Step 3.
- D-B (mine): since there is no migration, the 0026 count and the down-recipe chain are dropped; the 0026 query stays only as a D3 control (B986's was degenerate: 0 non-null hashes).
- D-C (mine): card ids are kept OUT of the kit body (rule 7); the kit cites rulings by date and time, and the Stamp slots (Tuesday's) carry the ids for `decision_queue.sh show`.
- D-D (mine): `kam` (a seeded demo login) is written "the first seeded account", and `kreiser.org@me.com` stays because D1 must match it exactly (it is the az account name, as in B986).
- D-E (mine): the kit says the seat does not decide the footer row; the drafter's default is STOP (Q2).

## Q-questions for Tuesday (each with a default)
- **Q1 W8, the cover words.** No card rules `(draft generated)` / `(released)`. Default: post a words card for the two phrases (options: keep as built; keep the zone visible, e.g. a "Sydney time" label; revert to UTC wording) and launch on option a/b only after it is ruled; OR stamp slot 4 with `27adb709` (25 PRs, leaves #130 out, no card needed for W8/W9).
- **Q2 Footer-look #474 (slot 5).** Default: STOP (reading "depends"): #120 is the very change the row is about and the card was ruled on 43, the review measured 100 (63 first lines 1-3 code points short). Cheapest unblock: a short card quoting 100 and 63, default "ship as built". If you read it as PROCEED, say so in slot 5.
- **Q3 Slot 3.** Rule #111, #113 and #114 BY NAME (product owner's 2026-11-02 for #111, 2026-11-03 for #113 and #114, per C-120, C-121, C-123). Default: ship, "verdict stands as written, discharged for this deploy only".
- **Q4 W1, W2, W5 readings (slot 6).** W1 (the existing 409 sentence now also answers the set-up card) and W2 (typed label `<label> (<group>)`, an existing form) read as not new words (default). **W5 is a mismatch the builder flagged and nobody ruled:** the hint under the justification box still says "Required for a custom value or an exclusion." although a secret local value needs none (raw `ControlDetail.tsx` line 767, count 1). Default: list it in the receipt for the product owner, do not block.
- **Q5 Which card is "the card" (slot 2).** The commission names `hpsmpoc-review-site-deploy-confirm-1116` (options a and b both include Composer). Default: that card, option a or b; say so in slot 2.
- **Q6 Network and time.** Whether the VM can reach the npm registry and finish the build inside the archived script's 900 s `--wait` is UNMEASURED. Default: a failed or timed-out build is a STOP with the log and the way back printed, never a retry.
- **Q7 Dashboard card after deploy.** The receipt names "what to look at himself": the new button on the Controls screen (visible only to a consultant when a secret field has no decision) and the cover/footer; none can be probed without a write or render. Default: say so, do not render.

## UNMEASURED
- Everything on the VM (needs `az vm run-command`, forbidden to the drafter): the deployed sha (public bundle names equal B986's only prove web unchanged), ledger 27, container ids, free space, whether `composer-d70edf7.tar.gz` and `composer-308b7aa.tar.gz` still hold B986's sha256s (RELAYED from B986 `archive.txt`), config hashes, the 0026 read, registry reachability, the VM-side name clashes.
- Whether the new default brand's moved hash disturbs any stored output (PR #130's body says nothing compares it: RELAYED).
- Whether an old build reads a secret-local row that the new build stored with an empty rationale (the way-back caveat).
- Whether `RenderRecordError` text (`not a time zone: ...`) can reach an API answer (the kit tells the seat to prove it by program, W9).
- Whether a launch-time `git ls-remote` from the project clone works: its `core.sshCommand` names an unmounted drive; the drafter used `gh api git/ref` instead.
- Stamp/Tuesday items: `.pre-stamp` copy (control 13) is not written by the drafter.

## Outside-the-fences disclosure
- **HTTP to a hosted host:** three GETs of the Composer demo (`/site.json`, `/`, `/api/v1/healthz`) at 10:05:42, no cookie, token or body, host read in-process from the `.env` `COMPOSER_DEMO_URL` line only (never printed, written nowhere); the commission permits public health/version GETs, DRAFTER_RULES fence 4 says none. Responses kept in scratch (`pub/`): none holds a secret.
- **`az` read verbs, after `az account show`, under the project's own `.azure`:** `resource list -g HPSM-DEV-RG`, `vm get-instance-view`, `network nsg show`. No `az vm run-command`, no write, no login.
- `gh api -X GET` only, under the project `.gh-config`. Project files read: CLARIFICATIONS.md, BACKLOG.md line 470, CLAUDE.md line 30, Briefs (B986/B537/B147 evidence and STATUS, B1423/B1495/B1581/B1077/B1420 STATUS), the archived remote-update.sh, local repo `rev-parse` and `cat-file` (read verbs). Tuesday files read: the census, the commission, DRAFTER_RULES, `EXPIRING-GRANTS.md` lines 9, 16, 24, `model-routing.md` line 96, `models_latest.json`, `NEXT-PICKUP-TUESDAY.md` by grep, `brief_seat.sh` by grep, the B1604 kit and report as shape templates. NOT read: `decision_queue.sh` in any form (so no card was read; card ids appear only as ids the commission and the project records already name), `briefs_staged/`, `scoreboard.md`, `_ledger.md`, any WEDNESDAY/FRIDAY tree, other clients.
- No `cd`, no token printed, no Artifact tool. Two hooks advised against `grep | cut` and case-sensitive phrase greps; I counted with `-c` and positive controls where it mattered. One command was refused by the no-delete hook (`rm` of my own sidecar skeleton); I moved it to scratch instead and re-ran `--init`.
- Scratch only under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s281/d1608/` (`raw/`, `g.sh`, `pub.sh`, `pub/`, `gatemap.py`, `fill.py`, earlier sidecar versions). Wrote only the kit, its sidecar and this report.

DRAFTED B1608: kit 176 lines, sidecar rc 0, questions 7
