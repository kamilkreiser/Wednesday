@echo off
setlocal
title Friday - Windows checking seat
rem ============================================================================
rem  Launch_Friday_Windows.cmd
rem  Starts a small Claude Code session ("Friday, Windows checking seat") on this
rem  Windows machine so it can look at the machine and say what is missing.
rem  cmd.exe only. No PowerShell script. No keys, logins or secrets in this file.
rem  Written on a Mac on 2026-11-20 and NOT yet run on Windows: if a step fails,
rem  copy the text in this window to Friday's panel.
rem ============================================================================

rem ---- settings you may change ------------------------------------------------
set "FRIDAY_MODEL=claude-opus-5-5"
set "FRIDAY_WORK=%USERPROFILE%\Friday-Windows"
rem -----------------------------------------------------------------------------

echo.
echo  Friday - Windows checking seat
echo  Work folder: %FRIDAY_WORK%
echo  Model:       %FRIDAY_MODEL%
echo.

if not exist "%FRIDAY_WORK%" mkdir "%FRIDAY_WORK%"
if not exist "%FRIDAY_WORK%" goto :nowork

rem ---- find Claude Code -------------------------------------------------------
set "CLAUDE_EXE="
if exist "%USERPROFILE%\.local\bin\claude.exe" set "CLAUDE_EXE=%USERPROFILE%\.local\bin\claude.exe"
if defined CLAUDE_EXE goto :haveclaude
where claude >nul 2>nul
if not errorlevel 1 set "CLAUDE_EXE=claude"
if defined CLAUDE_EXE goto :haveclaude

echo  Claude Code is not installed on this machine yet.
echo  The official installer for cmd is this one line:
echo.
echo    curl -fsSL https://claude.ai/install.cmd -o install.cmd ^&^& install.cmd ^&^& del install.cmd
echo.
echo  It needs no Administrator rights and installs to %USERPROFILE%\.local\bin
echo.
choice /c YN /m "  Run that installer now"
if errorlevel 2 goto :noinstall
pushd "%TEMP%"
curl -fsSL https://claude.ai/install.cmd -o install.cmd
if errorlevel 1 goto :dlfail
call install.cmd
del install.cmd 2>nul
popd
if exist "%USERPROFILE%\.local\bin\claude.exe" set "CLAUDE_EXE=%USERPROFILE%\.local\bin\claude.exe"
if not defined CLAUDE_EXE goto :installfail

:haveclaude
echo  Claude Code: %CLAUDE_EXE%
call "%CLAUDE_EXE%" --version
echo.

rem ---- Git for Windows is optional (recommended) ------------------------------
where git >nul 2>nul
if errorlevel 1 goto :nogit
echo  Git for Windows: found.
goto :gitdone
:nogit
echo  Note: Git for Windows was not found. That is fine for the check:
echo  Claude Code will run commands through PowerShell instead of Git Bash.
:gitdone
echo.

rem ---- write the seat's brief (the lines of this file that start with ::B) ----
set "BRIEF=%FRIDAY_WORK%\FRIDAY-WINDOWS-BRIEF.txt"
if exist "%BRIEF%" del "%BRIEF%"
for /f "tokens=1* delims= " %%a in ('findstr /b /c:"::B" "%~f0"') do echo(%%b>>"%BRIEF%"
if not exist "%BRIEF%" goto :nobrief
echo  Brief written: %BRIEF%
echo.
echo  If this is the first run, a browser opens for the Claude login.
echo  Starting the session now. Type  /exit  to leave it.
echo.

cd /d "%FRIDAY_WORK%"
call "%CLAUDE_EXE%" --model %FRIDAY_MODEL% "You are Friday's Windows checking seat. Read the file FRIDAY-WINDOWS-BRIEF.txt in this folder, whole, and follow it."
echo.
echo  Session ended. The report, if one was written, is in:
echo    %FRIDAY_WORK%\machine-report.md
goto :end

:nowork
echo  Could not create the work folder %FRIDAY_WORK%
goto :end
:noinstall
echo  Nothing was installed. Run this launcher again when you want to go on.
goto :end
:dlfail
popd
echo  The download failed. Check the internet connection, then run this again.
goto :end
:installfail
echo  The installer ran but claude.exe is not at %USERPROFILE%\.local\bin
echo  Close this window, open a new one and run this launcher again.
goto :end
:nobrief
echo  Could not write the brief file. Copy this window's text to Friday's panel.
goto :end

:end
echo.
pause
endlocal
goto :eof

rem ============================================================================
rem  The brief. Every line that starts with ::B is copied to the brief file.
rem ============================================================================
::B FRIDAY - WINDOWS CHECKING SEAT - BRIEF
::B
::B Who you are
::B You are a small helper seat for Friday, the coordinator on the owner's laptop.
::B The owner is at this keyboard. You are not the coordinator: you have no
::B mailbox, no board and no project files here. Your whole job is to look at this
::B Windows machine, write down what you find, and help the owner set up only
::B what he agrees to.
::B
::B Why
::B The owner revived this old Windows machine. Friday's project, a tool that
::B links two people's Claude Code sessions, has never been run on Windows or on
::B Linux. This machine may become the second machine for a first real test.
::B Friday needs to know what the machine is and what it can run.
::B
::B Rules, in order of weight
::B 1. This machine is old and weak. Do nothing heavy: no builds, no large
::B    downloads, no long scans, unless the owner says yes to that exact thing.
::B 2. Look first. Part 1 below is read-only. Change nothing during Part 1.
::B 3. Install or change something only after the owner said yes to that one
::B    item at this keyboard. Ask ONE question at a time and wait.
::B 4. Never ask for, type, store or print a password, key, token or login.
::B    If a step needs a login, the owner does it himself in the browser.
::B 5. Never change firewall rules, the registry, security settings, drivers,
::B    user accounts or other people's files. If you think one is needed, say
::B    why and stop: that goes to Friday first.
::B 6. Write only inside this folder, except for an install the owner agreed to.
::B 7. Delete nothing.
::B 8. If a command fails, show the error text as it is. Do not guess a cause
::B    as if it were known. Say what you measured and what you did not.
::B
::B Part 1 - the census (read-only)
::B Find out and write to the file machine-report.md in this folder:
::B  a. Windows edition, version and build; 64-bit or not; machine name.
::B  b. Processor model, number of cores, installed memory, free memory.
::B  c. Each disk: size and free space.
::B  d. Whether virtualisation is enabled in the firmware, and whether WSL is
::B     installed (wsl --status, wsl -l -v). Do NOT install or enable WSL here.
::B  e. Which of these are installed, with their versions: git, Git Bash,
::B     PowerShell (and pwsh), winget, rustup, rustc, cargo, the MSVC build
::B     tools or Visual Studio, node, python, OpenSSH client.
::B  f. Claude Code version, and which shell its command tool uses here.
::B  g. Network: the local address on the home network, whether the network
::B     is marked Private or Public, and whether this machine answers a ping
::B     to its own address. Do not scan the network.
::B  h. Whether long paths are enabled and whether Developer Mode is on.
::B  i. The system date, time and time zone.
::B  j. Anything that failed to read, with the exact error text.
::B Put at the top of the report five short lines in plain words: what this
::B machine is, whether it looks able to run WSL 2, whether it looks able to
::B build Rust programs natively, what is missing for each, and anything odd.
::B
::B Part 2 - tell the owner
::B Show him those five lines. Then list what is missing as separate items,
::B each with what it is for, its rough download size, and whether it needs
::B Administrator rights or a restart. Do not start any of them yet.
::B
::B Part 3 - only on his word
::B For each item he says yes to: do that one item, show the result, and add
::B a line to the report saying what was installed, how, and the version.
::B Prefer winget where it exists. If an item needs a restart, say so and stop.
::B
::B Part 4 - hand back
::B Tell the owner the report is at machine-report.md in this folder and ask
::B him to send its text to Friday on his board. Friday decides the next step,
::B which is likely to be either the Windows test runs of the project or a
::B first try of the project inside WSL. Do not start either yourself.
