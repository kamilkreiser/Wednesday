---
date: 2026-09-09
type: pickup
scope: DATASEC ONLY — Tuesday, on Kamils-Mac-mini. Secuura and general work are Wednesday's, on the Studio.
source: written at Tuesday s3's 50% checkpoint, 2026-09-09 ~16:0x AEST
status: live
supersede: replace this file WHOLESALE at the next pickup; never append. It replaced the s2 pickup.
---

# NEXT PICKUP — Tuesday, after s3. TWO SEATS ARE RUNNING and Kam is waiting on one of them.

**Run `2_Project_Files/tools/kam_rulings_today.sh` before writing anything** — and see the 🔴 channel
warning below, because that tool cannot see everything Kam says. **Mail timestamps are UTC ≈ AEST−10.**
**Rotation band 80–90%; 50% and 70% are checkpoints only.**

## 🟢 WHAT IS RUNNING — two seats, both verified at rung 5, both report to `tuesday-agent@`

| Pane | Seat | Commission | State |
|---|---|---|---|
| `%12` | **SecReview-Reformat** | Kam's proofread + reformat of the consolidated register | **THE ONE HE IS WAITING ON.** Reading the MyEmpire model when last checked. |
| `%11` | **Datasec/NexusAI** | Azure Marketplace readiness — ANALYSIS ONLY | Named its commission and its mail destination. |

**Launchers:** `2_Project_Files/fleet/launch_secreview_reformat.sh` (guards red-proofed: rc 6 missing
model, rc 9 altered totals, rc 0 positive control on the same scratch tree). NexusAI was briefed
through `brief_and_launch.sh` — **sent and VERIFIED at `datasec-nexusai@` 05:47:01Z** — then launched
by hand (see the launcher trap below).

🔴 **WHEN THE REFORMAT SEAT DELIVERS, EMAILING THE COPY TO KAM IS TUESDAY'S JOB, NOT THE AGENT'S.**
Kam is the principal, so mailing him is **not** external communication — but the brief tells the agent
not to do it. Send to `kamil.kreiser@datasec.com.au` (his instruction: the corporate address for
client material), from `tuesday-agent@` by direct POST, and **sweep the attachment personally before
sending, reading every hit.**

## 🔴 KAM'S THREE ASKS TODAY — verbatim, verified first-hand in `chat_kam.json` after a pull

- **15:37:33** — *"Please review the Nexus AI project and analyze if anything still needs to be actioned in order to prepare the project for a listing with Azure Marketplace."*
- **15:40:49** — *"With regard to the security review, please proofread the document as it's poorly written with no punctuation and grammar applied to it, and make sure the document is formatted properly. You can use the previous July or June report as a basis... Once the revised version is done, please email me another copy."*
- **15:41:28** — *"Also, do not use emojis as part of this document. Use tables and references so that it's properly formatted... you should be able to, in the folder, find a security review put together by My Empire for references."*

**Both arrived in WEDNESDAY's panel and she routed them unread.** Not a reassignment; the 09-08 split stands.

✅ **HIS "MY EMPIRE" REFERENCE EXISTS — he spelled it as two words and it is ONE.**
`Test Related Documents/Datasec - Penetration Test Report - 1.0.pdf`, 3.2 MB, *"Prepared by MyEmpire on
behalf of Datasec"*, v1.0, 15 Aug 2023, opening with a Document Control and version table.
**Two of Tuesday's three searches were the wrong FRAME** — filename-only, then the two-word spelling —
and only a content grep with a working control found it. **Do not report a thing absent on one frame.**

## 🔴 THE CHANNEL FINDING — the rulings tool is BLIND to a channel Kam really uses

The s2 pickup quoted Kam saying he had the document. **Four instruments said it never happened**:
`kam_rulings_today.sh`, `chat_kam.json`, `chat_log.json` and the inbox all stopped at 13:05.
**It is real.** It sits in the PREVIOUS SEAT'S TRANSCRIPT as a `queue-operation` at **13:14:56 AEST**
with `origin: {kind: "human"}`, absorbed mid-turn. **Kam typed it into the terminal pane, and
terminal-typed messages never enter `chat_log.json`.**
**THE RULE: before contradicting a predecessor's quote of Kam, grep `~/.claude/projects/<tree>/*.jsonl`.**
And note the trap in the mitigation: the 09-07 fix says curl the local dashboard API when the file lags —
**today the local API was BEHIND the file** (1,829 rows to 1,980). Both read the same stream, so both
share the blind spot.

## ⚠ TRAPS — s2's still hold; these are s3's additions

1. 🔴 **`cockpit.sh launch` IS DEAD FROM THIS SEAT FOR EVERY PROJECT.** `launchers.conf` pins
   `/Volumes/DevMASTER/...`; DevMASTER is not mounted here. **All 8 entries MISSING, T9 equivalent
   EXISTS (the control).** And the 2026-08-25 travel-drive fallback is defeated by the tree's NAME —
   `${SCRIPT_DIR%/WEDNESDAY/*}` never matches under a `TUESDAY` tree, so it returns the path unchanged
   and builds something impossible. **WORKAROUND, exact rather than approximate:
   `cockpit.sh add "<name>" 'bash "<real T9 path>"'` calls the SAME `add_pane` that `launch` calls**,
   so the pane is identical in name and monitor coverage. **Fix proposed to Wednesday and proven
   neutral on both WEDNESDAY path shapes: derive the drive root from the VOLUME, not the tree.**
2. **`send_brief.sh` REFUSES any project absent from `inbox_routing.conf`** — and **Datasec/Security
   Review is not in it.** That project is launched by a wrapper with a prompt file, never by mail.
3. **The brief gates are strict and they were all RIGHT:** a `PROVENANCE:` anchor needs its COLON;
   a `SELF-CHECK:` timestamp must be GENERATED, not typed; and a missing `RULED BY KAM, NOT YET IN AN
   ARTEFACT` section refused a brief and **turned out to be hiding three real undelivered NexusAI
   rulings, including `nexusai-rd369-round3-or-ship-at-the-cap` ruled `round3` by Kam TODAY at 12:09,
   authorised and not started.**
4. **The watcher wakes are mostly not yours.** Nine wakes at this seat today; **one was actionable.**
   Two were this seat's OWN outbound. Check your inbox AND the bus; if it is in neither, it is hers.

## 🔴 WHAT IS ACTUALLY ON KAM'S DESK (this seat's items only)

0. 🟡 **`secreview-june-register-discloses-credentials` — ruled `all-three`, and the DISTRIBUTION LEG IS NOW
   ANSWERED. Kam, 2026-09-09 ~16:3x, verbatim: *"no, nothing has been sent to anyone outside"*.**
   **So the exposure is CONTAINED to people who already hold repository access: nothing to recall, nobody to
   notify, no disclosure conversation. The scrub is routine work, not an incident.**
   🔴 **DO NOT LET THAT READ WIDER THAN IT IS: the eight secrets remain COMMITTED IN SOURCE, which is the
   original finding underneath this, so ROTATION IS STILL OWED and is NOT this seat's — Datasec production
   is ungranted and rotating live credentials is Kam's either way.** **SEQUENCING RULED BY TUESDAY: the
   scrub runs AFTER the reformat lands, because the reformat seat is using the June register as one of its
   two format models and editing it underneath would change the model mid-pass. Kam told, default stated.** Tuesday checked whether his 13:05
   *"nothing sent yet"* answered it — **it did not; that was about the Secuura review.** Do not close it.
   **Re-derived at source this session and it holds: eight value-bearing lines, F-16 six and F-12 two**
   (2 Entra client secrets, 1 platform API key, App Configuration read+write master keys in a committed
   tfstate backup, 1 PFX password, admin/DB password literals). **Class and count only — never a value,
   a prefix or a length.** **All six F-16 sites are ALSO in the circulated `.docx`**, verified inside
   `word/document.xml` with positive and negative controls — so a Markdown-only scrub leaves the
   customer-facing artefact disclosing. **Rotation is NOT this seat's: Datasec production is ungranted.**
   ⚠ **Tuesday's first detector for this FAILED ITS OWN CONTROL** (12 hits in a finding with no
   disclosure) and was discarded; the eight came from reading the evidence block with values masked.
1. **The developers' dev tenant ID** — Kam named it by DESCRIPTION only (15:37-era clarification at
   12:15). `fc05dcdd` is a strong candidate the workspace file forbids asserting. **A strong candidate
   is not a measurement.**

## STANDING

🔴 **EVERY WRAP: `git add 0_Brain/dashboard/data/usage_tuesday.json`** — generated AND must be
committed; this repo is the only transport to Kam's dashboard chip.
**Scope (Kam, verbatim):** *"you will work on ONLY datasec projects unless otherwise instructed."*
**Cross-seat mail is COORDINATION ONLY.** **FOUND / TESTED / HOW** on every analysis.
**Names, not pronouns. Never delete — quarantine.**
🔴 **DO NOT run the wrap's vault step** (`end-of-session.md:50` is `git add -A` and the vault's
untracked set holds Secuura paths). Skip it and say so.

## WHAT s3 WOULD SAY IF IT COULD SAY ONE THING

**Three times today an absence was my own frame rather than the world** — MyEmpire missing because I
searched filenames and the wrong spelling; a credential census that "found" twelve disclosures in a
finding with none; and four agreeing instruments that all read one stream. **Agreement between
instruments that share a source is not corroboration, it is one measurement counted several times.**
The thing that broke all three was the same: a control that could fail independently.
