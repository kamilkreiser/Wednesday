STARTABLE: YES, after the Stamp and ONLY after the deploy-round card reads `a` or `b` (it read `status:  open`, `choice=None` at 10:02 and again at 10:10, so the kit REFUSES at its own Step 0.3 today). The kit is unstamped: `/usr/bin/grep -c '_''___'` over it prints 12 (S0 to S10 and the last line; control on a scratch file: 1); `stamp_check.py <kit>` rc 0, 127 claims, 127 measured.

# B1607 DRAFTER REPORT (kit `2026-11-16_B1607_SEAT-D63_mps-showcase-deploy-main.md`, sidecar `.md.measured`)
Drafted Mon 16 Nov 2026 10:02 to about 10:13 AEDT (clocks from `date` in the same calls: 10:02:44, 10:04:07, 10:06:59, 10:09:53, 10:11:18, 10:12:01). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s281/d1607/` (raw script and PR bodies at the pinned sha, the card show outputs, the extracted packages, `mk_sidecar1607.py`). Shape copied from the B1542 kit (template) and its STATUS Deviations; the census section 2 and 6 read whole. Kit 103 lines (`wc -l`); one non-ASCII character (the em dash inside the product owner's verbatim "c — All Datasec projects' demos too").

## BLUF
- One Opus deploy kit, route and checks of B1542, **re-pinned `0bb3ed12` -> `5e800095` (8 squashes, 44 files, MPS #192 to #199)**. Model row C6 (`model-routing.md:96`), `claude-opus-5-5` (`models_latest.json:17`), launch line carries `BRIEF_SEAT_LEVEL=opus` inside the quotes, pane `Datasec/MPS-D63`, no port.
- **What the seat does that B1542 did not:** the deploy SCRIPT it runs changed (#192, #194): it now counts care-pack and staging rows by streaming every hosted quote and snapshot file from Kudu (counts only, a token per read) and refuses an older package; the kit names the real script lines, the approved stop words (C-152) and a by-program comparison of the script's printed lines against the approved word pack.
- **Rollback caveat after #196 (the one the commission asked for):** a snapshot written by the new build carries `fleetLineId` and an older build refuses it (RELAYED from the #196 body; the drafter measured that `0bb3ed12` sets `UnmappedMemberHandling.Disallow` at `ApiJson.cs:23`, not that its snapshot reader uses it). The kit makes a rollback to `0bb3ed12` (package kept locally, sha256 `a30e864c...db39c`, 3,246,161 B, proven by the drafter) legal only if the store is unchanged AND no snapshot holds `fleetLineId`; otherwise fix forward.
- **The seed secret (card `mpscalc-deploy-seed-secret-expired-1112`) is the likely stopper, Q1.** It was ruled `a` (deploy that night, skip three Seller checks) and says "a later read once the secret is renewed closes them"; it does not say later deploys may skip them. The project `.env` was last written 2026-10-16 (before the 11-12 expiry) and the backlog row `[B1544-OWED-4]` still lists the renewal as open, so the kit expects the secret STILL expired and, unless Stamp S4 extends the ruling, stops at the safe boundary before the swap.
- **MPSCALC-224 host read:** the package now carries `System.Security.Cryptography.Xml.dll` (215,848 B, version string `10.0.1526.53008`; the package holds 51 files, up from 50). The kit records the host patch line, the on-site file equal to the package, and writes the loaded-file-version as UNMEASURED (Q3). Finding: the last deploy already printed `DOTNETCORE-10.0.15` for the host (RELAYED, 3 hits in its STATUS), so the "host runs a patch below the fixed one" premise of MPSCALC-224 looks stale.
- **Hazard found and handled:** the root repo's `core.sshCommand` still points at `/Volumes/Laptop-DEV/...` (does not exist), so `git ls-remote` answered `Permission denied (publickey)` for the drafter and the repo does not hold `5e800095`; the kit gives the one allowed fetch with the key path on the command line only (key exists at `3_Access_Keys/github_deploy_rw`), and reads main with `gh api`.

## Facts re-measured with instruments (each is also in the sidecar or the kit)
| fact | instrument, time | result |
|---|---|---|
| main head | `gh api -X GET .../branches/main`, 10:02:44 | `5e80009525138879031c4b07a18436242dadf46c`; tree `d9e2dc5c50a8f9e41683d709ca20458d8fcc2efa`, one parent `d464c07e` |
| delta | `compare 0bb3ed12...5e800095 --paginate`, 10:02 | ahead 8, behind 0, 44 files (scripts 10, tests 7, web 18, src 6, docs 2, .github 1, infra 0); control: 8 merged PRs |
| CI | `commits/<sha>/check-runs`; `actions/runs?head_sha=`; `actions/artifacts?name=deploy-mpscalc-<sha>`; alerts; open PRs | 8 of 8 success; `ci` run 43724577328 attempt 1 success; Push on main 43724577088 success; artifact id 14166830533, 3,331,280 B, expired false, expires 2026-11-22T14:44:30Z; alerts 0; open PRs 0 |
| package | artifact zip downloaded read-only into scratch, `shasum`, MANIFEST | `mpscalc.zip` sha256 `09b0ffc7...6233`, 3,330,077 B, 51 files, commit = sha, run = 43724577328/attempts/1, scan hits 0 |
| file list vs rollback zip | `find`, `comm`, `cmp` over both extracted | only-new: Xml DLL, `EntraRoot-Coyrullp.js`, `index-CVEPJqD-.js`; only-old: the two Dv1fC5uO / Da9pY_Zr assets; changed: `MpsCalc.Api.deps.json`, Api/Engine/Import DLLs, `wwwroot/index.html`; byte-equal: CSS, both Pkcs DLLs, app host, `runtimeconfig.json` |
| Xml / Pkcs entries | `grep -o -F ... | wc -l` over deps.json | Xml 10.0.15: new 2, old 0; Pkcs 10.0.15: new 2, old 2 |
| "Software / month" | `grep -o -F` over the bundles | old 3, new 2; the four rental-proposal card fragments 1 each in both |
| live site | public `GET /` at 10:04:07 (one request) | 200; names `index-Da9pY_Zr.js` x1, `index-BbrcPc3D.js` x0 (= the last deploy's bundle) |
| identity | `az account show` under the project `.azure`, 10:04 | tenant `ec01829b-fdcb-4503-9834-eb2ffbd99169`, sub `a6b8fe11-d1b5-4293-8727-b34aba08a705` (environment mapping stays UNRESOLVED; the kit asserts none) |
| rollback zip | `shasum`, `stat`, `.RUN`, `git -C ... rev-parse HEAD` | `a30e864c...db39c`, 3,246,161 B, `.RUN` 43153226915, HEAD `0bb3ed12...`; `git -C` works on this worktree |
| deploy script | raw file at the sha, `grep -n` | 328 lines; usage line 33; `pre1_hosted` 146, `reread_overlay` 172, `kudu_get` 197, `rollforward_hosted` 205; stop line 231; floor `0217044e804afd4a457cbfd4ba4721f4f51071d1` at `deploy-package.py:662`; floor is an ancestor of `0bb3ed12` (local rc 0) and GitHub compare floor...main is ahead 121 |
| shallow? | `git rev-parse --is-shallow-repository` at the root repo | `false` |
| approved words | `decision_queue.sh show mpscalc-rollforward-stop-words-1115` | `status:  ruled`, `choice='a'  ruled_ts=2026-11-15T13:49:31.764183+11:00`; the main stop line's fragments occur in the script (line 231) and in the card text |
| seed-secret card | `show mpscalc-deploy-seed-secret-expired-1112` | ruled a, `ruled_ts=2026-11-12T18:36:55.207469+11:00`, delivered |
| deploy card | `show hpsmpoc-review-site-deploy-confirm-1116` | open, `choice=None  ruled_ts=None` (10:02 and 10:10) |
| panes, ports | `tmux list-panes -a`, `lsof -nP -iTCP:9920-9929 -sTCP:LISTEN` | no `MPS-` pane (NexusAI-N136 and HPSM-POC-H172 live: no path of this kit); 0 listeners |

## Step inputs table (measured-literals rule 4)
| step | inputs | produced by |
|---|---|---|
| 0 refusals | the kit copy, two card outputs, `gh`, `df` | BASE (cards exist; kit stamped) |
| 0W words | the fetched commits (`git diff -U0`), `C-111`, the WORD PACK in `Briefs/2026-11-15_B1554_STATUS.md`, the raw script | the one fetch in Target asserts (which runs BEFORE 0W by the kit's own order) and BASE files |
| 0C CI | check-runs, run, artifact list | BASE (GitHub) |
| target asserts | the fetch, `gh api` | BASE; the fetch is the only producer of the `5e800095` objects |
| 1 pre-read, 1S seed | `30_end_*` baselines, `live1542.py` header | BASE (last deploy's evidence folder) |
| 2 backup | Step 1's VFS reads | Step 1 |
| 3 counts | the backup copy | Step 2 |
| 4 package | the worktree (needs the fetch), `gh run download` | the fetch; Step 4 itself; the rollback zip is at BASE |
| 5 swap | the worktree, the verified package, both cards | Step 4 |
| 6-7 checks | the package dir, Step 1 and 2 outputs | Steps 1, 2, 4 |

## D-decisions (mine, each reversible at the Stamp)
- **D1.** The allowed file set is a PROPERTY with the measured list "at least these", not a closed list (rules: closed lists). Unlike the last deploy, the app host and both Pkcs DLLs are byte-equal here (no SDK pin in this delta), so no "two extra files" question should recur.
- **D2.** Words check is lighter than B1542's (91 commits): the production diff adds no customer string (one card removed; `ProposalPage.tsx` comments only, by my reading of its patch); the new surface is the deploy log's operator lines, compared by program against the approved word pack.
- **D3.** Rollback rule stricter than the #196 body strictly needs (any new or changed quote or snapshot file forces fix forward, plus the `fleetLineId` count), because a real user's save also changes what an older build would drop on its next save.
- **D4.** Seller reads, seed identity, and the stop: defaulted to STOP (Q1).
- **D5.** The kit makes the loaded-Xml-file-version read UNMEASURED rather than invent a Kudu process read I could not test.
- **D6.** No rendered view of the price screen or proposal (a proposal GET writes an event); same as the last kit.

## Questions for Tuesday (each with a default)
1. **Q1 Seed secret.** The 11-12 ruling `a` was for that night; the secret is very probably still expired. Default: kit STOPS at the safe boundary (nothing written) if the token fails, unless S4 says the product owner's 18:36 ruling of 12 Nov extends to this deploy. Either stamp S4 with that reading (then the Seller rows are UNMEASURED and the rollback trigger is start-refused or `check` unproven), or put a one-line card to him (skip again, or renew first). Lowering a rollback trigger on a live site was his call last time.
2. **Q2 Part A `PRE-1: STOP:` reasons.** The approved card named the Part B lines; the ten Part A reasons are in the word pack as "the ticket's own words" and are not on the card's face. Default: record them `operator-only, unreachable while overlay.json is absent` (the overlay was absent on 11-12 and PRE-1 would stop the deploy before printing anything else); no card.
3. **Q3 MPSCALC-224.** Is "host patch line + on-site Xml DLL byte-equal to the package + package DLL version strings" enough for the host read, with the loaded-file version UNMEASURED and the ticket staying open? Default: yes.
4. **Q4 Rollback strictness (D3).** Keep strict (fix forward on any changed quote file), or relax to the #196 reading (only snapshots refuse)? Default: strict; S8 can relax.
5. **Q5 Stale `core.sshCommand` on the root repo.** Third mention (B1542 candidate 2, the 11-12 attempt, today). Default: the kit carries the `-c` form; the real fix (launcher or `brief_seat.sh` refreshing it) is outside this brief and outside my fences.
6. **Q6 Launch timing.** The kit is unlaunchable until the card is tapped a or b. Default: launch one waiter after the Stamp and the tap; the S9 slots (swap cut-off, hard stop) are yours. Order beside the Composer kit: no shared resource; the census default (MPS first) stands.

## UNMEASURED (named so no one reads them as measured)
`deploy-from-ci.sh deploy` at `5e800095` has never been run against a host: the roll-forward count line and the per-read token calls are read from source, not seen in a run. The root repo cannot run `merge-base` on `5e800095` until the fetch (object absent). Whether the snapshot reader at `0bb3ed12` uses the strict options (only the options object is measured). Whether `.tools/dotnet-10.0.404` runs (`--version` not run). Whether the seed secret is still expired (inferred from the `.env` mtime and the open backlog row; no token request made). The loaded Xml file version on the host. Whether the web stub files (#193) change the served bundle beyond what the package shows (the new bundle name is measured; the old/new diff content is not read). Rendered screens.

## Outside-the-fences disclosure
- One public `GET /` of the showcase (10:04:07), permitted by the commission as a public version read; no cookie, token or body. One `az account show` under the project `.azure`; no az write; no `az webapp show`.
- `decision_queue.sh show` on three exact ids into scratch (never `list`). `gh api -X GET` only, including one artifact zip download into scratch (a GET; 3.3 MB). Git read verbs on the root repo (`ls-remote` failed on the stale key; `cat-file`, `merge-base`, `rev-parse`, `config --get`, `status --short`, `check-ignore`): no fetch, no ref write.
- I read `4_Credentials/.env` variable NAMES only (`grep -c '^NAME='`) and its mtime; no value was printed or stored. I read the project's BACKLOG, CLARIFICATIONS, the last deploy's STATUS and evidence files, and the Tuesday pickup file for the seed-secret trail. Extracted both packages into scratch. `tmux list-panes` and `lsof` read-only.
- One `rm -rf` of my own scratch folders was refused by the no-delete hook; nothing was deleted (I re-extracted over them). No ledger, scoreboard, briefs_staged, WEDNESDAY, FRIDAY or non-Datasec tree read. No Artifact, mail, board, Jira, push, PR, deploy.

DRAFTED B1607: kit 103 lines, sidecar rc 0, questions 6
