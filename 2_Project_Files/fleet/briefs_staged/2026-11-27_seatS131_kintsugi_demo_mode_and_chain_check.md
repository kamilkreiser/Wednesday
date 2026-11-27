# BRIEF: Seat S 131st, Secuura/Blockchain-S. KINTSUGI (dev box, NOT demo), READ-ONLY, ONE QUESTION (QA gate 421, finding G421-1): are the 10 "confirmed" anchor rows behind the 10 stuck certifications REAL Cardano preview transactions, or could they be DEMO_MODE mock confirmations? Three independent legs, reported SEPARATELY: A the box's configuration now, B the rows' own shape, C the chain's word. Nothing is repaired or written. Model: set at launch by Wednesday. A lean delta of Seat S 130th's brief (same box, route, method, controls). The STAMP at the end wins over every line.

PATHS: `BCH` = /Volumes/DevMASTER/!CODING/Secuura/Blockchain ; `P130` = BCH/5_Project_History/2026-11-27_seatS-130th ; `WED` = /Volumes/DevMASTER/WEDNESDAY (so `FLEET` = WED/2_Project_Files/fleet/briefs_staged).

**NO `cd` ANYWHERE: absolute paths only. Read this BRIEF WHOLE, to its last line, before any memory note; the launcher's first-action text (vault listing, board survey, extranet to-dos, `POST /api/seen`) is NOT your plan. Never `rm`: MOVE with `mv -n`. Never discard stderr. CREDENTIALS: this project's own mail key only, read INSIDE a python script from the project `.env`, never in argv or output; never the vault Access folder; never open 4_Credentials or 3_Access_Keys (NAME the Kintsugi key file, never open it). zsh: no unquoted word starting with `=`, no `echo rc=$?` after a pipeline, no unquoted globs; a grep that returns nothing is not an absence until a positive control from the same text hits (`/usr/bin/grep -i`). Every time you write comes from `date -u`, never typed.**

## QUEUE (every box contact waits for Wednesday's ANSWER to your plan QUESTION)
Local first (0, 4). After the ANSWER, each by name: S131-LICENCE, S131-KEYSCAN, S131-CONNECT, S131-ID, S131-CFG (leg A), S131-DM (leg B: `agg`, then `hashes`), then S131-CHAIN (leg C, your Mac, 5). Privacy check, STATUS, WAIT for her word, wrap.

## AUTHORITY
- **Wednesday's decision**, under Kam's signed protocol v1.3 (WED/0_Brain/learnings/2026-08-07_protocol-v1.3-signed-delegation.md). Scope, verbatim: "**Mine to authorise on his behalf:** merges · deploys to dev, staging, test and demo · ticket creation, triage, priority, status · scope and sequencing inside work he has already commissioned · accepting or rejecting an agent's deviation on technical grounds · anything reversible inside a project." It excludes production, money, external communication, irreversible actions and any authority originating with her. A read-only read of the dev box is reversible and inside the first list; not a new Kam ruling.
- **Why:** gate 421 (PR 2296, the KS-2366 repair) found G421-1 (Major): a DEMO_MODE mock stores a bare 64-hex sha256 as the "transaction", status confirmed, simulated false, passing every predicate S 129th and S 130th used; nobody has excluded it for Kintsugi. Its condition: show anchoring was NOT in DEMO_MODE over the stuck range, or look up a hash on preview.
- **Kam's ruling this serves** (`bash WED/2_Project_Files/tools/decision_queue.sh show secuura-ks2366-repair-old-stuck-certifications-1127`): title "KS-2366: the old stuck certifications' anchors DID confirm (demo 36 of 37, Kintsugi 10 of 10). Repair them?"; chosen option `[a] Repair, Kintsugi first`; `choice='a'  ruled_ts=2026-11-27T13:05:58.078926+11:00`. It licenses the repair on Kintsugi first and NOTHING in this brief: this read is Wednesday's precondition check.
- **Wednesday's ruling (hers):** the 10 transaction hashes of the stuck certifications' anchor rows MAY leave the box to a public Cardano preview explorer (5); NOTHING else may (no id, payload, tenant, certification or document id, no hash of any content).
- **Not licensed:** repair, data change, deploy, restart, rollback, any docker verb that writes, HTTP to the stack (it writes an `audit_logs` row), demo or production, mail to a human, Linear/GitHub/decision-queue writes, proposing a repair.
- **Project rules, quoted:** /Volumes/DevMASTER/!CODING/Secuura/CLAUDE.md names Kintsugi 0 times (its word `secuura` reads 9, the control); BCH/CLAUDE.md names it once, line 9: "kintsugi does NOT hold this invariant: 2 rows simulated=true AND status=confirmed (mock_tx_*, created 2026-08-20), measured by Seat D 35th; tracked as KS-1751". Secrets: BCH/CLAUDE.md 63 "`.env` and `.env.local` under `Blockchain/Dev/` are gitignored — never commit.", 166 likewise; workspace rule 3 "Never commit secrets"; 187 "The extranet is not a channel". Neither file grants or forbids a seat reading the box; the grant is this AUTHORITY plus her ANSWER. **S 130th held "no `.env` or config read"; this brief relaxes it for ONE key's value and the compose file's matched lines only if her ANSWER names S131-ENVKEY (3).**

## HOLDS (the whole session)
Read-only everywhere. No docker verb that writes (no run, compose, restart, rm, stop, pull, prune, cp, tag, exec -it); no file write on the box; **no env-file line other than the one key `ANCHORING_DEMO_MODE`, value only; no secret printed; never `docker inspect` env or mounts**; the wallet mnemonic and Blockfrost key are NEVER touched, tested, hashed or printed (no presence test either). Do not touch `.rebuild-seatD88` or any `.env.pre-*`. Prod and demo never contacted: **an ssh to any target other than 20.198.226.148 (hostname `secuura02-kintsugi-vm`) is a STOP.** No `az`. No HTTP to any Secuura host. **No identifier leaves the box except the 10 transaction hashes, only into `hashes_s131.out` and the leg-C lookup; never into a mail, the STATUS, the wrap or a note (mails name rows by ordinal 1 to 10).** The public API is called from your Mac, never the box, no key, at most 8 requests. Every tree under /Volumes/DevMASTER/!CODING/ is READ-ONLY except your REC folder, scratchpad and vault daily-note line. Mail only to `wednesday-agent@agentmail.to`.

RULED BY KAM, NOT YET IN AN ARTEFACT
- None carried into this seat's work. Kam's ruling on card secuura-ks2366-repair-old-stuck-certifications-1127 ("a — Repair, Kintsugi first") lands in PR 2296 and in a later deploy seat's Kintsugi run, not in this read; this seat acts on Wednesday's standing authority (AUTHORITY above).

RULED BY WEDNESDAY, CARRIED from S 130th (re-keyed)
- **R1:** NOTHING touches the network before her ANSWER, ssh-keyscan and the public API included; an item the ANSWER does not name does not run. S131-CONNECT condition: your keyscan equals SHA256:gl2JBs7KpV7/wrYd/7bzqTNQ+wyFQJomCtQkfUs8nuU AND the address is 20.198.226.148; a mismatch is a STOP with no connection; STATUS with the scan result before the first ssh, carry on without waiting.
- **R2:** 3b (refused write) runs ONLY after 3a reads `on`; 3b SUCCEEDING is a STOP: run nothing else, mail at once.
- **R3:** a REVISION head other than `4764b2cfbc28` is a STOP and a QUESTION (a deploy may have restarted anchoring); a stuck total other than exactly 10 is a STOP and a QUESTION (the 10 hashes must be the 10 certifications).
- **R5:** a mail not naming `(Seat S 131st)` is NOT yours. History's top entry at drafting is Seat W 78th's (the repair builder): its pane's state is STAMP W5. Re-read history.md's top just before adding your heading; another seat's edit in progress is a STOP.
- **R6:** report your statusline's weekly usage figure in the plan QUESTION; no `az`; if your pane's model looks wrong, say so first and touch no box.
- **R7:** no uuid-shaped string and no at-sign in any evidence or mail; **no 64-hex string anywhere except `evidence/hashes_s131.out` and your leg-C request/response files; every other box output, mail and the wrap read 0.** Planted-token controls read 1. Kit file sha256 lines in the plan mail are allowed.
- **R8 (STOP):** any of the 10 hashes NOT found on preview, any mock-pattern row (M above 0) or any stored block at or above 10,500,000 is a STOP and a STATUS mail: no further conclusion, nothing further on the box.

## 0. FIRST ACTIONS
1. `/usr/bin/grep -o -i -c 'seat s 131st'` over BCH/5_Project_History/history.md must be 0; controls 'seat s 130th' 1, 'seat s 129th' 1. REC = BCH/5_Project_History/<machine date>_seatS-131st/ (nothing else new under 5_Project_History). Seat name exactly `Seat S 131st`. `FLEET/s131_*.md` is an older series, another lane.
2. Read FIRST: P130/HANDOVER.md, DECLARED.md, tools/. Copy the launcher's preflight warnings to REC (VERBATIM into the plan mail).
3. **PLAN QUESTION FIRST** (R1): `[Secuura/Blockchain-S -> Wednesday] QUESTION: plan confirmation (Seat S 131st)` with the plan; EVERY remote tool in full (every SQL statement and shell read); kit hashes READ FROM THE FILES that minute vs the table in 4; the pin question; warnings VERBATIM; the weekly figure; the exact leg-C requests; the item names for her ANSWER (with gates S131-ENVKEY, S131-LOGCOUNT). No ANSWER in 15 minutes: local steps only.

## 1. WHAT THE REPOSITORY SAYS THE MOCK DOES (`git show origin/develop:<path>`, `GIT_OPTIONAL_LOCKS=0`, local tip 0e6479d7b of Nov 10: the deployed head 4764b2cf is NOT in the local objects; files under `Blockchain/Dev/services/anchoring/src/`)
- `mocks/mockProvider.ts` 55-59: `this.counter++;` then `const txHash = createHash('sha256').update(`mock-tx:${contentHash}:${this.counter}`).digest('hex');` (BARE 64-hex). 74-77: `blockNumber: 10_500_000 + this.counter * 47,` `slot: 131_000_000 + this.counter * 20,` `network: 'devnet',` `status: 'confirmed' as const,`; `waitForConfirmation` 91-92 repeats both. **The counter is incremented BEFORE use: the first mock block is 10,500,047 (n >= 1, not n >= 0), and it is per process, restarting at 0 with the container, so block numbers can repeat.**
- `cardano/index.ts` 60-68: `if (process.env.DEMO_MODE === 'true') { if (process.env.NODE_ENV === 'production') {... process.exit(1); } demoMode = true; mockProvider = new MockAnchoringProvider(); ...`. 253-257: the mock hash "does NOT match `FABRICATED_TX_PREFIX` ... and DOES match the /^[0-9a-f]{64}$/i test". 270-273: `if (demoMode && mockProvider) { ... const result = await mockProvider.submitAnchor(contentHash); return { txHash: result.transactionHash, fee: Number(result.fee) }; }`; 335-337 spread the mock confirmation (blockNumber, slot) in; the mock's `network: 'devnet'` is NOT passed on, so a stored network value does not discriminate.
- Compose, `Blockchain/Dev/docker-compose.yml` 1325: `- DEMO_MODE=${ANCHORING_DEMO_MODE:-false}`. The variable INSIDE the container is `DEMO_MODE`; `ANCHORING_DEMO_MODE` is only a compose interpolation key (env file or shell), NOT exported into the container: expect it UNSET there. A `DEMO_MODE=true` env-file line does not reach anchoring (others use `${DEMO_MODE:-true}`, 780, 2200). Anchoring sets `NODE_ENV=development` (1301): the production exit(1) does not protect Kintsugi.
- A DIFFERENT mock path (no Blockfrost key or wallet, `index.ts` 2070-2096): hash `mock_tx_<hex>`, `blockNumber = null`; the fabricated prefix S 130th counted 0 for the 10. Kintsugi HAS held such rows (KS-1751; S 130th's census: confirmed f 161, confirmed t 2, failed f 3): "never mocked here" cannot be assumed.
- **Leg-B pattern:** MOCK BLOCK = `block_number >= 10500047 and (block_number - 10500000) % 47 = 0`; MOCK SLOT = `slot >= 131000020 and (slot - 131000000) % 20 = 0`; PAIR = both with the same n. A real block can pass the modulus by chance (~1 in 47); the sharper test is magnitude: the drafter measured the live preview tip at block_height 4899218, abs_slot 129098820, so a stored block at or above 10,500,000 or slot at or above 131,000,000 is beyond the real chain. If `with_block` is low or 0, leg B is SILENT, not clean (a real path can store a null block, `index.ts` 1409).

## 2. REACH, IDENTITY AND THE PIN (carried unchanged from S 130th; after the ANSWER)
- Route: ssh `secuura@20.198.226.148`, key file BCH/3_Access_Keys/vm_secuura02_kintsugi (named, never opened); the runner's ssh options are S 130th's, unchanged; each run is a `hostname` check then the tool over `bash -s`.
- **THE PIN IS A PRIOR, NOT AN INDEPENDENT SOURCE:** `SHA256:gl2JBs7KpV7/wrYd/7bzqTNQ+wyFQJomCtQkfUs8nuU` for 20.198.226.148, extracted by the drafter from S 130th's brief and asserted equal to its `kint_hostkey_s130.sh` `WANT=` line and `kint_run_s130.sh` `H=` line. S 130th's scan equalled it.
- `kint_id_s131.sh` = `kint_id_s130.sh` with ONE edit (`ID_S130` -> `ID_S131`): I1 hostname; I2 REVISION head begins `revision=4764b2cfbc28` (R3); I3 originate container reported; I4 exactly one `-postgres` name, `secuura-postgres`.

## 3. LEG A, THE BOX'S CONFIGURATION NOW: remote tool `kint_cfg_s131.sh` (no SQL; named reads)
**"Now" is not "then".** `secuura-anchoring` was last started 2026-11-15 (PROVENANCE); the 10 certifications date 2026-09-17 to 2026-11-16. A1 prints the start. Leg A can support "not in DEMO_MODE since that start"; it cannot prove the past. Say so.
Tool (tested on a stub `docker`; `stat -c`, `date -d` are Ubuntu-only: stub them locally):
```
#!/bin/bash
set -u
case "$(hostname)" in secuura02-kintsugi-vm) : ;; *) echo "REFUSED: not the kintsugi box"; exit 9;; esac
echo "CFG $(date -u +%FT%TZ) host=$(hostname)"
stop() { echo "STOP: $1"; echo "END $(date -u +%FT%TZ)"; exit 7; }
C=secuura-anchoring
echo "--- A1 container, one inspect, named fields"
F=$(docker inspect -f '{{.Name}} | {{.Image}} | {{.State.Status}} | {{.State.StartedAt}} | {{index .Config.Labels "com.docker.compose.project.working_dir"}} | {{index .Config.Labels "com.docker.compose.project.config_files"}}' "$C") || stop "A1 inspect failed"
IFS='|' read -r NAME IMG STATE STARTED WD CF <<< "$F"
IMG=${IMG// /}; IMG=${IMG#sha256:}; IMG=${IMG:0:12}; NAME=${NAME// /}; STATE=${STATE// /}; STARTED=${STARTED// /}; WD=${WD// /}; CF=${CF// /}
echo "name=$NAME image12=$IMG status=$STATE startedAt=$STARTED"
echo "compose working_dir=$WD config_files=$CF"
echo "--- A2 container env, named keys only"
for k in DEMO_MODE ANCHORING_DEMO_MODE NODE_ENV CARDANO_NETWORK ZZ_S131_NO_SUCH_VAR; do
  v=$(docker exec "$C" printenv "$k" 2>&1); rc=$?; echo "A2 $k rc=$rc value=[$v]"
done
echo "--- A3 compose line, matched lines only"
IFS=',' read -r -a FILES <<< "$CF"
for f in "${FILES[@]}"; do
  [ -r "$f" ] || { echo "A3 unreadable"; continue; }
  echo "A3 control: container_name lines=$(/usr/bin/grep -c -F 'container_name' "$f") ; made-up token lines=$(/usr/bin/grep -c -F 'zz_s131_none' "$f")"
  /usr/bin/grep -n -F 'ANCHORING_DEMO_MODE' "$f"; echo "A3 matched-line count=$(/usr/bin/grep -c -F 'ANCHORING_DEMO_MODE' "$f")"
done
# GATE S131-ENVKEY begin
echo "--- A4 env file, ONE key, value only"
E="$WD/.env"
if [ -r "$E" ]; then
  echo "A4 lines naming the key anywhere=$(/usr/bin/grep -c -F 'ANCHORING_DEMO_MODE' "$E") ; lines starting with the key and =$(/usr/bin/grep -c '^ANCHORING_DEMO_MODE=' "$E")"
  echo "A4 value(s), at most 3:"; sed -n 's/^ANCHORING_DEMO_MODE=//p' "$E" | head -n 3
  echo "A4 file mtime epoch=$(stat -c %Y "$E") ; container start epoch=$(date -d "$STARTED" +%s)"
else echo "A4 env file not readable by this login"; fi
# GATE S131-ENVKEY end
# GATE S131-LOGCOUNT begin
echo "--- A5 boot-log counts only"
n_all=$(docker logs "$C" 2>&1 | /usr/bin/grep -c .)
n_demo=$(docker logs "$C" 2>&1 | /usr/bin/grep -c -F 'DEMO_MODE active')
n_ready=$(docker logs "$C" 2>&1 | /usr/bin/grep -c -F 'Integration ready')
n_none=$(docker logs "$C" 2>&1 | /usr/bin/grep -c -F 'zz_s131_none')
echo "A5 log_lines=$n_all demo_active=$n_demo integration_ready=$n_ready made_up=$n_none"
# GATE S131-LOGCOUNT end
echo "END $(date -u +%FT%TZ)"
```
- A1: ONE `docker inspect` of named fields (incl. the compose working dir and config files from labels); never env, mounts or logs.
- A2 expected: DEMO_MODE rc 0 `false` or rc 1 (unset = not demo); ANCHORING_DEMO_MODE rc 1 (not exported); NODE_ENV `development` (positive control); the made-up name rc 1. `DEMO_MODE` `true` is REPORTED prominently, not a STOP.
- A3: the compose line(s), matched lines only (controls in the tool); expected `- DEMO_MODE=${ANCHORING_DEMO_MODE:-false}`.
- **A4 (gate S131-ENVKEY; delete the block unless her ANSWER names it):** the env file's ONE key: two line counts, its value (at most 3 lines), the file's mtime epoch vs the container's start epoch. No other line. An mtime after the start means the file is not necessarily what the container started with.
- **A5 (gate S131-LOGCOUNT; delete unless named):** counts only of `DEMO_MODE active` and `Integration ready` in the boot log (controls in the tool). Rotation can empty the boot lines: then a 0 is not evidence.
- The runner's write-token regex finds nothing in this tool (drafter ran it, planted control hit).

## 4. THE KIT: S 130th's finished tools re-keyed by COUNTED edits (originals untouched; `rekey_s131.py` on the pattern of `rekey_s130.py` (not read whole by the drafter); mode 'x')
Sources P130/tools/ (say if any hash differs); outputs named `<tool>_s131.<ext>`. Counts are on NON-history lines (those starting `# LINEAGE`, `# NEW TOOL`, `# Differences`, `#!`); assert each; keep original headers as `# LINEAGE`; print old and new sha256.
| source | sha256 (bytes) | counted edits |
|---|---|---|
| am_s130.py | 2766b566b11fd21fc00dd576fab1d88fcc1121dcb7a3f212d98cf5109745b9e5 (6691) | `am_s130`->`am_s131` 4; `Seat S 130th`->`Seat S 131st` 4; REC path 1 |
| kint_run_s130.sh | 4a79316bcdcd4e83a668414c85a50cb9a00534efb97e02f9519db1d28a1d7425 (3391) | `s130`->`s131` 3; REC path 1; `SP=` 1; the tool `case` -> exactly `kint_id_s131.sh`, `kint_cfg_s131.sh`, `kint_dm_s131.sh`, a plain `case`, no glob; every guard unchanged (it already passes ONE plain token, `agg` or `hashes`) |
| kint_hostkey_s130.sh | d13f36b6a2b4025330d010bdc588e91c4f8c100c6c7095d2e8b4193acbabec8c (2888) | `s130`->`s131` 7; REC 1; scratchpad 1; the `WANT=` pin line and address NOT edited (assert byte-equal); both controls stay |
| kint_id_s130.sh | 56a071ffd82b6c590a2afe77511e9a14f8d8371301153878ea0b5ed8842fe1ad (2683) | `ID_S130`->`ID_S131` 1, nothing else |
| kint_anc_s130.sh | f6ef86698d1db7460dc4b302d2a66c01df416a76870e5798cf799d798f550845 (22859) | SOURCE of `kint_dm_s131.sh` (4.1) |
| privacy_s130.sh | ecb8345a54830b21556313b998f9cf6ff9be6cbd6aaf9242a6efd8307f52acd0 (1568) | header `s130`->`s131`; `box` kind on every box output EXCEPT `hashes_s131.out` (own pass: at-sign 0, uuid 0, 64-hex exactly 10 lines) |
Stale check: no `s130`, `130th`, `anc` or `CERTS` on a non-history line of any new file.
**4.1 `kint_dm_s131.sh` (argument `agg` or `hashes`; else exit 7) = `kint_anc_s130.sh` (284 lines, read whole) with these changes:**
- KEPT byte for byte (your script diffs them): lines 13-14, `q()` 16-18, `run` 19-28, `stop`/`must`/`isnum` 29-31; 3a 33-35 (S 130th read `on|secuura|t|t|f`), 3b 37-39, 3c 41-43 (`zz_s130_probe`->`zz_s131_probe` 1, `no_such_table_s130`->`no_such_table_s131` 2); CENSUS/DOCSUM before 45-54 (mode `agg` only); G1, G2 58-63 and runs 155-158 (want 12, 10); QA 64-90, its run and 8 checks 174-193, the `IFS` read 194.
- CHANGED: 195-197 -> **a stuck total other than exactly 10 is a STOP** (R3). DROPPED: QB, QC1, QC2, POS, M2-M4, FB1, FB2, CERTS, their runs and checks, the `fallback`/`measure` branch (91-152, 160-171, 199-263).
- ADDED: G3; mode `agg`: BA, BB, BN, M1 and the kept after-state (270-276); mode `hashes`: TX only (after 3a-3c, G1-G3, QA); new SUMMARY lines. **S 130th's instrument never touched `block_number`, `slot`, `network` or `confirmed_at`: its guards name six `anchor_store` columns without them.**
`<STUCK>` = S 130th's stuck predicate, unchanged (first CTE of its QA):
```
with stuck as (select d.id, d.tenant_id, d.created_at, b.blob from documents d cross join lateral (select coalesce(nullif(d.certification_metadata->'blockchain','null'::jsonb), nullif(d.metadata->'blockchain','null'::jsonb)) as blob) b where d.certification_metadata->>'certificationType' is not null and d.external_id is null and b.blob->>'anchoringStatus' = 'submitted' and b.blob->>'status' is null and b.blob->>'txHash' is null)
```
Each statement is `<STUCK>` then the text shown (run by the drafter on local PostgreSQL 15.19 with SYNTHETIC real-, mock- and mixed-shaped data: proves they parse and discriminate, nothing about Kintsugi):
```
G3 (want 5):  select count(*) from information_schema.columns where table_schema='public' and table_name='anchor_store' and ((column_name in ('block_number','slot') and data_type='bigint') or (column_name in ('network','anchor_type') and data_type='text') or (column_name='confirmed_at' and data_type='timestamp with time zone'))
BA (<K> = a.id = s.blob->>'anchorId')   BB (<K> = a.document_id = s.id::text):
, r as (select a.* from stuck s join anchor_store a on <K>)
select count(*) as n,
       count(*) filter (where block_number is not null) as with_block,
       count(*) filter (where block_number >= 10500047 and (block_number - 10500000) % 47 = 0) as mock_block_pattern,
       count(*) filter (where block_number >= 10500000) as block_at_or_above_10_5m,
       coalesce(min(block_number)::text, '-') as block_min,
       coalesce(max(block_number)::text, '-') as block_max,
       count(distinct block_number) as block_distinct,
       count(*) filter (where slot is not null) as with_slot,
       count(*) filter (where slot >= 131000020 and (slot - 131000000) % 20 = 0) as mock_slot_pattern,
       count(*) filter (where block_number >= 10500047 and (block_number - 10500000) % 47 = 0 and slot = 131000000 + 20 * ((block_number - 10500000) / 47)) as mock_pair_same_n,
       coalesce(min(slot)::text, '-') as slot_min,
       coalesce(max(slot)::text, '-') as slot_max,
       count(distinct slot) as slot_distinct,
       count(*) filter (where confirmed_at is not null) as with_confirmed_at,
       coalesce(round(min(extract(epoch from (confirmed_at - created_at)))::numeric, 3)::text, '-') as secs_min,
       coalesce(round((percentile_cont(0.5) within group (order by extract(epoch from (confirmed_at - created_at))))::numeric, 3)::text, '-') as secs_median,
       coalesce(round(max(extract(epoch from (confirmed_at - created_at)))::numeric, 3)::text, '-') as secs_max,
       count(*) filter (where transaction_hash ~ '^[0-9a-fA-F]{64}$') as hex64,
       count(distinct transaction_hash) as tx_distinct
  from r
BN:
select a.network, a.anchor_type, a.simulated, count(*) as n
  from stuck s join anchor_store a on a.id = s.blob->>'anchorId'
 group by 1,2,3 order by 1,2,3
M1 (made-up anchor id, want 0):
 select count(*) from stuck s join anchor_store a on a.id = 'zz-s131-no-such-anchor-7d2e'
TX (mode hashes ONLY):
select row_number() over (order by a.block_number nulls last, a.transaction_hash, a.id) as ord,
       coalesce(a.transaction_hash, '-') as transaction_hash,
       coalesce(a.block_number::text, '-') as block_number,
       coalesce(a.slot::text, '-') as slot,
       coalesce(extract(epoch from a.confirmed_at)::bigint::text, '-') as confirmed_epoch
  from stuck s join anchor_store a on a.id = s.blob->>'anchorId'
 order by 1
```
Checks, each `check <name>: <values> ok` or STOP: G3 = 5; BA, BB one row of 19 fields (1-4, 7-10, 13-14, 18-19 integers; 5-6, 11-12 integer or `-`; 15-17 decimal or `-`); BA.n = BB.n = QA `stuck_n` = 10; `mock_block_pattern` <= `with_block`; `mock_pair_same_n` <= `mock_block_pattern`; `block_distinct` <= `with_block`; BN counts sum 10; M1 = 0; BA equals BB line for line is REPORTED. Mode `hashes`: exactly 10 lines of 5 fields, `ord` 1-10, field 2 a 64-hex or `-` (`-` or non-hex is a STOP). SUMMARY: one `SUMMARY legB` line carrying BA's 19 named fields.
**4.2 Dry-run LOCALLY, no network:** stub `hostname` and `docker`, a throwaway local postgres on a 127.0.0.1 TCP port (a deep scratchpad overflows the unix-socket path), S 130th's `dry_data_s130.sql` copied with counted edits (add `anchor_type`, `block_number`, `slot`, `confirmed_at` and real- and mock-shaped values). Cases: `agg` rc 0 on real- and mock-shaped data (synthetic BA: real-shaped `10|10|0|0|4801940|...`, mock-shaped `10|10|10|10|10500141|...`); `hashes` rc 0, 10 lines; 3b succeeding rc 8; a missing column, stuck 9, stuck 11, a missing or unknown mode rc 7; runner and keyscan refused rc 9 with no licence; the cfg tool on stubs. Show outputs in the plan mail.

## 5. WHAT TO REPORT PER LEG
**B (mode `agg`; aggregates only; rows reached as S 130th reached them, BA by the blob's anchorId, BB by document id):** `mock_block_pattern` (M of 10), `block_ge_10_5m` beside it, `mock_slot_pattern`, `mock_pair`, `block_min`, `block_max`, `block_distinct`, `with_block`, the networks with counts (BN), `secs_min`/`secs_median`/`secs_max` of confirmed_at minus created_at (a mock confirms in well under a second; a real one needs a block interval, though a reconciler can confirm later: describe, do not over-read), `hex64`, `tx_distinct` (a batch can share a hash).
**C (from YOUR Mac, after `hashes` and S131-CHAIN):**
- Endpoint (quote every URL in the shell), found in public documentation: **Koios, preview instance, `https://preview.koios.rest/api/v1`**, the "Preview Network" entry in the OpenAPI at `https://api.koios.rest/koiosapi.yaml` (servers block lines 147-153), which states use is "completely free and there are no registration requirements", a public tier "unauthenticated", a burst limit of 100 requests per 10 s per IP and a 1 kb public request-body limit. No key.
- Req 1 `curl -sS -m 20 -w '\nHTTP %{http_code}\n' 'https://preview.koios.rest/api/v1/genesis?select=networkmagic,networkid'` must read `"2"`, `Testnet` (mainnet 764824073). Req 2 `GET .../tip` (`block_height` H, `abs_slot`, `block_time`).
- Req 3 a block ~100 below the tip with transactions (the NEWEST block's tx can read `[]` briefly: the drafter's first try did): `GET .../blocks?block_height=lt.<H-100>&tx_count=gt.0&order=block_height.desc&limit=1&select=hash,block_height,block_time,tx_count`. Req 4 `POST .../block_txs` `{"_block_hashes":["<hash>"]}`; take the first `tx_hash`.
- **POSITIVE CONTROL** Req 5 `POST .../tx_info` `{"_tx_hashes":["<that tx>"]}` (headers `content-type: application/json`, `accept: application/json`): 1 element, `block_height` equal to the block's. **NEGATIVE CONTROL** Req 6, a made-up hash from `python3 -I -c 'import secrets;print(secrets.token_hex(32))'`: **"not found" is HTTP 200 with body `[]`, not 404** (drafter-measured); must read `[]`. A failed control is a STOP, not a retry on another host.
- Req 7, the 10: ONE `POST .../tx_info` `{"_tx_hashes":[<distinct hashes of hashes_s131.out>]}`, body built in python, sent `--data @file` (under 1 kb; a 413 means split in two). A found hash returns `tx_hash`, `block_height`, `tx_timestamp`, `absolute_slot`, `block_hash`; a hash missing from the response is NOT FOUND. Req 8 only retries the positive control; HTTP 429: wait the documented 60 s once.
- Per row, by ORDINAL only: found or not; if found `block_height`, `tx_timestamp`, `absolute_slot`; against the box's stored values: block_number equals `block_height` (count; a null box block is apart, not a mismatch), the box's confirmed epoch minus `tx_timestamp` (min, max), slot equals `absolute_slot`; a different block than stored is REPORTED.
- A reason you find this lookup unsafe: STOP before Req 1 and QUESTION (STAMP W3).
**THE VERDICT: each leg separately, which legs agree, then ONE line exactly:** `REAL on chain: N of 10 found; mock-pattern rows: M of 10; DEMO_MODE now: <value>` (the container's DEMO_MODE as A2 printed it, `unset` for rc 1). R8 applies.

## 6. MAIL AND WRAP (as S 130th's)
From secuura-blockchain@agentmail.to to wednesday-agent@agentmail.to ONLY; subjects `[Secuura/Blockchain-S -> Wednesday] ... (Seat S 131st)`, body line 1 exactly `Seat S 131st`; no secrets, no at-sign in a body; `am_s131.py` (`get` needs the FULL message id); a 3-hour watcher. Sequence is the QUEUE; the final STATUS carries the three legs, their agreement, the verdict line, exact SQL, argv, box times and the limits in 7. No Linear, no human, no repair proposal.
WRAP: history entry `## <machine date> - Seat S 131st` at the top of history.md (guard 'seat s 131st' 0 then 1; 'seat s 130th' and 'seat s 129th' stay 1; no other seat's full name in it); REC/HANDOVER.md; REC/DECLARED.md (every edit and deviation, re-key counts and sha256s, every exec's argv, every public request's URL without hashes); a vault daily-note line by explicit path in ONE commit; the wrap mail. IF BLOCKED: no Kam; one QUESTION per mail, inbox every ~3 minutes; after ~15 minutes proceed on the safest read-only reading EXCEPT every box contact and the public lookup. HANDOVER at context ~70%.

## 7. WHAT THIS CANNOT SHOW (say it in the STATUS)
- A is "now" and dates only from the anchoring container's last start (2026-11-15); it does not prove 2026-09-17 to 2026-11-15.
- B is silent when blocks are null; the modulus can match a real block by chance (magnitude is sharper); a restarted mock counter repeats numbers.
- C proves a hash exists on preview and where; not that it carries this certification's payload (`_metadata` not requested), and for a re-anchored row it names that row's current transaction (one row per (document_id, network), overwritten on re-anchor).
- Only C is outside the box's own say-so. Preview is a TEST network. The code was read at a Nov 10 commit, not the deployed head. Nothing says a repair is right.

## ROUTING AND MODEL
## model: set at launch by Wednesday (no model id carried; Seats S 125th to S 130th ran Sonnet). Lane -S. Seat name exactly `Seat S 131st`.

PROVENANCE: (fact | source | read); short paths as in PATHS
- Mock hash, block, slot, network, status, counter formulas | `Blockchain/Dev/services/anchoring/src/mocks/mockProvider.ts` 55-59, 74-77, 91-92 via `git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files show origin/develop:<path>`, `GIT_OPTIONAL_LOCKS=0`; commit read 0e6479d7b06c06b6f8a77aae1cbad167afbdaa089 (deployed head 4764b2cf not in local objects: `git cat-file -t` failed) (paths inside your project repository, your project) | read 2026-11-27 (by the drafter)
- DEMO_MODE switch and mock delegation | same checkout, `.../anchoring/src/cardano/index.ts` 60-68, 253-257, 270-273, 335-337 (paths inside your project repository, your project) | read 2026-11-27 (by the drafter)
- Compose line, NODE_ENV, other services; origin 846717ecf of 2026-04-27 | `Blockchain/Dev/docker-compose.yml` 1325, 1301, 780, 2200; `git log -S` (paths inside your project repository, your project) | read 2026-11-27 (by the drafter)
- No-keys mock path, null block | `.../anchoring/src/index.ts` 2070-2096, 1409 (paths inside your project repository, your project) | read 2026-11-27 (by the drafter)
- anchor_store columns (block_number, slot, network, anchor_type, confirmed_at) | `Blockchain/Dev/migrations/003_consolidate-anchors.sql` 16-38; NOT read on the box (paths inside your project repository, your project) | read 2026-11-27 (by the drafter)
- G421-1 | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-27_gate421-tier1-ks2366-legacy-anchor-repair/verdict.md 42-47, 71-88 | read 2026-11-27 (by the drafter)
- Card title, chosen option, ruled_ts | command read: `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show secuura-ks2366-repair-old-stuck-certifications-1127` | read 2026-11-27 (by the drafter)
- v1.3 scope and exclusions | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-08-07_protocol-v1.3-signed-delegation.md 32-35, 37-41 | read 2026-11-27 (by the drafter)
- CLAUDE.md quotes and counts | `/usr/bin/grep -c -i kintsugi`, `sed -n 63p;166p;187p`, `grep -n` for line 9, on /Volumes/DevMASTER/!CODING/Secuura/CLAUDE.md and /Volumes/DevMASTER/!CODING/Secuura/Blockchain/CLAUDE.md | read 2026-11-27 (by the drafter)
- S 130th result, 3a row, census | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-27_S130_status_number.txt 8-33, 42-53; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-27_seatS-130th/HANDOVER.md | read 2026-11-27 (by the drafter)
- S 130th instrument, line numbers | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-27_seatS-130th/tools/kint_anc_s130.sh read whole | read 2026-11-27 (by the drafter)
- Pin, address, key file, runner guards | S 130th brief (regex), `kint_hostkey_s130.sh` `WANT=`, `kint_run_s130.sh` `H=`/`K=`; asserted equal by the generator | read 2026-11-27 (by the drafter)
- `secuura-anchoring`, image 3a6a53d4b268, StartedAt 2026-11-15T22:47:15.950724269Z; compose project `dev`, env file `Dev/.env` | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-26_seatS-126th/evidence/box_ps_s126.out 5, 42; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-27_seatD-88th/HANDOVER.md 7, 59 | read 2026-11-27 (by the drafter)
- Koios preview endpoint, no-key tier, limits, `tx_info` body | https://api.koios.rest/koiosapi.yaml (293254 bytes, sha256 86e8e9a8c83d091d50f9950da5be77de2448c2193644808bc6a26b56dce9cf07) lines 147-153, 128-139, 3372-3410 | read 2026-11-27 (by the drafter)
- Koios behaviour (tip 4899218, abs_slot 129098820; magic "2"; positive control found; made-up hash HTTP 200 `[]`) | the drafter's own `curl` calls to preview.koios.rest only; `date -u` printed 2026-11-27T04:47:25Z at the tip read | read 2026-11-27 (by the drafter)
- Kit sha256, bytes, edit counts; cfg tool and SQL tests | `shasum -a 256`, `wc -c`, a python counter over non-history lines of /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-27_seatS-130th/tools/; stub `docker`; local PostgreSQL 15.19 (127.0.0.1, scratchpad, stopped after, three synthetic data sets) | read 2026-11-27 (by the drafter)
- Ordinals 0 / 1 / 1; history top is Seat W 78th's | `/usr/bin/grep -o -i -c`, `sed -n 1,3p` over history.md | read 2026-11-27 (by the drafter)
- Her ruling that the 10 hashes MAY leave the box; the three-leg design | carried from Wednesday's commission, unread by the drafter | read 2026-11-27 (by the drafter)

UNMEASURED by the drafter (you measure): everything on Kintsugi: host key, REVISION head, whether `anchor_store` there has the five G3 columns with G3's types, the container's env, compose line and env file, the 10 rows' blocks, slots and timings, and whether any hash exists on preview.

DRAFTER'S OWN CHECK (kept): re-read end-to-end for contradictions | by the drafter at drafting | pin and address asserted equal to S 130th's brief and tools by the generator; stuck total, REVISION head, verdict-line shape, tool names and licence names agree wherever repeated; the hash rule (only `hashes_s131.out` and the lookup files; ordinals in mail) agrees in HOLDS, R7, 5 and the wrap.

## STAMP (Wednesday fills)
STAMP (Wednesday, 2026-11-27 16:04:05 AEDT, brief read WHOLE with the Read tool, 223 lines; gate 421's verdict read WHOLE by Wednesday today; no product code read by Wednesday). RULINGS, Wednesday's own: **W1 YES, S131-ENVKEY is licensed**: the ONE key ANCHORING_DEMO_MODE from the box env file, its value and the two counts and the mtime, exactly as block A4 prints them; no other line of that file by any command. **W2 YES, S131-LOGCOUNT is licensed**: the four counts of block A5, counts only; a 0 after log rotation is reported as not evidence. **W3 PROCEED**: the 10 transaction hashes may go to Koios preview from your Mac, in one POST, and nowhere else; the concern about a mock-derived hash is accepted as low (one-way, and the payload is what an anchor publishes by design). **W4 YES**: ordinals in mail, never a hash; the one exempt file is evidence/hashes_s131.out plus your leg-C request and response files, which stay in your REC. **W5**: Seat W 78th is WRAPPED and its pane is CLOSED (closed by Wednesday today). A NEW build seat, Seat W 79th, lane -W, is LIVE on the same project and SHARES YOUR INBOX: it works only in its own trees and touches no box; act only on mail naming (Seat S 131st); it may add a history entry at its wrap, so re-read history.md's top just before adding yours, as R5 says. **W6 AS DRAFTED** (the STOP list; DEMO_MODE reading true with the rest clean is reported prominently, not a STOP). **W7 ACCEPT** (n from 1; the magnitude test beside the modulus). **W8 ACCEPT** (Koios preview only; if it fails you ASK). **W9 ACCEPT** (the delta instrument). **W10**: your verdict is a precondition reading for Wednesday, who decides what it opens; you propose nothing about the repair. ONE ADDITION by Wednesday: your FIRST item in the plan QUESTION is the list of facts in THIS brief you measured as wrong. Open points as the drafter wrote them, kept for the record:
- **W1 (S131-ENVKEY; relaxes S 130th's "no env-file read"):** read ONE key, `ANCHORING_DEMO_MODE`, from the box env file (value, plus mtime)? Recommend YES: A2 shows the effective value, the file what the next start applies. If NO, delete A4.
- **W2 (S131-LOGCOUNT):** COUNTS of two boot-log lines? Recommend YES: the only view of what the process did since 2026-11-15; rotation can make a 0 meaningless (the brief says so).
- **W3 (the 10 hashes leave the box; one concern):** a real hash is public chain data. A MOCK row's "hash" is `sha256('mock-tx:' + anchor payload + ':' + counter)`, technically derived from payload; that payload is what a real anchor puts on chain by design and the hash is one-way, so risk is low. Koios learns this Mac's IP asked (test network). Recommend PROCEED.
- **W4:** mail carries ordinals, never hashes; R7's 64-hex rule has one exempt file. Recommend YES.
- **W5 (R5):** is Seat W 78th (history top at drafting, the repair builder) closed? Recommend you state it here.
- **W6 (STOP rule):** STOP on a hash not found, M above 0, a block at or above 10,500,000, a failed control, a pin or REVISION mismatch, or a stuck total other than 10; `DEMO_MODE now: true` with the rest clean is REPORTED. Recommend as drafted.
- **W7 (pattern):** n >= 1 (first mock block 10,500,047), not the commission's n >= 0, with `block_ge_10_5m` beside the modulus (live preview tip 4,899,218); M is the modulus count. Recommend ACCEPT.
- **W8 (endpoint):** Koios preview is the only keyless documented preview API found; if it fails the seat asks, not sends hashes elsewhere. Recommend ACCEPT.
- **W9 (instrument):** S 130th's proof, guards, QA and before/after kept byte for byte, QB/QC/POS/CERTS dropped; new SQL only G3, BA, BB, BN, M1, TX (a whole-table block comparison was prototyped, left out to stay lean). Recommend ACCEPT.
- **W10 (what the verdict opens):** a precondition for G421-1, not the repair. Recommend: pass it to the repair builder and next gate only if all three legs support "real"; else hold the Kintsugi apply.

SELF-CHECK: re-read end-to-end for contradictions | 2026-11-27 16:04
