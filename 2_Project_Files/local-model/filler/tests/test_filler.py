#!/usr/bin/env python3
"""Red-proofs for the filler CHECKERS: planted bad Spark output must be REJECTED, clean output ACCEPTED. No Spark, no network.
run: python3 -I tests/test_filler.py  (from any dir: paths are absolute)"""
import json, os, sys, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, F)
import filler_lib as L

SRC = open(os.path.join(F, "inputs/src/pr2209/password.ts"), encoding="utf-8").read()
REL = "Blockchain/Dev/services/auth/src/services/password.ts"
LINES = SRC.split("\n")
SCR = os.path.join(F, "runs", "_test_scratch")


def diff(old, new, ctx_before=(), ctx_after=(), start=None, path=REL):
    n = start
    body = ["--- a/%s" % path, "+++ b/%s" % path,
            "@@ -%d,%d +%d,%d @@" % (n, len(ctx_before) + 1 + len(ctx_after), n, len(ctx_before) + 1 + len(ctx_after))]
    body += [" " + c for c in ctx_before] + ["-" + old, "+" + new] + [" " + c for c in ctx_after]
    return "```diff\n" + "\n".join(body) + "\n```\n"


L178 = LINES[177]
GOOD = diff(L178, L178.replace("> 0", ">= 0"), LINES[175:177], LINES[178:180], 176)


class Mutants(unittest.TestCase):
    def chk(self, out, lo=174, hi=179, seen=None):
        return L.check_mutant(out, SRC, REL, lo, hi, SCR, seen if seen is not None else set())

    def test_clean_accepted(self):
        r = self.chk(GOOD)
        self.assertTrue(r["accepted"], r)
        self.assertEqual(r["changed"], [178, 178])

    def test_zero_context_accepted_and_wrong_removed_line_rejected(self):
        z = "```diff\n--- a/%s\n+++ b/%s\n@@ -178,1 +178,1 @@\n-%s\n+%s\n```\n" % (REL, REL, L178, L178.replace("> 0", ">= 0"))
        r = self.chk(z); self.assertTrue(r["accepted"], r); self.assertEqual(r["applied_via"], "u0")
        z2 = z.replace("-" + L178, "-" + L178.replace("Number", "Numbr"))
        r2 = self.chk(z2); self.assertFalse(r2["accepted"]); self.assertIn("refused", r2["reason"])

    def test_does_not_apply_rejected(self):
        bad = diff(L178.replace("Number", "Numbr"), L178.replace("> 0", ">= 0"), LINES[175:177], LINES[178:180], 176)
        r = self.chk(bad)
        self.assertFalse(r["accepted"]); self.assertIn("refused", r["reason"])

    def test_wrong_context_rejected(self):
        bad = diff(L178, L178.replace("> 0", ">= 0"), ["// not the real context", LINES[176]], LINES[178:180], 176)
        r = self.chk(bad)
        self.assertFalse(r["accepted"]); self.assertIn("refused", r["reason"])

    def test_comment_only_rejected(self):
        c = LINES[176]
        r = self.chk(diff(c, c + " (edited comment)", LINES[175:176], LINES[177:179], 176))
        self.assertFalse(r["accepted"]); self.assertIn("comment/whitespace", r["reason"])

    def test_whitespace_only_rejected(self):
        r = self.chk(diff(L178, L178.replace("&&", "&&  "), LINES[175:177], LINES[178:180], 176))
        self.assertFalse(r["accepted"]); self.assertIn("comment/whitespace", r["reason"])

    def test_outside_range_rejected(self):
        l = LINES[158]  # line 159, the function signature
        r = self.chk(diff(l, l.replace("password", "pw", 1), LINES[156:158], LINES[159:161], 157))
        self.assertFalse(r["accepted"]); self.assertIn("outside the target range", r["reason"])

    def test_wrong_path_rejected(self):
        r = self.chk(GOOD.replace(REL, "some/other/file.ts"))
        self.assertFalse(r["accepted"]); self.assertIn("wrong path", r["reason"])

    def test_two_hunks_rejected(self):
        two = GOOD.replace("\n```\n", "\n@@ -1,1 +1,1 @@\n-x\n+y\n```\n")
        r = self.chk(two)
        self.assertFalse(r["accepted"]); self.assertIn("hunks", r["reason"])

    def test_prose_rejected(self):
        r = self.chk("I would change the > to >= on line 178.")
        self.assertFalse(r["accepted"])

    def test_duplicate_rejected(self):
        seen = set()
        a = self.chk(GOOD, seen=seen); seen.add(a["result_hash"])
        b = self.chk(GOOD, seen=seen)
        self.assertTrue(a["accepted"]); self.assertFalse(b["accepted"]); self.assertIn("duplicate", b["reason"])


MAIL = open(os.path.join(F, "inputs/mail/pr2209_ready_r107.txt"), encoding="utf-8").read()
META = json.load(open(os.path.join(F, "inputs/pr2209.meta.json")))
FILES = json.load(open(os.path.join(F, "inputs/pr2209.files.json")))
CLEAN = {"pr": 2209, "files_changed": 2, "additions": 68, "deletions": 2,
         "files": [{"path": "services/auth/src/services/password.ts", "additions": 3, "deletions": 2},
                   {"path": "ks2021-hibp-range-match-needs-a-count-above-zero.test.ts", "additions": 65, "deletions": None}]}


class Numstat(unittest.TestCase):
    def chk(self, claim, mail=MAIL):
        return L.check_numstat(claim, mail, META, FILES, 2209)

    def test_clean_match(self):
        c = dict(CLEAN, files_changed=None)  # the mail states "files" only as two named paths; total files not claimed as a number
        r = self.chk(c); self.assertEqual(r["verdict"], "MATCH", r)

    def test_wrong_number_not_in_mail_rejected(self):
        r = self.chk(dict(CLEAN, files_changed=None, additions=69))
        self.assertEqual(r["verdict"], "REJECTED_UNGROUNDED"); self.assertTrue(any("69" in g for g in r["grounding"]))

    def test_invented_path_rejected(self):
        r = self.chk({"pr": 2209, "files_changed": None, "additions": None, "deletions": None,
                      "files": [{"path": "services/auth/src/routes/auth.ts", "additions": 3, "deletions": 2}]})
        self.assertEqual(r["verdict"], "REJECTED_UNGROUNDED")

    def test_seat_claim_wrong_vs_api_flagged(self):
        mail = MAIL.replace("+68/-2", "+69/-2")  # a seat that mis-states the PR: the faithful extraction must be FLAGGED
        r = self.chk(dict(CLEAN, files_changed=None, additions=69, files=[]), mail)
        self.assertEqual(r["verdict"], "MISMATCH"); self.assertIn("mail says 69, API says 68", r["mismatches"][0])

    def test_wrong_pr_rejected(self):
        r = self.chk(dict(CLEAN, pr=2208)); self.assertEqual(r["verdict"], "REJECTED_UNGROUNDED")

    def test_no_claims(self):
        r = self.chk({"pr": 2209, "files_changed": None, "additions": None, "deletions": None, "files": []})
        self.assertEqual(r["verdict"], "NO_CLAIMS")

    def test_descriptor_path_resolved_by_counts_and_wrong_count_flagged(self):
        c = {"pr": 2209, "files_changed": None, "additions": None, "deletions": None,
             "files": [{"path": "password.ts", "additions": 3, "deletions": 2}, {"path": "new test", "additions": 65, "deletions": None}]}
        r = self.chk(c); self.assertEqual(r["verdict"], "MATCH", r)
        mail = MAIL.replace(".test.ts +65", ".test.ts +66")
        c["files"][1]["additions"] = 66
        r = self.chk(c, mail); self.assertEqual(r["verdict"], "MISMATCH", r)

    def test_string_number_rejected(self):
        r = self.chk(dict(CLEAN, additions="68")); self.assertEqual(r["verdict"], "REJECTED_UNGROUNDED")


if __name__ == "__main__":
    unittest.main(verbosity=2)
