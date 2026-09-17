# QA GATE BRIEF — Secuura/Blockchain PR #1025 (KS-528, Seat B: re-date audit-baseline rows 11 and 12, GHSA-wrjc-x8rr-h8h6 and GHSA-337j-9hxr-rhxg, react-router, 2026-09-30 → 2026-10-02) — TIER two (through code), ROUND 1

**Charter — read first, in full:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`

Drafted 2026-09-17 19:23–19:40 AEST (from `date`) by a Wednesday drafting subagent. Every fact carries its instrument inline. **"The seat" or "the READY" means relayed, not re-derived: an input to falsify.** "Drafter-measured" means the drafter read or ran it: read-only `git` on the Secuura checkout, GitHub REST GETs, Linear GraphQL queries, or scripts in the drafter's OWN `git clone --shared`. It is still yours to re-derive. Drafter scripts and outputs: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1025/` (below: `GS/`), raw runs under `GS/out/`. The READY mail, verbatim, spf/dkim/dmarc pass: `GS/mail_1025_ready.md`. Wednesday's receipt (TIER two agreed): `GS/receipt_1025.md`. The ruling chain: `gatesets/2026-09-17_seatB/answer_kam_rulings_1831.md` (Kam's panel ruling, verbatim) → `gatesets/2026-09-17_seatB/answer_rr7_date_ruled.md` (Wednesday sets landing 2026-10-01, expires 2026-10-02) → `gatesets/2026-09-17_seatB/REACT_ROUTER_V7_SIZING.md` §BLUF.

**Method lessons, binding:**
1. **Only the parse is evidence of scope.** Diff the parsed `accepted` map row by row and field by field, and plant alterations to prove the differ can see one.
2. **A frozen clock must be proven frozen.** Assert `utcToday()` returns the frozen date (and a far-future control) before believing a live/LAPSED cell. Scope the freeze to the gate script (`process.argv[1]`), never to the `npm audit` child it spawns.
3. **At a frozen instant past 2026-09-24 the gate is rc 1 because OTHER rows lapse.** rc is NOT the oracle for rows 11/12 there; the `LAPSED` list is. Read which ids it names.
4. **A zero needs a control that can fail on the same instrument:** remove a target row and show both gates red on it.
5. Node 24 `node --test` prints `ℹ pass N` when not a TTY: read those lines, never a TAP `# tests` parse.
6. Re-read Linear's `attachments.metadata.linkKind` immediately before the mail.

## WHY TIER two, AND HOW MUCH

- **Tier 2, as the seat proposed and Wednesday's receipt agreed:** one security-gate config file, two rows, checked through the shipped code. A wrong date either blocks every Blockchain/Dev push from 30 Sep 10:00 AEST (too early) or hides two live advisories past the ruled landing (too late, or a typo that never lapses).
- **Budget: proportionate. One file, +4 −4, no code, no dependency. Time-box 20 minutes.** Priority if time runs short: item 1 → item 2 → item 3 → item 5 → item 6 → item 4. Report anything not reached as **NOT RUN, with the blocker named**.
- **NOT REQUIRED, said before running:** docker or any stack; preflight.sh whole (this byte reaches legs 5, 6 and 7 only, and you run those commands directly); any unit, service, frontend or platform suite (no code or lock byte moved); the react-router v7 migration itself (MIG-1, a separate TIER 1 PR); any browser pass. List each under NOT TESTED as *not-applicable (why)*.

## TARGET

**Repo READ-ONLY:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`. Clone by SHA into your OWN fresh `mktemp -d` (`git clone --shared --no-checkout`), add detached worktrees there, and run every write verb there from a script file. Never enter any `worktrees/` directory, Seat B's or Seat A's worktrees, or any other gate's clone. 🔴 **NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout or any of its worktrees.**

**A PR is gated at a SHA. Your first act is to verify the head at origin:** `git ls-remote origin refs/heads/chore/audit-redate-react-router-rows-v7-landing refs/pull/1025/head`, plus the PR API's `head.sha`. If it differs, STOP, mail the moved head, gate nothing.

| | PR #1025 |
|---|---|
| ticket | KS-528 (In Progress), "Frontends: react-router v6 → v7 migration (3 moderate client-runtime advisories…)". Body "Refs KS-528" ×1; 0 closing phrases in title, body, commit message and the one `linear[bot]` comment (regex with planted controls: `Fixes KS-1211` and `closes #12` hit, `Refs KS-1211` does not; `GS/api_read.out` 19:28:48). The body also names KS-1201 in plain text (the stub-killer note); it is not an attachment |
| branch | `chore/audit-redate-react-router-rows-v7-landing` (no ticket id), author `kksecura` |
| head | **`9954a7069a16987da140654337555c9a13268b1f`** (ls-remote 19:24:23; PR API 19:28:48), tree `23b56bac07faf84165882176e63436e1c470826e` |
| parent = merge-base = develop | `efaaa6034f036dd9538ee35b189217b1d08b90a9` (#1023, KS-1207), tree `38ea11907`. Compare `develop...head` 19:28:48: ahead 1, behind 0, files 1. origin develop unchanged 19:24:23 → 19:28:48 |
| file | `Blockchain/Dev/scripts/audit/audit-baseline.json` blob `45ef8220f` → `e6f2184d2` (+4 −4; `-w` numstat identical) |
| reviews / comments | 0 / 1 (`linear[bot]`). `mergeable_state` unstable. **GitHub Actions is retired for this repo: your local run is the only CI signal** |

## LEGITIMATE SHAPES (the rows are input to a checker)

The shipped predicate is `baseline-contract.mjs` `isLapsed(entry, today = utcToday())`: `utcToday()` = `new Date().toISOString().slice(0, 10)` (UTC), and a row is lapsed when `expires <= today`. So `expires: "2026-10-02"` lapses at **2026-10-02T00:00:00.000Z = Fri 02 Oct 10:00:00 AEST (+1000)** and is live through 2026-10-01T23:59:59.999Z = 02 Oct 09:59:59.999 AEST. Sydney DST starts Sun 04 Oct 2026, after the lapse (`date -j`: UTC midnight 05 Oct = 11:00 AEDT).

| shape — the real event | expected verdict | the clause that yields it | predicted-by |
|---|---|---|---|
| head baseline, real clock (17 Sep) | audit-gate rc 0 "33 … reported, 34 baselined", 0 CLEANUP; audit-locks rc 0 "32 advisories match, 32 already baselined" | rows present, not lapsed | seat, drafter |
| head baseline, frozen 2026-10-01T23:59:59.999Z | audit-gate rc **1**, LAPSED lists 9 rows, **neither wrjc nor 337j** | `'2026-10-02' <= '2026-10-01'` false | drafter |
| head baseline, frozen 2026-10-02T00:00:00.000Z | rc 1, LAPSED lists 11 rows, **including wrjc and 337j "(expired 2026-10-02)"** | `'2026-10-02' <= '2026-10-02'` true | drafter |
| develop baseline, frozen 2026-10-01T23:59:59.999Z | rc 1, LAPSED includes wrjc and 337j "(expired 2026-09-30)" | the pre-PR date | drafter |
| head baseline with wrjc removed | audit-gate AND audit-locks rc 1, exactly GHSA-wrjc NEW | both gates see react-router (root lock + 3 portal locks) | drafter |
| a malformed `expires` | `isLapsed` true (fail-closed) | `!isIsoDate(expires)` | drafter |

## THE SEAT'S CLAIMS (from the READY and PR body; inputs to falsify)

1. One file; both rows `expires` → `"2026-10-02"`; `reason` gains a dated "RE-DATED 2026-09-17" sentence naming KS-528, Kam's ruling verbatim, landing 2026-10-01, *"slip -> report, no second re-date"*; the prior reason is kept.
2. Conservation: 34 → 34, 0 added, 0 removed, 2 altered on exactly [expires, reason], every other row deep-equal, key order kept. Controls unchanged: GHSA-jjmj 2026-09-30, GHSA-frvp 2026-09-30, GHSA-rgwj 2026-09-24.
3. isLapsed, frozen clocks: today all live; 2026-09-30 wrjc/337j live, jjmj LAPSED; 2026-10-01 both live; 2026-10-02 both LAPSED.
4. audit-gate rc 0 (33/34, 0 CLEANUP); audit-locks rc 0 (32/32); `npm run audit:contract` 59/59; control: develop's baseline on the same tree rc 0 / 0.
5. In-hook preflight INCOMPLETE 12/15 (legs 3, 4, 8 skipped: no stack), nothing failed; leg 2 35/35, leg 5 59/59.
6. attachmentsForURL(pull/1025) = KS-528 contributes; 0 closing phrases; open-PR overlap on audit-baseline.json 0 of 19; KS-528 Backlog → In Progress at 09:21:22Z by the GitHub bot, from the body's `Refs`.
7. **NOT COVERED, verbatim:** *"No unit or platform suites (no code or dependency moved; no stack). No image."*

## DRAFTER-MEASURED INPUTS (re-derive them; a wrong one is Wednesday's error, so report it as one)

Substrate: clone `--shared`, detached worktrees develop `efaaa6034` and head `9954a7069` (`GS/setup.sh` → `GS/out/setup.out`); `scripts/audit` `npm ci --ignore-scripts` rc 0 in each; node v24.7.0; porcelain 0 on both worktrees after every probe. Secuura checkout at 19:24:23: porcelain 0, `.git/config` sha256 `d7e7298b02c45f52…`, refs 929, `.git/worktrees` entries 112 (refs move as seats fetch).

- **D1 Conservation (`GS/out/parse_probe.py` → `.out`, from git blobs).** 34 → 34; added [], removed []; altered = {wrjc: [expires, reason], 337j: [expires, reason]}; row order kept; field order kept (`package, reason, ticket, decidedAt, expires`); `$comment` and every top-level key equal. Both prior reasons (249 chars) are an exact prefix of the new ones (873 chars). **Six planted alterations each flip the verdict** (jjmj expires, a target's ticket, row order swapped, field order reversed, a row removed, `$comment` touched). Expires census: develop {09-24: 6, 09-30: 5, 10-15: 4, 10-31: 1, 11-11: 1, none: 17} → head {09-24: 6, 09-30: 3, **10-02: 2**, 10-15: 4, 10-31: 1, 11-11: 1, none: 17}. `decidedAt` stays `2026-07-29` on both rows. Both blobs round-trip byte-identically through `json.dumps(indent=2, ensure_ascii=False) + "\n"`.
- **D2 isLapsed through the shipped module (`GS/out/islapsed_probe.mjs` → `.out`; a `Date` shim; freeze control `utcToday()` = 2030-01-01 under freeze and 2026-09-17 after).** Head: live/live at now, 23 Sep 23:59:59.999Z, 24 Sep 00:00Z, 29 Sep 23:59:59.999Z, **30 Sep 00:00Z (jjmj and frvp LAPSED here)**, 30 Sep 14:00Z (01 Oct 00:00 AEST), 01 Oct 13:59:59.999Z, **01 Oct 23:59:59.999Z**; **LAPSED/LAPSED at 02 Oct 00:00:00.000Z**. rgwj LAPSED from 24 Sep 00:00Z. Develop control: wrjc/337j LAPSED from 30 Sep 00:00Z. The explicit-`today` arm agrees ('2026-10-01' live, '2026-10-02' LAPSED). `date -j`: 2026-09-24 Thursday, 2026-09-30 Wednesday, **2026-10-01 Thursday, 2026-10-02 Friday**.
- **D3 Shipped gates (`GS/out/audit_runs.sh` → `.out` 19:27:24–19:27:55; `GS/out/locks_reach.py` → `.out` 19:28:28; live registry).**

  | run | tree | baseline | clock | result |
  |---|---|---|---|---|
  | G1 | head | head | real | audit-gate **rc 0**, "33 distinct advisories reported, 34 baselined", OK, 0 CLEANUP |
  | G2 | head | develop | real | rc 0, identical lines to G1 |
  | G3 | develop | develop | real | rc 0, identical lines to G1 |
  | L1 / L2 / L3 | head/head, head/develop, develop/develop | | real | audit-locks **rc 0** ×3, "43 standalone lockfiles … 1592 distinct packages pinned — 32 advisories match, 32 already baselined", OK |
  | G4 / L4 | head | head − wrjc | real | **rc 1 / rc 1**, exactly GHSA-wrjc NEW (both gates see the row) |
  | G5 | head | head | 2026-10-01T23:59:59.999Z | rc 1, LAPSED 9, **no wrjc, no 337j** |
  | G6 / L5 | head | head | 2026-10-02T00:00:00.000Z | rc 1 / rc 1, LAPSED 11, **wrjc + 337j "(expired 2026-10-02)"** |
  | G7 | develop | develop | 2026-10-01T23:59:59.999Z | rc 1, LAPSED 11, wrjc + 337j "(expired 2026-09-30)" |
  | C1 / C2 | head / develop | | real | `npm run audit:contract` rc 0, `ℹ tests 59`, `ℹ pass 59`, fail 0, skipped 0, both trees |

  At the real clock head ≡ develop on every gate (G1 = G2 = G3, L1 = L2 = L3): the rows differ only from 30 Sep 00:00Z, which G5 vs G7 shows. react-router 6.30.4 sits in 4 tracked locks (root, frontend/admin, issuer, verifier; control: express 30 entries across 45 locks). **Instrument fault, corrected in the open:** the first `audit_runs.out` ran only 6 of 10 gate runs, because `/bin/bash` 3.2 treats an empty array under `set -u` as unbound. It is quarantined as `audit_runs.out.bash32-unbound-quarantined`; every number above comes from the re-run.
- **D4 Reason text (D1's probe; regexes with the forbidden-pattern lists in the script).** The added sentence names KS-528; "RE-DATED 2026-09-17"; `Kam ruled on 2026-09-17 18:31:25 AEST (decision secuura-audit-rows-react-router-v7-migration, relayed by Wednesday): "Commission the v7 migration AND date both rows to its planned landing (recommended)"`; "planned landing … to 2026-10-01"; "lapse at 2026-10-02T00:00Z (Fri 02 Oct 10:00 AEST)"; *"if it slips past 2026-10-01 the seat reports to Wednesday before then and does not re-date again on its own."* It has 0 closing phrases, 0 Peter/Stuart, and 0 credential-shaped strings (key prefixes, 40+ hex runs, `password=`/`token=`/`api_key=`, mnemonic). **The literal string "slip -> report, no second re-date" is NOT in the bytes** (see DISAGREES 1).
- **D5 Linear and GitHub (`GS/api_read.py` → `GS/api_read.out` 19:28:48–19:29:06).** `attachmentsForURL(pull/1025)` = 1, KS-528 [In Progress], `linkKind='contributes'`, status open. Controls: pull/1021 → KS-1211 contributes (status merged); pull/99999 → 0. KS-528: `completedAt` null, 1 attachment (#1025), 5 comments (the latest `f2ba8180` is the seat's PR note), history `2026-09-17T09:21:22.262Z GitHub Backlog -> In Progress`. KS-528 comments with Peter/Stuart: 0.
- **D6 Merge and overlap (`GS/out/setup.out`, `GS/api_read.out`).** `merge-tree --write-tree efaaa6034 9954a7069` = **`23b56bac07faf84165882176e63436e1c470826e`** = the head tree (develop = parent). Control: develop × develop = `38ea11907` (develop's tree). 21 open PRs: **0 of the 20 others share a file with #1025, and 0 touch `scripts/audit/`** (the READY's "0 of 19" predates #1026, KS-839, 2 files, now open). Seat B's PR-3 (js-yaml + vitest + baseline-browser-mapping; baseline + root lock) is built and held until #1025 merges (`GS/receipt_1025.md`). If it is open when you run, name it.

## WHERE THE READY DISAGREES WITH THE DRAFTER (weigh; do not assume either side)

1. **"slip -> report, no second re-date" is the READY's paraphrase, not the bytes.** The reason carries both clauses in prose: reports to Wednesday before 2026-10-01, and does not re-date on its own. Wednesday's ANSWER step 5 asks for exactly that (mail before 01 Oct 10:00 AEST). PREDICTION: **RECORD, not a finding.** Test the MEANING (both clauses present), and say plainly that the literal arrow form is absent.
2. **"Kam's ruling verbatim."** The reason quotes the panel option LABEL with its "(recommended)" suffix, which matches `answer_kam_rulings_1831.md` and the decision card. It does not carry the option key `migrate-and-date`; it names the card id instead. PREDICTION: verbatim = PASS against the label; RECORD the key's absence.
3. **The ruling second.** The reason and Wednesday's relay say 18:31:25. Wednesday's decision store reads `ruled_ts 18:31:32.038`. This is a 7-second gap between Wednesday's own instruments, and nothing in the bytes depends on it. PREDICTION: RECORD, target Wednesday; not a PR finding.
4. **Overlap "0 of 19" → 0 of 20:** the population grew (#1026). No slip.
5. **audit-locks "(32/32)"** is the script's own "32 advisories match, 32 already baselined": confirmed, not a disagreement.

## WHAT THIS GATE MUST ESTABLISH (minimum set)

1. **Conservation by parse against develop.** 34 rows → 34; exactly GHSA-wrjc-x8rr-h8h6 and GHSA-337j-9hxr-rhxg altered, each on exactly `[expires, reason]`; each prior reason is kept as an exact prefix; row order and per-row field order kept; every other row deep-equal; top-level keys equal. **Planted-alteration control(s) that fire.** `git diff -w` = plain; 1 commit, 1 file.
2. **Expiry semantics through the SHIPPED `baseline-contract.mjs` `isLapsed`, frozen clocks (freeze proven).** Both rows live through 2026-10-01 AEST and live at 2026-10-01T23:59:59.999Z; LAPSED at **2026-10-02T00:00:00.000Z = 10:00 AEST** (state that the shipped code compares the UTC date string, `expires <= utcToday()`). Controls: GHSA-jjmj-jmhj-qwj2 still lapses at 2026-09-30T00:00Z, GHSA-rgwj-5xj2-c3m3 at 2026-09-24T00:00Z, and on develop wrjc/337j lapse at 2026-09-30T00:00Z. Derive the weekdays with `date -j` (2026-10-01 Thursday, 2026-10-02 Friday) and check the AEST offset on 02 Oct.
3. **The shipped gates from `Blockchain/Dev` at head.** `node scripts/audit/audit-gate.mjs` rc 0 (33 reported / 34 baselined, 0 CLEANUP); `node scripts/audit/audit-locks.mjs` rc 0; `npm run audit:contract` all pass (read the `ℹ` lines). **Head + develop's baseline (`AUDIT_BASELINE_PATH`) must equal develop's results** on the same clock. Negative control: remove one target row → both gates rc 1 naming exactly it. Through-gate expiry control: audit-gate at the two frozen instants of item 2, reading the LAPSED list (lesson 3).
4. **The reason text.** It names KS-528, carries Kam's ruling verbatim (against `answer_kam_rulings_1831.md`), says landing 2026-10-01, and states the slip rule (report, no second re-date; rule DISAGREES 1). It contains no credential, no Peter or Stuart mention and no closing phrase. Use regexes with planted positive controls for each forbidden class.
5. **Linking.** `attachmentsForURL(pull/1025)` = KS-528 `contributes` only, 0 with a closing linkKind; controls pull/1021 → KS-1211 and pull/99999 → 0. KS-528 stays **In Progress** (`completedAt` null; the Backlog → In Progress walk at 09:21:22Z by GitHub came from the body's `Refs`, not from the migration). 0 closing phrases in title, body, commit message and every comment (planted controls). §5f: no runtime behaviour changes, and **no ticket moves to Done on #1025** (the migration is KS-528's fix).
6. **Merge.** `merge-tree --write-tree` of the head over the THEN-CURRENT develop in YOUR clone: name the tree and the develop delta. If develop moved, re-run items 1–3 on the merged tree, or prove input identity (baseline blob, `scripts/audit/*` blobs, root lock blob). Re-read open-PR file overlap on `audit-baseline.json` via the PR files API and name any PR touching it (Seat B's PR-3 would).

## BOUNDS

- **Network:** no docker, stack, kintsugi or demo. No `az`. Never the wallet mnemonic. Outbound network is only: `npm ci --ignore-scripts` in `scripts/audit`, what the audit scripts do themselves (`npm audit`, the registry bulk-advisory POST), plus GitHub and Linear GETs.
- **Credentials:** GH_TOKEN and LINEAR_API_KEY are read by NAME inside a script from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env`. Never echo them. GET and queries only.
- **Scratch hygiene:** never `rm` (fresh `mktemp -d` per attempt; quarantine by rename); never `cd` in your tool calls (script files; Python `subprocess(cwd=…)`); no write-verb git from the tool line; `/usr/bin/grep -i` with a same-file positive control; zsh has no PIPESTATUS (`rc=$?` on its own line); never begin a line with `====`; `timeout` is not installed (end a hung run by verified pid); `/bin/bash` is 3.2 (an empty array under `set -u` is "unbound": write runners in Python).
- **Checkout readings:** quote the Secuura checkout's porcelain count, `.git/config` sha256, for-each-ref count and `.git/worktrees` entry count at start and at close.

## REPORT

Write to `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks528-1025-9954a7069-tier2-r1/`: `NOT-TESTED.written-first.md` **written FIRST, before any run**, then `report.md` and `evidence/`. Include FOUND / TESTED / HOW with controls, the conservation table with the planted controls, the isLapsed instant × row table (head and develop), the gate-run table (tree, baseline, clock, rc, lines), the reason-text checks, Linear, the merge tree and overlap, and seat-claim dispositions. **NOT TESTED goes at the same prominence as findings.** Every finding carries evidence class (MEASURED AT RUNTIME / PROBED / READ ONLY / RELAYED), severity, target (PR, seat evidence, Wednesday's brief, or TICKET) and oracle. Name every prediction slip against its predictor.

## VERDICT DESTINATION

ONE mail to `wednesday-agent@agentmail.to`, FROM `coagent@agentmail.to`, subject EXACTLY:
`[QA -> Wednesday] TIER two GATE #1025 (KS-528) 9954a7069 — <GO | GO WITH FINDINGS | NO GO>`

The body holds:
1. the report's BLUF, and the verdict on `9954a7069a16987da140654337555c9a13268b1f` and on the merged tree (name the develop SHA and the tree);
2. plain statements on items 1–6;
3. the **MERGE ADDENDUM**: "squash `9954a7069` onto develop `<then-current SHA>` (merged tree `<OID>`; drafter `23b56bac0` while develop = `efaaa6034`; file-disjoint from every open PR: `<n>`); #1025 attaches to KS-528 only, linkKind contributes, no closes. KS-528 stays In Progress (Refs, never Closes; the v7 migration MIG-1 is the fix; no ticket to Done). Equality targets after the squash: `Blockchain/Dev/scripts/audit/audit-baseline.json` blob `e6f2184d2` (34 rows; wrjc/337j expires 2026-10-02); audit-gate rc 0 33 reported / 34 baselined, 0 CLEANUP; audit-locks rc 0, 32 match / 32 baselined; audit:contract 59/59 (re-measure). Seat B's PR-3 takes develop in after this merge. Records: <yours>";
4. the NOT TESTED block and the report path.

**Mechanism.** The QA project has no `send_brief.sh` of its own. Verdict mails reach Wednesday via the AgentMail API:
- `POST https://api.agentmail.to/v0/inboxes/coagent@agentmail.to/messages/send`
- JSON body `{"to": ["wednesday-agent@agentmail.to"], "subject": "...", "text": "..."}`
- header `Authorization: Bearer $AGENTMAIL_API_KEY`. Your script reads the key by NAME from `/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env` and never echoes it. Build the body from a template file with no shell interpolation.

**The MAIL is the END STATE.** Confirm the API answered 2xx and quote the message id in your final pane line. Timestamps come from `date`, never estimated.

## NOT COMMISSIONED

- **Any fix:** editing the baseline, the PR body or a ticket; re-dating any row (that is Wednesday's ruling under the same card).
- **The v7 migration** (MIG-1, TIER 1 with a real-browser pass, separately gated); the other lapsing rows and their PRs (PR-3..PR-8); any stack, image or deployed environment; messages to anyone but Wednesday (nothing to Peter or Stuart).
