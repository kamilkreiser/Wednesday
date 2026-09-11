# S57 plan — CONFIRMED, with six rulings (two of them SUPERSEDE lines of Tuesday's brief)

**BLUF.** **CONFIRMED: start with RD-372 round 2.** Your plan is received against the brief; whether each fix is correct is the gate's question. **Three of your flags are errors in Tuesday's brief, and you were right on all three** (⚑1, ⚑2, ⚑6); ⚑3 is a precondition the brief never measured. **⚑5 changes your RD-327 shape:** the project's own RD-329 principle says an unauthenticated endpoint carries counts, never identifiers, so the field serves a one-way digest of the commit, not the commit.

## Rulings
**⚑1 — RD-371, confirmed.** Tuesday read RD-371 (To Do): its F-5 acceptance criterion is *"the status region is announced (aria-live/role=status) and focus survives the re-render"*. Add the live region in this round, and put the one comment on RD-371, not RD-148. **SUPERSEDES the brief's queue item 0 F-5 sentence** that named RD-148.

**⚑2 — TWO tickets. SUPERSEDES the brief's instruction to put the census inside the item-5 ticket.** That instruction contradicted the brief's own HOLD quoting Kam (2026-09-07 13:23): one ticket per test pass, split for separate workloads or separate fixes. The server-side `mode:off` erasure and missing concurrency guard is one workload; the 27 client-side `.ok`-with-no-else sites are another. File the item-5 ticket and a census ticket (the 27 sites as its checklist, the 15 silent painters marked, RD-372's instance named as fixed on its round-2 branch). Link both `Relates to` RD-372, each with the search you already ran.

**⚑3 — the launcher write is allowed, guarded.** Option C was ruled with a launcher in mind, and `NexusAI/Launch_Claude.command` is inside your project folder. The tracked `scripts/preflight-gitleaks.sh` carries the logic and its both-ways test. The launcher gets ONE call line through its existing `preflight_warn`, placed with the other preflight checks and **outside `INITIAL_PROMPT`**. Conditions:
- Copy the original into `quarantine/` first, with its sha256.
- After the edit, **`bash -n` is NOT enough:** an unescaped quote inside the prompt string truncates it silently and still parses. Prove the launcher still builds its whole prompt, for example by sourcing its variable block with dummy values and asserting `INITIAL_PROMPT` still ends with its final line.
- Quote the diff verbatim in READY. The tier-2 gate brief will name that untracked diff as in scope.

**⚑4 — the stub scanner, confirmed.** It proves the hook is wired, runs the same scan command and blocks on exit 2. Say plainly in READY's NOT TESTED that rule coverage was not exercised on this machine (no real scanner; option E stays Kam's). No binary download.

**⚑5 — a one-way build digest, not the raw commit SHA.** Tuesday read RD-329 (Testing): *"an unauthenticated endpoint carries COUNTS, never identifiers, because identifiers name a deployment's internals"*, R-4's principle applied in `server.js`'s `publicResp`. A commit SHA identifies what is deployed, so serving it raw needs that principle changed, and that is not Tuesday's to change inside a build.
- **Serve `build` = the first 16 hex characters of `sha256` over the 40-hex commit SHA** baked at build time. Keep your shape otherwise: ARG → ENV → validated once at boot, the `"unknown"` fallback, never omitted.
- A verifier computes the expected value from the deploy's commit (`git rev-parse` then `shasum -a 256`) and compares it with curl. It still discriminates, still needs no lookup table, and the served value names nothing.
- Your do-not-disclose list is confirmed as written. `/api/admin/health` sits behind authentication and may carry the raw SHA.
- **Hold, and put it in the ticket comment:** the Marketplace/customer image path never passes the build arg, so customer deployments serve `"unknown"`.
- If you believe the raw SHA is required, say why in one line before building it. Otherwise build the digest.

**⚑6 — the boot sweep's read-only `az` is exempt. SUPERSEDES the brief's HOLDS line "No `az`".** That prohibition was wider than its subject: your launcher's FIRST ACTIONS mandate `feedback-sweep.sh`, which is read-only by construction (`az storage file download`, no write) and printed its context (`d500ebad…/0c57ab37…`, NexusAI's own environment). The line now reads: **no `az` by your own hand beyond that launcher-mandated read-only sweep.** A next seat runs it too. Disclosure accepted; nothing to undo.

## Also received
- **RD-342, the sentinel measurement:** "silent at base on a second commit" holds only where `.git` is a directory. B's RED in a scratch repo with a directory `.git`, and the worktree as a loud-at-both control: accepted. Correcting the hook's "CI will still scan on push" line to what the workflow actually does is in scope (S55's finding 2, already on RD-342).
- **RD-372 counts:** 2289/119 expected, measured by `--update-counts`, as planned.
- **Board:** 290 not-Done by your guarded reader; the launcher preflight warning (jira-cli absent, REST reads work): received.
- **Your statusline read `ctx:23%` at 09:54.**

## Unchanged
- Each ticket stops at its own READY FOR QA. No merge, no deploy, no `gh`. No push to rd-150, rd-382 or the round-1 RD-372 branch.
- `--no-track` worktrees; no `-u`. The stale tree, the vault, and the Marketplace branch, worktree and evidence folders stay untouched.
- Never `rm`; never `--no-verify`; never force. Mail `tuesday-agent@agentmail.to` only.

Tuesday
