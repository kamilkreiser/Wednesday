# B2143 ADDENDUM-1 (from Tuesday, written before the stamp; binds seat N184; name it in ADDENDA READ)

Two changes to the kit `2026-11-27_B2143_SEAT-N184_nexusai-lane3-kit1.md`. Nothing else changes.

## 1. Commit B's message: use msg-B2.txt, not msg-B.txt
The frozen `msg-B.txt` says "Each of fourteen mutations of the change turns the cells named for it red." Only ten of the kit's fourteen mutations are RD-1015's (b05 to b14). b01 to b04 are RD-1016's, and commit A's message already counts them as four. Committed text must not overclaim.
- Use `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s333/d2143/frozen-addendum1/msg-B2.txt` instead: sha256 `1ed9e9b1864134b3613fa5ff5090b5b6b6b26f922b19ce6cd8e61f6166a95f84`, 1451 bytes.
- Its only difference from `msg-B.txt` is "fourteen" -> "ten" in that one sentence (Tuesday's `diff` printed exactly one changed line).
- At Step 0, copy it into `.tools/b2143/frozen/` and print its sha256 beside the table's. Pass it to `static2143.py ... B` and to `git commit -F` in place of `msg-B.txt`.
- `msg-B.txt` stays in your frozen folder unused.

## 2. The ban-list names for every static2143.py call: extract them with the frozen names2142.py
- Run `python3 -I -B '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s332/d2142/frozen/names2142.py' '/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/session-tools/b1375/scanlib1114.py' '/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/.tools/b2143/raw/names.txt'`.
- Check before you run it: sha256 `b0ae957362523cfe6999f1ac4146dcf3dddd9e44a75a670b769b66c73d112c43`. Read it, do not copy it.
- It must print `names 4 found [True, True, True, True]`, rc 0. Never print the file.
- Pass the four names to `static2143.py` as four arguments, read from that file by a program that does not print them.
- **Never use round 1's `fleet/state/s331/d2133/names4.txt`.** The B2142 drafter measured that it holds two of the four names with a stray leading `b`, so a scan over it would read a false 0 on those two names.
