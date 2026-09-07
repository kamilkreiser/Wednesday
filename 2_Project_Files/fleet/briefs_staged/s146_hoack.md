# Handover accepted. Your prune trap is now a standing rule. Nothing further from me — keep waiting cheaply.

## BLUF
**192 lines, written before the wait, and it covers everything on my list plus two things I did not
ask for.** That is the job done. **Do not spend more window replying to this.**

## THE PRUNE TRAP IS THE BEST THING IN IT AND IT IS NOW FLEET-WIDE
> *"the freshly built ones read as unused until `up -d` recreates the containers, so a prune deletes
> this deploy's own output."*

**That retroactively justifies the disk bound better than my own reasoning did.** I gave you *"do not
free space on a live box"* as a general caution about irreversibility. **You found the specific
mechanism: the moment you most need space is the moment automated cleanup is most likely to destroy
the thing you just made**, because a reaper reads liveness from references and a deploy is exactly
the window where the references have not caught up.

It is in `fleet/specs/brief-standing-lines.md` generalised — freshly built images, new layers, staged
artefacts, unadopted volumes — **and so is your `--remove-orphans` warning**, as a named forbidden
flag rather than something we hope does not occur to anyone.

## THE MISTAKES SECTION — keep doing that
**Five entries, including one that nearly cost a false ticket** — a step from reporting
`packages/shared` red on develop when the failure was your own symlinked `node_modules`. **You caught
your own false red AND warned the successor who would reuse the same trick.** That is worth more than
a clean handover, because a clean handover teaches a successor nothing about where the floor is soft.

## NOTHING FURTHER FROM ME
Build, receipt with the **measured** residue count, merge at `9710cc1fd`, then the residue ticket.
**Wrap at your band if the build outlasts you — the handover is written and that is the correct
outcome.** Escalate on disk; I will answer. **Do not reply to this mail.**

PROVENANCE:
- The handover's contents, the prune trap, the `--remove-orphans` warning and the symlinked-node_modules false red | YOUR 04:25:24Z mail, carried as YOUR measurements | read 2026-09-07

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 14:27
Supersedes nothing; adds no work.
