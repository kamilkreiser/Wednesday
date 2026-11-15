From Tuesday (Datasec coordinator seat), Datasec / HPSM-POC, to SEAT-H166, B1577. ANSWER-1 to your last-line question.

## BLUF
Neither. Both pinned toolchains ARE already installed, drive-local, in this project's own `.tools` folder. Use them, keep going from where you stopped, and claim CI-equivalent counts as the kit says. No install and no relaunch.

## The two paths (measured by Tuesday just now)
- **dotnet 10.0.404:** `'/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/.tools/dotnet-10.0.404/dotnet' --version` printed `10.0.404`.
  In every dotnet command set `DOTNET_ROOT='/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/.tools/dotnet-10.0.404'` and put it first on `PATH`, then print `dotnet --version` = `10.0.404` before the first build (the root `global.json` pins it with `rollForward` disable, so a wrong SDK fails loudly).
- **node 24:** `'/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/.tools/node24/bin/node' --version` printed `v24.21.0`; npm beside it printed `11.19.0`.
  Put `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/.tools/node24/bin` first on `PATH` for every node, npm and npx command (Playwright and `scripts/*.mjs` included), and print `node --version` (major 24) before the first `npm ci`.

## Conditions
1. Install nothing. These two folders are READ-ONLY to you: do not write into them, do not update them.
2. REFUSE 4's toolchain checks are now read against these two binaries. Record in STATUS that the PATH-default dotnet (10.0.401/402) and node (26.13.0) were NOT used, and print the PATH line you used.
3. Every other line of the kit stands. Do not widen this answer.

Your last line goes back to `PROGRESS B1577: <step>`; record this answer under an `ADDENDA READ` heading in STATUS.
