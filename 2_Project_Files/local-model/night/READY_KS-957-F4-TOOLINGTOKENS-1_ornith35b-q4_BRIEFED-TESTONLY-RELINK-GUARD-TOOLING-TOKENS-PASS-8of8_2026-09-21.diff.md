# READY — KS-957-F4-TOOLINGTOKENS-1 (Ornith, briefed, test_only, new · bash) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks957-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 06:37 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks957-ornith35b-night/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_round25-drafter-precheck/KS-957/out.md.checker/patch.diff` rc 0, the morning Wednesday seat).

**Held 06:37 2026-09-21 by the morning Wednesday seat after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks957-ornith35b-night/out.md.checker`, not typed).** Tip `362e51fe0db7e73d5557924902763fe3f10fd8c7`. Touches ONE file: `Blockchain/Dev/scripts/__tests__/check_shared_relink_tooling_tokens.test.sh` (new). `+` lines 74 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 6/6 cells. Tampers (3), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `NPMGONE` → red exactly ['KS-957 F4 npm']
- `TOOLINGTOKENSGONE` → red exactly ['KS-957 F4 npm', 'KS-957 F4 pnpm', 'KS-957 F4 yarn']
- `YARNGONE` → red exactly ['KS-957 F4 yarn']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks957-ornith35b-night/input.json`. Brief: `night/briefs/KS-957-F4-TOOLINGTOKENS-1.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks957-ornith35b-night/checker.out`.

```diff
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/check_shared_relink_tooling_tokens.test.sh
@@ -0,0 +1,74 @@
+#!/usr/bin/env bash
+# Unit tests for check-shared-relink.sh -- KS-957 F4: each tooling TOKEN of the nodeish clause is red-proofed.
+#
+# The exemption arm reads a final stage that writes no node_modules and denies it when any line names a JS
+# runtime or its tooling. The tooling clause is `if (L ~ /node_modules|npm|npx|yarn|pnpm/)`. The KS-930 round-2
+# gate's tamper T9 deleted `npm|yarn|pnpm` from it and the main suite stayed GREEN: its cells name npx, a
+# node_modules path, or a runtime word the word-arm (`node|nodejs|bun|deno`) catches on its own, so no cell
+# depended on npm, yarn or pnpm. Round 3 red-proofed only the npx token it added.
+#
+# Each red cell here is a final stage on a non-JS base that names ONE tooling token in its CMD and nothing
+# else nodeish: no node_modules write, no runtime word, no unclassified line. So the verdict is the exemption
+# arm's, and that one token is the only thing between DENIED (rc 1) and EXEMPT (rc 0).
+#
+# Every cell prints `ok <desc>` or `FAIL <desc>` so a reader can see each verdict, not only the tally.
+set -uo pipefail
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+GATE="$(cd "$HERE/.." && pwd)/check-shared-relink.sh"
+PASS=0; FAIL=0
+TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
+ok()  { PASS=$((PASS+1)); echo "  ok   $1"; }
+bad() { FAIL=$((FAIL+1)); echo "  FAIL $1"; echo "       $2"; }
+NODEISH_MSG="names a JavaScript runtime or its tooling"
+EXEMPT_MSG="the re-link invariant does not apply"
+NO_RELINK_MSG="final stage has NO"
+# final_stage <name> <expected_rc> <final stage lines> <expected substring>
+# The builder stages are the main suite's row_case preamble; the trailing COPY --from=shared-builder line puts the
+# file in the guard's class and closes the final stage, exactly as row_case does.
+final_stage() {
+    local name="$1" want="$2" body="$3" want_out="$4" d out got first
+    d=$(mktemp -d "$TMP/case.XXXXXX")
+    mkdir -p "$d/services/thing"
+    echo "FROM node:24-alpine AS shared-builder
+WORKDIR /shared
+RUN npm ci --ignore-scripts
+FROM node:24-alpine AS builder
+WORKDIR /app
+RUN npm ci && npm run build
+$body
+COPY --from=shared-builder /shared /shared" > "$d/services/thing/Dockerfile"
+    out=$(bash "$GATE" "$d" 2>&1); got=$?
+    first=$(printf '%s' "$out" | grep -m1 '::' | cut -c1-220)
+    if [ "$got" != "$want" ]; then
+        bad "$name" "expected exit $want, got $got: $first"; return
+    fi
+    if ! printf '%s' "$out" | grep -qF -- "$want_out"; then
+        bad "$name" "exit correct, WRONG rule fired (wanted /$want_out/): $first"; return
+    fi
+    ok "$name (rc=$got)"
+}
+echo "check_shared_relink_tooling_tokens:"
+# --- the three tokens T9 deleted, one cell each, nothing else nodeish in the stage -----------------------
+final_stage "KS-957 F4 npm: CMD [npm, start] in a final alpine stage is DENIED by the tooling clause" 1 'FROM alpine:3.20
+COPY --from=builder /app /app
+CMD ["npm", "start"]' "$NODEISH_MSG"
+final_stage "KS-957 F4 yarn: CMD [yarn, start] in a final alpine stage is DENIED by the tooling clause" 1 'FROM alpine:3.20
+COPY --from=builder /app /app
+CMD ["yarn", "start"]' "$NODEISH_MSG"
+final_stage "KS-957 F4 pnpm: CMD [pnpm, start] in a final alpine stage is DENIED by the tooling clause" 1 'FROM alpine:3.20
+COPY --from=builder /app /app
+CMD ["pnpm", "start"]' "$NODEISH_MSG"
+# --- controls: the same stage shape judged by the OTHER clauses, so a red above is the token and nothing else ---
+final_stage "CONTROL npx: CMD [npx, tsx, ...] is DENIED (round 3's own red-proof, the token T9 kept)" 1 'FROM alpine:3.20
+COPY --from=builder /app /app
+CMD ["npx", "tsx", "/app/src/index.ts"]' "$NODEISH_MSG"
+final_stage "CONTROL none: the same stage with CMD [/bin/sh] is EXEMPT (no tooling token anywhere)" 0 'FROM alpine:3.20
+COPY --from=builder /app /app
+CMD ["/bin/sh"]' "$EXEMPT_MSG"
+final_stage "CONTROL install verb: RUN npm run build is a node_modules write, so clause A judges it, not the exemption" 1 'FROM alpine:3.20
+COPY --from=builder /app /app
+RUN npm run build
+CMD ["/bin/sh"]' "$NO_RELINK_MSG"
+echo "  $PASS passed, $FAIL failed"
+[ "$FAIL" -eq 0 ] || exit 1
+exit 0
```
