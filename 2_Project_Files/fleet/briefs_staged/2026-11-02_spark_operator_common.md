# Spark operator — common commission (Wednesday, 2026-11-02; read WHOLE before your own assignment)

Kam's instruction this morning, verbatim: "carry on with the plan and please make sure the spark is 100% busy or as close as possible".
You are a Spark operator: you produce HELD, tested patches for Secuura ticket KS-1868 (umbrella, "Refs" only: the "unreadable thrown value" catch class) by driving the local Spark model through the night/ tooling, and you FEED THE SPARK QUEUE so model rounds run back to back. You do not raise PRs, push, comment on tickets, or merge — a Claude raise seat does that from your held files.

## The class
A catch block (or `.catch`) that reads a thrown value unguarded — `err instanceof Error ? err.message : String(err)`, `error.message`, `e?.code`, `String(err)` — throws INSIDE the catch when the value is a revoked Proxy or an Error whose `message` getter throws. The house fix reuses the guard helper already in that service, or the pattern already merged in that service; never a new helper when one exists.
**Zod pre-check sites are OUT unless your assignment says otherwise:** a catch that starts with `instanceof z.ZodError` throws first on a revoked Proxy, and some have tests pinning `details: err.errors`; fixing only the message line is half a fix (operator 57). Skip them with the reason.

## Templates (read, copy the flow exactly)
- Operator 57 (screen + tenant-provisioning, queue-fed, one rebrief): `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator57/` (report.md, screen.md, gen/, every .out).
- Operator 53 (mcp-server, describeThrown, 3 passes x 3 hunks): `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator53/`.
- Operator 51 (nft-certificate): `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator51/`.
Flow: open-PR scan with a planted control (start AND end) -> brief under `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/` -> `spark/brief_lint.py` -> dry run -> control -> model round -> `night/hold_ready.py` -> held READY_* in `night/`. Read each tool's header before first use. The model's commonest failure today: it drops the `--- a/` / `+++ b/` header lines (operator 57's A2 fail); one added brief sentence fixed it.

## Per site, before briefing
Read the code at the tip; write down today vs after (response, persisted state), and whether an ORDINARY Error already gets the after-state. If a fix newly produces an outcome an ordinary Error does not produce, SKIP the site with the reason. Group sites into passes of ~3 hunks, disjoint by > 3 lines; name them O<your number>-P1...

## THE QUEUE (the point)
The Spark runs one round at a time (`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/state/round.lock`). A standing drainer (keepdraining.sh, alive) runs `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/queue.md` lines one at a time and appends rows to `spark/done.md`. Other operators are queueing at the same time. **As soon as your FIRST brief passes lint + dry run, APPEND its `--control` line to queue.md; append its model-round line ONLY after that control's done.md row shows CONTROL-PASS** (append only; never edit or remove another operator's line; operator 57's lines show the format). *(Corrected 07:5x: the first version said to queue both together, and operator 58's model round ran behind a failing control and was wasted.)* Prepare the next pass while yours run. Watch done.md for your rows, then hold_ready on PASS. **Detect your rows by polling, not by a tail filter** (operator 59's done.md monitors missed BOTH of its rows today and it stalled 11 min): every 30-60 s run `/usr/bin/grep -c -i '<your brief tag>' .../spark/done.md` against the count you last saw, with a positive control (an earlier row's tag), and act on any increase. A dry run that returns rc 3 BUSY means another round holds the lock: the control builds the same input, so queue the control. Never kill another round, touch another operator's lock, or edit their queue lines.

## Limits
- Tip: develop `03977e89a343ad7362760e4fb0270602fb6da5ce` (Wednesday's ls-remote 06:52 AEDT; unchanged at 07:47 per operator 57); re-read by ls-remote at start and end. Read-only clone with the deploy key: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate89-e25-1904-1906-1907/repo`; follow the checkout operator 57's outputs used.
- **In flight — never brief these files:** services/auth/src/routes/auth.ts, services/nft-certificate/src/services/minting.service.ts (Seat E 26th; PR 1909), services/mcp-server/src/http-server.ts (Seat V 14th), services/billing/src/routes/webhooks.ts (Seat F 21st), services/security/src/index.ts (Seat S 11th), services/tenant-provisioning/src/index.ts (operator 57's held passes), services/auth/src/routes/users.ts (PRs 1796/1798), and any file an open PR lists.
- Counter: original brief + at most ONE rebrief per pass. Never hand-edit model output.
- Every number from a saved command output in your report dir; "UNMEASURED" for anything not run.
- Writes ONLY under `/Volumes/DevMASTER/WEDNESDAY/`. Never into `/Volumes/DevMASTER/!CODING/`. No push, PR, ticket/board writes, or mail.
- zsh with hooks: never `cd`; `RC=$?` on the same line; outputs to files; no `=====`; deletes only of your own scratch by literal path.
- Secuura content only.
- Write your report with a Bash heredoc (`cat > .../report.md <<'EOF'`): the Write tool refuses subagent report files.

## Deliverable
`/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator<N>/report.md` in operator 57's shape: BLUF (held/failed/skipped with reasons, tip start/end); held files pasted from `ls night | grep O<N>`; per pass the hold_ready line verbatim, callers, BEHAVIOUR CHANGE text for the PR, recommended tier; raise-seat notes (strict or not, test names, hunk distances); round log with done.md row times; UNMEASURED. Final message to Wednesday: BLUF + held names + done.md row times only.
