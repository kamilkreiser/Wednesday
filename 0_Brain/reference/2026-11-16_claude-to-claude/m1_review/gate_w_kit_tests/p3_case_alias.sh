#!/bin/bash
# QA-W-KIT probe 5c: add_case_aliases (the function text extracted from build.sh at the head) on a fake cache.
W=/private/tmp/claude-501/qwk
F=${QWK_FAKE:-$W/hostile/fakecache}
mkdir -p "$F/xwin/crt/lib/x86_64" "$F/xwin/sdk/lib/um/x86_64" "$F/xwin/sdk/lib/sp ace" ${QWK_LOGS:-$W/hostile/fakelogs}
printf 'ORIGINAL-LOWER' > "$F/xwin/crt/lib/x86_64/kernel32.lib"        # lower-case name already exists, different content
printf 'MIXED' > "$F/xwin/crt/lib/x86_64/Kernel32.Lib"
printf 'MIXED2' > "$F/xwin/sdk/lib/um/x86_64/Advapi32.Lib"             # no lower-case yet -> link expected
printf 'MIXED3' > "$F/xwin/sdk/lib/sp ace/Ws2 32.Lib"                  # space in the name
ln -s /nonexistent-target "$F/xwin/sdk/lib/um/x86_64/userenv.lib"     # dangling link already at the lower-case name
printf 'MIXED4' > "$F/xwin/sdk/lib/um/x86_64/Userenv.Lib"
printf 'already' > "$F/xwin/sdk/lib/um/x86_64/dbghelp.lib"             # lower-case only, no mixed
find "$F" -exec stat -f '%N|%HT|%z|%i|%Y' {} + | sort > ${QWK_LOGS:-$W/hostile}/fc_before.txt
shasum -a 256 "$F/xwin/crt/lib/x86_64/kernel32.lib" > ${QWK_LOGS:-$W/hostile}/fc_kernel_before.txt
XWIN_CACHE_DIR=$F; LOGS=${QWK_LOGS:-$W/hostile/fakelogs}
eval "$(sed -n '/^add_case_aliases() {/,/^}/p' $W/clone/scripts/windows/build.sh)"
add_case_aliases
echo "--- after"; find "$F" -exec stat -f '%N|%HT|%z|%i|%Y' {} + | sort | diff ${QWK_LOGS:-$W/hostile}/fc_before.txt - | sed "s#$F#F#g"
shasum -a 256 -c ${QWK_LOGS:-$W/hostile}/fc_kernel_before.txt
echo "--- second call (idempotent?)"; add_case_aliases
cat $LOGS/case_aliases.list | sed "s#$F#F#g"
