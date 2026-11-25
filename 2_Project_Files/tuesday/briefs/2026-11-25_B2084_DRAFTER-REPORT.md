STARTABLE: NO

# B2084 DRAFTER REPORT: kit SEAT-D6, two Security Manager logins (+ ADDENDUM 1: guest invites and Reader)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-25_B2084_SEAT-D6_hpsmpoc-sm-two-staff-logins.md` (sidecar `.measured`: 27 claims, 0 TODO; `stamp_check.py <kit>` rc 0; 5 four-underscore lines: 4 slots plus READ-WHOLE). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s326/d2084/`. Drafted 2026-11-25 10:59 to about 11:15 AEDT.

## BLUF
- **Why NO: the project's az session is dead.** Under `HPSM-POC/4_Credentials/.azure`, `az account show` reads the right user, tenant and subscription from its cache (10:59:57). But every token read at 11:01 failed with `AADSTS50132`: ARM `vm get-instance-view`, an ARM roleAssignments GET, Graph `/me`. The error names password expiry or a recent password change. No seat can run a run-command until Kam signs in again: `AZURE_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/4_Credentials/.azure' az login --tenant ec01829b-fdcb-4503-9834-eb2ffbd99169`. That is Kam's step; the drafter ran no `az login`. The kit's REFUSE 1 catches it, and its AZ SESSION slot is where Tuesday records the fix.
- **The second blocker is ADDENDUM 1's e-mail addresses.** They are an ADDRESSES slot. Without them the kit still makes the two logins and writes Kam's invite clicks (Step 4 B).
- **The identity is Kam's own user `kamil@datasec-rd.com`, not a service principal.** `4_Credentials/.azure-sp` says "Please run 'az login'". So the rights ADDENDUM 1 asked about (can it invite, can it assign Reader) could NOT be measured: the session is expired, which is not a 403. The kit measures them read-only at its Step 1 and branches: A, the seat invites and assigns; or B, Kam's exact click-paths. It never widens rights.
- **What the kit changes:** two local accounts (`john.spears`, `william.nichols`), each in `HPIPSC` (Administrator) and `Remote Desktop Users` and not in `Administrators`. It does this through ONE new managed run-command `b2084-users`, with the passwords as protected parameters. It takes a census of users and six groups before and after, then ASSERTs that exactly these additions happened. It checks each password on the VM with Windows `ValidateCredentials`, never through SM sign-in or HTTP. The passwords go to one 0600 file, `4_Credentials/b2084-sm-staff-initial.txt` (gitignored, measured). Tuesday then delivers that file through `chat_reply.sh --file` and quarantines it. UNDO is written (disable, then remove) and not run.

## Facts re-measured (instrument, result, control)
- Ruling: `decision_queue.sh show datasec-hpsm-sm-staff-access-1125` reads ruled, choice a, ruled_ts 2026-11-25T10:58:55. **Kam's note "John Spears, William Nichols - full access" was not in the show output** (it has no note field). The note is RELAYED from the commission only, so Tuesday re-prints it at the stamp.
- az: account show OK at 10:59:57; three token reads failed AADSTS50132 at 11:01:22 to :31; `.azure-sp` is not logged in.
- gitignore: `check-ignore -v 4_Credentials/<file>` returns `.gitignore:4:4_Credentials/` (rc 0; control `CLAUDE.md` rc 1). `.tools/b2084/...` returns `.gitignore:29:.tools/`.
- Mail key: `^AGENTMAIL_API_KEY=` count 0 (control `^JIRA_API_TOKEN=` 1). The STATUS file is therefore the seat's only channel.
- How the existing user's account was made: B106 used protected parameters (`B106_STATUS.md:134`), the password was kept in `.env`, and the handover was "by a secure channel ... Not by plain email, and never in Jira or chat" (`:141`). B106 also named this same flow for other Datasec staff (`:146`). B306 ADDENDUM-1:13 says "password: sent separately". **Which channel Kam actually used is UNMEASURED**, so nothing was there to reuse beyond protected parameters. The kit uses the board drawer as the commission says.
- Group census form: `B337_evidence/s2c-group-change.txt` and `kit/ps_10_add_paul_hpipsc.ps1` (6 groups, BEFORE/AFTER/DIFF/ASSERT). The redactor over-redacts a username, giving 4 `LEAK-REDACTED` lines.
- Hold: `tuesday/holds/HPSM-POC.hold` (until 2026-12-10). `launch_when_cool.sh:19` and `:32` show that `LWC_HOLD_OVERRIDE="<words>"` passes one launch. The kit's launch line goes through `launch_when_cool.sh` with Kam's two notes as those words.
- HPSM-POC CLAUDE.md, grepped for VM, run-command, account, deploy and hold: **no rule on any of them**. The rules that apply are "Secrets: 4_Credentials + 3_Access_Keys only, never in notes/Jira/committed" and "Nothing goes to HP without Kam's send".
- Microsoft Learn (web reader): Bastion RDP needs Reader on the VM, its NIC and the Bastion resource, plus the VNet only when peered. A non-admin user must be in Remote Desktop Users. The Developer quickstart lists only the VM and NIC. **No page mentions a forced password change or NLA.**
- Records repo `datasecau/HPSM-POC-analysis` main is `13d5ab45` (gh api -X GET). Its highest entry is C-393. C-125 (line 1911) is the form: Kam's words as `> ` blocks, with account names written in full.
- Prior work: no `B2084` file in HPSM-POC Briefs (count 0; control: `B337` count 3). No STATUS file or history file names either person (control: the existing user's name matches at least 2 STATUS files). No HPSM-POC process is running (`pgrep -fl -i hpsm-poc` empty at 11:05).

## D-decisions (the drafter's; Tuesday can overrule)
- D1: the C-entry is written as text in STATUS and filed by Tuesday's records seat. The seat itself does no git work (B337 precedent).
- D2: the passwords are 20 characters from A-Z, a-z and 0-9, following the B106 SendKeys lesson (`:114`).
- D3: the run-command `b2084-users` is left in place, not deleted (never-delete; B337 FOR TUESDAY 4 form).
- D4: the proof is Windows `ValidateCredentials` plus group membership. The SM role is inferred from B337's measured `HPIPSC` = Administrator. The seat does no SM sign-in and makes no HTTP call.
- D5: model row C6 (line 96) and C4 (line 94): Opus, `claude-opus-5-5`. Pane `Datasec/HPSM-POC-D6`; no port.

## Questions for Tuesday (each with a default)
- **Q-1 "Must change at next logon"? Default: NOT set.** SM's sign-in and Bastion RDP with NLA both authenticate before a session exists. So the forced change is PREDICTED to block the first sign-in on both paths, with no screen where the person could change the password (UNMEASURED; the docs are silent). Instead, the sign-in note asks each person to change it themselves (Ctrl+Alt+End). Alternative: set it only if Step 2 reads NLA (`UserAuthentication`) = 0. Turning NLA off is NOT proposed.
- **Q-2 Account names `john.spears` and `william.nichols`? Default: yes**, in the `paul.waite` form.
- **Q-3 Invites and Reader. Default: the seat does them only if Step 1 positively reads CAN INVITE and CAN ASSIGN READER, and the addresses are stamped. Otherwise Step 4 B: Kam's clicks.** The invite is an e-mail sent under Kam's identity on his own words, "Invite them ... please set them up". If Tuesday wants Kam to send it himself regardless, answer "B".
- **Q-4 Reader scope. Default: resource group `hpsm-poc-sm-rg`**, as Kam's card proposed and as done for the existing user. The tighter alternative is three assignments: VM, NIC and Bastion. Reader on the RG also shows them the unrelated `swa-hpsmpoc-fta-review` and the budget.
- **Q-5 Records. Default: a C-entry text in STATUS for the records seat.** The alternative is that the seat pushes `records/b2084` itself.
- **Q-6 Names in the kit.** DRAFTER_RULES rule 7 says no person's name in kit text that the seat copies. The account names and Kam's quote must contain names, and the seat writes no commit, comment or Jira. **Default: keep them.** The launch line's override words also carry "Kam" and both names.

## UNMEASURED
Today's VM power state. Whether either account already exists on the VM. NLA's value. Kam's directory role, the tenant's `allowInvitesFrom`, and his RBAC rights today (the B106 record says Owner on the subscription, `B106_STATUS.md:78`, but that is RELAYED from 2026-10-03). Whether guests face MFA or Conditional Access. Whether a forced change blocks Bastion. The channel used for the existing user's password.

## FOR TUESDAY (not in the commission's scope, no action taken)
- Bastion Developer allows one RDP session at a time (`B106_STATUS.md:105`), and four people will now share it.
- Port 7637 is open to the internet with SM's sign-in as the only gate (C-125). These two new Administrator logins can be reached through it, as the existing ones can.

## Outside-the-fences disclosure
1. **The STANDING HOLD was touched by grep.** My first grep (`-rn` over `1_Project_Definition`, `--include='*.md'`) matched lines in two `Source_Documents/2026-10-16_*_REDACTED.md` files: e-mail header lines with HP staff names and addresses. I did not open them, and nothing from them is in the kit. Every later grep was scoped.
2. I printed the decision card to the pane with `decision_queue.sh show <exact id>`, as the commission said. That skipped the rules' "scratch file through an inclusion filter" step.
3. One web-reader sub-agent read three public Microsoft Learn pages. It sent no project data.
4. Writes: this report, the kit, its `.measured`, and the scratch folder `fleet/state/s326/d2084/`. The scratch holds a 2.2 MB GET of the records CLARIFICATIONS (`clar_main.md`), a Briefs listing, and the first `.measured` from `--init` (moved there so it could be re-initialised after two kit wording edits; nothing deleted).
5. No az write, run-command, `az login`, Jira, mail or HTTP to any host.
