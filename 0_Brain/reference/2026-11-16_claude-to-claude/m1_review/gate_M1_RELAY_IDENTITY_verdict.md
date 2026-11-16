VERDICT: NO GO — head e143847c960d83c89967b18fb81eeac0e9ac3e0c

# Gate M1 RELAY-IDENTITY — independent tier-1 QA (findings only; nothing fixed, nothing merged)

Branch `m1-relay-identity`, head `e143847c960d` (confirmed by `git rev-parse` on a fresh clone). Base `main` `18005d6`
(`origin/main` is still `18005d6`). Clone, worktrees, builds and every probe ran in the gate's scratch folder; nothing
was pushed; no git write verb was run inside `!CODING/`. Every relay the gate started listened on 127.0.0.1 with an
ephemeral port (one probe used a 127.0.0.1 port the driver itself took from the OS to make the bind fail). Tests and
drivers: `gate_relay_identity_tests/` (sources and small result logs; no identity file, no key, no build output).

**Why NO GO, in one paragraph.** The work is careful and every promise in the brief's section 5 reproduces. But on
macOS — the only platform this was built and tested on — the rule "nobody but you can read the key file" is enforced
only on the mode bits, and macOS access-control lists (ACLs) are a second, independent permission system the check
does not see. The gate RAN it: a key file carrying `everyone allow read` is loaded; worse, a 0700 parent directory
carrying an INHERITABLE `everyone allow read` entry passes the parent check, and the relay itself then CREATES the
key file with `group:everyone inherited allow read` while `ls -l` shows `-rw-------`, prints `identity: saved,
created`, and reloads it on the next start. The help text, the CLI README and STATUS all tell the user the file is
private. Closing this needs either an ACL check (a dependency or `unsafe`, both forbidden to the builder: an OWNER
decision) or an explicit, documented acceptance of the residual (ssh on macOS has the same blind spot). Either way the
current text overclaims, and that is the one thing a gate on "when may a stored key be trusted" must not wave through.
The fix round is small: F1 decision + text, F2–F4 corrections, three tests for the real survivors. If the owner
accepts F1 in writing and the text is corrected, this becomes GO WITH NOTES without further code.

## 1. Findings

| id | severity | file:line | exact sequence | RAN / REASONED |
|---|---|---|---|---|
| F1 | **Major** | `crates/coagent-cli/src/identity_file.rs:204-225` (`check_parent`), `:229-268` (`check_file`), `:328-333` (create) | (a) `chmod +a "everyone allow read" <scratch>/relay.identity` (mode stays 0600) → `coagent relay --identity-file <that>` → LOADED, listens. (b) `chmod +a "everyone allow list,search,add_file,delete_child" <dir>` (mode 0700) → load and create both pass. (c) `chmod +a "everyone allow read,file_inherit" <dir>` → `coagent relay --identity-file <dir>/n` → prints `identity: saved, created …`; `ls -le` of the new key file: `-rw-------@ … 0: group:everyone inherited allow read`; second start LOADS it. Every other local user can read the private key of a file the relay itself just created and called private. Help (`USAGE`), CLI README "File rules", STATUS §2 and §3 item 3 claim the file is private. Std Rust has no ACL API, so a fix needs a dependency or `unsafe` (owner), or a documented accepted residual. Combined with DQ2 (ancestors unchecked, parent judged by path), a DIFFERENT user who can write an ancestor directory can swap the parent between the check and the create so the new key lands in a directory of theirs with an inheritable allow-read ACL, then read it (REASONED). Linux POSIX default ACLs are masked by the 0600 create mode, so this is macOS-specific (REASONED). | RAN (a)(b)(c); REASONED (race, Linux) |
| F2 | Minor | `crates/coagent-relay/src/tls.rs:142-160` (`from_blob`), `:317-333` | Flip one byte of a valid blob at every position with masks 0x01, 0x80, 0xFF (1,611 mutants of a 537-byte blob): 969 refused, 0 accepted with the same fingerprint, **642 accepted with a DIFFERENT fingerprint — every one inside the certificate bytes**, and each of the 642 started a relay that served a pinned client. Only the certificate's public key is compared with the key; nothing checks the rest of the certificate (serial, validity, names, its self-signature). A corrupted or hand-edited identity file therefore starts with `identity: saved, loaded <path>` and a NEW pin, with no warning to the host. Joiners fail closed (pin mismatch), so nobody trusts a wrong relay, but the host is misled and the joiners get the "something may be impersonating the relay" path. Key-region flips: all refused. Cheap fixes: verify the self-signature on import, or keep the SHA-256 of the certificate in the blob and compare (layout is not merged yet). | RAN (`gate_identity_fuzz.rs` g02) |
| F3 | Minor | `crates/coagent-cli/src/identity_file.rs:301-350`; CLI README lines 36-38 | SIGKILL a creating relay at a random 0–60 ms, 150 times: 16 no file, 134 valid final file, **0 partial final files, 0 files with group/other bits**, but **11 runs left `.relay.identity.tmp-<pid>-<nanos>`** (536–538 bytes, mode 0600, the private key) and 1 run left the final file with link count 2 (temp name not yet unlinked). Nothing ever removes such a file later. Ctrl-C during creation behaves the same, because the SIGINT handler is installed only after the banner (REASONED from `relay_cmd.rs`). README and STATUS say "no temporary file is left behind on success or on failure"; true for every error return, false for a killed process. | RAN (`probe.py` kill section) |
| F4 | Minor | `crates/coagent-cli/src/identity_stdin.rs:53-71`; CLI README bounds table; STATUS §3 item 8 | Stdin given as a regular file shared with the driver; after exit the driver reads the shared file offset = bytes the relay consumed: 16,384-byte file → 16,384; 16,385 → 16,385; 16,386 → **16,386**; 1 MiB → **24,576**; 64 MiB → **24,576**. The logical buffer is capped at cap+1 (message "refused after reading 16385 bytes"), but the process takes up to cap + 8 KiB from the descriptor (std's `Stdin` is an 8 KiB `BufReader` under tokio's blocking reader). Memory stays bounded; the claim "at most the cap plus one byte read" is not true at the descriptor and the builder's binary test ("the pipe accepted < 1 MiB of 8 MiB") cannot tell. Endless pipe: writer got 65,536 bytes in (pipe buffer) before EPIPE; exit 1. | RAN |
| F5 | Minor | `crates/coagent-cli/src/relay_cmd.rs:146-160`, `identity_file.rs:375-386` | `coagent relay --listen 0.0.0.0:0 --identity-file <new>` (no `--allow-non-loopback`): the identity file is CREATED, then the start is refused as non-loopback. The non-loopback refusal is known before any file work (`bind_allowed`, a pure function) and could come first. Bind failure after creation (port in use) leaves the file and says `identity: saved, created … (the relay did not start)` — as DQ3 states. | RAN |
| F6 | Minor (test gap) | see §4 | 12 of the gate's 44 mutations survive; four are real unguarded checks: G08 regular-file check removed (a FIFO at the path would be opened and `open(2)` would block forever before the size check), G13 the re-check on the opened descriptor removed, G14 temporary file not exclusive (`create+truncate`, follows a planted symlink), G37 import cap off by one. The checks themselves work (the gate RAN the FIFO and every other refusal against the real binary); only the tests would not notice their removal. | RAN |
| N1 | Note | `identity_file.rs:217-218, 253-254` | Setuid/sticky bits pass: file 04600 and 01600 load; directory 04700 and 01700 load and create (setgid was cleared by the kernel). Harmless for a non-executable file and for a 0700 directory. | RAN |
| N2 | Note | `identity_file.rs:229-268` | Link count is not checked: a hard link to a valid identity loads (`identity: saved, loaded …/hardlink`, same pin). With the parent at 0700 only the owner or root can add a name there. On macOS another user can hard-link the owner's file into a directory of their own (no `protected_hardlinks`), which keeps the inode alive after the owner deletes their name, but cannot read it (0600 and no ACL — see F1). | RAN (load); REASONED (other user) |
| N3 | Note | `identity_file.rs:274` | `File::open` without `O_NONBLOCK`/`O_NOFOLLOW`: a FIFO swapped in between the `lstat` and the `open` blocks the start forever. Needs write access to the parent directory (owner, root, or an ancestor-writer per DQ2). A symlink swapped in is caught by the inode comparison. | REASONED |
| N4 | Note | `identity_file.rs:323-327` | A final name of 240 bytes fits NAME_MAX, the temporary name does not: refused with "could not create a temporary file next to: invalid filename". Fails closed, misleading text. | RAN |
| N5 | Note | `tls.rs:317-333` | Identities the relay would not itself generate are accepted and serve a pinned client: RSA-2048 (made with `openssl req -x509`), Ed25519, P-384, a CA certificate, an expired certificate, a not-yet-valid certificate. Safe: the blob comes from the local user or the parent process, and the client pins the hash only. Two certificates concatenated in the certificate part, garbage after the certificate, garbage after the key, parts swapped: all refused (UnusableCertificate / UnusableKey). | RAN (g06, g03, g04) |
| N6 | Note | `tls.rs` header parser | `coagent-relay-identity v1\r\n` (CRLF), `v1 \n`, `v01\n` are refused as "a version this program does not know" — refused, but a CRLF-damaged file gets a misleading reason. | RAN (g03 and through both options) |
| N7 | Note | `tls.rs` (no wiping) | The key stays in freed heap after use: `key_pkcs8`, the blob, the read buffer, the copy in `key_belongs_to_certificate` (`key.to_vec()`), and a clone at every `server_config`. It can reach swap or a core dump. Acceptable for an unreviewed beta: the key protects metadata only, and anyone who can read this process's memory or core files (same user or root) can already read the 0600 file. Cost of fixing: one `zeroize` dependency line (R2), owner's call. | REASONED |
| N8 | Note | `relay_cmd.rs` (pre-existing) | A SIGINT that arrives right after the banner, before the signal handler is installed, ends the process by the signal (exit -2 seen in 2 of 3 default runs of BOTH main and head, and in some head runs with options). Same on main; not introduced here. | RAN |
| N9 | Note | brief vs code | The `bytes_read: 0` that "proves" the size check precedes reading is a constant written in `check_file`, not a measurement; it still goes red under M93 because the fallback path reports a real count. Honest enough; the gate measured the file read independently (sizes over the cap are refused before reading: 16,385 B and a sparse 1 GiB file, both "it was not read", 0.00 s). | RAN |

No Blocker. Everything else the gate attacked held (§3).

## 2. Measured totals

- `git rev-parse HEAD` = `e143847c960d83c89967b18fb81eeac0e9ac3e0c`. Forbidden files byte-identical to `18005d6` (blob hashes compared one by one): `src/limits.rs, state.rs, frame.rs, meter.rs, server.rs, client.rs, bucket.rs, cut.rs, tests/gate_attacks.rs, tests/gate_r2_wire.rs, src/gate_r2_state.rs, src/gate_r2_meter.rs`, root `Cargo.toml`, `Cargo.lock`, and `PROTOCOL.md` (empty diff). Changed files (17): `BACKLOG.md`, `crates/coagent-cli/{Cargo.toml, README.md, src/args.rs, src/identity_file.rs (new), src/identity_stdin.rs (new), src/lib.rs, src/relay_cmd.rs, tests/identity_cli.rs (new), tests/identity_file.rs (new), tests/support/mod.rs (new)}`, `crates/coagent-relay/{README.md, red-controls/OUTPUT.txt, red-controls/run.py, src/lib.rs, src/tls.rs, tests/identity_blob.rs (new)}`.
- **Dependencies:** Cargo.lock unchanged; `cargo tree -p coagent-cli` package graph identical to main's apart from the checkout path; the only difference in `cargo tree -e features -i tokio` is the new line `tokio feature "io-std"`. Ruling: a feature on an existing crate, no new package, no change to the lock or the graph.
- **check.sh × 5 at head:** exit 0 every time; **293 passed, 0 failed, 5 ignored** every time; wall 87 s (cold), 62, 65, 59, 58 s. Matches the builder.
- **Red-control runner** `run.py --with-dep`: **93 rows, 93 RED, 0 problems**, "sources restored byte-for-byte" — all 66 old rows still RED. Each new row M80–M106 applied alone with its own cargo args, panic text captured (`results/red_why.log`): every one fails with the message its property names (M80 "two default starts share a fingerprint", M83 "a client pinned to the first start could not connect to the second … pin mismatch", M85 "readable by others (mode 644; umask 000)", M93 "more than the cap was read: 16385 bytes", M96 "a mismatched key was accepted and the relay listened", M97 "still waiting after the deadline", M98 "refused after reading 8388608 bytes", M100 "the key appeared in standard error (decimal byte list)", …). M102/M104 fail on a bare `assert_eq` of the error variant (the named one); M103 fails by a slice panic `mid > len`, which is the property's direct effect, as the builder declared.
- **Gate mutations:** 44 run, 32 RED, 12 survived (§4).
- **Default unchanged (main binary vs head binary, 3 starts each, empty cwd/TMPDIR/HOME in scratch):** banner prefixes identical and in the same order (`coagent relay`, `address`, `url`, `fingerprint`, `invite candidate`, blank, `Press Ctrl-C to stop. A reminder line is printed to stderr every 60 s.`), no `identity:` line, three distinct fingerprints each, cwd/TMPDIR/HOME empty afterwards. `lsof -p` of a running default relay: the same three REG/DIR entries for both binaries (cwd, the binary, dyld) — no identity file open. NOT observable: a full trace of every `open(2)` (needs `fs_usage`/`dtruss`, i.e. root); the gate did not use sudo. Usage errors: 16 argument sets, main and head give the same exit codes for every pre-existing one (2, and 1 for the non-loopback refusal); the new combinations exit 2 and create nothing.
- **Stdin deadline**, silent open pipe, 5 runs: 5.01, 5.01, 5.02, 5.01, 5.01 s (spread 0.01 s); a TTY (pty) 5.01 s twice; a valid blob with the pipe kept open: refused at 5.01 s ("536 bytes, then no end of file"); 2 bytes/s dribble: refused at 5.04 s (one deadline for the whole read, confirmed). `/dev/null` and a closed fd 0: "nothing was received", 0.01 s. Regular file holding a valid blob: accepted, same pin. Valid blob on a pipe: accepted, same pin, cwd/TMPDIR/HOME still empty.
- **Pin across restarts, end to end** (the relay crate's own `connect_pinned`, Ping→Pong): start 1 `--identity-file` (created) → client OK; stop; start 2 (loaded) same fingerprint, file byte/mode/mtime/inode/owner/link-count unchanged → the client pinned to start 1 connects and exchanges a frame; `--identity-stdin` with the same file's bytes → same pin, client OK; a default start → refused at `TlsHandshake`, `pin_mismatch=true`.
- **Secrecy scan:** two scan passes, one per driver process: 198 captured stdout+stderr texts against 178 private keys, and 33 texts against 15 keys (the keys are every identity file and leftover temp file those runs produced, plus the RSA key; the default/usage runs export no key and were not scanned), each key scanned as every 16-byte window in lowercase hex, uppercase hex, `{:?}` decimal list (with and without spaces) and every 18-byte window in standard and URL-safe base64 (alignment-independent core): **0 hits**. Positive control: the same scanner finds a deliberately printed key in all five spellings. Library `Debug`/`Display` of `TlsIdentity`, `IdentityBlob`, `IdentityBlobError`: no key (g07, with control). No `unwrap/expect/panic!` in the new non-test code of `identity_file.rs`, `identity_stdin.rs`, `relay_cmd.rs`, nor in `tls.rs`'s new non-test functions. The only `{:?}` in new non-test code prints the user's path argument. Default runs' keys are never exported, so they cannot be scanned (nothing to compare against).
- **Committed-text hygiene:** in every added line of the branch diff, counts of `/Volumes`, `/Users/`, `/private/tmp`, `kamil`, `kreiser`, `Laptop-DEV`, `FRIDAY`, `!CODING`, `Datasec`, `Secuura`, `NexusAI`, `Wednesday`: 0 each (positive control: `identity` 512, and `/Volumes` found in the builder's STATUS outside the repo). `BEGIN PRIVATE KEY`: 1 — a test's fake PEM header line, no key under it. No `.identity/.pem/.der/.key/.blob` file in the tree; no test scratch directory committed.
- **Disk:** the gate's scratch folder is 2.0 GB (five target directories); nothing was written in `coagent/`.

## 3. Check on the path versus check on the opened descriptor (step 4)

| Step (order) | Call | On what | What it decides | What a racer can do in the window after it |
|---|---|---|---|---|
| 1 | `fs::metadata(parent)` = `stat(2)`, follows links (`identity_file.rs:365`) | **PATH** | parent exists, is a directory, is the euid's, no group/other bit | Parent is never re-checked and never opened. Only someone who can rename the parent's NAME (the owner, root, or a writer of an ancestor — DQ2) can swap it. On load that buys little (step 3–4 still demand a file of the owner's, 0600, same inode as step 2). On create it decides where the key is written (F1 race) and what is unlinked at the end. |
| 2 | `fs::symlink_metadata(path)` = `lstat(2)` (`:375`) + `check_file` | **PATH** (link not followed) | not a link, not a directory, regular file, owner, no group/other bit, size ≤ cap; records (dev, ino) | Needs write on the parent (0700, owner's): owner/root/ancestor-swapper only. Swap to a symlink → caught at step 4 (inode). Swap to a FIFO → step 3 blocks forever (N3). |
| 3 | `File::open(path)` O_RDONLY (`:274`) | **PATH**, follows links, no O_NONBLOCK | — | — |
| 4 | `f.metadata()` = `fstat(2)` (`:275-283`) | **DESCRIPTOR** | (dev, ino) equal to step 2's; type, owner, no group/other bit, size ≤ cap re-checked on the open file | Content trust decisions are taken here, on the descriptor. A chmod/chown after this (owner or root only) changes nothing already read. G13 shows this re-check is untested. |
| 5 | `take(cap+1).read_to_end` (`:285`) | **DESCRIPTOR** | at most cap+1 bytes (File is unbuffered, so this holds at the descriptor) | A file that grows is cut at cap+1 and refused (`Grew` / `TooLarge`). |
| C1 | `OpenOptions.create_new(true).mode(0o600).open(tmp)` = `O_CREAT|O_EXCL` (`:328-333`) | **PATH** (exclusive: never follows a link at the temp name) | new inode, 0600 &~umask from the first byte (umask 000 → 0600, 077 → 0600, 022 → 0600, 277 → 0400; RAN) | Inherits an ACL from the directory it lands in (F1). Temp name `.<name>.tmp-<pid>-<subsec-nanos>` is predictable but exclusive; only a parent-writer can plant anything. |
| C2 | `write_all` + `sync_all` on the descriptor | **DESCRIPTOR** | full content before any name points at it | Killed here → temp file left (F3). Directory not fsynced (durability only). |
| C3 | `fs::hard_link(tmp, path)` = `link(2)` (`:339`) | **PATH** | fails if `path` exists (any type, link not followed) → `Exists` | A file planted at `path` meanwhile → refused, untouched. No window where the final name shows a partial or 0644 file (0 in 150 kills). |
| C4 | `remove_file(tmp)` in `Drop` | **PATH** | removes the temp name | Killed between C3 and C4 → final file with link count 2 (1 in 150). |

**Ownership.** `current_uid()` = `UnixStream::pair()` then `peer_cred().uid()` (tokio → `getpeereid` on macOS): the
EFFECTIVE uid, which is the uid that owns files this process creates, so creation and checks agree. If real and
effective differ (a setuid install, not a supported deployment) the checks follow the effective uid. No `unsafe`, no
dependency (`#![forbid(unsafe_code)]` still present in both crates). Foreign owner: only REASONED plus the builder's
injected-uid test; a real second user was not available to the gate either (no sudo).

## 4. Mutation table (gate's own, applied one at a time in a scratch worktree; tests = all of `coagent-cli` + `coagent-relay` `identity_blob` and lib units)

| id | mutation | result | caught by / judgement |
|---|---|---|---|
| G01 | parent "is a directory" check removed | SURVIVED | Equivalent in outcome: a regular file as parent makes the next `lstat` fail `ENOTDIR` → still refused (message only). |
| G02 | parent mask 0o077→0o070 (other bits ignored) | RED | refused_parent_open_to_others ("other, mode 701") |
| G03 | parent mask →0o007 (group ignored) | RED | refused_parent_open_to_others ("group, mode 750") |
| G04 | file mask →0o070 | RED | refused_file_open_to_group_or_others ("other read") |
| G05 | file mask →0o007 | RED | same + never_repaired |
| G06 | file mask →0o044 (write bits ignored) | RED | "group write" |
| G07 | directory-at-path branch removed | RED | refused_directory_at_the_path |
| G08 | regular-file check removed | **SURVIVED** | **Real unguarded check**: a FIFO at the path would pass owner/mode/size and `open` would block forever. No FIFO/device test. (The check works today: RAN, refused in 0.01 s.) |
| G09 | file cap `>` → `>=` | RED | over_the_cap…_before_reading (exact-cap file) |
| G10 | pre-read cap 16 KiB → 1 MiB | RED | refused_file_over_the_cap; …before_reading |
| G11 | file read bound `take(cap+1)` → 1 MiB | SURVIVED | Reachable only when the file grows between `fstat` and read; `from_blob` would still refuse as TooLarge; memory up to 1 MiB. Race-only, low value. |
| G12 | post-read bound removed | SURVIVED | Equivalent as the builder says (variant changes `Grew` → `Blob(TooLarge)`). |
| G13 | re-check on the opened descriptor removed | **SURVIVED** | **Real unguarded check** (only the inode comparison is tested). A mode/owner/size change between `lstat` and `open` would go unnoticed. Owner/root only; but it is the descriptor check the design leans on. |
| G14 | temp file not exclusive (`create(true).truncate(true)`) | **SURVIVED** | **Real unguarded property**: a symlink or file planted at the predictable temp name would be followed/truncated and the key written through it. Needs parent write (owner/root/ancestor-swapper). |
| G15 | temp created 0660 | RED | a_created_identity_file_is_private_and_alone (umask 000) |
| G16 | temp guard forgotten on success | RED | "the directory holds more than the identity file" |
| G17 | `sync_all` removed | SURVIVED | Not testable without power loss; durability only. Note. |
| G18 | parent looked up with `symlink_metadata` (stricter) | SURVIVED | Expected: no test pins DQ2's "a symlinked parent is judged by its target". Stricter, not weaker. |
| G19 | grandparent checked instead of parent | RED | refused_missing_parent; refused_parent_open_to_others |
| G20 | current uid = gid | RED | 17 tests |
| G21 | `AlreadyExists` on link reported as generic I/O | RED | create_never_replaces_an_existing_file |
| G22 | create on ANY metadata error (not only NotFound) | SURVIVED | Practically equivalent: the paths that give other errors (`ENOTDIR`, `EACCES`) then fail at temp-create or link → still refused, different text. Note. |
| G23 | empty stdin not reported as "nothing" | RED | stdin_closed_empty_is_refused (+2) |
| G24 | stdin TooLarge left to `from_blob` | RED | stdin_flood_* (2) |
| G25 | deadline constant 5 s → 30 s | RED | stdin_with_nothing_written_exits_within_the_deadline |
| G26 | stdin cap → 1 MiB | RED | stdin_flood_* ("refused after reading 1048576 bytes") |
| G27 | caller passes a one-day deadline | RED | stdin_with_nothing_written_exits_within_the_deadline |
| G28 | any `coagent-relay-identity v…` line accepted | RED | blob_refusals_through_both_options; version_2 |
| G29 | unknown version reported as wrong header | RED | same |
| G30 | header without newline always "truncated" | RED | a_blob_with_a_wrong_first_line_is_refused |
| G31 | `InconsistentKeys::Unknown` passes (rustls's own behaviour) | SURVIVED | Equivalent with the ring provider: rustls 0.23.46 `keys_match` returns Unknown only when `SigningKey::public_key()` is `None`, and the ring provider implements it for RSA, ECDSA and Ed25519 (builder's citation re-read: `signer.rs:190-200`). The refusal (DQ8) is sound but untestable here. |
| G32 | unparseable certificate accepted | RED | garbage_in_the_key_or_certificate_part_is_refused |
| G33 | fingerprint over the key, not the stored certificate | RED | 5 tests |
| G34 | export cap check removed | SURVIVED | Unreachable with identities this code generates (~540 B); equivalent in practice. |
| G35 | export writes the certificate length for both parts | RED | 16 tests |
| G36 | `IdentityBlob` Debug prints its bytes | RED | no_debug_or_display_form_contains_the_key ("decimal byte list") |
| G37 | import cap `>` → `>=` | **SURVIVED** | **Real, small test gap**: no test at exactly 16,384 bytes for the library (the CLI file cap has one, G09). |
| G38 | path starting with `-` accepted | RED | args::tests::refusals |
| G39 | `--identity-stdin` overrides without the exclusivity check | RED | args refusals; both_identity_options_are_a_usage_error |
| G40 | resolved identity not given to the relay | RED | restart + stdin fingerprint tests |
| G41 | identity refusal exits 0 | RED | 14 tests ("expected a non-zero exit") |
| G42 | `identity:` line printed before the banner | RED | a_created_identity_file_is_private_and_alone |
| G43 | Windows branch compiled on unix (both cfgs flipped) | RED | 13 file tests: the not-unix branch COMPILES on this host and refuses every `--identity-file`. Says nothing about a Windows target build (not attempted; `ring` needs a C toolchain). |
| G44 | file refusal prints the file's bytes | RED | the key-scan tests ("the key appeared in standard error (decimal byte list)") |

Survivors: G01, G08, G11, G12, G13, G14, G17, G18, G22, G31, G34, G37. Real unguarded: **G08, G13, G14, G37** (F6).

## 5. DESIGN QUESTION rulings

1. **DQ1 link-then-unlink instead of rename — SOUND.** `rename(2)` would replace an existing name; `link(2)` fails if it exists. Measured: no window where the FINAL name holds a partial or group/other-readable file (0 of 150 kills; it appears only after `fsync`, as the same 0600 inode). Under the TEMP name a complete or partial 0600 key exists briefly and survives a kill (11 of 150, F3); link count 2 if killed between link and unlink (1 of 150). Needs a filesystem with hard links (fails closed elsewhere). The doc must stop saying "never left behind"; a start could also refuse or report a stale `.<name>.tmp-*` beside the file.
2. **DQ2 ancestors not checked; a symlinked parent judged by its target — NEEDS THE OWNER.** Acceptable for a beta only as a DOCUMENTED residual, and today it is documented only in STATUS and the module comment, not in the README or help. Residual: a different user who can write any ancestor (a non-sticky shared directory on the path, or the directory holding a symlinked parent) can swap the parent between the check and the use: on load they can only point at another file the owner owns (step 4 holds); on create they choose where the new key is written and — with F1 — can make it readable to themselves. `/tmp`-style sticky ancestors do not allow the swap. The ssh `StrictModes` walk is the stricter fix.
3. **DQ3 file created before bind — SOUND** (a refusal must precede listening; RAN: port in use → file stays, message says so). Improvement F5: run the non-loopback refusal before creating.
4. **DQ4 stdin requires end of file — SOUND** (needed to refuse trailing bytes; one deadline for the whole read, measured).
5. **DQ5 position of the `identity:` line — SOUND** (default output identical in shape and order to main; RAN).
6. **DQ6 a repeated option is a usage error — SOUND** (exit 2, nothing created; RAN).
7. **DQ7 a path beginning with `-` refused — SOUND** (`./-x` works; RAN `--identity-file --identity-stdin` → exit 2).
8. **DQ8 `InconsistentKeys::Unknown` is a refusal — SOUND** (stricter than rustls; unreachable with ring, G31).
9. **DQ9 certificate names from `--listen` — SOUND** (cosmetic; the client pins the hash only, and N5 shows names, validity and CA flags are not consulted).
10. **DQ10 tokio feature `io-std` — SOUND** (no new package, Cargo.lock and the package graph unchanged; RAN `cargo tree`). Friday may still want it recorded as a dependency-line change.
11. **DQ11 I-11 not decided — SOUND / NEEDS THE OWNER** (correctly left to Kam; the option is built, its use is the daemon lane's).

## 6. Merge results

- `origin/main` = `18005d6` = the branch base, an ancestor of head: `git merge origin/main` in a scratch branch → "Already up to date"; the tree hash after the merge equals head's (`4154850d1f37…`), so the five `check.sh` runs above are the merged tree's results (exit 0, 293/0/5).
- Trial merge of `origin/m1-daemon` (`d8b5b4b`) into a scratch branch at head: **one textual conflict, in `BACKLOG.md`** (both branches appended; one hunk). No conflict in any `crates/coagent-cli` or `crates/coagent-relay` file; `Cargo.toml`/`Cargo.lock` auto-merged (the daemon branch's additions). Merge aborted; that branch was not judged. (Its relay-child banner reader uses `url: `/`fingerprint: `, which a default start prints unchanged.)

## 7. What the gate could not do

- Run as a second user (no sudo): the foreign-owner and foreign-ACL cases are REASONED, plus the builder's injected-uid test.
- Trace every file open of a default run (`fs_usage`/`dtruss` need root): replaced by empty cwd/TMPDIR/HOME before/after and an `lsof` snapshot of the running process.
- Build or run on Windows or Linux; the Windows branch was only compiled on this host by flipping its `cfg` (G43).
- Race the TOCTOU windows for real (they need a second user or root to matter); they are reasoned in §3.
- A Unix socket at the path was not run (the scratch path is longer than the AF_UNIX limit); it takes the same branch as the FIFO, which was run.

## 8. For the owner, in plain words

1. A saved relay identity lets joiners reconnect after you restart the relay, and they still refuse any other relay that pretends to be it — the gate checked this end to end.
2. Anyone who gets a copy of the identity file can pose as your relay: they would see who connects, when and how much, and could cut people off; they still cannot read what is said.
3. On a Mac, the program checks the file's ordinary permissions but not the extra "sharing" rules Finder or `chmod +a` can add; keep the file in a private folder of your own that you have never shared, and do not add people to it in Finder's "Sharing & Permissions".
4. Anyone who has seen two of your invitations can tell they came from the same relay; use the saved identity only for a relay you mean to keep.
5. If the relay ever says `created` when you expected `loaded`, or the fingerprint changes, stop and check the path and the file before sending new invitations; delete stray `.…tmp-…` files next to it, which can hold the key after a crash.
