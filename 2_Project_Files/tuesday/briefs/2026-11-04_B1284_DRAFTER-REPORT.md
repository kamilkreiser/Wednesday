STARTABLE: YES once Tuesday fills the seven Stamp slots plus the last line (slots file B1284_slots.json) and re-reads branch head, main, open PRs and the deploy switch; no pane or branch blocks it (load1 was 13.03 at 19:01, launch_when_cool waits for below 7).

## BLUF
1. Kit: 97 lines, 8 four-underscore lines (seven slots plus the last line). B1284 and SEAT-N99 were unused (ls of briefs with `/usr/bin/grep -i` found no B1284 and no N99; N98 = B1278, G341 = B1281).
2. The fix is ONE assertion inside K1, placed right after the `firstRunComplete` toBeUndefined line (`:403`), reusing `settingsText` already read at `:401`: tenant and client must be non-empty strings in the settings file. No new fs call, no request, no new `test(`.
3. The product's status answer does NOT report this state (measured, D-1), so the settings file is the source.
4. Counts file does not change: 5312/317 stays; the kit forbids `--update-counts` and STOPs on any other pair.
5. Red-first: the seat first reproduces the gate's miss (PK4 green at head and under MK), then adds the assertion, then PK4 must be red at the new sentence at head and under MK; MK on the unedited seed red on K1 alone at `not.toBe(before)`; PK1 PK2 PK3 PK5 PK6 as the gate measured; control plant of its own.
6. Sonnet, row C2 (`model-routing.md:92`), id `claude-sonnet-5-5` at `models_latest.json:23`; launch line carries `BRIEF_SEAT_LEVEL=sonnet`; hard stop Step 0 + 120 min, target 75; ports 9850-9859.

## Facts re-measured (instrument | result | control)
| fact | instrument | result | control |
|---|---|---|---|
| branch, main | `git --no-optional-locks ls-remote origin` on the shared checkout, 18:59 AEDT | branch `fc99818aecac06bc5ce944a79495ab658820b506`, main `6e7e94146d77f5127c055d9e922b77bb0f4d9863`, no `b1284*` | the same call prints `b1215`, `b1238`, the b1278 branch and main |
| open PRs | `gh api -X GET pulls?state=open --jq length` (project GH_CONFIG_DIR) | 0 | `pulls/99999` 404 |
| deploy switch | `actions/variables --jq .total_count`; `environments` | 0; `["dev"]` | `variables/zzqxnonexist` 404 |
| test file at head | `gh api -X GET contents?ref=fc99818a` raw, `git hash-object` | `694b004f`, 455 lines, 11 `^test(` | `grep -c '^test('` printed 11, K1 at `:394` |
| other blobs | same | `server.js` `c04a0f4e` 22428 lines (equals the earlier kit's value), `jsonStorage.js` `bba3742b`, `authEnforcement.js` `ca764a4b`; counts file 5312/317 | `server.js` blob equals B1278's `c04a0f4e` |
| K1 pointers | `awk NR==` over the raw test file | seed `:204`-`:206`, users assert `:209`, `:401` read, `:403` firstRunComplete assert, `:415` 401 sentence, `:420` status 200, `:423` re-plant, `:430` `not.toBe(before)`, `:437` "Last in the file" | each line printed its quoted text |
| product pointers | `awk NR==`/`grep -n` over raw files | `riskConditionAdminPasses` `server.js:20991`, input `:20993`, `adminGateRefuses` `authEnforcement.js:634`, `:646` `if (!signInConfigured) return false;`, `:592`, `:618` | `adminGateRefuses({` occurs 9 times (matches the earlier kit) |
| status answer | read `/api/auth/status` `server.js:3625`, `getEntraIdConfig` `:2419`, `authEnforcement.js:618` | `entraIdConfigured` = `c.complete` = tenant AND client AND clientSecret; K1's boot sets no secret | `signInConfigured` at `:592` is tenant AND client only, so the two differ on this boot |
| plain storage | `jsonStorage.js:42`-`:52`, `isSensitiveKey` `:374` | the keys `entraTenantId`/`entraClientId` match no sensitive word; `:2752` reads them as plain `held()` values | the seat MEASURES it (kit says STOP if not plain strings) |
| CI predicate | `grep -n` over raw `build.yml`, `verify-suite.sh` at head | `build.yml:84` `npm run verify -- --maxWorkers=2`; `verify-suite.sh:349` SHRANK, `:360` stale, `:366` `VERDICT: PASS` | numbers identical to the earlier kit's |
| landing rule | `awk NR==` over CLARIFICATIONS.md | `:2067` merge path never squash, `:2062` C-190, ADDENDUM `:2080` | quoted from the file |
| gate verdict | read line 1 of `Briefs/2026-11-04_B1281_STATUS.md` and the whole `evidence/residue.md` | NO GO round 1 of 2, majors B1281-1; Finding 1 fix and PK4 cell quoted in the kit | only one B1281 STATUS exists in the Briefs folder |
| model row | `sed -n` model-routing.md 92-93; models_latest.json | C2 `:92`, C3 `:93`; sonnet id at `:23` | `grep -n sonnet` printed `:22`-`:23` |
| ports 9850-9859 | `lsof -nP -iTCP:9850-9859 -sTCP:LISTEN \| wc -l`; word-boundary scan of non-`.pre-` SEAT kits of 3-4 Nov | 0 listeners; 0 files | blocks 9730-9739 (3 files), 9740-9749 (7), 9860 (2), 9880 (1), 9900 (13) were taken or hit, so avoided |
| panes | `tmux list-panes -a -F '#{@cockpit_name}'` 19:00 | `tuesday`, `Datasec/HPSM-POC-D50`, `Datasec/HPSM-POC-H119`, `fleet-monitor` | no NexusAI pane |
| slot count | `/usr/bin/grep -c -E '_''_''_''_'` on the kit | 8; `@[A-Z]+@` tokens 0 | the slots file has 8 keys |

## D-decisions
- D-1: source = settings file (`settingsText`), not `/api/auth/status`, because the status answer needs a client secret (`:618`) that K1's boot never sets, so it would report false on the very boot K1 builds. Kit says so and asks D3 to cite it.
- D-2: the assertion is a thrown `K1 premise failed:` sentence, same style as the file's 401/403 premises, placed BEFORE the premise POST so PK4 goes red at it and not later; PK1 (`:403`) still goes red first.
- D-3: the kit makes the seat REPRODUCE the gate's miss first (PK4 green at head and under MK, STOP otherwise), so the red proof can fail.
- D-4: PK1/2/3/5/6 are reconstructions from the gate's prose (only PK4 was an exact edit); the kit tells the seat to print each plant's diff and report any difference, never a silent pass. PK3's marker line is copied from U1's seed.
- D-5: header comment K1 line is updated (allowed; same file, no count effect).
- D-6: kit forbids `--update-counts` and STOPs on a changed counts file or any pair other than 5312/317; one path vs the head, two vs main.
- D-7: plain fast-forward push of the existing branch; STOP if origin's branch is not at `fc99818a` after the seat's one fetch.

## Q-questions (each with a default)
- Q-1: round count wording: "round 2 of 2 on class `NexusAI RD-924: first-run input cell of the RD-902 read-path check`". Default: as written.
- Q-2: gate tier after this kit (round-2 gate, G2 Opus column, as round 1). Default: same as round 1.
- Q-3: hard stop 120 / target 75 (the brief said 120). Default: accept.
- Q-4: ports 9850-9859. Default: accept.
- Q-5: the seat creates a second tree `worktrees/b1284-probe` for plants (a `git worktree add` in the seat's OWN clone; the drafter fence forbids worktrees only for the drafter in a project repo). Default: allowed.

## UNMEASURED
- That the two keys are plain strings in the K1 boot's settings.json at run time (read from source only; the seat measures and STOPs otherwise).
- Whether the harness environment sets a tenant or client through env (env is read first by `resolveEntraConfig`, `server.js:2420` comment); the assertion tests the settings file only, which is what the seed writes.
- That PK1, PK2, PK3, PK5, PK6 reconstructions equal the gate's exact edits.
- No jest, node or npm was run; the red/green predictions come from the gate's measures and source reading.
- Hosted Build, Gitleaks and CodeQL; node 24 on Linux; gauge.

## Outside the fences
- `gh api -X GET` raw `contents?ref=fc99818a` of four files and the workflow/script/counts, under the project GH_CONFIG_DIR; the files were saved to the session scratchpad (outside the briefs folder) and read there. No fetch, no worktree, no ref write in any project repo.
- Read the B1281 STATUS line 1 (the sibling `ls` of the project Briefs folder lists names only) and `evidence/residue.md`; read the B1278 `.pre-stamp` and stamped kit, B1281 and B1283 slots files and the B1283 report for shape.
- `lsof` and `tmux list-panes` reads; no write outside the three output files. First Bash call was refused by a `cd` hook (a `cd` was typed); re-issued without it.
