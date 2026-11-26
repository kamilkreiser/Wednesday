# QA-POLICY-WORDS: properties (a) ls-tree, (i) protected sha256 / prefixes / fn counts / SHAPE_RIGHT, (e) docs phrases
import subprocess, hashlib, re, sys
C = "/private/tmp/claude-501/qpw/clone"
B, H, P184 = "2004a04ebba7e1d031dfa341da26f76693345aff", "821cae22525785e0771f0d2deb7bed4b24b2a4af", "184b35ef17cf9865c4f9b20c721f9647233f8b98"
def g(*a): return subprocess.run(["git", "-C", C, *a], capture_output=True, check=True).stdout
def show(sha, p): return g("show", f"{sha}:{p}")
def lstree(sha, p):
    out = {}
    for l in g("ls-tree", "-r", sha, p).decode().splitlines():
        meta, path = l.split("\t"); out[path] = meta.split()[2]
    return out
print("== (a) ls-tree src")
for a, b in [(B, H), (P184, H)]:
    x, y = lstree(a, "crates/coagent-policy/src"), lstree(b, "crates/coagent-policy/src")
    diff = sorted(k for k in set(x) | set(y) if x.get(k) != y.get(k))
    print(f"{a[:7]} vs {b[:7]}: entries {len(x)}/{len(y)}; differing: {diff}")
for p in ["crates/coagent-policy/Cargo.toml", "crates/coagent-policy/red-controls.sh", "Cargo.toml", "Cargo.lock"]:
    print(p, lstree(B, p)[p][:12], lstree(H, p)[p][:12], "EQUAL" if lstree(B, p) == lstree(H, p) else "DIFF")
print("== (i) protected sha256")
TABLE = {
"q01_gate_attacks.rs":"368fe3eea6426af4e4550bc25d3cfdacde921ea65b0cb591efbe1aa745451550",
"r2_gate_attacks.rs":"2169c25ac8b057b5acdddc1c404b394bc81bc4bdb00b5e02b3552bbba50ab50d",
"r3_gate_attacks.rs":"2e3f799ed40ab505597d8df9f8ac587b6402612738fa144a297f26ad32a3f71f",
"r4_gate_attacks.rs":"89b48198c8b1758d8ab947a216937c606fc46ee0579cb5c85bd0d1f5085a02cf",
"r5b_bound_probe.rs":"05be31e0d9f426236eff245d660faa2021f634d03e074135da22d21c2ea44ab8",
"r5b_r4_regressions.rs":"e845c11b50a5ccd617549be1728b141619703d223cb30b7bee588ba08b75203f",
"r5b_shell_t3.rs":"b4425d8b1b0e6306106b1071da03953a39a8121381934a3682e517868e1fbddd",
"qa_strict.rs":"75b80cad8f671e9b1c5263b4f77113d5550a7b0a48ebab4e972f763bf2dc7f6b",
"qa_strict_m2/qa_strict.rs":"694d07c672b3dde3ebd6f7675d9a48168b72924b4d19cca86e6db56cd584bfb3",
"qa_strict_m2/common/mod.rs":"1670356301cfdaed77bbc67114645de68aed5440348d9fee66f50f02d1338c4c",
"common/mod.rs":"e4b20635c03ebebd578dae741c64d58825e51536d8b607859b55fd8599f3fc59",
"bypass_common/mod.rs":"043477832f4ad1c9720251487eef8b3c757ed6e16b65175eebad84861c5178e1",
"t21_bypass_refusals.rs":"ee597d751ffd8d45b99041b3240a0aa7de1392c1e1d9bca630b32f74906ef25f",
"t12_docs.rs":"359f9ef6d9b07c408496cc8fb275e7b1dadfa881821887dcec0b1c111dcfc17d",
"t26_owner_property.rs":"bd765aeb852df9550d814fa5493a24a0d83627b6c9c6c03b0330fad786b1db4e",
"t17_addendum5.rs":"07184587c3ae7428030efb077fc8dab976db2ae11c6185b0dfa824f4718e151a",
"owner_common/mod.rs":"106fdddcbacb2c480a49cb8d466be700a7ef1d4d5e2c7b1fbd1761317a3022db"}
bad = 0
for f, want in TABLE.items():
    hb = hashlib.sha256(show(B, "crates/coagent-policy/tests/" + f)).hexdigest()
    hh = hashlib.sha256(show(H, "crates/coagent-policy/tests/" + f)).hexdigest()
    ok = hb == want == hh; bad += not ok
    print(f"{'OK ' if ok else 'BAD'} {f} {hh[:12]}")
print("mismatches", bad, "| empty-input hash in table:", hashlib.sha256(b"").hexdigest() in TABLE.values())
ctl = hashlib.sha256(show(B, "crates/coagent-policy/tests/t28_at_names.rs")).hexdigest(), hashlib.sha256(show(H, "crates/coagent-policy/tests/t28_at_names.rs")).hexdigest()
print("control t28 base/head:", ctl[0][:12], ctl[1][:12], "differ" if ctl[0] != ctl[1] else "SAME")
print("== (i) byte prefixes")
for p in ["BACKLOG.md", "docs/M0-OUTCOMES.md"]:
    b, h = show(B, p), show(H, p)
    print(p, "lines", b.count(b"\n"), h.count(b"\n"), "prefix" if h.startswith(b) else "NOT PREFIX", "bytes added", len(h) - len(b))
print("== (i) #[test] counts and removed assert lines")
for f in ["t25_owner_allow.rs", "t27_owner_dark.rs", "t28_at_names.rs"]:
    p = "crates/coagent-policy/tests/" + f
    print(f, "#[test]", show(B, p).count(b"#[test]"), show(H, p).count(b"#[test]"), "fn", len(re.findall(rb"\nfn |\n\s*fn ", show(B, p))), len(re.findall(rb"\nfn |\n\s*fn ", show(H, p))))
d = g("diff", B, H, "--", "crates/coagent-policy/tests").decode()
rem = [l for l in d.splitlines() if l.startswith("-") and not l.startswith("---")]
print("removed test lines:", len(rem)); [print("   ", l) for l in rem]
print("removed lines holding assert:", sum("assert" in l for l in rem))
print("== (i) SHAPE_RIGHT")
def arr(src, name):
    m = re.search(name + r": \[&str; (\d+)\] = \[(.*?)\];", src, re.S)
    return int(m.group(1)), re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(2))
for sha in (B, H):
    print(sha[:7], arr(show(sha, "crates/coagent-policy/tests/t28_at_names.rs").decode(), "SHAPE_RIGHT"))
nb, ab = arr(show(B, "crates/coagent-policy/tests/t28_at_names.rs").decode(), "SHAPE_RIGHT")
nh, ah = arr(show(H, "crates/coagent-policy/tests/t28_at_names.rs").decode(), "SHAPE_RIGHT")
print("len", len(ab), len(ah), "differing positions (1-based):", [(i + 1, ab[i], ah[i]) for i in range(len(ab)) if ab[i] != ah[i]])
print("== (i) POLICY.md removed lines")
d = g("diff", "-U0", B, H, "--", "docs/POLICY.md").decode()
[print("   ", l) for l in d.splitlines() if l.startswith(("-", "@@")) and not l.startswith("---")]
