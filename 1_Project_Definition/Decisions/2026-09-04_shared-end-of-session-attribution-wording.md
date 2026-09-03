# Drafted wording — `fleet-vault-note-attribution`

**For Kam. One decision, one word.** This is the exact edit Wednesday proposes to
`/Volumes/DevMASTER/Notes (MASTER)/skills/Current/end-of-session.md`, **Step 1b**.
Wednesday has NOT made it — that file is shared across every client, so amending it is
Kam's call, not a coordinator's unilateral edit.

- **Say `adopt`** and Wednesday makes exactly the edit below, verbatim, and nothing else.
- **Say `leave`** and nothing changes; the agents keep self-correcting after the fact.

---

## Why (one paragraph, then the wording)

Every project's agent appends its own section to the **same** shared daily note in
`Notes (MASTER)/daily/`. Two seats running concurrently therefore stage each other's
in-progress text by construction — `git add -A` or `git add daily/<date>.md` sweeps in
whatever the other seat has written but not yet committed, under a message naming only
the committer. **Third occurrence: 2026-09-02, 2026-09-03, 2026-09-04.** The last one is
recorded in the vault at `2df509c` (the mis-attributed commit) and `f68e5c7` (the
NexusAI agent's own additive correction — it did **not** revert, which was right: the
other seat's lines were additions with zero deletions, so a revert would have destroyed
them).

**The agent's own diagnosis is the part worth acting on, verbatim:**

> *"The reminder is not the failing part: the check sits at COMMIT time while the
> decision forms at BOOT, and by commit time the file feels like mine."*

A fourth reminder would not have helped. The replacement is a **mechanism in the same
command as the commit**, which is correct whether or not anyone remembered anything
hours earlier.

---

## The edit — Step 1b, exactly as proposed

**Current Step 1b block:**

```bash
cd "$VAULT_DIR"   # set by the project launcher
git fetch
git pull --rebase
git add -A
git commit -m "vault: session notes ($(date +%Y-%m-%d))" || echo "nothing to commit"
git push
```

**Proposed Step 1b block — four added lines and a two-sentence note:**

```bash
cd "$VAULT_DIR"   # set by the project launcher
git fetch
git pull --rebase
git add -A

# ATTRIBUTION — derive it, never remember it. The shared daily note is written by
# EVERY project's agent, so a concurrent seat's in-progress section is staged with
# yours by construction. Read who is actually in this commit off the staged diff:
NOTE="daily/$(date +%Y-%m-%d).md"
git diff --cached -- "$NOTE" | grep '^+## ' || true

git commit -m "vault: session notes ($(date +%Y-%m-%d))" || echo "nothing to commit"
git push
```

**And immediately beneath the block, this note:**

> **Every heading that command prints belongs in your commit message.** If one of them
> is not yours, name it too — say whose it is. **Never revert to "clean up" someone
> else's section:** their text is additive, a revert destroys it, and a misattribution
> is a record problem that is fixed by *adding* a record, not by rewriting a pushed
> commit. If you find you have already pushed a message that named only yourself,
> push a short follow-up commit that names the rest — that is the whole remedy.

---

## What this does and does not change

- **Does:** puts the check at the moment the answer is knowable, in the same command as
  the commit. Costs one line of output per wrap.
- **Does not:** change who may write the note, add a round trip, or make Wednesday a
  bottleneck at the moment several agents wrap together — which is exactly when all
  three instances happened.
- **Does not** touch any other step, any project's own `CLAUDE.md`, or any client file.

## The option Wednesday did NOT recommend, and why

Giving the note a single writer (agents write, Wednesday commits) removes the race
outright — but it costs a round trip on every wrap and puts a coordinator in the path
at the busiest moment of the night. The derive-from-diff rule gets the same correctness
with no coupling.

---

**Provenance**

- Step 1b's current text | `Notes (MASTER)/skills/Current/end-of-session.md` lines 42–56 | read 2026-09-04 06:14
- The third instance, both commits | `git show 2df509c` and `git show f68e5c7` in the vault repo | read 2026-09-04 06:14
- The agent's diagnosis and proposed mechanism, quoted verbatim | the NexusAI agent's own self-report in `f68e5c7`'s commit body and its wrap mail to `wednesday-agent@`, 2026-09-03 18:35:00Z | read 2026-09-04 06:05
- Prior instances 2026-09-02 and 2026-09-03 | `0_Brain/learnings/_ledger.md`, the w=3 row dated 2026-09-04 | read 2026-09-04 06:05
