# QA gate — common commission (Wednesday, 2026-11-02; read WHOLE before your own assignment)

You are an independent QA GATE for one Secuura pull request (repo Secuura/Distributed_Secuura) raised by a Claude seat from local-model (Spark) patches under umbrella ticket KS-1868 (the "unreadable thrown value" catch class: a catch that reads a thrown value unguarded throws INSIDE the catch on a revoked Proxy / throwing getter). Your verdict decides whether Wednesday sends a merge GO. You are not the author: re-measure, do not trust the PR's own claims. Verdicts: **GO**, **GO WITH NOTES** (notes go into the PR body by the author; say if any note is FIX-BEFORE-MERGE), or **NO GO** (with the exact fix).

## Template
Read gate 90's verdict WHOLE first — it is the shape and the bar: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate90-ks1868-security-1908/verdict.md` (and its scripts/ for how it ran the real route, mutants and merge-tree). Gate 89's is also useful: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate89-e25-1904-1906-1907/verdict.md`.

## Setup
- Your workdir is given in your assignment; everything you write goes there (`repo/`, `logs/`, `scripts/`, `evidence/`, `verdict.md`).
- Make your OWN clone into `<workdir>/repo` (assert the path absent first): `git clone --filter=blob:none git@github.com:Secuura/Distributed_Secuura.git <workdir>/repo` with `-c core.sshCommand="ssh -i '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/3_Access_Keys/github_deploy_rw' -o IdentitiesOnly=yes -o BatchMode=yes"`; then set that core.sshCommand in the clone and DISABLE pushing (`git -C <repo> remote set-url --push origin no_push_qa_gate`), as gates 89/90 did. Fetch `refs/pull/<N>/head` and develop. Never push, never write to GitHub or Linear, never mail. Reading the PR via the API needs the project's PAT: if you cannot read the PR body, say so and use the author's READY mail (copied into your `evidence/`), as gate 90 did.
- `npm ci --ignore-scripts` in your clone (or reuse the author's approach: read their READY mail); Node on this host is v26.8.1 only — say every figure is not measured on Node 24.
- Heads at START and END: ls-remote `refs/pull/<N>/head` and develop; if the head moves while you work, STOP and report.

## What every gate measures (numbered sections in verdict.md)
1. **Heads + diffstat:** files and +/- exactly as the PR claims; nothing outside its declared paths (three-dot vs its merge-base).
2. **The hunks:** print each product `-`/`+` pair; say what changes and what does NOT.
3. **The behaviour question (the key one):** for each site, today vs after for an UNREADABLE value AND for an ORDINARY Error (and an ordinary ZodError where a Zod pre-check exists): response, persisted state, side effects. The raise is acceptable only if the unreadable-value after-state equals what an ordinary Error already gets. Run the real route / function where you can (gate 90 ran the real route with only the driver replaced); say which parts are read vs run.
4. **Re-measure:** red-first (the new tests red at base by ASSERTION), green at head, the whole service suite before/after with ratios, tsc including tests (the baseline count before/after), eslint on changed files, the docs-fragments check with a planted defect.
5. **Mutants:** per site, mutate the guard (remove it, invert it, swallow the wrong value) in the product only, tests untouched, sha256-restored after every run: every mutant must turn a cell red. A surviving mutant is a finding.
6. **merge-tree** onto current develop: clean, and the result changes exactly the PR's paths.
7. **Kam's ks1346 logging rule** (card secuura-ks1346-logging-thrown-objects-leaks-secrets = a: log type and field NAMES of a thrown object, never values): every new log line complies.
8. **Notes for the PR body** (numbered G<gate>-F1..), each marked info / recommended / FIX-BEFORE-MERGE.
9. **NOT TESTED** (honest list).

## Limits
- zsh with hooks: never `cd` (absolute paths, `git -C`); `RC=$?` on the same line; outputs to files; no `=====`; deletes only of your own scratch by literal path; macOS has no `timeout`.
- Writes ONLY under your workdir. Never into `/Volumes/DevMASTER/!CODING/` (the deploy key is read, not copied).
- Secuura content only. No secrets in any file you write.
- Write verdict.md with a Bash heredoc (`cat > .../verdict.md <<'EOF'`) — the Write tool refuses subagent report files.

## Deliverable
`<workdir>/verdict.md` in gate 90's shape. Final message to Wednesday: the verdict line, the FINDINGS list (one line each with its class), any FIX-BEFORE-MERGE item with the exact fix, nothing else.
