This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Seat W-KIT only. It answers your STOP Q1 with the owner's word. Report under "## ADDENDUM 3 (cache folder granted)" in your STATUS file.

# W-KIT — ADDENDUM 3: the one cache folder outside the project is granted

**The owner (Kam), card `general-c2c-win-kit-cache-outside-project-1120`, verbatim:** "a — Yes: one cache folder at the top of the drive". The option as shown to him: "/Volumes/Laptop-DEV/coagent-xwin-cache, cache files only (1.1 GB; 179 GB free). Everything else stays inside the project."

The ruling, exactly as granted:
1. The kit's Microsoft cache lives at `/Volumes/Laptop-DEV/coagent-xwin-cache` and nowhere else outside the project. ONLY the tool's cache goes there: `xwin-kit`, `target/windows`, `windows-out`, logs and everything else stay inside `$COAGENT_TOOLS` as your brief says.
2. Create that folder (it does not exist: Friday checked the name is free). Fill it by COPYING the 1.1 GB already in `$COAGENT_TOOLS/xwin-cache` (`cp -R`, no new download), then confirm the copy by file count and total bytes on both sides. Do not move or delete the original: leave it in place and say so (the coordinator decides later whether to quarantine it).
3. `scripts/windows/build.sh`: its default `XWIN_CACHE_DIR` becomes that exact path, written as a single constant at the top with a comment naming this addendum and the reason (the tool refuses a cache path with a space; the project folder's name has spaces). Keep your guard that refuses a path with a space. `scripts/windows/README.md` and the folder's removal command (quarantine it; it is only a cache) say the same.
4. Then carry on with your brief from section 5 item 5: the first run and the second run of `build.sh` (count with `fleet/heavy_runs.sh` below 3 before each), the header proof, the two texts, BACKLOG (add: the cache folder outside the project, granted by the owner's card, and why), the final tree.
5. In section 9 of your STATUS, under "Machine-wide installs made", list this folder as the ONE item outside the project, with its size and removal.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
