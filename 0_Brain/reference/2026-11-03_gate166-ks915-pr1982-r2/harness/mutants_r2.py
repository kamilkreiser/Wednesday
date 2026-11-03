# Gate 166 mutants on the head script: (name, old, new). Exact-string replace; a mutant that does not
# apply is reported, never silently skipped. Writes one mutated script per name to argv[2]/<name>.sh.
import sys, os
src = open(sys.argv[1]).read(); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
GREP = '< <(grep -E "^[[:space:]]*(export[[:space:]]+)?$2[[:space:]]*[=:]"'
TRAP = "trap 'if [[ -n \"$TMP_FILE\" ]]; then " + "r" + "m -f \"$TMP_FILE\"; fi' EXIT"
M = [
 # gate 165 surviving classes, re-expressed on the new code
 ("g165_mA_contains_localhost", '""|localhost|127.0.0.1|::1|postgres) return 0', '""|localhost|*localhost*|127.0.0.1|::1|postgres) return 0'),
 ("g165_mC_no_hostaddr", 'host|hostaddr) return 1', 'host) return 1'),
 ("g165_mE_schemeless_ok", '    *) return 1 ;;\n  esac\n  authority=', '    *) return 0 ;;\n  esac\n  authority='),
 ("g165_mF_no_lower_nodeenv", '[[ "$(lower "$c")" != production ]]', '[[ "$c" != production ]]'),
 ("g165_mH_no_quote_strip_candidates", '  t="${t#[\\"\\\'\\`]}"; t="${t%[\\"\\\'\\`]}"; printf \'%s\\n\' "$t"\n', ''),
 ("g165_mH2_no_dquote_effective", '    \\"*) v="${v#\\"}"; v="${v%%\\"*}" ;;\n', ''),
 ("g165_mJ_junk_after_bracket", "RE_BRACKET='^\\[([^]]*)\\](:[0-9]*)?$'", "RE_BRACKET='^\\[([^]]*)\\]'"),
 ("g165_mU_first_line_only_db", 'done < <(raw_values "$FILE_SRC" DATABASE_URL)', 'done < <(raw_values "$FILE_SRC" DATABASE_URL | head -n1)'),
 ("g165_mU_first_line_only_node", 'done < <(raw_values "$FILE_SRC" NODE_ENV)', 'done < <(raw_values "$FILE_SRC" NODE_ENV | head -n1)'),
 ("g165_mY_set_x", '\nset +x\n', '\nset -x\n'),
 ("g165_mZ_print_value", '  unset value\n', '  echo "$value"\n  unset value\n'),
 # the round-2 checks
 ("r2_no_comma_check", '  case "$host" in *,*) return 1 ;; esac\n', ''),
 ("r2_no_pct_name_check", '    case "$name" in *%*) return 1 ;; esac\n', ''),
 ("r2_query_name_case_sensitive", 'case "$(lower "$name")" in host|hostaddr', 'case "$name" in host|hostaddr'),
 ("r2_plain_unanchored", "RE_PLAIN='^([^]:[]*)(:[0-9]*)?$'", "RE_PLAIN='^([^]:[]*)'"),
 ("r2_raw_no_export", GREP, '< <(grep -E "^[[:space:]]*$2[[:space:]]*[=:]"'),
 ("r2_raw_no_leading_space", GREP, '< <(grep -E "^(export[[:space:]]+)?$2[[:space:]]*[=:]"'),
 ("r2_raw_no_space_before_eq", GREP, '< <(grep -E "^[[:space:]]*(export[[:space:]]+)?$2[=:]"'),
 ("r2_raw_no_colon", GREP, '< <(grep -E "^[[:space:]]*(export[[:space:]]+)?$2[[:space:]]*="'),
 ("r2_no_cr_strip", "    line=\"${line%$'\\r'}\"\n", ''),
 ("r2_cand_no_anyhash", '  c="${t%%#*}"; c="${c%"${c##*[![:space:]]}"}"; printf \'%s\\n\' "$c"\n', ''),
 ("r2_eff_no_inline_comment", '    *) v="${v%%[[:space:]]#*}"; v=', '    *) v='),
 ("r2_no_symlink_env", 'for f in "$ENV_FILE" "$ENV_LOCAL_FILE"; do', 'for f in "$ENV_LOCAL_FILE"; do'),
 ("r2_no_symlink_envlocal", 'for f in "$ENV_FILE" "$ENV_LOCAL_FILE"; do', 'for f in "$ENV_FILE"; do'),
 ("r2_tmpname_round1", 'mktemp "$DEV_DIR/.env-ks915.XXXXXX"', 'mktemp "$DEV_DIR/.env.ks915.XXXXXX"'),
 ("r2_setkey_canonical_only", 're = "^[ \\t]*(export[ \\t]+)?" k "[ \\t]*[=:]"', 're = "^" k "="'),
 ("r2_no_case_rewrite", 'elif [[ "$(lower "$seed")" == true ]]; then', 'elif false; then'),
 ("r2_seed_first_wins", 'while IFS= read -r raw; do seed="$(effective "$raw")"; done', 'while IFS= read -r raw; do seed="$(effective "$raw")"; break; done'),
 ("r2_no_shell_db", 'then check_db_value "$DATABASE_URL" "the shell environment"; fi', 'then :; fi'),
 ("r2_no_shell_node", 'then check_node_value "$NODE_ENV" "the shell environment"; fi', 'then :; fi'),
 ("r2_no_file_db", 'do check_db_value "$raw" "$FILE_NAME"; done < <(raw_values "$FILE_SRC" DATABASE_URL)', 'do :; done < <(raw_values "$FILE_SRC" DATABASE_URL)'),
 ("r2_no_file_node", 'do check_node_value "$raw" "$FILE_NAME"; done < <(raw_values "$FILE_SRC" NODE_ENV)', 'do :; done < <(raw_values "$FILE_SRC" NODE_ENV)'),
 ("r2_trap_removed", TRAP, ':'),
 ("r2_admin_set_first_only", 'done < <(raw_values "$ENV_FILE" ADMIN_USER_PASSWORD)', 'done < <(raw_values "$ENV_FILE" ADMIN_USER_PASSWORD | head -n1)'),
 ("r2_no_postgres_service", '::1|postgres) return 0', '::1) return 0'),
 ("r2_empty_url_refused", '[[ -z "$url" ]] && return 0', '[[ -z "$url" ]] && return 1'),
 ("r2_no_lower_host", '  case "$(lower "$1")" in\n    ""|localhost', '  case "$1" in\n    ""|localhost'),
 ("r2_refuse_exit_1", 'nothing was written." 3\n}', 'nothing was written." 1\n}'),
]
for name, old, new in M:
    n = src.count(old)
    if n != 1:
        print(f"{name}: DID-NOT-APPLY (matches={n})"); continue
    open(os.path.join(out, name + ".sh"), "w").write(src.replace(old, new))
    print(f"{name}: applied")
print("total", len(M))
