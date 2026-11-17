VERDICT: GO WITH NOTES — head afc24720f033db6295a0d0b8016a4365aa850b91

# Gate M1 RELAY-IDENTITY round 2: independent tier-1 QA (findings only, nothing fixed, nothing merged)

Branch `m1-relay-identity`. `git rev-parse HEAD` on a fresh clone gives `afc24720f033…`, and
`git ls-remote origin` gives `afc24720f033db6295a0d0b8016a4365aa850b91 refs/heads/m1-relay-identity`. Both match the
head stated in STATUS. Round 1 was at `e143847`. The base `main` and `origin/main` are both `18005d6`. The clone,
worktrees, builds and every probe ran in the gate's scratch folder. Nothing was pushed, and no git write verb was run
inside `!CODING/`. Every relay the gate started listened on 127.0.0.1 with an ephemeral port. One bind-failure probe
used a 127.0.0.1 port the driver itself took from the OS. Every non-loopback probe was refused before any bind: none
printed `url:`, all exited 1 within 0.00–0.01 s, and none used `--allow-non-loopback`. Tests and drivers are in
`gate_relay_identity_tests_r2/` (sources plus sanitised small logs; no identity file, no key, no build output).

**Why GO WITH NOTES, in one paragraph.** Every round-1 finding is closed or was changed as the owner ruled, and every
re-attack held. Round 1's every-byte flip found 642 changed certificates loading under a new fingerprint. Over 66,824
changes of v3 blobs the gate now sees 0. Standard input is now consumed to exactly 16,385 bytes at the descriptor. A
refused non-loopback start creates no file. The four formerly unguarded checks now go red when removed. The cleanup
routine never followed a link, never removed a directory, FIFO or foreign-moded file, never touched a near-miss name,
and never damaged the content behind a hard link, including under a 200-start race. 320 random kills plus clean
starts left 0 leftovers. The macOS ACL text (F1) is true and pinned by a text test. No ACL code, no dependency and no
`unsafe` was added. What remains is three wording faults and a handful of test gaps:
- the cleanup deletes silently when the start is then refused, and STATUS says the opposite;
- the README says an *edited* certificate is refused, which the gate disproved by re-hashing;
- the README still calls the ACL question "open" after Kam's ruling;
- four cleanup/order checks have no test.

None of these lets a key be read by anyone who could not read it before, and none makes a joiner trust a wrong relay.
They should be fixed with the merge or in the next lane. They are not a reason to hold the merge.

## 1. Findings

| id | severity | file:line | exact sequence | RAN / REASONED |
|---|---|---|---|---|
| R2-1 | Minor | `crates/coagent-cli/src/relay_cmd.rs:111` (the "removed N" line is printed only after `load_or_create` returns Ok); `identity_file.rs:449` (cleanup runs before the load/create that may then fail); CLI README:42; STATUS A1-DQ2 | Put a valid identity at mode 0640 in a 0700 folder, plus a 0600 file `.relay.identity.tmp-1-2`. Run `coagent relay --identity-file <dir>/relay.identity`. Result: exit 1, refused for mode 0640. **The leftover is gone and no line says so** (`removed_line=[]`, `leftover kept=False`). The same happens for any refusal after the cleanup (damaged identity, create failure), and when a start is killed after the cleanup but before the print: across 160 kills, 46 left a leftover that later starts removed, but only 24 removals were reported. STATUS A1-DQ2 says the line is printed "immediately, so it is seen even if the start then fails". **That is false.** The README's "prints one line saying how many it removed" holds only for starts that succeed. The files deleted are the program's own crash leftovers, so no secret is exposed. The finding is that the most dangerous new code deletes without telling, against the ruling's "print one line". Fix: print inside `remove_leftovers` or return the count with the error; test with a refused load. | RAN (A11, kill stats) |
| R2-2 | Minor | CLI README:63 ("so a damaged or edited certificate is refused") | Take a valid v3 blob, flip one certificate byte (serial byte 15, or the last byte of the signature), then store the new SHA-256 in place of the old. Through both options this loads: `identity: saved, loaded`, a NEW fingerprint, and a client pinned to that new fingerprint completes Ping/Pong (library `r2_02` and CLI `BLOB cert serial flipped, REHASHED`). Without the re-hash it is refused (`CertificateHashMismatch`). So the hash catches accidental damage only. Anyone who can write the file can re-hash an edit, or simply drop in another identity, and the certificate's self-signature is not verified (a broken signature loads). STATUS A1.3 says the self-signature is not checked and why (RAN-consistent). The README says neither, and the word "edited" claims more than the hash gives. The relay README's "a damaged certificate never loads as a different identity" is accurate. Fix: README "damaged (not deliberately edited: the hash is not a signature)", plus one sentence that the self-signature is not verified. | RAN |
| R2-3 | Minor | CLI README:51-52; STATUS A1.2, A1.11 | Both still say "Whether to check ACLs is an open decision for the owner". Kam ruled on 2026-11-17 (`general-c2c-relay-identity-acl-1117` = a): accept it for the beta and say so plainly. The rest of the F1 text is true (§3). Only this sentence is stale: it should say the limitation is accepted for the beta. Text only. The builder wrote it before the ruling. | REASONED (read) |
| R2-4 | Minor (test gap) | `identity_file.rs:363`, `:365`, `:449`; `relay_cmd.rs:159` | Four checks hold today but no test goes red without them: **N20** (leftover owner check removed), **N21** (leftover "other" bits ignored: a 0604 leftover would be deleted instead of refusing), **N24** (cleanup moved before the parent check: a start pointed at an open folder would delete the user's matching files there before refusing), **N36** (early refusal ignores `--allow-non-loopback`, which would break hosting on a non-loopback address). Behaviour today: the gate RAN 0604 refused (A12c) and parent 0755 leaving the leftover (A8 and the F5 probe). The owner check and the allow-flag were read only, because they need another user or a non-loopback bind, both outside the gate's rules. All four are cheap to test: `remove_leftovers(path, uid + 1)` is public; a 0604 leftover; a leftover in a 0755 folder; `--listen 192.0.2.1:0 --allow-non-loopback`, which fails to bind with EADDRNOTAVAIL instead of the refusal text, so nothing listens. | RAN (mutants); REASONED (owner, allow-flag behaviour) |
| R2-5 | Note | brief and addendum vs code | The blob is **v3**, not the `v2` the addendum asked for. The builder's reason holds (verified): the gate's unchanged `g03` asserts that `coagent-relay-identity v2\n` + a current body is refused, so a literal v2 would turn that gate test red. v1 and v2 lines are refused as `UnknownVersion` (RAN, library and both options). The ruling: **SOUND.** Friday still has to say yes to A1-DQ1. | RAN |
| R2-6 | Note | `identity_file.rs:330` + APFS | The name comparison is case-sensitive, but APFS is case-insensitive. Starting with `--identity-file <dir>/RELAY.IDENTITY` loads the existing `relay.identity` (same fingerprint) but does not remove `.relay.identity.tmp-1-2`. This fails safe (the leftover is kept). Separately, `to_string_lossy` on names could make two different non-UTF-8 names collide, but APFS refuses non-UTF-8 names (`EILSEQ`, RAN). On Linux it would at most remove another identity's leftover of the same exact shape (REASONED). | RAN / REASONED |
| R2-7 | Note | `identity_file.rs` create vs cleanup | Two relays creating the same NEW path at the same moment, 30 pairs: 1 pair had both listening on the same fingerprint, 29 pairs had one refused. 25 of the refusals said "could not link the new identity file at: entity not found" because the other start's cleanup removed its in-flight temporary file. 4 said "a file appeared…". Every folder ended with exactly one valid file. The design fails closed, but the message misleads. | RAN |
| R2-8 | Note (equivalent / low) | — | Surviving mutants judged equivalent or cosmetic: N07 (a CRLF v3 header accepted: the body and hash are still exact, so harmless; `g03`'s CRLF case uses the v1 literal), N26 (cleanup removal error ignored: would over-report "removed" and leave the leftover; needs an `unlink` failure in a 0700 folder of the user's), N33 (deadline message's byte count). Round-1 equivalents G01, G11, G12, G17, G18, G22, G31, G34 are unchanged. | RAN |
| R2-9 | Note | `args.rs:20`, CLI README | "a line beginning with a number under the file": the real `ls -le` line is ` 0: group:everyone allow read`, with a leading space (RAN). Plain enough. `ls -l` of the ACL'd file shows `-rw-------@` (the `@` comes from an extended attribute, and it masks the `+` ACL marker), so "while `ls -l` still shows `-rw-------`" is true as written (RAN). | RAN |
| N6, N8 (r1) | Note | unchanged | CRLF still gets "a version this program does not know". SIGINT before the handler is installed still ends a start by the signal: rc -2 was seen in a few head runs, and N8 is on main too. | RAN |

No Blocker. No Major.

## 2. Measured totals

- **check.sh ×5 at head:** exit 0 every time; **314 passed, 0 failed, 5 ignored** every time; wall 100, 80, 69, 77, 70 s.
  This matches STATUS. The `--nocapture` run of the two gate files at head: `g02` printed "1707 mutants : refused 1707,
  accepted-same-fp 0, accepted-DIFFERENT-fp 0".
- **Red-control runner** `run.py --with-dep` (unchanged, in a scratch worktree, own target): **102 rows, 102 RED,
  0 problems**, "sources restored byte-for-byte", "red controls: ALL RED", 601 s. All 66 pre-lane rows and M80–M106
  are still RED. **Each row M80–M115 was applied alone with its own cargo args, and the panic text was captured**
  (`results/red_why.log`). Every new row fails with the text its property names:
  - M107 "a damaged certificate loaded as a different identity: byte 45 ^ 0x01 gave sha256:…" and "a certificate whose stored hash differs was accepted"
  - M108 "a leftover temporary file survived the next start"
  - M109 "group-readable: the relay listened"
  - M110 "…consumed more than the cap plus one byte…: 16386 of 16386"
  - M111 "the identity file was created before the non-loopback refusal"
  - M112 "a FIFO at the path was opened: the start blocked for 10 s"
  - M113 "the opened file was not checked again…"
  - M114 "the key was written through a planted symbolic link"
  - M115 "…Err(TooLarge { len: 16384 })"

  The re-anchored M84, M96, M97 and M98 fail with their round-1 texts.
- **Integrity:** these files have blob hashes identical to `18005d6`: the relay crate's `limits.rs`, `state.rs`,
  `frame.rs`, `meter.rs`, `server.rs`, `client.rs`, `bucket.rs`, `cut.rs`, `PROTOCOL.md`, `tests/gate_attacks.rs`,
  `tests/gate_r2_wire.rs`, `src/gate_r2_state.rs`, `src/gate_r2_meter.rs`, `Cargo.toml`; root `Cargo.toml`,
  `Cargo.lock`; `crates/coagent-cli/Cargo.toml` (the round-1 `io-std` feature line is gone again). `spikes/` diff: 0
  lines. The relay `lib.rs` change is re-export lines only. `run.py` against main: only additions and this lane's four
  re-anchors; no other seat's row was changed.
- **Gate files:** `tests/gate/gate_identity_fuzz.rs` and `tests/gate/gate_pin_client.rs` are **byte-identical** to the
  reference copies (`cmp`). The wrappers `tests/gate_identity_fuzz.rs` and `tests/gate_pin_client.rs` hold only a
  comment, `#[rustfmt::skip]`, `#[allow(clippy::all, clippy::pedantic)]` and `#[path = "gate/…"] mod gate;`.
  **Ruling: acceptable.** The allows silence lints only, not tests. Every assertion runs: 8 of 8 green inside
  check.sh, and they go red under mutants (G28 → `g03`, G33 → `g05`, G36 → `g07`). No gate line was edited.
- **Default unchanged** (main binary vs head binary, 3 starts each, empty cwd/TMPDIR/HOME in scratch):
  - Banner prefixes are identical and in the same order (`coagent relay`, `address`, `url`, `fingerprint`,
    `invite candidate`, `Press Ctrl-C…`), with no `identity:` line.
  - There are 3 distinct fingerprints per binary.
  - Nothing is left in cwd/TMPDIR/HOME.
  - `lsof` REG/DIR is the same 3 entries for both binaries (cwd, binary, dyld).
  - Exit codes for 12 usage cases are identical (2; 1 for the non-loopback refusal).
- **F4 (descriptor), standard input as a regular file shared with the driver, offset read after exit, two runs each:**

  | input size | bytes consumed |
  |---|---|
  | 16,384 | 16,384 |
  | 16,385 | 16,385 |
  | 16,386 | **16,385** |
  | 1 MiB | **16,385** |
  | 64 MiB | **16,385** |
  | a valid 570-byte blob + 100,000 junk bytes | 16,385 |
  | a valid blob alone | 570 |

  The documented bound "the cap plus one byte consumed from the descriptor" equals the measured bound. Other stdin
  measurements:
  - An endless pipe: the writer got 81,920 bytes in (64 KiB pipe buffer + 16,385), then exit 1 at 0.05 s.
  - Deadline, silent open pipe, ×5: 5.01, 5.01, 5.05, 5.02, 5.01 s.
  - A valid blob with the pipe kept open is refused at 5.04 s ("570 bytes, then no end of file").
  - `/dev/null` and a closed fd 0 are refused at once ("nothing was received").
- **F2 (blob):**
  - Library `r2_01`: 3 fresh identities × every byte × masks 0x01/0x80/0xFF/0x55 (6,824 changes), plus 60,000 random
    two-byte changes. Of **66,824 changes: 66,823 refused, 1 same fingerprint, 0 different, 0 panics.** The worst
    import took 8.2 ms. The single-flip refusals break down as: hash mismatch 2,948, unusable key 1,665, key/cert
    mismatch 1,068, unusable cert 744, wrong header 288, truncated 87, unknown version 24.
  - Lengths at u32 extremes (0, 1, 0x7fffffff, 0x80000000, 0xfffffffe, 0xffffffff, 16 KiB, blob length) in both
    length fields: all refused in under 1 µs, no panic.
  - A hash of 31, 33 or 0 bytes, an all-zero hash, and v1/v2/CRLF/`v3 `/`v03`/`V3`/`v4`/`v30`/leading-space lines:
    all refused (the table is in `r2_blob.log`).
  - Re-hashed edits load under a new pin (R2-2).
- **Kill loop (F3), two runs of 160 SIGKILLs at random 0–80 ms, same folder, the final file moved aside after each:**
  - Run 1: 120 valid final files, 0 partial, 0 with group/other bits; a leftover was seen right after 25 kills.
  - Run 2: 113 valid, 0 partial, 0 open bits; a leftover was seen after 46 kills, never more than 1 at once, none
    with open bits.
  - Before run 2's clean start the folder held 1 leftover. The clean start said "removed 1 leftover…". **After it the
    folder holds exactly `relay.identity`, valid, link count 1.**
  - Run 1's last kill left none, and its clean start likewise left only the valid file.
- **Pin across restarts, end to end** (the gate's `gate_pin_client` against the binary):
  - start 1 is created and the client connects;
  - start 2 is loaded with the same fingerprint, and the file's hash, mode, mtime, inode, owner and link count are
    unchanged;
  - the client pinned to start 1 exchanges Ping/Pong;
  - `--identity-stdin` with the same bytes gives the same pin and the client connects;
  - a default start is refused at `TlsHandshake` with `pin_mismatch true`.
- **Secrecy scan:** 555 captured stdout+stderr texts (every CLI run of the second probe pass, including all kill,
  race and pair runs) were scanned against 395 private keys: every identity file and leftover those runs produced or
  saw. Each key was searched as 16-byte windows in lowercase hex, uppercase hex and `{:?}` decimal (with and without
  spaces), and as 18-byte windows in standard and URL-safe base64. Result: **0 hits.** Positive control: the same
  scanner finds a deliberately printed key in all five spellings. The three mutants that print a key (G36, G44,
  M100) go red on the builder's own scans.
- **Committed-file hygiene:** all 4,042 added lines of `18005d6..afc2472` (`red-controls/OUTPUT.txt` included) were
  searched for `/Volumes`, `/Users/`, `/private/tmp`, `/tmp/`, `/home/`, `kamil`, `kreiser`, `Laptop-DEV`, `FRIDAY`,
  `!CODING`, `Datasec`, `Secuura`, `NexusAI`, `Wednesday`, `Friday`, `general-c2c`, `1117`, `1116`, `card `: **0
  each**. Positive controls: `identity` 662; `/Volumes` found twice in STATUS, which is outside the repo. The one
  `BEGIN PRIVATE KEY` is a test's fake header with no key under it. No `.identity/.pem/.der/.key/.blob/.p12/.crt` or
  `tmp-` file is in the tree.
- **No `unsafe`** in either crate's `src` except the two `#![forbid(unsafe_code)]` lines (searched case-insensitively,
  excluding prose such as "without `unsafe`"). No ACL/xattr code. No dependency added; `Cargo.lock` is unchanged.

## 3. Round-1 findings

- **F1 (Major): CHANGED, carried out as ruled.** No ACL check, no dependency, no `unsafe` were added (verified above).
  `USAGE` and the CLI README now say exactly what is checked (owner and permission bits of the file and its folder)
  and what is not (macOS ACLs and extended sharing rules; folders above the file's folder). They give `ls -le <file>`
  and `ls -led <folder>`. The bounds table repeats this. No user-facing text calls the file "private": a
  case-insensitive search of both READMEs, `args.rs`, `identity_file.rs`, `relay_cmd.rs` and `tls.rs` finds "private"
  only for "the private key", `doctor`'s network class, and code. The gate RAN the claims:
  - an `everyone allow read` ACL on the file loads, as documented;
  - `ls -le` shows ` 0: group:everyone allow read`;
  - an inheriting folder ACL gives the relay's new file ` 0: group:everyone inherited allow read`, as documented;
  - `ls -l` shows `-rw-------@`, as documented.

  The text test `help_and_readme_say_what_is_and_is_not_checked` pins four sentences in both texts and forbids three
  overclaims. The one stale sentence is R2-3.
  **What a user must do to keep the file safe:** keep it in a folder that you created yourself, that only you can open
  (`chmod 700`), and that you have never shared in Finder. Once, run `ls -led <folder>` and `ls -le <file>`. Any line
  under them that starts with a number means someone else has been given access, so move the file. Do not copy the
  file anywhere, including backups, cloud sync or e-mail. Anyone with a copy can pose as your relay (they see who
  connects and when, not what is said). If you think a copy escaped, delete the file and start without it, then send
  new invitations.
- **F2: CLOSED for damage.** 0 different fingerprints in 66,824 changes; v1 refused. It does not protect against a
  deliberate re-hashed edit, and the README overstates this (R2-2).
- **F3: CLOSED.** Cleanup works and every attack on it held (§4). 320 kills; after each clean start, 0 leftovers.
  The silent-removal gap is R2-1.
- **F4: CLOSED.** The descriptor is consumed to exactly the cap plus one byte, and the docs say so.
- **F5: CLOSED.**
  - A non-loopback listen (0.0.0.0, [::], 10.255.255.1, 192.0.2.1) with a new identity path, option before or after:
    exit 1, the file does not exist, the folder is empty, and nothing listened.
  - Usage errors (bad address, port only, bad `--status-secs`, unknown flag, both options in either order, the file
    option twice): exit 2, no file.
  - Non-loopback + `--identity-stdin` with a silent open pipe: refused at 0.01 s, without waiting for input.
  - A leftover is not removed by a start refused for its address.
  - A bind failure after creation (port in use): exit 1, "identity: saved, created … (the relay did not start)"; the
    file is valid and the next start loads it, as DQ3 and STATUS state.
- **F6: CLOSED.** G08, G13, G14 and G37 are all RED now, with the property's own text (table below).
- **N1–N9:** unchanged; nothing new. N6 and N8 were seen again.

## 4. Cleanup attack table (identity path `<d>/relay.identity`, `<d>` 0700; RAN against the head binary)

| attack | outcome | verdict |
|---|---|---|
| A1 symlink `.relay.identity.tmp-11-22` → a 0600 file of the user elsewhere | refused "not a regular file", exit 1; target content hash unchanged; link left | held: never followed |
| A1b dangling symlink of the pattern | refused; the target was NOT created | held |
| A2 directory of the pattern (with a file inside) | refused; directory and its file untouched | held |
| A3 FIFO of the pattern | refused at 0.01 s (no blocking); FIFO left | held |
| A4 hard link of the pattern → an unrelated 0600 user file | removed ("removed 1"); the other name's content is intact (hash), link count back to 1 | held: only a name is removed |
| A4b hard link → an unrelated 0644 user file | refused "other users have access"; name and target untouched | held (a DoS only, fails closed) |
| A5 leftover = hard link to the identity file itself (kill between link and unlink) | removed; identity loads with the same fingerprint, content unchanged, link count 1 | held |
| A6 25 near-miss names (`relay.identity.bak`, `~`, `.swp`, `.relay.identity`, no leading dot, `tmp-1`, `tmp--1`, `tmp-1-`, `tmp-1-2-3`, `tmp-a-1`, `tmp-1-2.bak`, trailing/leading space, `TMP`, upper-case name, Arabic-Indic digit, `+1`, newline, double dot, `relayXidentity`, `identit`, `1_2`, `.other.identity.tmp-1-2`, `.relay.tmp-1-2`) | **none removed or changed**; the real identity loads | held: the pattern is exact |
| A6b matching shapes `tmp-0-0`, a 24-digit pid, leading zeros | removed (3) | as designed (these are the program's own name shape) |
| A6c path given in another case (APFS case-insensitive) | loads; the lower-case leftover is NOT removed | fails safe (R2-6) |
| A6d non-UTF-8 name | APFS refuses to create it (EILSEQ) | n/a on macOS |
| A7 another identity file and its leftover in the same folder | both untouched | held |
| A8 leftover in a 0755 folder | refused for the folder; leftover kept | held today, untested (N24, R2-4) |
| A9 five good leftovers + one 0640 | refused naming the 0640; **all six kept**, nothing created | held (A1-DQ3) |
| A10 leftover modes 04600, 0400, 0000, 0200, 01600 | each removed | as designed (no group/other bits) |
| A11 refused load (identity 0640) with a 0600 leftover | refused; **leftover removed silently** | R2-1 |
| A12a 5,000 matching leftovers | all removed, one line "removed 5000", 4.4–5.0 s | bounded (linear) |
| A12b 50,000 non-matching files | start at 0.06–0.08 s; nothing removed | bounded |
| A12c 5,000 leftovers, the last one 0604 | refused at 0.03 s; all 5,000 kept | held |
| Attacker-controlled folder | not reachable as such: the folder must pass the owner + mode check. With a folder ACL granting another user `add_file` (which F1 accepts), that user can plant only files they own (refused "not yours"), links (refused) or hard links to the owner's files (only a name is removed). | REASONED: fails closed or harmless |
| Race: a thread flips the name between a 0600 file, a symlink and a hard link to a victim file (atomic `rename`) during 200 starts | 100 listened, 100 refused (twice: 94/106 in run 1); **the victim's content is intact both times**. `unlink` never follows a link, so a swap between check and removal only ever removes a name. | held |
| 30 simultaneous creates on one new path | 29 with one refused (25 "could not link…: entity not found", 4 "a file appeared…"), 1 where both listened on the same fingerprint; every folder ended with exactly one valid file | fails closed (R2-7) |
| Kill loop 2 × 160 + clean start | see §2: 0 partial, 0 open bits, 0 leftovers after the clean start | held |

## 5. Mutation table

80 mutants: round 1's 44 (G01–G44; the three standard-input anchors moved to the new code with the same mutation),
plus 36 new (N01–N36) on code changed since `e143847`. Each was applied alone in a scratch worktree. Tests: all of
`coagent-cli`, plus `coagent-relay` `identity_blob`, `gate_identity_fuzz` and the lib units. **65 RED, 15
SURVIVED, 0 no-compile, 0 anchor problems.** Sources were restored byte-for-byte, and both worktrees were clean
afterwards.

| id | mutation | result | caught by (first) / says |
|---|---|---|---|
| G01 | parent must be a directory: check removed | **SURVIVED** | equivalent (round 1: ENOTDIR still refuses) |
| G02 | parent mode: OTHER bits ignored (mask 0o070) | RED | refused_parent_open_to_others — "…directory open to others was loaded (other, mode 701)" |
| G03 | parent mode: GROUP bits ignored (mask 0o007) | RED | refused_parent_open_to_others — "(group, mode 750)" |
| G04 | file mode: OTHER bits ignored | RED | refused_file_open_to_group_or_others — "(other read)" |
| G05 | file mode: GROUP bits ignored | RED | a_group_readable_identity_is_refused_and_never_repaired — "a group-readable identity: the relay listened" |
| G06 | file mode: only read bits checked | RED | refused_file_open_to_group_or_others — "(group write)" |
| G07 | directory-at-path branch removed | RED | refused_directory_at_the_path |
| G08 | regular-file check removed (FIFO opened) | **RED** (was SURVIVED) | refused_fifo_at_the_path_without_blocking — "a FIFO at the path was opened: the start blocked for 10 s" |
| G09 | size cap `>=` | RED | an_identity_file_over_the_cap_is_refused_before_reading |
| G10 | pre-read cap 1 MiB | RED | refused_file_over_the_cap; "more than the cap was read: 16385 bytes" |
| G11 | file read bound 1 MiB | **SURVIVED** | equivalent (race-only, round 1) |
| G12 | post-read bound removed | **SURVIVED** | equivalent (round 1) |
| G13 | descriptor re-check removed | **RED** (was SURVIVED) | the_opened_file_is_checked_again — "the opened file was not checked again: a group-readable identity was loaded" |
| G14 | temp file not exclusive | **RED** (was SURVIVED) | the_temporary_file_is_exclusive_and_never_follows_a_link — "the key was written through a planted symbolic link" |
| G15 | temp created 0660 | RED | a_created_identity_file_is_private_and_alone — "(mode 660; … umask 000)"; kill loop "final file open to others" |
| G16 | temp guard forgotten | RED | "the directory holds more than the identity file" |
| G17 | fsync removed | **SURVIVED** | durability only (round 1) |
| G18 | parent with symlink_metadata (stricter) | **SURVIVED** | stricter, not weaker (round 1) |
| G19 | grandparent checked | RED | refused_missing_parent; leftover tests |
| G20 | uid = gid | RED | many ("did not print its banner") |
| G21 | AlreadyExists → generic I/O | RED | create_never_replaces_an_existing_file |
| G22 | create on any metadata error | **SURVIVED** | practically equivalent (round 1) |
| G23 | empty stdin not "Nothing" | RED | stdin_closed_empty_is_refused |
| G24 | stdin TooLarge left to from_blob | RED | stdin_flood_* |
| G25 | deadline 30 s | RED | "still waiting after the deadline (5 s + 10 s)" |
| G26 | stdin cap 1 MiB | RED | stdin_flood_*; descriptor test "16386 of 16386" |
| G27 | one-day deadline passed | RED | stdin_with_nothing_written_exits_within_the_deadline |
| G28 | any version line accepted | RED | blob_refusals_through_both_options — "version 2: the relay listened"; gate g03 |
| G29 | unknown version → wrong header | RED | "version 2: the refusal does not say "version"" |
| G30 | no newline → always truncated | RED | a_blob_with_a_wrong_first_line_is_refused |
| G31 | InconsistentKeys::Unknown passes | **SURVIVED** | unreachable with ring (round 1) |
| G32 | unparseable certificate accepted | RED | garbage_in_the_key_or_certificate_part_is_refused |
| G33 | fingerprint over the key | RED | a_saved_identity_survives_a_restart; gate g05 |
| G34 | export cap check removed | **SURVIVED** | unreachable with generated identities (round 1) |
| G35 | export: cert length for both parts | RED | many |
| G36 | IdentityBlob Debug prints bytes | RED | gate g07; no_debug_or_display_form_contains_the_key |
| G37 | import cap `>=` | **RED** (was SURVIVED) | the_import_cap_is_exactly_16_kib — "Err(TooLarge { len: 16384 })" |
| G38 | path starting with `-` accepted | RED | args::tests::refusals |
| G39 | `--identity-stdin` overrides silently | RED | args::tests::refusals |
| G40 | identity not handed to the relay | RED | a_saved_identity_survives_a_restart (pin mismatch) |
| G41 | identity refusal exits 0 | RED | "expected a non-zero exit, got Some(0)" |
| G42 | identity line before the banner | RED | a_created_identity_file_is_private_and_alone |
| G43 | Windows branch on unix | RED | file tests ("did not print its banner") |
| G44 | file error prints the file's bytes | RED | "the key appeared in standard error (decimal byte list)" |
| N01 | hash check: first byte only | RED | blob_refusals_through_both_options — "certificate hash damaged: the relay listened" |
| N02 | export stores a zero hash | RED | every reload refused ("did not print its banner") |
| N03 | export stores no hash | RED | "key, then the 32-byte certificate hash" |
| N04 | one trailing byte after the hash accepted | RED | "one trailing byte: the relay listened" |
| N05 | v1 line accepted | RED | "version 1 (the round-1 layout, no hash): the refusal does not say "version"" |
| N06 | v2 line accepted | RED | "version 2: the relay listened" |
| N07 | CRLF v3 line accepted | **SURVIVED** | harmless (body and hash still exact); R2-8 |
| N08 | hash mismatch reported as TrailingBytes | RED | "certificate hash damaged: the refusal does not say "damaged or was edited"" |
| N09 | missing hash reported as truncated key | RED | a_blob_truncated_at_every_byte_position_is_refused — "truncated to 536 of 568 bytes" |
| N10 | key-belongs result ignored | RED | "a mismatched key was accepted and the relay listened…" |
| N11 | `Fingerprint::of_certificate` wrong bytes | RED | blob_refusals_through_both_options |
| N12 | fingerprint from stored hash, check removed | RED | "certificate hash damaged: the relay listened" |
| N13 | pattern: leading dot not required | RED | leftover test "…(or another file was removed)" |
| N14 | pattern: digits not required | RED | the_leftover_pattern_is_exact — `.relay.identity.tmp-1-2x` |
| N15 | pattern: second number not checked | RED | the_leftover_pattern_is_exact — `.relay.identity.tmp-1-` |
| N16 | pattern: empty numbers allowed | RED | the_leftover_pattern_is_exact |
| N17 | pattern: any identity's leftovers match | RED | leftover test "…(or another file was removed)" |
| N18 | cleanup: only directories refused | RED | a_suspicious_leftover_* — "symbolic link: the refusal does not say "not a regular file"" |
| N19 | cleanup metadata follows links | RED | "symbolic link: the relay listened" |
| N20 | cleanup owner check removed | **SURVIVED** | **real test gap** (R2-4) |
| N21 | cleanup "other" bits ignored | **SURVIVED** | **real test gap** (R2-4) |
| N22 | cleanup group bits ignored | RED | "group-readable: the relay listened" |
| N23 | suspicious match skipped, start proceeds | RED | "group-readable: the relay listened" |
| N24 | cleanup before the parent check | **SURVIVED** | **real test gap** (R2-4) |
| N25 | cleanup count reported as 0 | RED | leftover_temporary_files_are_removed_at_the_next_start |
| N26 | cleanup removal error ignored | **SURVIVED** | low (R2-8) |
| N27 | create's temp name off-pattern | RED | a_killed_create_leaves_nothing_after_the_next_start — "a leftover temporary file survived the next start" |
| N28 | planted file at temp name removed on EEXIST | RED | the_temporary_file_is_exclusive_* (planted file gone) |
| N29 | cleanup message not printed | RED | leftover_temporary_files_are_removed_at_the_next_start |
| N30 | cleanup line on stdout | RED | leftover_temporary_files_are_removed_at_the_next_start |
| N31 | stdin limit cap+2 | RED | stdin_flood_* — "refused after reading 16386 bytes" |
| N32 | stdin through a BufReader again | RED | descriptor test — "16386 of 16386" |
| N33 | deadline message reports 0 bytes | **SURVIVED** | cosmetic (R2-8) |
| N34 | stdin TooLarge `>=` | RED | stdin_flood_reader_* — "TooLarge { bytes_read: 16384 }" |
| N35 | early non-loopback refusal exits 0 | RED | non_loopback_listen_is_refused_without_the_flag_and_nothing_is_started |
| N36 | early refusal ignores `--allow-non-loopback` | **SURVIVED** | **real test gap** (R2-4) |

Survivors: round-1 equivalents G01, G11, G12, G17, G18, G22, G31, G34 (unchanged rulings); new N07, N26, N33
(equivalent or cosmetic); **real: N20, N21, N24, N36** (R2-4). All four of round 1's real survivors (G08, G13, G14,
G37) are now RED.

## 6. Merge results

- `origin/main` = `18005d6` is an ancestor of head. `git merge origin/main` in a scratch branch gives "Already up to
  date", and the tree hash afterwards equals head's (`d0627089…`). So the five check.sh runs above are the merged
  tree's results: exit 0, 314/0/5.
- Trial merge of `origin/m1-daemon` (`d8b5b4b`): **one textual conflict, `BACKLOG.md`**. Merge aborted.
- Trial merge of `origin/m3-roster` (`d88d5d7`): **one textual conflict, `BACKLOG.md`**. Merge aborted.
- No conflict in any crate file. Those branches were not judged.

## 7. What the gate could not do

- Run as a second user (no sudo). The foreign owner of the file, the folder and a leftover is REASONED plus the
  builder's injected-uid tests. N20 shows the leftover owner check has no such test.
- Start with `--allow-non-loopback`: forbidden by this gate's rules, so N36's behaviour is read, not run.
- Trace every `open(2)` of a default run (needs root). It was replaced by empty cwd/TMPDIR/HOME and an `lsof`
  snapshot, as in round 1.
- Build or run on Windows or Linux.
- Race against a second user for real. The check-versus-removal race was run within one user (200 starts, twice).

## 8. For the owner, in plain words

1. A saved relay identity lets people you invited reconnect after you restart the relay, and they still refuse any
   other relay pretending to be yours. The gate checked this end to end.
2. Anyone who gets a copy of the identity file can pose as your relay. They would see who connects, when and how
   much, and could cut people off, but they cannot read what is said.
3. The program checks the file's and its folder's ordinary permissions only, not the extra Mac "sharing" rules. You
   accepted that for the beta. Keep the file in a folder only you have ever had, and check it once with
   `ls -le <file>` and `ls -led <folder>`: no numbered lines should appear.
4. A damaged file is refused instead of quietly becoming a different relay. Someone who can write to the file can
   still replace it, so treat write access like read access.
5. After a crash the program cleans up its own leftover copies of the key at the next start. If it ever refuses to
   start because of a "leftover temporary identity file", look at that file before deleting it.
