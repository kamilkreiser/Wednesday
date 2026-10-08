import hashlib, os
S = "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/ba10491f-d904-4eb7-a83b-e46c1bc8cc8e/scratchpad/raise18"
OUT = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged"
part = open(S + "/src/common_partition.md").read().rstrip("\n")
tail = open(S + "/src/common_tail.md").read().rstrip("\n")
block = open(S + "/standing_block.md").read().rstrip("\n")
assert block.startswith("**The rule, extended") and "Test by its handle" in block
tail = tail.replace("@@STANDING_BLOCK@@", block)
tail = tail.replace("(STANDING_LINES `:17-47`)", "(STANDING_LINES `:17-46`)")
part = part.replace("`%@@PANE_R@@`", "`%<id at launch>`").replace("`%@@PANE_E@@`", "`%<id at launch>`") \
           .replace("`%@@PANE_G@@`", "`%<id at launch>`").replace("`%@@PANE_F@@`", "`%<id at launch>`")
OTHER_BOARD = ("No board exception in this seat. (R 18th alone makes ONE board change this round, KS-1450 -> Done + one "
               "comment: that is ITS event under the board guard, not yours.)")
seats = {
    "R": dict(file="2026-10-08_seatR18_raise_r2_r5_ks1450done.md", pane="Secuura/Blockchain-R", name="Seat R 18th",
              hk="R18", nxt="R 19th",
              board="**Exception, this seat only:** QUEUE B's ONE board write on KS-1450 (state -> Done + ONE comment), our own ticket closed by us (Kam 2026-10-08 10:45). Nothing else on the board.",
              fixes=[("140 lines, sha256/16 `9933eea0319606c9` per Wednesday's pickup, re-hash it", "139 lines by `wc -l`, sha256/16 `9933eea0319606c9`, drafter-hashed, matching Wednesday's pickup"),
                     ("R 17th handover read whole (140 lines;", "R 17th handover read whole (139 lines by `wc -l`, `9933eea0319606c9`;")]),
    "E": dict(file="2026-10-08_seatE11_raise_openapi_ks591_ks1364_ks1449.md", pane="Secuura/Blockchain-E", name="Seat E 11th",
              hk="E11", nxt="E 12th", board=OTHER_BOARD,
              fixes=[("(`:89-90`, `:126-127`; it exits 2)", "(`:83-84`, `:138-139`; it exits 2)"),
                     ("(STANDING_LINES `:412`, `:416`)", "(STANDING_LINES `:412`, `:414`)")]),
    "G": dict(file="2026-10-08_seatG4_raise_originate_ks593_ks1171.md", pane="Secuura/Blockchain-G", name="Seat G 4th",
              hk="G4", nxt="G 5th", board=OTHER_BOARD, fixes=[]),
    "F": dict(file="2026-10-08_seatF5_raise_scripts_ks808_ks1355_ks1328.md", pane="Secuura/Blockchain-F", name="Seat F 5th",
              hk="F5", nxt="F 6th", board=OTHER_BOARD,
              fixes=[("(via `trap4_f3.py`, whose `RF` is a REQUIRED `argv[2]` since F 4th: `:248-253`)", "(via `trap4_f3.py`, whose `RF` is a REQUIRED `argv[2]` since F 4th: §6)"),
                     ("(`pathgatef3.py` is fail-closed behind a round token: F 4th `:243-245`)", "(`pathgatef3.py` is fail-closed behind a round token: F 4th §6)"),
                     ("**F 4th kept generation `f3` filenames by design** (`:232-235`:", "**F 4th kept generation `f3` filenames by design** (§6:")]),
}
for k, c in seats.items():
    src = open(f"{S}/src/{k}.md").read()
    for a, b in c["fixes"]:
        assert src.count(a) == 1, (k, a)
        src = src.replace(a, b)
    t = tail.replace("@@PANE@@", c["pane"]).replace("@@SEATNAME@@", c["name"]).replace("@@HANDOVERKEY@@", c["hk"]) \
            .replace("@@NEXTSEAT@@", c["nxt"]).replace("@@BOARD_EXCEPTION@@", c["board"])
    assert src.count("## @@PARTITION@@") == 1 and src.count("@@COMMON_TAIL@@") == 1, k
    src = src.replace("## @@PARTITION@@", part).replace("@@COMMON_TAIL@@", t)
    left = [x for x in ("@@PARTITION", "@@COMMON", "@@STANDING", "@@PANE", "@@SEATNAME", "@@BOARD", "@@NEXTSEAT", "@@HANDOVERKEY") if x in src]
    assert not left, (k, left)
    assert block in src, k
    p = f"{OUT}/{c['file']}"
    assert not os.path.exists(p), p
    open(p, "w").write(src)
    b = src.encode()
    print(f"{p} | {len(b)} B | {src.count(chr(10))} lines | sha256/16 {hashlib.sha256(b).hexdigest()[:16]} | @FILL@ {src.count('@FILL@')} | SELF-CHECK lines {src.count('SELF-CHECK: re-read end-to-end for contradictions | @FILL@')}")
