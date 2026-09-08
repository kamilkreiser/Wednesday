---
date: 2026-09-08
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's (Kam ruled the name 11:56). Read Datasec mail by SUBJECT only.
source: replaced WHOLESALE at 15:4x by s153
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — 15:4x Tuesday. Kam is minutes from moving the T9 to the new machine.

## 🔴 THE LIVE THING: KAM UNPLUGS THE T9 IN ~15 MIN — STOP THE RSYNC FIRST
He asked at 15:40 whether the T9 is ready to unplug. **Answer given: ready for HER, not a complete
mirror.** The protocol he was told, and it must be honoured:
**he says the word → you `kill 14970` (the full rsync) → confirm nothing is mid-write → then he pulls it.**
Yanking mid-write leaves a half-written file, which is harder to notice than a missing one.
- **pid 14970** = the full `!CODING` pass, still running (~40 min in, I/O bound through node_modules).
  Log stays empty by design — check `lsof -p 14970`, never the log.
- **pid 44057** = a NON-DESTRUCTIVE `rsync -n` contents check of Datasec, started pre-emptively so
  the answer is ready if he asks for certainty → `2_Project_Files/fleet/state/datasec_contents_dryrun.log`.
- **MEASURED:** all 17 Datasec projects present on T9. **The T9 is AHEAD of DevMASTER for Datasec** —
  ~7,536 source files touched since 09-07 that DevMASTER lacks (the laptop seat's own work, exactly
  the topology Kam described). The additive push preserved all of it. Secuura is ~573K files behind
  on T9; that is Wednesday's scope, not hers, and the new machine does not need it.
- **STATED TO HIM, and keep stating it:** counts were compared, **not contents** — a count is not a
  subset check. Every project folder is present and nothing was deleted; individual file equality is
  what pid 44057 is establishing.

## 🟢 KAM'S THREE ASKS — ALL DISCHARGED THIS HOUR
1. **Tuesday's tree: he ran both commands.** Verified by reading, not by his terminal output:
   HEAD `6b76491d`, **clean**, the stash preserved (`refs/stash`, his files in it), her own launcher
   and `_ledger_laptop_datasec.md` present, the boot-pull block in her launcher. **She is
   self-maintaining from here.**
2. **`confirmbigdel = true` SHIPPED** on his explicit 15:37 authorisation, in HIS file
   `/Volumes/DevMASTER/!SYNC FILES/devnas.prf`, backup beside it (`.pre-confirmbigdel-2026-09-08`),
   verified with a positive control. **HONEST SCOPE, and Wednesday overstated it to him first:** it
   aborts only on a WHOLE-REPLICA delete (unison's own doc; with `batch = true` it aborts rather than
   prompts). It does NOT stop 500 files vanishing from a subtree — that is `scheduler/nas_sync.sh`'s
   alarm. **Prevention for the catastrophe, detection for the drift.**
3. **#768 RULED `route-to-main`** (15:38) — **he overruled BOTH Peter and Wednesday**, who both said
   let it ride. Relayed to s150 with that framing. **s150 opened PR #908 against `main`** on a
   `hotfix/ks-988-dependabot-drop-github-actions` branch, +22/−8 one file, diff verified identical to
   #768's own stat. **Card not closed until the ruling is IN an artefact** — s150 owes the PR link +
   comments on #768 and KS-988.

## 🟢 SECUURA — s150 in `%171` (~71% ctx; its band is 80–90, it rotates itself)
`develop` `e69fa0dc5` → `27b0ee294` (#907) → `9806be0ac` (#793) → `5c6777658` (#895).
**Open:** PR **#908** against `main` (Kam's ruling) · then back to the P2 queue.
**#895 merged with ZERO approving reviews** — read from the endpoint, stated on the ticket in the
repo's own language, because that was Kam's exception to make. **KS-682 is NOT proven until #896's
four-slot Playwright sweep runs.** KS-999/KS-1000/KS-997/KS-988 filed.

## 🔴 THE FINDING OF THE DAY — now FIVE instances, and the fifth is on OUR board
Every Peter item was work already done or an action already his, with nobody writing it where he
would see it: **#793** · **#721** (eight days on nobody) · **#768 item 3** · **#785** · and now
**KS-566**, which was done, deployed and mutually closed with Stuart while our board said In Review.
**Two of the nine had ZERO Peter comments** — the "hold" text was our own PR title and a Linear bot.
s150's formulation, adopted: ***"Peter's board is not wrong; it is uninformed, and we are the ones
who did not inform it."*** **If the pattern holds, the In Review column is overstated and the real
P2 queue is shorter than 27.** Kam has been told; no action asked.

## 🔴 STILL WITH KAM (nothing blocking)
- Older cards: `secuura-ks963-widen-to-preauth` (default holds) · `hpsm-…` · `secrev-…` ·
  `nexusai-rd369-…` (last three TUESDAY's).
- **NOT FILED, still owed:** `secuura-ten-cascade-collateral-restore-or-leave`.
- **PS #783** unreadable — the PAT 404s on the whole `Secuura/platform-s` repo (control run).

## 🔴 HOW TO WRITE TO KAM — CHANGED TWICE TODAY, BOTH HIS WORDS
1. **15:23 — the panel speaks the WHOLE message**, no paragraph split, no cap. Length now costs him
   real seconds. `2026-09-08_the-panel-reads-the-whole-message`.
2. **15:34 — the ASK GOES FIRST, spelled out as literal steps:** *"I need you to do X. The rationale
   is Y. My recommendation was… Other options include…"* If nothing is needed, say **"no action
   needed"** in the first line. `2026-09-08_ask-format-action-first`. The 08-06 format keeps its
   fields and gained a pointer; it had the ask FOURTH.

## 🔴 WEDNESDAY'S ERRORS THIS SEAT — eight, all cheap, all in `_ledger.md` (211 rows)
1. Told Kam nobody executed his #793 rulings — read `--undelivered` as a fact about the world.
   **An unmarked card means UNKNOWN, never UNDONE.**
2. Invented *"a DIRTY mark is probably real"*; all three were stale. **A snapshot is stale in every direction.**
3. `chat_reply.sh --help` posted "help" to his panel — a write-only tool with no usage guard.
4. `cockpit.sh say %171` — it wants the pane NAME; failed rc=1 with the rc uncaptured.
5. Made the panel speak only the first paragraph — his 14:24 words were about WHICH DEVICE, not HOW
   MUCH, and the quote sat in the code comment as if it authorised the choice.
6+7. **w=2, and the diagnosis is filed:** two safety claims stated wider than their checks —
   *"additive, so nothing is at risk"* (additive rules out deletions, not overwrites) and
   *"confirmbigdel prevents the August failure"* (whole-replica only). The scope-word rule listed
   words for classifying WORK; these were claims about a TOOL'S GUARANTEE, so the handle missed.
   `2026-09-08_a-safety-claim-names-the-property-it-checked`.
8. Buried the ask under its context — his 15:34 correction, above.

## HOLDS / STANDING
- 18,609-line hold on #896/#899/#900 STANDS; **#899 before #900** or the merge is a silent no-op.
- Refresh no advisory expiry date. Nobody messages Peter or Stuart outside ticket comments.
- **No check on that repo can pass** (Actions dead 19 days) — cite the manual twelve-leg preflight.
- **PROJECT TRAP:** any probe of `users.email` by literal comparison is void by construction (AES-GCM).
- The guard fails CLOSED on `$VAR` in `git -C` — **write literals**. It also refuses `stash list`
  (a read verb under a write parent) and a command QUOTED inside a message. Five correct refusals today.
- `decision_queue.sh add --json` reads the payload from **stdin**, takes no companion flags — put
  `"_override_prior": true` inside the JSON.
- **`timeout` does not exist on macOS.** Nor `declare -A`.

## BOOT NUMBERS (WED-139)
digest **303,794 B / 4,021 lines** WHOLE; ledger **400,644 B / 203 rows** at boot — today's 35 WHOLE,
09-07 (71) + 09-06 (97) as headlines. Statusline **7% → 21% → 31% → ~62% at 15:4x.** Ledger now 211 rows.
