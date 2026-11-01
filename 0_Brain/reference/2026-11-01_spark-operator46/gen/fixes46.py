"""operator 46: spelled product edits (old, new) per task, applied to the file text at the tip."""
FIX = {
 'p1': ('Blockchain/Dev/scripts/check-dockerfile-non-root.sh', [
  ("""  last_user=$(grep -E '^[[:space:]]*USER[[:space:]]+' "$f" | tail -1 | sed -E 's/^[[:space:]]*USER[[:space:]]+//; s/[#].*$//' | tr -d '[:space:]' || true)

  if [ -z "$last_user" ]; then
""",
   """  last_user=$(grep -E '^[[:space:]]*USER[[:space:]]+' "$f" | tail -1 | sed -E 's/^[[:space:]]*USER[[:space:]]+//; s/[#].*$//' | tr -d '[:space:]' || true)

  # KS-1903: `USER root:root`, `USER 0:0` and `USER ROOT` run as root too: drop any :group, ignore case.
  last_user=${last_user%%:*}
  last_user=$(printf '%s' "$last_user" | tr 'A-Z' 'a-z')

  if [ -z "$last_user" ]; then
""")]),
 'p2': ('Blockchain/Dev/scripts/check-akto-container-names.sh', [
  ("""PATTERN+="|((\\\\?\\\\?|\\\\|\\\\|)[[:space:]]*[\\"'\\`]akto-[a-z0-9-]+[\\"'\\`])"

hits=$(
""",
   """PATTERN+="|((\\\\?\\\\?|\\\\|\\\\|)[[:space:]]*[\\"'\\`]akto-[a-z0-9-]+[\\"'\\`])"

# KS-1902: a flag that takes a SEPARATE value (-u root, -e FOO=1, --tail 5) before the name. Each flag may
# be followed by ONE value word, so the chain from the verb to the name is not broken by the value.
PATTERN+="|(docker[[:space:]]+(exec|logs|inspect|cp|kill|stop|rm|restart)([[:space:]]+-[^[:space:]]+([[:space:]]+[^-[:space:]][^[:space:]]*)?)+[[:space:]]+[\\"']?akto-[a-z0-9-]+)"

hits=$(
""")]),
 'p3': ('systemTest/__tests__/manifest_readers_agree.test.sh', [
  ("""CLEAR=(-u SECUURA_STACK_SLOT -u SECUURA_ARTIFACT_SUFFIX -u STACK_SLOT -u SECUURA_ACTOR_MANIFEST)
""",
   """CLEAR=(-u SECUURA_STACK_SLOT -u SECUURA_ARTIFACT_SUFFIX -u STACK_SLOT -u SECUURA_ACTOR_MANIFEST)

# KS-1884: each driver's stderr goes to its own file here (not /dev/null), so a FAIL can say why a driver answered nothing.
ERR_DIR="$(mktemp -d "${TMPDIR:-/tmp}/readers-agree.XXXXXX")"
trap 'rm -rf "$ERR_DIR"' EXIT
"""),
  ("""catch (e) { console.log('ERROR'); }" 2>/dev/null | tail -1 )
}
playwright() {""",
   """catch (e) { console.log('ERROR'); }" 2>"$ERR_DIR/writer" | tail -1 )
}
playwright() {"""),
  ("""manifestPathForThisSlot())); } catch (e) { console.log('ERROR'); }" 2>/dev/null | tail -1 )""",
   """manifestPathForThisSlot())); } catch (e) { console.log('ERROR'); }" 2>"$ERR_DIR/playwright" | tail -1 )"""),
  (""".catch(() => console.log('ERROR'));" 2>/dev/null | tail -1 )""",
   """.catch(() => console.log('ERROR'));" 2>"$ERR_DIR/performance" | tail -1 )"""),
  ("""    print('ERROR')" 2>/dev/null | tail -1 )""",
   """    print('ERROR')" 2>"$ERR_DIR/schemathesis" | tail -1 )"""),
  ("""performance='$f' schemathesis='$s'"
""",
   """performance='$f' schemathesis='$s'"
    for _k in writer playwright performance schemathesis; do
      [[ -s "$ERR_DIR/$_k" ]] && echo "     $_k stderr: $(head -c 400 "$ERR_DIR/$_k" | tr '\\n' ' ')"
    done
""")]),
}
