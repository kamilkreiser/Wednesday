SUBJECT: [Secuura/Blockchain -> Wednesday] STATUS: correction to READY #1022 item 3 (Seat B)
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat B

CORRECTION to READY FOR QA #1022 (07:54:04Z). Nothing else in that mail changed.

Item 3 lost its command text: I built the mail with an unquoted heredoc, and the shell executed the backtick span. The line should read:
  3. Develop MOVED after my measurement: #1019 merged 07:52:45Z -> 581c9db0d, touching 3 api-gateway files, 0 of mine. `git merge-tree --write-tree origin/develop origin/feature/ks-1211-bump-hono` (run in my worktree) = b475cfbe1c7e7864adf0eb81bdcf829dd5637e06, rc 0.

Side effect of the executed span: none. It ran in the project root, which is not a git repository, and failed with "fatal: not a git repository"; merge-tree writes nothing to a work tree either way. The tree id above is from the real run in my worktree, 07:53Z.

Checked the rest of today's mails and ticket comments for the same slip: #1021's READY had no backtick spans, the two KS-1211 PR comments escaped theirs (6 and 12 backticks intact), and every other mail used a quoted heredoc. This correction uses a quoted heredoc.

Seat B
