# Applies the re-check's mutants of the RR-1 fix / RR-2 (each in its own worktree). Usage: mutants.py <name> <engine.rs>
import sys, re
name, f = sys.argv[1], sys.argv[2]
s = open(f).read()
INV_START = "        // RR-1 (addendum 5, form (b)): the peer's end is APPLIED before this command can reuse\n"
JOIN_START = "        // RR-1 (addendum 5, form (b)): as at the start of `cmd_invite`.\n"
INV_END = "        if self.session_active() {\n            return Response::err(\n                id,\n                code::SESSION_ACTIVE,"
JOIN_END = "        let parsed = invite::parse(blob)\n"
def cut(s, a, b):
    i = s.index(a); j = s.index(b, i)
    assert s.count(a) == 1
    return s[:i] + s[j:]
INNER = """            if has_target {
                log!("the peer's end was applied before this command");
                if let Some(s) = self.sess.as_mut() {
                    s.rec.ended = true;
                }
                self.end_session("ended by the peer").await;
            }
"""
if name == "mi":      # remove the block from cmd_invite only
    s = cut(s, INV_START, INV_END)
elif name == "mj":    # remove the block from cmd_join only
    s = cut(s, JOIN_START, JOIN_END)
elif name == "mn":    # set ended_cleaned without calling end_session (both blocks; the tick untouched)
    assert s.count(INNER) == 2, s.count(INNER)
    s = s.replace(INNER, "            let _ = has_target;\n")
elif name == "m2":    # RR-2 mutant m2: with the setting on, use the identity although the save failed
    old = """                    self.relay_refused = Some(t.clone());
                    return Err(t);
                }
                log!(
                    "relay identity: a new one ({}), saved in relay-identity.key","""
    assert s.count(old) == 1
    s = s.replace(old, """                    let _ = t;
                }
                log!(
                    "relay identity: a new one ({}), saved in relay-identity.key",""")
else:
    raise SystemExit("unknown mutant " + name)
open(f, "w").write(s)
print("mutated", name, f)
