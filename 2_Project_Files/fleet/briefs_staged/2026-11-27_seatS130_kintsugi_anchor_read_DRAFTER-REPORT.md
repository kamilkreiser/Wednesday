# DRAFTER REPORT: Seat S 130th brief (Kintsugi anchor read)

Brief: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-27_seatS130_kintsugi_anchor_read.md. Drafted 2026-11-27 (machine clock Fri 27 Nov 2026 12:30:18 AEDT / 01:30:18 UTC when I last read `date`). I touched no Secuura host (no ssh, no keyscan, no HTTP, no database on any box). Only local work: reads, one `decision_queue.sh show` (read verb), and a throwaway local PostgreSQL 15 in my scratchpad (started, tested, stopped; data left there).

## COMMISSION FACTS I MEASURED AS WRONG (or overstated)
1. **"Kintsugi documents grew to 151 total since [S 127th's 105]" is wrong.** 151 is not growth since S 127th: S 125th read documents=151 at 2026-11-25T19:26:55Z (quoted in S 127th's brief PROVENANCE), S 127th read 151 at 2026-11-25T23:06:36Z (box_cnt_s127.out line 13), D 88th read 151 today (D88 q_plan line 31). The 105 is a SUBSET: document-class rows with a confirmed blob and a tx hash (98 + 7 in the bucket table, box_cnt_s127.out lines 49 and 54). The growth 76 -> 151 happened on 2026-11-24 (72 rows 13:02-14:41Z) and 2026-11-25 07:18-07:19Z (3 rows), BEFORE S 127th's count (D88 q_plan line 31). The brief says so.
2. **"Seat S 129th made on demo an hour ago":** S 129th's box reads ran 01:08:47Z to 01:08:49Z (S129_status_number.txt line 6); at my last `date` it was 01:30Z, so about 22 minutes. Immaterial to the brief; noted because the clock is the evidence.
3. **"D 88th's KS-535 line `network preview`":** that exact string is NOT on D 88th's mail line. D88 q_plan line 28 reads "... blockfrost <sha16>, preview, simulate UNSET; ...". The string "network preview" is printed by D 88th's tool ks535_ro_d88.sh line 65 (`echo "KS535 OK ... network preview, simulate unset"`). The brief cites both, quoting the mail line as "preview, simulate UNSET".
4. **"Kintsugi's anchor_store census by (status, simulated) has NOT been read by anyone you can cite":** right for (status, simulated), overstated as a whole. D 88th's `nonfinal` tool read Kintsugi's `anchor_store`: 166 rows in total, 0 outside confirmed and failed (nonfinal_d88.sh lines 88-90; D88_status_b.txt lines 12 and 17). No confirmed/failed split, no simulated split. The brief cites that as the only record and gives NO expected census values.
5. **"Kintsugi's container, user and database may differ from demo's `secuura-postgres` / `secuura`":** the container name does NOT differ (`secuura-postgres`, box_cnt_s127.sh line 10, box_ps_s126.out). The real difference: S 129th's demo tool hard-codes `-d secuura` (demo_anc_s129.sh line 14) and its 3a pattern hard-codes `on|secuura|...` (line 32), while S 127th's Kintsugi `q()` uses `-d "$POSTGRES_DB"` and user `$POSTGRES_USER`, both from the container's env, never printed. Kintsugi's database NAME is not in any record I could find (compose default is `secuura`, docker-compose.yml lines 135 and 280). Copying S 129th's tool unedited would have hard-wired an unverified name and STOPPED at 3a if it differs.
6. **"S 127th's ... host-key pin step and hostname guard" in box_cnt_s127.sh:** the hostname guard is there (line 6); the pin step is NOT in that file. It is in boxrun_s127.sh lines 49-51 (strict known_hosts) and in the keyscan record pin_s127.out. The brief cites those.
7. Nothing else found wrong: S 127th's 10/1/0, D 88th's re-read, REVISION head 4764b2cfbc28 (k46), originate image ca145807416e, container 6962a608cf42, TimeZone UTC, the pin and address, the guard name, the decision card BLUF sentence and ruling all read as the commission says. Ordinal: 'seat s 130th' 0, 129th 1, 128th 1, 127th 1 (history top entry is D 88th's). An OLDER series `briefs_staged/s130_*.md` (four files) exists, a different lane; the brief says so.

## FACTS IN THE BRIEF (fact | source | read today?)
| fact | source | read today |
|---|---|---|
| Card BLUF sentence, default line, option a detail, `choice='a'`, ruled_ts 11:44:49.881596+11:00 | command read: bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show secuura-ks2366-stuck-certs-anchor-read-demo-1127 | yes |
| Standing delegation (dev/staging/test reads are Wednesday's) | commission text only; delegation file not located | no (stated, not read) |
| 10 submitted, 1 failed, 0 confirmed; oldest 2026-09-17, newest 2026-11-16; failed 2026-10-21; 105 confirmed document rows; documents 151; `on|t|t`; box time 2026-11-25T23:06:36Z | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-26_seatS-127th/evidence/box_cnt_s127.out lines 2, 7, 13, 43-54, 57 | yes |
| 105 stated in the status | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-26_S127_status.txt line 23 | yes |
| Kintsugi psql mechanism and hostname guard | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-26_seatS-127th/tools/box_cnt_s127.sh lines 6, 10 | yes |
| Key file name, user, address, pin history (Seat A 25th) | boxrun_s127.sh lines 43-51 (same folder), pin_s127.out line 4 | yes |
| D 88th keyscan equals the pin | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-27_D88_q_plan.txt line 21 | yes |
| REVISION head 4764b2cfbc28 (k46), originate ca145807416e, container started 2026-11-27T00:59:44.440Z | D88_status_b.txt lines 12, 18 | yes |
| Container id 6962a608cf42 | D88_status_b.txt / D88_status_c.txt (named in the commission and in history top entry; the id tool's inspect format does not print it, so the brief reports the image only) | yes |
| 10/1/0 identical before and after the one live request; TimeZone UTC | D88_status_c.txt lines 9, 15; D88_q_plan.txt line 32 | yes |
| anchor_store total 166, 0 non-final | D88_status_b.txt lines 12, 17; nonfinal_d88.sh lines 88-90 | yes |
| Kintsugi preview network | D88_q_plan.txt line 28; ks535_ro_d88.sh line 65 | yes |
| REVISION path /home/secuura/secuura/Dev/REVISION on Kintsugi | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-26_seatS-125th/tools/box_rev_s125.sh line 7 | yes |
| One `-postgres` container name (`secuura-postgres`; the other database-ish name is `secuura-pgbouncer`) | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-26_seatS-126th/evidence/box_ps_s126.out | yes (a 2026-11-25 record) |
| Line 1 of the Kintsugi REVISION file is `revision=...` | inferred from D88_status_b.txt line 18 ("head-1 assertion PASS"); S 129th's id logic reads `head -n 1` | partly (inferred) |
| S 129th result 36 of 37, link 37/37, controls | S129_status_number.txt lines 8-45 | yes |
| S 129th kit hashes and sizes; edit counts | command read: shasum -a 256, wc -c, python counter over non-history lines of /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-27_seatS-129th/tools/ | yes |
| S 129th plan mail holds both instruments verbatim (lines 163-254 SQL) | S129_q_plan.txt | yes |
| Ordinals 0 / 1 / 1 / 1 | command read: /usr/bin/grep -o -i -c over history.md | yes |
| CERTS statement and 3a case pattern parse and give the expected rows on synthetic data | command read in my scratchpad, local PostgreSQL 15 | yes (proves parse only) |
| D 88th wrapped (history entry on top; WRAP ruled) | history.md top entry | yes |

## COUNTED EDITS TO THE S 129th KIT (all counts on non-history lines, computed 2026-11-27)
Runner `demo_run_s129.sh`: s129 3; REC 1; scratchpad 1; key name 1; address 1; hostname 2; `demo_` 4; `not a demo remote script` 1. Hostkey: s129 7; REC 1; scratchpad 1; `demo_` 8; address 1; pin 1; `AA 6th's recorded` 1. Id: hostname 2; box text 1; ID_S129 1; revision token 2; reading text 1; `secuura-anchoring` 1; `anchoring container` 1; lines 24-25 replaced by one report line (removes 3 image tokens, 2 `anchoring`). Mail: 1, 4, 4.
Anchor tool `demo_anc_s129.sh` (the SQL itself is byte for byte, only these):
- host guard 1 + 1; `-d secuura` -> `-d "$POSTGRES_DB"` 1; 3a pattern 1 (+ its message 1); census awk block (lines 44-49) replaced by a report line 1;
- **expected stuck total 37 -> 10 : 5** (lines 177-179: `-ge`, `below`, `-gt`, `above`, `= 37`) and `STAMP W4` -> `BRIEF R3` : 2;
- **created_after literal `2026-11-27 00:29:56+00` -> `2026-11-25 23:06:36+00` : 1; column `created_after_s128_count` -> `created_after_s127_count` : 4;**
- **positive-control floor 155 -> 105 : 3** (line 241);
- made-up tokens and probes `s129` -> `s130` : 7 (after replacing comment line 55 with a `# LINEAGE` line, which carries the other 2 of the 9); `Seat S 129th` -> `Seat S 130th` : 1;
- ADDED (the only new SQL): the CERTS certification census statement and one report-only shape check; schema guards stay 12 and 10 unchanged.
Stale-check tokens: `demo` (any case), `129th`, `s129`, `s128`, `296`, and the demo address and pin read from the source files by the script (the brief does not repeat them, per the commission).

## NOT MEASURED
- Everything on Kintsugi (nothing contacted): host key today, REVISION line 1, database name, `anchor_store` columns `document_id` and `simulated` and all data types (D 88th's tools read id, status, transaction_hash, created_at, updated_at, simulated only), the (status, simulated) census, whether the 10 stuck blobs carry `anchorId`, whether either key reaches an anchor row, whether `match_by_external_id` is above 0 for the 105 document rows (a STOP under R8 if 0), whether the 10 moved since D 88th's last read, five-field 3a value of field 5.
- The k46 originate sources (objects not read): whether the new certification-anchor poller can move an old stuck row. This is why a total below 10 is a STOP.
- The delegation file (cited from the commission only).
- Container id 6962a608cf42 is not checkable by the id tool's inspect format (it prints name, image, state, StartedAt); the StartedAt is in the brief as the cross-check.
- I did not run the full S 129th tool locally; only the new CERTS statement and the case pattern.

## QUESTIONS FOR WEDNESDAY
1. **Database name (3a).** I replaced S 129th's hard-coded `secuura` with `"$POSTGRES_DB"` and made 3a accept any non-empty name, REPORTING it. Alternative: hold the seat to a strict `secuura` and let a different name STOP it. Which?
2. **I3 originate image is REPORT-only, not a STOP** (the REVISION head is the identity). OK, or do you want the originate image `ca145807416e` as a STOP too?
3. **CERTS is new SQL** (not byte for byte): needed because the QA only counts the stuck class, while the commission wants the 10 / 1 / 0 identity. S 127th's S3 statement would have done it but carries the default-tenant uuid constant, which R7 forbids in evidence. OK to ship CERTS?
4. **R7 and 64-hex:** I restricted the "no 64-hex" rule to box-output evidence and the numbers STATUS/wrap, because the plan mail must carry full kit sha256 (S 129th's did). Agree?
5. **Authority cite:** the brief quotes the card and says "standing delegation" from your commission, no file. Do you want a path to the delegation text inserted before you stamp?
6. **Timing:** D 88th's pane may still be live and shares the inbox; the brief carries S 129th's R5 unchanged. Should this seat wait for D 88th's pane to close, or run alongside as written?
