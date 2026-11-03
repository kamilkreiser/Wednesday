# Gate 173 mutants of the head script. Each (id, direction, old, new) must apply EXACTLY once.
import pathlib
W = pathlib.Path("/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate173-ks915-pr1989")
src = (W / "repo/Blockchain/Dev/scripts/restore-local-secrets.sh").read_text()
M = [
 ("m01_no_dotenv_reader", "permissive", '[[ ${#files[@]} -gt 0 ]] && read_dotenv "${files[@]}"', 'true'),
 ("m02_no_bash_reader", "permissive", 'for f in ${files[@]+"${files[@]}"}; do read_bash "$f"; done', ':'),
 ("m03_no_root_compose", "permissive", 'read_compose root; ROOT_READ="read"', 'ROOT_READ="read"'),
 ("m04_no_canonical_files", "permissive", 'for f in ${files[@]+"${files[@]}"}; do canonical_file "$f"; done', ':'),
 ("m05_no_canonical_shell", "permissive", '  canonical_shell\n}', '  :\n}'),
 ("m06_shell_judge_ignored", "permissive", '"REFUSE "*) refuse "pg-connection-string (node pg\'s URL reader)"', '"REFUSE "*) : "pg-connection-string (node pg\'s URL reader)"'),
 ("m07_nodeenv_no_trim_lower", "permissive", 'String(env.NODE_ENV).trim().toLowerCase() === "production"', 'String(env.NODE_ENV) === "production"'),
 ("m08_judge_no_pghostaddr", "permissive", 'if (set(env.PGHOSTADDR)) return', 'if (false) return'),
 ("m09_judge_no_pgservice", "permissive", 'if (set(env.PGSERVICE)) return', 'if (false) return'),
 ("m10_judge_no_pghost", "permissive", 'if (set(env.PGHOST) && !hostLocal(env.PGHOST)) return', 'if (false) return'),
 ("m11_judge_no_hostaddr_param", "permissive", 'if (set(c.hostaddr)) return', 'if (false) return'),
 ("m12_judge_no_service_param", "permissive", 'if (set(c.service)) return', 'if (false) return'),
 ("m13_localhost_substring", "permissive", '|| LOCAL.has(String(h).toLowerCase());', '|| LOCAL.has(String(h).toLowerCase()) || String(h).toLowerCase().includes("localhost");'),
 ("m14_dotenv_first_file_only", "permissive", 'for (const f of files) {\n    const why', 'for (const f of files.slice(0, 1)) {\n    const why'),
 ("m15_compose_first_service_only", "permissive", 'if (why) { console.log("REFUSE " + why + " for the " + name + " service"); return; }', 'if (why) { console.log("REFUSE " + why + " for the " + name + " service"); return; } break;'),
 ("m16_bash_first_marker", "permissive", 'f.lastIndexOf("@@RLS-KS915@@")', 'f.indexOf("@@RLS-KS915@@")'),
 ("m17_bash_no_set_r", "permissive", 'exit 90; set -r; set -a;', 'exit 90; set -a;'),
 ("m18_bash_real_path", "permissive", 'PATH="$sb/empty" HOME="$sb"', 'HOME="$sb"'),
 ("m19_bash_no_parse_check", "permissive", 'if ! env -u BASH_ENV -u ENV -u SHELLOPTS -u BASHOPTS -u PS4 "${CALLER_LOCALE[@]}" "$BASH" --norc --noprofile -n', 'if false && env -u BASH_ENV -u ENV -u SHELLOPTS -u BASHOPTS -u PS4 "${CALLER_LOCALE[@]}" "$BASH" --norc --noprofile -n'),
 ("m20_bash_noresult_failopen", "permissive", '*) cannot "bash set -a gave no reading of $(label_of "$f")" ;;', '*) return 0 ;;'),
 ("m21_compose_noverdict_failopen", "permissive", '*) cannot "$name gave no verdict" ;;', '*) return 0 ;;'),
 ("m22_compose_rc_ignored", "permissive", '[[ "$rc" -eq 0 ]] || cannot "$name exited $rc', '[[ "$rc" -eq 0 ]] || true "$name exited $rc'),
 ("m23_compose_noservices_ok", "permissive", 'console.log("ERROR no-services"); return;', 'console.log("OK"); return;'),
 ("m24_node_missing_ok", "permissive", 'command -v node >/dev/null 2>&1 || cannot', 'command -v node >/dev/null 2>&1 || true'),
 ("m25_dotenv_missing_ok", "permissive", 'MISSING) cannot "the dotenv library this repo loads is not installed; run npm ci in Blockchain/Dev" ;;', 'MISSING) return 0 ;;'),
 ("m26_docker_missing_ok", "permissive", 'command -v docker >/dev/null 2>&1 || cannot', 'command -v docker >/dev/null 2>&1 || true'),
 ("m27_reline_allows_dollar", "permissive", '([^[:space:]#$"`', '([^[:space:]#"`'),
 ("m28_canon_nodeenv_any_case", "permissive", '*NODE_ENV*) [[ "$v" =~ ^[a-z]*$ && "$v" != production ]] ;;', '*NODE_ENV*) [[ "$v" != production ]] ;;'),
 ("m29_canon_no_query_check", "permissive", 'for p in "${params[@]}"; do case "${p%%=*}" in host|hostaddr|service) return 1 ;; esac; done', ':'),
 ("m30_canon_no_cr_split", "permissive", "done < <(tr '\\r' '\\n' < \"$f\")", 'done < "$f"'),
 ("m31_canon_no_nul_check", "permissive", '|| refuse "the canonical-line check" "$(label_of "$f") contains a NUL byte"', '|| true'),
 ("m32_no_recheck_after_bootstrap", "permissive", 'check_links\ncheck_all\ncase "$COMPOSE_FACTS"', 'check_links\nread_compose dev\ncase "$COMPOSE_FACTS"'),
 ("m33_no_canon_on_tmp", "permissive", '  canonical_file "$TMP_FILE"\n', '  :\n'),
 ("m34_no_admin_match_compose", "permissive", 'if [[ "$WRITE_ADMIN" -eq 1 && "$COMPOSE_FACTS" != *"ADMIN_MATCH yes"* ]]; then', 'if false; then'),
 ("m35_no_admin_match_dotenv", "permissive", 'if [[ "$WRITE_ADMIN" -eq 1 && "$DOTENV_FACTS" != *"ADMIN_MATCH yes"* ]]; then', 'if false; then'),
 ("m36_no_allow_match", "permissive", 'if [[ "$WRITE_ALLOW" -eq 1 && "$COMPOSE_FACTS" != *"ALLOW exact-true"* ]]; then', 'if false; then'),
 ("m37_no_hardlink_check", "permissive", 'if [[ -f "$f" && "$(links_of "$f")" != 1 ]]; then', 'if false; then'),
 ("m38_no_symlink_check", "permissive", '    if [[ -L "$f" ]]; then\n      die "refused: $(label_of "$f") is a symbolic link', '    if false; then\n      die "refused: $(label_of "$f") is a symbolic link'),
 ("m39_rewrite_keeps_later_dups", "other", '{ if (!done[i]) { print k[i] "=" v[i]; done[i] = 1 }; next }', '{ if (!done[i]) { print k[i] "=" v[i]; done[i] = 1; next } }'),
 ("m40_no_trap", "other", "trap 'if [[ -n \"$TMP_FILE\" ]]; then rm -f \"$TMP_FILE\"; fi' EXIT", ':'),
 ("m41_tmp_not_ignored", "other", 'mktemp "$DEV_DIR/.env-ks915.XXXXXX"', 'mktemp "$DEV_DIR/.env.ks915.XXXXXX"'),
 ("m42_bootstrap_keeps_bash_env", "other", 'env -u BASH_ENV -u ENV -u SHELLOPTS -u BASHOPTS -u PS4 "${CALLER_LOCALE[@]}" "$BASH" "$SCRIPT_DIR/bootstrap-env.sh"', 'env "${CALLER_LOCALE[@]}" "$BASH" "$SCRIPT_DIR/bootstrap-env.sh"'),
 ("m43_case_true_not_rewritten", "other", 'case "$ALLOW_STATE" in blank|case-true) WRITE_ALLOW=1 ;; esac', 'case "$ALLOW_STATE" in blank) WRITE_ALLOW=1 ;; esac'),
 ("m44_always_regenerate", "other", 'if [[ "$ADMIN_STATE" == blank || "$ROTATE" -eq 1 ]]; then WRITE_ADMIN=1; fi', 'WRITE_ADMIN=1'),
 ("m45_no_root_env_file", "permissive", '  [[ -f "$ROOT_ENV_FILE" ]] && echo "$ROOT_ENV_FILE"\n', ''),
 ("m46_no_envlocal_file", "permissive", '  [[ -f "$ENV_LOCAL_FILE" ]] && echo "$ENV_LOCAL_FILE"\n', ''),
 ("m47_no_locale_c", "permissive", 'export LC_ALL=C\n', ''),
 ("m48_no_chmod_env", "other", 'chmod 600 "$ENV_FILE"\nsay', 'say'),
 ("m49_print_value", "leak", 'say "generated ADMIN_USER_PASSWORD (${#value} characters) in Blockchain/Dev/.env"', 'say "generated ADMIN_USER_PASSWORD (${value} characters) in Blockchain/Dev/.env"'),
 ("m50_compose_env_not_map_ok", "permissive", 'console.log("ERROR environment-not-a-map " + name); return;', 'continue;'),
]
ok = 0
for mid, d, old, new in M:
    n = src.count(old)
    if n != 1:
        print(f"{mid}\tNOT-APPLIED count={n}"); continue
    (W / "mut" / f"{mid}.sh").write_text(src.replace(old, new)); ok += 1
    print(f"{mid}\t{d}\tapplied")
print("applied", ok, "of", len(M))
