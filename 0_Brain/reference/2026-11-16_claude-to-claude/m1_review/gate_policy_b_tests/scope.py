# QA-POLICY-B item 1: scope and engine-change checks by program (git read verbs only). usage: python3 -B scope.py <repo>
import subprocess, sys, hashlib
R = sys.argv[1]; B = "5cab5e42df6cb3db05f3d38c7ba973beafd044b2"; H = "cd7b6fdd1a4b2de5937795b052a68d793146eb6d"
def g(*a, raw=False):
    out = subprocess.run(["git", "-C", R] + list(a), capture_output=True, check=True).stdout
    return out if raw else out.decode()
OWNED = ["BACKLOG.md", "crates/coagent-policy/Cargo.toml", "crates/coagent-policy/red-controls.sh",
         "crates/coagent-policy/src/action.rs", "crates/coagent-policy/src/shell/mod.rs",
         "crates/coagent-policy/tests/t25_owner_allow.rs", "crates/coagent-policy/tests/t27_owner_dark.rs",
         "crates/coagent-policy/tests/t28_at_names.rs", "crates/coagent-policy/tests/t29_free_text.rs",
         "docs/M0-OUTCOMES.md", "docs/POLICY.md"]
names = g("diff", "--name-only", f"{B}...{H}").split()
print("1a changed paths:", len(names), "equal to the 11 owned:", sorted(names) == sorted(OWNED))
ex = [f":(exclude){p}" for p in OWNED]
n0 = len(g("diff", B, H, "--", ".", *ex, raw=True))
n1 = len(g("diff", B, H, "--", ".", *ex[1:], raw=True))
print(f"1b bytes of diff outside the 11: {n0}; control (BACKLOG.md let back in): {n1}")
def tree(sha, path):
    d = {}
    for l in g("ls-tree", "-r", sha, "--", path).splitlines():
        meta, p = l.split("\t"); d[p] = meta.split()[2]
    return d
tb, th = tree(B, "crates/coagent-policy/src"), tree(H, "crates/coagent-policy/src")
diff = sorted(p for p in set(tb) | set(th) if tb.get(p) != th.get(p))
print(f"1c src entries base {len(tb)} head {len(th)}; differing: {diff}")
for p in diff: print("   ", p, tb.get(p, "-")[:7], "->", th.get(p, "-")[:7])
tc = tree("184b35e", "crates/coagent-policy/src")
print("   control 184b35e vs base differing:", sorted(p for p in set(tc) | set(tb) if tc.get(p) != tb.get(p)))
for p in ["crates/coagent-policy/src/engine.rs", "Cargo.lock", "Cargo.toml", "rust-toolchain.toml"]:
    a = g("rev-parse", f"{B}:{p}").strip(); b = g("rev-parse", f"{H}:{p}").strip()
    print(f"1d {p}: base {a[:12]} head {b[:12]} equal {a == b}")
for p in ["crates/coagent-policy/Cargo.toml", "crates/coagent-policy/red-controls.sh"]:
    d = g("diff", "-U0", B, H, "--", p).splitlines()
    add = [l for l in d if l.startswith("+") and not l.startswith("+++")]
    rem = [l for l in d if l.startswith("-") and not l.startswith("---")]
    print(f"1e {p}: added {len(add)} removed {len(rem)}")
    for l in add: print("     ", l[:200])
lib = g("show", f"{H}:crates/coagent-policy/src/lib.rs")
print("1f forbid(unsafe_code) in lib.rs:", "#![forbid(unsafe_code)]" in lib)
dd = g("diff", "-U0", B, H)
addl = [l for l in dd.splitlines() if l.startswith("+") and not l.startswith("+++")]
print("   added lines containing 'unsafe':", [l[:120] for l in addl if "unsafe" in l])
TABLE = {
 "q01_gate_attacks.rs": "368fe3eea6426af4e4550bc25d3cfdacde921ea65b0cb591efbe1aa745451550",
 "r2_gate_attacks.rs": "2169c25ac8b057b5acdddc1c404b394bc81bc4bdb00b5e02b3552bbba50ab50d",
 "r3_gate_attacks.rs": "2e3f799ed40ab505597d8df9f8ac587b6402612738fa144a297f26ad32a3f71f",
 "r4_gate_attacks.rs": "89b48198c8b1758d8ab947a216937c606fc46ee0579cb5c85bd0d1f5085a02cf",
 "r5b_bound_probe.rs": "05be31e0d9f426236eff245d660faa2021f634d03e074135da22d21c2ea44ab8",
 "r5b_r4_regressions.rs": "e845c11b50a5ccd617549be1728b141619703d223cb30b7bee588ba08b75203f",
 "r5b_shell_t3.rs": "b4425d8b1b0e6306106b1071da03953a39a8121381934a3682e517868e1fbddd",
 "qa_strict.rs": "75b80cad8f671e9b1c5263b4f77113d5550a7b0a48ebab4e972f763bf2dc7f6b",
 "qa_strict_m2/qa_strict.rs": "694d07c672b3dde3ebd6f7675d9a48168b72924b4d19cca86e6db56cd584bfb3",
 "qa_strict_m2/common/mod.rs": "1670356301cfdaed77bbc67114645de68aed5440348d9fee66f50f02d1338c4c",
 "common/mod.rs": "e4b20635c03ebebd578dae741c64d58825e51536d8b607859b55fd8599f3fc59",
 "bypass_common/mod.rs": "043477832f4ad1c9720251487eef8b3c757ed6e16b65175eebad84861c5178e1",
 "t21_bypass_refusals.rs": "ee597d751ffd8d45b99041b3240a0aa7de1392c1e1d9bca630b32f74906ef25f",
 "t12_docs.rs": "359f9ef6d9b07c408496cc8fb275e7b1dadfa881821887dcec0b1c111dcfc17d",
 "t26_owner_property.rs": "bd765aeb852df9550d814fa5493a24a0d83627b6c9c6c03b0330fad786b1db4e",
 "t17_addendum5.rs": "07184587c3ae7428030efb077fc8dab976db2ae11c6185b0dfa824f4718e151a",
 "owner_common/mod.rs": "106fdddcbacb2c480a49cb8d466be700a7ef1d4d5e2c7b1fbd1761317a3022db"}
bad = 0
for f, want in TABLE.items():
    for sha in (B, H):
        got = hashlib.sha256(g("show", f"{sha}:crates/coagent-policy/tests/{f}", raw=True)).hexdigest()
        if got != want: bad += 1; print("   MISMATCH", f, sha[:7], got[:16])
empty = hashlib.sha256(b"").hexdigest()
ctl = hashlib.sha256(g("show", f"{H}:crates/coagent-policy/tests/t28_at_names.rs", raw=True)).hexdigest()
print(f"1g protected files: {len(TABLE)} x 2 SHAs, mismatches {bad}; control empty-input hash {empty[:12]} in table: {empty in TABLE.values()}; control t28 at head {ctl[:12]} in table: {ctl in TABLE.values()}")
for p in ["BACKLOG.md", "docs/M0-OUTCOMES.md", "docs/POLICY.md"]:
    a = g("show", f"{B}:{p}", raw=True); b = g("show", f"{H}:{p}", raw=True)
    print(f"1h {p}: base {len(a)} B, head {len(b)} B, base a byte prefix of head: {b.startswith(a)}" + ("  (control)" if p.endswith("POLICY.md") else ""))
tdiff = g("diff", "-U0", B, H, "--", "crates/coagent-policy/tests").splitlines()
remfn = [l for l in tdiff if l.startswith("-") and not l.startswith("---") and "fn " in l]
print("1i removed test lines holding 'fn ':", remfn)
print("1j git diff 821cae2 5cab5e4 -- crates/coagent-policy | wc -c ->", len(g("diff", "821cae2", B, "--", "crates/coagent-policy", raw=True)),
      "; control 184b35e..5cab5e4 ->", len(g("diff", "184b35e", B, "--", "crates/coagent-policy", raw=True)))
for cid in ["general-c2c-policy-web-fetch-prompt-1126", "general-c2c-policy-long-text-names-1126", "general-c2c-allow-terminal-change-delete-send-1125"]:
    r = subprocess.run(["git", "-C", R, "grep", "-c", "-F", cid, H], capture_output=True).stdout.decode().strip()
    print(f"1k card id {cid}: files at head: {r.splitlines() if r else 0}")
print("   added lines naming a card id:", [l[:100] for l in addl if "general-c2c-" in l])
