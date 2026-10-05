#!/bin/bash
# code_patch2_arms.sh — arms for the multi-file tier (tasks/code_patch2/) and its lint gate (2026-10-05).
#
# A synthetic 2-product jest service is built in a SCRATCH git repo (never under !CODING): src/a.ts (add() subtracts)
# and src/b.ts (twice() adds 1), an existing test src/__tests__/existing.test.ts (a sorted manifest), a reference test.
# The golden fixes BOTH products, appends the new test's name to the manifest, and adds src/__tests__/fix.test.ts
# (R1/R2 red at the tip by assertion, C1 green). node_modules: one symlink to spark/cache/src's (itself a symlink to
# the Secuura checkout's) — read only.
#   C1 PASS      the golden                                         -> rc 0, RESULT: PASS (7/7)
#   C2 FAIL      golden + an UNDECLARED src/c.ts section            -> rc 1, A3 ... UNDECLARED
#   C3 FAIL      golden minus b.ts (declared, UNTOUCHED)            -> rc 1, A3 ... UNTOUCHED
#   C4 FAIL      the red cells are GREEN before the product hunks   -> rc 1, A4 ... NOT red before the product sections
#   C5 FAIL      a.ts re-adds a line its tip already has             -> rc 1, A3d names a.ts (per-product A3d still fires)
#   L1 REFUSE    a header saying NOT RUNNABLE                       -> brief_lint rc 2
#   L2 REFUSE    a 2-product header on tier code_patch              -> brief_lint rc 2, CONTRACT
#   L3 ACCEPT    KS-1278 with tier=code_patch2 + override_not_runnable (the control for L1/L2)
set -uo pipefail
SPARK="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; LM="$(dirname "$SPARK")"
CHK="$LM/tasks/code_patch2/checker.sh"
NM="$SPARK/cache/src/Blockchain/Dev/node_modules"
T="${SPARK_TEST_TMP:-$(mktemp -d "${TMPDIR:-/tmp}/cp2_arms.XXXXXX")}"; mkdir -p "$T"
P=0; F=0
ok()  { echo "ARM PASS $*"; P=$((P+1)); }
bad() { echo "ARM FAIL $*"; F=$((F+1)); }
[ -e "$NM/jest" ] || { echo "code_patch2_arms: no jest under $NM (run a round once to seed the cache)"; exit 2; }
echo "code_patch2_arms: fixtures in $T"

# ---------------------------------------------------------------- the synthetic repo
SYN="$T/syn"; S="$SYN/Blockchain/Dev/services/demo"
mkdir -p "$S/src/__tests__"
git -C "$T" init -q syn
cat > "$S/package.json" <<'E'
{ "name": "demo", "private": true, "scripts": { "test": "jest" }, "devDependencies": { "jest": "*", "ts-jest": "*" } }
E
cat > "$S/jest.config.js" <<'E'
module.exports = { preset: 'ts-jest', testEnvironment: 'node', roots: ['<rootDir>/src'], testMatch: ['**/__tests__/**/*.test.ts'] };
E
cat > "$S/tsconfig.json" <<'E'
{ "compilerOptions": { "target": "ES2022", "module": "commonjs", "strict": true, "esModuleInterop": true, "skipLibCheck": true, "types": ["node", "jest"], "rootDir": "./src", "outDir": "./dist" },
  "include": ["src/**/*"], "exclude": ["node_modules", "dist", "src/__tests__"] }
E
printf 'export function add(x: number, y: number): number {\n  return x - y;\n}\n' > "$S/src/a.ts"
printf 'export function twice(n: number): number {\n  return n + 1;\n}\n' > "$S/src/b.ts"
printf "export const NAME = 'demo';\n" > "$S/src/c.ts"
printf "const KNOWN = [\n  'existing.test.ts',\n];\n\ndescribe('existing', () => {\n  it('control EX C1: the manifest is sorted', () => {\n    expect([...KNOWN].sort()).toEqual(KNOWN);\n  });\n});\n" > "$S/src/__tests__/existing.test.ts"
printf "import { add } from '../a';\n\ndescribe('ref', () => {\n  it('control REF: add is a function', () => {\n    expect(typeof add).toBe('function');\n  });\n});\n" > "$S/src/__tests__/ref.test.ts"
git -C "$SYN" add -A && git -C "$SYN" -c user.name=arms -c user.email=arms@local commit -q -m "synthetic tip"
TIP="$(git -C "$SYN" rev-parse HEAD)"

D="Blockchain/Dev/services/demo/src"
mkdiff() { # mkdiff <out.md> <variant: golden|undeclared|untouched|greenbefore>
  python3 - "$1" "$2" "$D" <<'PY'
import sys
out, v, D = sys.argv[1:4]
a = f"""--- a/{D}/a.ts
+++ b/{D}/a.ts
@@ -1,3 +1,3 @@
 export function add(x: number, y: number): number {{
-  return x - y;
+  return x + y;
 }}
"""
b = f"""--- a/{D}/b.ts
+++ b/{D}/b.ts
@@ -1,3 +1,3 @@
 export function twice(n: number): number {{
-  return n + 1;
+  return n * 2;
 }}
"""
c = f"""--- a/{D}/c.ts
+++ b/{D}/c.ts
@@ -1,1 +1,1 @@
-export const NAME = 'demo';
+export const NAME = 'demo2';
"""
m = f"""--- a/{D}/__tests__/existing.test.ts
+++ b/{D}/__tests__/existing.test.ts
@@ -1,3 +1,4 @@
 const KNOWN = [
   'existing.test.ts',
+  'fix.test.ts',
 ];
"""
r1, r2 = ("expect(add(2, 3)).toBe(5);", "expect(twice(4)).toBe(8);") if v != "greenbefore" else ("expect(add(2, 0)).toBe(2);", "expect(twice(1)).toBe(2);")
body = ["import { add } from '../a';", "import { twice } from '../b';", "", "describe('code_patch2 synthetic', () => {",
        "  it('RED SYN R1: add adds', () => {", "    " + r1, "  });",
        "  it('RED SYN R2: twice doubles', () => {", "    " + r2, "  });",
        "  it('control SYN C1: add of zeros is zero', () => {", "    expect(add(0, 0)).toBe(0);", "  });", "});"]
n = "--- /dev/null\n+++ b/" + D + "/__tests__/fix.test.ts\n@@ -0,0 +1," + str(len(body)) + " @@\n" + "".join("+" + l + "\n" for l in body)
a_dup = a.replace("@@ -1,3 +1,3 @@", "@@ -1,3 +1,4 @@").replace("+  return x + y;\n", "+  return x + y;\n+export function add(x: number, y: number): number {\n")
parts = {"dupctx": [a_dup, b, m, n], "golden": [a, b, m, n], "undeclared": [a, b, c, m, n], "untouched": [a, m, n], "greenbefore": [a, b, m, n]}[v]
open(out, "w").write("```diff\n" + "".join(parts) + "```\n")
PY
}
mkinput() { # mkinput <input.json>
  python3 - "$1" "$TIP" "$D" "$SYN" <<'PY'
import json, sys
out, tip, D, syn = sys.argv[1:5]
sub = "Blockchain/Dev"
d = {"ticket": {"identifier": "KS-0", "title": "synthetic", "description": "synthetic code_patch2 arm (no brief text: A3i skips)"},
     "repo": {"source_checkout": syn, "tip": tip, "branch": "synthetic", "repo_subdir": sub, "service_dir": "services/demo",
              "shared_pkg_dir": "", "shared_pkg_name": "", "test_runner": "jest (npx jest)"},
     "tip": tip, "source_checkout": syn, "repo_subdir": sub, "service_dir": "services/demo", "shared_pkg_dir": "", "shared_pkg_name": "",
     "product_file": f"{D}/a.ts", "test_dir": f"{D}/__tests__", "reference_test_file": f"{D}/__tests__/ref.test.ts",
     "suggested_test_file": f"{D}/__tests__/fix.test.ts",
     "defect_line": {"line": 2, "text": "  return x - y;", "sites": [], "expected_plus": ["return x + y;", "return n * 2;", "'fix.test.ts',"],
                     "red_cells": ["RED SYN R1", "RED SYN R2"]},
     "files": {}, "task_type": "code_patch2",
     "product_files": [f"{D}/a.ts", f"{D}/b.ts"],
     "test_files": [{"path": f"{D}/__tests__/fix.test.ts", "status": "new"}, {"path": f"{D}/__tests__/existing.test.ts", "status": "modified"}]}
json.dump(d, open(out, "w"), indent=1)
PY
}
arm() { # arm <name> <variant> <want rc> <substring>
  local name="$1" v="$2" want="$3" sub="$4" W="$T/$1"
  mkdir -p "$W"; git clone -q "$SYN" "$W/clone"
  ln -s "$NM" "$W/clone/Blockchain/Dev/node_modules"; echo "/Blockchain/Dev/node_modules" >> "$W/clone/.git/info/exclude"
  mkinput "$W/input.json"; mkdiff "$W/out.md" "$v"
  bash "$CHK" "$W/input.json" "$W/out.md" "$W/clone" > "$W/checker.out" 2>&1; local rc=$?
  local res; res="$(grep -m1 '^RESULT:' "$W/checker.out")"
  local why; why="$(grep -E '^FAIL ' "$W/checker.out" | head -1 | cut -c1-200)"
  if [ "$rc" -eq "$want" ] && grep -qF -- "$sub" "$W/checker.out"; then ok "$name rc=$rc :: $res${why:+ :: $why}"
  else bad "$name rc=$rc (want $want, '$sub') :: $res :: $why (full: $W/checker.out)"; fi
}
arm C1-pass golden 0 "RESULT: PASS (7/7)"
grep -E '^(PASS|FAIL) A[0-9]' "$T/C1-pass/checker.out" | cut -c1-150 | sed 's/^/    C1: /'
arm C2-undeclared undeclared 1 "UNDECLARED"
arm C3-untouched untouched 1 "UNTOUCHED"
arm C4-green-before greenbefore 1 "NOT red before the product sections"
arm C5-a3d-per-product dupctx 1 "A3d CONTEXT MARKED AS ADDITION — '+' line(s) that already exist at a product's tip and are not in the brief: a.ts"

# ---------------------------------------------------------------- lint arms
BR="$LM/night/briefs/KS-1278-revoke-atomic"
mkdir -p "$T/L1" "$T/L2"
cp "$LM/night/briefs/KS-1345-list/KS-1345.md" "$T/L1/KS-1345.md"
python3 - "$T/L1/KS-1345.md" <<'PY'
import sys; p = sys.argv[1]; L = open(p).read().split("\n"); L.insert(7, "Routing: NOT RUNNABLE on today's checker (arm L1)"); open(p, "w").write("\n".join(L))
PY
cp "$BR/KS-1278.md" "$T/L2/KS-1278.md"
o="$(python3 "$SPARK/brief_lint.py" "$T/L1" 2>&1)"; r=$?
[ "$r" -eq 2 ] && echo "$o" | grep -q 'NOT RUNNABLE' && ok "L1 NOT RUNNABLE refused rc=2 :: $(echo "$o" | grep -m1 'NOT RUNNABLE' | cut -c1-140)" || bad "L1 rc=$r $o"
o="$(python3 "$SPARK/brief_lint.py" "$T/L2" tier=code_patch override_not_runnable=arm 2>&1)"; r=$?
[ "$r" -eq 2 ] && echo "$o" | grep -q 'CONTRACT' && ok "L2 2-product brief on code_patch refused rc=2 :: $(echo "$o" | grep -m1 CONTRACT | cut -c1-170)" || bad "L2 rc=$r $o"
o="$(python3 "$SPARK/brief_lint.py" "$BR" tier=code_patch2 override_not_runnable=arm 2>&1)"; r=$?
[ "$r" -eq 0 ] && echo "$o" | grep -q "B_TIER=code_patch2" && ok "L3 control: KS-1278 accepted on code_patch2 with the override" || bad "L3 rc=$r $o"
echo "code_patch2_arms: $P pass, $F fail (fixtures $T)"
[ "$F" -eq 0 ]
