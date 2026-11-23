VERDICT: GO WITH NOTES — head ce7276c86aaaa222c1622620a2e8b4734fb3a187
# QA-W-GATE-TEST-R2: the one short check of the fix round of `w-gate-test` (ADDENDUM 11) and the merge of main (ADDENDUM 12)

Seat QA-W-GATE-TEST-R2, 2026-11-23. Brief: `FRIDAY/2_Project_Files/friday/briefs_drafts/2026-11-23_coagent_QA-W-GATE-TEST-R2_check_brief.md`.
Tags: **TESTED** = I ran it (Mac, in my own clone, 0 model runs); **READ** = I read it. Ground truth: the PC's saved mails in
`FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/windows/` (READ-ONLY). My scripts and their outputs:
`FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_w_gate_test_r2_tests/` (none of them holds an id, a name or
the work folder: checked by grep).

## BLUF
1. **The session ids are gone from what would merge.** My own byte scan of every committed file finds 0 session ids, 0 prompt
   ids, 0 real tool-use ids and 0 UUIDs of any kind in the 37 files this branch adds or changes against main. The same scan finds
   all 34 session ids at `3838bd5`. They remain in history only: commits `3330813`, `462faca` and `8044dc0`, as ruled, with no
   rewrite. Older session ids also remain in main's own older spikes, which this branch does not touch.
2. **The committed runner is still the one that ran on the PC.** `w1.py`, `run.ps1` and `cases.tsv`, and every code file of the
   lane's folders, are byte-identical to `462faca` (the last sitting). The only code files added are the two re-judge programs.
   They are byte-identical to the ones outside the branch and still give 0 cases with an issue on the saved mails. Selftest: 44 PASS.
3. **The round and the merge changed only what they were meant to change.** All 14 raw copies differ from their mails only in
   ruled placeholders. Each placeholder stands for its own class, and the counts equal those in the headers. The M2 sentence holds
   for every case it names, in both sittings. The merge kept both sides byte for byte. **One Minor:** a number in RESULT.md was
   true one commit earlier and is now stale (the committed copy's line is 4,030 characters, not "4,054 again"). It is about the
   copy, not about what the PC returned. **Verdict: GO WITH NOTES.**

## Head, previous head and main (TESTED)
- `git ls-remote` against GitHub (deploy key): `refs/heads/w-gate-test` = `ce7276c86aaaa222c1622620a2e8b4734fb3a187`,
  `refs/heads/main` = `20785c3e9389ac2275cdfda2ec7fb55eb1176425`, as the brief says.
- `git merge-base --is-ancestor <x> ce7276c` is true for `3838bd5`, `20785c3`, `462faca`, `9bbc466` and `3768a67`: no history
  was rewritten.
- History since `3838bd5`: `9bbc466` (the ADDENDUM 11 round), then `e013029` (a merge with parents `9bbc466` and `20785c3`),
  then `ce7276c` (ADDENDUM 12 ruling 2: 2 files, 4 lines).
- The builder's STATUS ends `ce7276c…` and then `READY FOR QA W-GATE-TEST r3`, as the brief requires.

## 1. Scope and ancestry (TESTED)
- `git diff --name-status 3838bd5..ce7276c`, apart from `spikes/U-B1-hook-allow-silent/` (main's, see 6): 14 paths, all in
  the owned set. The 2 documents are M, `RESULT.md` and `cases.md` are M, the 8 raw copies of stage B parts 2-4, stage C and
  last-sitting parts 1-4 are M, and the two re-judge programs are A. This is exactly the builder's list.
- `main...head`: 35 A, 2 M (`BACKLOG.md`, `docs/M0-OUTCOMES.md`). Paths outside `spikes/W1-windows-exec-hook/`,
  `spikes/W4-windows-paths/`, `preview/plugin-template-windows/` and the two documents: 0. Control: the same filter flags a
  made-up `crates/x`.
- Product diff `main..head` over `crates scripts preview/lib preview/plugin-template preview/make-plugin.sh Cargo.toml
  Cargo.lock`: **0 bytes**. Control: the same command over the last commit that touched `crates/` (`a074aca`) gives 23,816 bytes.

## 2. The ids (TESTED: `idscan.py`, bytes of every blob in the tree, hex case-insensitive)
Classes: any UUID; a `session_id` value; a UUID inside `transcript_path` (`…\<uuid>.jsonl`); a `prompt_id` value; `toolu_…`;
an event `"uuid"` value; `req_…`; `msg_…`. "Lane files" = the blobs that differ from main's at `20785c3`.

| Class (lane files) | `3838bd5` (positive control) hits / distinct | head `ce7276c` hits / distinct |
|---|---|---|
| **session ids** (`session_id` field ∪ `transcript_path`) | **34 distinct** (34 fields + 32 paths) | **0** |
| any UUID | 100 / 68 | **0** |
| `prompt_id` value | 32 / 32 | 0 |
| `toolu_` id | 101 / 67 (97 real + 4 made-up) | **4 / 2 (made-up only)** |
| event `uuid` | 2 / 2 | 0 |
| `req_`, `msg_` | 0 | 0 |

- At `3838bd5` the scan finds the **34** session ids the first check counted, in the same 8 raw copies. That is the positive
  control, and it fires.
- **The 4 `toolu_` hits at the head are not the owner's.** `toolu_standin` appears 3 times in `mac/stand_in_claude.py`, the
  Mac stand-in for Claude Code. `toolu_w1_hookcheck` appears once in `w1.py`, its model-free hook check. Both are fixed strings
  the builder wrote into its own code. Both files are unchanged since `462faca`.
- Files identical to main carry ids of main's own older spikes (in the whole tree at the head, 59 distinct `session_id` values).
  They are not part of what this branch merges.
- **Placeholder counts in each raw header against my own count of each placeholder in the body: 0 mismatches in 14 files**
  (`rawcmp2.py`). Totals: `<session-id>` 66 (34 in `session_id` fields + 32 in `transcript_path`), `<prompt-id>` 32,
  `<tool-use-id>` 97 (65 `id` + 32 `tool_use_id`), `<event-uuid>` 2. Each one sits in the field of its own class
  (`phcontext.py`). Each of the 34 lines that carries `<session-id>` replaced one session id, not two different ones.

## 3. The raw copies (TESTED: `rawcmp2.py`, all 14 against the saved mails)
- Each copy is compared with its saved mail line by line, after the 5 mail-header lines are dropped (WO-21 has none). The
  header's SHA-256 matches the saved mail in **14 of 14**. Line counts are equal in 14 of 14.
- Each differing line must equal the mail line with every placeholder replaced by text **of its own class**:
  - `<session-id>`, `<prompt-id>` and `<event-uuid>`: a UUID.
  - `<tool-use-id>`: `toolu_[A-Za-z0-9]+`.
  - The older work-folder and mailbox placeholders: any text, reported only by count and number of distinct originals.
- Result: **unexplained lines 0 and header mismatches 0, in all 14 copies.**
- Red controls, all on BODY lines of `stageB_WO-18_part2.txt`, each made in memory:

| Spoil | Result |
|---|---|
| line 53 `false` → `true` (a changed word) | unexplained 1 |
| line 96 `F10b` → `F10x` (a changed word on a placeholder line) | unexplained 1 |
| line 145 `false` → `<session-id>` (a placeholder over a non-UUID) | unexplained 1, and the header count is off by 1 |
| line 52 `<tool-use-id>` → `<session-id>` (wrong class) | unexplained 1, and two header counts are off |
| line 96 `"session_id":"<session-id>"` → `<prompt-id>` (same pattern, wrong name) | both header counts are off by 1 |

## 4. The runner is the one that ran (TESTED)
- `git diff --quiet 462faca ce7276c -- w1.py run.ps1 cases.tsv` (in `spikes/W1-windows-exec-hook/`): **exit 0**. Control:
  the same command for `w1.py` over `9467746..462faca` gives exit 1.
- Every `.rs`, `.toml`, `.lock`, `.ps1`, `.py` and `.tsv` file under the three lane folders, minus the two record tools:
  `git diff --quiet` **exit 0**. `--name-status` over those folders lists only the two `A` re-judge programs.
- `w1.py selftest` at the head on the Mac, with TMPDIR in my work dir: **44 PASS, 0 FAIL**, `SELFTEST PASS: 0 failed`.
- The committed `W_GATE_TEST_rejudge_returned.py` and `…_C.py` are byte-identical to `coagent/5_Project_History/`'s copies
  (`cmp` 0; sha256 `c4e35e4c…` and `5ae64f08…`).
- Run as committed on the saved mails, with `cases.tsv` from `462faca`: `CASES WITH AN ISSUE: 0` each, and 32 OK lines each.

## 5. Every changed sentence (READ + TESTED where it names a case or a number)
Every hunk of `3838bd5..9bbc466` in `RESULT.md`, `cases.md`, `docs/M0-OUTCOMES.md` and `BACKLOG.md` has an OLD/NEW pair in
the builder's STATUS, and each pair matches its hunk. **No hunk is without a pair.** The 8 raw headers' added sentence and the
two programs are named there too.

| Item | Where at head | Check | Verdict |
|---|---|---|---|
| **M2** | `RESULT.md:106-111` | TESTED (`m2check.py`, saved verdict blocks of WO-18 and WO-21). F3d/b, F4d/b, F9d/b: each name `[…\tga\debug\coagent-hook.exe --data-dir …]`. F7d/b: `no-such-coagent-hook.exe --data-dir`. F5d/b: `[…\w1-stub.exe crash]`. W3, W6, P3, P6: one error result each, whose whole text is `PreToolUse:<Write/PowerShell> hook error: coagent W1 stub daemon says deny`. All of this holds **in both sittings**. These 14 ids are the 14 blocking cases; the stub's one witness each comes from both re-judges | SUPPORTED, not wider |
| **M3** | `M0-OUTCOMES.md:115-118` | READ. The sentence is next to the two PASS statements. It says the smallest model `claude-haiku-5-5` (WO-18/WO-21 by the first check, B1/L1) and "one PC that is not a clean machine" | DONE |
| m1 | `BACKLOG.md:1278-1282`; `RESULT.md:188-190` | READ. One BACKLOG entry and one RESULT sentence. No code: runner unchanged (4) | DONE |
| m2 | `RESULT.md:112-118, 179-181`; `BACKLOG.md:1283-1287` | READ + `git grep` for fail-open. F10 is RAN with its witness; F6/F8 are REASONED from F5/F7. No other place states F6/F8 fail-open as RAN (the `cases.md` hits are the plan table). One BACKLOG entry | DONE |
| m3 | `RESULT.md:39, 41`; `M0-OUTCOMES.md:120, 126`; `BACKLOG.md:1233-1234` | READ. "RAN ON PC three times" agrees with the first check (WO-18 p1:36, WO-19:37, WO-21 p1:33). "49 MATCH, 2 INFO, 0 findings" agrees with its A8. `run.ps1:1` unchanged, as ruled | DONE (see Note n2) |
| m4 | `M0-OUTCOMES.md:116-118`; `cases.md:9, 61-63` | READ. The three unexercised things are named in both. `cases.md:9` now reads "Git present", then the look-alike | DONE |
| m5 | `spikes/W1-windows-exec-hook/W_GATE_TEST_rejudge_returned*.py`; `RESULT.md:42, 119-120, 184-185` | TESTED (4). Called record tools, not part of the runner | DONE |
| n1 | `RESULT.md:134-135` | TESTED (`n8n1check.py`). The PC's line is **4,054** (WO-19:193) ✔. The committed copy is 4,078 at `3838bd5` ✔ and 4,054 at `9bbc466` ✔, but **4,030 at the head**: ADDENDUM 12 replaced the 36-character event uuid by the 12-character `<event-uuid>`. "4,054 again now" is stale | **Minor m1 below** |
| n2 | builder STATUS:289 | READ: Developer Mode added (WO-15 p2:7) | DONE |
| n3-n5 | builder STATUS:264-266 ("what C3b needs" 9-11) | READ | DONE |
| n6 | `BACKLOG.md:1288-1292` | READ. `resolve_existing` exists at `crates/coagent-policy/src/path/mod.rs:175`. `windows.rs` exists | DONE |
| n8 | `RESULT.md:116-118, 180-181` | TESTED from the console logs: stage B F9/F10 8.8-8.9 s, the other 28 cases 3.6-6.4 s; last sitting F9/F10 8.8-8.9 s, the other 28 cases 3.5-5.0 s | SUPPORTED |
| n7 | none | READ: no change, as ruled | DONE |

**`git grep -i "without git"` at the head: 7 hits, each read in its sentence.**
- `BACKLOG.md:1234` and `M0-OUTCOMES.md:117` say what remains: "a PC without Git", and the rule of "a PC without Git".
- `cases.md:62` is the same phrase as M0-OUTCOMES.
- `BACKLOG.md:1274` and `RESULT.md:7` quote the design row.
- `spikes/W-native-windows/RESULT.md:4` is an older spike, not edited.
- `w1.py:141` is a comment ("a LOOK-ALIKE of a PC without Git").

**No hit names the tested configuration "without Git".**

## 6. The merge (TESTED: `mergecheck.py`)
**Prefix test, with its control.** For each document, main's file at `20785c3` is a byte-for-byte prefix of the head's.

| Document | Main | Head | Prefix | Control (one byte of main's copy changed) |
|---|---|---|---|---|
| `BACKLOG.md` | 202,116 bytes | 213,481 bytes | True | False |
| `docs/M0-OUTCOMES.md` | 10,208 bytes | 12,657 bytes | True | False |

**This lane's appended bytes.** Before the merge they are `9bbc466` minus its base `3768a67`; after it, the head minus
`20785c3`. They are **identical byte for byte**: 11,365 bytes (62 lines) and 2,449 bytes, so no line was dropped or altered.
In both documents the head is exactly main plus this lane's part. Control: dropping one lane line breaks the identity (False).

**Main's own side.** From `3768a67` to `20785c3`, main only appended: +8,098 and +2,849 bytes, with no line of main's changed.

**The other checks:**
- Conflict markers in the whole tree at the head: 0. Control: the same pattern finds a made marker.
- `spikes/U-B1-hook-allow-silent/` against main: `git diff --quiet` exit 0, with 247 files in each.
- The merge commit changes, against its lane parent, only main's U-B1 folder and the two documents. Against its main parent
  it changes only the lane's folders and the two documents.
- No rebase and no force: see the ancestry facts above.
- `ce7276c` changes 2 files and 4 lines: a header line and the init line in each of the two copies.

**The names scan of the other classes** (TESTED: `namescan.py`, over all 10,632 added lines of `main...head`; a positive
control per class, counts only):

| Class | Added lines | Control (hits) |
|---|---|---|
| account name | 0 | 19 (workspace CLAUDE.md) |
| home path | 0 | 1 (synthetic) |
| machine name | 0 | 1 (machine report) |
| mail address | 0 | 4 (saved WO-18 mail) |
| network address | 0 | 3 (machine report) |
| token | 0 | 1 (synthetic) |
| the helper's real work folder | 0 | 23 (saved WO-18 mail) |
| volume or workspace path | 14 | 1 (synthetic) |

The 14 volume or workspace hits are the raw headers naming the saved mails by the vault-relative path
`FRIDAY/0_Brain/reference/…`, with other hits 0 (Note n4). The id classes are in section 2.

## 7. The BACKLOG sweep line (READ: `BACKLOG.md:1266` and `:1270`)
- It names the commits that keep the ids: `3330813`, `462faca` and `8044dc0`. It also keeps the two earlier classes: `3bca92f`
  for the work folder, and the commits before `f9de425` for the mail address.
- It says the three commits keep the ids, with no history rewrite (Friday's ruling).
- It gives main's older session ids as "99 distinct by the independent check's count (QA-W-GATE-TEST verdict, section 8), not
  counted here". The count is attributed to the first check, as required.
- It does not name the init-event `uuid` class of ADDENDUM 12 (Note n3).

## Findings
| # | Severity | File and line | Finding | Suggested fix (words) |
|---|---|---|---|---|
| m1 | **Minor** | `spikes/W1-windows-exec-hook/RESULT.md:134-135` | "…and 4,054 again now that the session id is `<session-id>`". That was true at `9bbc466`. At the head the committed stage C init line is **4,030** characters, because ADDENDUM 12 then replaced the event uuid (36 characters) by `<event-uuid>` (12). The PC's figure, 4,054, is right. Only the statement about the copy is stale. I rate it Minor, not Major: it is not wider than the PC's mails, and it changes no pass. Friday may weigh it otherwise. | Say "4,030 at `ce7276c`, after the session id and the event uuid placeholders", or drop the copy's length and keep only the PC's 4,054. |
| n1 | Note | `spikes/W1-windows-exec-hook/mac/stand_in_claude.py` (3), `w1.py` (1) | `toolu_standin` and `toolu_w1_hookcheck` are the builder's own made-up ids in its stand-in code and hook check. They are not the owner's, and they are unchanged since `462faca`. | None. |
| n2 | Note | `spikes/W1-windows-exec-hook/raw/README.md:1` | "Empty until then." is stale. The folder holds 14 copies. The first check did not list it, and the round's list was closed, so leaving it was right. | One word change in a later documents round. |
| n3 | Note | `BACKLOG.md:1266/1270` | The sweep line does not name the init-event `uuid` (ADDENDUM 12). Its two values stay in history in `462faca` (stage C copy) and `8044dc0` (last sitting part 1), which the line already names for other classes. | Add "and the two init-event uuids" when the line is next touched. |
| n4 | Note | the 14 raw headers, line 1 | Each names its saved mail by the vault-relative path `FRIDAY/0_Brain/reference/…`. That is a coordinator folder name, not a volume path. It was already there at `3838bd5` and is not changed by this round. | None now. Weigh it in the publication sweep. |
| n5 | Note | main's older spikes | My own narrower count of main's distinct session ids (`session_id` values or `<uuid>.jsonl`) is 59, where the first check gave 99. The number depends on the definition. At the head, the files identical to main hold 673 distinct UUIDs in all. | The sweep should go by "any UUID", not by a count. |

**No Blocker, no Major.**

## What was NOT checked
| Item | Why | Who could check it |
|---|---|---|
| Anything on the PC, any model run, `run.ps1` itself | The brief forbids it; this round changes no runner | Not needed for this round |
| The substance already confirmed by the first check (its judge, battery, W4, stub against daemon) | Out of this round's scope; the runner and cases are byte-identical to what it checked | The first verdict stands |
| `cargo fmt`, clippy, `scripts/check.sh`, a workspace build or test suite | The brief says nothing heavy; product diff is 0 bytes | Friday's clean-clone merge check |
| The U-B1 lane's own content | It is main's, byte-identical to main; not this lane's | Its own check (ALLOW-MEASURE) |
| A rewrite or clean history | Friday ruled no rewrite; the ids stay in `3330813`, `462faca`, `8044dc0` | The publication sweep |
| The builder's STATUS sentences outside the ADDENDUM 11/12 sections | STATUS is history; the brief names the sections from "ADDENDUM 11" on | n/a |

## Housekeeping (said plainly)
- 0 model runs. Nothing sent to the PC. No push, merge, fix or edit in the project. The only project file I wrote is my STATUS.
- Work dir: `/private/tmp/claude-501/qwg2`. It holds my clone (detached at `ce7276c`, to run the selftest), the selftest's
  temporary folder and my scripts. Copies of the scripts and outputs are in the vault folder named above.
- My slip: one shell command started with `cd` into my work dir, against the brief's rule. It changed nothing, and the shell
  reset its folder.
- An earlier run of `idscan.py --detail` printed sample id values to my terminal only. The saved outputs were re-run without
  sample values.
- No process of mine is left.
