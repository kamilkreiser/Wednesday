# B1749 drafter commission — MPS hosted deploy of main 317bbb14 WITH the infrastructure apply (SEAT-D67)
Commissioned by Tuesday (s293), 2026-11-19. Drafter model: OPUS (routing row C8's exception: the kit is for a deploy whose
infrastructure apply replaces every app setting of a hosted site). You DRAFT a kit; you deploy nothing, run no `az`, and
send no request to any hosted host.

Draft ONE deploy kit `2_Project_Files/tuesday/briefs/2026-11-19_B1749_SEAT-D67_mps-hosted-deploy-main-317bbb14.md`
(+ `.measured` sidecar; return the drafter report as TEXT in your reply, Tuesday saves it) in the FORM of the last MPS
hosted deploy kit `2026-11-16_B1607_SEAT-D63_mps-showcase-deploy-main.md` (same folder: read it WHOLE, with its stamp
slots as filled, and the deploy seat's STATUS of that run in the MPS project's
`1_Project_Definition/Briefs/2026-11-16_B1607_STATUS.md`: Corrections, Deviations and every STOP first; prevent each by
name). Follow `2_Project_Files/tuesday/DRAFTER_RULES.md` whole (the volume is /Volumes/Datasec_DEV; read its newest
section of 2026-11-19).

THE AUTHORITY (read each at source and quote it in the kit, with the card ids kept OUT of any text that goes into the
project or onto GitHub):
- The product owner's ruling of 2026-11-19 on Tuesday's card `mps-hosted-deploy-main-317bbb14-1119`: read it with
  `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tools/decision_queue.sh show mps-hosted-deploy-main-317bbb14-1119`
  (status ruled, choice a, ruled_ts 2026-11-19T18:00:38; his tap on the board 18:00:05, verbatim: "Decision
  mps-hosted-deploy-main-317bbb14-1119: a - Deploy now, without the three seller checks again"). Quote the card's BLUF and
  option a's detail WORD FOR WORD: they are the scope. Option a: "Backup first. Run the infrastructure apply that sets
  the template place (it rewrites every app setting, so the settings are compared before and after), put the package on
  the site, check the files match, create one test template, restart, and see it listed. The one new warning sentence
  for operators goes as written. Every other check runs. Same rules as 16 November: roll forward only, stop if the start
  is refused or a check is unproven. The test login's secret stays yours to renew whenever you choose." (re-read it from
  the store; the store is the authority, not this paragraph).
- The earlier rulings it stands on: card `mpscalc-showcase-template-path-1116` (ruled a, 2026-11-16: the template store
  path and the warning), the 16 November deploy rules (the B1607 kit and the project's CLARIFICATIONS.md entries C-164,
  C-165, C-166, C-171, C-172; C-172 says the infrastructure file replaces every app setting on each apply). The standing
  rule: each MPS hosted deploy has its own card (CLARIFICATIONS.md line 324).

SCOPE, EXACTLY:
- The commit deployed is `317bbb14c7258023b1d2855a9bcce1b9b07b93f6` and NO other. One pull request (#218, a one-line API
  message change) is open against main; the product owner was told on the board it is NOT part of this deploy. **Tuesday
  HOLDS the merge of #218 until this deploy has run, so main should still read 317bbb14 when the seat starts; the kit
  makes that a Step-0 check (main moved = STOP and ask).** Even so, the kit pins the commit for the package and for the
  infrastructure file, proves by program that what is deployed is that commit's package, and says what the deploy tool
  does when main is newer than the pinned commit (read `scripts/deploy-from-ci.sh` whole at 317bbb14: its "refusal of an
  older package" rule may refuse a pinned older commit once a newer CI package exists: establish this from the script,
  and if it would refuse, the kit must say how the pinned commit's CI package is selected, or STOP-AND-ASK; never a
  workaround that disables a check).
- The infrastructure apply (`infra/modules/showcase.bicep` and whatever applies it): BEFORE the apply, a read-only dump
  of every app setting NAME of the hosted site (names and a hash of each value, never a value); a what-if of the apply
  where the tool offers one; the predicted difference stated as exactly: the template store path setting added (name
  from the code at 317bbb14), nothing else changed or removed. If the what-if or the names comparison shows ANY other
  setting added, changed or removed, the apply does NOT run: STOP with the list. AFTER the apply: the same dump and the
  comparison by program.
- Backup first, as the 16 November run did (name what is backed up and where; a backup is proven by reading it back).
- The acceptance check of MPSCALC-372: create one synthetic template, restart, see it listed; then remove nothing
  (never delete; say what the synthetic template is named so it can be recognised).
- WITHOUT the three seller checks (the test login's secret was expired on 16 November): name the three, state they are
  skipped by the product owner's ruling, and run EVERY other check of the runbook. Do not try the expired secret, do not
  renew it, do not touch any identity or secret.
- Roll forward only; stop if the start is refused or a check is unproven; never run a migration Down; no data change
  beyond the one synthetic template.
- AZURE IDENTITY AND TENANT: the kit names the exact environment, subscription and resource group from the B1607 kit and
  its STATUS (measured there), the project's own `AZURE_CONFIG_DIR` and the service principal the 16 November seat used;
  the seat runs `az account show` and compares tenant and subscription with the kit before any other `az` command, and
  an authorisation error is REPORTED, never worked around. Nothing outside that resource group is read or written.
- Records and tickets are NOT this seat's (a records pass follows): the seat writes its STATUS with every measured fact
  the records need (what ran, when, the before and after settings names, the package identity, each check and its result,
  what was skipped and why).
- Model for the deploy seat: OPUS (a hosted deploy with an infrastructure apply). Say so with the routing row.

REQUIRED: a PRIOR-WORK section (what the hosted site runs now, RELAYED from C-166 and the B1607 STATUS, marked relayed:
the seat measures it first, read-only, and STOPs if the site already runs 317bbb14 or something newer); every command
quoted from the B1607 kit's real run or from the scripts at 317bbb14 (never from memory); every expected output quoted
from the 16 November STATUS or marked UNMEASURED; an explicit list of STOP conditions; a rollback or stop position for
every step (what state the site is in if the seat stops there); the 18 commits between 5e800095 and 317bbb14 listed
with the one that changes the live site named; the launch line; Stamp slots for Tuesday (base, the authority read, the
launch window, hard stop, the environment facts Tuesday must re-read).

HOW: read-only everywhere except your kit, sidecar and scratch
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s293/d1749/`. Project:
'/Volumes/Datasec_DEV/!CODING/Datasec/Datasec MPS Commercial Calculator' (code at origin by `gh api -X GET` under the
project's own GH_CONFIG_DIR; the local checkout is stale). NO `az` command of any kind, no request to any hosted host,
no deploy, no build, no test run, no mail, no Jira write (Jira GET allowed: JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN by
name in-process). `decision_queue.sh` only with `show` and `list`. NEVER read `.local/`, `Source_Documents/**`, a price
book, or any secret value (name a credential by its variable name only). Nothing of HPSM-POC or any other project. No
`cd`; no unquoted word starting with `=`; zsh; absolute paths; never delete; clocks from `date`; every zero with a
positive control. `stamp_check.py <kit>` must exit 0; Stamp slots unfilled; ASCII; built whole, temp file, os.replace.
First line of your reply: `STARTABLE: YES|NO - why`. Then: files, what the deploy tool does with a pinned older commit,
the predicted settings difference, the STOP list, corrections to this commission, D/Q defaults, UNMEASURED.
