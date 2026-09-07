---
date: 2026-09-07
type: pickup
scope: SECUURA + Wednesday's own work. Datasec belongs to the LAPTOP seat — do not touch its threads.
source: replaced WHOLESALE at 21:0x by the 20:12 seat; state block kept current at 22:16
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — 22:10 AEST Monday. TWO CARDS ON KAM'S DESK. #897 UNDER GATE. #892 FROZEN. Nothing deployed.

**Run `2_Project_Files/tools/kam_rulings_today.sh` before writing anything — read EVERY line.**
Mail UTC ≈ AEST−10. **ROTATION BAND 80–90% (Kam 10:49); 70% is a CHECKPOINT ONLY.**

## 🔴 FIRST ACTION — read Kam's panel, then `%162`, then the inbox.
**TWO THINGS ARE HIS AND BOTH HAVE SAFE DEFAULTS:**
- **`secuura-892-round4-passed-but-introduced-two-majors`** (rec `round5`, **default HOLD**) — round 4
  CLOSED the blocker and introduced two Majors; **F-2 reintroduces KS-969's own failure class from
  inside KS-969's own test suite**, which is why this is his and not Wednesday's.
- **`secuura-ks968-rotation-three-worlds`** (rec `separate`, **default STOP**) — two booleans separate
  a real login-breaking rotation from two innocent states.
## 🟢 IN FLIGHT — #897 AMENDING. The gate REPORTED and `%169` is closed.
**VERDICT: GO with findings. KS-978 / F-B is GENUINELY CLOSED.** **Wednesday ruled AMEND BEFORE
MERGE** and mailed it 22:14 — **not a round** (no cap on #897; that is #892's), doc-only, reversible,
Wednesday's call. **One edit closes both findings:**
- **F-1 MAJOR** — `POST /api/documents` answers 403 for **NINE** conditions; the rewrite publishes
  **TWO**. The gate's sentence is the ruling: *"the replaced text named no condition precisely… but
  it did not tell an integrator the list was CLOSED. The new sentence does."* **Vague-and-OPEN →
  specific-and-CLOSED.** Fix: keep the two, **re-open the list**, name the other codes, phrase it so
  it does not claim to be exhaustive.
- **F-2 MINOR** — *"belongs to a different Organisation"* is narrower than the predicate
  (`claimedOrgId !== callerOrgId`): a uuid belonging to NO org is refused identically. Fix the field
  description, the 403 description **and the runtime message**.
- **NO THIRD TICKET** — the regression test folds into **KS-811** (the gate's own call).
- **ON THE AMENDED DIFF: Wednesday does the completion check, then MERGES.** Do not re-raise it.
- **Stated limit to carry onto KS-978's closing comment:** scenario H proved the new cells are
  **presence regexes — they catch a DROP, not an INVERSION** (inverted meaning, all tokens kept → 7
  passed). That is KS-837's line 1, correctly not filed against the PR.

## (superseded) the gate that produced the above
**PR #897 @ `718008cef`** (off develop `6a7a7824e`) **closes KS-978 / F-B — the DEPLOY BLOCKER on
already-merged code.** Prose + generated spec only; **the 403 is untouched.** Gate `%169` was 17 min
in and **mid-way through writing `VERDICT: GO with findings — TIER 2 STANDS (no behaviour change)`**
when this block was written — **read the inbox, the verdict may already be there.**
- Brief: `2_Project_Files/fleet/qa-agent/briefs/2026-09-07_secuura-ks978-897-tier2.md`
- Launcher: `2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_897.sh` (all 8 branches
  exercised before arming). **Close the pane after it reports** (`pane_close.sh %169`).
- **On a GO: the merge is WEDNESDAY'S** under Kam's week grant — #897 is inside commissioned work,
  reversible, and makes no external commitment. **Score it, then merge, then say so.**

**`%162` Secuura/Blockchain is the ONLY builder pane** (all three gate panes closed after reporting,
listeners 26→26 each). It is **DORMANT BY DESIGN, told to stand down on #892 entirely**, and
**Wednesday is its wake path**. Its prompt is clear — no queued tap.

## ITS QUEUE, in the order Wednesday set and Kam's rulings bound
1. **Merges: #889 `48ad0354e` → develop, then #893 `0281b0faa` → develop.** GO given on Wednesday's
   word under Kam's week-scoped merge grant — **execution of his own `bind` ruling**, since
   `hold-for-finding1` held #889 until HE ruled the trust-boundary question, he ruled it at 19:00,
   and the gate proved F1 closed by a 2×2 tamper matrix rather than a green run.
2. **KS-968 — Kam ruled `id-count` at 20:56.** EXACTLY ONE query, nothing else:
   `SELECT count(*) FROM users WHERE id = 'a0000000-0000-4000-8000-000000000030';`
   **ID-keyed, so it touches no hash and is INDEPENDENT of the key in question.**
   **1 → a rotation happened → INCIDENT** (login resolves by `email_lookup_hash`; those rows cannot
   sign in by address). **0 → benign, KS-968 moot on that box.** **A THIRD QUERY IS OUTSIDE HIS
   WORDS** — an ambiguous result is a finding to report, never a licence to widen.
3. **#892 ROUND 4 — GATED, GO-with-findings, BLOCKER CLOSED — and FROZEN pending Kam.**
   The binding condition he paid for was **MET**: 1 of 10 failing, the right cell by name, reddening
   by **executing**. The gate proved that with **its own two controls** (a planted syntax error → 1
   cell, no trailer; an inert comment → 10 passed). **But the fix introduced F-1 and F-2, both
   MAJOR.** **DO NOT START A FIFTH ROUND — it is carded.** Old scope line, superseded:
   **The binding condition is MET and proved**: with the drift-arm call removed the new call-site cell
   reds, 1 of 10, and it is the right cell. The gate is told to verify the **identity** of the failing
   cell and the **EXECUTED-cell count** under each tamper — a cell that reds by failing to build
   proves nothing. **KS-977 filed (F2-A); F1-C is a comment on KS-973.**
4. **#889's THREE TICKETS — DONE.** KS-978/979/980 filed 11:27Z and verified against merged develop.
   **Measured on the board: they were NEVER filed** (newest was KS-977 @ 11:10). **F-B carries a
   DEPLOY-BLOCKER line that must sit ON the ticket** — #889 is merged and that ruling otherwise lives
   only in a mail. **CHECK THE BOARD, do not assume.** KS-811 to be read first — the gate calls F-B
   its gap class.
   **The original scope line, for reference —** F1-A (quarantine on EVERY non-publishing outcome,
   not just drift) + the DEGRADED banner must stop naming what the suite will run as + **THE
   CALL-SITE CELL, which is not optional** + the throw-arm regression cell with a clean-tree control.
   **F2-A and F1-C are NOT in this round. THERE IS NO ROUND 5** — a NO GO comes back to Kam.

## STATE — every SHA is an agent's read, NOT re-derived at this seat
    origin/develop   6a7a7824e  ← MOVED TONIGHT. #889 (2ff0eb850) then #893 (6a7a7824e), both
                                 merged on Wednesday's word, both with a NEGATIVE control proving
                                 #892's frozen work did not leak in. NOTHING DEPLOYED.
    demo VM          632f16dfe  (untouched all day)
    #892  1e31c80b9  ROUND 4 GATED (GO-with-findings, BLOCKER CLOSED) — FROZEN pending Kam's card.
    #897  718008cef  KS-978 / F-B, the DEPLOY BLOCKER. UNDER GATE at %169. Merge is Wednesday's on a GO.
  🔴 SCOPING FACT, measured by the seat: F-1/F-2/F-3 are NOT live on develop — those suites exist
     ONLY on the frozen #892 branch (`git ls-tree`). F-2's hazard reaches that branch, not the
     trunk — and MERGING #892 is what would put it there. Strengthens the card, does not soften it.
    #891  3c07157a2  ** KAM'S OWN CLICK ** https://github.com/Secuura/Distributed_Secuura/pull/891
**Filed tonight:** KS-974/975/976 (#894's findings) · KS-977 (#892 F2-A) · **KS-978 (#889 F-B — the
DEPLOY BLOCKER, and it is that ticket's FIRST LINE)** · KS-979 (F-A) · KS-980 (F-C); plus comments on
KS-808 and KS-973. **F-A and F-C were SPLIT, not grouped** — F-C carries a decision, F-A does not.
**KS-981 (F-1+F-3) · KS-982 (F-2) filed** — the seat split them from Wednesday's two-ticket proposal and gave its reasoning ON the tickets. **Nine tickets filed tonight. Nothing is owed on the board.**
**`ks597-qa-pg` is UP** (`docker ps`, 127.0.0.1:6499→5432) — the seat's disposable Postgres, its
teardown command in `HANDOVER-s148.md`. **It is the seat's to tear down, not Wednesday's.**

## 🔴 F-B ON #889 IS A DEPLOY BLOCKER — Wednesday's ruling, on the record
`originate.openapi.ts:289-293` still tells integrators `organizationUuid` is *"Accepted and
preserved"*; #889 makes a mismatched value a hard **403**, reproduced at the wire. **Not
merge-blocking** (contract/doc, no runtime misbehaviour, a merge publishes nothing). **Deploy-blocking:
fixed before anything carrying it reaches a surface an S integrator reads.** Severity was the
tester's; the priority is Wednesday's.

## WHAT WEDNESDAY GOT WRONG THIS SEAT — all caught, none reached a cost
- **A SEVERITY WORD WITH NOTHING BEHIND IT:** called #894's F-2 *"an unpinned arm rather than a live
  defect"*. It changed a live **200 → 403 on `/check`, the route with NO role gate.**
  Classification-is-the-field, **w=11**. Agent-caught in five minutes.
- **A TOOL PATH COMPOSED FROM ITS NAME:** `fleet/pane_prompt_check.sh` → "No such file"; it lives at
  **`fleet/cockpit/pane_prompt_check.sh`**. Was one sentence from telling Kam the ghost-text detector
  was missing. **Prove an absence with `find`/`grep` + a positive control.**
- **A WRONG MECHANISM WRITTEN INTO TWO LEDGER ROWS** — see STANDING below. Retracted and corrected.
- **A CONTROL THAT COULD NOT DISCRIMINATE:** curled port **6499 to prove the seat's Postgres survived
  a pane close** — 6499 is **Postgres, and curl speaks HTTP**, so `000` was guaranteed either way.
  `docker ps` + a TCP connect settled it (container UP). **A check that cannot fail, in Wednesday's
  own hands, minutes after crediting a tester for catching one.**

## STANDING — and the correction that matters most
No `cd` (hook; it also refuses `git -C $VAR` — use literal paths). Taps ≤200 chars with a verified
mail behind them (`--mail`), **and re-read the destination until the mail is VISIBLE — the send's
rc 0 raced the listing tonight.** `<<'EOF'` for briefs; **`-F -` for commits, never `-m`**. Never
delete — quarantine. **Search before filing BOTH ways: exact (symbol/path/error string) to decide,
FUZZY to discover — the noise is what found KS-808.**
**`decision_queue.sh add --json` SKIPS the flag loop**, so `--override-prior-rulings` is unreachable
there; the JSON-path equivalent is the key **`"_override_prior": true`** inside the object.
**`0_Brain/dashboard/data/` holds TWO irreplaceable files** — `chat_log.json` and `decisions.json`.
**Never `git add -A` it and never `git checkout <sha> --` it.** Discard the ten regenerated feeds by
name BEFORE pulling, then stage only those two.

**🟡 THE WATCHER'S IDLE LEG — MECHANISM CORRECTED 20:4x; DO NOT BUILD FROM THE OLD ONE.**
`STATE_DIR` is a **PER-INVOCATION `mktemp -d`** (`:30`), so the counters do NOT persist. The script
loops internally (`sleep` at `:217`) and **every fire path is `exit 0`, which kills the invocation and
DESTROYS that state.** The runner restarts it and `STABLE_N` samples later the same condition is
re-derived. **So the defect is not "no reset" — THE RESET AND THE FIRE ARE THE SAME EVENT, so a fire
can never suppress its own repeat.** **A `fired_$key` marker in `$STATE_DIR` would be wiped by the
exit that wrote it — that fix shape is VOID.** Correct shape: a **persistent** marker under
`$CTX_STATE` (`cockpit/state/`) keyed by pane AND capture hash, cleared when the hash changes, as the
ctx legs already do with `ctx_fired_${gen}_NN`. **MEASURED SAFE: leg (a), new mail, runs FIRST and
`exit 0`s before the pane leg (`:60-61`) — a repeating idle wake CANNOT mask a verdict.**

**🟡 QA LAUNCHERS.** `fleet/state/` is gitignored and holds **128 wrappers + 128 prompt files**,
invisible to every git search. **New wrappers go to the TRACKED `fleet/qa-agent/launchers/`.** The
bulk move of the 128 is **QUEUED** — a `mv`, never a gitignore change, never while gates are live.

## GIT
**PULL BEFORE EVERY WRITE** — the laptop seat is live on this vault. Discard the ten regenerated
dashboard feeds by name, stage `chat_log.json` + `decisions.json` + your real changes, then
`-c rebase.autoStash=true pull --rebase && push`. **Keep every autostash; drop nothing.**
