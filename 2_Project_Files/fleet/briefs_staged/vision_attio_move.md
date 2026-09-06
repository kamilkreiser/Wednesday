# KAM RULING — ATTIO MOVES OUT OF THE DATASEC GITHUB ORG. Read before any further Attio work.

## BLUF
**Kam has ruled that Attio must not live under Datasec.** His words, 2026-09-07 09:28: *"i would still
like it to live outside datasec. please instruct everyone."* Earlier the same morning, on the card
`attio-repo-home` => **move**: *"i will set up under kamilkkreiser but not in datasec."*

**New home: `git@github.com:KamORG454/attic.git`.** Note the spelling — **`attic`, not `attio`.**
Wednesday checked rather than assuming a typo: `KamORG454/attic` returns HTTP 200, `KamORG454/attio`
returns 404. **Use `attic`.** Kam pasted an `https://` URL; **deploy keys are SSH**, so the remote is
the `git@github.com:` form above or the key is never used.

**Until this move is complete, DO NOT PUSH to `datasecau/attio`.**

## WHY — and the part that is Wednesday's fault, stated so you do not inherit the habit
Kam approved the renewal-date change on its merits at 07:07 and discovered afterwards that the commits
had gone into the **Datasec** organisation. His correction: *"Your role is to double-check and do so.
I approved ATO push, but did not realize that this was going to the Datasec repository."*

**Every artefact in that chain — the card, the brief, the dry-run review, the GO — described WHAT would
change and none named WHERE it would land.** That is Wednesday's failure, not yours. **The standing
rule now, in the fleet standing lines: any card, brief or GO whose consequence is a commit NAMES the
remote and branch in its BLUF.** Same for a deploy (environment) and a ticket (board).

**For the record, because you should not carry a suspicion that is not true:** a contamination scan run
at Kam's challenge found **zero Secuura references** in anything pushed that day, with a control
proving the search was live (48 `attio` hits in the same diff). Measured across the whole workspace,
Attio appears in **83 Datasec files and 3 Secuura ones** — and all three are session history, one of
them a Secuura agent recording it deliberately did NOT use an Attio finding because it belonged to
another project. **Attio is not, and never was, mixed with Secuura.** Kam accepted that. He wants it
out of Datasec anyway, which is his call about his own companies.

## WHAT IS ALREADY DONE
- **Deploy keypair created**: `3_Access_Keys/attic_deploy_rw` (mode 600) and `.pub` (644). That folder
  is gitignored — Wednesday verified, line 2 of the project's `.gitignore`.
- **The public key is with Kam** to paste at `github.com/KamORG454/attic` → Settings → Deploy keys,
  **with "Allow write access" ticked.** Until he does that, no push to the new remote can succeed.

## WHAT YOU DO — after Kam confirms the key is pasted, and not before
1. **Verify the key works before anything else:** `ssh -T` against the new remote using that key, or a
   `git ls-remote`. **A push is not the test — a failed push is how you find out too late.**
2. **Push the full history to the new remote.** All 53 commits. Verify at the destination with
   `ls-remote` that the head matches, and that the commit count matches — **the count is the receipt,
   the exit code is not.**
3. **Repoint `core.sshCommand` and `origin` repo-locally** to the new remote and the new key.
4. **The old `datasecau/attio` repo is ARCHIVED, NEVER DELETED** (Kam's standing rule: cleanup means
   quarantine). Archiving is a GitHub org operation — **that is Kam's hands or his named identity, not
   yours and not Wednesday's.** Report when you are ready for him to do it.
5. **Chase every pointer** — launchers, CI, docs, `CLAUDE.md`, credential paths, any script naming the
   old remote. `grep -rn 'datasecau/attio'` and count first; do not truncate a list you will call
   complete.
6. **`CLAUDE.md` line 27 cites Secuura** as the worked example of the workspace coupled-pair rule.
   Kam has seen it and it is on his queue as its own option. **Do not remove it unless he rules it.**

## ONE THING NOT RULED, and Wednesday will not invent it
Kam named the **repository**. He has **not** said whether the local folder moves out of
`/Volumes/DevMASTER/!CODING/Datasec/ATTIO`. **Default: leave the folder where it is; move the remote
only.** If you think the folder must move for the isolation to be real, say so in your wrap with the
reason and Wednesday cards it — **do not move it on your own judgement.**

PROVENANCE:
- Kam's two rulings, verbatim | `kam_rulings_today.sh` and the card `attio-repo-home` => move, from his own panel messages at 09:12 and 09:28 | read 2026-09-07
- That `attic` resolves and `attio` does not | `curl` against both GitHub URLs from Wednesday's seat — 200 and 404 | measured 2026-09-07
- The 83 vs 3 file counts and the zero-Secuura scan with its control | Wednesday's greps across `!CODING`, controls included | measured 2026-09-07
- The deploy key's existence, modes, and that `3_Access_Keys/` is gitignored | Wednesday created it and read the modes and the project's `.gitignore` | measured 2026-09-07
- Whether Kam has pasted the public key yet | NOT ESTABLISHED — confirm before you push | read 2026-09-07
- Whether the local folder should move | NOT RULED by Kam | read 2026-09-07

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 09:30
