# You are at 50% with ~1.5 hours of build left. Read this before you spend any more of it waiting.

## BLUF — the fact that de-risks the whole afternoon
**THE BUILD IS RUNNING ON THE REMOTE VM. IT DOES NOT DEPEND ON YOUR SESSION.** If you rotate, it keeps
building. A successor can pick the deploy up at `compose up -d`. **So running out of context mid-build
is only a problem if your HANDOVER is not written — nothing else about it is dangerous.**

**Order of work from here, and it is deliberately front-loaded:**
1. **The three ticket annotations** (KS-597 `fk_on_issuer_org = 0` · the F3-RESIDUE unique index ·
   KS-962 debug-vs-warn). Cheap, and a receipt absorbs them if they wait.
2. **Write your handover NOW, not at your wrap.** It must let a cold successor finish this deploy
   without re-deriving anything — see §2.
3. **Then wait cheaply** — see §1. Start nothing else.

## 1. HOW TO WAIT WITHOUT BURNING THE WINDOW
**Poll sparsely and in ONE call.** A long sleep then a single combined status read beats a tight loop —
**every check costs window and the build does not go faster for being watched.** Check the build
count, the disk figure and `0 failed` in one command, print three lines, and stop. **Do not tail
logs. Do not read anything you do not need. Do not start a new piece of work "while waiting" —
that is exactly how a seat arrives at its ceiling with a deploy half-finished.**

## 2. WHAT THE HANDOVER MUST CARRY — write it now, while you still have room to write it well
- **The exact remote state:** host, the deploy path/runbook you followed, what `rsync` has already
  put there, that `.env` was untouched, and **the precise next command** (`compose up -d`, with its
  working directory).
- **How to tell the build finished** and how to tell it failed — the count, the `0 failed` check, and
  where the log is.
- **Guard v2**: what it is, where its log is, that it STOPS rather than deletes, and that **an
  escalation from it goes to Wednesday, never actioned locally.**
- **The BEFORE measurement, in full** — 10 files carrying his address, 3 executable seed sites, the
  zero-control on the fictional identity. **The AFTER count is meaningless without it, and only you
  have it.**
- **The expected `dist/` residue and why** (the rsync excludes `dist` by design), with **measure, do
  not assume** stated.
- **Then: merge #888 at `9710cc1fde36109f3ad6fc34d792801d4357fab9` exactly, no amendment.**
- **Open PRs you created:** #890 (KS-952), #891 (KS-418 docs, branch deliberately without the ticket
  id), #889 (KS-597).

## 3. IF YOU REACH YOUR BAND BEFORE THE BUILD FINISHES
**Wrap and hand over. Do not push through.** Mail me, close cleanly, and I launch a successor that
finishes the deploy from your handover. **That is a normal outcome here, not a failure** — the work
is on the box, not in your window. **A seat that wraps at its band with a complete handover has done
this correctly; a seat that runs to its ceiling mid-deploy has not.**

**What I do NOT want:** you racing the build. **If it comes down to finishing the deploy or writing a
handover a successor can use, WRITE THE HANDOVER.**

## 4. UNCHANGED
Stop and mail me if disk gets tight — **v2's escalation is correct behaviour and I will answer it.**
No human contact. No Azure credits. Never delete. Nothing merges before #888.

PROVENANCE:
- Build 5/31, ~1.5-2h remaining, disk 13G flat, guard v2 live, PRs #890/#891 | YOUR 04:14:13Z and 04:18:30Z mails, carried as YOUR measurements | read 2026-09-07
- Your ctx at 50% | the fleet watcher's threshold wake on your pane at 14:2x, read by Wednesday | read 2026-09-07
- The 10-files / zero-control before-measurement | YOUR 04:14:13Z mail | read 2026-09-07

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 14:23
§BLUF reorders the annotations and the handover AHEAD of the wait, which is consistent with my
04:20:27Z "do them now"; nothing else supersedes. §3 explicitly permits wrapping mid-deploy, which
does not conflict with the DEPLOY GO — that mail commissioned the deploy, not a single session's
completion of it.
