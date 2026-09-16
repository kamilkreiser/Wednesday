---
date: 2026-09-16
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's (live on the Mac mini). Datasec mail by subject only.
source: replaced WHOLESALE at 22:38 by the 21:36 seat (previous copy NEXT-PICKUP.md.pre-2238-wholesale — read it for Tuesday/structure history and the full BRIEF RULES text).
status: live
supersede: replace wholesale at the next pickup; do not append
---

# NEXT PICKUP — ⚡ **Kam's standing words:** 20:40–20:42 *"you have the approval to spin up other local agents [Claude agents] to test, approve, merge and move things forward … see what else needs our attention. highest priority and highest value items first"* (grant file `learnings/2026-09-16_new-account-spin-up-agents-to-test-approve-merge.md`) · 21:1x *"dont go overboard. try not to go beyond 40% token allocation"* (`fleet/USAGE_STOP` = 40, seat-scoped; gauge 11% at 22:36) · 21:1x *"keep working through easier tickets with the local LLM as well"* · 09:53 *"If something's blocking, move on to the next"* · email 07:57Z: failed local ticket = original + ONE rebrief, then Claude · **he leaves MONDAY NIGHT 2026-09-21.** First person on the panel. **A seat may END ITS TURN only with the model RUNNING or a batch QUEUED (or a search/brief commission whose completion wakes it).**

## 🔴 FIRST ACTS (state at 22:38)
1. **Seat A `%2` (`Secuura/Blockchain`, brief `fleet/briefs_staged/2026-09-16_raise_seat_A.md`, GOs arrive in `secuura-blockchain@`).**
   - **MERGED + VERIFIED at source tonight** (GitHub GET + Linear query by Wednesday): #1000 KS-960 squash `4ec051032` (KS-960 Backlog, link `contributes`) · #999 KS-1130 squash `80686962` (KS-1130 Done; KS-1129 Backlog, link `links`).
   - **#1001 KS-1165 @3925d4c07 — GO SENT 22:30** (tier-1 gate GO WITH FINDINGS). Ruling in the GO: pre-step reword "Closes" → "Part of"; merge; **KS-1165 stays OPEN** (DoD boxes 1+2 partial); seat files ONE new ticket for F-2 (production: v2 verify passes while the v1 family 307s to `/api/v1/` and is refused — versioning after CSRF); seat queues a TEST-ONLY follow-up PR for F-1 (a real-app mount-order cell, red-proofed by the gate's T3/T4) + F-3 wording, AHEAD of A6. **Owed:** read its MERGED receipt → verify at source (merge commit parents/files; KS-1165 state; the new F-2 ticket exists, is ours, searched first).
   - **#1002 KS-1123 @a376756ab — READY FOR QA 12:35Z.** A tier-2 gate DRAFTER was commissioned in-session at 22:3x (output files if it finished: `fleet/qa-agent/briefs/2026-09-16_secuura-1002-ks1123-tier2.md` + `.prompt.txt`, `fleet/qa-agent/launchers/launch_qa_secuura_ks1123_1002.sh`, `fleet/qa-agent/gatesets/2026-09-16_gate1002/`). **If this seat is a successor and those files do not exist: re-commission from tonight's #999/#1000 set** (see the 22:3x note line). Then: read brief + prompt WHOLE, `--check` yourself, `usage_gate.sh --check`, `cockpit.sh add "QA/Secuura-1002" "bash '<launcher>'"`, rung-5 read, verdict → completion check → head re-read (`git ls-remote`) → `GO: #1002 KS-1123 @<sha>` with the linkKind pre-step → verify merge at source.
   - Seat A's next: the F-2 ticket, the KS-1165 F-1 follow-up PR, A5 KS-932, then A6 KS-844. ≤3 open PRs.
2. **Ornith:** queue EMPTY since 22:14. **HELD tonight:** KS-1036 item 3 (PASS 8/8 on its rebrief; PR NOTE: re-count 71/40/2/29 at raise) · KS-890 (PASS 8/8 on RE-CHECK of the same r2 out.md after the doc-tier ANCHOR RESTORED repair — not a third model round). **Reallocated to Claude (Sunday batch):** KS-987 (D9 placement), KS-789 (D7) — plus the earlier KS-1168, KS-1163, KS-998, KS-866. **A SEARCH subagent was commissioned 22:1x** for up to three next tickets (report `scratchpad/ornith_search2_REPORT.md` — session-local; durable = new `night/briefs/KS-*.md` newer than 22:15, new `night/inputs/*`, and a new rejection block in `night/candidates.md`). **If this seat is a successor: look for those files; read each brief's `## The exact change` + `## Premises (measured)` before queuing; if none exist, re-commission the search (prefer vitest test-only / tamper-graded and one-file bash over docs inserts).**
3. `kam_rulings_today.sh` → `reconcile_rulings.py` (0 to rule at 22:07). Mail: `wednesday-agent@` (no label filter) + `coagent@` (Datasec subject only).

## ✅ BUILT TONIGHT (21:36 seat) — mechanisms in the path
- **Ornith G3 honours `night/ALLOW_SEATS`** (live QA-gate processes no longer idle the queue): `night_run.sh` `.pre-0916-g3allow`; arms `local-model/tests/g3_allow_seats_arms.sh` 4/4 (OLD fails ARM2); G2 arms 5/5 regression; proven live at 22:09 (`pgrep -f launch_qa_ = 2 — ALLOWED`). `ALLOW_SEATS` expires **2026-09-17 06:00** — the morning seat re-decides.
- **Doc tier ANCHOR RESTORED** (the insert-after-deletes-its-anchor dialect; doc twin of bash B3c): `tasks/doc_patch/anchor_restore.py` + `checker.sh` `.pre-0916-anchorrestore`; arms `local-model/tests/doc_anchor_restore_arms.sh` 10/10 (Wednesday's own run). ⚠ `tests/doc_d8d9_arms.sh` CANNOT run as written (its night clones are gone; builds from the moving tip) — fix owed.
- **Doc-tier D9 is VACUOUS on a blank anchor** (measured false PASS on KS-987 r0; KS-866's 20:11 PASS rested on one) — proposal H1 + D8b with arms in `local-model/runs/2026-09-16_rebriefs-docs-evidence/` (gitignored — holds client file copies). NOT built. Interim rule: never anchor a doc brief on a blank line.
- QA gate sets persisted: `fleet/qa-agent/gatesets/2026-09-16_gate999_1000/`, `2026-09-16_gate1001/`.

## ⚠ TRAPS (tonight's, plus the standing ones)
- **Linear `linkKind=closes` on a SECOND ticket** (a PR body saying "Root fix: KS-n", "does not close KS-n", a title prefix) closes that ticket on merge. Every GO carries the pre-step: reword the PR body, re-read `attachments.metadata.linkKind`, else merge and restore state at once. Seat A now regex-checks bodies before opening a PR.
- **`tsc -p services/<svc>` EXCLUDES `src/__tests__`** — a "tsc rc 0" says nothing about new test files; gate briefs ask for an including program.
- **Gate drafters run the launcher without `--check` to prove the TTY guard** (twice tonight, nothing started) — the owed fix is a `--check-tty` seam in the launcher generator; until then, say "never, not even for the TTY guard" in the commission.
- **The watcher's frozen-busy leg fires every ~6 min on a seat HOLDING by design** when its footer shows "· 1 monitor"; the IDLE-ACK covers only the idle-at-prompt leg. Triage = inbox → pane tail → detector; no tap. A frozen-busy ack is shared tooling (claim with Tuesday first).
- Push Wednesday's repo ONLY with `2_Project_Files/tools/safe_push.sh "<msg>" <paths>`. Never a hand `pull --rebase`.
- Never edit a live bash script in place (`.new` + `mv`; check `night/log/.night_run.lock` first). `git -C <outside WEDNESDAY> <write verb>` refused. `rm` refused. Timestamps from `date`, never typed (22:0x slip). The subject-token gate refuses stop/hold/checkpoint mid-subject.

## 📋 BRIEF RULES + COMMISSIONING — unchanged; full text in `NEXT-PICKUP.md.pre-2238-wholesale` (§ COMMISSIONING) — plus tonight's doc rules: never anchor on a blank line; anchor on a unique non-blank line with a non-blank neighbour; name no heading outside the edit in model-visible text; no `+` line sharing a long prefix with a `-` line; state column 0 explicitly for list items.

## ⏳ OPEN / NOT TONIGHT
- Sunday Claude batch: KS-1168, KS-1163, KS-998, KS-866, KS-987, KS-789 (docs text is in their briefs).
- Polish follow-ups recorded on their tickets (not commissioned): P1/P2-999 (stale twin header line numbers; 3× TS18046 in the twins), P1-1000 (cell 3 whitespace-brittle).
- Tuesday: structure work done on both machines; nothing owed between the seats except her next-boot preflight. Tonight's 23:00 close bell is the FIRST live run of the new seat-aware bell — read its log.
- Raise seats B/C and lanes A/B/C staged, NOT launched (Kam's 40%); their briefs still carry the `coagent@` GO-inbox defect — fix before any launch.
