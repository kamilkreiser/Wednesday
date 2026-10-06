LAUNCH BRIEF (Seat D 10th): pane `Secuura/Blockchain-D`. You have ONE job: **unfreeze the repo's pre-push gate.** Preflight legs 6 (npm-audit, KS-470) and 7 (standalone-lock advisories, KS-531) currently FAIL on every push from this repo, on five advisories that are not in `Blockchain/Dev/scripts/audit/audit-baseline.json`. You do an **in-range, lock-only refresh** to the four fixed versions, and add **two dated baseline rows** for the two advisories that have no in-range fix. It goes on ONE new ticket and ONE PR, and stops at ONE READY for a T1 QA gate. This PR merges FIRST, before #1393 / #1395 / #1396 can push. cloud: the Spark predicate fails (multi-file lock regeneration: 36 locks + the baseline). Secuura NEVER force-pushes.

# LAUNCH BRIEF: Seat D 10th, Secuura/Blockchain, pane `Secuura/Blockchain-D`. DEPENDENCY seat: lock refresh + baseline triage ONLY. From Wednesday

## 🔴 LAUNCH AMENDMENT (Wednesday, at send)
- **B 67th's pane is CLOSED.** Wednesday re-hashed its handover EQUAL (52485edb36fd4618) and ran `pane_close.sh %60` at about 13:20 AEDT (24→24 listeners). No other Secuura seat is live. The floor is `%0` wednesday + `%1` monitor. B 67th's row in the partition table is history; its worktree `s-b63-ks1278` and M stay NOT YOURS.
- **Read whole by Wednesday before sending.** The pre-ruled answers stand, and Q-PF / Q-TESTS / Q-TKT are ruled in the ANSWER to your ITEM 0.

## 🔴 READ FIRST
- **The refusal, WHOLE:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-06_seatB67_push_refused.txt` (P1). That is Seat B 67th's push of #1393's merge-in M, refused by the hook with `PREFLIGHT FAILED on leg(s) 6 7`. The ref did not move. B 67th measured that the cause is develop's state, not its change: the baseline blob is byte-identical to develop's (`4ef11079242c`), and all five ids appear 0 times in it, against a positive control of 9.
- **B 67th's handover**, read-only: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB67-2026-10-06.md` (221 lines, 15,496 B, sha256 prefix `52485edb36fd4618` at 02:19Z, P2). It says B 67th **WRAPPED COLD** on Wednesday's ruling (b) at 02:13:59Z, with M `944231047b27` BUILT and UNPUSHED.
- **The precedent rounds, which are your method** (P9, P10):
  - KS-1403 / `e6daa806e`: refresh in 3 locks + 2 baseline rows.
  - KS-1378 / `377989cf3` (#1356): in-range refresh across 18 locks.
  - KS-749 / `fe6daca34`: lock-only, with the commit body as the model for yours.
  - Read B 56th §3-§5: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB56-2026-10-04.md` `:55`-`:125`.
  - Read B 55th §13.2: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB55-2026-10-04.md` `:410`-`:432`.
  - These hold four traps that each nearly shipped. They are restated in METHOD below.
- **The D-lane tools:** generation `*d8`, re-seated to D 9th in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-05_seatD-9th/raise/` (44 files). Also read D 9th's handover `HANDOVER-seatD9-2026-10-05.md` `:145`-`:165` (P11).

## BLUF
**Ruling:** Kam's card `secuura-five-new-advisories-freeze-every-push-1006` is ruled **(a)** (see RULED BY KAM). This brief exists for that ruling.

**What's broken.** origin `develop` is **`4eaf7741a6a4b2c82752d0d94f8bbacb5493aabe`** (#1394 KS-723), read by `ls-remote` at 02:15:32Z (P3). At that develop:

| Advisory | Sev | Pinned | Vulnerable (npm bulk API) | Fixed | Parent's declared range | In range? |
|---|---|---|---|---|---|---|
| GHSA-jqcg-44mw-7w3h proxy-addr | **critical** | 2.0.7 | `>=1.1.0 <2.0.8` | 2.0.8 | express 4.22.3 `~2.0.7` (all 16); express 5.2.1 `^2.0.7` (root, mcp-server) | **YES** |
| GHSA-68fv-2mgg-jv7q source-map-js | **high** | 1.2.1 | `>=1.0.0 <1.2.2` | 1.2.2 | postcss 8.4.49-8.5.28 `^1.2.1`; magicast 0.5.3-0.5.5 `^1.2.1`; css-tree 3.2.1 `^1.2.1` | **YES** |
| GHSA-rj75-hqrm-r3gf postcss-selector-parser **7.x** | moderate | 7.1.4 (api-explorer only) | `<7.1.6` | 7.1.6 | stylelint 17.14.1 `^7.1.4`; @csstools/* peers `^7.1.1` | **YES** |
| GHSA-rj75-hqrm-r3gf postcss-selector-parser **6.x** | moderate | 6.1.4 (admin, issuer, verifier, root; all dev) | `<7.1.6` | none on 6.x (`legacy-v6` = 6.1.4) | tailwindcss 3.4.19 `^6.1.2`; postcss-nested 6.2.0 `^6.1.1` | **NO.** tailwindcss 3.4.19 is the last v3 and still needs `^6.1.2` |
| GHSA-hp3w-g68c-fv3c sprintf-js | moderate | 1.0.3 | `<=1.1.3` (all published versions) | **none** | argparse 1.0.10 `~1.0.2`, under js-yaml 3.15.2 `^1.0.7` | **NO** fix exists |
| GHSA-r4xh-jqrq-34v2 smol-toml | moderate | 1.8.0 (4 systemTest locks, dev) | `<=1.8.0` | 1.9.0 | knip `^1.8.0` (akto, playwright) / `^1.6.1` (api-explorer, performance) | **YES** |

All five packages are **purely transitive**:
- **0** `package.json` declares any of them (control: `"express":` in 28 manifests);
- **0** source files import any of them (control: express imported in 336 files).

Each fixed version's own dependency set **equals** the old one (registry metadata, P5). So a correct refresh changes **exactly three fields** per entry (`version`, `resolved`, `integrity`). Anything else that moves is collateral.

**The change set, predicted (P6):**
- **36 lock files, 54 entries:**
  - proxy-addr in 16 (15 service locks + the workspace root);
  - source-map-js in 33 (32 + root);
  - postcss-selector-parser 7.1.4 -> 7.1.6 in `systemTest/api-explorer` only (`systemTest/akto` already pins 7.1.6);
  - smol-toml in the 4 systemTest locks.
- **Plus** `Blockchain/Dev/scripts/audit/audit-baseline.json`: **+2 rows** (GHSA-rj75, GHSA-hp3w), 22 -> 24.
- **0 manifests, 0 overrides, 0 source, 0 tests, 0 docs.**
- `Blockchain/Dev/mobile/secuura-app/package-lock.json` is **OUT OF SCOPE**. It is excluded from leg 7 by `OUT_OF_SCOPE_LOCKS` (KS-769, fuse 2027-01-01). **Do not touch it**, even though it pins source-map-js 1.2.1 and sprintf-js 1.0.3 (both prod there).

**Order:**
1. ITEM 0 (read-only; ends in the plan-confirmation QUESTION; STOP for the ANSWER).
2. ITEM 1: file the ticket, create the worktree.
3. ITEM 2: build the lock and baseline change, and prove it.
4. ITEM 3: commit, push, open the PR.
5. ITEM 4: ONE READY for the T1 gate.
6. WRAP.

You do NOT merge; the merge is a later GO.

**Budget:** ~one PR (~30% ctx). **Never START a push past ~50%.** Hand over **COLD at ~60%**, naming every built commit (sha, tree, trailer proof) as UNPUSHED unless pushed. Read ctx off your OWN statusline, or write "Please read my ctx." Never estimate it. Never end a turn on a "next up" line with nothing running.

**IF AN INSTRUCTION FROM ME LOOKS WRONG, SAY SO.** In particular, if your ITEM 0 measurement contradicts any row of the table above, the measurement wins: HOLD that row and mail.

**WAKE:** your re-seated `inbox_watchd8.sh` (`SINCE` required), armed in the background at boot with `timeout: 7200000`. It EXITS on every FOR-ME match. **RE-ARM IN THE SAME ACTION THAT READS THE MAIL.** `SINCE` is the newest mail you have READ, never a wall clock.

RULED BY KAM
- **`secuura-five-new-advisories-freeze-every-push-1006` = (a)**, verbatim: "Decision secuura-five-new-advisories-freeze-every-push-1006: a — Fix forward (recommended)". Source: live board, 2026-10-06 13:15:04 +11:00, recorded by `reconcile_rulings.py` (HTTP 200), relayed by Wednesday (P12). Option (a) as carded:
  - refresh the locks to the four fixed versions, in range;
  - baseline ONLY what has no in-range fix (sprintf-js; postcss-selector-parser on 6.x), with the SHARED re-triage date and a ticket;
  - the change goes through a QA gate and merges first.
- **Kam's standing direction to bump rather than accept** (cited in KS-749's merged body `fe6daca34`):
  - card `secuura-four-advisories-ruled-after-measurement` (bump, 2026-09-09T10:30:36+10:00);
  - card `secuura-five-new-advisories-block-every-push-0929` (a, 2026-09-29T11:43:38+10:00).
- **Ticket creation, one ticket per TEST PASS** (Kam 2026-09-07 13:23, STANDING_LINES `:86`-`:93`). This is ONE pass, so ONE ticket.
- **Standing grants:**
  - the 2026-09-11 TESTED merge grant (the GO naming the head is the approval; not this round);
  - Kam's 2026-10-04 ~19:4x "do as much work with the spark and claude agents on the secura projects as you can";
  - the 31 Oct goal.

RULED BY KAM, NOT YET IN AN ARTEFACT
- secuura-five-new-advisories-freeze-every-push-1006: "a — Fix forward (recommended)" (13:15:04 +11:00) -> must land in YOUR PR body (authority line) AND in the reason of both new baseline rows.
- The other ~58 undelivered Secuura cards are the board-pass backlog (a separate seat's work). None of them touches locks, the baseline or these five advisories. They are NOT this seat's to deliver.

RULED BY WEDNESDAY FOR THIS ROUND
- **Shared re-triage date = `2026-10-31`.** It is the date on all 4 of develop's dated rows: react-router ×2 (KS-528), deepmerge-ts (KS-664), braces (KS-1403) (P7).
  - `isLapsed` is `expires <= utcToday()`, so a `2026-10-31` row is dead at 00:00Z Sat 31 Oct = 11:00 AEDT. Say so in the PR body.
  - **Re-date NOTHING that exists.**
- **The 15 stale CLEANUP rows STAY OUT of this PR.** The gate prints them as advisory: 12 undici + ip-address + @hono/node-server under KS-470, and 3 undici under KS-559.
  - Measured reason: every one of them is in `GRANDFATHERED_NO_EXPIRY` in `scripts/audit/baseline-contract.mjs` (`:59`-`:78` at `4eaf`, P8). Removing them is also a code edit to that set, it moves the contract suite, and their disposition belongs to KS-767 ("Decide the 17 baseline entries that carry no `expires`").
  - Name them in the PR body's NOT-DONE list.
- **No HIGH or CRITICAL is baselined.** proxy-addr (critical) and source-map-js (high) are fixed by the refresh, or the PR does not ship.
- **No major bump, no `overrides`, no manifest edit.** tailwindcss 3 -> 4, js-yaml 3 -> 4 and argparse 1 -> 2 would each clear a row. Each is a parent bump OUTSIDE its declared range and is NOT this round.
- **Baseline row shape** follows KS-1403's braces row (P7):
  - keys `package`, `reason`, `ticket`, `decidedAt`, `expires`;
  - the reason MEASURED by you: locks, prod/dev per lock, 0 direct importers with the must-hit control, no fix (registry), the authority line naming Kam's card and ruling verbatim;
  - `ticket` = your new ticket;
  - `decidedAt` = `2026-10-06`;
  - `expires` = `2026-10-31`.
- **🔴 The postcss-selector-parser row is keyed by GHSA id, so it suppresses EVERY version.** The baseline schema has no version or lock scope (`REQUIRED_FIELDS = ['package','reason','ticket']`). A GHSA-rj75 row would also hide a 7.x copy below 7.1.6. So:
  - the api-explorer 7.1.4 -> 7.1.6 refresh is REQUIRED even though the row would mask it;
  - the reason must say the row covers 6.1.4 only by intent;
  - your proof must show by parse that **0** in-scope locks pin any postcss-selector-parser 7.x below 7.1.6 after the change.

## THE PARTITION AND THE LOCK
| Seat | Pane | Token / lock | Files (never yours) |
|---|---|---|---|
| **D 10th (you)** | `Secuura/Blockchain-D` | `d10` / `.push-lock-d8` (Q-LOCKD10) | YOUR new branch + YOUR new worktree only; the 36 locks + baseline listed in the BLUF |
| B 67th (**WRAPPED COLD** per its handover; pane `%60` still listed at 02:19:37Z) | `Secuura/Blockchain` | `b67` / `.push-lock-56` (WAIT) | #1393, branch `feature/ks-1278-revoke-atomic-b63-1`, worktree **`s-b63-ks1278` (NOT YOURS: never read-write, never remove)**, M `944231047b27` |
| B 68th (may launch after your merge) | `Secuura/Blockchain` | `.push-lock-56` | #1393's re-predicted merge-in, on YOUR new develop |
| R lane (#1395 KS-1305) / E lane (#1396 KS-1256) / gate69 | `-R` / `-E` / QA | per their tools | never touch |

- **At draft, the only Secuura pane was `%60` `Secuura/Blockchain` (B 67th)** (panes `%0` wednesday, `%60`, `%1` fleet-monitor at 02:19:37Z). Lock floor: **0** `.push-lock-*` in `worktrees/` (P13). Treat B 67th as possibly still live until its pane is gone.
- **Your PR moves develop for everyone.** After it merges, M `944231047b27` is VOID (B 67th §1), and B 68th re-predicts. Tell nobody that yourself: it is Wednesday's relay.
- **Q-LOCKD10 (pre-ruled: yes):** keep generation `*d8` and `worktrees/.push-lock-d8`, with `export LOCK_SEAT='Secuura/Blockchain-D d10'`.
  - D 9th §Open says the D lane REUSES `.push-lock-d8`, and `twolockd8.sh:56` `mine_exists()` has pointed at the predecessor's lock for three generations. Check it first (P11).
  - Re-seat the SEAT token only (`d9`->`d10`, `9th`->`10th`) with D 9th's `reseatd9.py` (seat-only).
  - Copy the tools from D 9th's `raise/` into YOUR record folder and hash every entry at copy. Do NOT copy `*.rc/.out/.start/.end/stubs`, `merge54-1388*`, `addendum_1388_d9.json` or any `s-d8-ks1404wire-*` push record.
  - Extract the WAIT set from BOTH `lockd8.sh` and `pushd8.sh` / `pushd8_ff.sh`, and assert parity (STANDING_LINES `:414`). It must include `-56`, and every other `.push-lock-*` generation live on the floor at ITEM 0, with your own `-d8` absent from it.
  - ⚠ B 67th's brief listed `.push-lock-d8` under the R lane. Measure whose tools take `d8` and say so; it is UNMEASURED here.
- **The lock rule:** every ref write needs `.push-lock-d8` HELD by you, the WAITs absent and no unattributed lock. That covers the worktree add, the commit and the push.
  - **Attribute every lock by its holder file's `seat` field, never by path.** A `.push-lock-d8` whose `seat` is not `Secuura/Blockchain-D d10` is a STOP-and-mail. Never take it over, never remove it.
  - Hold the lock short: never across `npm ci`, a gate run or a suite.
  - Never pipe a lock take (`${PIPESTATUS[0]}` is EMPTY in zsh).
- **Matcher re-key (both halves):**
  - `inbox_matchd8.py`: `MINE = "d 10th"`. In `OTHER_SEATS`, remove `"d 10th"`/`"seat d 10th"`, and ADD `"d 9th"`, `"seat d 9th"`, `"d 11th"`, `"seat d 11th"`, `"b 67th"`, `"b 68th"`.
  - Prove: a constructed `(Seat D 11th)` reads NOT FOR ME; a B 67th subject reads FOREIGN; `QUESTION: plan confirmation (Seat D 10th)`'s ANSWER reads FOR ME.
  - `namecheckd8.py`: `MINE = "d10"`, FOREIGN adds `d9`, `seatd9`.
- **STALE KNOBS:** list every module-level knob with its value BEFORE any run. Grep every string literal for 36-char UUIDs and `/private/tmp/` paths and print the count checked. AST-parse every Python tool with ok/fail counters.

## ITEM 0 — plan confirmation (QUESTION `plan confirmation (Seat D 10th)`). STOP until Wednesday's ANSWER.
Before the ANSWER, do NONE of these: lock take, fetch into the shared store, worktree add, ref write, `npm` write into any tracked tree, ticket write, comment, PR. You MAY write inside your own record folder and inside YOUR scratch clone.

ITEM 0 carries:
- **Refs by `ls-remote`, instrument named:** develop, `refs/pull/{1393,1395,1396}/head`. At draft: develop `4eaf7741a6a4`, `/1393/` `b5adaba751d8`, `/1395/` `1bdfbe0f2f06`, `/1396/` `e6eb53fe2658` (P3). Identify develop by `git log -1` and its PR.
  - **If develop moved past `4eaf`, re-measure the whole BLUF table on the new develop.** A new advisory, or a different lock set, goes in the mail.
- **YOUR scratch clone:** `git clone --shared --no-checkout` of `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` into your scratchpad. `4eaf` IS present in the shared store at draft (`cat-file -t` rc 0, P3), so no fetch is needed unless develop moved. If it did:
  - fetch BY SHA from `git@github.com:Secuura/Distributed_Secuura.git` with `-c core.sshCommand="$(git -C <checkout> config --get core.sshCommand)"`, `--no-tags --no-write-fetch-head`;
  - **NEVER export `GIT_SSH_COMMAND`;**
  - show the shared checkout's `rev-parse --all` sha256 identical before and after.
- **🔴 THE IN-RANGE TABLE, second hand.** For every in-scope lock and each of the five packages:
  - pinned version, `dev` flag, and EVERY parent entry whose dependency resolves to that path (nearest `node_modules` walk), with its declared range;
  - the registry's vulnerable range from `POST https://registry.npmjs.org/-/npm/v1/security/advisories/bulk` (read-only);
  - in range: yes/no.
  - At draft (P4-P6): 78 entries over 45 locks, every parent listed in the BLUF table, no orphan.
  - **Any entry whose fixed version is NOT admitted by its parent's range is a STOP-and-mail, never a pin.**
- **The leg reproduction at base, in your scratch clone (read-only):** run `node scripts/audit/audit-gate.mjs` and `node scripts/audit/audit-locks.mjs` from `Blockchain/Dev` of a checkout of `4eaf`. They need `scripts/audit/node_modules` (`npm ci --ignore-scripts` inside your SCRATCH tree only).
  - Quote the counts. Expected per P1: leg 6, 4 NEW; leg 7, 43 locks / 1614 packages / 10 match / 5 unbaselined.
  - This is your BASE CONTROL.
- **Toolchain:** `node -v`, `npm -v` (host v24.7.0 / 11.5.1 at draft) and `docker info`.
  - Docker was DOWN at draft (socket absent, P13).
  - Host npm 11.5.1 was measured INERT for `npm update … --package-lock-only` on the root lock (B-successor1 `:22`). Host node 24 takes the clean-room's host path (`lockfile-cleanroom.sh:49-53`), so Docker is not needed for leg 2.
- **The project rules quoted from develop with their blob ids:**
  - `.claude/skills/secuura-test-discipline/SKILL.md` (blob `eaf43dfd4d98…`): §1 (plan first), §5d (the ticket URL in PR summaries; register the dep finding), §5e (no branches/PRs/tickets unless instructed; they ARE instructed here, on the ANSWER) and §5f (numbers, not adjectives; name what is unverified);
  - repo `CLAUDE.md` (blob `eccdb71822da…`): `:324`-`:346` the register rule (KS-485 / KS-493 H dependency stream) and `:349`-`:380` the preflight / audit-gate rule ("baseline entries need a reason + ticket, temporary ones an `expires`").
- **Linear, read-only:**
  - re-run the existing-ticket search (see LINEAR) and say what you searched;
  - re-read KS-1403, KS-1378, KS-749 and KS-769 (state, assignee, project, `archivedAt`, newest comment by `comments(first:50)` sorted client-side).
- **The ticket draft** (filed only on the ANSWER): title, body (facts + instruments, every sentence measured or "unmeasured"), project, priority. Board account, unassigned.
  - Propose the project; Wednesday rules it. Precedents: KS-749 "Dependency and Version Currency"; KS-1378 "Internal tooling"; KS-1403 none.
  - Cross-reference KS-470, KS-531 and KS-1403 hyphenated. A Linear ticket only cross-references, so that is allowed there.
- **Also:**
  - the fuse: develop's 4 dated rows and the hours to `2026-10-31T00:00Z`;
  - the watchers from a ps FILE;
  - your own watcher pid;
  - every launcher preflight warning, VERBATIM;
  - your ctx;
  - your pane id from `$TMUX_PANE`;
  - `df -m /Volumes/DevMASTER` (697,534 MiB free at draft).
- **QUESTIONS.** Each pre-ruled answer stands unless your ITEM 0 measurement contradicts it:
  - **Q-LOCKD10: yes** (above).
  - **Q-METHOD: yes, the surgical edit** (see METHOD). If you want `npm update` output instead, propose it with a measured collateral count.
  - **Q-WT: yes.** Create ONE worktree `worktrees/s-d10-advlock` on ONE new branch `feature/ks-<new>-advisory-lock-refresh-d10-1` from `4eaf…` (or the develop the ANSWER names), with `wtaddd8.sh`, under the lock.
  - **Q-PF (PROPOSED; Wednesday rules):** for this lock-only PR, accept the in-hook `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` with legs 3/4/8 stack-skipped. Precedent: KS-749 shipped on exactly that reading. Legs 2, 5, 6 and 7 must RUN and pass. A FAILED anywhere is a STOP.
  - **Q-TESTS (PROPOSED; Wednesday rules):** no service unit suites this round. The proof is the gates plus a real `npm ci --ignore-scripts` from the committed root lock (rc 0, lock byte-unchanged; KS-749 precedent), plus the tarball hashes. The service suites and the frontend CSS build diff go in Test Evidence as **NOT run**. The T1 gate decides whether more is owed.
  - **Q-TKT: confirm the ticket draft and its project.**

## METHOD (the four traps of the precedent rounds, carried)
1. **Lock-only, per entry, three fields.** For each of the 54 entries, set `version`, `resolved` (`https://registry.npmjs.org/<pkg>/-/<pkg>-<ver>.tgz`) and `integrity`, and touch NOTHING else. This is B 56th's method (KS-1403).
   - `npm update … --package-lock-only` on the root produced the bump **plus 13 collateral** dev-flag flips (B 56th §3a).
   - In a member it writes the ROOT lock unless `--no-workspaces` is given (B 55th §13.2).
   - If you use npm to cross-check, do it in a SCRATCH copy, and prove your surgical edit is **field-for-field identical** to npm's own output on each allowed entry.
2. **Integrity from the tarball, not from the clean-room.** `npm ci --dry-run` returns rc 0 on a bogus integrity (B 56th, planted `sha512-AAAA…`).
   - Download each fixed tarball once (`proxy-addr-2.0.8`, `source-map-js-1.2.2`, `postcss-selector-parser-7.1.6`, `smol-toml-1.9.0`) into your scratchpad and compute sha512. Use the OLD version's tarball as a firing negative control.
   - Cross-check against the registry's `dist.integrity` (prefixes at draft: `sha512-5nnx0yGyVUcY6t9RnWcARWt…`, `sha512-KGj/8Y43x35aZVDtt+J4mK1…`, `sha512-7qASPzhKF2l2KLboRZux8CC…`, `sha512-hpd+HLON7HdZXqYchMM/+La…`, P5).
   - In-repo positive controls: the 12 locks already pinning proxy-addr 2.0.8 and `systemTest/akto`'s postcss-selector-parser 7.1.6 must carry the same integrity.
3. **A semantic differ and a line differ answer different questions.**
   - Per lock, the JSON diff must be exactly the planned entries × 3 fields: 0 added, 0 removed, 0 other.
   - The `git diff --numstat` must be exactly 3 out / 3 in per entry.
   - No `libc` / `os` / `cpu` array lost, and key order equals base (B 56th §3b).
4. **The baseline is appended TEXTUALLY.** The file does not survive a JSON round-trip (B 56th §4).
   - Assert every pre-existing row is byte-equal afterwards, `$comment` unchanged, 22 -> 24.
   - Then `audit:contract` must still report its expected case count (`scripts/audit/expected-case-count` = **59** at `4eaf`).

## QUEUE (after the ANSWER)
1. **ITEM 1: ticket and worktree.**
   - Re-run the Linear search. If a ticket for these advisories now exists, STOP and mail; never file a duplicate.
   - File the ONE ticket as confirmed, and read it back.
   - Under the lock: `wtaddd8.sh` creates `s-d10-advlock` on the new branch from develop. Release the lock.
   - In the worktree, outside the lock: `npm ci --ignore-scripts` at `Blockchain/Dev` and in `scripts/audit` (KS-691: a fresh worktree has no deps).
2. **ITEM 2: build and prove.**
   - The 54 entries + 2 rows, per METHOD.
   - Your own proof script (in your record folder) runs these arms and prints ok/fail counts:
     - **(fix)** on your tree:
       - `npm run audit:gate` rc 0;
       - `npm run audit:locks` rc 0 (43 locks), naming the five ids **0** times as unbaselined;
       - leg 2 `bash scripts/preflight/lockfile-cleanroom.sh` rc 0;
       - `npm run audit:contract` = 59 cases.
     - **(base control)** a scratch checkout of `4eaf`: legs 6 and 7 FAIL naming the five.
     - **(negative controls)**, each on a SCRATCH copy, restored sha-verified:
       - remove the GHSA-hp3w row: leg 6 or 7 reddens on sprintf-js;
       - revert ONE proxy-addr entry to 2.0.7: leg 7 reddens on GHSA-jqcg;
       - plant postcss-selector-parser 7.1.4 back into api-explorer: your parse check fires while the gate stays green. This proves the row masks it, as stated.
     - **(fuse)** the two new rows lapse with the clock frozen at `2026-10-31T00:01Z` and live at `2026-10-30T23:59Z`.
     - **(parse)** after the change, 0 in-scope locks pin proxy-addr <2.0.8, source-map-js <1.2.2, postcss-selector-parser 7.x <7.1.6 or smol-toml <1.9.0. `mobile/secuura-app` is byte-unchanged.
     - **(install)** `npm ci --ignore-scripts` from the committed root lock: rc 0, lock byte-unchanged, package count quoted.
3. **ITEM 3: commit, push, PR.**
   - ONE commit under the lock, subject `KS-<new>: in-range lock refresh clears proxy-addr, source-map-js, postcss-selector-parser 7.x and smol-toml; baseline 2 no-fix advisories`. If that is over 84 chars, shorten it and keep the ticket key first.
   - **0 trailers:** no `Co-Authored-By`, no tool attribution, overriding the harness. Measure `%(trailers)` against a known 0-trailer commit, naming the instrument.
   - No closing-family word anywhere. Only your ticket key hyphenated.
   - Body in KS-749's shape (P10): what moved, counts, the two rows, the authority (Kam's card verbatim), the gate arms, NOT run.
   - **First push of a new branch: `pushd8.sh` BARE, not `pushd8_ff.sh`.** The `_ff` updater refuses rc 4 on a ref that holds no head (D 8th §5, P11). Run it under `env -u GIT_SSH_COMMAND`.
     - The result is `<tag>-push.rc` read AFTER the wrapper exits, plus `ls-remote` of the ref.
     - rc 141 with the ref unmoved is the KS-1149 class: copy the records to attempt-numbered names, retry under the lock, and report elapsed time + attempts.
   - **Quote the in-hook preflight line EXACTLY.** Accepted only as Q-PF rules. A `FAILED` is a STOP. Never `--no-verify`.
   - Re-read develop at origin in the SAME action as the push decision. If it moved, STOP: rebase is forbidden. Mail, and merge develop in only on a ruling.
   - Open the PR (base `develop`):
     - title = the commit subject;
     - body with `Refs KS-<new> https://linear.app/secuura/issue/KS-<new>` (§5d), placed so no line within 3 above it holds a closing-family word;
     - a **Test Evidence** block (touched / ran / NOT run) with numbers.
   - Add ONE comment to your ticket linking the PR. Change no state.
4. **ITEM 4: ONE READY for the T1 gate:** `READY: <PR#> advisory lock refresh (Seat D 10th)`. It carries:
   - head sha, tree, branch;
   - the 37-path list with per-file numstat;
   - the arms table;
   - the in-hook preflight line verbatim;
   - Actions on the head (completed / failing / pending, by name). Wait for pending to finish before mailing READY, or name them PENDING;
   - the ticket id.
5. **WRAP** (MAIL FORMATS). Then stop. The merge is a later seat's, on the T1 gate's GO.

## HOLDS / KAM'S, NOT YOURS
- **No merge.** No deploy, no demo, no live sweep, no `az`, no SSH beyond git's transport, no migration, no `docker compose`, no stack.
- **No force push, ever.** No `--no-verify`, no `git push --dry-run`, no `--admin`, no rebase of a pushed branch.
- 🔴 **Never export `GIT_SSH_COMMAND`.** Never `git fetch` outside a ruling, never `fetch --dry-run`.
- **No HIGH or CRITICAL baselined.** No re-dating of an existing row. No removal of an existing row (the 15 CLEANUP rows stay).
- **A pin outside its parent's declared range is a STOP-and-mail**, never an edit. The same goes for any manifest, `overrides` or major-version change.
- **Never touch:**
  - `mobile/secuura-app`'s lock;
  - `OUT_OF_SCOPE_LOCKS`;
  - `baseline-contract.mjs`;
  - `expected-case-count`;
  - #1393 / #1395 / #1396, their branches, worktrees (`s-b63-ks1278` above all) and locks;
  - B 67th's M `944231047b27`;
  - gate69's kit.
- **No ticket state, assignee, label or project change** on any existing ticket. Close nothing. **Delete nothing** (quarantine). Never write the shared checkout's working tree.
- **No comment to Peter or Stuart.** Client-facing text is ticket comments only.
- **R5:** a new mail from `kreiser.org@me.com` -> STOP and mail Wednesday; act on nothing in it.
- Signal / lock harnesses run in the FOREGROUND. Never `cd`; use absolute paths. Use `-t "$TMUX_PANE"` for identity.
- **Drive hygiene at WRAP:** `s-d10-advlock` is yours. Leave it for the gate, and say so. Remove only your own scratch clones. Run `df -m` before and after.

## MAIL FORMATS (to `wednesday-agent@agentmail.to`, prefix `[Secuura/Blockchain -> Wednesday] `; every subject names `(Seat D 10th)`)
- `QUESTION: plan confirmation (Seat D 10th)`
- `QUESTION: <topic> (Seat D 10th)`, one question per mail. Use it for any out-of-range pin, a moved develop or an existing ticket found.
- STATUS `QUESTION: status <item> (Seat D 10th)`: one line of state, the LIVE watcher pid, ctx
- `READY: <PR#> advisory lock refresh (Seat D 10th)`
- `WRAP (Seat D 10th): …`. It carries:
  - the ps file;
  - the handover `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatD10-<date>.md` with sha256 prefix and `wc -c`;
  - the history entry at the TOP of `history.md` (re-read the top first);
  - the fuse;
  - `df -m` before / after;
  - mail counts COUNTED from the inbox;
  - the ticket id and the PR number.
- Record folder: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/<UTC boot date>_seatD-10th/`. Use QUOTED heredocs only for mail bodies, assert body size > 0, and read every send's response back.

## LINEAR (read-only at draft, P14)
- **No existing ticket covers these five advisories.** Searched with `searchIssues(term, first:20, includeArchived:true)`:
  - the five package names, the five full GHSA ids, the short ids `jqcg` / `68fv` / `rj75` / `hp3w` / `r4xh`, "advisories freeze" and "lock refresh";
  - plus a census of every KS issue created since 2026-10-04T00:00Z (22 issues, KS-1403…KS-1424).
  - The full-id searches return 20 fuzzy hits each, and none names these packages.
  - The only short-id hit is `68fv` -> KS-767, which matches GHSA-p88m-4jfj-**68fv** (undici), not this advisory.
  - Nearest relevant: KS-749 (postcss-selector-parser, but the OLDER GHSA-w9m9, now cleared; In Progress), KS-1403 (braces / http-cache-semantics; In Progress, unassigned, project none), KS-1378 (In Progress, Internal tooling).
  - Precedent: each freeze wave got its OWN ticket (KS-1378, KS-1395, KS-1399/KS-1400, KS-1403). KS-1399 and KS-1400 look like one wave filed twice: search before filing.
- KS-1403: In Progress, unassigned, project none, updatedAt 2026-10-04T11:26:21Z, 0 comments, attachment `pull/1373`.
- KS-1378: In Progress, kamil.kreiser@secuura.ai, Internal tooling, updatedAt 2026-10-05T06:50:40Z, 3 comments, attachments `pull/1339`, `/1355`, `/1356`, `/1363`.
- KS-749: In Progress, kamil.kreiser@secuura.ai, Dependency and Version Currency, updatedAt 2026-10-05T03:11:55Z, 4 comments.
- KS-769: In Progress, kamil.kreiser@secuura.ai, project none, updatedAt 2026-10-05T01:03:29Z (mobile exclusion; named only).
- KS-493 (dependency work-stream H, Done, archived 2026-08-04) and KS-470 / KS-531 (Done, archived) are named only as gate owners. Write nothing to them.

## UNMEASURED (not provenance)
- Whether develop moves before your push (#1395 / #1396 / #1393 are all held behind this same freeze, so it probably does not, but that is not measured).
- Whether another advisory is published between draft and your push. Leg 6/7 counts are only as of P1 (02:03Z-02:10Z).
- Which lanes' tools take `.push-lock-d8` (B 67th's brief listed it under R).
- Whether D 9th's `*d8` tools still pass their own proofs on this host.
- Whether host npm 11.5.1 produces the same three-field output as npm 11.19.0 on these entries (relevant only if you cross-check with npm).
- The runtime effect of proxy-addr 2.0.8 on `trust proxy` handling in the 16 locks where it is a PROD dependency. No live sweep is owed by this PR, but §5f: the ticket does not go to Done on offline green.
- The frontend CSS build output with source-map-js 1.2.2 / postcss-selector-parser 7.1.6 (no build was run).
- Actions on your head, including `pr-lockfiles.yml`.
- B 67th's pane `%60` closing; your ctx and pane id.
- When each advisory was published (the registry gives version publish times only: proxy-addr 2.0.8 2026-09-15, source-map-js 1.2.2 2026-09-30, postcss-selector-parser 7.1.6 2026-09-03, smol-toml 1.9.0 2026-09-22).

PROVENANCE:
- P1 B 67th refusal: `PREFLIGHT FAILED on leg(s) 6 7 … (12/15 legs ran)`; leg 6 11 reported / 22 baselined / 4 NEW; leg 7 43 locks, 1614 packages, 10 match, 5 unbaselined; blast radius per package; 15 CLEANUP rows (12 undici + ip-address + @hono/node-server KS-470, 3 undici KS-559); baseline blob `4ef11079242c` identical to develop; five ids 0 vs control 9; push 02:03:19Z-02:10:20Z rc 1, ref unmoved | Read whole `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-06_seatB67_push_refused.txt` | read 2026-10-06
- P2 B 67th handover: 221 lines, 15,496 B, mtime 13:17 AEDT, sha256 prefix `52485edb36fd4618`; "WRAPPED COLD on Wednesday's ruling (option b, 02:13:59Z)"; M `944231047b27…` UNPUSHED, tree `0b4c3a265454`; "M IS VOID THE MOMENT develop MOVES" | `wc -l`, `ls -la`, `shasum -a 256`, `head -40` of `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB67-2026-10-06.md` | read 2026-10-06
- P3 origin 02:15:32Z-02:15:37Z: develop `4eaf7741a6a4b2c82752d0d94f8bbacb5493aabe`; branch == `/1393/` `b5adaba751d8`; `/1394/` `585171bc2c29`; `/1395/` `1bdfbe0f2f06`; `/1396/` `e6eb53fe2658`. Shared store `cat-file -t 4eaf…` = commit rc 0; shared `rev-parse --all` sha256 `078711df5a8ed907…` identical before and after (02:19Z); `s-b63-ks1278` HEAD `944231047b27` (read only) | `git -C <scratch clone> -c core.sshCommand=<checkout value> ls-remote git@github.com:Secuura/Distributed_Secuura.git …` (GIT_SSH_COMMAND unset, `env | grep -c` 0); `git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" cat-file -t`, `rev-parse --all | shasum -a 256` | read 2026-10-06
- P4 45 tracked locks at `4eaf`; leg-7 corpus = 45 minus the `Blockchain/Dev` root (leg 6) minus `mobile/secuura-app` (`OUT_OF_SCOPE_LOCKS`, KS-769, expires 2027-01-01, `lock-discovery.mjs:193`-`:221`) = 43 | `git ls-tree -r --name-only 4eaf | grep package-lock.json`; `git show 4eaf:Blockchain/Dev/scripts/audit/lock-discovery.mjs`; repo `CLAUDE.md` `:369`-`:373` | read 2026-10-06
- P5 registry: proxy-addr latest 2.0.8 (2026-09-15), deps `forwarded 0.2.0, ipaddr.js 1.9.1` == 2.0.7's; source-map-js latest 1.2.2 (2026-09-30), no deps; postcss-selector-parser latest 7.1.6, `legacy-v6` 6.1.4, 7.1.4 and 7.1.6 deps equal; sprintf-js latest 1.1.3; smol-toml latest 1.9.0, no deps; tailwindcss `v3-lts` 3.4.19 needs psp `^6.1.2`; postcss-nested 7.x+ needs psp `^7`; argparse 1.0.10 needs sprintf-js `~1.0.2`. Bulk advisory API: jqcg critical `>=1.1.0 <2.0.8`; 68fv high `>=1.0.0 <1.2.2`; rj75 moderate `<7.1.6`; hp3w moderate `<=1.1.3`; r4xh moderate `<=1.8.0`. Fixed tarball URLs and `dist.integrity` prefixes as in METHOD | `curl https://registry.npmjs.org/<pkg>` ×8; `curl -X POST …/-/npm/v1/security/advisories/bulk` (HTTP 200); parsed with `python3 -I` | read 2026-10-06
- P6 per-lock parent walk at `4eaf`: 78 entries, 0 without a resolving parent; parents/ranges as in the BLUF; proxy-addr 2.0.7 in 16 (15 service + root), 2.0.8 already in 12; source-map-js 1.2.1 in 34 (32 leg-7 + root + mobile); psp 6.1.4 in 4 (admin, issuer, verifier, root; all `dev`), 7.1.4 in api-explorer, 7.1.6 in akto; sprintf-js 1.0.3 in 6 (governance, originate, referral, vc-issuer dev; root nested under argparse, dev; mobile prod), grandparent js-yaml 3.15.2 `^1.0.7`; smol-toml 1.8.0 in 4 systemTest. Predicted change set: 36 locks, 54 entries. 0 manifests declare any of the five (control `"express":` 28); 0 importers (control express 336) | `python3 -I` scripts over `git show 4eaf:<lock>` in `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c5cbc1ba-f917-4149-bf03-282222796e89/scratchpad/d10/` (`parents.py`, `gp.py`, `importers.sh`); `git grep` | read 2026-10-06
- P7 baseline at `4eaf`: blob `4ef11079242c`, keys `$comment`, `accepted` (22). Dated rows: GHSA-wrjc / GHSA-337j react-router KS-528, GHSA-ggr8 deepmerge-ts KS-664, GHSA-vfj7 braces KS-1403 (decidedAt 2026-10-04), all `expires` 2026-10-31. Row keys `package, reason, ticket, decidedAt, expires`. The braces row reason carries the measured lock census, 0 direct callers with the express control, and "Authority: Kam ruled option b on card secuura-freeze5-high-no-fix-1004 …". The five ids are absent | `git show 4eaf:Blockchain/Dev/scripts/audit/audit-baseline.json`, `python3 -I` | read 2026-10-06
- P8 `baseline-contract.mjs` at `4eaf`: `REQUIRED_FIELDS = ['package','reason','ticket']` `:41`; `GRANDFATHERED_NO_EXPIRY` 18 ids `:59`-`:78` (contains every CLEANUP row's id family: undici ×13, ip-address, @hono/node-server, valibot, elliptic, uuid); any NEW entry without `expires` fails; `isLapsed` = `expires <= today` UTC. `expected-case-count` = 59. Root manifest `overrides` hold none of the five; workspaces `packages/*, services/*, frontend/*` | `git show 4eaf:…/baseline-contract.mjs | sed -n 40,95p`; `git show 4eaf:…/expected-case-count`; `package.json` parse | read 2026-10-06
- P9 preflight at `4eaf`: `TOTAL_LEGS=15`; leg 2 `run_delegated bash scripts/preflight/lockfile-cleanroom.sh` (`:269`-`:275`); scripts/audit deps installed once before leg 5 (`:336`-`:344`); leg 5 `npm run audit:contract` vs `expected-case-count` (`:346`); leg 6 `node scripts/audit/audit-gate.mjs` rc 0/1/2/3 (`:419`-`:440`); leg 7 `node scripts/audit/audit-locks.mjs` (`:442`-`:480`). `lockfile-cleanroom.sh` host node ≥24 skips Docker (`:49`-`:53`), `--no-workspaces` (`:80`-`:87`), regen hint `npm install --package-lock-only --ignore-scripts` in node:24-alpine (`:118`-`:120`). Preflight blob not re-hashed this draft (B 67th's brief: `270b8913c009`) | `git show 4eaf:Blockchain/Dev/scripts/preflight/preflight.sh`, `…/lockfile-cleanroom.sh`, `sed -n`, `grep -n` | read 2026-10-06
- P10 precedents: `e6daa806e` "KS-1403: refresh http-cache-semantics to 4.3.0 in 3 locks, baseline 2 advisories", 4 files +24/-8; `377989cf3` "KS-1378: in-range lock refresh clears six new advisories across 18 locks (#1356)", 18 files 90/90; `fe6daca34` KS-749 body (lock-only, 23 entries, 3 rows out, Kam's two standing cards, fuse frozen-clock test, legs 2/5/6/7 green, "PREFLIGHT INCOMPLETE - 12/15", mobile out of scope). B 56th `:55`-`:125` (npm update collateral 13, libc 20 restored, bogus-integrity trap, textual append, legproof 17 arms); B 55th `:410`-`:432` (`--no-workspaces` load-bearing; root-lock collateral reverted); B-successor1 `:22` (host npm 11.5.1 INERT for `npm update --package-lock-only`; one package per update) | `git -C <scratch clone> log --grep=KS-1378 --grep=KS-1403`, `log -- audit-baseline.json`, `log -1 --format=%B`, `show --stat`; `sed -n` on the three handovers in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/` | read 2026-10-06
- P11 D 9th handover (165 lines): pane `Secuura/Blockchain-D` %43; tools generation `*d8` in `2026-10-05_seatD-9th/raise/` (44 files: `lockd8.sh`, `pushd8.sh`, `pushd8_ff.sh`, `wtaddd8.sh`, `inbox_watchd8.sh`, `inbox_matchd8.py`, `namecheckd8.py`, `reseatd9.py`, `legproofd8.sh`, `twolockd8.sh`, …); `:163`-`:165` "Check `twolockd8.sh:56` `mine_exists()` first in generation `d10` … the D lane REUSES `.push-lock-d8`"; D 8th `:139`-`:143` first push uses `pushd8.sh` BARE, `_ff` refuses rc 4 with no head | `head -30`, `sed -n 140,165p`, `grep -n`, `ls` | read 2026-10-06
- P12 Kam's ruling: "Decision secuura-five-new-advisories-freeze-every-push-1006: a — Fix forward (recommended)", live board 2026-10-06 13:15:04 +11:00, `reconcile_rulings.py` HTTP 200 | Wednesday's relay to this drafter (mid-task message), not re-read on the board | read 2026-10-06
- P13 at 02:19:37Z: tmux panes `%0` wednesday, `%60` Secuura/Blockchain, `%1` fleet-monitor; `worktrees/` 0 `.push-lock-*`; `docker info` fails, socket absent; host node v24.7.0, npm 11.5.1; `df -m /Volumes/DevMASTER` 697,534 MiB free (02:21Z) | `tmux list-panes -a -F`, `ls -1A … | grep -c '^\.push-lock-'`, `docker info`, `node -v`, `npm -v`, `df -m` | read 2026-10-06
- P14 Linear, read-only: `searchIssues` ×17 terms (20 fuzzy hits for each package/GHSA term, none naming these packages; `68fv` -> KS-767 only; `jqcg`/`rj75`/`hp3w`/`r4xh` 0); `issues(createdAt >= 2026-10-04)` 22, none on these advisories; `issue()` reads of KS-1403, KS-1378, KS-749, KS-769, KS-493, KS-470, KS-531 as listed | Linear GraphQL, LINEAR_API_KEY from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env` sourced transiently with `set -a`, never printed; out `…/scratchpad/d10/linear.out`, `linear2.out` | read 2026-10-06
- P15 project rules at `4eaf`: SKILL blob `eaf43dfd4d985bf9b0badbfc7e85561c13407e1f` (§1 `:13`, §5d `:507`, §5e `:518`, §5f `:540`); repo `CLAUDE.md` blob `eccdb71822dae2563de0f6a88620a6ca7d55d769` (`:324`-`:346` register / KS-493 H, `:349`-`:380` preflight + baseline rule) | `git rev-parse 4eaf:<path>`, `git show`, `sed -n`, `grep -n` | read 2026-10-06
- P16 KS-1149 state (Backlog AND archived 2026-10-05T02:48:32Z, last comment 2026-09-14), named only as the rc-141 class: NOT queued work. Write nothing to it | Linear ticket KS-1149, `issue(id:"KS-1149")` read-only | read 2026-10-06
- P17 KS-691 state (Done, archived 2026-09-05, last comment 2026-09-02), named only as the precedent that a fresh worktree has no deps: NOT queued work | Linear ticket KS-691, `issue(id:"KS-691")` read-only | read 2026-10-06
SELF-CHECK: re-read end-to-end for contradictions | 2026-10-06 13:24
