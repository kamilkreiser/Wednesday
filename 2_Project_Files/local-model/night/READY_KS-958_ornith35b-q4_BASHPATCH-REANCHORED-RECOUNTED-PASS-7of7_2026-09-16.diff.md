# READY — KS-958 (check-shared-relink.sh: the classifier's two runtime-name tests at :338 and :342 match `tolower(L)` — every UPPERCASE spelling (ENV NODE_ENV=production in 13 of 35 Dockerfiles, NODE_VERSION, Node, NODEJS) is now DENIED like its lowercase twin; KS-930 round-3 F-QA-1) — Ornith ornith:35b (Q4_K_M) PASS 7/7 on r2 RE-CHECK, BASH_PATCH, tip develop M55 48e65c435 (G6 override verified against origin 0b25f823f), run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-16_ks958-ornith35b-night2 (recheck/)
# Source read by me (Wednesday): the APPLIED script is BYTE-IDENTICAL to a sed golden (tolower on :338 and :342, nothing else — `cmp`); the two product `+` lines are the brief's byte-for-byte; `nodeish_hit` still keeps the RAW line for the message (untouched, correct). The model's suite (84 lines): the reference's helpers verbatim (`expect`, `row_case`, the four path lines, the tail) + six `row_case` cells = the ticket's own table — rows 1–4 (NODE_ENV / NODE_VERSION / Node / NODEJS) red at the tip for the predicted reason (rc 0 EXEMPT vs expected 1), CONTROL lowercase node_env DENIED on both trees, CONTROL boundary `/srv/NODES /srv/ANODE` EXEMPT on both trees; after: 6/6 green; B6 both sibling suites (the 1,228-line reference suite included) no new failure. Accommodations named in the verdict: section_1 REANCHORED on the '-' LINES (the model's leading context line was a truncated copy of :332; header off by three); section_2 new-file header count RECOUNTED 75 -> 84 (the declared count would have applied 75 lines and dropped the last cell + the exit tail silently — r2's original FAIL B4 was this harness gap, retracted in done.md).
# PR NOTES for the Sunday raising seat: (1) TWO files: the two-line script change + the NEW suite scripts/__tests__/check_shared_relink_case.test.sh (reached by run-shell-suites.sh's glob — verify with --list); KS-958 → Done (its fix-shape is exactly this: `tolower(L)` before the two token tests; every token in both lists is already lowercase). (2) Do NOT bundle with KS-957 (the ticket says so: claims path vs behaviour gap). (3) The ticket's reachability note stands: every real class file writes node_modules in its final stage, so this arm is latent today — the PR body should say "latent, closed" not "live defect fixed". (4) The suite copies the reference's `expect`/`row_case` helpers rather than sourcing them — the reference has no source seam; a reviewer may ask for one (out of scope here).

```diff
--- a/Blockchain/Dev/scripts/check-shared-relink.sh
+++ b/Blockchain/Dev/scripts/check-shared-relink.sh
@@ -335,11 +335,11 @@
         # guard blocks every push touching Blockchain/Dev, so guessing is
         # expensive. Only the first is kept: it is the one to act on, and a list
         # would bury it.
-        if (L ~ /node_modules|npm|npx|yarn|pnpm/) {
+        if (tolower(L) ~ /node_modules|npm|npx|yarn|pnpm/) {
           nodeish[stage] = 1
           if (nodeish_hit[stage] == "") nodeish_hit[stage] = L
         }
-        else if (L ~ /(^|[^A-Za-z0-9_.-])(node|nodejs|bun|deno)([0-9._-]|[^A-Za-z0-9_.-]|$)/) {
+        else if (tolower(L) ~ /(^|[^A-Za-z0-9_.-])(node|nodejs|bun|deno)([0-9._-]|[^A-Za-z0-9_.-]|$)/) {
           nodeish[stage] = 1
           if (nodeish_hit[stage] == "") nodeish_hit[stage] = L
         }
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/check_shared_relink_case.test.sh
@@ -0,0 +1,84 @@
+# Unit tests for check-shared-relink.sh — KS-958: classifier matches runtime name case-insensitively.
+# The ticket's five-row table is the cell list; rows 1–4 are red at tip, rows 5–6 are controls.
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+GATE="$(cd "$HERE/.." && pwd)/check-shared-relink.sh"
+DEV_DIR="$(cd "$HERE/../.." && pwd)"
+REPO_ROOT="$(cd "$DEV_DIR/../.." && pwd)"
+
+PASS=0; FAIL=0; SKIP=0
+TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
+
+# expect <name> <expected_exit> <dockerfile-body> [expected_substring] [env-assignment]
+# The 4th argument pins the case to its own rule.
+expect() {
+    local name="$1" want="$2" body="$3" want_out="${4:-}" envset="${5:-}" d out got
+    d=$(mktemp -d "$TMP/case.XXXXXX")
+    mkdir -p "$d/services/thing"
+    printf '%s\n' "$body" > "$d/services/thing/Dockerfile"
+    if [ -n "$envset" ]; then
+        out=$(env "$envset" bash "$GATE" "$d" 2>&1); got=$?
+    else
+        out=$(bash "$GATE" "$d" 2>&1); got=$?
+    fi
+    if [ "$got" != "$want" ]; then
+        FAIL=$((FAIL+1)); echo "  FAIL: $name (expected exit $want, got $got)"; echo "$out" | sed 's/^/        /'; return
+    fi
+    if [ -n "$want_out" ] && ! printf '%s' "$out" | grep -qF -- "$want_out"; then
+        FAIL=$((FAIL+1)); echo "  FAIL: $name (exit correct, WRONG rule fired — wanted /$want_out/)"; echo "$out" | sed 's/^/        /'; return
+    fi
+    PASS=$((PASS+1))
+}
+
+ok() { PASS=$((PASS+1)); }
+bad() { FAIL=$((FAIL+1)); echo "  FAIL: $1"; }
+
+echo "check_shared_relink_case:"
+
+row_case() {  # row_case <name> <expected_rc> <final stage lines> <arm substring>
+    expect "$1" "$2" "FROM node:24-alpine AS shared-builder
+WORKDIR /shared
+RUN npm ci --ignore-scripts
+FROM node:24-alpine AS builder
+WORKDIR /app
+RUN npm ci && npm run build
+$3
+COPY --from=shared-builder /shared /shared" "$4"
+}
+
+NODEISH_MSG="names a JavaScript runtime or its tooling"
+
+row_case "KS-958 row 1: ENV NODE_ENV=production is DENIED (was A_EXEMPT — the uppercase spelling in 13 of 35 Dockerfiles)" 1 \
+  'FROM alpine:3.20
+ENV NODE_ENV=production
+CMD ["/bin/sh"]' "$NODEISH_MSG"
+
+row_case "KS-958 row 2: ENV NODE_VERSION=22 is DENIED" 1 \
+  'FROM alpine:3.20
+ENV NODE_VERSION=22
+CMD ["/bin/sh"]' "$NODEISH_MSG"
+
+row_case "KS-958 row 3: RUN echo Node is DENIED — mixed case" 1 \
+  'FROM alpine:3.20
+RUN echo Node
+CMD ["/bin/sh"]' "$NODEISH_MSG"
+
+row_case "KS-958 row 4: RUN echo NODEJS is DENIED — uppercase" 1 \
+  'FROM alpine:3.20
+RUN echo NODEJS
+CMD ["/bin/sh"]' "$NODEISH_MSG"
+
+row_case "KS-958 CONTROL: ENV node_env=production was already DENIED — only the case differs" 1 \
+  'FROM alpine:3.20
+ENV node_env=production
+CMD ["/bin/sh"]' "$NODEISH_MSG"
+
+row_case "KS-958 boundary: uppercase words CONTAINING node are still NOT a match" 0 \
+  'FROM alpine:3.20
+RUN mkdir -p /srv/NODES /srv/ANODE
+CMD ["/bin/sh"]' "the re-link invariant does not apply"
+
+echo "  $PASS passed, $FAIL failed, $SKIP skipped"
+[ "$FAIL" -eq 0 ] || exit 1
+exit 0
```
