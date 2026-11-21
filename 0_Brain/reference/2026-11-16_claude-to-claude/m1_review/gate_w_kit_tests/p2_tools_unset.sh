#!/bin/bash
# QA-W-KIT probe 5b: COAGENT_TOOLS unset / empty, in an isolated copy of the two scripts whose ancestors hold no tools folder.
I=/private/tmp/claude-501/qwk_iso
ls -d /tools /target /windows-out /private/tmp/claude-501/tools 2>&1 | sed 's/^/before: /'
find $I | sort > $I/../qwk_iso_before.txt
echo "== unset"; env -u COAGENT_TOOLS -u CARGO_TARGET_DIR -u XWIN_CACHE_DIR PATH=/usr/bin:/bin bash $I/repo/scripts/windows/build.sh </dev/null; echo "exit=$?"
echo "== empty string"; env COAGENT_TOOLS= PATH=/usr/bin:/bin bash $I/repo/scripts/windows/build.sh </dev/null; echo "exit=$?"
echo "== empty string, ambient PATH with the project's cargo but no kit"; env COAGENT_TOOLS= PATH="/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/tools/cargo/bin:/usr/bin:/bin" bash $I/repo/scripts/windows/build.sh </dev/null; echo "exit=$?"
find $I | sort | diff $I/../qwk_iso_before.txt - && echo "NOTHING WRITTEN under isolated tree"
ls -d /tools /target /windows-out /private/tmp/claude-501/tools 2>&1 | sed 's/^/after: /'
