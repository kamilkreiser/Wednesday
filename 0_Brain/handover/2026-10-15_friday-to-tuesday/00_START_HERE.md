---
date: 2026-10-15
type: handover
from: Friday (laptop seat)
to: Tuesday (Datasec seat, always-on machine)
client: Datasec — ONLY Datasec. Nothing in this folder concerns any other client.
status: live
source: Kam, terminal to Friday 2026-10-15 ~11:0x AEDT (verbatim below)
---

# HANDOVER — Friday → Tuesday: three Datasec projects (2026-10-15)

## Kam's words (verbatim, as dictated)
> *"I would like to manage the 3 projects that you have been working on on a machine that is constantly on and a newer
> machine while you keep working with me on the laptop when I am travelling. Can you please create thorough handover files
> for each project that will be read and picked up by the tuesday agent on the other machine. Also, you will have a lot of
> learining and rules so please share these with tuesday so all learnings about operation, and the project are shared with
> tuesday. Once you create all the necessary files, email instructions to tuesday and cc me on it. I will get a new external
> drive for you so assume Tuesday will start working of the laptop CCD."*

**What this means:**
- **Tuesday takes over coordination of three Datasec projects:** HPSM-POC, Datasec MPS Commercial Calculator and
  Datasec Security Composer. The HPSM records work Friday also held moves with HPSM-POC; it lives in the same family.
- **Tuesday works from the LAPTOP DRIVE**: the external volume named `Laptop-DEV`, which Kam will move to the always-on
  machine. Every project path below is `/Volumes/Laptop-DEV/!CODING/Datasec/<project>/`. If the volume mounts under a
  different name on your machine, swap the prefix and nothing else.
- Friday keeps working with Kam on the laptop while he travels, on a NEW drive. **From the moment you claim these projects,
  Friday no longer drives them** (see "Claims" below).

## Read in this order
1. This file.
2. `04_LEARNINGS-AND-OPERATING-RULES.md`: how Friday ran these projects, the tooling, and which lessons and ledger
   rows carry the operating knowledge. **Read it before you brief anything.**
3. The project files, each standalone:
   - `01_HPSM-POC.md`
   - `02_MPS-Commercial-Calculator.md`
   - `03_Security-Composer.md`
4. Each project's OWN `CLAUDE.md` → `1_Project_Definition/CLARIFICATIONS.md` → newest `5_Project_History/history.md`
   entry. These are the source of truth. The handover files are a mental model of them, measured 2026-10-15 10:5x AEDT.

## State at handover (measured 2026-10-15 ~10:5x AEDT, not copied from notes)
| | HPSM-POC | MPS Calculator | Security Composer |
|---|---|---|---|
| GitHub | `datasecau/HPSM-POC` (+ records `datasecau/HPSM-POC-analysis`) | `datasecau/MPS-Commercial-Calculator` | `datasecau/Datasec-Security-Composer` |
| main | `d916baf7` (B248 Pkcs 9.0.21, #155), main ci GREEN (run 38470487072) | `e2990622` (B94 rental book, #40), main ci green | `45591406` (B149, #78) |
| Open PR | none | **#41** (B97 rental-book word fixes, head `7dd8dc8d`, Friday GO) | **#79** (B152 approved words + looks, head `fa5a0b6a`, gate B153 GO WITH NOTES, Friday GO) |
| Hosted / demo | hosted `dc136e68` (FROZEN 14 Oct by Kam: nothing to hosted that day) | hosted `b9a3d769` (live-checked 10-13 22:23) | demo `ef916ce2` |
| GitHub Code Security | **enabled** (measured today) | **enabled** (measured today) | **enabled** (measured today) |
| Live seats | none | none | none |

**Code Security is back on for all four Datasec repos** (HPSM-POC, HPSM-POC-analysis, MPS, Composer; measured by API
today). On 10-14 it was OFF and no Datasec PR could merge. Your NexusAI repo was blocked by the same switch, so re-check it.

## Open Kam card (one)
- `composer-l05-setup-card-too-1014`: *"Security Composer: the approver email change also shows on the Expert set-up
  card. OK?"* (rec a; default: merge #79 when Code Security allows, nothing to demo until he taps). It sits on the FRIDAY
  tab. Ask Kam to re-file it under Tuesday, or read his tap there.

## Your first actions (in order)
1. `git pull` your brain tree. This folder, Friday's ledger, notes, pickup file and tooling all live in the shared
   `kamilkreiser/Wednesday` repo, under `0_Brain/handover/2026-10-15_friday-to-tuesday/`.
2. **Claims.** Friday's OPEN claims on these projects are released by Friday in the same commit as this handover (see
   `wed_claim.sh list`). Claim each project as YOURS before you brief:
   `2_Project_Files/tools/wed_claim.sh claim "Datasec/HPSM-POC — Tuesday"` (and MPS, Security-Composer, HPSM records).
   If a Friday claim still shows OPEN, it is stale: Friday has handed over. Release it with a note naming this handover.
3. Mount check: `ls "/Volumes/Laptop-DEV/!CODING/Datasec/"` must show `HPSM-POC`, `Datasec MPS Commercial Calculator`,
   `Datasec Security Composer`. Each project's `Launch_Claude.command` carries its own logins (deploy keys in
   `3_Access_Keys/`, env in `4_Credentials/`). They are on the drive, so they travel with it.
4. Read Kam's rulings for the three projects before any card (your `kam_rulings_today.sh`, view tuesday AND friday:
   his Friday-tab rulings on these projects stay binding).
5. Then the NEXT WORK list in each project file. The quickest wins: **merge MPS #41** (then hosted deploy) and
   **merge Composer #79** (then demo deploy). Both waited only on Code Security, which is now on.

## Grants: re-confirm before relying on them
Grants are seat-scoped, so **none transfers automatically**. Ask Kam once, in one question, whether these now apply to Tuesday:
- **Push READY changes to the Composer demo + hosted HPSM-POC without a card** (Kam to Friday 2026-10-06 19:31:00,
  verbatim *"Once it's ready, push to demo. Don't wait on my word."*, scope confirmed "both the Composer demo and
  HPSM-POC"). READY = QA gate passed + coordinator's own check.
- **MPS hosted deploys**: on 10-13 Kam ruled each one by card (`mpscalc-hosted-deploy-b9a3d76-1013` = a). Treat MPS
  hosted as card-per-deploy unless he says otherwise.
- **Friday's "ignore all usage gates" (10-13 18:49:38) is DEAD.** Its event happened: Kam signed Friday into the new
  account today. It never applied to you.

## Drive sync in progress (context, not your task)
On 2026-10-15 Kam asked Friday to sync the laptop drive with the T9. Friday backed up uncommitted work from both drives to
`/Volumes/KK_T9_External_HDD/_SYNC_2026-10-15/step1_uncommitted/`. It also cross-fetched commits between the drives' copies of 15
shared repos into namespaced refs (`refs/remotes/t9-drive-2026-10-15/*` on the laptop, `refs/remotes/laptop-drive-2026-10-15/*`
on the T9). No working tree, branch or HEAD was changed. If you see those refs, that is where they came from; they are
safe to leave. The rest of the sync, and freeing space on the laptop drive (it was 99.9% full), is still with Friday and Kam.
**The laptop drive was nearly full at handover (~1–2 GB free). Check `df -h /Volumes/Laptop-DEV` before any build.**
