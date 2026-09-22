# DRAFTER REPORT — Seat A 16th kintsugi deploy brief (`2026-09-22_seatA16_kintsugi-deploy-3bad652d1.md`)

Drafted 2026-09-22 15:30–15:58 AEST. Written: the brief and this report only. No host contacted except `api.linear.app` (read-only GraphQL, permitted by commission item (e)); no git write verb anywhere; nothing under `2_Project_Files` touched.

## Proposed subject (for `--subject-file`; line 1 = the subject, the prefix is prepended by send_brief.sh)
`Seat A 16th — deploy develop 3bad652d1 to kintsugi (full rebuild: packages/shared changed) + the FIRST KS-1175-shaped anchor, Kam's ruling a on secuura-ks1175-kintsugi-deploy-and-first-anchor; two STOPs; Seat B/C 19th parallel on the raise lanes`
No routing token in it (checked against `SUBJ_TOKEN_RE`).

## Gate simulation (run against the file)
- Literals at line start: `RULED BY KAM, NOT YET IN AN ARTEFACT` (line 122), `RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE` (128), `PROVENANCE:` (137), `SELF-CHECK: … | 2026-09-22 15:55` (157) — all bare, no heading prefix.
- Scope words (`send_brief.sh:383` regex): 0 hits. "irreversible" appears 3× — `\breversible\b` does not match it (no word boundary inside "irreversible").
- `## QUEUE` heading: none (so the queue-ticket provenance gate does not fire; every ticket named is in PROVENANCE anyway).
- Provenance lines: every `- ` line has ≥ 2 pipes; every relative path in a source field sits on a line carrying "YOUR project" / a `Client/Project` pattern or is absolute/backticked (simulated the gate's awk+grep: 0 offenders).
- Subjects named in the body: the four in (h), each with `(Seat A 16th)`; none carries STOP/HOLD/CHECKPOINT/HAND OVER NOW.

## SIZE — over the 14–20 KB target: 40.5 KB (34 KB body + 6.6 KB PROVENANCE)
Cut twice (51 → 43 → 40 KB). What remains is commissioned content, not padding: the fresh-clone protocol with the exact command (a), the 163-file rebuild classification with Dockerfile/compose line numbers (b), the anchor leg with the real route/line numbers, payload and on-chain shape (c), KS-535 (d), the two comment drafts (e), two ruled sections with 24 cards (e)(f), and per-fact instruments on every line (g). Section sizes: ITEM 0 7.3 KB, ITEM 6 5.7 KB, BLUF 3.4 KB, HOLDS 2.3 KB, ITEM 7 2.1 KB, the two ruled sections 3.8 KB, PROVENANCE 6.6 KB. If Wednesday wants it at 20 KB, the candidates are: the 23-card list → one line naming the A 14th brief as the source (−1.2 KB); READ FIRST items 2/6 (−0.7 KB); ITEM 0 (c)'s per-service bullets → the summary line only (−1.5 KB); ITEM 6's "What #1105 built" paragraph → a pointer to the A 15th history entry (−1.3 KB); PROVENANCE line-number lists (−2 KB). I did not make those cuts because each removes an instrument the seat would otherwise re-derive.

## What I MEASURED (instrument inline in the brief)
- origin develop = `3bad652d17cf111c1e2e1bed1ae7686894637487` (`ls-remote`, 15:30 AEST); shared checkout on `develop` at it, porcelain non-`??` 0; `f9c28a8b8`, `cbae988db`, `3c447abc7` all present locally (`cat-file -t`).
- Range `f9c28a8b8..3bad652d1`: 105 commits, 103 first-parent (#1077…#1175), 163 files. `migrations/` 51 entries at both refs, diff empty. 0 env/compose/Dockerfile/nginx/.sql/prisma files. `packages/shared` 7 files (`body-parser 1.20.6 → 1.20.8` + lock + 5 tests). 25 service dirs with package/lock changes (#1036).
- All 24 `services/*/Dockerfile` COPY `packages/shared`; api-gateway runner stage copies `/shared` (line 55) + `docs/openapi` (69) + `migrations` (75); originate copies `scripts/run-migrations.sh` (47); auth copies `services/auth/scripts` (67); frontends admin/issuer/verifier/website bake shared, status/demo-overlay/outlook-addin do not; `.dockerignore` content; compose build contexts and the yaml bind mount (line 553); the runbook `KINTSUGI-REBUILD-RUNBOOK.md` IS in the tree at `3bad652d1` (445 lines) beside `DRAFT-kintsugi-notice-HELD.md`.
- The KS-1175/KS-1284 code line numbers at `3bad652d1` (anchorSchema.ts 142-155/161/214/230-244/261-315; cardanoMetadatum.ts 7-9/59-75/78-91; transaction.ts 114; anchoring index.ts 450/457/463/699/827/888-891; anchorReadback.ts 16-18/38-54/106-128; gateway proxy.ts 844-849/857-859; scopes.ts 33-36; originate anchors.ts 282 with 0 `identity` mentions; originate documents.ts 614-621 KS-1265).
- The card: `choice='a'`, `ruled_ts=2026-09-22T15:25:32+10:00`; title names develop `7be81d5c9`; 24 undelivered `secuura-` cards (the A 14th's 23 + this one).
- Linear (05:35:20Z, http 200): KS-601 In Progress, 28 comments, last 2026-09-14T10:53Z (still the kintsugi record ticket); KS-1175 In Progress (3 comments, last 2026-09-20T15:17Z); KS-1284 In Progress; KS-1250 Backlog unassigned; KS-535 Done archived 2026-08-04; KS-485/KS-772 Todo.
- Launcher lines 126-135 (deploy-key wiring) and the repo's current `core.sshCommand` (the on-disk `-i` form) — quoted; remote `git@github.com:Secuura/Distributed_Secuura.git`.
- Directory census: `deploy-clones/` absent; `worktrees/` (sibling of `2_Project_Files`) 294 entries incl. `.push-lock-19`; `.git/worktrees` 295; `.env` key NAMES (no values); `.blockfrost_kintsugi` exists (607 B, not read).
- Wednesday's round-19 ANSWER files and mtimes (S1 14:10, plan 14:30 ×2, KS-1164 15:09, C19 addendum 14:10) — the RULED lines quoted from them.
- History: A 15th at line 171, A 14th at line 339, no A 16th entry; the A 14th handover + KINTSUGI-DEPLOY-STATE.md; s187 handover lines 3-60; s189 QA-login handover.

## What I could NOT measure (written as UNMEASURED / "the seat reads at item 0")
Kintsugi's running commit, container census, disk, `REVISION` content, the DB's highest migration, today's KS-535 hashes, the Blockfrost key's network prefix, `CARDANO_NETWORK`, the wallet address/balance, the QA login's validity, the served spec md5, whether the NSG line still holds. Kam's board timestamp 15:24:16 is Wednesday's own read relayed in the commission (I could not read the live board); the card file says 15:25:32 — both are in the brief.

## Where the templates / records CONTRADICT what I found (Wednesday should know)
1. **The A 14th "api-gateway byte-identical" expectation does NOT carry:** `packages/shared` changed and every backend Dockerfile bakes it, so the brief tells the seat to expect NO byte-identical backend and a CHANGED served-spec md5 (the 14th's V3 inverted). The commission's "if packages/shared changed, every image baking it rebuilds" is exactly what happened — it is a full rebuild in the s187 shape, not a scoped one.
2. **The s187 brief's `worktrees/s187-kintsugi` build-source pattern is replaced** by the fresh clone (commission item (a)); `worktrees/` is a sibling directory of `2_Project_Files` but `git worktree add` still writes into the shared `.git/worktrees/` (295 entries), which is why the clone is the only shape that satisfies the top line.
3. **The card's title names develop `7be81d5c9`; the tip is `3bad652d1`.** The brief pins to `3bad652d1` and says so.
4. **KS-535 hash:** the A 14th recorded NO sha16 (it used the wallet-prefix method); the only kintsugi hash on record is s187's `695d09df873ff42b` (2026-09-11). The brief says so and does not invent a 14th value.
5. **The root `CLAUDE.md` never names kintsugi** (grep 0; control `demo` 50) — its deploy text (steps 1-3, lines 173-201) is written for local + demo. The brief cites it only for the notification rule (185-201, 187), Peter's-nod rule (232, 238-239), KS-535 (11), migrations-baked (19) and the tenant (23).
6. **The A 15th handover says "a real PREVIEW anchor"** for the §5f sweep; the brief keeps the network UNMEASURED (commission item (c)) and requires the seat to state it before anchoring.
7. **The commission said "the 13-PR tree of the 18th round, see history.md line ~35"** — at my read the `3bad652d1` tip is Seat C 18th's six over Seat B 18th's seven over #1036 (history.md top entries); the range from `f9c28a8b8` is 103 first-parent squashes, not 13. The brief states the measured number.
8. **Wednesday's ANSWER to Seat C 19th (Q-1031)** re-words the 048 hold "after the merge" of the `run-migrations.sh` PR — that PR is round 19 and NOT in `3bad652d1`; the brief carries the 048 line unchanged.
9. The `originate` `/api/anchors` forwarder drops `identity` (0 mentions) — so the commission's "the originate flow" cannot be the anchor path; the brief names the gateway → anchoring direct path and says why.

## Residual risks for Wednesday's read
- The gateway's CSRF middleware and `x-emitter-*` strip may block a bearer-only POST from outside; the brief tells the seat to meet them, not route around — if that fails, the plan will need a ruling on an in-network POST (from the box, to `anchoring:4005`) which the brief does not pre-authorise.
- The QA-gate OWNER login is 10 days old; validity UNMEASURED.
- Disk: ~30 images vs the 14th's 3; the 4000 MB guard + the 4.4 G transient could STOP the round at ITEM 2 — the brief makes that a mail, never a prune.
