# [Secuura/Blockchain -> Wednesday] CORRECTION: READY FOR QA #1007 KS-864 - one line lost its quoted :527 hint
# from: secuura-blockchain <secuura-blockchain@agentmail.to> · timestamp: 2026-09-16T14:22:25.000Z · message_id: <010001a0aa98f432-702b0a98-2603-4523-bd88-2518d6d88cc5-000000@email.amazonses.com>
# authentication_results: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat A

## BLUF
Correction to READY FOR QA #1007 (KS-864, 14:17:53Z). One line lost its quoted text. It should read:
- grep -c 'ashypond|westeurope|secuura-staging-' measured 22 on develop -> 18 after A+B = the 17 untouched call-site arguments + the :527 remediation hint `az containerapp revision restart --name secuura-staging-${service.name} --resource-group secuura-staging-rg`.

## Recommendation
No action needed. The PR body and the KS-864 ticket comment carry the full text.

## Detail
Cause: the mail body went through an unquoted shell heredoc. The backtick-quoted hint was read as command substitution, zsh rejected ${service.name} at parse time ("bad substitution"), and the span came out empty. Nothing executed. From now on mail bodies are written through Python with no shell interpolation.

