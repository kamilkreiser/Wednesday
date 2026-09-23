# FRIDAY — your laptop seat

Friday is the agent you run on the **laptop**. She is Wednesday's sister seat (same persona, same lessons), works
**both Secuura and Datasec**, and talks to you on the **FRIDAY tab** of the live board. Wednesday (Studio) and
Tuesday (Mac mini) keep running as they are.

## Install (once, about 10 minutes)

1. Unzip `Friday_Installer_2026-09-23.zip` in **Downloads** (double-click it). You get a folder with
   `Install_Friday.command`, this README and a `friday-seat` folder (Friday's live-board certificate).

2. Open **Terminal** and paste this line (it works even if macOS blocks a double-click on a downloaded script):

   ```
   bash ~/Downloads/Friday_Installer_2026-09-23/Install_Friday.command
   ```

3. It asks **where to put the FRIDAY folder**. Press Enter for the suggestion (your workspace drive if it is
   plugged in, otherwise your home folder).

4. A browser opens to **sign in to GitHub** — use **kamilkreiser** (the account that owns the Wednesday repo).
   This login is kept inside the FRIDAY folder and does not change any other GitHub login on the laptop.

5. It downloads Friday and starts **first-time setup**, which asks, one at a time (every step can be skipped
   and re-run later):
   - the **workspace** folder that holds `!CODING` and `Notes (MASTER)`;
   - the **AgentMail key** (from `Notes (MASTER)/Access/Agent Mail.md`) — hidden while you paste;
   - the **Linear key** for Wednesday's task board (optional);
   - optional **client GitHub logins** — Secuura's and Datasec's, each stored in its own folder.

6. Claude opens. The **first time only**, type `/login` and sign in. That login belongs to Friday alone.

7. After setup you may delete the zip from Downloads — the certificate is now inside `FRIDAY/4_Credentials/`.

## Every day after that

Double-click **`FRIDAY/Launch_Friday.command`**. Talk to her on the **FRIDAY** tab of the live board.

## How she keeps the two clients apart

- Each client's logins live in their own folder (`FRIDAY/4_Credentials/clients/secuura/` and `…/datasec/`), and
  Friday loads **one client at a time** (`2_Project_Files/friday/friday_as.sh`).
- Every brief, mail, card and message she writes is about **one** client.
- Before she drives a project she **claims** it, so she never works a project Wednesday or Tuesday is already on.
- Her live-board tab is private to her and you; Wednesday and Tuesday cannot read it.

## If something goes wrong

- Setup stopped part-way: double-click `Launch_Friday.command` again — it resumes.
- Re-run one step: `bash FRIDAY/2_Project_Files/friday/first_run.sh`.
- Nothing in the installer or this folder contains a password; the only secret that travelled is the certificate,
  which came to you encrypted through your file drawer.
