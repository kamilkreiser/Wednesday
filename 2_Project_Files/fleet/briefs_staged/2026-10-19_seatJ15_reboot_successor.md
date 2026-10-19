## REBOOT SUCCESSOR — you are Seat J 15th (lane Secuura/Blockchain-J)

**Why you exist:** the Studio REBOOTED at 17:31 AEDT (06:31Z); your predecessor's pane died mid-work and /private/tmp was wiped, so **its scratch clone and anything it had not pushed are gone**. Pushed refs survive on GitHub. Make a FRESH clone in your own scratch, then arm the gate and identity exactly as HOLDS below say, and read them back in your plan confirmation. Read the shared inbox for mails to your lane letter since 05:00Z: they are your predecessor's thread and they bind you unless this mail says otherwise. Wherever the brief below names your predecessor's ordinal as "you", read your own. Develop is 722e07f19cee683ea037930e601e380a9491f7b5 (Wednesday ls-remote 18:3x AEDT). The other lanes were also killed: **live right now are only the seats Wednesday relaunches this hour (R, J, G)**; C (#1614) and E (#1613) are held for their gate verdicts and come back after them, so their files are still NOT yours.

**J-specific state (from J 14th's mails, read by Wednesday):** KS-1603 was BUILT to Wednesday's four rulings of 16:55 AEDT:
1. a transaction-scoped set_config bypass GUC around one EXISTS read, with a cell proving the bypass does not leak;
2. tenant-equality narrowing only;
3. fail-open plus a loud warn on a probe fault, with a cell for it;
4. the TOCTOU race goes to its own ticket. **Done: KS-1650**, Medium.

The batch route does one up-front read, so there is no partial write. Red-first: 3 behavioural reds plus 5 absence reds at develop; 6 controls green; anchoring integration 103/103. J 14th's last STATUS (06:19Z) said "push in the gate". **PR #1615 (head 4db96203546b) appeared after that. Establish whether it is yours (KS-1603) before anything else.** If it is: re-clone, re-run the reds and controls on its head, and send READY FOR GATE. If no KS-1603 branch was pushed, rebuild it to the four rulings. Then KS-1629. Wednesday APPROVED (17:22 AEDT) a read-only reading of SIMULATE_ANCHORING on both boxes: that variable only, with a control. Plan confirmation first.

---
## BLUF

You are **Seat J 14th** on Secuura Platform K (lane Secuura/Blockchain-J, the anchoring lane; J 13th wrapped at 05:13Z after merging #1568 and #1607). Two tickets, in order, one PR each: **KS-1603** (Backlog, priority 2, unassigned, 3 comments, last 2026-10-18T20:31Z): anchoring `POST /api/anchors` never checks who owns the `documentId`, so a caller can write a flat anchor onto another tenant's document. Build the **interim ownership check** Stuart asked for ("an interim ownership check on the flat anchor route would already protect S's rows"). Then **KS-1629** (Backlog, priority 4, unassigned, 1 comment, last 2026-10-19T02:47Z): originate `GET /api/anchors/:documentId` WRITES (a read mints a `tx_sim_` anchor_store row). Send a plan confirmation before your first write.

## QUEUE

1. **KS-1603 interim ownership check.** Read the ticket and all three comments, then KS-1384's newest comment (Kam's 9 Oct ruling, posted today as comment 229550f9). Wednesday's triage points at `services/anchoring/src/index.ts` near `:1372` (the flat-anchor upsert) and `services/originate/src/routes/anchors.ts` near `:109`, read at develop 7e2f8157cec2; #1607 changed anchoring index.ts since, so re-locate both at the tip. **The structural fix (a tenant column, one anchor per lifecycle event) is NOT this queue**: it is a multi-PR project on Kam's open card `secuura-ks1384-schedule-per-event-anchors-1019`. Build only the interim check: the smallest change that refuses a caller who does not own the document, on BOTH upsert paths if there are two. State in your plan what "owns" means in the code today (which column or join decides it) and cite the line; if the code has no way to decide ownership without the structural fix, STOP and mail me before writing. Red-first (a cell that writes onto another org's document is accepted at the tip and refused with the fix), a control (the owner's own write still succeeds), tier 1 gate. `Refs KS-1603`.
2. **KS-1629 read path that writes.** Same file family (`anchors.ts`, triage pointer `:168-219` at 7e2f8157cec2), so it goes AFTER KS-1603 is raised, on its own branch based on develop. Make the GET not write; red-first cell that counts anchor_store rows before and after a GET. If removing the write changes an answer a client relies on, STOP and mail me. Tier 2 unless the change touches auth. `Refs KS-1629`.
3. After each PR: READY FOR GATE with the cause, the cells, suite counts at the landing parent, the files, your predicted landing tree. Then one BLUF comment per ticket after the PR is raised (what changed, that it is at review, no date).
4. **Not in this queue:** KS-723 (the ~157 undocumented operations: spec-wide, collides with every lane) and KS-1454 (anchor schema). Leave both untouched; I will scope them separately.

## PARTITION

Yours: `services/anchoring/src/index.ts`, `services/anchoring/src/anchorOverwriteGuard.ts`, `services/originate/src/routes/anchors.ts`, and their tests. Say so before touching any other file. **NOT yours, live right now:** Seat R 52nd (Secuura/Blockchain-R): api-gateway (`src/index.ts`, `src/services/health.ts`, `src/routes/platform.ts` after E), originate `routes/verification.ts` (#1597 at gate). Seat C 25th (Secuura/Blockchain-C): originate `routes/documents.ts` and its KS-1402 suspects (`documentRepo.ts`, `gatewayProvenance.ts`). Seat E 3rd (Secuura/Blockchain-E): api-gateway `routes/platform.ts` (KS-1195) and ticket replies. A certifications seat may launch beside you on originate `routes/certifications.ts`. **You share an inbox with all of them: a brief or ANSWER naming another seat is not yours.** Identify yourself by your pane's cockpit name, never by which thread looks familiar.

## HOLDS

- **Identity:** before the first commit in ANY clone, set `git config user.name 'Kam Kreiser'` and `git config user.email kamil.kreiser@secuura.ai` LOCALLY, then read back `git config --show-origin user.email`. This Studio's global identity belongs to another client.
- **Work in a fresh clone in your own scratch or the project's deploy-clones/** (a `worktree add` writes a ref into the shared checkout; C 25th found the shared checkout's develop is stale, so fetch develop explicitly).
- **Pushing:** the repo's `.githooks/pre-push:352-358` refuses a push whose tip is not the checked-out HEAD, so check out the branch you push. `:76-80` refuses a non-fast-forward push. Never `--no-verify` and never `ALLOW_FORCE` without a mail from me naming it. Push with the transport in full: `-c core.sshCommand='<the repo's ssh command> -o ServerAliveInterval=30'`.
- Merge only on Wednesday's head-pinned GO after a gate verdict. No deploy.
- Client-facing communication = ticket comments only; the extranet is not a channel; nothing else to Stuart or Peter.
- No Docker on this Studio; PostgreSQL measurements run on a scratch PG in your scratch. Rotate inside your 80-90 band at a clean boundary; write the handover first.

## RULED BY KAM, NOT YET IN AN ARTEFACT

- None that this seat delivers. (KS-1384 (a) "one anchor per lifecycle event", 9 Oct, was delivered today as comment 229550f9 by Seat E 3rd; its scheduling is Kam's open card.)

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE

- The structural KS-1384 project is not started; only the interim check is built.
- KS-723 and KS-1454 are out of this queue.

PROVENANCE:
- KS-1603, KS-1629, KS-723, KS-1454 state, priority, assignee, comment counts and last-comment times (as quoted inline) | Linear GraphQL, read by Wednesday with the project's own key | read 2026-10-19
- develop 846ae2788b3b, tree f8301c94deac | git ls-remote origin + fetch into Wednesday's own scratch clone | read 2026-10-19
- file pointers at 7e2f8157cec2 and Stuart's "interim ownership check" words | Wednesday's triage 0_Brain/reference/2026-10-19_stuart-list-triage/TRIAGE.md rows 3 and BLUF, citing Stuart's 12:11 message (my project, not yours) | read 2026-10-19
- pre-push refusals | your own .githooks/pre-push at 846ae2788b3b lines 76-80 and 352-358, read by Wednesday | read 2026-10-19
- KS-1384 comment 229550f9 | Seat E 3rd's DELIVERED mail, comment(id:) read-back | read 2026-10-19

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-19 16:39
