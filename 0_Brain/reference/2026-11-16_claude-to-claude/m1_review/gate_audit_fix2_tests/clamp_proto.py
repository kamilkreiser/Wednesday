#!/usr/bin/env python3
"""Prototype of a crate-side close of the resume-defaults state (QA check, D(2)): the cap of
`try_set_limits` also keeps every part of the own seat at or below the defaults' (an offer whose
records are lower than the default records may not raise the own seat's bytes above the default
own seat's bytes). Applied to the WORK tree only; `restore` puts the pristine files back.
Usage: clamp_proto.py <area> apply|restore"""
import os, sys, shutil

AREA, MODE = sys.argv[1], sys.argv[2]
WORK = os.path.join(AREA, "work/crates/coagent-audit")
SRC = os.path.join(WORK, "src/session.rs")
TST = os.path.join(WORK, "tests/fix_qam1_seat.rs")
BAK = os.path.join(AREA, "clamp_bak")

if MODE == "restore":
    shutil.copy(os.path.join(BAK, "session.rs"), SRC)
    shutil.copy(os.path.join(BAK, "fix_qam1_seat.rs"), TST)
    sys.exit(0)

os.makedirs(BAK, exist_ok=True)
shutil.copy(SRC, os.path.join(BAK, "session.rs"))
shutil.copy(TST, os.path.join(BAK, "fix_qam1_seat.rs"))

s = open(SRC).read()
old = """            let d = StoreLimits::default();
            StoreLimits {
                bytes: limits.bytes.min(d.bytes),
                records: limits.records.min(d.records),
            }
        };"""
new = """            let d = StoreLimits::default();
            let mut n = StoreLimits {
                bytes: limits.bytes.min(d.bytes),
                records: limits.records.min(d.records),
            };
            // QA PROTOTYPE: no part of the own seat above the defaults' (own seat bytes are a
            // seat less one byte per record, so fewer records would otherwise give more bytes)
            let (db, dr) = d.per_peer();
            let max_pp = db - dr + n.per_peer().1;
            if n.per_peer().0 > max_pp {
                n.bytes = max_pp * SEATS;
            }
            n
        };"""
assert s.count(old) == 1
open(SRC, "w").write(s.replace(old, new))

t = open(TST).read()
old_c = """    let d = StoreLimits::default();
    StoreLimits {
        bytes: l.bytes.min(d.bytes),
        records: l.records.min(d.records),
    }
}"""
new_c = """    let d = StoreLimits::default();
    let mut n = StoreLimits {
        bytes: l.bytes.min(d.bytes),
        records: l.records.min(d.records),
    };
    let (db, dr) = d.per_peer();
    let max_pp = db - dr + n.per_peer().1;
    if n.per_peer().0 > max_pp {
        n.bytes = max_pp * 8;
    }
    n
}"""
assert t.count(old_c) == 1
t = t.replace(old_c, new_c)
# the carve-out switched OFF: the property is strict again (any resume-defaults state fails)
old_r = "    let d = StoreLimits::default();\n    // (i)\n"
new_r = "    let d = StoreLimits::default();\n    if std::env::var(\"QA_STRICT\").is_ok() {\n        return Err(\"QA prototype: carve-out off\".into());\n    }\n    // (i)\n"
assert t.count(old_r) == 1
t = t.replace(old_r, new_r)
open(TST, "w").write(t)
print("applied")
