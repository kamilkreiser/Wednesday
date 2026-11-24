| expected | command text | Bash | Monitor | PowerShell | Bash found, another not? |
|---|---|---|---|---|---|
| Credential | `cat ~/.aws/credentials` | found Credential | found Credential | found Credential | no |
| Credential | `gc ~/.ssh/id_rsa` | found Credential | found Credential | found Credential | no |
| Credential | `Get-Content $HOME/.ssh/id_rsa` | found Credential | found Credential | found Credential | no |
| Credential | `Get-Content $env:USERPROFILE\.ssh\id_rsa` | ALLOWED | ask T3 | found Credential | no |
| Credential | `type %USERPROFILE%\.ssh\id_rsa` | ALLOWED | ask T3 | found Credential | no |
| Credential | `Get-Content -Path ~/.git-credentials` | found Credential | found Credential | found Credential | no |
| Credential | `Select-String -Path ~/.aws/* -Pattern key` | found Credential | found Credential | found Credential | no |
| Credential | `cat "$HOME"/.netrc` | found Credential | found Credential | found Credential | no |
| Credential | `cat .env.local` | found Credential | found Credential | found Credential | no |
| Credential | `Get-Content .env` | found Credential | found Credential | found Credential | no |
| PermissionModeChange | `npx x --dangerously-skip-permissions` | found PermissionModeChange | found PermissionModeChange | found PermissionModeChange | no |
| PermissionModeChange | `& x.exe --dangerously-skip-permissions` | found PermissionModeChange | found PermissionModeChange | found PermissionModeChange | no |
| PermissionModeChange | `x --permission-mode=bypassPermissions` | found PermissionModeChange | found PermissionModeChange | found PermissionModeChange | no |
| SandboxBypass | `Get-ChildItem` | found SandboxBypass | found SandboxBypass | found SandboxBypass | no |
| Privilege | `sudo -i` | found Privilege | found Privilege | found Privilege | no |
| Privilege | `\sudo ls` | found Privilege | found Privilege | found Privilege | no |
| Privilege | `command sudo ls` | found Privilege | found Privilege | found Privilege | no |
| Privilege | `Start-Process pwsh -Verb RunAs` | found Privilege | found Privilege | found Privilege | no |
| Privilege | `Start-Process -Verb runAs pwsh` | found Privilege | found Privilege | found Privilege | no |
| Privilege | `Start-Process pwsh -Verb:RunAs` | found Privilege | found Privilege | found Privilege | no |
| Privilege | `gsudo ls` | found Privilege | found Privilege | found Privilege | no |
| LaterRunningWrite | `Add-Content ~/.gitconfig x` | found LaterRunningWrite | found LaterRunningWrite | found LaterRunningWrite | no |
| LaterRunningWrite | `Set-Content -Path ~/.gitconfig -Value x` | found LaterRunningWrite | found LaterRunningWrite | found LaterRunningWrite | no |
| LaterRunningWrite | `Out-File -FilePath ~/.config/git/config` | found LaterRunningWrite | found LaterRunningWrite | found LaterRunningWrite | no |
| LaterRunningWrite | `cp a ~/.local/bin/a` | found LaterRunningWrite | found LaterRunningWrite | found LaterRunningWrite | no |
| LaterRunningWrite | `New-Item ~/Library/LaunchAgents/x.plist` | found LaterRunningWrite | found LaterRunningWrite | found LaterRunningWrite | no |
| LaterRunningWrite | `Set-Content .git/config x` | found LaterRunningWrite | found LaterRunningWrite | found LaterRunningWrite | no |
| LaterRunningWrite | `echo x > .git/config` | found LaterRunningWrite | found LaterRunningWrite | found LaterRunningWrite | no |
| AgentProgramWord | `claude -p hi` | found AgentProgramWord | found AgentProgramWord | found AgentProgramWord | no |
| AgentProgramWord | `claude.exe -p hi` | ALLOWED | ask T3 | ask T3 | no |
| AgentProgramWord | `& claude.exe -p hi` | ALLOWED | ask T3 | ask T3 | no |
| AgentProgramWord | `& "claude" -p hi` | found AgentProgramWord | found AgentProgramWord | found AgentProgramWord | no |
| AgentProgramWord | `claude.cmd -p hi` | ALLOWED | ask T3 | ask T3 | no |
| AgentProgramWord | `Start-Process claude` | found AgentProgramWord | found AgentProgramWord | found AgentProgramWord | no |
| AgentProgramWord | `iex "claude -p hi"` | found AgentProgramWord | found AgentProgramWord | found AgentProgramWord | no |
| AgentProgramWord | `npx @anthropic-ai/claude-code` | ALLOWED | ask T3 | ask T3 | no |
| AgentProgramWord | `coagentd ctl x` | found AgentProgramWord | found AgentProgramWord | found AgentProgramWord | no |
| AgentProgramWord | `coagent.exe open` | ALLOWED | ask T3 | ask T3 | no |
| GateFileRead | `Get-Content ~/.claude.json` | deny (coagent: never allowed in a linked session (Claude Code user) | deny (coagent: never allowed in a linked session (Claude Code user) | deny (coagent: never allowed in a linked session (Claude Code user) | no |
| GateFileRead | `cat ~/.claude/settings.json` | deny (coagent: never allowed in a linked session (Claude Code user) | deny (coagent: never allowed in a linked session (Claude Code user) | deny (coagent: never allowed in a linked session (Claude Code user) | no |
| MayReadExcluded | `grep -r key .` | ALLOWED | ask T3 | ask T3 | no |
| MayReadExcluded | `Select-String -Path * -Pattern key -Recurse` | ALLOWED | ask T3 | ask T3 | no |
| MayReadExcluded | `Get-ChildItem -Recurse | Get-Content` | ALLOWED | ask T3 | ask T3 | no |
| NonWebFetch | `Invoke-WebRequest file:///etc/hosts` | ALLOWED | ask T3 | ask T3 | no |
| (none) | `npm test` | ALLOWED | ask T3 | ask T3 | no |

rows 45; Bash-found-but-other-missing: 0
