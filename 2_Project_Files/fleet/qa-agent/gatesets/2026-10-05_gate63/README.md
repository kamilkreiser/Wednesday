# Gateset 2026-10-05_gate63 — README for Wednesday

Drafted 2026-10-05, 10:31Z – 11:3xZ UTC (21:31 – 22:3x AEDT), by a drafting subagent. Every figure names the kit file it came from. Every builder statement below is a CLAIM the gate re-measures; the prompt says so.

## 0. What this gate is, and its status

**gate63 is a T1 gate over ONE Secuura/Blockchain PR: #1388, the second half of KS-1404 — "timestamping ships its trust anchors and compose points the verifier at them".**
- Author AND merger: **Seat D 8th**, pane `Secuura/Blockchain-D`. KS-1404 stays In Progress (the PR is `Refs`).
- **GO string:** `GO (Seat D 8th): merge 1388 on gate63`
  - **If Seat D 8th has WRAPPED before you sign, substitute the LIVE D-lane seat** in that string. The gate writes it as above.
- **NO GO string:** `NO GO (gate63): 1388 at 3ce575eeb63c — <N-1388-n: the blocker, one line>`
- **Information for the GO block (not a gate condition):** Kam's card `secuura-ks1404-anchors-before-049-merge-order-1005` = a, *"Hold #1383's merge until the anchor wiring has merged."* So #1383 (migration 049, Seat F 3rd, gate61r2) merges only AFTER this PR.
- **The head is single-parent on the base, with no merge-in** (`ex/c1_head_ex1.out`, rc 0, 13/13):
  - head `3ce575eeb63c1e2582287c72e75f0ff320d458f8`, branch `feature/ks-1404-tsa-anchor-wiring-d8-1`
  - parent `f01c1da5717f` (the base). **END_TREE `979926afe755107f970f70188447a02113d646e6`**, measured.
- **develop has moved TWICE.** It was `0f2422925317` at the READY (#1382 KS-1005, 09:55:16Z). It is **`32e058975d4e` since 10:43:37Z**, when #1387 KS-1388 merged while this kit was being drafted. The merge needs a **docs-only merge-in**, judged by Q-M (section 1). develop is RECORDED at launch, never refused.
- **9 paths, all 100644, measured:**

  | path | +/- |
  |---|---|
  | `Blockchain/Dev/docker-compose.yml` | +7/-1 |
  | `services/timestamping/Dockerfile` | +5/-0 |
  | `services/timestamping/config/README.md` | +16/-3 |
  | `services/timestamping/config/tsa-trust-anchors-dtrust.crt` (new) | +38/-0 |
  | `services/timestamping/src/__tests__/ks1404-wiring.test.ts` (new) | +226/-0 |
  | `services/timestamping/src/tsa/qualified-tsa.ts` | +11/-3 |
  | `services/timestamping/src/tsa/rfc3161-verify.ts` | +9/-4 |
  | flow doc | +23/-4 |
  | cheat doc | +5/-2 |

**Status: KIT COMPLETE, NOT LAUNCHED.**
- Every helper has a quiet case and firing arms, and every arm fired (section 3).
- The dry run returns rc 0 and reports only the routing line as missing (section 5).
- **Three things are yours:**
  - the routing line (section 4);
  - **whether Docker Desktop is running when the gate reaches C6** (W2);
  - the launch (section 7).

**The rulings the gate checks against** (quoted in the prompt):
- **Kam's card `secuura-ks1404-tsa-trust-and-library-1004` = a.** *"pkijs + trust the authority each environment's TSA_URL already points at"*, detail *"The seat measures TSA_URL per environment first, pins that provider's published root in config…"*
- **Your Q-SCOPE ruling.**
  - ONE per-provider anchor file holding ONLY the D-Trust root: D-TRUST Root CA 1 2017, DER sha256 `4d24807b9cad5110f40ed79d934346d7c9b0290431dc9b11a40bbb86fcf2aef6`.
  - Byte-identical to block 1 of the already-committed bundle `config/tsa-trust-anchors.crt`.
  - NO DigiCert root in the new file.
  - The compose default serves both boxes. NO `.env` edit. `docker-compose.production.yml` is OUT.
- **Both boxes resolve to D-Trust.** Kintsugi is PINNABLE-BY-CONFIG / UNEXERCISED. Demo is MOCK-ONLY, on one row dated 2026-07-30.

**What the drafter did:**
- **Writes:** only inside this directory.
  - `_scratch/clone` is a `git clone --shared --no-checkout` of the checkout. Its alternates point at the checkout's objects, which are read only.
  - `_scratch/wt_base`, `wt_head` and `wt_merge` are worktrees of THAT clone. `npm ci --ignore-scripts` ran in timestamping and `packages/shared` there.
  - SIM commits and trees went into the clone's object store only. No ref was written in the checkout.
  - **Small exception to "only inside this directory":** three `.crt` extracts went to the session scratchpad at first read (`…/scratchpad/g63/`). They are not in the kit.
- **In `/Volumes/DevMASTER/!CODING/`:** read verbs only (`ls-remote`, `show`, `log`, `diff`, `ls-tree`, `cat-file`, `rev-parse`, `merge-base`, `grep`, `config --get`, `status`), plus the clone source read.
  - **No fetch anywhere.** Every object needed was already in the shared store, including `32e058975d4e` and `48a9df70a5b6`.
  - **No merge-tree.** The independent merge cross-check was a `git merge --no-ff --no-commit` in `_scratch/wt_merge` (own clone), then aborted.
- **Network:**
  - GitHub REST GETs only: pulls/1388, its files, the open-PR census, and pulls/1387 / 649 / 575. GH_TOKEN was read by name and never printed.
  - npm registry reads for the scratch `npm ci`.
- **Not done:**
  - No Docker build (the daemon was down; section 2, W2).
  - No Linear read. No launch, no routing edit, no mail, no `rm`.

**`_scratch/` holds nested git repos and node_modules (about 1 GB).** Never `git add` it into the WEDNESDAY repo. Its worktrees are registered in `_scratch/clone` only.

## 1. Drafter predictions at 3ce575eeb63c over f01c1da5717f (the gate re-derives every one)

| check | file | result |
|---|---|---|
| C1 pin + scope | `ex/c1_head_ex1.out` (rc 0, 13/13) | **P1** origin pull/head == branch == head; develop `0f2422925317` recorded, descends from the base. **P2** one parent. **P3** 9 paths, exact +/-. **P4** tree `979926afe755` (control: base tree `ba3527224ff6`). **P5** trailers 1 raw byte (control 55). **P6** 0 Co-Authored-By. **P7** subject 85 chars. **P8** ONE `Refs KS-1404`, 0 STRICT closing refs (planted control 2), WIDE 0. **P9** all 100644. **P10** compose hunks (1243,1)+(1245,0→5) inside BASE block 1212–1269, next key `anchoring:`. **P11** env entries 14 → 15; the ONLY added key is `TSA_TRUST_ANCHORS_PEM=${TSA_TRUST_ANCHORS_PEM:-/app/config/tsa-trust-anchors-dtrust.crt}`; 0 removed or changed; every other changed line is a comment; outside-block lines identical. **P12** Dockerfile: 0 removed, ONE code line `COPY --from=builder /app/config ./config`, last FROM :35 < COPY :49 < chmod :55. **P13** 9 must-be-unchanged paths identical (production compose, both `.env.example`, package files, openapi, the old KS-1404 test, the bundle, `.dockerignore`). **Real control** `ex/c1_basehead_ex1.out`: rc 1, 10 FAIL |
| C2 anchor | `ex/c2_head_ex1.out` (rc 0, 7/7) | python AND openssl: 1 cert (bundle 2); DER sha256 `4d24807b…aef6` on both; == bundle block 1 (2,354 bytes), bundle unchanged base→head, block 2 differs; DigiCert absent (found in the bundle); CN `D-TRUST Root CA 1 2017`, self-signed, notAfter 2032-02-01; 0 bytes outside the armour; README records `4D:24:80:7B…` |
| C3 red-first | `ex/wiring_base_redfirst_ex1.out` (rc 1) | the head test alone in wt_base: **3 failed (A, B, C1) / 3 passed** — reproduces |
| C3 head | `ex/wiring_head_ex1.out` (rc 0); `ex/suite_head_ex2.out` (rc 0) | file 6/6; **whole suite 7 files / 86 passed** once shared is built. `ex/suite_head_ex1.out` = an instrument trip WITHOUT shared: 3 failed / 58 passed (61), 2 suites fail to LOAD |
| C3 comment-only | `ex/c3_src_ex1.out` (rc 0); `ex/c3_dist_ex1.out` (rc 0) | src: token lists equal (790 / 1841 tokens), raw differ, lexer controls fire. dist: 9 .js both sides, 0 token-different, 2 raw-different (qualified-tsa.js, rfc3161-verify.js). 9 .js.map raw-different, because `sources` carries the worktree NAME (INFO) |
| C3 tsc | `ex/tsc_{base,head}_ex1.*` | **rc 0, 0 errors at BOTH ends** (shared built). The builder claims ONE pre-existing TS2345 at both ends (D8) |
| C3 probe | `ex/probe_quiet_head_ex2.{out,jsonl}` (rc 0, 8/8) | P1 real file by path → "signer certificate does not chain…" (parsed). P2 1 anchor @4d24807b (bundle 2). P3 `/app/config/tsa-trust-anchors-dtrust.crt` missing → valid false, "no trust anchor configured", no throw, logged "could not be read". P4/P5/P6 fail closed. P7 synthetic root by path → true. P8 bundle by path → parsed |
| C4 docs | `ex/c4_docs_ex1.out` (rc 0, 7/7) | flow: changes confined to 11. (:1887–:1999 → :2018), h2 identical (13), `</body>` 1/1, h3 11.1–11.3 → +11.4; 11.2 "previously read", 11.3 "used to end". cheat: confined to KS-1404 section (:3726–:3778), rows 12 → 13, one new KS-1404 row. **INFO D7: 0 hosts named in either new text. INFO D8: "row below" at :3778 points at the wiring row at :3748, which is ABOVE** |
| C4 Q-M | `ex/c4_predict_realdev_ex2.out`, `ex/c4_predict_dev32e0_ex1.out`, `ex/gitmerge_*` | **develop 0f2422925317 → `7b46a0e04d743ae571a814725b85f56ec5130b17`; develop 32e058975d4e → `549e05e3ececa88e302566e974cd60ff6671aa9d`.** Each prediction == the tree of `git merge --no-ff --no-commit` in the drafter's own clone (clean auto-merge of both docs). `qm` M1–M7 PASS on SIM merge-ins at those trees (`ex/c4_qm_realdev_sim_ex1.out`, `ex/c4_qm_dev32e0_sim_ex1.out`) |
| C5 PR text | `ex/c5_pr1388_ex1.out` (rc 0, 7/7) | body 7,029 B, `updated_at` 10:28:11Z (`api/pr1388_body_drafter.md`, sha256 `c2c1f805d8358226…`). One Refs + URL; STRICT 0 (control 2), WIDE 0; only KS-1404; title == subject; required content present; image proof declared NOT run. FIG: "1937 packages", "TS2345 344→349", "all 9 emitted .js" |
| C6 image | `ex/c6_real_ex1.out` (rc **20**) | **NOT RUN: the Docker daemon was down at drafting** (`desktop-linux` socket absent; client 29.8.0). The gate may find it up (W2) |
| census | `ex/census_ex2.out` (rc 0, 10:5xZ) | 24 others: **0 OVERLAP**, 2 NEAR (#649 and #575, dependabot bumps of `timestamping/package.json`, open since 2026-07/08), 3 DOCS (#1383, #1384, #1385). Control FIRES on #1388. #1387 is no longer open: merged 10:43:37Z |

**Drafter's reading.** Every artefact claim in the READY that the kit can measure reproduces:
- head, base, END_TREE
- 9 paths
- the anchor's count, digest, block-1 identity and the absence of DigiCert
- compose hunks inside 1212–1269, with nothing else in compose changed
- the Dockerfile order
- red-first 3/3
- 6/6 and 86/86
- comment-only by projection
- 0 trailers, Refs-only

**Three figures do NOT reproduce** (D8):
- 1937 packages
- the TS2345
- the body's `:289`, which is the base's line; the refusal is at `:294` on the head

## 2. Doubts for the GATE to rule (the prompt carries D1–D11), and items for Wednesday

- **D1 TIER: T1 confirmed by the drafter.** The change sets which root the verifier trusts on every box, and it touches the runtime Dockerfile and compose.
- **D2 Cell (C) as built vs as briefed.**
  - The brief's (C) was "behaviour through the wired value".
  - The PR has C1 instead: a static check that the tree file exists and holds the D-Trust root alone. It also has C2: a SYNTHETIC root delivered by file path verifies.
  - Nothing in the PR's suite proves that the REAL D-Trust file parses inside the verifier.
  - The kit's probe P1/P2 does prove it. The gate rules whether the PR needs a cell for it.
- **D3 Cell A does not bind the default's variable name.** Its regex is `^\$\{[A-Z_]+:-(.*)\}$`. The drafter predicts tamper T-NAME stays GREEN. Likely polish.
- **D4 The image ships the WHOLE `config/` directory.**
  - The two-root bundle WITH DigiCert lands at `/app/config/tsa-trust-anchors.crt`, beside the per-provider file.
  - Q-SCOPE's "no DigiCert in the new file" holds. But a one-line box `.env` override would trust DigiCert.
  - Observation or finding: the gate rules.
- **D5 A missing anchor file is SILENT until a verify.**
  - The verifier fails closed with one `logger.error` per verify call (probe P3).
  - `/health` (`src/index.ts:162`) reports the TSA provider and url, but no anchor state.
  - So ITEM 3's kintsugi sweep must check the file in the container. `/health` cannot show it.
- **D6 A false sentence in the cheat sheet.** The corrected note at :3778 says "see the wiring row below", but the row is at :3748, above it. Minor, in a client-facing doc.
- **D7 No host named.** Skill §4 asks for "every figure with its date AND the host". Neither 11.4 nor the cheat row names a host, and both state red/green figures.
- **D8 Claims that do not reproduce for the drafter:**
  - "1937 packages": the drafter measured 267 (timestamping) + 349 (shared).
  - "one pre-existing TS2345 at both ends": the drafter measured tsc rc 0 with 0 errors at both ends.
  - the body's `rfc3161-verify.ts:289`.
  - The drafter's environment may differ from the builder's, so the gate rules.
- **D9 The KS-1005 cheat section on develop is UNWRAPPED** (gate62 N-1387-6). It lies outside the KS-1404 section, so the key-anchored prediction is unaffected. Measured on both develops; the gate confirms.
- **D10 PREFLIGHT-INCOMPLETE 12/15** (legs 3, 4, 8: no stack). Is that acceptable named residue for a T1 change? The gate may run preflight (X1).
- **D11 #649 and #575 (NEAR):** would either change what the image's `npm ci` installs if it landed first?

**Claim contradictions found by the drafter:** the three in D8. Everything else in section 1 is consistent.

**For Wednesday (not the gate's):**
- **W1. The GO names Seat D 8th.** If D 8th has wrapped, substitute the live D seat when you sign.
- **W2. The image proof needs the Docker daemon UP.**
  - It was DOWN at drafting (`ex/c6_real_ex1.out`: rc 20, NOT RUN). The kit refuses to let the gate start Docker Desktop itself, because other seats share this machine.
  - If you want C6 measured rather than NOT RUN, start Docker Desktop before the launch. The dry run and the launch both RECORD the daemon state (step 3d).
  - Budget: 2 builds × up to 1200 s, plus a Docker Hub pull of `node:24-alpine` and the Dockerfile's own `npm ci` steps.
- **W3. The merge-in.** The GO covers a docs-only merge-in M only if `c4_docs_gate63.py qm --repo <clone> --merge-in-head M --develop-after <develop>` passes M1–M7 on the real develop. Run it as the merger or as a gate.
  - The target tree on `32e058975d4e` is `549e05e3ecec`.
  - If develop moves again first (e.g. #1384 or #1385 lands), `c4 predict` gives the new target. It refuses only if develop touched a non-doc kit path or a KS-1404 section, and that re-gates.
- **W4. A moved HEAD refuses** the launcher (rc 6) and the action (rc 11). That is a re-draft (section 9).
- **W5. `mergeable_state` was `unstable`** at drafting. It carries no testing claim.

## 3. The kit's instruments (each exercised; outputs in `ex/`)

| script | what it does | quiet case | firing arms (all fired) |
|---|---|---|---|
| `lib_gate63.py` | `git()` READ verbs only; `wgit()` write verbs only outside `!CODING` (lexical + realpath); GH GET with the token by name; `Tally`; STRICT and WIDE closing predicates | — | refusals exercised via c4 (`ex/c4_refusal_ex1.out`, rc 2) |
| `c1_pin_gate63.py` | P1–P13 | `c1_head_ex1` rc 0 13/13 | `c1_selftest_ex1` **23/23**: a 10th path, +/- drift, the anchor missing, two parents, tree == base, a trailer, a blind trailer control, Co-Authored-By, `(#1388)`, a 2nd Refs, KS-1376 hyphenated, STRICT `Closes KS-1404`, 100755, pull/head moved, develop not descending, the entry moved into `anchoring:`, LOG_LEVEL changed, the default pointed at the bundle, a line outside the block, COPY after chmod, `USER root` added, the production compose moved. Real control `c1_basehead_ex1` rc 1 |
| `c2_anchor_gate63.py` | A1–A7 (python + openssl) | `c2_head_ex1` rc 0 7/7 | `c2_selftest_ex2` **10/10**: DigiCert appended, the whole bundle, a flipped base64 char, a leading comment, CRLF, DigiCert alone, an empty file, the bundle changed base→head, the README fingerprint altered. **History:** `c2_selftest_ex1` = an INERT README arm (the README uses colon form; the tamper never landed). It now asserts the tamper landed |
| `c3_comments_gate63.py` | `src` S1–S2 / `dist` J1–J3, a JS/TS comment-stripping lexer | `c3_src_ex1` rc 0; `c3_dist_ex1` rc 0 | `c3_selftest_ex1` **5/5**: two CODE tampers and a STRING tamper fire; a COMMENT-only tamper stays quiet. `c3_dist_fire_ex1` rc 1: a code token changed in emitted JS fires J2 |
| `c4_docs_gate63.py` | docs D1–D8; KEY-ANCHORED predict; qm M1–M7 | `c4_docs_ex1` rc 0 7/7; predict == git merge on both real develops | `c4_selftest_ex3` **23/23**: 11.4 promoted to h2 `33.`, an edit in 12., the close tag, 11.2 loses "previously read", 11.4 drops the base sha; a 2nd KS-1404 row, an edit in KS-1333, the digest dropped, a duplicated KS-1404 key. Then: predict(base) == END_TREE; key-order != tail-order on the real develop; a SIM #1387-shaped develop with an UNWRAPPED cheat section; Q-M positive control; tail tree (M1), single parent (M2), an extra path (M1+M3), Co-Authored-By (M4), develop touching compose (M6), develop editing 11.3 (M6), two new commits (M2+M7); predict REFUSES both bad develops. `c4_refusal_ex1`: predict in the shared checkout → rc 2. **History:** `c4_selftest_ex1` and `c4_predict_realdev_ex1` = an instrument trip: `rev-parse <rev>:<absent>` echoes its argument, so two absent paths compared unequal and predict refused. Fixed with `--verify --quiet`; the trip is kept |
| `c5_prtext_gate63.py` | T1–T7 + FIG | `c5_pr1388_ex1` rc 0 7/7 (live fetch) | `c5_selftest_ex1` **13/13**: Refs removed, a 2nd Refs, `Closes KS-1404`, `fixes #1388` in the message, `resolves: KS-1404`, KS-1376, `(#1388)`, CRL/OCSP removed, the false→true sentence removed, Co-Authored-By, the image proof claimed as run. A QUIET arm: the English noun "fix" in prose stays 0 under STRICT (the builder's own fault 1) |
| `c6_image_gate63.py` | the image proof I1–I6, bounded; NOT RUN 20/21/22; build failure 23 | `c6_real_ex1` rc 20 NOT RUN (real daemon down) | `c6_selftest_ex1` **7/7** with a stub docker kept in the gate's scratch: daemon down 20, a quiet good run 0, the head anchor unreadable 1, a build hanging past a 3 s budget 21 (client killed), a network failure 22, `--out` inside `!CODING` 2, the worktrees swapped 2. `G63_DOCKER` is refused on a real run |
| `probe_anchor_gate63.test.ts` | runtime probe P1–P8 (copied into the gate's worktree, then quarantined) | `probe_quiet_head_ex2` rc 0 8/8 | `probe_fire_corrupt_anchor_ex1` rc 1 (P1, P2); `probe_fire_rethrow_ex1` rc 1 (P3, P4). Each tamper landed (sha asserted) and was restored by content; the worktree status was clean after |
| `gh_census_gate63.py` | OVERLAP / NEAR / DOCS census | `census_ex2` rc 0, control FIRES | `census_selftest_ex2` **8/8**. **History:** `census_ex1` rc 15. The first classifier called #649 and #575 OVERLAP, which would refuse every launch, so they are now NEAR (reported, not refused) |
| `launch_qa_secuura_ks1404_1388.sh` | the pane launcher: static prompt; re-reads origin; refuses a moved head (6), a develop that does not descend from the base (17), no TTY (21), overrides (16), prompt defects (8 / 33 / 39 / 25) | `--check` rc 0 | `ex/launcher_arms_ex2.out` (section 5) |
| `repin_and_launch_gate63.sh` | the launch action, steps 0–7 | `--dry-run` rc 0 | section 5 |
| `prompt_gate63.txt` | the gate's prompt | — | — |

`fixtures/`, `sim/`, `api/`, `_scratch/` and `_quarantine/` are drafter exercise output. They are never launched.

## 4. Routing line — NOT added
Back up the file first. Then add ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`:
```
QA/Secuura-ks1404-1388|coagent@agentmail.to|yes
```
Until it is present, step 0 of the real launch refuses rc 1. The dry run reports it instead.

## 5. Dry run and refusal arms
See `ex/dry_console_ex1.out` and `ex/launcher_arms_ex2.out` / `ex/repin_arms_ex1.out`. The results are summarised in the drafter's reply to Wednesday. The dry run reports:
- the routing line missing
- the census (0 OVERLAP)
- both head instruments agreeing
- develop recorded and descending
- C1 13/13
- the Docker daemon state
- the launcher `--check` rc 0

## 6. Rung-5 check (after the launch)
Within ~2–5 min, read the new pane (id from the launch's pane census): `/opt/homebrew/bin/tmux capture-pane -p -t <pane_id> | tail -60`.

It passes rung 5 only if it shows something only THIS commissioned gate would produce:
- the agent naming **KS-1404 / #1388**
- the head `3ce575eeb63c`
- a `*_gate63.py --selftest` run, or `CHECKED 23`
- the D-Trust digest `4d24807b`

**Rung 6** is `NOT-TESTED.written-first.md` appearing under `…/2026-10-05-ks1404-1388-g63/`. A bare prompt, a generic greeting, ctx, an exit code or a pane existing proves nothing.

## 7. How Wednesday launches it (after section 4's routing line; W2 first if you want C6 measured)

**Facts the launch uses:**
- Pane: `QA/Secuura-ks1404-1388`
- Report dir: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-05-ks1404-1388-g63/`
  - `NOT-TESTED.written-first.md` first, then `evidence/`, then `report.md` with `## MERGE ADDENDUM` last
  - `sha256 report.md` goes in the mail
- Verdict mail (from coagent@ to wednesday-agent@), subject: `[QA -> Wednesday] GATE63 #1388 (T1 KS-1404 wiring: timestamping ships the D-Trust anchor and compose points the verifier at it; author and merger Seat D 8th)`

**Launch commands.** Run them under `script -q /dev/null`, as gate58–62 were, so the TTY guard is satisfied. Dry run first:
```
script -q /dev/null bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate63/repin_and_launch_gate63.sh 1388 3ce575eeb63c1e2582287c72e75f0ff320d458f8 --dry-run
script -q /dev/null bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate63/repin_and_launch_gate63.sh 1388 3ce575eeb63c1e2582287c72e75f0ff320d458f8
```

**Exit codes:**
- rc 1: routing
- rc 9: input
- rc 3: API failure or a blind census control
- rc 15: OVERLAP
- rc 2: ls-remote
- rc 11: the head moved (RE-DRAFT)
- rc 10: develop does not descend from the base
- rc 13: C1 failed at the head, or the launcher's `--check` refused
- rc 16 / 12 / 14: override / usage gate / cockpit

**develop moving is NOT a refusal.** The Docker daemon state is recorded, never refused. Add `WED_USAGE_STOP=…` only with Kam's recorded authority.

## 8. NOT-RUN list (template for the gate's NOT-TESTED.written-first.md; the gate edits, never shortens)
- [ ] C6 image proof — if NOT RUN: `rc <20|21|22>`, reason `<daemon down | budget exceeded | network>`. I1–I5 are UNMEASURED, never inferred.
- [ ] The root-to-TSA binding: no real D-Trust token exists on either box (kintsugi 0 rows; demo 1 mock row).
- [ ] Real RSASSA-PSS chain validation under the D-Trust root (no real token).
- [ ] CRL / OCSP revocation; TSA policy OIDs.
- [ ] Whether either box's `.env` overrides the default (the builder's READ ONLY claim; no SSH from the gate).
- [ ] The kintsugi deploy and the §5f live sweep (ITEM 3, its own round); demo (ITEM 4; never a 049 SHA).
- [ ] Preflight legs 3 / 4 / 8 (PREFLIGHT-INCOMPLETE 12/15 is not a pass), and the whole preflight unless run.
- [ ] A REAL merge-in head (none exists yet; Q-M judges it later).
- [ ] Anything skipped for budget, with the reason.

## 9. Re-draft recipe (the HEAD moved; a moved develop is NOT a re-draft)
1. Re-read `ls-remote` + pulls/1388.
2. Re-measure kit `head`, `end_tree`, `files` (+/-), `head_blobs`, `compose_block_base_range`, the anchor digest, the subject and the body.
3. Edit the head in `kit.json`, `prompt_gate63.txt` and `launch_qa_secuura_ks1404_1388.sh`. They are static: there is no fill step.
4. Re-run every `--selftest`, then c1, c2, c3, c4 docs + predict, c5, the census, and a `--dry-run`.
5. A docs-only merge-in by the builder on top of `3ce575eeb63c` is NOT a re-draft. It is judged by `c4 qm` (Q-M). Any other new head is.
