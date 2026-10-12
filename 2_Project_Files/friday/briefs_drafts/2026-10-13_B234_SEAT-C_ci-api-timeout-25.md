From Friday (laptop seat), Datasec / HPSM-POC. Replies and wraps go to friday-laptop-agent@agentmail.to (your STATUS file is the wrap).
# BRIEF B234 · SEAT-C: raise the CI `api` job limit from 15 to 25 minutes (decisions pack POC-1, ruled by Kam) — one line, nothing else
**Fired: 2026-10-13 03:29 AEDT.** Pane `Datasec/HPSM-POC-C`. Your commission is THIS file, at `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-13_B234_SEAT-C_ci-api-timeout-25.md` (Friday's tree, read-only to you). Step 0: copy it into your `1_Project_Definition/Briefs/` unchanged, as the project's record. QA tier 2 (through-code; Friday reviews the diff). Round 1. The last SEAT-C seat, gate B204, is finished (`Briefs/2026-10-11_B204_STATUS.md`).

## Why (the ruling, verbatim from the pack)
Decisions pack 2026-10-12 (`FRIDAY/0_Brain/reference/2026-10-12_datasec-decisions-pack/`), item **POC-1**: "The automated test run for the server took 14 min 12 s against a 15-minute limit, and the next two lanes add more tests. Raise the limit? (a) Raise 15 → 25 minutes, change nothing else · (b) split the job in two". Kam accepted every default of the HPSM-POC pack on the live board 2026-10-12 ~20:11-20:12 (card `hpsmpoc-decisions-pack-1012` = a). Default (a): "Raise to 25 minutes. A one-line change through the normal code-scanning review. No test is skipped or trimmed."
Read by Friday (GitHub contents API at main a5fd6355122de2db155e6dd5c199f13bcf138cdd, 03:3x AEDT): `.github/workflows/ci.yml` line 32 `  api:`, line 35 `    timeout-minutes: 15`.

## Do
0. `git fetch origin`; `ls-remote origin refs/heads/main` must read a5fd6355… (or a later main: then say which and re-read line 35 there); `ls -a .tools | grep -i b234` → nothing.
1. Worktree `.tools/wt-B234` on a new branch `b234/ci-api-timeout-25` from origin main. Change ONLY the `api` job's `timeout-minutes: 15` → `25`. No other job, no other file, no step changes.
2. Prove: `git diff --stat` = 1 file, 1 line changed; the YAML still parses (`python3 -c "import yaml,sys; yaml.safe_load(open('.github/workflows/ci.yml'))"` or `npx --yes yaml-lint`, say which); `grep -n 'timeout-minutes' .github/workflows/ci.yml` before/after in the STATUS.
3. Push the branch only (`git push -u origin b234/ci-api-timeout-25`), read back with ls-remote. Friday opens the PR; CodeQL and CI run on it.
4. Records: append one line to `1_Project_Definition/CLARIFICATIONS.md` ONLY if this project's CLARIFICATIONS convention says rulings land there from build seats; otherwise name it in the STATUS as owed to the records seat. Do not invent a C-number.
5. Write `Briefs/2026-10-13_B234_STATUS.md`: diff, the two grep outputs, the ls-remote line. Last line `READY FOR REVIEW: b234/ci-api-timeout-25 <sha>` or `STOPPED: NEEDS FRIDAY`.

## HOLDS
- **HP Restricted material.** No HP Restricted document is given to ANY AI tool without HP's written approval (signed SOW §4.1.4(c)). Do not open `HP Reporting and Docs/` or the SOW file in the project root.
- **Datasec only.** No other client's names, tickets or paths.
- Another seat is live beside you: SEAT-B (B233) on `b231/reset-words-bff-table-f22`, file `web/e2e/hosted-reset.spec.ts` only. Not yours; do not touch that branch.
- No PR, no merge, no deploy, no Jira, no history.md, never open 4_Credentials/.env, never delete, never force-push. No ports needed.
