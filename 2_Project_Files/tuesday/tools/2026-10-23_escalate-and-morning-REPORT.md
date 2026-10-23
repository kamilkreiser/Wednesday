# 2026-10-23 escalate-48h and morning awaiting counts: build report

## Built (new files only)
- tools/kam_awaiting_counts.sh : OPEN Datasec cards grouped by project ("awaiting N for <Project>"), total, per-card age in hours. `--json` for machines. Read-only.
- tools/escalate_48h.sh : OPEN Datasec cards with age > 48 h (age = now minus the card `ts` field) not yet in the state file; ONE mail to kamil.kreiser@datasec.com.au from tuesday-agent@agentmail.to (AgentMail /v0/inboxes/<inbox>/messages/send, same call shape as send_brief.sh; key read in-process from 4_Credentials/.env, never printed). Subject `[Tuesday -> Kam] 48h unanswered: N Datasec card(s)`. State `fleet/state/escalated_48h.json` (gitignored, confirmed by `git check-ignore -v`) is written only after HTTP 200, with the message id. Sends only with `ESCALATE_SEND=1` and no `--dry-run`; otherwise prints the mail and writes nothing.
- tests/escalate_48h_arms.sh : the arms below.

Store: `0_Brain/dashboard/data/decisions.json`, override with `DQ_FILE` (same variable decision_queue.sh uses). Datasec filter is `client_project` startswith `Datasec/`. Other overrides: `ESCALATE_STATE`, `ESCALATE_ENV`, `ESCALATE_THRESHOLD_H`.

Findings: the store's cards have one timestamp field, `ts`; one of 903 cards lacks it (skipped with a stderr warning). Failure to read state refuses to send. A mail covering several cards marks all of them escalated with one message id.

Live dry-run today (store untouched, nothing sent): 1 open Datasec card, composer-l05-setup-card-too-1014 (Security-Composer, 219 h), which would be the first escalation on arming.

## Arms output
```
awaiting 2 for ProjA
  arm-47h  47.0h
  arm-1h  1.0h
awaiting 2 for ProjB
  arm-50h-done  50.0h
  arm-49h  49.0h
total awaiting: 4
PASS counts ProjA=2 ProjB=2
PASS total 4
PASS counts never show non-Datasec
PASS counts exclude ruled
PASS json valid and total 4
DRY RUN (nothing sent, no state written)
to: kamil.kreiser@datasec.com.au
from: tuesday-agent@agentmail.to
subject: [Tuesday -> Kam] 48h unanswered: 1 Datasec card(s)

BLUF: 1 Datasec decision card(s) have waited more than 48 hours for your answer. The live board is where to answer; reply there, not by email.

- arm-49h
    project: ProjB
    title: T arm-49h
    age: 49 h
    default action if you don't answer: DA arm-49h

Each card is escalated once; you will not get this mail again for the same card.
-- Tuesday
PASS dry-run lists 49h
PASS dry-run omits arm-1h
PASS dry-run omits arm-47h
PASS dry-run omits arm-50h-done
PASS dry-run omits arm-other-60h
PASS dry-run omits arm-ruled-70h
PASS dry-run omits Secuura
PASS subject says 1 card
PASS state untouched by dry-run
PASS default (no ESCALATE_SEND) is dry
PASS state untouched by default run
escalate_48h: nothing to escalate
PASS after simulated send, lists nothing
PASS send without key refuses, no state, no mail
PASS=18 FAIL=0
```

## How to arm (PROPOSED, not installed)
1. Morning ritual / checkpoint: run `bash .../tools/kam_awaiting_counts.sh` and paste its lines into the morning fleet-activity item (summary, plan, then "awaiting N for X, M for Y"). No send risk.
2. Escalation: run `ESCALATE_SEND=1 bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/tools/escalate_48h.sh` from the checkpoint ritual, or hourly via launchd (StartInterval 3600 running that command with the env var set). Because each card is escalated once, hourly runs do not repeat mail. Recommend one dry-run read by Kam's approval first, since the first real run will mail the 219 h card.
