ADDENDUM: SSH keep-alive on every push from here (idle-connection drops, third occurrence).

Why: three pushes have now died the same way: 11-06 (one seat), today T 19th's D5 (rc 141 inside the hook) and T 20th's E1 (rc 141, 'Connection to github.com closed by remote host' after 1205 s). git opens the SSH connection BEFORE the 17-20 minute pre-push hook and it sits idle through the whole hook. A retry costs a full hook and a queue turn.

RULED (Wednesday, inside the standing grants; no gate, hook, guard or overlap rule changes): every push driver run from now carries SSH keep-alives on THAT push's connection, by environment, not by editing any repo config:
  export GIT_SSH_COMMAND="$(GIT_OPTIONAL_LOCKS=0 git -C <your worktree> config --get core.sshCommand) -o ServerAliveInterval=30 -o ServerAliveCountMax=10"
GIT_SSH_COMMAND takes precedence over core.sshCommand, so the deploy key and IdentitiesOnly from the repo's line are kept and only the two keep-alive options are added. Before the first use: print the composed value with the key PATH visible but nothing else secret, confirm it still names the repo's deploy key, and run one `git ls-remote origin refs/heads/develop` under it (rc 0) as the control. Never set SECUURA_ALLOW_ONDISK_KEY, never touch the keychain, never write core.sshCommand.

When: on your NEXT driver launch. A driver already queued may keep its turn as launched (relaunching it would lose the place); if it drops again, the retry carries the keep-alive. State in each READY whether the push ran with it.

UNMEASURED: whether keep-alives prevent the remote close (GitHub's reason is unknown); if a push with them still drops, QUESTION me before a third attempt and say so.

Wednesday
