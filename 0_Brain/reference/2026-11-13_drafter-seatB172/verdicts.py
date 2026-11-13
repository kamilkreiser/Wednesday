R="/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/"
rows=[
(2098,"2026-11-09_gate264-tier2-t15-batch","PR 2093: GO WITH NOTES; PR 2094: GO WITH NOTES; PR 2097: GO; PR 2098: GO","943b69fdd988"),
(2097,"2026-11-09_gate264-tier2-t15-batch","PR 2093: GO WITH NOTES; PR 2094: GO WITH NOTES; PR 2097: GO; PR 2098: GO","ebf1ed1d0869"),
(2096,"2026-11-09_gate265-tier2-pr2095-pr2096","PR 2095: GO; PR 2096: GO","85785a9f3663"),
(2095,"2026-11-09_gate265-tier2-pr2095-pr2096","PR 2095: GO; PR 2096: GO","90e8ee1d8f93"),
(2090,"2026-11-07_gate252-tier2-batch","| 2090 | KS-692 | 4c4f696f7699 | GO |","4c4f696f7699"),
(2089,"2026-11-07_gate252-tier2-batch","| 2089 | KS-1493 | 3796e4b90c6a | GO |","3796e4b90c6a"),
(2079,"2026-11-13_gate345-pr2079","PR 2079: GO WITH NOTES (at head 0fffdfba0f9578f23d48112068d1451ea947cd29; tier 1)","0fffdfba0f95"),
(2220,"2026-11-13_gate346-tier2-pr2220-2221","PR 2220: GO WITH NOTES (at head ab5a7e119cc8ef3740750504f8631d4031c5f9dd; tier 2)","ab5a7e119cc8"),
(2221,"2026-11-13_gate346-tier2-pr2220-2221","PR 2221: GO WITH NOTES (at head 32a9bf0fb2d329453e417a76d92af6ab429f3148; tier 2)","32a9bf0fb2d3"),
(2222,"2026-11-13_gate347-tier2-pr2222-2223","PR 2222: GO WITH NOTES (at head 39035798163ab367857602c14d830c2225d9680b; tier 2)","39035798163a"),
(2223,"2026-11-13_gate347-tier2-pr2222-2223","PR 2223: GO (at head 8752357228cdc9650b5b7cc5f2383b61a8fdb7d8; tier 2)","8752357228cd"),
(2224,"2026-11-13_gate348-tier1-pr2224-2225","PR 2224: GO WITH NOTES (at head a160347eab6655cccac7882bc6933372a475716e; tier 1)","a160347eab66"),
(2224,"2026-11-13_gate348-tier1-pr2224-2225","NEGATIVE CONTROL nonsense line PR 2224: NO GO","a160347eab66"),
]
for n,f,line,h in rows:
    t=open(R+f+"/verdict.md",encoding="utf-8",errors="replace").read()
    ls=t.split("\n")
    idx=[i+1 for i,l in enumerate(ls) if line in l]
    print(n,f.split("_")[1][:7],"line present:",bool(idx),"at file line",idx[:2],"head12 in file:",h in t)
