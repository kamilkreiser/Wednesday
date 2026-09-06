# QA Agent Invocation Brief — Secuura / Blockchain (SEAT A), PR #852 (KS-490 (3)) @ `8acf0d260` — TIER 2, through-code, CONFIG, NARROW (~10 min): every `deployment/azure` pointer at the decommissioned Secuura tenant repointed at the live Founders Hub demo estate — 4 files +14/−14, two commits

**TIER 2 — reason (Kam's 2026-09-05 20:19 grant):** configuration files that NO code path consumes (the builder measured `deploy.sh` passes every value inline) — through-code only; nothing runs, nothing deploys, **NO `az` command by anyone**. Round 1 of the class. The builder's tree is LIVE — own by-SHA clone only.

**R0 (client isolation):** exactly one client's content — Secuura / Blockchain. Report under `projects/secuura/`. Nothing from any other client.

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`.

## 1. Target
- **Head:** `kamilkreiser/ks-490-repoint-stale-azure-parameters` = `refs/pull/852/head` = **`8acf0d260abf81a9b0f26153c1d1289f06e9774d`** (Wednesday's `ls-remote` 14:03:05); TWO commits on merge-base `5c69ee8b6…` (`e9b772e29` the two key-vault ids in `main.parameters.json`; `8acf0d260` the widening); **`develop` = `81bf7b078…`; `merge-tree --write-tree 81bf7b078 8acf0d260` = rc 0 (`82acc2da…`)** — re-derive.
- **Diff (Wednesday's numstat + BOTH commits' diffs READ WHOLE, 13:55 / 14:03):** `main.parameters.json` 5/5 · `services.parameters.json` 7/7 · `main.bicep` 1/1 · `services.bicep` 1/1 — the six identical key-vault ids (`/subscriptions/27ef4264-…/resourceGroups/secuura-staging-rg/…/vaults/secuura-staging-kv` → `/subscriptions/a0ee7d32-2e4a-47a0-9a49-9c001817a545/resourceGroups/secuura-demo-rg/…/vaults/secuura02-demo-kv`), the three env values in each parameters file (`staging` → `demo`, `westeurope` → `southeastasia`, `secuura01` → `secuura02`), and the two bicep usage comments' `--resource-group`.

## 2. Claims to FALSIFY (Wednesday's own reads are labelled; the rest are the builder's)
1. **The values are the LIVE estate's — READ against the sources, do not trust the PR body:** `!CODING/Secuura/CLAUDE.md:9` (subscription), `!CODING/Secuura/Blockchain/CLAUDE.md:38-50` (demo env, `secuura02`, `secuura-demo-rg`, `secuura02-demo-kv`, region `southeastasia`), and `.github/workflows/deploy-demo.yml:42-48` at the head (KS-552's block: `secuura-demo-rg` / `southeastasia` / `secuura02` / `demo`). Wednesday read all three at 13:55–14:03 and they agree with the diff; confirm independently, and confirm the DISCRIMINATOR the builder named — `uksouth` at `CLAUDE.md:25` is the OLD region, so a source saying `southeastasia` is choosing, not defaulting.
2. **Counts at the head, per file, with a control that fires (Wednesday's from objects: `27ef4264` 0/0; `a0ee7d32` 2/4; `staging`/`secuura01`/`westeurope` 0/0 in both parameters files; `secuura-demo-rg` 2/4/1/1 across the four files):** re-derive; the builder's control = the same sweep over the rest of `deployment/azure` still returns ~99 lines across 11 files.
3. **Both JSONs parse** (Wednesday: 5 and 9 params) and the `-U0` hunks are exactly `:6 :9 :12 :17 :25` (main), `:6 :9 :12 :23 :31 :39 :47` (services), `:11` (main.bicep), `:7` (services.bicep) — nothing else moved.
4. **No code path consumes either parameters file (builder's):** `grep -c 'main.parameters\|services.parameters' deploy.sh` = 0 against a control (`services.bicep` hits ≥1 file); each file is reached only from its bicep's usage comment and from `scripts/check-no-latest-tags.sh`'s scanned list (`:37`). Re-derive; state the exposure in one sentence.
5. **`scripts/check-no-latest-tags.sh` exits 0 at the head, read as the SCRIPT's status (not a pipe's); a planted `"secuura01:latest"` in `main.parameters.json` makes it exit 1 naming the file and line** (the builder's plant); restore by hash.
6. **Two shapes deliberately NOT widened to (builder's, Wednesday confirmed at the head): `setup-keyvault.sh:27` `SUBSCRIPTION_ID="27ef4264-…"` (a script that would `az account set` to the DELETED subscription) and `main.bicep:15` / `services.bicep:21` `param environment string = 'staging'` (template DEFAULTS).** Confirm both exist at the head unchanged; record as a follow-up ROW (executable default + runnable script = a different shape), NOT a finding against this PR. Do NOT run `setup-keyvault.sh`.
7. **Scope hygiene:** exactly 4 files; `rev-list 5c69ee8b6..8acf0d260` = 2; nothing under `services/*`; no `.github/` change; **no `az` call anywhere in the builder's evidence** (read the PR body's Test Evidence for an `az` line — there must be none).
8. **Secret gate:** canary that FIRES first (standing line #46), then `gitleaks git --log-opts=5c69ee8b6..8acf0d260`. The dead subscription id is not a secret; the key-vault paths carry no values.
9. **NOT COMMISSIONED:** any deployment; `az`; the demo; #845/#849/#851; the 11 documentation files still naming the dead estate (README, `env.staging.example`).

## 3. Scope / boundary / logistics
Own by-SHA clone; findings only; never fix, never write tickets, never touch the builder's tree, never call out, **never run `az` or any deploy script**, never `--no-verify`, never `rm`. **Time-box ~10 minutes.** Findings sink: `projects/secuura/reports/2026-09-06-s139-ks490-3-852-8acf0d260-tier2/report.md` + `evidence/`. Escalation through Wednesday (`wednesday-agent@agentmail.to`, QUESTION). **When done:** mail Wednesday FROM `coagent@agentmail.to`, subject `[QA -> Wednesday] Secuura KS-490 (3) PASS 1 @ 8acf0d260 (PR #852, tier 2, config)` — first line PASS or NO GO; the counts table; the two follow-up shapes named; the head observed at the end (three readings).

---

PROVENANCE:
- `refs/pull/852/head` = `8acf0d260abf81a9b0f26153c1d1289f06e9774d`; `develop` = `81bf7b078fc2342aac34f0ab3aaebe83b91b7b74`; merge-base `5c69ee8b6…`; rev-list 2; numstat 4 files +14/−14; `merge-tree` rc 0 `82acc2da…` | `git ls-remote origin` + local objects from Wednesday's seat, NO fetch | read 2026-09-06 14:03:05
- Both commits' diffs READ WHOLE; the per-file counts; both JSONs parsed; the two un-widened shapes at `:27` / `:15` / `:21` | `git diff` / `git show <sha>:<path>` over local objects | read 2026-09-06 13:55, 14:03
- The live values | `!CODING/Secuura/CLAUDE.md:9`; `!CODING/Secuura/Blockchain/CLAUDE.md:38-50`; `.github/workflows/deploy-demo.yml:42-48` at `8acf0d260` — read-only | read 2026-09-06 13:55:08, 14:03:48
- The builder's claims (the 12 lines; the location sources; the before/after table with the 99-line control; the refuse-unless-exact edits; `check-no-latest-tags` with the plant; the no-consumer measurement; preflight 12/12; the two NOT-widened shapes; the false-consumer error disclosed) | `[Secuura/Blockchain -> Wednesday] READY: KS-490 (3) PR #852 @ 8acf0d260, widened …` 2026-09-06T04:02:01Z and `… @ e9b772e29 …` 03:54:03Z, both read whole (saved `fleet/state/mail_040200_s139_852_widened_ee5a62a9.txt`, `mail_035400_s139_ks490_3_852_ready_67640b35.txt`) | read 2026-09-06 14:0x
- Wednesday's widening ruling (six ids + env values, one PR; `location` only on a readable source; no `az`) | `briefs_staged/s139_852_widen_answer.md` 03:56:49Z | read 2026-09-06 14:0x
- KS-490 state (In Review, P2, ours; 11 comments, last 02:45Z; "Review E — Deployment, containers & CI/CD supply chain") | Linear GraphQL, team KS, read-only | read 2026-09-06 12:57
- TIER 2 for config | `learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md` — Wednesday's project, not yours | read 2026-09-06 (boot digest)
- scope: the values against the sources; counts with a control; JSON + hunks; the no-consumer measurement; the tag gate with a plant; the two follow-up shapes; scope hygiene; the secret scan; nothing runs | this brief's §2–§3, written by Wednesday | read 2026-09-06 14:0x

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-06 14:06
(checked: the head stated once with its two commits and merge-base; "no `az`" in §1, §2.7, §3 consistently; Wednesday's reads labelled with times and the builder's claims as the builder's; the two un-widened shapes ruled once (follow-up row, not a finding); the report path and subject name the PR and the SHA.)
