# Gateset 2026-09-25_gate21T2b — README for Wednesday (the drafter launched NOTHING, sent NOTHING, tapped NOTHING, committed NOTHING, wrote nothing outside this directory)

ONE TIER-2 batch gate, round 21 (the SECOND tier-2 batch), round 1 of 2, over FIVE PRs (FROZEN at five by Wednesday), BASE `6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7`,
pinned launch develop `379c6eb1d45905f398fae67ee7dd2f46ad40432f` (7 past BASE):
**#1225 KS-1291** `120420a2e7b1a0d10dd41ee4320f7e88bc1529c6` (L1, originate route handler, a dead guard removed; legs 3/4/8 OWED) ·
**#1227 KS-1252+KS-1253** `69a72726e8eee0711a56b782d04936bf647e9160` (L4, a checker plus a new suite; 2 commits) ·
**#1229 KS-865+KS-808(3)** `ed85bd81d0acb137c89e1257d05ef9c72855086b` (L4, a checker plus runner text plus a new suite; 2 commits) ·
**#1231 KS-1281** `bd1d2daec2bf1b934437eae19c6239fe257305a6` (B25, Ornith, vc-issuer) · **#1232 KS-1128** `ec0d7efcf682112639505cf45baec71b899b665f` (B25, Ornith, api-gateway).
10 paths, pairwise disjoint (10 pairs), and disjoint from develop's 17 moved paths. END_TREE `4da02cbfc8139fd1fe30c36f1930fe79f7a11960` agrees in three orders and by `apply --cached`
(`10 files changed, 523 insertions(+), 26 deletions(-)`). GO string: `GO: merge #1225, #1227, #1229, #1231, #1232 batch`. #1230 (tier 1) is NOT in this gate.
The shape is copied from the running sibling `../2026-09-25_gate21T2` (template, pins, fill, self-locating launcher, repin-and-launch derived by anchored replacement, controls).

## 1. Measured (every claim with its instrument)
- **Heads.** All five equal Wednesday's pins on four readings: `git ls-remote origin` (lsremote_1.out, 05:18:55Z), the scratch-clone fetch (predict_1/3), fill's ls-remote (fill_5.out) and the pulls API (repin_dryrun_1.out). All five are `open` and `mergeable True`.
- **Merge-base and behind.** Instrument: GitHub compare develop...head (the sibling's pattern; GH_TOKEN by name from the Secuura .env). All five show merge_base == BASE and ahead 1/2/2/1/1. Behind was 4 over ecb1aa75 (gh_read_1.out) and is 7 over 379c6eb1d (launcher_check_3.out). The files list equals each PR's own paths by name (`paths=own`).
- **BASE-INVARIANT.** Instrument: `merge-tree --write-tree` in a scratch bare clone FROM ORIGIN (predict_3.out). For each PR, `diff --name-only develop merged` == its own paths, blob-equal to the head. The same holds for the END_TREE (== the 10 paths). The launcher re-asserts the by-name compare at every run (exit 10).
- **Develop moved twice while I drafted.** ecb1aa75 (4 past BASE: #1216 #1217 #1214 #1213) became 379c6eb1d at 05:42–05:43Z, when the batch1215 gate's GO merged #1220, #1215 and #1222. I re-pinned (predict_2/3 then fill_3/4/5). `pins_gate21T2b.txt.pre-ecb1aa75` is kept. Neither move touches the 10 paths, and no moved path is named by any batch test file (predict_3 (l)). **Develop will move again** when #1218, #1221 and #1223 merge. The repin script's step 3b re-pins in the launch action; that path is controlled by R3 but was not run end to end.
- **Linear** (linear_reads_1.out, queries only): each PR attaches exactly its own key(s), `contributes`, all In Progress. KS-1252 and KS-1253 are unassigned.
- **Docker** at 05:27:58Z (stackstate_1.out): `docker info` rc 1, `docker ps` answered HTTP 500, and the first call hung for more than 120 s. No stack was up. #1225's legs are expected to stay OWED.
- **login_stub census** at 05:3xZ: 8 live, all foreign (4 `s-b25-audit`, 4 `s-l4-ks1127`, ppid 1). Source: `systemTest/__tests__/bootstrap_login_diagnosis.test.sh`, run by `run-shell-suites.sh`. It sits at repo root, outside Blockchain/Dev, which is why a Blockchain/Dev-only grep reads 0.

## 2. Things Wednesday should know or decide
1. **Your added #1231 MEMORY FALLBACK rule is in** (the prompt, launcher exit 37, controls X3/X4). It was added at your request mid-draft because a DB not built by migration 001 "falls back to memory on first store", a potential SILENT DATA LOSS path for issued VCs (gone at restart). The gate must establish real-path reach (compose/bicep/kintsugi, or UNMEASURED), establish loud vs silent, and grade a silent, reachable fallback as BLOCKING for a tier-2 GO. My read (READ ONLY) pre-loaded in the prompt:
   - The table-absent path #1231 changes is LOUD: two `warn`s, one naming the table.
   - `store()` also has `if (!isDbAvailable()) return;` after the memory write, with no log. It is identical at BASE :54 (and the same shape at :211), so #1231 did not introduce it.
   - Your rule reads literally on it if that path is reachable. I told the gate to report it separately and to NOT fold it into or out of #1231's verdict. **Your call** whether a pre-existing silent path blocks #1231.
   - Reach pointers: compose mounts `docker/init` as `docker-entrypoint-initdb.d` (runs only on an EMPTY volume); Azure `migrate/run.sh` runs init.sql with `ON_ERROR_STOP=0`.
2. **Two checkers.** #1227 (E7 guard) and #1229 (check-no-latest-tags) are checkers, so the prompt carries §2a LEGITIMATE SHAPES tables (drafter-predicted). Notable row: enumerate the product's own minted `<prefix>_<uuid>` prefixes against the fourteen new exact prefixes (`invite_`, `reset_`, `access_`, `nonce_` …). I did NOT enumerate them myself.
3. **#1231 substrate.** `vc_credentials_store` is created by THREE schema sources (migrations/001:745, docker/init/03-service-tables.sql:135, deployment/azure/migrate/init.sql:779). The gate is told to compare them and not reconcile them. The least-privilege SELECT is UNMEASURED by construction, because the gate may never connect to a DB port. The head's docblock still says "(auto-created)".
4. **Foreign keys in bodies (MG-3).** #1229's body names **KS-318, which is Done and ARCHIVED**, hyphenated. It did NOT attach (attachmentsForURL shows 2, own keys only), but a squash body that keeps it risks the archived-key case. #1225's body names KS-1155, KS-1265 and KS-1277; #1229's names KS-1031 and KS-897. The squash bodies must drop or un-hyphenate them.
5. **MG-11.** Titles are 95 / 132 / 182 / 69 / 75 chars; #1225, #1227 and #1229 exceed 92 and need shorter squash subjects.
6. **Small claim slips for the gate to grade.** #1229's READY says "the single remaining mention" of BACKLOG, but I count 3 comment lines (:159/:160/:165) and 0 echo lines. #1232's body says both "918/918" and "re-run once, 920/920" for packages/shared. Leg 14 on the END_TREE is predicted at 59 (each READY measured its own 58).
7. **Not in this batch.** #1230 KS-1131 (tier 1). KS-1140 GF-1 and KS-1110 (your ks1110shape answer queued them for "the next tier-2 batch"; the batch was frozen at five without them). L4's tier-1 PR 2 (6320a61d8).

## 3. Controls — `controls_gate21T2b.sh` on the FINAL kit -> `controls_3.out`: 46 OK / 0 MISMATCH (rc 0, 06:13–06:27Z)
Every arm runs `--check` (or a `--dry-run`) against a doctored copy under `_sp/`. Each doctored phrase sits outside the by-name ladder and the BOTH list, and `doctor` asserts its anchor. The doctored arms pin `QAB1225_CUR_DEV` to the pinned develop so a live develop move cannot mask the rule under test. P and D use real origin reads.

| arm | fault planted | want | arm | fault planted | want |
|---|---|---|---|---|---|
| P | none (real reads) | 0 | P2 | none, develop pinned | 0 |
| F3 | capture missing | 3 | F4 | prompt missing | 4 |
| C | stale #1232 head | 6 | D | develop moved | 17 |
| Q | compare behind wrong | 10 | G | no `ultrathink` | 8 |
| U | unfilled `{{…}}` | 8 | W | capture lacks #1232 head | 20 |
| O | capture lacks a seat item | 30 | T | ticket statement | 32 |
| I | tier line | 7 | L | by-name keyword | 33 |
| K/K2/K3/K4 | legs rule ×4 (stack not ours; SKIP≠pass; OWED≠green; never start Docker) | 35 | B/B2 | red-proof; #1225 removal proof | 36 |
| X/X2 | substrate UNMEASURED; fallback check | 37 | X3/X4 | MEMORY FALLBACK blocks; verdict clause | 37 |
| Y/Y2/Y3 | load; fake pg only; `:1142` catch | 38 | H | holds | 39 |
| N/N2 | narrowing len12/credit; KS-1253 open | 40 | S1/S2 | login_stub cwd+ppid; counts | 41 |
| V | legitimate shapes | 42 | A | GO string | 26 |
| E | addendum 1/2/3/2/2 | 25 | SJ | subject | 23 |
| Z | END_TREE in full | 31 | NT | non-TTY launch | 21 |
| M | moved launcher | 2 | R1 | repin dry run | 0 |
| R2 | stale head (repin) | 11 | R3 | pinned develop stale (repin) | 10 |
| R4 | REAL run, routing absent -> stops at step 0 | 1 | R5 | bad scratchpad | 9 |
| R7 | no launcher | 9 | R6 | moved-kit dry run (MOVED KIT ×1) | 0 |

Earlier runs:
- controls_2.out: 44 OK / 0 MISMATCH on the kit before your rule.
- quarantine/controls_1.INVALIDATED-develop-moved.out: develop moved during that run, so every arm hit exit 17 first. It measured nothing about the rules; kept, not counted.
- Moved kit: an rsync copy re-fills at its new home (movedkit_fill_1.out rc 0) and passes `--check` there (movedkit_check_1.out rc 0).

**NOT controlled:**
- exit 16 (overrides at launch). Reaching it needs a TTY, and a faulty arm would exec claude, so I did not risk it.
- exit 2 (QA project missing) and exit 5 (repo missing). There is no override for either.
- The repin's `mergeable=False` refusal. There is no override, and all five read True live.
- The real launch path.

## 4. The routing line — NOT WRITTEN: add it FIRST (`PROPOSED_inbox_routing_line.txt`)
    QA/Secuura-batch1225|coagent@agentmail.to|yes
My read: batch1225 absent (0); the control batch1215 is present (1). Step 0 of the repin refuses rc 1 without it (control R4).

## 5. The exact launch command (copy + re-pin + launch; from a shell that can reach tmux)
    /usr/bin/rsync -a --exclude '_sp' /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/fa11cd0d-1030-4620-83ac-40d313b499eb/scratchpad/gate21T2b/ /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T2b/ && /bin/bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T2b/repin_and_launch_gate21T2b.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T2b/launch_qa_secuura_batch1225-t2.sh <your session scratchpad under /private/tmp/claude-501/>

Steps: 0 routing (1) · 0b moved kit -> re-fill here (8) · 1 ls-remote (2) · 2 pulls API + mergeable (3) · 3 heads == pins, open, not mergeable=False (11) · 3b develop moved -> predict + fill in the same action (10) · 4 usage gate (12) · 5 `--check` (13) · 6 `cockpit.sh add QA/Secuura-batch1225 <launcher>` (14). Append `--dry-run` to rehearse steps 0–3 (repin_dryrun_1.out rc 0; repin_dryrun_2.out rc 0 on the final kit, 06:27:22Z, develop unmoved).

## 6. Files
- Kit: COMMISSION.md · README.md · PROPOSED_inbox_routing_line.txt · prompt_gate21T2b.TEMPLATE.txt · launcher_gate21T2b.TEMPLATE.sh.txt · fill_gate21T2b.py · the rendered `2026-09-25_secuura-batch1225-t2.prompt.txt` (fill_5: 451 lines, 59449 B; its sha256 changes with the home path) and `launch_qa_secuura_batch1225-t2.sh` (261 lines, mode 755, `bash -n` rc 0) · derive_repin_gate21T2b.py -> repin_and_launch_gate21T2b.sh · controls_gate21T2b.sh.
- Instruments: lsremote_1.out · gh_read_gate21T2b.py + gh_read_1.out + gh_body_* + gh_comments_* · capture_mail_gate21T2b.py + capture_list*.out + capture_1.out (rc 0; 4 READY sections, all 7 keys) + 50 mail_*.md + the combined mail_gate21T2b_ready.md · linear_reads_* · predict_gate21T2b.py + predict_1..3.out (all rc 0, 0 hard fails) + pins/devlog (+ .pre-ecb1aa75) · stackstate_1.out.
- Records: fill_1..5 (fill_1 rc 8 — a BOTH token line-broken in the capture, fixed) · launcher_check_1..3 · repin_dryrun_* · controls_2/3 · movedkit_* · launch_061301.routing.out (written by control R4's real run).
- Kept, not deleted: `.pre-*` copies, quarantine/, and `_sp/` (the scratch clones, ~520 MB, which the launch command excludes).

## 7. NOT done / NOT measured
- No launch, mail, tap, commit, push or routing-conf write.
- The Secuura checkout was touched with `ls-remote` and `config --get` only. Every git write verb ran in scratch clones FROM ORIGIN under `_sp/`.
- Mail was read by API GET only; inbox_digest.sh was not used.
- Not pre-run (the gate's job): any suite, tsc, red proof, canary, probe, `npm ci`.
- UNMEASURED:
  - whether a stack will be up at launch;
  - the minted-prefix enumeration for #1227;
  - every environment check-no-latest-tags.sh runs in;
  - the vc_credentials_store DDL agreement across the three sources;
  - whether any real deployment reaches #1231's fallback;
  - the least-privilege SELECT;
  - the usage gate's state and the machine load at launch;
  - the repin step-3b develop-moved branch end to end.
