# o156 report (KS-1873, Secuura/Blockchain)
ROUND NOT RUN: STOP at pre-check 2 (ticket names no fix). No held READY, no brief, no files outside this folder.

1 tunnel + pin PASS: tunnel.sh check = UP (http://127.0.0.1:47788/v1/models 200); ls-remote develop = c78c80bd537015674fa5e22701d745946f94d4fb (matches Wednesday's read).
2 Linear STOP: KS-1873 "Admin create-user writes the new user's plaintext email to the info log" (Backlog). Zero comments. Body (read at develop e43a289c1c7b) states the problem only:
  "services/auth/src/routes/users.ts, in the admin create-user handler, logs logger.info('Admin created user', { email, role: user.role, createdBy: req.user!.userId }): the new user's plaintext email address goes to the info log. The tokenisation guide (docs/TOKENISATION.md) says logs carry no PII."
  "Not established: whether the logger redacts the email key (I did not trace the logger configuration), and whether other handlers log emails (I read this one line, not the whole service)."
  No sentence names a fix and no ruling exists. The options (mask / hash / drop the field / log a user id instead) are all open, plus an unanswered precondition: the logger may already redact `email`. The reported line is users.ts:678 per the commission; the ticket gives no line number.
3, 4 not run (STOP at 2).
Route: a card for Wednesday to rule on (which of mask / hash / drop / userId), and to have someone trace the logger redaction first; then re-offer as a Spark row if the ruling is a fully spelled-out edit. Tier 1 auth file, so the PR needs a TIER-1 Opus gate regardless.
Scratch: scratch/lin.py (read-only Linear query; key never printed).
