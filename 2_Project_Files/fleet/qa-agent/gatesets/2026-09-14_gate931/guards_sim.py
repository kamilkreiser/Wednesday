#!/usr/bin/env python3
"""guards_sim.py — READ-ONLY simulation of the ks1061-shared-mock-completeness.test.ts guard
(ROOT_MOCK / VIA_HELPER regexes, copied verbatim from the file at HEAD — see model/ks1061-shared-mock-completeness.test.ts.head)
against real file content read with `git show <ref>:<path>` (a read verb) on the read-only Secuura
checkout. NO JEST IS RUN — this is a prediction the gate itself must confirm by actually running
`npx jest src/__tests__/ks1061-shared-mock-completeness.test.ts`. Every count below is
predicted-by: drafter.

Four things simulated:
  1. Census at four refs (develop's declared merge-base dfc63fe48/M23, the PR's pre-merge tip
     f2e0cb3c1, the PR HEAD 53b8a1f7a, and develop's LIVE tip at this drafter's read).
  2. The RED-FIRST state: the synthetic tree at the merge commit 3da9623fe (develop merged in,
     BEFORE the fold commit 53b8a1f7a) — built in-memory from the saved model/ files: the ten
     already-converted suites keep their PR-side (post-merge == premerge, the merge changes
     nothing in them) content, ks444 takes its HEAD (resolved-at-merge) content, and ks1103/ks764
     take their PRE-FOLD (devbase, i.e. develop's hand-written factory) content — because the merge
     commit brings them in unconverted and only the LAST commit (the fold) converts them.
  3. Four tampers (T1..T4) against the HEAD state, predicting the guard's reaction to each.
  4. The whole-suite root-factory count HEAD vs develop-tip, for the "12 at develop / 2 folded"
     claim in the PR body and the builder's READY mail.
"""
import subprocess, re, sys, os

REPO = "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files"
DIR = "Blockchain/Dev/services/originate/src/__tests__"

ROOT_MOCK = re.compile(r"jest\.mock\(\s*'@secuura/shared'\s*,")
VIA_HELPER = re.compile(r"jest\.mock\(\s*'@secuura/shared'\s*,\s*\(\)\s*=>\s*\n?\s*require\('\./helpers/sharedModuleMock'\)\.makeSharedMock\(")

def sh(*args):
    r = subprocess.run(["git", "-C", REPO] + list(args), capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr

def ls_tree(ref, path):
    rc, out, err = sh("ls-tree", "--name-only", ref, path + "/")
    if rc != 0:
        return []
    return [l.split("/")[-1] for l in out.splitlines() if l.endswith(".test.ts")]

def show(ref, path):
    rc, out, err = sh("show", f"{ref}:{path}")
    if rc != 0:
        return None
    return out

def census(ref, label):
    files = sorted(ls_tree(ref, DIR))
    total = 0
    offenders = []
    per_file = {}
    for f in files:
        src = show(ref, f"{DIR}/{f}")
        if src is None:
            continue
        declared = len(ROOT_MOCK.findall(src))
        via = len(VIA_HELPER.findall(src))
        if declared:
            per_file[f] = (declared, via)
            total += declared
            if declared != via:
                offenders.append(f"{f} ({declared} factories, {via} via helper)")
    print(f"--- {label} (ref {ref[:12]}) --- {len(files)} .test.ts files, {len(per_file)} with a root factory, totalFactories={total}")
    for f, (d, v) in sorted(per_file.items()):
        flag = "" if d == v else "  <== OFFENDER"
        print(f"    {f}: declared={d} via_helper={v}{flag}")
    print(f"    offenders: {offenders if offenders else '[]'}")
    return total, offenders, per_file

MODEL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model")

def read_model(name):
    p = os.path.join(MODEL, name)
    with open(p, "r", encoding="utf-8") as fh:
        return fh.read()

def census_text(per_file_text, label):
    total = 0
    offenders = []
    report = {}
    for fname, src in per_file_text.items():
        declared = len(ROOT_MOCK.findall(src))
        via = len(VIA_HELPER.findall(src))
        if declared:
            report[fname] = (declared, via)
            total += declared
            if declared != via:
                offenders.append(f"{fname} ({declared} factories, {via} via helper)")
    print(f"--- {label} --- {len(per_file_text)} files considered, {len(report)} with a root factory, totalFactories={total}")
    for f, (d, v) in sorted(report.items()):
        flag = "" if d == v else "  <== OFFENDER"
        print(f"    {f}: declared={d} via_helper={v}{flag}")
    ok = "3 / 3 (guard GREEN)" if total >= 10 and not offenders else f"{len(offenders)} failed / {len(report) - len(offenders)} passed / {len(report)} total (guard RED)"
    print(f"    offenders: {offenders if offenders else '[]'}  ->  predicted jest result: {ok}")
    print(f"    predicted-by: drafter")
    return total, offenders

TWELVE = ["gdprService.erasure.test.ts", "ks1103-verify-hash-field.test.ts",
          "ks444-webhooks-create-description-guard.test.ts", "ks445-pg-error-classification.test.ts",
          "ks563-certified-vs-anchored.test.ts", "ks584-p3-auth-error-classification.test.ts",
          "ks584-p3-verify-list.test.ts", "ks584-verify-row-selection.test.ts",
          "ks695-erasure-by-external-ref.test.ts", "ks764-admin-api-keys-revoke-route-contract.test.ts",
          "ks914-deliver-webhook-blocked-vs-failed.test.ts", "qa-f4-resolveonbehalfof-org-normalisation.test.ts"]

if __name__ == "__main__":
    refs = [
        ("dfc63fe48ebaa97271f3ff66315a742ba4d79bc2", "develop @ PR's ORIGINAL declared merge-base (M23, dfc63fe48) [SUPERSEDED pin]"),
        ("f2e0cb3c125d117b1c9f8157bad28399f16b5e8e", "PR's pre-merge tip (f2e0cb3c1) [unchanged by the re-pin]"),
        ("53b8a1f7a6056c1560af71252c753c005bee8f06", "PR HEAD, round-1 ORIGINAL [SUPERSEDED — do not gate]"),
        ("7953070230d285fdebc0c65b834ac8340c02c0b6", "PR HEAD, RE-PINNED (795307023 — the ks695 union merge-in of M31) [GATE THIS ONE]"),
        ("b9f541e6b158f831576ecc870244f361f219a114", "develop @ the RE-PINNED merge-base (M31, b9f541e6b, contains #985's squash)"),
    ]
    for ref, label in refs:
        census(ref, label)
        print()

    print("=" * 100)
    print("SIMULATED RED-FIRST: the merge commit 3da9623fe (develop merged in, BEFORE the fold commit)")
    print("Built in-memory: the 10 already-converted suites @ HEAD/premerge (unchanged by the merge);")
    print("ks444 @ HEAD (resolved during the merge itself); ks1103+ks764 @ devbase (NOT yet folded).")
    per_file = {}
    for f in TWELVE:
        if f in ("ks1103-verify-hash-field.test.ts", "ks764-admin-api-keys-revoke-route-contract.test.ts"):
            per_file[f] = read_model(f"{f}.devbase")  # unfolded — develop's hand-written factory
        else:
            per_file[f] = read_model(f"{f}.head")
    total, offenders = census_text(per_file, "SIMULATED red-first (merge commit, pre-fold)")
    exp_offenders = ["ks1103-verify-hash-field.test.ts (1 factories, 0 via helper)",
                      "ks764-admin-api-keys-revoke-route-contract.test.ts (1 factories, 0 via helper)"]
    match = sorted(offenders) == sorted(exp_offenders) and total == 12
    print(f"    MATCHES builder's claimed red-first (offenders=[ks1103,ks764], totalFactories=12, '1 failed / 2 passed / 3 total'): {match}")
    print()

    print("=" * 100)
    print("SIMULATED HEAD (post-fold) — must read GREEN, 12/12, 0 offenders")
    per_file = {f: read_model(f"{f}.head") for f in TWELVE}
    total, offenders = census_text(per_file, "SIMULATED HEAD (post-fold)")
    print(f"    MATCHES expected green (0 offenders, totalFactories=12): {total == 12 and offenders == []}")
    print()

    print("=" * 100)
    print("TAMPERS T1..T4 against HEAD state (anchor uniqueness asserted by controls_check.sh, not here)")
    base = {f: read_model(f"{f}.head") for f in TWELVE}

    # T1: revert ks764 fold to devbase (unfolded) text
    t1 = dict(base); t1["ks764-admin-api-keys-revoke-route-contract.test.ts"] = read_model("ks764-admin-api-keys-revoke-route-contract.test.ts.devbase")
    total, offenders = census_text(t1, "T1: ks764 fold reverted")
    print(f"    T1 predicted: offenders==['ks764...'] only: {offenders == ['ks764-admin-api-keys-revoke-route-contract.test.ts (1 factories, 0 via helper)']}")
    print()

    # T2: revert ks1103 fold to devbase (unfolded) text
    t2 = dict(base); t2["ks1103-verify-hash-field.test.ts"] = read_model("ks1103-verify-hash-field.test.ts.devbase")
    total, offenders = census_text(t2, "T2: ks1103 fold reverted")
    print(f"    T2 predicted: offenders==['ks1103...'] only: {offenders == ['ks1103-verify-hash-field.test.ts (1 factories, 0 via helper)']}")
    print()

    # T3: delete the assertSafeOutboundUrl override line from ks444 (guard's own regex is blind to
    # this — T3 is a SECOND guard, the ks444 suite's own assertions, not ks1061's; simulated here only
    # to show the completeness guard does NOT catch it (still green), which is the point T3 makes.
    ks444 = base["ks444-webhooks-create-description-guard.test.ts"]
    t3_line = "    assertSafeOutboundUrl: jest.fn(async (raw: unknown) => ({ ok: true as const, url: String(raw) })),\n"
    assert ks444.count(t3_line) == 1, "T3 anchor not unique in ks444 @ HEAD — refuses"
    t3 = dict(base); t3["ks444-webhooks-create-description-guard.test.ts"] = ks444.replace(t3_line, "", 1)
    total, offenders = census_text(t3, "T3: assertSafeOutboundUrl override deleted from ks444")
    print(f"    T3 predicted: completeness guard STAYS GREEN (0 offenders) — the regex only counts factories, not their keys: {offenders == []}")
    print(f"    T3's real effect is on ks444's OWN suite (both 201 cells -> Received: 500), asserted by controls_check.sh's byte-diff, not by this guard.")
    print()

    # T4: inert comment inserted into the guard file itself
    guard_src = read_model("ks1061-shared-mock-completeness.test.ts.head")
    marker = "describe('KS-1061"
    assert guard_src.count(marker) == 1, "T4 anchor not unique in the guard file"
    t4_guard = guard_src.replace(marker, "// inert tamper comment\n" + marker, 1)
    open(os.path.join(MODEL, "_t4_guard.tmp"), "w", encoding="utf-8").write(t4_guard)
    print(f"T4: inert comment landed in the guard file (byte count +{len(t4_guard) - len(guard_src)}); the guard's OWN two other `it()` blocks")
    print(f"    (export-surface equality, override/throw behaviour) are unaffected by a comment — predicted 3/3 STILL GREEN.")
    print(f"    predicted-by: drafter")
