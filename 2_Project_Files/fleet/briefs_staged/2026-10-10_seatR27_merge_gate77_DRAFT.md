LAUNCH BRIEF (Seat R 27th): successor of Seat R 26th on pane `Secuura/Blockchain-R`. **A MERGE SEAT for gate77's LAST TWO already-gated PRs, landed ONE AT A TIME, in a fixed order, on `origin` `develop`.** Rows #1432, #1433, #1429, #1434 and #1436 are LANDED. Each remaining row is one docs-only keep-both MERGE-IN M (parents [row head, REAL develop]) pushed BARE through the hook to that row's PR branch, then ONE API squash onto develop on Wednesday's GO for that row. Nothing deploys. Secuura NEVER force-pushes. **You can probably land BOTH rows: neither needs the amendment unless develop moves under a pushed M. The CTX BUDGET below (MEASURED) still binds, and you wrap at the threshold with a handover naming the next row, or naming that gate77 is complete.** cloud: merge (carrying 0 Spark tasks). **No raise work.**


## SEND AMENDMENT (Wednesday fills at send; this block WINS where it differs from the text below)
- develop at send = **`<WEDNESDAY: fresh ls-remote, 40-hex, UTC time>`**. Expected `ae9bf6828f88131dfcc0b410f14c2f436903eb49` (R 26th's squash of #1436, `merged_at` 13:07:03Z, verified at source by R 26th AND by Wednesday, `…_seatR26_ANSWER_wrap.md`: ONE parent `09a7b2ec8c11`, tree `22b21d646973ae9214b73e72e15141d18fe64e1c`). **If it moved, every predicted tree below is VOID until the chain is re-run (row #1431, step R-1), and ANY move is a STOP-and-mail (no seat is live to have moved it).** Peter merges with MERGE commits and moved develop under R 26th's pushed M at ~12:0xZ (#1438, #1439): re-read develop again immediately BEFORE each push.
- The two row heads at send: **`<WEDNESDAY: ls-remote>`** #1431 expected `d715e5dfbbf2` · #1430 expected `d9928f4a8a4d` (the gate's pins; each row branch == its `refs/pull/<n>/head`).
- Live floor (Wednesday's `tmux list-panes` at send): **`<WEDNESDAY>`**. Read your own id with `$TMUX_PANE`, never with a bare `tmux display`.
- Sole live Secuura session at launch? **`<WEDNESDAY: pgrep -fl claude | grep -i -c secuura, with positive control>`**. **The boot pull, VERBATIM from `fleet/STANDING_LINES.md:436` (the rule; nothing in this brief overrides it):**
  > - **The Secuura launcher's step-1 boot pull is the PROJECT's rule; a brief does not forbid it (Wednesday, 2026-10-07, after R 7th and R 11th):** `Launch_Claude.command` pulls `2_Project_Files` at boot when the seat is the SOLE live session, and makes the sync READ-ONLY only when other sessions are live (KS-907, `:244-352`). The seat runs it before it reads any mail. Briefs therefore say: "Your launcher's boot pull (sole seat) may fast-forward the shared develop refs. RECORD it (from/to, FETCH_HEAD, the new `rev-parse --all` baseline) and carry on. AFTER boot: no fetch or pull in the shared checkout, and no write to either develop ref." Never "refuse the pull when the KS-907 line is absent": that inverts the launcher, which pulls precisely when the line is absent.

  Applied to you: the shared checkout's `develop` / `origin/develop` read **`1fba82ddb2b8`** at the drafter's read (2026-10-09T13:19:57Z; `rev-parse --all` 1,656 lines, sha256/16 `bd34017bc0224558` == R 26th's wrap value). origin `develop` is expected `ae9bf6828f88`. **Record what your boot pull did** (from/to, FETCH_HEAD, the new `rev-parse --all` baseline). R 26th found the launcher made no pull (0 live `pull`/`fetch` call sites in `Launch_Claude.command`; its trap (rr)): a no-pull outcome is valid and then R-2 is GENUINE. If a pull fast-forwarded the shared refs to `ae9bf6828f88`, the develop objects are PRESENT and R-2 for #1431 is the RECORDED NO-OP with controls; if not, R-2 is the GENUINE objects-only transfer with its ABSENT → PRESENT control. (Drafter, 13:19Z: `cat-file -t ae9bf6828f88…` fails, negative control `deadbeef…` fails, positive controls `09a7b2ec8c11` and `44753e3e7f4e` `commit`: ABSENT.)
- Usage at send: **`<WEDNESDAY: usage_gate.sh --check %, gauge age>`**.
- **MODEL: the newest Opus.** The launcher pins `claude-opus-5`; Wednesday types `/model claude-opus-5-5` into your pane **at its IDLE prompt when your plan mail arrives** and mails you a resume pointer; a tap sent mid-turn arrives as a message and does NOT switch. Put one line `MODEL: <as your session reports it>` in every STATUS / QUESTION / WRAP mail.
- Rulings on the drafter's questions: **`<WEDNESDAY fills Q-… rulings at send>`**.
- Wednesday's pane is `%0`. Send all mail to `wednesday-agent@agentmail.to`. **Every mail you send, and every mail Wednesday sends you, carries the `-R` suffix tag** (`[Secuura/Blockchain-R -> Wednesday]` / `[Wednesday -> Secuura/Blockchain-R]`); an unsuffixed tag reads FOREIGN on this lane (trap (n)).

# LAUNCH BRIEF: Seat R 27th, Secuura/Blockchain, lane R (pane `Secuura/Blockchain-R`, lane token `ra27`, lock `.push-lock-d8`). From Wednesday.
Staged by Wednesday's brief-drafting sub-agent on 2026-10-10 (read verbs only), from the predecessor's SEND brief as template; sent by Wednesday. Every value carries its instrument. Values marked **(drafter)** are a reading the drafter made with read verbs; **you RE-MEASURE them**. Values marked **(R 26th)** were measured by R 26th (handover or WRAP); **(Wednesday)** by Wednesday.

## BLUF
- **Whose / where:** repository `git@github.com:Secuura/Distributed_Secuura.git` (`origin`), base branch **`develop`**, expected **`ae9bf6828f88131dfcc0b410f14c2f436903eb49`** (R 26th's squash of #1436; ONE parent `09a7b2ec8c11a211a0ffe2a4dca87e6100345cb8`, tree `22b21d646973ae9214b73e72e15141d18fe64e1c`). Shared checkout `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` (its `.git` is the shared object store; its working tree is read-only to seats, STANDING_LINES :348).
- **The two remaining PRs, in this EXACT merge order** (gate77 Q-ORDER77): **#1431 (KS-1355) → #1430 (KS-1328, the FINAL row).** No row is reordered, skipped or batched. A NO GO, a STOP or a moved head halts the WHOLE queue at that row.
- **gate77's old final-tree prediction `550d0ef42882` is VOID** (Peter's #1438/#1439 moved the docs on develop). R-1 runs with **NO `--expect-final`**. The step trees you measure are the predictions.
- **Authority:** Kam's TESTED grant (`0_Brain/learnings/2026-09-11_secuura-we-approve-and-merge-our-own-tested-work.md`: *"FIx and merge all tickets after they are tested"*, 16:56:44; and its **17:50 EXTENSION**, *"you also have my approval to merge anything that has been finished and tested"*, 17:50:39) + gate77's GO for each row at its head (report.md sha256 `e00b1aa46018b137567f9b4d4dab620f4b3ff41d2dced7c9ee891acfcfdf04cd`, drafter `shasum`: EQUAL) + **Wednesday's signed GO per row**. The project's own rule: *"Wednesday's GO, naming the head SHA, is the approval"* (`CLAUDE.md` Merge flow).
- **ONE GO mail per PR, plus a SEPARATE ADDENDUM.** Their exact subjects are in THE GO section below. **You squash a row only on a Wednesday mail whose SUBJECT carries that row's GO string, naming THIS seat's ordinal, with DKIM/SPF/DMARC pass checked by your provenance tool.** A GO naming another seat (R 26th's for #1436, R 25th's for #1434, and earlier) is not yours.
- **Both rows are the ORIGINAL merge-in shape** (each branch has never had a merge-in; head ONE parent `0a6177ea5482`): `--expect-conflicts 2`, **`RA27_PREV_MERGE_IN` UNSET**, and the GO carries NO `previous merge-in P1` line. That line and knob exist only for a SECOND merge-in onto a row whose M is already pushed and whose develop then moved (the amendment R 26th built). If develop moves under YOUR pushed M, STOP and mail `STATUS: re-prediction on <12-hex> (Seat R 27th)`: the ruling is Wednesday's.
- **The BODY-CORRECTIONS are already inside the GATE77 bodies** (#1430 legs 3 4 8; #1431 legs 3 4 8). **You squash with the GATE77 body file, byte for byte. NEVER the PR's original text.**
- **CTX BUDGET (section below): MEASURED Δ ≈ 10 per ordinary row; threshold to START a row = 55%.** A seat cannot read its own ctx; never read your own statusline. Mail `QUESTION: ctx read (Seat R 27th)` with the plan mail and after every LANDED row.
- **Never end a turn on a "next up" line with nothing running** (STANDING_LINES :342-345).

**THE SEQUENCE.** Nothing writes a ref before step 3 (your launcher's boot pull, recorded per the SEND AMENDMENT, is the project's rule and precedes all of this).
1. **ITEM 0** (read-only + your record folder): the handover's first three, the tool copy and re-key (ordinals, scratch UUID and per-row values only: the gate77 ports are INHERITED), the gatelines exit-code check, the arms (rebuilt on #1431, a ONE-parent head), the kit self-tests, the R-1 dry chain. **Finish ITEM 0 in full before the plan mail.**
2. **The plan mail** `QUESTION: plan confirmation (Seat R 27th)` with your ctx-read request, **budgeted at ≤ 35% ctx**. **Then HOLD** (Wednesday switches your model at the idle prompt here).
3. **On Wednesday's row-1431 release** (an ANSWER carrying the release line shown in MAIL FORMATS, standing alone on its own line), run ROW STEPS R-0 to R-8 for #1431.
4. Mail `STATUS: merge-in 1431 pushed (Seat R 27th)`. WAIT for GO + ADDENDUM.
5. Squash (R-9), verify at source (R-10), mail `STATUS: merged 1431 (Seat R 27th)` + `QUESTION: ctx read (Seat R 27th)`.
6. FOLLOW-UP 3 right after #1431 is verified at source **if Wednesday's last ctx read was ≤ 62%**; else your handover carries it (see FOLLOW-UPS and Q-FU3ORDER27).
7. On Wednesday's release for #1430 → that row, **if the ctx read says ≤ 55%**. Then WRAP.

**IF AN INSTRUCTION FROM ME LOOKS WRONG, SAY SO.** 🔴 **Where your copy of a tool and this brief disagree about a gate, a knob, a path or a line number, THE TOOL WINS.** Run nothing on the disputed point; tell Wednesday what the tool says.

**WAKE:** your re-keyed `inbox_watchra1.sh` (`WATCHRA27_*`), armed in the background at boot with `timeout: 7200000` (as soon as the matcher re-key is proven). It EXITS when it fires, so re-arm it IN THE SAME ACTION that reads each mail, with `SINCE` = the newest mail you have READ (STANDING_LINES :403). Wednesday's tap usually arrives seconds BEFORE the watcher's next 60 s poll: read the inbox by API on the tap, and re-arm after the watcher fires on its own (trap (x)). After every push and every squash, LIST the inbox by API before the next ref write. Name a watcher pid only from a `ps` FILE read immediately before, **with your own shell's pid (`$$`) excluded** (trap (g)), and re-read before naming a SECOND watcher (trap (s)). Grep the fire banner `NEW WEDNESDAY MAIL FOR ME` or the `|FOR ME|` field, never bare `FOR ME` (trap (t)). Stop every watcher before WRAP and prove 0 are live, with a positive control.

## FOR R 27th, THE FIRST THREE THINGS (R 26th's handover; it is AUTHORITATIVE, so read it THERE, whole)
`/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatR26-2026-10-09.md`, **70 lines, sha256 `671820b78f2bab9e3baf814a08775c39700c9d7fbea2c0fe18b2569a875c65d1`** (drafter `shasum -a 256` + `wc -l`, 2026-10-10: EQUAL). Its section "FOR R 27th, THE FIRST THREE THINGS" binds you. In short:
1. 🔴 **The NEXT ROW is #1431 (KS-1355) on the REAL develop `ae9bf6828f88131dfcc0b410f14c2f436903eb49`.** Head `d715e5dfbbf2c301373016f2397cc9390c520dfb`, ONE parent `0a6177ea5482227e83d5045b68b8577a56326ffc` (= PR base B), branch `feature/ks-1355-stack-guard-one-line-per-project-f5-1`, END_TREE `6a0b2c28456e8b1c37cbacad0d337b7a9eca8111` (drafter `log -1 --format=%P/%T d715e5dfbbf2`: EQUAL). ORIGINAL shape (`--expect-conflicts 2`, `RA27_PREV_MERGE_IN` UNSET).
   - **R-1, VERBATIM from the handover:** `c2_merge_gate77.py chain --repo <your clone> --develop ae9bf6828f88131dfcc0b410f14c2f436903eb49 --order 1431,1430 --drop 1432,1433,1429,1434,1436 --out <fresh canonical dir>` — **NO `--expect-final`.** `--out` must not pre-exist.
   - **What R 26th measured (R 26th, `wrap/chain_for_r27.out`, rc 0, on `ae9bf6828f88`; you RE-MEASURE, never copy):** CODE-UNMOVED + READBACK PASS for both rows. **#1431 step tree `71820d50dbfa823ba3f363e9b41cf60775b95d7a`** (flow `030546822ffc64b1165cec9c17e0672be3f95b4c` / cheat `5fab0e4256f6332f5a6ec1eb11c280b171ad4274`, OURS..M 55 paths); **#1430 `4b84742d8e51e2aecd593fe824a9e1dc74ddbf85`** (flow `b68da6ff6b31644410fb25c9182d47cf03a6a974` / cheat `d2d860bdfe47d95d3ae606a556ebfdb8bacf8842`, 57 paths) = the final; ONEPASS == chain. Flow blocks `+42 / +43`, cheat `KS-1355 / KS-1328`. develop's tree `22b21d646973` == R 26th's #1436 step tree, which is why these equal its re-prediction made on `09a7b2ec8c11`.
   - **R-2 is a GENUINE objects-only transfer** (unless your boot pull brought the objects in): recipe `row1436/rp/r2.sh` in R 26th's folder (fetch from YOUR clone's PATH by SHA, `--no-tags --no-write-fetch-head`, under its own lock; refs byte-identical; ABSENT → PRESENT; closure rc read UNPIPED).
   - **`--dev-parent`** = develop's FIRST parent: `ae9bf6828f88` is a SQUASH with ONE parent `09a7b2ec8c11` → `--dev-parent-count 1`. (`09a7b2ec8c11` itself was a 2-parent merge commit: Peter merges with MERGE commits. A develop move by Peter can need `--dev-parent-count 2`: measure it, never assume.)
   - **Develop can move under you.** Re-read develop by `ls-remote` immediately BEFORE the push as well as at R-0 and R-9; the push tool does not.
2. 🔴 **Your `r 27th` re-key** (counts measured by R 26th on its copies, CASE-SENSITIVE raw — re-measure, never force; residue greps CASE-INSENSITIVE):
   - `tools/inbox_matchra1.py:102` `MINE = "r 26th"` → `"r 27th"`. `OTHER_SEATS` (`:280`): REMOVE `"r 27th"`/`"seat r 27th"` (R 26th forward-added them; raw `r 27th` = 4), ADD the predecessor's two entries (`r` + 26th ordinal, `seat r` + 26th ordinal), forward-add the 28th-ordinal pair. **Fix the `:102` inline comment too** — a bare swap leaves it crediting the wrong seat. Prove on the PARSED list (`ast.literal_eval`) and on the watcher's fire predicate `^NEW\|.*\|FOR ME` (REAL subjects from the API, join on the echoed subject, trap (u)). The matcher reads the inbox JSON on STDIN at import: a bare `import` HANGS. Drive it with `SINCE=… python3 inbox_matchra1.py < feed.json`.
   - `tools/inbox_watchra1.sh`: `WATCHRA26_` 5 occ / 5 lines = 4 LIVE (`:115-117`, `:121`) + 1 in the predecessor's header. → `WATCHRA27_*` on the 4 live sites; PREPEND your own header; banner `(Seat R 26th)` → `(Seat R 27th)`.
   - `tools/sweepra26.py` → `sweepra27.py`: `2[0-5]` → `2[0-6]` (9 occ / 5 lines); `ra26` → `ra27` incl. CONTROL 1b's planted `E='RA26_WT'` (UPPERCASE: a case-sensitive pass misses it); `seatR-26th` → `seatR-27th`. Prove on the PARSED `PATTERNS`; `--dir` is NOT repeatable; assert SHOWN == SUMMARY (trap (gg)).
   - **builder** `merge/build_addendumra26_gate77.py` (AMENDED): `RA26_` **124 occ / 74 lines** = 113 original LIVE + 1 in the predecessor's header (line 2) + **10 added by the amendment**; `RA25_` 2, both header prose. The ordinal `R 26th` appears on lines 2, 9, 141, 190, 220, 293, 525, 529: classify each LIVE vs HISTORICAL BY HAND; the GO-clause regex and the own-ordinal assert are LIVE, the `AMENDED by` and `ADDED BY HAND` notes are HISTORY. ADD the predecessor's claim string to `PREDECESSOR_CLAIMS` AND the meta-assert tuple (its claim is in develop's tip `ae9bf6828f88`); assert YOUR ordinal ABSENT from develop's tip. The amended shape stays in the file, fail-closed: knob UNSET ⇒ original shape only.
   - **Scratch UUID `053628bc-1fb2-406e-8dc3-8b8bc9cf2ad3`** (R 26th's) is in files you will RUN: `m3_args_ra26_1436.sh`, `m3_args_ra26_1436_M2.sh`, `m3_args_ra26_TEMPLATE.sh`, `run_armsra26.py`, `row1436/m7_env_1436.sh`, `row1436/rp/r2.sh`. Re-point them to YOUR session's UUID and assert 0 residue. ALSO the `REC=` record-folder paths (`seatR-26th`) inside `m3_args_*`, `r7_push_*`, `run_arms*`: R 26th's first pass MISSED these and they would have run against its folder.
   - **PREPEND headers; never token-swap a header.** R 26th's mechanical pass token-swapped the lane token INSIDE the earlier seat's header lines in 7 files and manufactured a false lineage claim (trap (hh)). Restore the predecessor's header line VERBATIM from its untouched original.
   - **Arms:** rebuild on #1431 (a ONE-parent head). Per Wednesday, **all 11 must reach their own asserts again, P1 included** — this restores A5/A7/A8/A11, which #1436's 2-parent head could not exercise.
3. 🔴 **What lied to you — carry (a)-(mm) from the predecessor's brief, plus these (R 26th's (nn)-(ww)):**
   - (nn) **zsh does not word-split a scalar — it bit R 26th TWICE.** `for f in $RUN` gave a VACUOUS residue zero; `set -- $P` counted M as "1 parent". Glob directly; read parents as `M^1`/`M^2`/`M^3`; a "files visited = N" control on every loop.
   - (oo) **A chain-written TREE exists only in YOUR clone.** A `git -C <shared checkout> diff --name-only M <T'>` printed `bad object` to stderr and `wc` counted 0 — a vacuous zero. Compute path counts in the clone.
   - (pp) trap (i) again: `"$T:Projects…"` → zsh `:P` modifier. Brace `"${T}:Projects…"`.
   - (qq) trap (j) again (6th recurrence): the BARE `tmux display-message` read `wednesday`. Pin `-t "$TMUX_PANE"` in call 1.
   - (rr) **The boot pull may not run, and that is a valid outcome** (see SEND AMENDMENT). Instruments: `FETCH_HEAD` mtime vs launch, the newest `develop` reflog entry, and `rev-parse --all` hash == `bd34017bc0224558`. Then R-2 is GENUINE.
   - (ss) `qm_gate77ra27.py` REFUSES a pre-existing `--out` (`FileExistsError`). Pass a fresh path; never `mkdir` it first.
   - (tt) **gatelines rc 3 is the FORMAT gate** ("touched no Blockchain/Dev path"), not "suite absent". An absent declared suite is rc 1 MISMATCH.
   - (uu) **Develop moved under a PUSHED M** (Peter, #1438/#1439, docs + systemTest, no row code). Every non-force shape was refused by builder `:266-269` and qm Q1 until the amendment (a second accepted shape, M2 = [P1, D]). A force-push is Kam's class and was not taken. Relevant to you only if develop moves under your pushed M; the ruling is Wednesday's.
   - (vv) An f-string `{{ }}` escape written OUTSIDE an f-string made `json.dump` crash AFTER the body was composed; curl then sent NOTHING. Always read back HTTP 200 + the stored body length.
   - (ww) Playwright went red mid-run while Schemathesis/Akto/k6 were pending. Wait for the poller's job-level CLASS; the colour alone is not a verdict.
   - (a) **`kit.json rows.<n>.subject` is the ROW HEAD's commit subject, NOT the squash subject** (and (dd) inside it). For your rows (R 26th/drafter `json.load` + `tr -d '\n' | wc -c` on `merge_inputs/<n>.squash_subject.DRAFT.txt`): **#1431 kit 67 vs declared 66; #1430 kit 63 vs declared 61.** Land ONLY from `merge_inputs/<n>.squash_subject.DRAFT.txt` / this brief's table.
   - (b) **`python3 -I` strips the script's own directory from `sys.path`:** a `ModuleNotFoundError: lib_gate77` LOAD FAILURE wears the expected selftest rc 1. Run kit scripts WITHOUT `-I`; the genuine expected rc 1 names its own cause (`CODE-UNMOVED #1427`). Control per (bb).
   - (c) **BSD `sed` has no `\b`.** Use Python `re`.
   - (d) **Raw-substring counts raise FALSE STOPs on the docs.** The claims that hold: every step a PURE insertion, every flow-number delta exactly +1, the kit's READBACK gate PASS.
   - (e) **The `.DRY` file is `subject + "\n\n" + body`** (`mergera1.py:550`); the API gets `commit_title`/`commit_message` separately (`:562`). Strip the 2 subject lines before the GATE77-prefix compare.
   - (f) `m7`'s banner named the GATED head as "PINNED" although `mergera1.py:556` pins `P["head"]` = M. Banner fixed since R 23rd's m7; you inherit the fix.
   - (g) **A `ps` capture contains your own shell's argv.** Exclude `$$`.
   - (h) **A control piped into `tail` reports `tail`'s rc.** Run controls unpiped.
   - (i) **zsh: `"$T:systemTest/…"` is a colon modifier.** Brace `"${T}:path"`.
   - (j) **The bare `tmux display-message` read `wednesday`.** Pin `-t "$TMUX_PANE"`.
   - (k) **A hard-coded check count turned the qm positive control red on a faithful M.** Keep it derived.
   - (l) **`c2_merge_gate77.py selftest` with NO arguments prints usage and exits rc 9**, not the expected rc 1. It needs `--repo --develop --out`. Read the cause.
   - (m) **Linear `searchIssues` is fuzzy.** Use exact `containsIgnoreCase` filters, TEAM-SCOPED (R 26th's unscoped `number: in:[…]` also returned PS-808 from Stuart's board); the fabricated term returns 0 there.
   - (n) **The matcher reads an UNSUFFIXED `[Wednesday -> Secuura/Blockchain]` subject as FOREIGN on this lane.** Ruled: Wednesday keeps `-R` on every mail; do not edit the matcher; its `:92-95` docstring is a lineage note.
   - (o) **chain.json's doc blobs live at `docs.flow.blob` / `docs.cheat.blob`.** Assert no compared field is `None`, plus a wrong-value arm.
   - (p) **Builder kit gap (Wednesday's kit item; do NOT edit the builder mid-batch):** on a MERGE-IN landing it parses the GO's `- END_TREE:` but asserts it only on a "behind" landing, and prints tree(M) labelled "head's own tree END_TREE" (SEEN on #1434 and #1436). **Each row, check `git log -1 --format=%T <gated head>` == the GO's `- END_TREE:` BY HAND and record it.** For #1431 that is `6a0b2c28456e…`, NOT the step tree `71820d50dbfa…`; for #1430 `d87632c85d8c…`.
   - (q) **The ADDENDUM's basis tool is `poll_actionsra27.py`** (your copy). If an ADDENDUM names any other tool, mail it, do not STOP.
   - (r) + (jj) **Schemathesis was GREEN on #1429's, #1434's AND #1436's M** — gate77's red expectation failed three times. **Record what you SEE per row; no expectation in either direction.** Read the run's FULL job list: the poller lists only FAILING jobs, so "absent from the failures" ≠ "green". pr-platform-suites on DEVELOP reads `failure`.
   - (s) A `ps` capture can hold the watcher's own poll subshell (identical argv, gone 3 s later). Re-read before naming a second watcher.
   - (t) A substring grep for `FOR ME` matches the NEGATIVE line. Grep the fire banner or the `|FOR ME|` field.
   - (u) The matcher SORTS by timestamp. Harnesses join on the echoed subject, never positionally.
   - (v) A copied per-row driver carries the previous row's 40-hex values. Re-key every 40-hex; assert none of the old row's remain (now: #1436's head `90d98754db7b…`, M2 `bb0639b7b25b…`, P1 `a9f823f61b93…`, END_TREE `43a9d3089e19…`, tree `22b21d646973…`, develop `09a7b2ec8c11…`, base `81d2e5f4c415…`, body `f67d768da94f…`).
   - (w) `gatelines…py --want` keys are test-file BASENAMES (`run_shell_suites.test.sh=59,0`), not phrases.
   - (x) Wednesday's tap usually arrives seconds BEFORE the watcher's next poll. Read by API on the tap; re-arm after the watcher fires and exits.
   - (y) **A hash-manifest parser that checked ZERO rows printed a CLEAN-looking result.** `_TOOL_HASHES_*.txt` is `<path> <hash> <lines>`, path FIRST. Assert `accounted == parsed` and `rows != []`.
   - (z) **A substring grep is not a trailer instrument.** Use `git interpret-trailers --parse` with a positive control.
   - (aa) **BLOCK is not a gate name in `chain`.** `^PASS BLOCK` and `^FAIL BLOCK` both read 0 in a chain run.
   - (bb) **A `python3 -I` control with a manual `sys.path.insert` cannot discriminate.** You never `cd`, so discriminate by running a kit script by ABSOLUTE path with and without `-I`.
   - (cc) **A ref-diff baseline that predates the predecessor's own writes.** Bound your boot by reconstruction: shared `rev-parse --all` 1,656 lines, sha256/16 `bd34017bc0224558` (drafter, 13:19Z; == R 26th's wrap value = its boot baseline `9ece24fd19b592dc` plus the one tracking ref `feature/ks-808-…` moved by its push).
   - (ee) **A release literal inside a sentence that says the release has NOT been sent.** Wednesday writes a release literal ONLY on its own line, and only when it IS the release. A release literal inside prose is NOT a release: do not act on it; mail.
   - (ff) **`while read` drops a final line with no trailing newline.** Use `|| [ -n "$w" ]`.
   - (gg) **Vacuous zeros from format mismatch.** Assert SHOWN == SUMMARY.
   - (hh) **A token swap on a docstring header manufactures a false lineage claim.** PREPEND headers; restore port notes (`m7_squash :3-:4`).
   - (kk) **KS-1201 did not leak on #1434's push:** `pushra1_ff.sh :119-127` reaps stubs itself. A bare `ps | grep -c login_stub` counts the grep itself.
   - (ll) **A GO carried a stale UPPERCASE lane token.** **Grep every GO case-insensitively for `ra26` / `R 26th` / `seatra26` / `s-ra26-` and report any hit** (mail it; prose only, not a STOP unless it lands in a parsed line).
   - (mm) **The trailer control reads 54 B by `interpret-trailers --parse` and 55 B by `%(trailers)|wc -c`**; a trailer-free M reads 0 and 1. Name the instrument with the number.

Also carried: a zsh SCALAR does not word-split (assert 0 rc-127 non-runs in every arm suite); a path-level Actions classifier can mask a new failing JOB (classify job-by-job too); background `python3` needs `-u`; Claude Code's removal-safety check blocks inline `bash -c '…'` (use script files); the floor changes after a brief is sent; run every kit self-test with a CANONICAL `TMPDIR` (not `/var` → `/private/var`).

### WHAT CHANGED since the predecessor's brief
1. Rows: #1436 LANDED (develop `ae9bf6828f88`). Two rows remain; **no `--expect-final`** (the old final is VOID).
2. Tools are AMENDED by R 26th: builder `e0de1d60f9cc3138` / 608 and qm `773c41462cbb195f` / 180 now carry a SECOND accepted merge-in shape (M2 = [P1, D]; knob `RA27_PREV_MERGE_IN` after your re-key; UNSET ⇒ original shape only, fail-closed; token-proofed 0 delete/replace opcodes). m7 is NOT edited. For #1431/#1430 leave the knob UNSET.
3. **Two kit findings from R 26th (banner-only, not edited mid-batch):** (1) the builder's summary print `M parents (3 reads): … [0]==gated head` is FALSE for the M2 shape (the assert that ran was the new one); it is not wrong for your original-shape rows, so if it prints, it is true; (2) trap (p)/(ii): `head's own tree END_TREE` prints tree(M) under the END_TREE label — hand-check END_TREE every row.
4. FOLLOW-UP 3 is now YOURS (Wednesday 13:10:13Z ruling after R 26th read 68% ctx).
5. Schemathesis was green on three real M's now (#1429, #1434, #1436).

## TOOLS
**Copy** from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-09_seatR-26th/` into `…/<date you boot>_seatR-27th/` (drafter `ls -d` on the `seatR-27th` name: confirm it does not exist yet), SAME subfolder layout (`tools/`, `merge/`, `boot/`, `merge_inputs/`, `row1436/` for the shapes). Hash each copy into `_COPY_HASHES_ra27.txt` and `cmp` it. **Never run a tool from R 26th's folder** (`$R` is the script's own dir). Keep one-shot ITEM 0 instruments in `_item0_proofs/`, OUT of the swept `tools/` dir. Expected (R 26th's `_TOOL_HASHES_ra26.txt`, 25 rows; drafter parsed it 2026-10-10 and compared the 16 handover-named hashes: all agree; re-hash all 25 yourself with `shasum -a 256 | cut -c1-16` + `wc -l`, manifest parser per trap (y)):

| tool (R 26th path) | sha256/16 | lines | your copy |
|---|---|---|---|
| `tools/inbox_matchra1.py` | `a03c5e7f406e1dfc` | 614 | same name, RE-KEYED (first-three item 2) |
| `tools/inbox_watchra1.sh` | `6c8157a06fe13ef3` | 161 | same name, `WATCHRA27_*` (4 live), banner, header PREPENDED |
| `tools/sweepra26.py` | `d6966681f18a31fc` | 277 | `sweepra27.py`: class 1-26 (9 occurrences / 5 lines) + CONTROL 1b |
| `tools/gatelinesra26.py` | `c96424eaef7778f8` | 134 | `gatelinesra27.py` (rc 0 MATCH / 1 MISMATCH / 3 N/A / 2 unreadable; `--want` basenames) |
| `tools/provenance_ra26.py` (= `merge/` copy) | `d215ce0275a6e3f9` | 91 | `provenance_ra27.py`, in BOTH `tools/` and `merge/` (m7 exits 7 without the `merge/` copy) |
| `tools/lockra1.sh` | `b7aa55e5574362e9` | 559 | UNCHANGED (lock name gate `.push-lock-d8`; WAIT entry 3 `.push-lock-g1`) |
| `tools/pushra1_ff.sh` | `dd8b1083a37fb82d` | 128 | UNCHANGED (LOCK_SEAT required) |
| `tools/mergeinra26_gate77.sh` | `acc5db6fd072713c` | 330 | `mergeinra27_gate77.sh`, seat token only |
| `tools/m3_args_ra26_1436.sh` | `4193dea93b4fa7c5` | 46 | the FIRST-merge-in shape (22 flags): write `m3_args_ra27_<n>.sh` per row, EVERY value re-derived, scratch UUID + `REC=` re-pointed. (`m3_args_ra26_1436_M2.sh` `f3f5691e51a6e613` / 43 is the SECOND-merge-in shape: reference only, not for your rows.) |
| `tools/poll_actionsra26.py` | `10bc6e20b9c982cb` | 97 | `poll_actionsra27.py` (workflow ID + job-level); the ADDENDUM basis names THIS file |
| `tools/qm_gate77ra26.py` | `773c41462cbb195f` | 180 (AMENDED) | `qm_gate77ra27.py` (`run` / `arms`; `--prev-merge-in` optional, OMIT for your rows) |
| `tools/s1_ra26.sh` | `c8268b0da0ef960c` | 37 | `s1_ra27.sh` |
| `tools/r7_push_ra26.sh` | `c017930687c682ab` | 24 | `r7_push_ra27.sh` |
| `merge/build_addendumra26_gate77.py` | `e0de1d60f9cc3138` | 608 (AMENDED) | `build_addendumra27_gate77.py` (`RA27_`, clause, PREDECESSOR_CLAIMS + meta-assert tuple, attributions restored) |
| `merge/run_armsra26.py` | `8a2b81e415a32f7f` | 163 | `run_armsra27.py`, `SCR`/`CL` re-pointed, GO-clause values re-keyed, arms rebuilt on #1431 |
| `merge/mergera1.py` | `aaf230e7d1975213` | 604 | UNCHANGED |
| `boot/m7_squashra26.sh` | `57a15378fd44bb85` | 113 | `m7_squashra27.sh` (`RA27_`, provenance/builder names; banner fix kept; `:3-:4` port notes and attribution kept) |
| `row1436/m7_env_1436.sh` | `553bf2b063f7e5a0` | 41 | the env-file SHAPE; write `m7_env_<n>.sh` per row (`M7_MERGE_IN_HEAD` fail-closed; **omit** the `PREV_MERGE_IN` export) |
| `row1436/m7_drive.sh` | `2a6ae95eb8ff16dc` | 16 | `row<n>/m7_drive.sh` (GO timestamp 2nd arg, M as REQUIRED 3rd arg asserted == the pushed M) |
| `merge/go_fixture_1436_mergein_SYNTHETIC.txt` / `…_ondevelop_SYNTHETIC.txt` | `30bcc871de9037bb` / `f31c729705b6e80d` | 22 / 21 | rebuilt on #1431 per Q-ARMSROW27 |
| `merge/addendum_fixture_gate77_SYNTHETIC.txt` | `898419553e31f8e1` | 3 | re-keyed |
| `merge_inputs/1436.squash_body.GATE77.txt` | `f67d768da94f66a6` | 50 | reference only (#1436's landed body); your rows read the GATE77 evidence files directly |

- A different hash is a STOP and a mail. Re-hash R 26th's originals at your wrap (manifest parser per trap (y)).
- 🔴 **Re-key: THE GENERIC CLAUSE BINDS, AND IT COMES FIRST: re-key EVERY lane-bearing declaration incl. LOCK_SEAT defaults, fixtures, adoption sets, record-folder paths and scratch UUIDs; keep HISTORICAL attributions; PREPEND headers, never swap; the tool wins.** That covers LOCK_SEAT values (`Secuura/Blockchain-R ra27`), env prefixes (`RA26_` → `RA27_`), ref namespaces (`seatra26` → `seatra27`), worktree names (`s-ra27-m<n>`), log/artefact names (`s-ra27-m<n>-ff-…-push.*`), fixtures, banners, GO-clause ordinals, record-folder paths (`seatR-26th` → `seatR-27th`), scratchpad UUIDs (`053628bc-…` → yours), and every live 12+-hex constant outside comments (:422). Build the token list from EVERY generation each file names (:294, :428). Print `N checked` per tool; `0 checked` is a FAIL (:339-340). Every residue grep is CASE-INSENSITIVE (trap (ll)). **The list below is an EXPECTATION, not the definition:** `ra26`→`ra27`, the 26th ordinal→27th, `s-ra26-`→`s-ra27-`, `RA26_`→`RA27_`, `WATCHRA26_`→`WATCHRA27_`, `seatra26`→`seatra27`, `seatR-26th`→`seatR-27th`, `2[0-5]`→`2[0-6]`, `053628bc-…`→ your UUID. **Raw counts are expectations from R 26th's handover, never forced:** builder `RA26_` 113 original live + 10 amendment + 1 header (124 raw / 74 lines); watcher `WATCHRA26_` 4 live + 1 header (5 raw / 5 lines). Name other seats in comments WITHOUT quote marks (:448).
- **Port cost is near zero:** every gate77 port was built, armed and accepted under R 23rd and carried by R 24th-R 26th. You RE-KEY ordinals and re-derive per-row values; you do not re-port.

### Gatelines exit code (carried; re-check because it is cheap)
- **ITEM 0 check:** drive `gatelinesra27.py` on a planted MISMATCH log (a copy of R 26th's real #1436 push log, found under its `tools/` or `row1436/` as `s-ra26-m1436-ff-…-push.out`, with one count altered, in your scratch) and on that real log UNALTERED (the MATCH control; `.rc` 0). **Want: rc ≠ 0 on the plant, rc 0 on the control, every call site reads the rc UNPIPED, `--want` keys are BASENAMES, the want-file loop survives a final line with no newline (trap (ff)).**
- **Do NOT hard-code a count.** Expected shell suites per M, measured from the hook's own output (`all N tracked shell suite(s) are reached by the runner` / `shell suites: N passed, 0 failed, 0 skipped (of N)`): **#1431 → 73; #1430 → 73** (R 26th: #1436's M carried 73 incl. its added suite; these rows add none; gate77's CI tallies). EXPECTATIONS. **A surprise is a STOP-and-mail.**

## ITEM 0: BOUNDED and read-only. Then `QUESTION: plan confirmation (Seat R 27th)`, and WAIT
Before the ANSWER, do NONE of these: take a lock; add a worktree; write a ref (your launcher's boot pull, recorded, is the project's rule and is not yours to refuse); transfer objects; install; edit a PR; write a ticket; comment. You MAY write your record folder `5_Project_History/<date you boot>_seatR-27th/` and your session scratchpad.

Measure:
- **(a) Refs, in ONE `ls-remote` saved to a file:** develop; `refs/pull/{1383,1429,1430,1431,1432,1433,1434,1436,1437}/head`; each remaining row's branch (table below); any `-ra27-` ref (expect 0; control `-ra19-`); `date -u`. **A moved row head is a STOP: mail.** A moved develop is a STOP-and-mail too (no seat is live to move it); name it; R-1 re-runs the chain only on Wednesday's ruling. (Context, not yours: `refs/pull/1436/head` and its branch read M2 `bb0639b7b25b` (merged); `refs/pull/1437/head` `b4933a457f38` = K 2nd's PR, gate79; `refs/pull/1383/head` `32e8459bc0f5`, HELD; the `-ra26-` count is `<unmeasured: you read it>`.)
- **(b) The shared store, read verbs only:** `rev-parse --all` count + sha256/16 (drafter 1,656 lines, `bd34017bc0224558`, 13:19Z); `cat-file -e` of develop `ae9bf6828f88…` (**drafter: ABSENT**; negative control `deadbeef…`; positive controls `09a7b2ec8c11`, `44753e3e7f4e`, the two row heads). Shared checkout `develop` / `origin/develop` = `1fba82ddb2b8` (drafter `rev-parse`) — record what your launcher's boot pull did to them. Locks by holder `seat` field, two polls, control in a private `mktemp -d` (:446): drafter `ls -a worktrees/ | grep -i -c push-lock` = 0 at 13:19Z (dotfile control `.seat-claim-s158`), plus the stale `lock-holder.json` / `lock-released.txt` artefact (Wednesday-ruled: leave it). Worktrees present include `s-ra26-m1436` (R 26th's, merged, 2,737 MB), `s-ra25-m1434`, `s-ra24-m1433`, `s-ra24-m1429`, `s-ra23-m1432`, the row authors' `s-f5-ks1355`, `s-f5-ks1328`, and the older `s-ra4-ks1436` (NOT yours, never reuse it) — no `s-ra27-*` (drafter `ls`: none).
- **(c) The clone:** `clone --shared --no-checkout` of the shared checkout into YOUR scratchpad; set `origin` to the GitHub URL (:410); fetch develop BY SHA under the checkout's own `core.sshCommand` with `GIT_SSH_COMMAND` unset; assert the fetched sha == ls-remote; **assert `rev-parse ae9bf6828f88^{tree}` == `22b21d646973ae9214b73e72e15141d18fe64e1c` and its ONE parent == `09a7b2ec8c11a211a0ffe2a4dca87e6100345cb8`** (Wednesday + R 26th measured; the predictions depend on it; the drafter could not: object absent from the shared store). The kit's lib refuses a write verb under `!CODING`, so `--repo` is always YOUR clone.
- **(d) The gate77 kit, re-hashed** (`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-09_gate77/`, READ-ONLY to you): `kit.json` `ec67d311b60564a1` (1,118 lines), `KIT_REPORT.md` `a02ad6bd8c115196` (160), `KIT_REPORT_ADDENDUM_1436.md` `3b85e6edaacad494` (115), `RULINGS_wednesday.md` `f1c6e2be1238398b` (111) (drafter `shasum` + `wc -l`, 2026-10-10: ALL UNCHANGED), and kit.json's `script_sha256` pins. `merge_seat_ordinal` still reads `Seat R 23rd` and `rows.1436.tier` reads `T2` — informational, NOT a STOP. The kit `--selftest`s with a CANONICAL TMPDIR, WITHOUT `python3 -I` (trap (b)) and WITH `--repo --develop --out` (trap (l)); `c2_merge_gate77.py selftest` reads 11/11 arms + gate76 calibration PASS + the six-row final PASS with an EXPECTED rc 1 naming `CODE-UNMOVED #1427` (the old six-row final is a kit self-test, not a prediction for this chain). **Then R-1 dry:** the chain in first-three item 1: want rc 0, ONEPASS == chain, step trees == the table below (in order `71820d50dbfa`, `4b84742d8e51`), CODE-UNMOVED / READBACK / XCHECK PASS (BLOCK is not a chain gate, trap (aa)). BASE-CONTAINED is a #1436-only gate and is not expected for these rows: say what the tool prints.
- **(e) The gate77 report + bodies:** `report.md` sha256 `e00b1aa4…04cd` (drafter: EQUAL); the two remaining `evidence/<n>.squash_body.GATE77.txt` by `wc -c` + `shasum -a 256` (drafter 2026-10-10: 2/2 EQUAL the table).
- **(f) Tools:** the copy receipt; the re-key (first-three item 2) with raw counts before/after per tool, LIVE vs HISTORICAL named, and a 0-residue assert (case-insensitive) for `ra26`, `RA26_`, `053628bc`, `seatR-26th` and #1436's 40-hex values in every file you will RUN; the gatelines arm; the refusal arms at their own asserts (:444) with positive controls; membership BY IMPORT on full-length real subjects from the API (R 26th's real GO subject for #1436 reads FOREIGN; an R 28th-addressed subject on your pane tag reads NOT mine; an unlisted addressee such as R 29th reads UNKNOWN ADDRESSEE; STANDING_LINES :411, :415, :417); and on the fire predicate (item 2). All in your record folder; nothing writes a ref.
- **(g) Seat facts:** `$TMUX_PANE`, then `tmux display-message -t "$TMUX_PANE" -p '#{@cockpit_name}'` with a nonexistent-option control; launcher ancestry from `ps` (the `--model`); the launcher's boot-pull effect; watcher pid from a ps FILE (`$$` excluded); `df -m /Volumes/DevMASTER` (R 26th: 365,718 MB free, 81%); every launcher preflight warning VERBATIM from `4_Credentials/.launch_preflight_last.txt`.
- **(h) Linear, read-only (exact `containsIgnoreCase` filters, TEAM-SCOPED, trap (m)):** state, assignee, newest comment and the PR attachment's `linkKind`/`status` for KS-1355 and KS-1328 (UNASSIGNED at earlier reads: **no board note is owed by you**; do not reassign it); KS-808 (expected In Progress, #1436 attachment `merged`) as a positive control; fabricated-key control (KS-99999) in ITS OWN query. **FOLLOW-UP 3 pre-read:** R 26th's ITEM 0 found 8 tickets mentioning `run-migrations.sh` (KS-808, KS-1296, KS-1443, KS-1305, KS-1401, KS-1376, KS-1054, KS-1031), none owning `:187-188`; re-run that exact search BY SYMBOL (any NEW hit that owns `:187-188` → a comment there, not a new ticket). **UNKNOWN to the drafter (no Linear read).**

**Your plan confirmation carries:** blocks (a)-(h); the boot-pull record; the re-key receipts (raw counts before/after per tool); the gatelines arm results; the launcher lines VERBATIM; the R-1 dry chain; a ctx read request. **Budget: mailed by ≤ 35% ctx** (R 26th: 36% at its plan; yours inherits the tools and only re-keys).

## THE ROWS (gate77; values COPIED from the predecessor's table and R 26th's wrap; **Wednesday re-reads before each GO**)
| gate step | PR | ticket | author (handover, sha256/16) | branch (push target) | gated head (40-hex) | END_TREE | predicted M / squash tree (R 26th, on `ae9bf6828f88`; you re-measure) |
|---|---|---|---|---|---|---|---|
| 1-5 | #1432, #1433, #1429, #1434, #1436 | KS-1410, KS-1139, KS-1449, KS-1171, KS-808 | — | — | — | — | **LANDED**: `eb19d99d3ace`, `4db6c7743a13`, `1fba82ddb2b8`, `44753e3e7f4e`, **`ae9bf6828f88131dfcc0b410f14c2f436903eb49`** (R 26th, tree `22b21d646973…`) |
| 6 | #1431 | KS-1355 (T2) | F 5th, `HANDOVER-seatF5-2026-10-08.md` `c3b79f6e2352acff` | `feature/ks-1355-stack-guard-one-line-per-project-f5-1` | `d715e5dfbbf2c301373016f2397cc9390c520dfb` | `6a0b2c28456e8b1c37cbacad0d337b7a9eca8111` | `71820d50dbfa823ba3f363e9b41cf60775b95d7a` |
| 7 | #1430 | KS-1328 (T2) | F 5th, same | `feature/ks-1328-db-retry-describe-budget-f5-1` | `d9928f4a8a4dc0ed0e16f967c8ae2df3448de877` | `d87632c85d8c28eec6ab828bb2857191df67de9c` | `4b84742d8e51e2aecd593fe824a9e1dc74ddbf85` (the NEW final; gate77's `550d0ef42882` is VOID) |

- **Drafter cross-checks (read verbs, 2026-10-10), NOT a recompute of the predictions:** each END_TREE == `log -1 --format=%T <head>` (2/2: `6a0b2c28456e`, `d87632c85d8c`); each head's one parent == `0a6177ea5482227e83d5045b68b8577a56326ffc` (2/2); F 5th's handover `c3b79f6e2352acff` EQUAL. Head == `refs/pull/<n>/head` == branch: Wednesday's ls-remote at send (the drafter's local store does not hold the pull refs).
- **Base (PR base B):** #1431, #1430 = ONE parent `0a6177ea5482227e83d5045b68b8577a56326ffc` (RAISE_BASE).
- **`--dev-parent` per row = the REAL develop's FIRST parent** (for #1431: `ae9bf6828f88`'s one parent `09a7b2ec8c11…`, with `--dev-parent-count 1`; you read it). It changes every row.
- **Predicted trees are on the chain's SIM develop.** The squash tree of row k == the M tree of row k when develop has not moved between M and the squash, so the REAL develop's tree after #1431 lands must equal `71820d50dbfa…`. A mismatch after a squash is a STOP.
- **Composed doc blobs per step (R 26th's `chain_for_r27.out`; re-derive from YOUR chain's own `<i>_<n>_<key>.html` and `git hash-object`, no `-w`):** #1431 flow `030546822ffc64b1165cec9c17e0672be3f95b4c` / cheat `5fab0e4256f6332f5a6ec1eb11c280b171ad4274` · #1430 flow `b68da6ff6b31644410fb25c9182d47cf03a6a974` / cheat `d2d860bdfe47d95d3ae606a556ebfdb8bacf8842`. (The kit's `with1427/` files are PRE-#1438/#1439 and are NOT the reference now; the old values `0ef9042a…`/`305b1ba9…`/`541220f4…`/`d85a73bb…` are VOID.)
- **Doc block numbers:** flow `42. 43.` and cheat keys `KS-1355 KS-1328`, in landing order, each appended once and LAST at its step, after #1436's `41.` / `KS-808` now on develop.

**Squash subject + body per row** (**Wednesday re-reads before each GO**; drafter 2026-10-10: bodies `wc -c` + `shasum -a 256` of `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-09-gate77/evidence/<n>.squash_body.GATE77.txt`, 2/2 EQUAL; subjects as the table, 66 / 61):
| PR | declared subject (lands byte for byte, no ` (#n)`) | chars | GATE77 body bytes | body sha256 |
|---|---|---|---|---|
| #1431 | `KS-1355: stack_guard lists a project once when its owners disagree` | 66 | 4866 | `2e5d52290c197785166b56f9d5f7a22b2a44b2a83489958693f4f7ab5f5d0909` |
| #1430 | `KS-1328: pin the kyc db-retry suite to a 60 s describe budget` | 61 | 3734 | `5d1dde094e96a19f49b71c2176227750cce52f17af3256e00b207593875ad158` |

- **Body composition (the lineage's shape, measured on #1427, #1432, #1433, #1429, #1434, #1436):** the squash body = the GATE77 file's bytes VERBATIM + `\n` + ONE `merge_note` line. Wednesday verified #1436's landed body opens with the 8,071-byte GATE77 file BYTE-EQUAL (8,070-B control differs). **Assert the GATE77 file's sha256 == the table BEFORE composing, and the composed prefix == the file AFTER** (on the body, with the `.DRY` subject lines stripped: trap (e)). Never edit, re-flow or re-hyphenate a GATE77 body; never use the PR's body.
- **The GATE77 bodies already carry:** own key only hyphenated; every foreign key de-hyphenated; 0 closing-family hits under both kit regexes; 0 attribution; NO TRAILER (by `interpret-trailers --parse`, trap (z)); **and the BODY-CORRECTIONS**. Your `.DRY` read checks each of these on the SENT body (STANDING_LINES :374).
- **M subject (Q-MSUBJ23 shape, ruled):** `Merge develop <12-hex> into the <KS-n> branch (docs keep-both, gate77 step <k>)` with k = the gate step above (#1431 = step 6, #1430 = step 7). On `ae9bf6828f88`: **82 chars** for each (drafter `printf %s | wc -c`: 82 / 82); the length for a later develop is re-measured; assert ≤ 92.

## ROW STEPS (for each row k, in order; every step for row k+1 waits for Wednesday's release for that row)
- **R-0 refs in ONE action:** `ls-remote` develop + the row's `refs/pull/<n>/head` + branch. **Row head moved = STOP.** Develop must equal the develop you just landed (or `ae9bf6828f88` for #1431). Anything else moved develop: STOP, mail, do not re-predict on your own (a foreign landing is Wednesday's to rule).
- **R-1 the chain, re-run on the REAL develop (the gate's MERGE-IN CONDITION, verbatim, minus the VOID final):** `python3 <kit>/c2_merge_gate77.py chain --repo <your clone> --develop <REAL develop now, 40-hex> --order <remaining rows, in order> --drop <every row already landed> --out <fresh canonical dir>` (no `-I`; **NO `--expect-final`**). **For #1431: `--develop ae9bf6828f88131dfcc0b410f14c2f436903eb49 --order 1431,1430 --drop 1432,1433,1429,1434,1436`; for #1430: `--order 1430 --drop 1432,1433,1429,1434,1436,1431`.** The tool refuses unless `--order` ∪ `--drop` = all seven (`c2_merge_gate77.py:291-298`). Want: rc 0; step 1 tree == the table's tree for row k; CODE-UNMOVED, READBACK and XCHECK PASS; ONEPASS == chain. **Compare chain.json by its substantive fields (pr, head, tree, `docs.flow.blob`, `docs.cheat.blob`), never by file hash; assert no compared field is `None`, plus a wrong-value arm (trap (o)).** `cmp` the step-1 composed docs against your own chain's `<i>_<n>_<key>.html` for that row, with a discriminating control.
- **R-2 objects:** if `cat-file -e <develop>` is ABSENT in the shared store (it is, for `ae9bf6828f88`, at the drafter's read), ONE objects-only transfer from YOUR clone (`fetch <clone path> <sha> --no-tags --no-write-fetch-head`) under ITS OWN `lockra1.sh` take/release, `rev-parse --all` byte-identical before/after, `cat-file -e` with positive + negative controls (R 21st's recipe, Wednesday-ruled; R 26th's `row1436/rp/r2.sh` is the shape). **R-2 is a recorded no-op ONLY when the objects are already PRESENT**: take the lock, `cat-file -e` with both controls, `rev-parse --all` byte-identical, record why no transfer was needed. Each squash you land is a new develop, so expect a transfer before #1430 too.
- **R-3 worktree (Q-WT, ruled):** `worktree add --detach /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-ra27-m<n> <gated head>` under ONE lock take, never `-b`; `rev-parse --all` byte-identical across it; RELEASE with the HOLDER FILE's pid, never `$$`. Develop must read PRESENT from INSIDE the worktree (:408). Never reuse `s-ra4-ks1436` or any other seat's worktree.
- **R-4 the merge-in M, via `mergeinra27_gate77.sh`** (takes and releases `.push-lock-d8` ITSELF; never wrap it, :377), driven by `m3_args_ra27_<n>.sh` (a bash ARRAY; all 22 flags REQUIRED and re-derived by the TOOL's own meaning; `--dev-parent` = develop's FIRST parent with its count; `--base` COMPUTED by `merge-base`; `--predicted-tree`, `--flow-blob`, `--cheat-blob` from R-1; `--expect-conflicts 2`; `--m-retain` = the local branch ref's real value; `--lock-seat 'Secuura/Blockchain-R ra27'` + `--my-ref-ns seatra27`; `--own-key <row key>`; `--head-paths` = the row's code paths from kit.json (#1431: 2; #1430: 1, kit `json.load`); `--dev-paths` = base..develop minus `Projects Documents/` (DERIVED per row from the base `0a6177ea5482`, disjoint from `--head-paths`); `--expect-ours-paths`/`--expect-dev-paths` from the chain's own push-delta line; `--vclone` = YOUR clone; `--subj` per the M-subject line above). env `PUSH_LOCK_DIR=/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/.push-lock-d8` (hoisted check), `GIT_SSH_COMMAND` UNSET.
  - **ONE docs-only keep-both merge-in M, parents EXACTLY [row head, REAL develop]** (each read separately: "is a commit", "exactly 2 parents", parent 1 ==, parent 2 ==; :424). **The two doc blobs = the chain's composition VERBATIM. Never `git merge-file --union`, never a hand edit of a conflict hunk.** Every non-doc path == git's merge. tree(M) == R-1's step tree. 0 trailers vs the control (54 B by `interpret-trailers --parse` / 55 B by `%(trailers)|wc -c`: name the instrument, trap (mm)). The tool's own `N gates CHECKED, N passed, 0 failed` / `VERDICT: PASS` + `.rc`. Then read M AT SOURCE with a wrong-value arm per fact; brace every `"${M}:${P}"`.
  - **#1431 and #1430 are ordinary one-parent heads** (unlike #1436). Their code paths: #1431 (KS-1355) 2, #1430 (KS-1328) 1. The MODE_CENSUS and `--dev-paths` are DERIVED per row and accepted as measured (Wednesday's ruling).
  - **#1429's YAML (`Blockchain/Dev/docs/openapi/secuura-api.yaml`) is ON develop.** It is a dev path for your rows; nothing regenerates it in this batch (Q-YAML1429). The in-hook leg 1 must print `OK — spec is in sync`. **A yaml drift is a RE-GATE STOP, never a regen.** (K 2nd's #1437 also regenerates this file; that is ITS merge seat's keep-both later, never yours.)
- **R-5 qm (`qm_gate77ra27.py run`, WITHOUT `--prev-merge-in`):** Q1 parents == [head, develop] (count AND order); Q2 tree(M) == predicted (STRICT); Q3 read-back + UNIQUE per doc; Q4 M's docs minus the row's block == develop's docs byte for byte; Q5 code blobs in M == the head's; Q6 the guard on tree(M) on a canonical path (12/0 is NOT tag-balance evidence, :442). Check count DERIVED, never hard-coded (trap (k)). Then P2 on the REAL M against the GO fixture re-keyed to this row (every 40-hex re-keyed, trap (v)).
- **R-6 S-1 in the pushing worktree AT M, outside the lock (the merge-in condition):** `npm ci --ignore-scripts` in `Blockchain/Dev`, `npm run build --workspace=packages/shared`, assert `packages/shared/dist/index.js` exists; `npm ci --ignore-scripts` in EVERY `systemTest/*` with a `package.json` (enumerate from `git ls-tree`, refuse on 0; R 25th found 4: akto, api-explorer, performance, playwright). **Every M carries #1435's five `package-lock.json` files.** Then legs 6 and 7 standalone (`npm run audit:gate`, `npm run audit:locks` from `Blockchain/Dev`): a NEW advisory = STOP and mail; never baseline. F-02: `ssh -T` auth probe under the repo's key + a refused-key control; never `push --dry-run` (:386-387); never set `SECUURA_ALLOW_ONDISK_KEY`. KS-1086: snapshot the five indicators + `.git/config` before and after.
- **R-7 push M BARE through the hook:** **re-read develop by `ls-remote` immediately before the push (the push tool does not).** `env -u GIT_SSH_COMMAND LOCK_SEAT='Secuura/Blockchain-R ra27' FF_DRYPROOF=1 bash <REC>/tools/pushra1_ff.sh <abs worktree> <row branch> <gated head>`, then the same without `FF_DRYPROOF` (or via your re-keyed `r7_push_ra27.sh`). The FULL preflight runs in-hook (~7 min). **Expected, not measured, on each M:** `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` (legs 3 4 8, no stack) and the shell-suite count per the gatelines section (73 / 73). Result = the tool's `.rc` + `ls-remote` (:405). rc 141 with the ref unmoved: report it, retry ONCE under the lock, never loop. **`PREFLIGHT FAILED` or a refused push = STOP. `--no-verify` is FORBIDDEN.** Quote the gate lines EXACTLY; record that the push moves the shared `refs/remotes/origin/<branch>` and leaves the local branch ref (:434). KS-1201: the push tool reaps login stubs itself; count stubs with a planted-process control (trap (kk)).
- **R-8 Actions on M** by FULL 40-hex `head_sha`, classified by WORKFLOW ID (three workflows are named `pr`) AND job-by-job, against TWO references: develop's own runs and the gated head's `pull_request` runs. Shape measured by R 26th on #1436's M (Wednesday's ADDENDUM): workflows pass 3; fails-on-develop 2 (`pr-security-gates` 287315271; `pr-platform-suites` 307901253); no-develop-run-and-fails-on-the-head 1 (`security-scan` 243569498, Dependency Audit step 7); jobs: fails-on-develop 4, no-D/fails-on-H 1, NEW 0. **Schemathesis: record per row what you see, from the FULL job list (trap (jj)); green on #1429, #1434 and #1436 although gate77 expected red; no expectation; neither colour is a STOP by itself; a NEW failing job is.** Two agreeing terminal polls + a fabricated-sha control (total_count 0). Mail `STATUS: merge-in <n> pushed (Seat R 27th)` with M, its qm, the arm result, the push's gate lines VERBATIM incl. the shell-suite count, the Actions table by workflow ID and job. WAIT.
- **R-9 the squash, on GO + ADDENDUM only:** provenance check of BOTH (arms: no record; dmarc flipped; body sha zeroed; genuine record + TAMPERED body; wrong prefix; a real signed mail passes); the GO's lines parsed by your builder's `ast`-extracted regexes, each exactly once; **a case-insensitive grep of the GO for the previous seat's tokens (trap (ll)), reported**; **the GO's `- END_TREE:` checked BY HAND == `git log -1 --format=%T <gated head>` (trap (p)/(ii))**; develop AND the PR head re-read by `ls-remote` in the SAME action (develop == the GO's D, head == M; a moved develop = STOP + `STATUS: re-prediction on <12-hex> (Seat R 27th)`); builder → `m7_env_<n>.sh` (with `M7_MERGE_IN_HEAD` exported, `RA27_PREV_MERGE_IN` UNSET) → `m7_squashra27.sh dry` (via `row<n>/m7_drive.sh <…> <GO timestamp from the API> <M>`) → READ the `.DRY` body (subject lines stripped first; ONE `Merged by Seat R 27th`; last line == the GO's merge_note; GATE77 prefix byte-equal; 0 trailers / Co-Authored-By / `Generated with`; subject byte-equal at the declared length from the TABLE, never kit.json; hyphenated key set == {own key}; 0 closing adjacency) → `m7_squashra27.sh go`, **PINNED** (`sha: <M>`). No `--admin`; HTTP 422 = meet it and STOP. Read back HTTP 200 + stored body length (trap (vv)).
- **R-10 verify at source** (`ls-remote` AND the API): squash tree == the table; "is a commit", "exactly 1 parent", "parent == the develop you merged onto", each with a wrong-value arm; 0 trailers (`interpret-trailers --parse`, non-blind on `bf277eead268`); 0 `Generated with`; landed subject == declared (no ` (#n)`); landed doc blobs == the composed blobs; "did it land" = the PR's `merged` field. Ticket BEFORE/AFTER: it must NOT walk to Done (Q-LIVE77: KS-1355 owes a live sweep; #1430 is tests-only and its ticket does not move on this merge either). A bot attachment change (`open` → `merged`) is REPORTED, never reverted. If a ticket walked: STOP, `STATUS: <KS> walked (Seat R 27th)`, never move it back. Mail `STATUS: merged <n> (Seat R 27th)` + `QUESTION: ctx read (Seat R 27th)`.

**STOP (mail, do not proceed) — the gate's list, VERBATIM:** "STOP (mail, do not proceed): CODE-UNMOVED fails / any row head moves / BASE-CONTAINED fails for #1436 / PREFLIGHT FAILED or a refused push / a chain readback fails. --no-verify is forbidden." Plus this brief's: a body sha256 ≠ the table; a predicted tree ≠ the real tree; develop moved by anyone but you (your launcher's recorded boot pull of the shared refs is not a develop move on origin); a shell-suite count ≠ the expectation; a NEW advisory at legs 6/7; a NEW failing job in Actions; a GO END_TREE ≠ the head's tree; a ticket walked to Done.

## CTX BUDGET (MEASURED; Wednesday reads, you cannot)
- **A seat cannot read its own ctx; never read your own statusline.** Wednesday reads your pane's statusline when you ask by `QUESTION: ctx read (Seat R 27th)`.
- **Measured (Wednesday's pane reads):** R 23rd 47% → 57% for #1432 (Δ 10). R 24th 37% → 52% before #1429 (Δ 15 incl. FOLLOW-UP 2 + all of #1433) → 58% after (Δ 6). R 25th 30% → 46% at the plan ANSWER (heavy ITEM 0) → 59% after #1434 (Δ 13 incl. proofs). **R 26th: 36% (plan) → 49% → 53% → 68% after #1436 INCLUDING a full re-prediction, a second merge-in M2 and the amendment build (an unusual row; not a budget for yours).** **Working Δ ≈ 10 per ordinary row incl. its follow-ups.**
- **Ceiling 65%** (lineage). **Threshold to START a row: ctx ≤ 55%.** FOLLOW-UP 3 is filed only if Wednesday's last read was ≤ 62%.
- **Expectation (drafter's arithmetic, not a measure):** ITEM 0 is LIGHT (tools inherited; re-key only): plan mail at **≤ 35%**. From 35: #1431 → ~45-48 → #1430 → ~55-58 → FU3 only if the read says ≤ 62% (or FU3 before #1430; see Q-FU3ORDER27). If a develop move forces a re-prediction (the heavy R 26th shape), expect ~68% and WRAP with #1430 as the named next row. At usage 90%+ WRAP COLD.
- **Safe boundaries:** (a) a row LANDED and verified at source; (b) M PUSHED and STATUS mailed (a successor squashes it on a GO naming ITSELF, after re-reading develop + head). **A merge-in started and not pushed is the one state that must never be left for a successor.** If you cross 65% inside R-4 → R-7, finish to the push, then wrap.
- **WRAP at the threshold, or when both rows have landed,** with a handover naming the NEXT ROW (number, head, its chain `--order`/`--drop`) — or stating that gate77 is complete (#1437, K 2nd's, waits for a K 3rd merge seat) — the real develop, and your tools by measured hash.

## THE PARTITION (from BOTH sides)
| Seat | Pane | Token / lock | Writes | Never |
|---|---|---|---|---|
| **R 27th (you)** — the ONLY live Secuura seat | `Secuura/Blockchain-R` | `ra27` / **`.push-lock-d8`**, holder JSON `{"seat": "Secuura/Blockchain-R ra27", "pid": …, "branch": …, "started_utc": …}` (the lineage format) | your launcher's recorded boot pull (project rule, :436); per row: ONE objects-only transfer (or the recorded no-op when PRESENT), ONE detached worktree `s-ra27-m<n>`, ONE merge-in M touching ONLY the two `Projects Documents/*.html` docs beyond git's merge, ONE push of M to that row's branch (its NAME adopted for that one push, gate73 Q-ADOPT10 (a) / RULINGS Q-MERGEIN76), ONE API squash on GO; FOLLOW-UP 3 under its conditions; your record folder, handover, history entry | any other push, branch or raise; any edit to a row's code; any deploy |
| **#1437** (K 2nd's PR, `refs/pull/1437/head` `b4933a457f38`, gate79 GO) | — | — | **waits for a K 3rd merge seat AFTER gate77's rows land** | **NEVER touched by you**: not merged, not pushed to, not commented, not re-predicted. Its yaml regen and its flow `44.` / cheat `KS-1402` blocks reach develop only through that later seat's keep-both. |
| K 2nd (WRAPPED) | — | `k2` / `.push-lock-g1` | nothing | worktree `s-k1-ks1402`, its branch, records, lock |
| R 26th (WRAPPED, ctx 68%) | your pane | `ra26` | nothing | `worktrees/s-ra26-m1436` (2,737 MB, left for Kam's drive-hygiene word), `clone_ra26`, its records (COPY tools, never run or edit them there) |
| R 25th, R 24th, R 23rd, R 22nd, R 21st and earlier (WRAPPED) | your pane | `ra25`, `ra24`, `ra23`… (and the older `s-ra4-ks1436`) | nothing | `worktrees/s-ra25-m1434`, `s-ra24-m1433`, `s-ra24-m1429`, `s-ra23-m1432`, `s-ra22-m1427`, `s-ra21-m1427`, `s-ra4-ks1436`, their records |
| Row authors (F 6th, F 5th; WRAPPED) | — | — | nothing | their worktrees (`s-f6-ks808`, `s-f5-ks1355`, `s-f5-ks1328`), records, handovers (READ for merge_note only); **R5: no author may be named in a GO** |
| gate77 / gate79 (CLOSED) | — | — | — | the kits and reports: READ-ONLY inputs |

- **The two-lock protocol:** your `lockra1.sh` still WAITs while `.push-lock-g1` is held (WAIT entry 3). No other seat is live, so expect no contention; attribute any lock you do find by its holder `seat` field, never by its path, and mail before touching it.
- **Shared inbox `secuura-blockchain@agentmail.to`.** Act only on mail whose subject carries `-R` AND `(Seat R 27th)`. A mail naming another seat is NOT yours, even on your pane tag (R 26th's, R 25th's and earlier GOs/ADDENDUMs/ANSWERs are in that inbox: FOREIGN). Unlisted addressee = UNKNOWN ADDRESSEE (:417). A new mail from `kreiser.org@me.com` = STOP and mail Wednesday.
- **Identity by `$TMUX_PANE`**, never a bare `tmux display` (:398).

## HOLDS
- **No merge-in write before Wednesday's release for that row (it releases R-0..R-8 for that row only; the release line stands alone on its own line in an ANSWER, MAIL FORMATS); no squash without that row's GO (+ ADDENDUM), in its SUBJECT, naming THIS seat.** One row at a time; row k+1 never starts before row k is verified at source and Wednesday's release for row k+1.
- **Project MUSTs that touch merges, docs and pushes** (read from a SHA; never from the main checkout's working tree, :348):
  - `CLAUDE.md` Merge flow: *"We approve our own work; the author merges once it is TESTED"*; **TESTED = a QA gate verdict at the PR's current head + Test Evidence + our own suites**; *"Wednesday's GO, naming the head SHA, is the approval"*; *"Untested, or no GO → no merge. Never push straight to develop."* (You are the merge seat, never the author: gate77 R5.)
  - `CLAUDE.md` Pull-request rules: never dispatch `pre-merge-platform-suites.yml` (KS-441); `mergeable_state: clean` is NOT "tested" (rows read `dirty`: expected, develop moved on the docs).
  - `CLAUDE.md` Branching: Git Flow; feature → `develop` only; nothing to `main`/`release/*`.
  - `CLAUDE.md` / `.githooks/pre-push:46-70`: **no force push, ever**; merge develop IN (:399).
  - Project-root `…/Secuura/Blockchain/CLAUDE.md` :185-194: notify Stuart and Peter **ON THE TICKETS ONLY, batched at session wrap**; **the extranet is not a channel: never post there, never `POST /api/seen`** (decline the launcher's); nobody but Kam messages the humans. (R 26th did NOT do the batched notify; it is carried to Wednesday's board pass, not yours: no mail or comment to them.)
  - `CLAUDE.md` :168-175: refer to other organisations' issues in plain words only in anything GitHub renders.
  - SKILL `secuura-test-discipline` §4: every test change updates BOTH platform-k HTML docs in the same commit; **quote the SPACE in `Projects Documents`**; never cross platforms. (Your M carries the rows' own blocks, composed; you add none.)
  - SKILL §5d: ticket comments cite `file:line`; append, never rewrite another's register; never retitle a ticket someone else authored.
  - SKILL §5f: **a runtime change does not move to Done on offline green**; report numbers, not adjectives; name what is unverified.
- **No `--no-verify`, no force push, no `-u`, no `push --dry-run`, no `--admin`.** No baseline edit, lock edit, audit-baseline entry or spec/guard/manifest edit, ever. Your launcher's boot pull is the project's rule (SEND AMENDMENT, :436): RECORD it. **AFTER boot:** no `git fetch`/`pull` in the shared checkout; `GIT_SSH_COMMAND` stays UNSET for every network verb (:416); never write either develop ref in the shared checkout by hand, and leave both where the boot pull put them (Wednesday's ruling).
- **No deploy, no `az`, no SSH (beyond the F-02 probe), no migration, no Docker, no stack.**
- **No ticket state change.** No client-facing communication beyond the facts-only ticket text in FOLLOW-UP 3. No mail or comment to Peter or Stuart. No extranet.
- **Never delete: quarantine.** Never touch any gate kit or report, another seat's worktree/lock/mail/records, or #1437 / K 2nd's anything. **Your own merged-row worktrees are LEFT in place for Kam's drive-hygiene word.**
- No secret in argv, a kept ps capture, a mail or a record file.
- Signature classes pause for Kam. A squash onto develop is irreversible: it moves ONLY on its GO.
- Never `cd`. Absolute paths; `${VAR:?}` on every path built from a variable; `-z` for paths. macOS has no `timeout`. zsh has no `PIPESTATUS`; never store a command in a variable; never name a variable `path`; brace `"${M}:…"`. Every residue grep is case-insensitive; every zero you report carries a control.

## THE GO (verbatim subjects; nothing else authorises a squash)
From `wednesday-agent@agentmail.to`, DKIM pass, the SUBJECTS EXACTLY, ONE PAIR PER ROW, sent only after that row's M is pushed and qm-green:

`[Wednesday -> Secuura/Blockchain-R] GO (Seat R 27th): merge 1431 on gate77`

`[Wednesday -> Secuura/Blockchain-R] GO (Seat R 27th): merge 1430 on gate77`

Each is followed by a SEPARATE ADDENDUM whose subject is exactly (with `<n>` the row):

`[Wednesday -> Secuura/Blockchain-R] ADDENDUM (Seat R 27th): Actions verdict for GO <n> on gate77`

carrying `ACTIONS VERDICT (Wednesday):` and `0 new failures`, its basis naming `poll_actionsra27.py`.

Your builder's GO-clause regex (re-keyed; `ast`-proved on three strings: the R 27th form matches; the R 26th and R 28th forms do not):

`GO \(Seat R 27th\): merge \d{3,5} on [a-z0-9]+`

**GO body shape (the predecessor's GO for #1436 is the template, MINUS its `previous merge-in P1` line, which belongs only to a second-merge-in row and is ABSENT here; Wednesday builds each from the ROWS tables and runs it against your `ast`-extracted regexes before sending: every line exactly once, clause fullmatch, ABSENT strings 0, residue grep CASE-INSENSITIVE for `ra26`/`R 26th`, and the merge-in knob named `RA27_MERGE_IN_HEAD`, derived from the seat). Values COPIED from the table above; Wednesday re-reads each at source before each GO:**
| builder line | #1431 | #1430 | instrument |
|---|---|---|---|
| `- develop D:` | `ae9bf6828f88131dfcc0b410f14c2f436903eb49` (if unmoved) | the develop #1431 landed as | ls-remote at GO time |
| `- PR head:` (GATED head; M rides in `RA27_MERGE_IN_HEAD`) | `d715e5dfbbf2c301373016f2397cc9390c520dfb` | `d9928f4a8a4dc0ed0e16f967c8ae2df3448de877` | ls-remote |
| `- PR base B:` | `0a6177ea5482227e83d5045b68b8577a56326ffc` | `0a6177ea5482227e83d5045b68b8577a56326ffc` | `log -1 --format=%P` |
| `- END_TREE:` (seat checks BY HAND, trap (p)) | `6a0b2c28456e8b1c37cbacad0d337b7a9eca8111` | `d87632c85d8c28eec6ab828bb2857191df67de9c` | `log -1 --format=%T` |
| `- Target tree T':` (step tree, == tree(M)) | `71820d50dbfa823ba3f363e9b41cf60775b95d7a` | `4b84742d8e51e2aecd593fe824a9e1dc74ddbf85` | chain + M |
| `flow \`Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html\` = ` | `030546822ffc64b1165cec9c17e0672be3f95b4c` | `b68da6ff6b31644410fb25c9182d47cf03a6a974` | chain + hash-object + read from M |
| `cheat \`Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html\` = ` | `5fab0e4256f6332f5a6ec1eb11c280b171ad4274` | `d2d860bdfe47d95d3ae606a556ebfdb8bacf8842` | same |
| `Declared squash subject: \`…\`` | `KS-1355: stack_guard lists a project once when its owners disagree` | `KS-1328: pin the kyc db-retry suite to a 60 s describe budget` | gate77 verdict / `merge_inputs/` |
| `N chars, LANDS N` | 66 | 61 | `printf %s \| wc -c` |
| `N bytes, sha256 …` (digits only, NO thousands comma) | `4866`, `2e5d52290c197785166b56f9d5f7a22b2a44b2a83489958693f4f7ab5f5d0909` | `3734`, `5d1dde094e96a19f49b71c2176227750cce52f17af3256e00b207593875ad158` | `wc -c` + `shasum -a 256` |
| `merge_note: \`…\`` (Q-NOTE77) | `Merged by Seat R 27th on the authority of HANDOVER-seatF5-2026-10-08.md sha256 c3b79f6e2352acff` | same | `shasum` |

All values in this table are **copied; Wednesday re-reads before each GO.**

**PRESENT in each GO:** its clause, `qm Q2 STRICT`, `qm green`, and the line "npm ci + shared build ran in the pushing worktree before the push (every M carries #1435's five lockfiles)". **ABSENT:** `NEW-FAILING`, `PENDING NONE`, any author seat name, the `previous merge-in P1` line, any `ra26` / `R 26th` token in any case.

## FOLLOW-UPS (ours, facts-only; board search BY SYMBOL first with a fabricated-term control; one ticket per logical path)
- **DONE, NOT REPEATED:** N-1432-4 (KS-1448 comment `0606604f-…`); FOLLOW-UP 2 (KS-1410 comment `03d49da2-f313-4fce-a334-fe3c19875cfd`; KS-1346 comment `efdb60a7-8727-4805-9cc7-a8ce7a2b51f2`). Do not comment again.
- **FOLLOW-UP 3 (YOURS; Wednesday 13:10:13Z ruling after R 26th read 68% ctx): Q-ERRTEXT808 → a NEW ticket related to KS-808, ONLY if Wednesday's last ctx read was ≤ 62%; otherwise your handover carries it.** `Blockchain/Dev/scripts/run-migrations.sh:187-188` still prints "the remaining applied=N-counts-skips defect is KS-808" on every failed-migration run; after #1436 (now on develop `ae9bf6828f88`) that runtime text describes a defect the code no longer has (gate77 N-1436-1, Minor). **Board search BY SYMBOL first** (exact `containsIgnoreCase`, TEAM-SCOPED, fabricated-term control in its own query): R 26th's ITEM 0 found exactly 8 hits — KS-808, KS-1296, KS-1443, KS-1305, KS-1401, KS-1376, KS-1054, KS-1031 — none owning `:187-188`. If still none: a NEW ticket related to KS-808 (KS-808 stays In Progress for its live sweep), facts-only, `file:line` read FROM A SHA at a develop that contains #1436 (never the working tree). If a new hit owns it: a comment there instead. Spec in R 26th's handover FOLLOW-UPS; the handover wins on a disagreement.
- **NOT OWED: a board note for KS-1328 being UNASSIGNED** (Wednesday's board pass). Do not reassign it.
- **N-BATCH-1..7, the `kit.json rows.<n>.subject` defect, the `merge_seat_ordinal` / `rows.1436.tier` fields, the builder END_TREE gap (trap (p)) and R 26th's stale `M parents` summary print are Wednesday's kit items, NOT yours.** Do not file them.
- **KS-808 stays In Progress** (live sweep after a deploy, §5f); its #1436 attachment flipped `open → merged` (bot; reported, not reverted).
- **Live sweeps owed (not yours to run, carried for the record):** KS-1171, KS-1139, KS-1449, KS-808; KS-1355 once landed.
- **Ticket comments are the client channel.** No extranet. Nothing to Peter or Stuart beyond facts-only ticket text (no mentions unless Wednesday rules). No ticket state changes.

## STANDING FINDINGS CARRIED (STANDING_LINES, by current line; file 448 lines, sha256/16 `72335e0c124f9f22`, drafter `shasum` + `wc -l` 2026-10-10: UNCHANGED, so its line numbers stand)
| line | finding |
|---|---|
| `:320` | a declared subject never carries `(#n)`; `len <= 92` |
| `:336` | other-seats lists; act only on a GO naming THIS seat |
| `:339` | "0 checked" is never CLEAN |
| `:342` | never end a turn on a "next up" line with nothing running |
| `:348` | read repo files from a SHA, never the main checkout's working tree |
| `:374` | a merge tool must not ADD attribution; check the SENT body |
| `:377` | a tool that takes the lock itself is never wrapped |
| `:386` | `push --dry-run` runs the hook |
| `:398` | pane id from `$TMUX_PANE` |
| `:399` | no force push, ever; MERGE develop in |
| `:400` | a fresh worktree builds `packages/shared` before its first push |
| `:403` | watcher SINCE = newest mail READ |
| `:405` | a result is the tool's `.rc` + `ls-remote` |
| `:408` | a merge-in needs develop's objects in the WORKTREE's store |
| `:409` | inherited tools fail closed on unset knobs |
| `:410` | a `clone --shared` origin is the LOCAL checkout |
| `:411` / `:415` | trap 4's FORWARD half; the untagged-arm tension |
| `:416` | never export `GIT_SSH_COMMAND` around a push tool |
| `:417` | unlisted addressee = UNKNOWN ADDRESSEE |
| `:420` | `for-each-ref` globs do not cross `/` |
| `:422` | develop parent is an argument; sweep 12+-hex constants |
| `:423` | `rev-parse <sha>:<path>` echoes on absence |
| `:424` | "ONE parent" is three reads |
| `:428` | re-key EVERY lane-bearing declaration |
| `:432` | `npm ci` in every systemTest package |
| `:434` | a worktree push moves the shared tracking ref |
| `:436` | the boot pull is the project's rule (quoted VERBATIM in the SEND AMENDMENT) |
| `:440` | authenticity gates bind the record to the BODY |
| `:442` | html_docs_matrix 12/0 is NOT tag-balance evidence |
| `:444` | a refusal arm counts only at its own assert |
| `:446` | never plant a control in the shared `worktrees/` |
| `:448` | quoted seat tokens in comments count to raw asserts |

## MAIL FORMATS
Subjects (prefix `[Secuura/Blockchain-R -> Wednesday] `; the `-R` suffix on EVERY mail):
- `QUESTION: <topic> (Seat R 27th)` (incl. `QUESTION: plan confirmation (Seat R 27th)`, `QUESTION: ctx read (Seat R 27th)`)
- `STATUS: re-prediction on <12-hex> (Seat R 27th)`
- `STATUS: objects PRESENT (Seat R 27th)` (optional; may ride in the next STATUS)
- `STATUS: merge-in <n> pushed (Seat R 27th)`
- `STATUS: merged <n> (Seat R 27th)`
- `STATUS: <KS> walked (Seat R 27th)`
- `WRAP (Seat R 27th): …`

Wednesday's releases to you come in an `[Wednesday -> Secuura/Blockchain-R] ANSWER: …` mail. The release line stands ALONE on its own line in that mail's body, and only when it IS the release; for each row it is exactly:

`START ROW 1431 (Seat R 27th)`

`START ROW 1430 (Seat R 27th)`

(each releases R-0..R-8 for that row only). The GO + ADDENDUM pair (THE GO section) then releases R-9..R-10. A release string found inside a prose sentence is NOT a release (trap (ee)): do not act on it; mail.

**The WRAP mail carries:** BLUF (rows landed, the NEXT ROW or "gate77 complete", real develop); 0 watchers live, proved; EVERY REF WRITE (the boot pull's from/to, each transfer or recorded no-op, worktree add, M commit, push + tracking-ref side effect, squash); each ticket before/after; follow-ups done (ids) or carried; UNMERGED / UNMEASURED; drive hygiene (your own merged-row worktrees + scratch clones; never another seat's; report MB); the tool hashes a successor inherits, RE-MEASURED; your handover; `MODEL:` line.

**WRAP:** verify every landed squash at source BEFORE wrapping. Handover **`5_Project_History/HANDOVER-seatR27-<date you wrap>.md`**, opening **"FOR R 28th, THE FIRST THREE THINGS"** if a row remains: (1) the NEXT ROW, the real develop, and its exact chain `--order`/`--drop`; (2) your `r 28th` traps (MINE the 28th ordinal, sweep class 1-27, fixtures, forward-add the 29th, scratch UUIDs) and your tools by MEASURED hash; (3) what lied to you (carry (a)-(ww) forward unless one is fixed at source). If both rows landed, the handover opens with "GATE77 COMPLETE" and the state of FOLLOW-UP 3, and names no next row. Insert the history entry at the TOP and prove insert-only.

## RULED BY KAM, NOT YET IN AN ARTEFACT
**`<WEDNESDAY: paste the regenerated list at send: bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered secuura- (rc, UTC time, row count). The predecessor's list held 67 rows, regenerated 2026-10-09T10:47:43Z, and was NOT re-run by this drafter (it did not touch that tool).>`**
None is in your queue. Act on NONE; if one bears on your work, mail Wednesday. (Bearing on this batch, for awareness only: `secuura-required-approvals-zero-after-the-untick` (raise-to-1, Kam applies it himself), `secuura-force-push-own-branch-standing` (narrow-allow on an agent's OWN unshared branch; the PR branches you push to are NOT yours and are shared, so it does not apply).)

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE (from `briefs_staged` ANSWERs to Blockchain-R)
Carried from earlier briefs:
- **Re-predict, not re-gate, on a develop move that touches no row path; a conflict or moved path outside the two docs IS a re-gate: STOP and mail** (`…_seatR21_ANSWER_refused.md` ruling 1). For gate77 the chain tool enforces it (CODE-UNMOVED).
- **The objects-only transfer recipe** (`…_seatR21_ANSWER_plan.md` sequencing 1).
- **The mergein's `PUSH_LOCK_DIR` check stays HOISTED** with the `.push-lock-d8` basename assert (`…_seatR21_ANSWER_ctx_hoist.md` ruling 1).
- **Not in any seat: `--no-verify`, a baseline entry, the CLEANUP rows** (`…_seatR21_ANSWER_refused.md` ruling 3).
- **chain.json is compared by substantive fields, never by file hash** (`…_seatR22_ANSWER_plan.md` ruling 4).
- **Matcher: "verify MINE", not "remove yourself from OTHER_SEATS"** (`…_seatR22_ANSWER_plan.md` ruling 6).
- **The gate kits and gate reports are READ-ONLY inputs; `--repo` = your clone, `--out` = your scratchpad** (`…_seatR22_ANSWER_plan.md` ruling 5).
- **Kit selftest on a canonical TMPDIR** (`…_seatR22_ANSWER_ctx.md` finding 2).
- **Once a merge-in starts, the safe boundary is the pushed M, not the ceiling** (`…_seatR22_ANSWER_ctx.md`).
- **Model: `/model claude-opus-5-5` typed by Wednesday at your IDLE prompt; a mid-turn tap does not switch** (`…_seatR22_ANSWER_plan.md` Model).
- **gate77 rulings binding you:** #1436 = TIER 1; `run-migrations.sh:187-188` and the KS-1452 merge subject graded by the gate (Minor, follow-up / squash replaces it); never union (R8) (`RULINGS_wednesday.md`).
- `kit.json rows.<n>.subject` is the row head's subject, NOT the squash subject; #1437 is never yours; PREDECESSOR_CLAIMS tightening ACCEPTED as a shape; gate77 ports ACCEPTED as built; each `merge-in pushed` STATUS carries the arm result, qm on the REAL M, gate lines verbatim WITH the shell-suite count, the Actions table by workflow ID and job; a board hit that owns a follow-up gets a comment, not a new ticket; merged-row worktrees stay; KS-1328 unassigned is Wednesday's.
- **Every mail to this lane carries `-R`; do not edit the matcher; its `:92-95` docstring is a lineage note** (`…_seatR24_ANSWER_plan.md` finding 3).
- **The derived `MODE_CENSUS` and `--dev-paths` are accepted as measured, per row** (`…_seatR24_ANSWER_plan.md` Detail).
- **The stale `worktrees/lock-holder.json` (F 4th, 2026-10-05, released) is an artefact, not a lock: leave it** (`…_seatR24_ANSWER_plan.md` Detail).
- **Builder END_TREE gap: Wednesday's kit item; do not edit mid-batch; the seat's hand check stands** (`…_seatR24_ANSWER_row1429.md` kit item 1). **ADDENDUM basis tool name: cosmetic; corrected per seat** (kit item 2).
- **Merged-row worktrees stay; drive hygiene is a later ruling** (`…_seatR24_ANSWER_wrap.md` item 5; `…_seatR25_ANSWER_wrap.md` step 4).
- **The boot pull is the PROJECT's rule for a sole live session (`STANDING_LINES.md:436`); a brief does not forbid it; record what it did.** After boot: no further fetch or pull in the shared checkout. **The shared refs stay where the boot pull put them; never reset them** (`…_seatR25_ANSWER_bootpull.md`).
- **R-2 is a recorded no-op ONLY when the objects are already PRESENT** (lock, `cat-file -e` with both controls, `rev-parse --all` byte-identical, reason recorded); otherwise the full transfer with its ABSENT → PRESENT control (`…_seatR25_ANSWER_bootpull.md` step 2).
- **Finish ITEM 0 in full, then send the plan confirmation**; arm the watcher as soon as the matcher re-key is proven; the launcher's "Kam picks or adjusts the plan" wording is generic boot text, not Kam speaking — the plan confirmation goes to Wednesday; if Kam types into your pane his word wins and you say so (`…_seatR25_ANSWER_item0f.md`).
- **LIVE vs HISTORICAL split accepted as the re-key method;** headers PREPENDED, never swapped; `M7_MERGE_IN_HEAD` fail-closed (`…_seatR25_ANSWER_plan.md` Accepted).
- **A release literal appears ONLY on its own line, and only when it IS the release** (trap (ee)). **Residue checks are CASE-INSENSITIVE, and the merge-in knob name in a GO is derived from the seat** (trap (ll)).
- **Schemathesis green on #1429, #1434 and #1436 where gate77 expected red: not a STOP; record per row.**
New from the ANSWERs to R 26th (2026-10-09 / 2026-10-10):
- **OPTION 2 (the second-merge-in AMENDMENT), ruled 12:24:12Z (`…_seatR26_ANSWER_M2.md`):** when develop moved under a PUSHED M and only docs moved, the seat pushes a fast-forward M2 = [P1, D]; the builder and qm accept that shape only with the knob/flag set and the GO carrying `previous merge-in P1`. **It does NOT apply to #1431 or #1430** unless develop moves under YOUR pushed M, and then only on Wednesday's ruling; for these rows the knob is UNSET.
- **Develop moved under R 26th's pushed M: RE-PREDICT was ruled, never a force-push** (`…_seatR26_ANSWER_devmoved.md`; force-push is Kam's class).
- **FOLLOW-UP 3 → R 27th, ruled 13:10:13Z (`…_seatR26_ANSWER_wrap.md`):** R 26th's ctx read 68% (> 62%), so it was NOT filed by R 26th; the ticket for `run-migrations.sh:187-188` (board search by symbol first) is yours under the ≤ 62% condition. Do not move KS-808 on the board; it stays In Progress until its own close path.
- **#1436 verified at source by Wednesday independently** (scratch clone; tree `22b21d646973…` == T'; 8,071-B GATE77 prefix byte-equal; trailers 0): your starting develop is trusted, but you still assert it in ITEM 0 (c).

## UNKNOWN / UNMEASURED (by the drafter; you measure or say so)
| item | why unknown | instrument that closes it |
|---|---|---|
| Every real M for the 2 rows, its in-hook preflight, its Actions, qm on a real M | nothing built | R-4 → R-8 |
| develop `ae9bf6828f88`'s tree `22b21d646973` and its one parent `09a7b2ec8c11` | object ABSENT from the shared store; drafter did not fetch | your clone, ITEM 0 (c) (R 26th + Wednesday measured it) |
| The R-1 dry chain on `ae9bf6828f88` with `--drop 1432,1433,1429,1434,1436` | drafter did not run it (no clone; read verbs only); R 26th's result is quoted from its WRAP/handover | ITEM 0 (d) |
| MODE_CENSUS and `--dev-paths` for #1431 / #1430 (base `0a6177ea5482`) | derived per row; drafter did not derive | arms rebuild / R-4 inputs |
| What your launcher's boot pull does this launch | depends on the floor at launch | ITEM 0 (b)/(g), recorded |
| GitHub API state of the two PRs today (`mergeable`, labels, `base.sha`), and `refs/pull/<n>/head` for #1431/#1430 | the drafter holds no Secuura GitHub identity and made no network read | the PR API / Wednesday's ls-remote at send |
| Linear state of KS-1355, KS-1328; any NEW `run-migrations.sh` owner | no Linear read | ITEM 0 (h) |
| Schemathesis colour on each real M | green three times where red was expected | R-8, full job list, per row |
| Shell-suite count on each real M (73 / 73 expected) | EXPECTATION | the hook's own output |
| Whether Peter lands more commits on develop before your push | unknowable | `ls-remote` before every push |
| Your session's scratch UUID | known only at boot | your scratchpad path |
| The four platform suites; preflight legs 3/4/8; every live sweep owed | no stack | — (not in this brief) |

## Qs FOR WEDNESDAY (each with the drafter's recommended default; rule them in one pass at send or in the plan ANSWER)
All earlier Q-rulings (R 23rd-R 26th) are RULED and none is reopened.
- **Q-ARMSROW27 (which row the synthetic arms/fixtures use):** R 26th's arms are built on #1436 (a 2-parent head). **Default: rebuild the GO fixtures + addendum fixture on #1431 (one-parent head, ORIGINAL shape) against `ae9bf6828f88`, DERIVED `EXPECT_PATHS`/`MODE_CENSUS`, every fixture GO clause re-keyed to this seat except A6; all 11 arms at their own asserts incl. P1 (Wednesday's R 26th instruction).**
- **Q-FU3ORDER27 (FOLLOW-UP 3 timing):** the precedent files FU3 right after the first row. **Default: file FU3 after #1431 is verified IF the ctx read says ≤ 62%, but only AFTER Wednesday has released #1430 and the read confirms ≤ 55% for starting it; if the read is > 55%, file FU3 (≤ 62%) and WRAP, leaving #1430 to a successor.** Alternative: FU3 strictly after #1430.
- **Q-DEVMOVE27 (develop moves under a pushed M):** **Default: STOP and mail `STATUS: re-prediction on <12-hex> (Seat R 27th)`; Wednesday rules (re-predict vs option 2); the seat never improvises a shape, never force-pushes.**
- **Q-BOOTPULL27 (R-2):** **Default: as the SEND AMENDMENT states both outcomes; no-op only when PRESENT.**
- **Q-RA4WT27 / Q-KITTIER27:** informational, as before.

PROVENANCE:
- develop `ae9bf6828f88131dfcc0b410f14c2f436903eb49`, parent `09a7b2ec8c11`, tree `22b21d646973`, `merged_at 13:07:03Z`, #1436 head/M2 | `…_seatR26_ANSWER_wrap.md` (Wednesday ls-remote 13:08:14Z + scratch clone), `…_seatR26_STATUS_merged1436.txt`, handover §1 | read 2026-10-10
- shared store: `ae9bf6828f88` and `deadbeef…` absent; `09a7b2ec8c11`, `44753e3e7f4e` commit; `develop`/`origin/develop` `1fba82ddb2b8`; `rev-parse --all` 1,656 lines `bd34017bc0224558`; `ls -a worktrees | grep -i -c push-lock` 0; `s-ra26-m1436` and `s-ra25-m1434` present | `git -C <checkout> cat-file -t / rev-parse / rev-parse --all | wc -l | shasum`, `ls` | read 2026-10-09T13:19:57Z (drafter)
- #1431 `d715e5dfbbf2…` and #1430 `d9928f4a8a4d…`: one parent `0a6177ea5482…`, END_TREE `6a0b2c28456e…` / `d87632c85d8c…` | `git -C <checkout> log -1 --format='%H %P %T'` | read 2026-10-10 (drafter)
- GATE77 bodies #1431 4866 B `2e5d5229…`, #1430 3734 B `5d1dde09…`; report.md `e00b1aa46018b137`; F 5th handover `c3b79f6e2352acff`; subjects 66 / 61 (table; kit 67 / 63 per handover); M subjects 82 / 82 | `wc -c`, `shasum -a 256`, `printf %s | wc -c` | read 2026-10-10 (drafter)
- kit hashes `ec67d311b60564a1` (1,118) / `a02ad6bd8c115196` (160) / `3b85e6edaacad494` (115) / `f1c6e2be1238398b` (111) | `shasum -a 256 | cut -c1-16`, `wc -l` | read 2026-10-10 (drafter)
- step trees `71820d50dbfa…` / `4b84742d8e51…`, composed blobs, 55 / 57 OURS..M paths, `+42 / +43` | R 26th's `wrap/chain_for_r27.out` as quoted in its handover and WRAP (NOT re-run by the drafter) | R 26th, 13:1xZ 2026-10-09
- R 26th handover 70 lines, sha256 `671820b78f2bab9e…` (full value in first-three header), read whole; WRAP 2026-10-09T13:13:31Z and ANSWER_wrap read whole; `_TOOL_HASHES_ra26.txt` 25 rows parsed | `shasum`, `wc -l`, `cat` | read 2026-10-10 (drafter)
- STANDING_LINES `:436` text (quoted verbatim); file 448 lines `72335e0c124f9f22` (unchanged) | `grep -n -i "boot pull"`, `wc -l`, `shasum` | read 2026-10-10 (drafter)
- R 26th GO / ADDENDUM shapes (`…_seatR26_GO_1436.md`, `…_seatR26_ADDENDUM_1436.md`) | read whole | read 2026-10-10 (drafter)
- TESTED grant + 17:50 extension; project MUSTs; STOP list verbatim; partition rows for K 2nd / #1437 | carried from the predecessor's SEND brief (not re-read at source by this drafter) | read 2026-10-10
- NOT measured by the drafter: ls-remote (no network read), usage %, floor, decision-queue list, Linear, the R-1 chain, any 12-hex in the SEND AMENDMENT placeholders.

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-10
