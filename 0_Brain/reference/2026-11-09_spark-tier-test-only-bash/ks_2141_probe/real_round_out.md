```diff
--- a/Blockchain/Dev/scripts/__tests__/ks1560_private_path_suites_link_jq.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/ks1560_private_path_suites_link_jq.test.sh
@@ -42,7 +42,7 @@
 # KS-1560 M-2 (PR #1528 gate note, mutant B): this used to be `grep -qF 'bin/jq' "$f"`, a substring anywhere in the file, so
 # deleting the real `ln -sf "$JQ_BIN" "$root/bin/jq"` line and leaving the words `bin/jq` in a comment, a string or an
 # existence test kept the census green. A line that starts with `ln` cannot be a comment, an echo or a `[ -x ... ]` test.
-links_jq() { grep -qE '^[[:space:]]*ln[[:space:]]+-[A-Za-z]*s[A-Za-z]*[[:space:]].*bin/jq["'"'"]?[[:space:]]*($|[;&|#])' "$1"; }
+links_jq() {
+    local f="$1" body="" line
+    while IFS= read -r line; do
+        body+="$line"$'\n'
+        [[ "$line" =~ \\$ ]] || break
+    done < "$f"
+    body="${body%%#*}"
+    [[ "$body" =~ (^|[[:space:]])ln([[:space:]]+--symbolic|[[:space:]]+-[A-Za-z]*s[A-Za-z]*)[[:space:]]+.*bin/jq([[:space:]]*($|[;&|)]|>|>>|2>|2>>)) ]]
+}
 
 census=""      # suites with both a jq check and a private PATH
 offenders=""   # of those, the ones with no bin/jq link
@@ -100,6 +100,7 @@
 printf '%s\n' 'ln -sf "$DOCKER_BIN" "$root/bin/docker"   # jq is checked on the outer PATH' > "$FX/other_binary.sh"
 check "CONTROL linking some other binary is NOT a link of jq" "no" "$(verdict "$FX/other_binary.sh")"
 
+# Respellings of the real statement that must still count, so the stricter predicate does not turn a fine suite red.
+accepted=0; total=0
+while IFS= read -r line; do
+    total=$((total + 1)); printf '%s\n' "$line" > "$FX/spelling.sh"
+    [[ "$(verdict "$FX/spelling.sh")" == "yes" ]] && accepted=$((accepted + 1))
+done <<'SPELLINGS'
+ln -sf "$JQ_BIN" "$root/bin/jq"
+	ln -sfn "$JQ_BIN" "$root/bin/jq"
+  ln -fs $JQ_BIN $root/bin/jq
+ln -s "$JQ_BIN" "$root/bin/jq" || exit 2
+ln -sf "$JQ_BIN" "$root/bin/jq"   # the F-4 fix
+SPELLINGS
+check "CONTROL every harmless respelling of the link statement still counts ($total spellings)" "$total" "$accepted"
+
+# --- F-2078-1: legitimate spellings must be judged a link ---------------------
+accepted=0; total=0
+while IFS= read -r line; do
+    total=$((total + 1)); printf '%s\n' "$line" > "$FX/spelling.sh"
+    [[ "$(verdict "$FX/spelling.sh")" == "yes" ]] && accepted=$((accepted + 1))
+done <<'SPELLINGS'
+ln -sf "$JQ_BIN" "$root/bin/jq" 2>/dev/null
+ln -sf "$JQ_BIN" "$root/bin/jq" >/dev/null
+mkdir -p "$root/bin" && ln -sf "$JQ_BIN" "$root/bin/jq"
+if ! ln -sf "$JQ_BIN" "$root/bin/jq"; then exit 1; fi
+( ln -sf "$JQ_BIN" "$root/bin/jq" )
+command ln -sf "$JQ_BIN" "$root/bin/jq"
+ln --symbolic --force "$JQ_BIN" "$root/bin/jq"
+SPELLINGS
+check "F-2078-1 every legitimate respelling of the link statement is judged a link (7 spellings)" "$total" "$accepted"
+
+# --- F-2078-1: a backslash-continued ln -sf is judged a link ------------------
+printf '%s\n' 'ln -sf \' '  "$JQ_BIN" "$root/bin/jq"' > "$FX/backslash.sh"
+check "F-2078-1 a backslash-continued ln -sf is judged a link" "yes" "$(verdict "$FX/backslash.sh")"
+
+# --- F-2078-2: a trailing comment or word naming bin/jq on another statement is NOT a link ---
+accepted=0; total=0
+while IFS= read -r line; do
+    total=$((total + 1)); printf '%s\n' "$line" > "$FX/spelling.sh"
+    [[ "$(verdict "$FX/spelling.sh")" == "no" ]] && accepted=$((accepted + 1))
+done <<'SPELLINGS'
+ln -sf "$DOCKER_BIN" "$root/bin/docker"  # jq is at $root/bin/jq
+ln -sf "$DOCKER_BIN" "$root/bin/docker"; echo "$root/bin/jq"
+ln -sf "$root/bin/jq" "$stub/elsewhere" # bin/jq
+SPELLINGS
+check "F-2078-2 a trailing comment or word naming bin/jq on another statement is NOT a link (3 spellings)" "$total" "$accepted"
+
 echo ""
 echo "ks1560_private_path_suites_link_jq: ${PASS} passed, ${FAIL} failed"
 (( FAIL == 0 ))
```
