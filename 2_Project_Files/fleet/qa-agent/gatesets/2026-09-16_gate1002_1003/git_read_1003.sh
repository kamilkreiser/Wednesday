#!/bin/bash
# READ-ONLY git reads (show / diff / rev-parse / ls-remote / for-each-ref / merge-base) against the Secuura checkout for
# #1003 in the #1002+#1003 drafter set. No write verb, no checkout, no fetch. Usage: git_read_1003.sh <gateset dir>
set -u
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
G="${1:?gateset dir}"
B2=80686962828197acf305e4010a2ed5b401285743
H2=a376756aba1e1ae32c49ed47ba057fd80c7ed136
B3=5b4f38a48aeb40c2295895aaa5cd08e273aa7a08
H3=c5488a6891e6ac6fe950c101196d8c33ab8e173f
AG=Blockchain/Dev/services/api-gateway
IDX=$AG/src/index.ts
CSRF=$AG/src/middleware/csrf.ts
COMP=$AG/src/__tests__/ks1165-api-gateway-csrf-excludedpaths-carries-no.test.ts
NEW=$AG/src/__tests__/ks1165-real-app-csrf-mount-order.test.ts
echo "read at $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "porcelain $(git -C "$R" --no-optional-locks status --porcelain | wc -l | tr -d ' ') config_sha $(shasum -a 256 "$R/.git/config" | cut -d' ' -f1) for_each_ref $(git -C "$R" for-each-ref | wc -l | tr -d ' ')"
git -C "$R" ls-remote origin refs/heads/develop refs/heads/feature/ks-1123-ornith-verify-status-pins refs/heads/feature/ks-1165-f1-real-app-mount-cell
echo "## #1003 base..head raw + numstat (whole tree)"
git -C "$R" diff --raw --no-renames "$B3" "$H3"
git -C "$R" diff --numstat --no-renames "$B3" "$H3"
echo "parents of H3: $(git -C "$R" rev-parse "$H3^@" | tr '\n' ' ')"
echo "merge-base H3 develop: $(git -C "$R" merge-base "$H3" "$B3")"
echo "## #1002 vs #1003 file sets (from their own bases)"
git -C "$R" diff --name-only "$B2" "$H2" | sort > "$G/files_1002.txt"
git -C "$R" diff --name-only "$B3" "$H3" | sort > "$G/files_1003.txt"
echo "shared: $(comm -12 "$G/files_1002.txt" "$G/files_1003.txt" | wc -l | tr -d ' ')  (1002: $(wc -l < "$G/files_1002.txt" | tr -d ' '), 1003: $(wc -l < "$G/files_1003.txt" | tr -d ' '))"
echo "merge-base H2 H3: $(git -C "$R" merge-base "$H2" "$H3")"
echo "## blobs: index.ts / csrf.ts / composed / new at B2 H2 B3 H3"
for f in "$IDX" "$CSRF" "$COMP" "$NEW" "$AG/src/routes/verification.ts"; do
  line=""
  for c in "$B2" "$H2" "$B3" "$H3"; do
    b="$(git -C "$R" rev-parse --verify --quiet "$c:$f" 2>/dev/null)"; line="$line ${c:0:9}=${b:0:9}"; [ -z "$b" ] && line="${line}ABSENT"
  done
  echo "$line  ${f#$AG/}"
done
git -C "$R" show "$H3:$IDX" > "$G/index.h3.ts"
git -C "$R" show "$H3:$CSRF" > "$G/csrf.h3.ts"
git -C "$R" show "$B3:$COMP" > "$G/composed.base.ts"
git -C "$R" show "$H3:$COMP" > "$G/composed.head.ts"
echo "## tamper anchors at H3 (fixed strings, multi-line via python)"
python3 - "$G/index.h3.ts" "$G/csrf.h3.ts" <<'PYA'
import sys
idx = open(sys.argv[1], encoding="utf-8").read(); csrf = open(sys.argv[2], encoding="utf-8").read()
A = [
 ("index", "T3/T5s anchor: if (NODE_ENV !== 'test') {\\n  app.use(csrfMiddleware.generateToken);", "if (NODE_ENV !== 'test') {\n  app.use(csrfMiddleware.generateToken);"),
 ("index", "bare: if (NODE_ENV !== 'test') {", "if (NODE_ENV !== 'test') {"),
 ("index", "T4 pair 1: generateToken + protect + close", "  app.use(csrfMiddleware.generateToken);\n  app.use(csrfMiddleware.protect);\n}\n"),
 ("index", "T4 pair 2: app.use(enforceJsonContentType);\\n", "app.use(enforceJsonContentType);\n"),
 ("index", "app.use(csrfMiddleware.protect)", "app.use(csrfMiddleware.protect)"),
 ("index", "app.use(cookieParser", "app.use(cookieParser"),
 ("csrf", "T1: the v2 comment + entry (two lines)", "    // KS-1165: the v2 twins are published anonymous (security: []) like v1 — same exclusion, same startsWith rule.\n    '/api/v2/verification/verify',\n"),
 ("csrf", "T1 entry line only", "    '/api/v2/verification/verify',\n"),
 ("csrf", "gate1001 T5: startsWith", "config.excludedPaths.some(path => req.path.startsWith(path))"),
]
for which, label, a in A:
    s = idx if which == "index" else csrf
    n = s.count(a)
    ln = [i + 1 for i in range(len(s)) if s.startswith(a, i)] if n else []
    lines = [s.count("\n", 0, i - 1) + 1 for i in ln]
    print(f"{which:5} count={n} lines={lines}  <{label}>")
PYA
echo "-- context index.ts around the CSRF block"
/usr/bin/grep -n -i -E "cookieParser|csrfMiddleware|enforceJsonContentType\)|NODE_ENV !== 'test'|export default" "$G/index.h3.ts"
echo "## real-app file: expectations census"
git -C "$R" show "$H3:$NEW" | /usr/bin/grep -n -E "^\s*it\(|toBe\(|toEqual\(" | cut -c1-160
echo "## composed file cell count at H3: $(/usr/bin/grep -c -E "^\s*it\(" "$G/composed.head.ts")"
echo "## api-gateway test file counts: B3 $(git -C "$R" ls-tree -r --name-only "$B3" -- "$AG/src/__tests__" | /usr/bin/grep -c -E '\.test\.ts$')  H3 $(git -C "$R" ls-tree -r --name-only "$H3" -- "$AG/src/__tests__" | /usr/bin/grep -c -E '\.test\.ts$')  H2 $(git -C "$R" ls-tree -r --name-only "$H2" -- "$AG/src/__tests__" | /usr/bin/grep -c -E '\.test\.ts$')  B2 $(git -C "$R" ls-tree -r --name-only "$B2" -- "$AG/src/__tests__" | /usr/bin/grep -c -E '\.test\.ts$')"
echo "porcelain $(git -C "$R" --no-optional-locks status --porcelain | wc -l | tr -d ' ') config_sha $(shasum -a 256 "$R/.git/config" | cut -d' ' -f1) for_each_ref $(git -C "$R" for-each-ref | wc -l | tr -d ' ')"
echo "done at $(date '+%H:%M:%S %Z')"
