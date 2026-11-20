# FOR RECORDS: gate B1824, OXPd 2, WP1.1 the local secret store, round 2 of 2, head bf1a4a2, GO WITH FINDINGS

Carried forward from the round-1 file (`2026-11-20_B1809_verify/FOR-RECORDS.md`), marked with what round 2 closed, plus what
this gate found. Nothing here is decided by this gate; every open point is marked decided by nobody.

## 1. State of the lane

- Branch `b1789/wp11-local-secret-store` at `bf1a4a24492f7849705e48cbc1d4938e15f30c56`, two commits on main `7bf37526`; main is
  now `c56f3f3b`. Hosted run `44827089866` of the head: four jobs success. No pull request yet.
- **It cannot land as it is:** a merge with main conflicts in `Datasec.Suite.slnx`. One more commit (the solution file only)
  is owed, by a seat, after the print lane and the card decoders land; then a delta check of that commit; then the landing
  of `landing.txt`. The gate made no commit.
- The server does not use the store: nothing here protects a value of the server today.

## 2. Round-1 findings: what round 2 closed

| Round-1 finding | State at bf1a4a2 |
|---|---|
| 1 Blocker (ring checked at start only) | CLOSED (gate's rows: running 4 of 4 refused; emptied ring refused; linked keys folder refused; key source switch refused; refresh refused) |
| 2 Major (unprotected key planted) | CLOSED on both legs for that key; the Windows variant is new finding N1 below |
| 3 rollback, unread headers | headers CLOSED (D11); rollback, `Delete` then `Put`, another root: NAMED limits, true |
| 4 guard on `RevokeOlderKeys` | CLOSED (guard and overload); a mixed-records cell owed (N7) |
| 5 `Rewrap` does not name failures; `ListNames` fails whole | OPEN, backlog (builder's line 1) |
| 6 pipes, folders, modes, sizes, links | CLOSED; a pipe swapped in after the look is NAMED |
| 7 the key file | NAMED limits (link window, no owner check, hard link, linked parent, folder others can write, zero bytes) |
| 8 surviving mutants | CLOSED (all 17 killed or text gone) |
| 9 Windows default descriptor | ANSWERED: refused on the hosted runner; NAMED limit |
| 10 the value cipher | OPEN, records (AES-256-CBC + HMAC-SHA256, unchanged) |
| 11 two stores on one partition | one README sentence and R13 (a store that runs on while another rotates refuses writes); a lock between processes OPEN, backlog |
| 12 temporary files never removed | OPEN, backlog; now also the repository's `.writing` files in `keys/` |
| 13 solution file order | CLOSED (block SLNX) |
| 14 text items (control numbers in test names, "component C15", "WP1.1") | OPEN, records; the root README still lists `src/Datasec.Suite.Secrets` under reserved names: the one README pass after the wave |
| 15 STATUS sentence on the header check | CORRECTED (STATUS, CORRECTIONS; `SecretRecord.KeyId` now checks the header) |

## 3. New findings of this gate (all Minor, none blocking; VERDICT.md)

1. **N1 Windows: a key planted under DPAPI-NG to a rule the store's account opens is accepted** and can become the write key
   at the next start; the planter knows its master key. DPAPI-NG does not authenticate who protected an entry; the store
   compares no rule. Owed: one README Limits sentence and the class summary's limits, at the latest with the host wiring;
   the installer sets an owner-only access list on the root (runbook line); backlog: compare each entry's rule with the
   configured one. DERIVED; UNMEASURED on Windows.
2. **N2** `RotateKey` can throw after its new key is written (the README's "none throws after its write succeeded" is
   untrue there). README sentence or a pre-check.
3. **N3** A partition folder that is a link is not refused; the store chmods its target to 700 and writes there.
4. **N4** A hard link in `keys/` has its target's mode set to 600 by the start.
5. **N5** The record folder is link-checked at the start only.
6. **N6** A clone of the store's own entry under a new id with the newest date becomes the write key at the next start, with
   an algorithm the cloner chose from the library's set; the master key stays secret.
7. **N7** Cells owed: a revocation alone with no record refuses (mutant n6 survives); the guard with a mixed set of records
   (n13 survives). Survivors that need concurrency or a crash to show: the per-record light check of `Rewrap`, the length
   re-check after an open, the repository's temporary file and move.
8. **N8** A ring left by the round-1 head carries 90-day keys; with generation off a single expired key stops writes. No such
   ring exists.

## 4. Backlog lines the builder proposes (its FOR TUESDAY "Backlog lines"; not written by it), with the gate's word

1. `Rewrap` names the records it failed on; `ListNames` fails whole on one unreadable record. Keep.
2. The value cipher. Keep (open point 3 below).
3. A lock between processes over one partition. Keep.
4. Temporary files of an interrupted write are never removed (records and `keys/`). Keep.
5. The text items of round-1 finding 14. Keep.
6. Two checks with no separating cell (the direct-child rule; the full check at the top of `RotateKey`). Keep; add the
   gate's n7/n8 and n4/n18 pairs.
7. The key file's owner check and its link window. Keep.
8. A time bound for a pipe swapped in at a record's path. Keep.
9. The repository's write and a move onto an open file on Windows: UNMEASURED until a Windows cell runs it. Keep.
10. (gate) N1 to N6 as above.

## 5. Open points for the project's master list (each decided by nobody)

1. **The key lifetime:** keys now last 36500 days and end only by rotation (forced by generation off; the gate's spike g3).
   Whether a key should ever end by time is a product question.
2. **The value limit of 1 MiB** and the words a caller reads: the reason names `StorageFailed`, `ValueTooLarge`,
   `RecordsUnderOlderKeys`, their fixed messages, the parameter name `abandonRecordsUnderOlderKeys` (a public API).
3. **The value cipher** (AES-256-CBC with HMAC-SHA256, the library's default) against naming AES-256-GCM for values too.
4. **The DPAPI-NG descriptor** for a stand-alone Windows node and for the pair: the default was refused on the hosted runner;
   and, with N1, who may write the key folder on Windows.
5. **What "sealed" means for the Linux key file**, and what performs the sealing (carried from round 1).
6. **Rollback:** nothing stops an older record of the same name being put back (named limit; carried).

## 6. What is left of WP1.1 after this lane (carried from round 1, unchanged)

The device registry; the state database, its entities and migrations; a database-backed record store; the clock checks; the
wiring of the store into the server host; the Key Vault provider; a sealed key; escrow; the rotation screens of the admin
console.

## 7. For the kits that follow

- The resolution commit of this lane touches `Datasec.Suite.slnx` only; its expected bytes are in `landing.txt` step 0 (b1 to
  b3), by ordinal order of the Path values.
- A gate commission that names scratch folders: this gate used `/private/tmp/b1824-gate/` as its brief from the commissioner
  said (the commission's own text names `/private/tmp/b1819-gate/`, another review's folder).
- The workspace hook refuses git write verbs outside the session scratchpad: a gate's merge measurement runs there.
