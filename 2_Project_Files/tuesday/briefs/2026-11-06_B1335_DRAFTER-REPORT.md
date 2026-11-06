STARTABLE: YES

# B1335 SEAT-N102 drafter report (NexusAI RD-573, jest port band), drafted 2026-11-06 15:42 to 15:50 AEDT

## BLUF
Kit written, 91 lines, 8 four-underscore slots (control: grep count 8), slots file with 8 keys. Nothing in the lane needs a customer-facing word, a ruling or a hosted touch (test infrastructure only, helper plus a new test plus the counts file). Two things differ from the sweep: the counts pair is 5327/319 now, not 5314/318 (RD-798 landed as `a5fdf1d4`), and the port block 9350-9359 is the live block of gate pane G354 (D-3).

## Facts re-measured (instrument, control)
- main `15b1426fb41b325b6bf4dc2996b995213ff3f2be` by `gh api -X GET branches/main`; open PRs 0; `heads/b1335` and `heads/rd573` length 0, control `heads/b13` length 1 (`b1317/...`). `ls-remote` over ssh failed ("Repository not found": no deploy key in this shell), so refs were read by API only.
- Helper at that sha, `grep -n`: `:62 BAND_BASE = 39000`, `:66 SLOT_COUNT = floor((49152 - BAND_BASE)/SLOT_SPAN)` (15 slots, top 48600), comment `:55-:56`. Blob `bb45cd78...`; counts blob `aadcc165...`, `:4 5327`, `:5 319`. Helper last changed 2026-09-29 (`67b840b8`).
- Why 39000: `e952f3b9` (RD-203, 2026-09-02) chose it with a comment claiming "below the ephemeral range macOS and Linux allocate from" (wrong for Linux); RD-591 `a2a93b2b` kept it ("clear of RD-490's 38900-38939"). Not measured against a kernel by anyone.
- Callers: 68 files under `__tests__/` and `tests/` name `reservePort|listenInBand|listenOnReservedPort` (5 helpers, 63 tests; control: the helper itself matches). 40 name a child-process verb, 33 pass PORT by env/flag. The ticket's "25" was NOT reproduced in any frame.
- Fixed-port census (frame: all text in the tarball minus node_modules/lockfile, port-context regex, 318 hits; control fires on 3001 x120 and 39000 x1): nothing between 14076 and 32767. The 13958/14075 hits are line numbers in HISTORY.md, 27001/27018 etc. are not ports. Candidate base 20000 / ceiling 32768 / 19 slots / top 32160.
- Existing cell `rd591-cross-seat-isolation.test.js:108` (A2) judges only `<= 49152` (macOS), so it never saw the Linux gap and stays green after the move.
- This Mac: sysctl 49152-65535, no `/proc/sys/net/ipv4/ip_local_port_range`. CI: `build.yml:17 ubuntu-latest`. Linux range 32768-60999 is the ticket's figure, UNMEASURED by me.
- Merge: CLARIFICATIONS.md:2067 quoted (merge commit, never squash); `deploy-demo.yml:27-:32` triggers on push to main and `tests/**` does not match `__tests__/`, so a merge triggers the workflow; vars total_count 0, newest three runs skipped (control: 4412 runs).
- Ports: `lsof 9350-9359` 0 lines now (control 7000: 3), but the scan of the 45 non-`.pre-` SEAT kits of 5-6 Nov hits 3 files (B1326, B1328, B1330): G354 holds 9350-9359 and its pane is live. `9370-9379`: lsof 0, kit scan 0 hits. No listener on this Mac in 14076-32767.
- Model: `model-routing.md:92` C2, `:109` G2, `models_latest.json:23 claude-sonnet-5-5`.

## D-decisions (mine)
- D-1: cells E0 (sampler control), E1 (Linux default range, constants, red at base on any host), E2 (live host range: /proc on Linux, sysctl on darwin, named failure elsewhere), E3 (runner shape: 64 held loopback dials, control that samples are in the live range), E4 (clear of fixed ports). The new file imports only exports that exist at the base blob, so the base red is an assertion, not a setup failure (that is F-A1 applied to this cell).
- D-2: F-A3, F-A4, F-B1 left out (sweep quoted F-A2 and F-A1 only); recorded as HOLDS and D8.
- D-3: the kit names block 9370-9379 instead of the assigned 9350-9359. The seat types no port, so the effect is only the reservation line.
- D-4: honest limit written into the kit: on a Mac only E1 can be red at the base; E2 and E3 can redden only on a host whose ephemeral low is under the band top (CI). No Linux red is measured by anyone before the PR's Build.

## Q-questions for Tuesday (each with a default)
- Q-1: base value. Default 20000 with a named ceiling 32768 (19 slots). Alternative: keep 15 slots by a lower base. 27017 (Mongo) lies in the band but the bind proof skips it.
- Q-2: widen scope to F-A3 and F-A4? Default no.
- Q-3: E3 (real sockets through `listenInBand`, guarded). Default include; the seat STOPs if the guard interferes.
- Q-4: port block. Default 9370-9379 (see D-3); override in S3 if you prefer the assigned block.
- Q-5: other platforms in E2. Default a named failure, not a pass.
- Q-6: Linux-kernel re-measure that the ticket's first comment asks the gate to make (the earlier tester used Docker, which this kit forbids the seat). Default: gate G2 Sonnet is asked whether it has a Linux host; if not, the PR's Build on ubuntu-latest is the only Linux read and says so. This is the one item I think may be underweighted: a Sonnet G2 gate cannot reproduce the base red on Linux.
- Q-7: stale old-band comments in other files (listed in D8). Default leave, record.
- Q-8: N103 partition: B1336 not yet written, so its side is UNMEASURED; default stamp it from that kit.

## UNMEASURED
Linux runner's actual `ip_local_port_range`; whether E3's 64 in-process dials pass the guard cleanly (seat measures); whether the ticket's 25 files reproduce; hosted CodeQL on the added lines; N103's paths.

## Outside the fences
None known. Reads: DRAFTER_RULES, the B1317 kit and slots, SWEEP-1006 lines 70-90, model-routing and models_latest lines, project CLAUDE.md and CLARIFICATIONS.md (local, read-only), Jira GETs for RD-573, RD-757, RD-490, RD-591 (and RD-99999999 control, 404) through the project's `b774lib.py`, `gh api -X GET` under the project GH_CONFIG_DIR (tarball into the scratchpad), `lsof`, `tmux list-panes`, `sysctl`, one failed `git ls-remote` (no key; read verb, no harm). No decision_queue, no hosted host, no store-listing verb. Scratch files: the session scratchpad only.
