| id | mutation | result | caught by (first) / says |
|---|---|---|---|
| G01 | parent must be a directory: check removed | **SURVIVED** |  |
| G02 | parent mode: OTHER bits ignored (mask 0o070) | RED | refused_parent_open_to_others — "an identity in a directory open to others was loaded (other, mode 701)" |
| G03 | parent mode: GROUP bits ignored (mask 0o007) | RED | refused_parent_open_to_others — "an identity in a directory open to others was loaded (group, mode 750)" |
| G04 | file mode: OTHER bits ignored (mask 0o070) | RED | refused_file_open_to_group_or_others — "a group-readable identity was loaded (other read)" |
| G05 | file mode: GROUP bits ignored (mask 0o007) | RED | a_group_readable_identity_is_refused_and_never_repaired — "a group-readable identity: the relay listened" |
| G06 | file mode: only read bits checked (mask 0o044) | RED | refused_file_open_to_group_or_others — "a group-readable identity was loaded (group write)" |
| G07 | directory-at-path branch removed (falls to not-regular) | RED | refused_directory_at_the_path — "a directory at the path: the refusal does not say "is a directory"" |
| G08 | regular-file check removed (a FIFO would be opened) | RED | refused_fifo_at_the_path_without_blocking — "a FIFO at the path was opened: the start blocked for 10 s" |
| G09 | size cap off by one (>= : a file of exactly the cap refused) | RED | an_identity_file_over_the_cap_is_refused_before_reading — "unexpected refusal: exact.identity: the id" |
| G10 | size cap loosened to 1 MiB in the pre-read check | RED | refused_file_over_the_cap — "over the cap: the refusal does not say "larger than"" |
| G11 | file read bound loosened (take cap+1 -> 1 MiB) | **SURVIVED** |  |
| G12 | post-read bound removed (builder: equivalent) | **SURVIVED** |  |
| G13 | fd re-check (fstat) removed | RED | the_opened_file_is_checked_again — "the opened file was not checked again: a group-readable identity was loaded" |
| G14 | temp file not exclusive (create+truncate) | RED | the_temporary_file_is_exclusive_and_never_follows_a_link — "the key was written through a planted symbolic link" |
| G15 | temp file created 0660 | RED | a_created_identity_file_is_private_and_alone — "assertion `left == right` failed: the created file is readable by others (mode 660; the program ran under umas" |
| G16 | temp name leaked on success (forget the guard) | RED | a_created_identity_file_is_private_and_alone — "assertion `left == right` failed: the directory holds more than the identity file" |
| G17 | file fsync removed | **SURVIVED** |  |
| G18 | parent judged without following a link (stricter) | **SURVIVED** |  |
| G19 | the GRANDPARENT is checked instead of the parent | RED | leftover_temporary_files_are_removed_at_the_next_start — "assertion `left == right` failed: a leftover temporary file survived the next start (or another file was remov" |
| G20 | current uid = the group id | RED | leftover_temporary_files_are_removed_at_the_next_start — "the relay did not print its banner within 20 s" |
| G21 | AlreadyExists on link reported as a generic I/O error | RED | create_never_replaces_an_existing_file — "refused for another reason: relay.id" |
| G22 | a load that hits NotFound (race) ... create on any metadata error | **SURVIVED** |  |
| G23 | stdin: empty input not reported as Nothing | RED | stdin_closed_empty_is_refused — "empty standard input: the refusal does not say "nothing was received"" |
| G24 | stdin: TooLarge test off (left to from_blob) | RED | stdin_flood_is_refused_having_read_at_most_the_cap_plus_one — "oversize standard input: the refusal does not say "more than 16384 bytes"" |
| G25 | stdin deadline constant 5 s -> 30 s | RED | stdin_with_nothing_written_exits_within_the_deadline — "the relay was still waiting after the deadline (5 s + 10 s)" |
| G26 | stdin cap loosened (cap+1 -> 1 MiB) | RED | stdin_flood_is_refused_having_read_at_most_the_cap_plus_one — "more than the cap was read: coagent relay: more than 16384 bytes arrived on standard input; refused after read" |
| G27 | caller passes a one-day deadline | RED | stdin_with_nothing_written_exits_within_the_deadline — "the relay was still waiting after the deadline (5 s + 10 s)" |
| G28 | any version line accepted | RED | blob_refusals_through_both_options — "version 2: the relay listened" |
| G29 | unknown version reported as wrong header | RED | blob_refusals_through_both_options — "version 2: the refusal does not say "version"" |
| G30 | no newline: always 'truncated header' | RED | a_blob_with_a_wrong_first_line_is_refused — "assertion `left == right` failed" |
| G31 | InconsistentKeys::Unknown passes (as rustls does) | **SURVIVED** |  |
| G32 | unparseable certificate accepted | RED | garbage_in_the_key_or_certificate_part_is_refused — "accepted" |
| G33 | fingerprint computed over the key, not the stored certificate | RED | a_saved_identity_survives_a_restart — "assertion `left == right` failed: the second fingerprint differs from the first" |
| G34 | export cap check removed | **SURVIVED** |  |
| G35 | export writes the certificate length for both parts | RED | a_mismatched_key_is_refused_before_listening_through_both_options — "assertion `left == right` failed: key, then the 32-byte certificate hash" |
| G36 | IdentityBlob Debug prints its bytes | RED | gate::g07_debug_display_never_holds_key — "key in IdentityBlob([byte list…]" |
| G37 | import cap off by one (> -> >= : a blob of exactly the cap refused) | RED | the_import_cap_is_exactly_16_kib — "a blob of exactly the cap was refused for size or misjudged: Err(TooLarge { len: 16384 })" |
| G38 | a path starting with '-' accepted | RED | args::tests::refusals — "relay --identity-file --identity-stdin" |
| G39 | --identity-stdin overrides silently (no exclusivity on this side) | RED | args::tests::refusals — "relay --identity-file a --identity-stdin" |
| G40 | resolved identity not handed to the relay | RED | a_saved_identity_survives_a_restart — "a client pinned to the first start could not connect to the second: Err("tls handshake: unexpected error: cert" |
| G41 | identity refusal exits 0 | RED | a_group_readable_identity_is_refused_and_never_repaired — "a group-readable identity: expected a non-zero exit, got Some(0)" |
| G42 | identity line printed BEFORE the banner | RED | a_created_identity_file_is_private_and_alone — "["identity: saved, loaded relay.identi" |
| G43 | Windows branch compiled on unix (cfgs swapped) | RED | a_created_identity_file_is_private_and_alone — "the relay did not print its banner within 20 s" |
| G44 | the stdin error text carries the raw error kind of rustls (n/a) -> file error prints the blob length only | RED | a_mismatched_key_is_refused_before_listening_through_both_options — "the key appeared in standard error (decimal byte list)" |
| N01 | hash check weakened to the first byte only | RED | blob_refusals_through_both_options — "certificate hash damaged: the relay listened" |
| N02 | export stores a zero hash | RED | a_created_identity_file_is_private_and_alone — "the relay did not print its banner within 20 s" |
| N03 | export stores no hash | RED | a_mismatched_key_is_refused_before_listening_through_both_options — "assertion `left == right` failed: key, then the 32-byte certificate hash" |
| N04 | one trailing byte after the hash accepted | RED | blob_refusals_through_both_options — "one trailing byte: the relay listened" |
| N05 | a v1 line accepted as current | RED | blob_refusals_through_both_options — "version 1 (the round-1 layout, no hash): the refusal does not say "version"" |
| N06 | a v2 line accepted as current | RED | blob_refusals_through_both_options — "version 2: the relay listened" |
| N07 | a CRLF v3 line accepted | **SURVIVED** |  |
| N08 | hash mismatch reported as TrailingBytes (own error lost) | RED | blob_refusals_through_both_options — "certificate hash damaged: the refusal does not say "damaged or was edited"" |
| N09 | missing hash reported as a truncated key | RED | a_blob_truncated_at_every_byte_position_is_refused — "assertion `left == right` failed: truncated to 536 of 568 bytes" |
| N10 | key-belongs check result ignored | RED | a_mismatched_key_is_refused_before_listening_through_both_options — "a mismatched key was accepted and the relay listened (or bound before refusing): coagent relay: TLS setup fail" |
| N11 | Fingerprint::of_certificate hashes the wrong bytes | RED | blob_refusals_through_both_options — "range start index 1 out of range for slice of length 0" |
| N12 | fingerprint taken from the stored hash, hash check removed | RED | blob_refusals_through_both_options — "certificate hash damaged: the relay listened" |
| N13 | pattern: leading dot not required | RED | leftover_temporary_files_are_removed_at_the_next_start — "assertion `left == right` failed: a leftover temporary file survived the next start (or another file was remov" |
| N14 | pattern: digits not required | RED | the_leftover_pattern_is_exact — ".relay.identity.tmp-1-2x" |
| N15 | pattern: second number not checked | RED | the_leftover_pattern_is_exact — ".relay.identity.tmp-1-" |
| N16 | pattern: empty numbers allowed | RED | the_leftover_pattern_is_exact — ".relay.identity.tmp-1-" |
| N17 | pattern: any identity name's leftovers match | RED | leftover_temporary_files_are_removed_at_the_next_start — "assertion `left == right` failed: a leftover temporary file survived the next start (or another file was remov" |
| N18 | cleanup: only directories refused (symlink/FIFO removed) | RED | a_suspicious_leftover_is_left_alone_and_refuses_the_start — "symbolic link: the refusal does not say "not a regular file"" |
| N19 | cleanup: metadata follows links | RED | a_suspicious_leftover_is_left_alone_and_refuses_the_start — "symbolic link: the relay listened" |
| N20 | cleanup: owner check removed | **SURVIVED** |  |
| N21 | cleanup: other bits ignored (mask 0o070) | **SURVIVED** |  |
| N22 | cleanup: group bits ignored (mask 0o007) | RED | a_suspicious_leftover_is_left_alone_and_refuses_the_start — "group-readable: the relay listened" |
| N23 | cleanup: suspicious match skipped, others removed, start proceeds | RED | a_suspicious_leftover_is_left_alone_and_refuses_the_start — "group-readable: the relay listened" |
| N24 | cleanup runs BEFORE the parent check | **SURVIVED** |  |
| N25 | cleanup count reported as 0 | RED | leftover_temporary_files_are_removed_at_the_next_start — "1794897523 relay listening on 127.0.0.1:64937 (certificate sha256:…)" |
| N26 | cleanup removal error ignored | **SURVIVED** |  |
| N27 | create's temp name no longer matches the cleanup pattern | RED | a_killed_create_leaves_nothing_after_the_next_start — "assertion `left == right` failed: a leftover temporary file survived the next start" |
| N28 | a planted file at the temp name is removed on EEXIST | RED | the_temporary_file_is_exclusive_and_never_follows_a_link — "called `Result::unwrap()` on an `Err` value: Os { code: 2, kind: NotFound, message: "No such file or directory" |
| N29 | cleanup message not printed | RED | leftover_temporary_files_are_removed_at_the_next_start — "1794897599 relay listening on 127.0.0.1:65405 (certificate sha256:…)" |
| N30 | cleanup line printed on stdout | RED | leftover_temporary_files_are_removed_at_the_next_start — "1794897632 relay listening on 127.0.0.1:49255 (certificate sha256:…)" |
| N31 | stdin limit cap+2 | RED | stdin_flood_is_refused_having_read_at_most_the_cap_plus_one — "more than the cap was read: coagent relay: more than 16384 bytes arrived on standard input; refused after read" |
| N32 | stdin read through a BufReader again | RED | stdin_is_consumed_at_most_the_cap_plus_one_at_the_descriptor — "the relay consumed more than the cap plus one byte from its standard input: 16386 of 16386" |
| N33 | deadline message reports 0 bytes | **SURVIVED** |  |
| N34 | stdin TooLarge threshold off by one (>=) | RED | stdin_flood_reader_takes_at_most_the_cap_plus_one — "called `Result::unwrap()` on an `Err` value: TooLarge { bytes_read: 16384 }" |
| N35 | early non-loopback refusal exits 0 | RED | non_loopback_listen_is_refused_without_the_flag_and_nothing_is_started — "assertion `left == right` failed" |
| N36 | early refusal ignores --allow-non-loopback (always refuses non-loopback) | **SURVIVED** |  |
80
