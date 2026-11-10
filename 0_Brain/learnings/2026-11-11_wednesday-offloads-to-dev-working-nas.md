---
date: 2026-11-11
type: preference
source: "Kam to Wednesday, terminal, 2026-11-11 ~10:5x: 'dont forget the NAS is connected so you can offlaod things there too' / 'i set it up recently'. Extends Tuesday's rule of the same morning (Kam: 'Put it in a logical folder and with a date so we can periodically clean this up. please save this as an ongoing workflow')."
status: live
tier: W
---

# Wednesday offloads to the DEV-Working NAS too: dated folders under Secuura/Wednesday or General/Wednesday, through the tool only

**The lesson:** When I need to back up or offload anything (gate scratch, old evidence, a copy before a risky change, files crowding a drive), it goes to the new NAS share `/Volumes/DEV-Working` through `2_Project_Files/tools/nas_offload.sh --client <secuura|general> <topic-kebab> "<why>" <abs source...>`. That writes `Secuura/Wednesday/<YYYY-MM-DD>_<topic>/` or `General/Wednesday/<YYYY-MM-DD>_<topic>/`, verifies sha256 per file, and writes a MANIFEST with REVIEW-AFTER +30 days. Every other rule is Tuesday's lesson [[2026-11-11_nas-dev-working-dated-offload]], applied to my half.

**How to apply:**
1. **Copy, never move.** Removing a source after VERIFIED is a separate step, inside my own tree only, quarantine rules apply.
2. **One client per offload; never Datasec.** `Datasec/` on the share is Tuesday's: never read, list or write it. The tool refuses Datasec and TUESDAY sources and secrets (4_Credentials, 3_Access_Keys, .env, keys).
3. **Clean-up is Kam's word.** Folders past REVIEW-AFTER are listed for him at weekly consolidation; deleted only when he says.
4. **Two NASes, do not confuse them.** DEV-Working is the NEW NAS (SMB //DotORG@192.168.20.154, mounted by Kam's login; also Backup and Seagate Hub shares). The OLD NAS (ssh alias `nas`, 192.168.8.190; the nightly `nas_push.sh` mirror to /Volumes/Development) did not answer from the Mac mini on 11-11 (ssh timeout; /Volumes/Development not mounted), so the naspush job refuses until Kam says whether to repoint it.

**Built + tested 11-11:** one VERIFIED copy (`General/Wednesday/2026-11-11_workflow-selftest`, 2 files incl. a spaced name) and four refusals (bad --client, existing folder, 4_Credentials source, a Datasec source). The first manifest carried Tuesday's seat label (copied tool); the label was fixed in the tool and corrected in that manifest.
