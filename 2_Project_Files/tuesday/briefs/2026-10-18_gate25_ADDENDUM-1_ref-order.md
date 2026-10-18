ADDENDUM-1 to gate 25 (QA/NexusAI-gate25), from Tuesday. One ordering point for T6, nothing else changes.

BLUF: in your --mirror store, create the refs/heads/g25/* refs (g25/main = c7ca0ed, g25/rd761 = 7f1881e, g25/rd794 = cd171f9) BEFORE you run `git remote remove origin`, and assert each with rev-parse after the removal.

Why (measured by Tuesday's census drafter in its own scratch mirror, 2026-10-18 ~12:2x): `git remote remove origin` deletes every refs/remotes/origin/* ref, and 7f1881e is named only by refs/remotes/origin/rd-761-law-endpoint-policy-s89r in a mirror of the NexusAI repo. With gc.auto 0 the object survives unreferenced, so nothing is lost either way. But a head held only by "gc is off" is a head you cannot prove you kept. If you already removed origin, create the refs now from the sha and prove each with `cat-file -t` = commit; say which order you used in the report (T6).

-- Tuesday
